"""Read-only reconciliation of run artifacts."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .agents.codex import parse_codex_jsonl
from .models import Usage


def _number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value >= 0


def _valid_usage(value: Any) -> bool:
    return isinstance(value, dict) and all(
        isinstance(value.get(name), int) and not isinstance(value.get(name), bool) and value[name] >= 0
        for name in Usage.__dataclass_fields__
    )


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def audit_run(run_dir: Path) -> dict[str, Any]:
    errors: list[str] = []
    try:
        result = _load(run_dir / "result.json")
    except (OSError, json.JSONDecodeError, TypeError) as exc:
        return {"ok": False, "errors": [f"invalid result.json: {exc}"]}
    if not isinstance(result, dict):
        return {"ok": False, "errors": ["invalid result.json: result must be object"]}
    if result.get("require_usage") is True and result.get("agent") != "command":
        errors.append("require_usage is valid only for command runs")
    tasks = result.get("tasks")
    if not isinstance(tasks, list):
        errors.append("tasks must be a list")
        tasks = []
    total = Usage()
    validities: list[bool] = []
    availabilities: list[bool] = []
    invalid_accounting_seen = False
    for embedded in tasks:
        if not isinstance(embedded, dict):
            errors.append("non-object task")
            continue
        task_id = embedded.get("task_id", "?")
        directory = run_dir / "tasks" / str(task_id)
        try:
            task = _load(directory / "task-result.json")
        except (OSError, json.JSONDecodeError, TypeError) as exc:
            errors.append(f"{task_id}: invalid/missing task-result.json: {exc}")
            continue
        if not isinstance(task, dict):
            errors.append(f"{task_id}: task-result must be object")
            continue
        if task != embedded:
            errors.append(f"{task_id}: task-result disagrees with run result")
        agent = task.get("agent") if isinstance(task.get("agent"), dict) else {}
        if not isinstance(task.get("agent"), dict):
            errors.append(f"{task_id}: agent must be object")
        accounting = agent.get("accounting_valid") is True
        available = agent.get("usage_available") is True
        accounting_errors = agent.get("accounting_errors")
        if not isinstance(accounting_errors, list) or not all(isinstance(item, str) for item in accounting_errors):
            errors.append(f"{task_id}: accounting_errors must be a list of strings")
            accounting_errors = []
        if accounting and accounting_errors:
            errors.append(f"{task_id}: valid accounting cannot contain accounting errors")
        if not accounting:
            invalid_accounting_seen = True
            errors.append(f"{task_id}: accounting is invalid")
            if not accounting_errors:
                errors.append(f"{task_id}: invalid accounting requires an actionable error")
            if agent.get("ok") is not False:
                errors.append(f"{task_id}: invalid accounting must make agent.ok false")
            if task.get("success") is not False:
                errors.append(f"{task_id}: invalid accounting must make task success false")
        elif not isinstance(agent.get("ok"), bool):
            errors.append(f"{task_id}: agent.ok must be boolean")
        recorded = agent.get("usage")
        if (accounting and available) != isinstance(recorded, dict):
            errors.append(f"{task_id}: usage null/available flags disagree")
        if isinstance(recorded, dict) and not _valid_usage(recorded):
            errors.append(f"{task_id}: malformed usage values")
        validities.append(accounting)
        availabilities.append(accounting and available)
        sidecar: Any = None
        sidepath = directory / "usage.json"
        if sidepath.is_file():
            try:
                sidecar = _load(sidepath)
                if not isinstance(sidecar, dict):
                    raise ValueError("sidecar must be object")
            except (OSError, json.JSONDecodeError, TypeError, ValueError) as exc:
                errors.append(f"{task_id}: invalid usage sidecar: {exc}")
        elif result.get("agent") == "command" and result.get("require_usage") is True:
            errors.append(f"{task_id}: required usage sidecar is missing")
        elif available:
            errors.append(f"{task_id}: usage sidecar is missing")
        raw = ""
        try:
            if (directory / "agent.stdout").is_file():
                raw = (directory / "agent.stdout").read_text(encoding="utf-8")
        except OSError as exc:
            errors.append(f"{task_id}: cannot read agent.stdout: {exc}")
        derived = isinstance(sidecar, dict) and sidecar.get("derived_from_codex_jsonl") is True
        if derived or result.get("agent") == "codex":
            parsed_events, raw_usage, counts = parse_codex_jsonl(raw)
            if not counts["accounting_valid"]:
                errors.extend(f"{task_id}: raw JSONL: {e}" for e in counts["usage_errors"])
            events_path = directory / "events.jsonl"
            if not events_path.is_file():
                errors.append(f"{task_id}: missing events.jsonl")
            else:
                try:
                    event_lines = [json.loads(line) for line in events_path.read_text(encoding="utf-8").splitlines() if line.strip()]
                    if event_lines != parsed_events:
                        errors.append(f"{task_id}: events.jsonl disagrees with raw stdout")
                except (OSError, json.JSONDecodeError, TypeError) as exc:
                    errors.append(f"{task_id}: invalid events.jsonl: {exc}")
            if recorded != raw_usage.to_dict():
                errors.append(f"{task_id}: raw usage disagrees with task result")
            if result.get("agent") == "codex" and accounting_errors != counts["usage_errors"]:
                errors.append(f"{task_id}: accounting_errors disagree with raw JSONL")
            expected = {"event_count": len(parsed_events), "command_count": counts["commands"], "file_change_count": counts["file_changes"],
                        "failed_event_count": counts["failed_events"], "file_reads": counts["file_reads"], "unique_file_reads": counts["unique_file_reads"], "file_revisits": counts["file_revisits"], "usage_record_count": counts["usage_records"]}
            for key, value in expected.items():
                if agent.get(key) != value:
                    errors.append(f"{task_id}: {key} disagrees with raw JSONL")
            if derived and isinstance(sidecar, dict):
                side_expected = {**expected, **raw_usage.to_dict(), "accounting_valid": counts["accounting_valid"],
                                 "usage_available": counts["usage_records"] > 0 and counts["usage_valid"]}
                for key, value in side_expected.items():
                    if sidecar.get(key) != value:
                        errors.append(f"{task_id}: sidecar {key} disagrees with raw JSONL")
                if "accounting_errors" in sidecar and sidecar["accounting_errors"] != counts["usage_errors"]:
                    errors.append(f"{task_id}: sidecar accounting_errors disagrees with raw JSONL")
                if sidecar.get("usage_errors") != counts["usage_errors"]:
                    errors.append(f"{task_id}: sidecar usage_errors disagrees with raw JSONL")
        if isinstance(sidecar, dict) and isinstance(recorded, dict):
            for name in Usage.__dataclass_fields__:
                if sidecar.get(name) != recorded.get(name):
                    errors.append(f"{task_id}: sidecar usage.{name} disagrees with task result")
        if accounting and available and _valid_usage(recorded):
            total.add(Usage(**{name: recorded[name] for name in Usage.__dataclass_fields__}))
        if not _number(task.get("task_total_wall_seconds")):
            errors.append(f"{task_id}: missing/non-negative task timing")
    expected_valid = bool(validities) and all(validities)
    expected_available = bool(availabilities) and all(availabilities)
    if result.get("aggregate_accounting_valid") is not expected_valid:
        errors.append("aggregate accounting-valid flag disagrees with tasks")
    if result.get("aggregate_usage_available") is not expected_available:
        errors.append("aggregate usage-available flag disagrees with tasks")
    if expected_available:
        if result.get("aggregate_usage") != total.to_dict():
            errors.append("run aggregate_usage does not equal task sum")
    elif result.get("aggregate_usage") is not None:
        errors.append("aggregate_usage must be null when usage unavailable")
    if invalid_accounting_seen and result.get("success") is not False:
        errors.append("invalid task accounting must make run success false")
    for key in ("run_total_wall_seconds", "evaluator_wall_seconds", "agent_process_wall_seconds"):
        if not _number(result.get(key)):
            errors.append(f"missing/non-negative run timing {key}")
    return {"ok": not errors, "errors": errors, "run_id": result.get("run_id")}
