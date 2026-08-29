import json
import tempfile
import unittest
from pathlib import Path
from alf.audit import audit_run, audit_representation_checkpoint
from alf.runner import _derive_protocol_disposition

class AuditTests(unittest.TestCase):
    def test_c3_checkpoint_four_baselines_are_interpretable(self):
        root = Path(__file__).parents[1] / "benchmarks" / "successor" / "representation-v1"
        for treatment in ("descriptive", "deterministic"):
            for language in ("csharp", "fsharp"):
                report = audit_representation_checkpoint(root / "transformed" / treatment / language / "baseline", root, language, treatment, "baseline")
                self.assertTrue(report["ok"], report["errors"])
                self.assertTrue(report["representation_interpretable"], report)

    def test_reconciles_derived_redacted_recovered_fixture(self):
        fixture = Path(__file__).parent / "fixtures" / "a3-redacted-run"
        report = audit_run(fixture)
        self.assertTrue(report["ok"], report["errors"])
        result = json.loads((fixture / "result.json").read_text())
        self.assertEqual(len(result["tasks"]), 2)
        self.assertEqual(result["aggregate_usage"]["input_tokens"], 317078)
        self.assertEqual(sum(t["agent"]["event_count"] for t in result["tasks"]), 52)
        self.assertAlmostEqual(result["run_total_wall_seconds"], 297.617385)
        self.assertAlmostEqual(result["tasks"][0]["task_total_wall_seconds"], 186.280462)
        self.assertAlmostEqual(result["tasks"][1]["task_total_wall_seconds"], 110.009695)
        selected_task = json.loads((fixture / "tasks" / "002-overdue" / "task-result.json").read_text())
        self.assertAlmostEqual(selected_task["task_total_wall_seconds"], 110.009695)
        provenance = json.loads((fixture / "provenance.json").read_text())
        self.assertAlmostEqual(provenance["observed_timings_seconds"]["agent_process"], 98.57900000000154)
        self.assertEqual(provenance["source_run_hash"], "539576170a0009164fbb7b8462c7d94bebf8d7dbcc8a96edf75e0f4afbda74dd")
        self.assertEqual(provenance["source_hashes"]["001-priority agent.stdout"], "8ee22b9047b307dca241429086da6a7b986d685738e0c4ebc3d4f9ff2a8c3326")
        self.assertEqual(provenance["source_hashes"]["002-overdue agent.stdout"], "e7d99b36c6f31f3b8653b245b34f8d69855f71b5f7fd95b4e8167dca7dba34e8")
        self.assertTrue(provenance["expected_audit"]["ok"])

    def _derived_fixture(self):
        root = Path(tempfile.mkdtemp()); task_dir = root / "tasks" / "t1"; task_dir.mkdir(parents=True)
        usage = {k: 0 for k in ("input_tokens", "cached_input_tokens", "cache_write_input_tokens", "output_tokens", "reasoning_output_tokens", "tool_calls")}
        event = {"type": "turn.completed", "usage": {k: usage[k] for k in usage if k != "tool_calls"}}
        raw = json.dumps(event) + "\n"; (task_dir / "agent.stdout").write_text(raw); (task_dir / "events.jsonl").write_text(raw)
        side = {**usage, "event_count": 1, "command_count": 0, "file_change_count": 0, "failed_event_count": 0, "file_reads": 0, "unique_file_reads": 0, "file_revisits": 0, "usage_record_count": 1, "accounting_valid": True, "usage_available": True, "usage_errors": [], "derived_from_codex_jsonl": True}
        (task_dir / "usage.json").write_text(json.dumps(side))
        agent = {"ok": True, "usage": usage, "usage_available": True, "accounting_valid": True, "accounting_errors": [], "event_count": 1, "command_count": 0, "file_change_count": 0, "failed_event_count": 0, "file_reads": 0, "unique_file_reads": 0, "file_revisits": 0, "usage_record_count": 1}
        tr = {"task_id": "t1", "agent": agent, "task_total_wall_seconds": 1, "success": True}; (task_dir / "task-result.json").write_text(json.dumps(tr))
        run = {"run_id": "x", "agent": "command", "require_usage": True, "tasks": [tr], "aggregate_usage": usage, "aggregate_usage_available": True, "aggregate_accounting_valid": True, "run_total_wall_seconds": 1, "evaluator_wall_seconds": 0, "agent_process_wall_seconds": 0, "success": True}
        (root / "result.json").write_text(json.dumps(run)); return root

    def test_reconciles_derived_codex_run(self):
        root = self._derived_fixture(); self.assertTrue(audit_run(root)["ok"])

    def test_detects_raw_events_mismatch(self):
        root = self._derived_fixture(); (root / "tasks" / "t1" / "events.jsonl").write_text("{}\n"); self.assertFalse(audit_run(root)["ok"])

    def test_detects_sidecar_task_mismatch(self):
        root = self._derived_fixture(); side = root / "tasks" / "t1" / "usage.json"; side.write_text(side.read_text().replace('"event_count": 1', '"event_count": 2')); self.assertFalse(audit_run(root)["ok"])

    def test_detects_sidecar_usage_record_count_mismatch(self):
        root = self._derived_fixture(); side = root / "tasks" / "t1" / "usage.json"
        side.write_text(side.read_text().replace('"usage_record_count": 1', '"usage_record_count": 2'))
        self.assertFalse(audit_run(root)["ok"])

    def test_detects_task_result_run_mismatch(self):
        root = self._derived_fixture(); run = json.loads((root / "result.json").read_text()); run["tasks"][0]["success"] = False; (root / "result.json").write_text(json.dumps(run)); self.assertFalse(audit_run(root)["ok"])

    def test_detects_aggregate_flag_or_sum_mismatch(self):
        root = self._derived_fixture(); run = json.loads((root / "result.json").read_text()); run["aggregate_usage_available"] = False; (root / "result.json").write_text(json.dumps(run)); self.assertFalse(audit_run(root)["ok"])

    def test_rejects_malformed_structure(self):
        root = Path(tempfile.mkdtemp()); (root / "result.json").write_text(json.dumps({"tasks": None})); self.assertFalse(audit_run(root)["ok"])

    def test_required_usage_missing_sidecar_is_actionable(self):
        root = self._derived_fixture(); (root / "tasks" / "t1" / "usage.json").unlink(); report = audit_run(root); self.assertFalse(report["ok"]); self.assertTrue(any("required usage sidecar" in e for e in report["errors"]))

    def test_detects_accounting_error_success_contradictions(self):
        root = self._derived_fixture()
        path = root / "tasks" / "t1" / "task-result.json"
        task = json.loads(path.read_text())
        task["agent"]["accounting_errors"] = ["tampered"]
        path.write_text(json.dumps(task))
        run_path = root / "result.json"
        run = json.loads(run_path.read_text())
        run["tasks"] = [task]
        run_path.write_text(json.dumps(run))
        self.assertFalse(audit_run(root)["ok"])

    def test_reconciles_synthetic_run(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); task = root / "tasks" / "t1"; task.mkdir(parents=True)
            usage = {"input_tokens": 2, "cached_input_tokens": 0, "cache_write_input_tokens": 0,
                     "output_tokens": 3, "reasoning_output_tokens": 1, "tool_calls": 0}
            (task / "usage.json").write_text(json.dumps(usage), encoding="utf-8")
            agent = {"ok": True, "usage": usage, "usage_available": True, "accounting_valid": True,
                     "accounting_errors": [],
                     "event_count": 0, "command_count": 0, "file_change_count": 0,
                     "failed_event_count": 0, "file_reads": 0, "unique_file_reads": 0, "file_revisits": 0}
            tr = {"task_id": "t1", "agent": agent, "success": True, "task_total_wall_seconds": 1}
            (task / "task-result.json").write_text(json.dumps(tr), encoding="utf-8")
            run = {"run_id": "synthetic", "agent": "command", "tasks": [tr], "aggregate_usage": usage,
                   "run_total_wall_seconds": 2, "evaluator_wall_seconds": 1, "agent_process_wall_seconds": 1,
                   "aggregate_accounting_valid": True, "aggregate_usage_available": True, "success": True}
            (root / "result.json").write_text(json.dumps(run), encoding="utf-8")
            self.assertTrue(audit_run(root)["ok"])

    def test_missing_sidecar_is_actionable(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); task = root / "tasks" / "t1"; task.mkdir(parents=True)
            usage = {k: 0 for k in ("input_tokens", "cached_input_tokens", "cache_write_input_tokens", "output_tokens", "reasoning_output_tokens", "tool_calls")}
            tr = {"task_id": "t1", "agent": {"ok": True, "usage": usage, "usage_available": True,
                  "accounting_valid": True, "accounting_errors": []}, "task_total_wall_seconds": 1}
            (task / "task-result.json").write_text(json.dumps(tr), encoding="utf-8")
            (root / "result.json").write_text(json.dumps({"tasks": [tr], "aggregate_usage": usage, "run_total_wall_seconds": 1, "evaluator_wall_seconds": 1, "agent_process_wall_seconds": 1, "aggregate_accounting_valid": True, "aggregate_usage_available": True}), encoding="utf-8")
            report = audit_run(root)
            self.assertFalse(report["ok"])
            self.assertIn("usage sidecar", report["errors"][0])

    def test_difficulty_audit_requires_representation_sidecars(self):
        root = self._derived_fixture(); run_path = root / "result.json"; run = json.loads(run_path.read_text())
        audit = {"ok": True, "representation_interpretable": True, "include_representation_analysis": True, "errors": []}
        run["provenance"] = {"cell_id": "difficulty-v1"}; run["representation_audit"] = audit; run["tasks"][0]["representation_audit"] = audit
        run["disposition"] = _derive_protocol_disposition(run)
        run_path.write_text(json.dumps(run)); (root / "tasks" / "t1" / "task-result.json").write_text(json.dumps(run["tasks"][0])); (root / "representation-audit.json").write_text(json.dumps(audit)); (root / "tasks" / "t1" / "representation-audit.json").write_text(json.dumps(audit))
        self.assertTrue(audit_run(root)["ok"])
        (root / "representation-audit.json").unlink(); report = audit_run(root); self.assertFalse(report["ok"])
        self.assertTrue(any("baseline representation audit" in error for error in report["errors"]))

    def test_difficulty_audit_rejects_tampered_task_representation_sidecar(self):
        root = self._derived_fixture(); run_path = root / "result.json"; run = json.loads(run_path.read_text())
        audit = {"ok": True, "representation_interpretable": True, "include_representation_analysis": True, "errors": []}
        run["provenance"] = {"cell_id": "difficulty-v1"}; run["representation_audit"] = audit; run["tasks"][0]["representation_audit"] = audit
        run["disposition"] = _derive_protocol_disposition(run)
        run_path.write_text(json.dumps(run)); (root / "tasks" / "t1" / "task-result.json").write_text(json.dumps(run["tasks"][0])); (root / "representation-audit.json").write_text(json.dumps(audit))
        (root / "tasks" / "t1" / "representation-audit.json").write_text(json.dumps({**audit, "ok": False}))
        report = audit_run(root); self.assertFalse(report["ok"])
        self.assertTrue(any("representation audit disagrees" in error for error in report["errors"]))

    def test_difficulty_audit_rejects_disposition_only_tampering(self):
        root = self._derived_fixture(); run_path = root / "result.json"; run = json.loads(run_path.read_text())
        audit = {"ok": True, "representation_interpretable": True, "include_representation_analysis": True, "errors": []}
        run["provenance"] = {"cell_id": "difficulty-v1"}; run["representation_audit"] = audit; run["tasks"][0]["representation_audit"] = audit
        run["disposition"] = _derive_protocol_disposition(run)
        run["disposition"]["include_representation_analysis"] = False
        run_path.write_text(json.dumps(run)); (root / "tasks" / "t1" / "task-result.json").write_text(json.dumps(run["tasks"][0])); (root / "representation-audit.json").write_text(json.dumps(audit)); (root / "tasks" / "t1" / "representation-audit.json").write_text(json.dumps(audit))
        report = audit_run(root)
        self.assertFalse(report["ok"])
        self.assertTrue(any("frozen disposition" in error for error in report["errors"]))
