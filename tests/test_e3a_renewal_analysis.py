import copy
import hashlib
import importlib.util
import json
import unittest
import tempfile
from pathlib import Path

from alf.protocol import canonical_json_hash


PATH = Path(__file__).parents[1] / "reports/workstream-e3a-oauth-renewal-2026-09-09/analyze-pilot.py"
SPEC = importlib.util.spec_from_file_location("renewal_analysis", PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


TASK = "007-query-engine-refactor"


def source(tag, language="csharp"):
    if language == "fsharp":
        return {"OrderFlow.fsproj": "<Project><ItemGroup><Compile Include=\"OrderFlowEngine.fs\" /><Compile Include=\"Program.fs\" /></ItemGroup></Project>",
                "OrderFlowEngine.fs": f"// {tag}", "Program.fs": f"// {tag}"}
    return {"OrderFlowEngine.cs": f"// {tag}", "Program.cs": f"// {tag}"}


def slot(language="csharp", repetition=1, first=None, terminal=None, status="finished"):
    first = first or source("first", language)
    terminal = terminal if terminal is not None else first
    rounds = [
            {"submission": "{}", "applied_source": first, "applied_sha256": canonical_json_hash(first), "development": {}, "usage": {k: None for k in ("input_tokens", "cached_input_tokens", "cache_write_input_tokens", "output_tokens", "reasoning_output_tokens")}},
        {"submission": "{}", "applied_source": terminal, "applied_sha256": canonical_json_hash(terminal), "development": {}, "usage": {k: None for k in ("input_tokens", "cached_input_tokens", "cache_write_input_tokens", "output_tokens", "reasoning_output_tokens")}},
    ]
    scores = {endpoint: {"format": True, "build": True, "holdout_behavior": True,
                         "declared_obligations": None, "task_completion": None,
                         "holdout_evaluation": {"passed": True, "build_passed": True}}
              for endpoint in ("first", "terminal")}
    return {"slot_id": f"{repetition}-{language}", "task_id": TASK, "language": language,
            "repetition": repetition, "status": status, "reason": None,
            "trajectory": {"rounds": rounds, "first_phase_usage": {}, "repair_usage": {}, "total_usage": {}},
            "scores": scores, "elapsed_seconds": None}


def report():
    slots = []
    for repetition in range(1, 3):
        for language in ("csharp", "fsharp"):
            slots.append(slot(language, repetition))
    return {"specification_sha256": canonical_json_hash(spec()), "slots": slots}


def spec():
    return {"tasks": [TASK], "repetitions": 2}


class RenewalAnalysisTests(unittest.TestCase):
    def test_packets_are_blinded_and_deduplicated(self):
        packets, mapping = MODULE.prepare_review_packets(report())
        self.assertEqual(len(packets), 2)
        self.assertEqual({"source", "source_sha256", "language"}, set(packets[0]))
        self.assertEqual(len(mapping), 8)
        self.assertNotIn("slot_id", packets[0])

    def test_invalid_terminal_does_not_salvage_last_applied_source(self):
        value = report()
        bad = value["slots"][0]
        bad["trajectory"]["rounds"][-1] = {"applied_source": None, "applied_sha256": None}
        packets, mapping = MODULE.prepare_review_packets(value)
        self.assertEqual(len(packets), 2)
        self.assertIsNone(next(x for x in mapping if x["slot_id"] == bad["slot_id"] and x["endpoint"] == "terminal")["source_sha256"])

    def test_source_bound_review_and_known_failure(self):
        value = report()
        raw_before = copy.deepcopy(value["slots"][0]["scores"])
        packets, _ = MODULE.prepare_review_packets(value)
        digest = packets[0]["source_sha256"]
        reviews = {digest: {"reviewer_id": "r1", "reviewer_type": "ai-session",
                            "source_sha256": digest, "domain_model_in_engine": False, "live_dispatch_in_engine": True,
                            "program_io_boundary": True}}
        result = MODULE.analyze(value, spec(), reviews)
        derived = result["slots"][0]["derived_scores"]["first"]
        self.assertFalse(derived["declared_obligations"])
        self.assertEqual(len(result["reviews_applied"]), 1)
        self.assertEqual(result["slots"][0]["scores"], raw_before)
        self.assertIn("FORMAT/BUILD/DEVELOPMENT/HOLDOUT/OBLIGATIONS/COMPLETION", MODULE.render_markdown(result))

    def test_review_mismatch_rejected_and_report_unchanged(self):
        value = report()
        before = copy.deepcopy(value)
        with self.assertRaises(ValueError):
            MODULE.analyze(value, spec(), {"deadbeef": {"reviewer_id": "r", "reviewer_type": "human"}})
        self.assertEqual(value, before)

    def test_hashes_distinguish_canonical_value_from_exact_report_bytes(self):
        value = report()
        exact = hashlib.sha256(b'{"slots": []}\n').hexdigest()
        result = MODULE.analyze(value, spec(), report_file_sha256=exact)
        self.assertEqual(result["report_file_sha256"], exact)
        self.assertEqual(result["report_canonical_sha256"], canonical_json_hash(value))

    def test_review_requires_explicit_source_hash(self):
        value = report()
        digest = MODULE.prepare_review_packets(value)[0][0]["source_sha256"]
        with self.assertRaises(ValueError):
            MODULE.analyze(value, spec(), {digest: {"reviewer_id": "r", "reviewer_type": "human"}})

    def test_report_specification_identity_is_required(self):
        value = report()
        value.pop("specification_sha256")
        with self.assertRaises(ValueError):
            MODULE.analyze(value, spec())
        value = report()
        value["specification_sha256"] = "wrong"
        with self.assertRaises(ValueError):
            MODULE.analyze(value, spec())

    def test_markdown_has_endpoint_rows_and_phase_table(self):
        value = report()
        for current in value["slots"]:
            for index, round_ in enumerate(current["trajectory"]["rounds"]):
                round_["usage"].update({"input_tokens": 10 if index == 0 else 30, "output_tokens": 2 if index == 0 else 6})
        result = MODULE.analyze(value, spec())
        text = MODULE.render_markdown(result)
        self.assertEqual(text.count("| 1-csharp | first |"), 1)
        self.assertIn("| csharp | initial | 2 | 20 | 4 |", text)
        self.assertIn("| csharp | repair | 2 | 60 | 12 |", text)
        self.assertIn("| csharp | total | 4 | 80 | 16 |", text)
        self.assertNotIn("\r", text)

    def test_all_true_review_derives_completion_without_mutating_raw(self):
        value = report()
        raw = copy.deepcopy(value["slots"][0]["scores"])
        packets, _ = MODULE.prepare_review_packets(value)
        digest = packets[0]["source_sha256"]
        review = {digest: {"source_sha256": digest, "reviewer_id": "r", "reviewer_type": "human",
                           "domain_model_in_engine": True, "live_dispatch_in_engine": True, "program_io_boundary": True}}
        result = MODULE.analyze(value, spec(), review)
        self.assertTrue(result["slots"][0]["derived_scores"]["first"]["task_completion"])
        self.assertIsNone(result["slots"][0]["scores"]["first"]["task_completion"])
        self.assertEqual(result["slots"][0]["scores"], raw)
        self.assertIn("| 1-csharp | first | ? | 1/1/?/1/1/1 |", MODULE.render_markdown(result))

    def test_cli_outputs_have_exact_hash_and_lf(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            report_path = root / "report.json"
            spec_path = root / "spec.json"
            output = root / "out"
            report_path.write_text(json.dumps(report()), encoding="utf-8", newline="\n")
            spec_path.write_text(json.dumps(spec()), encoding="utf-8", newline="\n")
            self.assertEqual(MODULE.main(["--report", str(report_path), "--spec", str(spec_path), "--output-dir", str(output)]), 0)
            expected = hashlib.sha256(report_path.read_bytes()).hexdigest()
            data = json.loads((output / "analysis.json").read_text(encoding="utf-8"))
            self.assertEqual(data["report_file_sha256"], expected)
            for path in output.iterdir():
                self.assertNotIn(b"\r\n", path.read_bytes())

    def test_duplicate_review_keys_are_rejected_by_json_hook(self):
        with self.assertRaises(ValueError):
            json.loads('{"a": 1, "a": 2}', object_pairs_hook=MODULE._reject_duplicate_keys)


if __name__ == "__main__":
    unittest.main()
