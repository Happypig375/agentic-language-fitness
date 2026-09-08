#!/usr/bin/env python3
"""Opt-in E3a composition on the canonical remote runner; no retry or resume."""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from alf.e3a_codex import CodexOAuthAdapter, DispatchGuard
from alf.e3a_runner import Journal, run_batch
from alf.e3a_sandbox import DockerEvaluator
from alf.config import load_manifest
from alf.environment_profile import environment_profile_sha256, load_environment_profile
from alf.protocol import canonical_json_hash
from alf.workstream_e2 import _atomic_json
from alf.workstream_e3a import PACKET_DIR, SubmissionError, apply_submission, read_json


def _wrapper():
    path = ROOT / "scripts" / "codex-docker.py"
    spec = importlib.util.spec_from_file_location("alf_codex_docker", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class DockerTransport:
    """One fresh empty workspace and canonical wrapper invocation per dispatch."""
    is_live = True

    def __init__(self, args: argparse.Namespace, profile: dict, spec: dict):
        self.args, self.profile, self.spec = args, profile, spec
        self.wrapper = _wrapper()

    def launch(self, stdin: bytes, timeout: float):
        with tempfile.TemporaryDirectory(prefix="alf-e3a-turn-") as directory:
            return self.wrapper.run_e3a_cli(
                stdin, workspace=Path(directory), native_binary=self.args.native_binary,
                expected_binary_sha256=self.args.native_sha256,
                model_catalog=self.args.model_catalog,
                image=self.spec["environment"]["container_image_id"],
                expected_image_id=self.spec["environment"]["container_image_id"],
                model=self.spec["model"]["requested"],
                reasoning_effort=self.spec["model"]["reasoning_effort"],
                auth_source=self.args.auth_file, environment_profile=self.profile,
                timeout=min(timeout, self.spec["budgets"]["request_timeout_seconds"]))


def _sha(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def _git_head() -> str:
    status = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all"], cwd=ROOT,
        text=True, capture_output=True, check=True, timeout=15)
    if status.stdout.strip():
        raise ValueError("live execution requires a clean, reviewed implementing commit")
    return subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True,
                          capture_output=True, check=True, timeout=15).stdout.strip()


def _policy_sha(spec: dict) -> str:
    # Only activation metadata may differ between shakedown and pilot.
    return canonical_json_hash({k: v for k, v in spec.items()
                                if k not in {"status", "execution_authorized"}})


def _source_identity(root: Path = ROOT) -> str:
    packet = read_json(root / PACKET_DIR / "review-packet.json")
    expected = {p: h for p, h in packet["text_lf_sha256"].items()
                if p != f"{PACKET_DIR}/specification.json"}
    actual = {p: hashlib.sha256((root / p).read_text(encoding="utf-8").encode("utf-8")).hexdigest()
              for p in expected}
    if not actual or actual != expected:
        raise ValueError("reviewed source identities differ from the working tree")
    return canonical_json_hash(actual)


def verify_pilot_prerequisite(root: Path, spec: dict, runtime: dict) -> None:
    """A small tracked freeze record binds the successful shakedown to this pilot."""
    freeze = read_json(root / PACKET_DIR / "freeze.json")
    path = (root / freeze["shakedown_report"]).resolve()
    path.relative_to(root.resolve())
    if freeze["specification_sha256"] != canonical_json_hash(spec) or _sha(path) != freeze["shakedown_report_sha256"]:
        raise ValueError("freeze or shakedown report identity mismatch")
    report = read_json(path)
    if not (freeze["policy_sha256"] == report["policy_sha256"] == _policy_sha(spec)):
        raise ValueError("shakedown and pilot policies differ")
    if (report.get("scope") != "unrelated-two-step-replay-shakedown-not-scientific-trajectories"
            or report.get("candidate_model_calls") == 0 or report.get("passed") is not True
            or report.get("batch_stop") is not None or report.get("dispatches") != 2
            or len(report.get("attempts", [])) != 2):
        raise ValueError("pilot requires a successful live two-dispatch shakedown")
    for step in report["attempts"]:
        if (step["response"].get("status") != "completed" or step["response"].get("batch_stop")
                or not step.get("applied_source") or step["evaluation"].get("passed") is not True):
            raise ValueError("shakedown did not complete both exercises")
    for key in ("runner_source_sha256", "native_sha256", "catalog_sha256",
                "container_image_id", "environment_profile_sha256"):
        if not runtime.get(key) or report["runtime"].get(key) != runtime[key]:
            raise ValueError("shakedown and pilot runtime identities differ: " + key)


