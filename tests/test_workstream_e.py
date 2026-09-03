import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import tiktoken

from alf.workstream_e import (
    COVERED_COMMAND_EQUIVALENCE_CLASSES,
    COVERED_EVENT_SHAPES,
    EXPECTED_ATTEMPTS,
    EXPECTED_TASK_IDS,
    FAMILY_ID,
    NULL_LEDGER,
    REPORT_TYPE,
    SERIALIZATION_VERSION,
    _canonical_raw_inventory,
    _commit_source_metrics,
    _git_diff_boundary,
    _operation_outcomes,
    _volume,
    analyze_archive,
    analyze_event_stream,
    classify_command,
    diagnostics,
    markdown_report,
    validate_public_report,
    write_report,
)
from alf.variance import _artifact_hashes, _hash, _source_tree


def command_item(command, *, item_id="cmd", exit_code=0, output="", event_type="item.completed"):
    return {
        "type": event_type,
        "item": {
            "id": item_id,
            "type": "command_execution",
            "command": command,
            "status": ("completed" if exit_code == 0 else "failed")
                      if event_type == "item.completed" else "in_progress",
            "exit_code": exit_code,
            "aggregated_output": output,
        },
    }


def file_item(path, *, item_id="patch", kind="update", event_type="item.completed"):
    return {
        "type": event_type,
        "item": {
            "id": item_id,
            "type": "file_change",
            "status": "completed" if event_type == "item.completed" else "in_progress",
            "changes": {"path": path, "kind": kind},
        },
    }


def _run_git(workspace, *args):
    return subprocess.run(["git", *args], cwd=workspace, check=True, capture_output=True,
                          text=True, encoding="utf-8").stdout.strip()


def _write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")


def _build_git_chain(root):
    workspace = root / "git-template"
    workspace.mkdir()
    _run_git(workspace, "init", "-q")
    _run_git(workspace, "config", "user.name", "Synthetic")
    _run_git(workspace, "config", "user.email", "synthetic@example.invalid")
    (workspace / "App.csproj").write_text("<Project />\n", encoding="utf-8")
    (workspace / "Program.cs").write_text("class Program {}\n", encoding="utf-8")
    _run_git(workspace, "add", ".")
    _run_git(workspace, "commit", "-q", "-m", "baseline")
    commits = [_run_git(workspace, "rev-parse", "HEAD")]
    for index, task_id in enumerate(EXPECTED_TASK_IDS, 1):
        with (workspace / "Program.cs").open("a", encoding="utf-8", newline="\n") as stream:
            stream.write(f"// stage {index}\n")
        _run_git(workspace, "add", "Program.cs")
        _run_git(workspace, "commit", "-q", "-m", task_id)
        commits.append(_run_git(workspace, "rev-parse", "HEAD"))
    return workspace, commits


def _command_fixture_cases():
    path = Path(__file__).parent / "fixtures" / "workstream-e" / "command-equivalence-classes.json"
    return json.loads(path.read_text(encoding="utf-8"))["cases"]


def _synthetic_events(index, usage):
    events = [
        {"type": "thread.started", "thread_id": f"thread-{index}"},
        {"type": "turn.started"},
        file_item("/workspace/Program.cs", item_id=f"patch-{index}", event_type="item.started"),
        file_item("/workspace/Program.cs", item_id=f"patch-{index}"),
    ]
    for ordinal, case in enumerate(_command_fixture_cases(), 1):
        item_id = f"cmd-{index}-{ordinal}"
        events.extend([
            command_item(case["command"], item_id=item_id, event_type="item.started"),
            command_item(case["command"], item_id=item_id),
        ])
    events.extend([
        {"type": "item.completed", "item": {"id": f"msg-{index}", "type": "agent_message", "text": "done"}},
        {"type": "item.started", "item": {"id": f"todo-{index}", "type": "todo_list", "items": []}},
        {"type": "item.updated", "item": {"id": f"todo-{index}", "type": "todo_list", "items": []}},
        {"type": "item.completed", "item": {"id": f"todo-{index}", "type": "todo_list", "items": []}},
        {"type": "turn.completed", "usage": {key: value for key, value in usage.items() if key != "tool_calls"}},
    ])
    return events


