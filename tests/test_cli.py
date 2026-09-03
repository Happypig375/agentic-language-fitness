import io
import json
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

from alf.cli import (
    build_parser,
    cmd_e2_audit,
    cmd_e2_check,
    cmd_e2_freeze,
    cmd_e2_run,
    cmd_workstream_e,
)


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


class CliWorkstreamE2Tests(unittest.TestCase):
    def arguments(self, action: str):
        common = [
            "--root",
            "C:/synthetic/repo",
            "--manifest",
            "benchmarks/successor/manifest.json",
            "e2",
            action,
        ]
        if action == "freeze":
            return build_parser().parse_args([*common, "--output", "protocols/e2/definition.json"])
        if action == "check":
            return build_parser().parse_args([*common, "--definition", "protocols/e2/definition.json"])
        if action == "audit":
            return build_parser().parse_args(
                [
                    *common,
                    "--definition",
                    "protocols/e2/definition.json",
                    "--report",
                    "reports/e2/report.json",
                    "--raw-output",
                    "C:/external/raw",
                ]
            )
        return build_parser().parse_args(
            [
                *common,
                "--definition",
                "protocols/e2/definition.json",
                "--runner-git-sha",
                "A" * 40,
                "--container-image-id",
                "sha256:" + "b" * 64,
                "--package-cache",
                "C:/external/cache",
                "--raw-output",
                "C:/external/raw",
                "--output-json",
                "C:/external/report.json",
                "--output-markdown",
                "C:/external/report.md",
            ]
        )

    def test_parser_accepts_all_e2_actions_and_normalizes_runner_sha(self):
        self.assertEqual(self.arguments("freeze").func, cmd_e2_freeze)
        self.assertEqual(self.arguments("check").func, cmd_e2_check)
        self.assertEqual(self.arguments("audit").func, cmd_e2_audit)
        run = self.arguments("run")
        self.assertEqual(run.func, cmd_e2_run)
        self.assertEqual(run.runner_git_sha, "a" * 40)

    def test_freeze_and_check_dispatch(self):
        frozen = {
            "definition_sha256": "a" * 64,
            "states": [{}] * 18,
            "schedule": [{}] * 90,
        }
        stream = io.StringIO()
        with patch("alf.cli.freeze_definition", return_value=frozen) as freeze, redirect_stdout(stream):
            self.assertEqual(cmd_e2_freeze(self.arguments("freeze")), 0)
        self.assertEqual(json.loads(stream.getvalue())["states"], 18)
        freeze.assert_called_once()

        with patch(
            "alf.cli.check_definition",
            return_value={"ok": False, "errors": ["synthetic"], "definition_sha256": "a" * 64},
        ), redirect_stdout(io.StringIO()):
            self.assertEqual(cmd_e2_check(self.arguments("check")), 1)

    def test_audit_dispatches_report_definition_and_external_raw_path(self):
        args = self.arguments("audit")
        stream = io.StringIO()
        synthetic = '{"definition_sha256":"' + "a" * 64 + '"}'
        with patch("pathlib.Path.read_text", return_value=synthetic), patch(
            "alf.cli.audit_report",
            return_value={"ok": True, "errors": [], "report_sha256": "b" * 64},
        ) as audit, redirect_stdout(stream):
            self.assertEqual(cmd_e2_audit(args), 0)
        self.assertTrue(json.loads(stream.getvalue())["ok"])
        self.assertEqual(audit.call_args.args[2].as_posix(), Path(args.raw_output).resolve().as_posix())

    def test_run_dispatches_every_identity_and_prints_only_publishable_paths(self):
        report = {"report_sha256": "c" * 64, "samples": [{}] * 90}
        stream = io.StringIO()
        args = self.arguments("run")
        with patch("alf.cli.run_baseline", return_value=report) as run, redirect_stdout(stream):
            self.assertEqual(cmd_e2_run(args), 0)
        kwargs = run.call_args.kwargs
        self.assertEqual(kwargs["runner_git_sha"], "a" * 40)
        self.assertEqual(kwargs["container_image_id"], "sha256:" + "b" * 64)
        self.assertEqual(kwargs["raw_output"], "C:/external/raw")
        output = json.loads(stream.getvalue())
        self.assertEqual(output["samples"], 90)
        self.assertNotIn("raw", output)

    def test_run_parser_rejects_short_runner_sha(self):
        argv = [
            "--root",
            "C:/synthetic/repo",
            "e2",
            "run",
            "--definition",
            "definition.json",
            "--runner-git-sha",
            "short",
            "--container-image-id",
            "sha256:" + "b" * 64,
            "--package-cache",
            "cache",
            "--raw-output",
            "raw",
            "--output-json",
            "report.json",
            "--output-markdown",
            "report.md",
        ]
        with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            build_parser().parse_args(argv)


if __name__ == "__main__":
    unittest.main()
