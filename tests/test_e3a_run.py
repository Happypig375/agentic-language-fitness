import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).parents[1]
spec = importlib.util.spec_from_file_location("e3a_run", ROOT / "scripts/e3a_run.py")
MODULE = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(MODULE)


def fixture():
    s = MODULE.read_json(ROOT / "protocols/workstream-e3a-v1/specification.json")
    m = MODULE.read_json(ROOT / s["manifest"])
    s["execution_authorized"] = True
    s["user_live_execution_approved"] = True
    return s, m


class Transport:
    is_live = False
    def __init__(self, replies=None, usage=None, on_launch=None, startup=False):
        self.replies = list(replies or ['{"files":{"Program.cs":"class Program {}"}}'])
        self.usage = usage or {"input_tokens": 10, "output_tokens": 10}
        self.calls = []; self.on_launch = on_launch; self.startup = startup
    def launch(self, stdin, timeout):
        self.calls.append(bytes(stdin))
        if self.on_launch: self.on_launch(bytes(stdin))
        text = self.replies.pop(0)
        prefix = [json.dumps({"type": "thread.started"})]
        if self.startup:
            prefix.extend(Path(ROOT / "tests/fixtures/e3a-codex-startup-envelope.jsonl").read_text().splitlines()[1:3])
        prefix.extend([json.dumps({"type": "turn.started"})])
        raw = "\n".join([*prefix,
            json.dumps({"type": "item.completed", "item": {"type": "agent_message", "text": text}}),
            json.dumps({"type": "turn.completed", "usage": self.usage}), ""])
        return {"stdout": raw, "stderr": "", "returncode": 0, "timed_out": False,
                "output_overflow": False, "cleanup_confirmed": True}


class Eval:
    def __init__(self, passed=True, close_error=False): self.passed, self.calls, self.closed, self.close_error = passed, [], False, close_error
    def prepare(self): return {"prepared": True}
    def evaluate(self, source, cases, deadline):
        self.calls.append((source, cases))
        return {"passed": self.passed, "build_passed": self.passed, "output": ""}
    def close(self):
        self.closed = True
        if self.close_error: raise RuntimeError("cleanup")


