from __future__ import annotations

import json
import platform
import shutil
import sys
import tempfile
import uuid
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .agents import CodexAgent, CommandAgent, ScriptedAgent
from .evaluator import evaluate_project
from .metrics import git_diff_metrics, git_head, snapshot_repository
from .models import AgentResult, Usage
from .process import run_process


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def command_version(command: list[str], cwd: Path) -> str | None:
    result = run_process(command, cwd=cwd, timeout=30)
    if not result.ok:
        return None
    return (result.stdout or result.stderr).strip().splitlines()[0] if (result.stdout or result.stderr).strip() else None


def environment_snapshot(root: Path, agent_name: str) -> dict[str, Any]:
    data: dict[str, Any] = {
        "platform": platform.platform(),
        "machine": platform.machine(),
        "python": sys.version.replace("\n", " "),
        "git": command_version(["git", "--version"], root),
        "dotnet": command_version(["dotnet", "--version"], root),
    }
    if agent_name == "codex":
        data["codex"] = command_version(["codex", "--version"], root)
    return data


def make_agent(name: str, *, model: str | None, agent_command: str | None, require_usage: bool = False):
    if name == "scripted":
        return ScriptedAgent()
    if name == "codex":
        return CodexAgent(model=model)
    if name == "command":
        return CommandAgent(agent_command or "", require_usage=require_usage)
    raise ValueError(f"Unknown agent: {name}")


def init_workspace(root: Path, manifest: dict[str, Any], language: str, workspace: Path) -> None:
    cfg = manifest["languages"][language]
    source = root / cfg["base"]
    if not source.is_dir():
        raise FileNotFoundError(source)
    shutil.copytree(source, workspace)
    init = run_process(["git", "init", "-q"], cwd=workspace, timeout=30)
    if not init.ok:
        raise RuntimeError(f"Failed to initialize workspace: {init.stderr}")
    exclude = workspace / ".git" / "info" / "exclude"
    exclude.write_text(".alf/\nbin/\nobj/\n", encoding="utf-8")
    for argv in (
        ["git", "config", "user.name", "ALF Harness"],
        ["git", "config", "user.email", "alf@example.invalid"],
        ["git", "add", "."],
        ["git", "commit", "-q", "-m", "baseline"],
    ):
        result = run_process(argv, cwd=workspace, timeout=30)
        if not result.ok:
            raise RuntimeError(f"Failed to initialize workspace: {' '.join(argv)}\n{result.stderr}")


def write_agent_logs(task_dir: Path, result: AgentResult) -> dict[str, str]:
    task_dir.mkdir(parents=True, exist_ok=True)
    stdout_path = task_dir / "agent.stdout"
    stderr_path = task_dir / "agent.stderr"
    events_path = task_dir / "events.jsonl"
    stdout_path.write_text(result.process.stdout, encoding="utf-8")
    stderr_path.write_text(result.process.stderr, encoding="utf-8")
    with events_path.open("w", encoding="utf-8") as handle:
        for event in result.events:
            handle.write(json.dumps(event, sort_keys=True) + "\n")
    return {
        "stdout": str(stdout_path),
        "stderr": str(stderr_path),
        "events": str(events_path),
    }


def _agent_summary(result: AgentResult, log_paths: dict[str, str]) -> dict[str, Any]:
    return {
        "ok": result.ok,
        "model": result.model,
        "process": result.process.summary(),
        "usage": result.usage.to_dict() if result.usage_available and result.accounting_valid else None,
        "event_count": result.event_count,
        "command_count": result.command_count,
        "file_change_count": result.file_change_count,
        "failed_event_count": result.failed_event_count,
        "file_reads": result.file_reads,
        "unique_file_reads": result.unique_file_reads,
        "file_revisits": result.file_revisits,
        "logs": log_paths,
        "accounting_valid": result.accounting_valid,
        "usage_available": result.usage_available,
        "accounting_errors": result.accounting_errors,
        "agent_process_wall_seconds": result.process.duration_seconds,
    }


