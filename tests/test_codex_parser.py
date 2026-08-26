import json
import unittest

from alf.agents.codex import parse_codex_jsonl


class CodexParserTests(unittest.TestCase):
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