class E3aRunTests(unittest.TestCase):
    def test_two_step_shakedown_accepts_captured_startup_envelope(self):
        s, m = fixture(); t = Transport([json.dumps({"files": {"Program.cs": "class Program {}"}})] * 2, startup=True)
        ev = Eval()
        with tempfile.TemporaryDirectory() as d:
            report = MODULE.run_shakedown(s, m, transport=t, evaluator_factory=lambda: ev,
                                           output=Path(d) / "run", runtime_metadata={}, root=ROOT)
        self.assertTrue(report["passed"])
        self.assertEqual(report["dispatches"], 2)
        self.assertEqual(report["dispatch_ceiling"], 5)
        for call in t.calls:
            self.assertNotIn("Under-development", call.decode())

    def test_two_launches_replay_and_journal_order(self):
        s, m = fixture(); journal_dir = None
        def before_launch(stdin):
            lines = (journal_dir / "attempts.jsonl").read_text().splitlines()
            event = json.loads(lines[-1])
            self.assertEqual(event["event"], "dispatch-debited")
            self.assertEqual(event["stdin_utf8"].encode("utf-8"), stdin)
        programs = ['using System;\nwhile (Console.ReadLine() is not null) Console.WriteLine("{\\"value\\":' + str(value) + '}");\n'
                    for value in (1, 2)]
        replies = [json.dumps({"files": {"Program.cs": source}}) for source in programs]
        t = Transport(replies, on_launch=before_launch)
        ev = Eval()
        runtime = {"runner_git_commit": "fixture-commit"}
        with tempfile.TemporaryDirectory() as d:
            journal_dir = Path(d) / "run"
            report = MODULE.run_shakedown(s, m, transport=t, evaluator_factory=lambda: ev,
                                           output=journal_dir, runtime_metadata=runtime, root=ROOT)
            saved = json.loads((journal_dir / "report.json").read_text())
            self.assertEqual(saved["runtime"], runtime)
            self.assertTrue(saved["passed"])
        self.assertEqual(report["dispatches"], 2)
        self.assertEqual(len(t.calls), 2)
        second = json.loads(t.calls[1])
        self.assertEqual(second["transcript"][1]["role"], "assistant")
        self.assertEqual(second["transcript"][1]["data"], replies[0])
        self.assertEqual(second["transcript"][-1]["data"]["source"]["Program.cs"], programs[0])
        self.assertNotIn("turn.completed", second["transcript"][1]["data"])
        self.assertNotEqual(second["transcript"][-1]["data"]["source"], second["transcript"][0]["data"]["source"])
        self.assertEqual(second["instructions"], json.loads(t.calls[0])["instructions"])
        self.assertEqual(len(ev.calls), 3)  # preflight, value 1, value 2
        self.assertEqual([c[1][0]["expected"]["value"] for c in ev.calls], [0, 1, 2])
        self.assertTrue(report["passed"] and ev.closed)
        self.assertEqual(report["runtime"], runtime)

    def test_integration_ceiling_is_carried_to_guard_and_sixth_debit_is_refused(self):
        s, _ = fixture()
        self.assertEqual(MODULE._integration_dispatch_ceiling(s), 5)
        guard = MODULE.DispatchGuard(MODULE._integration_dispatch_ceiling(s))
        for _ in range(5):
            guard.debit()
        with self.assertRaises(ValueError):
            guard.debit()

    def test_invalid_or_mismatched_integration_ceiling_fails_before_launch(self):
        cases = []
        for value in (True, False, 0, 6, "5", None):
            cases.append(("approved_integration_dispatches", value))
            cases.append(("integration_dispatch_ceiling", value))
        cases.append(("mismatch", 4))
        for field, value in cases:
            s, m = fixture()
            if field == "mismatch":
                s["budgets"]["integration_dispatch_ceiling"] = value
            elif field == "integration_dispatch_ceiling":
                s["budgets"][field] = value
            else:
                s[field] = value
            with tempfile.TemporaryDirectory() as d:
                transport = Transport()
                with self.assertRaises(ValueError):
                    MODULE.run_shakedown(s, m, transport=transport, evaluator_factory=Eval,
                                          output=Path(d) / "run", runtime_metadata={}, root=ROOT)
                self.assertEqual(transport.calls, [])

    def test_ambiguous_first_stops_after_one_dispatch(self):
        s, m = fixture(); ev = Eval()
        class Ambiguous(Transport):
            def launch(self, stdin, timeout):
                self.calls.append(bytes(stdin))
                return {"stdout": "", "stderr": "timeout", "returncode": 124,
                        "timed_out": True, "output_overflow": False, "cleanup_confirmed": True}
        with tempfile.TemporaryDirectory() as d:
            report = MODULE.run_shakedown(s, m, transport=Ambiguous(), evaluator_factory=lambda: ev,
                                           output=Path(d) / "run", runtime_metadata={}, root=ROOT)
        self.assertEqual(report["dispatches"], 1); self.assertEqual(len(ev.calls), 1)

    def test_missing_usage_preserves_known_evaluation_then_stops(self):
        s, m = fixture(); t, ev = Transport(usage={"input_tokens": 10}), Eval()
        with tempfile.TemporaryDirectory() as d:
            report = MODULE.run_shakedown(s, m, transport=t, evaluator_factory=lambda: ev,
                                           output=Path(d) / "run", runtime_metadata={}, root=ROOT)
        self.assertEqual(report["dispatches"], 1); self.assertEqual(len(ev.calls), 2)
        self.assertTrue(report["batch_stop"])

    def test_preflight_failure_has_zero_dispatches(self):
        s, m = fixture(); ev = Eval(passed=False); t = Transport()
        with tempfile.TemporaryDirectory() as d:
            report = MODULE.run_shakedown(s, m, transport=t, evaluator_factory=lambda: ev,
                                           output=Path(d) / "run", runtime_metadata={}, root=ROOT)
        self.assertEqual(report["dispatches"], 0); self.assertEqual(t.calls, [])

    def test_existing_output_refuses_without_factory_or_overwrite(self):
        s, m = fixture(); t = Transport(); called = []
        with tempfile.TemporaryDirectory() as d:
            output = Path(d) / "run"; output.mkdir(); marker = output / "marker"; marker.write_text("keep")
            with self.assertRaises(FileExistsError):
                MODULE.run_shakedown(s, m, transport=t, evaluator_factory=lambda: called.append(1),
                                     output=output, runtime_metadata={}, root=ROOT)
            self.assertEqual(called, []); self.assertEqual(marker.read_text(), "keep")

    def test_cleanup_failure_marks_report_unconfirmed(self):
        s, m = fixture(); t = Transport(); ev = Eval(close_error=True)
        with tempfile.TemporaryDirectory() as d:
            report = MODULE.run_shakedown(s, m, transport=t, evaluator_factory=lambda: ev,
                                           output=Path(d) / "run", runtime_metadata={}, root=ROOT)
        self.assertFalse(report["passed"]); self.assertEqual(report["batch_stop"], "cleanup-unconfirmed")

    def test_invalid_and_oversized_replies_are_not_evaluated(self):
        s, m = fixture()
        for reply in ["not-json", '{"files":{"Program.cs":"' + "x" * 50000 + '"}}']:
            t, ev = Transport([reply]), Eval()
            with tempfile.TemporaryDirectory() as d:
                report = MODULE.run_shakedown(s, m, transport=t, evaluator_factory=lambda: ev,
                                               output=Path(d) / "run", runtime_metadata={}, root=ROOT)
            self.assertEqual(report["dispatches"], 1); self.assertEqual(len(ev.calls), 1)

    def test_main_refuses_held_authorization_before_wrapper_or_output(self):
        args = ["--phase", "shakedown", "--native-binary", "x", "--native-sha256", "x",
                "--model-catalog", "x", "--auth-file", "x", "--output", "missing.json"]
        with patch.object(MODULE, "read_json", return_value={"execution_authorized": False,
                "user_live_execution_approved": True}), self.assertRaises(SystemExit):
            MODULE.main(args)

    def test_docker_transport_forwards_pins_and_uses_fresh_empty_workspace(self):
        s, _ = fixture(); seen = []; workspaces = []
        class Wrapper:
            def run_e3a_cli(self, stdin, **kwargs):
                seen.append((bytes(stdin), kwargs))
                workspace = kwargs["workspace"]
                workspaces.append(workspace)
                assert workspace.is_dir() and not any(workspace.iterdir())
                return {"stdout": "", "stderr": "", "returncode": 1, "timed_out": False,
                        "output_overflow": False, "cleanup_confirmed": True}
        args = type("Args", (), {"native_binary": Path("native"), "native_sha256": "sha",
                                  "model_catalog": Path("catalog"), "auth_file": Path("auth")})()
        transport = MODULE.DockerTransport(args, {"profile_id": "p"}, s)
        with patch.object(transport, "wrapper", Wrapper()):
            for _ in range(2):
                transport.launch(b"{}", 1)
                self.assertFalse(workspaces[-1].exists())
        self.assertEqual(len(seen), 2)
        self.assertNotEqual(workspaces[0], workspaces[1])
        self.assertTrue(all(not path.exists() for path in workspaces))
        for stdin, kwargs in seen:
            self.assertEqual(stdin, b"{}")
            self.assertEqual(kwargs["expected_binary_sha256"], "sha")
            self.assertEqual(kwargs["model_catalog"], Path("catalog"))
            self.assertEqual(kwargs["auth_source"], Path("auth"))
            self.assertEqual(kwargs["native_binary"], Path("native"))
            self.assertEqual(kwargs["image"], s["environment"]["container_image_id"])
            self.assertEqual(kwargs["expected_image_id"], s["environment"]["container_image_id"])
            self.assertEqual(kwargs["environment_profile"], {"profile_id": "p"})
            self.assertEqual(kwargs["model"], s["model"]["requested"])
            self.assertEqual(kwargs["reasoning_effort"], s["model"]["reasoning_effort"])
            self.assertEqual(kwargs["timeout"], 1)

    def test_policy_hash_ignores_activation_flags_but_binds_model_and_limits(self):
        s, _ = fixture()
        altered = dict(s, status="frozen", execution_authorized=False)
        self.assertEqual(MODULE._policy_sha(s), MODULE._policy_sha(altered))
        changed = dict(s, model=dict(s["model"], reasoning_effort="low"))
        self.assertNotEqual(MODULE._policy_sha(s), MODULE._policy_sha(changed))
        changed = dict(s, budgets=dict(s["budgets"], request_input_tokens=1))
        self.assertNotEqual(MODULE._policy_sha(s), MODULE._policy_sha(changed))

    def _freeze_fixture(self, root, *, report=None, freeze=True, runtime=None):
        s, _ = fixture()
        runtime = runtime or {"runner_source_sha256": "source", "native_sha256": "native",
                              "catalog_sha256": "catalog", "container_image_id": "image",
                              "environment_profile_sha256": "profile"}
        report = report or {"scope": "unrelated-two-step-replay-shakedown-not-scientific-trajectories",
            "policy_sha256": MODULE._policy_sha(s), "passed": True, "batch_stop": None,
            "dispatches": 2, "candidate_model_calls": None, "runtime": runtime,
            "attempts": [{"response": {"status": "completed"}, "applied_source": {"x": "y"}, "evaluation": {"passed": True}},
                         {"response": {"status": "completed"}, "applied_source": {"x": "z"}, "evaluation": {"passed": True}}]}
        path = root / "shakedown-report.json"; path.write_text(json.dumps(report), encoding="utf-8")
        if freeze:
            packet = root / "protocols/workstream-e3a-v1"; packet.mkdir(parents=True, exist_ok=True)
            (packet / "freeze.json").write_text(json.dumps({"shakedown_report": "shakedown-report.json",
                "shakedown_report_sha256": MODULE._sha(path), "specification_sha256": MODULE.canonical_json_hash(s),
                "policy_sha256": MODULE._policy_sha(s)}), encoding="utf-8")
        return s, runtime, path

    def test_freeze_prerequisite_accepts_valid_report_and_changed_git_commit(self):
        with tempfile.TemporaryDirectory() as d:
            s, runtime, _ = self._freeze_fixture(Path(d)); runtime["runner_git_commit"] = "different"
            MODULE.verify_pilot_prerequisite(Path(d), s, runtime)

    def test_freeze_prerequisite_rejects_missing_tampered_or_failed_records(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); s, runtime, path = self._freeze_fixture(root)
            path.write_text(path.read_text() + " ", encoding="utf-8")
            with self.assertRaises(ValueError): MODULE.verify_pilot_prerequisite(root, s, runtime)
        for mutate in ("candidate_model_calls", "dispatches", "passed", "attempt_status", "batch_stop", "attempt_applied", "attempt_eval", "policy", "native"):
            with tempfile.TemporaryDirectory() as d:
                root = Path(d); s, runtime, path = self._freeze_fixture(root)
                report = json.loads(path.read_text())
                if mutate == "candidate_model_calls": report["candidate_model_calls"] = 0
                elif mutate == "dispatches": report["dispatches"] = 1
                elif mutate == "passed": report["passed"] = False
                elif mutate == "attempt_status": report["attempts"][0]["response"]["status"] = "failed"
                elif mutate == "batch_stop": report["batch_stop"] = True
                elif mutate == "attempt_applied": report["attempts"][0]["applied_source"] = None
                elif mutate == "attempt_eval": report["attempts"][0]["evaluation"]["passed"] = False
                elif mutate == "policy":
                    s["model"]["reasoning_effort"] = "low"
                    freeze = json.loads((root / "protocols/workstream-e3a-v1/freeze.json").read_text())
                    freeze["specification_sha256"] = MODULE.canonical_json_hash(s)
                    (root / "protocols/workstream-e3a-v1/freeze.json").write_text(json.dumps(freeze), encoding="utf-8")
                else: runtime["native_sha256"] = "changed"
                path.write_text(json.dumps(report), encoding="utf-8")
                freeze = json.loads((root / "protocols/workstream-e3a-v1/freeze.json").read_text())
                freeze["shakedown_report_sha256"] = MODULE._sha(path)
                (root / "protocols/workstream-e3a-v1/freeze.json").write_text(json.dumps(freeze), encoding="utf-8")
                with self.assertRaises(ValueError): MODULE.verify_pilot_prerequisite(root, s, runtime)

    def test_freeze_prerequisite_requires_freeze_file(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); s, runtime, _ = self._freeze_fixture(root)
            (root / "protocols/workstream-e3a-v1/freeze.json").unlink()
            with self.assertRaises(FileNotFoundError): MODULE.verify_pilot_prerequisite(root, s, runtime)

    def test_main_pilot_requires_frozen_status(self):
        args = ["--phase", "pilot", "--native-binary", "x", "--native-sha256", "x",
                "--model-catalog", "x", "--auth-file", "x", "--output", "missing.json"]
        with patch.object(MODULE, "read_json", return_value={"execution_authorized": True,
                "user_live_execution_approved": True, "status": "bounded-implementation-not-frozen"}), self.assertRaises(SystemExit):
            MODULE.main(args)


if __name__ == "__main__":
    unittest.main()
