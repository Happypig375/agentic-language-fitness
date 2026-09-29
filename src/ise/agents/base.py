from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from ..models import AgentResult


class Agent(ABC):
    @abstractmethod
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
        raise NotImplementedError
