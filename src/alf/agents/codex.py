from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .base import Agent
from ..models import AgentResult, Usage
from ..process import run_process


def parse_codex_jsonl(text: str) -> tuple[list[dict[str, Any]], Usage, dict[str, Any]]:
    events: list[dict[str, Any]] = []
    usage = Usage()
    counts: dict[str, Any] = {"commands": 0, "file_changes": 0, "other_tools": 0, "failed_events": 0,
                              "file_reads": 0, "unique_file_reads": 0, "file_revisits": 0,
                              "usage_records": 0, "usage_valid": True, "usage_errors": []}
    usage_fields = ("input_tokens", "cached_input_tokens", "cache_write_input_tokens",
                    "output_tokens", "reasoning_output_tokens")
    reads: list[str] = []
    def extract_reads(command: str) -> list[str]:
        # shlex(posix=False) retains backslashes in Windows paths and quotes
        # around paths with spaces.  Only accept a deliberately small grammar.
        import shlex
        if any(operator in command for operator in ("|", ";", "&&", "||", ">", "<", "`", "$")):
            return []
        try:
            lexer = shlex.shlex(command, posix=False)
            lexer.whitespace_split = True
            lexer.commenters = ""
            raw_tokens = list(lexer)
        except ValueError:
            return []
        tokens = [token[1:-1] if len(token) >= 2 and token[0] == token[-1] and token[0] in "\"'" else token
                  for token in raw_tokens]
        if not tokens or any(token in {"|", ";", "&&", "||", ">", "<"} for token in tokens):
            return []
        tool = tokens[0]
        if tool in {"cat", "head", "tail", "less", "more"}:
            paths = tokens[1:]
        elif tool == "rg" and len(tokens) >= 3:
            # rg PATTERN PATH...; option forms are intentionally unsupported.
            paths = tokens[2:]
        elif tool == "sed" and len(tokens) >= 4 and tokens[1] == "-n" and not tokens[2].startswith("-"):
            # sed -n PROGRAM PATH...; PROGRAM is not a file.
            paths = tokens[3:]
        else:
            return []
        return paths if paths and all(path and not path.startswith("-") for path in paths) else []
    for raw in text.splitlines():
        raw = raw.strip()
        if not raw:
            continue
        try:
            event = json.loads(raw)
        except json.JSONDecodeError:
            counts["failed_events"] += 1
            events.append({"type": "alf.invalid-jsonl", "raw": raw})
            continue
        events.append(event)
        event_type = event.get("type")
        if event_type == "turn.completed":
            counts["usage_records"] += 1
            values = event.get("usage")
            error = None
            if not isinstance(values, dict):
                error = "turn.completed is missing an object-valued usage field"
            else:
                for field_name in usage_fields:
                    value = values.get(field_name)
                    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                        error = f"usage.{field_name} must be a non-negative integer"
                        break
            if error:
                counts["usage_valid"] = False
                counts["usage_errors"].append(error)
            # Retain valid counters even when the record is invalid, while making
            # the invalid status explicit to callers.
            if isinstance(values, dict):
                partial = {name: values[name] for name in usage_fields
                           if isinstance(values.get(name), int) and not isinstance(values.get(name), bool)
                           and values[name] >= 0}
                usage.add(Usage(**partial))
        elif event_type in {"turn.failed", "error"}:
            counts["failed_events"] += 1
        if event_type in {"item.started", "item.updated", "item.completed"}:
            item_type = (event.get("item") or {}).get("type")
            if item_type in {"command_execution", "command", "shell_command"} and event_type == "item.completed":
                counts["commands"] += 1
                command = (event.get("item") or {}).get("command") or (event.get("item") or {}).get("cmd")
                if isinstance(command, str):
                    # Only count unambiguous simple read commands; never infer recovery.
                    reads.extend(extract_reads(command))
            if item_type in {"file_change", "file_changes", "patch"} and event_type == "item.completed":
                counts["file_changes"] += 1
            if item_type in {"mcp_tool_call", "web_search"} and event_type == "item.completed":
                counts["other_tools"] += 1
            if item_type == "error" and event_type == "item.completed":
                counts["failed_events"] += 1
    usage.tool_calls = counts["commands"] + counts["file_changes"] + counts["other_tools"]
    counts["file_reads"] = len(reads)
    counts["unique_file_reads"] = len(set(reads))
    counts["file_revisits"] = len(reads) - len(set(reads))
    counts["accounting_valid"] = bool(counts["usage_valid"] and counts["usage_records"] > 0)
    if not counts["usage_records"]:
        counts["usage_errors"].append("no turn.completed usage records found")
    return events, usage, counts


class CodexAgent(Agent):
    def __init__(self, model: str | None = None, executable: str = "codex"):
        self.model = model
        self.executable = executable

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
    ) -> AgentResult:
        alf_dir = workspace / ".alf"
        alf_dir.mkdir(exist_ok=True)
        prompt_file = alf_dir / "TASK.md"
        prompt_file.write_text(prompt, encoding="utf-8")
        instructions = (
            "You are operating inside an Agentic Language Fitness benchmark workspace. "
            "Implement the task in .alf/TASK.md. Work only inside this workspace. "
            "Do not search parent directories for tests, manifests, or gold answers. "
            "Preserve the line-delimited JSON protocol and existing behavior. "
            "Use the compiler and your own tests as needed. Finish with the repository edited in place.\n\n"
            + prompt
        )
        argv = [
            self.executable,
            "exec",
            "--json",
            "--ephemeral",
            "--ignore-user-config",
            "--ignore-rules",
            "--sandbox",
            "workspace-write",
            "--cd",
            str(workspace),
            "--color",
            "never",
        ]
        if self.model:
            argv.extend(["--model", self.model])
        argv.append("-")
        process = run_process(argv, cwd=workspace, input_text=instructions, timeout=timeout)
        events, usage, counts = parse_codex_jsonl(process.stdout)
        return AgentResult(
            process=process,
            usage=usage,
            model=self.model,
            event_count=len(events),
            command_count=counts["commands"],
            file_change_count=counts["file_changes"],
            failed_event_count=counts["failed_events"],
            file_reads=counts["file_reads"], unique_file_reads=counts["unique_file_reads"],
            file_revisits=counts["file_revisits"],
            events=events,
            accounting_valid=counts["accounting_valid"],
            usage_available=counts["usage_records"] > 0 and counts["usage_valid"],
            accounting_errors=list(counts["usage_errors"]),
        )
