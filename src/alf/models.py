from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class Usage:
    input_tokens: int = 0
    cached_input_tokens: int = 0
    cache_write_input_tokens: int = 0
    output_tokens: int = 0
    reasoning_output_tokens: int = 0
    tool_calls: int = 0

    def add(self, other: "Usage") -> None:
        self.input_tokens += other.input_tokens
        self.cached_input_tokens += other.cached_input_tokens
        self.cache_write_input_tokens += other.cache_write_input_tokens
        self.output_tokens += other.output_tokens
        self.reasoning_output_tokens += other.reasoning_output_tokens
        self.tool_calls += other.tool_calls

    def to_dict(self) -> dict[str, int]:
        return asdict(self)


@dataclass
class ProcessResult:
    argv: list[str]
    returncode: int
    stdout: str
    stderr: str
    duration_seconds: float
    timed_out: bool = False
    missing_executable: bool = False

    @property
    def ok(self) -> bool:
        return self.returncode == 0 and not self.timed_out and not self.missing_executable

    def summary(self) -> dict[str, Any]:
        return {
            "argv": self.argv,
            "returncode": self.returncode,
            "duration_seconds": self.duration_seconds,
            "timed_out": self.timed_out,
            "missing_executable": self.missing_executable,
        }


@dataclass
class AgentResult:
    process: ProcessResult
    usage: Usage = field(default_factory=Usage)
    model: str | None = None
    event_count: int = 0
    command_count: int = 0
    file_change_count: int = 0
    failed_event_count: int = 0
    events: list[dict[str, Any]] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return self.process.ok and self.failed_event_count == 0
