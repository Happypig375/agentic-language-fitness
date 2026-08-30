"""Schema-v3 validation and deterministic gates for Workstream D."""

from __future__ import annotations

import hashlib
import itertools
from pathlib import Path
from typing import Any

from .protocol import (
    DIFFICULTY_C3_ARTIFACTS,
    DIFFICULTY_C3_SOURCE_COMMIT,
    DIFFICULTY_IMAGE_ARCHIVE,
    DIFFICULTY_TASK_HASHES,
    FAILURE_PRECEDENCE,
    REQUIRED_FAILURES,
    _load_json,
    _repo_path,
    tracked_text_sha256,
)

FAMILY_ID = "workstream-d-language-v1"
CONFIGURATIONS = ("H", "M", "L")
FAMILY_DEFINITION = "protocols/workstream-d-language-v1/definition.json"
SCHEDULE_FILE = "protocols/workstream-d-language-v1/schedule.json"
CATALOG_FILE = "protocols/workstream-d-language-v1/model-catalog-preflight.json"
BENCHMARK_MANIFEST = "benchmarks/successor/representation-v1/descriptive.manifest.json"
BENCHMARK_MANIFEST_SHA256 = (
    "5d174f5703184381984ae068c22571b280be9881d6d8ed9941be713b89925749"
)
ASSIGNMENT_SHA256 = "3bc3eaab8cc61097f59b098dc7753a9d452374d45438a31b8f465d85a56c1bd1"

PINS = {
    "H": {"requested_id": "gpt-5.4", "reasoning_effort": "medium"},
    "M": {"requested_id": "gpt-5.4", "reasoning_effort": "low"},
    "L": {"requested_id": "gpt-5.4-mini", "reasoning_effort": "medium"},
}

_DIRECTION_ORDER = {
    "F#>C#": ["fsharp", "csharp"],
    "C#>F#": ["csharp", "fsharp"],
}

_FORMAL_ASSIGNMENTS = [
    (1, 1, "H", "F#>C#"),
    (1, 2, "M", "C#>F#"),
    (1, 3, "L", "F#>C#"),
    (2, 1, "M", "F#>C#"),
    (2, 2, "L", "C#>F#"),
    (2, 3, "H", "C#>F#"),
    (3, 1, "L", "C#>F#"),
    (3, 2, "H", "F#>C#"),
    (3, 3, "M", "F#>C#"),
    (4, 1, "H", "C#>F#"),
    (4, 2, "L", "F#>C#"),
    (4, 3, "M", "C#>F#"),
    (5, 1, "L", "C#>F#"),
    (5, 2, "M", "C#>F#"),
    (5, 3, "H", "F#>C#"),
    (6, 1, "M", "F#>C#"),
    (6, 2, "H", "C#>F#"),
    (6, 3, "L", "F#>C#"),
]

# Kept as a small public representation for analysis/tests that predate the
# explicit within-macroblock placement field.
ROWS = [
    (macroblock, configuration, direction)
    for macroblock, _, configuration, direction in _FORMAL_ASSIGNMENTS
]

_CALIBRATION_ROWS = [
    {
        "block_id": "cal-h-primary",
        "calibration_id": "cal-h-primary",
        "configuration_id": "H",
        "order": ["fsharp", "csharp"],
        "direction": "F#>C#",
        "stage": 0,
        "counting": False,
        "role": "calibration-primary",
        "conditional": False,
    },
    {
        "block_id": "cal-m-primary",
        "calibration_id": "cal-m-primary",
        "configuration_id": "M",
        "order": ["csharp", "fsharp"],
        "direction": "C#>F#",
        "stage": 0,
        "counting": False,
        "role": "calibration-primary",
        "conditional": False,
    },
    {
        "block_id": "cal-l-primary",
        "calibration_id": "cal-l-primary",
        "configuration_id": "L",
        "order": ["fsharp", "csharp"],
        "direction": "F#>C#",
        "stage": 0,
        "counting": False,
        "role": "calibration-primary",
        "conditional": False,
    },
    {
        "block_id": "cal-m-reverse",
        "calibration_id": "cal-m-reverse",
        "configuration_id": "M",
        "order": ["fsharp", "csharp"],
        "direction": "F#>C#",
        "stage": 0,
        "counting": False,
        "role": "calibration-reverse-confirmation",
        "conditional": True,
        "condition": (
            "run only when the primary pair classifies M as provisionally "
            "too easy or too hard"
        ),
    },
    {
        "block_id": "cal-l-reverse",
        "calibration_id": "cal-l-reverse",
        "configuration_id": "L",
        "order": ["csharp", "fsharp"],
        "direction": "C#>F#",
        "stage": 0,
        "counting": False,
        "role": "calibration-reverse-confirmation",
        "conditional": True,
        "condition": (
            "run only when the primary pair classifies L as provisionally "
            "too easy or too hard"
        ),
    },
]

