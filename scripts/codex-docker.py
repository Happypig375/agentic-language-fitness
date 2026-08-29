#!/usr/bin/env python3
"""Run one ALF command-adapter task in an isolated Codex Docker container."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path
from typing import Sequence

# The command adapter launches this script with cwd set to the task workspace.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from alf.agents.codex import parse_codex_jsonl

IMAGE_DEFAULT = "alf-codex:0.149.1"
SAFETY_PROMPT = (
    "You are operating inside an Agentic Language Fitness benchmark workspace. "
    "Implement the task provided below. Work only inside /workspace; do not search "
    "parent directories or for gold answers/evaluator files. Preserve existing behavior "
    "and finish with the repository edited in place.\n\n"
)


def decode_output(value: str | bytes | None) -> str:
    if value is None:
        return ""
    return value.decode("utf-8", errors="replace") if isinstance(value, bytes) else value


def resolve_auth_path(explicit: str | None, environ: dict[str, str] | None = None) -> Path | None:
    """Resolve an auth file without reading or printing its contents."""
    env = os.environ if environ is None else environ
    candidates: list[Path] = []
    if explicit:
        candidates.append(Path(explicit).expanduser())
    if env.get("CODEX_AUTH_FILE"):
        candidates.append(Path(env["CODEX_AUTH_FILE"]).expanduser())
    if env.get("CODEX_HOME"):
        candidates.append(Path(env["CODEX_HOME"]) / "auth.json")
    if env.get("USERPROFILE"):
        candidates.append(Path(env["USERPROFILE"]) / ".codex" / "auth.json")
    if env.get("HOME"):
        candidates.append(Path(env["HOME"]) / ".codex" / "auth.json")
    for candidate in candidates:
        if candidate.is_file():
            return candidate.resolve()
    return None


def build_docker_argv(
    workspace: Path,
    image: str,
    auth_file: Path | None = None,
    model: str | None = None,
    docker_executable: str = "docker",
    *,
    reasoning_effort: str | None = None,
    memory: str | None = None,
    cpus: int | None = None,
    pids_limit: int | None = None,
) -> list[str]:
    """Build argv using Docker --mount flags (never a shell command)."""
    for path in (workspace, auth_file):
        if path is not None and "," in str(path):
            raise ValueError("Docker mount paths containing commas are unsupported")
    name = f"alf-codex-{uuid.uuid4().hex[:16]}"
    resolved_memory = memory or os.environ.get("ALF_DOCKER_MEMORY", "2g")
    resolved_cpus = cpus if cpus is not None else int(os.environ.get("ALF_DOCKER_CPUS", "2"))
    resolved_pids = pids_limit if pids_limit is not None else int(os.environ.get("ALF_DOCKER_PIDS", "256"))
    if not resolved_memory or resolved_cpus <= 0 or resolved_pids <= 0:
        raise ValueError("Docker memory, CPU, and PID limits must be positive")
    argv = [docker_executable, "run", "--rm", "-i", "--name", name,
            "--network", "bridge", "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
            "--pids-limit", str(resolved_pids),
            "--memory", resolved_memory,
            "--cpus", str(resolved_cpus), "--user", "codex",
            "--mount", f"type=bind,src={workspace.resolve()},dst=/workspace"]
    if auth_file is not None:
        argv.extend(["--mount", f"type=bind,src={auth_file.resolve()},dst=/home/codex/.codex/auth.json,readonly"])
    argv.extend([
        image,
        "exec", "--json", "--ephemeral", "--ignore-user-config", "--ignore-rules",
        "--dangerously-bypass-approvals-and-sandbox", "--cd", "/workspace",
    ])
    if model:
        argv.extend(["--model", model])
    if reasoning_effort:
        if reasoning_effort not in {"low", "medium", "high"}:
            raise ValueError("reasoning_effort must be low, medium, or high")
        argv.extend(["--config", f"model_reasoning_effort={reasoning_effort}"])
    argv.append("-")
    return argv


def build_login_status_argv(auth_file: Path, image: str = IMAGE_DEFAULT, docker_executable: str = "docker") -> list[str]:
    """Build a model-free auth validation command using the exact Codex-home mount."""
    if "," in str(auth_file):
        raise ValueError("Docker mount paths containing commas are unsupported")
    return [docker_executable, "run", "--rm", "--network", "bridge", "--cap-drop", "ALL",
            "--security-opt", "no-new-privileges", "--user", "codex", "-i",
            "--mount", f"type=bind,src={auth_file.resolve()},dst=/home/codex/.codex/auth.json,readonly",
            image, "login", "status"]


def write_usage(workspace: Path, stdout: str, model: str | None, image: str | None = None) -> None:
    """Parse JSONL and write only aggregate, non-secret usage metadata."""
    events, usage, counts = parse_codex_jsonl(stdout)
    data = usage.to_dict()
    data.update({
        "model": model,
        "command_count": counts["commands"],
        "file_change_count": counts["file_changes"],
        "other_tool_count": counts["other_tools"],
        "failed_event_count": counts["failed_events"],
        "event_count": len(events),
        "image": image,
        "derived_from_codex_jsonl": True,
        "usage_available": bool(counts.get("usage_records") and counts.get("usage_valid")),
        "usage_record_count": counts.get("usage_records", 0),
        "accounting_valid": bool(counts.get("accounting_valid")),
        "usage_errors": counts.get("usage_errors", []),
        "file_reads": counts.get("file_reads", 0),
        "unique_file_reads": counts.get("unique_file_reads", 0),
        "file_revisits": counts.get("file_revisits", 0),
    })
    target = workspace / ".alf" / "usage.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(data, sort_keys=True) + "\n", encoding="utf-8")


def image_identifier(image: str) -> str:
    """Return Docker's immutable image ID, or an explicit unavailable marker."""
    try:
        result = subprocess.run(
            ["docker", "image", "inspect", image, "--format", "{{.Id}}"],
            text=True, capture_output=True, check=False,
        )
        value = (result.stdout or "").strip()
        return value if result.returncode == 0 and value else "unavailable"
    except (OSError, subprocess.SubprocessError):
        return "unavailable"


