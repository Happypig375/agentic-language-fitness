from __future__ import annotations

from collections import Counter
import copy
import importlib.metadata
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from alf.config import load_manifest
from alf.protocol import canonical_json_hash
import alf.workstream_e2 as e2
import alf.workstream_e2_report as e2_report
import alf.workstream_e2_runner as e2_runner


class _CharacterEncoding:
    name = e2.TOKENIZER_ENCODING

    @staticmethod
    def encode(text: str) -> list[str]:
        return list(text)


class WorkstreamE2DefinitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).parents[1].resolve()
        cls.artifacts = cls.root / ".artifacts"
        cls.artifacts.mkdir(exist_ok=True)
        cls.definition = e2._build_definition(cls.root, "benchmarks/successor/manifest.json")

    def _definition_path(self, directory: str | Path, value: dict | None = None) -> Path:
        path = Path(directory) / "definition.json"
        e2._atomic_json(path, value or self.definition)
        return path

    def test_schedule_is_five_deterministic_adjacent_paired_rounds(self) -> None:
        rows = e2.build_schedule()
        self.assertEqual(rows, self.definition["schedule"])
        self.assertEqual(len(rows), 90)
        self.assertEqual(
            Counter((row["language"], row["stage"]) for row in rows),
            Counter({(language, stage): 5 for language in e2.LANGUAGES for stage in range(9)}),
        )
        for round_number in range(1, 6):
            part = [row for row in rows if row["round"] == round_number]
            self.assertEqual(len(part), 18)
            for offset in range(0, 18, 2):
                self.assertEqual(part[offset]["stage"], part[offset + 1]["stage"])
                self.assertEqual({part[offset]["language"], part[offset + 1]["language"]}, set(e2.LANGUAGES))
                self.assertEqual([part[offset]["language_position"], part[offset + 1]["language_position"]], [1, 2])
        for stage in range(9):
            first = Counter(
                row["language"] for row in rows if row["stage"] == stage and row["language_position"] == 1
            )
            self.assertEqual(sorted(first.values()), [2, 3])
        self.assertEqual(e2._schedule_errors(rows), [])

    def test_definition_is_deterministic_and_contains_exact_command_contract(self) -> None:
        again = e2._build_definition(self.root, "benchmarks/successor/manifest.json")
        self.assertEqual(self.definition, again)
        self.assertEqual(self.definition["commands"]["templates"], e2.COMMAND_TEMPLATES)
        self.assertEqual(
            self.definition["commands"]["expanded_by_language"]["fsharp"]["build"],
            [
                "dotnet",
                "build",
                "OrderFlow.fsproj",
                "--configuration",
                "Release",
                "--no-incremental",
                "--no-restore",
                "--nologo",
            ],
        )

    def test_states_capture_compile_order_source_discovery_and_full_stage_diff(self) -> None:
        states = {(row["language"], row["stage"]): row for row in self.definition["states"]}
        self.assertEqual(len(states), 18)
        fsharp = states[("fsharp", 7)]
        csharp = states[("csharp", 7)]
        self.assertEqual(
            fsharp["compile_obligations"]["static_source_inputs"],
            ["OrderFlowEngine.fs", "Program.fs"],
        )
        self.assertEqual(fsharp["compile_obligations"]["mode"], "explicit-project-order")
        self.assertEqual(
            csharp["compile_obligations"]["static_source_inputs"],
            ["OrderFlowEngine.cs", "Program.cs"],
        )
        self.assertEqual(csharp["compile_obligations"]["mode"], "sdk-default-source-discovery")
        self.assertEqual(fsharp["stage_local_diff"]["added_paths"], ["OrderFlowEngine.fs"])
        self.assertIn("OrderFlow.fsproj", fsharp["stage_local_diff"]["modified_paths"])
        self.assertGreater(fsharp["stage_local_diff"]["added_lines"], 0)
        self.assertGreater(fsharp["stage_local_diff"]["diff_bytes"], 0)
        self.assertEqual(fsharp["metrics"]["source_files"], 2)
        self.assertEqual(fsharp["cumulative_task_obligations"][-1]["project_file_changed"], True)
        self.assertEqual(csharp["cumulative_task_obligations"][-1]["project_file_changed"], False)

    def test_stage_eight_retains_stage_seven_workspace_checks(self) -> None:
        states = {(row["language"], row["stage"]): row for row in self.definition["states"]}
        for language in e2.LANGUAGES:
            at_seven = states[(language, 7)]["workspace_checks"]["counts"]
            at_eight = states[(language, 8)]["workspace_checks"]["counts"]
            self.assertEqual(at_eight["file_exists"], at_seven["file_exists"])
            self.assertEqual(at_eight["text_contains"], at_seven["text_contains"])
            self.assertGreater(at_eight["text_not_contains"], at_seven["text_not_contains"])

    def test_definition_excludes_case_prompt_and_source_text(self) -> None:
        serialized = json.dumps(self.definition, sort_keys=True)
        for forbidden in ("ready filters pending and sorts", "late-low", "module OrderFlowEngine", "Request was null"):
            self.assertNotIn(forbidden, serialized)

    def test_lf_normalization_makes_snapshot_cross_platform(self) -> None:
        with tempfile.TemporaryDirectory() as left, tempfile.TemporaryDirectory() as right:
            left_path = Path(left)
            right_path = Path(right)
            (left_path / "Program.cs").write_bytes(b"line1\nline2\n")
            (right_path / "Program.cs").write_bytes(b"line1\r\nline2\r\n")
            (left_path / "App.csproj").write_bytes(b"<Project />\n")
            (right_path / "App.csproj").write_bytes(b"<Project />\r\n")
            self.assertEqual(e2._snapshot(left_path, _CharacterEncoding())[0], e2._snapshot(right_path, _CharacterEncoding())[0])

    def test_exact_tokenizer_version_is_required(self) -> None:
        with patch("alf.workstream_e2.importlib.metadata.version", return_value="0.13.0"):
            with self.assertRaisesRegex(ValueError, "exactly 0.14.0"):
                e2._get_encoding()
        with patch(
            "alf.workstream_e2.importlib.metadata.version",
            side_effect=importlib.metadata.PackageNotFoundError("tiktoken"),
        ):
            with self.assertRaisesRegex(ValueError, "tiktoken==0.14.0"):
                e2._get_encoding()

    def test_freeze_check_is_atomic_side_effect_free_and_rejects_tampering(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.artifacts) as directory:
            path = Path(directory) / "definition.json"
            frozen = e2.freeze_definition(self.root, "benchmarks/successor/manifest.json", path)
            self.assertEqual(frozen, self.definition)
            with patch("alf.workstream_e2_runner._invoke", side_effect=AssertionError("subprocess forbidden")):
                self.assertTrue(e2.check_definition(self.root, path, "benchmarks/successor/manifest.json")["ok"])
            mutations = {
                "schema": lambda value: value.__setitem__("schema_version", "changed"),
                "seed": lambda value: value.__setitem__("schedule_seed", "changed"),
                "tokenizer": lambda value: value["tokenizer"].__setitem__("encoding", "changed"),
                "contract": lambda value: value["execution_contract"].__setitem__("rounds", 6),
                "state": lambda value: value["states"][0].__setitem__("case_count", 999),
            }
            with patch("alf.workstream_e2._build_definition", return_value=frozen):
                for name, mutate in mutations.items():
                    with self.subTest(name=name):
                        changed = copy.deepcopy(frozen)
                        mutate(changed)
                        changed.pop("definition_sha256")
                        changed["definition_sha256"] = canonical_json_hash(changed)
                        e2._atomic_json(path, changed)
                        result = e2.check_definition(self.root, path, "benchmarks/successor/manifest.json")
                        self.assertFalse(result["ok"])
                        self.assertIn("definition differs from canonical recomputation", result["errors"])

    def test_freeze_refuses_output_outside_repository(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "inside the repository"):
                e2.freeze_definition(
                    self.root,
                    "benchmarks/successor/manifest.json",
                    Path(directory) / "definition.json",
                )

    def test_schedule_validator_rejects_nonadjacent_or_duplicate_entries(self) -> None:
        changed = copy.deepcopy(e2.build_schedule())
        changed[1]["stage"] = (changed[1]["stage"] + 1) % 9
        self.assertTrue(e2._schedule_errors(changed))
        changed = copy.deepcopy(e2.build_schedule())
        changed[1]["language"] = changed[0]["language"]
        self.assertTrue(e2._schedule_errors(changed))
        changed = copy.deepcopy(e2.build_schedule())
        changed[0]["stage"] = []
        self.assertTrue(e2._schedule_errors(changed))


