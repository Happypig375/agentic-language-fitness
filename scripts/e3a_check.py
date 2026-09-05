"""Review-only E3a checks. Builds ONLY repository-owned gold/finite fault fixtures.

This is intentionally not an evaluator for candidate submissions. It uses the
host SDK, not the proposed production sandbox, and has no model client.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from alf.config import load_manifest  # noqa: E402
from alf.process import run_process  # noqa: E402
from alf.protocol import canonical_json_hash  # noqa: E402
from alf.workstream_e2 import _get_encoding, TOKENIZER_ENCODING, TOKENIZER_VERSION  # noqa: E402
from alf.workstream_e3a import (  # noqa: E402
    PACKET_DIR, apply_submission, budget, candidate_payload, development_cases,
    holdout_cases, read_json, schedule, snapshot, structural_development,
)


def make_packet() -> dict:
    spec = read_json(ROOT / PACKET_DIR / "specification.json")
    manifest = load_manifest(ROOT, spec["manifest"])
    archive = read_json(ROOT / "reports/workstream-e-v3/forensic-report.json")
    encoding = _get_encoding()
    identities = {}
    for name in ["specification.json", "candidate-instructions.md", "baseline-contract.md", "holdout-cases.json"]:
        path = f"{PACKET_DIR}/{name}"
        identities[path] = hashlib.sha256((ROOT / path).read_text(encoding="utf-8").encode("utf-8")).hexdigest()
    for path in ["src/alf/workstream_e3a.py", "scripts/e3a_check.py", "tests/test_workstream_e3a.py"]:
        identities[path] = hashlib.sha256((ROOT / path).read_text(encoding="utf-8").encode("utf-8")).hexdigest()
    tasks = []
    for task_id in spec["tasks"]:
        stage = next(i + 1 for i, task in enumerate(manifest["tasks"]) if task["id"] == task_id)
        dev, holdout = development_cases(manifest, stage), holdout_cases(ROOT, task_id)
        if {canonical_json_hash(c["input"]) for c in dev} & {canonical_json_hash(c["input"]) for c in holdout}:
            raise ValueError("holdout input copied from development cases")
        languages = {}
        for language in spec["languages"]:
            predecessor, target = [snapshot(ROOT, manifest, language, s) for s in [stage - 1, stage]]
            if apply_submission(predecessor, json.dumps({"files": target}), language, spec) != target:
                raise ValueError("declared replacement policy does not permit archived task changes")
            payload = candidate_payload(ROOT, manifest, language, task_id)
            payload_text = json.dumps(payload, ensure_ascii=False)
            languages[language] = {
                "predecessor_sha256": canonical_json_hash(predecessor),
                "archived_target_sha256": canonical_json_hash(target),
                "predecessor_files": {p: hashlib.sha256(t.encode("utf-8")).hexdigest() for p, t in predecessor.items()},
                "candidate_payload_sha256": canonical_json_hash(payload),
                "source_and_project_utf8_bytes": sum(len(t.encode("utf-8")) for t in predecessor.values()),
                "source_and_project_lines": sum(len(t.splitlines()) for t in predecessor.values()),
                "source_and_project_tokenizer_proxy": sum(len(encoding.encode(t)) for t in predecessor.values()),
                "payload_utf8_bytes": len(payload_text.encode("utf-8")),
                "payload_tokenizer_proxy": len(encoding.encode(payload_text)),
            }
        observations = []
        for run in archive["runs"]:
            task = next(t for t in run["tasks"] if t["task_id"] == task_id)
            first = task["build_state"]["first_post_edit_candidate_build"]
            observations.append({
                "attempt_id": run["attempt_id"], "language": run["language"],
                "configuration": run["configuration_id"],
                "first_post_edit_build": first["outcome"]["value"],
                "repair_cycles": len(task["build_state"]["repair_cycles"]),
                "project_mutations": task["project_file_mutation_count"],
                "diagnostic_codes": task["diagnostics"]["counts_by_code"],
            })
        tasks.append({"task_id": task_id, "predecessor_stage": stage - 1, "source": languages,
                      "development_cases": len(dev), "holdout_cases": len(holdout),
                      "development_sha256": canonical_json_hash(dev), "holdout_sha256": canonical_json_hash(holdout),
                      "archived_observations": observations})
    return {"status": "review-only-not-frozen", "execution_authorized": False,
            "scientific_specification_sha256": canonical_json_hash(spec), "text_lf_sha256": identities,
            "e1_report_identity": archive["report_sha256"],
            "tokenizer_proxy": {"package": "tiktoken", "version": TOKENIZER_VERSION, "encoding": TOKENIZER_ENCODING,
                                "actual_provider_input": False}, "tasks": tasks, "budget": budget(spec),
            "schedule": schedule(spec), "independent_review": "pending", "live_validation": "not-authorized"}


def build_fixtures() -> dict:
    spec = read_json(ROOT / PACKET_DIR / "specification.json")
    manifest = load_manifest(ROOT, spec["manifest"])
    sdk = run_process(["dotnet", "--version"], cwd=ROOT)
    if not sdk.ok or sdk.stdout.strip() != spec["environment"]["sdk"]:
        raise RuntimeError("fixture SDK differs from proposal")
    evidence = []
    with tempfile.TemporaryDirectory(prefix="alf-e3a-trusted-") as tmp:
        base = Path(tmp).resolve()
        for task_id in spec["tasks"]:
            stage = next(i + 1 for i, task in enumerate(manifest["tasks"]) if task["id"] == task_id)
            for language in spec["languages"]:
                for role, s in [("predecessor", stage - 1), ("archived-target", stage), ("fault", stage)]:
                    source = snapshot(ROOT, manifest, language, s)
                    ext = "cs" if language == "csharp" else "fs"
                    if role == "fault":
                        path = f"{'OrderFlowEngine' if stage == 7 else 'Program'}.{ext}"
                        if stage == 1:
                            old, new = (("OrderByDescending(order => order.Priority ?? 0)", "OrderBy(order => order.Priority ?? 0)")
                                        if language == "csharp" else ("-(priorityOf order)", "(priorityOf order)"))
                        else:
                            old, new = '"invalid transition"', '"FAULT transition"'
                        if old not in source[path]:
                            raise RuntimeError("fixed fault no longer matches archived source")
                        source[path] = source[path].replace(old, new)
                    if role != "predecessor" and not structural_development(source, language, task_id)["passed"]:
                        raise RuntimeError("archived fixture violates declared file/order checks")
                    work = base / f"{task_id}-{language}-{role}"
                    work.mkdir()
                    for path, text in source.items():
                        (work / path).write_text(text, encoding="utf-8", newline="\n")
                    project = f"OrderFlow.{ext}proj"
                    env = {"DOTNET_CLI_TELEMETRY_OPTOUT": "1", "DOTNET_NOLOGO": "1", "DOTNET_CLI_UI_LANGUAGE": "en-US"}
                    restore = [p.replace("{project}", project) for p in spec["environment"]["restore"]]
                    restored = run_process(restore, cwd=work, env=env, timeout=60)
                    if not restored.ok:
                        raise RuntimeError("trusted fixture restore failed: " + restored.stdout + restored.stderr)
                    lock = work / "packages.lock.json"
                    if not lock.is_file():
                        raise RuntimeError("restore did not create a lock file")
                    lock_hash = hashlib.sha256(lock.read_bytes()).hexdigest()
                    # Seed an unmistakable stale binary, then remove only the
                    # two resolved build-output paths inside this fresh temp root.
                    stale = work / "bin/Debug/net10.0/OrderFlow.dll"
                    stale.parent.mkdir(parents=True, exist_ok=True)
                    stale.write_bytes(b"E3A STALE OUTPUT MUST NEVER EXECUTE")
                    for rel in ["bin", "obj/Debug"]:
                        target = (work / rel).resolve()
                        if not target.is_relative_to(base) or target == base:
                            raise RuntimeError("unsafe temporary output path")
                        if target.exists():
                            shutil.rmtree(target)
                    built = run_process([p.replace("{project}", project) for p in spec["environment"]["build"]],
                                        cwd=work, env=env, timeout=60)
                    if not built.ok or not stale.is_file() or stale.read_bytes().startswith(b"E3A STALE"):
                        raise RuntimeError("trusted no-restore build failed: " + built.stdout + built.stderr)
                    if lock_hash != hashlib.sha256(lock.read_bytes()).hexdigest():
                        raise RuntimeError("build changed dependency lock")
                    actual_source = {path: (work / path).read_text(encoding="utf-8") for path in source}
                    if actual_source != source:
                        raise RuntimeError("build changed submitted source")
                    suites = {"preflight": development_cases(manifest, s)} if role == "predecessor" else {
                        "development": development_cases(manifest, stage), "holdout": holdout_cases(ROOT, task_id)}
                    outcomes = {}
                    for name, cases in suites.items():
                        process = run_process(spec["environment"]["execute"], cwd=work, env=env, timeout=10,
                                              input_text="".join(json.dumps(c["input"]) + "\n" for c in cases))
                        if not process.ok:
                            raise RuntimeError("trusted fixture program failed: " + process.stderr)
                        actual = [json.loads(line) for line in process.stdout.splitlines()]
                        if len(actual) != len(cases):
                            raise RuntimeError("unexpected line protocol output")
                        failures = [case["name"] for case, value in zip(cases, actual) if value != case["expected"]]
                        outcomes[name] = {"cases": len(cases), "failures": failures}
                    if role == "fault" and not outcomes["holdout"]["failures"]:
                        raise RuntimeError("holdout failed to reject fixed semantic fault")
                    # The old F# priority gold negates Int32.MinValue. Preserve
                    # history and assert this independently detected oracle defect.
                    expected_failure = ["priority-extremes-default-and-ordinal-ties"] if (
                        role == "archived-target" and stage == 1 and language == "fsharp") else []
                    if role != "fault":
                        for name, result in outcomes.items():
                            if result["failures"] != (expected_failure if name == "holdout" else []):
                                raise RuntimeError(f"unexpected trusted fixture result: {task_id} {language} {role} {outcomes}")
                    evidence.append({"task": task_id, "language": language, "role": role,
                                     "source_sha256": canonical_json_hash(source), "lock_sha256": lock_hash,
                                     "binary_sha256": hashlib.sha256(stale.read_bytes()).hexdigest(), "outcomes": outcomes})
    return {"fixture_only": True, "candidate_model_calls": 0, "sandbox_verified": False, "platform": sys.platform,
            "sdk": sdk.stdout.strip(), "builds": len(evidence), "evidence": evidence}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit-packet", action="store_true")
    parser.add_argument("--build-fixtures", action="store_true")
    parser.add_argument("--output", type=Path, help="write generated fixture evidence (not a candidate run)")
    args = parser.parse_args()
    packet = make_packet()
    if args.emit_packet:
        print(json.dumps(packet, indent=2, ensure_ascii=False))
        return
    if packet != read_json(ROOT / PACKET_DIR / "review-packet.json"):
        raise SystemExit("E3a review packet drift; regenerate and review (not a freeze)")
    result = build_fixtures() if args.build_fixtures else {"packet": "matches", "candidate_model_calls": 0}
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
