"""Model-free H0 source residence and deterministic envelope audit."""
from __future__ import annotations
import argparse, hashlib, json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Mapping
from .config import load_manifest
from .e3a_codex import build_replay
from .protocol import canonical_json_hash
from .workstream_e2 import _get_encoding
from .workstream_e3a import snapshot

STAGE = 7
LANGUAGES = ("csharp", "fsharp")

def sha256(value: bytes | str) -> str:
    return hashlib.sha256(value.encode("utf-8") if isinstance(value, str) else value).hexdigest()

def _definition(root: Path, path: str | Path) -> dict[str, Any]:
    p = Path(path) if Path(path).is_absolute() else root / path
    return json.loads(p.read_text(encoding="utf-8"))

def _text(root: Path, rel: str) -> str:
    return (root / rel).read_text(encoding="utf-8").replace("\r\n", "\n")

def _manifest(root: Path, definition: Mapping[str, Any]) -> Any:
    path = root / definition["manifest"]
    raw = json.loads(path.read_text(encoding="utf-8"))
    if canonical_json_hash(raw) != definition["manifest_sha256"]:
        raise ValueError("manifest identity does not match H0 definition")
    manifest = load_manifest(root, definition["manifest"])
    ids = [task["id"] for task in manifest["tasks"]]
    if ids[STAGE] != definition["task_id"] or ids[STAGE - 1] != definition["predecessor_task_id"]:
        raise ValueError("task/predecessor binding does not match H0 definition")
    return manifest

def source_for(root: Path, definition: Mapping[str, Any], language: str) -> dict[str, str]:
    if language not in LANGUAGES:
        raise ValueError("unsupported language")
    manifest = _manifest(root, definition)
    source = snapshot(root, manifest, language, STAGE)
    roles = definition["roles"].get(language, {})
    if set(roles) != set(definition["reference_roles"]): raise ValueError("role set mismatch")
    expected = {roles[r] for r in definition["reference_roles"]}
    if len(expected) != 3 or set(source) != expected: raise ValueError("source file set mismatch")
    if canonical_json_hash(source) != definition["source_sha256"][language]: raise ValueError("source identity mismatch")
    return {p: source[p].replace("\r\n", "\n") for p in expected}

def fixture_payload(root: Path, definition: Mapping[str, Any], language: str, source: Mapping[str, str], order: list[str], *, include_source: bool = True) -> dict[str, Any]:
    manifest = _manifest(root, definition)
    task = manifest["tasks"][STAGE]
    roles = definition["roles"][language]
    contracts = contract_payload(root, definition)
    if order not in definition["role_orders"] or set(order) != set(definition["reference_roles"]): raise ValueError("invalid role order")
    source_entries = [{"role": r, "filename": roles[r], "text": source[roles[r]], "sha256": sha256(source[roles[r]])} for r in order] if include_source else []
    return {**contracts,
            "source": source_entries,
            "context": {"language": language, "task_id": task["id"], "predecessor_task_id": manifest["tasks"][STAGE - 1]["id"], "source_access": "whole-file"}}

def contract_payload(root: Path, definition: Mapping[str, Any]) -> dict[str, Any]:
    manifest = _manifest(root, definition)
    payload = {
        "baseline_contract": _text(root, "protocols/workstream-e3a-v1/baseline-contract.md"),
        "earlier_contracts": [_text(root, t["prompt"]) for t in manifest["tasks"][:STAGE]],
        "current_task": _text(root, manifest["tasks"][STAGE]["prompt"]),
    }
    if "contracts_sha256" not in definition:
        raise ValueError("H0 definition is missing contracts_sha256")
    if canonical_json_hash(payload) != definition["contracts_sha256"]:
        raise ValueError("contract identity does not match H0 definition")
    return payload

def envelope(root: Path, definition: Mapping[str, Any], language: str, source: Mapping[str, str], order: list[str]) -> bytes:
    return build_replay("H0 fixture: inspect eligible whole-file source and preserve contracts.", [], fixture_payload(root, definition, language, source, order))

def empty_envelope(root: Path, definition: Mapping[str, Any], language: str, order: list[str]) -> bytes:
    return build_replay("H0 fixture: inspect eligible whole-file source and preserve contracts.", [], fixture_payload(root, definition, language, {}, order, include_source=False))

