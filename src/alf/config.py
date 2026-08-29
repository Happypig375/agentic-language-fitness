from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class Manifest(dict[str, Any]):
    """Manifest mapping with non-serialized source context."""

    manifest_parent: Path


DEFAULT_MANIFEST = Path("benchmarks/pilot/manifest.json")
# Keep the toolchain contract in one place so environment checks and tests do
# not silently drift from global.json and the benchmark project files.
REQUIRED_DOTNET_SDK = "10.0.302"
REQUIRED_DOTNET_TARGET_FRAMEWORK = "net10.0"


def find_repo_root(start: Path | None = None) -> Path:
    current = (start or Path.cwd()).resolve()
    for candidate in (current, *current.parents):
        if (candidate / "pyproject.toml").is_file() and (candidate / "benchmarks").is_dir():
            return candidate
    raise FileNotFoundError("Could not find repository root containing pyproject.toml and benchmarks/")


def load_manifest(root: Path, manifest_path: str | Path = DEFAULT_MANIFEST) -> Manifest:
    path = Path(manifest_path)
    if not path.is_absolute():
        path = root / path
    data = Manifest(json.loads(path.read_text(encoding="utf-8")))
    data.manifest_parent = path.parent.resolve()
    required = {"schema_version", "id", "languages", "baseline_cases", "tasks"}
    missing = required - data.keys()
    if missing:
        raise ValueError(f"Manifest missing required fields: {sorted(missing)}")
    if not data["languages"] or not data["tasks"]:
        raise ValueError("Manifest must define at least one language and one task")
    task_ids = [task["id"] for task in data["tasks"]]
    if len(task_ids) != len(set(task_ids)):
        raise ValueError("Manifest task IDs must be unique")
    for language, cfg in data["languages"].items():
        for key in ("base", "project_file", "source_file"):
            if key not in cfg:
                raise ValueError(f"Language {language!r} missing {key!r}")
    # Older tasks may omit workspace_checks (or use an empty object). Once a
    # task declares checks, its language/key shape is exact so a malformed
    # sibling cannot hide behind a single-language run.
    from .benchmark_artifacts import checks_for_language

    languages = set(data["languages"])
    first_language = next(iter(languages))
    for task in data["tasks"]:
        checks_for_language(task, first_language, languages)
    return data


def resolve(root: Path, relative: str | Path) -> Path:
    path = Path(relative)
    return path if path.is_absolute() else root / path