def _make_archive(root):
    template, commits = _build_git_chain(root)
    repositories = [_commit_source_metrics(template, commit)["repository"] for commit in commits]
    diffs = [_git_diff_boundary(template, commits[index - 1], commits[index])["metrics"]
             for index in range(1, len(commits))]
    archive = root / "archive"
    command_count = len(_command_fixture_cases())
    attempts = []
    for config, attempt_ids in EXPECTED_ATTEMPTS.items():
        for attempt_id in sorted(attempt_ids):
            run = archive / config / attempt_id
            shutil.copytree(template, run / "workspace")
            (run / "tasks").mkdir(parents=True)
            language = "csharp" if "csharp" in attempt_id else "fsharp"
            reasoning = "high" if config == "m" else "medium"
            model = "gpt-5.6-terra" if config == "h" else "gpt-5.6-luna"
            order = "csharp-first" if "reverse" in attempt_id else "fsharp-first"
            position = 1 if language == order.split("-")[0] else 2
            tasks = []
            aggregate = {"input_tokens": 0, "cached_input_tokens": 0, "cache_write_input_tokens": 0,
                         "output_tokens": 0, "reasoning_output_tokens": 0, "tool_calls": 0}
            for index, task_id in enumerate(EXPECTED_TASK_IDS, 1):
                usage = {"input_tokens": 10, "cached_input_tokens": 2, "cache_write_input_tokens": 0,
                         "output_tokens": 3, "reasoning_output_tokens": 1,
                         "tool_calls": command_count + 1}
                for key, value in usage.items():
                    aggregate[key] += value
                events = _synthetic_events(index, usage)
                task_dir = run / "tasks" / task_id
                task_dir.mkdir()
                jsonl = "\n".join(json.dumps(event, sort_keys=True) for event in events) + "\n"
                (task_dir / "events.jsonl").write_text(jsonl, encoding="utf-8")
                (task_dir / "agent.stdout").write_text(jsonl, encoding="utf-8")
                (task_dir / "agent.stderr").write_text("", encoding="utf-8")
                before = repositories[index - 1]
                after = repositories[index]
                diff = diffs[index - 1]
                agent = {
                    "accounting_errors": [], "accounting_valid": True, "usage_available": True,
                    "ok": True, "event_count": len(events), "command_count": command_count,
                    "file_change_count": 1, "failed_event_count": 0, "file_reads": 0,
                    "unique_file_reads": 0, "file_revisits": 0, "usage_record_count": 1,
                    "agent_process_wall_seconds": 1.0, "usage": usage,
                }
                task = {
                    "task_id": task_id, "pre_commit": commits[index - 1], "post_commit": commits[index],
                    "agent": agent, "evaluation": {"ok": True, "evaluator_wall_seconds": 0.5},
                    "repository_before": before, "repository_after": after, "diff": diff,
                    "success": True, "task_total_wall_seconds": 1.5,
                }
                sidecar = {**usage, "derived_from_codex_jsonl": True, "usage_errors": [],
                           "accounting_valid": True, "usage_available": True, "event_count": len(events),
                           "command_count": command_count, "file_change_count": 1, "failed_event_count": 0,
                           "file_reads": 0, "unique_file_reads": 0, "file_revisits": 0,
                           "usage_record_count": 1}
                _write_json(task_dir / "usage.json", sidecar)
                _write_json(task_dir / "task-result.json", task)
                tasks.append(task)
            result = {
                "agent": "codex", "require_usage": False, "run_id": attempt_id,
                "language": language, "requested_model": model, "success": True,
                "provenance": {"attempt_id": attempt_id, "configuration_id": config.upper(),
                               "reasoning_effort": reasoning, "order": order, "position": position},
                "tasks": tasks, "aggregate_usage": aggregate, "aggregate_usage_available": True,
                "aggregate_accounting_valid": True, "agent_process_wall_seconds": 8.0,
                "evaluator_wall_seconds": 4.0, "run_total_wall_seconds": 12.0,
            }
            _write_json(run / "result.json", result)
            _write_json(run / "attempt.json", {"attempt_id": attempt_id})
            _write_json(run / "protocol-manifest.json", {"family_id": FAMILY_ID})
            artifacts = _artifact_hashes(run, run.parent)
            source = _source_tree(run)
            inventory = _canonical_raw_inventory(run, run.parent)
            attempts.append({
                "attempt_id": attempt_id, "configuration_id": config.upper(), "language": language,
                "model": model, "reasoning_effort": reasoning, "order": order, "position": position,
                "task_count": 8, "successful_tasks": 8, "success": True,
                "result_sha256": inventory["files"][next(i for i, row in enumerate(inventory["files"])
                                                           if row["path"].endswith("/result.json"))]["sha256"],
                "raw_inventory": {key: inventory[key] for key in ("file_count", "bytes", "tree_sha256")},
                "artifact_hashes": {"file_count": len(artifacts["files"]), "set_sha256": artifacts["set_sha256"]},
                "source_tree": {"file_count": source["file_count"], "tree_sha256": source["tree_sha256"]},
                "audit": {"ok": True, "errors": []},
            })
    report = {"report_type": REPORT_TYPE, "family_id": FAMILY_ID, "attempts": attempts}
    report["report_sha256"] = _hash(report)
    report_path = root / "calibration.json"
    _write_json(report_path, report)
    return archive, report_path


