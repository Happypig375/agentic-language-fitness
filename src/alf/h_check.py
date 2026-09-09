"""Deterministic, model-free construction audit for workstream H1/H2."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
from pathlib import Path
from typing import Any, Mapping

from . import h0, h_workload
from .h import HController, MAX_AUTHORED_BYTES, MAX_REPLY_BYTES, parse_action
from .workstream_e3a import apply_submission, canonical_json_hash

LEVELS = ("core", "expanded")
LANGUAGES = ("csharp", "fsharp")
ACCESSES = ("H1", "H2")
ORDERS = ("forward", "reverse")


def _json(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()


def _sha(data: bytes | str) -> str:
    return hashlib.sha256(data.encode() if isinstance(data, str) else data).hexdigest()


def _file_identity(root: Path, relative: str) -> dict[str, Any]:
    data = (root / relative).read_text(encoding="utf-8").encode("utf-8")
    return {"path": relative.replace("\\", "/"), "bytes": len(data), "sha256": _sha(data)}


def _submission(gold: Mapping[str, str]) -> str:
    return json.dumps({"action": "submit", "files": dict(gold)}, ensure_ascii=False,
                      sort_keys=True, separators=(",", ":"))


def _public_payload_ok(payload: Mapping[str, Any]) -> bool:
    def keys(value: Any):
        if isinstance(value, Mapping):
            for key, child in value.items():
                yield str(key).lower()
                yield from keys(child)
        elif isinstance(value, list):
            for child in value:
                yield from keys(child)
    forbidden = {"private_cases", "gold", "gold_source", "holdout", "relevance",
                 "evaluator_roles", "future_tasks"}
    return not forbidden.intersection(keys(payload))


def _controller(source: Mapping[str, str], order: list[str], payload: Mapping[str, Any],
                language: str, access: str, spec: Mapping[str, Any], cap: int = MAX_AUTHORED_BYTES) -> HController:
    return HController(source, order, contracts=payload, task={}, language=language, access=access,
                       byte_cap=cap, submission_spec=spec)


def _request_record(data: bytes, resident: list[str], exposure: list[str], *,
                    include_token_proxy: bool = True) -> dict[str, Any]:
    return {"bytes": len(data), "sha256": _sha(data),
            "token_proxy": h0.tokenize(data) if include_token_proxy else None,
            "replay_utf8": data.decode("utf-8"),
            "resident": list(resident), "exposure": list(exposure), "provider_context_limit": None,
            "provider_input_tokens": None, "subscription_usd": None}


def reference_requests(source: Mapping[str, str], order: list[str], payload: Mapping[str, Any],
                       language: str, access: str, spec: Mapping[str, Any], *,
                       include_token_proxy: bool = True) -> tuple[list[bytes], list[dict[str, Any]]]:
    controller = _controller(source, order, payload, language, access, spec)
    first = controller.request()
    requests, records = [first], [_request_record(first, list(order) if access == "H1" else [],
        list(order) if access == "H1" else [], include_token_proxy=include_token_proxy)]
    if access == "H1":
        return requests, records
    groups = [order[:4], order[4:]]
    resident: list[str] = []
    exposed: list[str] = []
    for group in groups:
        if not group:
            continue
        raw = json.dumps({"action": "read", "paths": group}, separators=(",", ":"))
        result = controller.apply(raw)
        for name in order:
            if name in group and name not in resident:
                resident.append(name)
                exposed.append(name)
        requests.append(result["request"])
        records.append(_request_record(result["request"], resident, exposed,
                                       include_token_proxy=include_token_proxy))
    return requests, records


def derive_caps(measurements: list[dict[str, Any]], headroom: int = 1024, rounding: int = 1024) -> tuple[int, int]:
    core = max(request["bytes"] for item in measurements if item["level"] == "core" for request in item["requests"])
    overall = max(request["bytes"] for item in measurements for request in item["requests"])
    return (math.ceil((core + headroom) / rounding) * rounding,
            math.ceil((overall + headroom) / rounding) * rounding)


def schedule(seed: int, caps: tuple[int, int]) -> list[dict[str, Any]]:
    blocks = []
    for level in LEVELS:
        for cap_name, cap in zip(("low", "high"), caps):
            for access in ACCESSES:
                for order_index, order in enumerate(ORDERS):
                    first = LANGUAGES if order_index == 0 else tuple(reversed(LANGUAGES))
                    blocks.append([{"level": level, "cap": cap_name, "cap_bytes": cap,
                                    "access": access, "file_order": order, "language": language}
                                   for language in first])
    random.Random(seed).shuffle(blocks)
    result = []
    for pair_index, block in enumerate(blocks, 1):
        for slot in block:
            result.append({"slot": len(result) + 1, "pair": pair_index, **slot})
    return result


def audit(root: Path, specification: str | Path = "protocols/workstream-h1-h2/specification.json", *,
          permit_activation: bool = False) -> dict[str, Any]:
    root = Path(root)
    spec_path = Path(specification)
    spec_path = spec_path if spec_path.is_absolute() else root / spec_path
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    failures: list[str] = []
    live_state = (spec["execution_authorized"], spec["user_live_execution_approved"],
                  spec["approved_integration_dispatches"], spec["approved_pilot_dispatches"],
                  spec.get("analysis", {}).get("human_review_approved", False),
                  spec.get("model", {}).get("h_live_integration_verified", False))
    if not permit_activation and any(live_state):
        failures.append("live-execution-flags-enabled")
    if spec.get("status") in {"model-free-construction", "pre-execution-human-review"} and any(live_state):
        failures.append("status-authorization-inconsistent")
    definition = h0._definition(root, spec["workload"]["core_definition"])
    measurements, bundles, identities = [], {}, []
    artifact_paths = [spec["workload"]["core_definition"], spec["workload"]["expanded_contract"],
                      "benchmarks/workstream-h/public-examples.json",
                      "benchmarks/successor/tasks/008-summary-api/task.md",
                      "src/alf/h.py", "src/alf/h_workload.py", "src/alf/h_check.py",
                      "src/alf/h_run.py", "src/alf/h_sandbox.py", "src/alf/h_fixtures.py",
                      "scripts/h_run.py", "scripts/h_check.py", "scripts/h_native_check.py",
                      "src/alf/h0.py", "src/alf/e3a_codex.py", "src/alf/e3a_runner.py",
                      "src/alf/e3a_sandbox.py", "src/alf/workstream_e3a.py",
                      "src/alf/config.py", "src/alf/process.py", "src/alf/protocol.py",
                      "scripts/codex-docker.py", "infra/remote-runner/environment-profile.json",
                      "protocols/workstream-e3a-v1/specification.json",
                      "protocols/workstream-e3a-v1/freeze.json"]
    identities = [_file_identity(root, path) for path in artifact_paths]
    declared = {"benchmarks/workstream-h/contract.md": spec["workload"]["expanded_contract_sha256"],
                "benchmarks/workstream-h/public-examples.json": spec["workload"]["public_examples_sha256"]}
    for item in identities:
        if item["path"] in declared and item["sha256"] != declared[item["path"]]:
            failures.append(f"declared-identity-mismatch:{item['path']}")
    for level in LEVELS:
        payload = h_workload.public_payload(root, level)
        if not _public_payload_ok(payload):
            failures.append(f"{level}-public-payload-leak")
        if not all(key in payload for key in ("current_task", "earlier_contracts", "baseline_contract")):
            failures.append(f"{level}-public-payload-incomplete")
        if level == "expanded" and not all(key in payload for key in ("expanded_contract", "expanded_public_examples")):
            failures.append("expanded-public-payload-incomplete")
        for language in LANGUAGES:
            try:
                source = h_workload.source_for(root, level, language)
                gold = h_workload.source_for(root, level, language, gold=True)
            except Exception as exc:
                failures.append(f"{level}-{language}-load:{type(exc).__name__}:{exc}")
                continue
            if level == "core" and canonical_json_hash(source) != definition["source_sha256"][language]:
                failures.append(f"core-{language}-h0-identity")
            if len(source) > spec["authority"]["max_total_files"] or sum(len(x.encode()) for x in source.values()) > 65_536:
                failures.append(f"{level}-{language}-source-bound")
            raw = _submission(gold)
            try:
                action = parse_action(raw)
                if len(raw.encode()) > MAX_REPLY_BYTES:
                    raise ValueError("gold reply exceeds output bound")
                applied = apply_submission(source, json.dumps({"files": action["files"]}, ensure_ascii=False,
                                           separators=(",", ":")), language, spec)
                if applied != gold:
                    raise ValueError("gold application mismatch")
            except Exception as exc:
                failures.append(f"{level}-{language}-gold:{type(exc).__name__}:{exc}")
            bundles[f"{level}-{language}"] = {"source": {p: _sha(t) for p, t in sorted(source.items())},
                                                "gold": {p: _sha(t) for p, t in sorted(gold.items())},
                                                "gold_submission": {"bytes": len(raw.encode()), "sha256": _sha(raw)},
                                                "public_payload_sha256": canonical_json_hash(payload)}
            for reverse in (False, True):
                order = h_workload.ordered_filenames(source, language, reverse)
                for access in ACCESSES:
                    try:
                        requests, records = reference_requests(source, order, payload, language, access, spec)
                    except Exception as exc:
                        failures.append(f"{level}-{language}-{reverse}-{access}:{type(exc).__name__}:{exc}")
                        continue
                    if any(any(text.encode() in request for text in gold.values() if text not in source.values()) for request in requests):
                        failures.append(f"{level}-{language}-{reverse}-{access}-future-gold-leak")
                    measurements.append({"level": level, "language": language,
                        "file_order": "reverse" if reverse else "forward", "access": access,
                        "ordered_filenames": order, "requests": records})
    caps = derive_caps(measurements) if measurements else (0, 0)
    if not (0 < caps[0] < caps[1] <= MAX_AUTHORED_BYTES):
        failures.append("pressure-caps-not-distinct-bounded")
    def maximum(level: str, access: str) -> int:
        return max((request["bytes"] for item in measurements if item["level"] == level and item["access"] == access
                    for request in item["requests"]), default=0)
    if maximum("core", "H1") > caps[0] or maximum("core", "H2") > caps[0]:
        failures.append("core-low-overlap-absent")
    if max((r["bytes"] for x in measurements for r in x["requests"]), default=0) > caps[1]:
        failures.append("high-reference-fit-absent")
    if maximum("expanded", "H1") <= caps[0]:
        failures.append("expanded-h1-low-pressure-absent")
    slots = schedule(spec["schedule"]["seed"], caps)
    # H2 starts from its map-only request. Later read overflow is a retained
    # policy outcome, not preflight exclusion informed by a reference strategy.
    lookup = {(x["level"], x["language"], x["file_order"], x["access"]):
              (x["requests"][0]["bytes"] if x["access"] == "H2" else max(r["bytes"] for r in x["requests"]))
              for x in measurements}
    mask = [{**slot, "feasible": lookup.get((slot["level"], slot["language"], slot["file_order"], slot["access"]),
                                              MAX_AUTHORED_BYTES + 1) <= slot["cap_bytes"],
             "dispatches": 0, "outcome": "unexecuted-preflight"} for slot in slots]
    proposed = {"workload.source_sha256": canonical_json_hash({k: v["source"] for k, v in sorted(bundles.items())}),
                "workload.cases_sha256": canonical_json_hash({level: h_workload.cases_for(root, level) for level in LEVELS}),
                "workload.public_payload_sha256": canonical_json_hash(
                    {level: h_workload.public_payload(root, level) for level in LEVELS}),
                "budgets.cap_low": caps[0], "budgets.cap_high": caps[1],
                "schedule.schedule_sha256": canonical_json_hash(slots),
                "schedule.feasibility_mask_sha256": canonical_json_hash(mask)}
    populated = {
        "workload.source_sha256": spec["workload"].get("source_sha256"),
        "workload.cases_sha256": spec["workload"].get("cases_sha256"),
        "workload.public_payload_sha256": spec["workload"].get("public_payload_sha256"),
        "budgets.cap_low": spec["budgets"].get("cap_low"),
        "budgets.cap_high": spec["budgets"].get("cap_high"),
        "schedule.schedule_sha256": spec["schedule"].get("schedule_sha256"),
        "schedule.feasibility_mask_sha256": spec["schedule"].get("feasibility_mask_sha256"),
    }
    for key, value in populated.items():
        if value is not None and value != proposed[key]:
            failures.append(f"populated-pin-mismatch:{key}")
    try:
        specification_identity = _file_identity(root, str(spec_path.relative_to(root)))
    except ValueError:
        specification_data = spec_path.read_text(encoding="utf-8").encode()
        specification_identity = {"path": "external-specification.json", "bytes": len(specification_data),
                                  "sha256": _sha(specification_data)}
    return {"status": "passed" if not failures else "failed", "failures": failures,
            "specification": specification_identity,
            "check_scope": {"model_free": True, "live_execution_performed": False,
                            "dispatches_performed": 0, "oauth_staged": False,
                            "native_invoked": False, "network_used": False},
            "specification_authorization": {
                "execution_authorized": spec["execution_authorized"],
                "user_live_execution_approved": spec["user_live_execution_approved"],
                "human_review_approved": spec.get("analysis", {}).get("human_review_approved", False),
                "h_live_integration_verified": spec.get("model", {}).get("h_live_integration_verified", False),
                "approved_integration_dispatches": spec["approved_integration_dispatches"],
                "approved_pilot_dispatches": spec["approved_pilot_dispatches"]},
            "context_accounting": {"unit": "complete-authored-input-utf8-bytes",
                "token_proxy": "tiktoken==0.14.0/o200k_base", "provider_context_limit": None,
                "provider_count_request": False, "subscription_usd": None},
            "caps": {"low": caps[0], "high": caps[1]}, "bundles": bundles,
            "identities": identities, "measurements": measurements, "schedule": slots,
            "feasibility_mask": mask, "proposed_specification_updates": proposed}


def write_artifacts(report: Mapping[str, Any], output_dir: Path) -> None:
    output_dir = Path(output_dir)
    if output_dir.exists():
        raise FileExistsError("output directory already exists")
    output_dir.mkdir(parents=True)
    files = {"report.json": report, "schedule.json": report["schedule"],
             "feasibility-mask.json": report["feasibility_mask"]}
    for index, item in enumerate(report["measurements"], 1):
        files[f"envelope-{index:02d}.json"] = item
    for name, value in files.items():
        (output_dir / name).write_bytes(_json(value))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--specification", default="protocols/workstream-h1-h2/specification.json")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--build-fixtures", action="store_true")
    parser.add_argument("--sandbox", action="store_true")
    parser.add_argument("--fixture-image-id")
    parser.add_argument("--permit-activation", action="store_true",
                        help="read-only audit of an activated specification")
    args = parser.parse_args(argv)
    root = Path(__file__).resolve().parents[2]
    report = audit(root, args.specification, permit_activation=args.permit_activation)
    if report["status"] == "passed" and (args.build_fixtures or args.sandbox):
        from .h_fixtures import build_fixtures, build_sandbox_fixtures
        if args.sandbox:
            spec = json.loads((root / args.specification).read_text(encoding="utf-8"))
            report["trusted_fixtures"] = build_sandbox_fixtures(root, spec, args.fixture_image_id)
        else:
            report["trusted_fixtures"] = build_fixtures(root, spec_sdk(report, root, args.specification))
        if report["trusted_fixtures"]["status"] != "passed":
            report["status"] = "failed"
    write_artifacts(report, Path(args.output_dir))
    return 0 if report["status"] == "passed" else 1


def spec_sdk(report: Mapping[str, Any], root: Path, specification: str) -> str:
    del report
    path = Path(specification)
    path = path if path.is_absolute() else root / path
    return json.loads(path.read_text(encoding="utf-8"))["environment"]["sdk"]
