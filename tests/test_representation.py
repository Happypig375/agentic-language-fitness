from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import tempfile
import unittest
import uuid
from pathlib import Path
from unittest import mock

from alf.benchmark_artifacts import artifact_plan
from alf.config import load_manifest
from alf.representation import (
    ROLE_SPECS,
    SOURCE_COMMIT,
    RepresentationError,
    _digest,
    _coverage_report,
    _coverage_complete,
    _lex,
    _load_snapshots,
    _manifest_contract,
    _public_sequence,
    build_representation,
    check_representation,
    scan_identifiers,
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class RepresentationScannerTests(unittest.TestCase):
    def test_positions_are_utf8_byte_offsets_and_ordinals(self):
        source = 'let value = "é"\nlet value2 = value\n'.encode("utf-8")
        rows = scan_identifiers(source, "fsharp")
        values = [row for row in rows if row.token == "value"]
        self.assertEqual(len(values), 2)
        self.assertEqual(values[0].offset, len("let ".encode("utf-8")))
        self.assertEqual(values[0].length, len("value".encode("utf-8")))
        self.assertEqual([row.ordinal for row in rows], list(range(len(rows))))
        self.assertEqual([row.offset for row in rows], sorted(row.offset for row in rows))

    def test_interpolation_expression_is_scanned_but_literal_and_format_are_not(self):
        source = b'var s = $"literal {request.Id,10:yyyy} {{escaped}}";'
        names = [row.token for row in scan_identifiers(source, "csharp")]
        self.assertIn("request", names)
        self.assertIn("Id", names)
        self.assertNotIn("literal", names)
        self.assertNotIn("yyyy", names)
        self.assertNotIn("escaped", names)

    def test_interpolation_handles_nesting_and_escaped_braces(self):
        source = b'var s = $"{{literal}} {(request.Items[Get(index)]).Id}";'
        names = [row.token for row in scan_identifiers(source, "csharp")]
        for expected in ("request", "Items", "Get", "index", "Id"):
            self.assertIn(expected, names)
        self.assertNotIn("literal", names)
        self.assertEqual(len(names), len(set((row.ordinal, row.offset) for row in scan_identifiers(source, "csharp"))))

    def test_verbatim_interpolation_handles_doubled_quotes_in_both_prefix_orders(self):
        for source in (
            b'var s = $@"literal ""quoted"" {request.Id}";',
            b'var s = @$"literal ""quoted"" {request.Id}";',
        ):
            names = [row.token for row in scan_identifiers(source, "csharp")]
            self.assertIn("request", names)
            self.assertIn("Id", names)
            self.assertNotIn("literal", names)
            self.assertNotIn("quoted", names)

    def test_comments_strings_chars_and_leading_whitespace_directives_are_excluded(self):
        source = (
            b"  #if request\n"
            b"// request\n"
            b"/* request */\n"
            b"var request = \"request\"; var c = 'r';\n"
            b"  #endif\n"
        )
        names = [row.token for row in scan_identifiers(source, "csharp")]
        self.assertEqual(names.count("request"), 1)

    def test_nested_fsharp_block_comments_are_excluded(self):
        source = b"(* outer request (* nested request *) *) let request = 1"
        names = [row.token for row in scan_identifiers(source, "fsharp")]
        self.assertEqual(names.count("request"), 1)

    def test_protected_chunks_include_literals_not_interpolation_expressions(self):
        source = b'var s = $"left {request.Id:yyyy} right"; // tail'
        _, chunks = _lex(source, "csharp")
        joined = b"|".join(chunks)
        self.assertIn(b"left", joined)
        self.assertIn(b"yyyy", joined)
        self.assertIn(b"tail", joined)
        self.assertNotIn(b"request", joined)

    def test_malformed_and_unsupported_constructs_fail_closed(self):
        invalid = (
            b'var x = "unterminated',
            b'var x = $"unterminated {value";',
            b'var x = """raw""";',
            b"let ``escaped`` = 1",
            "let λ = 1".encode("utf-8"),
        )
        for source in invalid:
            with self.subTest(source=source):
                with self.assertRaises(RepresentationError):
                    scan_identifiers(source, "fsharp" if b"let" in source else "csharp")

    def test_non_ascii_and_backticks_inside_literals_are_allowed(self):
        source = 'let request = "λ and ``escaped``"'.encode("utf-8")
        names = [row.token for row in scan_identifiers(source, "fsharp")]
        self.assertEqual(names.count("request"), 1)


class RepresentationMappingTests(unittest.TestCase):
    def test_digest_is_stable_and_collision_extends(self):
        used: set[str] = set()
        first = _digest("private-helper-function", "role-a", used)
        used.add(first)
        second = _digest("private-helper-function", "role-a", used)
        self.assertEqual(first[:4], "fun_")
        self.assertEqual(len(second), len(first) + 2)
        self.assertNotEqual(first, second)

    def test_role_inventory_is_explicit_and_paired(self):
        self.assertEqual(len(ROLE_SPECS), 15)
        self.assertEqual(len({role.role_id for role in ROLE_SPECS}), 15)
        exception = next(role for role in ROLE_SPECS if role.role_id == "local.exception")
        self.assertEqual((exception.csharp, exception.fsharp), ("ex", "ex"))

    def test_coverage_report_exposes_deficits_surpluses_and_unexpected_tokens(self):
        inventory = {
            "snapshots": {"csharp:a.cs": {}, "csharp:b.cs": {}},
            "roles": [{
                "role_id": "role-a",
                "occurrences": {"csharp:a.cs": [{"offset": 1}], "csharp:b.cs": []},
            }],
        }
        rows, eligible, transformed = _coverage_report(
            inventory,
            {"role-a": {"csharp:a.cs": 0, "csharp:b.cs": 1}},
        )
        self.assertEqual((eligible, transformed), (1, 1))
        self.assertEqual(rows["role-a"]["csharp:a.cs"]["coverage"], 0.0)
        self.assertEqual(rows["role-a"]["csharp:a.cs"]["status"], "deficit")
        self.assertIsNone(rows["role-a"]["csharp:b.cs"]["coverage"])
        self.assertEqual(rows["role-a"]["csharp:b.cs"]["status"], "unexpected")
        self.assertFalse(_coverage_complete(rows), "offsetting aggregate counts must not hide per-snapshot mismatches")
        surplus_rows, _, _ = _coverage_report(
            inventory,
            {"role-a": {"csharp:a.cs": 2, "csharp:b.cs": 0}},
        )
        self.assertEqual(surplus_rows["role-a"]["csharp:a.cs"]["coverage"], 2.0)
        self.assertEqual(surplus_rows["role-a"]["csharp:a.cs"]["status"], "surplus")
        covered_rows, _, _ = _coverage_report(
            inventory,
            {"role-a": {"csharp:a.cs": 1, "csharp:b.cs": 0}},
        )
        self.assertTrue(_coverage_complete(covered_rows))


class RepresentationArtifactTests(unittest.TestCase):
    root = Path(__file__).parents[1]
    artifact_root = root / "benchmarks" / "successor" / "representation-v1"

    @classmethod
    def setUpClass(cls):
        cls.mapping = json.loads((cls.artifact_root / "mapping.json").read_text(encoding="utf-8"))
        cls.inventory = json.loads((cls.artifact_root / "role-inventory.json").read_text(encoding="utf-8"))
        cls.reports = json.loads((cls.artifact_root / "reports.json").read_text(encoding="utf-8"))
        original_bytes = subprocess.run(
            ["git", "show", f"{SOURCE_COMMIT}:benchmarks/successor/manifest.json"],
            cwd=cls.root,
            stdout=subprocess.PIPE,
            check=True,
        ).stdout
        cls.original = json.loads(original_bytes.decode("utf-8"))
        cls.snapshots = _load_snapshots(cls.root, cls.original)

    def test_root_manifests_load_and_all_artifact_plans_are_safe(self):
        count = 0
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            for name in ("descriptive.manifest.json", "deterministic.manifest.json"):
                manifest = load_manifest(self.root, self.artifact_root / name)
                self.assertEqual(len(manifest["tasks"]), 8)
                self.assertIsInstance(manifest["tasks"][6]["gold"]["fsharp"], dict)
                self.assertEqual(len(manifest["tasks"][6]["gold"]["fsharp"]["files"]), 3)
                self.assertEqual(len(manifest["tasks"][7]["gold"]["csharp"]["files"]), 2)
                for language in manifest["languages"]:
                    for task in manifest["tasks"]:
                        self.assertTrue(artifact_plan(self.root, manifest, language, task, workspace))
                        count += 1
        self.assertEqual(count, 32)
        self.assertEqual(self.reports["manifest_artifact_plans_validated"], 32)

    def test_inventory_contains_all_roles_and_snapshot_pins(self):
        roles = {role["role_id"]: role for role in self.inventory["roles"]}
        self.assertEqual(set(roles), {role.role_id for role in ROLE_SPECS})
        self.assertEqual(len(self.inventory["snapshots"]), len(self.snapshots))
        exception = roles["local.exception"]
        self.assertEqual(exception["source"], {"csharp": "ex", "fsharp": "ex"})
        for counts in self.inventory["declarations_by_role_and_language"].values():
            self.assertGreater(counts["csharp"], 0)
            self.assertGreater(counts["fsharp"], 0)
        for snapshot in self.snapshots:
            recorded = self.inventory["snapshots"][snapshot.key]
            self.assertEqual(recorded["source_sha256"], sha256(snapshot.data))

    def test_private_helpers_are_scoped_and_public_overdue_is_not_transformed(self):
        overdue = next(role for role in self.inventory["roles"] if role["role_id"] == "helper.overdue")
        nonempty = {key: rows for key, rows in overdue["occurrences"].items() if rows}
        self.assertEqual(set(nonempty), {
            "csharp:gold/007-query-engine-refactor/OrderFlowEngine.cs",
            "csharp:gold/008-summary-api/OrderFlowEngine.cs",
            "fsharp:gold/007-query-engine-refactor/OrderFlowEngine.fs",
            "fsharp:gold/008-summary-api/OrderFlowEngine.fs",
        })
        self.assertTrue(all(len(rows) == 2 for rows in nonempty.values()))
        csharp = (self.artifact_root / "transformed/deterministic/csharp/gold/008-summary-api/OrderFlowEngine.cs").read_text(encoding="utf-8")
        fsharp = (self.artifact_root / "transformed/deterministic/fsharp/gold/008-summary-api/OrderFlowEngine.fs").read_text(encoding="utf-8")
        self.assertIn("int Overdue", csharp)
        self.assertNotIn(" Overdue(", csharp)
        self.assertIn("overdue: int", fsharp)
        self.assertIn("overdue = overdueCount", fsharp)
        self.assertNotIn("let private overdue ", fsharp)

    def test_descriptive_arm_is_canonical_git_blob_identity_for_every_file(self):
        for snapshot in self.snapshots:
            with self.subTest(snapshot=snapshot.key):
                materialized = self.artifact_root / "transformed" / "descriptive" / snapshot.language / snapshot.relative_path
                self.assertEqual(materialized.read_bytes(), snapshot.data)

    def test_deterministic_arm_reconstructs_independently_from_recorded_spans(self):
        role_by_id = {role["role_id"]: role for role in self.inventory["roles"]}
        for snapshot in self.snapshots:
            edits = []
            for role_id, role in role_by_id.items():
                for row in role["occurrences"][snapshot.key]:
                    edits.append((row["offset"], row["length"], row["token"], role["replacement"], role_id))
            expected = bytearray(snapshot.data)
            for offset, length, token, replacement, _ in sorted(edits, reverse=True):
                self.assertEqual(bytes(expected[offset:offset + length]), token.encode("utf-8"))
                expected[offset:offset + length] = replacement.encode("ascii")
            materialized = self.artifact_root / "transformed" / "deterministic" / snapshot.language / snapshot.relative_path
            self.assertEqual(materialized.read_bytes(), bytes(expected), snapshot.key)

    def test_public_sequences_and_protected_lexical_chunks_are_independently_equal(self):
        for snapshot in self.snapshots:
            if snapshot.source_path.suffix.lower() not in (".cs", ".fs"):
                continue
            offsets = {
                row["offset"]
                for role in self.inventory["roles"]
                for row in role["occurrences"][snapshot.key]
            }
            deterministic = (self.artifact_root / "transformed" / "deterministic" / snapshot.language / snapshot.relative_path).read_bytes()
            with self.subTest(snapshot=snapshot.key):
                self.assertEqual(
                    _public_sequence(snapshot.data, snapshot.language, offsets),
                    _public_sequence(deterministic, snapshot.language),
                )
                self.assertEqual(_lex(snapshot.data, snapshot.language)[1], _lex(deterministic, snapshot.language)[1])

    def test_reports_are_reconciled_from_inventory_and_all_static_invariants_pass(self):
        occurrences = sum(
            len(rows)
            for role in self.inventory["roles"]
            for rows in role["occurrences"].values()
        )
        self.assertEqual(self.reports["roles"], 15)
        self.assertEqual(self.reports["occurrences"], occurrences)
        self.assertEqual(self.reports["coverage"], 1.0)
        self.assertTrue(all(self.reports["collision_checks"].values()))
        self.assertTrue(all(self.reports["invariants"].values()))
        snapshots = {snapshot.key: snapshot for snapshot in self.snapshots}
        roles = {role["role_id"]: role for role in self.inventory["roles"]}
        for role_id, role_rows in self.reports["coverage_by_role"].items():
            replacement = roles[role_id]["replacement"]
            for snapshot_key, row in role_rows.items():
                snapshot = snapshots[snapshot_key]
                materialized = self.artifact_root / "transformed" / "deterministic" / snapshot.language / snapshot.relative_path
                independently_observed = (
                    sum(item.token == replacement for item in scan_identifiers(materialized.read_bytes(), snapshot.language))
                    if snapshot.source_path.suffix.lower() in (".cs", ".fs", ".csproj", ".fsproj")
                    else 0
                )
                self.assertEqual(row["transformed"], independently_observed)
                if row["eligible"]:
                    self.assertEqual(row["eligible"], row["transformed"])
                    self.assertEqual(row["coverage"], 1.0)
                else:
                    self.assertEqual(row["status"], "absent")

    def test_metrics_cover_both_languages_all_stages_and_signed_deltas(self):
        metrics = self.reports["metrics"]
        self.assertEqual(metrics["proxy"]["version"], "0.14.0")
        self.assertEqual(metrics["proxy"]["encoding"], "o200k_base")
        expected_stages = {"baseline", *(task["id"] for task in self.original["tasks"])}
        numeric = {"source_files", "source_bytes", "source_lines", "approx_lexical_tokens", "tiktoken_count"}
        for language in ("csharp", "fsharp"):
            self.assertEqual(set(metrics["languages"][language]), expected_stages)
            for row in metrics["languages"][language].values():
                self.assertEqual(set(row["signed_delta_deterministic_minus_descriptive"]), numeric)
                for treatment in ("descriptive", "deterministic"):
                    arm = row[treatment]
                    self.assertEqual(len(arm["canonical_input_sha256"]), 64)
                    self.assertEqual(len(arm["tiktoken_ids_sha256"]), 64)
                for field in numeric:
                    self.assertEqual(
                        row["signed_delta_deterministic_minus_descriptive"][field],
                        row["deterministic"][field] - row["descriptive"][field],
                    )

    def test_provenance_and_artifact_hashes_reconcile(self):
        source_manifest = json.loads((self.artifact_root / "source-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(source_manifest["source_commit"], SOURCE_COMMIT)
        self.assertEqual(len(source_manifest["task_prompts"]), 8)
        manifest_blob = subprocess.run(
            ["git", "show", f"{SOURCE_COMMIT}:benchmarks/successor/manifest.json"],
            cwd=self.root,
            stdout=subprocess.PIPE,
            check=True,
        ).stdout
        self.assertEqual(source_manifest["original_manifest"]["sha256"], sha256(manifest_blob))
        generator = self.root / source_manifest["generator_source"]["path"]
        self.assertEqual(source_manifest["generator_source"]["sha256"], sha256(generator.read_bytes()))
        for treatment, languages in source_manifest["generated_files"].items():
            for language, files in languages.items():
                for relative, expected in files.items():
                    path = self.artifact_root / "transformed" / treatment / language / relative
                    self.assertEqual(sha256(path.read_bytes()), expected)

        hashes = json.loads((self.artifact_root / "artifact-hashes.json").read_text(encoding="utf-8"))
        self.assertTrue(hashes["self_excluded"])
        actual = {
            path.relative_to(self.artifact_root).as_posix(): sha256(path.read_bytes())
            for path in self.artifact_root.rglob("*")
            if path.is_file() and path.name != "artifact-hashes.json"
        }
        self.assertEqual(hashes["files"], actual)

    def test_generated_manifest_contract_matches_c2_exactly(self):
        original_contract = _manifest_contract(self.original)
        for name in ("descriptive.manifest.json", "deterministic.manifest.json"):
            generated = json.loads((self.artifact_root / name).read_text(encoding="utf-8"))
            self.assertEqual(_manifest_contract(generated), original_contract)

    def test_representation_check_is_successful_and_write_free(self):
        before = {
            path.relative_to(self.artifact_root).as_posix(): (sha256(path.read_bytes()), path.stat().st_mtime_ns)
            for path in self.artifact_root.rglob("*") if path.is_file()
        }
        report = check_representation(self.root)
        after = {
            path.relative_to(self.artifact_root).as_posix(): (sha256(path.read_bytes()), path.stat().st_mtime_ns)
            for path in self.artifact_root.rglob("*") if path.is_file()
        }
        self.assertTrue(report["ok"])
        self.assertTrue(report["write_free"])
        self.assertEqual(before, after)

    def _artifact_copy(self) -> Path:
        destination = self.artifact_root.parent / f"representation-v1-test-{uuid.uuid4().hex[:12]}"
        shutil.copytree(self.artifact_root, destination)
        self.addCleanup(lambda: shutil.rmtree(destination, ignore_errors=True))
        return destination

    def test_check_fails_on_missing_artifact_without_touching_canonical_tree(self):
        destination = self._artifact_copy()
        (destination / "mapping.json").unlink()

        def copy_known_good(_root: Path, temporary: Path, _artifact_name: str):
            shutil.copytree(self.artifact_root, temporary)
            return {"ok": True}

        with mock.patch("alf.representation._build_representation_into", side_effect=copy_known_good):
            with self.assertRaisesRegex(RepresentationError, "artifacts are stale"):
                check_representation(self.root, destination)

    def test_check_fails_fast_on_recorded_source_drift(self):
        destination = self._artifact_copy()
        source_manifest_path = destination / "source-manifest.json"
        source_manifest = json.loads(source_manifest_path.read_text(encoding="utf-8"))
        source_manifest["original_manifest"]["sha256"] = "0" * 64
        source_manifest_path.write_text(json.dumps(source_manifest), encoding="utf-8")
        with mock.patch("alf.representation._build_representation_into") as regenerate:
            with self.assertRaisesRegex(RepresentationError, "recorded input drift"):
                check_representation(self.root, destination)
            regenerate.assert_not_called()

    def test_build_refuses_targets_outside_versioned_successor_child(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(RepresentationError, "versioned direct child"):
                build_representation(self.root, Path(directory) / "representation-v1")


if __name__ == "__main__":
    unittest.main()
