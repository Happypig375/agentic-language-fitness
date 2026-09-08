"""Model-free tests. Mock replies/fixture rubric claims are not provider evidence."""
from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import time
import unittest
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch

from alf.config import load_manifest
from alf.e3a_api import BudgetGuard, GuardFailure, HttpTransport, ResponsesAdapter
from alf.e3a_codex import CodexOAuthAdapter, DispatchGuard, parse_cli_jsonl
from alf.e3a_runner import run_batch
from alf.e3a_sandbox import DockerEvaluator, SandboxFailure, bounded_process, container_arguments, tree_identity
from alf.models import ProcessResult
from alf.protocol import canonical_json_hash
from alf.workstream_e3a import (PACKET_DIR, PolicyViolation, apply_submission, candidate_payload,
    feedback_packet, project_development, read_json, run_trajectory, score_submission, snapshot)

ROOT = Path(__file__).resolve().parents[1]
SPEC = read_json(ROOT / PACKET_DIR / "specification.json")
HISTORICAL_SPEC = read_json(ROOT / "tests" / "fixtures" / "e3a-original-api-specification.json")
MANIFEST = load_manifest(ROOT, SPEC["manifest"])
module_spec = importlib.util.spec_from_file_location("e3a_check_fixtures", ROOT / "scripts/e3a_check.py")
fixtures = importlib.util.module_from_spec(module_spec)
module_spec.loader.exec_module(fixtures)
sandbox_check_spec = importlib.util.spec_from_file_location("e3a_sandbox_check", ROOT / "scripts/e3a_sandbox_check.py")
sandbox_check = importlib.util.module_from_spec(sandbox_check_spec)
sandbox_check_spec.loader.exec_module(sandbox_check)


def rates(spec=SPEC):
    return {"model": spec["model"]["requested"], "service_tier": "default", "input_reservation_rate": "0.25",
            "output_rate": "1.20", "checked_date": spec["budgets"]["pricing_checked_utc_date"],
            "count_call_upper_usd": "0", "account_verified": False, "fixture_assumptions_only": True}


class MockTransport:
    is_live = False

    def __init__(self, answer=lambda body: '{"files":{}}'):
        self.calls, self.answer, self.generation = [], answer, 0
        self.count = 10
        self.change = lambda body: body
        self.fail = None

    def post(self, path, body, timeout):
        self.calls.append((path, copy.deepcopy(body), timeout))
        if self.fail and path == self.fail:
            raise TimeoutError("fixture timeout")
        if path.endswith("input_tokens"):
            return {"http_status": 200, "body": {"object": "response.input_tokens", "input_tokens": self.count}}
        self.generation += 1
        response = {"id": f"mock-{self.generation}", "previous_response_id": body.get("previous_response_id"),
            "status": "completed", "model": body["model"], "service_tier": body["service_tier"],
            "reasoning": body["reasoning"], "usage": {"input_tokens": 10, "output_tokens": 6,
                "input_tokens_details": {"cached_tokens": 2}, "output_tokens_details": {"reasoning_tokens": 3}},
            "output": [{"type": "message", "role": "assistant", "content": [
                {"type": "output_text", "text": self.answer(body)}]}]}
        return {"http_status": 200, "body": self.change(response)}

    def launch(self, stdin, timeout):
        self.calls.append(("codex-exec", bytes(stdin), timeout))
        if self.fail:
            return {"stdout": b"", "stderr": b"fixture", "returncode": 1,
                    "timed_out": False, "output_overflow": False, "cleanup_confirmed": True}
        self.generation += 1
        answer = self.answer(json.loads(stdin))
        stdout = "\n".join([
            json.dumps({"type": "thread.started", "thread_id": f"thread-{self.generation}"}),
            json.dumps({"type": "turn.started"}),
            json.dumps({"type": "item.completed", "item": {"type": "agent_message", "text": answer}}),
            json.dumps({"type": "turn.completed", "usage": {"input_tokens": 10, "output_tokens": 6,
                        "cached_input_tokens": 2, "reasoning_output_tokens": 3}}), ""])
        return {"stdout": stdout, "stderr": "", "returncode": 0, "timed_out": False,
                "output_overflow": False, "cleanup_confirmed": True}