class WorkstreamEClassifyTests(unittest.TestCase):
    def test_requires_exact_linux_bash_lc_wrapper(self):
        for shell in ("bash", "/bin/bash", "/usr/bin/bash"):
            self.assertEqual(classify_command(f'{shell} -lc "dotnet build App"')["labels"], ["build"])
        for command in ("sh -lc 'dotnet build App'", "bash -c 'dotnet build App'",
                        "bash -lc 'dotnet build App' extra", None):
            got = classify_command(command)
            self.assertTrue(got["ambiguous_or_unparsed"])
            self.assertEqual(got["disposition"], "unparsed")
            self.assertEqual(got["labels"], [])

    def test_preserves_connectors_and_ignores_quoted_connectors(self):
        got = classify_command("/bin/bash -lc 'rg \"a|b; c\" src && dotnet build App || true'")
        self.assertEqual(got["connectors"], ["and_if", "or_if"])
        self.assertEqual(got["labels"], ["build", "other", "search"])
        self.assertEqual([op["operation_ordinal"] for op in got["operations"]], [1, 2, 3])
        self.assertEqual([op["connector_before"] for op in got["operations"]], [None, "and_if", "or_if"])

    def test_bounded_multilabel_restore_build_run_and_redirections(self):
        mixed = classify_command("bash -lc 'dotnet restore App | dotnet build App | dotnet run --project App'")
        self.assertEqual(mixed["labels"], ["build", "project_configuration", "test_or_run"])
        self.assertEqual(mixed["connectors"], ["pipeline", "pipeline"])
        write = classify_command("bash -lc 'printf value >> src/A.fs'")
        self.assertEqual(write["labels"], ["edit"])
        self.assertTrue(write["operations"][0]["redirection"]["append_output"])
        read = classify_command("bash -lc 'sed -n 1p src/A.fs < input.txt; rg name src\nls src'")
        self.assertEqual(read["connectors"], ["sequence", "newline"])
        self.assertTrue(read["operations"][0]["redirection"]["has_input"])

    def test_quoted_json_is_argument_not_an_embedded_command(self):
        got = classify_command("bash -lc 'echo \"{\\\"command\\\":\\\"dotnet build App\\\"}\"'")
        self.assertEqual(got["labels"], ["other"])
        self.assertNotIn("build", got["labels"])

    def test_unsupported_constructs_are_explicitly_ambiguous(self):
        cases = {
            "bash -lc \"cat > x <<'EOF'\nvalue\nEOF\"": "heredoc",
            "bash -lc 'echo $(pwd)'": "command_substitution",
            "bash -lc 'echo `pwd`'": "backtick_substitution",
            "bash -lc '(dotnet build App)'": "unsupported_parentheses",
            "bash -lc 'echo \"oops'": "unbalanced_quote",
        }
        for command, reason in cases.items():
            with self.subTest(reason=reason):
                got = classify_command(command)
                self.assertTrue(got["ambiguous_or_unparsed"])
                self.assertIn(reason, got["ambiguity_reasons"])


class WorkstreamEOutcomeTests(unittest.TestCase):
    def outcomes(self, command, exit_code, output=""):
        classified = classify_command(command)
        status = "completed" if exit_code == 0 else "failed"
        return [row["value"] for row in _operation_outcomes(classified, exit_code, output, status)]

    def test_atomic_and_successful_and_chain_outcomes(self):
        no_output = _operation_outcomes(
            classify_command("bash -lc 'dotnet build App'"), 0, "", "completed",
        )[0]
        self.assertIsNone(no_output["value"])
        self.assertEqual(no_output["reason"], "zero_error_evidence_unavailable")
        self.assertEqual(self.outcomes("bash -lc 'dotnet build App'", 0, "Build succeeded.\n"), ["success"])
        self.assertEqual(self.outcomes("bash -lc 'dotnet build App'", 1), ["failure"])
        self.assertEqual(
            self.outcomes("bash -lc 'dotnet restore App && dotnet build App && dotnet run'", 0),
            ["success", None, "success"],
        )
        and_chain = _operation_outcomes(
            classify_command("bash -lc 'dotnet restore App && dotnet build App && dotnet run'"),
            0, "", "completed",
        )
        self.assertEqual(and_chain[1]["reason"], "zero_error_evidence_unavailable")
        self.assertEqual(
            self.outcomes("bash -lc 'dotnet restore App && dotnet build App && dotnet run'", 0,
                          "Build succeeded.\n    0 Error(s)\n"),
            ["success", "success", "success"],
        )
        self.assertEqual(self.outcomes("bash -lc 'dotnet restore App && dotnet build App'", 1), [None, None])

    def test_pipeline_exit_only_belongs_to_terminal_atom(self):
        self.assertEqual(self.outcomes("bash -lc 'dotnet build App | dotnet run'", 1), [None, "failure"])
        self.assertEqual(self.outcomes("bash -lc 'dotnet build App; true'", 0), [None, "success"])

    def test_or_true_does_not_convert_preceding_failure_to_success(self):
        self.assertEqual(self.outcomes("bash -lc 'dotnet build App || true'", 0), [None, None])

    def test_anchored_build_evidence_requires_shell_success_attribution(self):
        self.assertEqual(
            self.outcomes("bash -lc 'dotnet build App || true'", 0, "Build FAILED.\n    1 Error(s)\n"),
            ["failure", None],
        )
        self.assertEqual(
            self.outcomes("bash -lc 'dotnet build App && dotnet run'", 1, "Build succeeded.\n    0 Error(s)\n"),
            [None, None],
        )
        self.assertEqual(
            self.outcomes("bash -lc 'dotnet build App || true'", 0, "Build succeeded.\n    0 Error(s)\n"),
            [None, None],
        )
        conflict = _operation_outcomes(
            classify_command("bash -lc 'dotnet build App'"), 0,
            "Build succeeded.\nBuild FAILED.\n", "completed",
        )[0]
        self.assertIsNone(conflict["value"])
        self.assertEqual(conflict["reason"], "conflicting_exit_and_build_evidence")
        exit_conflict = _operation_outcomes(
            classify_command("bash -lc 'dotnet build App'"), 1,
            "Build succeeded.\n    0 Error(s)\n", "failed",
        )[0]
        self.assertIsNone(exit_conflict["value"])
        self.assertEqual(exit_conflict["reason"], "conflicting_exit_and_build_evidence")


