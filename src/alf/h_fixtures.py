"""Trusted-source-only local SDK fixture evaluation for H construction."""
from __future__ import annotations

import hashlib
import copy
import json
import os
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any, Callable, Mapping

from .h_workload import cases_for, source_for
from .protocol import canonical_json_hash

CAPTURE = 1_048_576
CREDENTIAL_MARKERS = ("TOKEN", "SECRET", "API_KEY", "AUTH", "CODEX", "PROXY")


class FixtureError(RuntimeError):
    pass


def credential_free_environment(workspace: Path, environ: Mapping[str, str] | None = None) -> dict[str, str]:
    source = os.environ if environ is None else environ
    result = {key: value for key, value in source.items()
              if not any(marker in key.upper() for marker in CREDENTIAL_MARKERS)}
    result.update({"DOTNET_NOLOGO": "1", "DOTNET_CLI_TELEMETRY_OPTOUT": "1",
                   "DOTNET_CLI_WORKLOAD_UPDATE_NOTIFY_DISABLE": "true",
                   "DOTNET_CLI_HOME": str(workspace / ".dotnet"), "TEMP": str(workspace), "TMP": str(workspace)})
    return result


def mutate_once(source: Mapping[str, str], filename: str, old: str, new: str) -> dict[str, str]:
    if filename not in source or not old or source[filename].count(old) != 1:
        raise FixtureError("trusted mutation selector must match exactly once")
    changed = dict(source)
    changed[filename] = changed[filename].replace(old, new, 1)
    return changed


def _run(argv: list[str], *, cwd: Path, env: Mapping[str, str], timeout: float,
         stdin: bytes | None = None, invoke: Callable[..., Any] = subprocess.run) -> dict[str, Any]:
    try:
        completed = invoke(argv, cwd=cwd, env=dict(env), input=stdin, capture_output=True,
                           timeout=timeout, check=False)
    except subprocess.TimeoutExpired as exc:
        stdout, stderr = exc.stdout or b"", exc.stderr or b""
        return {"returncode": None, "timed_out": True, "overflow": len(stdout) + len(stderr) > CAPTURE,
                "stdout": stdout[:CAPTURE].decode("utf-8", "replace"),
                "stderr": stderr[:CAPTURE].decode("utf-8", "replace")}
    stdout = completed.stdout.encode() if isinstance(completed.stdout, str) else completed.stdout
    stderr = completed.stderr.encode() if isinstance(completed.stderr, str) else completed.stderr
    return {"returncode": completed.returncode, "timed_out": False,
            "overflow": len(stdout) + len(stderr) > CAPTURE,
            "stdout": stdout[:CAPTURE].decode("utf-8", "replace"),
            "stderr": stderr[:CAPTURE].decode("utf-8", "replace")}


