"""Deterministic, transcript-free post-hoc variance and power reporting."""
from __future__ import annotations

import hashlib
import itertools
import json
import math
import random
import statistics
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from statistics import NormalDist
from typing import Any, Iterable

from .runner import _derive_protocol_disposition

USAGE_METRICS = ("input_tokens", "cached_input_tokens", "output_tokens", "reasoning_output_tokens", "tool_calls")
TASK_METRICS = USAGE_METRICS + ("commands", "changed_files", "added_lines", "deleted_lines", "diff_bytes", "file_reads", "unique_file_reads", "file_revisits", "agent_process_wall_seconds", "evaluator_wall_seconds", "task_total_wall_seconds")
RUN_METRICS = TASK_METRICS + ("run_total_wall_seconds",)
PROVENANCE_FIELDS = {"attempt_id", "attempt_number", "block_id", "cell_id", "definition_sha256", "git_head", "image", "image_id", "language", "manifest_file", "manifest_sha256", "model", "order", "position", "reasoning_effort", "schedule_sha256"}
ATTEMPT_FIELDS = {"schema_version", "run_id", "state", "started_at", "finished_at", "provenance", "disposition"}
DISPOSITION_FIELDS = {"protocol_valid", "failure_category", "classification_basis", "candidate_outcome", "analysis_role", "retryable", "include_success_time", "include_usage_metrics", "include_paired_performance"}
INFRA_FAILURES = {"protocol", "auth", "provider", "host", "evaluator"}
SOURCE_SUFFIXES = {".fs", ".fsx", ".cs", ".fsproj", ".csproj", ".json", ".md"}
SOURCE_EXCLUDES = {".git", ".alf", "bin", "obj", "__pycache__"}


