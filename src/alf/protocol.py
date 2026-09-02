"""Validation and freezing for versioned, auditable experiment cells."""

from __future__ import annotations

import hashlib
import json
import os
import platform
import random
import re
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable


SCHEMA_VERSION = 1
SCHEMA_V2 = 2
SCHEMA_V3 = 3
SUPPORTED_REASONING_EFFORTS = {"low", "medium", "high"}
CODEX_CLI_VERSION = "0.149.1"
DOTNET_SDK_VERSION = "10.0.302"
TARGET_FRAMEWORK = "net10.0"
EXPECTED_IMAGE = "alf-codex:0.149.1"
EXPECTED_IMAGE_ID = (
    "sha256:0320a60c5b2628cebeb2c897bbf80da949f3b9bb99fa61f5a3475c7276328756"
)
# Schema-v3 Workstream D records the image Config digest reported by Docker;
# the retained OCI archive itself remains identified by its index digest.
WORKSTREAM_D_V3_IMAGE_ID = (
    "sha256:5d3e97d195dbbe7e47e47055e46f8c6f15fb9553be0c7ef19ed0060756fc7116"
)
SCHEDULE_SEED = 20260829
SCHEDULE_GENERATOR = (
    "Python 3.12: r=random.Random(20260829); "
    "first=['fsharp']*5+['csharp']*5; r.shuffle(first); r.shuffle(first); "
    "explicit sequence is authoritative"
)

DIFFICULTY_C3_SOURCE_COMMIT = "4e58677e0bfff18c2104298ad35fc4e801bbd052"
DIFFICULTY_IMAGE_ARCHIVE = {
    "path": (
        r"X:\backup20260827\Archives\SourceRepos\agentic-language-fitness-images"
        r"\alf-codex-0.149.1-sha256-0320a60c5b2628ce.tar"
    ),
    "bytes": 630053888,
    "sha256": "55ee85f0656cef429d1cd40edced79782d54abb7b2180c9770c14bea06828ddf",
    "local_image_id": EXPECTED_IMAGE_ID,
}
DIFFICULTY_C3_ARTIFACTS = {
    "definition": {
        "path": "benchmarks/successor/representation-v1/definition.json",
        "sha256": "e2c21b484da5cfd2e20b59548360b3102acbe0492925e1198c3f18eb4e95ef00",
    },
    "mapping": {
        "path": "benchmarks/successor/representation-v1/mapping.json",
        "sha256": "7a1b36918a83b6cbad5093c797cc3e79503d97f1c245cfc6e781eb0c28e72546",
    },
    "role_inventory": {
        "path": "benchmarks/successor/representation-v1/role-inventory.json",
        "sha256": "2a30fbe1474c8207da3ee315e45b6628f438fab2142a0b25a32eda795427dc41",
    },
    "exclusions": {
        "path": "benchmarks/successor/representation-v1/exclusions.json",
        "sha256": "b742b889c367a967a00a755ccaae5eb970e423cd2c11b329e15978d559240079",
    },
    "source_manifest": {
        "path": "benchmarks/successor/representation-v1/source-manifest.json",
        "sha256": "65339303386e2aa6c55ae4a6ede2843c99ec61eeb25b009bdd08d49ced4ec19d",
    },
    "reports": {
        "path": "benchmarks/successor/representation-v1/reports.json",
        "sha256": "6f4f662f85eb9c3c0ab55cfbead40e741d8e16bf5edf6950cd542a0ce6008f14",
    },
}
DIFFICULTY_CONDITIONS = {
    "fsharp-descriptive": {
        "language": "fsharp",
        "representation": "descriptive",
        "manifest": "benchmarks/successor/representation-v1/descriptive.manifest.json",
        "manifest_sha256": "5d174f5703184381984ae068c22571b280be9881d6d8ed9941be713b89925749",
    },
    "csharp-descriptive": {
        "language": "csharp",
        "representation": "descriptive",
        "manifest": "benchmarks/successor/representation-v1/descriptive.manifest.json",
        "manifest_sha256": "5d174f5703184381984ae068c22571b280be9881d6d8ed9941be713b89925749",
    },
    "fsharp-deterministic": {
        "language": "fsharp",
        "representation": "deterministic",
        "manifest": "benchmarks/successor/representation-v1/deterministic.manifest.json",
        "manifest_sha256": "7de96dbd84daab058eed9476a91ad052a78bb6c1aa4eacdff9aa6cdb848f6ac5",
    },
    "csharp-deterministic": {
        "language": "csharp",
        "representation": "deterministic",
        "manifest": "benchmarks/successor/representation-v1/deterministic.manifest.json",
        "manifest_sha256": "7de96dbd84daab058eed9476a91ad052a78bb6c1aa4eacdff9aa6cdb848f6ac5",
    },
}
DIFFICULTY_TASK_HASHES = {
    "001-priority": "4b003212969d3c3537f65d82320ba88ee42bb5a20a13e3ce6951f16dcfb1f1c0",
    "002-overdue": "c166e62c2ed2f915a2865555ad824a8cc63b74ef1980b43f0a6b5ce62a94545c",
    "003-at-risk-window": "b37955c3b54b1a04a5359715969d7e97692cfe013fa22e6c4fd85a965a429199",
    "004-vip-ready": "90d06aa42a610bc8e55d5e8f03cb6d47e305ca3f044baf7cc4a4032a1151556e",
    "005-null-order-robustness": "4ce101299b1d61acf53d1e61344fbcee7f40a9ae7c88e1283b9e8ff5834c9c50",
    "006-transition-validation": "0ac889d9ea84732feffee90400461f985676cc1800dfb680d5542100db054a01",
    "007-query-engine-refactor": "26ce7bb89282d4ba89e966e1abb2e15873314449ab19a4711809d0b7c303cbc5",
    "008-summary-api": "4db339c6e5e95535ca8f4cfe3235b864372179cb15cc138b3592686fc5de1139",
}
DIFFICULTY_WILLIAMS_ROWS = [
    ["fsharp-descriptive", "csharp-descriptive", "csharp-deterministic", "fsharp-deterministic"],
    ["csharp-descriptive", "fsharp-deterministic", "fsharp-descriptive", "csharp-deterministic"],
    ["fsharp-deterministic", "csharp-deterministic", "csharp-descriptive", "fsharp-descriptive"],
    ["csharp-deterministic", "fsharp-descriptive", "fsharp-deterministic", "csharp-descriptive"],
]

