"""Select bounded CI for ordinary pushes; uncertain changes use the full suite."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PROSE_FILES = frozenset({"README.md", "AGENTS.md", "PLAN.md", "references.md"})
MAINTENANCE_FILES = frozenset({
    "src/alf/maintenance.py",
    "scripts/maintenance_check.py",
    "tests/test_maintenance.py",
    "benchmarks/maintenance-sim/construction.json",
    "benchmarks/maintenance-sim/contract.md",
    "benchmarks/maintenance-sim/fixtures/cases.json",
    "benchmarks/maintenance-sim/fixtures/faults.json",
})
SHA = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})\Z")


def select_scope(paths: list[str] | None) -> str:
    """Only the inspected prose and isolated maintenance paths may skip suites."""
    if paths is None:
        return "full"
    scope = "docs"
    for path in paths:
        parts = PurePosixPath(path).parts
        if not parts or path.startswith("/") or ".." in parts or "\\" in path:
            return "full"
        if path in PROSE_FILES or (path.startswith("docs/") and path.endswith(".md")):
            continue
        maintenance = path in MAINTENANCE_FILES or path.startswith(
            "benchmarks/maintenance-sim/seed/"
        ) or (
            path.startswith(("benchmarks/maintenance-sim/reference/",
                             "benchmarks/maintenance-sim/fixtures/faults/"))
            and path.endswith(".patch")
        ) or (
            path.startswith(("benchmarks/maintenance-sim/guidance/",
                             "benchmarks/maintenance-sim/episodes/"))
            and path.endswith(".md")
        )
        if not maintenance:
            return "full"
        scope = "maintenance"
    return scope


def push_range(event_name: str, event: dict, head: str) -> tuple[str, str] | None:
    """PRs/manual/tag/new-branch/forced pushes deliberately retain full CI."""
    before = event.get("before", "")
    if (event_name != "push" or event.get("forced") or event.get("deleted")
            or not str(event.get("ref", "")).startswith("refs/heads/")
            or not isinstance(before, str) or not SHA.fullmatch(before)
            or set(before) == {"0"} or not SHA.fullmatch(head)
            or event.get("after") != head):
        return None
    return before, head


def changed_paths(root: Path, base: str, head: str) -> list[str]:
    if not SHA.fullmatch(base) or not SHA.fullmatch(head):
        raise ValueError("Expected complete commit identities")
    result = subprocess.run(
        ["git", "diff", "--name-only", "--no-renames", "-z", base, head, "--"],
        cwd=root, check=True, capture_output=True,
    )
    # No API page limit; rename sources/deletions remain visible to classification.
    return [path.decode("utf-8") for path in result.stdout.split(b"\0") if path]


def check_changed_markdown(root: Path, paths: list[str]) -> None:
    """Check encoding only, not links, claims, frozen bytes or Markdown rendering."""
    root = root.resolve()
    for path in paths:
        if not path.endswith(".md"):
            continue
        source = root / path
        if source.is_symlink() or not source.resolve().is_relative_to(root):
            raise ValueError(f"Markdown path is not an in-repository regular file: {path}")
        if source.exists():  # A deleted path still influenced scope selection.
            source.read_text(encoding="utf-8", errors="strict")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", help="Local reproduction: full base commit SHA")
    parser.add_argument("--head", help="Local reproduction: full head commit SHA")
    args = parser.parse_args(argv)
    if bool(args.base) != bool(args.head):
        parser.error("--base and --head must be supplied together")
    paths = None
    comparison = None
    try:
        if args.base:
            comparison = args.base, args.head
        else:
            event_path = os.environ.get("GITHUB_EVENT_PATH")
            event = json.loads(Path(event_path).read_text(encoding="utf-8")) if event_path else {}
            if not isinstance(event, dict):
                raise ValueError("Expected event object")
            comparison = push_range(
                os.environ.get("GITHUB_EVENT_NAME", ""), event,
                os.environ.get("GITHUB_SHA", ""),
            )
        if comparison:
            paths = changed_paths(ROOT, *comparison)
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"Change detection unavailable ({type(error).__name__}); selecting full CI.")
    scope = select_scope(paths)
    if paths is not None:
        check_changed_markdown(ROOT, paths)
        subprocess.run(["git", "diff", "--check", *comparison, "--"], cwd=ROOT, check=True)
    print(json.dumps({"scope": scope, "comparison": comparison,
                      "changed_paths": len(paths) if paths is not None else None}))
    output = os.environ.get("GITHUB_OUTPUT")
    if output:
        with Path(output).open("a", encoding="utf-8") as stream:
            stream.write(f"scope={scope}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
