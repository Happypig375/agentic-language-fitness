"""Frozen states and schedule for the model-free Workstream E2 baseline.

Execution and report/audit concerns live in ``workstream_e2_runner`` and
``workstream_e2_report`` respectively.
"""
from __future__ import annotations

from collections import Counter
import difflib
import hashlib
import importlib.metadata
import json
import os
import re
import shutil
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path, PurePosixPath
from typing import Any

from .benchmark_artifacts import (
    artifact_plan,
    check_workspace,
    checks_for_language,
    copy_artifacts,
)
from .config import REQUIRED_DOTNET_SDK, load_manifest
from .metrics import TOKEN_RE
from .protocol import canonical_json_hash, tracked_text_sha256


DEFINITION_SCHEMA = "alf.workstream-e2.definition.v1"
REPORT_SCHEMA = "alf.workstream-e2.report.v1"
ATTEMPT_SCHEMA = "alf.workstream-e2.attempt.v1"
RAW_INVENTORY_SCHEMA = "alf.workstream-e2.raw-inventory.v1"
SCHEDULE_SEED = "alf-workstream-e2-paired-rounds-v1"
TOKENIZER_VERSION = "0.14.0"
TOKENIZER_ENCODING = "o200k_base"
SOURCE_SERIALIZATION = "lf-normalized-utf8-files-v1"
ENVIRONMENT_PROFILE = "github-actions-ubuntu-24.04-dotnet10.0.302-offline-v1"
COMMAND_TIMEOUT_SECONDS = 300
ROUNDS = 5
STAGES = 9
LANGUAGES = ("csharp", "fsharp")
SOURCE_SUFFIXES = {".cs", ".fs", ".fsx", ".csproj", ".fsproj"}
EXCLUDED_PARTS = {".git", ".alf", "bin", "obj", "__pycache__"}
CHECK_KEYS = ("file_exists", "text_contains", "text_not_contains")
COMMAND_TEMPLATES = {
    "restore": ["dotnet", "restore", "<project>", "--nologo"],
    "build": [
        "dotnet",
        "build",
        "<project>",
        "--configuration",
        "Release",
        "--no-incremental",
        "--no-restore",
        "--nologo",
    ],
    "run": [
        "dotnet",
        "run",
        "--project",
        "<project>",
        "--configuration",
        "Release",
        "--no-build",
    ],
}
WARNING_RE = re.compile(rb"\bwarning(?:\s+([A-Za-z]+\d+))?\b", re.IGNORECASE)
HEX_40_RE = re.compile(r"^[0-9a-f]{40}$")
HEX_64_RE = re.compile(r"^[0-9a-f]{64}$")
ABSOLUTE_WINDOWS_RE = re.compile(r"^[A-Za-z]:[\\/]")


class E2RunError(RuntimeError):
    """A bounded, publish-safe E2 failure."""

    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _normalise_text(raw: bytes, *, label: str) -> bytes:
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"{label} is not UTF-8") from exc
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def _resolve(root: Path, value: str | Path) -> Path:
    path = Path(value)
    return (path if path.is_absolute() else root / path).resolve()


def _inside(parent: Path, child: Path) -> bool:
    parent = parent.resolve()
    child = child.resolve()
    return child == parent or parent in child.parents


def _repo_relative(root: Path, path: Path, *, label: str) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError as exc:
        raise ValueError(f"{label} must be inside the repository") from exc


def _safe_relative(value: str, *, label: str) -> str:
    path = PurePosixPath(value.replace("\\", "/"))
    if path.is_absolute() or not path.parts or any(part in {"", ".", ".."} for part in path.parts):
        raise ValueError(f"{label} must be a safe relative path")
    return path.as_posix()


