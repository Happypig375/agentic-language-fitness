"""Archive-only, deterministic Workstream E1 forensic attribution.

This module deliberately consumes retained JSON envelopes and event sidecars only;
it never starts a candidate, evaluator, model, or network process.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shlex
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from .audit import audit_run
from .metrics import EXCLUDED_PARTS, SOURCE_SUFFIXES, TOKEN_RE
from .models import Usage
from .variance import _artifact_hashes, _hash, _source_tree

try:
    import tiktoken
except ImportError:  # pragma: no cover
    tiktoken = None

SCHEMA_VERSION = "workstream-e1-report-v1"
CLASSIFIER_VERSION = "e1-bash-v1"
DIAGNOSTIC_VERSION = "e1-dotnet-diagnostics-v1"
SERIALIZATION_VERSION = "e1-lf-length-framed-v1"
REPORT_TYPE = "workstream-d-v3-non-counting-calibration"
OUTPUT_REPORT_TYPE = "workstream-e1-archive-forensic-attribution"
FAMILY_ID = "workstream-d-language-v3"
EXPECTED_ATTEMPTS = {
    "h": {"cal-h-primary-csharp-01", "cal-h-primary-fsharp-01"},
    "m": {"cal-m-primary-csharp-01", "cal-m-primary-fsharp-01",
          "cal-m-reverse-csharp-01", "cal-m-reverse-fsharp-01"},
    "l": {"cal-l-primary-csharp-01", "cal-l-primary-fsharp-01",
          "cal-l-reverse-csharp-01", "cal-l-reverse-fsharp-01"},
}
EXPECTED_TASK_IDS = (
    "001-priority", "002-overdue", "003-at-risk-window", "004-vip-ready",
    "005-null-order-robustness", "006-transition-validation",
    "007-query-engine-refactor", "008-summary-api",
)
COVERED_EVENT_SHAPES = (
    "thread.started", "turn.started", "turn.completed",
    "item.started:command_execution", "item.completed:command_execution",
    "item.started:file_change", "item.completed:file_change",
    "item.completed:agent_message", "item.started:todo_list",
    "item.updated:todo_list", "item.completed:todo_list",
)
COVERED_COMMAND_EQUIVALENCE_CLASSES = (
    "atomic", "and-if", "pipeline", "or-if", "sequence", "newline",
    "mixed-restore-build-run", "quoted-data-argument",
    "input-redirection", "output-redirection", "append-redirection", "stderr-redirection",
    "heredoc-ambiguous", "substitution-ambiguous", "parentheses-ambiguous",
)
USAGE_FIELDS = tuple(Usage.__dataclass_fields__)
LABELS = (
    "source_inspection",
    "search",
    "edit",
    "build",
    "test_or_run",
    "project_configuration",
    "environment",
    "other",
)
NULL_LEDGER = {
    "candidate_command_duration_seconds": "v3 command events contain no timestamps or durations",
    "candidate_event_duration_seconds": "v3 event streams contain no timestamps or durations",
    "time_before_first_post_edit_build_seconds": "candidate event timing is unavailable",
    "time_to_first_post_edit_build_seconds": "candidate event timing is unavailable",
    "time_after_first_post_edit_build_seconds": "candidate event timing is unavailable",
    "model_interaction_count": "agent-message items are not model interaction records",
    "per_interaction_usage": "v3 retains only one aggregate provider usage record per task",
    "first_patch_tokens": "first-patch provider usage is not retained",
    "phase_input_tokens": "phase-specific provider input usage is not retained",
    "phase_output_tokens": "phase-specific provider output usage is not retained",
    "phase_reasoning_tokens": "phase-specific provider reasoning usage is not retained",
    "unique_source_exposure": "aggregate input cannot identify unique source exposure",
    "repeated_source_exposure": "aggregate input cannot identify repeated source exposure",
    "transcript_tool_replay_tokens": "replayed transcript and tool tokens are not observable",
    "peak_context_tokens": "peak context size is not retained",
    "compaction": "compaction markers are not retained",
    "full_evaluator_output_volume": "only bounded evaluator tails are retained",
    "intermediate_patch_content": "only completed file-change metadata and committed boundaries are retained",
}

def _sha_bytes(raw: bytes) -> str: return hashlib.sha256(raw).hexdigest()

def _null(reason: str) -> dict[str, Any]:
    return {"value": None, "reason": reason}


def _unwrap_bash(command: Any) -> tuple[str | None, list[str]]:
    """Accept exactly the Linux v3 `bash -lc PAYLOAD` envelope."""
    if not isinstance(command, str):
        return None, ["command_not_string"]
    try:
        words = shlex.split(command, posix=True)
    except ValueError:
        return None, ["invalid_wrapper_quoting"]
    if len(words) != 3 or words[0] not in {"bash", "/bin/bash", "/usr/bin/bash"} or words[1] != "-lc":
        return None, ["unsupported_shell_wrapper"]
    return words[2], []


_CONNECTORS = {
    "&&": "and_if",
    "||": "or_if",
    "|": "pipeline",
    ";": "sequence",
    "\n": "newline",
}


def _scan_payload(payload: str) -> tuple[list[str], list[str], list[dict[str, bool]], list[str]]:
    """Split only unquoted v3 connectors and record redirection facts."""
    atoms: list[str] = []
    connectors: list[str] = []
    redirections: list[dict[str, bool]] = []
    reasons: set[str] = set()
    start = 0
    quote: str | None = None
    escaped = False
    paren_depth = 0
    redir = {"has_input": False, "has_output": False, "append_output": False,
             "has_stderr": False, "has_heredoc": False}

    def finish(end: int, connector: str | None = None) -> None:
        nonlocal start, redir
        atoms.append(payload[start:end].strip())
        redirections.append(dict(redir))
        redir = {"has_input": False, "has_output": False, "append_output": False,
                 "has_stderr": False, "has_heredoc": False}
        if connector is not None:
            connectors.append(_CONNECTORS[connector])

    i = 0
    while i < len(payload):
        ch = payload[i]
        nxt = payload[i + 1] if i + 1 < len(payload) else ""
        if escaped:
            escaped = False
            i += 1
            continue
        if ch == "\\" and quote != "'":
            escaped = True
            i += 1
            continue
        if quote:
            if ch == quote:
                quote = None
            elif quote == '"' and ch == "$" and nxt == "(":
                reasons.add("command_substitution")
            elif quote == '"' and ch == "`":
                reasons.add("backtick_substitution")
            i += 1
            continue
        if ch in "'\"":
            quote = ch
            i += 1
            continue
        if ch == "$" and nxt == "(":
            reasons.add("command_substitution")
        if ch == "`":
            reasons.add("backtick_substitution")
        if ch in "()":
            reasons.add("unsupported_parentheses")
            paren_depth += 1 if ch == "(" else -1
            if paren_depth < 0:
                reasons.add("unbalanced_parentheses")
                paren_depth = 0
        if ch in "{}":
            reasons.add("unsupported_brace_group")
        if ch == "<":
            redir["has_input"] = True
            if nxt == "<":
                redir["has_heredoc"] = True
                reasons.add("heredoc")
            if nxt == "(":
                reasons.add("process_substitution")
        elif ch == ">":
            redir["has_output"] = True
            redir["append_output"] = redir["append_output"] or nxt == ">" or (i > start and payload[i - 1] == ">")
            prefix = payload[max(start, i - 2):i]
            redir["has_stderr"] = bool(re.search(r"(?:^|\D)2$", prefix))
            if nxt == "(":
                reasons.add("process_substitution")
        connector: str | None = None
        width = 1
        if ch == "&" and nxt == "&":
            connector, width = "&&", 2
        elif ch == "|" and nxt == "|":
            connector, width = "||", 2
        elif ch == "|":
            connector = "|"
        elif ch == ";":
            connector = ";"
        elif ch == "\n":
            connector = "\n"
        elif ch == "&":
            reasons.add("unsupported_background_operator")
        if connector is not None:
            finish(i, connector)
            start = i + width
            i += width
            continue
        i += 1
    finish(len(payload))
    if quote is not None:
        reasons.add("unbalanced_quote")
    if paren_depth:
        reasons.add("unbalanced_parentheses")
    if escaped:
        reasons.add("dangling_escape")
    if any(not atom for atom in atoms):
        reasons.add("empty_atom")
    return atoms, connectors, redirections, sorted(reasons)


def _atom_words(atom: str) -> tuple[list[str] | None, list[str]]:
    try:
        words = shlex.split(atom, posix=True)
    except ValueError:
        return None, ["invalid_atom_quoting"]
    while words and re.fullmatch(r"[A-Za-z_][A-Za-z_0-9]*=.*", words[0]):
        words.pop(0)
    if not words:
        return None, ["missing_executable"]
    # A quoted JSON value may be an argument; only argv[0] is executable.
    if words[0].startswith(("{", "[")):
        return None, ["non_executable_data"]
    return words, []


def _classify_atom(words: list[str], redirection: dict[str, bool]) -> tuple[set[str], list[str]]:
    executable = Path(words[0]).name.lower()
    argv = words[1:]
    subcommand = next((arg.lower() for arg in argv if not arg.startswith("-")), "")
    labels: set[str] = set()
    reasons: list[str] = []
    if executable == "dotnet":
        if subcommand in {"build", "msbuild", "compile"}:
            labels.add("build")
        elif subcommand in {"test", "run", "vstest"}:
            labels.add("test_or_run")
        elif subcommand in {"restore", "clean", "new", "sln", "add", "remove", "tool", "format"}:
            labels.add("project_configuration")
            if subcommand == "format":
                labels.add("edit")
        elif any(arg in {"--info", "--version", "--list-sdks", "--list-runtimes"} for arg in argv):
            labels.add("environment")
        else:
            reasons.append("unsupported_dotnet_subcommand")
    elif executable in {"msbuild", "csc", "fsc"}:
        labels.add("build")
    elif executable in {"pytest", "nunit3-console", "vstest.console"}:
        labels.add("test_or_run")
    elif executable in {"rg", "grep", "git-grep"}:
        labels.add("search")
    elif executable in {"cat", "head", "tail", "less", "more", "sed", "awk", "find", "ls", "tree", "wc"}:
        if not (executable == "cat" and redirection["has_output"]):
            labels.add("source_inspection")
        if (executable == "sed" and any(arg.startswith("-i") for arg in argv)) or redirection["has_output"]:
            labels.add("edit")
    elif executable == "git":
        if subcommand in {"status", "diff", "show", "log", "grep", "ls-files", "rev-parse"}:
            labels.add("search" if subcommand == "grep" else "source_inspection")
        elif subcommand in {"config", "init"}:
            labels.add("project_configuration")
        elif subcommand in {"apply", "mv", "rm"}:
            labels.add("edit")
        else:
            reasons.append("unsupported_git_subcommand")
    elif executable in {"apply_patch", "mkdir", "touch", "cp", "mv", "rm", "rmdir", "chmod", "tee"}:
        labels.add("edit")
    elif executable in {"printf", "echo"}:
        labels.add("edit" if redirection["has_output"] else "other")
    elif executable in {"env", "printenv", "uname", "which", "whereis", "pwd"}:
        labels.add("environment")
    elif executable == "command" and argv[:1] == ["-v"]:
        labels.add("environment")
    elif executable in {"true", "false", ":"}:
        labels.add("other")
    else:
        reasons.append("unsupported_executable")
    return labels, reasons

def classify_command(command: Any) -> dict[str, Any]:
    """Return bounded labels and an explicit ambiguity disposition."""
    payload, wrapper_reasons = _unwrap_bash(command)
    if payload is None:
        return {
            "classifier_version": CLASSIFIER_VERSION,
            "labels": [],
            "ambiguous_or_unparsed": True,
            "disposition": "unparsed",
            "ambiguity_reasons": wrapper_reasons,
            "connectors": [],
            "equivalence_classes": [],
            "operations": [],
        }
    atoms, connectors, redirections, scan_reasons = _scan_payload(payload)
    labels: set[str] = set()
    operations: list[dict[str, Any]] = []
    all_reasons = set(scan_reasons)
    dotnet_subcommands: set[str] = set()
    quoted_data_argument = False
    for index, (atom, redirection) in enumerate(zip(atoms, redirections), 1):
        words, parse_reasons = _atom_words(atom)
        atom_labels: set[str] = set()
        atom_reasons = list(parse_reasons)
        if words is not None:
            atom_labels, classify_reasons = _classify_atom(words, redirection)
            atom_reasons.extend(classify_reasons)
            if Path(words[0]).name.lower() == "dotnet":
                subcommand = next((arg.lower() for arg in words[1:] if not arg.startswith("-")), "")
                dotnet_subcommands.add(subcommand)
            for argument in words[1:]:
                if argument.startswith(("{", "[")):
                    try:
                        quoted_data_argument = isinstance(json.loads(argument), (dict, list))
                    except json.JSONDecodeError:
                        pass
        all_reasons.update(atom_reasons)
        labels.update(atom_labels)
        operations.append({
            "operation_ordinal": index,
            "connector_before": None if index == 1 else connectors[index - 2],
            "labels": sorted(atom_labels),
            "ambiguous_or_unparsed": bool(atom_reasons or scan_reasons),
            "ambiguity_reasons": sorted(set(atom_reasons) | set(scan_reasons)),
            "redirection": redirection,
        })
    ambiguous = bool(all_reasons)
    equivalence: set[str] = set()
    if not connectors:
        equivalence.add("atomic")
    connector_classes = {"and_if": "and-if", "pipeline": "pipeline", "or_if": "or-if",
                         "sequence": "sequence", "newline": "newline"}
    equivalence.update(connector_classes[connector] for connector in connectors)
    for redirection in redirections:
        if redirection["has_input"]:
            equivalence.add("input-redirection")
        if redirection["has_output"]:
            equivalence.add("output-redirection")
        if redirection["append_output"]:
            equivalence.add("append-redirection")
        if redirection["has_stderr"]:
            equivalence.add("stderr-redirection")
    if {"restore", "build", "run"}.issubset(dotnet_subcommands):
        equivalence.add("mixed-restore-build-run")
    if quoted_data_argument:
        equivalence.add("quoted-data-argument")
    if "heredoc" in all_reasons:
        equivalence.add("heredoc-ambiguous")
    if {"command_substitution", "backtick_substitution", "process_substitution"} & all_reasons:
        equivalence.add("substitution-ambiguous")
    if {"unsupported_parentheses", "unbalanced_parentheses"} & all_reasons:
        equivalence.add("parentheses-ambiguous")
    ordered_equivalence = [name for name in COVERED_COMMAND_EQUIVALENCE_CLASSES if name in equivalence]
    return {
        "classifier_version": CLASSIFIER_VERSION,
        "labels": sorted(labels),
        "ambiguous_or_unparsed": ambiguous,
        "disposition": "ambiguous" if ambiguous else "classified",
        "ambiguity_reasons": sorted(all_reasons),
        "connectors": connectors,
        "equivalence_classes": ordered_equivalence,
        "operations": operations,
    }


def _normalise_lf(text: Any) -> str:
    if not isinstance(text, str):
        text = "" if text is None else str(text)
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _volume(text: Any) -> dict[str, Any]:
    normalised = _normalise_lf(text)
    raw = normalised.encode("utf-8")
    if tiktoken is None or getattr(tiktoken, "__version__", None) != "0.14.0": raise ValueError("E1 requires tiktoken==0.14.0")
    tokens = len(tiktoken.get_encoding("o200k_base").encode(normalised))
    return {
        "serialization_version": SERIALIZATION_VERSION,
        "bytes": len(raw),
        "lines": len(normalised.splitlines()),
        "o200k_proxy_tokens": tokens,
        "sha256": _sha_bytes(raw),
    }


def _framed_output_volume(rows: list[tuple[int, str]]) -> dict[str, Any]:
    chunks = [f"{SERIALIZATION_VERSION}\n"]
    for ordinal, value in rows:
        normalised = _normalise_lf(value)
        chunks.append(f"{ordinal}:{len(normalised.encode('utf-8'))}\n{normalised}")
    return _volume("".join(chunks))


_DIAG = {
    "FS0058": "parse-indentation", "FS0597": "parse-indentation", "FS3100": "parse-indentation",
    "FS0001": "type-inference-record", "FS0764": "type-inference-record", "FS1129": "type-inference-record",
    "FS3133": "type-inference-record", "FS3566": "type-inference-record", "CS0029": "type-inference-record",
    "CS1503": "type-inference-record", "FS0039": "missing-symbol-api", "FS3261": "nullability",
    "NETSDK1064": "dependency-restore", "CS0105": "duplicate-import",
}
_DIAG_RE = re.compile(
    r"^\s*(?:(?P<file>.+?)(?:\((?P<span>[^)]*)\))?\s*:\s*)?"
    r"(?P<severity>error|warning)\s+(?P<code>(?:FS|CS|MSB|NETSDK)\d+)\s*:\s*(?P<message>.*)$",
    re.IGNORECASE,
)


def _diagnostic_file(value: str | None) -> str | None:
    if not value:
        return None
    value = value.replace("\\", "/").strip()
    if value.startswith("/workspace/"):
        return value[len("/workspace/"):]
    if value.startswith("/") or re.match(r"^[A-Za-z]:/", value) or ".." in value.split("/"):
        return value.rsplit("/", 1)[-1]
    return value

def diagnostics(text: Any) -> dict[str, Any]:
    instances: dict[tuple[Any, ...], dict[str, Any]] = {}
    by_code: dict[str, int] = {}
    by_category: dict[str, int] = {}
    by_severity: dict[str, int] = {}
    occurrence_count = 0
    for line in _normalise_lf(text).splitlines():
        m = _DIAG_RE.match(line)
        if m:
            occurrence_count += 1
            severity = m.group("severity").lower()
            code = m.group("code").upper()
            category = _DIAG.get(code, "unclassified")
            file_name = _diagnostic_file(m.group("file"))
            span = re.sub(r"\s+", "", m.group("span") or "") or None
            message_hash = _sha_bytes(re.sub(r"\s+", " ", m.group("message").strip()).encode("utf-8"))
            row = {"severity": severity, "code": code, "category": category,
                   "file": file_name, "span": span, "message_sha256": message_hash}
            instances[(severity, code, file_name, span, message_hash)] = row
            by_code[code] = by_code.get(code, 0) + 1
            by_category[category] = by_category.get(category, 0) + 1
            by_severity[severity] = by_severity.get(severity, 0) + 1
    return {
        "mapping_version": DIAGNOSTIC_VERSION,
        "occurrence_count": occurrence_count,
        "counts_by_code": dict(sorted(by_code.items())),
        "counts_by_category": dict(sorted(by_category.items())),
        "counts_by_severity": dict(sorted(by_severity.items())),
        "instances": sorted(instances.values(), key=lambda row: (
            row["severity"], row["code"], row["file"] or "", row["span"] or "", row["message_sha256"])),
    }


def _build_output_evidence(text: Any) -> tuple[str | None, str]:
    value = _normalise_lf(text)
    success = bool(re.search(r"(?im)^\s*Build succeeded\.\s*$", value))
    failure = bool(re.search(r"(?im)^\s*Build FAILED\.\s*$", value))
    for match in re.finditer(r"(?im)^\s*(\d+)\s+Error\(s\)\s*$", value):
        if int(match.group(1)) == 0:
            success = True
        else:
            failure = True
    if diagnostics(value)["counts_by_severity"].get("error", 0):
        failure = True
    if success and failure:
        return None, "conflicting_recorded_build_evidence"
    if failure:
        return "failure", "anchored_recorded_build_evidence"
    if success:
        return "success", "anchored_recorded_build_evidence"
    return None, "no_anchored_recorded_build_evidence"


def _operation_outcomes(
    classification: dict[str, Any], exit_code: Any, recorded: Any, status: Any = None,
) -> list[dict[str, Any]]:
    operations = classification["operations"]
    results = [_null("compound_outer_exit_not_attributable") for _ in operations]
    valid_exit = isinstance(exit_code, int) and not isinstance(exit_code, bool)
    if not valid_exit:
        results = [_null("outer_exit_unavailable") for _ in operations]
    elif status not in {"completed", "failed"}:
        results = [_null("outer_status_unavailable") for _ in operations]
    elif (exit_code == 0) != (status == "completed"):
        results = [_null("conflicting_outer_exit_status") for _ in operations]
    elif len(operations) == 1 and not operations[0]["ambiguous_or_unparsed"]:
        results[0] = {"value": "success" if exit_code == 0 else "failure", "reason": "atomic_outer_exit"}
    elif operations and all(connector == "and_if" for connector in classification["connectors"]) and exit_code == 0:
        for index, operation in enumerate(operations):
            if not operation["ambiguous_or_unparsed"]:
                results[index] = {"value": "success", "reason": "successful_and_chain"}
    elif operations and classification["connectors"] and all(
        connector in {"pipeline", "sequence", "newline"} for connector in classification["connectors"]
    ) and not operations[-1]["ambiguous_or_unparsed"]:
        results[-1] = {"value": "success" if exit_code == 0 else "failure", "reason": "terminal_outer_exit"}
    # Build success requires both an attributable zero exit and anchored zero-error
    # evidence.  Failure evidence can identify a sole build, but successful output
    # can never supply missing shell attribution for an inner compound operation.
    build_indexes = [i for i, operation in enumerate(operations) if "build" in operation["labels"]]
    evidence, reason = _build_output_evidence(recorded)
    for index in build_indexes:
        shell = results[index]
        if shell["value"] == "success":
            if len(build_indexes) == 1 and evidence == "success":
                results[index] = {"value": "success", "reason": "attributable_exit_and_zero_error_evidence"}
            elif evidence in {"failure"} or reason == "conflicting_recorded_build_evidence":
                results[index] = _null("conflicting_exit_and_build_evidence")
            else:
                results[index] = _null("zero_error_evidence_unavailable")
        elif shell["value"] == "failure":
            if evidence == "success" or reason == "conflicting_recorded_build_evidence":
                results[index] = _null("conflicting_exit_and_build_evidence")
        elif len(build_indexes) == 1 and evidence == "failure":
            results[index] = {"value": "failure", "reason": reason}
        elif len(build_indexes) == 1 and evidence == "success":
            results[index] = _null("shell_success_attribution_unavailable")
        elif reason == "conflicting_recorded_build_evidence":
            results[index] = _null(reason)
    return results

_ACTUAL_ITEM_TYPES = {"agent_message", "command_execution", "file_change", "todo_list"}


def _safe_change_path(value: Any) -> str | None:
    if not isinstance(value, str) or not value:
        return None
    value = value.replace("\\", "/")
    if value.startswith("/workspace/"):
        value = value[len("/workspace/"):]
    if value.startswith("/") or re.match(r"^[A-Za-z]:/", value):
        return None
    parts = [part for part in value.split("/") if part not in {"", "."}]
    if not parts or ".." in parts:
        return None
    return "/".join(parts)


def _point(event_ordinal: int, operation_ordinal: int = 0) -> tuple[int, int]:
    return event_ordinal, operation_ordinal


def _operation_ref(event_ordinal: int, operation: dict[str, Any]) -> dict[str, Any]:
    return {
        "event_ordinal": event_ordinal,
        "operation_ordinal": operation["operation_ordinal"],
        "outcome": operation["outcome"],
    }


def _repair_cycles(operations: list[dict[str, Any]], mutations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    points = sorted(mutation["point"] for mutation in mutations)
    attempts = sorted(
        (operation for operation in operations
         if {"build", "test_or_run"}.intersection(operation["labels"])),
        key=lambda operation: operation["point"],
    )
    cycles: list[dict[str, Any]] = []
    for failed in attempts:
        if failed["outcome"]["value"] != "failure":
            continue
        later_mutations = [point for point in points if failed["point"] < point]
        if not later_mutations:
            continue
        first_mutation = later_mutations[0]
        retry = next((attempt for attempt in attempts if first_mutation < attempt["point"]), None)
        if retry is None:
            continue
        between = [point for point in later_mutations if point < retry["point"]]
        failure_class = "build" if "build" in failed["labels"] else "test_or_run"
        retry_class = "build" if "build" in retry["labels"] else "test_or_run"
        cycles.append({
            "failure_operation_class": failure_class,
            "retry_operation_class": retry_class,
            "failure": _operation_ref(failed["event_ordinal"], failed),
            "mutation_count": len(between),
            "first_mutation_event_ordinal": first_mutation[0],
            "retry": _operation_ref(retry["event_ordinal"], retry),
            "reopened": retry["outcome"]["value"] == "failure",
        })
    return sorted(cycles, key=lambda row: (
        row["failure"]["event_ordinal"], row["failure"]["operation_ordinal"]))


def _build_state(commands: list[dict[str, Any]], mutations: list[dict[str, Any]]) -> dict[str, Any]:
    operations = [
        {**operation, "event_ordinal": command["event_ordinal"],
         "point": _point(command["event_ordinal"], operation["operation_ordinal"])}
        for command in commands for operation in command["operations"]
    ]
    builds = [operation for operation in operations if "build" in operation["labels"]]
    mutation_points = sorted(mutation["point"] for mutation in mutations)
    first_mutation = mutation_points[0] if mutation_points else None
    pre = list(builds) if first_mutation is None else [build for build in builds if build["point"] < first_mutation]
    post = [build for build in builds if first_mutation is not None and build["point"] > first_mutation]
    first_post = post[0] if post else None
    initial_batch = []
    if first_mutation is not None:
        boundary = first_post["point"] if first_post is not None else (10**12, 0)
        initial_batch = [point for point in mutation_points if first_mutation <= point < boundary]

    def build_ref(operation: dict[str, Any]) -> dict[str, Any]:
        return _operation_ref(operation["event_ordinal"], operation)

    command_ordinals = [command["event_ordinal"] for command in commands]
    return {
        "first_mutation_event_ordinal": first_mutation[0] if first_mutation else None,
        "initial_edit_batch": {
            "mutation_count": len(initial_batch),
            "first_event_ordinal": initial_batch[0][0] if initial_batch else None,
            "last_event_ordinal": initial_batch[-1][0] if initial_batch else None,
        },
        "pre_edit_builds": [build_ref(build) for build in pre],
        "first_post_edit_candidate_build": (
            build_ref(first_post) if first_post is not None
            else _null("no_completed_mutation" if first_mutation is None
                       else "no_recognized_candidate_build_after_first_mutation")
        ),
        "later_builds": [build_ref(build) for build in post[1:]],
        "command_counts": {
            "before_first_post_edit_build": (
                sum(ordinal < first_post["event_ordinal"] for ordinal in command_ordinals)
                if first_post is not None else None
            ),
            "after_first_post_edit_build": (
                sum(ordinal > first_post["event_ordinal"] for ordinal in command_ordinals)
                if first_post is not None else None
            ),
        },
        "repair_cycles": _repair_cycles(operations, mutations),
    }


def analyze_event_stream(events: list[dict[str, Any]], task: dict[str, Any] | None = None) -> dict[str, Any]:
    """Analyze already-decoded v3 events without retaining transcript text."""
    shape_counts: dict[str, int] = {}
    completed_ids: set[str] = set()
    commands: list[dict[str, Any]] = []
    mutations: list[dict[str, Any]] = []
    output_frames: list[tuple[int, str]] = []
    diagnostic_chunks: list[str] = []
    completed_item_counts = {name: 0 for name in sorted(_ACTUAL_ITEM_TYPES)}
    for event_ordinal, event in enumerate(events, 1):
        event_type = event.get("type") if isinstance(event, dict) else None
        item = event.get("item") if isinstance(event, dict) and isinstance(event.get("item"), dict) else None
        item_type = item.get("type") if item else None
        shape = str(event_type) + (f":{item_type}" if item_type is not None else "")
        _require(shape in COVERED_EVENT_SHAPES, "event_shape_uncovered")
        shape_counts[shape] = shape_counts.get(shape, 0) + 1
        if event_type != "item.completed" or item_type not in _ACTUAL_ITEM_TYPES:
            continue
        item_id = item.get("id")
        if isinstance(item_id, str):
            if item_id in completed_ids:
                continue
            completed_ids.add(item_id)
        completed_item_counts[item_type] += 1
        if item_type == "command_execution":
            classification = classify_command(item.get("command"))
            _require(bool(classification["equivalence_classes"])
                     and set(classification["equivalence_classes"]).issubset(COVERED_COMMAND_EQUIVALENCE_CLASSES),
                     "command_equivalence_class_uncovered")
            recorded = item.get("aggregated_output") if isinstance(item.get("aggregated_output"), str) else ""
            outcomes = _operation_outcomes(
                classification, item.get("exit_code"), recorded, item.get("status"),
            )
            operations = []
            for operation, outcome in zip(classification["operations"], outcomes):
                row = {**operation, "outcome": outcome}
                operations.append(row)
                if "edit" in row["labels"]:
                    mutations.append({
                        "event_ordinal": event_ordinal,
                        "operation_ordinal": row["operation_ordinal"],
                        "point": _point(event_ordinal, row["operation_ordinal"]),
                        "kind": "command_mutation",
                        "path": None,
                        "project_file": False,
                    })
            commands.append({
                "event_ordinal": event_ordinal,
                "classifier_version": CLASSIFIER_VERSION,
                "labels": classification["labels"],
                "ambiguous_or_unparsed": classification["ambiguous_or_unparsed"],
                "disposition": classification["disposition"],
                "ambiguity_reasons": classification["ambiguity_reasons"],
                "connectors": classification["connectors"],
                "equivalence_classes": classification["equivalence_classes"],
                "operations": operations,
                "outer_exit_observed": isinstance(item.get("exit_code"), int) and not isinstance(item.get("exit_code"), bool),
                "outer_exit_zero": item.get("exit_code") == 0 if isinstance(item.get("exit_code"), int) else None,
                "recorded_output_volume": _volume(recorded),
            })
            output_frames.append((event_ordinal, recorded))
            diagnostic_chunks.append(recorded)
        elif item_type == "file_change":
            changes = item.get("changes")
            if isinstance(changes, dict):
                changes = [changes]
            if not isinstance(changes, list):
                changes = []
            for change in changes:
                if not isinstance(change, dict):
                    continue
                path = _safe_change_path(change.get("path"))
                project_file = bool(path and Path(path).suffix.lower() in {".fsproj", ".csproj"})
                mutations.append({
                    "event_ordinal": event_ordinal,
                    "operation_ordinal": 0,
                    "point": _point(event_ordinal),
                    "kind": change.get("kind") if change.get("kind") in {"add", "update", "delete"} else "unclassified",
                    "path": path,
                    "project_file": project_file,
                    "labels": ["edit", "project_configuration"] if project_file else ["edit"],
                })
    state = _build_state(commands, mutations)
    label_counts = {label: sum(label in command["labels"] for command in commands) for label in LABELS}
    task = task if isinstance(task, dict) else {}
    evaluation = task.get("evaluation") if isinstance(task.get("evaluation"), dict) else {}
    agent = task.get("agent") if isinstance(task.get("agent"), dict) else {}
    return {
        "task_id": task.get("task_id"),
        "event_count": len(events),
        "event_shape_counts": dict(sorted(shape_counts.items())),
        "completed_item_counts": completed_item_counts,
        "commands": commands,
        "counts": label_counts,
        "mutations": [{key: value for key, value in mutation.items() if key != "point"} for mutation in mutations],
        "mutation_count": len(mutations),
        "project_file_mutation_count": sum(mutation["project_file"] for mutation in mutations),
        "recorded_output_volume": _framed_output_volume(output_frames),
        "diagnostics": diagnostics("\n".join(diagnostic_chunks)),
        "build_state": state,
        "pre_edit_build": state["pre_edit_builds"],
        "first_post_edit_candidate_build": state["first_post_edit_candidate_build"],
        "later_build_count": len(state["later_builds"]),
        "repair_cycle_count": len(state["repair_cycles"]),
        "candidate": {"outcome": agent.get("ok"), "event_count": len(events)},
        "evaluator": {
            "outcome": evaluation.get("ok"),
            "duration_seconds": evaluation.get("evaluator_wall_seconds"),
            "full_output_volume": _null(NULL_LEDGER["full_evaluator_output_volume"]),
        },
        "usage": agent.get("usage"),
        "timing": {
            "agent_process_wall_seconds": agent.get("agent_process_wall_seconds"),
            "task_total_wall_seconds": task.get("task_total_wall_seconds"),
            "event_duration_seconds": _null(NULL_LEDGER["candidate_event_duration_seconds"]),
        },
    }


class IntegrityError(ValueError):
    """Fail-closed E1 input error carrying only a stable derived code."""

    def __init__(self, code: str):
        self.code = code
        super().__init__(f"E1 integrity gate failed: {code}")


def _require(condition: bool, code: str) -> None:
    if not condition:
        raise IntegrityError(code)


def _canonical_raw_inventory(run: Path, config_root: Path) -> dict[str, Any]:
    _require(run.is_dir() and config_root.is_dir(), "raw_inventory_root_missing")
    rows: list[dict[str, Any]] = []
    total_bytes = 0
    # The preserved inventory was frozen from WindowsPath ordering.  Explicit
    # case-folding makes that identity reproducible on both CI platforms.
    for path in sorted((item for item in run.rglob("*") if item.is_file()),
                       key=lambda item: item.relative_to(config_root).as_posix().casefold()):
        _require(not path.is_symlink(), "raw_inventory_symlink")
        raw = path.read_bytes()
        relative = path.relative_to(config_root).as_posix()
        rows.append({"path": relative, "bytes": len(raw), "sha256": _sha_bytes(raw)})
        total_bytes += len(raw)
    return {"files": rows, "file_count": len(rows), "bytes": total_bytes, "tree_sha256": _hash(rows)}


def _git(workspace: Path, *args: str) -> bytes:
    _require(workspace.is_dir() and (workspace / ".git").exists(), "workspace_git_missing")
    _require(all(isinstance(arg, str) and "\x00" not in arg for arg in args), "git_argument_invalid")
    try:
        result = subprocess.run(
            ["git", *args], cwd=workspace, stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, timeout=30,
        )
    except (OSError, subprocess.SubprocessError):
        raise IntegrityError("git_command_failed") from None
    _require(result.returncode == 0, "git_command_failed")
    return result.stdout


def _commit_exists(workspace: Path, commit: Any) -> str:
    _require(isinstance(commit, str) and re.fullmatch(r"[0-9a-f]{40}", commit) is not None,
             "boundary_commit_invalid")
    _git(workspace, "cat-file", "-e", f"{commit}^{{commit}}")
    return commit


def _safe_repo_path(raw: bytes | str) -> str:
    try:
        value = raw.decode("utf-8") if isinstance(raw, bytes) else raw
    except UnicodeDecodeError:
        raise IntegrityError("repository_path_not_utf8") from None
    value = value.replace("\\", "/")
    _require(bool(value) and not value.startswith("/") and re.match(r"^[A-Za-z]:/", value) is None,
             "repository_path_not_relative")
    parts = value.split("/")
    _require(all(part not in {"", ".", ".."} for part in parts), "repository_path_not_relative")
    return "/".join(parts)


def _git_tree_blobs(workspace: Path, commit: str) -> list[tuple[str, bytes]]:
    output = _git(workspace, "ls-tree", "-r", "-z", "--long", commit)
    rows: list[tuple[str, str]] = []
    for record in output.split(b"\x00"):
        if not record:
            continue
        try:
            header, raw_path = record.split(b"\t", 1)
            mode, kind, object_id, _size = header.decode("ascii").split()
        except (ValueError, UnicodeDecodeError):
            raise IntegrityError("git_tree_record_invalid") from None
        _require(kind == "blob" and re.fullmatch(r"[0-9a-f]{40}", object_id) is not None,
                 "git_tree_record_invalid")
        rows.append((_safe_repo_path(raw_path), object_id))
    rows.sort(key=lambda row: row[0])
    return [(path, _git(workspace, "cat-file", "blob", object_id)) for path, object_id in rows]


def _included_source(path: str) -> bool:
    relative = Path(path)
    return relative.suffix.lower() in SOURCE_SUFFIXES and not any(part in EXCLUDED_PARTS for part in relative.parts)


def _source_serialization(files: list[tuple[str, bytes]]) -> bytes:
    chunks = [f"{SERIALIZATION_VERSION}\n".encode("utf-8")]
    for path, raw in sorted(files):
        try:
            normalised = raw.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")
        except UnicodeDecodeError:
            raise IntegrityError("source_not_utf8") from None
        path_bytes = path.encode("utf-8")
        chunks.extend((f"{len(path_bytes)}:{len(normalised)}\n".encode("ascii"), path_bytes, b"\n", normalised))
    return b"".join(chunks)


def _commit_source_metrics(workspace: Path, commit: str) -> dict[str, Any]:
    included = [(path, raw) for path, raw in _git_tree_blobs(workspace, commit) if _included_source(path)]
    repository = {"source_files": 0, "source_bytes": 0, "source_lines": 0, "approx_lexical_tokens": 0}
    project = {"file_count": 0, "bytes": 0, "lines": 0, "approx_lexical_tokens": 0}
    files: list[dict[str, Any]] = []
    for path, raw in included:
        text = raw.decode("utf-8", errors="replace")
        lexical = len(TOKEN_RE.findall(text))
        lines = len(text.splitlines())
        repository["source_files"] += 1
        repository["source_bytes"] += len(raw)
        repository["source_lines"] += lines
        repository["approx_lexical_tokens"] += lexical
        is_project = Path(path).suffix.lower() in {".fsproj", ".csproj"}
        if is_project:
            project["file_count"] += 1
            project["bytes"] += len(raw)
            project["lines"] += lines
            project["approx_lexical_tokens"] += lexical
        files.append({"path": path, "bytes": len(raw), "lines": lines,
                      "approx_lexical_tokens": lexical, "sha256": _sha_bytes(raw),
                      "project_file": is_project})
    serial = _source_serialization(included)
    try:
        serial_text = serial.decode("utf-8")
    except UnicodeDecodeError:  # guarded by _source_serialization
        raise IntegrityError("source_not_utf8") from None
    proxy = _volume(serial_text)
    proxy["sha256"] = _sha_bytes(serial)
    proxy["bytes"] = len(serial)
    return {"repository": repository, "source_proxy": proxy, "project_files": project, "files": files}


def _diff_metrics_for_paths(workspace: Path, before: str, after: str,
                            paths: list[str] | None = None) -> tuple[dict[str, int], str, list[str]]:
    if paths == []:
        return ({"changed_files": 0, "added_lines": 0, "deleted_lines": 0, "diff_bytes": 0},
                _sha_bytes(b""), [])
    suffix = ["--", *paths] if paths is not None else []
    raw_numstat = _git(workspace, "diff", "--numstat", "--no-renames", before, after, *suffix)
    try:
        numstat = raw_numstat.decode("utf-8")
    except UnicodeDecodeError:
        raise IntegrityError("boundary_numstat_invalid") from None
    changed = additions = deletions = 0
    numstat_paths: list[str] = []
    for line in numstat.splitlines():
        parts = line.split("\t")
        _require(len(parts) == 3, "boundary_numstat_invalid")
        _require(parts[0].isdigit() or parts[0] == "-", "boundary_numstat_invalid")
        _require(parts[1].isdigit() or parts[1] == "-", "boundary_numstat_invalid")
        changed += 1
        additions += int(parts[0]) if parts[0].isdigit() else 0
        deletions += int(parts[1]) if parts[1].isdigit() else 0
        numstat_paths.append(_safe_repo_path(parts[2]))
    patch = _git(workspace, "diff", "--binary", "--no-ext-diff", "--no-textconv", "--no-renames",
                 before, after, *suffix)
    return ({"changed_files": changed, "added_lines": additions,
             "deleted_lines": deletions, "diff_bytes": len(patch)}, _sha_bytes(patch), sorted(numstat_paths))


def _git_diff_boundary(workspace: Path, before: str, after: str) -> dict[str, Any]:
    name_status = _git(workspace, "diff", "--name-status", "-z", "--no-renames", before, after)
    fields = name_status.split(b"\x00")
    if fields and fields[-1] == b"":
        fields.pop()
    _require(len(fields) % 2 == 0, "boundary_name_status_invalid")
    paths: list[dict[str, str]] = []
    kind_map = {"A": "add", "M": "update", "D": "delete"}
    for index in range(0, len(fields), 2):
        try:
            status = fields[index].decode("ascii")
        except UnicodeDecodeError:
            raise IntegrityError("boundary_name_status_invalid") from None
        _require(status in kind_map, "boundary_change_kind_unsupported")
        paths.append({"path": _safe_repo_path(fields[index + 1]), "kind": kind_map[status]})
    paths.sort(key=lambda row: row["path"])
    metrics, diff_sha, numstat_paths = _diff_metrics_for_paths(workspace, before, after)
    _require(numstat_paths == [row["path"] for row in paths], "boundary_numstat_path_mismatch")
    tracked_paths = [row["path"] for row in paths if row["kind"] != "add"]
    recorded_metrics, recorded_sha, recorded_paths = _diff_metrics_for_paths(
        workspace, before, after, tracked_paths)
    _require(recorded_paths == sorted(tracked_paths), "boundary_numstat_path_mismatch")
    return {
        "changed_paths": paths,
        "metrics": metrics,
        "diff_sha256": diff_sha,
        "archived_runner_diff_metrics": recorded_metrics,
        "archived_runner_diff_sha256": recorded_sha,
    }


def _reconcile_file_changes(analysis: dict[str, Any],
                            changed_paths: list[dict[str, str]]) -> list[dict[str, str]]:
    observed: dict[str, set[str]] = {}
    for mutation in analysis["mutations"]:
        if mutation.get("path") is not None and mutation.get("kind") in {"add", "update", "delete"}:
            observed.setdefault(mutation["path"], set()).add(mutation["kind"])
    expected = {row["path"]: row["kind"] for row in changed_paths}
    _require(set(observed) == set(expected), "boundary_file_change_path_mismatch")
    dispositions: list[dict[str, str]] = []
    for path, kind in sorted(expected.items()):
        kinds = observed[path]
        if kind in kinds:
            disposition = "exact"
        elif kind == "update" and {"add", "delete"}.issubset(kinds):
            disposition = "delete-add-equivalent-update"
        else:
            raise IntegrityError("boundary_file_change_kind_mismatch")
        dispositions.append({"path": path, "boundary_kind": kind, "disposition": disposition})
    return dispositions


def _validate_events(events: list[dict[str, Any]]) -> None:
    top_shapes = {
        "thread.started": {"thread_id", "type"},
        "turn.started": {"type"},
        "turn.completed": {"type", "usage"},
        "item.started": {"item", "type"},
        "item.updated": {"item", "type"},
        "item.completed": {"item", "type"},
    }
    item_shapes = {
        "agent_message": {"id", "text", "type"},
        "command_execution": {"aggregated_output", "command", "exit_code", "id", "status", "type"},
        "file_change": {"changes", "id", "status", "type"},
        "todo_list": {"id", "items", "type"},
    }
    counts = {name: 0 for name in ("thread.started", "turn.started", "turn.completed")}
    for event in events:
        _require(isinstance(event, dict), "events_non_object")
        event_type = event.get("type")
        _require(event_type in top_shapes and set(event) == top_shapes[event_type], "event_shape_unsupported")
        if event_type in counts:
            counts[event_type] += 1
        if event_type == "thread.started":
            _require(isinstance(event.get("thread_id"), str) and bool(event["thread_id"]), "thread_event_invalid")
        elif event_type == "turn.completed":
            _require(isinstance(event.get("usage"), dict), "turn_usage_invalid")
        elif event_type.startswith("item."):
            item = event.get("item")
            _require(isinstance(item, dict) and item.get("type") in item_shapes, "item_shape_unsupported")
            item_type = item["type"]
            _require(set(item) == item_shapes[item_type], "item_shape_unsupported")
            _require(isinstance(item.get("id"), str) and bool(item["id"]), "item_id_invalid")
            allowed = {
                "item.started": {"command_execution", "file_change", "todo_list"},
                "item.updated": {"todo_list"},
                "item.completed": {"agent_message", "command_execution", "file_change", "todo_list"},
            }
            _require(item_type in allowed[event_type], "item_event_pair_unsupported")
            if item_type == "command_execution":
                _require(isinstance(item.get("command"), str) and isinstance(item.get("aggregated_output"), str),
                         "command_event_invalid")
                if event_type == "item.completed":
                    _require(item.get("status") in {"completed", "failed"} and isinstance(item.get("exit_code"), int)
                             and not isinstance(item.get("exit_code"), bool), "command_event_invalid")
            elif item_type == "file_change":
                _require(isinstance(item.get("changes"), (dict, list)), "file_change_event_invalid")
            elif item_type == "agent_message":
                _require(isinstance(item.get("text"), str), "agent_message_event_invalid")
            else:
                _require(isinstance(item.get("items"), list), "todo_event_invalid")
    _require(all(value == 1 for value in counts.values()), "event_boundary_count_invalid")


def _read_events(path: Path) -> tuple[list[dict[str, Any]], str]:
    _require(path.is_file(), "events_missing")
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8")
        events = [json.loads(line) for line in text.splitlines() if line.strip()]
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise IntegrityError("events_invalid_json") from None
    _validate_events(events)
    return events, _sha_bytes(raw)


def _read_object(path: Path, missing_code: str, invalid_code: str) -> tuple[dict[str, Any], str]:
    _require(path.is_file(), missing_code)
    raw = path.read_bytes()
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise IntegrityError(invalid_code) from None
    _require(isinstance(value, dict), invalid_code)
    return value, _sha_bytes(raw)


def _verify_task_envelopes(run: Path, result: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    tasks = result.get("tasks")
    _require(isinstance(tasks, list) and len(tasks) == 8 and all(isinstance(task, dict) for task in tasks),
             "task_roster_invalid")
    task_ids = [task.get("task_id") for task in tasks]
    _require(tuple(task_ids) == EXPECTED_TASK_IDS and len(set(task_ids)) == 8, "task_roster_invalid")
    tasks_root = run / "tasks"
    _require(tasks_root.is_dir(), "tasks_directory_missing")
    actual_dirs = {path.name for path in tasks_root.iterdir() if path.is_dir()}
    _require(actual_dirs == set(EXPECTED_TASK_IDS), "task_directory_roster_mismatch")
    _require(all(path.is_dir() for path in tasks_root.iterdir()), "task_directory_extra_file")
    analyses: list[dict[str, Any]] = []
    identities: list[dict[str, Any]] = []
    usage_total = {name: 0 for name in USAGE_FIELDS}
    for embedded in tasks:
        task_id = embedded["task_id"]
        task_dir = tasks_root / task_id
        copied, copied_sha = _read_object(task_dir / "task-result.json", "task_result_missing", "task_result_invalid")
        _require(copied == embedded, "task_envelope_mismatch")
        sidecar, usage_sha = _read_object(task_dir / "usage.json", "usage_sidecar_missing", "usage_sidecar_invalid")
        agent = embedded.get("agent")
        _require(isinstance(agent, dict) and isinstance(agent.get("usage"), dict), "task_usage_invalid")
        evaluation = embedded.get("evaluation")
        number = lambda value: isinstance(value, (int, float)) and not isinstance(value, bool) and value >= 0
        _require(isinstance(agent.get("ok"), bool) and number(agent.get("agent_process_wall_seconds"))
                 and isinstance(evaluation, dict) and isinstance(evaluation.get("ok"), bool)
                 and number(evaluation.get("evaluator_wall_seconds"))
                 and number(embedded.get("task_total_wall_seconds")), "task_timing_or_outcome_invalid")
        usage = agent["usage"]
        for name in USAGE_FIELDS:
            _require(isinstance(usage.get(name), int) and not isinstance(usage.get(name), bool)
                     and usage[name] >= 0, "task_usage_invalid")
            _require(sidecar.get(name) == usage[name], "usage_sidecar_mismatch")
            usage_total[name] += usage[name]
        events, events_sha = _read_events(task_dir / "events.jsonl")
        _require(agent.get("event_count") == len(events), "task_event_count_mismatch")
        analyses.append(analyze_event_stream(events, embedded))
        identities.append({"task_id": task_id, "events_sha256": events_sha,
                           "task_result_sha256": copied_sha, "usage_sha256": usage_sha})
    _require(result.get("aggregate_usage") == usage_total, "aggregate_usage_mismatch")
    _require(result.get("aggregate_usage_available") is True
             and result.get("aggregate_accounting_valid") is True, "aggregate_usage_invalid")
    return analyses, identities


def _verify_boundaries(run: Path, tasks: list[dict[str, Any]], analyses: list[dict[str, Any]],
                       source_cache: dict[str, dict[str, Any]] | None = None,
                       boundary_cache: dict[tuple[str, str], dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    workspace = run / "workspace"
    if source_cache is None:
        source_cache = {}
    if boundary_cache is None:
        boundary_cache = {}
    derived: list[dict[str, Any]] = []
    previous: str | None = None
    for task, analysis in zip(tasks, analyses):
        before = _commit_exists(workspace, task.get("pre_commit"))
        after = _commit_exists(workspace, task.get("post_commit"))
        if previous is not None:
            _require(before == previous, "boundary_chain_mismatch")
        previous = after
        if (before, after) not in boundary_cache:
            boundary_cache[(before, after)] = _git_diff_boundary(workspace, before, after)
        boundary = boundary_cache[(before, after)]
        _require(boundary["archived_runner_diff_metrics"] == task.get("diff"),
                 "boundary_diff_metrics_mismatch")
        reconciliation = _reconcile_file_changes(analysis, boundary["changed_paths"])
        if before not in source_cache:
            source_cache[before] = _commit_source_metrics(workspace, before)
        if after not in source_cache:
            source_cache[after] = _commit_source_metrics(workspace, after)
        source_before, source_after = source_cache[before], source_cache[after]
        _require(source_before["repository"] == task.get("repository_before"), "repository_before_mismatch")
        _require(source_after["repository"] == task.get("repository_after"), "repository_after_mismatch")
        changed_project_files = [row for row in boundary["changed_paths"]
                                 if Path(row["path"]).suffix.lower() in {".fsproj", ".csproj"}]
        derived.append({
            **analysis,
            "boundary": {
                "pre_commit": before,
                "post_commit": after,
                **boundary,
                "repository_before": source_before["repository"],
                "repository_after": source_after["repository"],
                "source_before": source_before["source_proxy"],
                "source_after": source_after["source_proxy"],
                "project_files_before": source_before["project_files"],
                "project_files_after": source_after["project_files"],
                "changed_project_files": changed_project_files,
                "file_change_reconciliation": reconciliation,
            },
        })
    head = _git(workspace, "rev-parse", "HEAD").decode("ascii").strip()
    _require(previous is not None and head == previous, "boundary_final_head_mismatch")
    return derived


def _sum_map(target: dict[str, int | float], source: dict[str, Any]) -> None:
    for key, value in source.items():
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            target[key] = target.get(key, 0) + value


def _aggregate_tasks(tasks: list[dict[str, Any]]) -> dict[str, Any]:
    labels = {label: 0 for label in LABELS}
    pre_edit = {"source_inspection": 0, "search": 0}
    first_post = {"success": 0, "failure": 0, "unavailable": 0}
    failed_operations = {"build": 0, "test_or_run": 0}
    diagnostic_codes: dict[str, int] = {}
    diagnostic_categories: dict[str, int] = {}
    diagnostic_severities: dict[str, int] = {}
    usage = {name: 0 for name in USAGE_FIELDS}
    timing = {"agent_process_wall_seconds": 0.0, "task_total_wall_seconds": 0.0,
              "evaluator_wall_seconds": 0.0}
    candidate_outcomes = {"success": 0, "failure": 0, "unavailable": 0}
    evaluator_outcomes = {"success": 0, "failure": 0, "unavailable": 0}
    output = {"bytes": 0, "lines": 0, "o200k_proxy_tokens": 0}
    source_after = {"bytes": 0, "lines": 0, "o200k_proxy_tokens": 0}
    ambiguous = later_builds = repairs = occurrences = instances = 0
    project_mutations = changed_project_files = 0
    output_hashes: list[str] = []
    event_shapes: dict[str, int] = {}
    equivalence_classes: dict[str, int] = {}
    for task in tasks:
        _sum_map(labels, task.get("counts", {}))
        _sum_map(event_shapes, task.get("event_shape_counts", {}))
        ambiguous += sum(bool(command.get("ambiguous_or_unparsed")) for command in task.get("commands", []))
        first_mutation = task.get("build_state", {}).get("first_mutation_event_ordinal")
        if isinstance(first_mutation, int):
            for command in task.get("commands", []):
                if command.get("event_ordinal", 10**12) < first_mutation:
                    for label in pre_edit:
                        pre_edit[label] += label in command.get("labels", [])
        first = task.get("build_state", {}).get("first_post_edit_candidate_build", {})
        value = first.get("outcome", {}).get("value") if isinstance(first.get("outcome"), dict) else first.get("value")
        first_post[value if value in {"success", "failure"} else "unavailable"] += 1
        later_builds += len(task.get("build_state", {}).get("later_builds", []))
        repairs += len(task.get("build_state", {}).get("repair_cycles", []))
        for command in task.get("commands", []):
            for equivalence_class in command.get("equivalence_classes", []):
                equivalence_classes[equivalence_class] = equivalence_classes.get(equivalence_class, 0) + 1
            for operation in command.get("operations", []):
                if operation.get("outcome", {}).get("value") == "failure":
                    for operation_class in failed_operations:
                        failed_operations[operation_class] += operation_class in operation.get("labels", [])
        diagnostic = task.get("diagnostics", {})
        occurrences += diagnostic.get("occurrence_count", 0)
        instances += len(diagnostic.get("instances", []))
        _sum_map(diagnostic_codes, diagnostic.get("counts_by_code", {}))
        _sum_map(diagnostic_categories, diagnostic.get("counts_by_category", {}))
        _sum_map(diagnostic_severities, diagnostic.get("counts_by_severity", {}))
        volume = task.get("recorded_output_volume", {})
        _sum_map(output, {key: volume.get(key) for key in output})
        if isinstance(volume.get("sha256"), str):
            output_hashes.append(volume["sha256"])
        _sum_map(usage, task.get("usage", {}))
        task_timing = task.get("timing", {})
        _sum_map(timing, {"agent_process_wall_seconds": task_timing.get("agent_process_wall_seconds"),
                          "task_total_wall_seconds": task_timing.get("task_total_wall_seconds"),
                          "evaluator_wall_seconds": task.get("evaluator", {}).get("duration_seconds")})
        for name, source in (("candidate", candidate_outcomes), ("evaluator", evaluator_outcomes)):
            outcome = task.get(name, {}).get("outcome")
            source["success" if outcome is True else "failure" if outcome is False else "unavailable"] += 1
        project_mutations += task.get("project_file_mutation_count", 0)
        changed_project_files += len(task.get("boundary", {}).get("changed_project_files", []))
        _sum_map(source_after, {key: task.get("boundary", {}).get("source_after", {}).get(key)
                                for key in source_after})
    return {
        "task_count": len(tasks),
        "command_count": sum(len(task.get("commands", [])) for task in tasks),
        "command_label_counts": labels,
        "ambiguous_command_count": ambiguous,
        "pre_edit_exploration": pre_edit,
        "first_post_edit_build_outcomes": first_post,
        "later_build_count": later_builds,
        "failed_candidate_operations": failed_operations,
        "repair_cycle_count": repairs,
        "candidate_diagnostics": {
            "occurrence_count": occurrences, "instance_count": instances,
            "counts_by_code": dict(sorted(diagnostic_codes.items())),
            "counts_by_category": dict(sorted(diagnostic_categories.items())),
            "counts_by_severity": dict(sorted(diagnostic_severities.items())),
        },
        "recorded_output_volume": {
            "serialization_version": SERIALIZATION_VERSION, **output,
            "task_volume_set_sha256": _hash(output_hashes),
            "disclaimer": "offline proxy over framed LF-normalized recorded candidate output; not provider billing or context",
        },
        "aggregate_usage": usage,
        "timing_totals_seconds": timing,
        "candidate_outcomes": candidate_outcomes,
        "evaluator": {"outcomes": evaluator_outcomes,
                      "duration_seconds": timing["evaluator_wall_seconds"]},
        "project_file_obligations": {"candidate_mutation_count": project_mutations,
                                     "committed_changed_file_count": changed_project_files},
        "source_proxy_after_totals": {
            **source_after,
            "disclaimer": "sum of task-boundary canonical source proxies; not unique model source exposure",
        },
        "coverage": {
            "event_shape_counts": dict(sorted(event_shapes.items())),
            "command_equivalence_class_counts": dict(sorted(equivalence_classes.items())),
        },
    }


def _group_aggregates(runs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for run in runs:
        groups.setdefault((run["configuration_id"], run["language"]), []).extend(run["tasks"])
    return [{"configuration_id": config, "language": language,
             **_aggregate_tasks(groups[(config, language)])}
            for config, language in sorted(groups)]


def _attribution_signatures() -> list[dict[str, Any]]:
    return [
        {"candidate": "static-context-size", "observable_measures": [
            "task boundary source proxies", "task aggregate input usage", "observable repair and exploration counts"],
         "limitation": "v3 identifies neither unique source exposure nor a context-scale relationship",
         "next_treatment": "model-free baselines and a preregistered multi-scale context study"},
        {"candidate": "first-pass-ability", "observable_measures": [
            "first post-edit build outcomes", "candidate diagnostic codes and categories"],
         "limitation": "first-patch tokens and phase reasoning are unavailable",
         "next_treatment": "matched gold-predecessor one-shot patch pilot"},
        {"candidate": "repair-amplification", "observable_measures": [
            "failed build and test operations", "repair cycles", "candidate diagnostic and command volumes"],
         "limitation": "per-cycle provider usage and replay tokens are unavailable",
         "next_treatment": "matched monolithic full-repair pilot"},
        {"candidate": "familiarity-comprehension", "observable_measures": [
            "source inspection and search commands before the first mutation"],
         "limitation": "observable navigation cannot establish training familiarity or hidden reasoning",
         "next_treatment": "matched comprehension and localization pilot"},
        {"candidate": "toolchain-project-obligations", "observable_measures": [
            "project-file mutations", "committed project-file changes", "evaluator duration"],
         "limitation": "candidate build duration is unavailable in v3",
         "next_treatment": "model-free language and toolchain baselines"},
        {"candidate": "context-pollution", "observable_measures": [],
         "limitation": "v3 starts a fresh process and conversation per task and cannot identify cross-task context pollution",
         "next_treatment": "separately reviewed persistent-context routing experiment"},
    ]


_FORBIDDEN_PUBLIC_KEYS = {
    "command", "aggregated_output", "agent_message", "message", "text", "thread_id", "thread_ids",
    "argv", "log", "logs", "process", "host_memory", "stdout", "stderr", "case_results",
    "input_payload", "test_input", "prompt", "excerpt", "excerpts",
}


def _looks_absolute_path(value: str) -> bool:
    return (bool(re.search(r"(?<![A-Za-z0-9])[A-Za-z]:[\\/]", value))
            or bool(re.search(r"(?<![A-Za-z0-9])(?:\\\\|//)[^\s]+", value))
            or bool(re.search(r"(?<![A-Za-z0-9_.-])/(?!/)[^\s]*", value)))


def validate_public_report(report: dict[str, Any], *, require_hash: bool = True) -> None:
    _require(isinstance(report, dict), "public_report_not_object")
    _require(report.get("report_type") == OUTPUT_REPORT_TYPE
             and report.get("family_id") == FAMILY_ID, "public_report_identity_invalid")
    _require("tasks" not in report and isinstance(report.get("runs"), list), "public_report_task_duplication")

    def visit(value: Any, parent_key: str | None = None) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                _require(isinstance(key, str), "public_report_key_invalid")
                normalized = key.lower().replace("-", "_")
                _require(normalized not in _FORBIDDEN_PUBLIC_KEYS, "public_report_forbidden_key")
                visit(child, normalized)
        elif isinstance(value, list):
            for child in value:
                visit(child, parent_key)
        elif isinstance(value, str):
            _require(not _looks_absolute_path(value), "public_report_absolute_path")
            if parent_key in {"path", "file"}:
                _require(_safe_change_path(value) == value, "public_report_path_not_relative")
    visit(report)
    if require_hash:
        declared = report.get("report_sha256")
        unsigned = dict(report)
        unsigned.pop("report_sha256", None)
        _require(isinstance(declared, str) and re.fullmatch(r"[0-9a-f]{64}", declared) is not None
                 and _hash(unsigned) == declared, "public_report_hash_invalid")

def analyze_archive(calibration_report: str | Path, archive_root: str | Path,
                    analyzer_git_sha: str) -> dict[str, Any]:
    """Verify all preserved evidence before returning any derived structure."""
    _require(isinstance(analyzer_git_sha, str)
             and re.fullmatch(r"[0-9a-fA-F]{40}", analyzer_git_sha) is not None,
             "analyzer_git_sha_invalid")
    analyzer_git_sha = analyzer_git_sha.lower()
    calibration_path = Path(calibration_report)
    calibration_raw = calibration_path.read_bytes()
    try:
        calibration = json.loads(calibration_raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise IntegrityError("calibration_report_invalid") from None
    _require(isinstance(calibration, dict), "calibration_report_invalid")
    declared_hash = calibration.get("report_sha256")
    hash_input = dict(calibration)
    hash_input.pop("report_sha256", None)
    _require(isinstance(declared_hash, str) and re.fullmatch(r"[0-9a-f]{64}", declared_hash) is not None
             and _hash(hash_input) == declared_hash, "calibration_self_hash_mismatch")
    _require(calibration.get("report_type") == REPORT_TYPE and calibration.get("family_id") == FAMILY_ID,
             "calibration_identity_mismatch")
    attempts = calibration.get("attempts")
    _require(isinstance(attempts, list) and len(attempts) == 10
             and all(isinstance(attempt, dict) for attempt in attempts), "attempt_roster_invalid")
    declared_ids = [attempt.get("attempt_id") for attempt in attempts]
    _require(all(isinstance(value, str) for value in declared_ids)
             and len(set(declared_ids)) == 10, "attempt_roster_invalid")
    declared_by_config: dict[str, set[str]] = {name: set() for name in EXPECTED_ATTEMPTS}
    for attempt in attempts:
        config = str(attempt.get("configuration_id", "")).lower()
        _require(config in EXPECTED_ATTEMPTS, "attempt_configuration_invalid")
        declared_by_config[config].add(attempt["attempt_id"])
    _require(declared_by_config == EXPECTED_ATTEMPTS, "attempt_roster_invalid")

    root = Path(archive_root)
    _require(root.is_dir(), "archive_root_missing")
    root_entries = list(root.iterdir())
    _require(all(path.is_dir() for path in root_entries)
             and {path.name for path in root_entries} == set(EXPECTED_ATTEMPTS), "archive_configuration_roster_mismatch")
    for config, expected in EXPECTED_ATTEMPTS.items():
        entries = list((root / config).iterdir())
        _require(all(path.is_dir() for path in entries) and {path.name for path in entries} == expected,
                 "archive_attempt_roster_mismatch")

    runs: list[dict[str, Any]] = []
    flat_tasks: list[dict[str, Any]] = []
    config_inventory_rows: dict[str, list[dict[str, Any]]] = {name: [] for name in EXPECTED_ATTEMPTS}
    source_metric_cache: dict[str, dict[str, Any]] = {}
    boundary_metric_cache: dict[tuple[str, str], dict[str, Any]] = {}
    for attempt in sorted(attempts, key=lambda row: row["attempt_id"]):
        attempt_id = attempt["attempt_id"]
        config = str(attempt["configuration_id"]).lower()
        run = root / config / attempt_id
        run_entries = list(run.iterdir())
        _require({path.name for path in run_entries if path.is_dir()} == {"tasks", "workspace"},
                 "attempt_directory_roster_mismatch")
        _require({path.name for path in run_entries if path.is_file()}
                 == {"attempt.json", "protocol-manifest.json", "result.json"},
                 "attempt_file_roster_mismatch")

        raw_inventory = _canonical_raw_inventory(run, run.parent)
        declared_inventory = attempt.get("raw_inventory")
        _require(isinstance(declared_inventory, dict)
                 and {key: raw_inventory[key] for key in ("file_count", "bytes", "tree_sha256")}
                 == declared_inventory, "raw_inventory_mismatch")
        config_inventory_rows[config].append({"attempt_id": attempt_id,
                                              "tree_sha256": raw_inventory["tree_sha256"]})

        result, result_file_sha = _read_object(run / "result.json", "result_missing", "result_invalid")
        _require(result_file_sha == attempt.get("result_sha256"), "result_sha256_mismatch")
        provenance = result.get("provenance")
        _require(isinstance(provenance, dict), "result_identity_mismatch")
        _require(result.get("run_id") == attempt_id and provenance.get("attempt_id") == attempt_id
                 and result.get("language") == attempt.get("language")
                 and result.get("requested_model") == attempt.get("model")
                 and str(provenance.get("configuration_id", "")).lower() == config
                 and provenance.get("reasoning_effort") == attempt.get("reasoning_effort")
                 and provenance.get("order") == attempt.get("order")
                 and provenance.get("position") == attempt.get("position"), "result_identity_mismatch")
        _require(attempt.get("task_count") == 8 and attempt.get("successful_tasks") == 8
                 and attempt.get("success") is True and result.get("success") is True,
                 "result_completion_mismatch")

        artifacts = _artifact_hashes(run, run.parent)
        declared_artifacts = attempt.get("artifact_hashes")
        _require(isinstance(declared_artifacts, dict)
                 and artifacts["set_sha256"] == declared_artifacts.get("set_sha256")
                 and len(artifacts["files"]) == declared_artifacts.get("file_count"),
                 "artifact_identity_mismatch")
        source_tree = _source_tree(run)
        declared_source = attempt.get("source_tree")
        _require(isinstance(declared_source, dict)
                 and source_tree["tree_sha256"] == declared_source.get("tree_sha256")
                 and source_tree["file_count"] == declared_source.get("file_count"),
                 "source_tree_identity_mismatch")

        analyses, task_identities = _verify_task_envelopes(run, result)
        verified_tasks = _verify_boundaries(run, result["tasks"], analyses,
                                            source_metric_cache, boundary_metric_cache)
        for task_row, identity in zip(verified_tasks, task_identities):
            task_row.pop("completed_item_counts", None)
            for legacy_alias in ("pre_edit_build", "first_post_edit_candidate_build",
                                 "later_build_count", "repair_cycle_count"):
                task_row.pop(legacy_alias, None)
            task_row["attempt_id"] = attempt_id
            task_row["configuration_id"] = config.upper()
            task_row["language"] = attempt["language"]
            task_row["input_identity"] = identity
            task_row["missingness"] = {key: _null(reason) for key, reason in NULL_LEDGER.items()}
        audit = audit_run(run)
        _require(isinstance(audit, dict) and audit.get("ok") is True, "audit_failed")
        declared_audit = attempt.get("audit")
        _require(isinstance(declared_audit, dict) and declared_audit.get("ok") is True
                 and declared_audit.get("errors") == audit.get("errors"), "audit_identity_mismatch")

        identity = {
            "result_sha256": result_file_sha,
            "raw_inventory": {key: raw_inventory[key] for key in ("file_count", "bytes", "tree_sha256")},
            "artifact_set_sha256": artifacts["set_sha256"],
            "source_tree_sha256": source_tree["tree_sha256"],
            "attempt_identity_sha256": _hash(attempt),
        }
        run_row = {
            "attempt_id": attempt_id,
            "configuration_id": config.upper(),
            "language": attempt["language"],
            "model": attempt["model"],
            "reasoning_effort": attempt["reasoning_effort"],
            "order": attempt["order"],
            "position": attempt["position"],
            "input_identity": identity,
            "aggregate_usage": result["aggregate_usage"],
            "timing": {name: result.get(name) for name in (
                "agent_process_wall_seconds", "evaluator_wall_seconds", "run_total_wall_seconds")},
            "tasks": verified_tasks,
            "aggregate": _aggregate_tasks(verified_tasks),
            "missingness": {key: _null(reason) for key, reason in NULL_LEDGER.items()},
        }
        runs.append(run_row)
        flat_tasks.extend(verified_tasks)
    _require(len(runs) == 10 and len(flat_tasks) == 80, "global_task_count_mismatch")
    config_inventories = [{"configuration_id": config.upper(),
                           "inventory_sha256": _hash(sorted(rows, key=lambda row: row["attempt_id"]))}
                          for config, rows in sorted(config_inventory_rows.items())]
    overall_aggregate = _aggregate_tasks(flat_tasks)
    observed_events = set(overall_aggregate["coverage"]["event_shape_counts"])
    observed_equivalence = set(overall_aggregate["coverage"]["command_equivalence_class_counts"])
    output: dict[str, Any] = {
        "report_type": OUTPUT_REPORT_TYPE,
        "family_id": FAMILY_ID,
        "schema_version": SCHEMA_VERSION,
        "versions": {
            "classifier": CLASSIFIER_VERSION,
            "diagnostic_mapping": DIAGNOSTIC_VERSION,
            "recorded_output_serialization": SERIALIZATION_VERSION,
            "source_serialization": SERIALIZATION_VERSION,
            "privacy_validation": "e1-public-privacy-v1",
        },
        "purpose": (
            "descriptive and hypothesis-routing only; excludes causal claims, post-hoc p-values, "
            "context-scale slopes, and mathematical intercept estimates"
        ),
        "inputs": {
            "calibration_report_sha256": declared_hash,
            "calibration_file_sha256": _sha_bytes(calibration_raw),
            "analyzer_git_sha": analyzer_git_sha,
            "configuration_inventories": config_inventories,
        },
        "totals": {"run_count": len(runs), "task_count": len(flat_tasks)},
        "runs": runs,
        "task_index": [{"attempt_id": task["attempt_id"], "task_id": task["task_id"]}
                       for task in flat_tasks],
        "aggregates": {
            "overall": overall_aggregate,
            "by_configuration_and_language": _group_aggregates(runs),
        },
        "coverage": {
            "event_shape_catalog": list(COVERED_EVENT_SHAPES),
            "command_equivalence_class_catalog": list(COVERED_COMMAND_EQUIVALENCE_CLASSES),
            "observed_event_shape_counts": overall_aggregate["coverage"]["event_shape_counts"],
            "observed_command_equivalence_class_counts": (
                overall_aggregate["coverage"]["command_equivalence_class_counts"]
            ),
            "unobserved_event_shapes": sorted(set(COVERED_EVENT_SHAPES) - observed_events),
            "unobserved_command_equivalence_classes": sorted(
                set(COVERED_COMMAND_EQUIVALENCE_CLASSES) - observed_equivalence
            ),
            "outside_catalog_event_shapes": sorted(observed_events - set(COVERED_EVENT_SHAPES)),
            "outside_catalog_command_equivalence_classes": sorted(
                observed_equivalence - set(COVERED_COMMAND_EQUIVALENCE_CLASSES)
            ),
        },
        "attribution_signatures": _attribution_signatures(),
        "proxy_contract": {
            "tokenizer": "tiktoken 0.14.0 o200k_base",
            "normalization": "LF-normalized UTF-8 with sorted repo-relative source paths",
            "recorded_output": "length-framed completed candidate command output only",
            "source": "length-framed committed source files using the frozen source-inclusion grammar",
            "disclaimer": "offline source and output proxies are neither provider billing nor unique model context",
        },
        "missingness": {key: _null(reason) for key, reason in NULL_LEDGER.items()},
    }
    validate_public_report(output, require_hash=False)
    output["report_sha256"] = _hash(output)
    validate_public_report(output)
    return output

def markdown_report(report: dict[str, Any]) -> str:
    validate_public_report(report)
    lines = [
        "# Workstream E1 archive-only forensic attribution",
        "",
        report["purpose"] + ".",
        "",
        "## Integrity and provenance",
        "",
        f"- Schema: `{report['schema_version']}`",
        f"- Report SHA-256: `{report['report_sha256']}`",
        f"- Calibration report SHA-256: `{report['inputs']['calibration_report_sha256']}`",
        f"- Analyzer Git SHA: `{report['inputs']['analyzer_git_sha']}`",
        f"- Verified runs/tasks: `{report['totals']['run_count']}` / `{report['totals']['task_count']}`",
        "- Every run passed result, raw-inventory, artifact, source-tree, task-envelope, usage, audit, and Git-boundary reconciliation.",
        "",
        "## Observability and missingness",
        "",
        "Task-level provider usage and agent/evaluator/task timing aggregates are retained. Candidate event and command timing, interaction-level usage, source exposure, replay, context, compaction, full evaluator volume, and intermediate patch content are unavailable.",
        "",
    ]
    for key in sorted(report["missingness"]):
        lines.append(f"- `{key}`: {report['missingness'][key]['reason']}")
    lines.extend([
        "",
        "## Descriptive measures by configuration and language",
        "",
        "| Config | Language | Tasks | Pre-edit inspect/search | First build S/F/U | Failed build/test | Repairs | Diagnostics (occ/inst) | Output proxy tokens | Project changes | Evaluator S/F/U; seconds |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ])
    for row in report["aggregates"]["by_configuration_and_language"]:
        pre = row["pre_edit_exploration"]
        first = row["first_post_edit_build_outcomes"]
        failed = row["failed_candidate_operations"]
        diagnostic = row["candidate_diagnostics"]
        project = row["project_file_obligations"]
        evaluator = row["evaluator"]
        outcomes = evaluator["outcomes"]
        lines.append(
            f"| {row['configuration_id']} | {row['language']} | {row['task_count']} | "
            f"{pre['source_inspection']}/{pre['search']} | "
            f"{first['success']}/{first['failure']}/{first['unavailable']} | "
            f"{failed['build']}/{failed['test_or_run']} | {row['repair_cycle_count']} | "
            f"{diagnostic['occurrence_count']}/{diagnostic['instance_count']} | "
            f"{row['recorded_output_volume']['o200k_proxy_tokens']} | "
            f"{project['candidate_mutation_count']}/{project['committed_changed_file_count']} | "
            f"{outcomes['success']}/{outcomes['failure']}/{outcomes['unavailable']}; "
            f"{evaluator['duration_seconds']:.3f} |"
        )
    lines.extend(["", "## Attribution-signature routing", ""])
    for signature in report["attribution_signatures"]:
        measures = ", ".join(signature["observable_measures"]) or "none in v3"
        lines.extend([
            f"### {signature['candidate']}", "",
            f"Observable measures: {measures}.", "",
            f"Limitation: {signature['limitation']}.", "",
            f"Required next treatment: {signature['next_treatment']}.", "",
        ])
    lines.extend([
        "## Evidence and claim limits", "",
        "The ten calibrations are non-counting and hypothesis-generating. Aggregate input is total provider input processed over a trajectory, not unique source tokens. Recorded-output and committed-source token counts are offline proxies, not provider billing or context. Fresh-per-task runs cannot establish cross-task context pollution. This report estimates no mechanism, post-hoc significance, mathematical intercept, context-scale slope, or crossover.",
        "",
    ])
    return "\n".join(lines)

def write_report(report: dict[str, Any], output_json: str | Path, output_markdown: str | Path) -> None:
    validate_public_report(report)
    json_bytes = (json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")
    markdown_bytes = markdown_report(report).encode("utf-8")
    json_path, markdown_path = Path(output_json), Path(output_markdown)
    _require(json_path.resolve() != markdown_path.resolve(), "output_paths_must_differ")
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    staged: list[Path] = []

    def stage(destination: Path, content: bytes) -> Path:
        descriptor, name = tempfile.mkstemp(prefix=f".{destination.name}.", suffix=".tmp",
                                            dir=destination.parent)
        temporary = Path(name)
        staged.append(temporary)
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        return temporary

    try:
        staged_json = stage(json_path, json_bytes)
        staged_markdown = stage(markdown_path, markdown_bytes)
        os.replace(staged_json, json_path)
        staged.remove(staged_json)
        os.replace(staged_markdown, markdown_path)
        staged.remove(staged_markdown)
    finally:
        for temporary in staged:
            try:
                temporary.unlink()
            except FileNotFoundError:
                pass