REQUIRED_FAILURES = {
    "agent",
    "provider",
    "auth",
    "host",
    "evaluator",
    "timeout",
    "protocol",
    "accounting",
}
FAILURE_PRECEDENCE = [
    "protocol",
    "auth",
    "provider",
    "host",
    "timeout",
    "accounting",
    "agent",
    "evaluator",
]
REQUIRED_DEFINITION_FIELDS = {
    "schema_version",
    "cell_id",
    "description",
    "benchmark_manifest",
    "benchmark_manifest_sha256",
    "task_hashes",
    "model",
    "codex",
    "image_archive",
    "toolchain",
    "limits",
    "network_policy",
    "documentation_policy",
    "artifact_policy",
    "failure_taxonomy",
    "failure_precedence",
    "inclusion",
    "retry_policy",
    "fresh_process",
    "schedule_file",
    "raw_root",
    "retention",
}
REQUIRED_PROBE_FIELDS = {
    "os",
    "platform",
    "architecture",
    "cpu",
    "physical_memory_bytes",
    "python",
    "git",
    "dotnet",
    "docker_client",
    "docker_server",
    "image_id",
    "image_platform",
    "image_size_bytes",
    "container_codex",
    "container_dotnet",
}

_CELL_ID = re.compile(r"^[a-z0-9][a-z0-9-]*$")
_HEX_64 = re.compile(r"^[0-9a-f]{64}$")
_IMAGE_ID = re.compile(r"^sha256:[0-9a-f]{64}$")


def sha256(path: Path) -> str:
    """Return raw-byte SHA-256 (used for binary archives)."""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tracked_text_sha256(path: Path) -> str:
    """Hash UTF-8 tracked text after normalizing CRLF and lone CR to LF."""

    try:
        text = path.read_bytes().decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"invalid UTF-8 tracked text at {path}: {exc}") from exc
    data = text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def _safe_tracked_hash(path: Path) -> str | None:
    try:
        return tracked_text_sha256(path)
    except (OSError, ValueError):
        return None


def canonical_json_hash(value: dict[str, Any]) -> str:
    """Hash a JSON object using the manifest's canonical serialization."""

    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _load_json(path: Path, label: str) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid {label} JSON at {path}: {exc}") from exc


def _repo_path(
    root: Path,
    value: str | Path,
    field: str,
    *,
    allow_root: bool = False,
) -> Path:
    if not isinstance(value, (str, Path)) or not str(value):
        raise ValueError(f"{field} must be a non-empty path")
    path = Path(value)
    candidate = path.resolve() if path.is_absolute() else (root / path).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"{field} escapes repository: {value}") from exc
    if candidate == root and not allow_root:
        raise ValueError(f"{field} must not be the repository root")
    return candidate


def _require_nonempty_string(value: Any, field: str, errors: list[str]) -> bool:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{field} must be a non-empty string")
        return False
    return True


def _require_hash(value: Any, field: str, errors: list[str]) -> bool:
    if not isinstance(value, str) or _HEX_64.fullmatch(value) is None:
        errors.append(f"{field} must be lowercase SHA-256 hex")
        return False
    return True


def _require_string_fields(
    value: Any,
    field: str,
    required: set[str],
    errors: list[str],
) -> bool:
    if not isinstance(value, dict):
        errors.append(f"{field} must be an object")
        return False
    ok = True
    for name in sorted(required):
        ok = _require_nonempty_string(value.get(name), f"{field}.{name}", errors) and ok
    return ok


def _empty_report(errors: list[str]) -> dict[str, Any]:
    return {
        "ok": False,
        "errors": errors,
        "definition": {},
        "schedule": {},
        "definition_sha256": None,
        "schedule_sha256": None,
        "definition_file": None,
        "schedule_file": None,
        "raw_root": None,
    }


def _generated_first_languages(seed: int) -> list[str]:
    generator = random.Random(seed)
    first = ["fsharp"] * 5 + ["csharp"] * 5
    generator.shuffle(first)
    generator.shuffle(first)
    return first


