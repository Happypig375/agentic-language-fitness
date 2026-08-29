from __future__ import annotations

import json
import platform
import re
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
from .protocol import classify_failure, load_frozen_manifest


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


def make_agent(name: str, *, model: str | None, agent_command: str | None, require_usage: bool = False, expected_protocol: dict[str, Any] | None = None):
    if name == "scripted":
        return ScriptedAgent()
    if name == "codex":
        return CodexAgent(model=model)
    if name == "command":
        return CommandAgent(agent_command or "", require_usage=require_usage, expected_protocol=expected_protocol)
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
        "usage_record_count": result.usage_record_count,
        "logs": log_paths,
        "accounting_valid": result.accounting_valid,
        "usage_available": result.usage_available,
        "accounting_errors": result.accounting_errors,
        "agent_process_wall_seconds": result.process.duration_seconds,
        "auth_ok": result.auth_ok,
        "container_limits": result.container_limits,
    }


_ATTEMPT_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")


def _stored_results(output_root: Path) -> list[dict[str, Any]]:
    """Load retained result objects, ignoring unrelated malformed files."""

    results: list[dict[str, Any]] = []
    if not output_root.exists():
        return results
    for path in output_root.rglob("result.json"):
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            continue
        if isinstance(value, dict):
            results.append(value)
    return results