_COMMON_CHILD_PINS = {
    "benchmark_manifest": BENCHMARK_MANIFEST,
    "benchmark_manifest_sha256": BENCHMARK_MANIFEST_SHA256,
    "task_hashes": DIFFICULTY_TASK_HASHES,
    "codex": {
        "cli_version": "0.149.1",
        "image": "alf-codex:0.149.1",
        "dockerfile": "Dockerfile.codex-agent",
    },
    "image_archive": DIFFICULTY_IMAGE_ARCHIVE,
    "c3_source_commit": DIFFICULTY_C3_SOURCE_COMMIT,
    "c3_artifacts": DIFFICULTY_C3_ARTIFACTS,
    "toolchain": {"dotnet_sdk": "10.0.302", "target_framework": "net10.0"},
    "limits": {
        "task_timeout_seconds": 600,
        "evaluator_timeout_seconds": 300,
        "memory": "2g",
        "cpus": 2,
        "pids": 256,
    },
    "network_policy": (
        "bridge network; candidate egress and external documentation are allowed "
        "equally for both languages; mounts are limited to /workspace plus "
        "minimized authentication file"
    ),
    "documentation_policy": (
        "No benchmark/evaluator/gold files or parent repository are exposed to candidate"
    ),
    "artifact_policy": {
        "raw": "retain every attempt outside Git",
        "redaction": "remove credentials and prompt/transcript secrets",
        "retention": "retain raw and hashes for the study record",
    },
    "failure_taxonomy": [
        "agent",
        "provider",
        "auth",
        "host",
        "evaluator",
        "timeout",
        "protocol",
        "accounting",
    ],
    "failure_precedence": FAILURE_PRECEDENCE,
    "inclusion": {
        "formal_outcomes": (
            "Retain the first protocol-valid candidate outcome for every formal "
            "language slot"
        ),
        "metric_missingness": (
            "Use only valid available metrics and retain terminal-stop outcomes"
        ),
        "infrastructure_invalid": (
            "Retain and report pre-candidate infrastructure failures; retry only "
            "under the frozen sequential policy"
        ),
        "calibration": ("Non-counting and excluded from the assignment and 4+2 gate"),
        "sensitivity": ("Report all failures and common-exposure-prefix outcomes"),
    },
    "retry_policy": (
        "Retry only protocol/auth/provider/host/evaluator infrastructure-invalid "
        "attempts; retain every attempt and never replace a candidate outcome"
    ),
    "fresh_process": True,
    "accounting": (
        "require a fresh valid usage sidecar; fail closed for usage metrics while "
        "retaining candidate outcomes"
    ),
    "retention": {
        "location": "child raw_root plus read-only study archive",
        "period": "retain raw artifacts and hashes for at least five years",
        "redaction": "remove credentials and transcript secrets before curation",
    },
}

_CHILD_FIELDS = {
    "schema_version",
    "family_id",
    "cell_id",
    "configuration_id",
    "description",
    "representation",
    "model",
    "parent_definition",
    "schedule_file",
    "schedule_sha256",
    "catalog_file",
    "catalog_sha256",
    "assignment_sha256",
    "raw_root",
    *_COMMON_CHILD_PINS.keys(),
}


def canonical_assignment(rows: list[tuple[int, str, str]] | None = None) -> str:
    """Return the reviewed assignment's canonical newline-delimited encoding."""

    selected = ROWS if rows is None else rows
    return "".join(
        f"mb{macroblock}|{configuration}|{direction}\n"
        for macroblock, configuration, direction in selected
    )


