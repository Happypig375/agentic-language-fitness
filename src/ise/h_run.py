"""Guarded H integration/pilot orchestration.  Importing this module is model-free."""
from __future__ import annotations

import copy
import hashlib
import json
import time
from pathlib import Path
from typing import Any, Callable, Mapping

from .h import HBoundaryError, HController, TrajectoryDispatcher
from .h_check import audit
from .h_workload import cases_for, ordered_filenames, public_payload, source_for
from .protocol import canonical_json_hash
from .e3a_runner import Journal
from .workstream_e2 import _atomic_json

INTEGRATION_CEILING = 5
INTEGRATION_PLANNED = 3
PILOT_CEILING = 64
PILOT_SLOTS = 32


def policy_sha(spec: Mapping[str, Any]) -> str:
    """Identity excluding only activation/review bookkeeping."""
    ignored = {"status", "execution_authorized", "user_live_execution_approved",
               "approved_integration_dispatches", "approved_pilot_dispatches"}
    policy = copy.deepcopy({k: v for k, v in spec.items() if k not in ignored})
    policy.get("model", {}).pop("h_live_integration_verified", None)
    policy.get("analysis", {}).pop("human_review_approved", None)
    return canonical_json_hash(policy)


def require_live_authority(spec: Mapping[str, Any], phase: str) -> int:
    if phase not in {"integration", "pilot"}:
        raise HBoundaryError("invalid H phase")
    if not (spec.get("execution_authorized") is True
            and spec.get("user_live_execution_approved") is True
            and spec.get("analysis", {}).get("human_review_approved") is True):
        raise HBoundaryError("H live execution is not explicitly authorized")
    key, ceiling = (("approved_integration_dispatches", INTEGRATION_CEILING)
                    if phase == "integration" else
                    ("approved_pilot_dispatches", PILOT_CEILING))
    if spec.get(key) != ceiling:
        raise HBoundaryError("approved dispatch ceiling is absent or mismatched")
    return ceiling


def verified_construction(root: Path, spec: Mapping[str, Any]) -> dict[str, Any]:
    result = audit(root, permit_activation=True)
    proposed = result["proposed_specification_updates"]
    paths = ("workload.source_sha256", "workload.cases_sha256", "workload.public_payload_sha256", "budgets.cap_low",
             "budgets.cap_high", "schedule.schedule_sha256", "schedule.feasibility_mask_sha256")
    def get(path: str) -> Any:
        a, b = path.split(".")
        return spec.get(a, {}).get(b)
    if result["status"] != "passed" or any(get(path) != proposed[path] for path in paths):
        raise HBoundaryError("reviewed H construction identities are not frozen")
    return result


def verify_pilot_freeze(root: Path, spec: Mapping[str, Any], runtime: Mapping[str, Any]) -> None:
    freeze_path = root / "protocols/workstream-h1-h2/freeze.json"
    freeze = json.loads(freeze_path.read_text(encoding="utf-8"))
    report_path = (root / freeze["integration_report"]).resolve()
    report_path.relative_to(root.resolve())
    raw = report_path.read_bytes()
    report = json.loads(raw)
    if (freeze.get("specification_sha256") != canonical_json_hash(spec)
            or freeze.get("policy_sha256") != policy_sha(spec)
            or freeze.get("integration_report_sha256") != hashlib.sha256(raw).hexdigest()
            or report.get("phase") != "integration"
            or report.get("policy_sha256") != policy_sha(spec)
            or report.get("passed") is not True or report.get("dispatches") != INTEGRATION_PLANNED
            or report.get("batch_stop") is not None):
        raise HBoundaryError("pilot requires a matching successful integration freeze")
    for key, value in runtime.items():
        if key.endswith("sha256") or key == "container_image_id":
            if report.get("runtime", {}).get(key) != value:
                raise HBoundaryError("integration runtime identity differs: " + key)


def _new_slot(item: Mapping[str, Any]) -> dict[str, Any]:
    return {**copy.deepcopy(dict(item)), "slot_id": f"h-{item['slot']:02d}",
            "status": "unstarted", "reason": "not-reached", "dispatches": []}