class WorkstreamE2RunnerPrimitiveTests(unittest.TestCase):
    def test_warning_summary_ignores_build_footers_but_keeps_diagnostics(self) -> None:
        summary = e2_runner._warning_summary(
            b"warning CS1234: first\n  0 Warning(s)\n  2 Warning(s)\n",
            b"warning: uncoded\nwarning FS5678: second\n",
        )
        self.assertEqual(summary["count"], 3)
        self.assertEqual(summary["codes"], {"CS1234": 1, "FS5678": 1, "UNSPECIFIED": 1})
        self.assertEqual(len(summary["line_sha256"]), 3)

    def test_fresh_workspace_rejects_bin_and_obj(self) -> None:
        for name in ("bin", "obj", "BIN"):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                (Path(directory) / name).mkdir()
                with self.assertRaises(e2.E2RunError):
                    e2._assert_no_build_directories(Path(directory))

    def test_regime_uses_exact_fresh_and_repeat_sequences(self) -> None:
        cases = [{"input": {"x": 1}, "expected": {"ok": True}}]
        checks = {key: [] for key in e2.CHECK_KEYS}
        calls: list[tuple[str, list[str]]] = []

        def execute(operation: str, argv: list[str], **_: object):
            calls.append((operation, argv))
            stdout = b'{"ok":true}\n' if operation == "run" else b""
            return {"operation": operation}, stdout, b""

        with tempfile.TemporaryDirectory() as directory, patch("alf.workstream_e2_runner._execute_command", side_effect=execute), patch(
            "alf.workstream_e2_runner._host_load", return_value={"load": 0}
        ):
            workspace = Path(directory)
            fresh = e2_runner._run_regime(
                workspace=workspace,
                config={"project_file": "OrderFlow.csproj"},
                cases=cases,
                checks=checks,
                fresh=True,
                env={},
                raw=workspace / "raw",
                raw_prefix="fresh",
                timeout=300,
            )
            repeat = e2_runner._run_regime(
                workspace=workspace,
                config={"project_file": "OrderFlow.csproj"},
                cases=cases,
                checks=checks,
                fresh=False,
                env={},
                raw=workspace / "raw",
                raw_prefix="repeat",
                timeout=300,
            )
        self.assertEqual([name for name, _ in calls], ["restore", "build", "run", "build", "run"])
        self.assertEqual([row["operation"] for row in fresh["operations"]], ["restore", "build", "run"])
        self.assertEqual([row["operation"] for row in repeat["operations"]], ["build", "run"])
        self.assertEqual(calls[0][1], ["dotnet", "restore", "OrderFlow.csproj", "--nologo"])
        self.assertEqual(calls[1][1], e2_runner._expanded_commands({"project_file": "OrderFlow.csproj"})["build"])

    def test_restore_failure_aborts_before_build_without_retry(self) -> None:
        calls: list[str] = []

        def fail(operation: str, *_: object, **__: object):
            calls.append(operation)
            raise e2.E2RunError("restore_failed")

        with tempfile.TemporaryDirectory() as directory, patch("alf.workstream_e2_runner._execute_command", side_effect=fail):
            with self.assertRaisesRegex(e2.E2RunError, "restore_failed"):
                e2_runner._run_regime(
                    workspace=Path(directory),
                    config={"project_file": "OrderFlow.csproj"},
                    cases=[],
                    checks={key: [] for key in e2.CHECK_KEYS},
                    fresh=True,
                    env={},
                    raw=Path(directory) / "raw",
                    raw_prefix="failed",
                    timeout=300,
                )
        self.assertEqual(calls, ["restore"])

    def test_command_writes_raw_bytes_warning_metadata_and_times_out(self) -> None:
        success = subprocess.CompletedProcess(
            ["dotnet", "build"],
            0,
            stdout=b"warning CS1234: synthetic\n",
            stderr=b"detail\n",
        )
        with tempfile.TemporaryDirectory() as directory, patch("alf.workstream_e2_runner._invoke", return_value=success):
            raw = Path(directory)
            record, stdout, stderr = e2_runner._execute_command(
                "build",
                ["dotnet", "build"],
                cwd=raw,
                input_bytes=None,
                env={},
                raw=raw,
                raw_stem="sample/build",
                timeout=1,
            )
            self.assertEqual(stdout, success.stdout)
            self.assertEqual(stderr, success.stderr)
            self.assertEqual(record["warnings"]["codes"], {"CS1234": 1})
            self.assertEqual((raw / record["stdout"]["path"]).read_bytes(), success.stdout)
            self.assertTrue((raw / record["metadata_path"]).is_file())

        timeout = subprocess.TimeoutExpired(["dotnet", "build"], 1, output=b"partial", stderr=b"late")
        with tempfile.TemporaryDirectory() as directory, patch("alf.workstream_e2_runner._invoke", side_effect=timeout):
            raw = Path(directory)
            with self.assertRaisesRegex(e2.E2RunError, "build_timeout"):
                e2_runner._execute_command(
                    "build",
                    ["dotnet", "build"],
                    cwd=raw,
                    input_bytes=None,
                    env={},
                    raw=raw,
                    raw_stem="sample/build",
                    timeout=1,
                )
            self.assertEqual((raw / "sample/build.stdout.bin").read_bytes(), b"partial")
            metadata = json.loads((raw / "sample/build.json").read_text(encoding="utf-8"))
            self.assertTrue(metadata["timed_out"])

    def test_evaluator_fails_closed_on_count_json_value_and_workspace_checks(self) -> None:
        cases = [{"input": 1, "expected": {"ok": True}}]
        empty = {key: [] for key in e2.CHECK_KEYS}
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            for output, code in (
                (b"", "count"),
                (b"not-json\n", "invalid_json"),
                (b'{"ok":false}\n', "case_mismatch"),
            ):
                with self.subTest(code=code), self.assertRaises(e2.E2RunError):
                    e2_runner._evaluate_output(output, cases, workspace, empty)
            bad_checks = {**empty, "file_exists": ["missing.txt"]}
            with self.assertRaisesRegex(e2.E2RunError, "workspace_check_failed"):
                e2_runner._evaluate_output(b'{"ok":true}\n', cases, workspace, bad_checks)

    def test_publish_report_removes_partial_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            json_path = Path(directory) / "report.json"
            markdown_path = Path(directory) / "report.md"
            report = {"synthetic": True}
            with patch("alf.workstream_e2_report.markdown_report", return_value="# synthetic\n"), patch(
                "alf.workstream_e2_report._atomic_json", side_effect=OSError("synthetic")
            ):
                with self.assertRaises(OSError):
                    e2_report.publish_report(report, json_path, markdown_path)
            self.assertFalse(json_path.exists())
            self.assertFalse(markdown_path.exists())


