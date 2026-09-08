"""Finite E3a batch/report orchestration. No implicit model, retry, or remote service."""
from __future__ import annotations

import copy
import json
import os
import time
from pathlib import Path
from typing import Callable

from .e3a_codex import CodexOAuthAdapter, DispatchGuard
from .e3a_sandbox import SandboxFailure
from .protocol import canonical_json_hash
from .workstream_e2 import _atomic_json
from .workstream_e3a import (
    candidate_payload, development_cases, holdout_cases, run_trajectory,
    schedule, score_submission, snapshot, usage_sum,
)


class Journal:
    def __init__(self, output: Path):
        output.mkdir(parents=True, exist_ok=False)  # never resume/replace an ambiguous run
        self.output = output
        self.path = output / "attempts.jsonl"

    def record(self, event: dict) -> None:
        with self.path.open("a", encoding="utf-8", newline="\n") as stream:
            stream.write(json.dumps(event, ensure_ascii=True) + "\n")
            stream.flush()
            os.fsync(stream.fileno())


def summarize(slots: list[dict], spec: dict) -> dict:
    """All assigned slots and paired missingness survive, including a stopped batch."""
    pairs = []
    for task in spec["tasks"]:
        for repetition in range(1, spec["repetitions"] + 1):
            selected = {row["language"]: row for row in slots if row["task_id"] == task and row["repetition"] == repetition}
            values = {lang: row.get("scores", {}).get("first", {}).get("task_completion") for lang, row in selected.items()}
            difference = (int(values["fsharp"]) - int(values["csharp"])) if all(v is not None for v in values.values()) else None
            pairs.append({"task_id": task, "repetition": repetition, "completion": values,
                          "fsharp_minus_csharp": difference})
            resources = {}
            for phase in ("first_phase_usage", "repair_usage", "total_usage"):
                for measure in ("input_tokens", "output_tokens"):
                    observed = {lang: row.get("trajectory", {}).get(phase, {}).get(measure)
                                for lang, row in selected.items()}
                    resources[phase + "." + measure] = {"values": observed, "fsharp_minus_csharp":
                        observed["fsharp"] - observed["csharp"] if all(v is not None for v in observed.values()) else None}
            elapsed = {lang: row.get("elapsed_seconds") for lang, row in selected.items()}
            resources["trajectory_with_scoring_seconds"] = {"values": elapsed, "fsharp_minus_csharp":
                elapsed["fsharp"] - elapsed["csharp"] if all(v is not None for v in elapsed.values()) else None}
            pairs[-1]["resources"] = resources
    attempted_rounds = [round_ for row in slots for round_ in row.get("trajectory", {}).get("rounds", [])]
    repair_rounds = [round_ for row in slots for round_ in row.get("trajectory", {}).get("rounds", [])[1:]]
    task_summaries = {}
    for task in spec["tasks"]:
        rows = [pair for pair in pairs if pair["task_id"] == task]
        metrics = {"first_completion": [row["fsharp_minus_csharp"] for row in rows]}
        metrics.update({key: [row["resources"][key]["fsharp_minus_csharp"] for row in rows]
                        for key in rows[0]["resources"]})
        task_summaries[task] = {}
        for key, values in metrics.items():
            known = [value for value in values if value is not None]
            task_summaries[task][key] = {"paired_differences": values, "coverage": len(known),
                "complete_mean": sum(known) / len(values) if len(known) == len(values) else None,
                "observed_min": min(known) if known else None, "observed_max": max(known) if known else None}
    equal_task_means = {}
    for metric in next(iter(task_summaries.values())):
        means = [row[metric]["complete_mean"] for row in task_summaries.values()]
        equal_task_means[metric] = sum(means) / len(means) if all(v is not None for v in means) else None
    return {"assigned": len(slots), "started": sum(row["status"] != "unstarted" for row in slots),
            "paired_first_completion": pairs, "attempted_rounds": len(attempted_rounds),
            "per_task": task_summaries, "equal_task_complete_means": equal_task_means,
            "observed_usage": usage_sum(attempted_rounds), "incremental_repair_usage": usage_sum(repair_rounds),
            "usage_coverage": {k: sum(r["usage"][k] is not None for r in attempted_rounds)
                               for k in usage_sum(attempted_rounds)}}


