import json
import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch

from alf.h_fixtures import (FixtureError, build_sandbox_fixtures, credential_free_environment, evaluate_fault,
                            evaluate_trusted, evaluate_with_sandbox, fault_mutations,
                            mutate_once, _semantic_caught)
from alf.h_workload import source_for


class HFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).resolve().parents[1]

    def test_environment_scrubs_credentials_and_proxy_values(self):
        env = credential_free_environment(Path("work"), {"PATH": "ok", "OPENAI_API_KEY": "secret",
                                                     "CODEX_HOME": "secret", "HTTPS_PROXY": "secret"})
        self.assertEqual(env["PATH"], "ok")
        self.assertEqual(env["DOTNET_CLI_WORKLOAD_UPDATE_NOTIFY_DISABLE"], "true")
        self.assertFalse(any("secret" == value for value in env.values()))

    def test_mutation_requires_one_exact_source_match_and_is_isolated(self):
        source = {"Engine.cs": "before unique after"}
        changed = mutate_once(source, "Engine.cs", "unique", "fault")
        self.assertEqual(source["Engine.cs"], "before unique after")
        self.assertEqual(changed["Engine.cs"], "before fault after")
        for old in ("", "missing", "e"):
            with self.assertRaises(FixtureError):
                mutate_once(source, "Engine.cs", old, "x")

    def test_fixture_is_scoped_and_semantically_compares_every_case(self):
        source = {"OrderFlow.csproj": "<Project />", "Engine.cs": "class Engine {}"}
        original = dict(source)
        cases = [{"name": "one", "input": {"x": 1}, "expected": {"ok": True}}]
        calls = []
        def invoke(argv, **kwargs):
            calls.append((argv, kwargs))
            if argv[1:] == ["--version"]:
                policy = json.loads((Path(kwargs["cwd"]) / "global.json").read_text(encoding="utf-8"))
                self.assertEqual(policy, {"sdk": {"version": "10.0.302", "rollForward": "disable",
                                                   "allowPrerelease": False}})
                return subprocess.CompletedProcess(argv, 0, b"10.0.302\n", b"")
            if argv[1] == "build":
                return subprocess.CompletedProcess(argv, 0, b"built", b"")
            return subprocess.CompletedProcess(argv, 0, b'{"ok":false}\n', b"")
        result = evaluate_trusted(source, cases, "csharp", invoke=invoke)
        self.assertFalse(result["passed"])
        self.assertEqual(result["category"], "semantic")
        self.assertEqual(result["differences"][0]["name"], "one")
        self.assertEqual(json.loads(calls[2][1]["input"]), {"x": 1})
        self.assertTrue(all(calls[index][1]["timeout"] <= limit for index, limit in ((0, 10), (1, 60), (2, 10))))
        self.assertFalse(any("AUTH" in key.upper() or "TOKEN" in key.upper()
                             for key in calls[2][1]["env"]))
        self.assertEqual(source, original)

    def test_sdk_mismatch_retains_bounded_version_diagnostics(self):
        source = {"OrderFlow.csproj": "<Project />", "Engine.cs": "class Engine {}"}
        def invoke(argv, **kwargs):
            return subprocess.CompletedProcess(argv, 0, b"11.0.100\n", b"selected newer SDK")
        with self.assertRaises(FixtureError) as caught:
            evaluate_trusted(source, [], "csharp", invoke=invoke)
        message = str(caught.exception)
        self.assertIn('"expected": "10.0.302"', message)
        self.assertIn('"observed_stdout": "11.0.100\\n"', message)
        self.assertIn('"timed_out": false', message)
        self.assertLess(len(message), 9000)

    def test_build_failure_is_not_semantic_fault_detection(self):
        source = {"OrderFlow.csproj": "<Project />", "Engine.cs": "class Engine {}"}
        def invoke(argv, **kwargs):
            if argv[1:] == ["--version"]:
                return subprocess.CompletedProcess(argv, 0, b"10.0.302\n", b"")
            return subprocess.CompletedProcess(argv, 1, b"", b"compile error")
        result = evaluate_trusted(source, [], "csharp", invoke=invoke)
        self.assertEqual((result["passed"], result["category"]), (False, "build"))

    def test_fault_requires_build_success_and_semantic_rejection(self):
        source = {"OrderFlow.csproj": "<Project />", "Engine.cs": "class Engine { /*good*/ }"}
        cases = [{"name": "oracle", "input": {}, "expected": {"ok": True}}]
        calls = 0
        def invoke(argv, **kwargs):
            nonlocal calls
            calls += 1
            if argv[1:] == ["--version"]:
                return subprocess.CompletedProcess(argv, 0, b"10.0.302\n", b"")
            if argv[1] == "build":
                return subprocess.CompletedProcess(argv, 0, b"ok", b"")
            return subprocess.CompletedProcess(argv, 0, b'{"ok":false}\n', b"")
        result = evaluate_fault(source, cases, "csharp", "Engine.cs", "/*good*/", "/*fault*/",
                                "missing-key", invoke=invoke)
        self.assertTrue(result["caught"])
        self.assertEqual(calls, 3)

    def test_scope_refuses_missing_project_file_count_and_actual_cr(self):
        with self.assertRaises(FixtureError):
            evaluate_trusted({"x.cs": "x"}, [], "csharp")
        too_many = {"OrderFlow.csproj": "<Project />", **{f"X{i}.cs": "x" for i in range(8)}}
        with self.assertRaises(FixtureError):
            evaluate_trusted(too_many, [], "csharp")
        with self.assertRaises(FixtureError):
            evaluate_trusted({"OrderFlow.csproj": "<Project />", "X.cs": "a\r\nb"}, [], "csharp")

    def test_complete_named_matrix_has_exact_single_match_selectors(self):
        expected = {"missing-summary-key", "extra-summary-key", "case-sensitive-counts",
                    "inclusive-overdue", "subtract-overdue"}
        for level in ("core", "expanded"):
            for language in ("csharp", "fsharp"):
                gold = source_for(self.root, level, language, True)
                mutations = fault_mutations(language, level)
                names = [item[0] for item in mutations]
                required = expected | ({"reconcile-corruption", "dependency-corruption"}
                                       if level == "expanded" else set())
                self.assertEqual(set(names), required)
                self.assertEqual(len(names), len(required))
                for name, filename, old, new in mutations:
                    with self.subTest(level=level, language=language, fault=name):
                        changed = mutate_once(gold, filename, old, new)
                        self.assertNotEqual(changed[filename], gold[filename])
                        if name == "subtract-overdue":
                            self.assertIn("pending - 1" if language == "fsharp" else "pending--" if level == "core" else "all.Count(order => IsActive", changed[filename])

    def test_fsharp_subtract_overdue_uses_each_levels_declared_bindings(self):
        expected = {"core": ("isPending", "isProcessing"),
                    "expanded": ("pendingOrder", "processingOrder")}
        for level, bindings in expected.items():
            gold = source_for(self.root, level, "fsharp", True)
            mutation = next(item for item in fault_mutations("fsharp", level)
                            if item[0] == "subtract-overdue")
            changed = mutate_once(gold, mutation[1], mutation[2], mutation[3])[mutation[1]]
            for binding in bindings:
                self.assertIn(f"let {binding} =", changed)
                self.assertIn(f"if {bindings[0]} then", changed)
            wrong = "pendingOrder" if level == "core" else "isPending"
            self.assertNotIn(f"if {wrong} then pending <- pending - 1", changed)

    def test_sandbox_adapter_is_prepared_evaluated_and_closed(self):
        events = []
        class Fake:
            def __init__(self, baseline, language, spec, fixture_image_id=None):
                events.append(("init", language, fixture_image_id, dict(baseline)))
            def prepare(self): events.append(("prepare",)); return {"ready": True}
            def evaluate(self, source, cases, deadline):
                events.append(("evaluate", source, cases, deadline)); return {"passed": True}
            def close(self): events.append(("close",))
        source = {"OrderFlow.csproj": "<Project />", "Program.cs": "class Program {}"}
        result = evaluate_with_sandbox(source, [], "csharp", {"execution_authorized": False}, source,
                                       fixture_image_id="fixture", evaluator_type=Fake)
        self.assertTrue(result["passed"])
        self.assertEqual([event[0] for event in events], ["init", "prepare", "evaluate", "close"])

    def test_fixture_image_uses_disabled_private_spec_copy(self):
        original = {"execution_authorized": True, "user_live_execution_approved": True,
                    "approved_integration_dispatches": 5, "approved_pilot_dispatches": 64,
                    "analysis": {"human_review_approved": True},
                    "model": {"h_live_integration_verified": True}}
        observed = []
        class Fake:
            def __init__(self, baseline, language, spec, fixture_image_id=None): observed.append(spec)
            def prepare(self): return {}
            def evaluate(self, source, cases, deadline): return {"passed": True}
            def close(self): pass
        source = {"OrderFlow.csproj": "<Project />", "Program.cs": "class P{}"}
        with patch("alf.h_fixtures.source_for", return_value=source), \
             patch("alf.h_fixtures.cases_for", return_value=[]), \
             patch("alf.h_fixtures.fault_matrix", return_value=[]):
            report = build_sandbox_fixtures(self.root, original, "sha256:" + "0" * 64,
                                            evaluator_type=Fake)
        self.assertTrue(report["fixture_only"] and report["non_experimental"])
        self.assertEqual(original["approved_pilot_dispatches"], 64)
        self.assertTrue(all(not item["execution_authorized"] and not item["user_live_execution_approved"]
                            and item["approved_integration_dispatches"] == 0
                            and item["approved_pilot_dispatches"] == 0 for item in observed))

    def test_actual_docker_result_shape_credits_only_clean_semantic_failure(self):
        result = {"passed": False, "category": "development", "build_passed": True,
                  "operations": [{"build": {"returncode": 0}}, {"program": {
                      "returncode": 0, "timed_out": False, "output_limit_exceeded": False}}]}
        self.assertTrue(_semantic_caught(result))
        for change in ({"returncode": 1}, {"timed_out": True}, {"output_limit_exceeded": True}):
            changed = json.loads(json.dumps(result))
            changed["operations"][-1]["program"].update(change)
            self.assertFalse(_semantic_caught(changed))
        changed = dict(result, build_passed=False)
        self.assertFalse(_semantic_caught(changed))


if __name__ == "__main__":
    unittest.main()
