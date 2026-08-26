from __future__ import annotations

import os
import subprocess
import time
from pathlib import Path
from typing import Mapping, Sequence

from .models import ProcessResult


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
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            env=merged_env,
            check=False,
        )
        return ProcessResult(
            argv=list(argv),
            returncode=completed.returncode,
            stdout=completed.stdout,
            stderr=completed.stderr,
            duration_seconds=time.monotonic() - started,
        )
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout.decode() if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        stderr = exc.stderr.decode() if isinstance(exc.stderr, bytes) else (exc.stderr or "")
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
