import unittest

from alf.cli import build_parser


class CliProtocolTests(unittest.TestCase):
    def test_parser_accepts_williams_order_and_position_four(self):
        args = build_parser().parse_args(["run", "--language", "fsharp", "--order", "williams-01", "--position", "4"])
        self.assertEqual((args.order, args.position), ("williams-01", 4))


if __name__ == "__main__":
    unittest.main()
