"""Workstream E2a: authenticated command inventory and aligned model-free replay.

E2a is deliberately separate from the accepted E2 ecology. It authenticates
the retained E1 archive, publishes only a redacted semantic command inventory,
and replays those forms without starting Codex, a candidate, or a model call.
Raw argv and command output remain in an external evidence directory.
"""
from __future__ import annotations

from collections import Counter, defaultdict
import hashlib
import json
import math
import os
import re
import statistics
import subprocess
import tempfile
import time
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, IO

from .benchmark_artifacts import check_workspace
from .config import load_manifest
from .protocol import canonical_json_hash, tracked_text_sha256
from .workstream_e import (
    EXPECTED_TASK_IDS,
    _atom_words,
    _read_events,
    _scan_payload,
    _unwrap_bash,
    classify_command,
    diagnostics,
    validate_public_report,
)
from .workstream_e2 import (
    CHECK_KEYS,
    HEX_40_RE,
    HEX_64_RE,
    _atomic_bytes,
    _atomic_json,
    _canonical_bytes,
    _compile_obligations,
    _cumulative_checks,
    _included_source,
    _inside,
    _materialize,
    _normalise_text,
    _resolve,
    _safe_relative,
    _sha,
)
from .workstream_e2_report import inventory as raw_file_inventory
from .workstream_e2_runner import _evaluate_output


INVENTORY_SCHEMA = "alf.workstream-e2a.inventory.v1"
DEFINITION_SCHEMA = "alf.workstream-e2a.definition.v1"
ENVIRONMENT_SCHEMA = "alf.workstream-e2a.environment-observation.v1"
MEASUREMENT_SCHEMA = "alf.workstream-e2a.measurement.v1"
REPORT_SCHEMA = "alf.workstream-e2a.report.v1"
RAW_INVENTORY_SCHEMA = "alf.workstream-e2a.raw-inventory.v1"
ATTEMPT_SCHEMA = "alf.workstream-e2a.attempt.v1"

EXPECTED_COMPLETED_COMMANDS = 435
EXPECTED_BENCHMARK_DOTNET_OPERATIONS = 258
EXPECTED_DOTNET_ENVIRONMENT_QUERIES = 7
EXPECTED_OPERATION_TOTALS = {
    "restore": 14,
    "build": 119,
    "run": 120,
    "test": 4,
    "direct": 1,
}
EXPECTED_NU1900 = {
    ("H", "csharp"): 0,
    ("H", "fsharp"): 41,
    ("L", "csharp"): 0,
    ("L", "fsharp"): 88,
    ("M", "csharp"): 0,
    ("M", "fsharp"): 68,
}
EXPECTED_RUN_COUNTS = {
    ("H", "csharp"): 1,
    ("H", "fsharp"): 1,
    ("L", "csharp"): 2,
    ("L", "fsharp"): 2,
    ("M", "csharp"): 2,
    ("M", "fsharp"): 2,
}

ROUNDS = 5
SCHEDULE_SEED = "alf-workstream-e2a-exact-command-paired-v1"
COMMAND_TIMEOUT_SECONDS = 300

PROFILE_ID = "remote-highmem-local-egress-r1"
RUNNER_PROFILE_ID = "runner-remote-highmem-local-egress-r1"
V3_RUNNER_GIT_SHA = "b180ed938b6286764e06ffee85a86381e8a14850"
V3_IMAGE_ID = "sha256:5d3e97d195dbbe7e47e47055e46f8c6f15fb9553be0c7ef19ed0060756fc7116"
V3_IMAGE_ARCHIVE_SHA256 = "55ee85f0656cef429d1cd40edced79782d54abb7b2180c9770c14bea06828ddf"
V3_IMAGE_ARCHIVE_BYTES = 630_053_888
DOTNET_SDK = "10.0.302"

ACCEPTED_E2_DEFINITION_SHA256 = "09d5669fd554e611b4df505454a40f06a0e9b2a23c4a16a28c9cc94d640067f7"
ACCEPTED_E2_SCHEDULE_SHA256 = "c6915378561201778e6cfdc139bd9deff0cb58d7621da3e45b5ec8dda27c37e1"
ACCEPTED_E2_REPORT_SHA256 = "2e4381ab67dd4cc7aed24c323e8edbd30bf83dd29bafc58554615bcd6f24c49a"
ACCEPTED_E2_ENVIRONMENT_PROFILE = "github-actions-ubuntu-24.04-dotnet10.0.302-offline-v1"
ACCEPTED_MANIFEST_SHA256 = "dd440baf352a3b33adc625d478df44424efb1069e1a479d2fbe8f086044a6f0d"
ACCEPTED_E2_REFERENCE_SHA256 = "2b59b04ffbc066eb8a9942198b77bee8116e4ce54f5f0d67157dd68302eb0fcc"

FORM_FLAG_ORDER = (
    "--ignore-failed-sources",
    "--no-build",
    "--no-restore",
    "--no-incremental",
    "--nologo",
)
OPERATIONS = tuple(EXPECTED_OPERATION_TOTALS)
LANGUAGES = ("csharp", "fsharp")
CONFIGURATIONS = ("H", "L", "M")
PINNED_IMAGE_ENVIRONMENT = {
    "PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
    "APP_UID": "1654",
    "ASPNETCORE_HTTP_PORTS": "8080",
    "DOTNET_RUNNING_IN_CONTAINER": "true",
    "DOTNET_VERSION": "10.0.10",
    "ASPNET_VERSION": "10.0.10",
    "DOTNET_GENERATE_ASPNET_CERTIFICATE": "false",
    "DOTNET_NOLOGO": "true",
    "DOTNET_SDK_VERSION": "10.0.302",
    "DOTNET_USE_POLLING_FILE_WATCHER": "true",
    "NUGET_XMLDOC_MODE": "skip",
    "POWERSHELL_DISTRIBUTION_CHANNEL": "PSDocker-DotnetSDK-Ubuntu-24.04",
}

_NU1900_RE = re.compile(r"\bNU1900\b", re.IGNORECASE)
_REDIRECTION_TOKEN_RE = re.compile(r"^\d*(?:<|>|>>|<>|<<<|<<)")
_ABSOLUTE_WINDOWS_RE = re.compile(r"^[A-Za-z]:[\\/]")
_CREDENTIAL_RE = re.compile(r"\b(?:sk-[A-Za-z0-9_-]{8,}|Bearer\s+\S+)", re.IGNORECASE)


class E2aError(RuntimeError):
    """Bounded E2a failure whose message is safe to publish or log."""

    def __init__(self, code: str):
        if re.fullmatch(r"[a-z0-9_]+", code) is None:
            code = "unexpected_error"
        self.code = code
        super().__init__(code)


def _require(condition: bool, code: str) -> None:
    if not condition:
        raise E2aError(code)


