"""Read-only reconciliation of run artifacts."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from .agents.codex import parse_codex_jsonl
from .models import Usage
from .representation import CSHARP_KEYWORDS, FSHARP_KEYWORDS, scan_identifiers


def _checkpoint_failure(message: str) -> dict[str, Any]:
    return {
        "ok": False,
        "representation_interpretable": False,
        "include_representation_analysis": False,
        "errors": [message],
        "source_hashes": {},
        "counts": {},
        "observations": [],
    }


def _overdue_alias_is_private_helper(
    data: bytes, language: str, token: str, offset: int
) -> bool:
    """Disambiguate the helper alias from the public summary field."""

    text = data.decode("utf-8", errors="strict")
    char_start = len(data[:offset].decode("utf-8", errors="strict"))
    char_end = char_start + len(token)
    if language == "csharp":
        suffix = text[char_end:]
        match = re.match(r"\s*(.)", suffix, flags=re.DOTALL)
        return bool(match and match.group(1) == "(")
    line_start = text.rfind("\n", 0, char_start) + 1
    line_end = text.find("\n", char_end)
    line_end = len(text) if line_end < 0 else line_end
    line = text[line_start:line_end].strip()
    if line.startswith("let private overdue"):
        return True
    if not line.startswith("overdue"):
        return False
    suffix = line[len("overdue") :].lstrip()
    return bool(suffix and suffix[0] not in "=:")


def _reference_identifier_names(
    artifact_root: Path, treatment: str, language: str, stage: str
) -> set[str]:
    """Load the assigned frozen checkpoint vocabulary without exposing source."""

    checkpoint = artifact_root / "transformed" / treatment / language
    checkpoint = (
        checkpoint / "baseline"
        if stage == "baseline"
        else checkpoint / "gold" / stage
    )
    if not checkpoint.is_dir():
        raise ValueError(f"frozen representation checkpoint is unavailable: {stage}")
    names: set[str] = set()
    for path in sorted(checkpoint.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".cs", ".fs"}:
            continue
        source_language = "csharp" if path.suffix.lower() == ".cs" else "fsharp"
        names.update(row.token for row in scan_identifiers(path.read_bytes(), source_language))
    return names


def audit_representation_checkpoint(
    workspace: Path,
    artifact_root: Path,
    language: str | None = None,
    treatment: str | None = None,
    stage: str = "baseline",
) -> dict[str, Any]:
    """Classify treatment drift without modifying the candidate workspace."""

    if language not in {"csharp", "fsharp"}:
        return _checkpoint_failure(f"unsupported checkpoint language: {language}")
    if treatment not in {"descriptive", "deterministic"}:
        return _checkpoint_failure(f"unsupported representation treatment: {treatment}")
    if not isinstance(stage, str) or not stage:
        return _checkpoint_failure("checkpoint stage must be a non-empty string")

    try:
        mapping = _load(artifact_root / "mapping.json")
        exclusions = _load(artifact_root / "exclusions.json")
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return _checkpoint_failure(f"invalid representation scanner artifact: {exc}")
    if not isinstance(mapping, dict) or not isinstance(mapping.get("roles"), list):
        return _checkpoint_failure("mapping.json must contain a roles list")
    if not isinstance(exclusions, dict):
        return _checkpoint_failure("exclusions.json must contain an object")

    aliases_by_language: dict[str, dict[str, str]] = {"csharp": {}, "fsharp": {}}
    replacement_roles: dict[str, str] = {}
    for index, role in enumerate(mapping["roles"]):
        if not isinstance(role, dict):
            return _checkpoint_failure(f"mapping role {index} must be an object")
        role_id = role.get("role_id")
        source = role.get("source")
        replacement = role.get("replacement")
        if (
            not isinstance(role_id, str)
            or not role_id
            or not isinstance(source, dict)
            or set(source) != {"csharp", "fsharp"}
            or not all(isinstance(source.get(name), str) and source[name] for name in source)
            or not isinstance(replacement, str)
            or not replacement
        ):
            return _checkpoint_failure(f"mapping role {index} is malformed")
        if replacement in replacement_roles:
            return _checkpoint_failure(f"duplicate mapped replacement: {replacement}")
        replacement_roles[replacement] = role_id
        for source_language in ("csharp", "fsharp"):
            aliases_by_language[source_language][source[source_language]] = role_id

    entries = exclusions.get("entries")
    public_by_language = exclusions.get("public_identifiers")
    per_snapshot = exclusions.get("per_snapshot")
    if not isinstance(entries, list):
        return _checkpoint_failure("exclusions.entries must be a list")
    if not isinstance(public_by_language, dict) or not all(
        isinstance(public_by_language.get(name), list)
        and all(isinstance(item, str) for item in public_by_language[name])
        for name in ("csharp", "fsharp")
    ):
        return _checkpoint_failure("exclusions.public_identifiers is malformed")
    if not isinstance(per_snapshot, dict):
        return _checkpoint_failure("exclusions.per_snapshot must be an object")

    try:
        reference_names = _reference_identifier_names(
            artifact_root, treatment, language, stage
        )
    except (OSError, UnicodeError, ValueError) as exc:
        return _checkpoint_failure(f"invalid frozen representation checkpoint: {exc}")

    generally_excluded: set[str] = set()
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict) or not isinstance(entry.get("names"), list):
            return _checkpoint_failure(f"exclusions entry {index} is malformed")
        for name in entry["names"]:
            if not isinstance(name, str):
                return _checkpoint_failure(f"exclusions entry {index} contains a non-string name")
            generally_excluded.update(name.split("/"))

    counts: dict[str, Any] = {
        "mapped_descriptive_aliases": 0,
        "mapped_replacements": 0,
        "reintroduced_aliases": 0,
        "opposite_treatment_names": 0,
        "unclassified_identifiers": 0,
        "roles": {},
    }
    hashes: dict[str, str] = {}
    observations: list[dict[str, Any]] = []
    errors: list[str] = []
    excluded_directories = {".git", ".alf", "bin", "obj", "__pycache__"}
    source_paths = sorted(
        path
        for path in workspace.rglob("*")
        if path.is_file()
        and path.suffix.lower() in {".cs", ".fs"}
        and not excluded_directories.intersection(path.relative_to(workspace).parts)
    )

    for path in source_paths:
        relative = path.relative_to(workspace).as_posix()
        source_language = "csharp" if path.suffix.lower() == ".cs" else "fsharp"
        try:
            data = path.read_bytes()
            rows = scan_identifiers(data, source_language)
        except Exception as exc:  # scanner exceptions are protocol failures
            errors.append(f"scanner failure: {relative}: {exc}")
            continue
        hashes[relative] = hashlib.sha256(data).hexdigest()

        snapshot_relative = (
            f"baseline/{relative}" if stage == "baseline" else f"gold/{stage}/{relative}"
        )
        snapshot_key = f"{source_language}:{snapshot_relative}"
        snapshot_rows = per_snapshot.get(snapshot_key, [])
        if not isinstance(snapshot_rows, list):
            errors.append(f"malformed per-snapshot exclusion list: {snapshot_key}")
            continue
        snapshot_excluded = {
            item["identifier"]
            for item in snapshot_rows
            if isinstance(item, dict) and isinstance(item.get("identifier"), str)
        }
        if len(snapshot_excluded) != len(snapshot_rows):
            errors.append(f"malformed per-snapshot exclusion entry: {snapshot_key}")
            continue

        aliases = aliases_by_language[source_language]
        keywords = CSHARP_KEYWORDS if source_language == "csharp" else FSHARP_KEYWORDS
        public_names = set(public_by_language[source_language])
        for row in rows:
            token = row.token
            role_id = replacement_roles.get(token) or aliases.get(token)
            occurrence = {"path": relative, "offset": row.offset, "name": token}

            if token in replacement_roles:
                role = counts["roles"].setdefault(
                    replacement_roles[token],
                    {"replacement": 0, "alias": 0, "occurrences": []},
                )
                role["replacement"] += 1
                role["occurrences"].append({**occurrence, "kind": "replacement"})
                counts["mapped_replacements"] += 1
                if treatment == "descriptive":
                    counts["opposite_treatment_names"] += 1
                    observations.append({**occurrence, "kind": "opposite_treatment"})
                continue

            if token in aliases:
                if token in snapshot_excluded:
                    continue
                if role_id == "helper.overdue" and not _overdue_alias_is_private_helper(
                    data, source_language, token, row.offset
                ):
                    # The public SummaryResponse field intentionally keeps this
                    # spelling in both treatments.
                    continue
                role = counts["roles"].setdefault(
                    role_id,
                    {"replacement": 0, "alias": 0, "occurrences": []},
                )
                role["alias"] += 1
                role["occurrences"].append({**occurrence, "kind": "alias"})
                counts["mapped_descriptive_aliases"] += 1
                if treatment == "deterministic":
                    counts["reintroduced_aliases"] += 1
                    counts["opposite_treatment_names"] += 1
                    observations.append({**occurrence, "kind": "reintroduced_alias"})
                continue

            if treatment == "descriptive" and token.startswith(
                ("loc_", "mem_", "typ_", "fun_")
            ):
                counts["opposite_treatment_names"] += 1
                observations.append({**occurrence, "kind": "opposite_treatment"})
                continue

            if (
                token not in keywords
                and token not in public_names
                and token not in generally_excluded
                and token not in snapshot_excluded
                and token not in reference_names
                and len(token) > 1
            ):
                counts["unclassified_identifiers"] += 1
                observations.append({**occurrence, "kind": "unclassified"})

    interpretable = not errors and counts["opposite_treatment_names"] == 0
    return {
        "ok": not errors,
        "representation_interpretable": interpretable,
        "include_representation_analysis": interpretable,
        "errors": errors,
        "source_hashes": hashes,
        "counts": counts,
        "observations": observations,
    }


representation_checkpoint_audit = audit_representation_checkpoint


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
    monitored = isinstance(result.get("provenance"), dict) and result["provenance"].get("cell_id") == "difficulty-v1"
    if monitored:
        try:
            baseline_audit = _load(run_dir / "representation-audit.json")
            if baseline_audit != result.get("representation_audit"): errors.append("baseline representation audit disagrees with embedded report")
        except (OSError, json.JSONDecodeError, TypeError) as exc:
            errors.append(f"missing/invalid baseline representation audit: {exc}")
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
        if monitored:
            try:
                checkpoint = _load(directory / "representation-audit.json")
                if checkpoint != embedded.get("representation_audit"): errors.append(f"{task_id}: representation audit disagrees with embedded report")
            except (OSError, json.JSONDecodeError, TypeError) as exc:
                errors.append(f"{task_id}: missing/invalid representation audit: {exc}")
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
    if monitored:
        # Import lazily because runner uses this module for checkpoint scanning.
        # The persisted disposition must still reconcile with the same frozen,
        # deterministic classifier used before predecessor/retry decisions.
        from .runner import _derive_protocol_disposition

        expected_disposition = _derive_protocol_disposition(result)
        if result.get("disposition") != expected_disposition:
            errors.append("frozen disposition disagrees with derived runner classification")
    return {"ok": not errors, "errors": errors, "run_id": result.get("run_id")}
