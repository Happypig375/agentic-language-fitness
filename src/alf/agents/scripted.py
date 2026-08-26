from __future__ import annotations

import shutil
import time
from pathlib import Path
from typing import Any

from .base import Agent
from ..models import AgentResult, ProcessResult


class ScriptedAgent(Agent):
    """Applies cumulative gold snapshots. Used only to validate the harness."""

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
        started = time.monotonic()
        source = root / task["gold"][language]
        target = workspace / language_config["source_file"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        process = ProcessResult(
            argv=["scripted-copy", str(source), str(target)],
            returncode=0,
            stdout=f"Applied {source}\n",
            stderr="",
            duration_seconds=time.monotonic() - started,
        )
        return AgentResult(process=process, model="gold-snapshot")