def _canon(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _hash(value: Any) -> str:
    return hashlib.sha256(_canon(value).encode()).hexdigest()


def _byte_hash(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _text_hash(value: bytes) -> str:
    text = value.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
    return _byte_hash(text.encode())


def _num(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) and value >= 0


def _utc(value: Any) -> datetime | None:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (AttributeError, ValueError):
        return None
    return parsed.astimezone(timezone.utc) if parsed.tzinfo else None


def _summary(values: Iterable[float | int]) -> dict[str, Any]:
    rows = list(values)
    return {"n": len(rows), "mean": statistics.mean(rows) if rows else None,
            "median": statistics.median(rows) if rows else None,
            "sample_sd": statistics.stdev(rows) if len(rows) > 1 else None,
            "sample_variance": statistics.variance(rows) if len(rows) > 1 else None,
            "minimum": min(rows) if rows else None, "maximum": max(rows) if rows else None}


def _counts(values: Iterable[Any]) -> dict[str, int]:
    result: dict[str, int] = {}
    for value in values:
        key = str(value)
        result[key] = result.get(key, 0) + 1
    return dict(sorted(result.items()))


def _series_seed(seed: int, label: str) -> int:
    return int.from_bytes(hashlib.sha256(f"{seed}:{label}".encode()).digest()[:8], "big")


def _bootstrap(values: list[float], samples: int, seed: int) -> dict[str, Any]:
    if not values:
        return {"observations": 0, "resamples": samples, "seed": seed, "mean": None,
                "descriptive": _summary([]), "ci_95": {"lower": None, "upper": None}}
    rng = random.Random(seed)
    means = sorted(statistics.mean(rng.choice(values) for _ in values) for _ in range(samples))
    def percentile(p: float) -> float:
        position = (samples - 1) * p
        low, high = math.floor(position), math.ceil(position)
        return means[low] if low == high else means[low] * (high - position) + means[high] * (position - low)
    return {"observations": len(values), "resamples": samples, "seed": seed,
            "mean": statistics.mean(values), "descriptive": _summary(values),
            "ci_95": {"lower": percentile(.025), "upper": percentile(.975)}}


def _pearson(left: list[float], right: list[float]) -> float | None:
    if len(left) < 2 or len(left) != len(right): return None
    lm, rm = statistics.mean(left), statistics.mean(right)
    numerator = sum((x-lm)*(y-rm) for x, y in zip(left, right))
    ls, rs = sum((x-lm)**2 for x in left), sum((y-rm)**2 for y in right)
    return numerator / math.sqrt(ls*rs) if ls and rs else None


def _trend(xs: list[float], ys: list[float]) -> dict[str, Any]:
    if len(xs) < 2: return {"n": len(xs), "slope": None, "pearson_r": None}
    xm, ym = statistics.mean(xs), statistics.mean(ys)
    denominator = sum((x-xm)**2 for x in xs)
    return {"n": len(xs), "slope": sum((x-xm)*(y-ym) for x, y in zip(xs, ys))/denominator if denominator else None,
            "pearson_r": _pearson(xs, ys)}


def _repo_root(cell: Path, definition_file: str) -> Path | None:
    # Post-hoc verification is against the frozen commit, not the current worktree.
    return next((p for p in (cell, *cell.parents) if (p / ".git").exists()), None)


def _git_blob(root: Path, commit: Any, relative: Any) -> bytes | None:
    if not isinstance(commit, str) or not isinstance(relative, str) or Path(relative).is_absolute() or ".." in Path(relative).parts: return None
    result = subprocess.run(["git", "show", f"{commit}:{Path(relative).as_posix()}"], cwd=root,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    return result.stdout if result.returncode == 0 else None


def _manifest(cell: Path) -> tuple[dict, bytes, dict, list[str]]:
    errors: list[str] = []
    raw = (cell / "resolved-manifest.json").read_bytes()
    value = json.loads(raw.decode())
    if not isinstance(value, dict): raise ValueError("resolved-manifest.json must contain an object")
    unsigned = dict(value); claimed = unsigned.pop("manifest_sha256", None)
    if claimed != _hash(unsigned): errors.append("manifest: canonical self-hash mismatch")
    if value.get("schema_version") != 1: errors.append("manifest: unsupported schema_version")
    if value.get("frozen") is not True or value.get("dirty") is not False: errors.append("manifest: not a clean frozen manifest")
    definition, schedule = value.get("definition"), value.get("schedule")
    if not isinstance(definition, dict) or not isinstance(schedule, dict):
        errors.append("manifest: embedded definition and schedule must be objects")
        return value, raw, {"manifest_file_sha256": _byte_hash(raw)}, errors
    if value.get("cell_id") != definition.get("cell_id") or value.get("cell_id") != schedule.get("cell_id"):
        errors.append("manifest: embedded cell identifiers disagree")
    definition_file, schedule_file = value.get("definition_file"), definition.get("schedule_file")
    sources: dict[str, Any] = {"manifest_file_sha256": _byte_hash(raw), "git_head": value.get("git_head")}
    if not isinstance(definition_file, str) or not isinstance(schedule_file, str):
        errors.append("manifest: definition_file or schedule_file is invalid"); return value, raw, sources, errors
    root = _repo_root(cell, definition_file)
    if root is None:
        errors.append("manifest: repository root for canonical frozen sources was not found"); return value, raw, sources, errors
    db, sb = _git_blob(root, value.get("git_head"), definition_file), _git_blob(root, value.get("git_head"), schedule_file)
    if db is None or sb is None:
        errors.append("manifest: canonical definition or schedule is absent from frozen git_head"); return value, raw, sources, errors
    sources.update({"definition": {"path": Path(definition_file).as_posix(), "sha256": _text_hash(db)},
                    "schedule": {"path": Path(schedule_file).as_posix(), "sha256": _text_hash(sb)}})
    try: canonical_definition, canonical_schedule = json.loads(db), json.loads(sb)
    except json.JSONDecodeError:
        errors.append("manifest: canonical definition or schedule is invalid JSON"); return value, raw, sources, errors
    if definition != canonical_definition: errors.append("manifest: embedded definition differs from frozen git source")
    if schedule != canonical_schedule: errors.append("manifest: embedded schedule differs from frozen git source")
    if value.get("definition_sha256") != _text_hash(db): errors.append("manifest: definition_sha256 differs from frozen git source")
    if value.get("schedule_sha256") != _text_hash(sb): errors.append("manifest: schedule_sha256 differs from frozen git source")
    benchmark_file = definition.get("benchmark_manifest")
    bb = _git_blob(root, value.get("git_head"), benchmark_file)
    if bb is None: errors.append("manifest: frozen benchmark manifest is unavailable")
    else:
        sources["benchmark_manifest"] = {"path": Path(benchmark_file).as_posix(), "sha256": _text_hash(bb)}
        if definition.get("benchmark_manifest_sha256") != _text_hash(bb): errors.append("manifest: frozen benchmark manifest hash mismatch")
        try: benchmark = json.loads(bb)
        except json.JSONDecodeError: benchmark = {}; errors.append("manifest: frozen benchmark manifest is invalid JSON")
        task_hashes, actual, task_order = definition.get("task_hashes"), {}, []
        for task in benchmark.get("tasks", []) if isinstance(benchmark, dict) else []:
            if not isinstance(task, dict) or not isinstance(task.get("id"), str) or not isinstance(task.get("prompt"), str): continue
            task_order.append(task["id"])
            blob = _git_blob(root, value.get("git_head"), task["prompt"])
            if blob is None: errors.append(f"manifest: frozen prompt is unavailable for {task['id']}"); continue
            digest = _text_hash(blob); actual[task["id"]] = {"path": Path(task["prompt"]).as_posix(), "sha256": digest}
            if not isinstance(task_hashes, dict) or task_hashes.get(task["id"]) != digest: errors.append(f"manifest: frozen prompt hash mismatch for {task['id']}")
        if not isinstance(task_hashes, dict) or set(task_hashes) != set(actual): errors.append("manifest: frozen task hash identifiers are incomplete")
        sources["task_prompts"] = actual; sources["benchmark_task_order"] = task_order
    sources["source_set_sha256"] = _hash(sources)
    return value, raw, sources, errors


def _schedule(manifest: dict, errors: list[str]) -> list[dict]:
    schedule = manifest.get("schedule") if isinstance(manifest.get("schedule"), dict) else {}
    if schedule.get("schema_version") != 1: errors.append("schedule: unsupported schema_version")
    if schedule.get("cell_id") != manifest.get("cell_id"): errors.append("schedule: cell_id differs from manifest")
    rows = []
    calibration = schedule.get("calibration")
    if isinstance(calibration, dict):
        rows.append({**calibration, "calibration": True, "block_index": 0})
        if calibration.get("counting") is not False: errors.append("schedule: calibration must be explicitly non-counting")
    else: errors.append("schedule: calibration block is missing")
    formal = schedule.get("formal")
    if not isinstance(formal, list): errors.append("schedule: formal blocks must be a list"); formal = []
    rows.extend({**row, "calibration": False, "block_index": i} for i, row in enumerate(formal, 1) if isinstance(row, dict))
    ids = [row.get("block_id") for row in rows]
    if any(not isinstance(x, str) for x in ids) or len(ids) != len(set(ids)): errors.append("schedule: block identifiers must be unique strings")
    for row in rows:
        if row.get("order") not in (["fsharp", "csharp"], ["csharp", "fsharp"]): errors.append(f"schedule: {row.get('block_id')} must contain both languages exactly once")
    constraints = schedule.get("constraints") if isinstance(schedule.get("constraints"), dict) else {}
    if constraints.get("formal_blocks") != len(formal): errors.append("schedule: formal block count disagrees with constraints")
    valid_orders = [row.get("order") for row in rows if not row.get("calibration") and row.get("order") in (["fsharp", "csharp"], ["csharp", "fsharp"])]
    first_counts = _counts(order[0] for order in valid_orders)
    declared_balance = constraints.get("balanced_first_language")
    if not isinstance(declared_balance, dict) or first_counts != {key: declared_balance[key] for key in sorted(declared_balance)}:
        errors.append("schedule: actual first-language balance disagrees with constraints")
    max_run = constraints.get("max_same_order_run")
    if not isinstance(max_run, int) or isinstance(max_run, bool) or max_run <= 0:
        errors.append("schedule: max_same_order_run must be a positive integer")
    else:
        run_length = 0; previous = None
        for order in valid_orders:
            run_length = run_length + 1 if order[0] == previous else 1; previous = order[0]
            if run_length > max_run:
                errors.append("schedule: actual order exceeds max_same_order_run constraint"); break
    return rows


def _source_tree(run: Path) -> dict:
    files = []
    workspace = run / "workspace"
    if workspace.is_dir():
        for path in sorted(workspace.rglob("*")):
            relative = path.relative_to(workspace)
            if path.is_file() and path.suffix.lower() in SOURCE_SUFFIXES and not any(part in SOURCE_EXCLUDES for part in relative.parts):
                raw = path.read_bytes(); files.append({"path": relative.as_posix(), "bytes": len(raw), "sha256": _byte_hash(raw)})
    return {"file_count": len(files), "files": files, "tree_sha256": _hash(files)}


def _artifact_hashes(run: Path, cell: Path) -> dict:
    paths = [run/"protocol-manifest.json", run/"attempt.json", run/"result.json"]
    paths += sorted((run/"tasks").glob("*/task-result.json")) + sorted((run/"tasks").glob("*/usage.json"))
    rows = []
    for path in paths:
        if path.is_file():
            raw = path.read_bytes(); rows.append({"path": path.relative_to(cell).as_posix(), "bytes": len(raw), "sha256": _byte_hash(raw)})
    return {"files": rows, "set_sha256": _hash(rows)}


def _derived_envelope_audit(run: Path, result: dict) -> dict:
    """Reconcile copied JSON envelopes without opening stdout, stderr, or events."""
    errors = []
    tasks = result.get("tasks") if isinstance(result.get("tasks"), list) else []
    usage_names = (*USAGE_METRICS[:-1], "cache_write_input_tokens", USAGE_METRICS[-1])
    total = {name: 0 for name in usage_names}
    validities, availabilities = [], []
    for embedded in tasks:
        if not isinstance(embedded, dict): errors.append("non-object task envelope"); continue
        task_id = embedded.get("task_id"); directory = run / "tasks" / str(task_id)
        try: copied = json.loads((directory / "task-result.json").read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError): errors.append(f"{task_id}: invalid or missing task-result.json"); continue
        if copied != embedded: errors.append(f"{task_id}: task-result differs from embedded task")
        agent = embedded.get("agent") if isinstance(embedded.get("agent"), dict) else {}
        valid, available = agent.get("accounting_valid") is True, agent.get("usage_available") is True
        validities.append(valid); availabilities.append(valid and available)
        usage = agent.get("usage") if isinstance(agent.get("usage"), dict) else None
        if (valid and available) != isinstance(usage, dict): errors.append(f"{task_id}: usage flags and envelope disagree")
        if isinstance(usage, dict):
            if any(not _num(usage.get(name)) for name in usage_names): errors.append(f"{task_id}: usage values are invalid")
            else:
                for name in usage_names: total[name] += usage[name]
            if usage["input_tokens"] < usage["cached_input_tokens"]: errors.append(f"{task_id}: cached input exceeds input")
            try: sidecar = json.loads((directory / "usage.json").read_text(encoding="utf-8"))
            except (OSError, UnicodeError, json.JSONDecodeError): errors.append(f"{task_id}: invalid or missing usage.json")
            else:
                if not isinstance(sidecar, dict) or any(sidecar.get(name) != usage.get(name) for name in usage_names):
                    errors.append(f"{task_id}: usage sidecar differs from task envelope")
        if not _num(embedded.get("task_total_wall_seconds")): errors.append(f"{task_id}: task timing is invalid")
    expected_valid = bool(validities) and all(validities); expected_available = bool(availabilities) and all(availabilities)
    if result.get("aggregate_accounting_valid") is not expected_valid: errors.append("aggregate accounting flag differs from tasks")
    if result.get("aggregate_usage_available") is not expected_available: errors.append("aggregate usage-available flag differs from tasks")
    if expected_available and result.get("aggregate_usage") != total: errors.append("aggregate usage differs from task sum")
    if not expected_available and result.get("aggregate_usage") is not None: errors.append("unavailable aggregate usage must be null")
    for name in ("agent_process_wall_seconds", "evaluator_wall_seconds", "run_total_wall_seconds"):
        if not _num(result.get(name)): errors.append(f"run timing {name} is invalid")
    return {"ok": not errors, "error_count": len(errors)}


def _task_metric(task: dict, name: str) -> Any:
    agent = task.get("agent") if isinstance(task.get("agent"), dict) else {}
    usage = agent.get("usage") if isinstance(agent.get("usage"), dict) else {}
    diff = task.get("diff") if isinstance(task.get("diff"), dict) else {}
    evaluation = task.get("evaluation") if isinstance(task.get("evaluation"), dict) else {}
    locations = {"commands": (agent, "command_count"), "changed_files": (diff, "changed_files"), "added_lines": (diff, "added_lines"),
                 "deleted_lines": (diff, "deleted_lines"), "diff_bytes": (diff, "diff_bytes"), "file_reads": (agent, "file_reads"),
                 "unique_file_reads": (agent, "unique_file_reads"), "file_revisits": (agent, "file_revisits"),
                 "agent_process_wall_seconds": (agent, "agent_process_wall_seconds"), "evaluator_wall_seconds": (evaluation, "evaluator_wall_seconds"),
                 "task_total_wall_seconds": (task, "task_total_wall_seconds")}
    value = usage.get(name) if name in USAGE_METRICS else locations[name][0].get(locations[name][1])
    return value if _num(value) else None


def _run_metric(result: dict, tasks: list[dict], name: str) -> Any:
    usage = result.get("aggregate_usage") if isinstance(result.get("aggregate_usage"), dict) else {}
    if name in USAGE_METRICS: value = usage.get(name)
    elif name in ("agent_process_wall_seconds", "evaluator_wall_seconds", "run_total_wall_seconds"): value = result.get(name)
    else:
        values = [_task_metric(task, name) for task in tasks]
        value = sum(values) if values and all(x is not None for x in values) else None
    return value if _num(value) else None


def _failure(task: dict) -> str | None:
    if task.get("success") is True: return None
    agent = task.get("agent") if isinstance(task.get("agent"), dict) else {}; process = agent.get("process") if isinstance(agent.get("process"), dict) else {}
    evaluation = task.get("evaluation") if isinstance(task.get("evaluation"), dict) else {}
    build = evaluation.get("build") if isinstance(evaluation.get("build"), dict) else {}; run = evaluation.get("run") if isinstance(evaluation.get("run"), dict) else {}
    if agent.get("accounting_valid") is False: return "accounting_invalid"
    if process.get("timed_out") is True: return "agent_timeout"
    if process.get("missing_executable") is True: return "agent_host_failure"
    if agent.get("ok") is False: return "agent_process_failure"
    if build.get("timed_out") is True or run.get("timed_out") is True: return "evaluator_timeout"
    if build.get("returncode") not in (None, 0): return "build_failure"
    if run.get("returncode") not in (None, 0): return "run_failure"
    if any(isinstance(case, dict) and case.get("passed") is False for case in evaluation.get("case_results", [])): return "behavioral_case_failure"
    return "task_failure"


def _task_row(task: dict, disposition: dict) -> dict:
    agent = task.get("agent") if isinstance(task.get("agent"), dict) else {}
    performance = disposition.get("include_paired_performance") is True
    usage = disposition.get("include_usage_metrics") is True and agent.get("accounting_valid") is True and agent.get("usage_available") is True
    metrics = {m: _task_metric(task, m) if performance and (m not in USAGE_METRICS or usage) else None for m in TASK_METRICS}
    return {"task_id": task.get("task_id"), "started_at": task.get("started_at"), "finished_at": task.get("finished_at"),
            "success": task.get("success") if disposition.get("include_success_time") is True else None,
            "failure_reason": _failure(task) if disposition.get("include_success_time") is True else None,
            "accounting_valid": agent.get("accounting_valid") is True, "usage_available": agent.get("usage_available") is True,
            "usage_record_count": agent.get("usage_record_count"), "fresh_process_recorded": isinstance(agent.get("process"), dict),
            "input_includes_cached_valid": metrics["input_tokens"] >= metrics["cached_input_tokens"] if _num(metrics["input_tokens"]) and _num(metrics["cached_input_tokens"]) else None,
            "metrics": metrics}


def _attempt(run: Path, cell: Path, manifest: dict, manifest_bytes: bytes, expected: dict,
             expected_task_ids: list[str], errors: list[str]) -> dict | None:
    rel = run.relative_to(cell).as_posix()
    if not (run/"result.json").is_file() or not (run/"attempt.json").is_file(): errors.append(f"{rel}: retained attempt is missing result.json or attempt.json"); return None
    try: result, envelope = json.loads((run/"result.json").read_text()), json.loads((run/"attempt.json").read_text())
    except (OSError, UnicodeError, json.JSONDecodeError) as exc: errors.append(f"{rel}: invalid retained JSON envelope ({type(exc).__name__})"); return None
    if not isinstance(result, dict) or not isinstance(envelope, dict): errors.append(f"{rel}: result and attempt envelopes must be objects"); return None
    provenance = result.get("provenance") if isinstance(result.get("provenance"), dict) else {}
    disposition = result.get("disposition") if isinstance(result.get("disposition"), dict) else {}
    if set(provenance) != PROVENANCE_FIELDS: errors.append(f"{rel}: provenance envelope fields are not exact")
    if set(envelope) != ATTEMPT_FIELDS: errors.append(f"{rel}: attempt envelope fields are not exact")
    if set(disposition) != DISPOSITION_FIELDS: errors.append(f"{rel}: disposition envelope fields are not exact")
    if envelope.get("schema_version") != 1 or envelope.get("state") != "completed": errors.append(f"{rel}: attempt envelope is not schema-1 completed")
    aid = provenance.get("attempt_id")
    if envelope.get("run_id") != result.get("run_id") or result.get("run_id") != aid or aid != run.name: errors.append(f"{rel}: directory, run, and attempt identifiers disagree")
    if envelope.get("provenance") != provenance or envelope.get("disposition") != disposition: errors.append(f"{rel}: attempt envelope differs from result envelope")
    for key in ("started_at", "finished_at"):
        if envelope.get(key) != result.get(key) or _utc(result.get(key)) is None: errors.append(f"{rel}: {key} is missing, non-UTC, or differs across envelopes")
    if result.get("language") != provenance.get("language"): errors.append(f"{rel}: result and provenance language disagree")
    copied = run/"protocol-manifest.json"
    if not copied.is_file() or copied.read_bytes() != manifest_bytes: errors.append(f"{rel}: copied protocol manifest is missing or not an exact byte copy")
    definition = manifest.get("definition", {}); model = definition.get("model", {}); codex = definition.get("codex", {})
    pins = {"cell_id": manifest.get("cell_id"), "manifest_sha256": manifest.get("manifest_sha256"), "definition_sha256": manifest.get("definition_sha256"),
            "schedule_sha256": manifest.get("schedule_sha256"), "git_head": manifest.get("git_head"), "model": model.get("snapshot"),
            "reasoning_effort": model.get("reasoning_effort"), "image": codex.get("image"), "image_id": manifest.get("image_id"), "manifest_file": "protocol-manifest.json"}
    for key, value in pins.items():
        if provenance.get(key) != value: errors.append(f"{rel}: provenance {key} does not match the frozen manifest")
    block = expected.get(provenance.get("block_id"))
    if block is None: errors.append(f"{rel}: attempt is not in the frozen schedule")
    else:
        order, position = block.get("order"), provenance.get("position")
        label = "fsharp-first" if order and order[0] == "fsharp" else "csharp-first"
        if provenance.get("order") != label: errors.append(f"{rel}: provenance order disagrees with the frozen schedule")
        if position not in (1, 2) or provenance.get("language") != order[position-1]: errors.append(f"{rel}: provenance position/language disagrees with the frozen schedule")
    number = provenance.get("attempt_number")
    if isinstance(number, int) and isinstance(provenance.get("block_id"), str) and provenance.get("language") in {"fsharp", "csharp"}:
        if aid != f"{provenance['block_id']}-{provenance['language']}-{number:02d}": errors.append(f"{rel}: attempt_id is not canonical")
    else: errors.append(f"{rel}: attempt number/block/language is invalid")
    try: derived = _derive_protocol_disposition(result)
    except Exception: derived = None
    if derived != disposition: errors.append(f"{rel}: disposition differs from frozen deterministic classification")
    raw_tasks = result.get("tasks") if isinstance(result.get("tasks"), list) else []
    recorded_task_ids = [task.get("task_id") for task in raw_tasks if isinstance(task, dict)]
    valid_early_stop = (
        result.get("success") is False
        and bool(raw_tasks)
        and isinstance(raw_tasks[-1], dict)
        and raw_tasks[-1].get("success") is False
        and recorded_task_ids == expected_task_ids[:len(recorded_task_ids)]
    )
    if len(recorded_task_ids) != len(raw_tasks) or len(set(recorded_task_ids)) != len(recorded_task_ids):
        errors.append(f"{rel}: task identifiers must be unique strings")
    if recorded_task_ids != expected_task_ids and not valid_early_stop:
        errors.append(f"{rel}: tasks are not the exact frozen order or a failure-terminated prefix")
    task_directories = sorted(path.name for path in (run / "tasks").iterdir() if path.is_dir()) if (run / "tasks").is_dir() else []
    if sorted(recorded_task_ids) != task_directories:
        errors.append(f"{rel}: retained task directories differ from the task envelope")
    tasks = [_task_row(task, disposition) for task in raw_tasks if isinstance(task, dict)]
    performance, usage = disposition.get("include_paired_performance") is True, disposition.get("include_usage_metrics") is True
    metrics = {m: _run_metric(result, raw_tasks, m) if performance and (m not in USAGE_METRICS or usage) else None for m in RUN_METRICS}
    if _num(metrics["input_tokens"]) and _num(metrics["cached_input_tokens"]) and metrics["input_tokens"] < metrics["cached_input_tokens"]: errors.append(f"{rel}: cached input exceeds input tokens")
    audit = _derived_envelope_audit(run, result)
    if disposition.get("analysis_role") == "primary" and audit["ok"] is not True: errors.append(f"{rel}: primary attempt fails derived-envelope audit")
    return {"attempt_id": aid, "path": rel, "block_id": provenance.get("block_id"), "block_index": block.get("block_index") if block else None,
            "calibration": block.get("calibration") if block else None, "language": provenance.get("language"), "position": provenance.get("position"),
            "order": provenance.get("order"), "attempt_number": number, "started_at": result.get("started_at"), "finished_at": result.get("finished_at"),
            "success": result.get("success") if disposition.get("include_success_time") is True else None, "failure_category": disposition.get("failure_category"),
            "disposition": disposition, "accounting_valid": result.get("aggregate_accounting_valid") is True, "usage_available": result.get("aggregate_usage_available") is True,
            "audit": audit, "metrics": metrics, "tasks": tasks,
            "artifact_hashes": _artifact_hashes(run, cell), "source_tree": _source_tree(run)}


def _primaries(attempts: list[dict], schedule: list[dict], errors: list[str]) -> list[dict]:
    groups: dict[tuple, list[dict]] = {}
    for row in attempts: groups.setdefault((row.get("block_id"), row.get("position"), row.get("language")), []).append(row)
    expected = {(block.get("block_id"), pos, lang) for block in schedule for pos, lang in enumerate(block.get("order") or [], 1)}
    for key in sorted(set(groups)-expected, key=str): errors.append(f"schedule: unscheduled attempt slot {key}")
    output = []
    for block in schedule:
        block_primary = []
        for pos, lang in enumerate(block.get("order") or [], 1):
            rows = sorted(groups.get((block.get("block_id"), pos, lang), []), key=lambda r: (r.get("attempt_number", 10**9), r.get("attempt_id", "")))
            if not rows: errors.append(f"schedule: missing retained attempt for {block.get('block_id')} position {pos}"); continue
            for n, row in enumerate(rows, 1):
                if row.get("attempt_number") != n: errors.append(f"{row.get('attempt_id')}: attempt numbering is not strictly sequential")
            primary_indexes = [i for i, row in enumerate(rows) if row["disposition"].get("analysis_role") == "primary"]
            if primary_indexes != [len(rows)-1]: errors.append(f"schedule: {block.get('block_id')} position {pos} must end in exactly one primary")
            for row in rows[:-1]:
                d = row["disposition"]
                if not (d.get("analysis_role") == "infrastructure-invalid" and d.get("retryable") is True and d.get("candidate_outcome") is False and d.get("failure_category") in INFRA_FAILURES and d.get("include_success_time") is False and d.get("include_usage_metrics") is False and d.get("include_paired_performance") is False):
                    errors.append(f"{row.get('attempt_id')}: only retryable infrastructure failures may precede a primary")
            if primary_indexes == [len(rows)-1]:
                primary = rows[-1]
                if primary["disposition"].get("retryable") is not False or primary["disposition"].get("candidate_outcome") is not True: errors.append(f"{primary.get('attempt_id')}: primary is not immutable")
                output.append(primary); block_primary.append(primary)
        first = next((row for row in block_primary if row.get("position") == 1), None)
        second_all = [row for row in attempts if row.get("block_id") == block.get("block_id") and row.get("position") == 2]
        if first and second_all and (min(_utc(row["started_at"]) for row in second_all) < _utc(first["finished_at"])): errors.append(f"schedule: {block.get('block_id')} did not execute position 1 before position 2")
    return sorted(output, key=lambda r: (r.get("block_index", 10**9), r.get("position", 10**9)))


def _language_stats(attempts: list[dict]) -> dict:
    output = {}; task_ids = sorted({t["task_id"] for a in attempts for t in a["tasks"] if isinstance(t.get("task_id"), str)})
    for language in ("fsharp", "csharp"):
        rows = [a for a in attempts if a.get("language") == language]; tasks = [t for a in rows for t in a["tasks"]]
        output[language] = {"chain_outcomes": {"n": len(rows), "successes": sum(a.get("success") is True for a in rows), "failures": sum(a.get("success") is False for a in rows), "failure_reasons": _counts(a.get("failure_category") for a in rows if a.get("failure_category"))},
                            "task_outcomes": {"n": len(tasks), "successes": sum(t.get("success") is True for t in tasks), "failures": sum(t.get("success") is False for t in tasks), "failure_reasons": _counts(t.get("failure_reason") for t in tasks if t.get("failure_reason"))},
                            "aggregate_metrics": {m: _summary(a["metrics"][m] for a in rows if _num(a["metrics"].get(m))) for m in RUN_METRICS}, "per_task": {}}
        for task_id in task_ids:
            selected = [t for t in tasks if t.get("task_id") == task_id]
            output[language]["per_task"][task_id] = {"outcomes": {"n": len(selected), "successes": sum(t.get("success") is True for t in selected), "failures": sum(t.get("success") is False for t in selected), "failure_reasons": _counts(t.get("failure_reason") for t in selected if t.get("failure_reason"))},
                                                           "metrics": {m: _summary(t["metrics"][m] for t in selected if _num(t["metrics"].get(m))) for m in TASK_METRICS}}
    return output


def _pair_metric(f: Any, c: Any) -> dict:
    return {"difference_fsharp_minus_csharp": f-c if _num(f) and _num(c) else None,
            "log_ratio_fsharp_over_csharp": math.log(f/c) if _num(f) and _num(c) and f > 0 and c > 0 else None}


def _pairs(formal: list[dict], schedule: list[dict]) -> list[dict]:
    result = []
    for block in (b for b in schedule if not b.get("calibration")):
        selected = {a.get("language"): a for a in formal if a.get("block_id") == block.get("block_id")}
        if set(selected) != {"fsharp", "csharp"}: continue
        f, c = selected["fsharp"], selected["csharp"]
        task_ids = sorted(set(t["task_id"] for t in f["tasks"]) & set(t["task_id"] for t in c["tasks"]))
        tasks = {}
        for task_id in task_ids:
            ft, ct = next(t for t in f["tasks"] if t["task_id"] == task_id), next(t for t in c["tasks"] if t["task_id"] == task_id)
            tasks[task_id] = {"outcomes": {"fsharp_success": ft["success"], "csharp_success": ct["success"]},
                              "metrics": {m: _pair_metric(ft["metrics"].get(m), ct["metrics"].get(m)) for m in TASK_METRICS}}
        result.append({"block_id": block["block_id"], "block_index": block["block_index"], "order": "fsharp-first" if block["order"][0] == "fsharp" else "fsharp-second",
                       "outcomes": {"fsharp_success": f["success"], "csharp_success": c["success"]}, "metrics": {m: _pair_metric(f["metrics"].get(m), c["metrics"].get(m)) for m in RUN_METRICS}, "tasks": tasks,
                       "started_at": min(f["started_at"], c["started_at"]), "finished_at": max(f["finished_at"], c["finished_at"]),
                       "within_block_start_spacing_seconds": abs((_utc(f["started_at"])-_utc(c["started_at"])).total_seconds())})
    return result


def _bootstrap_all(pairs: list[dict], samples: int, seed: int) -> dict:
    def level(rows: list[dict], prefix: str, metrics: tuple[str, ...]) -> dict:
        return {m: {field: _bootstrap([float(r["metrics"][m][field]) for r in rows if isinstance(r["metrics"][m].get(field), (int, float))], samples, _series_seed(seed, f"{prefix}:{m}:{field}"))
                    for field in ("difference_fsharp_minus_csharp", "log_ratio_fsharp_over_csharp")} for m in metrics}
    task_ids = sorted({tid for pair in pairs for tid in pair["tasks"]})
    return {"method": "deterministic nonparametric percentile bootstrap of paired-block means", "resamples": samples, "base_seed": seed,
            "aggregate": level(pairs, "aggregate", RUN_METRICS),
            "per_task": {tid: level([p["tasks"][tid] for p in pairs if tid in p["tasks"]], f"task:{tid}", TASK_METRICS) for tid in task_ids}}


def _diagnostics(pairs: list[dict], formal: list[dict]) -> dict:
    order = {label: {"blocks": len(selected := [p for p in pairs if p["order"] == label]),
                     "metrics": {m: _summary(p["metrics"][m]["difference_fsharp_minus_csharp"] for p in selected if isinstance(p["metrics"][m].get("difference_fsharp_minus_csharp"), (int, float))) for m in RUN_METRICS}}
             for label in ("fsharp-first", "fsharp-second")}
    position = {str(pos): {"attempts": len(selected := [a for a in formal if a["position"] == pos]),
                           "per_language": {lang: {m: _summary(a["metrics"][m] for a in selected if a["language"] == lang and _num(a["metrics"].get(m))) for m in RUN_METRICS} for lang in ("fsharp", "csharp")}} for pos in (1, 2)}
    temporal = {"blocks": [], "trends": {}}
    if pairs:
        origin = min(_utc(p["started_at"]) for p in pairs); previous = None
        for p in pairs:
            start, finish = _utc(p["started_at"]), _utc(p["finished_at"])
            temporal["blocks"].append({"block_id": p["block_id"], "block_index": p["block_index"], "started_at": p["started_at"], "finished_at": p["finished_at"],
                                       "elapsed_days_from_first": (start-origin).total_seconds()/86400, "within_block_start_spacing_seconds": p["within_block_start_spacing_seconds"],
                                       "block_elapsed_seconds": (finish-start).total_seconds(), "spacing_from_previous_block_start_seconds": None if previous is None else (start-previous).total_seconds()}); previous = start
        for m in RUN_METRICS:
            selected = [(p, p["metrics"][m]["difference_fsharp_minus_csharp"]) for p in pairs if isinstance(p["metrics"][m].get("difference_fsharp_minus_csharp"), (int, float))]
            ys = [float(v) for _, v in selected]
            temporal["trends"][m] = {"by_block_index": _trend([float(p["block_index"]) for p, _ in selected], ys),
                                      "by_utc_elapsed_day": _trend([(_utc(p["started_at"])-origin).total_seconds()/86400 for p, _ in selected], ys)}
    agreement = []
    for left, right in itertools.combinations(RUN_METRICS, 2):
        values = [(p["metrics"][left]["difference_fsharp_minus_csharp"], p["metrics"][right]["difference_fsharp_minus_csharp"]) for p in pairs if isinstance(p["metrics"][left].get("difference_fsharp_minus_csharp"), (int, float)) and isinstance(p["metrics"][right].get("difference_fsharp_minus_csharp"), (int, float))]
        nonzero = [(x, y) for x, y in values if x and y]
        agreement.append({"left": left, "right": right, "n": len(values), "sign_comparable_n": len(nonzero), "same_sign_n": sum((x>0)==(y>0) for x, y in nonzero),
                          "sign_agreement": sum((x>0)==(y>0) for x, y in nonzero)/len(nonzero) if nonzero else None,
                          "pearson_r": _pearson([float(x) for x, _ in values], [float(y) for _, y in values])})
    return {"order_strata": order, "position_strata": position, "temporal": temporal, "cross_metric_agreement": agreement}


def _known_sd_power(effect: float, residual_sd: float, n: int, *, alpha: float = .05) -> float:
    """Closed-form power for a two-sided z test with known positive SD."""
    if residual_sd <= 0 or n <= 0 or not 0 < alpha < 1:
        raise ValueError("known-SD power requires positive SD/n and 0 < alpha < 1")
    normal = NormalDist()
    critical = normal.inv_cdf(1-alpha/2)
    shift = abs(effect)*math.sqrt(n)/residual_sd
    return normal.cdf(-critical-shift) + 1-normal.cdf(critical-shift)


def _minimum_known_sd_n(effect: float, residual_sd: float, *, target: float = .8, alpha: float = .05) -> int:
    """Find the exact first integer n meeting target by monotone expansion/search."""
    if effect == 0 or not 0 < target < 1:
        raise ValueError("minimum known-SD n requires nonzero effect and 0 < target < 1")
    lower, upper = 1, 2
    while _known_sd_power(effect, residual_sd, upper, alpha=alpha) < target:
        lower, upper = upper, upper*2
    while lower+1 < upper:
        midpoint = (lower+upper)//2
        if _known_sd_power(effect, residual_sd, midpoint, alpha=alpha) >= target: upper = midpoint
        else: lower = midpoint
    return upper if _known_sd_power(effect, residual_sd, lower, alpha=alpha) < target else lower


def _power(pairs: list[dict], simulations: int, seed: int) -> dict:
    observations = [(p["metrics"]["input_tokens"]["log_ratio_fsharp_over_csharp"], p["order"]) for p in pairs if isinstance(p["metrics"]["input_tokens"].get("log_ratio_fsharp_over_csharp"), (int, float))]
    strata = sorted({order for _, order in observations})
    residuals = [value-statistics.mean(other for other, other_order in observations if other_order == order) for value, order in observations]
    df = len(residuals)-len(strata); sd = math.sqrt(sum(x*x for x in residuals)/df) if df > 0 else None
    alpha, target = .05, .80
    grid = [5, 10, 20, 30, 50, 75, 100, 150, 200, 250, 300, 400, 500, 750, 1000]
    effects = {}
    for ratio in (1.07, 1.08):
        effect = math.log(ratio)
        analytic = [{"n": n, "power": _known_sd_power(effect, sd, n, alpha=alpha) if sd else None} for n in grid]
        minimum = _minimum_known_sd_n(effect, sd, target=target, alpha=alpha) if sd else None
        simulation = []
        for n in grid:
            simulation_seed = _series_seed(seed, f"power:{ratio}:{n}")
            estimate = None
            if sd:
                rng = random.Random(simulation_seed); se = sd/math.sqrt(n); critical = NormalDist().inv_cdf(1-alpha/2)
                estimate = sum(abs(rng.gauss(effect, se))/se >= critical for _ in range(simulations))/simulations
            simulation.append({"n": n, "estimated_power": estimate, "simulations": simulations, "seed": simulation_seed})
        effects[f"{int(round((ratio-1)*100))}_percent"] = {
            "ratio": ratio, "log_effect": effect, "analytic_power_grid": analytic,
            "analytic_minimum_pairs_at_80_percent": minimum, "simulation_cross_check": simulation,
        }
    return {"outcome": "paired input-token log ratio (F#/C#)", "observations": len(observations), "order_strata": strata, "residual_degrees_of_freedom": df,
            "paired_log_ratio_residual_sd": sd, "residual_sd_assumption": "observed pilot residual SD after removing frozen order-stratum means",
            "alpha_two_sided": alpha, "target_power": target,
            "analytic_method": "Monotone closed-form two-sided known-SD z-test power using NormalDist.cdf; analytic minima drive the decision.",
            "simulation_method": "Fixed-seed normal Monte Carlo at displayed grid sizes is a cross-check only and does not define the minimum.",
            "simulations_per_n": simulations, "simulation_base_seed": seed, "effects": effects,
            "limits": ["The ten-block pilot residual SD has only the reported residual degrees of freedom and is uncertain.", "Known-SD z power assumes independent normal order-residual log ratios and is a planning approximation.", "Planning should allow for SD estimation, attrition, temporal drift, and multiplicity.", "Power describes token log ratios, not correctness or a universal language effect."]}


def _input_summary(pairs: list[dict]) -> dict:
    return {"blocks": len(pairs), "difference": _summary(p["metrics"]["input_tokens"]["difference_fsharp_minus_csharp"] for p in pairs if isinstance(p["metrics"]["input_tokens"].get("difference_fsharp_minus_csharp"), (int, float))),
            "log_ratio": _summary(p["metrics"]["input_tokens"]["log_ratio_fsharp_over_csharp"] for p in pairs if isinstance(p["metrics"]["input_tokens"].get("log_ratio_fsharp_over_csharp"), (int, float)))}


def _decision(errors: list[str], counts: dict, power: dict, language: dict) -> dict:
    minimums = [x["analytic_minimum_pairs_at_80_percent"] for x in power["effects"].values() if isinstance(x["analytic_minimum_pairs_at_80_percent"], int)]
    task_total = sum(x["task_outcomes"]["n"] for x in language.values()); task_successes = sum(x["task_outcomes"]["successes"] for x in language.values())
    chain_total = sum(x["chain_outcomes"]["n"] for x in language.values()); chain_successes = sum(x["chain_outcomes"]["successes"] for x in language.values())
    task_rate = task_successes/task_total if task_total else None; chain_rate = chain_successes/chain_total if chain_total else None
    saturation_threshold = .95
    near_saturated = task_rate is not None and task_rate >= saturation_threshold
    variance_overwhelming = bool(minimums) and max(minimums) > 100
    success = {"chains": {"successes": chain_successes, "attempts": chain_total, "rate": chain_rate},
               "tasks": {"successes": task_successes, "attempts": task_total, "rate": task_rate},
               "near_saturation_task_success_threshold": saturation_threshold, "correctness_near_saturated": near_saturated}
    if errors:
        outcome, rationale = "accounting_or_provenance_unstable", [f"The post-hoc verifier found {len(errors)} structural error(s)."]
        next_action = "Repair the apparatus and begin a new protocol cell before interpreting performance."
    elif counts["complete_blocks"] != counts["scheduled_formal_blocks"]:
        outcome, rationale = "formal_cell_incomplete", ["Not every scheduled formal block has two retained primary outcomes."]
        next_action = "Finish or formally disposition every frozen scheduled slot before making the variance decision."
    elif variance_overwhelming and near_saturated:
        outcome, rationale = "variance_overwhelms_plausible_effects_and_correctness_near_saturated", [f"The monotone analytic token power curve needs approximately {min(minimums)}–{max(minimums)} paired blocks for 80% power.", f"Formal task success is {task_successes}/{task_total} ({task_rate:.1%}), meeting the explicit ≥{saturation_threshold:.0%} near-saturation threshold; formal chain success is {chain_successes}/{chain_total} ({chain_rate:.1%})."]
        next_action = "Extend or recalibrate the maintenance chain while improving temporal blocking and increasing paired repetitions."
    elif variance_overwhelming:
        outcome, rationale = "variance_overwhelms_plausible_7_to_8_percent_effects", [f"The monotone analytic token power curve needs approximately {min(minimums)}–{max(minimums)} paired blocks for 80% power.", f"Formal task success is {task_successes}/{task_total} ({task_rate:.1%}); formal chain success is {chain_successes}/{chain_total} ({chain_rate:.1%})."]
        next_action = "Improve temporal blocking and increase paired repetitions before interpreting plausible token effects."
    elif near_saturated:
        outcome, rationale = "measurement_stable_but_correctness_near_saturated", [f"Formal task success is {task_successes}/{task_total} ({task_rate:.1%}), meeting the explicit ≥{saturation_threshold:.0%} near-saturation threshold; formal chain success is {chain_successes}/{chain_total} ({chain_rate:.1%})."]
        next_action = "Extend or recalibrate the maintenance chain while retaining blocking and sufficient paired repetitions."
    else:
        outcome, rationale = "stable_measurable_variation", ["The frozen cell is complete and planned effects are measurable at a practical sample size."]
        next_action = "Proceed to benchmark recalibration and multi-configuration feasibility with the frozen blocking rules."
    rationale.append(next_action)
    rationale.append("This variance pilot does not establish a causal or universal language ranking.")
    return {"outcome": outcome, "rationale": rationale, "next_action": next_action, "formal_success": success,
            "variance_overwhelming": variance_overwhelming, "analytic_minimum_pairs_at_80_percent": minimums}


def variance_report(cell_root: str | Path, *, bootstrap_samples: int = 2000, power_simulations: int = 2000, seed: int = 20260829) -> dict:
    if bootstrap_samples <= 0: raise ValueError("bootstrap_samples must be positive")
    if power_simulations <= 0: raise ValueError("power_simulations must be positive")
    cell = Path(cell_root).resolve(); manifest, manifest_bytes, sources, errors = _manifest(cell); schedule = _schedule(manifest, errors)
    expected = {row["block_id"]: row for row in schedule if isinstance(row.get("block_id"), str)}
    runs = sorted(path for path in cell.iterdir() if path.is_dir() and ((path/"result.json").exists() or (path/"attempt.json").exists()))
    expected_task_ids = list(sources.get("benchmark_task_order") or [])
    attempts = [row for path in runs if (row := _attempt(path, cell, manifest, manifest_bytes, expected, expected_task_ids, errors)) is not None]
    if len({row["attempt_id"] for row in attempts}) != len(attempts): errors.append("attempts: duplicate retained attempt_id")
    primaries = _primaries(attempts, schedule, errors); formal = [a for a in primaries if a["calibration"] is False]; calibration = [a for a in primaries if a["calibration"] is True]
    excluded = [a for a in attempts if a["disposition"].get("analysis_role") == "infrastructure-invalid"]
    pairs = _pairs(formal, schedule); language = _language_stats(formal); power = _power(pairs, power_simulations, seed)
    tasks = [task for attempt in formal for task in attempt["tasks"]]
    counts = {"attempts": len(attempts), "scheduled_formal_blocks": sum(not row["calibration"] for row in schedule), "formal_primary": len(formal),
              "calibration_attempts": sum(a["calibration"] is True for a in attempts), "calibration_primary": len(calibration), "complete_blocks": len(pairs),
              "excluded_infrastructure": len(excluded), "candidate_failures": sum(a["success"] is False for a in formal),
              "formal_accounting": {"valid": sum(a["accounting_valid"] and a["usage_available"] for a in formal), "expected": len(formal)},
              "formal_task_accounting": {"valid": sum(t["accounting_valid"] and t["usage_available"] for t in tasks),
                                         "expected": len(formal) * len(expected_task_ids)}}
    errors = sorted(set(errors)); successful = [p for p in pairs if p["outcomes"]["fsharp_success"] is True and p["outcomes"]["csharp_success"] is True]
    report = {"schema_version": 1, "cell_id": manifest.get("cell_id"), "manifest_sha256": manifest.get("manifest_sha256"),
              "generated_from": {"cell_path": ".", "transcripts_read": False, "input_token_semantics": "input_tokens includes cached_input_tokens; cached input is not added again", "manifest_sources": sources},
              "structural_validation": {"ok": not errors, "errors": errors}, "counts": counts, "schedule": schedule, "attempts": attempts,
              "formal_primary_attempts": formal, "calibration": {"primary_attempts": calibration}, "excluded_attempts": excluded,
              "outcomes_and_metrics": {"per_language": language}, "paired_blocks": pairs, "paired_bootstrap": _bootstrap_all(pairs, bootstrap_samples, seed),
              "variance_diagnostics": {"within_language_and_task": language, **_diagnostics(pairs, formal)},
              "frozen_rule_sensitivity": {"frozen_primary_rule": _input_summary(pairs), "successful_chains_only_non_preregistered": _input_summary(successful),
                                           "excluded_infrastructure_attempts": len(excluded), "excluded_infrastructure_failure_categories": _counts(a["failure_category"] for a in excluded),
                                           "formal_primary_attempts": len(formal), "interpretation": "Frozen analysis retains candidate failures and excludes preregistered infrastructure-invalid attempts; successful-only results are a labeled, non-preregistered sensitivity check."},
              "power": power}
    report["decision"] = _decision(errors, counts, power, language); report["report_sha256"] = _hash(report)
    return report


def calibration_fixture(report: dict) -> dict:
    keys = ("attempt_id", "block_id", "language", "position", "order", "started_at", "finished_at", "success", "failure_category", "accounting_valid", "usage_available", "metrics", "tasks", "artifact_hashes", "source_tree")
    attempts = [{key: attempt.get(key) for key in keys} for attempt in report.get("calibration", {}).get("primary_attempts", [])]
    fixture = {"schema_version": 1, "cell_id": report.get("cell_id"), "manifest_sha256": report.get("manifest_sha256"),
               "manifest_sources": report.get("generated_from", {}).get("manifest_sources"), "transcripts_included": False,
               "fresh_context_policy": "fresh candidate process and model conversation per task", "primary_attempts": attempts,
               "summary": {"primary_attempts": len(attempts), "tasks": sum(len(a.get("tasks") or []) for a in attempts),
                           "accounting_valid_attempts": sum(a.get("accounting_valid") is True for a in attempts),
                           "single_terminal_usage_tasks": sum(t.get("usage_record_count") == 1 for a in attempts for t in a.get("tasks") or []),
                           "fresh_process_records": sum(t.get("fresh_process_recorded") is True for a in attempts for t in a.get("tasks") or [])}}
    fixture["calibration_sha256"] = _hash(fixture); return fixture


def _fmt(value: Any, digits: int = 3) -> str:
    return "—" if value is None else f"{value:,}" if isinstance(value, int) else f"{value:,.{digits}f}" if isinstance(value, float) else str(value)


def markdown_report(report: dict) -> str:
    counts, validation = report["counts"], report["structural_validation"]; language = report["outcomes_and_metrics"]["per_language"]; bootstrap = report["paired_bootstrap"]["aggregate"]
    lines = ["# Variance and power decision report", "", f"Cell: `{report['cell_id']}`  ", f"Frozen manifest: `{report['manifest_sha256']}`  ", f"Report SHA-256: `{report['report_sha256']}`", "",
             "This report is post-hoc, deterministic, and transcript-free. Input tokens already include cached input tokens.", "", "## Dataset and verification", "",
             f"Structural verification: **{'passed' if validation['ok'] else 'failed'}**. Retained attempts: {counts['attempts']}; formal primaries: {counts['formal_primary']}; calibration primaries: {counts['calibration_primary']}; complete paired blocks: {counts['complete_blocks']}/{counts['scheduled_formal_blocks']}; excluded infrastructure attempts: {counts['excluded_infrastructure']}.", "",
             f"Formal run accounting: {counts['formal_accounting']['valid']}/{counts['formal_accounting']['expected']}. Formal task accounting: {counts['formal_task_accounting']['valid']}/{counts['formal_task_accounting']['expected']}." ]
    if validation["errors"]: lines += ["", "Structural errors:", ""] + [f"- {e}" for e in validation["errors"]]
    lines += ["", "## Correctness outcomes", "", "| Language | Chains | Chain successes | Tasks | Task successes | Failure reasons |", "|---|---:|---:|---:|---:|---|"]
    for name in ("fsharp", "csharp"):
        chain, tasks = language[name]["chain_outcomes"], language[name]["task_outcomes"]
        lines.append(f"| {name} | {chain['n']} | {chain['successes']} | {tasks['n']} | {tasks['successes']} | {_canon({**chain['failure_reasons'], **tasks['failure_reasons']})} |")
    lines += ["", "### Per-task outcomes and input-token variation", "", "| Task | Language | Successes / attempts | Input mean | Input median | Input sample SD |", "|---|---|---:|---:|---:|---:|"]
    task_ids = sorted(set(language["fsharp"]["per_task"]) | set(language["csharp"]["per_task"]))
    for task_id in task_ids:
        for name in ("fsharp", "csharp"):
            task = language[name]["per_task"][task_id]; outcome, metric = task["outcomes"], task["metrics"]["input_tokens"]
            lines.append(f"| {task_id} | {name} | {outcome['successes']} / {outcome['n']} | {_fmt(metric['mean'])} | {_fmt(metric['median'])} | {_fmt(metric['sample_sd'])} |")
    lines += ["", "## Aggregate metrics by language", "", "| Metric | F# mean | F# median | F# sample SD | C# mean | C# median | C# sample SD |", "|---|---:|---:|---:|---:|---:|---:|"]
    for metric in RUN_METRICS:
        f, c = language["fsharp"]["aggregate_metrics"][metric], language["csharp"]["aggregate_metrics"][metric]
        lines.append(f"| {metric} | {_fmt(f['mean'])} | {_fmt(f['median'])} | {_fmt(f['sample_sd'])} | {_fmt(c['mean'])} | {_fmt(c['median'])} | {_fmt(c['sample_sd'])} |")
    lines += ["", "## Paired effects and uncertainty", "", "Positive values mean F# used more of the metric than C#.", "", "| Metric | Blocks | Mean F#−C# | Difference sample SD | Bootstrap 95% CI | Mean log(F#/C#) | Bootstrap 95% CI |", "|---|---:|---:|---:|---:|---:|---:|"]
    for metric in RUN_METRICS:
        d, r = bootstrap[metric]["difference_fsharp_minus_csharp"], bootstrap[metric]["log_ratio_fsharp_over_csharp"]
        lines.append(f"| {metric} | {d['observations']} | {_fmt(d['mean'])} | {_fmt(d['descriptive']['sample_sd'])} | [{_fmt(d['ci_95']['lower'])}, {_fmt(d['ci_95']['upper'])}] | {_fmt(r['mean'],5)} | [{_fmt(r['ci_95']['lower'],5)}, {_fmt(r['ci_95']['upper'],5)}] |")
    order = report["variance_diagnostics"]["order_strata"]
    lines += ["", "## Order, position, and temporal diagnostics", "", f"Mean paired input-token difference was {_fmt(order['fsharp-first']['metrics']['input_tokens']['mean'])} when F# ran first and {_fmt(order['fsharp-second']['metrics']['input_tokens']['mean'])} when F# ran second. JSON preserves position strata, within-block spacing, block-index/UTC trends, and cross-metric sign/Pearson agreement.", "",
              "## Frozen-rule sensitivity and exclusions", "", report["frozen_rule_sensitivity"]["interpretation"], "", f"Calibration is separate and non-counting. {counts['excluded_infrastructure']} infrastructure-invalid attempt(s) remain retained with classifications and hashes.", "",
              "## Power planning", "", f"Order-residual paired input-token log-ratio SD: {_fmt(report['power']['paired_log_ratio_residual_sd'],6)} with {report['power']['residual_degrees_of_freedom']} residual degrees of freedom. Fixed-seed simulation used {report['power']['simulations_per_n']:,} draws per displayed grid size as a cross-check only.", "", "| Plausible ratio | Log effect | Analytic minimum pairs at 80% power |", "|---:|---:|---:|"]
    for effect in report["power"]["effects"].values(): lines.append(f"| {effect['ratio']:.2f} | {effect['log_effect']:.6f} | {_fmt(effect['analytic_minimum_pairs_at_80_percent'])} |")
    lines += ["", "Analytic method: " + report["power"]["analytic_method"], "", "Simulation cross-check: " + report["power"]["simulation_method"], "", "Limits:", ""] + [f"- {x}" for x in report["power"]["limits"]]
    formal_success = report["decision"]["formal_success"]
    chain_rate = "—" if formal_success["chains"]["rate"] is None else f"{formal_success['chains']['rate']:.1%}"
    task_rate = "—" if formal_success["tasks"]["rate"] is None else f"{formal_success['tasks']['rate']:.1%}"
    lines += ["", "## Decision", "", f"Formal success: {formal_success['chains']['successes']}/{formal_success['chains']['attempts']} chains ({chain_rate}) and {formal_success['tasks']['successes']}/{formal_success['tasks']['attempts']} tasks ({task_rate}); the explicit pilot near-saturation threshold is ≥{formal_success['near_saturation_task_success_threshold']:.0%} task success.", "", f"**{report['decision']['outcome']}**", ""] + [f"- {x}" for x in report["decision"]["rationale"]]
    return "\n".join(lines) + "\n"