def _marker_case(value: int) -> list[dict]:
    return [{"name": "unrelated-marker", "input": {}, "expected": {"value": value}}]


def _integration_dispatch_ceiling(spec: dict) -> int:
    """Validate the active approved/declared integration allowance before launch."""
    approved = spec.get("approved_integration_dispatches")
    declared = spec.get("budgets", {}).get("integration_dispatch_ceiling")
    if (type(approved) is not int or type(declared) is not int
            or approved != declared or not 0 < approved <= 5):
        raise ValueError("invalid or mismatched integration dispatch ceiling")
    return approved


def run_shakedown(spec: dict, manifest: dict, *, transport, evaluator_factory,
                  output: Path, runtime_metadata: dict, root: Path = ROOT) -> dict:
    """Two distinct toy exercises, not a measured trajectory or failure retry."""
    dispatch_ceiling = _integration_dispatch_ceiling(spec)
    journal = Journal(output)
    guard = DispatchGuard(dispatch_ceiling)
    mock = not getattr(transport, "is_live", True)
    report = {
        "scope": "unrelated-two-step-replay-shakedown-not-scientific-trajectories",
        "specification_sha256": canonical_json_hash(spec),
        "policy_sha256": _policy_sha(spec),
        "runtime": copy.deepcopy(runtime_metadata), "passed": False,
        "batch_stop": None, "attempts": [], "provider_requests": None,
        "dispatch_ceiling": dispatch_ceiling,
        "subscription_cost_usd": None, "candidate_model_calls": 0 if mock else None,
    }
    journal.record({"event": "shakedown-started", "report": copy.deepcopy(report)})
    evaluator = None
    try:
        if not mock and not (spec.get("execution_authorized") and
                             spec.get("user_live_execution_approved")):
            report["batch_stop"] = "execution-not-authorized"
            raise ValueError(report["batch_stop"])
        language = manifest["languages"]["csharp"]
        project = (root / language["base"] / language["project_file"]).read_text(encoding="utf-8")
        current = {language["project_file"]: project,
                   "Program.cs": 'using System;\nwhile (Console.ReadLine() is not null) Console.WriteLine("{\\"value\\":0}");\n'}
        payload = {
            "instructions": (root / PACKET_DIR / "candidate-instructions.md").read_text(encoding="utf-8"),
            "baseline_contract": "Unrelated integration exercise: read JSON lines and emit one JSON object per input line. No OrderFlow task or research outcome is involved.",
            "current_task": 'Replace Program.cs to emit {"value":1} for every input line. Keep the project unchanged.',
            "source": copy.deepcopy(current),
        }
        if CodexOAuthAdapter.replay_size(payload) > spec["authority"]["max_replay_bytes"]:
            report["batch_stop"] = "preflight-replay-byte-budget-exhausted"
            raise ValueError(report["batch_stop"])
        evaluator = evaluator_factory()
        report["preparation"] = evaluator.prepare()
        deadline = time.monotonic() + spec["budgets"]["trajectory_timeout_seconds"]
        report["preflight"] = evaluator.evaluate(current, _marker_case(0), deadline)
        journal.record({"event": "shakedown-preflight", "result": report["preflight"]})
        if not report["preflight"].get("passed"):
            report["batch_stop"] = "preflight-failed"
            raise ValueError(report["batch_stop"])
        adapter = CodexOAuthAdapter(spec, transport, dispatch_guard=guard, record=journal.record)
        feedback = None
        for value in (1, 2):
            response = adapter.generate(payload, None, current, feedback, deadline)
            step = {"step": value, "response": response, "applied_source": None, "evaluation": None}
            report["attempts"].append(step)
            if response.get("status") != "completed":
                report["batch_stop"] = response.get("failure", "incomplete-response")
                break
            try:
                updated = apply_submission(current, response["text"], "csharp", spec,
                                           project_reference=project)
            except SubmissionError as exc:
                step["submission_error"] = type(exc).__name__
                report["batch_stop"] = response.get("failure") or "invalid-submission"
                journal.record({"event": "shakedown-step", "step": copy.deepcopy(step)})
                break
            step["applied_source"] = updated
            step["evaluation"] = evaluator.evaluate(updated, _marker_case(value), deadline)
            journal.record({"event": "shakedown-step", "step": copy.deepcopy(step)})
            # An accounting alarm stops further dispatch, not scoring a complete answer.
            if response.get("batch_stop"):
                report["batch_stop"] = response.get("failure", "accounting-alarm")
                break
            if not step["evaluation"].get("passed"):
                report["batch_stop"] = "shakedown-evaluation-failed"
                break
            current = updated
            feedback = {"version": "shakedown-replay-check-v1", "text":
                'The first integration step passed. For the separate second replay check, now emit {"value":2} per input line. This is not failure feedback or a measured repair.'}
        report["passed"] = guard.dispatched == 2 and report["batch_stop"] is None
    except BaseException as exc:
        report["batch_stop"] = report["batch_stop"] or type(exc).__name__
        journal.record({"event": "shakedown-interrupted", "type": type(exc).__name__})
        if isinstance(exc, (KeyboardInterrupt, SystemExit)):
            raise
    finally:
        if evaluator is not None:
            try:
                evaluator.close()
            except Exception:
                report["passed"] = False
                report["batch_stop"] = "cleanup-unconfirmed"
        report["dispatches"] = guard.dispatched
        _atomic_json(output / "report.json", report)
        journal.record({"event": "shakedown-finished", "passed": report["passed"],
                        "dispatches": guard.dispatched, "batch_stop": report["batch_stop"]})
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", choices=["shakedown", "pilot"], required=True)
    parser.add_argument("--native-binary", type=Path, required=True)
    parser.add_argument("--native-sha256", required=True)
    parser.add_argument("--model-catalog", type=Path, required=True)
    parser.add_argument("--auth-file", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    spec = read_json(ROOT / PACKET_DIR / "specification.json")
    if not (spec.get("execution_authorized") and spec.get("user_live_execution_approved")):
        parser.error("E3a execution is not authorized")
    if args.phase == "pilot" and spec.get("status") != "frozen":
        parser.error("pilot requires frozen specification")
    if args.output.exists():
        parser.error("refusing to overwrite existing output")
    profile = load_environment_profile(ROOT / "infra/remote-runner/environment-profile.json",
                                       repository_root=ROOT)
    manifest = load_manifest(ROOT, spec["manifest"])
    runtime = {"runner_git_commit": _git_head(), "runner_source_sha256": _source_identity(),
               "native_sha256": _sha(args.native_binary),
               "catalog_sha256": _sha(args.model_catalog),
               "environment_profile_sha256": environment_profile_sha256(profile),
               "container_image_id": spec["environment"]["container_image_id"]}
    transport = DockerTransport(args, profile, spec)
    if (runtime["native_sha256"] != transport.wrapper.E3A_NATIVE_SHA256
            or args.native_sha256 != transport.wrapper.E3A_NATIVE_SHA256):
        parser.error("native binary hash differs from the reviewed binary")
    if runtime["catalog_sha256"] != transport.wrapper.E3A_MODEL_CATALOG_SHA256:
        parser.error("model catalog differs from the pinned native catalog")
    if args.phase == "shakedown":
        report = run_shakedown(spec, manifest, transport=transport,
            evaluator_factory=lambda: DockerEvaluator(ROOT, manifest, spec, "csharp"),
            output=args.output, runtime_metadata=runtime)
    else:
        verify_pilot_prerequisite(ROOT, spec, runtime)
        report = run_batch(ROOT, manifest, spec, transport=transport,
            evaluator_factory=lambda language: DockerEvaluator(ROOT, manifest, spec, language),
            output=args.output, runner_git_commit=runtime["runner_git_commit"],
            phase="pilot", max_dispatches=72, runtime_metadata=runtime)
    passed = report.get("passed", report["batch_stop"] is None)
    print(json.dumps({"phase": args.phase, "passed": passed, "dispatches": report["dispatches"],
                      "batch_stop": report["batch_stop"], "output": str(args.output)}))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
