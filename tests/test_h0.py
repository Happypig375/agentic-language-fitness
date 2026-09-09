import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import alf.h0 as h0
from alf.h0 import SourceFixture, default_renderer, input_allowance, source_allowance, tokenize


class FakeEncoding:
    name = "o200k_base"
    def encode(self, text):
        return list(text.encode("utf-8"))


class H0FixtureTests(unittest.TestCase):
    def test_utf8_identity_reference_and_assembled_text(self):
        fixture = SourceFixture({"a.cs": "é"})
        first, reference = fixture.read("a.cs"), fixture.read("a.cs")
        self.assertEqual((first.returned, first.charge_bytes, first.text), ("full", 2, "é"))
        self.assertEqual((reference.returned, reference.charge_bytes, reference.text), ("reference", 0, None))
        self.assertIn("é".encode(), fixture.assembled_request())

    def test_eviction_clear_and_changed_version(self):
        fixture = SourceFixture({"a": "old"}); fixture.read("a"); fixture.evict("a")
        self.assertEqual(fixture.read("a").returned, "full"); fixture.clear()
        self.assertEqual(fixture.read("a").returned, "full"); fixture.update("a", "old")
        self.assertEqual(fixture.read("a").returned, "reference"); fixture.update_existing_path("a", "new")
        self.assertEqual(fixture.read("a").text, "new")

    def test_input_map_is_copied_and_same_text_paths_are_distinct(self):
        original = {"a": "same", "b": "same"}; fixture = SourceFixture(original)
        self.assertNotEqual(fixture.read("a").identity, fixture.read("b").identity); fixture.update("a", "changed")
        self.assertEqual(original["a"], "same")

    def test_resident_cap_is_current_envelope_not_cumulative_exposure(self):
        cap = len(default_renderer({"a": "x"}))
        fixture = SourceFixture({"a": "x"}, budget=cap)
        for _ in range(cap + 1):
            self.assertEqual(fixture.read("a").returned, "full")
            fixture.evict("a")
        self.assertGreater(fixture.exposure_bytes, cap)
        self.assertEqual(fixture.unique_exposed_bytes, 1)
        self.assertEqual(fixture.resident_bytes, 0)

    def test_refused_new_path_preserves_nonempty_state(self):
        cap = len(default_renderer({"a": "x"})); fixture = SourceFixture({"a": "x", "oversized": "z" * 100}, budget=cap)
        fixture.read("a"); before = (fixture.resident_paths, fixture.exposure_bytes, set(fixture.unique_exposed), fixture.assembled_request())
        with self.assertRaises(ValueError): fixture.read("oversized")
        self.assertEqual(before, (fixture.resident_paths, fixture.exposure_bytes, set(fixture.unique_exposed), fixture.assembled_request()))
        self.assertEqual(fixture.events[-1]["event"], "refused")

    def test_exact_boundary_and_one_byte_over(self):
        exact = SourceFixture({"a": "x"}, budget=len(default_renderer({"a": "x"}))); exact.read("a")
        over = SourceFixture({"a": "xx"}, budget=len(default_renderer({"a": "x"})))
        with self.assertRaises(ValueError): over.read("a")

    def test_allowance_strictness_and_reserve_once(self):
        definition = {"synthetic_budget": {"request_cap": 10, "output_reserve": 2, "safety_margin": 1}}
        self.assertEqual(input_allowance(definition), 7); self.assertEqual(input_allowance(definition, convention="input-only"), 9)
        self.assertEqual(source_allowance(definition, 3), 4)
        for bad in (True, -1):
            with self.assertRaises(ValueError): SourceFixture({}, cap=bad)
        with self.assertRaises(ValueError): SourceFixture({}, convention="other")

    def test_token_proxy_uses_utf8_bytes_with_fake_encoder(self):
        result = tokenize("é".encode(), FakeEncoding()); self.assertEqual(result["tokens"], 2)
        self.assertEqual(len(result["token_stream_sha256"]), 64)


