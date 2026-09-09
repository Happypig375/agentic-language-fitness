import importlib.util, json, tempfile, unittest
from pathlib import Path
from unittest.mock import patch

from alf.h import HBoundaryError
from alf.h_run import policy_sha, require_live_authority, run_integration, run_pilot, verify_pilot_freeze
from alf.protocol import canonical_json_hash
from tests.test_h import Offline, SOURCE, SPEC as SUBMISSION_SPEC, cli

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("h_run_script", ROOT / "scripts/h_run.py")
SCRIPT = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(SCRIPT)


class HRunTests(unittest.TestCase):
    @staticmethod
    def live_spec():
        return {"execution_authorized": True, "user_live_execution_approved": True,
                "approved_integration_dispatches": 5, "approved_pilot_dispatches": 64,
                "analysis": {"human_review_approved": True},
                "authority": dict(SUBMISSION_SPEC["authority"]),
                "budgets": {"trajectory_timeout_seconds": 600}}

    def test_policy_identity_excludes_only_nested_activation_bookkeeping(self):
        spec = {"model": {"requested": "m", "actual_version": "v", "h_live_integration_verified": False},
                "analysis": {"human_review_approved": False, "required_architecture": ["x"]},
                "workload": {"public_payload_sha256": "a"}}
        baseline = policy_sha(spec)
        changed = json.loads(json.dumps(spec))
        changed["model"]["h_live_integration_verified"] = True
        changed["analysis"]["human_review_approved"] = True
        self.assertEqual(policy_sha(changed), baseline)
        for section, key in (("model", "requested"), ("model", "actual_version"),
                             ("analysis", "required_architecture"), ("workload", "public_payload_sha256")):
            changed = json.loads(json.dumps(spec)); changed[section][key] = "changed"
            self.assertNotEqual(policy_sha(changed), baseline)
    def test_default_denial_precedes_live_path_reads_and_status(self):
        argv = ["--phase", "pilot", "--native-binary", "native", "--native-sha256", "x",
                "--model-catalog", "catalog", "--auth-file", "auth", "--output", "out"]
        with patch.object(SCRIPT, "_read", return_value={"execution_authorized": False}), \
             patch.object(SCRIPT, "_sha") as sha, patch.object(SCRIPT.subprocess, "run") as run, \
             patch.object(SCRIPT, "verified_construction") as construction, self.assertRaises(SystemExit):
            SCRIPT.main(argv)
        sha.assert_not_called(); run.assert_not_called(); construction.assert_not_called()

    def test_exact_shared_guards(self):
        base = {"execution_authorized": True, "user_live_execution_approved": True,
                "approved_integration_dispatches": 5, "approved_pilot_dispatches": 64,
                "analysis": {"human_review_approved": True}}
        self.assertEqual(require_live_authority(base, "integration"), 5)
        self.assertEqual(require_live_authority(base, "pilot"), 64)
        for key in ("approved_integration_dispatches", "approved_pilot_dispatches"):
            changed = dict(base); changed[key] -= 1
            with self.assertRaises(HBoundaryError):
                require_live_authority(changed, "integration" if "integration" in key else "pilot")

    def test_integration_composed_three_calls_require_behavior_and_exact_read(self):
        spec = self.live_spec()
        actions = ('{"action":"submit","files":{}}',
                   '{"action":"read","paths":["Program.cs"]}',
                   '{"action":"submit","files":{}}')
        source = {"OrderFlow.csproj": SOURCE["OrderFlow.csproj"], "Program.cs": "class Program {}"}
        with tempfile.TemporaryDirectory() as temporary:
            report = run_integration(spec, transport=Offline([cli(x) for x in actions]),
                evaluator=lambda _source, _deadline: {"passed": True}, source=source,
                order=list(source), submission_spec=SUBMISSION_SPEC,
                output=Path(temporary) / "pass")
            self.assertTrue(report["passed"])
            rows = [json.loads(x) for x in (Path(temporary) / "pass/attempts.jsonl").read_text().splitlines()]
            self.assertEqual(sum(row["event"] == "dispatch-debited" for row in rows), 3)
        for outputs, evaluator, reason in (
            ([cli(x) for x in actions], lambda _source, _deadline: {"passed": False}, "integration-behavior-failed"),
            ([cli(actions[0]), cli('{"action":"read","paths":["OrderFlow.csproj"]}'), cli(actions[2])],
             lambda _source, _deadline: {"passed": True}, "integration-H2-read-transition-mismatch")):
            with self.subTest(reason=reason), tempfile.TemporaryDirectory() as temporary:
                report = run_integration(spec, transport=Offline(outputs), evaluator=evaluator, source=source,
                    order=list(source), submission_spec=SUBMISSION_SPEC, output=Path(temporary) / "fail")
                self.assertEqual(report["batch_stop"], reason)

    def test_pilot_retains_all_32_slots_for_candidate_failure_and_hard_stop(self):
        construction = {"feasibility_mask": [
            {"slot": n, "feasible": True, "level": "core", "language": "csharp",
             "file_order": "forward", "access": "H1", "cap_bytes": 131072}
            for n in range(1, 33)]}
        source = {"OrderFlow.csproj": SOURCE["OrderFlow.csproj"], "Program.cs": "class Program {}"}
        class Evaluator:
            def prepare(self): return {"passed": True}
            def evaluate(self, _source, _cases, _deadline): return {"passed": False}
            def close(self): pass
        patches = (patch("alf.h_run.source_for", return_value=source),
                   patch("alf.h_run.ordered_filenames", return_value=list(source)),
                   patch("alf.h_run.public_payload", return_value={}),
                   patch("alf.h_run.cases_for", return_value=[]))
        for item in patches: item.start()
        self.addCleanup(lambda: [item.stop() for item in reversed(patches)])
        submit = cli('{"action":"submit","files":{}}')
        with tempfile.TemporaryDirectory() as temporary:
            report = run_pilot(ROOT, self.live_spec(), construction,
                transport=Offline([submit] * 32), evaluator_factory=lambda *_: Evaluator(),
                output=Path(temporary) / "wrong", runtime={})
            self.assertEqual((len(report["slots"]), report["dispatches"], report["batch_stop"]), (32, 32, None))
            self.assertTrue(all(slot["status"] == "finished" for slot in report["slots"]))
        with tempfile.TemporaryDirectory() as temporary:
            report = run_pilot(ROOT, self.live_spec(), construction,
                transport=Offline([submit], cleanup_confirmed=False), evaluator_factory=lambda *_: Evaluator(),
                output=Path(temporary) / "hard", runtime={})
            self.assertEqual(len(report["slots"]), 32)
            self.assertEqual(report["batch_stop"], "cleanup-unconfirmed")
            self.assertEqual(sum(slot["status"] == "unstarted" for slot in report["slots"]), 31)

    def test_freeze_binds_report_policy_phase_and_every_runtime_identity(self):
        spec = self.live_spec(); runtime = {"source_sha256": {"a.py": "one", "b.py": "two"},
                                            "native_sha256": "native", "container_image_id": "image"}
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); protocol = root / "protocols/workstream-h1-h2"; protocol.mkdir(parents=True)
            results = root / "results"; results.mkdir()
            report = {"phase": "integration", "policy_sha256": policy_sha(spec), "passed": True,
                      "dispatches": 3, "batch_stop": None, "runtime": runtime}
            raw = (json.dumps(report, sort_keys=True) + "\n").encode(); (results / "report.json").write_bytes(raw)
            freeze = {"specification_sha256": canonical_json_hash(spec), "policy_sha256": policy_sha(spec),
                      "integration_report": "results/report.json",
                      "integration_report_sha256": __import__("hashlib").sha256(raw).hexdigest()}
            (protocol / "freeze.json").write_text(json.dumps(freeze))
            verify_pilot_freeze(root, spec, runtime)
            for field, value in (("phase", "pilot"), ("policy_sha256", "old")):
                changed = dict(report); changed[field] = value
                changed_raw = (json.dumps(changed, sort_keys=True) + "\n").encode()
                (results / "report.json").write_bytes(changed_raw)
                freeze["integration_report_sha256"] = __import__("hashlib").sha256(changed_raw).hexdigest()
                (protocol / "freeze.json").write_text(json.dumps(freeze))
                with self.assertRaises(HBoundaryError): verify_pilot_freeze(root, spec, runtime)
            (results / "report.json").write_bytes(raw)
            freeze["integration_report_sha256"] = __import__("hashlib").sha256(raw).hexdigest()
            (protocol / "freeze.json").write_text(json.dumps(freeze))
            changed_spec = json.loads(json.dumps(spec)); changed_spec["authority"]["max_total_files"] = 7
            freeze["specification_sha256"] = canonical_json_hash(changed_spec)
            freeze["policy_sha256"] = policy_sha(changed_spec)
            (protocol / "freeze.json").write_text(json.dumps(freeze))
            with self.assertRaises(HBoundaryError): verify_pilot_freeze(root, changed_spec, runtime)
            freeze["specification_sha256"], freeze["policy_sha256"] = canonical_json_hash(spec), policy_sha(spec)
            (protocol / "freeze.json").write_text(json.dumps(freeze))
            for changed_runtime in ({**runtime, "native_sha256": "changed"},
                                    {**runtime, "source_sha256": {"a.py": "one", "b.py": "changed"}},
                                    {**runtime, "source_sha256": {"a.py": "one"}}):
                with self.assertRaises(HBoundaryError): verify_pilot_freeze(root, spec, changed_runtime)


if __name__ == "__main__": unittest.main()
