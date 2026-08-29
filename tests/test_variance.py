import contextlib
import hashlib
import io
import json
import subprocess
import tempfile
import unittest
from unittest.mock import patch
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from pathlib import Path

from alf.cli import main
from alf.runner import _derive_protocol_disposition
from alf.variance import (_decision, _known_sd_power, _minimum_known_sd_n, _power, _schedule,
                          calibration_fixture, markdown_report, variance_report)


def canonical_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def text_hash(path):
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.sha256(text.encode()).hexdigest()


def timestamp(minute, second=0):
    return (datetime(2026, 1, 1, tzinfo=timezone.utc) + timedelta(minutes=minute, seconds=second)).isoformat()


class SyntheticCell:
    """Build current-schema, audit-valid retained artifacts without transcripts."""

    def __init__(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.cell = self.root / "results" / "synthetic-cell"
        self.cell.mkdir(parents=True)
        protocol = self.root / "protocols" / "synthetic-cell"
        benchmark = self.root / "benchmarks" / "synthetic"
        (benchmark / "tasks").mkdir(parents=True)
        (benchmark / "tasks" / "001-one.md").write_text("Do one thing.\n", encoding="utf-8")
        (benchmark / "tasks" / "002-two.md").write_text("Do another thing.\n", encoding="utf-8")
        benchmark_manifest = {"schema_version": 1, "id": "synthetic", "tasks": [
            {"id": "001-one", "prompt": "benchmarks/synthetic/tasks/001-one.md"},
            {"id": "002-two", "prompt": "benchmarks/synthetic/tasks/002-two.md"},
        ]}
        (benchmark / "manifest.json").write_text(json.dumps(benchmark_manifest, indent=2) + "\n", encoding="utf-8")
        protocol.mkdir(parents=True)
        self.schedule = {"schema_version": 1, "cell_id": "synthetic-cell", "seed": 7,
                         "calibration": {"block_id": "calibration-01", "order": ["csharp", "fsharp"], "counting": False},
                         "formal": [{"block_id": "block-01", "order": ["fsharp", "csharp"]},
                                    {"block_id": "block-02", "order": ["csharp", "fsharp"]}],
                         "constraints": {"formal_blocks": 2, "balanced_first_language": {"csharp": 1, "fsharp": 1},
                                         "max_same_order_run": 1}}
        schedule_path = protocol / "schedule.json"
        schedule_path.write_text(json.dumps(self.schedule, indent=2) + "\n", encoding="utf-8")
        self.definition = {"schema_version": 1, "cell_id": "synthetic-cell",
                           "benchmark_manifest": "benchmarks/synthetic/manifest.json",
                           "benchmark_manifest_sha256": text_hash(benchmark / "manifest.json"),
                           "task_hashes": {"001-one": text_hash(benchmark / "tasks" / "001-one.md"),
                                           "002-two": text_hash(benchmark / "tasks" / "002-two.md")},
                           "schedule_file": "protocols/synthetic-cell/schedule.json",
                           "fresh_process": True,
                           "model": {"snapshot": "synthetic-model", "reasoning_effort": "medium"},
                           "codex": {"image": "synthetic:1"}}
        definition_path = protocol / "definition.json"
        definition_path.write_text(json.dumps(self.definition, indent=2) + "\n", encoding="utf-8")
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)
        subprocess.run(["git", "config", "user.name", "Synthetic"], cwd=self.root, check=True)
        subprocess.run(["git", "config", "user.email", "synthetic@example.invalid"], cwd=self.root, check=True)
        subprocess.run(["git", "add", "protocols", "benchmarks"], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-qm", "synthetic frozen sources"], cwd=self.root, check=True)
        self.head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.root, text=True).strip()
        self.manifest = {"schema_version": 1, "cell_id": "synthetic-cell", "definition": self.definition,
                         "definition_file": "protocols/synthetic-cell/definition.json", "definition_sha256": text_hash(definition_path),
                         "schedule": self.schedule, "schedule_sha256": text_hash(schedule_path), "dirty": False, "frozen": True,
                         "git_head": self.head, "image": "synthetic:1", "image_id": "sha256:" + "a" * 64}
        self.manifest["manifest_sha256"] = canonical_hash(self.manifest)
        self.manifest_bytes = (json.dumps(self.manifest, indent=2, sort_keys=True) + "\n").encode()
        (self.cell / "resolved-manifest.json").write_bytes(self.manifest_bytes)
        # One retryable infrastructure failure before the block-01 F# primary.
        self.write_attempt("calibration-01", "csharp", 1, 1, "csharp-first", 0, calibration=True)
        self.write_attempt("calibration-01", "fsharp", 2, 1, "csharp-first", 30, calibration=True)
        self.write_attempt("block-01", "fsharp", 1, 1, "fsharp-first", 60, infrastructure=True)
        self.write_attempt("block-01", "fsharp", 1, 2, "fsharp-first", 70, token_base=130)
        self.write_attempt("block-01", "csharp", 2, 1, "fsharp-first", 100, token_base=100)
        self.write_attempt("block-02", "csharp", 1, 1, "csharp-first", 130, token_base=110)
        self.write_attempt("block-02", "fsharp", 2, 1, "csharp-first", 160, token_base=90, candidate_failure=True)

    def close(self):
        self.temporary.cleanup()

    def provenance(self, block, language, position, number, order):
        return {"attempt_id": f"{block}-{language}-{number:02d}", "attempt_number": number, "block_id": block,
                "cell_id": "synthetic-cell", "definition_sha256": self.manifest["definition_sha256"], "git_head": self.head,
                "image": "synthetic:1", "image_id": self.manifest["image_id"], "language": language,
                "manifest_file": "protocol-manifest.json", "manifest_sha256": self.manifest["manifest_sha256"],
                "model": "synthetic-model", "order": order, "position": position, "reasoning_effort": "medium",
                "schedule_sha256": self.manifest["schedule_sha256"]}

    @staticmethod
    def evaluation(ok=True):
        return {"ok": ok, "build": {"returncode": 0, "timed_out": False, "missing_executable": False},
                "run": {"returncode": 0, "timed_out": False, "missing_executable": False},
                "case_results": [{"name": "synthetic case", "passed": ok}], "evaluator_wall_seconds": 2.0}

    def task(self, task_id, token_base, start, *, success=True, infrastructure=False):
        usage = {"input_tokens": token_base, "cached_input_tokens": token_base // 2, "cache_write_input_tokens": 0,
                 "output_tokens": token_base // 10, "reasoning_output_tokens": token_base // 20, "tool_calls": 3}
        agent = {"accounting_valid": not infrastructure, "usage_available": not infrastructure,
                 "accounting_errors": ["protocol sidecar mismatch"] if infrastructure else [],
                 "usage": None if infrastructure else usage, "usage_record_count": 0 if infrastructure else 1,
                 "ok": not infrastructure, "auth_ok": True, "command_count": 4, "file_change_count": 1,
                 "file_reads": 2, "unique_file_reads": 1, "file_revisits": 1, "agent_process_wall_seconds": 5.0,
                 "process": {"returncode": 1 if infrastructure else 0, "timed_out": False,
                             "missing_executable": False, "duration_seconds": 5.0}}
        return {"task_id": task_id, "started_at": timestamp(start, 1),
                "finished_at": timestamp(start, 11), "success": success and not infrastructure,
                "agent": agent, "evaluation": self.evaluation(success and not infrastructure),
                "diff": {"changed_files": 1, "added_lines": 3, "deleted_lines": 1, "diff_bytes": 50},
                "task_total_wall_seconds": 10.0}

    def write_attempt(self, block, language, position, number, order, minute, *, calibration=False,
                      infrastructure=False, candidate_failure=False, token_base=120):
        attempt_id = f"{block}-{language}-{number:02d}"; run = self.cell / attempt_id
        (run / "tasks").mkdir(parents=True); (run / "workspace").mkdir()
        (run / "workspace" / ("Program.fs" if language == "fsharp" else "Program.cs")).write_text(f"// {attempt_id}\n", encoding="utf-8")
        tasks = [self.task("001-one", token_base, minute, infrastructure=infrastructure)]
        if not infrastructure:
            tasks.append(self.task("002-two", token_base + 10, minute + 1, success=not candidate_failure))
        aggregate = None if infrastructure else {name: sum(task["agent"]["usage"][name] for task in tasks) for name in
                                                  ("input_tokens", "cached_input_tokens", "cache_write_input_tokens", "output_tokens", "reasoning_output_tokens", "tool_calls")}
        provenance = self.provenance(block, language, position, number, order)
        result = {"schema_version": 1, "run_id": attempt_id, "language": language, "agent": "command", "requested_model": "synthetic-model",
                  "require_usage": True, "started_at": timestamp(minute),
                  "finished_at": timestamp(minute, 20), "success": not infrastructure and not candidate_failure,
                  "provenance": provenance, "baseline": self.evaluation(), "tasks": tasks,
                  "aggregate_accounting_valid": not infrastructure, "aggregate_usage_available": not infrastructure,
                  "aggregate_usage": aggregate, "agent_process_wall_seconds": 5.0 * len(tasks),
                  "evaluator_wall_seconds": 2.0 * (len(tasks) + 1), "run_total_wall_seconds": 20.0}
        result["disposition"] = _derive_protocol_disposition(result)
        run.joinpath("protocol-manifest.json").write_bytes(self.manifest_bytes)
        for task in tasks:
            directory = run / "tasks" / task["task_id"]; directory.mkdir()
            directory.joinpath("task-result.json").write_text(json.dumps(task), encoding="utf-8")
            if not infrastructure:
                directory.joinpath("usage.json").write_text(json.dumps(task["agent"]["usage"]), encoding="utf-8")
        run.joinpath("result.json").write_text(json.dumps(result), encoding="utf-8")
        envelope = {"schema_version": 1, "run_id": attempt_id, "state": "completed", "started_at": result["started_at"],
                    "finished_at": result["finished_at"], "provenance": provenance, "disposition": result["disposition"]}
        run.joinpath("attempt.json").write_text(json.dumps(envelope), encoding="utf-8")


class VarianceReportTests(unittest.TestCase):
    def setUp(self):
        self.fixture = SyntheticCell()

    def tearDown(self):
        self.fixture.close()

    def report(self):
        return variance_report(self.fixture.cell, bootstrap_samples=30, power_simulations=30, seed=11)

    def test_full_current_schema_contract_and_self_hash(self):
        report = self.report()
        self.assertTrue(report["structural_validation"]["ok"], report["structural_validation"]["errors"])
        self.assertEqual(report["counts"]["attempts"], 7)
        self.assertEqual(report["counts"]["formal_primary"], 4)
        self.assertEqual(report["counts"]["calibration_primary"], 2)
        self.assertEqual(report["counts"]["excluded_infrastructure"], 1)
        self.assertEqual(report["counts"]["complete_blocks"], 2)
        self.assertEqual(report["counts"]["formal_accounting"], {"valid": 4, "expected": 4})
        self.assertEqual(report["counts"]["formal_task_accounting"], {"valid": 8, "expected": 8})
        self.assertEqual(report["outcomes_and_metrics"]["per_language"]["fsharp"]["chain_outcomes"]["failures"], 1)
        self.assertEqual(report["outcomes_and_metrics"]["per_language"]["fsharp"]["task_outcomes"]["failures"], 1)
        self.assertIn("001-one", report["paired_blocks"][0]["tasks"])
        self.assertEqual(report["paired_blocks"][0]["metrics"]["input_tokens"]["difference_fsharp_minus_csharp"], 60)
        self.assertIsNotNone(report["paired_bootstrap"]["aggregate"]["input_tokens"]["difference_fsharp_minus_csharp"]["descriptive"]["sample_sd"])
        self.assertEqual(report["variance_diagnostics"]["order_strata"]["fsharp-first"]["blocks"], 1)
        self.assertIn("by_utc_elapsed_day", report["variance_diagnostics"]["temporal"]["trends"]["input_tokens"])
        self.assertTrue(report["variance_diagnostics"]["cross_metric_agreement"])
        self.assertIn("sample_variance", report["outcomes_and_metrics"]["per_language"]["fsharp"]["per_task"]["001-one"]["metrics"]["input_tokens"])
        unsigned = dict(report); claimed = unsigned.pop("report_sha256")
        self.assertEqual(claimed, canonical_hash(unsigned))

    def test_retryable_infrastructure_is_retained_but_metric_excluded(self):
        report = self.report()
        excluded = report["excluded_attempts"][0]
        self.assertEqual(excluded["failure_category"], "protocol")
        self.assertTrue(all(value is None for value in excluded["metrics"].values()))
        self.assertEqual([a["attempt_number"] for a in report["attempts"] if a["block_id"] == "block-01" and a["language"] == "fsharp"], [1, 2])
        self.assertEqual(report["frozen_rule_sensitivity"]["excluded_infrastructure_attempts"], 1)

    def test_retry_sequence_rejects_a_second_primary(self):
        run = self.fixture.cell / "block-01-fsharp-01"
        result_path, attempt_path = run / "result.json", run / "attempt.json"
        result, envelope = json.loads(result_path.read_text()), json.loads(attempt_path.read_text())
        bad = dict(result["disposition"])
        bad.update({"analysis_role": "primary", "candidate_outcome": True, "retryable": False})
        result["disposition"] = bad; envelope["disposition"] = bad
        result_path.write_text(json.dumps(result)); attempt_path.write_text(json.dumps(envelope))
        report = self.report()
        errors = report["structural_validation"]["errors"]
        self.assertTrue(any("must end in exactly one primary" in error for error in errors))
        self.assertTrue(any("frozen deterministic classification" in error for error in errors))

    def test_posthoc_manifest_verification_uses_frozen_git_sources(self):
        definition = self.fixture.root / "protocols" / "synthetic-cell" / "definition.json"
        definition.write_text("{}\n", encoding="utf-8")
        report = self.report()
        self.assertTrue(report["structural_validation"]["ok"], report["structural_validation"]["errors"])
        self.assertEqual(report["generated_from"]["manifest_sources"]["definition"]["sha256"],
                         self.fixture.manifest["definition_sha256"])

    def test_schedule_constraints_are_revalidated(self):
        manifest = deepcopy(self.fixture.manifest)
        manifest["schedule"]["formal"][1]["order"] = ["fsharp", "csharp"]
        errors = []
        _schedule(manifest, errors)
        self.assertTrue(any("balance disagrees" in error for error in errors))
        self.assertTrue(any("max_same_order_run" in error for error in errors))

    def test_report_never_opens_transcript_files(self):
        for run in self.fixture.cell.iterdir():
            if run.is_dir() and (run / "result.json").is_file():
                (run / "agent.stdout").write_text("poison transcript", encoding="utf-8")
                (run / "events.jsonl").write_text("not json", encoding="utf-8")
        original = Path.read_text
        def guarded(path, *args, **kwargs):
            if path.name in {"agent.stdout", "agent.stderr", "events.jsonl"}:
                raise AssertionError(f"opened transcript {path.name}")
            return original(path, *args, **kwargs)
        with patch.object(Path, "read_text", guarded):
            report = self.report()
        self.assertTrue(report["structural_validation"]["ok"])

    def test_primary_task_omission_and_duplication_are_rejected(self):
        result_path = self.fixture.cell / "block-02-csharp-01" / "result.json"
        result = json.loads(result_path.read_text())
        result["tasks"] = result["tasks"][:1]
        result["aggregate_usage"] = result["tasks"][0]["agent"]["usage"]
        result_path.write_text(json.dumps(result))
        report = self.report()
        self.assertTrue(any("exact frozen order" in error for error in report["structural_validation"]["errors"]))

        # Rebuild the cell, then duplicate an otherwise valid embedded task.
        self.fixture.close(); self.fixture = SyntheticCell()
        result_path = self.fixture.cell / "block-02-csharp-01" / "result.json"
        result = json.loads(result_path.read_text())
        result["tasks"].append(deepcopy(result["tasks"][0]))
        result_path.write_text(json.dumps(result))
        report = self.report()
        self.assertTrue(any("unique strings" in error for error in report["structural_validation"]["errors"]))

    def test_exact_manifest_provenance_attempt_and_schedule_tampering_fails(self):
        target = self.fixture.cell / "block-02-fsharp-01" / "protocol-manifest.json"
        target.write_bytes(target.read_bytes() + b" ")
        report = self.report()
        self.assertFalse(report["structural_validation"]["ok"])
        self.assertTrue(any("exact byte copy" in error for error in report["structural_validation"]["errors"]))
        target.write_bytes(self.fixture.manifest_bytes)
        envelope_path = self.fixture.cell / "block-02-fsharp-01" / "attempt.json"
        envelope = json.loads(envelope_path.read_text()); envelope["unexpected"] = True
        envelope_path.write_text(json.dumps(envelope))
        report = self.report()
        self.assertTrue(any("attempt envelope fields are not exact" in error for error in report["structural_validation"]["errors"]))

    def test_positive_resampling_arguments_required(self):
        with self.assertRaisesRegex(ValueError, "bootstrap_samples must be positive"):
            variance_report(self.fixture.cell, bootstrap_samples=0)
        with self.assertRaisesRegex(ValueError, "power_simulations must be positive"):
            variance_report(self.fixture.cell, power_simulations=0)

    def test_analytic_known_sd_power_is_calibratable_and_monotone(self):
        curve = [_known_sd_power(1.0, 1.0, n) for n in range(1, 15)]
        self.assertTrue(all(left <= right for left, right in zip(curve, curve[1:])))
        self.assertEqual(next(n for n in range(1, 100) if _known_sd_power(1.0, 1.0, n) >= .8), 8)
        self.assertEqual(_minimum_known_sd_n(1.0, 1.0), 8)
        self.assertAlmostEqual(_known_sd_power(1.0, 1.0, 8), 0.8074304194325572)
        self.assertGreater(_minimum_known_sd_n(.001, 100.0), 100_000)
        with self.assertRaises(ValueError):
            _known_sd_power(1.0, 0.0, 8)

    def test_power_analytic_minimum_and_simulation_cross_check_are_deterministic(self):
        pairs = [{"order": order, "metrics": {"input_tokens": {"log_ratio_fsharp_over_csharp": value}}}
                 for order, values in (("fsharp-first", (.1, .3, -.1)), ("fsharp-second", (-.2, .2, .4)))
                 for value in values]
        first, second = _power(pairs, 50, 123), _power(pairs, 50, 123)
        self.assertEqual(first, second)
        for effect in first["effects"].values():
            analytic = effect["analytic_power_grid"]
            self.assertTrue(all(left["power"] <= right["power"] for left, right in zip(analytic, analytic[1:])))
            minimum = effect["analytic_minimum_pairs_at_80_percent"]
            self.assertGreaterEqual(_known_sd_power(effect["log_effect"], first["paired_log_ratio_residual_sd"], minimum), .8)
            self.assertLess(_known_sd_power(effect["log_effect"], first["paired_log_ratio_residual_sd"], minimum-1), .8)
            self.assertTrue(all(row["simulations"] == 50 for row in effect["simulation_cross_check"]))

    def test_decision_reports_combined_and_individual_gates(self):
        counts = {"complete_blocks": 10, "scheduled_formal_blocks": 10}
        def language(task_successes, chain_successes):
            return {"fsharp": {"task_outcomes": {"n": 20, "successes": task_successes[0]}, "chain_outcomes": {"n": 10, "successes": chain_successes[0]}},
                    "csharp": {"task_outcomes": {"n": 20, "successes": task_successes[1]}, "chain_outcomes": {"n": 10, "successes": chain_successes[1]}}}
        def power(minimum):
            return {"effects": {"7_percent": {"analytic_minimum_pairs_at_80_percent": minimum},
                                "8_percent": {"analytic_minimum_pairs_at_80_percent": minimum-20}}}
        combined = _decision([], counts, power(220), language((19, 20), (9, 10)))
        self.assertEqual(combined["outcome"], "variance_overwhelms_plausible_effects_and_correctness_near_saturated")
        self.assertEqual(combined["formal_success"]["tasks"], {"successes": 39, "attempts": 40, "rate": .975})
        self.assertEqual(combined["formal_success"]["chains"], {"successes": 19, "attempts": 20, "rate": .95})
        rationale = " ".join(combined["rationale"]).lower()
        for phrase in ("extend or recalibrate", "blocking", "repetitions", "39/40", "19/20"):
            self.assertIn(phrase, rationale)
        variance_only = _decision([], counts, power(220), language((15, 15), (8, 8)))
        self.assertEqual(variance_only["outcome"], "variance_overwhelms_plausible_7_to_8_percent_effects")
        saturation_only = _decision([], counts, power(80), language((19, 20), (9, 10)))
        self.assertEqual(saturation_only["outcome"], "measurement_stable_but_correctness_near_saturated")
        structural = _decision(["bad envelope"], counts, power(220), language((19, 20), (9, 10)))
        self.assertIn("repair the apparatus", structural["next_action"].lower())
        self.assertNotIn("extend or recalibrate", structural["next_action"].lower())
        incomplete = _decision([], {"complete_blocks": 9, "scheduled_formal_blocks": 10}, power(220), language((19, 20), (9, 10)))
        self.assertIn("scheduled slot", incomplete["next_action"].lower())

    def test_calibration_fixture_is_deterministic_redacted_and_self_hashed(self):
        first, second = calibration_fixture(self.report()), calibration_fixture(self.report())
        self.assertEqual(first, second)
        unsigned = dict(first); claimed = unsigned.pop("calibration_sha256")
        self.assertEqual(claimed, canonical_hash(unsigned))
        serialized = json.dumps(first)
        self.assertNotIn(str(self.fixture.root), serialized)
        self.assertNotIn("stdout", serialized)
        self.assertFalse(first["transcripts_included"])
        self.assertEqual(first["summary"]["primary_attempts"], 2)
        self.assertEqual(first["summary"]["single_terminal_usage_tasks"], 4)
        self.assertTrue(all(len(file["sha256"]) == 64 for attempt in first["primary_attempts"] for file in attempt["source_tree"]["files"]))

    def test_cli_outputs_are_byte_reproducible_and_markdown_substantive(self):
        out1, out2 = self.fixture.root / "out1", self.fixture.root / "out2"
        outputs = []
        for output in (out1, out2):
            output.mkdir()
            argv = ["variance-report", str(self.fixture.cell), "--output-json", str(output/"report.json"),
                    "--output-markdown", str(output/"report.md"), "--output-calibration", str(output/"calibration.json"),
                    "--bootstrap-samples", "20", "--power-simulations", "20", "--seed", "17"]
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(main(argv), 0)
            outputs.append(output)
        for name in ("report.json", "report.md", "calibration.json"):
            self.assertEqual((outputs[0]/name).read_bytes(), (outputs[1]/name).read_bytes())
        markdown = (out1/"report.md").read_text()
        for section in ("Correctness outcomes", "Aggregate metrics", "Paired effects", "Power planning", "Decision"):
            self.assertIn(section, markdown)
        self.assertNotIn(str(self.fixture.root), (out1/"report.json").read_text())


if __name__ == "__main__":
    unittest.main()