def minimized_auth(source: Path | None) -> Path | None:
    """Create a temporary auth file with refresh credentials removed."""
    if source is None:
        return None
    value = json.loads(source.read_text(encoding="utf-8"))
    def strip_refresh(item):
        if isinstance(item, dict):
            return {k: ("" if k.lower() == "refresh_token" else strip_refresh(v)) for k, v in item.items()}
        if isinstance(item, list):
            return [strip_refresh(v) for v in item]
        return item
    handle = tempfile.NamedTemporaryFile(mode="w", suffix=".json", prefix="alf-auth-", delete=False, encoding="utf-8")
    try:
        json.dump(strip_refresh(value), handle)
        handle.close()
        # The container's unprivileged codex user must be able to read the bind mount.
        os.chmod(handle.name, 0o644)
        return Path(handle.name)
    except Exception:
        handle.close()
        Path(handle.name).unlink(missing_ok=True)
        raise


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", default=os.environ.get("ALF_WORKSPACE"), required=not bool(os.environ.get("ALF_WORKSPACE")))
    parser.add_argument("--prompt-file", default=os.environ.get("ALF_PROMPT_FILE"))
    parser.add_argument("--prompt", default=None)
    parser.add_argument("--model", default=os.environ.get("ALF_MODEL") or os.environ.get("CODEX_MODEL"))
    parser.add_argument("--reasoning-effort", choices=["low", "medium", "high"], default=os.environ.get("ALF_REASONING_EFFORT"))
    parser.add_argument("--memory", default=os.environ.get("ALF_DOCKER_MEMORY", "2g"))
    parser.add_argument("--cpus", type=int, default=os.environ.get("ALF_DOCKER_CPUS", "2"))
    parser.add_argument("--pids-limit", type=int, default=os.environ.get("ALF_DOCKER_PIDS", "256"))
    parser.add_argument("--require-auth-preflight", action="store_true")
    parser.add_argument("--image", default=os.environ.get("ALF_CODEX_IMAGE") or os.environ.get("CODEX_IMAGE") or IMAGE_DEFAULT)
    parser.add_argument("--auth", default=os.environ.get("CODEX_AUTH_FILE"))
    args = parser.parse_args(argv)
    workspace = Path(args.workspace).expanduser().resolve()
    if not workspace.is_dir():
        parser.error(f"workspace is not a directory: {workspace}")
    if args.prompt is not None:
        task = args.prompt
    elif args.prompt_file:
        task = Path(args.prompt_file).read_text(encoding="utf-8")
    else:
        task = sys.stdin.read()
    auth_source = resolve_auth_path(args.auth)
    auth = minimized_auth(auth_source)
    image_id = image_identifier(args.image)
    try:
        command = build_docker_argv(
            workspace,
            args.image,
            auth,
            args.model,
            reasoning_effort=args.reasoning_effort,
            memory=args.memory,
            cpus=args.cpus,
            pids_limit=args.pids_limit,
        )
    except Exception:
        if auth is not None:
            auth.unlink(missing_ok=True)
        raise
    name = command[command.index("--name") + 1]
    timeout = float(os.environ.get("ALF_TIMEOUT", "300"))
    timed_out = False
    auth_ok: bool | None = None
    try:
        if args.require_auth_preflight:
            if auth is None:
                auth_ok = False
            else:
                auth_status = subprocess.run(
                    build_login_status_argv(auth, args.image),
                    text=True,
                    capture_output=True,
                    timeout=30,
                    check=False,
                )
                auth_ok = auth_status.returncode == 0
        if args.require_auth_preflight and not auth_ok:
            completed = type(
                "AuthFailure",
                (),
                {
                    "stdout": "",
                    "stderr": "Codex authentication preflight failed\n",
                    "returncode": 78,
                },
            )()
        else:
            completed = subprocess.run(
                command,
                input=SAFETY_PROMPT + task,
                text=True,
                capture_output=True,
                timeout=timeout,
            )
    except subprocess.TimeoutExpired as exc:
        timed_out = True
        subprocess.run(["docker", "rm", "-f", name], capture_output=True, check=False)

        class TimeoutResult:
            stdout = decode_output(exc.stdout)
            stderr = decode_output(exc.stderr)
            returncode = 124

        completed = TimeoutResult()
    finally:
        if auth is not None:
            auth.unlink(missing_ok=True)
    sys.stdout.write(completed.stdout)
    sys.stdout.flush()
    sys.stderr.write(completed.stderr)
    sys.stderr.flush()
    write_usage(workspace, completed.stdout, args.model, args.image)
    sidecar = workspace / ".alf" / "usage.json"
    data = json.loads(sidecar.read_text(encoding="utf-8"))
    data["image_id"] = image_id
    data["reasoning_effort"] = args.reasoning_effort
    data["timed_out"] = timed_out
    data["auth_ok"] = auth_ok
    data["container_limits"] = {
        "memory": args.memory,
        "cpus": args.cpus,
        "pids": args.pids_limit,
    }
    sidecar.write_text(json.dumps(data, sort_keys=True) + "\n", encoding="utf-8")
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
