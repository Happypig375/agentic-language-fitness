from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

from alf.process import run_process


class RunProcessTests(unittest.TestCase):
    def test_captures_utf8_stdout_and_stderr(self) -> None:
        script = (
            "import sys; "
            "sys.stdout.buffer.write('snowman ☃ and euro €\\n'.encode('utf-8')); "
            "sys.stderr.buffer.write('stderr 漢字\\n'.encode('utf-8'))"
        )

        with tempfile.TemporaryDirectory() as directory:
            result = run_process([sys.executable, "-c", script], cwd=Path(directory))

        self.assertTrue(result.ok)
        self.assertEqual(result.stdout, "snowman ☃ and euro €\n")
        self.assertEqual(result.stderr, "stderr 漢字\n")

    def test_timeout_preserves_utf8_output(self) -> None:
        script = (
            "import sys, time; "
            "sys.stdout.buffer.write('before timeout ☃\\n'.encode('utf-8')); sys.stdout.flush(); "
            "sys.stderr.buffer.write('warning 漢字\\n'.encode('utf-8')); sys.stderr.flush(); "
            "time.sleep(10)"
        )

        with tempfile.TemporaryDirectory() as directory:
            result = run_process([sys.executable, "-c", script], cwd=Path(directory), timeout=1.0)

        self.assertTrue(result.timed_out)
        self.assertIsInstance(result.stdout, str)
        self.assertIsInstance(result.stderr, str)
        self.assertIn("before timeout ☃", result.stdout)
        self.assertIn("warning 漢字", result.stderr)
