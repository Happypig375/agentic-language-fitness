import unittest
import json
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from alf.cli import cmd_doctor
from alf.config import REQUIRED_DOTNET_SDK, REQUIRED_DOTNET_TARGET_FRAMEWORK, load_manifest


class ManifestTests(unittest.TestCase):
    def test_pilot_manifest_loads(self):
        root = Path(__file__).resolve().parents[1]
        manifest = load_manifest(root)
        self.assertEqual(manifest["id"], "pilot-order-flow")
        self.assertEqual(set(manifest["languages"]), {"fsharp", "csharp"})
        self.assertEqual([task["id"] for task in manifest["tasks"]], ["001-priority", "002-overdue"])

    def test_pilot_projects_target_required_framework(self):
        root = Path(__file__).resolve().parents[1]
        for language, project_file in (("fsharp", "OrderFlow.fsproj"), ("csharp", "OrderFlow.csproj")):
            project = root / "benchmarks" / "pilot" / "repos" / language / "v0" / project_file
            self.assertIn(f"<TargetFramework>{REQUIRED_DOTNET_TARGET_FRAMEWORK}</TargetFramework>", project.read_text())

    def test_toolchain_pins_are_consistent(self):
        root = Path(__file__).resolve().parents[1]
        global_json = json.loads((root / "global.json").read_text())
        self.assertEqual(global_json["sdk"]["version"], REQUIRED_DOTNET_SDK)
        ci = (root / ".github" / "workflows" / "ci.yml").read_text()
        self.assertIn(f"dotnet-version: '{REQUIRED_DOTNET_SDK}'", ci)
        dockerfile = (root / "Dockerfile").read_text()
        self.assertIn(f"mcr.microsoft.com/dotnet/sdk:{REQUIRED_DOTNET_SDK}", dockerfile)

    def test_doctor_requires_exact_sdk_without_local_sdk(self):
        root = Path(__file__).resolve().parents[1]
        args = type("Args", (), {"root": str(root), "require_agent": None, "strict": True})()
        for detected, expected_ok in ((REQUIRED_DOTNET_SDK, True), ("10.0.301", False)):
            with patch("alf.cli.environment_snapshot", return_value={"dotnet": detected}), patch(
                "alf.cli.shutil.which", return_value="tool"
            ), redirect_stdout(StringIO()):
                self.assertEqual(cmd_doctor(args), 0 if expected_ok else 1)


if __name__ == "__main__":
    unittest.main()
