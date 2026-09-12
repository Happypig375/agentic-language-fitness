"""Bounded, trusted maintenance-simulation construction audit.

This module handles authored fixtures only.  It deliberately has no candidate,
model, authentication, or live-dispatch entry point.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Callable, Mapping

from .h_fixtures import credential_free_environment
from .h0 import tokenize
from .workstream_e2 import TOKENIZER_ENCODING, TOKENIZER_VERSION

LANGUAGES = ("csharp", "fsharp")
SDK = "10.0.302"
MAX_SOURCE_FILES = 16
MAX_SOURCE_BYTES = 131072
_EPISODE = re.compile(r"^(0[1-8])\.md$")
_SAFE = re.compile(r"^[A-Za-z0-9._-]+$")
_SOURCE_EXTENSIONS = {".cs", ".fs", ".csproj", ".fsproj", ".md"}
_FAULT_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


class MaintenanceFixtureError(ValueError):
    pass


def _strict_json_equal(left: Any, right: Any) -> bool:
    """JSON equality without Python's bool==int coercion."""
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return (left.keys() == right.keys() and
                all(_strict_json_equal(left[key], right[key]) for key in left))
    if isinstance(left, list):
        return len(left) == len(right) and all(_strict_json_equal(a, b) for a, b in zip(left, right))
    return left == right


def _read_lf(path: Path) -> str:
    data = path.read_bytes()
    if data.startswith(b"\xef\xbb\xbf") or data.startswith((b"\xff\xfe", b"\xfe\xff")):
        raise MaintenanceFixtureError(f"BOM/UTF-16 is not permitted: {path}")
    if b"\x00" in data or b"\r" in data:
        raise MaintenanceFixtureError(f"invalid non-LF or NUL bytes: {path}")
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise MaintenanceFixtureError(f"invalid UTF-8: {path}") from exc


def validate_layout(root: Path) -> dict[str, Any]:
    root = Path(root)
    base = root / "benchmarks" / "maintenance-sim"
    required = [base / "contract.md", base / "guidance" / "common.md"]
    required += [base / "guidance" / f"{x}.md" for x in LANGUAGES]
    required += [base / "episodes" / f"{i:02d}.md" for i in range(1, 9)]
    missing = [str(p.relative_to(root)) for p in required if not p.is_file()]
    if missing:
        raise MaintenanceFixtureError("missing maintenance fixture files: " + ", ".join(missing))
    for p in required:
        _read_lf(p)
    result: dict[str, Any] = {"base": str(base), "sdk": SDK, "languages": {}, "episodes": 8}
    for language in LANGUAGES:
        seed = base / "seed" / language
        reference = base / "reference" / language
        if not seed.is_dir() or not reference.is_dir():
            raise MaintenanceFixtureError(f"missing seed/reference fixture tree for {language}")
        entries = list(seed.iterdir())
        if any(p.is_symlink() or not p.is_file() for p in entries):
            raise MaintenanceFixtureError(f"seed must be flat and symlink-free for {language}")
        files = sorted(entries)
        if len(files) == 0 or len(files) > MAX_SOURCE_FILES:
            raise MaintenanceFixtureError(f"invalid source file count for {language}")
        if any(p.name != p.name.strip() or not _SAFE.fullmatch(p.name) or p.suffix.lower() not in _SOURCE_EXTENSIONS
               or p.name == "global.json" for p in files):
            raise MaintenanceFixtureError(f"unsafe source filename for {language}")
        project = "Simulation.csproj" if language == "csharp" else "Simulation.fsproj"
        if project not in {p.name for p in files}:
            raise MaintenanceFixtureError(f"missing {project} for {language}")
        total = 0
        for p in files:
            total += len(_read_lf(p).encode("utf-8"))
        if total > MAX_SOURCE_BYTES:
            raise MaintenanceFixtureError(f"source byte bound exceeded for {language}")
        patches = []
        for i in range(1, 9):
            p = reference / f"{i:02d}.patch"
            if p.is_symlink() or not p.is_file():
                raise MaintenanceFixtureError(f"missing reference patch: {p}")
            _read_lf(p)
            patches.append(p.name)
        result["languages"][language] = {"seed_files": [p.name for p in files],
                                          "source_bytes": total, "patches": patches}
    return result


