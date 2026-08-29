import json
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from alf.cli import cmd_doctor
from alf.config import REQUIRED_DOTNET_SDK, REQUIRED_DOTNET_TARGET_FRAMEWORK, load_manifest


class ManifestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).resolve().parents[1]
        cls.successor = load_manifest(cls.root, "benchmarks/successor/manifest.json")
        cls.pilot = load_manifest(cls.root)

    def test_successor_has_canonical_eight_task_ids(self):
        self.assertEqual([task["id"] for task in self.successor["tasks"]], [
            "001-priority", "002-overdue", "003-at-risk-window", "004-vip-ready",
            "005-null-order-robustness", "006-transition-validation",
            "007-query-engine-refactor", "008-summary-api"])

    def test_baseline_and_first_two_tasks_are_byte_and_value_identical_to_pilot(self):
        self.assertEqual(self.successor["baseline_cases"], self.pilot["baseline_cases"])
        for index in (0, 1):
            successor, pilot = self.successor["tasks"][index], self.pilot["tasks"][index]
            self.assertEqual(successor["cases"], pilot["cases"])
            self.assertEqual((self.root / successor["prompt"]).read_bytes(), (self.root / pilot["prompt"]).read_bytes())
            for language in ("fsharp", "csharp"):
                self.assertEqual((self.root / successor["gold"][language]).read_bytes(), (self.root / pilot["gold"][language]).read_bytes())

    def test_every_gold_path_is_unique_and_exists(self):
        paths = []
        for task in self.successor["tasks"]:
            for gold in task["gold"].values():
                entries = gold["files"] if isinstance(gold, dict) else [{"source": gold}]
                for entry in entries:
                    path = self.root / entry["source"]
                    self.assertTrue(path.is_file(), entry["source"])
                    paths.append(path.resolve())
        self.assertEqual(len(paths), len(set(paths)))

    def test_task_file_paths_and_cases_are_unique(self):
        seen = set()
        for task in self.successor["tasks"]:
            self.assertNotIn(task["id"], seen)
            seen.add(task["id"])
            names = [case["name"] for case in task["cases"]]
            self.assertEqual(len(names), len(set(names)), task["id"])
            self.assertTrue((self.root / task["prompt"]).is_file())

    def test_task007_and_task008_use_exact_multifile_targets_and_fsharp_compile_order(self):
        for task in self.successor["tasks"][6:]:
            for language in ("fsharp", "csharp"):
                targets = [entry["target"] for entry in task["gold"][language]["files"]]
                self.assertEqual(len(targets), len(set(targets)))
                self.assertEqual(targets, ["OrderFlow.fsproj", "OrderFlowEngine.fs", "Program.fs"] if language == "fsharp" else ["OrderFlowEngine.cs", "Program.cs"])

    def test_workspace_checks_are_cumulative_and_summary_is_not_leaked_early(self):
        old_literals = {'"ready"', '"overdue"', '"atRisk"', '"vipReady"', '"transition"'}
        task7 = self.successor["tasks"][6]
        for language in ("fsharp", "csharp"):
            checks = task7["workspace_checks"][language]
            forbidden = {entry["text"] for entry in checks["text_not_contains"]}
            self.assertTrue(old_literals <= forbidden)
            self.assertNotIn('"summary"', forbidden)
        task8 = self.successor["tasks"][7]
        for language in ("fsharp", "csharp"):
            self.assertEqual(set(task8["workspace_checks"][language]), {"file_exists", "text_contains", "text_not_contains"})
            self.assertEqual(task8["workspace_checks"][language]["file_exists"], [])
            self.assertEqual(task8["workspace_checks"][language]["text_contains"], [])
            self.assertEqual(task8["workspace_checks"][language]["text_not_contains"], [{"path": "Program.fs" if language == "fsharp" else "Program.cs", "text": '"summary"'}])

    def test_early_gold_sources_do_not_leak_future_operations_or_engine_contract(self):
        future = ('"summary"', "OrderFlowEngine", "module OrderFlowEngine", "public static class OrderFlowEngine")
        for task in self.successor["tasks"][2:6]:
            for gold in task["gold"].values():
                entries = gold["files"] if isinstance(gold, dict) else [{"source": gold}]
                for entry in entries:
                    path = self.root / entry["source"]
                    if not path.is_file():
                        continue
                    text = path.read_text(encoding="utf-8")
                    self.assertFalse(any(literal in text for literal in future), str(path))

    def test_prompts_state_stable_error_contracts(self):
        required = {
            "003-at-risk-window": "asOf is required for atRisk",
            "005-null-order-robustness": "asOf is required for overdue",
            "006-transition-validation": "id is required for transition",
        }
        for task in self.successor["tasks"]:
            if task["id"] not in required:
                continue
            prompt = self.root / task["prompt"]
            if prompt.is_file():
                self.assertIn(required[task["id"]], prompt.read_text(encoding="utf-8"))

    def test_cases_cover_boundary_null_error_and_precedence_contracts(self):
        by_id = {task["id"]: task for task in self.successor["tasks"]}
        def case(task_id, name):
            return next(item for item in by_id[task_id]["cases"] if item["name"] == name)
        names = lambda task_id: {item["name"] for item in by_id[task_id]["cases"]}
        self.assertGreaterEqual(len(by_id["003-at-risk-window"]["cases"]), 8)
        self.assertGreaterEqual(len(by_id["004-vip-ready"]["cases"]), 6)
        self.assertGreaterEqual(len(by_id["005-null-order-robustness"]["cases"]), 9)
        self.assertGreaterEqual(len(by_id["006-transition-validation"]["cases"]), 14)
        self.assertIn("atRisk upper exclusive", names("003-at-risk-window"))
        self.assertIn("unknown operation exact error", names("003-at-risk-window"))
        self.assertIn("overdue required asOf precedence", names("005-null-order-robustness"))
        self.assertIn("transition missing id precedence", names("006-transition-validation"))
        self.assertEqual(case("003-at-risk-window", "atRisk one second inside lower boundary")["expected"], {"ids": ["inside"]})
        self.assertEqual(case("003-at-risk-window", "atRisk compares equivalent offsets")["expected"], {"ids": ["same", "inside"]})
        self.assertEqual(case("004-vip-ready", "vip final tie uses ordinal id")["expected"], {"ids": ["A", "a", "b"]})
        null_cases = by_id["005-null-order-robustness"]["cases"]
        for operation in ("ready", "overdue", "atRisk", "vipReady"):
            operation_cases = [case for case in null_cases if case["input"].get("operation") == operation]
            self.assertTrue(any("orders" not in case["input"] for case in operation_cases), operation)
            self.assertTrue(any(case["input"].get("orders") is None for case in operation_cases), operation)
            self.assertTrue(any(case["input"].get("orders") == [None, None] for case in operation_cases), operation)
        transition_cases = by_id["006-transition-validation"]["cases"]
        invalid = [case for case in transition_cases if case["expected"] == {"error": "invalid transition"}]
        self.assertGreaterEqual(len(invalid), 12)
        self.assertTrue(any(case["input"].get("id") == "" for case in transition_cases))
        self.assertTrue(any(case["input"].get("toStatus") is None for case in transition_cases))
        allowed = {
            ("pending", "processing"): {"id": "p", "status": "processing"},
            ("pending", "cancelled"): {"id": "p", "status": "cancelled"},
            ("processing", "completed"): {"id": "p", "status": "completed"},
            ("processing", "cancelled"): {"id": "p", "status": "cancelled"},
        }
        for (source, target), expected in allowed.items():
            matched = [x for x in transition_cases if x["input"].get("id") == "p" and isinstance(x["input"].get("toStatus"), str) and x["input"]["toStatus"].lower() == target and x["input"].get("orders") and isinstance(x["input"]["orders"][0], dict) and x["input"]["orders"][0].get("status", "").lower() == source and x["expected"] == expected]
            self.assertTrue(matched, (source, target))
        recognized = {"pending", "processing", "completed", "cancelled"}
        recognized_invalid = [x for x in invalid if x["input"].get("toStatus") in recognized and x["input"].get("orders") and x["input"]["orders"][0].get("status") in recognized]
        self.assertEqual(len({(x["input"]["orders"][0]["status"], x["input"]["toStatus"]) for x in recognized_invalid}), 12)
        summary_cases = by_id["008-summary-api"]["cases"]
        summary = next(x for x in summary_cases if x["name"] == "summary status and overdue counts")
        self.assertEqual(set(summary["expected"]), {"pending", "processing", "completed", "cancelled", "overdue"})
        self.assertEqual(next(x for x in summary_cases if x["name"] == "summary null orders zero")["expected"]["overdue"], 0)
        exact_index = next(i for i, x in enumerate(summary_cases) if x["name"] == "summary exact object keys")
        self.assertEqual(summary_cases[exact_index + 1]["name"], "post-summary ready remains unchanged")

    def test_pilot_projects_target_required_framework(self):
        for language, project_file in (("fsharp", "OrderFlow.fsproj"), ("csharp", "OrderFlow.csproj")):
            project = self.root / "benchmarks" / "pilot" / "repos" / language / "v0" / project_file
            self.assertIn(f"<TargetFramework>{REQUIRED_DOTNET_TARGET_FRAMEWORK}</TargetFramework>", project.read_text())

    def test_toolchain_pins_are_consistent(self):
        global_json = json.loads((self.root / "global.json").read_text())
        self.assertEqual(global_json["sdk"]["version"], REQUIRED_DOTNET_SDK)
        self.assertEqual(global_json["sdk"]["rollForward"], "disable")
        ci = (self.root / ".github" / "workflows" / "ci.yml").read_text()
        self.assertIn(f"dotnet-version: '{REQUIRED_DOTNET_SDK}'", ci)
        self.assertIn(f"mcr.microsoft.com/dotnet/sdk:{REQUIRED_DOTNET_SDK}", (self.root / "Dockerfile").read_text())

    def test_doctor_requires_exact_sdk_without_local_sdk(self):
        args = type("Args", (), {"root": str(self.root), "require_agent": None, "strict": True})()
        for detected, expected_ok in ((REQUIRED_DOTNET_SDK, True), ("10.0.301", False)):
            with patch("alf.cli.environment_snapshot", return_value={"dotnet": detected}), patch("alf.cli.shutil.which", return_value="tool"), redirect_stdout(StringIO()):
                self.assertEqual(cmd_doctor(args), 0 if expected_ok else 1)


if __name__ == "__main__":
    unittest.main()
