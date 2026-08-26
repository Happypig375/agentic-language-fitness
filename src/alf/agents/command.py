from __future__ import annotations

import json
import shlex
from pathlib import Path
from typing import Any

from .base import Agent
from ..models import AgentResult, Usage
from ..process import run_process


class CommandAgent(Agent):
    def __init__(self, command_template: str):
        if not command_template.strip():
            raise ValueError("--agent-command is required for the command adapter")
        self.command_template = command_template

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
        rendered = self.command_template.format(
            workspace=str(workspace),
            prompt_file=str(prompt_file),
            task_id=task["id"],
            language=language,
        )
        argv = shlex.split(rendered)
        process = run_process(
            argv,
            cwd=workspace,
            timeout=timeout,
            env={
                "ALF_WORKSPACE": str(workspace),
                "ALF_PROMPT_FILE": str(prompt_file),
                "ALF_TASK_ID": task["id"],
                "ALF_LANGUAGE": language,
            },
        )
        usage = Usage()
        model: str | None = None
        sidecar = alf_dir / "usage.json"
        if sidecar.is_file():
            data = json.loads(sidecar.read_text(encoding="utf-8"))
            for field in usage.__dataclass_fields__:
                value = data.get(field)
                if isinstance(value, int) and value >= 0:
                    setattr(usage, field, value)
            model = data.get("model") if isinstance(data.get("model"), str) else None
        return AgentResult(process=process, usage=usage, model=model)
