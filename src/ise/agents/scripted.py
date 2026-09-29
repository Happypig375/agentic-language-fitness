from __future__ import annotations

import time
from pathlib import Path
from typing import Any

from .base import Agent
from ..models import AgentResult, ProcessResult
from ..benchmark_artifacts import artifact_plan, copy_artifacts
from ..config import Manifest


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
        plan = task.get("_artifact_plan")
        if plan is None:
            context = task.get("_artifact_context", {})
            manifest = Manifest({"languages": {language: language_config}})
            manifest.manifest_parent = Path(
                context.get("manifest_parent")
                if isinstance(context, dict) and context.get("manifest_parent")
                else root / "benchmarks/pilot"
            )
            plan = artifact_plan(root, manifest, language, task, workspace)
        copy_artifacts(plan)
        process = ProcessResult(
            argv=["scripted-copy", *[str(item.source) for item in plan]],
            returncode=0,
            stdout=f"Applied {len(plan)} gold artifact(s)\n",
            stderr="",
            duration_seconds=time.monotonic() - started,
        )
        return AgentResult(process=process, model="gold-snapshot")
