import json
import os
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, call, patch

import alf.benchmark_artifacts as artifacts
from alf.benchmark_artifacts import (
    artifact_plan,
    check_workspace,
    checks_for_language,
    copy_artifacts,
    merge_workspace_checks,
)
from alf.config import Manifest, load_manifest
from alf.evaluator import evaluate_project
from alf.models import ProcessResult


CHECK_KEYS = ("file_exists", "text_contains", "text_not_contains")


def empty_checks():
    return {key: [] for key in CHECK_KEYS}


class BenchmarkArtifactTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.bench = self.root / "benchmarks" / "pilot"
        self.bench.mkdir(parents=True)
        (self.bench / "gold.cs").write_text("gold", encoding="utf-8")
        self.workspace = self.root / "workspace"
        self.workspace.mkdir()
        self.manifest = Manifest(
            {"languages": {"csharp": {"source_file": "Program.cs"}}}
        )
        self.manifest.manifest_parent = self.bench

    def tearDown(self):
        self.tmp.cleanup()

    def task(self, gold):
        return {"gold": {"csharp": gold}}

    def symlink_or_skip(self, link: Path, target: Path, *, directory: bool = False):
        try:
            link.symlink_to(target, target_is_directory=directory)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f"symlink creation unavailable: {exc}")

    def test_legacy_string_and_multifile_copy_store_normalized_parts(self):
        plan = artifact_plan(
            self.root,
            self.manifest,
            "csharp",
            self.task("benchmarks/pilot/gold.cs"),
            self.workspace,
        )
        self.assertEqual(plan[0].source_parts, ("gold.cs",))
        self.assertEqual(plan[0].target_parts, ("Program.cs",))
        copy_artifacts(plan)
        self.assertEqual((self.workspace / "Program.cs").read_text(), "gold")

        (self.bench / "two.cs").write_text("two", encoding="utf-8")
        plan = artifact_plan(
            self.root,
            self.manifest,
            "csharp",
            self.task(
                {
                    "files": [
                        {
                            "source": "benchmarks\\pilot\\gold.cs",
                            "target": "src\\generated/Program.cs",
                        },
                        {
                            "source": "benchmarks/pilot/two.cs",
                            "target": "src/Two.cs",
                        },
                    ]
                }
            ),
            self.workspace,
        )
        self.assertEqual(plan[0].target_parts, ("src", "generated", "Program.cs"))
        copy_artifacts(plan)
        self.assertEqual(
            (self.workspace / "src/generated/Program.cs").read_text(), "gold"
        )
        self.assertEqual((self.workspace / "src/Two.cs").read_text(), "two")

    def test_reject_traversal_duplicates_metadata_and_extra_fields(self):
        invalid = (
            {"files": [{"source": "benchmarks/pilot/gold.cs", "target": "../x"}]},
            {"files": [{"source": "benchmarks/pilot/gold.cs", "target": ".git/x"}]},
            {
                "files": [
                    {"source": "benchmarks/pilot/gold.cs", "target": "A"},
                    {"source": "benchmarks/pilot/gold.cs", "target": "a"},
                ]
            },
            {
                "files": [
                    {
                        "source": "benchmarks/pilot/gold.cs",
                        "target": "x",
                        "unexpected": True,
                    }
                ]
            },
        )
        for gold in invalid:
            with self.subTest(gold=gold), self.assertRaises(ValueError):
                artifact_plan(self.root, self.manifest, "csharp", self.task(gold), self.workspace)

    def test_rejects_absolute_aliases_and_malformed_check_paths(self):
        for target in (
            "/x",
            "C:/x",
            "\\\\server\\share\\x",
            "",
            ".",
            "a/../x",
            "a//x",
        ):
            with self.subTest(target=target), self.assertRaises(ValueError):
                artifact_plan(
                    self.root,
                    self.manifest,
                    "csharp",
                    self.task(
                        {
                            "files": [
                                {
                                    "source": "benchmarks/pilot/gold.cs",
                                    "target": target,
                                }
                            ]
                        }
                    ),
                    self.workspace,
                )
        with self.assertRaises(ValueError):
            merge_workspace_checks(
                self.workspace,
                {
                    "file_exists": "Program.cs",
                    "text_contains": [],
                    "text_not_contains": [],
                },
            )
        for path in ("../x", "C:\\x", ".alf/x", "a//x"):
            checks = empty_checks()
            checks["file_exists"] = [path]
            with self.subTest(path=path), self.assertRaises(ValueError):
                merge_workspace_checks(self.workspace, checks)

    def test_windows_path_aliases_are_rejected_identically_for_every_path_kind(self):
        aliases = [
            "file.cs:stream",
            "CON",
            "con.txt",
            "PRN.json",
            "aux.fs",
            "NUL.cs",
            *(f"COM{index}.txt" for index in range(1, 10)),
            *(f"lpt{index}.json" for index in range(1, 10)),
            "trailing.",
            "trailing ",
        ]
        for alias in aliases:
            with self.subTest(kind="source", alias=alias), self.assertRaises(ValueError):
                artifact_plan(
                    self.root,
                    self.manifest,
                    "csharp",
                    self.task(f"benchmarks/pilot/safe/{alias}/gold.cs"),
                    self.workspace,
                )
            with self.subTest(kind="target", alias=alias), self.assertRaises(ValueError):
                artifact_plan(
                    self.root,
                    self.manifest,
                    "csharp",
                    self.task(
                        {
                            "files": [
                                {
                                    "source": "benchmarks/pilot/gold.cs",
                                    "target": f"safe/{alias}/Program.cs",
                                }
                            ]
                        }
                    ),
                    self.workspace,
                )
            checks = empty_checks()
            checks["file_exists"] = [f"safe/{alias}/Program.cs"]
            with self.subTest(kind="check", alias=alias), self.assertRaises(ValueError):
                merge_workspace_checks(self.workspace, checks)

    def test_workspace_check_schema_is_exact_and_validates_siblings(self):
        languages = {"csharp", "fsharp"}
        self.assertEqual(
            checks_for_language({}, "csharp", languages),
            empty_checks(),
        )
        self.assertEqual(
            checks_for_language({"workspace_checks": {}}, "csharp", languages),
            empty_checks(),
        )
        exact = {language: empty_checks() for language in languages}
        self.assertEqual(
            checks_for_language({"workspace_checks": exact}, "csharp", languages),
            empty_checks(),
        )

        malformed = [
            {"file_exists": [], "text_contains": [], "text_not_contains": []},
            {"csharp": empty_checks()},
            {
                "csharp": empty_checks(),
                "fsharp": {"file_exists": [], "text_contains": []},
            },
            {
                "csharp": empty_checks(),
                "fsharp": {**empty_checks(), "extra": []},
            },
            {
                "csharp": empty_checks(),
                "fsharp": {
                    "file_exists": "Program.fs",
                    "text_contains": [],
                    "text_not_contains": [],
                },
            },
        ]
        for raw in malformed:
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                checks_for_language(
                    {"workspace_checks": raw}, "csharp", languages
                )

    def test_plan_is_all_or_nothing_for_missing_second_source(self):
        task = self.task(
            {
                "files": [
                    {"source": "benchmarks/pilot/gold.cs", "target": "one.cs"},
                    {"source": "benchmarks/pilot/missing.cs", "target": "two.cs"},
                ]
            }
        )
        with self.assertRaises(ValueError):
            artifact_plan(self.root, self.manifest, "csharp", task, self.workspace)
        self.assertFalse((self.workspace / "one.cs").exists())

    def test_rejects_missing_nonregular_and_outside_sources(self):
        outside = self.root / "outside.cs"
        outside.write_text("outside", encoding="utf-8")
        for source in (
            "benchmarks/pilot/missing.cs",
            "benchmarks/pilot",
            "outside.cs",
            "../outside.cs",
            str(outside),
        ):
            with self.subTest(source=source), self.assertRaises(ValueError):
                artifact_plan(
                    self.root, self.manifest, "csharp", self.task(source), self.workspace
                )

    def test_checks_are_serializable_and_conjunctive(self):
        (self.workspace / "Program.cs").write_text(
            "public static class OrderFlowEngine", encoding="utf-8"
        )
        checks = {
            "file_exists": ["Program.cs"],
            "text_contains": [
                {"path": "Program.cs", "text": "OrderFlowEngine"}
            ],
            "text_not_contains": [
                {"path": "Program.cs", "text": "class Customer"}
            ],
        }
        report = check_workspace(self.workspace, checks)
        self.assertTrue(report["ok"])
        self.assertTrue(json.loads(json.dumps(report))["ok"])
        self.assertFalse(
            check_workspace(self.workspace, {"file_exists": ["missing.cs"]})["ok"]
        )
        (self.workspace / "invalid.cs").write_bytes(b"\xff")
        self.assertFalse(
            check_workspace(
                self.workspace,
                {"text_contains": [{"path": "invalid.cs", "text": "x"}]},
            )["ok"]
        )

    def test_initial_symlink_and_parent_symlink_are_rejected(self):
        outside = self.root / "outside"
        outside.mkdir()
        (outside / "gold.cs").write_text("secret", encoding="utf-8")
        source_link = self.bench / "link.cs"
        target_link = self.workspace / "link.cs"
        check_link = self.workspace / "check"
        self.symlink_or_skip(source_link, outside / "gold.cs")
        self.symlink_or_skip(target_link, outside / "target.cs")
        self.symlink_or_skip(check_link, outside, directory=True)
        with self.assertRaises(ValueError):
            artifact_plan(
                self.root,
                self.manifest,
                "csharp",
                self.task("benchmarks/pilot/link.cs"),
                self.workspace,
            )
        with self.assertRaises(ValueError):
            artifact_plan(
                self.root,
                self.manifest,
                "csharp",
                self.task(
                    {
                        "files": [
                            {
                                "source": "benchmarks/pilot/gold.cs",
                                "target": "link.cs",
                            }
                        ]
                    }
                ),
                self.workspace,
            )
        checks = empty_checks()
        checks["file_exists"] = ["check/gold.cs"]
        merge_workspace_checks(self.workspace, checks)
        with self.assertRaises(ValueError):
            check_workspace(self.workspace, checks)

    def test_source_leaf_replaced_after_plan_is_not_read(self):
        plan = artifact_plan(
            self.root,
            self.manifest,
            "csharp",
            self.task("benchmarks/pilot/gold.cs"),
            self.workspace,
        )
        outside = self.root / "outside-secret.cs"
        outside.write_text("outside-secret", encoding="utf-8")
        (self.bench / "gold.cs").unlink()
        self.symlink_or_skip(self.bench / "gold.cs", outside)
        with self.assertRaises(ValueError):
            copy_artifacts(plan)
        self.assertFalse((self.workspace / "Program.cs").exists())

    def test_source_parent_replaced_after_plan_is_not_read(self):
        source_parent = self.bench / "nested"
        source_parent.mkdir()
        (source_parent / "gold.cs").write_text("gold", encoding="utf-8")
        plan = artifact_plan(
            self.root,
            self.manifest,
            "csharp",
            self.task("benchmarks/pilot/nested/gold.cs"),
            self.workspace,
        )
        outside = self.root / "outside-source"
        outside.mkdir()
        (outside / "gold.cs").write_text("outside-secret", encoding="utf-8")
        source_parent.rename(self.bench / "nested-original")
        self.symlink_or_skip(source_parent, outside, directory=True)
        with self.assertRaises(ValueError):
            copy_artifacts(plan)
        self.assertFalse((self.workspace / "Program.cs").exists())

    def test_target_leaf_replaced_after_plan_does_not_write_outside(self):
        outside = self.root / "outside-target.cs"
        outside.write_text("keep", encoding="utf-8")
        plan = artifact_plan(
            self.root,
            self.manifest,
            "csharp",
            self.task("benchmarks/pilot/gold.cs"),
            self.workspace,
        )
        self.symlink_or_skip(self.workspace / "Program.cs", outside)
        with self.assertRaises(ValueError):
            copy_artifacts(plan)
        self.assertEqual(outside.read_text(encoding="utf-8"), "keep")

    def test_target_parent_replaced_after_plan_does_not_write_outside(self):
        target_parent = self.workspace / "generated"
        target_parent.mkdir()
        plan = artifact_plan(
            self.root,
            self.manifest,
            "csharp",
            self.task(
                {
                    "files": [
                        {
                            "source": "benchmarks/pilot/gold.cs",
                            "target": "generated/Program.cs",
                        }
                    ]
                }
            ),
            self.workspace,
        )
        outside = self.root / "outside-target"
        outside.mkdir()
        target_parent.rename(self.workspace / "generated-original")
        self.symlink_or_skip(target_parent, outside, directory=True)
        with self.assertRaises(ValueError):
            copy_artifacts(plan)
        self.assertFalse((outside / "Program.cs").exists())

    def test_check_leaf_and_parent_replaced_after_plan_are_not_read(self):
        checked_parent = self.workspace / "src"
        checked_parent.mkdir()
        checked = checked_parent / "Program.cs"
        checked.write_text("safe", encoding="utf-8")
        checks = empty_checks()
        checks["text_contains"] = [
            {"path": "src/Program.cs", "text": "outside-secret"}
        ]
        normalized = merge_workspace_checks(self.workspace, checks)
        outside = self.root / "outside-check"
        outside.mkdir()
        (outside / "Program.cs").write_text("outside-secret", encoding="utf-8")

        checked.unlink()
        self.symlink_or_skip(checked, outside / "Program.cs")
        with self.assertRaises(ValueError):
            check_workspace(self.workspace, normalized)

        checked.unlink()
        checked.write_text("safe", encoding="utf-8")
        checked_parent.rename(self.workspace / "src-original")
        self.symlink_or_skip(checked_parent, outside, directory=True)
        with self.assertRaises(ValueError):
            check_workspace(self.workspace, normalized)

    def test_win32_backend_unavailable_fails_closed_without_fallback(self):
        checks = empty_checks()
        checks["file_exists"] = ["missing.cs"]
        with (
            patch("alf.benchmark_artifacts._is_windows", return_value=True),
            patch(
                "alf.benchmark_artifacts._get_windows_api",
                side_effect=ValueError("Win32 unavailable"),
            ),
        ):
            with self.assertRaisesRegex(ValueError, "Win32 unavailable"):
                check_workspace(self.workspace, checks)

    def test_mocked_win32_child_rejection_loop_closes_every_opened_handle(self):
        api = Mock()
        api.FILE_FLAG_BACKUP_SEMANTICS = 0x1
        api.FILE_FLAG_OPEN_REPARSE_POINT = 0x2
        api.FILE_READ_ATTRIBUTES = 0x4
        api.FILE_SHARE_READ = 0x8
        api.OPEN_EXISTING = 0x10
        opened = iter(range(1000, 1050))
        api.open.side_effect = lambda *args: next(opened)

        def verify(_api, handle, *, field):
            if handle % 2 == 0:
                return r"\\?\C:\safe-root"
            raise ValueError(f"{field} contains a reparse point")

        with (
            patch("alf.benchmark_artifacts._get_windows_api", return_value=api),
            patch("alf.benchmark_artifacts._win_verify_directory", side_effect=verify),
        ):
            for _ in range(25):
                with self.assertRaises(ValueError):
                    artifacts._win_parent_chain(
                        Path(r"C:\safe-root"),
                        ("reparse", "file.cs"),
                        field="workspace check",
                    )

        expected = []
        for root_handle in range(1000, 1050, 2):
            expected.extend([call(root_handle + 1), call(root_handle)])
        self.assertEqual(api.close.call_args_list, expected)

    def test_mocked_posix_leaf_rejection_loop_closes_leaf_and_root_fds(self):
        opened = iter(range(2000, 2050))

        def open_fd(*args, **kwargs):
            return next(opened)

        def fstat_fd(fd):
            if fd % 2 == 0:
                return SimpleNamespace(st_mode=stat.S_IFDIR, st_nlink=1)
            raise OSError("deterministic leaf fstat rejection")

        close = Mock()
        with (
            patch("alf.benchmark_artifacts._require_posix_primitives", return_value=(0x1000, 0x2000)),
            patch("alf.benchmark_artifacts.os.open", side_effect=open_fd),
            patch("alf.benchmark_artifacts.os.fstat", side_effect=fstat_fd),
            patch("alf.benchmark_artifacts.os.close", close),
        ):
            for _ in range(25):
                with self.assertRaisesRegex(OSError, "leaf fstat rejection"):
                    artifacts._posix_open_regular(
                        Path("/safe-root"),
                        ("file.cs",),
                        field="gold source",
                        allow_missing=False,
                        single_link=False,
                    )

        expected = []
        for root_fd in range(2000, 2050, 2):
            expected.extend([call(root_fd + 1), call(root_fd)])
        self.assertEqual(close.call_args_list, expected)

    def test_mocked_posix_target_verification_failure_closes_leaf_and_parent(self):
        close = Mock()
        with (
            patch("alf.benchmark_artifacts._require_posix_primitives", return_value=(0x1000, 0x2000)),
            patch("alf.benchmark_artifacts._posix_parent_chain", return_value=([3000], 3000)),
            patch("alf.benchmark_artifacts.os.open", return_value=3001),
            patch(
                "alf.benchmark_artifacts.os.fstat",
                return_value=SimpleNamespace(st_mode=stat.S_IFREG, st_nlink=1),
            ),
            patch(
                "alf.benchmark_artifacts.os.ftruncate",
                side_effect=OSError("deterministic truncate rejection"),
            ),
            patch("alf.benchmark_artifacts.os.close", close),
        ):
            with self.assertRaisesRegex(OSError, "truncate rejection"):
                artifacts._posix_open_target(
                    Path("/safe-root"), ("file.cs",), field="gold target"
                )
        self.assertEqual(close.call_args_list, [call(3001), call(3000)])

    def _open_resource_count(self):
        if os.name == "nt":
            import ctypes
            from ctypes import wintypes

            kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
            kernel32.GetCurrentProcess.argtypes = []
            kernel32.GetCurrentProcess.restype = wintypes.HANDLE
            kernel32.GetProcessHandleCount.argtypes = [
                wintypes.HANDLE,
                ctypes.POINTER(wintypes.DWORD),
            ]
            kernel32.GetProcessHandleCount.restype = wintypes.BOOL
            count = wintypes.DWORD()
            if not kernel32.GetProcessHandleCount(
                kernel32.GetCurrentProcess(), ctypes.byref(count)
            ):
                self.skipTest("GetProcessHandleCount unavailable")
            return count.value
        proc_fds = Path("/proc/self/fd")
        if proc_fds.is_dir():
            return len(list(proc_fds.iterdir()))
        self.skipTest("deterministic open-resource counter unavailable")

    def test_real_reparse_rejection_loop_does_not_leak_os_resources(self):
        outside = self.root / "rejection-loop-outside"
        outside.mkdir()
        (outside / "secret.cs").write_text("secret", encoding="utf-8")
        link = self.workspace / "unsafe-parent"
        self.symlink_or_skip(link, outside, directory=True)
        checks = empty_checks()
        checks["file_exists"] = ["unsafe-parent/secret.cs"]
        # Warm up lazy Win32 API initialization before counting.
        with self.assertRaises(ValueError):
            check_workspace(self.workspace, checks)
        before = self._open_resource_count()
        for _ in range(40):
            with self.assertRaises(ValueError):
                check_workspace(self.workspace, checks)
        after = self._open_resource_count()
        self.assertEqual(after, before)

    @unittest.skipUnless(os.name == "nt", "Windows junction test")
    def test_windows_junction_substitution_after_plan_is_rejected(self):
        target_parent = self.workspace / "generated"
        target_parent.mkdir()
        plan = artifact_plan(
            self.root,
            self.manifest,
            "csharp",
            self.task(
                {
                    "files": [
                        {
                            "source": "benchmarks/pilot/gold.cs",
                            "target": "generated/Program.cs",
                        }
                    ]
                }
            ),
            self.workspace,
        )
        outside = self.root / "junction-outside"
        outside.mkdir()
        target_parent.rename(self.workspace / "generated-original")
        created = subprocess.run(
            ["cmd.exe", "/d", "/c", "mklink", "/J", str(target_parent), str(outside)],
            capture_output=True,
            text=True,
            check=False,
        )
        if created.returncode != 0:
            self.skipTest(f"junction creation unavailable: {created.stderr}")
        with self.assertRaises(ValueError):
            copy_artifacts(plan)
        self.assertFalse((outside / "Program.cs").exists())