def _validate_cell_v1(root: Path, definition_path: str | Path) -> dict[str, Any]:
    """Validate a tracked protocol definition and all referenced inputs."""

    root = root.resolve()
    try:
        definition_file = _repo_path(root, definition_path, "definition_path")
    except ValueError as exc:
        return _empty_report([str(exc)])

    try:
        definition = _load_json(definition_file, "definition")
    except ValueError as exc:
        return _empty_report([str(exc)])
    if not isinstance(definition, dict):
        return _empty_report(["definition must contain an object"])

    errors: list[str] = []
    missing = sorted(REQUIRED_DEFINITION_FIELDS - definition.keys())
    errors.extend(f"missing definition field: {field}" for field in missing)

    if definition.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION}")
    cell_id = definition.get("cell_id")
    if not isinstance(cell_id, str) or _CELL_ID.fullmatch(cell_id) is None:
        errors.append("cell_id must contain only lowercase letters, digits, and hyphens")
    _require_nonempty_string(definition.get("description"), "description", errors)

    model = definition.get("model")
    if not isinstance(model, dict):
        errors.append("model must be an object")
    else:
        if set(model) != {"snapshot", "reasoning_effort"}:
            errors.append("model must contain exactly snapshot and reasoning_effort")
        if not isinstance(model.get("snapshot"), str) or not model["snapshot"].strip():
            errors.append("model.snapshot must be a non-empty string")
        if model.get("reasoning_effort") not in SUPPORTED_REASONING_EFFORTS:
            errors.append("model.reasoning_effort must be low, medium, or high")

    codex = definition.get("codex")
    if not isinstance(codex, dict):
        errors.append("codex must be an object")
    else:
        if codex.get("cli_version") != CODEX_CLI_VERSION:
            errors.append(f"codex.cli_version must be {CODEX_CLI_VERSION}")
        if codex.get("image") != EXPECTED_IMAGE:
            errors.append(f"codex.image must be {EXPECTED_IMAGE}")
        try:
            dockerfile = _repo_path(root, codex.get("dockerfile", ""), "codex.dockerfile")
            if not dockerfile.is_file():
                errors.append("codex.dockerfile is unavailable")
        except ValueError as exc:
            errors.append(str(exc))

    archive = definition.get("image_archive")
    if not isinstance(archive, dict):
        errors.append("image_archive must be an object")
    else:
        _require_nonempty_string(archive.get("path"), "image_archive.path", errors)
        archive_bytes = archive.get("bytes")
        if (
            not isinstance(archive_bytes, int)
            or isinstance(archive_bytes, bool)
            or archive_bytes <= 0
        ):
            errors.append("image_archive.bytes must be a positive integer")
        _require_hash(archive.get("sha256"), "image_archive.sha256", errors)
        image_id = archive.get("local_image_id")
        if not isinstance(image_id, str) or _IMAGE_ID.fullmatch(image_id) is None:
            errors.append("image_archive.local_image_id must be a SHA-256 image ID")
        elif image_id != EXPECTED_IMAGE_ID:
            errors.append("image_archive.local_image_id does not match the retained image")

    if definition.get("toolchain") != {
        "dotnet_sdk": DOTNET_SDK_VERSION,
        "target_framework": TARGET_FRAMEWORK,
    }:
        errors.append("toolchain pins are invalid")
    if definition.get("limits") != {
        "task_timeout_seconds": 600,
        "evaluator_timeout_seconds": 300,
        "memory": "2g",
        "cpus": 2,
        "pids": 256,
    }:
        errors.append("resource limits are invalid")

    for field in ("network_policy", "documentation_policy", "retry_policy"):
        _require_nonempty_string(definition.get(field), field, errors)
    _require_string_fields(
        definition.get("artifact_policy"),
        "artifact_policy",
        {"raw", "redaction", "retention"},
        errors,
    )
    _require_string_fields(
        definition.get("inclusion"),
        "inclusion",
        {
            "formal_outcomes",
            "metric_missingness",
            "infrastructure_invalid",
            "calibration",
            "sensitivity",
        },
        errors,
    )
    _require_string_fields(
        definition.get("retention"),
        "retention",
        {"location", "period", "redaction"},
        errors,
    )
    if definition.get("fresh_process") is not True:
        errors.append("fresh_process must be true")

    taxonomy = definition.get("failure_taxonomy")
    if (
        not isinstance(taxonomy, list)
        or len(taxonomy) != len(REQUIRED_FAILURES)
        or set(taxonomy) != REQUIRED_FAILURES
    ):
        errors.append("failure taxonomy is incomplete or duplicated")
    if definition.get("failure_precedence") != FAILURE_PRECEDENCE:
        errors.append("failure precedence is invalid")

    _require_hash(
        definition.get("benchmark_manifest_sha256"),
        "benchmark_manifest_sha256",
        errors,
    )
    benchmark: dict[str, Any] = {}
    try:
        benchmark_path = _repo_path(
            root,
            definition.get("benchmark_manifest", ""),
            "benchmark_manifest",
        )
        if not benchmark_path.is_file():
            errors.append("benchmark manifest is unavailable")
        else:
            try:
                if tracked_text_sha256(benchmark_path) != definition.get("benchmark_manifest_sha256"):
                    errors.append("benchmark manifest hash mismatch")
            except ValueError as exc:
                errors.append(str(exc))
            loaded_benchmark = _load_json(benchmark_path, "benchmark manifest")
            if not isinstance(loaded_benchmark, dict):
                errors.append("benchmark manifest must contain an object")
            else:
                benchmark = loaded_benchmark
    except ValueError as exc:
        errors.append(str(exc))

    task_hashes = definition.get("task_hashes")
    if not isinstance(task_hashes, dict) or not task_hashes:
        errors.append("task_hashes must be a non-empty object")
        task_hashes = {}
    else:
        for task_id, expected_hash in task_hashes.items():
            if not isinstance(task_id, str) or not task_id:
                errors.append("task_hashes keys must be non-empty strings")
            _require_hash(expected_hash, f"task_hashes.{task_id}", errors)

    tasks = benchmark.get("tasks")
    if not isinstance(tasks, list):
        errors.append("benchmark tasks must be a list")
        tasks = []
    task_ids: list[str] = []
    for index, task in enumerate(tasks):
        if not isinstance(task, dict):
            errors.append(f"benchmark task {index} must be an object")
            continue
        task_id = task.get("id")
        if not isinstance(task_id, str) or not task_id:
            errors.append(f"benchmark task {index} has an invalid id")
            continue
        task_ids.append(task_id)
        try:
            prompt = _repo_path(root, task.get("prompt", ""), f"task {task_id} prompt")
            if not prompt.is_file():
                errors.append(f"task prompt is unavailable: {task_id}")
            else:
                try:
                    if tracked_text_sha256(prompt) != task_hashes.get(task_id):
                        errors.append(f"task hash mismatch: {task_id}")
                except ValueError as exc:
                    errors.append(str(exc))
        except ValueError as exc:
            errors.append(str(exc))
    if len(task_ids) != len(set(task_ids)):
        errors.append("benchmark task IDs must be unique")
    if set(task_ids) != set(task_hashes):
        errors.append("task set does not match benchmark manifest")

    schedule_path: Path | None = None
    schedule: dict[str, Any] = {}
    try:
        schedule_path = _repo_path(
            root,
            definition.get("schedule_file", ""),
            "schedule_file",
        )
        loaded_schedule = _load_json(schedule_path, "schedule")
        if not isinstance(loaded_schedule, dict):
            errors.append("schedule must contain an object")
        else:
            schedule = loaded_schedule
    except ValueError as exc:
        errors.append(str(exc))

    if schedule.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schedule.schema_version must be {SCHEMA_VERSION}")
    if schedule.get("cell_id") != cell_id:
        errors.append("schedule cell mismatch")
    if schedule.get("seed") != SCHEDULE_SEED:
        errors.append(f"schedule seed must be {SCHEDULE_SEED}")
    if schedule.get("generator") != SCHEDULE_GENERATOR:
        errors.append("schedule generator metadata is invalid")
    if schedule.get("calibration") != {
        "block_id": "calibration-01",
        "order": ["csharp", "fsharp"],
        "counting": False,
    }:
        errors.append("calibration must be the non-counting C# then F# block")

    formal = schedule.get("formal")
    if not isinstance(formal, list):
        errors.append("schedule formal blocks must be a list")
        formal = []
    expected_ids = [f"block-{index:02d}" for index in range(1, 11)]
    actual_ids = [
        block.get("block_id") if isinstance(block, dict) else None for block in formal
    ]
    if len(formal) != 10 or actual_ids != expected_ids:
        errors.append("formal block IDs are invalid")
    orders = [block.get("order") if isinstance(block, dict) else None for block in formal]
    valid_orders = (["csharp", "fsharp"], ["fsharp", "csharp"])
    if any(order not in valid_orders for order in orders):
        errors.append("schedule order must contain each language once")
    first_languages = [order[0] for order in orders if order in valid_orders]
    if first_languages.count("csharp") != 5 or first_languages.count("fsharp") != 5:
        errors.append("formal schedule is not balanced")
    if any(
        first_languages[index] == first_languages[index - 1] == first_languages[index - 2]
        for index in range(2, len(first_languages))
    ):
        errors.append("schedule exceeds max same-order run length")
    if len(first_languages) == 10 and first_languages != _generated_first_languages(SCHEDULE_SEED):
        errors.append("formal schedule does not match the recorded generator")
    if schedule.get("constraints") != {
        "formal_blocks": 10,
        "balanced_first_language": {"csharp": 5, "fsharp": 5},
        "max_same_order_run": 2,
    }:
        errors.append("schedule constraints are invalid")

    raw_root: Path | None = None
    try:
        raw_root = _repo_path(root, definition.get("raw_root", ""), "raw_root")
    except ValueError as exc:
        errors.append(str(exc))

    return {
        "ok": not errors,
        "errors": errors,
        "definition": definition,
        "schedule": schedule,
        "definition_sha256": tracked_text_sha256(definition_file) if definition_file.is_file() else None,
        "schedule_sha256": _safe_tracked_hash(schedule_path) if schedule_path is not None and schedule_path.is_file() else None,
        "definition_file": str(definition_file),
        "schedule_file": str(schedule_path) if schedule_path is not None else None,
        "raw_root": str(raw_root) if raw_root is not None else None,
    }