def evaluate_trusted(source: Mapping[str, str], cases: list[Mapping[str, Any]], language: str,
                     sdk: str = "10.0.302", *, invoke: Callable[..., Any] = subprocess.run) -> dict[str, Any]:
    project = "OrderFlow.csproj" if language == "csharp" else "OrderFlow.fsproj"
    if project not in source or len(source) > 8 or sum(len(text.encode()) for text in source.values()) > 65_536:
        raise FixtureError("source is outside trusted H fixture scope")
    with tempfile.TemporaryDirectory(prefix="alf-h-fixture-") as temporary:
        workspace = Path(temporary)
        # The fresh directory is intentionally outside the repository, so it
        # cannot inherit the reviewed root global.json. Materialize the same
        # exact SDK selection policy before any dotnet process starts.
        (workspace / "global.json").write_text(json.dumps({"sdk": {
            "version": sdk, "rollForward": "disable", "allowPrerelease": False}},
            indent=2) + "\n", encoding="utf-8", newline="\n")
        for name, text in source.items():
            if Path(name).name != name or "\r" in text or "\x00" in text:
                raise FixtureError("unsafe trusted fixture source")
            (workspace / name).write_text(text, encoding="utf-8", newline="\n")
        env = credential_free_environment(workspace)
        version = _run(["dotnet", "--version"], cwd=workspace, env=env, timeout=10, invoke=invoke)
        if version["returncode"] != 0 or version["timed_out"] or version["overflow"] or version["stdout"].strip() != sdk:
            raise FixtureError("SDK identity mismatch: " + json.dumps({
                "expected": sdk, "observed_stdout": version["stdout"][:4096],
                "observed_stderr": version["stderr"][:4096],
                "returncode": version["returncode"], "timed_out": version["timed_out"],
                "overflow": version["overflow"]}, sort_keys=True))
        build = _run(["dotnet", "build", project, "--configuration", "Debug", "--nologo",
                      "-p:NuGetAudit=false"], cwd=workspace, env=env, timeout=60, invoke=invoke)
        result = {"source_sha256": {name: hashlib.sha256(text.encode()).hexdigest()
                                    for name, text in sorted(source.items())}, "case_count": len(cases),
                  "sdk": sdk, "build": build, "runtime": None, "differences": []}
        if build["returncode"] != 0 or build["timed_out"] or build["overflow"]:
            return {**result, "passed": False, "category": "build"}
        payload = b"".join(json.dumps(case["input"], ensure_ascii=True,
                         separators=(",", ":")).encode() + b"\n" for case in cases)
        dll = workspace / "bin" / "Debug" / "net10.0" / "OrderFlow.dll"
        runtime = _run(["dotnet", str(dll)], cwd=workspace, env=env, timeout=10,
                       stdin=payload, invoke=invoke)
        result["runtime"] = runtime
        if runtime["returncode"] != 0 or runtime["timed_out"] or runtime["overflow"]:
            return {**result, "passed": False, "category": "runtime"}
        lines = runtime["stdout"].splitlines()
        for index, case in enumerate(cases):
            try:
                actual = json.loads(lines[index])
            except (IndexError, json.JSONDecodeError):
                actual = "<missing-or-invalid>"
            if actual != case["expected"]:
                result["differences"].append({"index": index, "name": case["name"], "actual": actual,
                                              "expected": case["expected"]})
        if len(lines) != len(cases):
            result["differences"].append({"line_count": len(lines), "expected_line_count": len(cases)})
        return {**result, "passed": not result["differences"], "category": "semantic"}


def evaluate_fault(source: Mapping[str, str], cases: list[Mapping[str, Any]], language: str,
                   filename: str, old: str, new: str, fault: str, *,
                   invoke: Callable[..., Any] = subprocess.run) -> dict[str, Any]:
    """A fault is caught only by a successful build with a semantic difference."""
    changed = mutate_once(source, filename, old, new)
    result = evaluate_trusted(changed, cases, language, invoke=invoke)
    caught = _semantic_caught(result)
    return {"fault": fault, "mutation": {"file": filename, "old_sha256": hashlib.sha256(old.encode()).hexdigest(),
            "new_sha256": hashlib.sha256(new.encode()).hexdigest()}, "caught": caught, "result": result}


