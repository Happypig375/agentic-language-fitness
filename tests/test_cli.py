import io
import json
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest.mock import patch

from alf.cli import build_parser, cmd_workstream_e


class CliProtocolTests(unittest.TestCase):
    def test_parser_accepts_williams_order_and_position_four(self):
        args = build_parser().parse_args(["run", "--language", "fsharp", "--order", "williams-01", "--position", "4"])
        self.assertEqual((args.order, args.position), ("williams-01", 4))


class CliWorkstreamETests(unittest.TestCase):
    def arguments(self, command="e1-report", sha="A" * 40):
        return build_parser().parse_args([
            command,
            "--calibration-report", "calibration.json",
            "--archive-root", "private-archive-sentinel",
            "--analyzer-git-sha", sha,
            "--output-json", "derived.json",
            "--output-markdown", "derived.md",
        ])

    def test_parser_accepts_alias_and_normalizes_sha(self):
        self.assertEqual(self.arguments("e1").analyzer_git_sha, "a" * 40)
        with redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                self.arguments(sha="short")

    def test_success_summary_has_counts_outputs_and_no_archive_path(self):
        report = {"report_sha256": "f" * 64, "totals": {"run_count": 10, "task_count": 80}}
        args = self.arguments()
        stream = io.StringIO()
        with patch("alf.cli.analyze_archive", return_value=report) as analyze, \
             patch("alf.cli.write_report") as writer, redirect_stdout(stream):
            self.assertEqual(cmd_workstream_e(args), 0)
        summary = json.loads(stream.getvalue())
        self.assertEqual(summary["runs"], 10)
        self.assertEqual(summary["tasks"], 80)
        self.assertEqual(summary["output_json"], "derived.json")
        self.assertNotIn("private-archive-sentinel", stream.getvalue())
        analyze.assert_called_once()
        writer.assert_called_once_with(report, "derived.json", "derived.md")

    def test_integrity_failure_does_not_call_writer(self):
        args = self.arguments()
        with patch("alf.cli.analyze_archive", side_effect=ValueError("integrity")), \
             patch("alf.cli.write_report") as writer:
            with self.assertRaisesRegex(ValueError, "integrity"):
                cmd_workstream_e(args)
        writer.assert_not_called()


if __name__ == "__main__":
    unittest.main()