def _validate_cell_v2(root: Path, definition_path: str | Path) -> dict[str, Any]:
    """Validate the condition-level schema used by the difficulty cell.

    This is deliberately separate from v1: changing the v1 validator would
    silently change the already frozen variance cells.
    """
    root = root.resolve()
    try:
        definition_file = _repo_path(root, definition_path, "definition_path")
        definition = _load_json(definition_file, "definition")
    except ValueError as exc:
        return _empty_report([str(exc)])
    if not isinstance(definition, dict):
        return _empty_report(["definition must contain an object"])
    errors: list[str] = []
    if definition.get("schema_version") != SCHEMA_V2:
        errors.append("schema_version must be 2")
    cell_id = definition.get("cell_id")
    if cell_id != "difficulty-v1":
        errors.append("cell_id must be difficulty-v1")
    _require_nonempty_string(definition.get("description"), "description", errors)

    exact_pins = {
        "model": {"snapshot": "gpt-5.4", "reasoning_effort": "medium"},
        "codex": {
            "cli_version": CODEX_CLI_VERSION,
            "image": EXPECTED_IMAGE,
            "dockerfile": "Dockerfile.codex-agent",
        },
        "image_archive": DIFFICULTY_IMAGE_ARCHIVE,
        "toolchain": {
            "dotnet_sdk": DOTNET_SDK_VERSION,
            "target_framework": TARGET_FRAMEWORK,
        },
        "limits": {
            "task_timeout_seconds": 600,
            "evaluator_timeout_seconds": 300,
            "memory": "2g",
            "cpus": 2,
            "pids": 256,
        },
        "network_policy": (
            "bridge network; candidate egress and external documentation are allowed equally "
            "for both languages; mounts are limited to /workspace plus minimized authentication file"
        ),
        "documentation_policy": (
            "No benchmark/evaluator/gold files or parent repository are exposed to candidate"
        ),
        "artifact_policy": {
            "raw": "retain every attempt outside Git",
            "redaction": "remove credentials and prompt/transcript secrets",
            "retention": "retain raw and hashes for the study record",
        },
        "failure_precedence": FAILURE_PRECEDENCE,
        "inclusion": {
            "formal_outcomes": "Pilot is non-counting; retain all outcomes",
            "metric_missingness": "Use only valid available metrics",
            "infrastructure_invalid": "Retain and report infrastructure failures",
            "calibration": "Non-counting",
            "sensitivity": "Report all failures",
        },
        "retry_policy": (
            "Retry only protocol/auth/provider/host/evaluator infrastructure-invalid attempts; "
            "retain every attempt and never replace a candidate outcome"
        ),
        "fresh_process": True,
        "schedule_file": "protocols/difficulty-v1/schedule.json",
        "raw_root": "results/difficulty-v1",
        "retention": {
            "location": "results/difficulty-v1 plus read-only study archive",
            "period": "retain raw artifacts and hashes for at least five years",
            "redaction": "remove credentials and transcript secrets before curation",
        },
        "c3_source_commit": DIFFICULTY_C3_SOURCE_COMMIT,
        "c3_artifacts": DIFFICULTY_C3_ARTIFACTS,
        "conditions": DIFFICULTY_CONDITIONS,
        "task_hashes": DIFFICULTY_TASK_HASHES,
    }
    for field, expected in exact_pins.items():
        if definition.get(field) != expected:
            errors.append(f"{field} pins are invalid")

    taxonomy = definition.get("failure_taxonomy")
    if (
        not isinstance(taxonomy, list)
        or len(taxonomy) != len(REQUIRED_FAILURES)
        or set(taxonomy) != REQUIRED_FAILURES
    ):
        errors.append("failure taxonomy is invalid")

    try:
        dockerfile = _repo_path(root, "Dockerfile.codex-agent", "codex.dockerfile")
        if not dockerfile.is_file():
            errors.append("codex.dockerfile is unavailable")
    except ValueError as exc:
        errors.append(str(exc))

    c3 = definition.get("c3_artifacts")
    if not isinstance(c3, dict) or set(c3) != set(DIFFICULTY_C3_ARTIFACTS):
        errors.append("c3_artifacts must contain exactly the six approved pins")
        c3 = c3 if isinstance(c3, dict) else {}
    for name, expected_pin in DIFFICULTY_C3_ARTIFACTS.items():
        pin = c3.get(name)
        if pin != expected_pin:
            errors.append(f"c3 artifact hash mismatch or pin mismatch: {name}")
            continue
        try:
            artifact = _repo_path(root, pin["path"], f"c3_artifacts.{name}")
            if not artifact.is_file() or tracked_text_sha256(artifact) != pin["sha256"]:
                errors.append(f"c3 artifact hash mismatch: {name}")
        except (OSError, ValueError) as exc:
            errors.append(str(exc))

    conditions = definition.get("conditions")
    if not isinstance(conditions, dict) or set(conditions) != set(DIFFICULTY_CONDITIONS):
        errors.append("conditions must contain exactly the four approved treatments")
        conditions = conditions if isinstance(conditions, dict) else {}
    loaded_manifests: dict[str, dict[str, Any]] = {}
    for condition, expected_spec in DIFFICULTY_CONDITIONS.items():
        spec = conditions.get(condition)
        if spec != expected_spec:
            errors.append(f"condition {condition} language/representation or manifest pin is invalid")
            continue
        try:
            manifest_path = _repo_path(root, spec["manifest"], f"condition {condition} manifest")
            if not manifest_path.is_file():
                errors.append(f"condition {condition} manifest is unavailable")
                continue
            if tracked_text_sha256(manifest_path) != spec["manifest_sha256"]:
                errors.append(f"condition {condition} manifest hash mismatch")
            loaded = _load_json(manifest_path, f"condition {condition} manifest")
        except (OSError, ValueError) as exc:
            errors.append(str(exc))
            continue
        if not isinstance(loaded, dict):
            errors.append(f"condition {condition} manifest must be an object")
            continue
        provenance = loaded.get("representation_provenance")
        if (
            not isinstance(provenance, dict)
            or provenance.get("treatment") != expected_spec["representation"]
            or provenance.get("source_commit") != DIFFICULTY_C3_SOURCE_COMMIT
        ):
            errors.append(f"condition {condition} representation provenance mismatch")
        loaded_manifests[condition] = loaded

    task_hashes = definition.get("task_hashes")
    if task_hashes != DIFFICULTY_TASK_HASHES:
        errors.append("task hash mismatch: task_hashes must contain the eight canonical prompt pins")
        task_hashes = task_hashes if isinstance(task_hashes, dict) else {}
    for condition, manifest in loaded_manifests.items():
        tasks = manifest.get("tasks")
        if not isinstance(tasks, list) or len(tasks) != len(DIFFICULTY_TASK_HASHES):
            errors.append(f"condition {condition} must contain eight tasks")
            continue
        task_ids: list[Any] = []
        for task in tasks:
            if not isinstance(task, dict):
                errors.append(f"condition {condition} contains a malformed task")
                continue
            task_id = task.get("id")
            task_ids.append(task_id)
            try:
                prompt_path = _repo_path(root, task.get("prompt", ""), f"task {task_id} prompt")
                if (
                    not prompt_path.is_file()
                    or tracked_text_sha256(prompt_path) != DIFFICULTY_TASK_HASHES.get(task_id)
                ):
                    errors.append(f"task hash mismatch: {task_id}")
            except (OSError, ValueError) as exc:
                errors.append(str(exc))
        if len(task_ids) != len(set(task_ids)) or set(task_ids) != set(DIFFICULTY_TASK_HASHES):
            errors.append(f"condition {condition} task set does not match top-level hashes")

    schedule_path: Path | None = None
    schedule: dict[str, Any] = {}
    try:
        schedule_path = _repo_path(root, definition.get("schedule_file", ""), "schedule_file")
        loaded_schedule = _load_json(schedule_path, "schedule")
        if not isinstance(loaded_schedule, dict):
            raise ValueError("schedule must contain an object")
        schedule = loaded_schedule
    except ValueError as exc:
        errors.append(str(exc))

    expected_schedule = {
        "schema_version": 2,
        "cell_id": "difficulty-v1",
        "williams_rows": DIFFICULTY_WILLIAMS_ROWS,
        "pilot": [
            {
                "block_id": "pilot-01",
                "order_id": "williams-01",
                "order": DIFFICULTY_WILLIAMS_ROWS[0],
                "counting": False,
                "role": "difficulty-pilot",
            }
        ],
        "formal": [],
        "randomization": False,
        "seed": None,
        "generator": "none; explicit Williams rows are authoritative",
        "constraints": {
            "pilot_blocks": 1,
            "formal_blocks": 0,
            "order_id": "williams-01",
            "randomization": False,
            "seed": None,
            "complete_williams_superblocks": True,
        },
    }
    if schedule != expected_schedule:
        if schedule.get("williams_rows") != DIFFICULTY_WILLIAMS_ROWS:
            errors.append("Williams rows are invalid")
        else:
            errors.append("difficulty schedule metadata is invalid")

    raw_root: Path | None = None
    try:
        raw_root = _repo_path(root, definition.get("raw_root", ""), "raw_root")
    except ValueError as exc:
        errors.append(str(exc))
    return {
        "ok": not errors,
        "errors": errors,
        "definition": definition,
        "schedule": schedule,
        "definition_sha256": _safe_tracked_hash(definition_file),
        "schedule_sha256": _safe_tracked_hash(schedule_path) if schedule_path else None,
        "definition_file": str(definition_file),
        "schedule_file": str(schedule_path) if schedule_path else None,
        "raw_root": str(raw_root) if raw_root else None,
    }


