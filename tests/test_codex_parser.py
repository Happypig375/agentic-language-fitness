import json
import unittest

from alf.agents.codex import parse_codex_jsonl


class CodexParserTests(unittest.TestCase):
    def test_read_telemetry_handles_supported_paths(self):
        usage = {k: 0 for k in ("input_tokens", "cached_input_tokens", "cache_write_input_tokens", "output_tokens", "reasoning_output_tokens")}
        commands = ["cat src/main.py", 'head "docs/read me.md"', r'cat C:\repo\one.py C:\repo\two.py',
                    "cat repeat.py", "cat repeat.py", "rg PATTERN src/a.py src/b.py", "sed -n '1,8p' src/main.py"]
        text = "\n".join(json.dumps({"type": "item.completed", "item": {"type": "command_execution", "command": c}}) for c in commands)
        _, _, counts = parse_codex_jsonl(text + "\n" + json.dumps({"type": "turn.completed", "usage": usage}))
        self.assertEqual(counts["file_reads"], 9)
        self.assertEqual(counts["unique_file_reads"], 7)
        self.assertEqual(counts["file_revisits"], 2)

    def test_read_telemetry_rejects_ambiguous_shell(self):
        usage = {k: 0 for k in ("input_tokens", "cached_input_tokens", "cache_write_input_tokens", "output_tokens", "reasoning_output_tokens")}
        commands = ["cat a.py | cat b.py", "cat --number a.py", "sed -n -e '1p' a.py"]
        text = "\n".join(json.dumps({"type": "item.completed", "item": {"type": "command_execution", "command": c}}) for c in commands)
        _, _, counts = parse_codex_jsonl(text + "\n" + json.dumps({"type": "turn.completed", "usage": usage}))
        self.assertEqual(counts["file_reads"], 0)
    def test_multiple_usage_records_are_summed(self):
        record = {"input_tokens": 1, "cached_input_tokens": 2, "cache_write_input_tokens": 3,
                  "output_tokens": 4, "reasoning_output_tokens": 5}
        events, usage, counts = parse_codex_jsonl("\n".join(json.dumps({"type": "turn.completed", "usage": record}) for _ in range(2)))
        self.assertEqual(usage.input_tokens, 2)
        self.assertEqual(usage.reasoning_output_tokens, 10)
        self.assertEqual(counts["usage_records"], 2)
        self.assertTrue(counts["accounting_valid"])

    def test_missing_and_negative_usage_are_invalid(self):
        lines = [
            {"type": "turn.completed"},
            {"type": "turn.completed", "usage": {"input_tokens": -1}},
        ]
        _, _, counts = parse_codex_jsonl("\n".join(json.dumps(x) for x in lines))
        self.assertFalse(counts["accounting_valid"])
        self.assertEqual(len(counts["usage_errors"]), 2)

    def test_conservative_read_extractor(self):
        usage = {k: 0 for k in ("input_tokens", "cached_input_tokens", "cache_write_input_tokens", "output_tokens", "reasoning_output_tokens")}
        lines = [
            {"type": "item.completed", "item": {"type": "command_execution", "command": "cat src/foo.py"}},
            {"type": "item.completed", "item": {"type": "command_execution", "command": 'head "README file.md"' }},
            {"type": "item.completed", "item": {"type": "command_execution", "command": "rg PATTERN src"}},
            {"type": "turn.completed", "usage": usage},
        ]
        _, _, counts = parse_codex_jsonl("\n".join(json.dumps(x) for x in lines))
        self.assertEqual(counts["file_reads"], 3)
        self.assertEqual(counts["unique_file_reads"], 3)
    def test_usage_and_item_counts(self):
        lines = [
            {"type": "thread.started", "thread_id": "x"},
            {"type": "item.completed", "item": {"type": "command_execution"}},
            {"type": "item.completed", "item": {"type": "file_change"}},
            {
                "type": "turn.completed",
                "usage": {
                    "input_tokens": 100,
                    "cached_input_tokens": 40,
                    "cache_write_input_tokens": 10,
                    "output_tokens": 20,
                    "reasoning_output_tokens": 5
                }
            }
        ]
        events, usage, counts = parse_codex_jsonl("\n".join(json.dumps(line) for line in lines))
        self.assertEqual(len(events), 4)
        self.assertEqual(usage.input_tokens, 100)
        self.assertEqual(usage.cached_input_tokens, 40)
        self.assertEqual(usage.output_tokens, 20)
        self.assertEqual(usage.reasoning_output_tokens, 5)
        self.assertEqual(usage.tool_calls, 2)
        self.assertEqual(counts["commands"], 1)
        self.assertEqual(counts["file_changes"], 1)

    def test_invalid_json_is_preserved_and_counted(self):
        events, _, counts = parse_codex_jsonl("not-json\n")
        self.assertEqual(events[0]["type"], "alf.invalid-jsonl")
        self.assertEqual(counts["failed_events"], 1)


if __name__ == "__main__":
    unittest.main()