def _json_object(path: Path, code: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        raise E2aError(code) from None
    if not isinstance(value, dict):
        raise E2aError(code)
    return value


def _self_hash(document: dict[str, Any], field: str) -> bool:
    claimed = document.get(field)
    unsigned = dict(document)
    unsigned.pop(field, None)
    return (
        isinstance(claimed, str)
        and HEX_64_RE.fullmatch(claimed) is not None
        and claimed == canonical_json_hash(unsigned)
    )


def _finish_hash(document: dict[str, Any], field: str) -> dict[str, Any]:
    result = dict(document)
    result[field] = canonical_json_hash(result)
    return result


# These are derived summaries whose floating-point reductions can differ by a
# tiny amount across Python versions.  Everything else in a report remains an
# exact, type-sensitive comparison (including identities and hashes).
_DERIVED_SUMMARY_FIELDS = frozenset({
    "absolute_distributions",
    "paired_language_effects",
    "audit_contrasts",
    "mechanical_tool_exposure_envelope",
})


def _json_equal_exact(left: Any, right: Any) -> bool:
    """Compare JSON-like values exactly, including scalar types."""

    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return (
            set(left) == set(right)
            and all(_json_equal_exact(left[key], right[key]) for key in left)
        )
    if isinstance(left, list):
        return len(left) == len(right) and all(
            _json_equal_exact(a, b) for a, b in zip(left, right)
        )
    return left == right


def _derived_json_equal(left: Any, right: Any) -> bool:
    """Compare one approved derived section with tightly bounded float drift."""

    if isinstance(left, float) or isinstance(right, float):
        return (
            isinstance(left, float)
            and isinstance(right, float)
            and math.isfinite(left)
            and math.isfinite(right)
            and math.isclose(left, right, rel_tol=1e-12, abs_tol=1e-12)
        )
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return (
            set(left) == set(right)
            and all(_derived_json_equal(left[key], right[key]) for key in left)
        )
    if isinstance(left, list):
        return len(left) == len(right) and all(
            _derived_json_equal(a, b) for a, b in zip(left, right)
        )
    return left == right


def _report_recomputation_equal(actual: dict[str, Any], expected: dict[str, Any]) -> bool:
    """Compare rebuilt reports, tolerating only approved derived summaries."""

    if set(actual) != set(expected):
        return False
    # A genuine rebuild incorporates any tolerated derived-float drift into
    # its own checksum.  Validate each document independently, while keeping
    # all other identity/non-derived fields exact.
    if not _self_hash(actual, "report_sha256") or not _self_hash(expected, "report_sha256"):
        return False
    return all(
        (_derived_json_equal(actual[key], expected[key]) if key in _DERIVED_SUMMARY_FIELDS
         else True if key == "report_sha256" else _json_equal_exact(actual[key], expected[key]))
        for key in actual
    )


def _normalise_language(value: Any) -> str:
    language = str(value).casefold()
    _require(language in LANGUAGES, "e1_language_invalid")
    return language


def _normalise_configuration(value: Any) -> str:
    configuration = str(value).upper()
    _require(configuration in CONFIGURATIONS, "e1_configuration_invalid")
    return configuration


def _event_roster_hash(digests: Iterable[str]) -> str:
    return _sha(_canonical_bytes(sorted(digests)))


def _strip_redirection_words(words: list[str]) -> list[str]:
    """Remove shell redirection syntax after E1's quote-aware scan."""

    kept: list[str] = []
    skip_operand = False
    for word in words:
        if skip_operand:
            skip_operand = False
            continue
        if _REDIRECTION_TOKEN_RE.match(word):
            if word in {"<", ">", ">>", "0<", "1>", "2>", "2>>", "<<", "<<<"}:
                skip_operand = True
            continue
        kept.append(word)
    return kept


def _configuration_from_args(args: list[str]) -> tuple[str, list[str]]:
    configuration = "debug"
    kept: list[str] = []
    index = 0
    while index < len(args):
        token = args[index]
        folded = token.casefold()
        value: str | None = None
        if folded in {"--configuration", "-c"}:
            _require(index + 1 < len(args), "dotnet_configuration_missing")
            value = args[index + 1]
            index += 2
        elif folded.startswith("--configuration="):
            value = token.split("=", 1)[1]
            index += 1
        elif folded.startswith("-c:"):
            value = token.split(":", 1)[1]
            index += 1
        else:
            kept.append(token)
            index += 1
            continue
        folded_value = value.casefold()
        _require(folded_value in {"debug", "release"}, "dotnet_configuration_unsupported")
        configuration = folded_value
    return configuration, kept


def _project_mode(operation: str, args: list[str]) -> tuple[str, list[str]]:
    positional = False
    option = False
    kept: list[str] = []
    index = 0
    while index < len(args):
        token = args[index]
        folded = token.casefold()
        if folded == "--project":
            _require(index + 1 < len(args), "dotnet_project_missing")
            _require(Path(args[index + 1]).suffix.casefold() in {".csproj", ".fsproj"},
                     "dotnet_project_unsupported")
            option = True
            index += 2
            continue
        if folded.startswith("--project="):
            _require(Path(token.split("=", 1)[1]).suffix.casefold() in {".csproj", ".fsproj"},
                     "dotnet_project_unsupported")
            option = True
            index += 1
            continue
        if Path(token).suffix.casefold() in {".csproj", ".fsproj"}:
            positional = True
            index += 1
            continue
        kept.append(token)
        index += 1
    _require(not (positional and option), "dotnet_project_conflict")
    if option:
        _require(operation == "run", "dotnet_project_option_unsupported")
        return "option-project", kept
    if positional:
        return "positional-project", kept
    return "cwd", kept


def _semantic_form(
    words: list[str],
    redirection: dict[str, bool],
    connector_before: str | None,
) -> tuple[str, dict[str, Any] | None]:
    """Return ``measurement``, ``environment``, or ``other`` and a safe form."""

    words = _strip_redirection_words(words)
    if not words or Path(words[0]).name.casefold() != "dotnet":
        return "other", None
    args = words[1:]
    _require(bool(args), "dotnet_operation_missing")
    environment_switches = {"--info", "--version", "--list-sdks", "--list-runtimes"}
    if any(arg.casefold() in environment_switches for arg in args):
        return "environment", None

    first = args.pop(0)
    if first.casefold().endswith(".dll"):
        operation = "direct"
        project_mode = "direct-dll"
        configuration = "debug"
        _require(not args, "dotnet_direct_arguments_unsupported")
        flags: list[str] = []
    else:
        operation = first.casefold()
        _require(operation in {"restore", "build", "run", "test"},
                 "dotnet_operation_unsupported")
        _require("--" not in args, "dotnet_program_arguments_unsupported")
        configuration, args = _configuration_from_args(args)
        project_mode, args = _project_mode(operation, args)
        observed_flags: list[str] = []
        for token in args:
            folded = token.casefold()
            _require(folded in FORM_FLAG_ORDER, "dotnet_option_unsupported")
            observed_flags.append(folded)
        _require(len(observed_flags) == len(set(observed_flags)), "dotnet_duplicate_option")
        flags = [flag for flag in FORM_FLAG_ORDER if flag in observed_flags]

    input_transport = "none"
    if redirection.get("has_input"):
        input_transport = "input-redirection"
    elif connector_before == "pipeline":
        input_transport = "pipeline"
    if input_transport != "none":
        _require(operation in {"run", "direct"}, "dotnet_input_transport_unsupported")
    form = {
        "operation": operation,
        "project_mode": project_mode,
        "configuration": configuration,
        "flags": flags,
        "input_transport": input_transport,
    }
    form["audit_eligible"] = audit_eligible(form)
    return "measurement", form


def _form_id(form: dict[str, Any]) -> str:
    safe = {key: form[key] for key in (
        "operation", "project_mode", "configuration", "flags", "input_transport", "audit_eligible"
    )}
    return "form-" + canonical_json_hash(safe)[:16]


def audit_eligible(form: dict[str, Any]) -> bool:
    operation = form.get("operation") or form.get("subcommand")
    flags_value = form.get("flags") or []
    flags = set() if flags_value == "none" else set(flags_value if isinstance(flags_value, list) else flags_value.split(","))
    return (
        operation == "restore"
        or (operation == "build" and "--no-restore" not in flags)
        or (operation == "run" and "--no-restore" not in flags and "--no-build" not in flags)
        or (operation == "test" and "--no-restore" not in flags)
    )


def _validate_inventory(data: dict[str, Any]) -> None:
    _require(data.get("schema_version") == INVENTORY_SCHEMA, "inventory_schema_invalid")
    _require(_self_hash(data, "inventory_sha256"), "inventory_self_hash_mismatch")
    denominator = data.get("denominator")
    _require(isinstance(denominator, dict), "inventory_denominator_invalid")
    _require(denominator.get("completed_command_events") == EXPECTED_COMPLETED_COMMANDS,
             "inventory_command_denominator_invalid")
    _require(denominator.get("benchmark_dotnet_operations") == EXPECTED_BENCHMARK_DOTNET_OPERATIONS,
             "inventory_dotnet_denominator_invalid")
    _require(denominator.get("dotnet_environment_queries_excluded") == EXPECTED_DOTNET_ENVIRONMENT_QUERIES,
             "inventory_environment_query_denominator_invalid")
    _require(denominator.get("operation_totals") == EXPECTED_OPERATION_TOTALS,
             "inventory_operation_totals_invalid")
    catalog = data.get("form_catalog")
    frequencies = data.get("frequencies")
    _require(isinstance(catalog, list) and bool(catalog), "inventory_form_catalog_invalid")
    _require(isinstance(frequencies, list) and bool(frequencies), "inventory_frequencies_invalid")
    by_id: dict[str, dict[str, Any]] = {}
    for form in catalog:
        _require(isinstance(form, dict), "inventory_form_invalid")
        expected_keys = {
            "form_id", "operation", "project_mode", "configuration", "flags",
            "input_transport", "audit_eligible",
        }
        _require(set(form) == expected_keys, "inventory_form_schema_invalid")
        identifier = form.get("form_id")
        _require(isinstance(identifier, str) and identifier == _form_id(form), "inventory_form_id_invalid")
        _require(identifier not in by_id, "inventory_form_id_duplicate")
        _require(form.get("operation") in OPERATIONS, "inventory_form_operation_invalid")
        _require(form.get("project_mode") in {"cwd", "positional-project", "option-project", "direct-dll"},
                 "inventory_project_mode_invalid")
        _require(form.get("configuration") in {"debug", "release"}, "inventory_configuration_invalid")
        flags = form.get("flags")
        _require(isinstance(flags, list) and flags == [x for x in FORM_FLAG_ORDER if x in flags],
                 "inventory_flags_invalid")
        _require(form.get("input_transport") in {"none", "pipeline", "input-redirection"},
                 "inventory_input_transport_invalid")
        _require(form.get("audit_eligible") is audit_eligible(form), "inventory_audit_eligibility_invalid")
        by_id[identifier] = form
    frequency_total = 0
    seen_frequency: set[tuple[str, str, str, str]] = set()
    for row in frequencies:
        _require(isinstance(row, dict) and set(row) == {
            "configuration_id", "language", "task_id", "form_id", "count"
        }, "inventory_frequency_schema_invalid")
        key = (row.get("configuration_id"), row.get("language"), row.get("task_id"), row.get("form_id"))
        _require(key not in seen_frequency, "inventory_frequency_duplicate")
        seen_frequency.add(key)
        _require(key[0] in CONFIGURATIONS and key[1] in LANGUAGES
                 and key[2] in EXPECTED_TASK_IDS and key[3] in by_id,
                 "inventory_frequency_identity_invalid")
        _require(isinstance(row.get("count"), int) and row["count"] > 0,
                 "inventory_frequency_count_invalid")
        frequency_total += row["count"]
    _require(frequency_total == EXPECTED_BENCHMARK_DOTNET_OPERATIONS,
             "inventory_frequency_total_invalid")
    nu_rows = data.get("nu1900")
    _require(isinstance(nu_rows, dict), "inventory_nu1900_invalid")
    observed_nu = {
        (row.get("configuration_id"), row.get("language")): row.get("occurrences")
        for row in nu_rows.get("by_configuration_and_language", [])
        if isinstance(row, dict)
    }
    _require(observed_nu == EXPECTED_NU1900, "inventory_nu1900_reconciliation_invalid")
    _require(nu_rows.get("by_language") == {"csharp": 0, "fsharp": 197},
             "inventory_nu1900_language_total_invalid")
    _validate_publishable(data, allow_relative_filenames=False)


def inventory(
    e1_report: str | Path,
    archive_root: str | Path,
    output: str | Path | None = None,
) -> dict[str, Any]:
    """Authenticate E1 and produce a deterministic, redacted command inventory."""

    report_path = Path(e1_report)
    archive = Path(archive_root).resolve()
    try:
        report = _json_object(report_path, "e1_report_invalid")
        validate_public_report(report)
    except E2aError:
        raise
    except (KeyError, TypeError, ValueError):
        raise E2aError("e1_report_authentication_failed") from None

    runs = report.get("runs")
    _require(isinstance(runs, list) and len(runs) == 10, "e1_run_roster_invalid")
    _require(archive.is_dir(), "e1_archive_missing")

    run_counts: Counter[tuple[str, str]] = Counter()
    form_counter: Counter[tuple[str, str, str, str]] = Counter()
    operation_counter: Counter[str] = Counter()
    nu1900_counter: Counter[tuple[str, str]] = Counter()
    agent_seconds: Counter[tuple[str, str]] = Counter()
    catalog: dict[str, dict[str, Any]] = {}
    expected_digests: set[str] = set()
    observed_digests: set[str] = set()
    completed_commands = 0
    environment_queries = 0
    benchmark_operations = 0

    seen_attempts: set[str] = set()
    task_count = 0
    for run in runs:
        _require(isinstance(run, dict), "e1_run_invalid")
        attempt_id = run.get("attempt_id")
        _require(isinstance(attempt_id, str) and attempt_id and attempt_id not in seen_attempts,
                 "e1_attempt_identity_invalid")
        seen_attempts.add(attempt_id)
        configuration = _normalise_configuration(run.get("configuration_id"))
        language = _normalise_language(run.get("language"))
        run_counts[(configuration, language)] += 1
        timing = run.get("timing")
        seconds = timing.get("agent_process_wall_seconds") if isinstance(timing, dict) else None
        _require(isinstance(seconds, (int, float)) and not isinstance(seconds, bool)
                 and math.isfinite(float(seconds)) and float(seconds) >= 0,
                 "e1_agent_seconds_invalid")
        agent_seconds[(configuration, language)] += float(seconds)
        tasks = run.get("tasks")
        _require(isinstance(tasks, list) and len(tasks) == 8, "e1_task_roster_invalid")
        _require(tuple(task.get("task_id") for task in tasks if isinstance(task, dict)) == EXPECTED_TASK_IDS,
                 "e1_task_order_invalid")
        for task in tasks:
            task_count += 1
            _require(isinstance(task, dict), "e1_task_invalid")
            task_id = task.get("task_id")
            _require(task.get("attempt_id") == attempt_id
                     and _normalise_configuration(task.get("configuration_id")) == configuration
                     and _normalise_language(task.get("language")) == language,
                     "e1_task_metadata_mismatch")
            identity = task.get("input_identity")
            digest = identity.get("events_sha256") if isinstance(identity, dict) else None
            _require(isinstance(digest, str) and HEX_64_RE.fullmatch(digest) is not None
                     and digest not in expected_digests,
                     "e1_event_identity_invalid")
            _require(identity.get("task_id") == task_id, "e1_event_task_identity_invalid")
            expected_digests.add(digest)

            expected_path = archive / configuration.casefold() / attempt_id / "tasks" / str(task_id) / "events.jsonl"
            try:
                resolved = expected_path.resolve(strict=True)
            except OSError:
                raise E2aError("e1_events_missing") from None
            _require(_inside(archive, resolved) and resolved.is_file() and not resolved.is_symlink(),
                     "e1_events_path_invalid")
            try:
                events, observed_digest = _read_events(resolved)
            except (OSError, ValueError):
                raise E2aError("e1_events_invalid") from None
            _require(observed_digest == digest, "e1_events_digest_mismatch")
            observed_digests.add(observed_digest)
            public_commands = task.get("commands")
            _require(isinstance(public_commands, list), "e1_classifier_record_mismatch")
            raw_command_ordinals = {
                event_ordinal
                for event_ordinal, event in enumerate(events, 1)
                if isinstance(event, dict)
                and event.get("type") == "item.completed"
                and isinstance(event.get("item"), dict)
                and event["item"].get("type") == "command_execution"
            }
            public_command_ordinals = [
                command.get("event_ordinal") if isinstance(command, dict) else None
                for command in public_commands
            ]
            _require(
                all(isinstance(ordinal, int) for ordinal in public_command_ordinals)
                and len(public_command_ordinals) == len(set(public_command_ordinals)),
                "e1_public_command_ordinal_duplicate_or_invalid",
            )
            _require(
                set(public_command_ordinals) == raw_command_ordinals,
                "e1_command_ordinal_roster_mismatch",
            )

            for public_command in public_commands:
                ordinal = public_command.get("event_ordinal") if isinstance(public_command, dict) else None
                _require(isinstance(ordinal, int) and 1 <= ordinal <= len(events),
                         "e1_command_ordinal_invalid")
                event = events[ordinal - 1]
                item = event.get("item") if isinstance(event, dict) else None
                _require(event.get("type") == "item.completed" and isinstance(item, dict)
                         and item.get("type") == "command_execution",
                         "e1_command_ordinal_mismatch")
                try:
                    reconstructed = classify_command(item.get("command"))
                except (KeyError, TypeError, ValueError):
                    raise E2aError("e1_command_reconstruction_failed") from None
                classifier_keys = (
                    "classifier_version", "labels", "ambiguous_or_unparsed", "disposition",
                    "ambiguity_reasons", "connectors", "equivalence_classes",
                )
                _require(
                    all(reconstructed.get(key) == public_command.get(key) for key in classifier_keys),
                    "e1_classifier_record_mismatch",
                )
                reconstructed_operations = reconstructed.get("operations")
                public_operations = public_command.get("operations")
                _require(
                    isinstance(public_operations, list)
                    and isinstance(reconstructed_operations, list)
                    and [
                        {key: value for key, value in operation.items() if key != "outcome"}
                        for operation in public_operations
                    ] == reconstructed_operations,
                    "e1_classifier_operation_mismatch",
                )
                completed_commands += 1
                output_text = item.get("aggregated_output")
                _require(isinstance(output_text, str), "e1_command_output_invalid")
                nu1900_counter[(configuration, language)] += sum(
                    1 for line in output_text.splitlines() if _NU1900_RE.search(line)
                )
                payload, wrapper_reasons = _unwrap_bash(item.get("command"))
                _require(payload is not None and not wrapper_reasons, "e1_command_wrapper_invalid")
                atoms, connectors, redirections, scan_reasons = _scan_payload(payload)
                for index, (atom, redirection) in enumerate(zip(atoms, redirections)):
                    words, parse_reasons = _atom_words(atom)
                    if words is None:
                        continue
                    _require(not parse_reasons, "e1_command_atom_invalid")
                    connector_before = connectors[index - 1] if index else None
                    kind, form = _semantic_form(words, redirection, connector_before)
                    if kind == "other":
                        continue
                    if kind == "environment":
                        environment_queries += 1
                        continue
                    _require(form is not None, "e1_form_missing")
                    identifier = _form_id(form)
                    catalog.setdefault(identifier, {"form_id": identifier, **form})
                    form_counter[(configuration, language, str(task_id), identifier)] += 1
                    operation_counter[form["operation"]] += 1
                    benchmark_operations += 1

    _require(task_count == 80, "e1_task_count_invalid")
    _require(run_counts == EXPECTED_RUN_COUNTS, "e1_configuration_language_roster_invalid")
    _require(observed_digests == expected_digests and len(expected_digests) == 80,
             "e1_event_digest_roster_invalid")
    try:
        archive_event_files = [path for path in archive.rglob("events.jsonl") if path.is_file()]
    except OSError:
        raise E2aError("e1_archive_scan_failed") from None
    _require(len(archive_event_files) == 80, "e1_archive_event_roster_invalid")
    _require(completed_commands == EXPECTED_COMPLETED_COMMANDS, "e1_command_denominator_mismatch")
    _require(environment_queries == EXPECTED_DOTNET_ENVIRONMENT_QUERIES,
             "e1_environment_query_denominator_mismatch")
    _require(benchmark_operations == EXPECTED_BENCHMARK_DOTNET_OPERATIONS,
             "e1_dotnet_denominator_mismatch")
    _require(dict(operation_counter) == EXPECTED_OPERATION_TOTALS,
             "e1_operation_totals_mismatch")
    observed_nu = {key: nu1900_counter.get(key, 0) for key in EXPECTED_NU1900}
    _require(observed_nu == EXPECTED_NU1900, "e1_nu1900_reconciliation_mismatch")

    document = {
        "schema_version": INVENTORY_SCHEMA,
        "source": {
            "e1_report_sha256": report["report_sha256"],
            "family_id": report["family_id"],
            "run_count": 10,
            "task_count": 80,
            "event_digest_roster_sha256": _event_roster_hash(expected_digests),
        },
        "denominator": {
            "completed_command_events": completed_commands,
            "benchmark_dotnet_operations": benchmark_operations,
            "dotnet_environment_queries_excluded": environment_queries,
            "operation_totals": {key: operation_counter[key] for key in OPERATIONS},
        },
        "form_catalog": [catalog[key] for key in sorted(catalog)],
        "frequencies": [
            {
                "configuration_id": configuration,
                "language": language,
                "task_id": task_id,
                "form_id": identifier,
                "count": count,
            }
            for (configuration, language, task_id, identifier), count in sorted(form_counter.items())
        ],
        "nu1900": {
            "status": "observed-in-authenticated-v3-command-streams",
            "by_configuration_and_language": [
                {
                    "configuration_id": configuration,
                    "language": language,
                    "occurrences": observed_nu[(configuration, language)],
                }
                for configuration, language in sorted(observed_nu)
            ],
            "by_language": {
                language: sum(value for (_, current), value in observed_nu.items() if current == language)
                for language in LANGUAGES
            },
            "unit": "emitted diagnostic lines, not independent defects",
        },
        "e1_agent_process_wall_seconds": [
            {
                "configuration_id": configuration,
                "language": language,
                "run_count": run_counts[(configuration, language)],
                "total_seconds": agent_seconds[(configuration, language)],
                "mean_seconds": agent_seconds[(configuration, language)] / run_counts[(configuration, language)],
            }
            for configuration, language in sorted(run_counts)
        ],
        "privacy": {
            "raw_commands": "external-only",
            "raw_output": "external-only",
            "candidate_and_thread_identifiers": "omitted",
            "absolute_paths": "omitted",
        },
    }
    result = _finish_hash(document, "inventory_sha256")
    _validate_inventory(result)
    if output is not None:
        _atomic_json(Path(output), result)
    return result


def _language_first_rounds(task_id: str, form_id: str) -> set[int]:
    ranked = sorted(
        range(1, ROUNDS + 1),
        key=lambda round_number: _sha(
            f"{SCHEDULE_SEED}|{task_id}|{form_id}|{round_number}|language-order".encode("ascii")
        ),
    )
    count = 2 + int(
        _sha(f"{SCHEDULE_SEED}|{task_id}|{form_id}|language-majority".encode("ascii")), 16
    ) % 2
    return set(ranked[:count])


def build_schedule(inventory_data: dict[str, Any]) -> list[dict[str, Any]]:
    """Derive five deterministic paired rounds from observed task/form cells."""

    _validate_inventory(inventory_data)
    catalog = {row["form_id"]: row for row in inventory_data["form_catalog"]}
    cells = sorted({(row["task_id"], row["form_id"]) for row in inventory_data["frequencies"]})
    first_rounds = {
        cell: _language_first_rounds(*cell)
        for cell in cells
    }
    rows: list[dict[str, Any]] = []
    position = 0
    for round_number in range(1, ROUNDS + 1):
        ordered_cells = sorted(
            cells,
            key=lambda cell: _sha(
                f"{SCHEDULE_SEED}|round={round_number}|{cell[0]}|{cell[1]}".encode("ascii")
            ),
        )
        for pair_position, (task_id, form_id) in enumerate(ordered_cells, 1):
            stage = EXPECTED_TASK_IDS.index(task_id) + 1
            first = "csharp" if round_number in first_rounds[(task_id, form_id)] else "fsharp"
            language_order = (first, "fsharp" if first == "csharp" else "csharp")
            conditions = ["audit_on", "audit_off"] if catalog[form_id]["audit_eligible"] else ["audit_on"]
            if len(conditions) == 2 and int(
                _sha(f"{SCHEDULE_SEED}|{round_number}|{task_id}|{form_id}|audit-order".encode("ascii")), 16
            ) % 2:
                conditions.reverse()
            for condition_position, condition in enumerate(conditions, 1):
                for language_position, language in enumerate(language_order, 1):
                    position += 1
                    rows.append({
                        "position": position,
                        "round": round_number,
                        "pair_position": pair_position,
                        "task_id": task_id,
                        "stage": stage,
                        "form_id": form_id,
                        "audit_condition": condition,
                        "condition_position": condition_position,
                        "language": language,
                        "language_position": language_position,
                    })
    return rows


def _schedule_errors(
    schedule: Any,
    inventory_data: dict[str, Any],
) -> list[str]:
    errors: list[str] = []
    if not isinstance(schedule, list):
        return ["schedule_not_list"]
    try:
        expected = build_schedule(inventory_data)
    except E2aError:
        return ["inventory_invalid"]
    if schedule != expected:
        errors.append("schedule_differs_from_deterministic_recomputation")
        return errors
    expected_keys = {
        "position", "round", "pair_position", "task_id", "stage", "form_id",
        "audit_condition", "condition_position", "language", "language_position",
    }
    catalog = {row["form_id"]: row for row in inventory_data["form_catalog"]}
    cell_counts: Counter[tuple[str, str, str, str]] = Counter()
    first_counts: Counter[tuple[str, str, str, str]] = Counter()
    for index, row in enumerate(schedule, 1):
        if not isinstance(row, dict) or set(row) != expected_keys or row.get("position") != index:
            errors.append("schedule_row_schema_invalid")
            continue
        key = (row["task_id"], row["form_id"], row["language"], row["audit_condition"])
        cell_counts[key] += 1
        if row["language_position"] == 1:
            first_counts[(
                row["task_id"], row["form_id"], row["audit_condition"], row["language"]
            )] += 1
        if row["audit_condition"] == "audit_off" and not catalog[row["form_id"]]["audit_eligible"]:
            errors.append("schedule_ineligible_audit_control")
    for task_id, form_id in sorted({(row["task_id"], row["form_id"]) for row in schedule}):
        conditions = ("audit_on", "audit_off") if catalog[form_id]["audit_eligible"] else ("audit_on",)
        for language in LANGUAGES:
            for condition in conditions:
                if cell_counts[(task_id, form_id, language, condition)] != ROUNDS:
                    errors.append("schedule_cell_count_invalid")
            for condition in conditions:
                first = first_counts[(task_id, form_id, condition, language)]
                if first not in {2, 3}:
                    errors.append("schedule_language_order_unbalanced")
    return sorted(set(errors))


def _accepted_e2_reference(e2_definition: dict[str, Any]) -> dict[str, Any]:
    _require(e2_definition.get("definition_sha256") == ACCEPTED_E2_DEFINITION_SHA256,
             "accepted_e2_definition_identity_mismatch")
    _require(e2_definition.get("schedule_sha256") == ACCEPTED_E2_SCHEDULE_SHA256,
             "accepted_e2_schedule_identity_mismatch")
    _require(e2_definition.get("environment_profile", e2_definition.get("execution_contract", {}).get(
        "environment_profile")) == ACCEPTED_E2_ENVIRONMENT_PROFILE,
        "accepted_e2_environment_identity_mismatch")
    unsigned = dict(e2_definition)
    claimed = unsigned.pop("definition_sha256", None)
    _require(claimed == canonical_json_hash(unsigned), "accepted_e2_self_hash_mismatch")
    manifest = e2_definition.get("manifest")
    _require(isinstance(manifest, dict)
             and manifest.get("normalized_sha256") == ACCEPTED_MANIFEST_SHA256,
             "accepted_manifest_identity_mismatch")
    states = e2_definition.get("states")
    _require(isinstance(states, list) and len(states) == 18, "accepted_e2_state_roster_invalid")
    state_refs: list[dict[str, Any]] = []
    seen: set[tuple[str, int]] = set()
    for state in states:
        _require(isinstance(state, dict), "accepted_e2_state_invalid")
        language = state.get("language")
        stage = state.get("stage")
        _require(language in LANGUAGES and isinstance(stage, int) and stage in range(9),
                 "accepted_e2_state_identity_invalid")
        _require((language, stage) not in seen, "accepted_e2_state_duplicate")
        seen.add((language, stage))
        if stage == 0:
            continue
        expected_task = EXPECTED_TASK_IDS[stage - 1]
        _require(state.get("task_id") == expected_task, "accepted_e2_state_task_mismatch")
        state_refs.append({
            "language": language,
            "stage": stage,
            "task_id": expected_task,
            "state_id": state.get("state_id"),
            "source_tree_sha256": state.get("source_tree_sha256"),
            "case_count": state.get("case_count"),
            "state_sha256": canonical_json_hash(state),
        })
    _require(len(state_refs) == 16, "accepted_e2_successor_state_roster_invalid")
    return {
        "definition_sha256": ACCEPTED_E2_DEFINITION_SHA256,
        "schedule_sha256": ACCEPTED_E2_SCHEDULE_SHA256,
        "accepted_report_sha256": ACCEPTED_E2_REPORT_SHA256,
        "environment_profile": ACCEPTED_E2_ENVIRONMENT_PROFILE,
        "manifest_normalized_sha256": ACCEPTED_MANIFEST_SHA256,
        "ecology": "accepted-offline-e2-kept-separate-and-not-pooled",
        "successor_states": sorted(state_refs, key=lambda row: (row["stage"], row["language"])),
    }


def environment_contract() -> dict[str, Any]:
    return {
        "profile_id": PROFILE_ID,
        "runner_profile_id": RUNNER_PROFILE_ID,
        "v3_runner_git_sha": V3_RUNNER_GIT_SHA,
        "container_image_id": V3_IMAGE_ID,
        "portable_image_archive": {
            "sha256": V3_IMAGE_ARCHIVE_SHA256,
            "bytes": V3_IMAGE_ARCHIVE_BYTES,
        },
        "dotnet_sdk": DOTNET_SDK,
        "resource_limits": {"memory": "2g", "memory_swap": "2g", "cpus": 2, "pids": 256},
        "storage": {
            "workspace_filesystem": "ext4",
            "work_root_filesystem": "ext4",
            "docker_data_filesystem": "ext4",
            "docker_storage_driver": "overlay2",
            "container_root_filesystem": "overlayfs",
            "tmp_filesystem": "overlayfs",
            "root_read_only": False,
            "tmp_writable_uid_1000": True,
        },
        "network": {
            "docker_network": "alf-internal",
            "internal": True,
            "bridge_gateway": "172.30.0.1",
            "http_proxy": "http://172.30.0.1:43128",
            "https_proxy": "http://172.30.0.1:43128",
            "no_proxy": ["127.0.0.1", "localhost"],
            "allowed_authority": "chatgpt.com:443",
            "nuget_source_reachability": "blocked-by-connect-proxy-allowlist",
        },
        "process": {
            "uid": 1000,
            "gid": 1000,
            "candidate_present": False,
            "codex_present": False,
            "model_endpoint_configured": False,
            "auth_present": False,
        },
        "cache": {
            "home_fresh_per_sample": True,
            "nuget_cache_fresh_per_sample": True,
            "home_under_ext4_work_root": True,
        },
        "source": {"canonical_gold_successors": True},
    }


def _mismatch_ledger() -> list[dict[str, str]]:
    return [
        {
            "component": "candidate-process",
            "status": "deliberately-absent",
            "bound": "model-free E2a measures tool commands only; no Codex or model request is made",
        },
        {
            "component": "authentication-home",
            "status": "deliberately-absent",
            "bound": "fresh HOME reproduces cache freshness but contains no Codex authentication material",
        },
        {
            "component": "workspace-state",
            "status": "standardized-successor",
            "bound": "each task/form uses its matched canonical gold successor, not an intermediate candidate edit",
        },
        {
            "component": "within-task-cache-history",
            "status": "unavailable",
            "bound": "each sample has a fresh HOME/cache; the exact cache history at each E1 command is not retained",
        },
        {
            "component": "host-load",
            "status": "observed-not-controlled",
            "bound": "per-sample load is retained, but machine-cold state and unrelated host work are not controlled",
        },
        {
            "component": "shell-plumbing",
            "status": "semantic-replay",
            "bound": "fixed argv uses shell=False; pipe versus file-backed stdin semantics are retained without incidental shell text",
        },
    ]


def freeze(
    inventory_data: dict[str, Any],
    e2_definition: dict[str, Any],
    output: str | Path | None = None,
    *,
    e2a_runner_git_sha: str,
) -> dict[str, Any]:
    """Freeze the form-derived E2a schedule and accepted-state references."""

    _validate_inventory(inventory_data)
    runner_sha = str(e2a_runner_git_sha).casefold()
    _require(HEX_40_RE.fullmatch(runner_sha) is not None, "e2a_runner_git_sha_invalid")
    e2_reference = _accepted_e2_reference(e2_definition)
    schedule = build_schedule(inventory_data)
    document = {
        "schema_version": DEFINITION_SCHEMA,
        "inventory_sha256": inventory_data["inventory_sha256"],
        "e1_report_sha256": inventory_data["source"]["e1_report_sha256"],
        "accepted_e2": e2_reference,
        "runner": {
            "e2a_runner_git_sha": runner_sha,
            "v3_runner_git_sha": V3_RUNNER_GIT_SHA,
            "profile_id": RUNNER_PROFILE_ID,
        },
        "environment_contract": environment_contract(),
        "measurement_contract": {
            "rounds": ROUNDS,
            "state": "matched-canonical-gold-successor-for-observed-task",
            "fresh_workspace_home_and_nuget_cache": "per-sample",
            "command_execution": "fixed-argv-shell-false",
            "input_transport": "pipe-or-file-backed-redirection-as-observed",
            "audit_control": "NuGetAudit=false-only-for-restore-capable-forms",
            "raw_output": "external-to-git",
            "model_or_candidate": "forbidden",
            "timeout_seconds": COMMAND_TIMEOUT_SECONDS,
        },
        "form_catalog": inventory_data["form_catalog"],
        "schedule_seed": SCHEDULE_SEED,
        "schedule": schedule,
        "schedule_sha256": _sha(_canonical_bytes(schedule)),
        "mismatch_ledger": _mismatch_ledger(),
    }
    result = _finish_hash(document, "definition_sha256")
    checked = check(result, inventory_data, e2_definition)
    _require(checked["ok"], "definition_internal_validation_failed")
    if output is not None:
        _atomic_json(Path(output), result)
    return result


def check(
    definition: dict[str, Any],
    inventory_data: dict[str, Any] | None = None,
    e2_definition: dict[str, Any] | None = None,
) -> dict[str, Any]:
    errors: list[str] = []
    try:
        if definition.get("schema_version") != DEFINITION_SCHEMA:
            errors.append("definition_schema_invalid")
        if not _self_hash(definition, "definition_sha256"):
            errors.append("definition_self_hash_mismatch")
        if definition.get("environment_contract") != environment_contract():
            errors.append("definition_environment_contract_mismatch")
        runner = definition.get("runner")
        if not isinstance(runner, dict) or runner.get("v3_runner_git_sha") != V3_RUNNER_GIT_SHA \
                or runner.get("profile_id") != RUNNER_PROFILE_ID \
                or not isinstance(runner.get("e2a_runner_git_sha"), str) \
                or HEX_40_RE.fullmatch(runner.get("e2a_runner_git_sha", "")) is None:
            errors.append("definition_runner_identity_invalid")
        if definition.get("schedule_sha256") != _sha(_canonical_bytes(definition.get("schedule"))):
            errors.append("definition_schedule_hash_mismatch")
        embedded_e2 = definition.get("accepted_e2")
        if not isinstance(embedded_e2, dict) \
                or canonical_json_hash(embedded_e2) != ACCEPTED_E2_REFERENCE_SHA256 \
                or embedded_e2.get("definition_sha256") != ACCEPTED_E2_DEFINITION_SHA256 \
                or embedded_e2.get("schedule_sha256") != ACCEPTED_E2_SCHEDULE_SHA256 \
                or embedded_e2.get("accepted_report_sha256") != ACCEPTED_E2_REPORT_SHA256 \
                or embedded_e2.get("environment_profile") != ACCEPTED_E2_ENVIRONMENT_PROFILE \
                or embedded_e2.get("manifest_normalized_sha256") != ACCEPTED_MANIFEST_SHA256 \
                or not isinstance(embedded_e2.get("successor_states"), list) \
                or len(embedded_e2.get("successor_states", [])) != 16:
            errors.append("definition_embedded_e2_identity_invalid")
        if inventory_data is not None:
            _validate_inventory(inventory_data)
            if definition.get("inventory_sha256") != inventory_data.get("inventory_sha256"):
                errors.append("definition_inventory_identity_mismatch")
            errors.extend(_schedule_errors(definition.get("schedule"), inventory_data))
            if definition.get("form_catalog") != inventory_data.get("form_catalog"):
                errors.append("definition_form_catalog_mismatch")
        if e2_definition is not None:
            expected_e2 = _accepted_e2_reference(e2_definition)
            if definition.get("accepted_e2") != expected_e2:
                errors.append("definition_accepted_e2_mismatch")
    except E2aError as exc:
        errors.append(exc.code)
    return {
        "ok": not errors,
        "errors": sorted(set(errors)),
        "definition_sha256": definition.get("definition_sha256"),
    }


def validate_environment(
    observed: dict[str, Any],
    definition: dict[str, Any],
    *,
    expected_commit: str | None = None,
) -> None:
    _require(observed.get("schema_version") == ENVIRONMENT_SCHEMA, "environment_schema_invalid")
    expected = definition.get("environment_contract")
    _require(isinstance(expected, dict), "environment_contract_missing")
    for key in (
        "profile_id", "runner_profile_id", "v3_runner_git_sha", "container_image_id",
        "portable_image_archive", "dotnet_sdk", "resource_limits", "storage", "network",
        "process", "cache", "source",
    ):
        _require(observed.get(key) == expected.get(key), "environment_observation_mismatch")
    runner_commit = expected_commit or definition.get("runner", {}).get("e2a_runner_git_sha")
    _require(observed.get("e2a_runner_git_sha") == runner_commit,
             "environment_runner_commit_mismatch")
    process = observed["process"]
    _require(not any(process[key] for key in (
        "candidate_present", "codex_present", "model_endpoint_configured", "auth_present"
    )), "environment_forbidden_candidate_auth_or_model")
    self_observation = observed.get("container_self_observation")
    if self_observation is not None:
        _require(isinstance(self_observation, dict), "environment_self_observation_invalid")
        _require(self_observation.get("uid") == 1000 and self_observation.get("gid") == 1000,
                 "environment_self_identity_invalid")
        cgroup = self_observation.get("cgroup_v2")
        _require(isinstance(cgroup, dict)
                 and cgroup.get("memory_max_bytes") == 2 * 1024 * 1024 * 1024
                 and cgroup.get("cpu_ratio") == 2.0
                 and cgroup.get("pids_max") == 256,
                 "environment_self_limits_invalid")
        mounts = self_observation.get("mounts")
        _require(isinstance(mounts, dict)
                 and mounts.get("root_filesystem") == "overlay"
                 and mounts.get("tmp_filesystem") == "overlay"
                 and mounts.get("work_root_filesystem") in {"ext2", "ext3", "ext4"}
                 and all(mounts.get(key) == "rw" for key in (
                     "root_mode", "tmp_mode", "work_root_mode"
                 )), "environment_self_mounts_invalid")
        _require(self_observation.get("tmp_writable") is True
                 and self_observation.get("proxy_environment_exact") is True
                 and self_observation.get("pinned_image_environment_exact") is True
                 and self_observation.get("codex_process_present") is False
                 and self_observation.get("model_endpoint_configured") is False
                 and self_observation.get("auth_material_present") is False,
                 "environment_self_safety_invalid")
    _validate_publishable(observed, allow_relative_filenames=False)


def _runtime_source_snapshot(workspace: Path, expected_state: dict[str, Any]) -> dict[str, Any]:
    """Validate E2 state bytes without importing the unavailable tiktoken wheel."""

    expected_files = expected_state.get("files")
    _require(isinstance(expected_files, list), "runtime_state_file_roster_invalid")
    expected_by_path = {
        row.get("path"): row for row in expected_files if isinstance(row, dict) and isinstance(row.get("path"), str)
    }
    _require(len(expected_by_path) == len(expected_files), "runtime_state_file_roster_invalid")
    observed_paths = sorted(
        path.relative_to(workspace).as_posix()
        for path in workspace.rglob("*")
        if path.is_file() and _included_source(path.relative_to(workspace))
    )
    _require(observed_paths == sorted(expected_by_path), "runtime_state_path_roster_mismatch")
    hashes: dict[str, str] = {}
    rows: list[dict[str, Any]] = []
    for relative in observed_paths:
        path = workspace / PurePosixPath(relative)
        _require(not path.is_symlink(), "runtime_state_symlink_forbidden")
        try:
            normalized = _normalise_text(path.read_bytes(), label="runtime source")
        except (OSError, ValueError):
            raise E2aError("runtime_state_source_invalid") from None
        digest = _sha(normalized)
        expected = expected_by_path[relative]
        _require(
            digest == expected.get("sha256")
            and len(normalized) == expected.get("bytes")
            and len(normalized.decode("utf-8").splitlines()) == expected.get("lines"),
            "runtime_state_file_identity_mismatch",
        )
        hashes[relative] = digest
        rows.append({"path": relative, "bytes": len(normalized), "lines": expected["lines"], "sha256": digest})
    source_tree_sha256 = _sha(_canonical_bytes(hashes))
    _require(source_tree_sha256 == expected_state.get("source_tree_sha256"),
             "runtime_state_tree_identity_mismatch")
    return {"source_tree_sha256": source_tree_sha256, "files": rows}


def _state_maps(
    definition: dict[str, Any],
    e2_definition: dict[str, Any],
) -> tuple[dict[tuple[str, int], dict[str, Any]], dict[tuple[str, int], dict[str, Any]]]:
    states: dict[tuple[str, int], dict[str, Any]] = {}
    for state in e2_definition.get("states", []):
        if isinstance(state, dict) and state.get("language") in LANGUAGES and isinstance(state.get("stage"), int):
            states[(state["language"], state["stage"])] = state
    references = {
        (row["language"], row["stage"]): row
        for row in definition.get("accepted_e2", {}).get("successor_states", [])
        if isinstance(row, dict)
    }
    _require(len(states) == 18 and len(references) == 16, "runtime_state_roster_invalid")
    for key, reference in references.items():
        state = states.get(key)
        _require(state is not None and canonical_json_hash(state) == reference.get("state_sha256")
                 and state.get("source_tree_sha256") == reference.get("source_tree_sha256")
                 and state.get("task_id") == reference.get("task_id"),
                 "runtime_state_reference_mismatch")
    return states, references


def canonical_argv(
    form: dict[str, Any],
    project: str,
    *,
    audit_condition: str = "audit_on",
    target_framework: str = "net10.0",
) -> list[str]:
    """Construct the one allowlisted argv represented by a public semantic form."""

    _require(audit_condition in {"audit_on", "audit_off"}, "audit_condition_invalid")
    _require(audit_condition != "audit_off" or audit_eligible(form), "audit_control_ineligible")
    operation = str(form.get("operation") or form.get("subcommand"))
    project_mode = form.get("project_mode") or form.get("project")
    if project_mode == "explicit-project":
        project_mode = "option-project" if operation == "run" else "positional-project"
    configuration = str(form.get("configuration", "debug")).casefold()
    flags_value = form.get("flags") or []
    flags = [] if flags_value == "none" else list(flags_value if isinstance(flags_value, list) else flags_value.split(","))
    _require(operation in OPERATIONS and configuration in {"debug", "release"}, "form_argv_invalid")
    _require(flags == [flag for flag in FORM_FLAG_ORDER if flag in flags], "form_argv_flags_invalid")

    if operation == "direct":
        _require(project_mode == "direct-dll" and not flags, "direct_form_invalid")
        configuration_dir = "Release" if configuration == "release" else "Debug"
        assembly = Path(project).stem + ".dll"
        argv = ["dotnet", f"bin/{configuration_dir}/{target_framework}/{assembly}"]
    else:
        argv = ["dotnet", operation]
        if project_mode == "positional-project":
            argv.append(project)
        elif project_mode == "option-project":
            _require(operation == "run", "form_project_mode_invalid")
            argv.extend(["--project", project])
        else:
            _require(project_mode == "cwd", "form_project_mode_invalid")
        if configuration == "release":
            argv.extend(["--configuration", "Release"])
        argv.extend(flags)
        if audit_condition == "audit_off":
            argv.append("-p:NuGetAudit=false")
    return argv


def _prerequisite_argv(form: dict[str, Any], project: str) -> list[list[str]]:
    operation = form["operation"]
    flags = set(form["flags"])
    needs_restore = (
        operation == "direct"
        or "--no-restore" in flags
        or "--no-build" in flags
    )
    needs_build = operation == "direct" or "--no-build" in flags
    commands: list[list[str]] = []
    if needs_restore:
        commands.append(["dotnet", "restore", project])
    if needs_build:
        build = ["dotnet", "build", project, "--no-restore"]
        if form["configuration"] == "release":
            build.extend(["--configuration", "Release"])
        commands.append(build)
    return commands


def _case_payload(cases: list[dict[str, Any]]) -> bytes:
    try:
        return "".join(
            json.dumps(case["input"], sort_keys=True, separators=(",", ":")) + "\n"
            for case in cases
        ).encode("utf-8")
    except (KeyError, TypeError, ValueError):
        raise E2aError("case_payload_invalid") from None


def _cases(manifest: dict[str, Any], stage: int) -> list[dict[str, Any]]:
    return list(manifest["baseline_cases"]) + [
        case for task in manifest["tasks"][:stage] for case in task.get("cases", [])
    ]


def _host_load() -> dict[str, Any]:
    result: dict[str, Any] = {
        "cpu_count": os.cpu_count(),
        "load_1m": None,
        "load_5m": None,
        "load_15m": None,
        "memory_total_kib": None,
        "memory_available_kib": None,
    }
    try:
        loads = Path("/proc/loadavg").read_text(encoding="ascii").split()[:3]
        result["load_1m"], result["load_5m"], result["load_15m"] = [float(value) for value in loads]
    except (OSError, ValueError):
        pass
    try:
        for line in Path("/proc/meminfo").read_text(encoding="ascii").splitlines():
            key, _, value = line.partition(":")
            if key == "MemTotal":
                result["memory_total_kib"] = int(value.split()[0])
            elif key == "MemAvailable":
                result["memory_available_kib"] = int(value.split()[0])
    except (OSError, ValueError, IndexError):
        pass
    return result


def _sample_environment(home: Path, observed: dict[str, Any]) -> dict[str, str]:
    network = observed["network"]
    return {
        **PINNED_IMAGE_ENVIRONMENT,
        "HOME": str(home),
        "CODEX_HOME": str(home),
        "HTTP_PROXY": network["http_proxy"],
        "HTTPS_PROXY": network["https_proxy"],
        "NO_PROXY": ",".join(network["no_proxy"]),
    }


def _mount_type_and_mode(target: Path) -> tuple[str, str]:
    try:
        lines = Path("/proc/self/mountinfo").read_text(encoding="utf-8").splitlines()
    except OSError:
        raise E2aError("runtime_mountinfo_unavailable") from None
    resolved = target.resolve()
    matches: list[tuple[int, str, str]] = []
    for line in lines:
        before, separator, after = line.partition(" - ")
        if not separator:
            continue
        left = before.split()
        right = after.split()
        if len(left) < 6 or not right:
            continue
        mountpoint = left[4].replace("\\040", " ").replace("\\011", "\t")
        try:
            mount_path = Path(mountpoint).resolve()
        except OSError:
            continue
        if resolved == mount_path or mount_path in resolved.parents:
            mode = "ro" if "ro" in left[5].split(",") else "rw"
            matches.append((len(mount_path.parts), right[0], mode))
    _require(bool(matches), "runtime_mountpoint_not_found")
    _, filesystem, mode = max(matches, key=lambda row: row[0])
    return filesystem, mode


def _read_cgroup_value(name: str) -> str:
    try:
        return (Path("/sys/fs/cgroup") / name).read_text(encoding="ascii").strip()
    except OSError:
        raise E2aError("runtime_cgroup_v2_unavailable") from None


def _codex_process_present() -> bool:
    proc = Path("/proc")
    _require(proc.is_dir(), "runtime_proc_unavailable")
    try:
        candidates = [path for path in proc.iterdir() if path.name.isdigit()]
    except OSError:
        raise E2aError("runtime_proc_scan_failed") from None
    for process in candidates:
        try:
            args = (process / "cmdline").read_bytes().split(b"\0")
        except OSError:
            continue
        for argument in args:
            if Path(argument.decode("utf-8", errors="ignore")).name.casefold() in {"codex", "codex.exe"}:
                return True
    return False


def _auth_material_present() -> bool:
    candidates: list[Path] = []
    home = os.environ.get("HOME")
    codex_home = os.environ.get("CODEX_HOME")
    if home:
        candidates.append(Path(home) / ".codex" / "auth.json")
    if codex_home:
        candidates.append(Path(codex_home) / "auth.json")
    return any(path.is_file() for path in candidates)


def _runtime_self_observation(work_root: Path, observed: dict[str, Any]) -> dict[str, Any]:
    _require(hasattr(os, "getuid") and hasattr(os, "getgid"), "runtime_posix_identity_unavailable")
    uid = os.getuid()
    gid = os.getgid()
    _require((uid, gid) == (1000, 1000), "runtime_uid_gid_mismatch")
    memory_max = _read_cgroup_value("memory.max")
    pids_max = _read_cgroup_value("pids.max")
    cpu_max = _read_cgroup_value("cpu.max").split()
    _require(memory_max == str(2 * 1024 * 1024 * 1024), "runtime_memory_limit_mismatch")
    _require(pids_max == "256", "runtime_pids_limit_mismatch")
    _require(len(cpu_max) == 2 and cpu_max[0] != "max", "runtime_cpu_limit_invalid")
    try:
        cpu_ratio = int(cpu_max[0]) / int(cpu_max[1])
    except (ValueError, ZeroDivisionError):
        raise E2aError("runtime_cpu_limit_invalid") from None
    _require(math.isclose(cpu_ratio, 2.0, rel_tol=0.0, abs_tol=1e-12),
             "runtime_cpu_limit_mismatch")

    root_fs, root_mode = _mount_type_and_mode(Path("/"))
    tmp_fs, tmp_mode = _mount_type_and_mode(Path("/tmp"))
    work_fs, work_mode = _mount_type_and_mode(work_root)
    _require(root_fs == "overlay" and tmp_fs == "overlay", "runtime_overlay_filesystem_mismatch")
    _require(root_mode == "rw" and tmp_mode == "rw" and work_mode == "rw",
             "runtime_mount_not_writable")
    _require(work_fs in {"ext2", "ext3", "ext4"}, "runtime_work_filesystem_mismatch")
    try:
        descriptor, temporary = tempfile.mkstemp(prefix="alf-e2a-writable-", dir="/tmp")
        os.close(descriptor)
        Path(temporary).unlink()
    except OSError:
        raise E2aError("runtime_tmp_not_writable") from None

    expected_network = observed["network"]
    _require(os.environ.get("HTTP_PROXY") == expected_network["http_proxy"]
             and os.environ.get("HTTPS_PROXY") == expected_network["https_proxy"]
             and os.environ.get("NO_PROXY") == ",".join(expected_network["no_proxy"]),
             "runtime_proxy_environment_mismatch")
    model_keys = (
        "OPENAI_API_KEY", "OPENAI_BASE_URL", "AZURE_OPENAI_API_KEY",
        "AZURE_OPENAI_ENDPOINT", "CODEX_API_KEY",
    )
    model_endpoint_configured = any(bool(os.environ.get(key)) for key in model_keys)
    auth_present = _auth_material_present()
    codex_present = _codex_process_present()
    pinned_image_environment_exact = all(
        os.environ.get(key) == value for key, value in PINNED_IMAGE_ENVIRONMENT.items()
    )
    _require(not model_endpoint_configured, "runtime_model_endpoint_configured")
    _require(not auth_present, "runtime_auth_present")
    _require(not codex_present, "runtime_codex_process_present")
    _require(pinned_image_environment_exact, "runtime_pinned_image_environment_mismatch")
    return {
        "uid": uid,
        "gid": gid,
        "cgroup_v2": {
            "memory_max_bytes": int(memory_max),
            "cpu_quota": int(cpu_max[0]),
            "cpu_period": int(cpu_max[1]),
            "cpu_ratio": cpu_ratio,
            "pids_max": int(pids_max),
        },
        "mounts": {
            "root_filesystem": root_fs,
            "root_mode": root_mode,
            "tmp_filesystem": tmp_fs,
            "tmp_mode": tmp_mode,
            "work_root_filesystem": work_fs,
            "work_root_mode": work_mode,
        },
        "tmp_writable": True,
        "proxy_environment_exact": True,
        "pinned_image_environment_exact": pinned_image_environment_exact,
        "codex_process_present": codex_present,
        "model_endpoint_configured": model_endpoint_configured,
        "auth_material_present": auth_present,
    }


def _stream_ref(relative: str, raw: bytes) -> dict[str, Any]:
    return {"file": relative, "bytes": len(raw), "sha256": _sha(raw)}


def _diagnostic_summary(stdout: bytes, stderr: bytes) -> dict[str, Any]:
    text = (stdout + b"\n" + stderr).decode("utf-8", errors="replace")
    parsed = diagnostics(text)
    return {
        "occurrence_count": parsed["occurrence_count"],
        "counts_by_code": parsed["counts_by_code"],
        "counts_by_category": parsed["counts_by_category"],
        "counts_by_severity": parsed["counts_by_severity"],
        "nu1900_occurrences": sum(1 for line in text.splitlines() if _NU1900_RE.search(line)),
    }


def _invoke(
    argv: list[str],
    *,
    cwd: Path,
    env: dict[str, str],
    timeout: int,
    input_bytes: bytes | None = None,
    stdin_stream: IO[bytes] | int | None = None,
) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        input=input_bytes,
        stdin=stdin_stream,
        capture_output=True,
        timeout=timeout,
        check=False,
        shell=False,
    )


