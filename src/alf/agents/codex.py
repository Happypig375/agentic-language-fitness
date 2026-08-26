from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .base import Agent
from ..models import AgentResult, Usage
from ..process import run_process


def parse_codex_jsonl(text: str) -> tuple[list[dict[str, Any]], Usage, dict[str, int]]:
    events: list[dict[str, Any]] = []
    usage = Usage()
    counts = {"commands": 0, "file_changes": 0, "other_tools": 0, "failed_events": 0}
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
            values = event.get("usage") or {}
            usage.add(
                Usage(
                    input_tokens=int(values.get("input_tokens") or 0),
                    cached_input_tokens=int(values.get("cached_input_tokens") or 0),
                    cache_write_input_tokens=int(values.get("cache_write_input_tokens") or 0),
                    output_tokens=int(values.get("output_tokens") or 0),
                    reasoning_output_tokens=int(values.get("reasoning_output_tokens") or 0),
                )
            )
        elif event_type in {"turn.failed", "error"}:
            counts["failed_events"] += 1
        if event_type in {"item.started", "item.updated", "item.completed"}:
            item_type = (event.get("item") or {}).get("type")
            if item_type in {"command_execution", "command", "shell_command"} and event_type == "item.completed":
                counts["commands"] += 1
            if item_type in {"file_change", "file_changes", "patch"} and event_type == "item.completed":
                counts["file_changes"] += 1
            if item_type in {"mcp_tool_call", "web_search"} and event_type == "item.completed":
                counts["other_tools"] += 1
            if item_type == "error" and event_type == "item.completed":
                counts["failed_events"] += 1
    usage.tool_calls = counts["commands"] + counts["file_changes"] + counts["other_tools"]
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
            events=events,
        )
