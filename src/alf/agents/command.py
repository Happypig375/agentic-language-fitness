from __future__ import annotations

import json
import os
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
            },
        )
        usage = Usage()
        model: str | None = None
        data: dict[str, Any] = {}
        sidecar = alf_dir / "usage.json"
        if sidecar.is_file():
            data = json.loads(sidecar.read_text(encoding="utf-8"))
            for field in usage.__dataclass_fields__:
                value = data.get(field)
                if isinstance(value, int) and value >= 0:
                    setattr(usage, field, value)
            model = data.get("model") if isinstance(data.get("model"), str) else None
        def count(name: str) -> int:
            value = data.get(name, 0) if sidecar.is_file() else 0
            return value if isinstance(value, int) and value >= 0 else 0
        return AgentResult(
            process=process, usage=usage, model=model,
            event_count=count("event_count"), command_count=count("command_count"),
            file_change_count=count("file_change_count"), failed_event_count=count("failed_event_count"),
        )