def _execute_operation(
    *,
    label: str,
    argv: list[str],
    cwd: Path,
    env: dict[str, str],
    raw: Path,
    stem: str,
    timeout: int,
    input_transport: str = "none",
    payload: bytes | None = None,
    redirection_file: Path | None = None,
) -> tuple[dict[str, Any], bytes, bytes]:
    _require(input_transport in {"none", "pipeline", "input-redirection"},
             "runtime_input_transport_invalid")
    started = time.perf_counter()
    timed_out = False
    handle: IO[bytes] | None = None
    try:
        if input_transport == "pipeline":
            completed = _invoke(argv, cwd=cwd, env=env, timeout=timeout, input_bytes=payload or b"")
        elif input_transport == "input-redirection":
            _require(redirection_file is not None and redirection_file.is_file(),
                     "runtime_redirection_input_missing")
            handle = redirection_file.open("rb")
            completed = _invoke(argv, cwd=cwd, env=env, timeout=timeout, stdin_stream=handle)
        else:
            completed = _invoke(argv, cwd=cwd, env=env, timeout=timeout, stdin_stream=subprocess.DEVNULL)
        stdout = completed.stdout or b""
        stderr = completed.stderr or b""
        exit_code: int | None = completed.returncode
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout or b""
        stderr = exc.stderr or b""
        if isinstance(stdout, str):
            stdout = stdout.encode("utf-8", errors="replace")
        if isinstance(stderr, str):
            stderr = stderr.encode("utf-8", errors="replace")
        exit_code = None
        timed_out = True
    except OSError:
        raise E2aError("runtime_process_start_failed") from None
    finally:
        if handle is not None:
            handle.close()

    stdout_relative = f"{stem}.stdout.bin"
    stderr_relative = f"{stem}.stderr.bin"
    metadata_relative = f"{stem}.json"
    _atomic_bytes(raw / stdout_relative, stdout)
    _atomic_bytes(raw / stderr_relative, stderr)
    record = {
        "label": label,
        "argv": argv,
        "shell": False,
        "input_transport": input_transport,
        "timeout_seconds": timeout,
        "wall_seconds": time.perf_counter() - started,
        "timed_out": timed_out,
        "exit_code": exit_code,
        "stdout": _stream_ref(stdout_relative, stdout),
        "stderr": _stream_ref(stderr_relative, stderr),
        "diagnostics": _diagnostic_summary(stdout, stderr),
    }
    _atomic_json(raw / metadata_relative, record)
    record["metadata_file"] = metadata_relative
    if timed_out:
        raise E2aError("runtime_command_timeout")
    if exit_code != 0:
        raise E2aError("runtime_command_failed")
    return record, stdout, stderr