class WorkstreamE2RunTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).parents[1].resolve()
        cls.artifacts = cls.root / ".artifacts"
        cls.artifacts.mkdir(exist_ok=True)
        cls.definition = e2._build_definition(cls.root, "benchmarks/successor/manifest.json")
        cls.manifest = load_manifest(cls.root, "benchmarks/successor/manifest.json")

    @staticmethod
    def _fast_atomic(path: Path, data: bytes) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

    def _definition_file(self, directory: str | Path) -> Path:
        path = Path(directory) / "definition.json"
        e2._atomic_json(path, self.definition)
        return path

    def _fake_invoke(self, calls: list[dict[str, object]]):
        all_cases = list(self.manifest["baseline_cases"]) + [
            case for task in self.manifest["tasks"] for case in task["cases"]
        ]

        def invoke(argv: list[str], *, cwd: Path, input_bytes: bytes | None, env: dict[str, str], timeout: int):
            calls.append({"argv": list(argv), "env": dict(env), "timeout": timeout})
            if argv == ["dotnet", "--version"]:
                return subprocess.CompletedProcess(argv, 0, b"10.0.302\n", b"")
            if argv[1] == "build":
                artifact = cwd / "bin" / "Release" / "net10.0" / "OrderFlow.dll"
                artifact.parent.mkdir(parents=True, exist_ok=True)
                artifact.write_bytes(b"synthetic-artifact")
                warning = b"warning CS1234: synthetic\n" if argv[2].endswith(".csproj") else b"warning FS1234: synthetic\n"
                return subprocess.CompletedProcess(argv, 0, b"build ok\n", warning)
            if argv[1] == "restore":
                return subprocess.CompletedProcess(argv, 0, b"restore ok\n", b"")
            if argv[1] == "run":
                outputs = []
                for line in (input_bytes or b"").decode("utf-8").splitlines():
                    case_input = json.loads(line)
                    match = next(case for case in all_cases if case["input"] == case_input)
                    outputs.append(json.dumps(match["expected"], separators=(",", ":")))
                return subprocess.CompletedProcess(argv, 0, ("\n".join(outputs) + "\n").encode("utf-8"), b"")
            raise AssertionError(argv)

        return invoke

    def test_full_mocked_run_executes_18_preflights_and_90_samples(self) -> None:
        calls: list[dict[str, object]] = []
        network = {
            "ok": True,
            "interfaces": ["lo"],
            "ipv4_usable_default_routes": 0,
            "ipv6_usable_default_routes": 0,
            "reason": None,
        }
        load = {
            "cpu_count": 4,
            "load_1m": 0.0,
            "load_5m": 0.0,
            "load_15m": 0.0,
            "memory_total_kib": 1000,
            "memory_available_kib": 900,
        }
        with tempfile.TemporaryDirectory(dir=self.artifacts) as definition_dir, tempfile.TemporaryDirectory() as external:
            definition_path = self._definition_file(definition_dir)
            base = Path(external)
            cache = base / "cache"
            cache.mkdir()
            raw = base / "raw"
            report_json = base / "report.json"
            report_md = base / "report.md"
            with patch("alf.workstream_e2_runner._network_snapshot", return_value=network), patch(
                "alf.workstream_e2_runner._host_load", return_value=load
            ), patch("alf.workstream_e2_runner.shutil.which", return_value="dotnet"), patch(
                "alf.workstream_e2_runner._invoke", side_effect=self._fake_invoke(calls)
            ), patch("alf.workstream_e2_runner._atomic_bytes", side_effect=self._fast_atomic), patch(
                "alf.workstream_e2_report._atomic_bytes", side_effect=self._fast_atomic
            ), patch("alf.workstream_e2._atomic_bytes", side_effect=self._fast_atomic):
                report = e2_runner.run_baseline(
                    root=self.root,
                    definition=definition_path,
                    manifest="benchmarks/successor/manifest.json",
                    runner_git_sha="a" * 40,
                    container_image_id="sha256:" + "b" * 64,
                    package_cache=cache,
                    raw_output=raw,
                    output_json=report_json,
                    output_markdown=report_md,
                )

            self.assertEqual(len(calls), 1 + 90 * 5)
            self.assertEqual(len(report["samples"]), 90)
            self.assertTrue(report["package_cache"]["unchanged"])
            self.assertEqual(len(report["distributions"]["operations"]), 90)
            self.assertTrue(e2_report.validate_report(report, self.definition)["ok"])
            self.assertTrue(e2_report.audit_report(report, self.definition, raw)["ok"])
            self.assertEqual(json.loads(report_json.read_text(encoding="utf-8")), report)
            self.assertTrue(report_md.is_file())
            terminal = json.loads((raw / "terminal-attempt.json").read_text(encoding="utf-8"))
            unsigned = dict(terminal)
            claimed = unsigned.pop("attempt_sha256")
            self.assertEqual(claimed, canonical_json_hash(unsigned))
            self.assertEqual(terminal["status"], "success")
            self.assertEqual(terminal["completed_preflight_states"], 18)
            self.assertEqual(terminal["completed_samples"], 90)
            self.assertTrue((raw / "raw-inventory.json").is_file())
            self.assertTrue((raw / "preflight/states.json").is_file())
            self.assertTrue((raw / report["samples"][0]["fresh"]["operations"][0]["stdout"]["path"]).is_file())
            allowed_env = {
                "PATH",
                "HOME",
                "TMPDIR",
                "DOTNET_CLI_HOME",
                "DOTNET_CLI_TELEMETRY_OPTOUT",
                "DOTNET_NOLOGO",
                "DOTNET_SKIP_FIRST_TIME_EXPERIENCE",
                "DOTNET_MULTILEVEL_LOOKUP",
                "NUGET_PACKAGES",
                "NUGET_HTTP_CACHE_PATH",
                "NUGET_XMLDOC_MODE",
                "TIKTOKEN_CACHE_DIR",
                "LANG",
                "LC_ALL",
                "TZ",
            }
            self.assertTrue(all(set(call["env"]) == allowed_env for call in calls))
            self.assertTrue(all("HTTP_PROXY" not in call["env"] for call in calls))

            tampered = copy.deepcopy(report)
            tampered["samples"][0]["input"] = "secret"
            tampered.pop("report_sha256")
            tampered["report_sha256"] = canonical_json_hash(tampered)
            result = e2_report.validate_report(tampered, self.definition)
            self.assertFalse(result["ok"])
            self.assertTrue(any("forbidden publishable field" in error for error in result["errors"]))

            tampered = copy.deepcopy(report)
            tampered["runner_git_sha"] = "/private/path"
            tampered.pop("report_sha256")
            tampered["report_sha256"] = canonical_json_hash(tampered)
            self.assertFalse(e2_report.validate_report(tampered, self.definition)["ok"])

            tampered = copy.deepcopy(report)
            tampered["samples"][0]["fresh"]["operations"][0]["metadata_path"] = "../outside.json"
            tampered.pop("report_sha256")
            tampered["report_sha256"] = canonical_json_hash(tampered)
            self.assertFalse(e2_report.validate_report(tampered, self.definition)["ok"])

            tampered = copy.deepcopy(report)
            tampered["samples"][0]["fresh"]["evaluator"]["case_count"] = 0
            tampered["samples"][0]["fresh"]["evaluator"]["passed_case_count"] = 0
            tampered.pop("report_sha256")
            tampered["report_sha256"] = canonical_json_hash(tampered)
            self.assertFalse(e2_report.validate_report(tampered, self.definition)["ok"])

            stream_path = raw / report["samples"][0]["fresh"]["operations"][0]["stdout"]["path"]
            stream_path.write_bytes(b"tampered")
            self.assertFalse(e2_report.audit_report(report, self.definition, raw)["ok"])

    def test_network_failure_writes_terminal_attempt_and_no_report_or_process(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.artifacts) as definition_dir, tempfile.TemporaryDirectory() as external:
            definition_path = self._definition_file(definition_dir)
            base = Path(external)
            cache = base / "cache"
            cache.mkdir()
            raw = base / "raw"
            report_json = base / "report.json"
            report_md = base / "report.md"
            with patch(
                "alf.workstream_e2_runner._network_snapshot",
                return_value={"ok": False, "interfaces": ["lo", "eth0"], "reason": "synthetic"},
            ), patch("alf.workstream_e2_runner._invoke", side_effect=AssertionError("must not run")):
                with self.assertRaisesRegex(e2.E2RunError, "network_isolation_proof_failed"):
                    e2_runner.run_baseline(
                        root=self.root,
                        definition=definition_path,
                        manifest="benchmarks/successor/manifest.json",
                        runner_git_sha="a" * 40,
                        container_image_id="sha256:" + "b" * 64,
                        package_cache=cache,
                        raw_output=raw,
                        output_json=report_json,
                        output_markdown=report_md,
                    )
            terminal = json.loads((raw / "terminal-attempt.json").read_text(encoding="utf-8"))
            self.assertEqual(terminal["status"], "failure")
            self.assertEqual(terminal["failure"]["code"], "network_isolation_proof_failed")
            self.assertFalse(report_json.exists())
            self.assertFalse(report_md.exists())

    def test_package_cache_change_aborts_after_sdk_without_retry(self) -> None:
        calls = 0

        def mutate(argv: list[str], *, env: dict[str, str], **_: object):
            nonlocal calls
            calls += 1
            (Path(env["NUGET_PACKAGES"]) / "changed").write_text("x", encoding="utf-8")
            return subprocess.CompletedProcess(argv, 0, b"10.0.302\n", b"")

        network = {
            "ok": True,
            "interfaces": ["lo"],
            "ipv4_usable_default_routes": 0,
            "ipv6_usable_default_routes": 0,
            "reason": None,
        }
        with tempfile.TemporaryDirectory(dir=self.artifacts) as definition_dir, tempfile.TemporaryDirectory() as external:
            definition_path = self._definition_file(definition_dir)
            base = Path(external)
            cache = base / "cache"
            cache.mkdir()
            raw = base / "raw"
            with patch("alf.workstream_e2_runner._network_snapshot", return_value=network), patch(
                "alf.workstream_e2_runner.shutil.which", return_value="dotnet"
            ), patch("alf.workstream_e2_runner._invoke", side_effect=mutate):
                with self.assertRaisesRegex(e2.E2RunError, "package_cache_changed"):
                    e2_runner.run_baseline(
                        root=self.root,
                        definition=definition_path,
                        manifest="benchmarks/successor/manifest.json",
                        runner_git_sha="a" * 40,
                        container_image_id="sha256:" + "b" * 64,
                        package_cache=cache,
                        raw_output=raw,
                        output_json=base / "report.json",
                        output_markdown=base / "report.md",
                    )
            self.assertEqual(calls, 1)
            terminal = json.loads((raw / "terminal-attempt.json").read_text(encoding="utf-8"))
            self.assertEqual(terminal["failure"]["code"], "package_cache_changed")

    def test_terminal_attempt_persistence_failure_is_not_silently_swallowed(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.artifacts) as definition_dir, tempfile.TemporaryDirectory() as external:
            definition_path = self._definition_file(definition_dir)
            base = Path(external)
            cache = base / "cache"
            cache.mkdir()
            with patch(
                "alf.workstream_e2_runner._network_snapshot",
                return_value={"ok": False, "interfaces": ["eth0"], "reason": "synthetic"},
            ), patch("alf.workstream_e2_runner.write_raw_inventory", side_effect=OSError("disk full")):
                with self.assertRaisesRegex(
                    e2.E2RunError,
                    "network_isolation_proof_failed_and_terminal_attempt_persistence_failed",
                ):
                    e2_runner.run_baseline(
                        root=self.root,
                        definition=definition_path,
                        manifest="benchmarks/successor/manifest.json",
                        runner_git_sha="a" * 40,
                        container_image_id="sha256:" + "b" * 64,
                        package_cache=cache,
                        raw_output=base / "raw",
                        output_json=base / "report.json",
                        output_markdown=base / "report.md",
                    )

    def test_run_refuses_raw_or_cache_inside_repository(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.artifacts) as definition_dir:
            definition_path = self._definition_file(definition_dir)
            with self.assertRaisesRegex(ValueError, "raw output"):
                e2_runner.run_baseline(
                    root=self.root,
                    definition=definition_path,
                    manifest="benchmarks/successor/manifest.json",
                    runner_git_sha="a" * 40,
                    container_image_id="sha256:" + "b" * 64,
                    package_cache=self.artifacts,
                    raw_output=self.artifacts / "raw",
                    output_json=self.artifacts / "report.json",
                    output_markdown=self.artifacts / "report.md",
                )


if __name__ == "__main__":
    unittest.main()
