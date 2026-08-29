import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from alf.agents.command import CommandAgent
from alf.models import ProcessResult, Usage


class CommandAgentTests(unittest.TestCase):
    def _expected_protocol(self):
        return {
            "image_id": "sha256:" + "a" * 64,
            "definition": {
                "model": {"snapshot": "m", "reasoning_effort": "medium"},
                "codex": {"image": "image"},
                "limits": {"memory": "2g", "cpus": 2, "pids": 256},
            },
        }

    def _protocol_sidecar(self, *, event_count=1, usage_available=True, accounting_valid=True, usage_errors=None):
        usage = {name: 0 for name in Usage.__dataclass_fields__}
        usage.update(
            {
                "model": "m",
                "reasoning_effort": "medium",
                "image": "image",
                "image_id": "sha256:" + "a" * 64,
                "timed_out": False,
                "auth_ok": True,
                "container_limits": {"memory": "2g", "cpus": 2, "pids": 256},
                "event_count": event_count,
                "command_count": 0,
                "file_change_count": 0,
                "failed_event_count": 0,
                "file_reads": 0,
                "unique_file_reads": 0,
                "file_revisits": 0,
                "usage_record_count": 1,
                "accounting_valid": accounting_valid,
                "usage_available": usage_available,
                "derived_from_codex_jsonl": True,
                "usage_errors": usage_errors or [],
            }
        )
        return usage

    def _run(self, sidecar=None, stdout="", expected_protocol=None):
        directory = tempfile.TemporaryDirectory()
        root = Path(directory.name) / "root"; workspace = root / "workspace"; workspace.mkdir(parents=True)
        def invoke(*args, **kwargs):
            if sidecar is not None:
                (workspace / ".alf").mkdir(exist_ok=True)
                text = sidecar if isinstance(sidecar, str) else json.dumps(sidecar)
                (workspace / ".alf" / "usage.json").write_text(text, encoding="utf-8")
            return ProcessResult(["ok"], 0, stdout, "", 0)
        agent = CommandAgent(
            "tool", require_usage=True, expected_protocol=expected_protocol
        )
        with patch("alf.agents.command.run_process", side_effect=invoke):
            got = agent.run(root=root, workspace=workspace, language="csharp", language_config={}, task={"id": "t"}, prompt="p", timeout=1)
        return directory, got

    def test_optional_missing_usage_is_unavailable(self):
        directory = tempfile.TemporaryDirectory(); root = Path(directory.name); workspace = root / "w"; workspace.mkdir()
        with patch("alf.agents.command.run_process", return_value=ProcessResult(["ok"], 0, "", "", 0)):
            got = CommandAgent("tool").run(root=root, workspace=workspace, language="csharp", language_config={}, task={"id": "t"}, prompt="p", timeout=1)
        self.assertTrue(got.accounting_valid); self.assertFalse(got.usage_available); directory.cleanup()

    def test_required_missing_usage_is_invalid(self):
        directory, got = self._run(); directory.cleanup()
        self.assertFalse(got.accounting_valid); self.assertTrue(any("missing" in e for e in got.accounting_errors))

    def test_malformed_sidecar_is_recorded(self):
        directory, got = self._run("{"); directory.cleanup()
        self.assertFalse(got.accounting_valid); self.assertTrue(got.accounting_errors)

    def test_required_complete_generic_usage_is_valid(self):
        usage = {name: 0 for name in Usage.__dataclass_fields__}
        directory, got = self._run(usage); directory.cleanup()
        self.assertTrue(got.accounting_valid); self.assertTrue(got.usage_available)

    def test_each_protocol_sidecar_pin_mismatch_invalidates_accounting(self):
        expected = self._expected_protocol()
        raw_usage = {
            name: 0 for name in Usage.__dataclass_fields__ if name != "tool_calls"
        }
        stdout = json.dumps({"type": "turn.completed", "usage": raw_usage})
        for field, value in (("model", "wrong"), ("reasoning_effort", "high"), ("image", "wrong-image"), ("image_id", "sha256:" + "b" * 64)):
            usage = self._protocol_sidecar()
            usage[field] = value
            directory = tempfile.TemporaryDirectory(); root = Path(directory.name); workspace = root / "w"; workspace.mkdir()
            def invoke(*args, **kwargs):
                (workspace / ".alf").mkdir(exist_ok=True)
                (workspace / ".alf" / "usage.json").write_text(json.dumps(usage), encoding="utf-8")
                return ProcessResult(["ok"], 0, stdout, "", 0)
            with patch("alf.agents.command.run_process", side_effect=invoke):
                got = CommandAgent("tool", require_usage=True, expected_protocol=expected).run(root=root, workspace=workspace, language="csharp", language_config={}, task={"id": "t"}, prompt="p", timeout=1)
            self.assertFalse(got.accounting_valid, field)
            self.assertFalse(got.ok, field)
            self.assertIn(f"protocol sidecar mismatch: {field}", got.accounting_errors)
            directory.cleanup()

    def test_protocol_timeout_sidecar_marks_candidate_process_timeout(self):
        expected = self._expected_protocol()
        usage = self._protocol_sidecar(
            event_count=0,
            usage_available=False,
            accounting_valid=False,
            usage_errors=["no turn.completed usage records found"],
        )
        usage["timed_out"] = True
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workspace = root / "w"
            workspace.mkdir()

            def invoke(*_args, **_kwargs):
                (workspace / ".alf").mkdir(exist_ok=True)
                (workspace / ".alf" / "usage.json").write_text(
                    json.dumps(usage), encoding="utf-8"
                )
                return ProcessResult(["tool"], 124, "", "", 1.0)

            with patch("alf.agents.command.run_process", side_effect=invoke):
                got = CommandAgent(
                    "tool", require_usage=True, expected_protocol=expected
                ).run(
                    root=root,
                    workspace=workspace,
                    language="csharp",
                    language_config={},
                    task={"id": "t"},
                    prompt="p",
                    timeout=1,
                )

        self.assertTrue(got.process.timed_out)
        self.assertFalse(got.accounting_valid)
        self.assertFalse(got.ok)

    def test_protocol_requires_one_derived_terminal_usage_record(self):
        expected = self._expected_protocol()
        raw_usage = {
            name: 0 for name in Usage.__dataclass_fields__ if name != "tool_calls"
        }
        record = json.dumps({"type": "turn.completed", "usage": raw_usage})

        sidecar = self._protocol_sidecar()
        directory, got = self._run(sidecar, record, expected)
        directory.cleanup()
        self.assertTrue(got.accounting_valid)
        self.assertEqual(got.usage_record_count, 1)

        duplicated = "\n".join((record, record))
        sidecar = self._protocol_sidecar(event_count=2)
        directory, got = self._run(sidecar, duplicated, expected)
        directory.cleanup()
        self.assertFalse(got.accounting_valid)
        self.assertEqual(got.usage_record_count, 2)
        self.assertTrue(
            any("exactly one" in error for error in got.accounting_errors)
        )

    def test_derived_sidecar_requires_usage_record_count(self):
        expected = self._expected_protocol()
        raw = json.dumps({"type": "turn.completed", "usage": {name: 0 for name in Usage.__dataclass_fields__ if name != "tool_calls"}})
        sidecar = self._protocol_sidecar()
        sidecar.pop("usage_record_count")
        directory, got = self._run(sidecar, raw, expected)
        directory.cleanup()
        self.assertFalse(got.accounting_valid)
        self.assertTrue(any("usage_record_count" in error for error in got.accounting_errors))

        sidecar = self._protocol_sidecar()
        sidecar["usage_record_count"] = 2
        directory, got = self._run(sidecar, raw, expected)
        directory.cleanup()
        self.assertFalse(got.accounting_valid)

        generic = {name: 0 for name in Usage.__dataclass_fields__}
        generic.update(
            {
                "model": "m",
                "reasoning_effort": "medium",
                "image": "image",
                "image_id": "sha256:" + "a" * 64,
                "timed_out": False,
                "auth_ok": True,
                "container_limits": {"memory": "2g", "cpus": 2, "pids": 256},
            }
        )
        directory, got = self._run(generic, "", expected)
        directory.cleanup()
        self.assertFalse(got.accounting_valid)
        self.assertIn(
            "protocol sidecar mismatch: derived_from_codex_jsonl",
            got.accounting_errors,
        )

    def test_valid_derived_sidecar_preserves_events(self):
        usage = {k: 0 for k in ("input_tokens", "cached_input_tokens", "cache_write_input_tokens", "output_tokens", "reasoning_output_tokens", "tool_calls")}
        stdout = json.dumps({"type": "turn.completed", "usage": {k: usage[k] for k in usage if k != "tool_calls"}})
        sidecar = {**usage, "event_count": 1, "command_count": 0, "file_change_count": 0, "failed_event_count": 0,
                   "file_reads": 0, "unique_file_reads": 0, "file_revisits": 0, "usage_record_count": 1, "accounting_valid": True, "usage_available": True,
                   "derived_from_codex_jsonl": True, "usage_errors": []}
        directory, got = self._run(sidecar, stdout); directory.cleanup()
        self.assertTrue(got.accounting_valid); self.assertEqual(len(got.events), 1)

    def test_derived_sidecar_mismatch_is_invalid(self):
        usage = {k: 0 for k in ("input_tokens", "cached_input_tokens", "cache_write_input_tokens", "output_tokens", "reasoning_output_tokens", "tool_calls")}
        stdout = json.dumps({"type": "turn.completed", "usage": {k: usage[k] for k in usage if k != "tool_calls"}})
        sidecar = {**usage, "event_count": 9, "command_count": 0, "file_change_count": 0, "failed_event_count": 0,
                   "file_reads": 0, "unique_file_reads": 0, "file_revisits": 0, "usage_record_count": 1, "accounting_valid": True, "usage_available": True,
                   "derived_from_codex_jsonl": True}
        directory, got = self._run(sidecar, stdout); directory.cleanup()
        self.assertFalse(got.accounting_valid); self.assertTrue(any("mismatch" in e for e in got.accounting_errors))

    def test_windows_tokenizer_preserves_quoted_backslash_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo root"
            workspace = root / "task workspace"
            workspace.mkdir(parents=True)
            sidecar = workspace / ".alf" / "usage.json"
            sidecar.parent.mkdir()
            sidecar.write_text(
                json.dumps(
                    {
                        "event_count": 2,
                        "command_count": 1,
                        "failed_event_count": 1,
                        "model": "m",
                    }
                ),
                encoding="utf-8",
            )
            result = ProcessResult(["ok"], 0, "", "", 0)
            with (
                patch("alf.agents.command.os.name", "nt"),
                patch("alf.agents.command.run_process", return_value=result) as run,
            ):
                agent = CommandAgent(
                    'tool "{root}\\nested path\\agent.exe" --workspace "{workspace}"'
                )
                got = agent.run(
                    root=root,
                    workspace=workspace,
                    language="csharp",
                    language_config={},
                    task={"id": "t"},
                    prompt="p",
                    timeout=4,
                )

            # CommandAgent tokenizes but does not normalize path separators. On an
            # actual Windows host, str(root) already contains backslashes; when
            # simulating Windows on POSIX, preserve the rendered Windows suffix.
            expected_executable = f"{root}\\nested path\\agent.exe"
            self.assertEqual(run.call_args.args[0][1], expected_executable)
            self.assertEqual(run.call_args.kwargs["env"]["ALF_ROOT"], str(root))
            self.assertEqual(run.call_args.kwargs["env"]["ALF_TIMEOUT"], "4")
            self.assertEqual(run.call_args.kwargs["timeout"], 34.0)
            self.assertEqual(got.event_count, 0)
            self.assertEqual(got.command_count, 0)
            self.assertEqual(got.failed_event_count, 0)
            self.assertTrue(got.ok)
            self.assertFalse(got.accounting_errors)


if __name__ == "__main__":
    unittest.main()