def _source_map(workspace: Path) -> dict[str, str]:
    return {p.name: _read_lf(p) for p in workspace.iterdir() if p.is_file() and p.name != "global.json"}


def reconstruct(root: Path, language: str, checkpoint: int) -> dict[str, str]:
    """Apply reviewed patches in an owned temporary directory and return LF source."""
    if language not in LANGUAGES or not 0 <= checkpoint <= 8:
        raise MaintenanceFixtureError("invalid language or checkpoint")
    base = Path(root) / "benchmarks" / "maintenance-sim"
    for p in (base / "contract.md", base / "guidance" / "common.md",
              base / "guidance" / f"{language}.md"):
        if not p.is_file(): raise MaintenanceFixtureError(f"missing stage fixture: {p}")
    seed = base / "seed" / language
    if not seed.is_dir(): raise MaintenanceFixtureError(f"missing seed fixture tree for {language}")
    with tempfile.TemporaryDirectory(prefix="alf-maintenance-") as td:
        workspace = Path(td)
        entries = list(seed.iterdir())
        if any(p.is_dir() or p.is_symlink() for p in entries): raise MaintenanceFixtureError("seed must be flat and symlink-free")
        for p in entries:
            if (not _SAFE.fullmatch(p.name) or p.name in {".", ".."} or
                    p.name == "global.json" or p.suffix.lower() not in _SOURCE_EXTENSIONS):
                raise MaintenanceFixtureError("unsafe seed filename")
            (workspace / p.name).write_bytes(p.read_bytes())
        for i in range(1, checkpoint + 1):
            patch = base / "reference" / language / f"{i:02d}.patch"
            if not patch.is_file(): raise MaintenanceFixtureError(f"missing reference patch: {patch}")
            _read_lf(patch)
            git_apply = ["git", "-c", "core.autocrlf=false", "-c", "core.safecrlf=false", "apply"]
            try: check = subprocess.run(git_apply + ["--check", str(patch)], cwd=workspace,
                                        capture_output=True, text=True, check=False, timeout=20)
            except subprocess.TimeoutExpired as exc: raise MaintenanceFixtureError(f"patch check timeout {i:02d}") from exc
            if check.returncode:
                raise MaintenanceFixtureError(f"reference patch {i:02d} does not apply: {check.stderr[:1000]}")
            try: applied = subprocess.run(git_apply + [str(patch)], cwd=workspace,
                                          capture_output=True, text=True, check=False, timeout=20)
            except subprocess.TimeoutExpired as exc: raise MaintenanceFixtureError(f"patch apply timeout {i:02d}") from exc
            if applied.returncode:
                raise MaintenanceFixtureError(f"reference patch {i:02d} failed: {applied.stderr[:1000]}")
        files = list(workspace.iterdir())
        if any(p.is_dir() or p.is_symlink() for p in files): raise MaintenanceFixtureError("reconstructed source must be flat")
        if any(p.name == "global.json" or p.suffix.lower() not in _SOURCE_EXTENSIONS for p in files):
            raise MaintenanceFixtureError("reconstructed source has forbidden filename")
        if len(files) > MAX_SOURCE_FILES: raise MaintenanceFixtureError("reconstructed source file bound exceeded")
        if sum(len(_read_lf(p).encode("utf-8")) for p in files) > MAX_SOURCE_BYTES: raise MaintenanceFixtureError("reconstructed byte bound exceeded")
        return _source_map(workspace)


def applicable_cases(cases: list[Mapping[str, Any]], checkpoint: int, *, visibility: str | None = None) -> list[dict[str, Any]]:
    if not 0 <= checkpoint <= 8:
        raise ValueError("checkpoint must be 0..8")
    out = []
    for case in cases:
        introduced = case.get("introduced", 0)
        through = case.get("through", 8)
        if type(introduced) is not int or type(through) is not int:
            raise ValueError("case bounds must be integers")
        if introduced < 0 or through < introduced or through > 8:
            raise ValueError("invalid case bounds")
        if introduced <= checkpoint <= through and (visibility is None or case.get("visibility") == visibility):
            out.append(dict(case))
    return out


