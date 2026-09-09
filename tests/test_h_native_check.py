import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).parents[1] / "scripts" / "h_native_check.py"
SPEC = importlib.util.spec_from_file_location("h_native_check", SCRIPT)
assert SPEC and SPEC.loader
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


class HNativeCheckTests(unittest.TestCase):
    def test_canonical_replays_cover_h1_and_h2_phases(self):
        with patch.object(module.h_check.h0, "tokenize", side_effect=AssertionError("tokenizer called")):
            items = module.canonical_replays(Path(__file__).parents[1],
                Path(__file__).parents[1] / "protocols/workstream-h1-h2/specification.json")
        self.assertEqual({x["access"] for x in items}, {"H1", "H2"})
        self.assertEqual({x["phase"] for x in items}, {"initial", "read", "final"})
        self.assertTrue(all(isinstance(x["replay"], bytes) for x in items))

    def test_run_one_requires_exact_authored_text_and_no_tools_probe(self):
        replay = b'{"canonical":true}\n'

        class Probe:
            PROMPT = "old"
            @staticmethod
            def _summarize_body(_raw): return {}
            @staticmethod
            def probe_passed(report): return report["ok"]
            def run_probe(self, _codex, **kwargs):
                self.kwargs = kwargs
                body = {"input": [
                    {"role": "user", "content": "native environment"},
                    {"role": "user", "content": self.PROMPT + "\n"}]}
                summary = self._summarize_body(json.dumps(body).encode())
                return {"ok": True, "request_bodies": [summary], "request_count": 1,
                        "total_post_attempts": 1, "candidate_model_calls": 0,
                        "real_provider_http_calls": 0}

        probe = Probe()
        result = module.run_one(probe, "native", replay, "baseline", 1)
        self.assertTrue(result["passed"])
        self.assertEqual(probe.PROMPT, "old")
        self.assertEqual(probe.kwargs["configs"], ("features.no_tools=true",
            "features.single_response=true", "features.code_mode_host=false"))
        self.assertTrue(probe.kwargs["expect_no_tools"])
        self.assertEqual(result["canonical_occurrences"], 1)
        self.assertEqual(result["native_added_user_message_count"], 1)
        self.assertEqual(result["native_added_user_messages"][0]["bytes"], len(b"native environment"))

    def test_run_one_rejects_wrong_last_text_and_duplicate_canonical_entry(self):
        class Probe:
            PROMPT = "old"
            @staticmethod
            def _summarize_body(_raw): return {}
            @staticmethod
            def probe_passed(_report): return True
            mode = "wrong"
            def run_probe(self, *_args, **_kwargs):
                canonical = self.PROMPT + "\n"
                content = [canonical, canonical] if self.mode == "duplicate" else [canonical, "wrong"]
                body = {"input": [{"role": "user", "content": text} for text in content]}
                return {"request_bodies": [self._summarize_body(json.dumps(body).encode())]}
        probe = Probe()
        self.assertFalse(module.run_one(probe, "native", b"replay\n", "baseline", 1)["text_match"])
        probe.mode = "duplicate"
        duplicate = module.run_one(probe, "native", b"replay\n", "baseline", 1)
        self.assertFalse(duplicate["text_match"])
        self.assertEqual(duplicate["canonical_occurrences"], 2)

    def test_run_one_requires_canonical_terminal_lf(self):
        with self.assertRaisesRegex(ValueError, "must end in one LF"):
            module.run_one(object(), "native", b"replay", "baseline", 1)

    def test_sha_mismatch_stops_before_loading_probe_or_replays(self):
        with tempfile.TemporaryDirectory() as directory:
            native = Path(directory) / "codex"
            native.write_bytes(b"wrong")
            with patch.object(module, "_load_probe") as load, patch.object(module, "canonical_replays") as replays:
                report = module.audit(native, Path("unused"), 1)
        self.assertEqual(report["failures"], ["native-sha256-mismatch"])
        self.assertEqual(report["native_sha256"], hashlib.sha256(b"wrong").hexdigest())
        load.assert_not_called(); replays.assert_not_called()

    def test_cli_retains_existing_evidence_and_writes_lf(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "report.json"
            argv = ["--codex", "not-invoked", "--output", str(output)]
            with patch.object(module, "audit", return_value={"status": "passed"}) as audit:
                self.assertEqual(module.main(argv), 0)
                self.assertNotIn(b"\r", output.read_bytes())
                before = output.read_bytes()
                with self.assertRaises(SystemExit):
                    module.main(argv)
                self.assertEqual(output.read_bytes(), before)
                audit.assert_called_once()


if __name__ == "__main__":
    unittest.main()