def _atomic_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(handle, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    except BaseException:
        try:
            Path(temporary).unlink(missing_ok=True)
        finally:
            raise


def _atomic_json(path: Path, value: Any) -> None:
    _atomic_bytes(path, json.dumps(value, indent=2, sort_keys=True).encode("utf-8") + b"\n")


def _get_encoding() -> Any:
    try:
        version = importlib.metadata.version("tiktoken")
    except importlib.metadata.PackageNotFoundError as exc:
        raise ValueError(f"tiktoken=={TOKENIZER_VERSION} is required") from exc
    if version != TOKENIZER_VERSION:
        raise ValueError(f"tiktoken must be exactly {TOKENIZER_VERSION}, found {version}")
    import tiktoken

    encoding = tiktoken.get_encoding(TOKENIZER_ENCODING)
    if getattr(encoding, "name", None) != TOKENIZER_ENCODING:
        raise ValueError("unexpected tokenizer encoding")
    return encoding


def _included_source(path: Path) -> bool:
    return path.suffix.lower() in SOURCE_SUFFIXES and not any(
        part.casefold() in EXCLUDED_PARTS for part in path.parts
    )


def _snapshot(workspace: Path, encoding: Any) -> tuple[dict[str, Any], dict[str, str]]:
    records: list[dict[str, Any]] = []
    texts: dict[str, str] = {}
    for path in sorted(workspace.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(workspace)
        if not _included_source(relative):
            continue
        rel = relative.as_posix()
        normalised = _normalise_text(path.read_bytes(), label=rel)
        text = normalised.decode("utf-8")
        kind = "project" if path.suffix.lower() in {".csproj", ".fsproj"} else "source"
        records.append(
            {
                "path": rel,
                "kind": kind,
                "sha256": _sha(normalised),
                "bytes": len(normalised),
                "lines": len(text.splitlines()),
                "lexical_units": len(TOKEN_RE.findall(text)),
                "tokenizer_proxy_tokens": len(encoding.encode(text)),
            }
        )
        texts[rel] = text

    if not records:
        raise ValueError("canonical state has no source/project files")
    file_hashes = {record["path"]: record["sha256"] for record in records}
    metrics: dict[str, int] = {}
    for prefix, selected in (
        ("source", [record for record in records if record["kind"] == "source"]),
        ("project", [record for record in records if record["kind"] == "project"]),
        ("tree", records),
    ):
        metrics[f"{prefix}_files"] = len(selected)
        for field in ("bytes", "lines", "lexical_units", "tokenizer_proxy_tokens"):
            metrics[f"{prefix}_{field}"] = sum(int(record[field]) for record in selected)
    return (
        {
            "source_tree_sha256": _sha(_canonical_bytes(file_hashes)),
            "files": records,
            "metrics": metrics,
        },
        texts,
    )


def source_tree_hash(files: dict[str, str]) -> str:
    """Compatibility helper for tests and downstream report checks."""

    return _sha(_canonical_bytes(files))


def _line_diff(before: str, after: str, path: str) -> tuple[int, int, int]:
    left = before.splitlines(keepends=True)
    right = after.splitlines(keepends=True)
    added = deleted = 0
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(a=left, b=right).get_opcodes():
        if tag in {"replace", "delete"}:
            deleted += i2 - i1
        if tag in {"replace", "insert"}:
            added += j2 - j1
    patch = "".join(
        difflib.unified_diff(left, right, fromfile=f"a/{path}", tofile=f"b/{path}", lineterm="\n")
    ).encode("utf-8")
    return added, deleted, len(patch)


def _stage_diff(
    before_snapshot: dict[str, Any] | None,
    before_texts: dict[str, str] | None,
    after_snapshot: dict[str, Any],
    after_texts: dict[str, str],
) -> dict[str, Any]:
    if before_snapshot is None or before_texts is None:
        return {
            "added_paths": [],
            "modified_paths": [],
            "deleted_paths": [],
            "changed_files": 0,
            "added_lines": 0,
            "deleted_lines": 0,
            "diff_bytes": 0,
            "metric_deltas": {key: 0 for key in after_snapshot["metrics"]},
        }

    before_files = {row["path"]: row for row in before_snapshot["files"]}
    after_files = {row["path"]: row for row in after_snapshot["files"]}
    added_paths = sorted(set(after_files) - set(before_files))
    deleted_paths = sorted(set(before_files) - set(after_files))
    modified_paths = sorted(
        path
        for path in set(before_files) & set(after_files)
        if before_files[path]["sha256"] != after_files[path]["sha256"]
    )
    added_lines = deleted_lines = diff_bytes = 0
    for path in [*added_paths, *modified_paths, *deleted_paths]:
        added, deleted, size = _line_diff(before_texts.get(path, ""), after_texts.get(path, ""), path)
        added_lines += added
        deleted_lines += deleted
        diff_bytes += size
    deltas = {
        key: int(after_snapshot["metrics"][key]) - int(before_snapshot["metrics"].get(key, 0))
        for key in after_snapshot["metrics"]
    }
    return {
        "added_paths": added_paths,
        "modified_paths": modified_paths,
        "deleted_paths": deleted_paths,
        "changed_files": len(added_paths) + len(modified_paths) + len(deleted_paths),
        "added_lines": added_lines,
        "deleted_lines": deleted_lines,
        "diff_bytes": diff_bytes,
        "metric_deltas": deltas,
    }


def _copy_base(root: Path, config: dict[str, Any], target: Path) -> None:
    source = _resolve(root, config["base"])
    if not source.is_dir() or not _inside(root, source):
        raise ValueError("base workspace is missing or outside the repository")
    shutil.copytree(
        source,
        target,
        dirs_exist_ok=True,
        ignore=shutil.ignore_patterns("bin", "obj", ".git", ".alf", "__pycache__"),
    )


def _assert_no_build_directories(workspace: Path) -> None:
    offenders = sorted(
        path.relative_to(workspace).as_posix()
        for path in workspace.rglob("*")
        if path.is_dir() and path.name.casefold() in {"bin", "obj"}
    )
    if offenders:
        raise E2RunError("fresh_workspace_contains_build_directory")


def _materialize(root: Path, manifest: dict[str, Any], language: str, stage: int, workspace: Path) -> None:
    _copy_base(root, manifest["languages"][language], workspace)
    for task in manifest["tasks"][:stage]:
        copy_artifacts(artifact_plan(root, manifest, language, task, workspace))
    _assert_no_build_directories(workspace)


def _cumulative_checks(manifest: dict[str, Any], language: str, stage: int) -> dict[str, list[Any]]:
    merged: dict[str, list[Any]] = {key: [] for key in CHECK_KEYS}
    languages = set(manifest["languages"])
    for task in manifest["tasks"][:stage]:
        selected = checks_for_language(task, language, languages)
        for key in CHECK_KEYS:
            merged[key].extend(selected[key])
    return merged


def _check_summary(checks: dict[str, list[Any]]) -> dict[str, Any]:
    paths: list[str] = []
    for value in checks["file_exists"]:
        paths.append(_safe_relative(value, label="workspace-check path"))
    for key in ("text_contains", "text_not_contains"):
        for value in checks[key]:
            paths.append(_safe_relative(value["path"], label="workspace-check path"))
    return {
        "counts": {key: len(checks[key]) for key in CHECK_KEYS},
        "paths": sorted(set(paths)),
    }


def _task_artifact_targets(
    root: Path,
    manifest: dict[str, Any],
    language: str,
    task: dict[str, Any],
    workspace: Path,
) -> list[str]:
    return [artifact.target_relative for artifact in artifact_plan(root, manifest, language, task, workspace)]


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _compile_obligations(workspace: Path, config: dict[str, Any], language: str) -> dict[str, Any]:
    project_relative = _safe_relative(config["project_file"], label="project file")
    project_path = workspace / project_relative
    try:
        xml_root = ET.fromstring(project_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ET.ParseError) as exc:
        raise ValueError("project file is not valid UTF-8 XML") from exc

    includes: list[str] = []
    removes: list[str] = []
    target_frameworks: list[str] = []
    for element in xml_root.iter():
        name = _local_name(element.tag)
        if name == "Compile":
            if "Include" in element.attrib:
                includes.append(_safe_relative(element.attrib["Include"], label="Compile Include"))
            if "Remove" in element.attrib:
                removes.append(_safe_relative(element.attrib["Remove"], label="Compile Remove"))
        elif name in {"TargetFramework", "TargetFrameworks"} and element.text:
            target_frameworks.extend(value.strip() for value in element.text.split(";") if value.strip())

    source_suffix = ".cs" if language == "csharp" else ".fs"
    discovered = sorted(
        path.relative_to(workspace).as_posix()
        for path in workspace.rglob(f"*{source_suffix}")
        if path.is_file() and _included_source(path.relative_to(workspace))
    )
    if language == "fsharp":
        if includes != discovered:
            raise ValueError("F# project Compile order does not exactly cover canonical .fs inputs")
        mode = "explicit-project-order"
        static_inputs = includes
    else:
        if includes or removes:
            raise ValueError("C# canonical project must use unmodified SDK source discovery")
        mode = "sdk-default-source-discovery"
        static_inputs = discovered
    return {
        "mode": mode,
        "project_file": project_relative,
        "target_frameworks": target_frameworks,
        "declared_compile_includes": includes,
        "declared_compile_removes": removes,
        "static_source_inputs": static_inputs,
        "static_source_input_count": len(static_inputs),
        "observed_compiler_inputs": None,
    }


def _state_id(language: str, stage: int, task_id: str) -> str:
    return f"{language}-s{stage:02d}-{task_id}"


def _state(
    root: Path,
    manifest: dict[str, Any],
    language: str,
    stage: int,
    encoding: Any,
    previous_snapshot: dict[str, Any] | None,
    previous_texts: dict[str, str] | None,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, str]]:
    with tempfile.TemporaryDirectory(prefix="alf-e2-state-") as temporary:
        workspace = Path(temporary)
        _materialize(root, manifest, language, stage, workspace)
        checks = _cumulative_checks(manifest, language, stage)
        check_result = check_workspace(workspace, checks)
        if not check_result["ok"]:
            raise ValueError("canonical workspace checks failed during freeze")
        snapshot, texts = _snapshot(workspace, encoding)
        compile_obligations = _compile_obligations(workspace, manifest["languages"][language], language)
        cumulative: list[dict[str, Any]] = []
        for task in manifest["tasks"][:stage]:
            selected = checks_for_language(task, language, set(manifest["languages"]))
            targets = _task_artifact_targets(root, manifest, language, task, workspace)
            cumulative.append(
                {
                    "task_id": task["id"],
                    "artifact_targets": targets,
                    "project_file_changed": manifest["languages"][language]["project_file"] in targets,
                    "cases_added": len(task.get("cases", [])),
                    "workspace_checks": _check_summary(selected),
                }
            )
        task_id = "baseline" if stage == 0 else manifest["tasks"][stage - 1]["id"]
        state = {
            "state_id": _state_id(language, stage, task_id),
            "language": language,
            "stage": stage,
            "task_id": task_id,
            "project": manifest["languages"][language]["project_file"],
            "task_count": stage,
            "case_count": len(manifest["baseline_cases"])
            + sum(len(task.get("cases", [])) for task in manifest["tasks"][:stage]),
            "workspace_checks": _check_summary(checks),
            "cumulative_task_obligations": cumulative,
            "compile_obligations": compile_obligations,
            "stage_local_diff": _stage_diff(previous_snapshot, previous_texts, snapshot, texts),
            **snapshot,
        }
        return state, snapshot, texts


def build_schedule() -> list[dict[str, Any]]:
    csharp_first_rounds: dict[int, set[int]] = {}
    for stage in range(STAGES):
        ranked_rounds = sorted(
            range(1, ROUNDS + 1),
            key=lambda round_number: _sha(
                f"{SCHEDULE_SEED}|stage={stage}|round={round_number}|language-balance".encode("ascii")
            ),
        )
        csharp_count = 2 + int(
            _sha(f"{SCHEDULE_SEED}|stage={stage}|language-majority".encode("ascii")), 16
        ) % 2
        csharp_first_rounds[stage] = set(ranked_rounds[:csharp_count])
    rows: list[dict[str, Any]] = []
    position = 0
    for round_number in range(1, ROUNDS + 1):
        stages = sorted(
            range(STAGES),
            key=lambda stage: _sha(f"{SCHEDULE_SEED}|round={round_number}|stage={stage}".encode("ascii")),
        )
        for pair_position, stage in enumerate(stages, 1):
            first = "csharp" if round_number in csharp_first_rounds[stage] else "fsharp"
            second = "fsharp" if first == "csharp" else "csharp"
            for language_position, language in enumerate((first, second), 1):
                position += 1
                rows.append(
                    {
                        "position": position,
                        "round": round_number,
                        "pair_position": pair_position,
                        "stage": stage,
                        "language": language,
                        "language_position": language_position,
                    }
                )
    return rows


def _schedule_errors(schedule: Any) -> list[str]:
    if not isinstance(schedule, list):
        return ["schedule must be a list"]
    errors: list[str] = []
    if len(schedule) != ROUNDS * STAGES * len(LANGUAGES):
        errors.append("schedule must contain exactly 90 entries")
        return errors
    expected_keys = {"position", "round", "pair_position", "stage", "language", "language_position"}
    valid_rows: list[dict[str, Any]] = []
    for index, row in enumerate(schedule, 1):
        if not isinstance(row, dict) or set(row) != expected_keys:
            errors.append(f"schedule entry {index} has invalid keys")
            continue
        if (
            row["position"] != index
            or not isinstance(row["round"], int)
            or row["round"] not in range(1, ROUNDS + 1)
            or not isinstance(row["pair_position"], int)
            or row["pair_position"] not in range(1, STAGES + 1)
            or not isinstance(row["stage"], int)
            or row["stage"] not in range(STAGES)
            or row["language"] not in LANGUAGES
            or row["language_position"] not in (1, 2)
        ):
            errors.append(f"schedule entry {index} has invalid values")
            continue
        valid_rows.append(row)
    counts = Counter((row["language"], row["stage"]) for row in valid_rows)
    for language in LANGUAGES:
        for stage in range(STAGES):
            if counts[(language, stage)] != ROUNDS:
                errors.append(f"{language} stage {stage} must occur five times")
    for stage in range(STAGES):
        first_counts = Counter(
            row.get("language")
            for row in valid_rows
            if row["stage"] == stage and row["language_position"] == 1
        )
        if set(first_counts) != set(LANGUAGES) or sorted(first_counts.values()) != [2, 3]:
            errors.append(f"stage {stage} language-first order must be balanced 2/3")
    for round_number in range(1, ROUNDS + 1):
        part = [row for row in valid_rows if row["round"] == round_number]
        if len(part) != STAGES * 2:
            errors.append(f"round {round_number} must contain 18 entries")
            continue
        for offset in range(0, len(part), 2):
            pair = part[offset : offset + 2]
            if (
                pair[0].get("stage") != pair[1].get("stage")
                or {pair[0].get("language"), pair[1].get("language")} != set(LANGUAGES)
                or [pair[0].get("language_position"), pair[1].get("language_position")] != [1, 2]
                or pair[0].get("pair_position") != offset // 2 + 1
                or pair[1].get("pair_position") != offset // 2 + 1
            ):
                errors.append(f"round {round_number} pair {offset // 2 + 1} is not adjacent/matched")
    return errors


def _build_definition(root: Path, manifest_path: str | Path) -> dict[str, Any]:
    root = root.resolve()
    path = _resolve(root, manifest_path)
    manifest_relative = _repo_relative(root, path, label="manifest")
    manifest = load_manifest(root, path)
    if tuple(sorted(manifest["languages"])) != LANGUAGES or len(manifest["tasks"]) != STAGES - 1:
        raise ValueError("E2 requires the matched C#/F# eight-task successor manifest")
    encoding = _get_encoding()

    by_identity: dict[tuple[str, int], dict[str, Any]] = {}
    for language in LANGUAGES:
        previous_snapshot: dict[str, Any] | None = None
        previous_texts: dict[str, str] | None = None
        for stage in range(STAGES):
            state, previous_snapshot, previous_texts = _state(
                root,
                manifest,
                language,
                stage,
                encoding,
                previous_snapshot,
                previous_texts,
            )
            by_identity[(language, stage)] = state
    states = [by_identity[(language, stage)] for stage in range(STAGES) for language in LANGUAGES]
    schedule = build_schedule()
    schedule_errors = _schedule_errors(schedule)
    if schedule_errors:
        raise ValueError("internal E2 schedule error: " + "; ".join(schedule_errors))
    expanded_commands = {
        language: {
            operation: [manifest["languages"][language]["project_file"] if arg == "<project>" else arg for arg in argv]
            for operation, argv in COMMAND_TEMPLATES.items()
        }
        for language in LANGUAGES
    }
    definition: dict[str, Any] = {
        "schema_version": DEFINITION_SCHEMA,
        "manifest": {
            "path": manifest_relative,
            "normalized_sha256": tracked_text_sha256(path),
        },
        "source_serialization": SOURCE_SERIALIZATION,
        "tokenizer": {
            "package": "tiktoken",
            "version": TOKENIZER_VERSION,
            "encoding": TOKENIZER_ENCODING,
        },
        "commands": {
            "templates": COMMAND_TEMPLATES,
            "expanded_by_language": expanded_commands,
            "timeout_seconds": COMMAND_TIMEOUT_SECONDS,
        },
        "execution_contract": {
            "environment_profile": ENVIRONMENT_PROFILE,
            "rounds": ROUNDS,
            "states": STAGES * len(LANGUAGES),
            "schedule_entries": ROUNDS * STAGES * len(LANGUAGES),
            "fresh_regime": ["restore", "build", "run", "evaluator"],
            "repeat_regime": ["build", "run", "evaluator"],
            "preflight_states": STAGES * len(LANGUAGES),
            "preflight": "materialize-hash-static-obligations-and-workspace-checks-only",
            "network": "container-only-loopback-no-usable-default-route",
            "package_cache": "preexisting-and-byte-identical",
            "os_page_cache": "not-cleared-or-controlled",
            "raw_output": "external-to-git",
        },
        "schedule_seed": SCHEDULE_SEED,
        "schedule": schedule,
        "schedule_sha256": _sha(_canonical_bytes(schedule)),
        "states": states,
    }
    definition["definition_sha256"] = canonical_json_hash(definition)
    return definition


def freeze_definition(root: Path, manifest_path: str | Path, output: str | Path) -> dict[str, Any]:
    root = root.resolve()
    definition = _build_definition(root, manifest_path)
    target = _resolve(root, output)
    _repo_relative(root, target, label="definition output")
    _atomic_json(target, definition)
    return definition


def _read_json_object(path: Path, *, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"{label} is not valid UTF-8 JSON") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a JSON object")
    return value


def check_definition(root: Path, definition_path: str | Path, manifest_path: str | Path) -> dict[str, Any]:
    root = root.resolve()
    path = _resolve(root, definition_path)
    errors: list[str] = []
    try:
        data = _read_json_object(path, label="E2 definition")
    except ValueError as exc:
        return {"ok": False, "errors": [str(exc)], "definition_sha256": None}

    claimed = data.get("definition_sha256")
    unsigned = dict(data)
    unsigned.pop("definition_sha256", None)
    if not isinstance(claimed, str) or not HEX_64_RE.fullmatch(claimed):
        errors.append("definition_sha256 must be lowercase SHA-256")
    elif claimed != canonical_json_hash(unsigned):
        errors.append("definition self-hash mismatch")
    errors.extend(_schedule_errors(data.get("schedule")))
    if data.get("schedule_sha256") != _sha(_canonical_bytes(data.get("schedule"))):
        errors.append("schedule hash mismatch")
    try:
        expected = _build_definition(root, manifest_path)
        if data != expected:
            errors.append("definition differs from canonical recomputation")
    except (OSError, ValueError) as exc:
        errors.append(f"canonical recomputation failed: {exc}")
    return {"ok": not errors, "errors": sorted(set(errors)), "definition_sha256": claimed}