def _program_output_tail(stdout: bytes, cases: list[dict[str, Any]]) -> bytes:
    if not cases:
        return b""
    try:
        lines = [line for line in stdout.decode("utf-8").splitlines() if line.strip()]
    except UnicodeDecodeError:
        raise E2aError("runtime_program_output_not_utf8") from None
    _require(len(lines) >= len(cases), "runtime_program_output_count_mismatch")
    return ("\n".join(lines[-len(cases):]) + "\n").encode("utf-8")


def _cache_summary(cache: Path) -> dict[str, Any]:
    if not cache.exists():
        return {"file_count": 0, "total_bytes": 0, "set_sha256": _sha(_canonical_bytes([]))}
    _require(cache.is_dir() and not cache.is_symlink(), "runtime_cache_invalid")
    return {
        key: value
        for key, value in raw_file_inventory(cache).items()
        if key in {"file_count", "total_bytes", "set_sha256"}
    }


def _validate_materialized_state(
    *,
    root: Path,
    workspace: Path,
    manifest: dict[str, Any],
    state: dict[str, Any],
) -> dict[str, Any]:
    language = state["language"]
    stage = state["stage"]
    observed = _runtime_source_snapshot(workspace, state)
    checks = _cumulative_checks(manifest, language, stage)
    try:
        checked = check_workspace(workspace, checks)
        compile_obligations = _compile_obligations(
            workspace, manifest["languages"][language], language
        )
    except (OSError, KeyError, TypeError, ValueError):
        raise E2aError("runtime_state_static_validation_failed") from None
    _require(checked.get("ok") is True, "runtime_workspace_checks_failed")
    _require(compile_obligations == state.get("compile_obligations"),
             "runtime_compile_obligations_mismatch")
    _require(len(_cases(manifest, stage)) == state.get("case_count"),
             "runtime_case_count_mismatch")
    return {
        "state_id": state["state_id"],
        "source_tree_sha256": observed["source_tree_sha256"],
        "case_count": state["case_count"],
        "workspace_check_counts": {key: len(checks[key]) for key in CHECK_KEYS},
    }


