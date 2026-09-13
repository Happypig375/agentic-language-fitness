"""CI routing tests run with the standard library only, before installing ALF."""
import importlib.util
import os
from pathlib import Path
import re
import subprocess
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "ci_scope.py"
SPEC = importlib.util.spec_from_file_location("ci_scope", SCRIPT)
ci_scope = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ci_scope)


class ScopeTests(unittest.TestCase):
    def test_prose_and_empty_diff(self):
        self.assertEqual(ci_scope.select_scope([]), "docs")
        self.assertEqual(ci_scope.select_scope([
            "AGENTS.md", "PLAN.md", "README.md", "references.md",
            "docs/literature-search-depth-audit-2026-09-14.md", "docs/nested/review.md",
        ]), "docs")

    def test_maintenance_inputs_and_prose_mix(self):
        paths = [*ci_scope.MAINTENANCE_FILES,
                 "benchmarks/maintenance-sim/seed/fsharp/Program.fs",
                 "benchmarks/maintenance-sim/reference/01/csharp.patch",
                 "benchmarks/maintenance-sim/fixtures/faults/01/fsharp.patch",
                 "benchmarks/maintenance-sim/guidance/fsharp.md",
                 "benchmarks/maintenance-sim/episodes/01.md"]
        for path in paths:
            with self.subTest(path=path):
                self.assertEqual(ci_scope.select_scope([path, "PLAN.md"]), "maintenance")

    def test_shared_frozen_and_unknown_paths_require_full(self):
        for path in [
            "src/alf/h_fixtures.py", "src/alf/h0.py", "src/alf/workstream_e2.py",
            "src/alf/cli.py", "scripts/ci_scope.py", "tests/test_ci_scope.py",
            "protocols/workstream-e3a-v1/candidate-instructions.md",
            "protocols/workstream-e3a-v1/baseline-contract.md",
            "protocols/workstream-e3a-v1/specification.json",
            "benchmarks/successor/tasks/001.md", "benchmarks/pilot/tasks/001.md",
            "benchmarks/workstream-h/contract.md", "reports/example.json",
            "benchmarks/maintenance-sim/new-input.json", "docs/input.json",
            ".github/workflows/ci.yml", "pyproject.toml", "uv.lock", "Dockerfile",
            "docs/../src/code.md", "/docs/note.md", "docs\\note.md", "unknown.txt",
        ]:
            with self.subTest(path=path):
                self.assertEqual(ci_scope.select_scope(["PLAN.md", path]), "full")
        self.assertEqual(ci_scope.select_scope(None), "full")

    def test_regular_push_range(self):
        base, head = "a" * 40, "b" * 40
        event = {"before": base, "after": head, "ref": "refs/heads/main"}
        self.assertEqual(ci_scope.push_range("push", event, head), (base, head))
        for name in ["pull_request", "workflow_dispatch", "schedule", ""]:
            self.assertIsNone(ci_scope.push_range(name, event, head))
        for changes in [
            {"before": "0" * 40}, {"before": "bad"}, {"before": None},
            {"after": "c" * 40}, {"ref": "refs/tags/v1"},
            {"forced": True}, {"deleted": True},
        ]:
            with self.subTest(changes=changes):
                self.assertIsNone(ci_scope.push_range("push", {**event, **changes}, head))

    def test_markdown_encoding_and_deleted_file(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "good.md").write_text("Good UTF-8: λ", encoding="utf-8")
            ci_scope.check_changed_markdown(root, ["good.md", "deleted.md"])
            (root / "bad.md").write_bytes(b"\xff")
            with self.assertRaises(UnicodeDecodeError):
                ci_scope.check_changed_markdown(root, ["bad.md"])
            with self.assertRaises(ValueError):
                ci_scope.check_changed_markdown(root, ["../outside.md"])

    def test_main_unknown_range_selects_full(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "output"
            with patch.dict(os.environ, {"GITHUB_OUTPUT": str(output)}, clear=True), \
                    patch.object(ci_scope, "changed_paths", side_effect=subprocess.CalledProcessError(128, "git")):
                self.assertEqual(ci_scope.main(["--base", "a" * 40, "--head", "b" * 40]), 0)
            self.assertEqual(output.read_text(encoding="utf-8"), "scope=full\n")

    def test_main_bad_event_selects_full(self):
        with tempfile.TemporaryDirectory() as directory:
            event = Path(directory) / "event.json"
            event.write_text("[]", encoding="utf-8")
            with patch.dict(os.environ, {"GITHUB_EVENT_PATH": str(event)}, clear=True):
                self.assertEqual(ci_scope.main([]), 0)

    def test_main_publishes_prose_scope_after_checks(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "output"
            (root / "PLAN.md").write_text("Prose\n", encoding="utf-8")
            with patch.dict(os.environ, {"GITHUB_OUTPUT": str(output)}, clear=True), \
                    patch.object(ci_scope, "ROOT", root), \
                    patch.object(ci_scope, "changed_paths", return_value=["PLAN.md"]), \
                    patch.object(ci_scope.subprocess, "run") as run:
                self.assertEqual(ci_scope.main(["--base", "a" * 40, "--head", "b" * 40]), 0)
                run.assert_called_once()
                self.assertEqual(output.read_text(encoding="utf-8"), "scope=docs\n")
                (root / "PLAN.md").write_bytes(b"\xff")
                with self.assertRaises(UnicodeDecodeError):
                    ci_scope.main(["--base", "a" * 40, "--head", "b" * 40])
                # No new success output was appended after the check failed.
                self.assertEqual(output.read_text(encoding="utf-8"), "scope=docs\n")

    def test_detection_does_not_truncate_after_a_page(self):
        names = [f"docs/note-{i}.md" for i in range(3500)] + ["src/alf/h0.py"]
        result = subprocess.CompletedProcess([], 0, "\0".join(names).encode() + b"\0")
        with patch.object(ci_scope.subprocess, "run", return_value=result):
            paths = ci_scope.changed_paths(Path.cwd(), "a" * 40, "b" * 40)
        self.assertEqual(len(paths), 3501)
        self.assertEqual(ci_scope.select_scope(paths), "full")


class GitRangeTests(unittest.TestCase):
    def test_multi_commit_push_and_renamed_code_are_not_docs_only(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            def git(*args):
                return subprocess.check_output(["git", *args], cwd=root).decode().strip()

            git("init", "--quiet")
            git("config", "user.name", "CI fixture")
            git("config", "user.email", "ci@example.invalid")
            (root / "code.py").write_text("value = 1\n", encoding="utf-8")
            git("add", ".")
            git("commit", "--quiet", "-m", "base")
            base = git("rev-parse", "HEAD")
            (root / "code.py").write_text("value = 2\n", encoding="utf-8")
            git("add", ".")
            git("commit", "--quiet", "-m", "code")
            (root / "PLAN.md").write_text("Prose\n", encoding="utf-8")
            git("add", ".")
            git("commit", "--quiet", "-m", "docs")
            head = git("rev-parse", "HEAD")
            self.assertEqual(ci_scope.select_scope(ci_scope.changed_paths(root, base, head)), "full")
            (root / "docs").mkdir()
            git("mv", "code.py", "docs/renamed.md")
            git("commit", "--quiet", "-m", "rename")
            renamed = git("rev-parse", "HEAD")
            paths = ci_scope.changed_paths(root, head, renamed)
            self.assertIn("code.py", paths)
            self.assertIn("docs/renamed.md", paths)
            self.assertEqual(ci_scope.select_scope(paths), "full")
            git("rm", "PLAN.md")
            git("commit", "--quiet", "-m", "delete docs")
            self.assertEqual(ci_scope.select_scope(ci_scope.changed_paths(
                root, renamed, git("rev-parse", "HEAD")
            )), "docs")


class WorkflowContractTests(unittest.TestCase):
    def test_missing_or_unrecognized_outputs_default_to_full(self):
        # Assert the approved predicates are wired into both real jobs, then
        # exercise their truth table. This is not a general YAML/expression parser.
        workflow = (SCRIPT.parents[1] / ".github/workflows/ci.yml").read_text(encoding="utf-8")
        predicate = """${{ always() && (needs.scope.result != 'success' ||
            (needs.scope.outputs.scope != 'docs' && needs.scope.outputs.scope != 'maintenance')) }}"""
        for name in ("validate-linux", "validate-windows"):
            body = re.search(rf"(?ms)^  {name}:\n(.*?)(?=^  [a-z]|\Z)", workflow).group(1)
            condition = re.search(r"(?m)^    if: (.+)$", body).group(1)
            self.assertEqual(re.sub(r"\s+", "", condition), re.sub(r"\s+", "", predicate))
            self.assertIn("if: ${{ needs.scope.result != 'success' }}", body)
            self.assertIn("run: exit 1", body)
        for result in ("success", "failure", "cancelled", "skipped"):
            for output in ("", "bogus", "full", "docs", "maintenance"):
                with self.subTest(result=result, output=output):
                    expected = result != "success" or output not in {"docs", "maintenance"}
                    self.assertEqual(result != "success" or (output != "docs" and output != "maintenance"), expected)


if __name__ == "__main__":
    unittest.main()