class Task007WorkspaceContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.repo_root = Path(__file__).resolve().parents[1]
        cls.manifest = load_manifest(cls.repo_root, "benchmarks/successor/manifest.json")
        cls.task = next(
            task for task in cls.manifest["tasks"] if task["id"].startswith("007-")
        )

    def materialize_structural_fixture(self, workspace: Path, checks):
        content_by_path = {}
        for path in checks["file_exists"]:
            content_by_path.setdefault(path, [])
        for item in checks["text_contains"]:
            content_by_path.setdefault(item["path"], []).append(item["text"])
        for path, required in content_by_path.items():
            target = workspace.joinpath(*path.replace("\\", "/").split("/"))
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("\n".join(required), encoding="utf-8")

    def test_manifest_driven_missing_engine_and_delegation_marker_fail(self):
        for language in self.manifest["languages"]:
            checks = checks_for_language(
                self.task, language, set(self.manifest["languages"])
            )
            with self.subTest(language=language), tempfile.TemporaryDirectory() as temp:
                workspace = Path(temp)
                self.materialize_structural_fixture(workspace, checks)
                self.assertTrue(check_workspace(workspace, checks)["ok"])

                engine = workspace / checks["file_exists"][0]
                engine.unlink()
                self.assertFalse(check_workspace(workspace, checks)["ok"])

                self.materialize_structural_fixture(workspace, checks)
                delegation = checks["text_contains"][1]
                program = workspace / delegation["path"]
                program.write_text("line I/O adapter only", encoding="utf-8")
                self.assertFalse(check_workspace(workspace, checks)["ok"])

    def test_manifest_driven_each_forbidden_declaration_and_literal_fails(self):
        for language in self.manifest["languages"]:
            checks = checks_for_language(
                self.task, language, set(self.manifest["languages"])
            )
            for forbidden in checks["text_not_contains"]:
                with (
                    self.subTest(language=language, forbidden=forbidden["text"]),
                    tempfile.TemporaryDirectory() as temp,
                ):
                    workspace = Path(temp)
                    self.materialize_structural_fixture(workspace, checks)
                    target = workspace / forbidden["path"]
                    with target.open("a", encoding="utf-8") as handle:
                        handle.write("\n" + forbidden["text"])
                    report = check_workspace(workspace, checks)
                    self.assertFalse(report["ok"])
                    matching = [
                        item
                        for item in report["text_not_contains"]
                        if item["text"] == forbidden["text"]
                    ]
                    self.assertEqual([item["passed"] for item in matching], [False])

    def test_structurally_passing_dead_delegation_requires_refactor_compliance(self):
        """The textual minimum can pass dead code; blinded review remains required."""
        for language in self.manifest["languages"]:
            checks = checks_for_language(
                self.task, language, set(self.manifest["languages"])
            )
            with self.subTest(language=language), tempfile.TemporaryDirectory() as temp:
                workspace = Path(temp)
                self.materialize_structural_fixture(workspace, checks)
                delegation = checks["text_contains"][1]
                program = workspace / delegation["path"]
                # The marker is deliberately inert. Automated checks cannot
                # establish live dispatch/control flow.
                program.write_text(
                    f"// dead delegation marker: {delegation['text']}", encoding="utf-8"
                )
                report = check_workspace(workspace, checks)
                self.assertTrue(report["ok"])
                requires_separate_refactor_compliance = True
                self.assertTrue(requires_separate_refactor_compliance)