class WorkstreamEDiagnosticTests(unittest.TestCase):
    def test_exact_mapping_raw_counts_and_dedup_without_messages(self):
        lines = [
            "/workspace/src/A.fs(1, 2): error FS0058: sample detail",
            "/workspace/src/A.fs(1, 2): error FS0058: sample   detail",
            "src/B.fs(3): warning FS0001: another detail",
            "App.cs(4): error CS9999: unknown detail",
            "error NETSDK1064: restore detail",
        ]
        got = diagnostics("\r\n".join(lines))
        self.assertEqual(got["occurrence_count"], 5)
        self.assertEqual(len(got["instances"]), 4)
        self.assertEqual(got["counts_by_category"]["parse-indentation"], 2)
        self.assertEqual(got["counts_by_category"]["type-inference-record"], 1)
        self.assertEqual(got["counts_by_category"]["dependency-restore"], 1)
        self.assertEqual(got["counts_by_category"]["unclassified"], 1)
        self.assertEqual(next(row for row in got["instances"] if row["code"] == "FS0058")["file"], "src/A.fs")
        self.assertNotIn("sample detail", str(got))
        self.assertNotIn("unknown detail", str(got))

    def test_only_registered_codes_have_specific_categories(self):
        got = diagnostics("A.cs(2): error CS1002: detail")
        self.assertEqual(got["instances"][0]["category"], "unclassified")


class WorkstreamEVolumeTests(unittest.TestCase):
    def test_lf_normalized_utf8_and_pinned_tokenizer(self):
        got = _volume("alpha\r\nbeta\r")
        canonical = "alpha\nbeta\n"
        self.assertEqual(got["serialization_version"], SERIALIZATION_VERSION)
        self.assertEqual(got["bytes"], len(canonical.encode("utf-8")))
        self.assertEqual(got["lines"], 2)
        self.assertEqual(got["o200k_proxy_tokens"], len(tiktoken.get_encoding("o200k_base").encode(canonical)))


class WorkstreamERedactedFixtureTests(unittest.TestCase):
    def test_synthetic_fixture_cases_execute_and_exactly_cover_catalogs(self):
        fixture_root = Path(__file__).parent / "fixtures" / "workstream-e"
        events = json.loads((fixture_root / "event-shapes.json").read_text(encoding="utf-8"))
        commands = json.loads((fixture_root / "command-equivalence-classes.json").read_text(encoding="utf-8"))
        self.assertEqual({case["fixture_id"] for case in events["cases"]}, set(COVERED_EVENT_SHAPES))
        self.assertEqual({case["fixture_id"] for case in commands["cases"]},
                         set(COVERED_COMMAND_EQUIVALENCE_CLASSES))
        for case in events["cases"]:
            with self.subTest(event=case["fixture_id"]):
                got = analyze_event_stream([case["event"]])
                self.assertEqual(got["event_shape_counts"], {case["expected_shape_key"]: 1})
        for case in commands["cases"]:
            with self.subTest(command=case["fixture_id"]):
                got = classify_command(case["command"])
                self.assertEqual(got["equivalence_classes"], case["expected_equivalence_classes"])
                self.assertEqual(got["labels"], case["selected_labels"])
                self.assertEqual(got["ambiguous_or_unparsed"], case["ambiguous"])
                for alternate in case.get("alternate_cases", []):
                    alternate_got = classify_command(alternate["command"])
                    self.assertEqual(alternate_got["equivalence_classes"],
                                     alternate["expected_equivalence_classes"])
                    self.assertTrue(alternate_got["ambiguous_or_unparsed"])
        serialized = json.dumps([events, commands])
        self.assertNotIn("/workspace/", serialized)
        self.assertNotIn("workstream-d-language-v3", serialized)

    def test_uncovered_event_shape_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "event_shape_uncovered"):
            analyze_event_stream([{"type": "item.updated", "item": {"type": "file_change"}}])
        with self.assertRaisesRegex(ValueError, "command_equivalence_class_uncovered"):
            analyze_event_stream([command_item("sh -lc 'true'")])


