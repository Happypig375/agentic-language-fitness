from __future__ import annotations

import os
import subprocess
import time
from pathlib import Path
from typing import Mapping, Sequence

from .models import ProcessResult


def _decode_output(value: str | bytes | None) -> str:
    """Return captured output as text without depending on the system locale."""
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value


def run_process(
    argv: Sequence[str],
    *,
    cwd: Path,
    input_text: str | None = None,
    timeout: float = 300,
    env: Mapping[str, str] | None = None,
) -> ProcessResult:
    started = time.monotonic()
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)
    try:
        completed = subprocess.run(
            list(argv),
            cwd=cwd,
            input=input_text,
            text=True,
            encoding="utf-8",
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            env=merged_env,
            check=False,
        )
        return ProcessResult(
            argv=list(argv),
            returncode=completed.returncode,
            stdout=_decode_output(completed.stdout),
            stderr=_decode_output(completed.stderr),
            duration_seconds=time.monotonic() - started,
        )
    except subprocess.TimeoutExpired as exc:
        stdout = _decode_output(exc.stdout)
        stderr = _decode_output(exc.stderr)
        return ProcessResult(
            argv=list(argv),
            returncode=124,
            stdout=stdout,
            stderr=stderr,
            duration_seconds=time.monotonic() - started,
            timed_out=True,
        )
    except FileNotFoundError as exc:
        return ProcessResult(
            argv=list(argv),
            returncode=127,
            stdout="",
            stderr=str(exc),
            duration_seconds=time.monotonic() - started,
            missing_executable=True,
        )
