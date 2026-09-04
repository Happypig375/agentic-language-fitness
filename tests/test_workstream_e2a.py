from __future__ import annotations

from collections import Counter
import copy
import hashlib
import json
import math
import tempfile
import unittest
from unittest import mock
from pathlib import Path

from alf.cli import build_parser
from alf.config import load_manifest
from alf.protocol import canonical_json_hash
from alf.workstream_e import (
    EXPECTED_TASK_IDS,
    FAMILY_ID,
    OUTPUT_REPORT_TYPE,
    classify_command,
)
from alf.workstream_e2 import _materialize
from alf.workstream_e2a import (
    ATTEMPT_SCHEMA,
    DEFINITION_SCHEMA,
    ENVIRONMENT_SCHEMA,
    EXPECTED_BENCHMARK_DOTNET_OPERATIONS,
    EXPECTED_COMPLETED_COMMANDS,
    EXPECTED_OPERATION_TOTALS,
    INVENTORY_SCHEMA,
    MEASUREMENT_SCHEMA,
    PINNED_IMAGE_ENVIRONMENT,
    RAW_INVENTORY_SCHEMA,
    REPORT_SCHEMA,
    E2aError,
    _finish_hash,
    _resolve_runtime_input,
    _runtime_source_snapshot,
    _sample_environment,
    _write_attempt,
    _write_raw_inventory,
    audit,
    audit_eligible,
    build_schedule,
    canonical_argv,
    check,
    environment_contract,
    freeze,
    inventory,
    report,
    validate_report,
    validate_environment,
)
import alf.workstream_e2a as e2a_module


ROOT = Path(__file__).resolve().parents[1]
E2_DEFINITION_PATH = ROOT / "protocols" / "workstream-e2-toolchain-v1" / "definition.json"
MANIFEST_PATH = ROOT / "benchmarks" / "successor" / "manifest.json"
RUNNER_SHA = "a" * 40


def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _command_record(command: str, ordinal: int) -> dict[str, object]:
    classified = classify_command(command)
    return {
        "event_ordinal": ordinal,
        **{key: classified[key] for key in (
            "classifier_version", "labels", "ambiguous_or_unparsed", "disposition",
            "ambiguity_reasons", "connectors", "equivalence_classes",
        )},
        "operations": [
            {**operation, "outcome": {"value": "success", "reason": "synthetic-success"}}
            for operation in classified["operations"]
        ],
    }


def _benchmark_commands() -> list[str]:
    commands = [
        "bash -lc \"dotnet restore && dotnet build && printf '{}' | dotnet run\"",
    ]
    commands.extend(["bash -lc 'dotnet restore'"] * 11)
    commands.append("bash -lc 'dotnet restore --ignore-failed-sources'")
    commands.append("bash -lc 'dotnet restore OrderFlow.fsproj'")
    commands.extend(["bash -lc 'dotnet build'"] * 10)
    commands.extend(["bash -lc 'dotnet build OrderFlow.fsproj'"] * 2)
    commands.extend(["bash -lc 'dotnet build --nologo'"] * 43)
    commands.extend(["bash -lc 'dotnet build --no-restore'"] * 58)
    commands.extend(["bash -lc 'dotnet build OrderFlow.fsproj --no-restore'"] * 2)
    commands.extend(["bash -lc 'dotnet build --no-restore --nologo'"] * 3)
    commands.extend(["bash -lc 'dotnet run --no-restore'"] * 3)
    commands.append("bash -lc 'dotnet run --no-restore --nologo'")
    # Include all three target-input forms and a real heredoc envelope.
    commands.append("bash -lc \"printf '{}' | dotnet run --no-build\"")
    commands.append("bash -lc 'dotnet run --no-build < cases.ndjson'")
    commands.append("bash -lc 'dotnet run --no-build <<EOF\n{}\nEOF'")
    commands.extend(["bash -lc 'dotnet run --no-build --no-restore'"] * 40)
    commands.extend(["bash -lc 'dotnet run --project OrderFlow.fsproj --no-build'"] * 20)
    commands.extend(["bash -lc 'dotnet run --no-build --nologo'"] * 20)
    commands.extend(["bash -lc 'dotnet run --no-build'"] * 32)
    commands.extend(["bash -lc 'dotnet test --no-restore'"] * 3)
    commands.append("bash -lc 'dotnet test --no-build --no-restore'")
    commands.append("bash -lc 'dotnet bin/Debug/net10.0/OrderFlow.dll < cases.ndjson'")
    counts = Counter()
    for command in commands:
        if ".dll" in command:
            counts["direct"] += 1
            continue
        classified = classify_command(command)
        for operation in classified["operations"]:
            labels = operation["labels"]
            if "build" in labels:
                counts["build"] += 1
            elif "project_configuration" in labels and "restore" in command:
                counts["restore"] += 1
            elif "test_or_run" in labels:
                if "dotnet test" in command:
                    counts["test"] += 1
                else:
                    counts["run"] += 1
    if counts != Counter(EXPECTED_OPERATION_TOTALS):
        raise AssertionError(counts)
    return commands