def _strict_nonnegative(value: Any, name: str) -> int:
    if type(value) is not int or value < 0: raise ValueError(f"{name} must be a non-negative integer")
    return value

def input_allowance(definition: Mapping[str, Any], *, convention: str = "joint") -> int:
    b = definition["synthetic_budget"]
    cap, reserve, safety = (
        _strict_nonnegative(b[k], k)
        for k in ("request_cap", "output_reserve", "safety_margin")
    )
    if convention not in {"joint", "input-only"}:
        raise ValueError("unknown synthetic accounting convention")
    value = cap - safety - (reserve if convention == "joint" else 0)
    if value < 0: raise ValueError("synthetic allowance is negative")
    return value

def source_allowance(definition: Mapping[str, Any], empty_source_bytes: int, *, convention: str = "joint") -> int:
    return max(0, input_allowance(definition, convention=convention) - _strict_nonnegative(empty_source_bytes, "empty_source_bytes"))

def default_renderer(mapping: Mapping[str, str]) -> bytes:
    return (json.dumps({"fixed_contracts": "H0", "retained_state": sorted(mapping), "wrappers": {"source": dict(sorted(mapping.items()))}}, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")

@dataclass(frozen=True)
class ReadResult:
    text: str | None
    returned: str
    charge_bytes: int
    identity: str

class SourceFixture:
    def __init__(self, eligible: Mapping[str, str], budget: int | None = None, *, render_resident: Callable[[Mapping[str, str]], bytes] = default_renderer, definition: Mapping[str, Any] | None = None, convention: str = "joint", cap: int | None = None, output_reserve: int = 0, safety_margin: int = 0):
        if convention not in {"joint", "input-only"}:
            raise ValueError("unknown synthetic accounting convention")
        if budget is not None:
            _strict_nonnegative(budget, "budget")
        self._eligible = dict(eligible)
        self._resident: dict[str, tuple[str, str]] = {}
        self._render = render_resident
        self._convention = convention
        if cap is not None:
            cap = _strict_nonnegative(cap, "cap")
            self._budget = cap - _strict_nonnegative(safety_margin, "safety_margin") - (_strict_nonnegative(output_reserve, "output_reserve") if convention == "joint" else 0)
            if self._budget < 0: raise ValueError("synthetic allowance is negative")
        else: self._budget = budget
        self._definition = definition
        self.exposure_bytes = 0
        self.unique_exposed: set[str] = set()
        self.unique_exposed_bytes = 0
        self.events: list[dict[str, Any]] = []
    def _check(self, path: str) -> str:
        if path not in self._eligible: raise KeyError(path)
        return self._eligible[path]
    def _allowance(self) -> int | None:
        if self._budget is not None: return self._budget
        return input_allowance(self._definition, convention=self._convention) if self._definition else None
    def assembled_request(self) -> bytes:
        return self._render({p: v[1] for p, v in self._resident.items()})
    def read(self, path: str) -> ReadResult:
        text = self._check(path)
        identity = f"{path}:{sha256(text)}"
        old = self._resident.get(path)
        reference = old is not None and old[0] == identity
        prospective = dict(self._resident)
        if not reference: prospective[path] = (identity, text)
        rendered = self._render({p: v[1] for p, v in prospective.items()})
        allowance = self._allowance()
        if allowance is not None and len(rendered) > allowance:
            self.events.append({"event": "refused", "path": path, "assembled_bytes": len(rendered)})
            raise ValueError("synthetic source budget exceeded")
        self._resident = prospective
        charge = 0 if reference else len(text.encode("utf-8"))
        if charge:
            self.exposure_bytes += charge
            if identity not in self.unique_exposed:
                self.unique_exposed.add(identity)
                self.unique_exposed_bytes += charge
        self.events.append({"event": "read", "path": path, "returned": "reference" if reference else "full", "bytes": charge})
        return ReadResult(None if reference else text, "reference" if reference else "full", charge, identity)
    def evict(self, path: str) -> None:
        self._resident.pop(path, None); self.events.append({"event": "evict", "path": path})
    def clear(self) -> None:
        self._resident.clear(); self.events.append({"event": "clear"})
    def update(self, path: str, text: str) -> None:
        self._check(path)
        if not isinstance(text, str): raise TypeError("source text must be a string")
        self._eligible[path] = text
        if self._resident.get(path, (None,))[0] != f"{path}:{sha256(text)}": self._resident.pop(path, None)
        self.events.append({"event": "update", "path": path, "sha256": sha256(text)})
    update_existing_path = update
    @property
    def resident_bytes(self) -> int: return sum(len(v[1].encode("utf-8")) for v in self._resident.values())
    @property
    def resident_paths(self) -> tuple[str, ...]: return tuple(sorted(self._resident))

def tokenize(data: bytes, encoder: Any | None = None) -> dict[str, Any]:
    ids = (encoder or _get_encoding()).encode(data.decode("utf-8"))
    return {
        "tokens": len(ids),
        "token_stream_sha256": sha256(
            json.dumps(ids, separators=(",", ":")).encode("ascii")
        ),
    }

def _assert_controls(definition: Mapping[str, Any]) -> dict[str, Any]:
    fixture = SourceFixture({"a.cs": "é", "b.cs": "xy"}, budget=256)
    first = fixture.read("a.cs")
    if not (first.returned == "full" and first.text == "é"):
        raise AssertionError("full read did not return Unicode source")
    reference = fixture.read("a.cs")
    if not (reference.returned == "reference" and reference.text is None and reference.charge_bytes == 0):
        raise AssertionError("reference read returned source bytes")
    if "é".encode("utf-8") not in fixture.assembled_request():
        raise AssertionError("resident text is absent from assembled request")
    fixture.evict("a.cs")
    if fixture.read("a.cs").returned != "full":
        raise AssertionError("evicted source was not reread fully")
    fixture.clear()
    if fixture.read("a.cs").returned != "full":
        raise AssertionError("cleared source was not reread fully")
    fixture.update("a.cs", "é")
    if fixture.read("a.cs").returned != "reference":
        raise AssertionError("unchanged update invalidated resident source")
    fixture.update("a.cs", "new")
    if fixture.read("a.cs").text != "new":
        raise AssertionError("changed update retained stale source")
    original = {"a": "x"}
    copied = SourceFixture(original)
    copied.update("a", "y")
    if original != {"a": "x"}:
        raise AssertionError("fixture mutated input mapping")
    repeated_cap = len(default_renderer({"a": "x"}))
    repeated = SourceFixture({"a": "x"}, budget=repeated_cap)
    for _ in range(repeated_cap + 1):
        if repeated.read("a").returned != "full":
            raise AssertionError("eviction-cycle full read failed")
        repeated.evict("a")
    if repeated.exposure_bytes <= repeated_cap:
        raise AssertionError("cumulative exposure did not exceed resident cap")
    if repeated.unique_exposed_bytes != 1 or repeated.resident_bytes != 0:
        raise AssertionError("eviction-cycle accounting is inconsistent")
    refused = SourceFixture({"a": "x", "oversized": "z" * 100}, budget=len(default_renderer({"a": "x"})))
    refused.read("a")
    before = (refused.resident_paths, refused.exposure_bytes, set(refused.unique_exposed), refused.assembled_request())
    try:
        refused.read("oversized")
    except ValueError:
        pass
    else:
        raise AssertionError("oversized new path was admitted")
    after = (refused.resident_paths, refused.exposure_bytes, set(refused.unique_exposed), refused.assembled_request())
    if before != after or refused.events[-1]["event"] != "refused":
        raise AssertionError("refusal mutated resident state or counters")
    exact = SourceFixture({"a": "x"}, budget=len(default_renderer({"a": "x"})))
    exact.read("a")
    over = SourceFixture({"a": "xx"}, budget=len(default_renderer({"a": "x"})))
    try:
        over.read("a")
    except ValueError:
        pass
    else:
        raise AssertionError("one-byte-over admission was accepted")
    try:
        SourceFixture({}, convention="bad")
        raise AssertionError("unknown convention accepted")
    except ValueError:
        pass
    try:
        SourceFixture({}, cap=True)
        raise AssertionError("boolean cap accepted")
    except ValueError:
        pass
    return {
        "scope": "synthetic-control-fixtures-only",
        "lifecycle": {
            "events": fixture.events,
            "resident_bytes": fixture.resident_bytes,
            "cumulative_exposed_bytes": fixture.exposure_bytes,
            "unique_exposed_bytes": fixture.unique_exposed_bytes,
            "current_assembled_bytes": len(fixture.assembled_request()),
        },
        "eviction_repetition": {
            "events": repeated.events,
            "resident_cap_bytes": repeated_cap,
            "resident_bytes": repeated.resident_bytes,
            "cumulative_exposed_bytes": repeated.exposure_bytes,
            "unique_exposed_bytes": repeated.unique_exposed_bytes,
        },
        "refusal": {
            "events": refused.events,
            "preserved_nonempty_state": True,
        },
        "boundary": {
            "empty_overhead": len(default_renderer({})),
            "exact_boundary_fit": len(exact.assembled_request()),
            "one_byte_over_refused": True,
            "unicode_utf8_bytes": len("é".encode("utf-8")),
        },
        "joint_allowance": input_allowance(definition),
        "input_only_allowance": input_allowance(definition, convention="input-only"),
    }

def audit(root: Path, definition_path: str | Path) -> dict[str, Any]:
    definition = _definition(root, definition_path)
    _manifest(root, definition)
    result = {
        "definition_sha256": canonical_json_hash(definition),
        "envelopes": [],
        "candidate_model_calls": 0,
        "provider_input": None,
        "physical_fit": None,
        "proxy_error_bound": None,
    }
    for language in LANGUAGES:
        source = source_for(root, definition, language)
        for order in definition["role_orders"]:
            data = envelope(root, definition, language, source, order)
            empty = empty_envelope(root, definition, language, order)
            full_source_bytes = sum(len(v.encode("utf-8")) for v in source.values())
            fits = {
                "joint": len(data) <= input_allowance(definition),
                "input-only": len(data) <= input_allowance(
                    definition, convention="input-only"
                ),
            }
            if not all(fits.values()):
                raise ValueError("H0 paired envelope exceeds the defined toy cap")
            result["envelopes"].append({"language": language, "order": order,
                "bytes": len(data), "sha256": sha256(data), "token_proxy": tokenize(data),
                "source_sha256": {p: sha256(v) for p, v in source.items()},
                "source_bytes": full_source_bytes,
                "eligible_source_files": len(source), "reference_source_files": len(source),
                "full_return_source_bytes": full_source_bytes, "resident_source_bytes": full_source_bytes,
                "empty_source_envelope_bytes": len(empty),
                "input_allowance": {"joint": input_allowance(definition), "input-only": input_allowance(definition, convention="input-only")},
                "source_allowance": {"joint": source_allowance(definition, len(empty)), "input-only": source_allowance(definition, len(empty), convention="input-only")},
                "synthetic_fit": fits})
    if len(result["envelopes"]) != 4:
        raise AssertionError("H0 audit did not produce four paired envelopes")
    result["controls"] = _assert_controls(definition)
    result["synthetic_budget"] = dict(definition["synthetic_budget"])
    result["token_proxy"] = {
        "package": "tiktoken",
        "version": "0.14.0",
        "encoding": "o200k_base",
        "rank_asset_sha256": definition["token_proxy"]["rank_asset_sha256"],
    }
    result["implementation_sha256"] = sha256(
        Path(__file__).read_text(encoding="utf-8").replace("\r\n", "\n")
    )
    result["definition_file_sha256"] = canonical_json_hash(definition); result["manifest_file_sha256"] = definition["manifest_sha256"]; return result

def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(); p.add_argument("--definition", default="protocols/workstream-h0/definition.json"); p.add_argument("--output-dir", required=True); a = p.parse_args(argv); root = Path(__file__).resolve().parents[2]; out = Path(a.output_dir); out.mkdir(parents=True, exist_ok=True); report = audit(root, a.definition); definition = _definition(root, a.definition)
    planned = []
    for item in report["envelopes"]:
        path = out / f"envelope-{item['language']}-{definition['role_orders'].index(item['order'])}.json"
        source = source_for(root, definition, item["language"])
        planned.append((path, envelope(root, definition, item["language"], source, item["order"])))
    rp = out / "report.json"
    planned.append((rp, (json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")))
    if any(path.exists() for path, _ in planned):
        raise FileExistsError(next(path for path, _ in planned if path.exists()))
    for path, content in planned:
        path.write_bytes(content)
    print(json.dumps({"envelopes": len(report["envelopes"]), "candidate_model_calls": 0}, sort_keys=True))
    return 0

if __name__ == "__main__": raise SystemExit(main())
