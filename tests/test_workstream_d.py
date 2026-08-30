import copy
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from alf.models import ProcessResult
from alf.protocol import (
    EXPECTED_IMAGE_ID,
    canonical_json_hash,
    freeze_cell,
    load_frozen_manifest,
    tracked_text_sha256,
    validate_cell,
)
from alf.runner import _prepare_protocol_run, run_chain
from alf.workstream_d import (
    ASSIGNMENT_SHA256,
    CONFIGURATIONS,
    ROWS,
    assignment_hash,
    classify_stage1,
    classify_stage1_family,
    stage1_slot_ids,
    validate_family,
    validate_schedule,
)

ROOT = Path(__file__).resolve().parents[1]
FAMILY_PATH = Path("protocols/workstream-d-language-v1/definition.json")
CHILD_PATHS = {
    "H": Path("protocols/workstream-d-language-v1/h.json"),
    "M": Path("protocols/workstream-d-language-v1/m.json"),
    "L": Path("protocols/workstream-d-language-v1/l.json"),
}


def _write_json(path: Path, value: dict) -> None:
    path.write_text(
        json.dumps(value, indent=2, sort_keys=False) + "\n", encoding="utf-8"
    )


class FamilyRepository:
    """Small contained copy of every artifact reached by the v3 validator."""

    def __init__(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.root = Path(self.directory.name).resolve()
        shutil.copy2(
            ROOT / "Dockerfile.codex-agent", self.root / "Dockerfile.codex-agent"
        )
        target = self.root / "protocols" / "workstream-d-language-v1"
        target.parent.mkdir(parents=True)
        shutil.copytree(ROOT / FAMILY_PATH.parent, target)
        treatment = self.root / "benchmarks" / "successor" / "representation-v1"
        treatment.parent.mkdir(parents=True)
        shutil.copytree(
            ROOT / "benchmarks" / "successor" / "representation-v1", treatment
        )
        shutil.copytree(
            ROOT / "benchmarks" / "successor" / "tasks",
            self.root / "benchmarks" / "successor" / "tasks",
        )

    def read(self, relative: Path) -> dict:
        return json.loads((self.root / relative).read_text(encoding="utf-8"))

    def write(self, relative: Path, value: dict) -> None:
        _write_json(self.root / relative, value)

    def refresh_parent_child_hashes(self) -> None:
        parent = self.read(FAMILY_PATH)
        for configuration, relative in CHILD_PATHS.items():
            parent["children"][configuration]["definition_sha256"] = (
                tracked_text_sha256(self.root / relative)
            )
        self.write(FAMILY_PATH, parent)

    def repin_schedule(self) -> None:
        schedule_hash = tracked_text_sha256(
            self.root / "protocols/workstream-d-language-v1/schedule.json"
        )
        parent = self.read(FAMILY_PATH)
        parent["schedule_sha256"] = schedule_hash
        self.write(FAMILY_PATH, parent)
        for relative in CHILD_PATHS.values():
            child = self.read(relative)
            child["schedule_sha256"] = schedule_hash
            self.write(relative, child)
        self.refresh_parent_child_hashes()

    def repin_catalog(self) -> None:
        catalog_hash = tracked_text_sha256(
            self.root
            / "protocols/workstream-d-language-v1/model-catalog-preflight.json"
        )
        parent = self.read(FAMILY_PATH)
        parent["catalog_sha256"] = catalog_hash
        self.write(FAMILY_PATH, parent)
        for relative in CHILD_PATHS.values():
            child = self.read(relative)
            child["catalog_sha256"] = catalog_hash
            self.write(relative, child)
        self.refresh_parent_child_hashes()

    def close(self) -> None:
        self.directory.cleanup()


def _valid_probe() -> dict:
    return {
        "os": "Windows",
        "platform": "Windows-test",
        "architecture": "AMD64",
        "cpu": "test cpu",
        "physical_memory_bytes": 8_000_000_000,
        "python": "3.12.2",
        "git": "git version 2.46.2",
        "dotnet": "10.0.302",
        "docker_client": "27.2.0",
        "docker_server": "27.2.0",
        "image_id": EXPECTED_IMAGE_ID,
        "image_platform": "linux/amd64",
        "image_size_bytes": 630_000_000,
        "container_codex": "codex-cli 0.149.1",
        "container_dotnet": "10.0.302",
    }


def _valid_archive(definition: dict) -> dict:
    archive = definition["image_archive"]
    return {
        "path": archive["path"],
        "bytes": archive["bytes"],
        "sha256": archive["sha256"],
        "verified": True,
    }


def _slots(
    configuration: str,
    *,
    passed: int = 8,
    entered: int | None = None,
) -> list[dict]:
    return [
        {
            "slot_id": slot_id,
            "configuration_id": configuration,
            "resolved": True,
            "audited": True,
            "passed_tasks": passed,
            "entered_through": passed if entered is None else entered,
        }
        for slot_id in sorted(stage1_slot_ids(configuration))
    ]


class WorkstreamDValidationTests(unittest.TestCase):
    def test_parent_and_all_three_child_cells_validate(self) -> None:
        parent = validate_family(ROOT, FAMILY_PATH)
        self.assertTrue(parent["ok"], parent["errors"])
        self.assertEqual(set(parent["children"]), set(CONFIGURATIONS))
        self.assertEqual(validate_schedule(parent["schedule"]), [])
        self.assertEqual(assignment_hash(ROWS), ASSIGNMENT_SHA256)
        for relative in CHILD_PATHS.values():
            with self.subTest(relative=relative):
                report = validate_cell(ROOT, relative)
                self.assertTrue(report["ok"], report["errors"])
                self.assertEqual(report["definition"]["schema_version"], 3)
                self.assertIn("family_definition", report)

    def test_family_validate_rejects_a_child_definition(self) -> None:
        report = validate_family(ROOT, CHILD_PATHS["H"])
        self.assertFalse(report["ok"])
        self.assertTrue(any("parent definition" in error for error in report["errors"]))

    def test_parent_rejects_mutated_missing_and_inconsistent_children(self) -> None:
        repo = FamilyRepository()
        try:
            parent = repo.read(FAMILY_PATH)
            parent["children"]["H"]["definition_sha256"] = "0" * 64
            repo.write(FAMILY_PATH, parent)
            report = validate_family(repo.root, FAMILY_PATH)
            self.assertFalse(report["ok"])
            self.assertTrue(
                any("definition hash" in error for error in report["errors"])
            )

            repo.close()
            repo = FamilyRepository()
            (repo.root / CHILD_PATHS["M"]).unlink()
            report = validate_family(repo.root, FAMILY_PATH)
            self.assertFalse(report["ok"])
            self.assertTrue(any("child M" in error for error in report["errors"]))

            repo.close()
            repo = FamilyRepository()
            child = repo.read(CHILD_PATHS["M"])
            child["network_policy"] = "inconsistent"
            repo.write(CHILD_PATHS["M"], child)
            repo.refresh_parent_child_hashes()
            report = validate_family(repo.root, FAMILY_PATH)
            self.assertFalse(report["ok"])
            self.assertTrue(
                any("network_policy" in error for error in report["errors"])
            )
        finally:
            repo.close()

    def test_parent_rejects_repo_path_and_raw_root_escape(self) -> None:
        repo = FamilyRepository()
        try:
            outside = repo.root.parent / "outside-child.json"
            parent = repo.read(FAMILY_PATH)
            parent["children"]["H"]["definition_file"] = str(outside)
            repo.write(FAMILY_PATH, parent)
            report = validate_family(repo.root, FAMILY_PATH)
            self.assertFalse(report["ok"])
            self.assertTrue(
                any("escapes repository" in error for error in report["errors"])
            )

            repo.close()
            repo = FamilyRepository()
            child = repo.read(CHILD_PATHS["L"])
            child["raw_root"] = str(repo.root.parent / "outside-results")
            repo.write(CHILD_PATHS["L"], child)
            repo.refresh_parent_child_hashes()
            report = validate_family(repo.root, FAMILY_PATH)
            self.assertFalse(report["ok"])
            self.assertTrue(
                any("raw_root escapes" in error for error in report["errors"])
            )
        finally:
            repo.close()

    def test_schedule_calibration_assignment_and_catalog_mutations_fail(self) -> None:
        repo = FamilyRepository()
        try:
            schedule_path = Path("protocols/workstream-d-language-v1/schedule.json")
            schedule = repo.read(schedule_path)
            schedule["formal"][0].update(
                {"direction": "C#>F#", "order": ["csharp", "fsharp"]}
            )
            repo.write(schedule_path, schedule)
            repo.repin_schedule()
            report = validate_family(repo.root, FAMILY_PATH)
            self.assertFalse(report["ok"])
            self.assertTrue(
                any("assignment hash" in error for error in report["errors"])
            )

            repo.close()
            repo = FamilyRepository()
            schedule = repo.read(schedule_path)
            schedule["calibration"][3]["conditional"] = False
            repo.write(schedule_path, schedule)
            repo.repin_schedule()
            report = validate_family(repo.root, FAMILY_PATH)
            self.assertFalse(report["ok"])
            self.assertTrue(any("calibration" in error for error in report["errors"]))

            repo.close()
            repo = FamilyRepository()
            catalog_path = Path(
                "protocols/workstream-d-language-v1/model-catalog-preflight.json"
            )
            catalog = repo.read(catalog_path)
            catalog["models"]["gpt-5.4-mini"]["supported_in_api"] = False
            repo.write(catalog_path, catalog)
            repo.repin_catalog()
            report = validate_family(repo.root, FAMILY_PATH)
            self.assertFalse(report["ok"])
            self.assertTrue(any("catalog entry" in error for error in report["errors"]))
        finally:
            repo.close()

    def test_gate_all_branches_and_precedence(self) -> None:
        saturated = classify_stage1(_slots("H"), configuration_id="H")
        self.assertEqual(saturated["classification"], "SATURATED")
        self.assertEqual(saturated["possible_positions"], 64)
        self.assertEqual(
            classify_stage1(_slots("H", passed=5, entered=5), configuration_id="H")[
                "classification"
            ],
            "IMPOSSIBLE",
        )
        self.assertEqual(
            classify_stage1(_slots("H", passed=3, entered=8), configuration_id="H")[
                "classification"
            ],
            "IMPOSSIBLE",
        )
        self.assertEqual(
            classify_stage1(_slots("H", passed=7, entered=7), configuration_id="H")[
                "classification"
            ],
            "INFORMATIVE",
        )
        self.assertEqual(
            classify_stage1(_slots("H", passed=6, entered=6), configuration_id="H")[
                "classification"
            ],
            "INDETERMINATE",
        )
        self.assertTrue(
            classify_stage1(
                _slots("H", passed=7, entered=7),
                apparatus_stop=True,
                configuration_id="H",
            )["apparatus_stop"]
        )

    def test_gate_requires_eight_unique_explicit_resolved_audited_slots(self) -> None:
        bad_cases = []
        bad_cases.append(_slots("H")[:7])
        duplicate = _slots("H")
        duplicate[1]["slot_id"] = duplicate[0]["slot_id"]
        bad_cases.append(duplicate)
        missing = _slots("H")
        del missing[0]["slot_id"]
        bad_cases.append(missing)
        unresolved = _slots("H")
        unresolved[0]["resolved"] = False
        bad_cases.append(unresolved)
        unaudited = _slots("H")
        unaudited[0]["audited"] = False
        bad_cases.append(unaudited)
        out_of_range = _slots("H")
        out_of_range[0]["passed_tasks"] = 9
        bad_cases.append(out_of_range)
        impossible_trajectory = _slots("H")
        impossible_trajectory[0]["passed_tasks"] = 6
        impossible_trajectory[0]["entered_through"] = 5
        bad_cases.append(impossible_trajectory)
        for slots in bad_cases:
            with self.subTest(slots=slots):
                self.assertTrue(
                    classify_stage1(slots, configuration_id="H")["apparatus_stop"]
                )

    def test_family_gate_ignores_contrast_fields_and_continues_on_any_informative(
        self,
    ) -> None:
        outcomes = {
            "H": _slots("H"),
            "M": _slots("M", passed=7, entered=7),
            "L": _slots("L", passed=5, entered=5),
            "fsharp_minus_csharp": 99_999_999,
        }
        report = classify_stage1_family(outcomes)
        self.assertTrue(report["continue"])
        self.assertFalse(report["apparatus_stop"])
        del outcomes["L"]
        self.assertTrue(classify_stage1_family(outcomes)["apparatus_stop"])


class WorkstreamDFreezeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = FamilyRepository()

    def tearDown(self) -> None:
        self.repo.close()

    def _freeze(self) -> dict:
        definition = self.repo.read(CHILD_PATHS["H"])
        with patch("alf.protocol._git", side_effect=["", "a" * 40]):
            return freeze_cell(
                self.repo.root,
                CHILD_PATHS["H"],
                _probe=lambda *_: _valid_probe(),
                _archive_verifier=lambda *_: _valid_archive(definition),
            )

    def _write_manifest(self, manifest: dict) -> Path:
        target = (
            self.repo.root
            / "results"
            / "workstream-d-language-v1"
            / "h"
            / "resolved-manifest.json"
        )
        target.parent.mkdir(parents=True, exist_ok=True)
        _write_json(target, manifest)
        return target

    def test_freeze_embeds_relative_family_schedule_catalog_and_identity(self) -> None:
        manifest = self._freeze()
        self.assertEqual(manifest["family_id"], "workstream-d-language-v1")
        self.assertEqual(manifest["configuration_id"], "H")
        self.assertEqual(manifest["family_definition_file"], FAMILY_PATH.as_posix())
        self.assertEqual(
            manifest["parent_schedule_file"],
            "protocols/workstream-d-language-v1/schedule.json",
        )
        self.assertEqual(
            manifest["catalog_file"],
            "protocols/workstream-d-language-v1/model-catalog-preflight.json",
        )
        self.assertIsInstance(manifest["family_definition"], dict)
        self.assertEqual(manifest["assignment_sha256"], ASSIGNMENT_SHA256)

        path = self._write_manifest(manifest)
        with (
            patch("alf.protocol._require_ignored"),
            patch("alf.protocol._git", side_effect=["", "a" * 40]),
        ):
            loaded = load_frozen_manifest(self.repo.root, path)
        self.assertEqual(loaded, manifest)

    def test_every_child_can_be_frozen_with_mocked_environment(self) -> None:
        for configuration, relative in CHILD_PATHS.items():
            with self.subTest(configuration=configuration):
                definition = self.repo.read(relative)
                with patch("alf.protocol._git", side_effect=["", "a" * 40]):
                    manifest = freeze_cell(
                        self.repo.root,
                        relative,
                        _probe=lambda *_: _valid_probe(),
                        _archive_verifier=lambda *_, definition=definition: (
                            _valid_archive(definition)
                        ),
                    )
                self.assertEqual(manifest["configuration_id"], configuration)
                self.assertEqual(manifest["definition"]["model"], definition["model"])

    def test_rehashed_v3_field_and_embedded_object_tampering_fails_load(self) -> None:
        original = self._freeze()
        mutations = {
            "configuration_id": lambda value: value.update(configuration_id="M"),
            "family_definition_sha256": lambda value: value.update(
                family_definition_sha256="0" * 64
            ),
            "family_definition": lambda value: value["family_definition"].update(
                representation="deterministic"
            ),
            "parent_schedule_sha256": lambda value: value.update(
                parent_schedule_sha256="0" * 64
            ),
            "catalog": lambda value: value["catalog"].update(supported_in_api=False),
            "assignment_sha256": lambda value: value.update(assignment_sha256="0" * 64),
            "unknown": lambda value: value.update(unreviewed=True),
        }
        for name, mutate in mutations.items():
            with self.subTest(name=name):
                manifest = copy.deepcopy(original)
                mutate(manifest)
                manifest.pop("manifest_sha256")
                manifest["manifest_sha256"] = canonical_json_hash(manifest)
                path = self._write_manifest(manifest)
                with (
                    patch("alf.protocol._require_ignored"),
                    patch("alf.protocol._git", side_effect=["", "a" * 40]),
                    self.assertRaisesRegex(ValueError, "Workstream D"),
                ):
                    load_frozen_manifest(self.repo.root, path)


class WorkstreamDRunnerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = FamilyRepository()
        self.report = validate_cell(self.repo.root, CHILD_PATHS["H"])
        self.assertTrue(self.report["ok"], self.report["errors"])
        self.definition = self.report["definition"]
        self.benchmark = json.loads(
            (self.repo.root / self.definition["benchmark_manifest"]).read_text(
                encoding="utf-8"
            )
        )
        self.output = self.repo.root / self.definition["raw_root"]
        self.output.mkdir(parents=True)
        self.manifest_path = self.repo.root / "mock-frozen-manifest.json"
        self.manifest_path.write_text("{}", encoding="utf-8")
        self.protocol = {
            "schema_version": 3,
            "manifest_sha256": "f" * 64,
            "cell_id": self.definition["cell_id"],
            "git_head": "a" * 40,
            "definition_sha256": self.report["definition_sha256"],
            "schedule_sha256": self.report["schedule_sha256"],
            "image": self.definition["codex"]["image"],
            "image_id": EXPECTED_IMAGE_ID,
            "definition": self.definition,
            "schedule": self.report["schedule"],
            "family_id": self.definition["family_id"],
            "configuration_id": "H",
            "family_definition_sha256": self.report["family_definition_sha256"],
            "parent_schedule_sha256": self.report["schedule_sha256"],
            "catalog_sha256": self.report["catalog_sha256"],
            "assignment_sha256": ASSIGNMENT_SHA256,
        }

    def tearDown(self) -> None:
        self.repo.close()

    @staticmethod
    def _image_result(image_id: str = EXPECTED_IMAGE_ID) -> ProcessResult:
        return ProcessResult(["docker"], 0, image_id + "\n", "", 0.01)

    def _prepare(self, **overrides):
        arguments = {
            "root": self.repo.root,
            "benchmark_manifest": self.benchmark,
            "language": "fsharp",
            "agent_name": "command",
            "output_root": self.output,
            "model": "gpt-5.4",
            "agent_command": None,
            "timeout": 600,
            "max_tasks": None,
            "require_usage": True,
            "protocol_manifest": self.manifest_path,
            "block_id": "mb01-h",
            "order": "fsharp-first",
            "attempt_id": "mb01-h-fsharp-01",
            "position": 1,
        }
        arguments.update(overrides)
        with (
            patch("alf.runner.load_frozen_manifest", return_value=self.protocol),
            patch("alf.runner.run_process", return_value=self._image_result()),
        ):
            return _prepare_protocol_run(**arguments)

    def _select_configuration(self, configuration: str) -> None:
        report = validate_cell(self.repo.root, CHILD_PATHS[configuration])
        self.assertTrue(report["ok"], report["errors"])
        self.report = report
        self.definition = report["definition"]
        self.benchmark = json.loads(
            (self.repo.root / self.definition["benchmark_manifest"]).read_text(
                encoding="utf-8"
            )
        )
        self.output = self.repo.root / self.definition["raw_root"]
        self.output.mkdir(parents=True, exist_ok=True)
        self.protocol.update(
            {
                "cell_id": self.definition["cell_id"],
                "definition_sha256": report["definition_sha256"],
                "schedule_sha256": report["schedule_sha256"],
                "definition": self.definition,
                "schedule": report["schedule"],
                "configuration_id": configuration,
                "family_definition_sha256": report["family_definition_sha256"],
                "parent_schedule_sha256": report["schedule_sha256"],
                "catalog_sha256": report["catalog_sha256"],
            }
        )

    def _prior_result(
        self,
        *,
        block_id: str = "mb01-h",
        order: str = "fsharp-first",
        position: int = 1,
        language: str = "fsharp",
        attempt_id: str = "mb01-h-fsharp-01",
        disposition: dict | None = None,
        baseline_ok: bool = True,
    ) -> None:
        target = self.output / f"prior-{attempt_id}"
        target.mkdir(parents=True)
        result = {
            "finished_at": "2026-08-30T00:00:00+00:00",
            "baseline": {"ok": baseline_ok},
            "tasks": [{"finished_at": "2026-08-30T00:00:01+00:00"}],
            "provenance": {
                "cell_id": self.protocol["cell_id"],
                "manifest_sha256": self.protocol["manifest_sha256"],
                "block_id": block_id,
                "order": order,
                "position": position,
                "language": language,
                "attempt_id": attempt_id,
            },
            "disposition": disposition
            or {
                "analysis_role": "primary",
                "protocol_valid": True,
                "candidate_outcome": True,
                "retryable": False,
            },
        }
        _write_json(target / "result.json", result)

    def test_formal_pair_positions_use_execution_position_not_placement(self) -> None:
        prepared, command, attempt_number = self._prepare()
        self.assertEqual(attempt_number, 1)
        self.assertEqual(prepared["_workstream_d_row"]["within_macroblock_position"], 1)
        self.assertIn('--model "gpt-5.4"', command)
        self.assertIn('--reasoning-effort "medium"', command)

        self._prior_result()
        prepared, _, attempt_number = self._prepare(
            language="csharp",
            position=2,
            attempt_id="mb01-h-csharp-01",
        )
        self.assertEqual(attempt_number, 1)
        self.assertEqual(prepared["_workstream_d_config"], "H")

    def test_calibration_pair_is_executable_and_non_counting(self) -> None:
        prepared, _, _ = self._prepare(
            block_id="cal-h-primary",
            attempt_id="cal-h-primary-fsharp-01",
        )
        row = prepared["_workstream_d_row"]
        self.assertEqual(row["calibration_id"], "cal-h-primary")
        self.assertEqual(row["stage"], 0)
        self.assertFalse(row["counting"])

        self._select_configuration("M")
        prepared, _, _ = self._prepare(
            block_id="cal-m-reverse",
            attempt_id="cal-m-reverse-fsharp-01",
        )
        row = prepared["_workstream_d_row"]
        self.assertEqual(row["role"], "calibration-reverse-confirmation")
        self.assertTrue(row["conditional"])

    def test_retry_increments_and_unresolved_attempt_blocks(self) -> None:
        self._prior_result(
            disposition={
                "analysis_role": "infrastructure-invalid",
                "retryable": True,
            }
        )
        _, _, number = self._prepare(attempt_id="mb01-h-fsharp-02")
        self.assertEqual(number, 2)

        unresolved = self.output / "unresolved"
        unresolved.mkdir()
        _write_json(
            unresolved / "attempt.json",
            {
                "state": "started",
                "provenance": {
                    "cell_id": self.protocol["cell_id"],
                    "manifest_sha256": self.protocol["manifest_sha256"],
                    "block_id": "cal-h-primary",
                    "position": 1,
                    "attempt_id": "cal-h-primary-fsharp-01",
                },
            },
        )
        with self.assertRaisesRegex(ValueError, "unresolved"):
            self._prepare(
                block_id="cal-h-primary",
                attempt_id="cal-h-primary-fsharp-02",
            )

    def test_wrong_model_order_configuration_position_and_attempt_fail(self) -> None:
        cases = (
            ({"model": "gpt-5.4-mini"}, "model"),
            ({"order": "csharp-first"}, "order"),
            ({"block_id": "mb01-m"}, "not in"),
            ({"position": 3}, "position"),
            ({"attempt_id": "mb01-h-fsharp-99"}, "attempt_id"),
        )
        for overrides, expected in cases:
            with (
                self.subTest(overrides=overrides),
                self.assertRaisesRegex(ValueError, expected),
            ):
                self._prepare(**overrides)

        self.protocol["configuration_id"] = "M"
        with self.assertRaisesRegex(ValueError, "configuration identity"):
            self._prepare()

    def test_position_two_requires_exact_retained_predecessor(self) -> None:
        with self.assertRaisesRegex(ValueError, "position-1"):
            self._prepare(
                language="csharp",
                position=2,
                attempt_id="mb01-h-csharp-01",
            )
        self._prior_result(baseline_ok=False)
        with self.assertRaisesRegex(ValueError, "position-1"):
            self._prepare(
                language="csharp",
                position=2,
                attempt_id="mb01-h-csharp-01",
            )

    def test_run_chain_records_complete_v3_provenance_and_exact_manifest(self) -> None:
        protocol = dict(self.protocol)
        protocol["_workstream_d_row"] = next(
            row for row in protocol["schedule"]["formal"] if row["block_id"] == "mb01-h"
        )
        protocol["_workstream_d_config"] = "H"
        benchmark = {
            "id": "v3-provenance-test",
            "languages": {"fsharp": {}},
            "baseline_cases": [],
            "tasks": [],
        }

        def initialize(_root, _manifest, _language, workspace):
            workspace.mkdir(parents=True)

        with (
            patch(
                "alf.runner._prepare_protocol_run",
                return_value=(protocol, "agent", 1),
            ),
            patch("alf.runner.init_workspace", side_effect=initialize),
            patch("alf.runner.make_agent", return_value=object()),
            patch(
                "alf.runner.evaluate_project",
                return_value={
                    "ok": False,
                    "build": {
                        "returncode": 1,
                        "timed_out": False,
                        "missing_executable": False,
                    },
                },
            ),
            patch("alf.runner.environment_snapshot", return_value={}),
        ):
            run_dir = run_chain(
                root=self.repo.root,
                manifest=benchmark,
                language="fsharp",
                agent_name="command",
                output_root=self.output,
                model="gpt-5.4",
                timeout=600,
                require_usage=True,
                protocol_manifest=self.manifest_path,
                block_id="mb01-h",
                order="fsharp-first",
                attempt_id="mb01-h-fsharp-01",
                position=1,
            )
        result = json.loads((run_dir / "result.json").read_text(encoding="utf-8"))
        provenance = result["provenance"]
        self.assertEqual(provenance["family_id"], "workstream-d-language-v1")
        self.assertEqual(provenance["configuration_id"], "H")
        self.assertEqual(provenance["pair_block_id"], "mb01-h")
        self.assertEqual(provenance["execution_position"], 1)
        self.assertEqual(provenance["within_macroblock_position"], 1)
        self.assertEqual(provenance["stage"], 1)
        self.assertTrue(provenance["counting"])
        self.assertEqual(provenance["assignment_sha256"], ASSIGNMENT_SHA256)
        self.assertEqual(
            (run_dir / "protocol-manifest.json").read_bytes(),
            self.manifest_path.read_bytes(),
        )


if __name__ == "__main__":
    unittest.main()