class EvaluatorWorkspaceCheckTests(unittest.TestCase):
    def process(self, returncode):
        return ProcessResult(
            argv=["dotnet"],
            returncode=returncode,
            stdout="",
            stderr="failure" if returncode else "",
            duration_seconds=0.01,
        )

    def test_build_failure_still_serializes_failed_workspace_checks(self):
        with tempfile.TemporaryDirectory() as temp:
            workspace = Path(temp)
            with patch("alf.evaluator.run_process", return_value=self.process(1)):
                result = evaluate_project(
                    workspace,
                    {"project_file": "OrderFlow.csproj"},
                    [],
                    workspace_checks={"file_exists": ["OrderFlowEngine.cs"]},
                )
        self.assertFalse(result["ok"])
        self.assertEqual(result["build"]["returncode"], 1)
        self.assertFalse(result["workspace_checks"]["ok"])

    def test_run_failure_remains_conjunctive_with_passing_workspace_checks(self):
        with tempfile.TemporaryDirectory() as temp:
            workspace = Path(temp)
            (workspace / "OrderFlowEngine.cs").write_text("engine", encoding="utf-8")
            with patch(
                "alf.evaluator.run_process",
                side_effect=[self.process(0), self.process(1)],
            ):
                result = evaluate_project(
                    workspace,
                    {"project_file": "OrderFlow.csproj"},
                    [],
                    workspace_checks={"file_exists": ["OrderFlowEngine.cs"]},
                )
        self.assertFalse(result["ok"])
        self.assertEqual(result["run"]["returncode"], 1)
        self.assertTrue(result["workspace_checks"]["ok"])


if __name__ == "__main__":
    unittest.main()
