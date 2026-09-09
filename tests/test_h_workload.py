import json
import tempfile
import unittest
from pathlib import Path
from alf import h0
from alf.h_workload import cases_for, oracle_additions, ordered_filenames, public_payload, source_for

ROOT = Path(__file__).resolve().parents[1]

class HWorkloadTests(unittest.TestCase):
    def test_public_examples_match_independent_oracle(self):
        data=json.loads((ROOT/"benchmarks/workstream-h/public-examples.json").read_text(encoding="utf-8"))
        for ex in data["examples"]:
            self.assertEqual(oracle_additions(ex["request"]), ex["response"], ex["name"])

    def test_utf16_and_case_insensitive_dispatch(self):
        request={"OpErAtIoN":"DEPENDENCYORDER","IDS":["\ue000","𝄞","A"],"EDGES":[]}
        self.assertEqual(oracle_additions(request), {"ids":["A","𝄞","\ue000"]})

    def test_reconcile_validation_precedence_and_ticks(self):
        self.assertEqual(oracle_additions({"operation":"reconcile","left":[{"id":"x","priority":1.0,"createdAt":"2024-01-01T00:00:00Z"}]}), {"error":"invalid left priority"})
        self.assertEqual(oracle_additions({"operation":"reconcile","left":[{"id":"x","priority":1,"createdAt":"2024-01-01T00:00:00.0000001Z"}],"right":[{"id":"x","priority":1,"createdAt":"2024-01-01T00:00:00Z"}]}), {"items":[{"id":"x","origin":"left"}]})
        self.assertEqual(oracle_additions({"operation":"reconcile","left":[{"id":"x","priority":1,"createdAt":"2024-01-01T00:00:00Z"},{"id":"x","priority":1}]}), {"error":"invalid left createdAt"})
        self.assertEqual(oracle_additions({"operation":"reconcile","left":[{"id":"x","priority":1,"createdAt":"2024-01-01T00:00:00Z"},{"id":"x","priority":1,"createdAt":"2024-01-01T00:00:00Z"}],"right":[None]}), {"error":"invalid right record"})
        self.assertEqual(oracle_additions({"operation":"reconcile","left":[{"id":"x","priority":"1","createdAt":"2024-01-01T00:00:00Z"}]}), {"error":"invalid left priority"})
        self.assertEqual(oracle_additions({"operation":"reconcile","left":[{"id":"x","priority":1,"createdAt":"2024-01-01T00:00:00+14:01"}]}), {"error":"invalid left createdAt"})

    def test_dependency_error_precedence(self):
        self.assertEqual(oracle_additions({"operation":"dependencyOrder","ids":["a","a"],"edges":[{"before":"x","after":"x"}]}), {"error":"duplicate id"})
        self.assertEqual(oracle_additions({"operation":"dependencyOrder","ids":["a"],"edges":[{"before":"x","after":"x"}]}), {"error":"unknown dependency"})
        self.assertEqual(oracle_additions({"operation":"dependencyOrder","ids":["a"],"edges":[{"before":"a","after":"a"}]}), {"error":"self dependency"})
        self.assertEqual(oracle_additions({"operation":"dependencyOrder","ids":["a","b"],"edges":[{"before":"a","after":"b"},{"before":"a"}]}), {"error":"invalid edge"})
        with self.assertRaises(ValueError): oracle_additions({"operation":"legacy"})

    def test_loader_and_order(self):
        definition=h0._definition(ROOT,"protocols/workstream-h0/definition.json")
        for language in ("csharp", "fsharp"):
            core=source_for(ROOT,"core",language)
            self.assertEqual(core, h0.source_for(ROOT,definition,language))
            self.assertEqual(ordered_filenames(core,language)[0], definition["roles"][language]["project"])
            self.assertEqual(set(source_for(ROOT,"core",language,gold=True)), set(core))
            for bundle in (source_for(ROOT,"expanded",language), source_for(ROOT,"expanded",language,gold=True)):
                self.assertTrue(set(definition["roles"][language].values()).issubset(bundle))
        core_payload=public_payload(ROOT,"core")
        self.assertEqual(set(core_payload), {"baseline_contract","earlier_contracts","current_task"})
        expanded_payload=public_payload(ROOT,"expanded")
        self.assertEqual(set(expanded_payload), {"baseline_contract","earlier_contracts","current_task","expanded_contract","expanded_public_examples"})

    def test_cases_expected_are_neutral_and_summary_toggle(self):
        no_summary=cases_for(ROOT,"expanded",False)
        with_summary=cases_for(ROOT,"expanded",True)
        self.assertGreater(len(with_summary),len(no_summary))
        self.assertTrue(any(c["name"]=="reconcile priority and origin" for c in with_summary))
        self.assertTrue(all(set(c)=={"name","input","expected"} for c in with_summary))

    def test_all_literal_addition_cases_match_independent_oracle(self):
        cases = cases_for(ROOT, "expanded", True)
        checked = []
        for case in cases:
            operation = case["input"].get("operation") if isinstance(case["input"], dict) else None
            if isinstance(operation, str) and operation.lower() in {"reconcile", "dependencyorder"}:
                self.assertEqual(oracle_additions(case["input"]), case["expected"], case["name"])
                checked.append(case["name"])
        public_count = len(json.loads((ROOT/"benchmarks/workstream-h/public-examples.json").read_text(encoding="utf-8"))["examples"])
        self.assertGreater(len(checked), public_count)

    def test_expanded_loader_canonicalizes_crlf_but_rejects_bare_cr_and_nul(self):
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp)/"benchmarks/workstream-h/repos/csharp/expanded"
            base.mkdir(parents=True)
            contents={"OrderFlow.csproj":"project\n","OrderFlowEngine.cs":"engine\n","Program.cs":"program\n"}
            for name,text in contents.items(): (base/name).write_bytes(text.replace("\n","\r\n").encode())
            self.assertEqual(source_for(Path(tmp),"expanded","csharp"),contents)
            (base/"Program.cs").write_bytes(b"program\rX")
            with self.assertRaises(ValueError): source_for(Path(tmp),"expanded","csharp")
            (base/"Program.cs").write_bytes(b"program\x00")
            with self.assertRaises(ValueError): source_for(Path(tmp),"expanded","csharp")

if __name__ == "__main__":
    unittest.main()