class RetiredApiProposalTests(unittest.TestCase):
    def setUp(self):
        self.guard = BudgetGuard(HISTORICAL_SPEC, max_requests=72, usd_ceiling="2", rates=rates(HISTORICAL_SPEC),
                                 checked_date=rates(HISTORICAL_SPEC)["checked_date"])
        self.transport = MockTransport()
        self.events = []
        self.adapter = ResponsesAdapter(HISTORICAL_SPEC, self.transport, self.guard, record=self.events.append)
        self.payload = candidate_payload(ROOT, MANIFEST, "csharp", "001-priority")

    def generate(self, previous=None, feedback=None):
        return self.adapter.generate(self.payload, previous, self.payload["source"], feedback, time.monotonic() + 30)

    def test_same_exact_count_context_and_instructions_on_every_continuation(self):
        first = self.generate()
        second = self.generate(first["id"], {"text": "ERROR fixture"})
        self.assertFalse(first.get("batch_stop", False))
        self.assertFalse(second.get("batch_stop", False))
        for count, create in zip(self.transport.calls[::2], self.transport.calls[1::2]):
            self.assertEqual(count[1], {k: v for k, v in create[1].items()
                                       if k not in {"service_tier", "max_output_tokens", "store", "stream"}})
            self.assertEqual(create[1]["instructions"], self.payload["instructions"])
            self.assertEqual(create[1]["tools"], [])
            self.assertEqual(create[1]["reasoning"], {"effort": "high", "context": "all_turns"})
        self.assertEqual(self.transport.calls[-1][1]["previous_response_id"], first["id"])
        self.assertEqual(self.guard.count_calls, 2)
        self.assertEqual(self.guard.committed, self.guard.cost(20, 12))
        self.assertIsNone(self.guard.entries[0]["usage"]["cache_write_input_tokens"])
        names = [event["event"] for event in self.events]
        self.assertLess(names.index("generation-reserved"), names.index("generation-dispatch"))

    def test_decimal_envelope_including_cache_write_premium(self):
        for _ in range(72):
            self.guard.before_count()
            self.guard.reserve(32768)
        self.assertEqual(self.guard.committed, Decimal("1.2976128"))
        self.assertEqual(self.guard.cost(32768, 8192) * 2, Decimal("0.0360448"))
        with self.assertRaises(GuardFailure):
            self.guard.before_count()

    def test_adapter_and_controller_initial_repair_usage_and_lineage(self):
        def development(source, index, deadline):
            return {"passed": index == 1, "build_passed": True, "category": "development",
                    "output": "ERROR fixture: wrong response" if index == 0 else ""}
        trajectory = run_trajectory(self.payload["source"], "csharp", SPEC,
            lambda p, s, f, d: self.adapter.generate(self.payload, p, s, f, d), development, task_id="001-priority")
        self.assertEqual(len(trajectory["rounds"]), 2)
        self.assertEqual(trajectory["first_phase_usage"]["input_tokens"], 10)
        self.assertEqual(trajectory["repair_usage"]["input_tokens"], 10)
        self.assertEqual(trajectory["total_usage"]["output_tokens"], 12)
        self.assertEqual(trajectory["rounds"][1]["previous_response_id"], "mock-1")
        self.assertFalse(trajectory["rounds"][0]["development"]["passed"])
        self.assertEqual(self.guard.count_calls, 2)

    def test_count_overflow_or_failure_never_dispatches_generation(self):
        for value in [32769, -1, True, None]:
            with self.subTest(value=value):
                self.setUp()
                self.transport.count = value
                result = self.generate()
                self.assertTrue(result["batch_stop"])
                self.assertEqual(len(self.transport.calls), 1)
                self.assertEqual(self.guard.entries, [])
        self.setUp()
        self.transport.fail = "/v1/responses/input_tokens"
        self.assertTrue(self.generate()["batch_stop"])
        self.assertEqual(len(self.transport.calls), 1)

    def test_count_and_generation_ceilings_and_ancillary_charge(self):
        card = {**rates(HISTORICAL_SPEC), "count_call_upper_usd": "0.001"}
        guard = BudgetGuard(HISTORICAL_SPEC, max_requests=2, usd_ceiling="0.05", rates=card, checked_date=card["checked_date"])
        guard.before_count()
        self.assertEqual(guard.committed, Decimal("0.001"))
        guard.reserve(32768)
        guard.before_count()
        guard.reserve(32768)
        self.assertEqual(guard.committed, Decimal("0.0380448"))
        with self.assertRaises(GuardFailure):
            guard.before_count()

    def test_small_budget_and_deadline_fail_before_dispatch(self):
        self.guard.ceiling = Decimal("0.001")
        self.assertTrue(self.generate()["batch_stop"])
        self.assertEqual(self.transport.calls, [])
        self.setUp()
        result = self.adapter.generate(self.payload, None, self.payload["source"], None, time.monotonic() - 1)
        self.assertTrue(result["batch_stop"])
        self.assertEqual(self.transport.calls, [])

    def test_reservation_after_count_can_exhaust_without_generation(self):
        self.guard.ceiling = Decimal("0.010")
        self.transport.count = 32768
        self.assertTrue(self.generate()["batch_stop"])
        self.assertEqual(len(self.transport.calls), 1)
        self.assertEqual(self.guard.entries, [])

    def test_ambiguous_generation_keeps_full_reservation_without_retry(self):
        self.transport.fail = "/v1/responses"
        result = self.generate()
        self.assertTrue(result["batch_stop"])
        self.assertEqual(len(self.transport.calls), 2)
        self.assertEqual(self.guard.entries[0]["state"], "held-unreconciled")
        self.assertEqual(self.guard.committed, self.guard.cost(10, 8192))
        self.assertTrue(self.guard.entries[0]["dispatch_attempted"])

    def test_usage_lineage_tier_model_and_effective_context_are_checked(self):
        changes = [{"usage": {"input_tokens": 10}}, {"usage": {"input_tokens": 11, "output_tokens": 6}},
            {"usage": {"input_tokens": 10, "output_tokens": 6, "input_tokens_details": {"cached_tokens": 11}}},
            {"previous_response_id": "wrong"}, {"service_tier": "priority"}, {"model": "other"},
            {"reasoning": {"effort": "high", "context": "current_turn"}}, {"status": "incomplete"}]
        for change in changes:
            with self.subTest(change=change):
                self.setUp()
                self.transport.change = lambda body: {**body, **change}
                result = self.generate()
                self.assertTrue(result["batch_stop"])
                self.assertEqual(result["text"], '{"files":{}}')
                self.assertEqual(self.guard.entries[0]["state"], "held-unreconciled")
                self.assertEqual(len(self.transport.calls), 2)

    def test_rate_assumptions_and_disabled_live_path_fail_closed(self):
        for change in [{"service_tier": "flex"}, {"input_reservation_rate": "0.20"},
                       {"checked_date": "2000-01-01"}, {"count_call_upper_usd": None},
                       {"count_call_upper_usd": "NaN"}, {"count_call_upper_usd": "oops"}]:
            with self.subTest(change=change), self.assertRaises(GuardFailure):
                BudgetGuard(HISTORICAL_SPEC, max_requests=72, usd_ceiling="2", rates={**rates(HISTORICAL_SPEC), **change},
                            checked_date=rates(HISTORICAL_SPEC)["checked_date"])
        with self.assertRaises(GuardFailure):
            HttpTransport("fixture-not-a-key")
        with self.assertRaises(GuardFailure):
            ResponsesAdapter(HISTORICAL_SPEC, HttpTransport("fixture-not-a-key", enabled=True), self.guard, record=lambda _: None)


