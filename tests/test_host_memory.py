import unittest
import importlib.util
import json
import tempfile
from pathlib import Path
from unittest.mock import patch

from alf.host_memory import evaluate_host_memory
from alf.models import ProcessResult
from alf.agents.command import CommandAgent
from alf.runner import _derive_protocol_disposition

SCRIPT = Path(__file__).parents[1] / "scripts" / "codex-docker.py"
SPEC = importlib.util.spec_from_file_location("codex_docker_memory", SCRIPT)
assert SPEC and SPEC.loader
docker_module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(docker_module)


class HostMemoryTests(unittest.TestCase):
    def test_threshold_evaluation(self):
        with patch("alf.host_memory.probe_host_memory", return_value={
            "platform": "Linux", "total_physical_bytes": 10,
            "available_physical_bytes": 8, "total_commit_bytes": 20,
            "available_commit_bytes": 12,
        }):
            result = evaluate_host_memory({
                "minimum_available_physical_bytes": 8,
                "minimum_available_commit_bytes": 12,
            })
        self.assertTrue(result["ok"])
        self.assertEqual(result["thresholds"]["minimum_available_commit_bytes"], 12)

    def test_probe_failure_is_not_inferred_from_zeroes(self):
        with patch("alf.host_memory.probe_host_memory", side_effect=OSError("unavailable")):
            result = evaluate_host_memory({
                "minimum_available_physical_bytes": 1,
                "minimum_available_commit_bytes": 1,
            })
        self.assertFalse(result["ok"])
        self.assertEqual(result["probe_error"], "unavailable")

    def test_wrapper_refusal_does_not_launch_docker_or_auth(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            calls = []
            requirement = {"minimum_available_physical_bytes": 10, "minimum_available_commit_bytes": 20}
            refused = {"observed_at": "now", "platform": "Linux", "thresholds": requirement,
                       "available_physical_bytes": 1, "available_commit_bytes": 2, "ok": False,
                       "probe_error": None}
            with patch.dict(docker_module.os.environ, {"ALF_HOST_MEMORY": json.dumps(requirement)}), \
                 patch.object(docker_module, "evaluate_host_memory", return_value=refused), \
                 patch.object(docker_module.subprocess, "run", side_effect=lambda *a, **k: calls.append(a[0])):
                code = docker_module.main(["--workspace", str(workspace), "--prompt", "x"])
            self.assertEqual(code, 75)
            self.assertEqual(calls, [])
            self.assertEqual(json.loads((workspace / ".alf" / "usage.json").read_text())["host_memory_gate"], "failed")

    def test_command_accepts_explicit_refusal_without_protocol_errors(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory); (workspace / ".alf").mkdir()
            req = {"minimum_available_physical_bytes": 10, "minimum_available_commit_bytes": 20}
            sidecar_value = {
                "host_memory_gate": "failed", "host_memory": {"thresholds": req, "ok": False},
                "model": "m", "image": "i", "image_id": "not-probed", "reasoning_effort": "medium",
                "container_limits": {"memory": "2g", "cpus": 2, "pids": 256},
                "auth_ok": None, "timed_out": False, "derived_from_codex_jsonl": False,
                "input_tokens": 0, "cached_input_tokens": 0, "cache_write_input_tokens": 0,
                "output_tokens": 0, "reasoning_output_tokens": 0, "tool_calls": 0,
                "usage_record_count": 0, "accounting_valid": False, "usage_available": False,
                "event_count": 0, "command_count": 0, "file_change_count": 0,
                "failed_event_count": 0, "file_reads": 0, "unique_file_reads": 0, "file_revisits": 0,
            }
            expected = {"schema_version": 3, "definition": {"model": {"requested_id": "m", "reasoning_effort": "medium"},
                "codex": {"image": "i"}, "image_id": "real", "limits": {"memory": "2g", "cpus": 2, "pids": 256}, "host_memory": {
                    "probe_scope": "x", **req, "failure_disposition": "x"}}, "image_id": "real"}
            agent = CommandAgent("echo", require_usage=True, expected_protocol=expected)
            def refuse(*_args, **_kwargs):
                (workspace / ".alf" / "usage.json").write_text(json.dumps(sidecar_value))
                return ProcessResult(["echo"], 75, "", "", 0.1)
            with patch("alf.agents.command.run_process", side_effect=refuse):
                result = agent.run(root=workspace, workspace=workspace, language="csharp", language_config={}, task={"id": "t"}, prompt="x", timeout=1, host_memory=req)
            self.assertFalse(result.accounting_valid)
            self.assertFalse(result.usage_available)
            self.assertFalse(any("protocol sidecar" in e for e in result.accounting_errors))

    def test_forged_refusal_identity_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory); (workspace / ".alf").mkdir()
            req = {"minimum_available_physical_bytes": 10, "minimum_available_commit_bytes": 20}
            value = {"host_memory_gate": "failed", "host_memory": {"thresholds": req, "ok": False},
                "model": "wrong", "image": "i", "image_id": "not-probed", "reasoning_effort": "medium",
                "container_limits": {"memory": "2g", "cpus": 2, "pids": 256}, "auth_ok": None, "timed_out": False,
                "derived_from_codex_jsonl": False, "returncode": 75}
            for field in ("input_tokens", "cached_input_tokens", "cache_write_input_tokens", "output_tokens", "reasoning_output_tokens", "tool_calls", "event_count", "command_count", "file_change_count", "failed_event_count", "file_reads", "unique_file_reads", "file_revisits", "usage_record_count"):
                value[field] = 0
            expected = {"schema_version": 3, "definition": {"model": {"requested_id": "m", "reasoning_effort": "medium"}, "codex": {"image": "i"}, "image_id": "real", "limits": {"memory": "2g", "cpus": 2, "pids": 256}, "host_memory": req}, "image_id": "real"}
            agent = CommandAgent("echo", require_usage=True, expected_protocol=expected)
            def forged(*_args, **_kwargs):
                (workspace / ".alf" / "usage.json").write_text(json.dumps(value))
                return ProcessResult(["echo"], 75, "", "", 0.1)
            with patch("alf.agents.command.run_process", side_effect=forged):
                result = agent.run(root=workspace, workspace=workspace, language="csharp", language_config={}, task={"id": "t"}, prompt="x", timeout=1, host_memory=req)
            self.assertFalse(result.accounting_valid)
            self.assertTrue(result.accounting_errors)
            run = {"baseline": {"ok": True, "build": {}}, "tasks": [{
                "agent": {"process": result.process.summary(), "host_memory": result.host_memory,
                           "auth_ok": result.auth_ok, "usage_available": result.usage_available,
                           "accounting_errors": result.accounting_errors},
                "evaluation": {"ok": True, "build": {}}}], "success": False,
                "aggregate_accounting_valid": False, "aggregate_usage_available": False,
                "provenance": {"cell_id": "v3"}}
            with patch("alf.runner.run_process", return_value=ProcessResult([], 0, "sha", "", 0)):
                disposition = _derive_protocol_disposition(run)
            self.assertEqual(disposition["failure_category"], "protocol")

    def test_explicit_gate_disposition_is_retryable_host(self):
        evaluation = {"ok": True, "build": {}}
        run = {"baseline": evaluation, "tasks": [{
            "agent": {"process": {"returncode": 75, "timed_out": False, "missing_executable": False},
                       "host_memory": {"ok": False}, "auth_ok": None, "usage_available": False,
                       "accounting_errors": []}, "evaluation": evaluation}],
            "success": False, "aggregate_accounting_valid": True,
            "aggregate_usage_available": False, "provenance": {"cell_id": "v3"}}
        with patch("alf.runner.run_process", return_value=ProcessResult([], 0, "sha", "", 0)):
            disposition = _derive_protocol_disposition(run)
        self.assertEqual(disposition["failure_category"], "host")
        self.assertTrue(disposition["retryable"])
        self.assertEqual(disposition["analysis_role"], "infrastructure-invalid")


if __name__ == "__main__":
    unittest.main()