def load_cases(root: Path) -> list[dict[str, Any]]:
    path = Path(root) / "benchmarks" / "maintenance-sim" / "fixtures" / "cases.json"
    if not path.is_file():
        raise MaintenanceFixtureError(f"missing trusted cases fixture: {path}")
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise MaintenanceFixtureError("duplicate JSON key in cases")
            result[key] = value
        return result
    try:
        data = json.loads(_read_lf(path), object_pairs_hook=pairs,
                          parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))
    except (json.JSONDecodeError, ValueError) as exc:
        raise MaintenanceFixtureError("invalid cases JSON") from exc
    if not isinstance(data, list) or any(not isinstance(x, dict) for x in data):
        raise MaintenanceFixtureError("cases.json must be an array of objects")
    if not data:
        raise MaintenanceFixtureError("cases.json must not be empty")
    result = [dict(x) for x in data]
    seen = set()
    for case in result:
        if not isinstance(case.get("id"), str) or not case["id"] or case["id"] in seen: raise MaintenanceFixtureError("case IDs must be unique nonempty strings")
        seen.add(case["id"])
        if case.get("visibility") not in {"public", "evaluation"}: raise MaintenanceFixtureError("invalid case visibility")
        if "input" not in case or "expected" not in case: raise MaintenanceFixtureError("case requires input and expected")
        if type(case.get("introduced")) is not int or not 0 <= case["introduced"] <= 8: raise MaintenanceFixtureError("invalid case introduced stage")
        if "through" in case and (type(case["through"]) is not int or not case["introduced"] <= case["through"] <= 8): raise MaintenanceFixtureError("invalid case supersession stage")
    return result