class CorrectionTests(unittest.TestCase):
    def test_oauth_replay_overflow_is_pre_dispatch_and_no_feedback(self):
        payload = candidate_payload(ROOT, MANIFEST, "csharp", "001-priority")
        payload["instructions"] = "x" * 200
        spec = copy.deepcopy(SPEC)
        spec["authority"]["max_replay_bytes"] = 32
        transport = MockTransport()
        adapter = CodexOAuthAdapter(spec, transport)
        result = adapter.generate(payload, None, payload["source"], None, time.monotonic() + 30)
        self.assertEqual(result["failure"], "trajectory-input-byte-budget-exhausted")
        self.assertEqual(transport.calls, [])

    def test_oauth_invalid_native_jsonl_sequence_fails_closed(self):
        raw = b'{"type":"turn.completed","usage":{"input_tokens":1,"output_tokens":1}}\n'
        parsed = parse_cli_jsonl(raw)
        self.assertNotEqual(parsed["status"], "completed")

    def test_oauth_large_completed_reply_retains_raw_and_stops_without_build(self):
        payload = candidate_payload(ROOT, MANIFEST, "csharp", "001-priority")
        class Large(MockTransport):
            def __init__(self, output_tokens):
                super().__init__(lambda body: "x" * 50000)
                self.output_tokens = output_tokens
            def launch(self, stdin, timeout):
                self.calls.append(("codex-exec", bytes(stdin), timeout))
                return {"stdout": "\n".join([
                    json.dumps({"type": "thread.started"}), json.dumps({"type": "turn.started"}),
                    json.dumps({"type": "item.completed", "item": {"type": "agent_message", "text": "x" * 50000}}),
                    json.dumps({"type": "turn.completed", "usage": {"input_tokens": 10, "output_tokens": self.output_tokens}}), ""]),
                        "stderr": "", "returncode": 0, "timed_out": False,
                        "output_overflow": False, "cleanup_confirmed": True}
        for output_tokens, expected_batch_stop, expected_stop in [
            (6, False, "terminal-submission-byte-budget-exhausted"),
            (9000, True, "reported-request-budget-exceeded"),
        ]:
            transport = Large(output_tokens)
            adapter = CodexOAuthAdapter(SPEC, transport)
            evaluated = []
            result = run_trajectory(payload["source"], "csharp", SPEC,
                lambda previous, source, feedback, deadline: adapter.generate(payload, previous, source, feedback, deadline),
                lambda source, index, deadline: evaluated.append(index) or {"passed": True, "build_passed": True, "category": "development", "output": ""},
                task_id="001-priority")
            self.assertEqual(len(result["rounds"]), 1)
            self.assertEqual(evaluated, [])
            self.assertEqual(result["stop"], expected_stop)
            self.assertEqual(result["batch_stop"], expected_batch_stop)
            self.assertIsNone(result["terminal_submission_source"])
            self.assertEqual(len(result["rounds"][0]["submission"]), 50000)

    def test_safe_compile_mistakes_are_retained_then_repaired(self):
        before = snapshot(ROOT, MANIFEST, "fsharp", 6)
        target = snapshot(ROOT, MANIFEST, "fsharp", 7)
        project = "OrderFlow.fsproj"
        good = target[project]
        mistakes = [good.replace('    <Compile Include="OrderFlowEngine.fs" />\n', ""),
            good.replace("OrderFlowEngine.fs", "Other.fs"),
            good.replace('<Compile Include="Program.fs" />', '<Compile Include="Program.fs" /><Compile Include="Program.fs" />'),
            good.replace("OrderFlowEngine.fs", "Temp.fs").replace("Program.fs", "OrderFlowEngine.fs").replace("Temp.fs", "Program.fs"),
            good.replace("</Project>", "</Project")]
        for mistake in mistakes:
            with self.subTest(project=mistake):
                raw = json.dumps({"files": {**target, project: mistake}})
                retained = apply_submission(before, raw, "fsharp", SPEC)
                self.assertEqual(retained[project], mistake)
                self.assertFalse(project_development(retained, "fsharp")["passed"])
                replies = iter([raw, json.dumps({"files": {project: good}})])
                evaluations = []
                def session(previous, source, feedback, deadline):
                    return {"id": "first" if previous is None else "repair", "status": "completed", "text": next(replies),
                            "usage": {"input_tokens": 10, "output_tokens": 6}}
                def develop(source, index, deadline):
                    evaluations.append(index)
                    return {"passed": True, "build_passed": True, "category": "development", "output": ""}
                trajectory = run_trajectory(before, "fsharp", SPEC, session, develop, task_id="007-query-engine-refactor")
                self.assertEqual(evaluations, [1])  # invalid project was never executed
                self.assertFalse(trajectory["rounds"][0]["development"]["passed"])
                self.assertEqual(trajectory["terminal_submission_source"], target)

    def test_forbidden_xml_even_when_malformed_is_terminal(self):
        before = snapshot(ROOT, MANIFEST, "fsharp", 6)
        for text in ['<Project><Import', '<Project><Target', '<Project><Compile Include="../x.fs" /></Project>',
                     '<Project><Compile Include="../x.fs"', '<Project><TargetFramework>net9.0</TargetFramework>',
                     '<Project><Compile Include="$(X).fs"', '<Project><PackageReference', '<!DOCTYPE Project>']:
            with self.subTest(text=text), self.assertRaises(PolicyViolation):
                apply_submission(before, json.dumps({"files": {"OrderFlow.fsproj": text}}), "fsharp", SPEC)

    def test_architecture_unknown_failure_and_alternative_naming(self):
        for language in SPEC["languages"]:
            for name, source in fixtures.architecture_fixtures(MANIFEST, language).items():
                row = {"submission": json.dumps({"files": source}), "applied_source": source}
                args = {"task_id": "007-query-engine-refactor", "language": language}
                score = score_submission(row, {"passed": True, "build_passed": True}, **args)
                self.assertIs(score["task_completion"], False if name == "unchanged" else None)
                self.assertTrue(score["build_and_behavior"])
                review = fixtures.fixture_review(source, name == "alternative-naming")
                score = score_submission(row, {"passed": True, "build_passed": True}, **args,
                                         review=review, allow_fixture_review=True)
                self.assertEqual(score["task_completion"], name == "alternative-naming")
                with self.assertRaises(ValueError):
                    score_submission(row, None, **args, review=review)
                with self.assertRaises(ValueError):
                    score_submission(row, None, **args, review={**review, "source_sha256": "mismatch"}, allow_fixture_review=True)

    def trajectory(self, outputs):
        before = snapshot(ROOT, MANIFEST, "csharp", 0)
        return run_trajectory(before, "csharp", SPEC, lambda p, s, f, d: {
            "id": "first" if p is None else p + "r", "status": "completed", "text": '{"files":{}}',
            "usage": {"input_tokens": 10, "output_tokens": 6}},
            lambda s, i, d: {"passed": False, "build_passed": False, "category": "build", "output": outputs[i]},
            task_id="001-priority")

    def test_feedback_early_final_warning_and_malformed_cases(self):
        huge = "error FS0001: " + "x" * 9000
        early = self.trajectory([huge])
        self.assertEqual(early["stop"], "feedback-budget-exhausted")
        self.assertFalse(early["batch_stop"])
        with patch("alf.workstream_e3a.feedback_packet", wraps=feedback_packet) as feedback:
            final = self.trajectory(["error E: failed", "error E: failed", huge])
            self.assertEqual(feedback.call_count, 2)
        self.assertEqual(final["stop"], "repair-budget")
        self.assertIsNone(final["rounds"][-1]["feedback"])
        warnings = self.trajectory(["warning W: " + "x" * 9000] * 3)
        self.assertEqual(len(warnings["rounds"]), 3)
        self.assertFalse(warnings["rounds"][0]["feedback"]["essential_error_overflow"])
        malformed = self.trajectory([None])
        self.assertEqual(malformed["stop"], "controller-feedback-failure")
        self.assertTrue(malformed["batch_stop"])


