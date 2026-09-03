"""Report synthesis, privacy validation, and raw-evidence audit for E2."""
from __future__ import annotations

from collections import defaultdict
import json
import math
import re
import statistics
from pathlib import Path
from typing import Any, Iterable

from .protocol import canonical_json_hash
from .workstream_e2 import (
    ABSOLUTE_WINDOWS_RE,
    ATTEMPT_SCHEMA,
    CHECK_KEYS,
    E2RunError,
    ENVIRONMENT_PROFILE,
    HEX_40_RE,
    HEX_64_RE,
    LANGUAGES,
    RAW_INVENTORY_SCHEMA,
    REPORT_SCHEMA,
    ROUNDS,
    STAGES,
    _atomic_bytes,
    _atomic_json,
    _canonical_bytes,
    _safe_relative,
    _sha,
)


def inventory(directory: Path, *, exclude: Iterable[str] = ()) -> dict[str, Any]:
    excluded = set(exclude)
    files: list[dict[str, Any]] = []
    for path in sorted(directory.rglob("*")):
        relative = path.relative_to(directory).as_posix()
        if relative in excluded:
            continue
        if path.is_symlink():
            raise E2RunError("evidence_or_cache_symlink_forbidden")
        if not path.is_file():
            continue
        raw = path.read_bytes()
        files.append({"path": relative, "bytes": len(raw), "sha256": _sha(raw)})
    return {
        "files": files,
        "file_count": len(files),
        "total_bytes": sum(row["bytes"] for row in files),
        "set_sha256": _sha(_canonical_bytes(files)),
    }


def inventory_summary(value: dict[str, Any]) -> dict[str, Any]:
    return {key: value[key] for key in ("file_count", "total_bytes", "set_sha256")}


def write_raw_inventory(raw: Path) -> dict[str, Any]:
    value = inventory(raw, exclude={"raw-inventory.json", "terminal-attempt.json"})
    document = {"schema_version": RAW_INVENTORY_SCHEMA, **value}
    document["inventory_sha256"] = canonical_json_hash(document)
    _atomic_json(raw / "raw-inventory.json", document)
    return document


def _stats(values: list[float | int]) -> dict[str, Any]:
    if not values:
        raise ValueError("cannot summarize an empty distribution")
    ordered = sorted(values)
    return {
        "count": len(ordered),
        "min": ordered[0],
        "median": statistics.median(ordered),
        "mean": statistics.fmean(ordered),
        "p95": ordered[max(0, math.ceil(len(ordered) * 0.95) - 1)],
        "max": ordered[-1],
    }


def distributions(samples: list[dict[str, Any]]) -> dict[str, Any]:
    operation_groups: dict[tuple[str, int, str, str], dict[str, list[float | int]]] = defaultdict(
        lambda: {"wall_seconds": [], "output_bytes": [], "warning_count": []}
    )
    composite_groups: dict[tuple[str, int, str], list[float]] = defaultdict(list)
    artifact_groups: dict[tuple[str, int, str], list[int]] = defaultdict(list)
    for sample in samples:
        for key in ("fresh", "repeat"):
            regime = sample[key]
            group = (sample["language"], sample["stage"], regime["regime"])
            composite_groups[group].append(regime["composite_wall_seconds"])
            artifact_groups[group].append(regime["artifact"]["bytes"])
            for operation in regime["operations"]:
                op_group = (*group, operation["operation"])
                operation_groups[op_group]["wall_seconds"].append(operation["wall_seconds"])
                operation_groups[op_group]["output_bytes"].append(
                    operation["stdout"]["bytes"] + operation["stderr"]["bytes"]
                )
                operation_groups[op_group]["warning_count"].append(operation["warnings"]["count"])

    operations = [
        {
            "language": language,
            "stage": stage,
            "regime": regime,
            "operation": operation,
            **{field: _stats(items) for field, items in values.items()},
        }
        for (language, stage, regime, operation), values in sorted(operation_groups.items())
    ]
    composites = [
        {
            "language": key[0],
            "stage": key[1],
            "regime": key[2],
            "wall_seconds": _stats(values),
        }
        for key, values in sorted(composite_groups.items())
    ]
    artifacts = [
        {
            "language": key[0],
            "stage": key[1],
            "regime": key[2],
            "bytes": _stats(values),
        }
        for key, values in sorted(artifact_groups.items())
    ]
    return {"operations": operations, "composites": composites, "artifacts": artifacts}