def run_batch(root: Path, manifest: dict, spec: dict, *, transport,
              evaluator_factory: Callable, output: Path, runner_git_commit: str,
              phase: str, max_dispatches: int, authorization_id: str | None = None,
              reviews: dict | None = None, clock: Callable = time.monotonic,
              runtime_metadata: dict | None = None) -> dict:
    journal = Journal(output)
    mock = not getattr(transport, "is_live", True)
    limits = spec.get("budgets", {})
    expected = {"integration": limits.get("integration_dispatch_ceiling", 2),
                "pilot": limits.get("pilot_dispatch_ceiling", 72)}
    if phase not in expected or type(max_dispatches) is not int or max_dispatches != expected[phase] or not 0 < max_dispatches <= 72:
        raise ValueError("phase/max_dispatches do not match the adopted dispatch ceiling")
    slots = [{**item, "slot_id": f"{i + 1:02d}-{item['task_id']}-{item['language']}-r{item['repetition']}",
              "status": "unstarted", "reason": "not-reached"} for i, item in enumerate(schedule(spec))]
    report = {"specification_sha256": canonical_json_hash(spec), "runner_git_commit": runner_git_commit,
              "mode": "model-free-mock" if mock else "authorized-live", "phase": phase,
              "authorization_id": authorization_id, "runtime": copy.deepcopy(runtime_metadata),
              "slots": slots, "batch_stop": None, "live_continuation_verified": False}
    journal.record({"event": "batch-assigned", "report": copy.deepcopy(report)})
    evaluators = {}
    if not hasattr(transport, "launch"):
        raise TypeError("run_batch requires the canonical OAuth/Codex launch transport")
    dispatch_guard = DispatchGuard(max_dispatches)
    try:
        # Check every fixed initial slot before any candidate dispatch.  A
        # replay that cannot fit is an apparatus/preflight failure, never a
        # reason to drop a language or replace a slot.
        replay_cap = spec.get("authority", {}).get("max_replay_bytes", 131072)
        for item in schedule(spec):
            stage = next(i for i, task in enumerate(manifest["tasks"]) if task["id"] == item["task_id"])
            for language in (item["language"],):
                payload = candidate_payload(root, manifest, language, item["task_id"])
                if CodexOAuthAdapter.replay_size(payload) > replay_cap:
                    report["batch_stop"] = "preflight-replay-byte-budget-exhausted"
                    raise RuntimeError(report["batch_stop"])
        for slot in slots:
            slot.update(status="setup", reason=None)
            language, task_id = slot["language"], slot["task_id"]
            stage = next(i for i, task in enumerate(manifest["tasks"]) if task["id"] == task_id)
            journal.record({"event": "slot-started", "slot": copy.deepcopy(slot)})
            if language not in evaluators:
                evaluators[language] = evaluator_factory(language)
                slot["preparation"] = evaluators[language].prepare()
            evaluator = evaluators[language]
            before = snapshot(root, manifest, language, stage)
            slot["preflight"] = evaluator.evaluate(before, development_cases(manifest, stage), clock() + 120)
            journal.record({"event": "preflight", "slot_id": slot["slot_id"], "result": slot["preflight"]})
            if not slot["preflight"]["passed"]:
                slot.update(status="apparatus-failure", reason="preflight-failed")
                report["batch_stop"] = "preflight-failed"
                break
            payload = candidate_payload(root, manifest, language, task_id)
            started = clock()
            deadline = started + spec["budgets"]["trajectory_timeout_seconds"]

            def develop(source, index, end):
                return evaluator.evaluate(source, development_cases(manifest, stage + 1), end)

            trajectory_adapter = CodexOAuthAdapter(
                spec, transport, record=journal.record, clock=clock, dispatch_guard=dispatch_guard
            )
            trajectory = run_trajectory(before, language, spec,
                lambda previous, source, packet, end: trajectory_adapter.generate(
                    payload, previous, source, packet, end),
                develop, task_id=task_id, record=journal.record, clock=clock, deadline=deadline)
            slot.update(status="finished", reason=trajectory["stop"], trajectory=trajectory)
            # The controller has returned: scorer results have no route back to
            # session.generate, continuation, or the planned sample size.
            scores = slot["scores"] = {}
            for endpoint, row in [("first", trajectory["rounds"][0] if trajectory["rounds"] else None),
                                  ("terminal", trajectory["rounds"][-1] if trajectory["rounds"] else None)]:
                source = (row or {}).get("applied_source")
                holdout = None
                if source and clock() < deadline:
                    holdout = evaluator.evaluate(source, holdout_cases(root, task_id), deadline)
                review = (reviews or {}).get(slot["slot_id"], {}).get(endpoint)
                scores[endpoint] = score_submission(row, holdout, task_id=task_id, language=language,
                                                     review=review, allow_fixture_review=mock)
                scores[endpoint]["holdout_evaluation"] = holdout
                journal.record({"event": "endpoint-scored", "slot_id": slot["slot_id"],
                                "endpoint": endpoint, "score": scores[endpoint]})
            slot["elapsed_seconds"] = clock() - started
            journal.record({"event": "slot-finished", "slot": slot})
            if trajectory["batch_stop"]:
                report["batch_stop"] = trajectory["stop"]
                break
    except BaseException as exc:
        report["batch_stop"] = report["batch_stop"] or type(exc).__name__
        for slot in slots:
            if slot["status"] == "setup":
                slot.update(status="apparatus-failure", reason=report["batch_stop"])
        journal.record({"event": "batch-interrupted", "type": type(exc).__name__})
        if isinstance(exc, (KeyboardInterrupt, SystemExit)):
            raise
    finally:
        for evaluator in evaluators.values():
            try:
                evaluator.close()
            except Exception:
                report["batch_stop"] = "cleanup-unconfirmed"
        for slot in slots:
            if slot["status"] == "unstarted":
                slot["reason"] = report["batch_stop"] or "not-reached"
        dispatched = dispatch_guard.dispatched
        report.update(summary=summarize(slots, spec), reservations=[],
                      count_http_calls=None, generation_requests=None,
                      dispatches=dispatched, candidate_model_calls=0 if mock else None,
                      committed_upper_usd=None)
        _atomic_json(output / "report.json", report)
        journal.record({"event": "batch-finished", "summary": report["summary"], "batch_stop": report["batch_stop"]})
    return report
