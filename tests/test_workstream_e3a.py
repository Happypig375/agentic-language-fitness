from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from collections import Counter
from pathlib import Path

from alf.config import load_manifest
from alf.workstream_e3a import (
    PACKET_DIR, PolicyViolation, SubmissionError, apply_submission, budget,
    candidate_payload, development_cases, feedback_packet, holdout_cases,
    normalize_usage, read_json, schedule, simulate_trajectory, snapshot, structural_development, usage_sum,
)

ROOT = Path(__file__).resolve().parents[1]


class E3aReviewFixtures(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spec = read_json(ROOT / PACKET_DIR / "specification.json")
        cls.manifest = load_manifest(ROOT, cls.spec["manifest"])
        cls.before = {lang: snapshot(ROOT, cls.manifest, lang, 0) for lang in cls.spec["languages"]}

    def test_schedule_is_paired_balanced_finite_and_not_authorized(self):
        rows = schedule(self.spec)
        self.assertEqual(rows, schedule(self.spec))
        self.assertEqual(len(rows), 24)
        self.assertEqual(set(Counter((r["task_id"], r["language"]) for r in rows).values()), {4})
        for a, b in zip(rows[::2], rows[1::2]):
            self.assertEqual((a["task_id"], a["repetition"]), (b["task_id"], b["repetition"]))
            self.assertNotEqual(a["language"], b["language"])
        self.assertEqual(set(Counter((r["task_id"], r["language"]) for r in rows[::2]).values()), {2})
        limits = budget(self.spec)
        self.assertEqual(limits["max_requests"], 72)
        self.assertEqual(limits["max_input_tokens"], 2359296)
        self.assertEqual(limits["max_output_tokens_including_reasoning"], 589824)
        self.assertEqual(limits["uncached_price_upper_bound_usd"], 1.179648)
        self.assertEqual(limits["authorized_requests"], 0)
        self.assertFalse(self.spec["execution_authorized"])

    def test_payload_is_predecessor_and_current_contract_only(self):
        for language in self.spec["languages"]:
            payload = candidate_payload(ROOT, self.manifest, language, "007-query-engine-refactor")
            self.assertEqual(set(payload), {"instructions", "baseline_contract", "earlier_contracts", "current_task", "source"})
            self.assertEqual(len(payload["earlier_contracts"]), 6)
            self.assertFalse(any("Engine" in name for name in payload["source"]))
            text = json.dumps(payload)
            for forbidden in ["AGENTS.md", "PLAN.md", "summary status", "matrix-47", "workstream-e", "gpt-5.6"]:
                self.assertNotIn(forbidden, text)

    def test_preflight_uses_old_contract_not_current_task(self):
        self.assertEqual(development_cases(self.manifest, 0), self.manifest["baseline_cases"])
        self.assertNotIn(self.manifest["tasks"][5]["cases"][0], development_cases(self.manifest, 5))

    def test_holdout_is_not_renamed_development_and_has_complete_status_matrix(self):
        for task_id in self.spec["tasks"]:
            stage = next(i + 1 for i, t in enumerate(self.manifest["tasks"]) if t["id"] == task_id)
            dev = {json.dumps(c["input"], sort_keys=True) for c in development_cases(self.manifest, stage)}
            held = holdout_cases(ROOT, task_id)
            self.assertFalse(dev & {json.dumps(c["input"], sort_keys=True) for c in held})
            if stage >= 6:
                matrix = [c for c in held if c["name"].startswith("matrix-")]
                self.assertEqual(len(matrix), 25)
                self.assertEqual(sum("status" in c["expected"] for c in matrix), 4)

    def test_task_required_fsharp_compile_changes_and_csharp_files_allowed(self):
        for language in self.spec["languages"]:
            before = snapshot(ROOT, self.manifest, language, 6)
            target = snapshot(ROOT, self.manifest, language, 7)
            self.assertEqual(apply_submission(before, json.dumps({"files": target}), language, self.spec), target)
            self.assertFalse(structural_development(before, language, "007-query-engine-refactor")["passed"])
            self.assertTrue(structural_development(target, language, "007-query-engine-refactor")["passed"])
            renamed = {p: text.replace("OrderFlowEngine.Handle", "OrderFlowEngine.Run").replace(
                "OrderFlowEngine.handle", "OrderFlowEngine.run") for p, text in target.items()}
            self.assertTrue(structural_development(renamed, language, "007-query-engine-refactor")["passed"])

    def test_invalid_submissions_are_atomic(self):
        before = self.before["csharp"]
        saved = copy.deepcopy(before)
        for raw in ["oops", '{"files":{},"files":{}}', '{"files":{"Program.cs":"a","Program.cs":"b"}}',
                    '{"files":{"Program.cs":null}}', '{"files":{"Program.cs":"\\ud800"}}',
                    json.dumps({"files": {"Program.cs": "bad\r\n"}}), "\ud800", "x" * 49153]:
            with self.subTest(raw=repr(raw[:60])), self.assertRaises(SubmissionError):
                apply_submission(before, raw, "csharp", self.spec)
            self.assertEqual(before, saved)

    def test_paths_and_project_policy(self):
        before = self.before["csharp"]
        for path in ["../auth.json", "Directory.Build.targets", "x/Program.cs", "OrderFlow.fsproj", "program.cs"]:
            with self.subTest(path=path), self.assertRaises(PolicyViolation):
                apply_submission(before, json.dumps({"files": {path: "x"}}), "csharp", self.spec)
        for change in [lambda p: p.replace("net10.0", "net9.0"),
                       lambda p: p.replace("</Project>", '<Target Name="Run"><Exec Command="bad" /></Target></Project>'),
                       lambda p: p.replace("</Project>", '<ItemGroup><PackageReference Include="X" Version="1" /></ItemGroup></Project>')]:
            for language, project in [("csharp", "OrderFlow.csproj"), ("fsharp", "OrderFlow.fsproj")]:
                with self.subTest(language=language), self.assertRaises(PolicyViolation):
                    apply_submission(self.before[language], json.dumps({"files": {project: change(self.before[language][project])}}), language, self.spec)
        with self.assertRaises(PolicyViolation):
            apply_submission(self.before["fsharp"], json.dumps({"files": {"Extra.fs": "module Extra"}}), "fsharp", self.spec)

    def test_feedback_complete_errors_stable_deduplicated_and_bounded(self):
        raw = "p.fs(1,2): error FS0001: mismatch\np.cs(2,3): error CS0029: mismatch\nwarning FS3261: nullable\n"
        result = feedback_packet(raw * 20, 8192)
        self.assertEqual(result["text"], feedback_packet("\n".join(reversed(raw.splitlines())), 8192)["text"])
        self.assertFalse(result["truncated"])
        self.assertEqual(result["unique_lines"], 3)
        many = "\n".join(f"p.fs({i},1): error FS0001: type mismatch" for i in range(500))
        over = feedback_packet(many, 8192)
        self.assertLessEqual(over["bytes"], 8192)
        self.assertTrue(over["essential_error_overflow"])
        self.assertIn("TRUNCATED", over["text"])
        warnings = feedback_packet(raw + "\n".join(f"warning {i}: {'x' * 100}" for i in range(100)), 8192)
        self.assertTrue(warnings["truncated"])
        self.assertFalse(warnings["essential_error_overflow"])
        self.assertIn("error FS0001", warnings["text"])
        self.assertIn("error CS0029", warnings["text"])
        multiline = feedback_packet("p.fs(1,2): error FS0001: expected\n  int\nbut got\n  string\nwarning W: note", 8192)
        self.assertIn("expected\n  int\nbut got\n  string", multiline["text"])
        huge_context = feedback_packet("p.fs(1,2): error FS0001: expected\n" + "x" * 9000, 8192)
        self.assertTrue(huge_context["essential_error_overflow"])

    @staticmethod
    def response(index, text='{"files":{}}', status="completed", usage=None):
        return {"id": f"fixture-{index}", "text": text, "status": status,
                "usage": usage if usage is not None else {"input_tokens": 10, "output_tokens": 6,
                         "input_tokens_details": {"cached_tokens": 4}, "output_tokens_details": {"reasoning_tokens": 2}}}

    def run_fixture(self, replies, checks):
        calls = []
        def session(previous, source, feedback):
            calls.append((previous, source, feedback))
            return replies[len(calls) - 1]
        result = simulate_trajectory(self.before["csharp"], "csharp", self.spec, session,
                                     lambda source, index: checks[index])
        return result, calls

    def test_passing_first_patch_stops_regardless_of_later_holdout_result(self):
        outputs = []
        for withheld_score in [True, False]:
            result, calls = self.run_fixture([self.response(0)], [{"passed": True, "category": "development", "output": ""}])
            self.assertEqual(len(calls), 1)
            self.assertEqual(result["repair_usage"], dict.fromkeys(result["repair_usage"], 0))
            outputs.append(result)  # score is only attached AFTER the trajectory
            scored = {"trajectory": result, "final_holdout": withheld_score}
            self.assertEqual(scored["final_holdout"], withheld_score)
        self.assertEqual(outputs[0], outputs[1])

    def test_failed_first_then_pass_preserves_mock_lineage_and_first_evidence(self):
        patch = json.dumps({"files": {"Program.cs": self.before["csharp"]["Program.cs"] + "\n// fixed\n"}})
        result, calls = self.run_fixture([self.response(0), self.response(1, patch)], [
            {"passed": False, "category": "development", "output": "ERROR case-a expected x received y"},
            {"passed": True, "category": "development", "output": ""}])
        self.assertIsNone(calls[0][0])
        self.assertEqual(calls[1][0], "fixture-0")
        self.assertIn("ERROR case-a", calls[1][2]["text"])
        self.assertEqual(result["rounds"][0]["submission"], '{"files":{}}')
        self.assertNotEqual(result["rounds"][0]["applied_sha256"], result["rounds"][1]["applied_sha256"])
        self.assertEqual(result["total_usage"]["input_tokens"], 20)
        self.assertEqual(result["total_usage"]["output_tokens"], 12)
        self.assertEqual(result["repair_usage"]["input_tokens"], 10)
        self.assertFalse(result["live_evidence"])

    def test_invalid_format_consumes_all_rounds_without_manual_repair(self):
        result, calls = self.run_fixture([self.response(i, "not JSON") for i in range(3)], [])
        self.assertEqual(len(calls), 3)
        self.assertEqual(result["stop"], "repair-budget")
        self.assertEqual(result["last_applied_source"], self.before["csharp"])
        self.assertIsNone(result["terminal_submission_source"])
        self.assertTrue(all(r["submission"] == "not JSON" for r in result["rounds"]))

    def test_terminal_invalid_submission_does_not_inherit_last_applied_score(self):
        result, _ = self.run_fixture([self.response(0), self.response(1, "invalid"), self.response(2, "invalid")], [
            {"passed": False, "category": "development", "output": "ERROR case: mismatch"}])
        self.assertEqual(result["first_submission_source"], self.before["csharp"])
        self.assertIsNone(result["terminal_submission_source"])
        self.assertEqual(result["last_applied_source"], self.before["csharp"])

    def test_ambiguous_or_incomplete_request_is_never_reissued(self):
        for status in ["timeout", "incomplete", "transport-error"]:
            result, calls = self.run_fixture([self.response(0, status=status, usage={"input_tokens": 17})], [])
            self.assertEqual(len(calls), 1)
            self.assertEqual(result["stop"], "request-incomplete-or-ambiguous")
            self.assertEqual(result["total_usage"]["input_tokens"], 17)
            self.assertIsNone(result["total_usage"]["output_tokens"])

    def test_forbidden_patch_and_essential_feedback_overflow_are_terminal(self):
        result, calls = self.run_fixture([self.response(0, '{"files":{"auth.json":"x"}}')], [])
        self.assertEqual(result["stop"], "protocol-violation")
        self.assertEqual(len(calls), 1)
        result, calls = self.run_fixture([self.response(0)], [{"passed": False, "category": "build",
            "output": "\n".join(f"p.fs({i},1): error FS0001: mismatch" for i in range(500))}])
        self.assertEqual(result["stop"], "feedback-cap-apparatus-failure")
        self.assertEqual(len(calls), 1)

    def test_usage_subsets_missingness_and_invalid_totals(self):
        usage = normalize_usage(self.response(0)["usage"])
        self.assertEqual(usage_sum([{"usage": usage}])["output_tokens"], 6)  # includes reasoning 2
        missing = normalize_usage({"input_tokens": 10, "output_tokens": 5})
        self.assertIsNone(missing["cached_input_tokens"])
        self.assertIsNone(usage_sum([{"usage": usage}, {"usage": missing}])["reasoning_output_tokens"])
        bad = normalize_usage({"input_tokens": True, "output_tokens": -1})
        self.assertFalse(bad["totals_available"])
        inconsistent = normalize_usage({"input_tokens": 5, "output_tokens": 3, "total_tokens": 7,
                                        "input_tokens_details": {"cached_tokens": 6}})
        self.assertEqual(inconsistent["invalid_fields"], ["cached_input_tokens", "total_tokens"])
        self.assertIsNone(inconsistent["cached_input_tokens"])
        self.assertEqual(inconsistent["raw"]["total_tokens"], 7)

    def test_accounting_problem_retains_correctness_but_prevents_more_requests(self):
        for usage, stop in [({"input_tokens": 4}, "accounting-unavailable-or-invalid"),
                            ({"input_tokens": 32769, "output_tokens": 8}, "reported-request-budget-exceeded")]:
            result, calls = self.run_fixture([self.response(0, usage=usage)], [
                {"passed": True, "category": "development", "output": ""}])
            self.assertEqual(result["stop"], stop)
            self.assertEqual(len(calls), 1)
            self.assertTrue(result["rounds"][0]["development"]["passed"])

    def test_review_packet_is_reproducible(self):
        module_spec = importlib.util.spec_from_file_location("e3a_check", ROOT / "scripts/e3a_check.py")
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)
        self.assertEqual(module.make_packet(), read_json(ROOT / PACKET_DIR / "review-packet.json"))


if __name__ == "__main__":
    unittest.main()
