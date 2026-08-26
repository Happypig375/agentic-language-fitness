import unittest
from pathlib import Path

from alf.config import load_manifest


class ManifestTests(unittest.TestCase):
    def test_pilot_manifest_loads(self):
        root = Path(__file__).resolve().parents[1]
        manifest = load_manifest(root)
        self.assertEqual(manifest["id"], "pilot-order-flow")
        self.assertEqual(set(manifest["languages"]), {"fsharp", "csharp"})
        self.assertEqual([task["id"] for task in manifest["tasks"]], ["001-priority", "002-overdue"])


if __name__ == "__main__":
    unittest.main()