class BatchTests(unittest.TestCase):
    def run_fixture(self, output, *, fail_first=False, ambiguous=False, card=None, held=True):
        def answer(body):
            if "transcript" in body:
                prompt = body["transcript"][0]["data"]
                prompt["source"] = body["transcript"][-1]["data"]["source"]
            else:
                prompt = json.loads(body["input"][0]["content"])
            stage = next(i + 1 for i, task in enumerate(MANIFEST["tasks"])
                         if (ROOT / task["prompt"]).read_text(encoding="utf-8") == prompt["current_task"])
            language = "fsharp" if "OrderFlow.fsproj" in prompt["source"] else "csharp"
            return json.dumps({"files": snapshot(ROOT, MANIFEST, language, stage)})
        transport = MockTransport(answer)
        if ambiguous:
            transport.fail = "/v1/responses"
        evaluations = []
        class Evaluator:
            def prepare(self):
                return {"mock": True}
            def evaluate(self, source, cases, deadline):
                evaluations.append(cases)
                failing = fail_first and len(evaluations) == 2
                holdout = any(case["name"] == "priority-extremes-default-and-ordinal-ties" for case in cases)
                return {"passed": not failing and (held or not holdout), "build_passed": not failing,
                        "category": "build" if failing else "development",
                        "output": "ERROR fixture: " + "x" * 9000 if failing else ""}
            def close(self):
                pass
        report = run_batch(ROOT, MANIFEST, SPEC, transport=transport,
                           evaluator_factory=lambda lang: Evaluator(), output=output,
                           runner_git_commit="mock-only", phase="pilot", max_dispatches=72)
        return report, transport

    def test_all_slots_retained_feedback_exhaustion_does_not_stop_batch(self):
        with tempfile.TemporaryDirectory() as tmp:
            report, transport = self.run_fixture(Path(tmp) / "run", fail_first=True)
            self.assertEqual(report["summary"]["assigned"], 24)
            self.assertEqual(report["summary"]["started"], 24)
            self.assertEqual(report["slots"][0]["reason"], "feedback-budget-exhausted")
            self.assertIsNone(report["batch_stop"])
            self.assertEqual(report["dispatches"], 24)
            self.assertIsNone(report["generation_requests"])
            self.assertIsNone(report["count_http_calls"])
            self.assertEqual(report["candidate_model_calls"], 0)
            self.assertEqual(len(report["summary"]["paired_first_completion"]), 12)
            self.assertTrue(all(row["scores"]["first"]["task_completion"] is None for row in report["slots"]
                                if row["task_id"] == "007-query-engine-refactor" and row != report["slots"][0]))
            self.assertTrue((Path(tmp) / "run/attempts.jsonl").is_file())
            with self.assertRaises(FileExistsError):
                self.run_fixture(Path(tmp) / "run")

    def test_holdout_cannot_change_request_sequence(self):
        with tempfile.TemporaryDirectory() as tmp:
            a, ta = self.run_fixture(Path(tmp) / "a", held=True)
            b, tb = self.run_fixture(Path(tmp) / "b", held=False)
            self.assertEqual([(p, v) for p, v, _ in ta.calls], [(p, v) for p, v, _ in tb.calls])
            self.assertNotEqual(a["summary"]["paired_first_completion"], b["summary"]["paired_first_completion"])

    def test_ambiguous_stops_without_replay_retains_unstarted_and_reservation(self):
        with tempfile.TemporaryDirectory() as tmp:
            report, transport = self.run_fixture(Path(tmp) / "run", ambiguous=True)
            self.assertEqual(report["dispatches"], 1)
            self.assertEqual(sum(row["status"] == "unstarted" for row in report["slots"]), 23)
            self.assertEqual(report["reservations"], [])
            self.assertIsNone(report["summary"]["observed_usage"]["input_tokens"])

    def test_rate_rejection_preserves_every_assignment_without_dispatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                run_batch(ROOT, MANIFEST, SPEC, transport=MockTransport(),
                          evaluator_factory=lambda lang: None, output=Path(tmp) / "run",
                          runner_git_commit="mock-only", phase="integration", max_dispatches=72)