def run_pilot(root: Path, spec: Mapping[str, Any], construction: Mapping[str, Any], *,
              transport: Any, evaluator_factory: Callable[[str, str, Mapping[str, str]], Any],
              output: Path, runtime: Mapping[str, Any], clock: Callable[[], float] = time.monotonic) -> dict:
    ceiling = require_live_authority(spec, "pilot")
    slots = [_new_slot(item) for item in construction["feasibility_mask"]]
    journal = Journal(output)
    report = {"phase": "pilot", "specification_sha256": canonical_json_hash(spec),
              "runtime": copy.deepcopy(dict(runtime)), "slots": slots, "dispatches": 0,
              "batch_stop": None, "passed": False, "architecture_review": None,
              "subscription_cost_usd": None}
    journal.record({"event": "batch-assigned", "report": copy.deepcopy(report)})
    dispatcher = TrajectoryDispatcher(transport, ceiling, allow_live=True,
        execution_authorized=True, user_live_execution_approved=True, clock=clock, record=journal.record)
    evaluators: dict[tuple[str, str], Any] = {}
    try:
        for slot in slots:
            if dispatcher.halted:
                slot["reason"] = "batch-stopped"
                continue
            if not slot["feasible"]:
                slot.update(status="infeasible-authored-budget", reason="preflight-authored-budget")
                continue
            slot.update(status="started", reason=None)
            level, language = slot["level"], slot["language"]
            key = (level, language)
            try:
                source = source_for(root, level, language)
                order = ordered_filenames(source, language, slot["file_order"] == "reverse")
                if key not in evaluators:
                    evaluators[key] = evaluator_factory(level, language, source)
                    slot["preparation"] = evaluators[key].prepare()
                controller = HController(source, order, contracts=public_payload(root, level), task={},
                    language=language, access=slot["access"], byte_cap=slot["cap_bytes"],
                    submission_spec=spec,
                    evaluator=lambda workspace, deadline, e=evaluators[key], l=level: e.evaluate(
                        workspace, cases_for(root, l, include_summary=True), deadline))
                outcome = controller.run_trajectory(dispatcher=dispatcher)
            except Exception as exc:
                outcome = {"failure": f"apparatus-{type(exc).__name__}", "batch_stop": True,
                           "dispatches": [], "events": []}
            slot["trajectory"] = outcome
            slot["dispatches"] = outcome.get("dispatches", [])
            slot["status"] = "finished" if outcome.get("evaluation") is not None else "failed"
            slot["reason"] = outcome.get("failure")
            evaluation = outcome.get("evaluation")
            model_format_failure = bool(outcome.get("failure") and outcome.get("dispatches")
                and outcome["dispatches"][-1].get("status") == "completed")
            known_failure = (model_format_failure or
                (isinstance(evaluation, Mapping) and
                 (evaluation.get("passed") is False or evaluation.get("build_passed") is False)))
            slot["task_completion"] = False if known_failure else None
            if outcome.get("batch_stop"):
                dispatcher.halted = True
            if dispatcher.halted:
                report["batch_stop"] = outcome.get("failure") or "dispatch-hard-stop"
        report["dispatches"] = dispatcher.guard.dispatched
        report["passed"] = report["batch_stop"] is None
    finally:
        for evaluator in evaluators.values():
            try:
                evaluator.close()
            except Exception:
                report.update(passed=False, batch_stop="cleanup-unconfirmed")
        report["dispatches"] = dispatcher.guard.dispatched
        _atomic_json(output / "report.json", report)
    return report


def run_integration(spec: Mapping[str, Any], *, transport: Any, evaluator: Callable[[dict[str, str], float], Any],
                    source: Mapping[str, str], order: list[str], submission_spec: Mapping[str, Any],
                    output: Path, runtime: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Three-call H protocol check: H1 submit, then H2 read Program + submit."""
    ceiling = require_live_authority(spec, "integration")
    journal = Journal(output)
    dispatcher = TrajectoryDispatcher(transport, ceiling, allow_live=True,
        execution_authorized=True, user_live_execution_approved=True, record=journal.record)
    report = {"phase": "integration", "scope": "unrelated-small-csharp-marker",
              "specification_sha256": canonical_json_hash(spec), "policy_sha256": policy_sha(spec),
              "runtime": copy.deepcopy(dict(runtime or {})), "attempts": [],
              "batch_stop": None, "passed": False, "dispatches": 0,
              "subscription_cost_usd": None}
    try:
        for access in ("H1", "H2"):
            controller = HController(source, order, contracts={"marker": "unrelated"},
                task={"requirement": "Change the program so every input line returns JSON {\"value\":1}.",
                      "h2_required_read": "For H2, first read exactly Program.cs, then submit."},
                language="csharp", access=access, byte_cap=131072,
                submission_spec=submission_spec, evaluator=evaluator)
            result = controller.run_trajectory(dispatcher=dispatcher)
            report["attempts"].append({"access": access, "result": result})
            if result.get("failure"):
                report["batch_stop"] = result["failure"]
                break
            evaluation = result.get("evaluation")
            if not isinstance(evaluation, Mapping) or evaluation.get("passed") is not True:
                report["batch_stop"] = "integration-behavior-failed"
                break
            if access == "H2":
                events = result.get("events", [])
                if (len(events) != 2 or events[0].get("action") != "read"
                        or events[0].get("paths") != ["Program.cs"]
                        or events[1].get("action") != "submit"):
                    report["batch_stop"] = "integration-H2-read-transition-mismatch"
                    break
        report["dispatches"] = dispatcher.guard.dispatched
        report["passed"] = report["batch_stop"] is None and report["dispatches"] == INTEGRATION_PLANNED
    finally:
        report["dispatches"] = dispatcher.guard.dispatched
        _atomic_json(output / "report.json", report)
    return report
