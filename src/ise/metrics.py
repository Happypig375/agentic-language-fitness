from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .process import run_process

EXCLUDED_PARTS = {".git", ".alf", "bin", "obj", "__pycache__"}
SOURCE_SUFFIXES = {".fs", ".fsx", ".cs", ".fsproj", ".csproj", ".json", ".md"}
TOKEN_RE = re.compile(r"[A-Za-z_][A-Za-z_0-9]*|\d+(?:\.\d+)?|[^\s]")


def _included(path: Path) -> bool:
    return not any(part in EXCLUDED_PARTS for part in path.parts) and path.suffix.lower() in SOURCE_SUFFIXES


def snapshot_repository(workspace: Path) -> dict[str, int]:
    files = 0
    bytes_total = 0
    lines = 0
    lexical_tokens = 0
    for path in sorted(workspace.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(workspace)
        if not _included(rel):
            continue
        raw = path.read_bytes()
        files += 1
        bytes_total += len(raw)
        text = raw.decode("utf-8", errors="replace")
        lines += len(text.splitlines())
        lexical_tokens += len(TOKEN_RE.findall(text))
    return {
        "source_files": files,
        "source_bytes": bytes_total,
        "source_lines": lines,
        "approx_lexical_tokens": lexical_tokens,
    }


def git_head(workspace: Path) -> str | None:
    result = run_process(["git", "rev-parse", "HEAD"], cwd=workspace, timeout=30)
    return result.stdout.strip() if result.ok else None


def git_diff_metrics(workspace: Path) -> dict[str, Any]:
    result = run_process(["git", "diff", "--numstat"], cwd=workspace, timeout=30)
    files = additions = deletions = 0
    if result.ok:
        for line in result.stdout.splitlines():
            parts = line.split("\t")
            if len(parts) < 3:
                continue
            files += 1
            if parts[0].isdigit():
                additions += int(parts[0])
            if parts[1].isdigit():
                deletions += int(parts[1])
    patch = run_process(["git", "diff", "--binary"], cwd=workspace, timeout=30)
    return {
        "changed_files": files,
        "added_lines": additions,
        "deleted_lines": deletions,
        "diff_bytes": len(patch.stdout.encode("utf-8")) if patch.ok else None,
    }
