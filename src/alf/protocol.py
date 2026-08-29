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
MODEL_SNAPSHOT = "gpt-5.4-mini-2026-03-17"
REASONING_EFFORT = "medium"
CODEX_CLI_VERSION = "0.149.1"
DOTNET_SDK_VERSION = "10.0.302"
TARGET_FRAMEWORK = "net10.0"
EXPECTED_IMAGE = "alf-codex:0.149.1"
EXPECTED_IMAGE_ID = (
    "sha256:0320a60c5b2628cebeb2c897bbf80da949f3b9bb99fa61f5a3475c7276328756"
)
SCHEDULE_SEED = 20260829
SCHEDULE_GENERATOR = (
    "Python 3.12: r=random.Random(20260829); "
    "first=['fsharp']*5+['csharp']*5; r.shuffle(first); r.shuffle(first); "
    "explicit sequence is authoritative"
)

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


def validate_cell(root: Path, definition_path: str | Path) -> dict[str, Any]:
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
    elif model != {
        "snapshot": MODEL_SNAPSHOT,
        "reasoning_effort": REASONING_EFFORT,
    }:
        errors.append("model pins are invalid")

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
        definition["image_archive"]
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
        "schema_version": SCHEMA_VERSION,
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
    if value.get("schema_version") != SCHEMA_VERSION:
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
    if value.get("cell_id") != definition.get("cell_id"):
        raise ValueError("protocol manifest cell mismatch")
    if value.get("definition") != definition or value.get("schedule") != schedule:
        raise ValueError("embedded protocol definition or schedule mismatch")
    if value.get("definition_sha256") != report["definition_sha256"]:
        raise ValueError("protocol definition hash mismatch")
    if value.get("schedule_sha256") != report["schedule_sha256"]:
        raise ValueError("protocol schedule hash mismatch")
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
