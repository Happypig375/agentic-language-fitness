import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from alf import maintenance
from scripts import maintenance_check


class MaintenanceTests(unittest.TestCase):
    def _write_cases(self, root, text):
        path = root / "benchmarks/maintenance-sim/fixtures/cases.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")

    def test_strict_json_equality_distinguishes_bool_and_int_recursively(self):
        self.assertFalse(maintenance._strict_json_equal({"x": True}, {"x": 1}))
        self.assertFalse(maintenance._strict_json_equal([False], [0]))
        self.assertTrue(maintenance._strict_json_equal({"x": [1, "a"]}, {"x": [1, "a"]}))

    def test_load_cases_rejects_duplicate_keys_nonfinite_and_empty(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            for text in ["[]", '[{"id":"a","id":"b","introduced":0,"visibility":"public","input":{},"expected":{}}]',
                         '[{"id":"a","introduced":0,"visibility":"public","input":NaN,"expected":{}}]']:
                self._write_cases(root, text)
                with self.assertRaises(maintenance.MaintenanceFixtureError):
                    maintenance.load_cases(root)

    def test_load_cases_requires_nonempty_ids_and_required_fields(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            for case in [{"id":"", "introduced":0, "visibility":"public", "input":{}, "expected":{}},
                         {"id":"a", "introduced":True, "visibility":"public", "input":{}, "expected":{}},
                         {"id":"a", "introduced":0, "visibility":"public"}]:
                self._write_cases(root, json.dumps([case]))
                with self.assertRaises(maintenance.MaintenanceFixtureError):
                    maintenance.load_cases(root)

    def test_layout_rejects_forbidden_global_json(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); base = root / "benchmarks/maintenance-sim"
            for rel in ["contract.md", "guidance/common.md", "guidance/csharp.md", "guidance/fsharp.md"]:
                (base / rel).parent.mkdir(parents=True, exist_ok=True); (base / rel).write_bytes(b"x\n")
            (base / "episodes").mkdir()
            for i in range(1, 9): (base / "episodes" / f"{i:02d}.md").write_bytes(b"x\n")
            for language, project in [("csharp", "Simulation.csproj"), ("fsharp", "Simulation.fsproj")]:
                seed = base / "seed" / language; ref = base / "reference" / language
                seed.mkdir(parents=True); ref.mkdir(parents=True)
                (seed / project).write_bytes(b"x\n")
                (seed / "global.json").write_bytes(b"x\n")
                for i in range(1, 9): (ref / f"{i:02d}.patch").write_bytes(b"")
            with self.assertRaises(maintenance.MaintenanceFixtureError):
                maintenance.validate_layout(root)
    def test_case_bounds_and_supersession(self):
        cases = [{"id": "a", "introduced": 0, "through": 2, "visibility": "public"},
                 {"id": "b", "introduced": 2, "visibility": "evaluation"}]
        self.assertEqual([x["id"] for x in maintenance.applicable_cases(cases, 2)], ["a", "b"])
        self.assertEqual([x["id"] for x in maintenance.applicable_cases(cases, 3)], ["b"])
        self.assertEqual(maintenance.applicable_cases(cases, 2, visibility="public")[0]["id"], "a")

    def test_case_invalid_bounds(self):
        with self.assertRaises(ValueError):
            maintenance.applicable_cases([{"introduced": 3, "through": 2}], 2)

    def test_envelope_has_no_future_episode_and_bytes(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); base = root / "benchmarks/maintenance-sim"
            for rel in ["guidance/common.md", "guidance/csharp.md", "guidance/fsharp.md", "contract.md"]:
                (base / rel).parent.mkdir(parents=True, exist_ok=True); (base / rel).write_text(rel, encoding="utf-8", newline="\n")
            (base / "episodes").mkdir()
            for i in range(1, 9): (base / "episodes" / f"{i:02d}.md").write_text(str(i), encoding="utf-8", newline="\n")
            env = maintenance.serialize_envelope(root, "csharp", 2, {"Simulation.csproj": "x"})
            self.assertEqual(env["source_files"], 1); self.assertEqual(env["source_bytes"], 1)
            self.assertNotIn("episode_03", env["components"]); self.assertFalse(env["live"])
            self.assertEqual(env["allocations"], {"integration": 0, "pilot": 0})

    def test_layout_missing_is_explicit(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaisesRegex(maintenance.MaintenanceFixtureError, "missing"):
                maintenance.validate_layout(Path(td))

    def test_seed_checkpoint_zero_does_not_require_future_patches(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); base = root / "benchmarks/maintenance-sim"
            for rel in ["contract.md", "guidance/common.md", "guidance/csharp.md"]:
                (base / rel).parent.mkdir(parents=True, exist_ok=True); (base / rel).write_text(rel, encoding="utf-8", newline="\n")
            seed = base / "seed/csharp"; seed.mkdir(parents=True)
            (seed / "Simulation.csproj").write_text("<Project />\n", encoding="utf-8", newline="\n")
            self.assertEqual(maintenance.reconstruct(root, "csharp", 0)["Simulation.csproj"], "<Project />\n")

    def test_envelope_stage_mapping_and_exact_artifact(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); base = root / "benchmarks/maintenance-sim"
            for rel, text in [("contract.md", "seed"), ("guidance/common.md", "common"), ("guidance/csharp.md", "cs")]:
                (base / rel).parent.mkdir(parents=True, exist_ok=True); (base / rel).write_text(text, encoding="utf-8", newline="\n")
            (base / "episodes").mkdir()
            for i in range(1, 9): (base / "episodes" / f"{i:02d}.md").write_text(f"episode-{i}", encoding="utf-8", newline="\n")
            result = maintenance.serialize_envelope(root, "csharp", 2, {"Simulation.cs": "x\n"}, task_episode=3)
            raw = result["serialized"].encode("utf-8")
            self.assertEqual(len(raw), result["input_bytes"]); self.assertEqual(hashlib.sha256(raw).hexdigest(), result["sha256"])
            self.assertEqual(result["envelope"]["source_checkpoint"], 2); self.assertEqual(result["envelope"]["task_episode"], 3)
            self.assertEqual(result["envelope"]["current_task"], "episode-3")
            self.assertEqual(result["envelope"]["past_public_obligations"], ["episode-1", "episode-2"])

    def test_failure_classification(self):
        self.assertEqual(maintenance.classify_build({"returncode": 1}), "build")
        self.assertEqual(maintenance.classify_build({"returncode": 0}), "runtime")
        self.assertEqual(maintenance.classify_build({"returncode": 0, "timed_out": True}), "build")

    def _runtime_root(self, root):
        base = root / "benchmarks/maintenance-sim"
        for rel in ["contract.md", "guidance/common.md", "guidance/csharp.md"]:
            p = base / rel; p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(b"x\n")
        seed = base / "seed/csharp"; seed.mkdir(parents=True)
        (seed / "Simulation.csproj").write_bytes(b"<Project />\n")

    def _invoke(self, runtime_stdout="{}\n", *, runtime_stderr="", runtime_timeout=False,
                build_timeout=False, runtime_returncode=0):
        calls = []
        def invoke(argv, **kwargs):
            calls.append((argv, kwargs))
            if argv[1] == "--version": return SimpleNamespace(returncode=0, stdout=maintenance.SDK + "\n", stderr="")
            if argv[1] == "build":
                if build_timeout: raise __import__("subprocess").TimeoutExpired(argv, 120)
                return SimpleNamespace(returncode=0, stdout="build ok", stderr="")
            if runtime_timeout: raise __import__("subprocess").TimeoutExpired(argv, 30)
            return SimpleNamespace(returncode=runtime_returncode, stdout=runtime_stdout, stderr=runtime_stderr)
        return invoke, calls

    def test_runtime_parser_rejects_malformed_duplicate_and_nonfinite_json(self):
        case = {"input": {}, "expected": {}}
        for output in ('{\n', '{"x":1,"x":2}\n', '{"x":NaN}\n'):
            with self.subTest(output=output), tempfile.TemporaryDirectory() as td:
                root = Path(td); self._runtime_root(root); invoke, _ = self._invoke(output)
                result = maintenance.build_checkpoint(root, "csharp", 0, [case], invoke=invoke)
                self.assertEqual((result["passed"], result["category"]), (False, "parse"))

    def test_runtime_wrong_line_count_and_bool_int_mismatch(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); self._runtime_root(root)
            invoke, _ = self._invoke('{}\n{}\n')
            result = maintenance.build_checkpoint(root, "csharp", 0, [{"input": {}, "expected": {}}], invoke=invoke)
            self.assertEqual(result["category"], "parse"); self.assertEqual(result["line_count"], 2)
            invoke, _ = self._invoke('{"x":true}\n')
            result = maintenance.build_checkpoint(root, "csharp", 0, [{"input": {}, "expected": {"x": 1}}], invoke=invoke)
            self.assertFalse(result["passed"]); self.assertEqual(result["category"], "semantic")

    def test_build_and_runtime_timeout_are_failures(self):
        for option, category in (({"build_timeout": True}, "build"), ({"runtime_timeout": True}, "runtime")):
            with self.subTest(category=category), tempfile.TemporaryDirectory() as td:
                root = Path(td); self._runtime_root(root); invoke, _ = self._invoke(**option)
                result = maintenance.build_checkpoint(root, "csharp", 0, [{"input": {}, "expected": {}}], invoke=invoke)
                self.assertFalse(result["passed"]); self.assertEqual(result["category"], category)

    def test_runtime_oversized_output_and_stderr_are_failures(self):
        for invoke in (self._invoke("x" * 65537)[0], self._invoke('{}\n', runtime_stderr="error")[0]):
            with tempfile.TemporaryDirectory() as td:
                root = Path(td); self._runtime_root(root)
                result = maintenance.build_checkpoint(root, "csharp", 0, [{"input": {}, "expected": {}}], invoke=invoke)
                self.assertFalse(result["passed"]); self.assertEqual(result["category"], "runtime")

    def test_read_lf_rejects_bom_crlf_and_empty_patch_fails(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); self._runtime_root(root)
            for data, reason in ((b"\xef\xbb\xbfx\n", "BOM"), (b"x\r\n", "non-LF")):
                p = root / "bad"; p.write_bytes(data)
                with self.assertRaisesRegex(maintenance.MaintenanceFixtureError, reason): maintenance._read_lf(p)
            ref = root / "benchmarks/maintenance-sim/reference/csharp"; ref.mkdir(parents=True)
            (ref / "01.patch").write_bytes(b"")
            with self.assertRaisesRegex(maintenance.MaintenanceFixtureError, "does not apply"):
                maintenance.reconstruct(root, "csharp", 1)

    def test_reconstruct_forces_lf_git_apply_per_call(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); self._runtime_root(root)
            ref = root / "benchmarks/maintenance-sim/reference/csharp"; ref.mkdir(parents=True)
            (ref / "01.patch").write_bytes(b"patch\n")
            completed = SimpleNamespace(returncode=0, stdout="", stderr="")
            with mock.patch("alf.maintenance.subprocess.run", return_value=completed) as run:
                maintenance.reconstruct(root, "csharp", 1)
            self.assertEqual(run.call_count, 2)
            for call in run.call_args_list:
                self.assertEqual(call.args[0][:5], ["git", "-c", "core.autocrlf=false", "-c", "core.safecrlf=false"])

    def test_cli_maps_all_sixteen_predecessor_task_pairs(self):
        cases = [{"id": str(i), "introduced": i, "visibility": "evaluation", "input": {}, "expected": {}}
                 for i in range(9)]
        calls = []
        def envelope(root, language, checkpoint, source, *, task_episode=None):
            calls.append((language, checkpoint, task_episode))
            return {"serialized": "{}\n", "envelope": {}, "language": language,
                    "source_checkpoint": checkpoint, "task_episode": task_episode}
        with tempfile.TemporaryDirectory() as td, \
             mock.patch.object(maintenance, "validate_layout", return_value={}), \
             mock.patch.object(maintenance, "load_cases", return_value=cases), \
             mock.patch.object(maintenance, "reconstruct", return_value={"Simulation.csproj": "x\n"}), \
             mock.patch.object(maintenance, "serialize_envelope", side_effect=envelope), \
             mock.patch.object(maintenance, "reference_submission_metrics", return_value=[]):
            self.assertEqual(maintenance_check.main(["--output-dir", td]), 0)
        expected = [(language, episode - 1, episode) for language in maintenance.LANGUAGES for episode in range(1, 9)]
        self.assertEqual(calls, expected)

    def test_cli_provenance_contains_execution_and_fault_sources(self):
        root = Path(maintenance_check.__file__).resolve().parents[1]
        expected_paths = ["src/alf/maintenance.py", "scripts/maintenance_check.py",
                          "tests/test_maintenance.py", "benchmarks/maintenance-sim/fixtures/faults.json"]
        with tempfile.TemporaryDirectory() as td, \
             mock.patch.object(maintenance, "validate_layout", return_value={}), \
             mock.patch.object(maintenance, "load_cases", return_value=[{"introduced": i} for i in range(9)]), \
             mock.patch.object(maintenance, "reconstruct", return_value={}), \
             mock.patch.object(maintenance, "serialize_envelope",
                               side_effect=lambda *args, **kwargs: {"serialized": "{}\n", "envelope": {}}), \
             mock.patch.object(maintenance, "reference_submission_metrics", return_value=[]):
            self.assertEqual(maintenance_check.main(["--output-dir", td]), 0)
            report = json.loads((Path(td) / "report.json").read_text(encoding="utf-8"))
        for rel in expected_paths:
            expected = hashlib.sha256((root / rel).read_bytes()).hexdigest()
            self.assertEqual(report["provenance"]["content_sha256"][rel], expected)

    def test_reference_submission_metric_includes_required_empty_notes(self):
        def reconstructed(root, language, checkpoint):
            return {"Program.cs": "before\n" if checkpoint == 0 else "after\n"}
        with mock.patch("alf.maintenance.reconstruct", side_effect=reconstructed):
            rows = maintenance.reference_submission_metrics(Path("unused"))
        expected = b'{"architecture_notes":"","files":{"Program.cs":"after\\n"}}'
        self.assertEqual(rows[0]["bytes"], len(expected))
        self.assertEqual(rows[0]["sha256"], hashlib.sha256(expected).hexdigest())
        self.assertIn("lower-bound placeholder", rows[0]["note"])
        self.assertIn("native/model framing", rows[0]["note"])

    def test_fault_manifest_missing_and_path_validation_are_explicit(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            with self.assertRaisesRegex(maintenance.MaintenanceFixtureError, "missing trusted fault manifest"):
                maintenance.load_fault_manifest(root)
            path = root / "benchmarks/maintenance-sim/fixtures/faults.json"
            path.parent.mkdir(parents=True)
            for patch in ["../escape.patch", "C:/escape.patch", ""]:
                path.write_text(json.dumps([{"id": "f", "language": "csharp", "checkpoint": 1,
                                             "patch": patch, "witness_case_id": "w"}]), encoding="utf-8", newline="\n")
                with self.assertRaises(maintenance.MaintenanceFixtureError): maintenance.load_fault_manifest(root)

    def test_fault_audit_requires_compile_success_for_semantic_kill(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            cases = [{"id": "w", "introduced": 0, "visibility": "evaluation", "input": {}, "expected": {}}]
            manifest = root / "benchmarks/maintenance-sim/fixtures/faults.json"
            manifest.parent.mkdir(parents=True)
            (manifest.parent / "faults").mkdir()
            (manifest.parent / "faults" / "one.patch").write_text("diff --git a/Simulation.csproj b/Simulation.csproj\n", encoding="utf-8", newline="\n")
            manifest.write_text(json.dumps([{"id": "f", "language": "csharp", "checkpoint": 0,
                                             "patch": "faults/one.patch", "witness_case_id": "w"}]), encoding="utf-8", newline="\n")
            source = {"Simulation.csproj": "x\n"}
            results = iter([{"passed": True, "category": "semantic"},
                            {"passed": False, "category": "build"}])
            with mock.patch.object(maintenance, "reconstruct", return_value=source), \
                 mock.patch.object(maintenance, "_fault_source", return_value=(source, "p")), \
                 mock.patch.object(maintenance, "_build_source", side_effect=lambda *a, **k: next(results)):
                report = maintenance.audit_faults(root, cases)
            self.assertEqual(report["status"], "failed")
            self.assertFalse(report["faults"][0]["semantic_kill"])

    def test_fault_audit_accepts_compile_successful_semantic_kill(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); manifest = root / "benchmarks/maintenance-sim/fixtures/faults.json"
            manifest.parent.mkdir(parents=True); (manifest.parent / "faults").mkdir()
            (manifest.parent / "faults" / "one.patch").write_text("patch\n", encoding="utf-8", newline="\n")
            manifest.write_text(json.dumps([{"id": "f", "language": "csharp", "checkpoint": 0,
                                             "patch": "faults/one.patch", "witness_case_id": "w"}]), encoding="utf-8", newline="\n")
            cases = [{"id": "w", "input": {}, "expected": {}}]; source = {"Simulation.csproj": "x\n"}
            results = iter([{"passed": True, "category": "semantic"}, {"passed": False, "category": "semantic"}])
            with mock.patch.object(maintenance, "reconstruct", return_value=source), \
                 mock.patch.object(maintenance, "_fault_source", return_value=(source, "p")), \
                 mock.patch.object(maintenance, "_build_source", side_effect=lambda *a, **k: next(results)):
                report = maintenance.audit_faults(root, cases)
            self.assertEqual(report["status"], "passed")
            self.assertTrue(report["faults"][0]["semantic_kill"])

    def test_applicability_keeps_dimensions_and_prior_failure(self):
        row = maintenance.classify_applicability(submission_disposition="wrong-behavior", prerequisite=True,
                                                  current=False, evaluation_available=True, recovery=True,
                                                  prior_failure="wrong-behavior")
        self.assertEqual(row["prerequisite_correctness"], True)
        self.assertEqual(row["current_correctness"], False)
        self.assertEqual(row["prior_failure"], "wrong-behavior")
        self.assertIsNone(row["attribution"])

    def test_applicability_build_runtime_parse_is_unknown_and_missing_data_is_explicit(self):
        for category in ("build", "runtime", "parse"):
            row = maintenance.classify_applicability(submission_disposition="noncompile", prerequisite=True,
                                                      current=False, evaluation_available=True, build_category=category)
            self.assertIsNone(row["prerequisite_correctness"])
            self.assertIsNone(row["current_correctness"])
            self.assertFalse(row["evaluation_availability"])
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaisesRegex(maintenance.MaintenanceFixtureError, "missing trusted cases"):
                maintenance.audit_applicability(Path(td))

    def test_real_applicability_audit_uses_fixed_sources_and_witnesses(self):
        cases = [{"id": "seed", "introduced": 0, "input": {}, "expected": {}},
                 {"id": "ep1", "introduced": 1, "input": {}, "expected": {}},
                 {"id": "ep2", "introduced": 2, "input": {}, "expected": {}}]
        cases += [{"id": ident, "introduced": episode, "input": {}, "expected": {}}
                  for episode, ident in maintenance._DOWNSTREAM_WITNESSES.items()
                  if ident not in {case["id"] for case in cases}]
        manifest = [{"id": f"{language}-drop", "language": language, "checkpoint": 1,
                     "patch": f"faults/{language}/drop-due-effects.patch", "witness_case_id": "ep1"}
                    for language in maintenance.LANGUAGES]
        def reconstructed(root, language, checkpoint):
            extension = "cs" if language == "csharp" else "fs"
            return {f"Simulation.{extension}": f"ref-{checkpoint}\n", f"Simulation.{extension}proj": "project\n"}
        def built(source, language, selected, **kwargs):
            text = "".join(source.values())
            if "intentionally not valid" in text:
                return {"passed": False, "category": "build"}
            current = any(case["introduced"] == 2 for case in selected)
            if "ref-0" in text and any(case["introduced"] > 0 for case in selected):
                return {"passed": False, "category": "semantic"}
            if "ref-1" in text and current:
                return {"passed": False, "category": "semantic"}
            if "wrong" in text:
                return {"passed": False, "category": "semantic"}
            return {"passed": True, "category": "semantic"}
        with mock.patch.object(maintenance, "load_fault_manifest", return_value=manifest), \
             mock.patch.object(maintenance, "reconstruct", side_effect=reconstructed), \
             mock.patch.object(maintenance, "_fault_source",
                               side_effect=lambda root, fault: ({**reconstructed(root, fault["language"], 1),
                                                                 "Fault.md": "wrong\n"}, "patch-hash")), \
             mock.patch.object(maintenance, "_build_source", side_effect=built):
            result = maintenance.audit_applicability(Path("unused"), cases)
        self.assertEqual(result["status"], "passed")
        self.assertEqual(len(result["records"]), 12)
        self.assertEqual(len(result["downstream_witnesses"]), 16)
        for language in maintenance.LANGUAGES:
            rows = [row for row in result["records"] if row["language"] == language]
            noop = next(row for row in rows if row["id"] == "no-op")
            malformed = next(row for row in rows if row["id"] == "malformed")
            self.assertEqual(noop["source_sha256"], malformed["source_sha256"])
            noncompile = next(row for row in rows if row["id"] == "noncompile")
            self.assertIsNone(noncompile["prerequisite_correctness"])
            self.assertFalse(noncompile["evaluation_availability"])
            recovery = next(row for row in rows if row["id"] == "recovery-control")
            self.assertEqual(recovery["prior_failure"], "wrong-behavior")
            self.assertFalse(recovery["strict_chain_success"])
            self.assertFalse(recovery["actual_candidate_repair"])

    def test_complete_fault_audit_rejects_missing_family_coverage(self):
        with mock.patch.object(maintenance, "load_fault_manifest", return_value=[
                {"id": "one", "language": "csharp", "checkpoint": 1,
                 "patch": "faults/csharp/drop-due-effects.patch", "witness_case_id": "w"}]):
            with self.assertRaisesRegex(maintenance.MaintenanceFixtureError, "exactly checkpoints"):
                maintenance.audit_faults(Path("unused"), [{"id": "w"}], require_complete=True)


if __name__ == "__main__": unittest.main()