def validate_cell(root: Path, definition_path: str | Path) -> dict[str, Any]:
    """Dispatch validation without changing schema-v1 behavior."""
    try:
        path = _repo_path(root.resolve(), definition_path, "definition_path")
        value = _load_json(path, "definition")
    except ValueError as exc:
        return _empty_report([str(exc)])
    if (
        isinstance(value, dict)
        and value.get("schema_version") == SCHEMA_V2
        and value.get("cell_id") == "difficulty-v1"
    ):
        return _validate_cell_v2(root, definition_path)
    if isinstance(value, dict) and value.get("schema_version") == SCHEMA_V3:
        from .workstream_d import validate_child

        return validate_child(root, definition_path)
    return _validate_cell_v1(root, definition_path)


def _git(root: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout).strip()
        raise ValueError(f"git {' '.join(args)} failed: {detail}")
    return completed.stdout.strip()


def _run_probe(root: Path, argv: list[str]) -> str:
    try:
        completed = subprocess.run(
            argv,
            cwd=root,
            text=True,
            capture_output=True,
            timeout=30,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return "unavailable"
    output = (completed.stdout or completed.stderr).strip()
    if completed.returncode != 0 or not output:
        return "unavailable"
    return output.splitlines()[0]


def _physical_memory_bytes(root: Path) -> int | str:
    if hasattr(os, "sysconf") and "SC_PAGE_SIZE" in os.sysconf_names:
        try:
            value = int(os.sysconf("SC_PAGE_SIZE")) * int(os.sysconf("SC_PHYS_PAGES"))
            return value if value > 0 else "unavailable"
        except (OSError, TypeError, ValueError):
            pass
    if platform.system() == "Windows":
        value = _run_probe(
            root,
            [
                "powershell",
                "-NoProfile",
                "-Command",
                "(Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory",
            ],
        )
        try:
            parsed = int(value)
            return parsed if parsed > 0 else "unavailable"
        except ValueError:
            pass
    return "unavailable"


def probe_environment(root: Path, image: str) -> dict[str, Any]:
    """Collect model-free host, Docker, image, and container facts."""

    root = root.resolve()
    cpu = platform.processor() or os.environ.get("PROCESSOR_IDENTIFIER") or "unavailable"
    size = _run_probe(root, ["docker", "image", "inspect", image, "--format", "{{.Size}}"])
    try:
        image_size: int | str = int(size)
    except ValueError:
        image_size = "unavailable"
    return {
        "os": platform.system() or "unavailable",
        "platform": platform.platform() or "unavailable",
        "architecture": platform.machine() or "unavailable",
        "cpu": cpu,
        "physical_memory_bytes": _physical_memory_bytes(root),
        "python": sys.version.replace("\n", " "),
        "git": _run_probe(root, ["git", "--version"]),
        "dotnet": _run_probe(root, ["dotnet", "--version"]),
        "docker_client": _run_probe(
            root, ["docker", "version", "--format", "{{.Client.Version}}"]
        ),
        "docker_server": _run_probe(
            root, ["docker", "version", "--format", "{{.Server.Version}}"]
        ),
        "image_id": _run_probe(
            root, ["docker", "image", "inspect", image, "--format", "{{.Id}}"]
        ),
        "image_platform": _run_probe(
            root,
            [
                "docker",
                "image",
                "inspect",
                image,
                "--format",
                "{{.Os}}/{{.Architecture}}",
            ],
        ),
        "image_size_bytes": image_size,
        "container_codex": _run_probe(root, ["docker", "run", "--rm", image, "--version"]),
        "container_dotnet": _run_probe(
            root,
            ["docker", "run", "--rm", "--entrypoint", "dotnet", image, "--version"],
        ),
    }


def _validate_probe(facts: dict[str, Any], definition: dict[str, Any]) -> None:
    unavailable = [
        field
        for field in sorted(REQUIRED_PROBE_FIELDS)
        if facts.get(field) in (None, "", "unavailable")
    ]
    memory = facts.get("physical_memory_bytes")
    if not isinstance(memory, int) or isinstance(memory, bool) or memory <= 0:
        unavailable.append("physical_memory_bytes")
    image_size = facts.get("image_size_bytes")
    if not isinstance(image_size, int) or isinstance(image_size, bool) or image_size <= 0:
        unavailable.append("image_size_bytes")
    if unavailable:
        raise ValueError("environment probe unavailable: " + ", ".join(sorted(set(unavailable))))
    expected_image_id = definition["image_archive"]["local_image_id"]
    if facts["image_id"] != expected_image_id:
        raise ValueError("Docker image ID mismatch")
    if facts["container_codex"] != f"codex-cli {definition['codex']['cli_version']}":
        raise ValueError("container Codex CLI version mismatch")
    if facts["container_dotnet"] != definition["toolchain"]["dotnet_sdk"]:
        raise ValueError("container .NET version mismatch")
    if facts["dotnet"] != definition["toolchain"]["dotnet_sdk"]:
        raise ValueError("host .NET version mismatch")


Probe = Callable[[Path, str], dict[str, Any]]
ArchiveVerifier = Callable[[dict[str, Any]], dict[str, Any]]


def verify_image_archive(archive: dict[str, Any]) -> dict[str, Any]:
    """Verify the retained image archive against the frozen metadata."""

    path = Path(archive["path"]).resolve()
    if not path.is_file():
        raise ValueError(f"retained image archive is unavailable: {path}")
    actual_bytes = path.stat().st_size
    if actual_bytes != archive["bytes"]:
        raise ValueError("retained image archive byte count mismatch")
    actual_hash = sha256(path)
    if actual_hash != archive["sha256"]:
        raise ValueError("retained image archive SHA-256 mismatch")
    return {
        "path": str(path),
        "bytes": actual_bytes,
        "sha256": actual_hash,
        "verified": True,
    }


def _archive_for_root(root: Path, archive: dict[str, Any]) -> dict[str, Any]:
    """Resolve repository-relative archive metadata without mutating a definition."""

    resolved = dict(archive)
    archive_path = Path(archive["path"])
    if not archive_path.is_absolute():
        resolved["path"] = str((root / archive_path).resolve())
    return resolved


def freeze_cell(
    root: Path,
    definition_path: str | Path,
    *,
    _probe: Probe | None = None,
    _archive_verifier: ArchiveVerifier | None = None,
) -> dict[str, Any]:
    """Resolve a valid definition against a clean commit and live environment."""

    root = root.resolve()
    report = validate_cell(root, definition_path)
    if not report["ok"]:
        raise ValueError("cannot freeze invalid cell: " + "; ".join(report["errors"]))
    if _git(root, "status", "--porcelain"):
        raise ValueError("cannot freeze a dirty repository")
    commit = _git(root, "rev-parse", "--verify", "HEAD")
    if _HEX_64.fullmatch(commit) is None and re.fullmatch(r"[0-9a-f]{40}", commit) is None:
        raise ValueError("Git HEAD is not a commit hash")

    definition = report["definition"]
    facts = (_probe or probe_environment)(root, definition["codex"]["image"])
    if not isinstance(facts, dict):
        raise ValueError("environment probe must return an object")
    _validate_probe(facts, definition)
    archive_verification = (_archive_verifier or verify_image_archive)(
        _archive_for_root(root, definition["image_archive"])
    )
    if (
        not isinstance(archive_verification, dict)
        or archive_verification.get("verified") is not True
        or archive_verification.get("bytes") != definition["image_archive"]["bytes"]
        or archive_verification.get("sha256") != definition["image_archive"]["sha256"]
    ):
        raise ValueError("retained image archive verification mismatch")

    definition_file = Path(report["definition_file"])
    manifest: dict[str, Any] = {
        "schema_version": definition.get("schema_version", SCHEMA_VERSION),
        "frozen": True,
        "frozen_at": datetime.now(timezone.utc).isoformat(),
        "cell_id": definition["cell_id"],
        "git_head": commit,
        "dirty": False,
        "definition_file": definition_file.relative_to(root).as_posix(),
        "definition_sha256": report["definition_sha256"],
        "schedule_sha256": report["schedule_sha256"],
        "image": definition["codex"]["image"],
        "image_id": facts["image_id"],
        "environment": facts,
        "image_archive_verification": archive_verification,
        "definition": definition,
        "schedule": report["schedule"],
    }
    if definition.get("schema_version") == SCHEMA_V3:
        family_definition_file = Path(report["family_definition_file"])
        schedule_file = Path(report["schedule_file"])
        catalog_file = Path(report["catalog_file"])
        manifest.update(
            {
                "family_id": definition["family_id"],
                "configuration_id": definition["configuration_id"],
                "family_definition_file": family_definition_file.relative_to(
                    root
                ).as_posix(),
                "family_definition_sha256": report["family_definition_sha256"],
                "family_definition": report["family_definition"],
                "parent_schedule_file": schedule_file.relative_to(root).as_posix(),
                "parent_schedule_sha256": report["schedule_sha256"],
                "catalog_file": catalog_file.relative_to(root).as_posix(),
                "catalog_sha256": report["catalog_sha256"],
                "catalog": report["catalog"],
                "assignment_sha256": report["assignment_sha256"],
            }
        )
    manifest["manifest_sha256"] = canonical_json_hash(manifest)
    return manifest


def _require_ignored(root: Path, path: Path) -> None:
    relative = path.relative_to(root).as_posix()
    _git(root, "check-ignore", "-q", "--", relative)


def write_frozen_manifest(
    root: Path,
    definition_path: str | Path,
    output: Path,
    *,
    _probe: Probe | None = None,
    _archive_verifier: ArchiveVerifier | None = None,
) -> Path:
    """Create a resolved manifest atomically inside the ignored raw root."""

    root = root.resolve()
    report = validate_cell(root, definition_path)
    if not report["ok"]:
        raise ValueError("cannot freeze invalid cell: " + "; ".join(report["errors"]))
    raw_root = Path(report["raw_root"])
    _require_ignored(root, raw_root / ".freeze-probe")

    target = output.resolve() if output.is_absolute() else (root / output).resolve()
    try:
        target.relative_to(raw_root)
    except ValueError as exc:
        raise ValueError("frozen manifest must be under definition raw_root") from exc
    if target.exists():
        raise FileExistsError(target)

    manifest = freeze_cell(
        root,
        definition_path,
        _probe=_probe,
        _archive_verifier=_archive_verifier,
    )
    payload = json.dumps(manifest, indent=2, sort_keys=True) + "\n"

    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_name(f".{target.name}.{uuid.uuid4().hex}.tmp")
    try:
        with temporary.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        try:
            os.link(temporary, target)
        except FileExistsError:
            raise FileExistsError(target) from None
    finally:
        temporary.unlink(missing_ok=True)
    return target


def load_frozen_manifest(root: Path, manifest_path: str | Path) -> dict[str, Any]:
    """Load a manifest and verify it against the current clean tracked checkout."""

    root = root.resolve()
    path = Path(manifest_path).resolve()
    value = _load_json(path, "protocol manifest")
    if not isinstance(value, dict):
        raise ValueError("protocol manifest must contain an object")
    if value.get("schema_version") not in {SCHEMA_VERSION, SCHEMA_V2, SCHEMA_V3}:
        raise ValueError("protocol manifest schema version is invalid")
    if value.get("frozen") is not True or value.get("dirty") is not False:
        raise ValueError("protocol manifest is not a clean frozen manifest")
    claimed_hash = value.get("manifest_sha256")
    unsigned = dict(value)
    unsigned.pop("manifest_sha256", None)
    if not isinstance(claimed_hash, str) or claimed_hash != canonical_json_hash(unsigned):
        raise ValueError("protocol manifest hash mismatch")

    definition_file = _repo_path(
        root,
        value.get("definition_file", ""),
        "protocol manifest definition_file",
    )
    report = validate_cell(root, definition_file)
    if not report["ok"]:
        raise ValueError("protocol definition is no longer valid: " + "; ".join(report["errors"]))
    definition = report["definition"]
    schedule = report["schedule"]
    if value.get("schema_version") != definition.get("schema_version"):
        raise ValueError("protocol manifest schema version does not match embedded definition")
    if value.get("cell_id") != definition.get("cell_id"):
        raise ValueError("protocol manifest cell mismatch")
    if value.get("definition") != definition or value.get("schedule") != schedule:
        raise ValueError("embedded protocol definition or schedule mismatch")
    if value.get("definition_sha256") != report["definition_sha256"]:
        raise ValueError("protocol definition hash mismatch")
    if value.get("schedule_sha256") != report["schedule_sha256"]:
        raise ValueError("protocol schedule hash mismatch")
    if value.get("schema_version") == SCHEMA_V3:
        family_definition_file = Path(report["family_definition_file"])
        schedule_file = Path(report["schedule_file"])
        catalog_file = Path(report["catalog_file"])
        expected_v3 = {
            "family_id": definition["family_id"],
            "configuration_id": definition["configuration_id"],
            "family_definition_file": family_definition_file.relative_to(
                root
            ).as_posix(),
            "family_definition_sha256": report["family_definition_sha256"],
            "family_definition": report["family_definition"],
            "parent_schedule_file": schedule_file.relative_to(root).as_posix(),
            "parent_schedule_sha256": report["schedule_sha256"],
            "catalog_file": catalog_file.relative_to(root).as_posix(),
            "catalog_sha256": report["catalog_sha256"],
            "catalog": report["catalog"],
            "assignment_sha256": report["assignment_sha256"],
        }
        for field, expected in expected_v3.items():
            if value.get(field) != expected:
                raise ValueError(f"protocol Workstream D {field} mismatch")
        required_v3_fields = {
            "schema_version",
            "frozen",
            "frozen_at",
            "cell_id",
            "git_head",
            "dirty",
            "definition_file",
            "definition_sha256",
            "schedule_sha256",
            "image",
            "image_id",
            "environment",
            "image_archive_verification",
            "definition",
            "schedule",
            "manifest_sha256",
            *expected_v3.keys(),
        }
        if set(value) != required_v3_fields:
            raise ValueError("protocol Workstream D manifest fields mismatch")
    if value.get("image") != definition["codex"]["image"]:
        raise ValueError("protocol image tag mismatch")
    if value.get("image_id") != definition["image_archive"]["local_image_id"]:
        raise ValueError("protocol image ID mismatch")
    archive_verification = value.get("image_archive_verification")
    if (
        not isinstance(archive_verification, dict)
        or archive_verification.get("verified") is not True
        or archive_verification.get("bytes") != definition["image_archive"]["bytes"]
        or archive_verification.get("sha256") != definition["image_archive"]["sha256"]
    ):
        raise ValueError("protocol image archive verification mismatch")

    raw_root = Path(report["raw_root"])
    try:
        path.relative_to(raw_root)
    except ValueError as exc:
        raise ValueError("protocol manifest must be under definition raw_root") from exc
    _require_ignored(root, path)

    if _git(root, "status", "--porcelain"):
        raise ValueError("repository is dirty; frozen protocol cannot run")
    head = _git(root, "rev-parse", "--verify", "HEAD")
    if head != value.get("git_head"):
        raise ValueError("repository HEAD does not match frozen protocol")
    return value


def classify_failure(
    *,
    protocol_ok: bool,
    accounting_ok: bool,
    auth_ok: bool,
    provider_ok: bool,
    host_ok: bool,
    timed_out: bool,
    agent_ok: bool,
    evaluator_ok: bool,
) -> str | None:
    """Return the first failing category under the frozen adjudication order."""

    values = {
        "protocol": protocol_ok,
        "auth": auth_ok,
        "provider": provider_ok,
        "host": host_ok,
        "timeout": not timed_out,
        "accounting": accounting_ok,
        "agent": agent_ok,
        "evaluator": evaluator_ok,
    }
    return next((name for name in FAILURE_PRECEDENCE if not values[name]), None)