def _build_authenticated_fixture(base: Path) -> tuple[Path, Path]:
    archive = base / "archive"
    commands = _benchmark_commands()
    if len(commands) != 256:
        raise AssertionError(len(commands))
    commands.extend([
        "bash -lc 'dotnet --version'",
        "bash -lc 'dotnet --info'",
        "bash -lc 'dotnet --list-sdks'",
        "bash -lc 'dotnet --list-runtimes'",
        "bash -lc 'dotnet --version'",
        "bash -lc 'dotnet --info'",
        "bash -lc 'dotnet --version'",
    ])
    commands.append("bash -lc '(test -f OrderFlow.fsproj)'" )
    commands.extend(["bash -lc 'pwd'"] * (EXPECTED_COMPLETED_COMMANDS - len(commands)))
    if len(commands) != EXPECTED_COMPLETED_COMMANDS:
        raise AssertionError(len(commands))

    run_specs = [
        ("H", "csharp", "h-csharp-01", 0),
        ("H", "fsharp", "h-fsharp-01", 41),
        ("L", "csharp", "l-csharp-01", 0),
        ("L", "fsharp", "l-fsharp-01", 44),
        ("L", "csharp", "l-csharp-02", 0),
        ("L", "fsharp", "l-fsharp-02", 44),
        ("M", "csharp", "m-csharp-01", 0),
        ("M", "fsharp", "m-fsharp-01", 34),
        ("M", "csharp", "m-csharp-02", 0),
        ("M", "fsharp", "m-fsharp-02", 34),
    ]
    per_run = [44] * 5 + [43] * 5
    cursor = 0
    runs: list[dict[str, object]] = []
    for run_number, ((configuration, language, attempt_id, nu_count), run_command_count) in enumerate(
        zip(run_specs, per_run), 1
    ):
        run_commands = commands[cursor:cursor + run_command_count]
        cursor += run_command_count
        task_sizes = [run_command_count // 8] * 8
        for index in range(run_command_count % 8):
            task_sizes[index] += 1
        task_cursor = 0
        remaining_nu = nu_count
        tasks: list[dict[str, object]] = []
        for task_number, (task_id, task_size) in enumerate(zip(EXPECTED_TASK_IDS, task_sizes), 1):
            task_commands = run_commands[task_cursor:task_cursor + task_size]
            task_cursor += task_size
            events: list[dict[str, object]] = [
                {"type": "thread.started", "thread_id": f"thread-{run_number}-{task_number}"},
                {"type": "turn.started"},
            ]
            public_commands: list[dict[str, object]] = []
            for local_index, command in enumerate(task_commands, 1):
                output_lines = min(remaining_nu, 5)
                remaining_nu -= output_lines
                output = "\n".join(
                    "warning NU1900: synthetic vulnerability source unavailable"
                    for _ in range(output_lines)
                )
                event = {
                    "type": "item.completed",
                    "item": {
                        "id": f"item-{run_number}-{task_number}-{local_index}",
                        "type": "command_execution",
                        "command": command,
                        "aggregated_output": output,
                        "exit_code": 0,
                        "status": "completed",
                    },
                }
                events.append(event)
                public_commands.append(_command_record(command, len(events)))
            events.append({"type": "turn.completed", "usage": {}})
            raw = b"".join(
                json.dumps(event, sort_keys=True, separators=(",", ":")).encode("utf-8") + b"\n"
                for event in events
            )
            task_dir = archive / configuration.casefold() / attempt_id / "tasks" / task_id
            task_dir.mkdir(parents=True, exist_ok=True)
            (task_dir / "events.jsonl").write_bytes(raw)
            tasks.append({
                "attempt_id": attempt_id,
                "configuration_id": configuration,
                "language": language,
                "task_id": task_id,
                "input_identity": {"events_sha256": _sha(raw), "task_id": task_id},
                "commands": public_commands,
            })
        if remaining_nu:
            raise AssertionError((attempt_id, remaining_nu))
        runs.append({
            "attempt_id": attempt_id,
            "configuration_id": configuration,
            "language": language,
            "timing": {"agent_process_wall_seconds": float(100 + run_number)},
            "tasks": tasks,
        })
    if cursor != len(commands):
        raise AssertionError((cursor, len(commands)))
    report_data: dict[str, object] = {
        "report_type": OUTPUT_REPORT_TYPE,
        "family_id": FAMILY_ID,
        "runs": runs,
    }
    report_data["report_sha256"] = canonical_json_hash(report_data)
    report_path = base / "forensic-report.json"
    report_path.write_text(json.dumps(report_data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report_path, archive


def _environment(runner_sha: str = RUNNER_SHA) -> dict[str, object]:
    observed = {
        "schema_version": ENVIRONMENT_SCHEMA,
        **environment_contract(),
        "e2a_runner_git_sha": runner_sha,
        "container_self_observation": {
            "uid": 1000,
            "gid": 1000,
            "cgroup_v2": {
                "memory_max_bytes": 2 * 1024 * 1024 * 1024,
                "cpu_quota": 200000,
                "cpu_period": 100000,
                "cpu_ratio": 2.0,
                "pids_max": 256,
            },
            "mounts": {
                "root_filesystem": "overlay",
                "root_mode": "rw",
                "tmp_filesystem": "overlay",
                "tmp_mode": "rw",
                "work_root_filesystem": "ext4",
                "work_root_mode": "rw",
            },
            "tmp_writable": True,
            "proxy_environment_exact": True,
            "pinned_image_environment_exact": True,
            "codex_process_present": False,
            "model_endpoint_configured": False,
            "auth_material_present": False,
        },
    }
    return observed


def _write_operation(raw: Path, stem: str, seconds: float) -> dict[str, object]:
    stdout = b"{}\n"
    stderr = b""
    stdout_file = f"{stem}.stdout.bin"
    stderr_file = f"{stem}.stderr.bin"
    metadata_file = f"{stem}.json"
    (raw / stdout_file).parent.mkdir(parents=True, exist_ok=True)
    (raw / stdout_file).write_bytes(stdout)
    (raw / stderr_file).write_bytes(stderr)
    record: dict[str, object] = {
        "label": "measured",
        "argv": ["dotnet", "build"],
        "shell": False,
        "input_transport": "none",
        "timeout_seconds": 300,
        "wall_seconds": seconds,
        "timed_out": False,
        "exit_code": 0,
        "stdout": {"file": stdout_file, "bytes": len(stdout), "sha256": _sha(stdout)},
        "stderr": {"file": stderr_file, "bytes": 0, "sha256": _sha(stderr)},
        "diagnostics": {
            "occurrence_count": 0,
            "counts_by_code": {},
            "counts_by_category": {},
            "counts_by_severity": {},
            "nu1900_occurrences": 0,
        },
    }
    (raw / metadata_file).write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    record["metadata_file"] = metadata_file
    return record


def _synthetic_raw(
    raw: Path,
    definition: dict[str, object],
    inventory_data: dict[str, object],
) -> None:
    raw.mkdir(parents=True)
    state_ids = {
        (row["language"], row["stage"]): row["state_id"]
        for row in definition["accepted_e2"]["successor_states"]
    }
    samples: list[dict[str, object]] = []
    for row in definition["schedule"]:
        seconds = 2.0 if row["language"] == "fsharp" else 1.0
        if row["audit_condition"] == "audit_off":
            seconds -= 0.1
        operation = _write_operation(raw, f"samples/{row['position']:04d}/measured", seconds)
        samples.append({
            **row,
            "state_id": state_ids[(row["language"], row["stage"])],
            "source_tree_sha256": "b" * 64,
            "prerequisites": [],
            "operation": operation,
            "evaluator": {
                "ok": True,
                "case_count": 0,
                "passed_case_count": 0,
                "workspace_check_counts": {},
                "wall_seconds": 0.001,
            },
            "cache": {
                "before": {"file_count": 0, "total_bytes": 0, "set_sha256": "c" * 64},
                "after": {"file_count": 0, "total_bytes": 0, "set_sha256": "c" * 64},
                "fresh_before": True,
            },
            "load_before": {"cpu_count": 2},
            "load_after": {"cpu_count": 2},
        })
    measurement = _finish_hash({
        "schema_version": MEASUREMENT_SCHEMA,
        "definition_sha256": definition["definition_sha256"],
        "inventory_sha256": inventory_data["inventory_sha256"],
        "schedule_sha256": definition["schedule_sha256"],
        "runner_git_sha": RUNNER_SHA,
        "environment": _environment(),
        "preflight": {
            "state_count": 16,
            "all_passed": True,
            "mode": "normalized-file-hash-compile-obligation-and-workspace-check",
        },
        "samples": samples,
    }, "measurement_sha256")
    (raw / "measurement.json").write_text(json.dumps(measurement, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    raw_inventory = _write_raw_inventory(raw)
    _write_attempt(raw, {
        "status": "success",
        "phase": "complete",
        "definition_sha256": definition["definition_sha256"],
        "runner_git_sha": RUNNER_SHA,
        "completed_preflight_states": 16,
        "completed_samples": len(samples),
        "current_position": None,
        "failure_code": None,
        "measurement_sha256": measurement["measurement_sha256"],
        "raw_inventory_sha256": raw_inventory["inventory_sha256"],
    })


class E2aTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temporary = tempfile.TemporaryDirectory(prefix="alf-e2a-tests-")
        cls.base = Path(cls.temporary.name)
        cls.e1_report_path, cls.archive = _build_authenticated_fixture(cls.base)
        cls.inventory = inventory(cls.e1_report_path, cls.archive)
        cls.e2_definition = json.loads(E2_DEFINITION_PATH.read_text(encoding="utf-8"))
        cls.definition = freeze(
            cls.inventory,
            cls.e2_definition,
            e2a_runner_git_sha=RUNNER_SHA,
        )

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temporary.cleanup()

    def test_inventory_authenticates_compounds_denominators_and_privacy(self):
        data = self.inventory
        self.assertEqual(data["schema_version"], INVENTORY_SCHEMA)
        self.assertEqual(data["denominator"]["completed_command_events"], 435)
        self.assertEqual(data["denominator"]["benchmark_dotnet_operations"], 258)
        self.assertEqual(data["denominator"]["operation_totals"], EXPECTED_OPERATION_TOTALS)
        self.assertEqual(data["nu1900"]["by_language"], {"csharp": 0, "fsharp": 197})
        forms = data["form_catalog"]
        self.assertTrue(any(row["input_transport"] == "pipeline" for row in forms))
        self.assertTrue(any(row["input_transport"] == "input-redirection" for row in forms))
        self.assertTrue(any(row["operation"] == "direct" for row in forms))
        public = json.dumps(data, sort_keys=True)
        self.assertNotIn("dotnet build", public)
        self.assertNotIn('"argv"', public)
        self.assertNotIn("thread-", public)

    def test_inventory_detects_raw_tamper_and_uses_enumerated_ordinal(self):
        copied = self.base / "tampered-archive"
        import shutil
        shutil.copytree(self.archive, copied)
        target = next(copied.rglob("events.jsonl"))
        target.write_bytes(target.read_bytes() + b"\n")
        with self.assertRaisesRegex(E2aError, "e1_events_digest_mismatch"):
            inventory(self.e1_report_path, copied)

    def test_inventory_rejects_duplicate_public_ordinal_with_raw_omission(self):
        report_data = json.loads(self.e1_report_path.read_text(encoding="utf-8"))
        commands = report_data["runs"][0]["tasks"][0]["commands"]
        self.assertGreaterEqual(len(commands), 2)
        commands[1]["event_ordinal"] = commands[0]["event_ordinal"]
        report_data.pop("report_sha256")
        report_data["report_sha256"] = canonical_json_hash(report_data)
        path = self.base / "duplicate-public-ordinal-report.json"
        path.write_text(json.dumps(report_data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        with self.assertRaisesRegex(E2aError, "e1_public_command_ordinal_duplicate_or_invalid"):
            inventory(path, self.archive)

    def test_runtime_definition_and_inventory_may_be_external_regular_files(self):
        with tempfile.TemporaryDirectory(prefix="alf-e2a-external-input-") as temporary:
            outside = Path(temporary)
            definition_file = outside / "definition.json"
            inventory_file = outside / "inventory.json"
            definition_file.write_text("{}\n", encoding="utf-8")
            inventory_file.write_text("{}\n", encoding="utf-8")
            self.assertEqual(
                _resolve_runtime_input(
                    ROOT,
                    definition_file,
                    require_inside_repository=False,
                    invalid_code="runtime_definition_file_invalid",
                ),
                definition_file.resolve(),
            )
            self.assertEqual(
                _resolve_runtime_input(
                    ROOT,
                    inventory_file,
                    require_inside_repository=False,
                    invalid_code="runtime_inventory_file_invalid",
                ),
                inventory_file.resolve(),
            )
            with self.assertRaisesRegex(E2aError, "runtime_definition_file_invalid"):
                _resolve_runtime_input(
                    ROOT,
                    outside,
                    require_inside_repository=False,
                    invalid_code="runtime_definition_file_invalid",
                )
            with self.assertRaisesRegex(E2aError, "runtime_e2_definition_file_invalid"):
                _resolve_runtime_input(
                    ROOT,
                    definition_file,
                    require_inside_repository=True,
                    invalid_code="runtime_e2_definition_file_invalid",
                )

    def test_form_derived_schedule_is_balanced_and_audit_bounded(self):
        schedule = build_schedule(self.inventory)
        self.assertEqual(schedule, self.definition["schedule"])
        catalog = {row["form_id"]: row for row in self.inventory["form_catalog"]}
        counts = Counter(
            (row["task_id"], row["form_id"], row["language"], row["audit_condition"])
            for row in schedule
        )
        for key, count in counts.items():
            self.assertEqual(count, 5, key)
            if key[3] == "audit_off":
                self.assertTrue(catalog[key[1]]["audit_eligible"])
        first = Counter(
            (row["task_id"], row["form_id"], row["audit_condition"], row["language"])
            for row in schedule if row["language_position"] == 1
        )
        self.assertTrue(all(value in {2, 3} for value in first.values()))

    def test_freeze_pins_accepted_e2_without_mutating_it(self):
        before = E2_DEFINITION_PATH.read_bytes()
        self.assertEqual(self.definition["schema_version"], DEFINITION_SCHEMA)
        self.assertTrue(check(self.definition, self.inventory, self.e2_definition)["ok"])
        self.assertEqual(before, E2_DEFINITION_PATH.read_bytes())
        tampered = copy.deepcopy(self.definition)
        tampered["accepted_e2"]["accepted_report_sha256"] = "0" * 64
        tampered["definition_sha256"] = canonical_json_hash({
            key: value for key, value in tampered.items() if key != "definition_sha256"
        })
        self.assertFalse(check(tampered, self.inventory)["ok"])

    def test_canonical_argv_preserves_flags_project_transport_and_audit(self):
        run_form = next(
            row for row in self.inventory["form_catalog"]
            if row["operation"] == "run" and row["project_mode"] == "option-project"
        )
        argv = canonical_argv(run_form, "OrderFlow.fsproj")
        self.assertEqual(argv[:4], ["dotnet", "run", "--project", "OrderFlow.fsproj"])
        eligible = next(row for row in self.inventory["form_catalog"] if row["audit_eligible"])
        self.assertIn("-p:NuGetAudit=false", canonical_argv(
            eligible, "OrderFlow.fsproj", audit_condition="audit_off"
        ))
        ignore_failed = next(
            row for row in self.inventory["form_catalog"]
            if "--ignore-failed-sources" in row["flags"]
        )
        self.assertIn(
            "--ignore-failed-sources",
            canonical_argv(ignore_failed, "OrderFlow.fsproj"),
        )
        ineligible = next(row for row in self.inventory["form_catalog"] if not row["audit_eligible"])
        with self.assertRaisesRegex(E2aError, "audit_control_ineligible"):
            canonical_argv(ineligible, "OrderFlow.fsproj", audit_condition="audit_off")
        self.assertEqual(audit_eligible(eligible), eligible["audit_eligible"])

    def test_environment_validation_is_fail_closed(self):
        observed = _environment()
        validate_environment(observed, self.definition)
        tampered = copy.deepcopy(observed)
        tampered["process"]["auth_present"] = True
        with self.assertRaisesRegex(E2aError, "environment_observation_mismatch"):
            validate_environment(tampered, self.definition)
        tampered = copy.deepcopy(observed)
        tampered["container_self_observation"]["cgroup_v2"]["pids_max"] = 512
        with self.assertRaisesRegex(E2aError, "environment_self_limits_invalid"):
            validate_environment(tampered, self.definition)

    def test_sample_environment_exactly_matches_v3_image_and_launch(self):
        home = Path("/external/work/sample/home")
        actual = _sample_environment(home, _environment())
        expected = {
            **PINNED_IMAGE_ENVIRONMENT,
            "HOME": str(home),
            "CODEX_HOME": str(home),
            "HTTP_PROXY": "http://172.30.0.1:43128",
            "HTTPS_PROXY": "http://172.30.0.1:43128",
            "NO_PROXY": "127.0.0.1,localhost",
        }
        self.assertEqual(actual, expected)
        for invented in ("LANG", "LC_ALL", "TZ", "TMPDIR", "E2A_SHA"):
            self.assertNotIn(invented, actual)
        tampered = _environment()
        tampered["container_self_observation"]["pinned_image_environment_exact"] = False
        with self.assertRaisesRegex(E2aError, "environment_self_safety_invalid"):
            validate_environment(tampered, self.definition)

    def test_runtime_state_check_needs_no_tokenizer(self):
        manifest = load_manifest(ROOT, MANIFEST_PATH)
        state = next(
            row for row in self.e2_definition["states"]
            if row["language"] == "csharp" and row["stage"] == 1
        )
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            _materialize(ROOT, manifest, "csharp", 1, workspace)
            observed = _runtime_source_snapshot(workspace, state)
        self.assertEqual(observed["source_tree_sha256"], state["source_tree_sha256"])

    def test_report_audit_and_tamper_detection(self):
        run_root = self.base / "synthetic-run"
        raw = run_root / "raw"
        _synthetic_raw(raw, self.definition, self.inventory)
        output_json = run_root / "report.json"
        output_markdown = run_root / "report.md"
        built = report(
            definition=self.definition,
            inventory_data=self.inventory,
            raw_output=raw,
            output_json=output_json,
            output_markdown=output_markdown,
        )
        self.assertEqual(built["schema_version"], REPORT_SCHEMA)
        self.assertIn("not subtracted", built["mechanical_tool_exposure_envelope"]["method"])
        self.assertEqual(len(built["samples"]), len(self.definition["schedule"]))
        audited = audit(
            definition=self.definition,
            inventory_data=self.inventory,
            report_data=built,
            raw_output=raw,
        )
        self.assertTrue(audited["ok"], audited["errors"])
        stream = next(raw.rglob("*.stdout.bin"))
        stream.write_bytes(b"tampered")
        audited = audit(
            definition=self.definition,
            inventory_data=self.inventory,
            report_data=built,
            raw_output=raw,
        )
        self.assertFalse(audited["ok"])
        self.assertIn("raw_inventory_disk_mismatch", audited["errors"])

    def test_derived_summary_float_drift_is_bounded_and_audit_rebuild_uses_it(self):
        run_root = self.base / "summary-comparison-run"
        raw = run_root / "raw"
        _synthetic_raw(raw, self.definition, self.inventory)
        built = report(
            definition=self.definition,
            inventory_data=self.inventory,
            raw_output=raw,
        )

        def mutate_summary_float(document, section):
            if section == "absolute_distributions":
                cell = document[section][0]["wall_seconds"]
            elif section == "paired_language_effects":
                cell = document[section][0]["csharp_wall_seconds"]
            elif section == "audit_contrasts":
                cell = document[section][0]["audit_on_wall_seconds"]
            else:
                cell = document[section]["by_configuration_and_language"][0]
                cell = {"value": cell["mechanical_tool_exposure_seconds"]}
            if section == "mechanical_tool_exposure_envelope":
                document[section]["by_configuration_and_language"][0][
                    "mechanical_tool_exposure_seconds"
                ] = math.nextafter(cell["value"], math.inf)
            else:
                cell["mean"] = math.nextafter(cell["mean"], math.inf)

        for section in (
            "absolute_distributions",
            "paired_language_effects",
            "audit_contrasts",
            "mechanical_tool_exposure_envelope",
        ):
            self.assertTrue(e2a_module._derived_json_equal(built[section], built[section]))

            tiny = copy.deepcopy(built)

            # Keep the fixture's known first float stable while exercising the
            # same recursive shape for every approved derived section.
            if section == "absolute_distributions":
                tiny[section][0]["wall_seconds"]["mean"] = math.nextafter(
                    tiny[section][0]["wall_seconds"]["mean"], math.inf
                )
                too_far = copy.deepcopy(built)
                too_far[section][0]["wall_seconds"]["mean"] += 1e-6
            elif section == "paired_language_effects":
                tiny[section][0]["csharp_wall_seconds"]["mean"] = math.nextafter(
                    tiny[section][0]["csharp_wall_seconds"]["mean"], math.inf
                )
                too_far = copy.deepcopy(built)
                too_far[section][0]["csharp_wall_seconds"]["mean"] += 1e-6
            elif section == "audit_contrasts":
                tiny[section][0]["audit_on_wall_seconds"]["mean"] = math.nextafter(
                    tiny[section][0]["audit_on_wall_seconds"]["mean"], math.inf
                )
                too_far = copy.deepcopy(built)
                too_far[section][0]["audit_on_wall_seconds"]["mean"] += 1e-6
            else:
                tiny[section]["by_configuration_and_language"][0][
                    "mechanical_tool_exposure_seconds"
                ] = math.nextafter(
                    tiny[section]["by_configuration_and_language"][0][
                        "mechanical_tool_exposure_seconds"
                    ], math.inf
                )
                too_far = copy.deepcopy(built)
                too_far[section]["by_configuration_and_language"][0][
                    "mechanical_tool_exposure_seconds"
                ] += 1e-6
            tiny.pop("report_sha256")
            self.assertTrue(validate_report(
                _finish_hash(tiny, "report_sha256"), self.definition, self.inventory
            )["ok"])
            too_far.pop("report_sha256")
            self.assertIn(
                f"report_{section.replace('mechanical_tool_exposure_envelope', 'exposure_envelope')}_mismatch",
                validate_report(
                    _finish_hash(too_far, "report_sha256"), self.definition, self.inventory
                )["errors"],
            )

        rebuilt = copy.deepcopy(built)
        rebuilt["absolute_distributions"][0]["wall_seconds"]["mean"] = math.nextafter(
            rebuilt["absolute_distributions"][0]["wall_seconds"]["mean"], math.inf
        )
        rebuilt.pop("report_sha256")
        rebuilt = _finish_hash(rebuilt, "report_sha256")
        with mock.patch.object(e2a_module, "_build_report", return_value=rebuilt):
            audited = audit(
                definition=self.definition,
                inventory_data=self.inventory,
                report_data=built,
                raw_output=raw,
            )
        self.assertTrue(audited["ok"], audited["errors"])

        for section in (
            "absolute_distributions",
            "paired_language_effects",
            "audit_contrasts",
            "mechanical_tool_exposure_envelope",
        ):
            rebuilt = copy.deepcopy(built)
            mutate_summary_float(rebuilt, section)
            rebuilt.pop("report_sha256")
            rebuilt = _finish_hash(rebuilt, "report_sha256")
            with mock.patch.object(e2a_module, "_build_report", return_value=rebuilt):
                audited = audit(
                    definition=self.definition,
                    inventory_data=self.inventory,
                    report_data=built,
                    raw_output=raw,
                )
            self.assertTrue(audited["ok"], (section, audited["errors"]))

        invalid_rebuilt = copy.deepcopy(rebuilt)
        invalid_rebuilt["report_sha256"] = "0" * 64
        with mock.patch.object(e2a_module, "_build_report", return_value=invalid_rebuilt):
            audited = audit(
                definition=self.definition,
                inventory_data=self.inventory,
                report_data=built,
                raw_output=raw,
            )
        self.assertFalse(audited["ok"])
        self.assertIn("report_differs_from_raw_recomputation", audited["errors"])

        sample_tampered = copy.deepcopy(built)
        sample_tampered["samples"][0]["wall_seconds"] = math.nextafter(
            sample_tampered["samples"][0]["wall_seconds"], math.inf
        )
        sample_tampered.pop("report_sha256")
        sample_tampered = _finish_hash(sample_tampered, "report_sha256")
        audited = audit(
            definition=self.definition,
            inventory_data=self.inventory,
            report_data=sample_tampered,
            raw_output=raw,
        )
        self.assertFalse(audited["ok"])
        self.assertIn("report_differs_from_raw_recomputation", audited["errors"])

    def test_derived_comparison_rejects_structure_types_nonfinite_and_sample_drift(self):
        self.assertFalse(e2a_module._derived_json_equal({"x": [1]}, {"x": [1, 2]}))
        self.assertFalse(e2a_module._derived_json_equal({"x": 1}, {"x": True}))
        self.assertFalse(e2a_module._derived_json_equal({"x": float("nan")}, {"x": 1.0}))
        self.assertFalse(e2a_module._derived_json_equal({"x": float("inf")}, {"x": 1.0}))
        self.assertFalse(e2a_module._json_equal_exact({"x": 1}, {"x": True}))

    def test_valid_rehash_structural_and_scalar_mutations_fail_validation(self):
        run_root = self.base / "summary-structure-run"
        raw = run_root / "raw"
        _synthetic_raw(raw, self.definition, self.inventory)
        built = report(
            definition=self.definition,
            inventory_data=self.inventory,
            raw_output=raw,
        )

        mutations = []
        string_mutation = copy.deepcopy(built)
        string_mutation["absolute_distributions"][0]["operation"] = "tampered"
        mutations.append(string_mutation)
        missing_key = copy.deepcopy(built)
        missing_key["absolute_distributions"][0].pop("operation")
        mutations.append(missing_key)
        extra_key = copy.deepcopy(built)
        extra_key["absolute_distributions"][0]["unexpected"] = 1
        mutations.append(extra_key)
        reordered = copy.deepcopy(built)
        reordered["absolute_distributions"][:2] = reordered["absolute_distributions"][1::-1]
        mutations.append(reordered)
        int_float = copy.deepcopy(built)
        int_float["absolute_distributions"][0]["wall_seconds"]["count"] = 5.0
        mutations.append(int_float)
        nonfinite = copy.deepcopy(built)
        nonfinite["absolute_distributions"][0]["wall_seconds"]["mean"] = float("nan")
        mutations.append(nonfinite)

        for mutated in mutations:
            mutated.pop("report_sha256")
            validated = validate_report(
                _finish_hash(mutated, "report_sha256"), self.definition, self.inventory
            )
            self.assertFalse(validated["ok"])

    def test_cli_has_complete_non_lambda_surface(self):
        parser = build_parser()
        common = {
            "inventory": ["--report", "e1.json", "--archive-root", "archive", "--output", "inventory.json"],
            "freeze": ["--inventory", "inventory.json", "--e2-definition", "e2.json", "--runner-git-sha", RUNNER_SHA, "--output", "definition.json"],
            "check": ["--definition", "definition.json", "--inventory", "inventory.json", "--e2-definition", "e2.json"],
            "run": ["--definition", "definition.json", "--inventory", "inventory.json", "--e2-definition", "e2.json", "--observed-environment", "env.json", "--runner-git-sha", RUNNER_SHA, "--work-root", "work", "--raw-output", "raw"],
            "report": ["--definition", "definition.json", "--inventory", "inventory.json", "--raw-output", "raw", "--output-json", "report.json", "--output-markdown", "report.md"],
            "audit": ["--definition", "definition.json", "--inventory", "inventory.json", "--report", "report.json", "--raw-output", "raw"],
        }
        for command, arguments in common.items():
            args = parser.parse_args(["e2a", command, *arguments])
            self.assertTrue(callable(args.func))
            self.assertNotEqual(getattr(args.func, "__name__", ""), "<lambda>")


if __name__ == "__main__":
    unittest.main()
