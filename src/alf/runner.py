from __future__ import annotations

import json
import os
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
from .environment_profile import environment_profile_sha256, load_environment_profile
from .metrics import git_diff_metrics, git_head, snapshot_repository
from .models import AgentResult, Usage
from .process import run_process
from .benchmark_artifacts import artifact_plan, checks_for_language, copy_artifacts, merge_workspace_checks
from .protocol import canonical_json_hash, classify_failure, load_frozen_manifest
from .audit import audit_representation_checkpoint


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def route_profile_identity(
    root: Path, provenance: dict[str, Any]
) -> tuple[str, str | None]:
    """Return the exact non-secret route profile used by a protocol run."""
    configured = os.environ.get("ALF_ENVIRONMENT_PROFILE_PATH")
    profile_path: Path | None = None
    if provenance.get("schema_version") == 3:
        tracked = root / "infra" / "remote-runner" / "environment-profile.json"
        if tracked.is_file():
            profile_path = tracked
            if configured:
                requested = Path(configured).expanduser()
                if not requested.is_absolute():
                    requested = root / requested
                if requested.resolve() != tracked.resolve():
                    raise ValueError(
                        "schema-v3 environment profile must be the tracked remote-runner profile"
                    )
    elif configured:
        profile_path = Path(configured).expanduser()
        if not profile_path.is_absolute():
            profile_path = root / profile_path
    if profile_path is not None:
        profile = load_environment_profile(profile_path, repository_root=root)
        return "sha256:" + environment_profile_sha256(profile), profile["profile_id"]

    # Compatibility identity for older frozen fixtures and local protocol families.
    legacy = {
        "schema_version": 0,
        "network_policy": provenance.get("definition", {}).get("network_policy"),
    }
    return "sha256:" + canonical_json_hash(legacy), None


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
        "auth_cache_staged": result.auth_cache_staged,
        "auth_cleanup_ok": result.auth_cleanup_ok,
        "route_profile_sha256": result.route_profile_sha256,
        "environment_profile_id": result.environment_profile_id,
        "container_limits": result.container_limits,
        "host_memory": result.host_memory,
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
    required_position: int = 1,
    condition: str | None = None,
) -> bool:
    """Return whether a result is an eligible retained predecessor outcome."""

    provenance = result.get("provenance")
    baseline = result.get("baseline")
    tasks = result.get("tasks")
    if not isinstance(provenance, dict) or not isinstance(baseline, dict):
        return False
    if baseline.get("ok") is not True or not result.get("finished_at"):
        return False
    if not isinstance(tasks, list) or not tasks or not all(
        isinstance(task, dict) and task.get("finished_at") for task in tasks
    ):
        return False
    same_attempt_context = (
        provenance.get("cell_id") == protocol.get("cell_id")
        and provenance.get("manifest_sha256") == protocol.get("manifest_sha256")
        and provenance.get("block_id") == block_id
        and provenance.get("order") == order
        and provenance.get("position") == required_position
        and provenance.get("language") == first_language
    )
    if not same_attempt_context:
        return False
    disposition = result.get("disposition")
    if condition is not None and provenance.get("condition") != condition:
        return False
    if not isinstance(disposition, dict) or disposition.get("analysis_role") != "primary":
        return False
    if protocol.get("schema_version") == 2:
        # Candidate correctness, timeout, and accounting failures remain immutable
        # primary outcomes. Apparatus failures never authorize the next position.
        if (
            disposition.get("protocol_valid") is not True
            or disposition.get("candidate_outcome") is not True
            or disposition.get("retryable") is not False
        ):
            return False
        baseline_audit = result.get("representation_audit")
        if (
            not isinstance(baseline_audit, dict)
            or baseline_audit.get("ok") is not True
            or baseline_audit.get("representation_interpretable") is not True
        ):
            return False
        if any(
            not isinstance(task.get("representation_audit"), dict)
            or task["representation_audit"].get("ok") is not True
            for task in tasks
        ):
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
    host_ok = host_ok and not any(
        isinstance(agent.get("host_memory"), dict) and agent["host_memory"].get("ok") is False
        for agent in task_agents
    )
    timed_out = any(
        process.get("timed_out") is True
        for process in [*task_processes, *task_evaluator_processes]
    )
    auth_ok = not any(
        agent.get("auth_ok") is False or agent.get("auth_cleanup_ok") is False
        for agent in task_agents
    )
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
    monitored = (
        isinstance(run_result.get("provenance"), dict)
        and run_result["provenance"].get("cell_id") == "difficulty-v1"
    )
    baseline_audit = run_result.get("representation_audit")
    task_audits = [
        task.get("representation_audit")
        for task in tasks
        if isinstance(task, dict)
    ]
    representation_protocol_ok = True
    if monitored:
        representation_protocol_ok = (
            isinstance(baseline_audit, dict)
            and baseline_audit.get("ok") is True
            and baseline_audit.get("representation_interpretable") is True
            and len(task_audits) == len(tasks)
            and all(
                isinstance(audit, dict) and audit.get("ok") is True
                for audit in task_audits
            )
        )
    protocol_ok = (
        isinstance(run_result.get("provenance"), dict)
        and sidecar_protocol_ok
        and representation_protocol_ok
    )
    category = classify_failure(
        protocol_ok=(
            protocol_ok
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
    audits = [baseline_audit, *task_audits]
    audit_interpretable = (
        all(
            isinstance(audit, dict)
            and audit.get("ok") is True
            and audit.get("representation_interpretable") is True
            for audit in audits
        )
        if monitored
        else True
    )
    disposition = {
        "protocol_valid": protocol_ok,
        "failure_category": category,
        "classification_basis": "frozen deterministic runner rules",
        "candidate_outcome": candidate_outcome,
        "analysis_role": "primary" if candidate_outcome else "infrastructure-invalid",
        "retryable": category in infrastructure_categories,
        "include_success_time": candidate_outcome,
        "include_usage_metrics": usage_included,
        "include_paired_performance": candidate_outcome,
    }
    if monitored:
        disposition.update(
            {
                "representation_interpretable": audit_interpretable,
                "include_representation_analysis": audit_interpretable,
            }
        )
    return disposition


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
        or not isinstance(position, int) or isinstance(position, bool) or position < 1
        or (order not in {"csharp-first", "fsharp-first"} and not re.fullmatch(r"williams-\d{2}", order or ""))
    ):
        raise ValueError(
            "protocol runs require a safe attempt_id, block_id, position, and "
            "legacy order or safe Williams order_id"
        )

    protocol = load_frozen_manifest(root, protocol_manifest)
    # Keep v2/v3 frozen manifests immutable; v1 callers historically receive identity.
    if protocol.get("schema_version") in {2, 3}:
        protocol = dict(protocol)
    definition = protocol["definition"]
    schedule = protocol["schedule"]

    v2 = protocol.get("schema_version") == 2
    v3 = protocol.get("schema_version") == 3
    selected_condition = None
    if v2:
        blocks = schedule.get("pilot") or []
        block = next((item for item in blocks if item.get("block_id") == block_id), None)
        if block is None or order != block.get("order_id") or position > len(block.get("order", [])):
            raise ValueError("protocol block/order/position mismatch")
        selected_condition = block["order"][position - 1]
        expected_language = selected_condition.split("-", 1)[0]
        if language != expected_language:
            raise ValueError("protocol condition/language mismatch")
        spec = definition.get("conditions", {}).get(selected_condition, {})
        benchmark_path = (root / (spec.get("manifest") or spec.get("manifest_path"))).resolve()
    else:
        benchmark_path = (root / definition["benchmark_manifest"]).resolve()
    try:
        tracked_benchmark = json.loads(benchmark_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"tracked benchmark manifest is unavailable: {exc}") from exc
    if benchmark_manifest != tracked_benchmark:
        raise ValueError("loaded benchmark does not match the frozen protocol")

    if v2:
        blocks = [*schedule.get("pilot", [])]
    elif v3:
        configuration = definition.get("configuration_id")
        if configuration not in {"H", "M", "L"}:
            raise ValueError(
                "schema-v3 protocol manifest must identify a child configuration"
            )
        if protocol.get("configuration_id") != configuration or protocol.get(
            "family_id"
        ) != definition.get("family_id"):
            raise ValueError("protocol family/configuration identity mismatch")
        blocks = [
            row
            for row in [
                *schedule.get("calibration", []),
                *schedule.get("formal", []),
            ]
            if row.get("configuration_id") == configuration
        ]
    else:
        blocks = [schedule["calibration"], *schedule["formal"]]
    block = next((item for item in blocks if item.get("block_id") == block_id), None)
    if block is None:
        raise ValueError("protocol block is not in the frozen schedule")
    if not v2:
        if position > len(block["order"]):
            raise ValueError("protocol position is invalid")
        expected_order = f"{block['order'][0]}-first"
        expected_language = block["order"][position - 1]
        if order != expected_order or language != expected_language:
            raise ValueError("protocol block/language/order mismatch")

    raw_root = (root / definition["raw_root"]).resolve()
    if output_root.resolve() != raw_root:
        raise ValueError("protocol output must be the definition's raw_root")
    requested_model = (
        definition["model"]["requested_id"] if v3 else definition["model"]["snapshot"]
    )
    if model != requested_model:
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
    attempt_label = selected_condition if v2 else language
    expected_attempt_id = f"{block_id}-{attempt_label}-{attempt_number:02d}"
    if attempt_id != expected_attempt_id:
        raise ValueError(f"attempt_id must be {expected_attempt_id}")

    image_probe = run_process(
        ["docker", "image", "inspect", protocol["image"], "--format", "{{.Id}}"],
        cwd=root,
        timeout=30,
    )
    if not image_probe.ok or image_probe.stdout.strip() != protocol["image_id"]:
        raise ValueError("Docker image tag does not match frozen image ID")

    if position > 1 and not any(
        _retained_position_one(
            prior,
            protocol=protocol,
            block_id=block_id,
            order=order,
            first_language=(block["order"][position - 2].split("-", 1)[0] if v2 else block["order"][position - 2]),
            required_position=position - 1,
            condition=(block["order"][position - 2] if v2 else None),
        )
        for prior in retained
    ):
        raise ValueError(
            "an eligible immediate predecessor (position-1 for position-2) "
            "must be retained before this position"
        )

    wrapper = root / "scripts" / "codex-docker.py"
    command = (
        f'"{sys.executable}" "{wrapper}" --workspace "{{workspace}}" '
        f'--prompt-file "{{prompt_file}}" --model "{requested_model}" '
        f'--reasoning-effort "{definition["model"]["reasoning_effort"]}" '
        f'--image "{definition["codex"]["image"]}" '
        f'--memory "{definition["limits"]["memory"]}" '
        f'--cpus {definition["limits"]["cpus"]} '
        f'--pids-limit {definition["limits"]["pids"]} '
        "--require-auth-preflight"
    )
    if v3 and (root / "infra" / "remote-runner" / "environment-profile.json").is_file():
        route_sha256, route_profile_id = route_profile_identity(root, protocol)
        protocol["_route_profile_sha256"] = route_sha256
        protocol["_environment_profile_id"] = route_profile_id
        protocol["_require_auth_cleanup"] = True
        command += " --environment-profile infra/remote-runner/environment-profile.json"
    if v2:
        protocol["_selected_condition"] = selected_condition
        protocol["_condition_manifest"] = str(benchmark_path.relative_to(root)).replace("\\", "/")
        protocol["_condition_manifest_sha256"] = definition["conditions"][selected_condition].get("manifest_sha256")
    if v3:
        protocol["_workstream_d_row"] = block
        protocol["_workstream_d_config"] = definition["configuration_id"]
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
        environment_facts = provenance.get("environment")
        if not isinstance(environment_facts, dict):
            # Compatibility for older frozen fixtures; real freezes embed the
            # complete environment probe.
            environment_facts = {
                "image": provenance["image"],
                "image_id": provenance["image_id"],
            }
        route_profile_sha256 = provenance.get("_route_profile_sha256")
        environment_profile_id = provenance.get("_environment_profile_id")
        if not isinstance(route_profile_sha256, str):
            route_profile_sha256, environment_profile_id = route_profile_identity(
                root, provenance
            )
        combined_environment = {
            "observed": environment_facts,
            "route_profile_sha256": route_profile_sha256,
        }
        run_provenance = {
            "manifest_file": "protocol-manifest.json",
            "manifest_sha256": provenance["manifest_sha256"],
            "cell_id": provenance["cell_id"],
            "git_head": provenance["git_head"],
            "definition_sha256": provenance["definition_sha256"],
            "scientific_spec_sha256": provenance["definition_sha256"],
            "runner_revision": provenance["git_head"],
            "environment_profile": "sha256:"
            + canonical_json_hash(combined_environment),
            "environment_profile_id": environment_profile_id,
            "route_profile_sha256": route_profile_sha256,
            "schedule_sha256": provenance["schedule_sha256"],
            "image": provenance["image"],
            "image_id": provenance["image_id"],
            "model": provenance["definition"]["model"].get(
                "snapshot", provenance["definition"]["model"].get("requested_id")
            ),
            "reasoning_effort": provenance["definition"]["model"]["reasoning_effort"],
            "block_id": block_id,
            "order": order,
            "position": position,
            "attempt_id": attempt_id,
            "attempt_number": attempt_number,
            "language": language,
        }
        if provenance.get("_selected_condition"):
            condition = provenance["_selected_condition"]
            scheduled_block = next(
                (
                    candidate
                    for candidate in provenance["schedule"].get("pilot", [])
                    if candidate.get("block_id") == block_id
                ),
                {},
            )
            run_provenance.update({
                "condition": condition,
                "representation": condition.split("-", 1)[1],
                "condition_manifest": provenance["_condition_manifest"],
                "condition_manifest_sha256": provenance["_condition_manifest_sha256"],
                "schedule_counting": scheduled_block.get("counting"),
                "schedule_role": scheduled_block.get("role"),
            })
        if provenance.get("schema_version") == 3:
            row = provenance["_workstream_d_row"]
            run_provenance.update(
                {
                    "family_id": provenance["family_id"],
                    "configuration_id": provenance["_workstream_d_config"],
                    "pair_block_id": row["block_id"],
                    "execution_position": position,
                    "macroblock": row.get("macroblock"),
                    "calibration_id": row.get("calibration_id"),
                    "within_macroblock_position": row.get("within_macroblock_position"),
                    "stage": row["stage"],
                    "role": row["role"],
                    "counting": row["counting"],
                    "schedule_role": row["role"],
                    "schedule_counting": row["counting"],
                    "assignment_sha256": provenance["assignment_sha256"],
                    "family_definition_sha256": provenance["family_definition_sha256"],
                    "parent_schedule_sha256": provenance["parent_schedule_sha256"],
                    "catalog_sha256": provenance["catalog_sha256"],
                }
            )
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
    tasks = manifest["tasks"][:max_tasks] if max_tasks is not None else manifest["tasks"]
    # Resolve every source, target, and check path before baseline/agent work.
    planned_artifacts = []
    planned_checks = []
    for task in tasks:
        planned_artifacts.append(artifact_plan(root, manifest, language, task, workspace))
        planned_checks.append(merge_workspace_checks(workspace, checks_for_language(task, language, set(manifest["languages"]))))
        for sibling_language in manifest["languages"]:
            merge_workspace_checks(workspace, checks_for_language(task, sibling_language, set(manifest["languages"])))
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
    representation_audit = None
    if provenance is not None and provenance.get("schema_version") == 2:
        artifact_root = root / "benchmarks" / "successor" / "representation-v1"
        _condition = provenance.get("_selected_condition", "")
        representation_audit = audit_representation_checkpoint(workspace, artifact_root, language, _condition.split("-", 1)[1] if "-" in _condition else None, "baseline")
        (run_dir / "representation-audit.json").write_text(json.dumps(representation_audit, indent=2, sort_keys=True), encoding="utf-8")
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
    if representation_audit is not None:
        run_result["representation_audit"] = representation_audit
        if not representation_audit.get("representation_interpretable"):
            run_result["finished_at"] = utc_now(); run_result["run_total_wall_seconds"] = time.monotonic() - run_started_monotonic
            run_result["success"] = False
            run_result["disposition"] = _derive_protocol_disposition(run_result)
            (run_dir / "result.json").write_text(json.dumps(run_result, indent=2, sort_keys=True), encoding="utf-8")
            if attempt_record is not None and attempt_record_path is not None:
                attempt_record.update({"state":"completed", "finished_at":run_result["finished_at"], "disposition":run_result["disposition"]})
                attempt_record_path.write_text(json.dumps(attempt_record, indent=2, sort_keys=True), encoding="utf-8")
            return run_dir
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
    condition = run_provenance.get("condition") if isinstance(run_provenance, dict) else None
    cumulative_checks: dict[str, Any] = {"file_exists": [], "text_contains": [], "text_not_contains": []}
    for task_index, task in enumerate(tasks):
        task_started_monotonic = time.monotonic()
        task_dir = run_dir / "tasks" / task["id"]
        prompt_path = root / task["prompt"]
        prompt = prompt_path.read_text(encoding="utf-8")
        pre = snapshot_repository(workspace)
        pre_head = git_head(workspace)
        task_started = utc_now()
        agent_task = dict(task)
        if agent_name == "scripted":
            agent_task["_artifact_context"] = {
                "manifest_parent": getattr(manifest, "manifest_parent", None)
            }
            agent_task["_artifact_plan"] = planned_artifacts[task_index]
        agent_kwargs = dict(
            root=root,
            workspace=workspace,
            language=language,
            language_config=cfg,
            task=agent_task,
            prompt=prompt,
            timeout=timeout,
        )
        if agent_name == "command":
            agent_kwargs["host_memory"] = (provenance or {}).get("definition", {}).get("host_memory")
        agent_result = agent.run(
            **agent_kwargs,
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
        task_checks = planned_checks[task_index]
        for check_key in cumulative_checks:
            cumulative_checks[check_key].extend(task_checks[check_key])
        evaluation_started = time.monotonic()
        evaluation = evaluate_project(
            workspace,
            cfg,
            cumulative_cases,
            timeout=min(timeout, 300),
            workspace_checks=cumulative_checks,
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
        if representation_audit is not None:
            task_audit = audit_representation_checkpoint(workspace, root / "benchmarks" / "successor" / "representation-v1", language, condition.split("-", 1)[1] if "-" in condition else None, task["id"])
            task_result["representation_audit"] = task_audit
            (task_dir / "representation-audit.json").write_text(json.dumps(task_audit, indent=2, sort_keys=True), encoding="utf-8")
            if task_audit.get("ok") is not True:
                task_ok = False
                task_result["success"] = False
                task_result["representation_checkpoint_failed"] = True
            elif task_audit.get("representation_interpretable") is not True:
                # Candidate-caused drift is observational: preserve correctness
                # and chain exposure while excluding representation analysis.
                task_result["representation_analysis_invalid"] = True
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
            planned = [artifact_plan(root, manifest, language, task, workspace) for task in manifest["tasks"]]
            planned_checks = []
            for task in manifest["tasks"]:
                for sibling_language in manifest["languages"]:
                    sibling_checks = checks_for_language(task, sibling_language, set(manifest["languages"]))
                    merge_workspace_checks(workspace, sibling_checks)
                planned_checks.append(merge_workspace_checks(workspace, checks_for_language(task, language, set(manifest["languages"]))))
            baseline = evaluate_project(workspace, cfg, manifest["baseline_cases"], timeout=timeout)
            language_report["baseline"] = baseline
            ok = baseline["ok"]
            cases = list(manifest["baseline_cases"])
            cumulative_checks: dict[str, Any] = {"file_exists": [], "text_contains": [], "text_not_contains": []}
            for task_index, task in enumerate(manifest["tasks"]):
                plan = planned[task_index]
                copy_artifacts(plan)
                cases.extend(task["cases"])
                checks = planned_checks[task_index]
                for check_key in cumulative_checks:
                    cumulative_checks[check_key].extend(checks[check_key])
                evaluation = evaluate_project(workspace, cfg, cases, timeout=timeout, workspace_checks=cumulative_checks)
                language_report["tasks"].append({"task_id": task["id"], "evaluation": evaluation})
                ok = ok and evaluation["ok"]
            language_report["ok"] = ok
            report["languages"][language] = language_report
            report["ok"] = report["ok"] and ok
    return report
