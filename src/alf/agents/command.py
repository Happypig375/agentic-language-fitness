from __future__ import annotations

import json
import os
import shlex
import shutil
from pathlib import Path
from typing import Any

from .base import Agent
from .codex import parse_codex_jsonl
from ..models import AgentResult, Usage
from ..process import run_process


def _nonnegative_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


class CommandAgent(Agent):
    def __init__(self, command_template: str, *, require_usage: bool = False, expected_protocol: dict[str, Any] | None = None):
        if not command_template.strip():
            raise ValueError("--agent-command is required for the command adapter")
        self.command_template = command_template
        self.require_usage = require_usage
        self.expected_protocol = expected_protocol

    def run(
        self,
        *,
        root: Path,
        workspace: Path,
        language: str,
        language_config: dict[str, Any],
        task: dict[str, Any],
        prompt: str,
        timeout: float,
        host_memory: dict[str, Any] | None = None,
    ) -> AgentResult:
        alf_dir = workspace / ".alf"
        alf_dir.mkdir(exist_ok=True)
        sidecar = alf_dir / "usage.json"
        sidecar.unlink(missing_ok=True)
        prompt_file = alf_dir / "TASK.md"
        prompt_file.write_text(prompt, encoding="utf-8")
        rendered = self.command_template.format(
            root=str(root),
            workspace=str(workspace),
            prompt_file=str(prompt_file),
            task_id=task["id"],
            language=language,
        )
        # POSIX shlex treats Windows backslashes as escapes.  `posix=False`
        # retains drive paths while still honoring quoted paths with spaces.
        if os.name == "nt":
            argv = [token[1:-1] if len(token) >= 2 and token[0] == token[-1] and token[0] in "\"'" else token
                    for token in shlex.split(rendered, posix=False)]
        else:
            argv = shlex.split(rendered)
        process = run_process(
            argv,
            cwd=workspace,
            # Allow the wrapper time to remove a timed-out named container.
            timeout=timeout + 30.0,
            env={
                "ALF_WORKSPACE": str(workspace),
                "ALF_ROOT": str(root),
                "ALF_PROMPT_FILE": str(prompt_file),
                "ALF_TASK_ID": task["id"],
                "ALF_LANGUAGE": language,
                "ALF_TIMEOUT": str(timeout),
                "ALF_HOST_MEMORY": json.dumps(host_memory) if host_memory else "",
            },
        )
        usage = Usage()
        model: str | None = None
        data: dict[str, Any] = {}
        accounting_valid = not self.require_usage
        usage_available = False
        auth_ok: bool | None = None
        container_limits: dict[str, Any] | None = None
        host_memory: dict[str, Any] | None = None
        accounting_errors: list[str] = []
        events: list[dict[str, Any]] = []
        usage_record_count = 0
        gate_failed = False
        if sidecar.is_file():
            try:
                value = json.loads(sidecar.read_text(encoding="utf-8"))
                if not isinstance(value, dict):
                    raise ValueError("sidecar must contain a JSON object")
                data = value
                gate_failed = data.get("host_memory_gate") == "failed" and isinstance(data.get("host_memory"), dict)
            except (OSError, json.JSONDecodeError, ValueError) as exc:
                accounting_errors.append(f"invalid usage sidecar: {exc}")
                accounting_valid = False
                data = {}
            derived = data.get("derived_from_codex_jsonl") is True
            if derived:
                parsed_events, parsed_usage, parsed_counts = parse_codex_jsonl(process.stdout)
                usage_record_count = parsed_counts["usage_records"]
                usage_available = parsed_counts["usage_records"] > 0 and parsed_counts["usage_valid"]
                accounting_valid = parsed_counts["accounting_valid"]
                accounting_errors.extend(parsed_counts["usage_errors"])
                for name in usage.__dataclass_fields__:
                    value = data.get(name)
                    if not _nonnegative_int(value) or value != getattr(parsed_usage, name):
                        accounting_valid = False
                        accounting_errors.append(f"derived sidecar mismatch: usage.{name}")
                count_map = {"event_count": len(parsed_events), "command_count": parsed_counts["commands"],
                             "file_change_count": parsed_counts["file_changes"], "failed_event_count": parsed_counts["failed_events"],
                             "file_reads": parsed_counts["file_reads"], "unique_file_reads": parsed_counts["unique_file_reads"],
                             "file_revisits": parsed_counts["file_revisits"]}
                count_map["usage_record_count"] = parsed_counts["usage_records"]
                for name, expected in count_map.items():
                    value = data.get(name)
                    if not _nonnegative_int(value) or value != expected:
                        accounting_valid = False
                        accounting_errors.append(f"derived sidecar mismatch: {name}")
                for name, expected in (("accounting_valid", parsed_counts["accounting_valid"]),
                                       ("usage_available", usage_available)):
                    if not isinstance(data.get(name), bool) or data[name] is not expected:
                        accounting_valid = False
                        accounting_errors.append(f"derived sidecar mismatch: {name}")
                if data.get("usage_errors") != parsed_counts["usage_errors"]:
                    accounting_valid = False
                    accounting_errors.append("derived sidecar mismatch: usage_errors")
                events = parsed_events
                if not accounting_valid:
                    accounting_errors.append("derived sidecar disagrees with Codex JSONL")
            elif not all(_nonnegative_int(data.get(field)) for field in usage.__dataclass_fields__):
                accounting_valid = False
                accounting_errors.append("usage sidecar has missing or invalid counters")
            else:
                accounting_valid = True
            for field in usage.__dataclass_fields__:
                value = data.get(field)
                if _nonnegative_int(value):
                    setattr(usage, field, value)
            model = data.get("model") if isinstance(data.get("model"), str) else None
            auth_ok = data.get("auth_ok") if isinstance(data.get("auth_ok"), bool) else None
            container_limits = (
                data.get("container_limits")
                if isinstance(data.get("container_limits"), dict)
                else None
            )
            host_memory = data.get("host_memory") if isinstance(data.get("host_memory"), dict) else None
            if not derived and not accounting_errors:
                usage_available = True
        def count(name: str) -> int:
            value = data.get(name, 0) if sidecar.is_file() else 0
            return value if _nonnegative_int(value) else 0
        # Preserve provenance before a later task can overwrite the shared sidecar.
        if sidecar.is_file():
            shutil.copy2(sidecar, alf_dir / f"usage-{task['id']}.json")
        elif self.require_usage:
            accounting_errors.append("required fresh usage sidecar is missing")
        if self.require_usage and not usage_available:
            accounting_valid = False
        expected = self.expected_protocol
        if expected:
            pins = expected["definition"]
            schema_version = expected.get("schema_version")
            if schema_version == 3:
                expected_model = pins.get("model", {}).get("requested_id")
                model_field = "requested_id"
            else:
                expected_model = pins.get("model", {}).get("snapshot")
                model_field = "snapshot"
            checks = {
                "model": expected_model,
                "reasoning_effort": pins["model"]["reasoning_effort"],
                "image": pins["codex"]["image"],
                "image_id": expected["image_id"],
            }
            if expected_model is None:
                accounting_valid = False
                accounting_errors.append(
                    f"protocol definition missing model.{model_field}"
                )
            for field, wanted in checks.items():
                actual = data.get("model") if field == "model" else data.get(field)
                if actual != wanted:
                    accounting_valid = False
                    accounting_errors.append(f"protocol sidecar mismatch: {field}")
            if data.get("derived_from_codex_jsonl") is not True:
                accounting_valid = False
                accounting_errors.append(
                    "protocol sidecar mismatch: derived_from_codex_jsonl"
                )
            elif usage_record_count != 1:
                accounting_valid = False
                accounting_errors.append(
                    "protocol accounting requires exactly one turn.completed usage record"
                )
            wanted_limits = {
                "memory": pins["limits"]["memory"],
                "cpus": pins["limits"]["cpus"],
                "pids": pins["limits"]["pids"],
            }
            if container_limits != wanted_limits:
                accounting_valid = False
                accounting_errors.append("protocol sidecar mismatch: container_limits")
            if not isinstance(data.get("auth_ok"), bool):
                accounting_valid = False
                accounting_errors.append("protocol sidecar mismatch: auth_ok")
            wanted_memory = pins.get("host_memory")
            if wanted_memory is not None:
                observed_memory = data.get("host_memory")
                wanted_thresholds = {
                    name: wanted_memory.get(name)
                    for name in ("minimum_available_physical_bytes", "minimum_available_commit_bytes")
                }
                if not isinstance(observed_memory, dict) or observed_memory.get("thresholds") != wanted_thresholds:
                    accounting_valid = False
                    accounting_errors.append("protocol sidecar mismatch: host_memory thresholds")
                elif not gate_failed and observed_memory.get("ok") is not True:
                    accounting_valid = False
                    accounting_errors.append("protocol sidecar mismatch: host_memory ok")
            wrapper_timed_out = data.get("timed_out")
            if not isinstance(wrapper_timed_out, bool):
                accounting_valid = False
                accounting_errors.append("protocol sidecar mismatch: timed_out")
            elif wrapper_timed_out != (process.returncode == 124):
                accounting_valid = False
                accounting_errors.append("protocol sidecar/process timeout mismatch")
            elif wrapper_timed_out:
                process.timed_out = True
            if gate_failed:
                wanted_memory = pins.get("host_memory", {})
                observed = data.get("host_memory", {})
                wanted_thresholds = {name: wanted_memory.get(name) for name in (
                    "minimum_available_physical_bytes", "minimum_available_commit_bytes")}
                gate_errors = []
                expected_model = pins.get("model", {}).get("requested_id", pins.get("model", {}).get("snapshot"))
                expected_limits = {"memory": pins.get("limits", {}).get("memory"),
                                   "cpus": pins.get("limits", {}).get("cpus"),
                                   "pids": pins.get("limits", {}).get("pids")}
                exact = ((process.returncode == 75, "host gate returncode"),
                         (data.get("model") == expected_model, "host gate model"),
                         (data.get("reasoning_effort") == pins.get("model", {}).get("reasoning_effort"), "host gate reasoning_effort"),
                         (data.get("image") == pins.get("codex", {}).get("image"), "host gate image"),
                         (data.get("image_id") == "not-probed", "host gate image_id"),
                         (data.get("container_limits") == expected_limits, "host gate container_limits"),
                         (data.get("auth_ok") is None, "host gate auth_ok"),
                         (data.get("timed_out") is False, "host gate timed_out"),
                         (data.get("derived_from_codex_jsonl") is False, "host gate derived flag"),
                         (data.get("host_memory_gate") == "failed", "host gate marker"),
                         (observed.get("thresholds") == wanted_thresholds, "host gate thresholds"),
                         (observed.get("ok") is False, "host gate ok"))
                gate_errors.extend(f"protocol sidecar mismatch: {label}" for valid, label in exact if not valid)
                zero_fields = tuple(usage.__dataclass_fields__) + ("event_count", "command_count", "file_change_count", "failed_event_count", "file_reads", "unique_file_reads", "file_revisits", "usage_record_count")
                gate_errors.extend(f"protocol sidecar mismatch: {field} must be zero" for field in zero_fields if data.get(field) != 0)
                if data.get("accounting_valid") is not False:
                    gate_errors.append("protocol sidecar mismatch: host gate accounting_valid")
                if data.get("usage_available") is not False:
                    gate_errors.append("protocol sidecar mismatch: host gate usage_available")
                if gate_errors:
                    accounting_errors = gate_errors
                    accounting_valid = False
                else:
                    accounting_valid = False
                    usage_available = False
                    accounting_errors = []
        return AgentResult(
            process=process, usage=usage, model=model,
            event_count=count("event_count"), command_count=count("command_count"),
            file_change_count=count("file_change_count"), failed_event_count=count("failed_event_count"),
            file_reads=count("file_reads"), unique_file_reads=count("unique_file_reads"), file_revisits=count("file_revisits"),
            usage_record_count=usage_record_count,
            accounting_valid=accounting_valid,
            usage_available=usage_available,
            accounting_errors=accounting_errors,
            events=events,
            auth_ok=auth_ok,
            container_limits=container_limits,
            host_memory=host_memory,
        )