class H0DefinitionTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(__file__).resolve().parents[1]; self.path = self.root / "protocols/workstream-h0/definition.json"
        self.definition = h0._definition(self.root, self.path)

    def test_manifest_task_predecessor_roles_and_source_pins(self):
        source = h0.source_for(self.root, self.definition, "csharp")
        self.assertEqual(set(source), {"OrderFlow.csproj", "OrderFlowEngine.cs", "Program.cs"})
        self.assertEqual(self.definition["task_id"], "008-summary-api"); self.assertEqual(self.definition["predecessor_task_id"], "007-query-engine-refactor")

    def test_manifest_binding_and_contract_mutations_refuse(self):
        with self.assertRaises(ValueError): h0.source_for(self.root, dict(self.definition, manifest_sha256="0" * 64), "csharp")
        missing_contract_pin = dict(self.definition)
        missing_contract_pin.pop("contracts_sha256")
        with self.assertRaises(ValueError): h0.contract_payload(self.root, missing_contract_pin)
        with patch.object(h0, "_text", return_value="altered"):
            with self.assertRaises(ValueError): h0.contract_payload(self.root, self.definition)

    def test_task_predecessor_roles_and_source_hash_mutations_refuse(self):
        for replacement in (
            {**self.definition, "task_id": "wrong"},
            {**self.definition, "predecessor_task_id": "wrong"},
        ):
            with self.assertRaises(ValueError): h0.source_for(self.root, replacement, "csharp")
        bad_roles = copy.deepcopy(self.definition)
        bad_roles["roles"]["csharp"]["engine"] = "Program.cs"
        with self.assertRaises(ValueError): h0.source_for(self.root, bad_roles, "csharp")
        bad_source = copy.deepcopy(self.definition)
        bad_source["source_sha256"]["csharp"] = "0" * 64
        with self.assertRaises(ValueError): h0.source_for(self.root, bad_source, "csharp")

    def test_contract_hash_is_checked_before_envelope(self):
        with patch.object(h0, "_text", side_effect=lambda root, path: "altered"):
            with self.assertRaises(ValueError): h0.envelope(self.root, self.definition, "csharp", {}, ["project", "engine", "io"])

    def test_role_orders_are_exact_and_source_only(self):
        source = h0.source_for(self.root, self.definition, "fsharp")
        first = h0.envelope(self.root, self.definition, "fsharp", source, self.definition["role_orders"][0])
        second = h0.envelope(self.root, self.definition, "fsharp", source, self.definition["role_orders"][1])
        self.assertNotEqual(first, second)
        payload = json.loads(first)
        entries = payload["transcript"][0]["data"]["source"]
        self.assertEqual([entry["role"] for entry in entries], self.definition["role_orders"][0])
        self.assertEqual({entry["filename"] for entry in entries}, set(source))
        self.assertTrue(all(entry["text"] == source[entry["filename"]] for entry in entries))

    def test_audit_reports_four_envelopes_and_null_provider_fields(self):
        with patch.object(h0, "tokenize", return_value={"tokens": 1, "token_stream_sha256": "x" * 64}): report = h0.audit(self.root, self.path)
        self.assertEqual(len(report["envelopes"]), 4); self.assertIsNone(report["provider_input"]); self.assertIsNone(report["physical_fit"]); self.assertEqual(report["candidate_model_calls"], 0)
        self.assertNotIn("source_accounting", report)
        self.assertEqual(report["controls"]["scope"], "synthetic-control-fixtures-only")
        for entry in report["envelopes"]:
            self.assertIn("empty_source_envelope_bytes", entry)
            self.assertIn("source_allowance", entry)
            self.assertTrue(all(entry["synthetic_fit"].values()))
            self.assertEqual(
                entry["source_allowance"]["joint"],
                entry["input_allowance"]["joint"] - entry["empty_source_envelope_bytes"],
            )

    def test_false_fit_is_rejected(self):
        constrained = copy.deepcopy(self.definition)
        source = h0.source_for(self.root, constrained, "csharp")
        serialized = h0.envelope(
            self.root,
            constrained,
            "csharp",
            source,
            constrained["role_orders"][0],
        )
        budget = constrained["synthetic_budget"]
        budget["request_cap"] = (
            len(serialized) + budget["output_reserve"] + budget["safety_margin"] - 1
        )
        with patch.object(h0, "_definition", return_value=constrained), patch.object(
            h0, "tokenize", return_value={"tokens": 1, "token_stream_sha256": "x" * 64}
        ):
            with self.assertRaises(ValueError):
                h0.audit(self.root, self.path)

    def test_repeated_audits_have_same_envelope_identities(self):
        with patch.object(h0, "tokenize", return_value={"tokens": 1, "token_stream_sha256": "x" * 64}):
            left, right = h0.audit(self.root, self.path), h0.audit(self.root, self.path)
        self.assertEqual(left["envelopes"], right["envelopes"])

    def test_cli_lf_reproducibility_and_collision_refusal(self):
        fake = FakeEncoding()
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            left, right = base / "left", base / "right"
            with patch.object(h0, "_get_encoding", return_value=fake):
                self.assertEqual(h0.main(["--output-dir", str(left)]), 0)
                self.assertEqual(h0.main(["--output-dir", str(right)]), 0)
            left_files = sorted(path.name for path in left.iterdir())
            self.assertEqual(len(left_files), 5)
            for name in left_files:
                left_bytes = (left / name).read_bytes()
                self.assertEqual(left_bytes, (right / name).read_bytes())
                self.assertNotIn(b"\r\n", left_bytes)

            collision = base / "collision"
            collision.mkdir()
            existing = collision / "report.json"
            existing.write_bytes(b"original\r\n")
            with patch.object(h0, "_get_encoding", return_value=fake):
                with self.assertRaises(FileExistsError):
                    h0.main(["--output-dir", str(collision)])
            self.assertEqual(existing.read_bytes(), b"original\r\n")
            self.assertEqual(list(collision.iterdir()), [existing])


if __name__ == "__main__": unittest.main()
