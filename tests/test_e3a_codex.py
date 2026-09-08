import json
import unittest
from pathlib import Path

from alf.e3a_codex import (MAX_CAPTURE_BYTES, CodexOAuthAdapter, DispatchGuard, build_replay,
                            normalize_cli_usage, parse_cli_jsonl)


class _Transport:
    is_live = False
    def __init__(self, reply):
        self.reply = reply
        self.calls = []

    def launch(self, stdin, timeout):
        self.calls.append((stdin, timeout))
        return {"stdout": self.reply, "stderr": b"", "returncode": 0,
                "timed_out": False, "output_overflow": False, "cleanup_confirmed": True}


class E3aCodexTests(unittest.TestCase):
    def test_captured_startup_diagnostics_are_admitted_separately(self):
        fixture = Path(__file__).parent / "fixtures" / "e3a-codex-startup-envelope.jsonl"
        raw = fixture.read_bytes()
        report = Path(__file__).parents[1] / "reports/workstream-e3a-oauth-shakedown-2026-09-08/attempt-01-report.json"
        captured = json.loads(report.read_text(encoding="utf-8"))["attempts"][0]["response"]["raw_stdout"]
        self.assertEqual(raw.decode().replace("\r\n", "\n"), captured.replace("\r\n", "\n"))
        parsed = parse_cli_jsonl(raw)
        self.assertEqual(parsed["status"], "completed")
        self.assertEqual([event["item"]["id"] for event in parsed["startup_diagnostics"]], ["item_0", "item_1"])
        self.assertEqual(parsed["text"], json.loads(raw.splitlines()[4])["item"]["text"])
        self.assertEqual(parsed["usage"]["input_tokens"], 6427)
        self.assertEqual(parsed["usage"]["output_tokens"], 79)
        self.assertEqual(parsed["usage"]["reasoning_output_tokens"], 37)

        lines = raw.decode().splitlines()
        mutated = json.loads(lines[1]); mutated["item"]["message"] += " changed"
        lines[1] = json.dumps(mutated, separators=(",", ":"))
        self.assertEqual(parse_cli_jsonl("\n".join(lines))["failure"], "unexpected-cli-sequence")
        lines = raw.decode().splitlines()
        lines[1], lines[2] = lines[2], lines[1]
        self.assertEqual(parse_cli_jsonl("\n".join(lines))["failure"], "unexpected-cli-sequence")
        lines = raw.decode().splitlines()
        lines.insert(3, lines[1])
        self.assertEqual(parse_cli_jsonl("\n".join(lines))["failure"], "unexpected-cli-sequence")

        base = raw.decode().splitlines()
        variants = []
        event = json.loads(base[1]); event["extra"] = True; variants.append((1, event))
        event = json.loads(base[1]); event["item"]["extra"] = True; variants.append((1, event))
        event = json.loads(base[1]); event["item"]["id"] = "item_9"; variants.append((1, event))
        for index, event in variants:
            changed = list(base); changed[index] = json.dumps(event, separators=(",", ":"))
            self.assertNotEqual(parse_cli_jsonl("\n".join(changed))["status"], "completed")

        for event in (
            {"type": "item.completed", "item": {"type": "command_execution"}},
            {"type": "item.completed", "item": {"type": "agent_message", "text": "x"}},
            {"type": "error", "message": "unexpected"},
        ):
            changed = list(base); changed.insert(1, json.dumps(event, separators=(",", ":")))
            self.assertNotEqual(parse_cli_jsonl("\n".join(changed))["status"], "completed")
        for index in (4, 6):
            changed = list(base); changed.insert(index, base[1])
            self.assertNotEqual(parse_cli_jsonl("\n".join(changed))["status"], "completed")
        changed = list(base); changed.insert(4, base[1])
        self.assertNotEqual(parse_cli_jsonl("\n".join(changed))["status"], "completed")
        changed = list(base); changed.insert(5, base[3])
        self.assertNotEqual(parse_cli_jsonl("\n".join(changed))["status"], "completed")

    def test_unknown_pre_turn_item_remains_rejected_and_no_warning_replay(self):
        raw = b'{"type":"thread.started"}\n{"type":"item.completed","item":{"id":"x","type":"error","message":"other"}}\n{"type":"turn.started"}\n{"type":"turn.completed","usage":{"input_tokens":1,"output_tokens":0}}\n'
        self.assertEqual(parse_cli_jsonl(raw)["failure"], "unexpected-cli-sequence")
        fixture = Path(__file__).parent / "fixtures" / "e3a-codex-startup-envelope.jsonl"
        spec = {"authority": {"max_replay_bytes": 131072}, "budgets": {"pilot_dispatch_ceiling": 2,
                "request_input_tokens": 32768, "request_output_tokens_including_reasoning": 8192}}
        transport = _Transport(fixture.read_bytes())
        adapter = CodexOAuthAdapter(spec, transport)
        first = adapter.generate({"instructions": "fixed"}, None, {}, None, 9999999999)
        second = adapter.generate({"instructions": "fixed"}, first["id"], {}, {}, 9999999999)
        transcript = json.loads(transport.calls[1][0])["transcript"]
        self.assertEqual(first["status"], "completed")
        self.assertEqual(second["status"], "completed")
        self.assertEqual([entry["role"] for entry in transcript], ["user", "assistant", "user"])
        self.assertEqual(transcript[1]["data"], first["text"])
        self.assertNotIn("startup_diagnostics", json.dumps(transcript))
        self.assertNotIn("Under-development", json.dumps(transcript))

    def test_replay_is_canonical_and_labels_final_entry_once(self):
        raw = build_replay("fixed", [{"role": "assistant", "data": "old"}], {"z": 1})
        self.assertEqual(raw[-1:], b"\n")
        doc = json.loads(raw)
        self.assertEqual(doc["instructions"], "fixed")
        self.assertEqual([item["role"] for item in doc["transcript"]], ["assistant", "user"])
        self.assertEqual(raw, build_replay("fixed", [{"role": "assistant", "data": "old"}], {"z": 1}))

    def test_guard_debits_failed_launches_without_retry(self):
        guard = DispatchGuard(1)
        self.assertEqual(guard.debit(), 1)
        with self.assertRaises(ValueError):
            guard.debit()

    def test_parser_rejects_tools_and_normalizes_zero_subsets(self):
        raw = b'{"type":"thread.started"}\n{"type":"turn.started"}\n{"type":"item.completed","item":{"type":"reasoning"}}\n{"type":"item.completed","item":{"type":"agent_message","text":"{}"}}\n{"type":"turn.completed","usage":{"input_tokens":4,"output_tokens":2,"cached_input_tokens":0}}\n'
        parsed = parse_cli_jsonl(raw)
        self.assertEqual(parsed["status"], "completed")
        self.assertIsNone(parsed["usage"]["cached_input_tokens"])
        tool = b'{"type":"thread.started"}\n{"type":"turn.started"}\n{"type":"item.completed","item":{"type":"command_execution"}}\n{"type":"turn.completed","usage":{"input_tokens":4,"output_tokens":2}}\n'
        self.assertEqual(parse_cli_jsonl(tool)["failure"], "unexpected-cli-item")

    def test_adapter_uses_visible_replay_and_stops_oversize_submission(self):
        reply = b'{"type":"thread.started"}\n{"type":"turn.started"}\n{"type":"item.completed","item":{"type":"agent_message","text":"{}"}}\n' \
                b'{"type":"turn.completed","usage":{"input_tokens":3,"output_tokens":4}}\n'
        spec = {"authority": {"max_replay_bytes": 131072}, "budgets": {"pilot_dispatch_ceiling": 2,
                "request_input_tokens": 32768, "request_output_tokens_including_reasoning": 8192}}
        transport = _Transport(reply)
        adapter = CodexOAuthAdapter(spec, transport)
        first = adapter.generate({"instructions": "fixed", "task": "x"}, "provider-id", {"a": 1}, None, 9999999999)
        self.assertEqual(first["status"], "completed")
        self.assertNotIn("previous_response_id", json.loads(transport.calls[0][0])["transcript"][-1])
        self.assertEqual(adapter.guard.dispatched, 1)
        self.assertEqual(first["stdin_bytes"], len(transport.calls[0][0]))
        self.assertEqual(len(first["stdin_sha256"]), 64)

    def test_usage_missing_remains_unknown(self):
        usage = normalize_cli_usage({"input_tokens": 4, "output_tokens": 2})
        self.assertTrue(usage["totals_available"])
        self.assertIsNone(usage["reasoning_output_tokens"])
        invalid = normalize_cli_usage({"input_tokens": 4, "output_tokens": 2,
                                       "cached_input_tokens": False})
        self.assertIn("cached_input_tokens", invalid["invalid_fields"])

    def test_jsonl_order_and_multiple_messages_fail_closed(self):
        bad_order = b'{"type":"thread.started"}\n{"type":"item.completed","item":{"type":"agent_message","text":"a"}}\n{"type":"turn.started"}\n{"type":"turn.completed","usage":{"input_tokens":1,"output_tokens":1}}\n'
        self.assertEqual(parse_cli_jsonl(bad_order)["failure"], "unexpected-cli-sequence")
        multiple = b'{"type":"thread.started"}\n{"type":"turn.started"}\n{"type":"item.completed","item":{"type":"agent_message","text":"a"}}\n{"type":"item.completed","item":{"type":"agent_message","text":"b"}}\n{"type":"turn.completed","usage":{"input_tokens":1,"output_tokens":1}}\n'
        self.assertEqual(parse_cli_jsonl(multiple)["failure"], "multiple-final-replies")

    def test_usage_alarm_keeps_completed_text_and_overflow_cannot_hide_alarm(self):
        text = "x" * 49153
        raw = "\n".join([json.dumps({"type":"thread.started"}), json.dumps({"type":"turn.started"}),
            json.dumps({"type":"item.completed", "item":{"type":"agent_message", "text":text}}),
            json.dumps({"type":"turn.completed", "usage":{"input_tokens":3}}), ""]).encode()
        spec = {"authority":{"max_replay_bytes":131072}, "budgets":{"pilot_dispatch_ceiling":2,
            "request_input_tokens":32768, "request_output_tokens_including_reasoning":8192}}
        result = CodexOAuthAdapter(spec, _Transport(raw)).generate({"instructions":"fixed"}, None, {}, None, 9999999999)
        self.assertEqual(result["failure"], "accounting-unavailable-or-invalid")
        self.assertTrue(result["batch_stop"])
        self.assertEqual(result["text"], text)
        self.assertTrue(result["submission_byte_overflow"])

    def test_combined_capture_limit_is_one_mib(self):
        transport = _Transport(b"")
        transport.launch = lambda stdin, timeout: {"stdout": b"x"*(MAX_CAPTURE_BYTES//2+1),
            "stderr": b"y"*(MAX_CAPTURE_BYTES//2), "returncode":0, "timed_out":False,
            "output_overflow":False, "cleanup_confirmed":True}
        spec = {"authority":{"max_replay_bytes":131072}, "budgets":{"pilot_dispatch_ceiling":2,
            "request_input_tokens":32768, "request_output_tokens_including_reasoning":8192}}
        result = CodexOAuthAdapter(spec, transport).generate({"instructions":"fixed"}, None, {}, None, 9999999999)
        self.assertEqual(result["failure"], "raw-capture-overflow")

    def test_empty_completed_reply_is_a_completed_format_candidate(self):
        raw = b'{"type":"thread.started"}\n{"type":"turn.started"}\n{"type":"turn.completed","usage":{"input_tokens":4,"output_tokens":0}}\n'
        self.assertEqual(parse_cli_jsonl(raw)["text"], "")

    def test_transport_metadata_failures_stop_after_debit(self):
        spec = {"authority": {"max_replay_bytes": 131072}, "budgets": {"pilot_dispatch_ceiling": 2,
                "request_input_tokens": 32768, "request_output_tokens_including_reasoning": 8192}}
        transport = _Transport(b"")
        transport.launch = lambda stdin, timeout: {"stdout": b"", "stderr": b"x", "returncode": 1,
            "timed_out": False, "output_overflow": False, "cleanup_confirmed": True}
        result = CodexOAuthAdapter(spec, transport).generate(
            {"instructions": "fixed"}, None, {}, None, 9999999999)
        self.assertTrue(result["dispatch_attempted"])
        self.assertTrue(result["batch_stop"])
        self.assertEqual(result["failure"], "transport-nonzero-exit")


if __name__ == "__main__":
    unittest.main()
