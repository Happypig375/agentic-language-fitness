import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from alf.agents.command import CommandAgent
from alf.models import ProcessResult


class CommandAgentTests(unittest.TestCase):
    def test_windows_tokenizer_preserves_quoted_backslash_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo root"
            workspace = root / "task workspace"
            workspace.mkdir(parents=True)
            sidecar = workspace / ".alf" / "usage.json"
            sidecar.parent.mkdir()
            sidecar.write_text(json.dumps({"event_count": 2, "command_count": 1, "failed_event_count": 1, "model": "m"}), encoding="utf-8")
            result = ProcessResult(["ok"], 0, "", "", 0)
            with patch("alf.agents.command.os.name", "nt"), patch("alf.agents.command.run_process", return_value=result) as run:
                agent = CommandAgent('tool "{root}\\nested path\\agent.exe" --workspace "{workspace}"')
                got = agent.run(root=root, workspace=workspace, language="csharp", language_config={}, task={"id": "t"}, prompt="p", timeout=4)
            self.assertEqual(run.call_args.args[0][1], str(root / "nested path" / "agent.exe"))
            self.assertEqual(run.call_args.kwargs["env"]["ALF_ROOT"], str(root))
            self.assertEqual(run.call_args.kwargs["env"]["ALF_TIMEOUT"], "4")
            self.assertEqual(run.call_args.kwargs["timeout"], 34.0)
            self.assertEqual(got.event_count, 2)
            self.assertEqual(got.command_count, 1)
            self.assertEqual(got.failed_event_count, 1)
            self.assertFalse(got.ok)


if __name__ == "__main__":
    unittest.main()