def load_fault_manifest(root: Path) -> list[dict[str, Any]]:
    """Load the authored, trusted semantic-fault manifest.

    Patch names are deliberately relative to ``fixtures`` (and must reside
    below ``fixtures/faults``) and cannot
    select files outside that directory.  An absent manifest is an error: an
    empty audit would falsely look like successful evidence.
    """
    path = Path(root) / "benchmarks" / "maintenance-sim" / "fixtures" / "faults.json"
    if not path.is_file():
        raise MaintenanceFixtureError(f"missing trusted fault manifest: {path}")
    try:
        data = json.loads(_read_lf(path), parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
    except (json.JSONDecodeError, ValueError) as exc:
        raise MaintenanceFixtureError("invalid faults.json") from exc
    if not isinstance(data, list) or not data:
        raise MaintenanceFixtureError("faults.json must be a nonempty array")
    seen: set[str] = set(); result = []
    for entry in data:
        if not isinstance(entry, dict):
            raise MaintenanceFixtureError("fault manifest entries must be objects")
        required = {"id", "language", "checkpoint", "patch", "witness_case_id"}
        if set(entry) != required:
            raise MaintenanceFixtureError("fault manifest entry fields are invalid")
        ident = entry["id"]
        if not isinstance(ident, str) or not _FAULT_ID.fullmatch(ident) or ident in seen:
            raise MaintenanceFixtureError("fault IDs must be unique safe strings")
        if entry["language"] not in LANGUAGES or type(entry["checkpoint"]) is not int or not 0 <= entry["checkpoint"] <= 8:
            raise MaintenanceFixtureError("invalid fault language or checkpoint")
        patch = entry["patch"]
        if not isinstance(patch, str) or not patch or Path(patch).is_absolute() or "\\" in patch:
            raise MaintenanceFixtureError("fault patch must be a relative POSIX path")
        parts = Path(patch).parts
        if any(part in {"", ".", ".."} for part in parts) or len(parts) < 2 or parts[0] != "faults":
            raise MaintenanceFixtureError("fault patch path traversal is not permitted")
        witness = entry["witness_case_id"]
        if not isinstance(witness, str) or not witness:
            raise MaintenanceFixtureError("fault witness_case_id must be nonempty")
        seen.add(ident); result.append(dict(entry))
    return result


def _fault_source(root: Path, fault: Mapping[str, Any]) -> tuple[dict[str, str], str]:
    base = Path(root) / "benchmarks" / "maintenance-sim"
    fixtures_root = (base / "fixtures").resolve()
    faults_root = fixtures_root / "faults"
    patch = fixtures_root / fault["patch"]
    try:
        patch.resolve().relative_to(faults_root)
    except ValueError as exc:
        raise MaintenanceFixtureError("fault patch must be inside fixtures/faults") from exc
    if not patch.is_file() or patch.is_symlink():
        raise MaintenanceFixtureError(f"missing fault patch: {patch}")
    patch_text = _read_lf(patch)
    source = reconstruct(root, fault["language"], fault["checkpoint"])
    with tempfile.TemporaryDirectory(prefix="alf-maintenance-fault-") as td:
        workspace = Path(td)
        for name, value in source.items():
            (workspace / name).write_text(value, encoding="utf-8", newline="\n")
        command = ["git", "-c", "core.autocrlf=false", "-c", "core.safecrlf=false", "apply"]
        checked = subprocess.run(command + ["--check", str(patch)], cwd=workspace, capture_output=True, text=True, check=False, timeout=20)
        if checked.returncode:
            raise MaintenanceFixtureError(f"fault patch does not apply: {fault['id']}: {checked.stderr[:1000]}")
        applied = subprocess.run(command + [str(patch)], cwd=workspace, capture_output=True, text=True, check=False, timeout=20)
        if applied.returncode:
            raise MaintenanceFixtureError(f"fault patch failed: {fault['id']}: {applied.stderr[:1000]}")
        return _source_map(workspace), hashlib.sha256(patch_text.encode()).hexdigest()


def serialize_envelope(root: Path, language: str, checkpoint: int, source: Mapping[str, str], *, task_episode: int | None = None) -> dict[str, Any]:
    if language not in LANGUAGES or not 0 <= checkpoint <= 8:
        raise ValueError("invalid language or checkpoint")
    base = Path(root) / "benchmarks" / "maintenance-sim"
    if len(source) > MAX_SOURCE_FILES or any(not isinstance(name, str) or not _SAFE.fullmatch(name) or Path(name).name != name
                                              or name == "global.json" or Path(name).suffix.lower() not in _SOURCE_EXTENSIONS
                                              or not isinstance(value, str) or "\r" in value or "\x00" in value
                                              for name, value in source.items()):
        raise MaintenanceFixtureError("unsafe or oversized envelope source")
    pieces = [("common_guidance", base / "guidance" / "common.md"),
              ("language_guidance", base / "guidance" / f"{language}.md"),
              ("contract", base / "contract.md")]
    for i in range(1, checkpoint + 1):
        pieces.append((f"episode_{i:02d}", base / "episodes" / f"{i:02d}.md"))
    if task_episode is not None and not 1 <= task_episode <= 8: raise ValueError("task episode must be 1..8")
    if task_episode is not None and checkpoint != task_episode - 1: raise ValueError("source checkpoint must precede task")
    if task_episode is not None: pieces.append((f"current_episode_{task_episode:02d}", base / "episodes" / f"{task_episode:02d}.md"))
    source_bytes = {name: value.encode("utf-8") for name, value in sorted(source.items())}
    if sum(map(len, source_bytes.values())) > MAX_SOURCE_BYTES: raise MaintenanceFixtureError("envelope source byte bound exceeded")
    envelope = {"version": 1, "language": language, "source_checkpoint": checkpoint, "task_episode": task_episode,
                "guidance": {name: _read_lf(path) for name, path in pieces if "guidance" in name},
                "seed_contract": _read_lf(base / "contract.md"),
                "past_public_obligations": [_read_lf(base / "episodes" / f"{i:02d}.md") for i in range(1, checkpoint + 1)],
                "current_task": _read_lf(base / "episodes" / f"{task_episode:02d}.md") if task_episode else None,
                "source": dict(sorted(source.items()))}
    data = json.dumps(envelope, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8") + b"\n"
    return {"envelope": envelope, "language": language, "source_checkpoint": checkpoint, "task_episode": task_episode,
            "input_bytes": len(data),
            "source_bytes": sum(map(len, source_bytes.values())), "source_files": len(source_bytes),
            "sha256": hashlib.sha256(data).hexdigest(), "serialized": data.decode("utf-8"), "token_proxy": tokenize(data),
            "components": {name: len(_read_lf(path).encode("utf-8")) for name, path in pieces},
            "source_sha256": {name: hashlib.sha256(value).hexdigest() for name, value in source_bytes.items()},
            "allocations": {"integration": 0, "pilot": 0}, "live": False}


def reference_submission_metrics(root: Path) -> list[dict[str, Any]]:
    """Measure canonical JSON full-file replacements for each reviewed patch."""
    rows = []
    for language in LANGUAGES:
        before = reconstruct(root, language, 0)
        for episode in range(1, 9):
            after = reconstruct(root, language, episode)
            changed = {name: after[name] for name in sorted(after)
                       if name not in before or after[name] != before[name]}
            removed = sorted(set(before) - set(after))
            if removed:
                raise MaintenanceFixtureError("reference patch removes files; replacement format cannot represent deletion")
            payload = json.dumps({"architecture_notes": "", "files": changed}, ensure_ascii=False,
                                 sort_keys=True, separators=(",", ":")).encode("utf-8")
            rows.append({"language": language, "episode": episode, "bytes": len(payload),
                         "sha256": hashlib.sha256(payload).hexdigest(),
                         "changed_files": sorted(changed), "removed_files": removed,
                         "note": "lower-bound placeholder with empty required architecture_notes; excludes actual note contents and native/model framing"})
            before = after
    return rows


def classify_build(result: Mapping[str, Any]) -> str:
    if result.get("returncode") != 0 or result.get("timed_out") or result.get("overflow"):
        return "build"
    return "runtime"


def _build_source(source: Mapping[str, str], language: str, cases: list[Mapping[str, Any]], sdk: str = SDK,
                  *, invoke: Callable[..., Any] = subprocess.run) -> dict[str, Any]:
    """Build and run an already-owned trusted source tree."""
    if not cases: raise MaintenanceFixtureError("trusted build requires at least one case")
    project = "Simulation.csproj" if language == "csharp" else "Simulation.fsproj"
    with tempfile.TemporaryDirectory(prefix="alf-maintenance-build-") as td:
        workspace = Path(td)
        (workspace / "global.json").write_text(json.dumps({"sdk": {"version": sdk, "rollForward": "disable",
                                                               "allowPrerelease": False}}) + "\n", encoding="utf-8")
        for name, value in source.items():
            (workspace / name).write_text(value, encoding="utf-8", newline="\n")
        env = credential_free_environment(workspace)
        def bounded(value):
            if value is None:
                return "", False
            if isinstance(value, bytes):
                value = value.decode("utf-8", "replace")
            return value[:65536], len(value) > 65536
        def run(argv, **kwargs):
            try:
                out = invoke(argv, **kwargs)
                stdout, stdout_truncated = bounded(out.stdout)
                stderr, stderr_truncated = bounded(out.stderr)
                return {"returncode": out.returncode, "stdout": stdout, "stderr": stderr,
                        "stdout_truncated": stdout_truncated, "stderr_truncated": stderr_truncated, "timed_out": False}
            except subprocess.TimeoutExpired as exc:
                stdout, _ = bounded(exc.stdout)
                stderr, _ = bounded(exc.stderr)
                return {"returncode": None, "stdout": stdout, "stderr": stderr, "timed_out": True}
        version = run(["dotnet", "--version"], cwd=workspace, env=env, capture_output=True, text=True,
                      timeout=15, check=False)
        observed = version["stdout"].strip()
        if version["returncode"] != 0 or version["timed_out"] or observed != sdk:
            return {"passed": False, "category": "build", "sdk": {"expected": sdk, "observed": observed}, "diagnostic": version}
        built = run(["dotnet", "build", project, "--configuration", "Debug", "--nologo", "-p:NuGetAudit=false"],
                    cwd=workspace, env=env, capture_output=True, text=True, timeout=120, check=False)
        if built["returncode"] != 0 or built["timed_out"] or built.get("stdout_truncated") or built.get("stderr_truncated"):
            return {"passed": False, "category": "build", "returncode": built["returncode"], "diagnostic": built}
        dll = workspace / "bin" / "Debug" / "net10.0" / "Simulation.dll"
        payload = "".join(json.dumps(c["input"], separators=(",", ":")) + "\n" for c in cases)
        ran = run(["dotnet", str(dll)], cwd=workspace, env=env, input=payload, capture_output=True, text=True,
                  timeout=30, check=False)
        if (ran["returncode"] != 0 or ran["timed_out"] or ran.get("stdout_truncated")
                or ran.get("stderr_truncated") or ran["stderr"]):
            return {"passed": False, "category": "runtime", "returncode": ran["returncode"], "diagnostic": ran}
        actual = []
        def pairs(items):
            result = {}
            for key, value in items:
                if key in result: raise ValueError("duplicate JSON key")
                result[key] = value
            return result
        for line in ran["stdout"].splitlines():
            try: actual.append(json.loads(line, object_pairs_hook=pairs, parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x))))
            except (json.JSONDecodeError, ValueError): actual.append("<invalid-json>")
        if any(a == "<invalid-json>" for a in actual) or len(actual) != len(cases):
            return {"passed": False, "category": "parse", "line_count": len(actual),
                    "expected_line_count": len(cases), "actual": actual}
        differences = [{"index": i, "actual": a, "expected": c["expected"]}
                       for i, (a, c) in enumerate(zip(actual, cases))
                       if not _strict_json_equal(a, c["expected"])]
        if len(actual) != len(cases): differences.append({"line_count": len(actual), "expected_line_count": len(cases)})
        return {"passed": not differences, "category": "semantic", "differences": differences,
                "source_sha256": {n: hashlib.sha256(v.encode()).hexdigest() for n, v in source.items()}}


