import tempfile
import unittest
from pathlib import Path

from alf.metrics import snapshot_repository


class MetricsTests(unittest.TestCase):
    def test_excludes_build_and_agent_directories(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "Program.fs").write_text("let answer = 42\n", encoding="utf-8")
            (root / "bin").mkdir()
            (root / "bin" / "Generated.cs").write_text("ignored", encoding="utf-8")
            (root / ".alf").mkdir()
            (root / ".alf" / "TASK.md").write_text("ignored", encoding="utf-8")
            metrics = snapshot_repository(root)
            self.assertEqual(metrics["source_files"], 1)
            self.assertEqual(metrics["source_lines"], 1)
            self.assertGreater(metrics["approx_lexical_tokens"], 0)


if __name__ == "__main__":
    unittest.main()