def run_chain(
    *,
    root: Path,
    manifest: dict[str, Any],
    language: str,
    agent_name: str,
    output_root: Path,
    model: str | None = None,
    agent_command: str | None = None,
    timeout: float = 600,
    max_tasks: int | None = None,
    require_usage: bool = False,
) -> Path:
    if require_usage and agent_name != "command":
        raise ValueError("--require-usage is valid only with --agent command")
    if language not in manifest["languages"]:
        raise ValueError(f"Unsupported language {language!r}; choose from {sorted(manifest['languages'])}")
    run_id = f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{language}-{agent_name}-{uuid.uuid4().hex[:8]}"
    run_dir = output_root / run_id
    workspace = run_dir / "workspace"
    run_dir.mkdir(parents=True, exist_ok=False)
    run_started_at = utc_now()
    run_started_monotonic = time.monotonic()
    init_workspace(root, manifest, language, workspace)
    cfg = manifest["languages"][language]
    agent = make_agent(agent_name, model=model, agent_command=agent_command, require_usage=require_usage)
    baseline_started = time.monotonic()
    baseline = evaluate_project(workspace, cfg, manifest["baseline_cases"], timeout=min(timeout, 300))
    baseline["evaluator_wall_seconds"] = time.monotonic() - baseline_started
    aggregate_usage = Usage()
    aggregate_accounting_valid = True
    aggregate_usage_available = True
    run_result: dict[str, Any] = {
        "schema_version": 1,
        "run_id": run_id,
        "benchmark": manifest["id"],
        "language": language,
        "agent": agent_name,
        "requested_model": model,
        "started_at": run_started_at,
        "environment": environment_snapshot(root, agent_name),
        "baseline": baseline,
        "tasks": [],
        "success": False,
        "agent_process_wall_seconds": 0.0,
        "evaluator_wall_seconds": 0.0,
        "run_total_wall_seconds": None,
        "aggregate_usage": None,
        "aggregate_usage_available": False,
        "aggregate_accounting_valid": False,
        "require_usage": require_usage,
    }
    run_result["evaluator_wall_seconds"] = baseline["evaluator_wall_seconds"]
    if not baseline["ok"]:
        run_result["run_total_wall_seconds"] = time.monotonic() - run_started_monotonic
        run_result["finished_at"] = utc_now()
        (run_dir / "result.json").write_text(json.dumps(run_result, indent=2, sort_keys=True), encoding="utf-8")
        return run_dir

    cumulative_cases = list(manifest["baseline_cases"])
    tasks = manifest["tasks"][:max_tasks] if max_tasks else manifest["tasks"]
    for task in tasks:
        task_started_monotonic = time.monotonic()
        task_dir = run_dir / "tasks" / task["id"]
        prompt_path = root / task["prompt"]
        prompt = prompt_path.read_text(encoding="utf-8")
        pre = snapshot_repository(workspace)
        pre_head = git_head(workspace)
        task_started = utc_now()
        agent_result = agent.run(
            root=root,
            workspace=workspace,
            language=language,
            language_config=cfg,
            task=task,
            prompt=prompt,
            timeout=timeout,
        )
        aggregate_usage.add(agent_result.usage)
        aggregate_accounting_valid = aggregate_accounting_valid and agent_result.accounting_valid
        aggregate_usage_available = (
            aggregate_usage_available
            and agent_result.accounting_valid
            and agent_result.usage_available
        )
        log_paths = write_agent_logs(task_dir, agent_result)
        provenance_sidecar = workspace / ".alf" / f"usage-{task['id']}.json"
        if provenance_sidecar.is_file():
            shutil.copy2(provenance_sidecar, task_dir / "usage.json")
        cumulative_cases.extend(task["cases"])
        evaluation_started = time.monotonic()
        evaluation = evaluate_project(workspace, cfg, cumulative_cases, timeout=min(timeout, 300))
        evaluation["evaluator_wall_seconds"] = time.monotonic() - evaluation_started
        run_result["agent_process_wall_seconds"] += agent_result.process.duration_seconds
        run_result["evaluator_wall_seconds"] += evaluation["evaluator_wall_seconds"]
        post = snapshot_repository(workspace)
        diff = git_diff_metrics(workspace)
        task_ok = agent_result.ok and evaluation["ok"]
        task_result: dict[str, Any] = {
            "task_id": task["id"],
            "started_at": task_started,
            "finished_at": None,
            "pre_commit": pre_head,
            "agent": _agent_summary(agent_result, log_paths),
            "evaluation": evaluation,
            "repository_before": pre,
            "repository_after": post,
            "diff": diff,
            "success": task_ok,
            "task_total_wall_seconds": None,
        }
        if task_ok:
            for argv in (["git", "add", "."], ["git", "commit", "-q", "-m", task["id"]]):
                commit = run_process(argv, cwd=workspace, timeout=30)
                if not commit.ok:
                    task_ok = False
                    task_result["success"] = False
                    task_result["commit_error"] = commit.stderr
                    break
            task_result["post_commit"] = git_head(workspace)
        # The documented task boundary ends immediately before serialization.
        task_result["task_total_wall_seconds"] = time.monotonic() - task_started_monotonic
        task_result["finished_at"] = utc_now()
        (task_dir / "task-result.json").write_text(
            json.dumps(task_result, indent=2, sort_keys=True), encoding="utf-8"
        )
        run_result["tasks"].append(task_result)
        if not task_ok:
            break

    run_result["aggregate_usage"] = aggregate_usage.to_dict() if aggregate_usage_available else None
    run_result["aggregate_usage_available"] = aggregate_usage_available
    run_result["aggregate_accounting_valid"] = aggregate_accounting_valid
    run_result["require_usage"] = require_usage
    run_result["finished_at"] = utc_now()
    run_result["run_total_wall_seconds"] = time.monotonic() - run_started_monotonic
    run_result["success"] = len(run_result["tasks"]) == len(tasks) and all(t["success"] for t in run_result["tasks"])
    (run_dir / "result.json").write_text(json.dumps(run_result, indent=2, sort_keys=True), encoding="utf-8")
    return run_dir


def validate_benchmark(root: Path, manifest: dict[str, Any], timeout: float = 300) -> dict[str, Any]:
    report: dict[str, Any] = {"ok": True, "languages": {}}
    for language, cfg in manifest["languages"].items():
        language_report: dict[str, Any] = {"baseline": None, "tasks": []}
        with tempfile.TemporaryDirectory(prefix=f"alf-validate-{language}-") as temp:
            workspace = Path(temp) / "workspace"
            init_workspace(root, manifest, language, workspace)
            baseline = evaluate_project(workspace, cfg, manifest["baseline_cases"], timeout=timeout)
            language_report["baseline"] = baseline
            ok = baseline["ok"]
            cases = list(manifest["baseline_cases"])
            for task in manifest["tasks"]:
                source = root / task["gold"][language]
                shutil.copy2(source, workspace / cfg["source_file"])
                cases.extend(task["cases"])
                evaluation = evaluate_project(workspace, cfg, cases, timeout=timeout)
                language_report["tasks"].append({"task_id": task["id"], "evaluation": evaluation})
                ok = ok and evaluation["ok"]
            language_report["ok"] = ok
            report["languages"][language] = language_report
            report["ok"] = report["ok"] and ok
    return report