class SandboxUnitTests(unittest.TestCase):
    def test_fixture_spec_isolated_from_active_authorization(self):
        active = copy.deepcopy(SPEC)
        active["execution_authorized"] = True
        fixture = sandbox_check.model_free_spec(active)
        self.assertTrue(active["execution_authorized"])
        self.assertFalse(fixture["execution_authorized"])
        expected = {**active, "execution_authorized": False}
        self.assertEqual(fixture, expected)
        self.assertIsNot(fixture["environment"], active["environment"])
        self.assertEqual(fixture["environment"], active["environment"])
        self.assertEqual(fixture["model"], active["model"])
        with patch("alf.e3a_sandbox.os.name", "posix"), self.assertRaisesRegex(
                SandboxFailure, "fixture image cannot replace"):
            DockerEvaluator(ROOT, MANIFEST, active, "csharp", fixture_image_id="fixture-image")

    def test_admin_failure_keeps_bounded_diagnostic(self):
        evaluator = DockerEvaluator.__new__(DockerEvaluator)
        evaluator.base, evaluator.docker = ROOT, ["docker"]
        failure = ProcessResult(["docker", "inspect"], 1, "", "missing tmpfs source: " + "x" * 5000, 0)
        with patch("alf.e3a_sandbox.run_process", return_value=failure), self.assertRaises(SandboxFailure) as raised:
            evaluator._admin(["inspect", "fixture"])
        self.assertIn("missing tmpfs source:", str(raised.exception))
        self.assertIn("[truncated]", str(raised.exception))
        self.assertLess(len(str(raised.exception)), 4200)

    def test_trusted_export_and_cleanup_never_use_docker_cp_or_change_mount_roots(self):
        with tempfile.TemporaryDirectory() as tmp:
            evaluator = DockerEvaluator.__new__(DockerEvaluator)
            evaluator.spec, evaluator.language, evaluator.project = SPEC, "csharp", "OrderFlow.csproj"
            evaluator.baseline = snapshot(ROOT, MANIFEST, "csharp", 0)
            evaluator.base = Path(tmp)
            evaluator.cache, evaluator.seed = Path(tmp) / "packages", Path(tmp) / "seed"
            evaluator.cache.mkdir()
            evaluator.seed.mkdir()
            evaluator.prepared_identity = None
            evaluator.image, evaluator.fixture_only, evaluator.evidence = "fixture", True, []
            commands, mounts, administration, removed = [], [], [], []
            def execute(name, command, timeout):
                commands.append(command)
                return {"returncode": 0, "stdout": "10.0.302" if command == ["dotnet", "--version"] else "",
                        "stderr": "", "timed_out": False, "output_limit_exceeded": False}
            def create(values):
                mounts.extend(values)
                return "fixture"
            def admin(args):
                administration.append(args)
                return "fixture"
            evaluator._exec, evaluator._admin = execute, admin
            evaluator._create, evaluator._remove = create, removed.append
            result = evaluator.prepare()
            self.assertIn(["cp", "-R", "/work/obj", "/work/packages.lock.json", "/seed-out/"], commands)
            self.assertIn(["find", "/packages", "/seed-out", "-mindepth", "1", "-exec", "chmod", "a+rwX", "{}", "+"], commands)
            self.assertIn((evaluator.seed, "/seed-out", True), mounts)
            self.assertNotIn("cp", [args[0] for args in administration])
            self.assertEqual(removed, ["fixture"])
            self.assertEqual(result["export"]["returncode"], 0)

            # A partial restore must still permit host-side cleanup and remove
            # the container. It must not publish a usable prepared identity.
            evaluator.prepared_identity = None
            (evaluator.base / "restore-input").rename(evaluator.base / "first-restore-input")
            commands.clear()
            def fail_restore(name, command, timeout):
                result = execute(name, command, timeout)
                if command[0] == "/bin/sh":
                    result.update(returncode=1, stderr="fixture restore failure")
                return result
            evaluator._exec = fail_restore
            with self.assertRaisesRegex(SandboxFailure, "fixture restore failure"):
                evaluator.prepare()
            self.assertTrue(any(command[0] == "find" for command in commands))
            self.assertFalse(any(command[0] == "cp" for command in commands))
            self.assertEqual(removed, ["fixture", "fixture"])
            self.assertIsNone(evaluator.prepared_identity)

    def test_container_policy_has_no_host_workspace_credentials_or_network(self):
        with tempfile.TemporaryDirectory() as tmp:
            args = container_arguments("fixture", SPEC["environment"]["container_image_id"], SPEC["environment"],
                                       [(Path(tmp), "/input", False)])
            for option, value in [("--network", "none"), ("--user", "1000:1000"), ("--pids-limit", "512"),
                                  ("--memory", "6442450944"), ("--memory-swap", "6442450944")]:
                self.assertEqual(args[args.index(option) + 1], value)
            self.assertIn("--read-only", args)
            self.assertTrue(args[args.index("--mount") + 1].endswith(",readonly"))
            self.assertNotIn("auth.json", " ".join(args))
            self.assertNotIn("docker.sock", " ".join(args))
            self.assertNotIn(str(ROOT), " ".join(args))
            with self.assertRaises(SandboxFailure):
                container_arguments("fixture", "mutable:tag", SPEC["environment"], [])

    def test_candidate_evaluation_cannot_write_the_preparation_export_mount(self):
        with tempfile.TemporaryDirectory() as tmp:
            evaluator = DockerEvaluator.__new__(DockerEvaluator)
            evaluator.spec, evaluator.language, evaluator.project = SPEC, "csharp", "OrderFlow.csproj"
            evaluator.baseline = snapshot(ROOT, MANIFEST, "csharp", 0)
            evaluator.base = Path(tmp)
            evaluator.seed, evaluator.cache = Path(tmp) / "seed", Path(tmp) / "packages"
            evaluator.seed.mkdir()
            evaluator.cache.mkdir()
            evaluator.prepared_identity = (tree_identity(evaluator.seed), tree_identity(evaluator.cache))
            evaluator.evidence = []
            mounts, commands, removed = [], [], []
            def create(values):
                mounts.extend(values)
                return "fixture"
            def execute(name, command, timeout, input_text=""):
                commands.append(command)
                return {"returncode": 0 if command[0] == "/bin/sh" else 1,
                        "stdout": "", "stderr": "", "timed_out": False, "output_limit_exceeded": False}
            evaluator._create, evaluator._exec, evaluator._remove = create, execute, removed.append
            result = evaluator.evaluate(evaluator.baseline, [], time.monotonic() + 5)
            self.assertEqual({target: writable for _, target, writable in mounts},
                             {"/input": False, "/seed": False, "/packages": False})
            self.assertFalse(result["build_passed"])
            self.assertIsNone(result["binary_sha256"])
            self.assertEqual(len(commands), 2)  # copy + failing build; no program
            self.assertEqual(removed, ["fixture"])

    def test_windows_has_no_host_execution_fallback(self):
        with patch("alf.e3a_sandbox.os.name", "nt"), self.assertRaises(SandboxFailure):
            DockerEvaluator(ROOT, MANIFEST, SPEC, "csharp")

    def test_complete_workspace_is_not_limited_to_one_response_envelope(self):
        evaluator = DockerEvaluator.__new__(DockerEvaluator)
        evaluator.spec, evaluator.language, evaluator.project = SPEC, "csharp", "OrderFlow.csproj"
        evaluator.baseline = snapshot(ROOT, MANIFEST, "csharp", 0)
        evaluator.prepared_identity = None
        source = {**evaluator.baseline, "Program.cs": "//" + "x" * 50000}
        # Reaches preparation enforcement, not a fictitious response-size error.
        with self.assertRaisesRegex(SandboxFailure, "prepared dependency"):
            evaluator.evaluate(source, [], time.monotonic() + 1)

    def test_bounded_client_output_and_deadline(self):
        # Trusted helper processes only; NOT sandbox/candidate execution evidence.
        result = bounded_process([sys.executable, "-c", "print('x'*100000)"], timeout=5, output_limit=1024)
        self.assertTrue(result["output_limit_exceeded"])
        self.assertLessEqual(len(result["stdout"].encode()) + len(result["stderr"].encode()), 1024)
        result = bounded_process([sys.executable, "-c", "import time; time.sleep(5)"], timeout=0.1)
        self.assertTrue(result["timed_out"])
        with self.assertRaises(SandboxFailure):
            bounded_process(["not-launched"], timeout=0)


if __name__ == "__main__":
    unittest.main()