def _stored_attempt_records(output_root: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    if not output_root.exists():
        return records
    for path in output_root.rglob("attempt.json"):
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            continue
        if isinstance(value, dict):
            records.append(value)
    return records


def _retained_position_one(
    result: dict[str, Any],
    *,
    protocol: dict[str, Any],
    block_id: str,
    order: str,
    first_language: str,
) -> bool:
    """Return whether a result is a completed, usable first-position outcome."""

    provenance = result.get("provenance")
    baseline = result.get("baseline")
    tasks = result.get("tasks")
    if not isinstance(provenance, dict) or not isinstance(baseline, dict):
        return False
    if baseline.get("ok") is not True or not result.get("finished_at"):
        return False
    if not isinstance(tasks, list) or not tasks:
        return False
    if not any(isinstance(task, dict) and task.get("finished_at") for task in tasks):
        return False
    same_attempt_context = (
        provenance.get("cell_id") == protocol.get("cell_id")
        and provenance.get("manifest_sha256") == protocol.get("manifest_sha256")
        and provenance.get("block_id") == block_id
        and provenance.get("order") == order
        and provenance.get("position") == 1
        and provenance.get("language") == first_language
    )
    if not same_attempt_context:
        return False
    disposition = result.get("disposition")
    if not isinstance(disposition, dict) or disposition.get("analysis_role") != "primary":
        return False
    return True


def _process_summaries(evaluation: Any) -> list[dict[str, Any]]:
    if not isinstance(evaluation, dict):
        return []
    values = [evaluation.get("build"), evaluation.get("run")]
    return [value for value in values if isinstance(value, dict)]


def _recorded_evaluation(evaluation: Any) -> bool:
    """Return whether the evaluator produced its required result envelope."""

    return (
        isinstance(evaluation, dict)
        and isinstance(evaluation.get("ok"), bool)
        and isinstance(evaluation.get("build"), dict)
    )


def _derive_protocol_disposition(run_result: dict[str, Any]) -> dict[str, Any]:
    """Classify a completed protocol attempt from recorded, deterministic signals."""

    baseline = run_result.get("baseline")
    baseline_recorded = _recorded_evaluation(baseline)
    baseline_ok = baseline_recorded and baseline.get("ok") is True
    baseline_processes = _process_summaries(baseline)
    tasks = run_result.get("tasks") if isinstance(run_result.get("tasks"), list) else []
    task_evaluations = [
        task.get("evaluation")
        for task in tasks
        if isinstance(task, dict)
    ]
    evaluations_recorded = len(task_evaluations) == len(tasks) and all(
        _recorded_evaluation(evaluation) for evaluation in task_evaluations
    )
    task_evaluator_processes = [
        process
        for evaluation in task_evaluations
        for process in _process_summaries(evaluation)
    ]
    task_agents = [
        task.get("agent")
        for task in tasks
        if isinstance(task, dict) and isinstance(task.get("agent"), dict)
    ]
    agent_processes = [
        (agent, agent.get("process"))
        for agent in task_agents
        if isinstance(agent.get("process"), dict)
    ]
    task_processes = [process for _agent, process in agent_processes]
    sidecar_protocol_ok = not any(
        isinstance(error, str) and error.startswith("protocol sidecar")
        for agent in task_agents
        for error in (agent.get("accounting_errors") or [])
    )

    host_ok = not any(
        process.get("missing_executable") is True
        for process in [
            *baseline_processes,
            *task_evaluator_processes,
            *task_processes,
        ]
    )
    timed_out = any(
        process.get("timed_out") is True
        for process in [*task_processes, *task_evaluator_processes]
    )
    auth_ok = not any(agent.get("auth_ok") is False for agent in task_agents)
    provider_ok = not any(
        process.get("returncode") not in (None, 0)
        and process.get("timed_out") is not True
        and process.get("missing_executable") is not True
        and agent.get("auth_ok") is True
        and agent.get("usage_available") is not True
        for agent, process in agent_processes
    )
    accounting_ok = (
        run_result.get("aggregate_accounting_valid") is True if baseline_ok else True
    )
    evaluator_ok = baseline_ok and evaluations_recorded
    agent_ok = (
        run_result.get("success") is True
        if baseline_ok and evaluations_recorded
        else True
    )
    category = classify_failure(
        protocol_ok=(
            isinstance(run_result.get("provenance"), dict) and sidecar_protocol_ok
        ),
        accounting_ok=accounting_ok,
        auth_ok=auth_ok,
        provider_ok=provider_ok,
        host_ok=host_ok,
        timed_out=timed_out,
        agent_ok=agent_ok,
        evaluator_ok=evaluator_ok,
    )
    infrastructure_categories = {"protocol", "auth", "provider", "host", "evaluator"}
    candidate_outcome = baseline_ok and category not in infrastructure_categories
    usage_included = (
        candidate_outcome
        and run_result.get("aggregate_accounting_valid") is True
        and run_result.get("aggregate_usage_available") is True
    )
    return {
        "protocol_valid": (
            isinstance(run_result.get("provenance"), dict) and sidecar_protocol_ok
        ),
        "failure_category": category,
        "classification_basis": "frozen deterministic runner rules",
        "candidate_outcome": candidate_outcome,
        "analysis_role": "primary" if candidate_outcome else "infrastructure-invalid",
        "retryable": category in infrastructure_categories,
        "include_success_time": candidate_outcome,
        "include_usage_metrics": usage_included,
        "include_paired_performance": candidate_outcome,
    }


def _reserve_protocol_run_directory(output_root: Path, attempt_id: str) -> Path:
    """Atomically reserve the globally unique run directory for an attempt."""

    run_dir = output_root / attempt_id
    try:
        run_dir.mkdir(exist_ok=False)
    except FileExistsError as exc:
        raise ValueError("attempt_id has already been atomically reserved") from exc
    return run_dir


def _prepare_protocol_run(
    *,
    root: Path,
    benchmark_manifest: dict[str, Any],
    language: str,
    agent_name: str,
    output_root: Path,
    model: str | None,
    agent_command: str | None,
    timeout: float,
    max_tasks: int | None,
    require_usage: bool,
    protocol_manifest: Path,
    block_id: str | None,
    order: str | None,
    attempt_id: str | None,
    position: int | None,
) -> tuple[dict[str, Any], str, int]:
    """Validate all frozen-cell inputs before a run directory is created."""

    if agent_name != "command" or not require_usage or max_tasks is not None:
        raise ValueError("protocol runs require command agent, --require-usage, and all tasks")
    if agent_command is not None:
        raise ValueError("protocol runs do not accept a caller agent command")
    if (
        not block_id
        or not attempt_id
        or _ATTEMPT_ID.fullmatch(attempt_id) is None
        or position not in {1, 2}
        or order not in {"csharp-first", "fsharp-first"}
    ):
        raise ValueError(
            "protocol runs require a safe attempt_id, block_id, position, and "
            "csharp-first/fsharp-first order"
        )

    protocol = load_frozen_manifest(root, protocol_manifest)
    definition = protocol["definition"]
    schedule = protocol["schedule"]

    benchmark_path = (root / definition["benchmark_manifest"]).resolve()
    try:
        tracked_benchmark = json.loads(benchmark_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"tracked benchmark manifest is unavailable: {exc}") from exc
    if benchmark_manifest != tracked_benchmark:
        raise ValueError("loaded benchmark does not match the frozen protocol")

    blocks = [schedule["calibration"], *schedule["formal"]]
    block = next((item for item in blocks if item.get("block_id") == block_id), None)
    if block is None:
        raise ValueError("protocol block is not in the frozen schedule")
    expected_order = f"{block['order'][0]}-first"
    expected_language = block["order"][position - 1]
    if order != expected_order or language != expected_language:
        raise ValueError("protocol block/language/order mismatch")

    raw_root = (root / definition["raw_root"]).resolve()
    if output_root.resolve() != raw_root:
        raise ValueError("protocol output must be the definition's raw_root")
    if model != definition["model"]["snapshot"]:
        raise ValueError("model does not match the frozen protocol")
    if timeout != definition["limits"]["task_timeout_seconds"]:
        raise ValueError("timeout does not match the frozen protocol")

    retained = _stored_results(output_root)
    attempt_records = _stored_attempt_records(output_root)
    for record in attempt_records:
        record_provenance = record.get("provenance")
        if (
            isinstance(record_provenance, dict)
            and record_provenance.get("attempt_id") == attempt_id
        ):
            raise ValueError("attempt_id has already been used")
        if (
            isinstance(record_provenance, dict)
            and record_provenance.get("cell_id") == protocol.get("cell_id")
            and record_provenance.get("manifest_sha256") == protocol.get("manifest_sha256")
            and record_provenance.get("block_id") == block_id
            and record_provenance.get("position") == position
            and record.get("state") != "completed"
        ):
            raise ValueError("a prior attempt for this block position is unresolved")

    matching_results: list[dict[str, Any]] = []
    for prior in retained:
        prior_provenance = prior.get("provenance")
        if not isinstance(prior_provenance, dict):
            continue
        if prior_provenance.get("attempt_id") == attempt_id:
            raise ValueError("attempt_id has already been used")
        if (
            prior_provenance.get("cell_id") == protocol.get("cell_id")
            and prior_provenance.get("manifest_sha256") == protocol.get("manifest_sha256")
            and prior_provenance.get("block_id") == block_id
            and prior_provenance.get("position") == position
        ):
            matching_results.append(prior)

    for prior in matching_results:
        disposition = prior.get("disposition")
        if not isinstance(disposition, dict):
            raise ValueError("a prior attempt lacks a frozen inclusion disposition")
        if disposition.get("analysis_role") == "primary":
            raise ValueError("this block position already has its primary candidate outcome")
        if disposition.get("retryable") is not True:
            raise ValueError("the prior attempt is not retryable under the frozen policy")

    attempt_number = len(matching_results) + 1
    expected_attempt_id = f"{block_id}-{language}-{attempt_number:02d}"
    if attempt_id != expected_attempt_id:
        raise ValueError(f"attempt_id must be {expected_attempt_id}")

    image_probe = run_process(
        ["docker", "image", "inspect", protocol["image"], "--format", "{{.Id}}"],
        cwd=root,
        timeout=30,
    )
    if not image_probe.ok or image_probe.stdout.strip() != protocol["image_id"]:
        raise ValueError("Docker image tag does not match frozen image ID")

    if position == 2 and not any(
        _retained_position_one(
            prior,
            protocol=protocol,
            block_id=block_id,
            order=order,
            first_language=block["order"][0],
        )
        for prior in retained
    ):
        raise ValueError("a completed position-1 outcome must be retained before position-2")

    wrapper = root / "scripts" / "codex-docker.py"
    command = (
        f'"{sys.executable}" "{wrapper}" --workspace "{{workspace}}" '
        f'--prompt-file "{{prompt_file}}" --model "{definition["model"]["snapshot"]}" '
        f'--reasoning-effort "{definition["model"]["reasoning_effort"]}" '
        f'--image "{definition["codex"]["image"]}" '
        f'--memory "{definition["limits"]["memory"]}" '
        f'--cpus {definition["limits"]["cpus"]} '
        f'--pids-limit {definition["limits"]["pids"]} '
        "--require-auth-preflight"
    )
    return protocol, command, attempt_number


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
    protocol_manifest: Path | None = None,
    block_id: str | None = None,
    order: str | None = None,
    attempt_id: str | None = None,
    position: int | None = None,
) -> Path:
    protocol_args = (block_id, order, attempt_id, position)
    if protocol_manifest is None and any(value is not None for value in protocol_args):
        raise ValueError("protocol block/order/attempt/position require --protocol-manifest")
    if require_usage and agent_name != "command":
        raise ValueError("--require-usage is valid only with --agent command")
    if language not in manifest["languages"]:
        raise ValueError(f"Unsupported language {language!r}; choose from {sorted(manifest['languages'])}")

    provenance: dict[str, Any] | None = None
    attempt_number: int | None = None
    if protocol_manifest is not None:
        provenance, agent_command, attempt_number = _prepare_protocol_run(
            root=root,
            benchmark_manifest=manifest,
            language=language,
            agent_name=agent_name,
            output_root=output_root,
            model=model,
            agent_command=agent_command,
            timeout=timeout,
            max_tasks=max_tasks,
            require_usage=require_usage,
            protocol_manifest=protocol_manifest,
            block_id=block_id,
            order=order,
            attempt_id=attempt_id,
            position=position,
        )

    if provenance is not None:
        assert attempt_id is not None
        run_id = attempt_id
        run_dir = _reserve_protocol_run_directory(output_root, attempt_id)
    else:
        run_id = (
            f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-"
            f"{language}-{agent_name}-{uuid.uuid4().hex[:8]}"
        )
        run_dir = output_root / run_id
        run_dir.mkdir(parents=True, exist_ok=False)
    workspace = run_dir / "workspace"
    run_started_at = utc_now()
    run_started_monotonic = time.monotonic()

    run_provenance = None
    attempt_record_path: Path | None = None
    attempt_record: dict[str, Any] | None = None
    if provenance is not None:
        run_provenance = {
            "manifest_file": "protocol-manifest.json",
            "manifest_sha256": provenance["manifest_sha256"],
            "cell_id": provenance["cell_id"],
            "git_head": provenance["git_head"],
            "definition_sha256": provenance["definition_sha256"],
            "schedule_sha256": provenance["schedule_sha256"],
            "image": provenance["image"],
            "image_id": provenance["image_id"],
            "model": provenance["definition"]["model"]["snapshot"],
            "reasoning_effort": provenance["definition"]["model"]["reasoning_effort"],
            "block_id": block_id,
            "order": order,
            "position": position,
            "attempt_id": attempt_id,
            "attempt_number": attempt_number,
            "language": language,
        }
        copied = run_dir / "protocol-manifest.json"
        copied.write_bytes(Path(protocol_manifest).read_bytes())
        attempt_record_path = run_dir / "attempt.json"
        attempt_record = {
            "schema_version": 1,
            "run_id": run_id,
            "started_at": run_started_at,
            "state": "started",
            "provenance": run_provenance,
        }
        attempt_record_path.write_text(
            json.dumps(attempt_record, indent=2, sort_keys=True), encoding="utf-8"
        )

    init_workspace(root, manifest, language, workspace)
    cfg = manifest["languages"][language]
    agent = make_agent(
        agent_name,
        model=model,
        agent_command=agent_command,
        require_usage=require_usage,
        expected_protocol=provenance,
    )

    baseline_started = time.monotonic()
    baseline = evaluate_project(
        workspace,
        cfg,
        manifest["baseline_cases"],
        timeout=min(timeout, 300),
    )
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
        "evaluator_wall_seconds": baseline["evaluator_wall_seconds"],
        "run_total_wall_seconds": None,
        "aggregate_usage": None,
        "aggregate_usage_available": False,
        "aggregate_accounting_valid": False,
        "require_usage": require_usage,
        "provenance": run_provenance,
    }
    if not baseline["ok"]:
        run_result["run_total_wall_seconds"] = time.monotonic() - run_started_monotonic
        run_result["finished_at"] = utc_now()
        if provenance is not None:
            run_result["disposition"] = _derive_protocol_disposition(run_result)
        (run_dir / "result.json").write_text(
            json.dumps(run_result, indent=2, sort_keys=True), encoding="utf-8"
        )
        if attempt_record is not None and attempt_record_path is not None:
            attempt_record.update(
                {
                    "state": "completed",
                    "finished_at": run_result["finished_at"],
                    "disposition": run_result["disposition"],
                }
            )
            attempt_record_path.write_text(
                json.dumps(attempt_record, indent=2, sort_keys=True), encoding="utf-8"
            )
        return run_dir

    cumulative_cases = list(manifest["baseline_cases"])
    tasks = manifest["tasks"][:max_tasks] if max_tasks is not None else manifest["tasks"]
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
        aggregate_accounting_valid = (
            aggregate_accounting_valid and agent_result.accounting_valid
        )
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
        evaluation = evaluate_project(
            workspace,
            cfg,
            cumulative_cases,
            timeout=min(timeout, 300),
        )
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
            for argv in (
                ["git", "add", "."],
                ["git", "commit", "-q", "-m", task["id"]],
            ):
                commit = run_process(argv, cwd=workspace, timeout=30)
                if not commit.ok:
                    task_ok = False
                    task_result["success"] = False
                    task_result["commit_error"] = commit.stderr
                    break
            task_result["post_commit"] = git_head(workspace)

        task_result["task_total_wall_seconds"] = time.monotonic() - task_started_monotonic
        task_result["finished_at"] = utc_now()
        (task_dir / "task-result.json").write_text(
            json.dumps(task_result, indent=2, sort_keys=True), encoding="utf-8"
        )
        run_result["tasks"].append(task_result)
        if not task_ok:
            break

    run_result["aggregate_usage"] = (
        aggregate_usage.to_dict() if aggregate_usage_available else None
    )
    run_result["aggregate_usage_available"] = aggregate_usage_available
    run_result["aggregate_accounting_valid"] = aggregate_accounting_valid
    run_result["finished_at"] = utc_now()
    run_result["run_total_wall_seconds"] = time.monotonic() - run_started_monotonic
    run_result["success"] = len(run_result["tasks"]) == len(tasks) and all(
        task["success"] for task in run_result["tasks"]
    )
    if provenance is not None:
        run_result["disposition"] = _derive_protocol_disposition(run_result)
    (run_dir / "result.json").write_text(
        json.dumps(run_result, indent=2, sort_keys=True), encoding="utf-8"
    )
    if attempt_record is not None and attempt_record_path is not None:
        attempt_record.update(
            {
                "state": "completed",
                "finished_at": run_result["finished_at"],
                "disposition": run_result["disposition"],
            }
        )
        attempt_record_path.write_text(
            json.dumps(attempt_record, indent=2, sort_keys=True), encoding="utf-8"
        )
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