def assignment_hash(rows: list[tuple[int, str, str]] | None = None) -> str:
    return hashlib.sha256(canonical_assignment(rows).encode("utf-8")).hexdigest()


def _expected_formal_row(
    macroblock: int,
    placement: int,
    configuration: str,
    direction: str,
) -> dict[str, Any]:
    return {
        "block_id": f"mb{macroblock:02d}-{configuration.lower()}",
        "macroblock": macroblock,
        "within_macroblock_position": placement,
        "configuration_id": configuration,
        "order": _DIRECTION_ORDER[direction],
        "direction": direction,
        "stage": 1 if macroblock <= 4 else 2,
        "counting": True,
        "role": "primary",
    }


def validate_schedule(schedule: dict[str, Any]) -> list[str]:
    """Validate the approved schedule, calibrations, and balance invariants."""

    errors: list[str] = []
    if not isinstance(schedule, dict):
        return ["schedule must be an object"]
    expected_top_level = {
        "schema_version",
        "family_id",
        "assignment_sha256",
        "calibration",
        "formal",
    }
    if set(schedule) != expected_top_level:
        errors.append("schedule fields are invalid")
    if schedule.get("schema_version") != 3:
        errors.append("schedule.schema_version must be 3")
    if schedule.get("family_id") != FAMILY_ID:
        errors.append("schedule family_id mismatch")
    if schedule.get("assignment_sha256") != ASSIGNMENT_SHA256:
        errors.append("schedule assignment_sha256 mismatch")

    formal = schedule.get("formal")
    if not isinstance(formal, list):
        formal = []
        errors.append("formal schedule must be a list")
    expected_formal = [_expected_formal_row(*row) for row in _FORMAL_ASSIGNMENTS]
    if formal != expected_formal:
        errors.append("formal schedule does not match the approved 18-row table")

    actual_assignments: list[tuple[int, str, str]] = []
    for row in formal:
        if not isinstance(row, dict):
            continue
        actual_assignments.append(
            (
                row.get("macroblock"),
                row.get("configuration_id"),
                row.get("direction"),
            )
        )
    if assignment_hash(actual_assignments) != ASSIGNMENT_SHA256:
        errors.append("canonical formal assignment hash mismatch")

    calibration = schedule.get("calibration")
    if calibration != _CALIBRATION_ROWS:
        errors.append("calibration rows or conditional rules are invalid")

    all_rows = [
        row
        for row in [*(calibration if isinstance(calibration, list) else []), *formal]
        if isinstance(row, dict)
    ]
    block_ids = [row.get("block_id") for row in all_rows]
    if any(
        not isinstance(block_id, str) or not block_id for block_id in block_ids
    ) or len(block_ids) != len(set(block_ids)):
        errors.append("schedule block_id values must be non-empty and unique")

    permutations: list[tuple[str, ...]] = []
    for macroblock in range(1, 7):
        rows = [row for row in formal if row.get("macroblock") == macroblock]
        rows.sort(key=lambda row: row.get("within_macroblock_position", 0))
        permutations.append(tuple(row.get("configuration_id") for row in rows))
        directions = [row.get("direction") for row in rows]
        if len(rows) != 3 or set(directions) != set(_DIRECTION_ORDER):
            errors.append(f"macroblock {macroblock} must mix both language directions")
    expected_permutations = set(itertools.permutations(CONFIGURATIONS))
    if len(permutations) != 6 or set(permutations) != expected_permutations:
        errors.append("macroblocks must contain each H/M/L permutation exactly once")

    for configuration in CONFIGURATIONS:
        rows = [row for row in formal if row.get("configuration_id") == configuration]
        placements = [row.get("within_macroblock_position") for row in rows]
        first_four = [row for row in rows if row.get("macroblock", 0) <= 4]
        if any(placements.count(placement) != 2 for placement in (1, 2, 3)):
            errors.append(
                f"configuration {configuration} must appear twice in each placement"
            )
        if sum(row.get("direction") == "F#>C#" for row in first_four) != 2:
            errors.append(
                f"configuration {configuration} stage-1 direction balance is invalid"
            )
        if sum(row.get("direction") == "F#>C#" for row in rows) != 3:
            errors.append(
                f"configuration {configuration} full direction balance is invalid"
            )
    if sum(row.get("direction") == "F#>C#" for row in formal) != 9:
        errors.append("overall formal language direction balance is invalid")

    adjacency_counts = {
        pair: sum(
            permutation[index : index + 2] == pair
            for permutation in permutations
            for index in (0, 1)
        )
        for pair in itertools.permutations(CONFIGURATIONS, 2)
    }
    if any(count != 2 for count in adjacency_counts.values()):
        errors.append("ordered configuration adjacency balance is invalid")
    return errors