def build_checkpoint(root: Path, language: str, checkpoint: int, cases: list[Mapping[str, Any]], sdk: str = SDK,
                     *, invoke: Callable[..., Any] = subprocess.run) -> dict[str, Any]:
    """Build and run one trusted checkpoint; failures remain separately classified."""
    return _build_source(reconstruct(root, language, checkpoint), language, cases, sdk, invoke=invoke)


def audit_faults(root: Path, cases: list[Mapping[str, Any]] | None = None, *,
                 invoke: Callable[..., Any] = subprocess.run,
                 require_complete: bool = False) -> dict[str, Any]:
    """Audit only authored fault patches; semantic kills are the evidence."""
    root = Path(root)
    cases = load_cases(root) if cases is None else cases
    manifest = load_fault_manifest(root)
    if require_complete:
        coverage = {(fault["language"], fault["checkpoint"], Path(fault["patch"]).name)
                    for fault in manifest}
        families = {1: "drop-due-effects.patch", 2: "omit-future-cancel.patch",
                    5: "bypass-policy.patch", 8: "leak-replay-registry.patch"}
        expected = {(language, checkpoint, name) for language in LANGUAGES
                    for checkpoint, name in families.items()}
        if len(manifest) != 8 or coverage != expected:
            raise MaintenanceFixtureError("complete fault audit requires exactly checkpoints 1, 2, 5, 8 for each language")
    by_id = {case.get("id"): case for case in cases}
    rows = []
    for fault in manifest:
        case = by_id.get(fault["witness_case_id"])
        if case is None:
            raise MaintenanceFixtureError(f"fault witness case is missing: {fault['witness_case_id']}")
        baseline_source = reconstruct(root, fault["language"], fault["checkpoint"])
        baseline = _build_source(baseline_source, fault["language"], [case], invoke=invoke)
        mutant_source, patch_sha = _fault_source(root, fault)
        mutant = _build_source(mutant_source, fault["language"], [case], invoke=invoke)
        semantic_kill = baseline.get("passed") is True and mutant.get("category") == "semantic" and not mutant.get("passed")
        case_sha = hashlib.sha256(json.dumps(case, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        rows.append({"id": fault["id"], "language": fault["language"], "checkpoint": fault["checkpoint"],
                     "witness_case_id": fault["witness_case_id"], "baseline": baseline, "mutant": mutant,
                     "semantic_kill": semantic_kill,
                     "provenance": {"source_sha256": {k: hashlib.sha256(v.encode()).hexdigest() for k, v in baseline_source.items()},
                                    "mutant_source_sha256": {k: hashlib.sha256(v.encode()).hexdigest() for k, v in mutant_source.items()},
                                    "patch_sha256": patch_sha, "case_sha256": case_sha}})
    return {"status": "passed" if rows and all(row["semantic_kill"] for row in rows) else "failed",
            "faults": rows, "trusted_source_only": True, "candidate_execution": False, "live": False}


def classify_applicability(*, submission_disposition: str, prerequisite: bool | None,
                           current: bool | None, evaluation_available: bool | None,
                           recovery: bool | None = None, prior_failure: str | None = None,
                           build_category: str | None = None) -> dict[str, Any]:
    """Keep fixed predecessor applicability dimensions independent.

    This is a record classifier, not candidate validation or continuation
    policy.  Unavailable build/runtime/parse evidence stays unknown (``None``).
    A recovery observation is additive and never rewrites ``prior_failure``.
    """
    if build_category in {"build", "runtime", "parse"}:
        prerequisite = current = None
        evaluation_available = False
    if submission_disposition not in {"applicable", "no-op", "malformed", "noncompile", "missing-feature", "wrong-behavior"}:
        raise ValueError("invalid fixed-fixture submission disposition")
    return {"submission_disposition": submission_disposition,
            "prerequisite_correctness": prerequisite,
            "current_correctness": current,
            "evaluation_availability": evaluation_available,
            "recovery": recovery,
            "prior_failure": prior_failure,
            "attribution": None}


_DOWNSTREAM_WITNESSES = {
    1: "queue-order", 2: "future-remove-canceled-after-due-remove",
    3: "follower-simultaneous", 4: "import-v1-migration", 5: "policy-clamp",
    6: "async-lifecycle", 7: "fast-forward-large", 8: "replay-success",
}


def _source_hashes(source: Mapping[str, str]) -> dict[str, str]:
    return {name: hashlib.sha256(value.encode("utf-8")).hexdigest()
            for name, value in sorted(source.items())}


def _noncompiling_source(source: Mapping[str, str], language: str) -> dict[str, str]:
    result = dict(source)
    suffix = ".cs" if language == "csharp" else ".fs"
    names = sorted(name for name in result if name.endswith(suffix))
    if not names:
        raise MaintenanceFixtureError(f"missing {suffix} source for noncompiling fixture")
    result[names[0]] += "\nthis is intentionally not valid source\n"
    return result


def _applicability_evaluation(source: Mapping[str, str], language: str,
                              prerequisite_cases: list[Mapping[str, Any]],
                              current_cases: list[Mapping[str, Any]],
                              invoke: Callable[..., Any]) -> tuple[bool | None, bool | None, bool, str | None, dict[str, Any]]:
    prerequisite = _build_source(source, language, prerequisite_cases, invoke=invoke)
    current = _build_source(source, language, current_cases, invoke=invoke)
    unavailable = next((result["category"] for result in (prerequisite, current)
                        if result.get("category") in {"build", "runtime", "parse"}), None)
    if unavailable is not None:
        return None, None, False, unavailable, {"prerequisite": prerequisite, "current": current}
    return (prerequisite.get("passed") is True, current.get("passed") is True, True, None,
            {"prerequisite": prerequisite, "current": current})


def audit_applicability(root: Path, cases: list[Mapping[str, Any]] | None = None,
                        *, invoke: Callable[..., Any] = subprocess.run) -> dict[str, Any]:
    """Run the fixed trusted episode-1-to-2 and downstream applicability audit."""
    root = Path(root)
    cases = load_cases(root) if cases is None else cases
    by_id = {case.get("id"): case for case in cases}
    if len(by_id) != len(cases):
        raise MaintenanceFixtureError("applicability audit requires unique case IDs")
    missing = [ident for ident in _DOWNSTREAM_WITNESSES.values() if ident not in by_id]
    if missing:
        raise MaintenanceFixtureError("missing applicability witness cases: " + ", ".join(missing))
    prerequisite_cases = applicable_cases(cases, 1)
    current_cases = [case for case in cases if case.get("introduced") == 2]
    if not prerequisite_cases or not current_cases:
        raise MaintenanceFixtureError("applicability audit requires checkpoint-1 prerequisite and episode-2 cases")
    manifest = load_fault_manifest(root)
    records: list[dict[str, Any]] = []
    downstream: list[dict[str, Any]] = []
    responses = {"no-op": b'{"architecture_notes":"no change","files":{}}',
                 "malformed": b'{"architecture_notes":'}
    for language in LANGUAGES:
        ref1 = reconstruct(root, language, 1)
        ref2 = reconstruct(root, language, 2)
        seed = reconstruct(root, language, 0)
        drop_faults = [fault for fault in manifest if fault["language"] == language
                       and fault["checkpoint"] == 1 and Path(fault["patch"]).name == "drop-due-effects.patch"]
        if len(drop_faults) != 1:
            raise MaintenanceFixtureError(f"requires one episode-1 drop-due-effects fault for {language}")
        wrong, wrong_patch_sha = _fault_source(root, drop_faults[0])
        fixtures = [
            ("no-op", "no-op", ref1, responses["no-op"], None),
            ("malformed", "malformed", ref1, responses["malformed"], None),
            ("noncompile", "noncompile", _noncompiling_source(ref1, language), None, None),
            ("missing-feature", "missing-feature", seed, None, None),
            ("wrong-behavior", "wrong-behavior", wrong, None, wrong_patch_sha),
            ("recovery-control", "applicable", ref2, None, None),
        ]
        prior_failure_seen = False
        strict_chain_success = True
        for ident, disposition, source, response, patch_sha in fixtures:
            pre, cur, available, category, evidence = _applicability_evaluation(
                source, language, prerequisite_cases, current_cases, invoke)
            if ident == "wrong-behavior":
                prior_failure_seen = not (pre is True and cur is True)
                strict_chain_success = strict_chain_success and not prior_failure_seen
            recovery = (pre is True and cur is True) if ident == "recovery-control" else None
            row = classify_applicability(
                submission_disposition=disposition, prerequisite=pre, current=cur,
                evaluation_available=available, recovery=recovery,
                prior_failure="wrong-behavior" if ident == "recovery-control" and prior_failure_seen else None,
                build_category=category)
            row.update({"id": ident, "language": language, "source_checkpoint": 1,
                        "task_episode": 2, "case_ids": {
                            "prerequisite": [case["id"] for case in prerequisite_cases],
                            "current": [case["id"] for case in current_cases]},
                        "source_sha256": _source_hashes(source), "evaluation": evidence,
                        "response_sha256": hashlib.sha256(response).hexdigest() if response is not None else None,
                        "fault_patch_sha256": patch_sha,
                        "strict_chain_success": strict_chain_success if ident == "recovery-control" else None,
                        "actual_candidate_repair": False, "gold_reset": False})
            records.append(row)
        for episode, case_id in _DOWNSTREAM_WITNESSES.items():
            result = _build_source(seed, language, [by_id[case_id]], invoke=invoke)
            downstream.append({"language": language, "source_checkpoint": 0, "task_episode": episode,
                               "witness_case_id": case_id, "case_sha256": hashlib.sha256(
                                   json.dumps(by_id[case_id], ensure_ascii=False, sort_keys=True,
                                              separators=(",", ":")).encode()).hexdigest(),
                               "source_sha256": _source_hashes(seed), "evaluation": result,
                               "evaluation_availability": result.get("category") not in {"build", "runtime", "parse"}})
    expected = {
        "no-op": (True, False, True), "malformed": (True, False, True),
        "noncompile": (None, None, False), "missing-feature": (False, False, True),
        "wrong-behavior": (False, False, True), "recovery-control": (True, True, True),
    }
    passed = (len(records) == 12 and all(
        (row["prerequisite_correctness"], row["current_correctness"], row["evaluation_availability"])
        == expected[row["id"]] for row in records)
        and all(row["evaluation_availability"] for row in downstream)
        and len(downstream) == 16)
    return {"status": "passed" if passed else "failed", "records": records,
            "downstream_witnesses": downstream,
            "note": "fixed response fixtures demonstrate task applicability, not future candidate parser/controller handling",
            "trusted_source_only": True, "candidate_execution": False, "live": False}
