import json
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest.mock import patch

from alf.models import ProcessResult
from alf.runner import (
    _derive_protocol_disposition,
    _prepare_protocol_run,
    _reserve_protocol_run_directory,
    run_chain,
)


class RunnerProtocolTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.root = Path(self.directory.name).resolve()
        self.output = self.root / "results" / "variance-v1"
        self.manifest_path = self.output / "resolved-manifest.json"
        self.manifest_path.parent.mkdir(parents=True)
        self.manifest_path.write_text("{}", encoding="utf-8")
        (self.root / "scripts").mkdir()
        (self.root / "scripts" / "codex-docker.py").write_text("", encoding="utf-8")

        self.benchmark = {
            "schema_version": 1,
            "id": "test-benchmark",
            "languages": {"csharp": {}, "fsharp": {}},
            "baseline_cases": [],
            "tasks": [],
        }
        benchmark_path = self.root / "benchmarks" / "pilot" / "manifest.json"
        benchmark_path.parent.mkdir(parents=True)
        benchmark_path.write_text(json.dumps(self.benchmark), encoding="utf-8")

        self.protocol = {
            "cell_id": "variance-v1",
            "manifest_sha256": "f" * 64,
            "git_head": "a" * 40,
            "definition_sha256": "b" * 64,
            "schedule_sha256": "c" * 64,
            "image": "alf-codex:0.149.1",
            "image_id": "sha256:" + "d" * 64,
            "definition": {
                "benchmark_manifest": "benchmarks/pilot/manifest.json",
                "raw_root": "results/variance-v1",
                "model": {
                    "snapshot": "gpt-5.4-mini-2026-03-17",
                    "reasoning_effort": "medium",
                },
                "limits": {
                    "task_timeout_seconds": 600,
                    "memory": "2g",
                    "cpus": 2,
                    "pids": 256,
                },
                "codex": {"image": "alf-codex:0.149.1"},
            },
            "schedule": {
                "calibration": {
                    "block_id": "calibration-01",
                    "order": ["csharp", "fsharp"],
                    "counting": False,
                },
                "formal": [
                    {"block_id": "block-01", "order": ["csharp", "fsharp"]},
                    {"block_id": "block-03", "order": ["fsharp", "csharp"]},
                ],
            },
        }

    def tearDown(self):
        self.directory.cleanup()

    def _image_result(self, image_id=None):
        return ProcessResult(
            ["docker"],
            0,
            (image_id or self.protocol["image_id"]) + "\n",
            "",
            0.01,
        )

    def _prepare(self, **overrides):
        arguments = {
            "root": self.root,
            "benchmark_manifest": self.benchmark,
            "language": "csharp",
            "agent_name": "command",
            "output_root": self.output,
            "model": "gpt-5.4-mini-2026-03-17",
            "agent_command": None,
            "timeout": 600,
            "max_tasks": None,
            "require_usage": True,
            "protocol_manifest": self.manifest_path,
            "block_id": "calibration-01",
            "order": "csharp-first",
            "attempt_id": "calibration-01-csharp-01",
            "position": 1,
        }
        arguments.update(overrides)
        with (
            patch("alf.runner.load_frozen_manifest", return_value=self.protocol),
            patch("alf.runner.run_process", return_value=self._image_result()),
        ):
            return _prepare_protocol_run(**arguments)

    def _prior_result(self, **overrides):
        value = {
            "finished_at": "2026-08-29T00:00:00+00:00",
            "baseline": {"ok": True},
            "tasks": [
                {
                    "finished_at": "2026-08-29T00:00:00+00:00",
                    "agent": {"process": {"timed_out": False}},
                }
            ],
            "aggregate_accounting_valid": True,
            "success": False,
            "disposition": {
                "analysis_role": "primary",
                "retryable": False,
            },
            "provenance": {
                "cell_id": self.protocol["cell_id"],
                "manifest_sha256": self.protocol["manifest_sha256"],
                "block_id": "calibration-01",
                "order": "csharp-first",
                "position": 1,
                "language": "csharp",
                "attempt_id": "calibration-01-csharp-01",
            },
        }
        value.update(overrides)
        directory = self.output / "prior"
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "result.json").write_text(json.dumps(value), encoding="utf-8")

    def test_partial_protocol_arguments_without_manifest_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "require --protocol-manifest"):
            run_chain(
                root=self.root,
                manifest=self.benchmark,
                language="csharp",
                agent_name="scripted",
                output_root=self.output,
                block_id="block-01",
            )

    def test_manifest_loader_errors_propagate_before_writes(self):
        with patch(
            "alf.runner.load_frozen_manifest",
            side_effect=ValueError("protocol manifest hash mismatch"),
        ):
            with self.assertRaisesRegex(ValueError, "hash mismatch"):
                _prepare_protocol_run(
                    root=self.root,
                    benchmark_manifest=self.benchmark,
                    language="csharp",
                    agent_name="command",
                    output_root=self.output,
                    model="gpt-5.4-mini-2026-03-17",
                    agent_command=None,
                    timeout=600,
                    max_tasks=None,
                    require_usage=True,
                    protocol_manifest=self.manifest_path,
                    block_id="calibration-01",
                    order="csharp-first",
                    attempt_id="calibration-01-csharp-01",
                    position=1,
                )
        self.assertEqual(list(self.output.iterdir()), [self.manifest_path])

    def test_protocol_requires_all_pins_and_rejects_caller_command(self):
        cases = (
            ({"attempt_id": None}, "safe attempt_id"),
            ({"agent_name": "scripted"}, "command agent"),
            ({"require_usage": False}, "require-usage"),
            ({"max_tasks": 1}, "all tasks"),
            ({"agent_command": "custom"}, "caller agent command"),
            ({"model": "wrong"}, "model"),
            ({"timeout": 599}, "timeout"),
        )
        for overrides, message in cases:
            with self.subTest(overrides=overrides):
                with self.assertRaisesRegex(ValueError, message):
                    self._prepare(**overrides)

    def test_schedule_language_order_and_output_are_exact(self):
        cases = (
            ({"block_id": "missing"}, "not in"),
            ({"order": "fsharp-first"}, "mismatch"),
            ({"language": "fsharp"}, "mismatch"),
            ({"output_root": self.root / "results" / "other"}, "raw_root"),
        )
        for overrides, message in cases:
            with self.subTest(overrides=overrides):
                with self.assertRaisesRegex(ValueError, message):
                    self._prepare(**overrides)

    def test_loaded_benchmark_and_image_id_must_match(self):
        with self.assertRaisesRegex(ValueError, "loaded benchmark"):
            self._prepare(benchmark_manifest={"languages": self.benchmark["languages"]})

        with (
            patch("alf.runner.load_frozen_manifest", return_value=self.protocol),
            patch(
                "alf.runner.run_process",
                return_value=self._image_result("sha256:" + "0" * 64),
            ),
        ):
            with self.assertRaisesRegex(ValueError, "image tag"):
                _prepare_protocol_run(
                    root=self.root,
                    benchmark_manifest=self.benchmark,
                    language="csharp",
                    agent_name="command",
                    output_root=self.output,
                    model="gpt-5.4-mini-2026-03-17",
                    agent_command=None,
                    timeout=600,
                    max_tasks=None,
                    require_usage=True,
                    protocol_manifest=self.manifest_path,
                    block_id="calibration-01",
                    order="csharp-first",
                    attempt_id="calibration-01-csharp-01",
                    position=1,
                )

    def test_attempt_ids_are_globally_unique(self):
        self._prior_result()
        with self.assertRaisesRegex(ValueError, "already been used"):
            self._prepare(attempt_id="calibration-01-csharp-01")

    def test_position_two_rejects_missing_or_invalid_first_outcome(self):
        with self.assertRaisesRegex(ValueError, "position-1"):
            self._prepare(
                language="fsharp",
                position=2,
                attempt_id="calibration-01-fsharp-01",
            )

        self._prior_result(
            baseline={"ok": False},
            aggregate_accounting_valid=False,
        )
        with self.assertRaisesRegex(ValueError, "position-1"):
            self._prepare(
                language="fsharp",
                position=2,
                attempt_id="calibration-01-fsharp-01",
            )

    def test_position_two_accepts_accounted_candidate_failure(self):
        self._prior_result()
        protocol, command, attempt_number = self._prepare(
            language="fsharp",
            position=2,
            attempt_id="calibration-01-fsharp-01",
        )
        self.assertIs(protocol, self.protocol)
        self.assertEqual(attempt_number, 1)
        self.assertIn("gpt-5.4-mini-2026-03-17", command)
        self.assertIn('--reasoning-effort "medium"', command)
        self.assertIn('--memory "2g" --cpus 2 --pids-limit 256', command)
        self.assertIn("--require-auth-preflight", command)

    def test_position_two_accepts_candidate_timeout_without_terminal_usage(self):
        timed_out_task = [
            {
                "finished_at": "2026-08-29T00:00:00+00:00",
                "agent": {"process": {"timed_out": True}},
            }
        ]
        self._prior_result(tasks=timed_out_task, aggregate_accounting_valid=False)
        self._prepare(
            language="fsharp",
            position=2,
            attempt_id="calibration-01-fsharp-01",
        )

    def test_position_two_accepts_accounting_invalid_primary(self):
        self._prior_result(aggregate_accounting_valid=False)
        self._prepare(
            language="fsharp",
            position=2,
            attempt_id="calibration-01-fsharp-01",
        )

    def test_primary_outcome_cannot_be_retried_or_replaced(self):
        self._prior_result()
        with self.assertRaisesRegex(ValueError, "primary candidate outcome"):
            self._prepare(attempt_id="calibration-01-csharp-02")

    def test_retryable_infrastructure_attempt_gets_next_sequential_id(self):
        self._prior_result(
            disposition={
                "analysis_role": "infrastructure-invalid",
                "retryable": True,
            }
        )
        _protocol, _command, attempt_number = self._prepare(
            attempt_id="calibration-01-csharp-02"
        )
        self.assertEqual(attempt_number, 2)

    def test_unresolved_started_attempt_blocks_the_position(self):
        record_dir = self.output / "started"
        record_dir.mkdir(parents=True)
        record = {
            "state": "started",
            "provenance": {
                "cell_id": self.protocol["cell_id"],
                "manifest_sha256": self.protocol["manifest_sha256"],
                "block_id": "calibration-01",
                "position": 1,
                "attempt_id": "calibration-01-csharp-01",
            },
        }
        (record_dir / "attempt.json").write_text(json.dumps(record), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "unresolved"):
            self._prepare(attempt_id="calibration-01-csharp-02")

    def test_attempt_directory_reservation_is_atomic(self):
        def reserve() -> str:
            try:
                return _reserve_protocol_run_directory(
                    self.output, "calibration-01-csharp-01"
                ).name
            except ValueError:
                return "rejected"

        with ThreadPoolExecutor(max_workers=2) as pool:
            outcomes = list(pool.map(lambda _index: reserve(), range(2)))
        self.assertCountEqual(
            outcomes, ["calibration-01-csharp-01", "rejected"]
        )

    def test_failure_disposition_is_operational_and_metric_specific(self):
        base = {
            "provenance": {"cell_id": "variance-v1"},
            "baseline": {"ok": True, "build": {"missing_executable": False}},
            "tasks": [
                {
                    "agent": {
                        "process": {
                            "returncode": 0,
                            "timed_out": False,
                            "missing_executable": False,
                        },
                        "auth_ok": True,
                        "usage_available": True,
                        "accounting_errors": [],
                    },
                    "evaluation": {
                        "ok": True,
                        "build": {
                            "returncode": 0,
                            "timed_out": False,
                            "missing_executable": False,
                        },
                        "run": {
                            "returncode": 0,
                            "timed_out": False,
                            "missing_executable": False,
                        },
                    },
                }
            ],
            "aggregate_accounting_valid": True,
            "aggregate_usage_available": True,
            "success": True,
        }
        success = _derive_protocol_disposition(base)
        self.assertIsNone(success["failure_category"])
        self.assertEqual(success["analysis_role"], "primary")
        self.assertTrue(success["include_usage_metrics"])

        timeout = json.loads(json.dumps(base))
        timeout["tasks"][0]["agent"]["process"]["returncode"] = 124
        timeout["tasks"][0]["agent"]["process"]["timed_out"] = True
        timeout["aggregate_accounting_valid"] = False
        timeout["aggregate_usage_available"] = False
        timeout["success"] = False
        disposition = _derive_protocol_disposition(timeout)
        self.assertEqual(disposition["failure_category"], "timeout")
        self.assertTrue(disposition["include_success_time"])
        self.assertFalse(disposition["include_usage_metrics"])
        self.assertFalse(disposition["retryable"])

        auth = json.loads(json.dumps(timeout))
        auth["tasks"][0]["agent"]["process"]["timed_out"] = False
        auth["tasks"][0]["agent"]["process"]["returncode"] = 78
        auth["tasks"][0]["agent"]["auth_ok"] = False
        disposition = _derive_protocol_disposition(auth)
        self.assertEqual(disposition["failure_category"], "auth")
        self.assertEqual(disposition["analysis_role"], "infrastructure-invalid")
        self.assertTrue(disposition["retryable"])

        provider = json.loads(json.dumps(auth))
        provider["tasks"][0]["agent"]["auth_ok"] = True
        provider["tasks"][0]["agent"]["usage_available"] = False
        disposition = _derive_protocol_disposition(provider)
        self.assertEqual(disposition["failure_category"], "provider")

        host = json.loads(json.dumps(provider))
        host["tasks"][0]["agent"]["process"]["missing_executable"] = True
        disposition = _derive_protocol_disposition(host)
        self.assertEqual(disposition["failure_category"], "host")

        evaluator_host = json.loads(json.dumps(base))
        evaluator_host["tasks"][0]["evaluation"]["ok"] = False
        evaluator_host["tasks"][0]["evaluation"]["build"]["returncode"] = 127
        evaluator_host["tasks"][0]["evaluation"]["build"][
            "missing_executable"
        ] = True
        evaluator_host["success"] = False
        disposition = _derive_protocol_disposition(evaluator_host)
        self.assertEqual(disposition["failure_category"], "host")
        self.assertTrue(disposition["retryable"])

        evaluator_timeout = json.loads(json.dumps(base))
        evaluator_timeout["tasks"][0]["evaluation"]["ok"] = False
        evaluator_timeout["tasks"][0]["evaluation"]["run"]["returncode"] = 124
        evaluator_timeout["tasks"][0]["evaluation"]["run"]["timed_out"] = True
        evaluator_timeout["success"] = False
        disposition = _derive_protocol_disposition(evaluator_timeout)
        self.assertEqual(disposition["failure_category"], "timeout")
        self.assertEqual(disposition["analysis_role"], "primary")
        self.assertFalse(disposition["retryable"])

        correctness = json.loads(json.dumps(base))
        correctness["tasks"][0]["evaluation"]["ok"] = False
        correctness["success"] = False
        disposition = _derive_protocol_disposition(correctness)
        self.assertEqual(disposition["failure_category"], "agent")
        self.assertEqual(disposition["analysis_role"], "primary")

        malformed_evaluator = json.loads(json.dumps(base))
        del malformed_evaluator["tasks"][0]["evaluation"]
        malformed_evaluator["success"] = False
        disposition = _derive_protocol_disposition(malformed_evaluator)
        self.assertEqual(disposition["failure_category"], "evaluator")
        self.assertTrue(disposition["retryable"])

        accounting = json.loads(json.dumps(provider))
        accounting["tasks"][0]["agent"]["process"]["returncode"] = 0
        disposition = _derive_protocol_disposition(accounting)
        self.assertEqual(disposition["failure_category"], "accounting")
        self.assertEqual(disposition["analysis_role"], "primary")

        evaluator = json.loads(json.dumps(base))
        evaluator["baseline"]["ok"] = False
        evaluator["tasks"] = []
        evaluator["success"] = False
        disposition = _derive_protocol_disposition(evaluator)
        self.assertEqual(disposition["failure_category"], "evaluator")


if __name__ == "__main__":
    unittest.main()