def fault_mutations(language: str, level: str) -> list[tuple[str, str, str, str]]:
    if language == "csharp":
        engine = "OrderFlowEngine.cs"
        program = "Program.cs"
        inclusive_old = "order.DueAt < asOf" if level == "expanded" else "order.DueAt.Value < asOf.Value"
        faults = [
            ("missing-summary-key", program, "JsonSerializer.Serialize(response, Options)",
             "JsonSerializer.Serialize(response, Options).Replace(\"\\\"pending\\\":\", \"\\\"pendingMissing\\\":\")"),
            ("extra-summary-key", program, "JsonSerializer.Serialize(response, Options)",
             "JsonSerializer.Serialize(response, Options).Replace(\"{\", \"{\\\"extra\\\":0,\")"),
            ("case-sensitive-counts", engine, "StringComparison.OrdinalIgnoreCase);", "StringComparison.Ordinal);"),
            ("inclusive-overdue", engine, inclusive_old, inclusive_old.replace(" < ", " <= ")),
            (("subtract-overdue", engine, "pending = all.Count(order => IsStatus(order.Status, \"pending\")),",
              "pending = all.Count(order => IsStatus(order.Status, \"pending\")) - (asOf is null ? 0 : all.Count(order => IsActive(order.Status) && order.DueAt < asOf)),") if level == "expanded" else
             ("subtract-overdue", engine, "overdue++;",
              "overdue++;\n                if (isPending) pending--; else processing--;")),
        ]
        if level == "expanded":
            faults += [("reconcile-corruption", "Reconcile.cs", "Better(value, prior.Value)", "false"),
                       ("dependency-corruption", "DependencyOrder.cs", "StringComparer.Ordinal);\n        var result",
                        "StringComparer.OrdinalIgnoreCase);\n        var result")]
        return faults
    engine = "OrderFlowEngine.fs"
    program = "Program.fs"
    inclusive_old = ("order.dueAt.Value < request.asOf.Value" if level == "expanded"
                     else "order.dueAt.Value < asOf.Value")
    pending_binding = "pendingOrder" if level == "expanded" else "isPending"
    processing_binding = "processingOrder" if level == "expanded" else "isProcessing"
    faults = [
        ("missing-summary-key", program, "Console.WriteLine(JsonSerializer.Serialize(response, options))",
         "Console.WriteLine(JsonSerializer.Serialize(response, options).Replace(\"\\\"pending\\\":\", \"\\\"pendingMissing\\\":\"))"),
        ("extra-summary-key", program, "Console.WriteLine(JsonSerializer.Serialize(response, options))",
         "Console.WriteLine(JsonSerializer.Serialize(response, options).Replace(\"{\", \"{\\\"extra\\\":0,\"))"),
        ("case-sensitive-counts", engine, "StringComparison.OrdinalIgnoreCase)", "StringComparison.Ordinal)"),
        ("inclusive-overdue", engine, inclusive_old, inclusive_old.replace(" < ", " <= ")),
        ("subtract-overdue", engine, "overdueCount <- overdueCount + 1",
         "overdueCount <- overdueCount + 1\n            "
         f"if {pending_binding} then pending <- pending - 1 else if {processing_binding} then processing <- processing - 1"),
    ]
    if level == "expanded":
        faults += [("reconcile-corruption", "ExpandedOperations.fs", "if preferRight then", "if false then"),
                   ("dependency-corruption", "ExpandedOperations.fs", "let ready = SortedSet<string>(StringComparer.Ordinal)",
                    "let ready = SortedSet<string>(StringComparer.OrdinalIgnoreCase)")]
    return faults


def evaluate_with_sandbox(source: Mapping[str, str], cases: list[Mapping[str, Any]], language: str,
                          spec: Mapping[str, Any], baseline: Mapping[str, str], *,
                          fixture_image_id: str | None = None, evaluator_type=None) -> dict[str, Any]:
    if evaluator_type is None:
        from .h_sandbox import HSandboxEvaluator
        evaluator_type = HSandboxEvaluator
    evaluator = evaluator_type(baseline, language, dict(spec), fixture_image_id=fixture_image_id)
    try:
        preparation = evaluator.prepare()
        result = evaluator.evaluate(dict(source), list(cases), time.monotonic() + 600)
        return {"preparation": preparation, **result}
    finally:
        evaluator.close()


def _semantic_caught(result: Mapping[str, Any]) -> bool:
    if result.get("passed") is not False:
        return False
    if result.get("category") == "semantic":
        runtime = result.get("runtime") or {}
        return (result.get("build", {}).get("returncode") == 0
                and runtime.get("returncode") == 0 and not runtime.get("timed_out")
                and not runtime.get("overflow"))
    if result.get("category") != "development" or result.get("build_passed") is not True:
        return False
    operations = result.get("operations")
    if not isinstance(operations, list) or not operations or "program" not in operations[-1]:
        return False
    program = operations[-1]["program"]
    return (program.get("returncode") == 0 and not program.get("timed_out")
            and not program.get("output_limit_exceeded"))