def _load_contained_json(
    root: Path,
    value: Any,
    field: str,
    errors: list[str],
) -> tuple[Path | None, dict[str, Any]]:
    try:
        path = _repo_path(root, value, field)
        loaded = _load_json(path, field)
        if not isinstance(loaded, dict):
            errors.append(f"{field} must contain an object")
            return path, {}
        return path, loaded
    except ValueError as exc:
        errors.append(str(exc))
        return None, {}


def _validate_catalog(catalog: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    models = catalog.get("models")
    if not isinstance(models, dict):
        return ["model catalog models must be an object"]
    if catalog.get("supported_in_api") is not True:
        errors.append("model catalog API support evidence is missing")
    for configuration, pin in PINS.items():
        requested_id = pin["requested_id"]
        item = models.get(requested_id)
        if not isinstance(item, dict):
            errors.append(f"model catalog entry is missing for {configuration}")
            continue
        if (
            item.get("slug") != requested_id
            or item.get("visible") is not True
            or item.get("supported_in_api") is not True
            or pin["reasoning_effort"] not in item.get("supported_efforts", [])
        ):
            errors.append(f"model catalog entry is invalid for {configuration}")
    return errors


def _validate_repo_artifacts(
    root: Path,
    definition: dict[str, Any],
    errors: list[str],
) -> None:
    benchmark_path, benchmark = _load_contained_json(
        root,
        definition.get("benchmark_manifest"),
        "benchmark_manifest",
        errors,
    )
    if benchmark_path is not None:
        if tracked_text_sha256(benchmark_path) != definition.get(
            "benchmark_manifest_sha256"
        ):
            errors.append("benchmark manifest hash mismatch")
        provenance = benchmark.get("representation_provenance")
        if (
            not isinstance(provenance, dict)
            or provenance.get("treatment") != "descriptive"
        ):
            errors.append("benchmark manifest is not descriptive-only")
        if (
            not isinstance(provenance, dict)
            or provenance.get("source_commit") != DIFFICULTY_C3_SOURCE_COMMIT
        ):
            errors.append("benchmark representation source commit mismatch")
        tasks = benchmark.get("tasks")
        if not isinstance(tasks, list) or len(tasks) != 8:
            errors.append("benchmark manifest must contain the eight canonical tasks")
            tasks = []
        task_ids: list[str] = []
        for task in tasks:
            if not isinstance(task, dict):
                errors.append("benchmark contains a malformed task")
                continue
            task_id = task.get("id")
            if not isinstance(task_id, str):
                errors.append("benchmark task id is invalid")
                continue
            task_ids.append(task_id)
            try:
                prompt = _repo_path(root, task.get("prompt"), f"task {task_id} prompt")
                if not prompt.is_file() or tracked_text_sha256(
                    prompt
                ) != DIFFICULTY_TASK_HASHES.get(task_id):
                    errors.append(f"task hash mismatch: {task_id}")
            except (OSError, ValueError) as exc:
                errors.append(str(exc))
        if set(task_ids) != set(DIFFICULTY_TASK_HASHES) or len(task_ids) != len(
            set(task_ids)
        ):
            errors.append("benchmark task set does not match the canonical task pins")

    try:
        dockerfile = _repo_path(
            root,
            definition.get("codex", {}).get("dockerfile"),
            "codex.dockerfile",
        )
        if not dockerfile.is_file():
            errors.append("codex.dockerfile is unavailable")
    except ValueError as exc:
        errors.append(str(exc))

    artifacts = definition.get("c3_artifacts")
    if not isinstance(artifacts, dict):
        errors.append("c3_artifacts must be an object")
        return
    for name, expected in DIFFICULTY_C3_ARTIFACTS.items():
        pin = artifacts.get(name)
        if pin != expected:
            errors.append(f"c3 artifact pin mismatch: {name}")
            continue
        try:
            artifact = _repo_path(root, pin.get("path"), f"c3_artifacts.{name}")
            if not artifact.is_file() or tracked_text_sha256(artifact) != pin.get(
                "sha256"
            ):
                errors.append(f"c3 artifact hash mismatch: {name}")
        except (OSError, ValueError) as exc:
            errors.append(str(exc))


def _base_report(
    *,
    definition_file: Path,
    definition: dict[str, Any],
    schedule_file: Path | None,
    schedule: dict[str, Any],
    catalog_file: Path | None,
    catalog: dict[str, Any],
    errors: list[str],
) -> dict[str, Any]:
    return {
        "ok": not errors,
        "errors": errors,
        "definition": definition,
        "schedule": schedule,
        "catalog": catalog,
        "definition_file": str(definition_file),
        "definition_sha256": (
            tracked_text_sha256(definition_file) if definition_file.is_file() else None
        ),
        "schedule_file": str(schedule_file) if schedule_file else None,
        "schedule_sha256": (
            tracked_text_sha256(schedule_file)
            if schedule_file is not None and schedule_file.is_file()
            else None
        ),
        "catalog_file": str(catalog_file) if catalog_file else None,
        "catalog_sha256": (
            tracked_text_sha256(catalog_file)
            if catalog_file is not None and catalog_file.is_file()
            else None
        ),
        "assignment_sha256": ASSIGNMENT_SHA256,
    }


def _validate_child_definition(
    root: Path,
    definition_file: Path,
    definition: dict[str, Any],
    parent_file: Path,
    parent: dict[str, Any],
    schedule_file: Path | None,
    schedule: dict[str, Any],
    catalog_file: Path | None,
    catalog: dict[str, Any],
) -> dict[str, Any]:
    errors: list[str] = []
    configuration = definition.get("configuration_id")
    if set(definition) != _CHILD_FIELDS:
        errors.append("child definition fields are incomplete or contain extras")
    if definition.get("schema_version") != 3:
        errors.append("schema_version must be 3")
    if definition.get("family_id") != FAMILY_ID:
        errors.append("family_id mismatch")
    if configuration not in CONFIGURATIONS:
        errors.append("configuration_id must be H, M, or L")
    else:
        if definition.get("cell_id") != f"{FAMILY_ID}-{configuration.lower()}":
            errors.append("child cell_id mismatch")
        if definition.get("description") != (
            f"Workstream D descriptive-language feasibility child {configuration}."
        ):
            errors.append("child description mismatch")
        if definition.get("model") != PINS[configuration]:
            errors.append("child model pin mismatch")
        if definition.get("raw_root") != (
            f"results/workstream-d-language-v1/{configuration.lower()}"
        ):
            errors.append("child raw_root mismatch")
    if definition.get("representation") != "descriptive":
        errors.append("child must be descriptive-only")
    if definition.get("parent_definition") != FAMILY_DEFINITION:
        errors.append("child parent_definition mismatch")
    if definition.get("schedule_file") != SCHEDULE_FILE:
        errors.append("child schedule_file mismatch")
    if definition.get("catalog_file") != CATALOG_FILE:
        errors.append("child catalog_file mismatch")
    if definition.get("assignment_sha256") != ASSIGNMENT_SHA256:
        errors.append("child assignment_sha256 mismatch")
    actual_schedule_hash = (
        tracked_text_sha256(schedule_file)
        if schedule_file and schedule_file.is_file()
        else None
    )
    actual_catalog_hash = (
        tracked_text_sha256(catalog_file)
        if catalog_file and catalog_file.is_file()
        else None
    )
    if definition.get("schedule_sha256") != actual_schedule_hash:
        errors.append("child schedule hash mismatch")
    if definition.get("catalog_sha256") != actual_catalog_hash:
        errors.append("child catalog hash mismatch")
    for field, expected in _COMMON_CHILD_PINS.items():
        if definition.get(field) != expected:
            errors.append(f"child {field} pins are invalid")
    if set(definition.get("failure_taxonomy", [])) != REQUIRED_FAILURES:
        errors.append("child failure taxonomy is invalid")

    try:
        raw_root = _repo_path(root, definition.get("raw_root"), "raw_root")
    except ValueError as exc:
        raw_root = None
        errors.append(str(exc))
    try:
        contained_parent = _repo_path(
            root, definition.get("parent_definition"), "parent_definition"
        )
        if contained_parent != parent_file:
            errors.append("child parent path does not match the family definition")
    except ValueError as exc:
        errors.append(str(exc))

    if configuration in CONFIGURATIONS:
        entry = parent.get("children", {}).get(configuration)
        expected_entry = {
            "cell_id": definition.get("cell_id"),
            "configuration_id": configuration,
            "definition_file": definition_file.relative_to(root).as_posix(),
            "definition_sha256": tracked_text_sha256(definition_file),
            "model": PINS[configuration],
        }
        if entry != expected_entry:
            errors.append("parent child entry or definition hash mismatch")

    _validate_repo_artifacts(root, definition, errors)
    report = _base_report(
        definition_file=definition_file,
        definition=definition,
        schedule_file=schedule_file,
        schedule=schedule,
        catalog_file=catalog_file,
        catalog=catalog,
        errors=errors,
    )
    report.update(
        {
            "raw_root": str(raw_root) if raw_root else None,
            "family_definition_file": str(parent_file),
            "family_definition_sha256": tracked_text_sha256(parent_file),
            "family_definition": parent,
        }
    )
    return report


def _validate_parent(root: Path, definition_file: Path) -> dict[str, Any]:
    errors: list[str] = []
    try:
        definition = _load_json(definition_file, "family definition")
    except ValueError as exc:
        return {
            "ok": False,
            "errors": [str(exc)],
            "definition": {},
            "schedule": {},
            "catalog": {},
        }
    if not isinstance(definition, dict):
        return {
            "ok": False,
            "errors": ["family definition must contain an object"],
            "definition": {},
            "schedule": {},
            "catalog": {},
        }
    expected_fields = {
        "schema_version",
        "family_id",
        "cell_id",
        "description",
        "representation",
        "schedule_file",
        "schedule_sha256",
        "catalog_file",
        "catalog_sha256",
        "assignment_sha256",
        "children",
    }
    if set(definition) != expected_fields:
        errors.append("family definition fields are invalid")
    if definition.get("schema_version") != 3:
        errors.append("schema_version must be 3")
    if (
        definition.get("family_id") != FAMILY_ID
        or definition.get("cell_id") != FAMILY_ID
    ):
        errors.append("family identity mismatch")
    if definition.get("representation") != "descriptive":
        errors.append("family must be descriptive-only")
    if definition.get("schedule_file") != SCHEDULE_FILE:
        errors.append("family schedule_file mismatch")
    if definition.get("catalog_file") != CATALOG_FILE:
        errors.append("family catalog_file mismatch")
    if definition.get("assignment_sha256") != ASSIGNMENT_SHA256:
        errors.append("family assignment_sha256 mismatch")

    schedule_file, schedule = _load_contained_json(
        root, definition.get("schedule_file"), "schedule_file", errors
    )
    catalog_file, catalog = _load_contained_json(
        root, definition.get("catalog_file"), "catalog_file", errors
    )
    errors.extend(validate_schedule(schedule))
    errors.extend(_validate_catalog(catalog))
    actual_schedule_hash = (
        tracked_text_sha256(schedule_file)
        if schedule_file and schedule_file.is_file()
        else None
    )
    actual_catalog_hash = (
        tracked_text_sha256(catalog_file)
        if catalog_file and catalog_file.is_file()
        else None
    )
    if definition.get("schedule_sha256") != actual_schedule_hash:
        errors.append("family schedule hash mismatch")
    if definition.get("catalog_sha256") != actual_catalog_hash:
        errors.append("family catalog hash mismatch")

    children = definition.get("children")
    if not isinstance(children, dict) or set(children) != set(CONFIGURATIONS):
        errors.append("children must contain exactly H, M, and L")
        children = {}
    child_reports: dict[str, dict[str, Any]] = {}
    for configuration in CONFIGURATIONS:
        entry = children.get(configuration)
        if not isinstance(entry, dict):
            errors.append(f"child {configuration} entry is missing")
            continue
        try:
            child_file = _repo_path(
                root,
                entry.get("definition_file"),
                f"children.{configuration}.definition_file",
            )
            child = _load_json(child_file, f"child {configuration} definition")
            if not isinstance(child, dict):
                errors.append(
                    f"child {configuration} definition must contain an object"
                )
                continue
        except ValueError as exc:
            errors.append(str(exc))
            continue
        child_report = _validate_child_definition(
            root,
            child_file,
            child,
            definition_file,
            definition,
            schedule_file,
            schedule,
            catalog_file,
            catalog,
        )
        child_reports[configuration] = child_report
        errors.extend(
            f"child {configuration}: {error}" for error in child_report["errors"]
        )

    if len(child_reports) == 3:
        common_fields = set(_COMMON_CHILD_PINS) | {
            "schema_version",
            "family_id",
            "representation",
            "parent_definition",
            "schedule_file",
            "schedule_sha256",
            "catalog_file",
            "catalog_sha256",
            "assignment_sha256",
        }
        reference = child_reports["H"]["definition"]
        for configuration in ("M", "L"):
            child = child_reports[configuration]["definition"]
            for field in sorted(common_fields):
                if child.get(field) != reference.get(field):
                    errors.append(
                        f"child {configuration} common pin differs from child H: {field}"
                    )

    report = _base_report(
        definition_file=definition_file,
        definition=definition,
        schedule_file=schedule_file,
        schedule=schedule,
        catalog_file=catalog_file,
        catalog=catalog,
        errors=errors,
    )
    report["children"] = child_reports
    return report


def validate_family(root: Path, definition_path: str | Path) -> dict[str, Any]:
    """Validate a parent family definition and every referenced child."""

    root = Path(root).resolve()
    try:
        definition_file = _repo_path(root, definition_path, "definition_path")
    except ValueError as exc:
        return {"ok": False, "errors": [str(exc)], "definition": {}, "schedule": {}}
    try:
        candidate = _load_json(definition_file, "family definition")
    except ValueError as exc:
        return {"ok": False, "errors": [str(exc)], "definition": {}, "schedule": {}}
    if not isinstance(candidate, dict):
        return {
            "ok": False,
            "errors": ["family definition must contain an object"],
            "definition": {},
            "schedule": {},
        }
    if candidate.get("configuration_id") is not None:
        return {
            "ok": False,
            "errors": ["family-validate requires the parent definition"],
            "definition": candidate,
            "schedule": {},
        }
    return _validate_parent(root, definition_file)


def validate_child(root: Path, definition_path: str | Path) -> dict[str, Any]:
    """Validate a child cell through its complete parent family graph."""

    root = Path(root).resolve()
    try:
        child_file = _repo_path(root, definition_path, "definition_path")
        child = _load_json(child_file, "child definition")
    except ValueError as exc:
        return {"ok": False, "errors": [str(exc)], "definition": {}, "schedule": {}}
    if not isinstance(child, dict):
        return {
            "ok": False,
            "errors": ["child definition must contain an object"],
            "definition": {},
            "schedule": {},
        }
    if child.get("configuration_id") not in CONFIGURATIONS:
        return {
            "ok": False,
            "errors": ["protocol validate requires a Workstream D child definition"],
            "definition": child,
            "schedule": {},
        }
    try:
        parent_file = _repo_path(
            root, child.get("parent_definition"), "parent_definition"
        )
    except ValueError as exc:
        return {
            "ok": False,
            "errors": [str(exc)],
            "definition": child,
            "schedule": {},
        }
    parent_report = _validate_parent(root, parent_file)
    configuration = child["configuration_id"]
    report = parent_report.get("children", {}).get(configuration)
    if report is None:
        return {
            "ok": False,
            "errors": parent_report.get("errors", [])
            or ["child is not referenced by the parent family"],
            "definition": child,
            "schedule": parent_report.get("schedule", {}),
        }
    errors = list(parent_report.get("errors", []))
    if child_file != Path(report["definition_file"]):
        errors.append("requested child path does not match the parent entry")
    result = dict(report)
    result["errors"] = errors
    result["ok"] = not errors
    return result


def _stage1_values(slots: Any) -> tuple[list[dict[str, Any]], bool]:
    if isinstance(slots, dict):
        values = list(slots.values())
        mapping_matches = all(
            isinstance(value, dict) and value.get("slot_id") == slot_id
            for slot_id, value in slots.items()
        )
        return values, mapping_matches
    if isinstance(slots, list):
        return slots, True
    return [], False


def stage1_slot_ids(configuration_id: str) -> set[str]:
    """Return the eight canonical language-slot IDs for macroblocks 1--4."""

    if configuration_id not in CONFIGURATIONS:
        raise ValueError("configuration_id must be H, M, or L")
    block_ids = [
        f"mb{macroblock:02d}-{configuration.lower()}"
        for macroblock, _, configuration, _ in _FORMAL_ASSIGNMENTS
        if macroblock <= 4 and configuration == configuration_id
    ]
    return {f"{block_id}:{position}" for block_id in block_ids for position in (1, 2)}


def classify_stage1(
    slots: Any,
    *,
    apparatus_stop: bool = False,
    configuration_id: str | None = None,
) -> dict[str, Any]:
    """Apply the frozen 4+2 gate to one configuration's eight stage-1 slots."""

    values, mapping_valid = _stage1_values(slots)
    slot_ids = [
        value.get("slot_id") if isinstance(value, dict) else None for value in values
    ]
    valid = (
        mapping_valid
        and len(values) == 8
        and all(isinstance(slot_id, str) and slot_id for slot_id in slot_ids)
        and len(set(slot_ids)) == 8
    )
    if configuration_id is not None and set(slot_ids) != stage1_slot_ids(
        configuration_id
    ):
        valid = False
    for value in values:
        if not isinstance(value, dict):
            valid = False
            continue
        passed = value.get("passed_tasks")
        entered = value.get("entered_through")
        if (
            value.get("resolved") is not True
            or value.get("audited") is not True
            or not isinstance(passed, int)
            or isinstance(passed, bool)
            or not 0 <= passed <= 8
            or not isinstance(entered, int)
            or isinstance(entered, bool)
            or not 0 <= entered <= 8
            or passed > entered
            or (
                configuration_id is not None
                and value.get("configuration_id") != configuration_id
            )
        ):
            valid = False
    if apparatus_stop or not valid:
        return {
            "classification": "APPARATUS_STOP",
            "continue": False,
            "apparatus_stop": True,
            "possible_positions": 64,
        }

    passed_positions = sum(value["passed_tasks"] for value in values)
    entered_positions = sum(value["entered_through"] for value in values)
    if all(value["passed_tasks"] == 8 for value in values):
        classification = "SATURATED"
    elif (
        not any(value["entered_through"] >= 6 for value in values)
        or passed_positions < 32
    ):
        classification = "IMPOSSIBLE"
    elif any(value["entered_through"] >= 7 for value in values) and any(
        value["passed_tasks"] < 8 for value in values
    ):
        classification = "INFORMATIVE"
    else:
        classification = "INDETERMINATE"
    return {
        "classification": classification,
        "continue": classification == "INFORMATIVE",
        "apparatus_stop": False,
        "passed_positions": passed_positions,
        "entered_positions": entered_positions,
        "possible_positions": 64,
    }


def classify_stage1_family(
    outcomes: Any,
    *,
    apparatus_stop: bool = False,
) -> dict[str, Any]:
    """Apply the continuation decision without consulting contrast fields."""

    if not isinstance(outcomes, dict) or any(
        configuration not in outcomes for configuration in CONFIGURATIONS
    ):
        return {"classifications": {}, "continue": False, "apparatus_stop": True}
    reports = {
        configuration: classify_stage1(
            outcomes[configuration],
            configuration_id=configuration,
        )
        for configuration in CONFIGURATIONS
    }
    stop = apparatus_stop or any(
        report["apparatus_stop"] for report in reports.values()
    )
    return {
        "classifications": reports,
        "continue": (
            not stop
            and any(
                report["classification"] == "INFORMATIVE" for report in reports.values()
            )
        ),
        "apparatus_stop": stop,
    }