class WorkstreamEEventAndStateTests(unittest.TestCase):
    def test_all_event_item_shapes_absolute_ordinals_and_dedup(self):
        events = [
            {"type": "thread.started", "thread_id": "private"},
            {"type": "turn.started"},
            command_item("bash -lc 'rg name src'", event_type="item.started"),
            command_item("bash -lc 'rg name src'", output="result"),
            command_item("bash -lc 'rg name src'", output="duplicate"),
            file_item("/workspace/App.fsproj", event_type="item.started"),
            file_item("/workspace/App.fsproj", kind="update"),
            {"type": "item.completed", "item": {"id": "msg", "type": "agent_message", "text": "private"}},
            {"type": "item.started", "item": {"id": "todo", "type": "todo_list", "items": []}},
            {"type": "item.updated", "item": {"id": "todo", "type": "todo_list", "items": []}},
            {"type": "item.completed", "item": {"id": "todo", "type": "todo_list", "items": []}},
            {"type": "turn.completed", "usage": {}},
        ]
        got = analyze_event_stream(events)
        self.assertEqual(got["commands"][0]["event_ordinal"], 4)
        self.assertEqual(len(got["commands"]), 1)
        self.assertEqual(got["event_shape_counts"]["item.completed:command_execution"], 2)
        self.assertEqual(got["completed_item_counts"]["todo_list"], 1)
        self.assertEqual(got["mutations"][0]["path"], "App.fsproj")
        self.assertEqual(got["mutations"][0]["labels"], ["edit", "project_configuration"])
        self.assertEqual(got["project_file_mutation_count"], 1)
        self.assertNotIn("private", str(got))
        self.assertNotIn("result", str(got))

    def test_pre_edit_first_post_later_build_and_repair_cycles(self):
        events = [
            command_item("bash -lc 'dotnet build App'", item_id="pre"),
            file_item("/workspace/src/A.fs", item_id="p1"),
            command_item("bash -lc 'dotnet build App'", item_id="b1", exit_code=1),
            file_item("/workspace/src/A.fs", item_id="p2"),
            command_item("bash -lc 'dotnet build App'", item_id="b2", exit_code=1),
            file_item("/workspace/src/A.fs", item_id="p3"),
            command_item("bash -lc 'dotnet build App'", item_id="b3", exit_code=0),
            command_item("bash -lc 'dotnet test App'", item_id="t1", exit_code=1),
            file_item("/workspace/src/A.fs", item_id="p4"),
            command_item("bash -lc 'dotnet test App'", item_id="t2", exit_code=0),
        ]
        state = analyze_event_stream(events)["build_state"]
        self.assertEqual(state["pre_edit_builds"][0]["event_ordinal"], 1)
        self.assertEqual(state["first_post_edit_candidate_build"]["event_ordinal"], 3)
        self.assertEqual(state["first_post_edit_candidate_build"]["outcome"]["value"], "failure")
        self.assertEqual([row["event_ordinal"] for row in state["later_builds"]], [5, 7])
        self.assertEqual(len(state["repair_cycles"]), 3)
        self.assertTrue(state["repair_cycles"][0]["reopened"])
        self.assertFalse(state["repair_cycles"][1]["reopened"])
        self.assertEqual(state["repair_cycles"][2]["failure_operation_class"], "test_or_run")

    def test_repair_cycle_closes_on_next_recognized_operation_regardless_of_class(self):
        events = [
            command_item("bash -lc 'dotnet build App'", item_id="failed-build", exit_code=1),
            file_item("/workspace/src/A.fs", item_id="repair"),
            command_item("bash -lc 'dotnet test App'", item_id="test"),
            command_item("bash -lc 'dotnet build App'", item_id="later-build", exit_code=1),
        ]
        cycles = analyze_event_stream(events)["build_state"]["repair_cycles"]
        self.assertEqual(len(cycles), 1)
        self.assertEqual(cycles[0]["failure_operation_class"], "build")
        self.assertEqual(cycles[0]["retry_operation_class"], "test_or_run")
        self.assertEqual(cycles[0]["retry"]["event_ordinal"], 3)
        self.assertFalse(cycles[0]["reopened"])

    def test_ambiguous_first_post_build_has_explicit_null_outcome(self):
        events = [
            file_item("/workspace/src/A.fs"),
            command_item("bash -lc 'dotnet build App && false'", item_id="amb", exit_code=1),
        ]
        first = analyze_event_stream(events)["build_state"]["first_post_edit_candidate_build"]
        self.assertIsNone(first["outcome"]["value"])
        self.assertEqual(first["outcome"]["reason"], "compound_outer_exit_not_attributable")

    def test_builds_without_a_mutation_are_pre_edit_only(self):
        state = analyze_event_stream([
            command_item("bash -lc 'dotnet build App'", item_id="only")
        ])["build_state"]
        self.assertEqual(len(state["pre_edit_builds"]), 1)
        self.assertIsNone(state["first_post_edit_candidate_build"]["value"])
        self.assertEqual(state["first_post_edit_candidate_build"]["reason"], "no_completed_mutation")

    def test_candidate_diagnostics_do_not_come_from_evaluator_fields(self):
        events = [command_item("bash -lc 'dotnet build App'", output="A.fs(1): error FS0039: hidden detail", exit_code=1)]
        task = {"task_id": "synthetic", "agent": {"ok": True},
                "evaluation": {"ok": False, "stderr_tail": "B.cs(2): error CS9999: evaluator detail"}}
        got = analyze_event_stream(events, task)
        self.assertEqual(got["diagnostics"]["counts_by_code"], {"FS0039": 1})
        self.assertFalse(got["evaluator"]["outcome"])
        self.assertNotIn("evaluator detail", str(got))


class WorkstreamEVerifierTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._temp = tempfile.TemporaryDirectory()
        cls.root = Path(cls._temp.name)
        cls.archive, cls.report = _make_archive(cls.root)
        cls.valid_report = analyze_archive(cls.report, cls.archive, "A" * 40)

    @classmethod
    def tearDownClass(cls):
        cls._temp.cleanup()

    def test_raw_inventory_source_proxy_and_boundary_conventions(self):
        attempt = sorted(EXPECTED_ATTEMPTS["h"])[0]
        run = self.archive / "h" / attempt
        report = json.loads(self.report.read_text(encoding="utf-8"))
        declared = next(row for row in report["attempts"] if row["attempt_id"] == attempt)
        inventory = _canonical_raw_inventory(run, run.parent)
        self.assertEqual({key: inventory[key] for key in ("file_count", "bytes", "tree_sha256")},
                         declared["raw_inventory"])
        result = json.loads((run / "result.json").read_text(encoding="utf-8"))
        task = result["tasks"][0]
        source = _commit_source_metrics(run / "workspace", task["pre_commit"])
        self.assertEqual(source["repository"], task["repository_before"])
        self.assertEqual(source["source_proxy"]["serialization_version"], SERIALIZATION_VERSION)
        self.assertEqual(_git_diff_boundary(run / "workspace", task["pre_commit"], task["post_commit"])["metrics"],
                         task["diff"])

    def test_end_to_end_ten_attempt_eighty_task_verifier(self):
        got = self.valid_report
        self.assertEqual(got["totals"], {"run_count": 10, "task_count": 80})
        self.assertEqual(got["inputs"]["analyzer_git_sha"], "a" * 40)
        self.assertEqual(len(got["runs"]), 10)
        self.assertEqual(len(got["task_index"]), 80)
        self.assertNotIn("tasks", got)
        self.assertEqual(got["coverage"]["unobserved_event_shapes"], [])
        self.assertEqual(got["coverage"]["unobserved_command_equivalence_classes"], [])
        self.assertEqual(got["coverage"]["outside_catalog_event_shapes"], [])
        self.assertEqual(got["coverage"]["outside_catalog_command_equivalence_classes"], [])
        repeated = analyze_archive(self.report, self.archive, "A" * 40)
        self.assertEqual(json.dumps(got, sort_keys=True), json.dumps(repeated, sort_keys=True))
        unsigned = dict(got)
        unsigned.pop("report_sha256")
        self.assertEqual(got["report_sha256"], _hash(unsigned))

    def test_public_aggregates_signatures_and_missingness_are_complete(self):
        got = self.valid_report
        self.assertEqual(set(got["missingness"]), set(NULL_LEDGER))
        self.assertTrue(all(value == {"value": None, "reason": NULL_LEDGER[key]}
                            for key, value in got["missingness"].items()))
        self.assertEqual(len(got["aggregates"]["by_configuration_and_language"]), 6)
        self.assertEqual(len(got["attribution_signatures"]), 6)
        self.assertIn("overall", got["aggregates"])
        self.assertIn("recorded_output_volume", got["aggregates"]["overall"])
        for run in got["runs"]:
            self.assertEqual(set(run["missingness"]), set(NULL_LEDGER))
            for task in run["tasks"]:
                self.assertEqual(set(task["missingness"]), set(NULL_LEDGER))

    def test_public_privacy_validator_rejects_raw_keys_paths_and_bad_hash(self):
        validate_public_report(self.valid_report)
        forbidden = json.loads(json.dumps(self.valid_report))
        forbidden["runs"][0]["tasks"][0]["command"] = "raw"
        with self.assertRaisesRegex(ValueError, "public_report_forbidden_key"):
            validate_public_report(forbidden)
        absolute = json.loads(json.dumps(self.valid_report))
        absolute["runs"][0]["tasks"][0]["boundary"]["changed_paths"][0]["path"] = "C:\\private\\file"
        with self.assertRaisesRegex(ValueError, "public_report_absolute_path"):
            validate_public_report(absolute)
        invalid_hash = json.loads(json.dumps(self.valid_report))
        invalid_hash["totals"]["task_count"] = 79
        with self.assertRaisesRegex(ValueError, "public_report_hash_invalid"):
            validate_public_report(invalid_hash)

    def test_markdown_and_atomic_writer_are_deterministic_and_transcript_free(self):
        first = markdown_report(self.valid_report)
        second = markdown_report(self.valid_report)
        self.assertEqual(first, second)
        for heading in ("## Integrity and provenance", "## Observability and missingness",
                        "## Descriptive measures by configuration and language",
                        "## Attribution-signature routing", "## Evidence and claim limits"):
            self.assertIn(heading, first)
        self.assertNotIn("thread-", first)
        self.assertNotIn("Build succeeded", first)
        with tempfile.TemporaryDirectory() as directory:
            json_path, markdown_path = Path(directory) / "report.json", Path(directory) / "report.md"
            write_report(self.valid_report, json_path, markdown_path)
            original = (json_path.read_bytes(), markdown_path.read_bytes())
            write_report(self.valid_report, json_path, markdown_path)
            self.assertEqual(original, (json_path.read_bytes(), markdown_path.read_bytes()))
            invalid = json.loads(json.dumps(self.valid_report))
            invalid["report_sha256"] = "0" * 64
            bad_json, bad_markdown = Path(directory) / "bad.json", Path(directory) / "bad.md"
            with self.assertRaisesRegex(ValueError, "public_report_hash_invalid"):
                write_report(invalid, bad_json, bad_markdown)
            self.assertFalse(bad_json.exists())
            self.assertFalse(bad_markdown.exists())

    def test_calibration_and_archive_roster_fail_closed(self):
        changed = json.loads(self.report.read_text(encoding="utf-8"))
        changed["family_id"] = "changed"
        bad_report = self.root / "bad-self-hash.json"
        _write_json(bad_report, changed)
        with self.assertRaisesRegex(ValueError, "calibration_self_hash_mismatch"):
            analyze_archive(bad_report, self.archive, "0" * 40)
        with tempfile.TemporaryDirectory() as directory:
            copied = Path(directory) / "archive"
            shutil.copytree(self.archive, copied)
            (copied / "extra").mkdir()
            with self.assertRaisesRegex(ValueError, "archive_configuration_roster_mismatch"):
                analyze_archive(self.report, copied, "0" * 40)
        missing = self.archive / "h" / sorted(EXPECTED_ATTEMPTS["h"])[0]
        hidden = missing.with_name(missing.name + ".missing")
        missing.rename(hidden)
        try:
            with self.assertRaisesRegex(ValueError, "archive_attempt_roster_mismatch"):
                analyze_archive(self.report, self.archive, "0" * 40)
        finally:
            hidden.rename(missing)
        extra_attempt = self.archive / "h" / "extra-attempt"
        extra_attempt.mkdir()
        try:
            with self.assertRaisesRegex(ValueError, "archive_attempt_roster_mismatch"):
                analyze_archive(self.report, self.archive, "0" * 40)
        finally:
            extra_attempt.rmdir()

    def test_result_inventory_artifact_and_source_identity_fail_closed(self):
        from alf.workstream_e import _read_object
        real_read = _read_object

        def wrong_result_hash(path, *codes):
            value, identity = real_read(path, *codes)
            return value, "0" * 64 if path.name == "result.json" else identity

        with patch("alf.workstream_e._read_object", side_effect=wrong_result_hash):
            with self.assertRaisesRegex(ValueError, "result_sha256_mismatch"):
                analyze_archive(self.report, self.archive, "0" * 40)
        with patch("alf.workstream_e._canonical_raw_inventory",
                   return_value={"files": [], "file_count": 0, "bytes": 0, "tree_sha256": "0" * 64}):
            with self.assertRaisesRegex(ValueError, "raw_inventory_mismatch"):
                analyze_archive(self.report, self.archive, "0" * 40)
        real_inventory = _canonical_raw_inventory
        with patch("alf.workstream_e._canonical_raw_inventory", side_effect=real_inventory), \
             patch("alf.workstream_e._artifact_hashes", return_value={"files": [], "set_sha256": "0" * 64}):
            with self.assertRaisesRegex(ValueError, "artifact_identity_mismatch"):
                analyze_archive(self.report, self.archive, "0" * 40)
        with patch("alf.workstream_e._source_tree", return_value={"files": [], "file_count": 0,
                                                                   "tree_sha256": "0" * 64}):
            with self.assertRaisesRegex(ValueError, "source_tree_identity_mismatch"):
                analyze_archive(self.report, self.archive, "0" * 40)

    def test_task_event_usage_envelope_and_audit_failures_have_codes(self):
        attempt = sorted(EXPECTED_ATTEMPTS["h"])[0]
        result = json.loads((self.archive / "h" / attempt / "result.json").read_text(encoding="utf-8"))
        with patch("alf.workstream_e._read_events", side_effect=ValueError("events_invalid_json")):
            with self.assertRaisesRegex(ValueError, "events_invalid_json"):
                analyze_archive(self.report, self.archive, "0" * 40)
        altered = json.loads(json.dumps(result))
        altered["tasks"][0]["agent"]["usage"]["input_tokens"] += 1
        with self.assertRaisesRegex(ValueError, "task_envelope_mismatch"):
            from alf.workstream_e import _verify_task_envelopes
            _verify_task_envelopes(self.archive / "h" / attempt, altered)
        task_root = self.archive / "h" / attempt / "tasks"
        missing = task_root / EXPECTED_TASK_IDS[-1]
        hidden = task_root / (EXPECTED_TASK_IDS[-1] + ".missing")
        missing.rename(hidden)
        try:
            with self.assertRaisesRegex(ValueError, "task_directory_roster_mismatch"):
                _verify_task_envelopes(self.archive / "h" / attempt, result)
        finally:
            hidden.rename(missing)
        extra_task = task_root / "extra-task"
        extra_task.mkdir()
        try:
            with self.assertRaisesRegex(ValueError, "task_directory_roster_mismatch"):
                _verify_task_envelopes(self.archive / "h" / attempt, result)
        finally:
            extra_task.rmdir()
        with tempfile.TemporaryDirectory() as directory:
            invalid_events = Path(directory) / "events.jsonl"
            invalid_events.write_text("not-json\n", encoding="utf-8")
            from alf.workstream_e import _read_events
            with self.assertRaisesRegex(ValueError, "events_invalid_json"):
                _read_events(invalid_events)
        usage_path = task_root / EXPECTED_TASK_IDS[0] / "usage.json"
        hidden_usage = usage_path.with_suffix(".missing")
        usage_path.rename(hidden_usage)
        try:
            with self.assertRaisesRegex(ValueError, "usage_sidecar_missing"):
                _verify_task_envelopes(self.archive / "h" / attempt, result)
        finally:
            hidden_usage.rename(usage_path)
        with patch("alf.workstream_e.audit_run", return_value={"ok": False, "errors": ["redacted"]}):
            with self.assertRaisesRegex(ValueError, "audit_failed"):
                analyze_archive(self.report, self.archive, "0" * 40)

    def test_boundary_diff_source_and_changed_path_fail_closed(self):
        attempt = sorted(EXPECTED_ATTEMPTS["h"])[0]
        run = self.archive / "h" / attempt
        result = json.loads((run / "result.json").read_text(encoding="utf-8"))
        events = [json.loads(line) for line in
                  (run / "tasks" / EXPECTED_TASK_IDS[0] / "events.jsonl").read_text(encoding="utf-8").splitlines()]
        analyses = [analyze_event_stream(events, result["tasks"][0])] * 8
        from alf.workstream_e import _verify_boundaries
        bad_diff = json.loads(json.dumps(result["tasks"]))
        bad_diff[0]["diff"]["added_lines"] += 1
        with self.assertRaisesRegex(ValueError, "boundary_diff_metrics_mismatch"):
            _verify_boundaries(run, bad_diff, analyses)
        bad_source = json.loads(json.dumps(result["tasks"]))
        bad_source[0]["repository_before"]["source_bytes"] += 1
        with self.assertRaisesRegex(ValueError, "repository_before_mismatch"):
            _verify_boundaries(run, bad_source, analyses)
        bad_chain = json.loads(json.dumps(result["tasks"]))
        bad_chain[1]["pre_commit"] = bad_chain[0]["pre_commit"]
        with self.assertRaisesRegex(ValueError, "boundary_chain_mismatch"):
            _verify_boundaries(run, bad_chain, analyses)
        wrong_path_events = json.loads(json.dumps(events))
        for event in wrong_path_events:
            if event.get("type") == "item.completed" and event.get("item", {}).get("type") == "file_change":
                event["item"]["changes"]["path"] = "/workspace/Other.cs"
        wrong_analysis = analyze_event_stream(wrong_path_events, result["tasks"][0])
        with self.assertRaisesRegex(ValueError, "boundary_file_change_path_mismatch"):
            _verify_boundaries(run, result["tasks"], [wrong_analysis] + analyses[1:])


if __name__ == "__main__":
    unittest.main()