def fault_matrix(root: Path, evaluate: Callable[[Mapping[str, str], list[Mapping[str, Any]], str, str], dict[str, Any]]) -> list[dict[str, Any]]:
    results = []
    for level in ("core", "expanded"):
        for language in ("csharp", "fsharp"):
            predecessor = source_for(root, level, language)
            gold = source_for(root, level, language, True)
            cases = cases_for(root, level, include_summary=True)
            noop = evaluate(predecessor, cases, language, level)
            results.append({"level": level, "language": language, "fault": "unchanged-predecessor",
                            "caught": _semantic_caught(noop), "result": noop})
            for name, filename, old, new in fault_mutations(language, level):
                changed = mutate_once(gold, filename, old, new)
                result = evaluate(changed, cases, language, level)
                caught = _semantic_caught(result)
                results.append({"level": level, "language": language, "fault": name,
                                "caught": caught, "result": result})
    return results


def build_fixtures(root: Path, sdk: str = "10.0.302", *,
                   invoke: Callable[..., Any] = subprocess.run) -> dict[str, Any]:
    targets = []
    for level in ("core", "expanded"):
        for language in ("csharp", "fsharp"):
            for gold in (False, True):
                source = source_for(root, level, language, gold)
                cases = cases_for(root, level, include_summary=gold)
                result = evaluate_trusted(source, cases, language, sdk, invoke=invoke)
                targets.append({"level": level, "language": language,
                                "checkpoint": "gold" if gold else "predecessor", **result})
    faults = fault_matrix(root, lambda source, cases, language, level: evaluate_trusted(
        source, cases, language, sdk, invoke=invoke))
    return {"status": "passed" if all(item["passed"] for item in targets) and all(x["caught"] for x in faults) else "failed",
            "trusted_source_only": True, "candidate_execution": False, "targets": targets, "faults": faults}


def build_sandbox_fixtures(root: Path, spec: Mapping[str, Any], fixture_image_id: str | None = None,
                           *, evaluator_type=None) -> dict[str, Any]:
    original_spec_sha256 = canonical_json_hash(spec)
    effective_spec = copy.deepcopy(dict(spec))
    if fixture_image_id is not None:
        effective_spec["execution_authorized"] = False
        effective_spec["user_live_execution_approved"] = False
        effective_spec["approved_integration_dispatches"] = 0
        effective_spec["approved_pilot_dispatches"] = 0
        effective_spec.setdefault("analysis", {})["human_review_approved"] = False
        effective_spec.setdefault("model", {})["h_live_integration_verified"] = False
    def evaluate(source, cases, language, level):
        baseline = source_for(root, level, language)
        return evaluate_with_sandbox(source, cases, language, effective_spec, baseline,
                                     fixture_image_id=fixture_image_id, evaluator_type=evaluator_type)
    targets = []
    for level in ("core", "expanded"):
        for language in ("csharp", "fsharp"):
            for gold in (False, True):
                result = evaluate(source_for(root, level, language, gold),
                                  cases_for(root, level, include_summary=gold), language, level)
                targets.append({"level": level, "language": language,
                                "checkpoint": "gold" if gold else "predecessor", **result})
    faults = fault_matrix(root, evaluate)
    passed = all(item.get("passed") for item in targets) and all(item["caught"] for item in faults)
    return {"status": "passed" if passed else "failed", "sandbox": True,
            "trusted_source_only": True, "candidate_execution": False,
            "fixture_only": fixture_image_id is not None, "non_experimental": True,
            "original_specification_sha256": original_spec_sha256,
            "effective_live_flags": {key: effective_spec.get(key) for key in
                ("execution_authorized", "user_live_execution_approved",
                 "approved_integration_dispatches", "approved_pilot_dispatches")},
            "targets": targets, "faults": faults}
