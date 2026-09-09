import unittest
from unittest.mock import patch

from alf.h_sandbox import HSandboxEvaluator


class HSandboxTests(unittest.TestCase):
    def test_activated_spec_forbids_fixture_image_before_inner_evaluator(self):
        with patch("alf.h_sandbox.DockerEvaluator") as inner, self.assertRaises(ValueError):
            HSandboxEvaluator({}, "csharp", {"execution_authorized": True}, fixture_image_id="sha256:" + "0" * 64)
        inner.assert_not_called()

    def test_adapter_materializes_baseline_and_delegates(self):
        source = {"OrderFlow.csproj": "<Project />\n", "Program.cs": "class P {}\n"}
        with patch("alf.h_sandbox.DockerEvaluator") as cls:
            adapter = HSandboxEvaluator(source, "csharp", {"execution_authorized": False})
            args = cls.call_args.args
            self.assertEqual(args[1]["id"], "h-private-baseline")
            self.assertEqual((args[0] / "baseline/Program.cs").read_text(), source["Program.cs"])
            adapter.prepare(); adapter.evaluate(source, [], 1.0); adapter.close()
        cls.return_value.prepare.assert_called_once()
        cls.return_value.evaluate.assert_called_once()


if __name__ == "__main__": unittest.main()