def _walk_json(value: Any, path: tuple[str, ...] = ()) -> Iterable[tuple[tuple[str, ...], Any]]:
    yield path, value
    if isinstance(value, dict):
        for key, child in value.items():
            yield from _walk_json(child, (*path, str(key)))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _walk_json(child, (*path, str(index)))


def validate_report(report: dict[str, Any], definition: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    expected_top_level = {
        "schema_version",
        "definition_sha256",
        "schedule_sha256",
        "runner_git_sha",
        "container_image_id",
        "environment",
        "package_cache",
        "raw_evidence",
        "preflight",
        "states",
        "samples",
        "distributions",
        "missingness",
        "report_sha256",
    }
    if set(report) != expected_top_level:
        errors.append("report top-level schema mismatch")
    if report.get("schema_version") != REPORT_SCHEMA:
        errors.append("report schema mismatch")
    claimed = report.get("report_sha256")
    unsigned = dict(report)
    unsigned.pop("report_sha256", None)
    if not isinstance(claimed, str) or not HEX_64_RE.fullmatch(claimed):
        errors.append("report_sha256 must be lowercase SHA-256")
    elif claimed != canonical_json_hash(unsigned):
        errors.append("report self-hash mismatch")
    if report.get("definition_sha256") != definition.get("definition_sha256"):
        errors.append("report definition identity mismatch")
    if report.get("schedule_sha256") != definition.get("schedule_sha256"):
        errors.append("report schedule identity mismatch")
    if not isinstance(report.get("runner_git_sha"), str) or not HEX_40_RE.fullmatch(
        report.get("runner_git_sha", "")
    ):
        errors.append("report runner identity invalid")
    image = report.get("container_image_id")
    if not isinstance(image, str) or not image.startswith("sha256:") or not HEX_64_RE.fullmatch(image[7:]):
        errors.append("report container identity invalid")
    if report.get("states") != definition.get("states"):
        errors.append("report static states differ from definition")
    environment = report.get("environment", {})
    if not isinstance(environment, dict) or environment.get("profile") != ENVIRONMENT_PROFILE:
        errors.append("report environment profile mismatch")
    if report.get("preflight") != {"state_count": 18, "all_passed": True, "mode": "static-only"}:
        errors.append("report preflight summary invalid")

    cache = report.get("package_cache", {})
    if (
        not isinstance(cache, dict)
        or set(cache) != {"before", "after", "unchanged"}
        or cache.get("before") != cache.get("after")
        or cache.get("unchanged") is not True
    ):
        errors.append("report package-cache identity invalid")
    raw_evidence = report.get("raw_evidence", {})
    if (
        not isinstance(raw_evidence, dict)
        or set(raw_evidence) != {"inventory_path", "inventory_sha256", "file_count", "total_bytes"}
        or raw_evidence.get("inventory_path") != "raw-inventory.json"
        or not isinstance(raw_evidence.get("inventory_sha256"), str)
        or not HEX_64_RE.fullmatch(raw_evidence.get("inventory_sha256", ""))
        or not isinstance(raw_evidence.get("file_count"), int)
        or raw_evidence.get("file_count", 0) <= 0
        or not isinstance(raw_evidence.get("total_bytes"), int)
        or raw_evidence.get("total_bytes", -1) < 0
    ):
        errors.append("report raw-evidence identity invalid")

    states = {
        (state.get("language"), state.get("stage")): state
        for state in definition.get("states", [])
        if isinstance(state, dict)
    }
    samples = report.get("samples")
    if not isinstance(samples, list) or len(samples) != ROUNDS * STAGES * len(LANGUAGES):
        errors.append("report must contain exactly 90 samples")
    else:
        schedule_keys = ("position", "round", "pair_position", "stage", "language", "language_position")
        observed_schedule = [{key: sample.get(key) for key in schedule_keys} for sample in samples]
        if observed_schedule != definition.get("schedule"):
            errors.append("report sample order differs from frozen schedule")
        for sample in samples:
            if set(sample) != {*schedule_keys, "state_id", "fresh", "repeat"}:
                errors.append("sample schema mismatch")
            state = states.get((sample.get("language"), sample.get("stage")))
            if state is None or sample.get("state_id") != state.get("state_id"):
                errors.append("sample state identity mismatch")
                continue
            expanded = definition["commands"]["expanded_by_language"][sample["language"]]
            for key, expected_sequence in (
                ("fresh", ["restore", "build", "run"]),
                ("repeat", ["build", "run"]),
            ):
                regime = sample.get(key, {})
                if not isinstance(regime, dict) or set(regime) != {
                    "regime",
                    "operations",
                    "evaluator",
                    "composite_wall_seconds",
                    "artifact",
                    "load_before",
                    "load_after",
                }:
                    errors.append(f"{key} regime schema mismatch")
                    continue
                if regime.get("regime") != f"{key}-workspace":
                    errors.append(f"{key} regime name mismatch")
                operations = regime.get("operations", [])
                if [row.get("operation") for row in operations] != expected_sequence:
                    errors.append(f"{key} command sequence mismatch")
                for operation, expected_name in zip(operations, expected_sequence):
                    if not isinstance(operation, dict) or set(operation) != {
                        "operation",
                        "argv",
                        "timeout_seconds",
                        "wall_seconds",
                        "timed_out",
                        "exit_code",
                        "stdout",
                        "stderr",
                        "warnings",
                        "metadata_path",
                    }:
                        errors.append("operation schema mismatch")
                        continue
                    if operation.get("operation") != expected_name or operation.get("argv") != expanded[expected_name]:
                        errors.append("operation identity/argv mismatch")
                    if operation.get("exit_code") != 0 or operation.get("timed_out") is not False:
                        errors.append("published operation was not successful")
                    for stream in ("stdout", "stderr"):
                        value = operation.get(stream, {})
                        if not isinstance(value, dict) or set(value) != {"path", "bytes", "sha256"}:
                            errors.append("operation stream schema mismatch")
                        else:
                            try:
                                if _safe_relative(value["path"], label="raw stream path") != value["path"]:
                                    errors.append("operation stream path is not canonical")
                            except (KeyError, TypeError, ValueError):
                                errors.append("operation stream path is unsafe")
                    try:
                        if (
                            _safe_relative(operation["metadata_path"], label="raw metadata path")
                            != operation["metadata_path"]
                        ):
                            errors.append("operation metadata path is not canonical")
                    except (KeyError, TypeError, ValueError):
                        errors.append("operation metadata path is unsafe")
                evaluator = regime.get("evaluator", {})
                if (
                    not isinstance(evaluator, dict)
                    or set(evaluator)
                    != {"ok", "case_count", "passed_case_count", "workspace_check_counts", "wall_seconds"}
                    or evaluator.get("ok") is not True
                    or evaluator.get("case_count") != state["case_count"]
                    or evaluator.get("passed_case_count") != state["case_count"]
                    or evaluator.get("workspace_check_counts") != state["workspace_checks"]["counts"]
                ):
                    errors.append("evaluator summary differs from frozen state")

    forbidden_keys = {
        "input",
        "expected",
        "actual",
        "source_text",
        "stdout_text",
        "stderr_text",
        "hostname",
        "environment_variables",
        "prompt",
        "transcript",
    }
    for path, value in _walk_json(report):
        if path and path[-1].casefold() in forbidden_keys:
            errors.append(f"forbidden publishable field: {'.'.join(path)}")
        if isinstance(value, float) and not math.isfinite(value):
            errors.append(f"non-finite numeric value: {'.'.join(path)}")
        if isinstance(value, str):
            if value.startswith("/") or ABSOLUTE_WINDOWS_RE.match(value):
                errors.append(f"absolute path in report: {'.'.join(path)}")
            lowered = value.casefold()
            if "bearer " in lowered or re.search(r"\bsk-[a-z0-9_-]{8,}", lowered):
                errors.append(f"credential-like value in report: {'.'.join(path)}")

    grouped = report.get("distributions", {})
    if (
        not isinstance(grouped, dict)
        or set(grouped) != {"operations", "composites", "artifacts"}
        or len(grouped.get("operations", [])) != 90
        or len(grouped.get("composites", [])) != 36
        or len(grouped.get("artifacts", [])) != 36
    ):
        errors.append("report distributions are incomplete")
    missingness = report.get("missingness", {})
    expected_missing = {"internal_compiler_phase_timing", "observed_compiler_inputs", "machine_cold_state"}
    if not isinstance(missingness, dict) or set(missingness) != expected_missing:
        errors.append("report missingness ledger is incomplete")
    else:
        for entry in missingness.values():
            if not isinstance(entry, dict) or set(entry) != {"value", "reason"} or entry.get("value") is not None:
                errors.append("report missingness entry invalid")
    return {"ok": not errors, "errors": sorted(set(errors)), "report_sha256": claimed}


def markdown_report(report: dict[str, Any]) -> str:
    lines = [
        "# Workstream E2 model-free baseline",
        "",
        f"Definition: `{report['definition_sha256']}`",
        f"Runner: `{report['runner_git_sha']}`",
        f"Container: `{report['container_image_id']}`",
        f"Samples: {len(report['samples'])} (five paired rounds; fresh and immediate repeat)",
        "",
        "## Operation timing summaries",
        "",
        "| Language | Stage | Regime | Operation | n | Mean seconds | Median seconds |",
        "|---|---:|---|---|---:|---:|---:|",
    ]
    for row in report["distributions"]["operations"]:
        timing = row["wall_seconds"]
        lines.append(
            f"| {row['language']} | {row['stage']} | {row['regime']} | {row['operation']} | "
            f"{timing['count']} | {timing['mean']:.6f} | {timing['median']:.6f} |"
        )
    lines.extend(
        [
            "",
            "Internal compiler phases and observed compiler inputs are unavailable; the report records static source/project obligations instead.",
            "The OS page cache was neither cleared nor controlled, so the regimes are named fresh-workspace and repeat-workspace.",
            "",
        ]
    )
    return "\n".join(lines)


def attempt_document(attempt: dict[str, Any]) -> dict[str, Any]:
    document = {"schema_version": ATTEMPT_SCHEMA, **attempt}
    document["attempt_sha256"] = canonical_json_hash(document)
    return document


def write_attempt(raw: Path, attempt: dict[str, Any]) -> None:
    _atomic_json(raw / "terminal-attempt.json", attempt_document(attempt))


def failure_identity(exc: BaseException) -> dict[str, Any]:
    code = exc.code if isinstance(exc, E2RunError) else "unexpected_error"
    return {
        "code": code,
        "type": type(exc).__name__,
        "detail_sha256": _sha(str(exc).encode("utf-8", errors="replace")),
    }


def publish_report(report: dict[str, Any], json_path: Path, markdown_path: Path) -> None:
    """Publish Markdown first and JSON last as the authoritative success marker."""

    try:
        _atomic_bytes(markdown_path, markdown_report(report).encode("utf-8"))
        _atomic_json(json_path, report)
    except BaseException:
        markdown_path.unlink(missing_ok=True)
        json_path.unlink(missing_ok=True)
        raise


def _self_hash(document: dict[str, Any], field: str) -> bool:
    claimed = document.get(field)
    unsigned = dict(document)
    unsigned.pop(field, None)
    return isinstance(claimed, str) and HEX_64_RE.fullmatch(claimed) is not None and claimed == canonical_json_hash(unsigned)


def audit_report(report: dict[str, Any], definition: dict[str, Any], raw: Path) -> dict[str, Any]:
    """Verify report -> raw inventory -> exact raw files and terminal attempt."""

    errors = list(validate_report(report, definition)["errors"])
    try:
        raw_inventory = json.loads((raw / "raw-inventory.json").read_text(encoding="utf-8"))
        if not isinstance(raw_inventory, dict) or raw_inventory.get("schema_version") != RAW_INVENTORY_SCHEMA:
            errors.append("raw inventory schema mismatch")
        elif not _self_hash(raw_inventory, "inventory_sha256"):
            errors.append("raw inventory self-hash mismatch")
        else:
            observed = inventory(raw, exclude={"raw-inventory.json", "terminal-attempt.json"})
            expected = {key: raw_inventory.get(key) for key in ("files", "file_count", "total_bytes", "set_sha256")}
            if observed != expected:
                errors.append("raw inventory files differ from disk")
            if report.get("raw_evidence", {}).get("inventory_sha256") != raw_inventory["inventory_sha256"]:
                errors.append("report raw inventory identity mismatch")
            if report.get("raw_evidence", {}).get("file_count") != raw_inventory["file_count"]:
                errors.append("report raw inventory count mismatch")
            if report.get("raw_evidence", {}).get("total_bytes") != raw_inventory["total_bytes"]:
                errors.append("report raw inventory byte count mismatch")
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        errors.append(f"raw inventory unavailable: {type(exc).__name__}")

    try:
        terminal = json.loads((raw / "terminal-attempt.json").read_text(encoding="utf-8"))
        if (
            not isinstance(terminal, dict)
            or terminal.get("schema_version") != ATTEMPT_SCHEMA
            or not _self_hash(terminal, "attempt_sha256")
            or terminal.get("status") != "success"
            or terminal.get("report_sha256") != report.get("report_sha256")
            or terminal.get("raw_inventory_sha256") != report.get("raw_evidence", {}).get("inventory_sha256")
        ):
            errors.append("terminal attempt identity mismatch")
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        errors.append(f"terminal attempt unavailable: {type(exc).__name__}")

    inventory_rows = {
        row.get("path"): row
        for row in raw_inventory.get("files", [])
        if isinstance(raw_inventory, dict) and isinstance(row, dict)
    } if "raw_inventory" in locals() and isinstance(raw_inventory, dict) else {}
    for sample in report.get("samples", []):
        for regime_name in ("fresh", "repeat"):
            for operation in sample.get(regime_name, {}).get("operations", []):
                for stream_name in ("stdout", "stderr"):
                    stream = operation.get(stream_name, {})
                    row = inventory_rows.get(stream.get("path"))
                    if row is None or row.get("bytes") != stream.get("bytes") or row.get("sha256") != stream.get("sha256"):
                        errors.append("operation stream differs from raw inventory")
                metadata_path = operation.get("metadata_path")
                try:
                    safe_metadata_path = _safe_relative(metadata_path, label="raw metadata path")
                    raw_metadata = json.loads((raw / safe_metadata_path).read_text(encoding="utf-8"))
                    expected_metadata = dict(operation)
                    expected_metadata.pop("metadata_path", None)
                    if raw_metadata != expected_metadata or safe_metadata_path not in inventory_rows:
                        errors.append("operation metadata differs from report/inventory")
                except (OSError, TypeError, ValueError, UnicodeError, json.JSONDecodeError):
                    errors.append("operation metadata unavailable")
    return {"ok": not errors, "errors": sorted(set(errors)), "report_sha256": report.get("report_sha256")}
