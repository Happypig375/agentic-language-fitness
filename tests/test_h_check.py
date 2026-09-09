import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from alf import h_check


class HCheckTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).resolve().parents[1]

    def test_cap_formula_rounding(self):
        measurements = [
            {"level": "core", "requests": [{"bytes": 1024}, {"bytes": 2049}]},
            {"level": "expanded", "requests": [{"bytes": 4097}]},
        ]
        self.assertEqual(h_check.derive_caps(measurements), (4096, 6144))

    def test_schedule_is_deterministic_paired_and_complete(self):
        left = h_check.schedule(20260909, (10, 20))
        right = h_check.schedule(20260909, (10, 20))
        self.assertEqual(left, right)
        self.assertEqual(len(left), 32)
        self.assertEqual([x["slot"] for x in left], list(range(1, 33)))
        self.assertEqual({x["pair"] for x in left}, set(range(1, 17)))
        for index in range(0, 32, 2):
            pair = left[index:index + 2]
            self.assertEqual(pair[0]["pair"], pair[1]["pair"])
            self.assertEqual({x["language"] for x in pair}, {"csharp", "fsharp"})
            self.assertEqual({k: pair[0][k] for k in ("level", "cap", "access", "file_order")},
                             {k: pair[1][k] for k in ("level", "cap", "access", "file_order")})
        cells = {(x["level"], x["cap"], x["access"], x["file_order"], x["language"]) for x in left}
        self.assertEqual(len(cells), 32)

    def test_reference_requests_preserve_exact_bytes_residence_and_no_gold(self):
        spec = json.loads((self.root / "protocols/workstream-h1-h2/specification.json").read_text())
        source = {"OrderFlow.csproj": "<Project />", "A.cs": "class A{}", "B.cs": "class B{}",
                  "C.cs": "class C{}", "D.cs": "class D{}"}
        payload = {"task": "public", "earlier_contract": "public"}
        requests, records = h_check.reference_requests(source, list(source), payload, "csharp", "H2", spec)
        self.assertEqual(len(requests), 3)
        self.assertEqual([x["replay_utf8"].encode() for x in records], requests)
        self.assertEqual(records[0]["resident"], [])
        self.assertEqual(set(records[-1]["resident"]), set(source))
        self.assertTrue(all(x["provider_context_limit"] is None and x["subscription_usd"] is None for x in records))

    def test_reference_token_proxy_opt_out_does_not_change_canonical_bytes(self):
        spec = json.loads((self.root / "protocols/workstream-h1-h2/specification.json").read_text())
        source = {"OrderFlow.csproj": "<Project />", "A.cs": "class A{}"}
        args = (source, list(source), {"current_task": "x"}, "csharp", "H2", spec)
        with_proxy, records = h_check.reference_requests(*args)
        with patch.object(h_check.h0, "tokenize", side_effect=AssertionError("tokenizer called")):
            quiet, quiet_records = h_check.reference_requests(*args, include_token_proxy=False)
        self.assertEqual(with_proxy, quiet)
        self.assertTrue(all(record["token_proxy"] is not None for record in records))
        self.assertTrue(all(record["token_proxy"] is None for record in quiet_records))

    def test_public_payload_leak_words_are_rejected(self):
        self.assertTrue(h_check._public_payload_ok({"task": "public"}))
        for key in ("gold", "private_cases", "holdout", "relevance"):
            self.assertFalse(h_check._public_payload_ok({key: "secret"}))

    def test_audit_identity_caps_mask_and_no_live_state(self):
        report = h_check.audit(self.root)
        self.assertEqual(report["status"], "passed", report["failures"])
        self.assertEqual(len(report["schedule"]), 32)
        self.assertEqual(len(report["feasibility_mask"]), 32)
        self.assertEqual(sum(x["feasible"] for x in report["feasibility_mask"]), 28)
        self.assertTrue(all(x["dispatches"] == 0 and x["outcome"] == "unexecuted-preflight"
                            for x in report["feasibility_mask"]))
        self.assertLess(report["caps"]["low"], report["caps"]["high"])
        self.assertLessEqual(report["caps"]["high"], 131_072)
        self.assertFalse(report["check_scope"]["live_execution_performed"])
        self.assertEqual(report["check_scope"]["dispatches_performed"], 0)
        self.assertFalse(any(report["specification_authorization"].values()))
        self.assertIsNone(report["context_accounting"]["provider_context_limit"])
        self.assertFalse(report["context_accounting"]["provider_count_request"])
        self.assertIsNone(report["context_accounting"]["subscription_usd"])
        self.assertTrue(all(item["sha256"] and not Path(item["path"]).is_absolute()
                            for item in report["identities"]))

    def test_h2_start_feasibility_uses_map_not_later_reference_overflow(self):
        report = h_check.audit(self.root)
        for item in report["measurements"]:
            if item["level"] == "expanded" and item["access"] == "H2":
                self.assertLessEqual(item["requests"][0]["bytes"], report["caps"]["low"])
                self.assertGreater(max(x["bytes"] for x in item["requests"]), report["caps"]["low"])
        low_h2 = [x for x in report["feasibility_mask"] if x["level"] == "expanded"
                  and x["access"] == "H2" and x["cap"] == "low"]
        self.assertTrue(all(x["feasible"] for x in low_h2))

    def test_pressure_failure_is_reported_without_adjustment(self):
        fake = [{"level": "core", "language": "csharp", "file_order": "forward", "access": "H1",
                 "requests": [{"bytes": 100, "sha256": "x"}]}]
        self.assertEqual(h_check.derive_caps(fake), (2048, 2048))

    def test_populated_pins_are_validated_but_null_draft_is_allowed(self):
        draft = json.loads((self.root / "protocols/workstream-h1-h2/specification.json").read_text())
        draft["budgets"]["cap_low"] = 1
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "spec.json"
            path.write_text(json.dumps(draft), encoding="utf-8")
            report = h_check.audit(self.root, path)
        self.assertIn("populated-pin-mismatch:budgets.cap_low", report["failures"])

    def test_permit_activation_reports_spec_state_but_performs_no_live_work(self):
        draft = json.loads((self.root / "protocols/workstream-h1-h2/specification.json").read_text())
        draft.update(status="execution-authorized", execution_authorized=True,
                     user_live_execution_approved=True, approved_integration_dispatches=5,
                     approved_pilot_dispatches=64)
        draft["analysis"]["human_review_approved"] = True
        draft["model"]["h_live_integration_verified"] = True
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "spec.json"; path.write_text(json.dumps(draft), encoding="utf-8")
            report = h_check.audit(self.root, path, permit_activation=True)
        self.assertEqual(report["status"], "passed", report["failures"])
        self.assertTrue(report["specification_authorization"]["execution_authorized"])
        self.assertTrue(report["specification_authorization"]["human_review_approved"])
        self.assertFalse(report["check_scope"]["live_execution_performed"])
        self.assertEqual(report["check_scope"]["dispatches_performed"], 0)

    def test_preexecution_status_rejects_enabled_flags_even_when_activation_audit_permitted(self):
        draft = json.loads((self.root / "protocols/workstream-h1-h2/specification.json").read_text())
        draft["status"] = "pre-execution-human-review"
        draft["analysis"]["human_review_approved"] = True
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "spec.json"; path.write_text(json.dumps(draft), encoding="utf-8")
            report = h_check.audit(self.root, path, permit_activation=True)
        self.assertIn("status-authorization-inconsistent", report["failures"])

    def test_same_length_public_contract_drift_changes_only_payload_identity_gate(self):
        baseline = h_check.audit(self.root)
        draft = json.loads((self.root / "protocols/workstream-h1-h2/specification.json").read_text())
        draft["workload"]["public_payload_sha256"] = baseline["proposed_specification_updates"][
            "workload.public_payload_sha256"]
        original = h_check.h_workload.public_payload
        def changed(root, level):
            payload = original(root, level)
            if level == "core":
                payload = json.loads(json.dumps(payload))
                text = payload["current_task"]
                payload["current_task"] = text.replace("summary", "summarx", 1)
                self.assertEqual(len(payload["current_task"]), len(text))
            return payload
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "spec.json"
            path.write_text(json.dumps(draft), encoding="utf-8")
            with patch.object(h_check.h_workload, "public_payload", side_effect=changed):
                report = h_check.audit(self.root, path)
        self.assertEqual(report["caps"], baseline["caps"])
        self.assertIn("populated-pin-mismatch:workload.public_payload_sha256", report["failures"])

    def test_output_is_deterministic_and_refuses_overwrite(self):
        report = h_check.audit(self.root)
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "new"
            h_check.write_artifacts(report, output)
            first = (output / "report.json").read_bytes()
            self.assertEqual(first, h_check._json(report))
            with self.assertRaises(FileExistsError):
                h_check.write_artifacts(report, output)

    def test_failed_cli_audit_never_starts_fixture_builder(self):
        with tempfile.TemporaryDirectory() as temporary, \
             patch.object(h_check, "audit", return_value={"status": "failed"}), \
             patch.object(h_check, "write_artifacts") as write, \
             patch("alf.h_fixtures.build_fixtures") as fixtures:
            result = h_check.main(["--output-dir", str(Path(temporary) / "out"), "--build-fixtures"])
        self.assertEqual(result, 1)
        fixtures.assert_not_called()
        write.assert_called_once()

    def test_gold_never_enters_reference_controller(self):
        original = h_check.reference_requests
        seen = []
        def inspect(source, order, payload, language, access, spec):
            values = original(source, order, payload, language, access, spec)
            seen.extend(values[0])
            return values
        with patch.object(h_check, "reference_requests", side_effect=inspect):
            report = h_check.audit(self.root)
        self.assertEqual(report["status"], "passed", report["failures"])
        for level in h_check.LEVELS:
            for language in h_check.LANGUAGES:
                source = h_check.h_workload.source_for(self.root, level, language)
                gold = h_check.h_workload.source_for(self.root, level, language, gold=True)
                additions = [text.encode() for text in gold.values() if text not in source.values()]
                self.assertTrue(all(value not in request for value in additions for request in seen))


if __name__ == "__main__":
    unittest.main()
