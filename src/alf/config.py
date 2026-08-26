from __future__ import annotations

import json
from pathlib import Path
from typing import Any


DEFAULT_MANIFEST = Path("benchmarks/pilot/manifest.json")


def find_repo_root(start: Path | None = None) -> Path:
    current = (start or Path.cwd()).resolve()
    for candidate in (current, *current.parents):
        if (candidate / "pyproject.toml").is_file() and (candidate / "benchmarks").is_dir():
            return candidate
    raise FileNotFoundError("Could not find repository root containing pyproject.toml and benchmarks/")


def load_manifest(root: Path, manifest_path: str | Path = DEFAULT_MANIFEST) -> dict[str, Any]:
    path = Path(manifest_path)
    if not path.is_absolute():
        path = root / path
    data = json.loads(path.read_text(encoding="utf-8"))
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
    return data


def resolve(root: Path, relative: str | Path) -> Path:
    path = Path(relative)
    return path if path.is_absolute() else root / path