def _preflight_states(
    *,
    root: Path,
    work_root: Path,
    manifest: dict[str, Any],
    states: dict[tuple[str, int], dict[str, Any]],
    references: dict[tuple[str, int], dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for language, stage in sorted(references, key=lambda key: (key[1], key[0])):
        state = states[(language, stage)]
        with tempfile.TemporaryDirectory(prefix="preflight-", dir=work_root) as temporary:
            workspace = Path(temporary) / "workspace"
            workspace.mkdir()
            try:
                _materialize(root, manifest, language, stage, workspace)
            except (OSError, KeyError, TypeError, ValueError):
                raise E2aError("runtime_state_materialization_failed") from None
            rows.append(_validate_materialized_state(
                root=root, workspace=workspace, manifest=manifest, state=state
            ))
    return rows


def _target_framework(state: dict[str, Any]) -> str:
    frameworks = state.get("compile_obligations", {}).get("target_frameworks")
    _require(isinstance(frameworks, list) and len(frameworks) == 1
             and isinstance(frameworks[0], str) and frameworks[0],
             "runtime_target_framework_invalid")
    return frameworks[0]


def _run_sample(
    *,
    root: Path,
    work_root: Path,
    raw: Path,
    row: dict[str, Any],
    form: dict[str, Any],
    manifest: dict[str, Any],
    state: dict[str, Any],
    observed_environment: dict[str, Any],
    timeout: int,
) -> dict[str, Any]:
    language = row["language"]
    stage = row["stage"]
    prefix = f"samples/{row['position']:04d}-{language}-{row['form_id']}-{row['audit_condition']}"
    with tempfile.TemporaryDirectory(prefix=f"sample-{row['position']:04d}-", dir=work_root) as temporary:
        sample_root = Path(temporary)
        workspace = sample_root / "workspace"
        home = sample_root / "home"
        workspace.mkdir()
        home.mkdir()
        try:
            _materialize(root, manifest, language, stage, workspace)
        except (OSError, KeyError, TypeError, ValueError):
            raise E2aError("runtime_state_materialization_failed") from None
        state_summary = _validate_materialized_state(
            root=root, workspace=workspace, manifest=manifest, state=state
        )
        cache = home / ".nuget" / "packages"
        cache_before = _cache_summary(cache)
        _require(cache_before["file_count"] == 0 and cache_before["total_bytes"] == 0,
                 "runtime_cache_not_fresh")
        auth_candidates = [home / ".codex" / "auth.json", home / "auth.json"]
        _require(not any(path.exists() for path in auth_candidates), "runtime_auth_present")
        env = _sample_environment(home, observed_environment)
        project = manifest["languages"][language]["project_file"]
        cases = _cases(manifest, stage)
        payload = _case_payload(cases)
        input_file = sample_root / "cases.ndjson"
        input_file.write_bytes(payload)

        prerequisites: list[dict[str, Any]] = []
        for prereq_index, argv in enumerate(_prerequisite_argv(form, project), 1):
            record, _, _ = _execute_operation(
                label="prerequisite",
                argv=argv,
                cwd=workspace,
                env=env,
                raw=raw,
                stem=f"{prefix}/prerequisite-{prereq_index}",
                timeout=timeout,
            )
            prerequisites.append(record)

        argv = canonical_argv(
            form,
            project,
            audit_condition=row["audit_condition"],
            target_framework=_target_framework(state),
        )
        load_before = _host_load()
        operation, stdout, _ = _execute_operation(
            label="measured",
            argv=argv,
            cwd=workspace,
            env=env,
            raw=raw,
            stem=f"{prefix}/measured",
            timeout=timeout,
            input_transport=form["input_transport"],
            payload=payload,
            redirection_file=input_file,
        )
        evaluator_cases = cases if form["input_transport"] != "none" else []
        evaluator_stdout = _program_output_tail(stdout, evaluator_cases)
        checks = _cumulative_checks(manifest, language, stage)
        try:
            evaluator = _evaluate_output(evaluator_stdout, evaluator_cases, workspace, checks)
        except (OSError, KeyError, TypeError, ValueError, RuntimeError):
            raise E2aError("runtime_evaluator_failed") from None
        final_state = _runtime_source_snapshot(workspace, state)
        _require(final_state["source_tree_sha256"] == state_summary["source_tree_sha256"],
                 "runtime_source_changed")
        cache_after = _cache_summary(cache)
        return {
            **row,
            "state_id": state["state_id"],
            "source_tree_sha256": state["source_tree_sha256"],
            "prerequisites": prerequisites,
            "operation": operation,
            "evaluator": evaluator,
            "cache": {"before": cache_before, "after": cache_after, "fresh_before": True},
            "load_before": load_before,
            "load_after": _host_load(),
        }


def _write_raw_inventory(raw: Path) -> dict[str, Any]:
    value = raw_file_inventory(raw, exclude={"raw-inventory.json", "terminal-attempt.json"})
    document = _finish_hash(
        {"schema_version": RAW_INVENTORY_SCHEMA, **value},
        "inventory_sha256",
    )
    _atomic_json(raw / "raw-inventory.json", document)
    return document


def _attempt_document(attempt: dict[str, Any]) -> dict[str, Any]:
    return _finish_hash({"schema_version": ATTEMPT_SCHEMA, **attempt}, "attempt_sha256")


def _write_attempt(raw: Path, attempt: dict[str, Any]) -> dict[str, Any]:
    document = _attempt_document(attempt)
    _atomic_json(raw / "terminal-attempt.json", document)
    return document


def _failure_code(exc: BaseException) -> str:
    return exc.code if isinstance(exc, E2aError) else "unexpected_error"


def _validate_measurement(
    measurement: dict[str, Any],
    definition: dict[str, Any],
) -> list[str]:
    errors: list[str] = []
    expected_keys = {
        "schema_version", "definition_sha256", "inventory_sha256", "schedule_sha256",
        "runner_git_sha", "environment", "preflight", "samples", "measurement_sha256",
    }
    if set(measurement) != expected_keys:
        errors.append("measurement_schema_invalid")
    if measurement.get("schema_version") != MEASUREMENT_SCHEMA:
        errors.append("measurement_schema_version_invalid")
    if not _self_hash(measurement, "measurement_sha256"):
        errors.append("measurement_self_hash_mismatch")
    if measurement.get("definition_sha256") != definition.get("definition_sha256"):
        errors.append("measurement_definition_identity_mismatch")
    if measurement.get("inventory_sha256") != definition.get("inventory_sha256"):
        errors.append("measurement_inventory_identity_mismatch")
    if measurement.get("schedule_sha256") != definition.get("schedule_sha256"):
        errors.append("measurement_schedule_identity_mismatch")
    if measurement.get("runner_git_sha") != definition.get("runner", {}).get("e2a_runner_git_sha"):
        errors.append("measurement_runner_identity_mismatch")
    environment = measurement.get("environment")
    try:
        if not isinstance(environment, dict) or "container_self_observation" not in environment:
            errors.append("measurement_self_observation_missing")
        else:
            validate_environment(environment, definition)
    except E2aError as exc:
        errors.append(exc.code)
    samples = measurement.get("samples")
    schedule = definition.get("schedule")
    if not isinstance(samples, list) or not isinstance(schedule, list) or len(samples) != len(schedule):
        errors.append("measurement_sample_count_invalid")
    else:
        schedule_keys = (
            "position", "round", "pair_position", "task_id", "stage", "form_id",
            "audit_condition", "condition_position", "language", "language_position",
        )
        if [{key: sample.get(key) for key in schedule_keys} for sample in samples] != schedule:
            errors.append("measurement_schedule_order_mismatch")
        for sample in samples:
            operation = sample.get("operation")
            if not isinstance(operation, dict) or operation.get("exit_code") != 0 \
                    or operation.get("timed_out") is not False or operation.get("shell") is not False:
                errors.append("measurement_operation_invalid")
            evaluator = sample.get("evaluator")
            if not isinstance(evaluator, dict) or evaluator.get("ok") is not True:
                errors.append("measurement_evaluator_invalid")
            cache = sample.get("cache")
            if not isinstance(cache, dict) or cache.get("fresh_before") is not True \
                    or cache.get("before", {}).get("file_count") != 0:
                errors.append("measurement_cache_freshness_invalid")
    return sorted(set(errors))


def _resolve_runtime_input(
    root: Path,
    value: str | Path,
    *,
    require_inside_repository: bool,
    invalid_code: str,
) -> Path:
    candidate = Path(value)
    if not candidate.is_absolute():
        candidate = root / candidate
    _require(candidate.exists() and candidate.is_file() and not candidate.is_symlink(), invalid_code)
    try:
        resolved = candidate.resolve(strict=True)
    except OSError:
        raise E2aError(invalid_code) from None
    if require_inside_repository:
        _require(_inside(root, resolved), invalid_code)
    return resolved


def run(
    *,
    root: Path,
    definition: str | Path,
    inventory_path: str | Path,
    e2_definition: str | Path,
    manifest: str | Path,
    observed_environment: str | Path | dict[str, Any],
    runner_git_sha: str,
    work_root: str | Path,
    raw_output: str | Path,
) -> dict[str, Any]:
    """Execute the frozen E2a schedule and retain raw evidence outside Git."""

    root = root.resolve()
    raw = Path(raw_output).resolve()
    work = Path(work_root).resolve()
    definition_path = _resolve_runtime_input(
        root,
        definition,
        require_inside_repository=False,
        invalid_code="runtime_definition_file_invalid",
    )
    inventory_file = _resolve_runtime_input(
        root,
        inventory_path,
        require_inside_repository=False,
        invalid_code="runtime_inventory_file_invalid",
    )
    e2_path = _resolve_runtime_input(
        root,
        e2_definition,
        require_inside_repository=True,
        invalid_code="runtime_e2_definition_file_invalid",
    )
    manifest_path = _resolve_runtime_input(
        root,
        manifest,
        require_inside_repository=True,
        invalid_code="runtime_manifest_file_invalid",
    )
    _require(not _inside(root, raw) and not _inside(root, work), "runtime_output_inside_repository")
    _require(raw != work and not _inside(raw, work) and not _inside(work, raw),
             "runtime_work_raw_overlap")
    _require(not raw.exists() or (raw.is_dir() and not any(raw.iterdir())),
             "runtime_raw_output_not_empty")
    _require(work.is_dir() and not work.is_symlink(), "runtime_work_root_invalid")
    raw.mkdir(parents=True, exist_ok=True)

    attempt: dict[str, Any] = {
        "status": "running",
        "phase": "initialization",
        "definition_sha256": None,
        "runner_git_sha": None,
        "completed_preflight_states": 0,
        "completed_samples": 0,
        "current_position": None,
        "failure_code": None,
    }
    try:
        runner_sha = str(runner_git_sha).casefold()
        _require(HEX_40_RE.fullmatch(runner_sha) is not None, "runtime_runner_git_sha_invalid")
        definition_data = _json_object(definition_path, "runtime_definition_invalid")
        inventory_data = _json_object(inventory_file, "runtime_inventory_invalid")
        e2_data = _json_object(e2_path, "runtime_e2_definition_invalid")
        checked = check(definition_data, inventory_data, e2_data)
        _require(checked["ok"], "runtime_definition_check_failed")
        _require(runner_sha == definition_data["runner"]["e2a_runner_git_sha"],
                 "runtime_runner_git_sha_mismatch")
        _require(tracked_text_sha256(manifest_path) == ACCEPTED_MANIFEST_SHA256,
                 "runtime_manifest_identity_mismatch")
        _accepted_e2_reference(e2_data)
        observed_input = (
            observed_environment
            if isinstance(observed_environment, dict)
            else _json_object(_resolve(root, observed_environment), "runtime_environment_observation_invalid")
        )
        validate_environment(observed_input, definition_data, expected_commit=runner_sha)
        observed = json.loads(json.dumps(observed_input))
        observed["container_self_observation"] = _runtime_self_observation(work, observed)
        validate_environment(observed, definition_data, expected_commit=runner_sha)
        attempt.update({
            "definition_sha256": definition_data["definition_sha256"],
            "runner_git_sha": runner_sha,
        })

        attempt["phase"] = "manifest"
        try:
            manifest_data = load_manifest(root, manifest_path)
        except (OSError, KeyError, TypeError, ValueError):
            raise E2aError("runtime_manifest_invalid") from None
        states, references = _state_maps(definition_data, e2_data)

        attempt["phase"] = "sdk"
        with tempfile.TemporaryDirectory(prefix="sdk-", dir=work) as temporary:
            home = Path(temporary)
            sdk_record, sdk_stdout, _ = _execute_operation(
                label="sdk-version",
                argv=["dotnet", "--version"],
                cwd=root,
                env=_sample_environment(home, observed),
                raw=raw,
                stem="environment/sdk-version",
                timeout=COMMAND_TIMEOUT_SECONDS,
            )
            try:
                sdk = sdk_stdout.decode("ascii").strip()
            except UnicodeDecodeError:
                raise E2aError("runtime_dotnet_sdk_output_invalid") from None
            _require(sdk == DOTNET_SDK, "runtime_dotnet_sdk_mismatch")

        attempt["phase"] = "preflight"
        preflight = _preflight_states(
            root=root,
            work_root=work,
            manifest=manifest_data,
            states=states,
            references=references,
        )
        attempt["completed_preflight_states"] = len(preflight)
        _atomic_json(raw / "preflight/states.json", {"states": preflight})
        _atomic_json(raw / "environment/observation.json", observed)

        catalog = {row["form_id"]: row for row in definition_data["form_catalog"]}
        samples: list[dict[str, Any]] = []
        attempt["phase"] = "measurement"
        for row in definition_data["schedule"]:
            attempt["current_position"] = row["position"]
            sample = _run_sample(
                root=root,
                work_root=work,
                raw=raw,
                row=row,
                form=catalog[row["form_id"]],
                manifest=manifest_data,
                state=states[(row["language"], row["stage"])],
                observed_environment=observed,
                timeout=definition_data["measurement_contract"]["timeout_seconds"],
            )
            samples.append(sample)
            attempt["completed_samples"] = len(samples)

        measurement = _finish_hash({
            "schema_version": MEASUREMENT_SCHEMA,
            "definition_sha256": definition_data["definition_sha256"],
            "inventory_sha256": inventory_data["inventory_sha256"],
            "schedule_sha256": definition_data["schedule_sha256"],
            "runner_git_sha": runner_sha,
            "environment": observed,
            "preflight": {
                "state_count": len(preflight),
                "all_passed": True,
                "mode": "normalized-file-hash-compile-obligation-and-workspace-check",
            },
            "samples": samples,
        }, "measurement_sha256")
        _require(not _validate_measurement(measurement, definition_data),
                 "runtime_measurement_internal_validation_failed")
        _atomic_json(raw / "measurement.json", measurement)
        raw_inventory = _write_raw_inventory(raw)
        attempt.update({
            "status": "success",
            "phase": "complete",
            "current_position": None,
            "measurement_sha256": measurement["measurement_sha256"],
            "raw_inventory_sha256": raw_inventory["inventory_sha256"],
        })
        terminal = _write_attempt(raw, attempt)
        return {
            "measurement_sha256": measurement["measurement_sha256"],
            "raw_inventory_sha256": raw_inventory["inventory_sha256"],
            "attempt_sha256": terminal["attempt_sha256"],
            "samples": len(samples),
        }
    except BaseException as exc:
        attempt.update({
            "status": "failure",
            "failure_code": _failure_code(exc),
        })
        try:
            _write_attempt(raw, attempt)
        except BaseException:
            pass
        if isinstance(exc, E2aError):
            raise
        raise E2aError("unexpected_error") from None


def _stats(values: list[float | int]) -> dict[str, Any]:
    _require(bool(values), "report_empty_distribution")
    numbers = [float(value) for value in values]
    _require(all(math.isfinite(value) for value in numbers), "report_nonfinite_distribution")
    ordered = sorted(numbers)
    count = len(ordered)
    mean = statistics.fmean(ordered)
    standard_deviation = statistics.stdev(ordered) if count > 1 else None
    standard_error = standard_deviation / math.sqrt(count) if standard_deviation is not None else None
    # E2a has five rounds. Keep a small fixed t table so no SciPy dependency is needed.
    t95 = {1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776}.get(count - 1, 1.96)
    confidence = (
        {
            "method": "two-sided-descriptive-t-interval",
            "level": 0.95,
            "lower": mean - t95 * standard_error,
            "upper": mean + t95 * standard_error,
        }
        if standard_error is not None
        else {"method": "unavailable-single-observation", "level": 0.95, "lower": None, "upper": None}
    )
    return {
        "count": count,
        "min": ordered[0],
        "median": statistics.median(ordered),
        "mean": mean,
        "standard_deviation": standard_deviation,
        "standard_error": standard_error,
        "confidence_interval": confidence,
        "p95": ordered[max(0, math.ceil(count * 0.95) - 1)],
        "max": ordered[-1],
    }


def _geometric_mean(values: list[float]) -> float | None:
    if not values or any(value <= 0 or not math.isfinite(value) for value in values):
        return None
    return math.exp(statistics.fmean(math.log(value) for value in values))


def _public_sample(sample: dict[str, Any]) -> dict[str, Any]:
    operation = sample["operation"]
    evaluator = sample["evaluator"]
    diagnostics_value = operation["diagnostics"]
    stdout_bytes = operation["stdout"]["bytes"]
    stderr_bytes = operation["stderr"]["bytes"]
    return {
        "position": sample["position"],
        "round": sample["round"],
        "pair_position": sample["pair_position"],
        "task_id": sample["task_id"],
        "stage": sample["stage"],
        "form_id": sample["form_id"],
        "audit_condition": sample["audit_condition"],
        "condition_position": sample["condition_position"],
        "language": sample["language"],
        "language_position": sample["language_position"],
        "state_id": sample["state_id"],
        "wall_seconds": operation["wall_seconds"],
        "stdout_bytes": stdout_bytes,
        "stderr_bytes": stderr_bytes,
        "total_output_bytes": stdout_bytes + stderr_bytes,
        "diagnostic_occurrences": diagnostics_value["occurrence_count"],
        "diagnostic_codes": diagnostics_value["counts_by_code"],
        "nu1900_occurrences": diagnostics_value["nu1900_occurrences"],
        "prerequisite_count": len(sample["prerequisites"]),
        "evaluator": {
            "ok": evaluator["ok"],
            "case_count": evaluator["case_count"],
            "passed_case_count": evaluator["passed_case_count"],
            "wall_seconds": evaluator["wall_seconds"],
        },
        "cache_after": sample["cache"]["after"],
        "load_before": sample["load_before"],
        "load_after": sample["load_after"],
    }


def _absolute_summaries(
    samples: list[dict[str, Any]],
    catalog: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    groups: dict[tuple[str, str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for sample in samples:
        groups[(sample["task_id"], sample["form_id"], sample["audit_condition"], sample["language"])].append(sample)
    rows: list[dict[str, Any]] = []
    for (task_id, form_id, condition, language), values in sorted(groups.items()):
        codes: Counter[str] = Counter()
        for value in values:
            codes.update(value["diagnostic_codes"])
        rows.append({
            "task_id": task_id,
            "form_id": form_id,
            "operation": catalog[form_id]["operation"],
            "audit_condition": condition,
            "language": language,
            "wall_seconds": _stats([value["wall_seconds"] for value in values]),
            "stdout_bytes": _stats([value["stdout_bytes"] for value in values]),
            "stderr_bytes": _stats([value["stderr_bytes"] for value in values]),
            "total_output_bytes": _stats([value["total_output_bytes"] for value in values]),
            "diagnostic_occurrences": _stats([value["diagnostic_occurrences"] for value in values]),
            "diagnostic_codes": dict(sorted(codes.items())),
            "nu1900_occurrences": sum(value["nu1900_occurrences"] for value in values),
        })
    return rows


def _paired_language_summaries(
    samples: list[dict[str, Any]],
    catalog: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    indexed = {
        (row["round"], row["task_id"], row["form_id"], row["audit_condition"], row["language"]): row
        for row in samples
    }
    cells = sorted({(row["task_id"], row["form_id"], row["audit_condition"]) for row in samples})
    rows: list[dict[str, Any]] = []
    for task_id, form_id, condition in cells:
        csharp_values: list[float] = []
        fsharp_values: list[float] = []
        deltas: list[float] = []
        ratios: list[float] = []
        output_deltas: list[float] = []
        diagnostic_deltas: list[float] = []
        for round_number in range(1, ROUNDS + 1):
            csharp = indexed[(round_number, task_id, form_id, condition, "csharp")]
            fsharp = indexed[(round_number, task_id, form_id, condition, "fsharp")]
            csharp_seconds = float(csharp["wall_seconds"])
            fsharp_seconds = float(fsharp["wall_seconds"])
            csharp_values.append(csharp_seconds)
            fsharp_values.append(fsharp_seconds)
            deltas.append(fsharp_seconds - csharp_seconds)
            if csharp_seconds > 0:
                ratios.append(fsharp_seconds / csharp_seconds)
            output_deltas.append(float(fsharp["total_output_bytes"] - csharp["total_output_bytes"]))
            diagnostic_deltas.append(float(
                fsharp["diagnostic_occurrences"] - csharp["diagnostic_occurrences"]
            ))
        rows.append({
            "task_id": task_id,
            "form_id": form_id,
            "operation": catalog[form_id]["operation"],
            "audit_condition": condition,
            "pair_count": ROUNDS,
            "csharp_wall_seconds": _stats(csharp_values),
            "fsharp_wall_seconds": _stats(fsharp_values),
            "fsharp_minus_csharp_seconds": _stats(deltas),
            "fsharp_over_csharp_ratio": {
                "count": len(ratios),
                "geometric_mean": _geometric_mean(ratios),
                "distribution": _stats(ratios) if ratios else None,
                "missing_reason": None if len(ratios) == ROUNDS else "zero-csharp-duration",
            },
            "fsharp_minus_csharp_output_bytes": _stats(output_deltas),
            "fsharp_minus_csharp_diagnostic_occurrences": _stats(diagnostic_deltas),
        })
    return rows


def _audit_contrast_summaries(
    samples: list[dict[str, Any]],
    catalog: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    indexed = {
        (row["round"], row["task_id"], row["form_id"], row["language"], row["audit_condition"]): row
        for row in samples
    }
    cells = sorted({
        (row["task_id"], row["form_id"], row["language"])
        for row in samples if catalog[row["form_id"]]["audit_eligible"]
    })
    rows: list[dict[str, Any]] = []
    for task_id, form_id, language in cells:
        on_values: list[float] = []
        off_values: list[float] = []
        deltas: list[float] = []
        ratios: list[float] = []
        output_deltas: list[float] = []
        nu1900_on = 0
        nu1900_off = 0
        for round_number in range(1, ROUNDS + 1):
            on = indexed[(round_number, task_id, form_id, language, "audit_on")]
            off = indexed[(round_number, task_id, form_id, language, "audit_off")]
            on_seconds = float(on["wall_seconds"])
            off_seconds = float(off["wall_seconds"])
            on_values.append(on_seconds)
            off_values.append(off_seconds)
            deltas.append(on_seconds - off_seconds)
            if off_seconds > 0:
                ratios.append(on_seconds / off_seconds)
            output_deltas.append(float(on["total_output_bytes"] - off["total_output_bytes"]))
            nu1900_on += on["nu1900_occurrences"]
            nu1900_off += off["nu1900_occurrences"]
        rows.append({
            "task_id": task_id,
            "form_id": form_id,
            "operation": catalog[form_id]["operation"],
            "language": language,
            "pair_count": ROUNDS,
            "audit_on_wall_seconds": _stats(on_values),
            "audit_off_wall_seconds": _stats(off_values),
            "audit_on_minus_off_seconds": _stats(deltas),
            "audit_on_over_off_ratio": {
                "count": len(ratios),
                "geometric_mean": _geometric_mean(ratios),
                "distribution": _stats(ratios) if ratios else None,
                "missing_reason": None if len(ratios) == ROUNDS else "zero-audit-off-duration",
            },
            "audit_on_minus_off_output_bytes": _stats(output_deltas),
            "nu1900_occurrences": {"audit_on": nu1900_on, "audit_off": nu1900_off},
        })
    return rows


def _exposure_envelope(
    samples: list[dict[str, Any]],
    inventory_data: dict[str, Any],
) -> dict[str, Any]:
    timing_groups: dict[tuple[str, str, str], list[float]] = defaultdict(list)
    for row in samples:
        if row["audit_condition"] == "audit_on":
            timing_groups[(row["language"], row["task_id"], row["form_id"])].append(
                float(row["wall_seconds"])
            )
    means = {key: statistics.fmean(values) for key, values in timing_groups.items()}
    detail: list[dict[str, Any]] = []
    totals: Counter[tuple[str, str]] = Counter()
    invocation_totals: Counter[tuple[str, str]] = Counter()
    for frequency in inventory_data["frequencies"]:
        key = (frequency["language"], frequency["task_id"], frequency["form_id"])
        _require(key in means and len(timing_groups[key]) == ROUNDS,
                 "report_exposure_timing_missing")
        seconds = frequency["count"] * means[key]
        group = (frequency["configuration_id"], frequency["language"])
        totals[group] += seconds
        invocation_totals[group] += frequency["count"]
        detail.append({
            "configuration_id": frequency["configuration_id"],
            "language": frequency["language"],
            "task_id": frequency["task_id"],
            "form_id": frequency["form_id"],
            "invocation_count": frequency["count"],
            "matched_audit_on_mean_seconds": means[key],
            "mechanical_count_times_mean_seconds": seconds,
        })
    agent = {
        (row["configuration_id"], row["language"]): row
        for row in inventory_data["e1_agent_process_wall_seconds"]
    }
    summary = [
        {
            "configuration_id": configuration,
            "language": language,
            "observed_e1_invocation_count": invocation_totals[(configuration, language)],
            "mechanical_tool_exposure_seconds": totals[(configuration, language)],
            "observed_e1_agent_process_seconds": agent[(configuration, language)]["total_seconds"],
            "observed_e1_run_count": agent[(configuration, language)]["run_count"],
        }
        for configuration, language in sorted(agent)
    ]
    return {
        "method": (
            "This is a mechanical invocation-count × matched-duration timing counterfactual. "
            "It is not subtracted from agent cost, is not a mediation estimate, and does not "
            "identify behavioral feedback effects."
        ),
        "candidate_aligned_condition": "audit_on",
        "detail": detail,
        "by_configuration_and_language": summary,
    }


def _build_report(
    *,
    definition: dict[str, Any],
    inventory_data: dict[str, Any],
    measurement: dict[str, Any],
    raw_inventory: dict[str, Any],
) -> dict[str, Any]:
    _validate_inventory(inventory_data)
    _require(check(definition, inventory_data)["ok"], "report_definition_invalid")
    _require(not _validate_measurement(measurement, definition), "report_measurement_invalid")
    _require(raw_inventory.get("schema_version") == RAW_INVENTORY_SCHEMA
             and _self_hash(raw_inventory, "inventory_sha256"),
             "report_raw_inventory_invalid")
    samples = [_public_sample(sample) for sample in measurement["samples"]]
    catalog = {row["form_id"]: row for row in inventory_data["form_catalog"]}
    report_document = {
        "schema_version": REPORT_SCHEMA,
        "definition_sha256": definition["definition_sha256"],
        "inventory_sha256": inventory_data["inventory_sha256"],
        "e1_report_sha256": inventory_data["source"]["e1_report_sha256"],
        "measurement_sha256": measurement["measurement_sha256"],
        "schedule_sha256": definition["schedule_sha256"],
        "runner_git_sha": definition["runner"]["e2a_runner_git_sha"],
        "accepted_e2": definition["accepted_e2"],
        "environment": measurement["environment"],
        "mismatch_ledger": definition["mismatch_ledger"],
        "raw_evidence": {
            "inventory_sha256": raw_inventory["inventory_sha256"],
            "file_count": raw_inventory["file_count"],
            "total_bytes": raw_inventory["total_bytes"],
            "set_sha256": raw_inventory["set_sha256"],
        },
        "preflight": measurement["preflight"],
        "samples": samples,
        "absolute_distributions": _absolute_summaries(samples, catalog),
        "paired_language_effects": _paired_language_summaries(samples, catalog),
        "audit_contrasts": _audit_contrast_summaries(samples, catalog),
        "mechanical_tool_exposure_envelope": _exposure_envelope(samples, inventory_data),
        "v3_nu1900": inventory_data["nu1900"],
        "measured_nu1900": {
            "by_language_and_audit": [
                {
                    "language": language,
                    "audit_condition": condition,
                    "occurrences": sum(
                        row["nu1900_occurrences"] for row in samples
                        if row["language"] == language and row["audit_condition"] == condition
                    ),
                }
                for language in LANGUAGES for condition in ("audit_on", "audit_off")
            ],
            "caveat": "Counts are repeated emitted diagnostic lines, not independent vulnerabilities or defects.",
        },
        "interpretation": {
            "scope": "descriptive model-free command and environment alignment only",
            "remainder": (
                "Any difference outside the mechanical envelope remains inseparable from model interaction, "
                "repair behavior, unavailable within-task cache history, and other trajectory effects."
            ),
            "non_mediation": (
                "The envelope is not subtracted from agent cost and is not a mediation or causal decomposition."
            ),
        },
        "missingness": {
            "e1_per_command_duration": {
                "value": None,
                "reason": "v3 command events have no timestamps or durations",
            },
            "e1_within_task_cache_state": {
                "value": None,
                "reason": "package-cache state at each retained E1 command is unavailable",
            },
            "internal_compiler_phase_timing": {
                "value": None,
                "reason": "ordinary dotnet commands expose no validated internal phase timing",
            },
            "machine_cold_state": {
                "value": None,
                "reason": "host load is observed but OS page cache and machine-cold state are uncontrolled",
            },
        },
    }
    result = _finish_hash(report_document, "report_sha256")
    validated = validate_report(result, definition, inventory_data)
    _require(validated["ok"], "report_internal_validation_failed")
    return result


def _walk_json(value: Any, path: tuple[str, ...] = ()) -> Iterable[tuple[tuple[str, ...], Any]]:
    yield path, value
    if isinstance(value, dict):
        for key, child in value.items():
            yield from _walk_json(child, (*path, str(key)))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _walk_json(child, (*path, str(index)))


def _validate_publishable(value: Any, *, allow_relative_filenames: bool) -> None:
    forbidden_keys = {
        "command", "argv", "stdout", "stderr", "aggregated_output", "thread_id",
        "attempt_id", "prompt", "transcript", "source_text", "input_payload",
        "expected", "actual", "hostname", "environment_variables", "auth_json",
    }
    for path, item in _walk_json(value):
        if path:
            normalized = path[-1].casefold().replace("-", "_")
            _require(normalized not in forbidden_keys, "publishable_forbidden_field")
        if isinstance(item, float):
            _require(math.isfinite(item), "publishable_nonfinite_number")
        if isinstance(item, str):
            _require(not item.startswith("/") and _ABSOLUTE_WINDOWS_RE.match(item) is None,
                     "publishable_absolute_path")
            _require(_CREDENTIAL_RE.search(item) is None, "publishable_credential_like_value")
            if not allow_relative_filenames and path and path[-1].casefold() in {"file", "path"}:
                raise E2aError("publishable_path_field")


def validate_report(
    report_data: dict[str, Any],
    definition: dict[str, Any],
    inventory_data: dict[str, Any],
) -> dict[str, Any]:
    errors: list[str] = []
    expected_keys = {
        "schema_version", "definition_sha256", "inventory_sha256", "e1_report_sha256",
        "measurement_sha256", "schedule_sha256", "runner_git_sha", "accepted_e2",
        "environment", "mismatch_ledger", "raw_evidence", "preflight", "samples",
        "absolute_distributions", "paired_language_effects", "audit_contrasts",
        "mechanical_tool_exposure_envelope", "v3_nu1900", "measured_nu1900",
        "interpretation", "missingness", "report_sha256",
    }
    if set(report_data) != expected_keys:
        errors.append("report_schema_invalid")
    if report_data.get("schema_version") != REPORT_SCHEMA:
        errors.append("report_schema_version_invalid")
    if not _self_hash(report_data, "report_sha256"):
        errors.append("report_self_hash_mismatch")
    if report_data.get("definition_sha256") != definition.get("definition_sha256"):
        errors.append("report_definition_identity_mismatch")
    if report_data.get("inventory_sha256") != inventory_data.get("inventory_sha256"):
        errors.append("report_inventory_identity_mismatch")
    if report_data.get("e1_report_sha256") != inventory_data.get("source", {}).get("e1_report_sha256"):
        errors.append("report_e1_identity_mismatch")
    if report_data.get("schedule_sha256") != definition.get("schedule_sha256"):
        errors.append("report_schedule_identity_mismatch")
    if report_data.get("runner_git_sha") != definition.get("runner", {}).get("e2a_runner_git_sha"):
        errors.append("report_runner_identity_mismatch")
    if report_data.get("accepted_e2") != definition.get("accepted_e2"):
        errors.append("report_accepted_e2_identity_mismatch")
    if report_data.get("mismatch_ledger") != definition.get("mismatch_ledger"):
        errors.append("report_mismatch_ledger_invalid")
    try:
        validate_environment(report_data.get("environment", {}), definition)
    except E2aError as exc:
        errors.append(exc.code)

    samples = report_data.get("samples")
    schedule = definition.get("schedule")
    if not isinstance(samples, list) or not isinstance(schedule, list) or len(samples) != len(schedule):
        errors.append("report_sample_count_invalid")
    else:
        schedule_keys = (
            "position", "round", "pair_position", "task_id", "stage", "form_id",
            "audit_condition", "condition_position", "language", "language_position",
        )
        if [{key: row.get(key) for key in schedule_keys} for row in samples] != schedule:
            errors.append("report_sample_schedule_mismatch")
        for row in samples:
            for field in (
                "wall_seconds", "stdout_bytes", "stderr_bytes", "total_output_bytes",
                "diagnostic_occurrences", "nu1900_occurrences", "prerequisite_count",
            ):
                value = row.get(field)
                if not isinstance(value, (int, float)) or isinstance(value, bool) \
                        or not math.isfinite(float(value)) or value < 0:
                    errors.append("report_sample_measure_invalid")
            if row.get("total_output_bytes") != row.get("stdout_bytes", 0) + row.get("stderr_bytes", 0):
                errors.append("report_sample_output_total_invalid")
            evaluator = row.get("evaluator")
            if not isinstance(evaluator, dict) or evaluator.get("ok") is not True \
                    or evaluator.get("case_count") != evaluator.get("passed_case_count"):
                errors.append("report_sample_evaluator_invalid")
    if isinstance(samples, list):
        try:
            catalog = {row["form_id"]: row for row in inventory_data["form_catalog"]}
            if not _derived_json_equal(
                report_data.get("absolute_distributions"),
                _absolute_summaries(samples, catalog),
            ):
                errors.append("report_absolute_distributions_mismatch")
            if not _derived_json_equal(
                report_data.get("paired_language_effects"),
                _paired_language_summaries(samples, catalog),
            ):
                errors.append("report_paired_language_effects_mismatch")
            if not _derived_json_equal(
                report_data.get("audit_contrasts"),
                _audit_contrast_summaries(samples, catalog),
            ):
                errors.append("report_audit_contrasts_mismatch")
            if not _derived_json_equal(
                report_data.get("mechanical_tool_exposure_envelope"),
                _exposure_envelope(samples, inventory_data),
            ):
                errors.append("report_exposure_envelope_mismatch")
        except (E2aError, KeyError, TypeError, ValueError, statistics.StatisticsError):
            errors.append("report_summary_recomputation_failed")
    if report_data.get("v3_nu1900") != inventory_data.get("nu1900"):
        errors.append("report_v3_nu1900_mismatch")
    raw_evidence = report_data.get("raw_evidence")
    if not isinstance(raw_evidence, dict) or set(raw_evidence) != {
        "inventory_sha256", "file_count", "total_bytes", "set_sha256"
    } or HEX_64_RE.fullmatch(str(raw_evidence.get("inventory_sha256", ""))) is None \
            or HEX_64_RE.fullmatch(str(raw_evidence.get("set_sha256", ""))) is None \
            or not isinstance(raw_evidence.get("file_count"), int) \
            or raw_evidence.get("file_count", 0) <= 0 \
            or not isinstance(raw_evidence.get("total_bytes"), int) \
            or raw_evidence.get("total_bytes", -1) < 0:
        errors.append("report_raw_evidence_invalid")
    missingness = report_data.get("missingness")
    if not isinstance(missingness, dict) or not missingness:
        errors.append("report_missingness_invalid")
    else:
        for row in missingness.values():
            if not isinstance(row, dict) or set(row) != {"value", "reason"} or row.get("value") is not None:
                errors.append("report_missingness_entry_invalid")
    try:
        _validate_publishable(report_data, allow_relative_filenames=False)
    except E2aError as exc:
        errors.append(exc.code)
    return {
        "ok": not errors,
        "errors": sorted(set(errors)),
        "report_sha256": report_data.get("report_sha256"),
    }


def markdown_report(report_data: dict[str, Any]) -> str:
    lines = [
        "# Workstream E2a exact-command, host-aligned model-free baseline",
        "",
        f"Definition: `{report_data['definition_sha256']}`  ",
        f"Inventory: `{report_data['inventory_sha256']}`  ",
        f"Runner: `{report_data['runner_git_sha']}`  ",
        f"Samples: {len(report_data['samples'])} across five paired rounds.",
        "",
        "No candidate, Codex process, authentication cache, model endpoint, or paid request was used.",
        "The accepted offline E2 result remains a separate ecology and is not pooled with E2a.",
        "",
        "## Paired command timing",
        "",
        "| Task | Form | Operation | Audit | C# mean s | F# mean s | F#−C# mean s | F#/C# geometric mean |",
        "|---|---|---|---|---:|---:|---:|---:|",
    ]
    for row in report_data["paired_language_effects"]:
        ratio = row["fsharp_over_csharp_ratio"]["geometric_mean"]
        ratio_text = "unavailable" if ratio is None else f"{ratio:.6f}"
        lines.append(
            f"| {row['task_id']} | {row['form_id']} | {row['operation']} | {row['audit_condition']} | "
            f"{row['csharp_wall_seconds']['mean']:.6f} | {row['fsharp_wall_seconds']['mean']:.6f} | "
            f"{row['fsharp_minus_csharp_seconds']['mean']:.6f} | {ratio_text} |"
        )
    lines.extend([
        "",
        "## Audit-on versus audit-off control",
        "",
        "| Task | Form | Language | Audit-on mean s | Audit-off mean s | On−off mean s | On/off geometric mean | NU1900 on/off |",
        "|---|---|---|---:|---:|---:|---:|---:|",
    ])
    for row in report_data["audit_contrasts"]:
        ratio = row["audit_on_over_off_ratio"]["geometric_mean"]
        ratio_text = "unavailable" if ratio is None else f"{ratio:.6f}"
        nu = row["nu1900_occurrences"]
        lines.append(
            f"| {row['task_id']} | {row['form_id']} | {row['language']} | "
            f"{row['audit_on_wall_seconds']['mean']:.6f} | {row['audit_off_wall_seconds']['mean']:.6f} | "
            f"{row['audit_on_minus_off_seconds']['mean']:.6f} | {ratio_text} | "
            f"{nu['audit_on']}/{nu['audit_off']} |"
        )
    lines.extend([
        "",
        "## Mechanical tool-exposure envelope",
        "",
        "| Configuration | Language | Observed invocations | Mechanical seconds | Observed E1 agent seconds |",
        "|---|---|---:|---:|---:|",
    ])
    for row in report_data["mechanical_tool_exposure_envelope"]["by_configuration_and_language"]:
        lines.append(
            f"| {row['configuration_id']} | {row['language']} | {row['observed_e1_invocation_count']} | "
            f"{row['mechanical_tool_exposure_seconds']:.6f} | {row['observed_e1_agent_process_seconds']:.6f} |"
        )
    lines.extend([
        "",
        report_data["mechanical_tool_exposure_envelope"]["method"],
        "",
        "## NU1900 and output-volume boundary",
        "",
        "The authenticated v3 streams contained 197 F# NU1900 lines and zero C# NU1900 lines. "
        "They are repeated emitted diagnostic lines, not independent defects. Absolute stdout, stderr, "
        "total output bytes, diagnostic occurrences, and descriptive uncertainty are retained in the JSON report.",
        "",
        "## Remaining mismatches",
        "",
    ])
    for row in report_data["mismatch_ledger"]:
        lines.append(f"- `{row['component']}` — {row['status']}: {row['bound']}")
    lines.extend([
        "",
        report_data["interpretation"]["remainder"],
        report_data["interpretation"]["non_mediation"],
        "",
    ])
    return "\n".join(lines)


def _record_evidence_errors(raw: Path, record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for stream_name in ("stdout", "stderr"):
        stream = record.get(stream_name)
        if not isinstance(stream, dict):
            errors.append("raw_stream_reference_invalid")
            continue
        try:
            relative = _safe_relative(stream["file"], label="raw stream")
            content = (raw / relative).read_bytes()
            if len(content) != stream.get("bytes") or _sha(content) != stream.get("sha256"):
                errors.append("raw_stream_identity_mismatch")
        except (OSError, KeyError, TypeError, ValueError):
            errors.append("raw_stream_unavailable")
    try:
        metadata_relative = _safe_relative(record["metadata_file"], label="raw metadata")
        metadata = _json_object(raw / metadata_relative, "raw_metadata_invalid")
        expected = dict(record)
        expected.pop("metadata_file", None)
        if metadata != expected:
            errors.append("raw_metadata_identity_mismatch")
    except (E2aError, KeyError, TypeError, ValueError):
        errors.append("raw_metadata_unavailable")
    return errors


def _audit_raw(
    raw: Path,
    definition: dict[str, Any],
) -> tuple[dict[str, Any] | None, dict[str, Any] | None, list[str]]:
    errors: list[str] = []
    measurement: dict[str, Any] | None = None
    raw_inventory: dict[str, Any] | None = None
    try:
        raw_inventory = _json_object(raw / "raw-inventory.json", "raw_inventory_unavailable")
        if raw_inventory.get("schema_version") != RAW_INVENTORY_SCHEMA \
                or not _self_hash(raw_inventory, "inventory_sha256"):
            errors.append("raw_inventory_invalid")
        else:
            observed = raw_file_inventory(raw, exclude={"raw-inventory.json", "terminal-attempt.json"})
            expected = {key: raw_inventory.get(key) for key in (
                "files", "file_count", "total_bytes", "set_sha256"
            )}
            if observed != expected:
                errors.append("raw_inventory_disk_mismatch")
    except (E2aError, OSError, ValueError):
        errors.append("raw_inventory_unavailable")
    try:
        measurement = _json_object(raw / "measurement.json", "measurement_unavailable")
        errors.extend(_validate_measurement(measurement, definition))
        for sample in measurement.get("samples", []):
            for prereq in sample.get("prerequisites", []):
                errors.extend(_record_evidence_errors(raw, prereq))
            if isinstance(sample.get("operation"), dict):
                errors.extend(_record_evidence_errors(raw, sample["operation"]))
    except (E2aError, OSError, ValueError):
        errors.append("measurement_unavailable")
    try:
        terminal = _json_object(raw / "terminal-attempt.json", "terminal_attempt_unavailable")
        if terminal.get("schema_version") != ATTEMPT_SCHEMA \
                or not _self_hash(terminal, "attempt_sha256") \
                or terminal.get("status") != "success" \
                or measurement is None \
                or terminal.get("measurement_sha256") != measurement.get("measurement_sha256") \
                or raw_inventory is None \
                or terminal.get("raw_inventory_sha256") != raw_inventory.get("inventory_sha256"):
            errors.append("terminal_attempt_invalid")
    except (E2aError, OSError, ValueError):
        errors.append("terminal_attempt_unavailable")
    return measurement, raw_inventory, sorted(set(errors))


def report(
    *,
    definition: dict[str, Any],
    inventory_data: dict[str, Any],
    raw_output: str | Path,
    output_json: str | Path | None = None,
    output_markdown: str | Path | None = None,
) -> dict[str, Any]:
    """Synthesize a publish-safe E2a report from audited external raw evidence."""

    raw = Path(raw_output).resolve()
    measurement, raw_inventory, errors = _audit_raw(raw, definition)
    _require(not errors and measurement is not None and raw_inventory is not None,
             "report_raw_audit_failed")
    result = _build_report(
        definition=definition,
        inventory_data=inventory_data,
        measurement=measurement,
        raw_inventory=raw_inventory,
    )
    if output_json is not None or output_markdown is not None:
        _require(output_json is not None and output_markdown is not None,
                 "report_outputs_must_be_paired")
        json_path = Path(output_json).resolve()
        markdown_path = Path(output_markdown).resolve()
        _require(json_path != markdown_path and not _inside(raw, json_path)
                 and not _inside(raw, markdown_path), "report_output_path_invalid")
        _require(not json_path.exists() and not markdown_path.exists(), "report_output_already_exists")
        try:
            _atomic_bytes(markdown_path, markdown_report(result).encode("utf-8"))
            _atomic_json(json_path, result)
        except BaseException:
            markdown_path.unlink(missing_ok=True)
            json_path.unlink(missing_ok=True)
            raise
    return result


def audit(
    *,
    definition: dict[str, Any],
    inventory_data: dict[str, Any],
    report_data: dict[str, Any],
    raw_output: str | Path,
    e1_report: str | Path | None = None,
    archive_root: str | Path | None = None,
) -> dict[str, Any]:
    """Reconcile report, measurement, every raw file, and optionally E1 again."""

    errors = list(validate_report(report_data, definition, inventory_data)["errors"])
    measurement, raw_inventory, raw_errors = _audit_raw(Path(raw_output).resolve(), definition)
    errors.extend(raw_errors)
    if measurement is not None and raw_inventory is not None:
        try:
            expected = _build_report(
                definition=definition,
                inventory_data=inventory_data,
                measurement=measurement,
                raw_inventory=raw_inventory,
            )
            if not _report_recomputation_equal(report_data, expected):
                errors.append("report_differs_from_raw_recomputation")
        except E2aError as exc:
            errors.append(exc.code)
    if (e1_report is None) != (archive_root is None):
        errors.append("e1_reaudit_inputs_incomplete")
    elif e1_report is not None and archive_root is not None:
        try:
            reconstructed = inventory(e1_report, archive_root)
            if reconstructed != inventory_data:
                errors.append("inventory_differs_from_e1_recomputation")
        except E2aError as exc:
            errors.append(exc.code)
    return {
        "ok": not errors,
        "errors": sorted(set(errors)),
        "report_sha256": report_data.get("report_sha256"),
    }
