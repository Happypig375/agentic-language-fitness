from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import ProcessResult
from .process import run_process
from .benchmark_artifacts import check_workspace


def _serialize_process(result: ProcessResult) -> dict[str, Any]:
    data = result.summary()
    data["stdout_tail"] = result.stdout[-4000:]
    data["stderr_tail"] = result.stderr[-4000:]
    return data


def evaluate_project(
    workspace: Path,
    language_config: dict[str, Any],
    cases: list[dict[str, Any]],
    *,
    timeout: float = 180,
    workspace_checks: dict[str, Any] | None = None,
) -> dict[str, Any]:
    project = workspace / language_config["project_file"]
    build = run_process(
        [
            "dotnet",
            "build",
            str(project),
            "--configuration",
            "Release",
            "--no-incremental",
            "--nologo",
        ],
        cwd=workspace,
        timeout=timeout,
        env={"DOTNET_CLI_TELEMETRY_OPTOUT": "1", "DOTNET_NOLOGO": "1"},
    )
    result: dict[str, Any] = {
        "ok": False,
        "build": _serialize_process(build),
        "run": None,
        "case_results": [],
        "workspace_checks": None,
    }
    def apply_workspace_result() -> None:
        if workspace_checks is None:
            return
        try:
            result["workspace_checks"] = check_workspace(workspace, workspace_checks)
        except (OSError, ValueError) as exc:
            result["workspace_checks"] = {"ok": False, "error": str(exc)}
    if not build.ok:
        apply_workspace_result()
        return result

    input_text = "".join(json.dumps(case["input"], separators=(",", ":")) + "\n" for case in cases)
    run = run_process(
        [
            "dotnet",
            "run",
            "--project",
            str(project),
            "--configuration",
            "Release",
            "--no-build",
        ],
        cwd=workspace,
        input_text=input_text,
        timeout=timeout,
        env={"DOTNET_CLI_TELEMETRY_OPTOUT": "1", "DOTNET_NOLOGO": "1"},
    )
    result["run"] = _serialize_process(run)
    if not run.ok:
        apply_workspace_result()
        return result

    lines = [line for line in run.stdout.splitlines() if line.strip()]
    all_ok = len(lines) == len(cases)
    for index, case in enumerate(cases):
        actual: Any = None
        parse_error: str | None = None
        if index < len(lines):
            try:
                actual = json.loads(lines[index])
            except json.JSONDecodeError as exc:
                parse_error = str(exc)
        else:
            parse_error = "missing output line"
        passed = parse_error is None and actual == case["expected"]
        all_ok = all_ok and passed
        result["case_results"].append(
            {
                "name": case["name"],
                "passed": passed,
                "expected": case["expected"],
                "actual": actual,
                "parse_error": parse_error,
            }
        )
    if len(lines) > len(cases):
        result["extra_output_lines"] = lines[len(cases) :]
    if workspace_checks is not None:
        apply_workspace_result()
    result["ok"] = all_ok and (result["workspace_checks"] is None or result["workspace_checks"]["ok"])
    return result
