#!/usr/bin/env python3
"""Run one ALF command-adapter task in an isolated Codex Docker container."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
import subprocess
import sys
import tempfile
import platform
import re
import shutil
import uuid
from urllib.parse import urlparse
from pathlib import Path
from typing import Sequence

# The command adapter launches this script with cwd set to the task workspace.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from alf.agents.codex import parse_codex_jsonl
from alf.environment_profile import (
    environment_profile_sha256,
    load_environment_profile,
    validate_container_route,
)
from alf.host_memory import evaluate_host_memory, parse_requirement

IMAGE_DEFAULT = "alf-codex:0.149.1"
CONTAINER_CODEX_HOME = "/tmp/alf-codex-home"
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
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


def container_user() -> str:
    """Use the invoking user on POSIX so bind-mounted workspaces remain writable."""
    if os.name == "nt":
        return "codex"
    uid = os.geteuid()
    gid = os.getegid()
    if uid <= 0 or gid <= 0:
        raise ValueError("refusing to run the candidate container as root")
    return f"{uid}:{gid}"


def validate_network_name(value: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,127}", value):
        raise ValueError("docker network name contains unsupported characters")
    return value


def append_proxy_environment(argv: list[str], key: str, value: str | None) -> None:
    if not value:
        return
    if any(character in value for character in ("\r", "\n", "\0")):
        raise ValueError("proxy settings contain control characters")
    if key != "NO_PROXY":
        parsed = urlparse(value)
        if parsed.scheme != "http" or not parsed.hostname or parsed.username or parsed.password:
            raise ValueError("proxy URL must be an unauthenticated http:// URL")
    argv.extend(["--env", f"{key}={value}"])


def build_docker_argv(
    workspace: Path,
    image: str,
    auth_home: Path | None = None,
    model: str | None = None,
    docker_executable: str = "docker",
    *,
    reasoning_effort: str | None = None,
    memory: str | None = None,
    cpus: int | None = None,
    pids_limit: int | None = None,
    docker_network: str | None = None,
    https_proxy: str | None = None,
    http_proxy: str | None = None,
    no_proxy: str | None = None,
) -> list[str]:
    """Build argv using Docker --mount flags (never a shell command)."""
    for path in (workspace, auth_home):
        if path is not None and "," in str(path):
            raise ValueError("Docker mount paths containing commas are unsupported")
    name = f"alf-codex-{uuid.uuid4().hex[:16]}"
    resolved_memory = memory or os.environ.get("ALF_DOCKER_MEMORY", "2g")
    resolved_cpus = cpus if cpus is not None else int(os.environ.get("ALF_DOCKER_CPUS", "2"))
    resolved_pids = pids_limit if pids_limit is not None else int(os.environ.get("ALF_DOCKER_PIDS", "256"))
    if not resolved_memory or resolved_cpus <= 0 or resolved_pids <= 0:
        raise ValueError("Docker memory, CPU, and PID limits must be positive")
    network = validate_network_name(
        docker_network or os.environ.get("ALF_DOCKER_NETWORK", "bridge")
    )
    if auth_home is not None and (
        not auth_home.is_dir() or not (auth_home / "auth.json").is_file()
    ):
        raise ValueError("auth_home must contain auth.json")
    argv = [docker_executable, "run", "--rm", "-i", "--name", name,
            "--network", network, "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
            "--pids-limit", str(resolved_pids),
            "--memory", resolved_memory,
            "--cpus", str(resolved_cpus), "--user", container_user(),
            "--mount", f"type=bind,src={workspace.resolve()},dst=/workspace"]
    if auth_home is not None:
        argv.extend([
            "--mount",
            f"type=bind,src={auth_home.resolve()},dst={CONTAINER_CODEX_HOME}",
        ])
    argv.extend([
        "--env", f"HOME={CONTAINER_CODEX_HOME}",
        "--env", f"CODEX_HOME={CONTAINER_CODEX_HOME}",
    ])
    append_proxy_environment(argv, "HTTPS_PROXY", https_proxy or os.environ.get("HTTPS_PROXY"))
    append_proxy_environment(argv, "HTTP_PROXY", http_proxy or os.environ.get("HTTP_PROXY"))
    append_proxy_environment(argv, "NO_PROXY", no_proxy or os.environ.get("NO_PROXY"))
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


def build_login_status_argv(auth_home: Path, image: str = IMAGE_DEFAULT, docker_executable: str = "docker", *, docker_network: str | None = None, https_proxy: str | None = None, http_proxy: str | None = None, no_proxy: str | None = None) -> list[str]:
    """Build model-free auth validation using a writable complete Codex home."""
    if "," in str(auth_home):
        raise ValueError("Docker mount paths containing commas are unsupported")
    if not auth_home.is_dir() or not (auth_home / "auth.json").is_file():
        raise ValueError("auth_home must contain auth.json")
    network = validate_network_name(
        docker_network or os.environ.get("ALF_DOCKER_NETWORK", "bridge")
    )
    argv = [docker_executable, "run", "--rm", "--cap-drop", "ALL",
            "--security-opt", "no-new-privileges", "--user", container_user(), "-i",
            "--network", network,
            "--env", f"HOME={CONTAINER_CODEX_HOME}",
            "--env", f"CODEX_HOME={CONTAINER_CODEX_HOME}",
            "--mount", f"type=bind,src={auth_home.resolve()},dst={CONTAINER_CODEX_HOME}",
            ]
    append_proxy_environment(argv, "HTTPS_PROXY", https_proxy or os.environ.get("HTTPS_PROXY"))
    append_proxy_environment(argv, "HTTP_PROXY", http_proxy or os.environ.get("HTTP_PROXY"))
    append_proxy_environment(argv, "NO_PROXY", no_proxy or os.environ.get("NO_PROXY"))
    argv.extend([image, "login", "status"])
    return argv


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
            text=True, encoding="utf-8", errors="replace", capture_output=True, check=False,
        )
        value = (result.stdout or "").strip()
        return value if result.returncode == 0 and value else "unavailable"
    except (OSError, subprocess.SubprocessError):
        return "unavailable"


def write_output(stream, value: str) -> None:
    """Write candidate text without letting a narrow Windows console abort the run."""
    try:
        stream.write(value)
    except UnicodeEncodeError:
        buffer = getattr(stream, "buffer", None)
        if buffer is not None:
            buffer.write(value.encode("utf-8", errors="replace"))
        else:
            encoding = getattr(stream, "encoding", None) or "utf-8"
            stream.write(value.encode(encoding, errors="replace").decode(encoding, errors="replace"))
    stream.flush()


def temporary_auth_copy(source: Path | None) -> Path | None:
    """Copy auth.json byte-for-byte to a private, writable temporary Codex home.

    The file is never parsed, projected, logged, or hashed. The private home is
    mounted read-write because Codex may refresh tokens.
    POSIX permissions are 0700 for the directory and 0600 for the file; the
    container uses the invoking UID/GID. Windows retains image-user behavior.
    """
    if source is None:
        return None
    home = Path(tempfile.mkdtemp(prefix="alf-auth-home-"))
    target = home / "auth.json"
    try:
        with source.open("rb") as source_handle:
            with target.open("wb") as handle:
                while True:
                    chunk = source_handle.read(1024 * 1024)
                    if not chunk:
                        break
                    handle.write(chunk)
        os.chmod(target, 0o600)
        os.chmod(home, 0o700)
        if os.name != "nt":
            os.chown(home, os.getuid(), os.getgid())
            os.chown(target, os.getuid(), os.getgid())
        return home
    except Exception:
        remove_temporary_auth_home(home)
        raise


def remove_temporary_auth_home(home: Path | None) -> None:
    """Remove credential material and fail visibly if any of it remains."""
    if home is None:
        return
    try:
        shutil.rmtree(home)
    except OSError as exc:
        raise RuntimeError("failed to remove temporary Codex authentication home") from exc
    if home.exists():
        raise RuntimeError("temporary Codex authentication home still exists")


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
    parser.add_argument("--environment-profile", default=os.environ.get("ALF_ENVIRONMENT_PROFILE_PATH"))
    parser.add_argument("--docker-network")
    parser.add_argument("--https-proxy")
    parser.add_argument("--http-proxy")
    parser.add_argument("--no-proxy")
    args = parser.parse_args(argv)
    workspace = Path(args.workspace).expanduser().resolve()
    if not workspace.is_dir():
        parser.error(f"workspace is not a directory: {workspace}")

    route_profile_sha256: str | None = None
    environment_profile_id: str | None = None
    if args.environment_profile:
        profile_path = Path(args.environment_profile).expanduser()
        if not profile_path.is_absolute():
            profile_path = REPOSITORY_ROOT / profile_path
        route_profile = load_environment_profile(
            profile_path, repository_root=REPOSITORY_ROOT
        )
        network = route_profile["docker_network"]
        proxy = route_profile["connect_proxy"]
        expected_proxy = f"http://{network['bridge_gateway']}:{proxy['remote_port']}"
        args.docker_network = args.docker_network or network["name"]
        args.https_proxy = args.https_proxy or expected_proxy
        args.http_proxy = args.http_proxy or expected_proxy
        args.no_proxy = args.no_proxy or ",".join(network["no_proxy"])
        validate_container_route(
            route_profile,
            docker_network=args.docker_network,
            https_proxy=args.https_proxy,
            http_proxy=args.http_proxy,
            no_proxy=args.no_proxy,
        )
        route_profile_sha256 = "sha256:" + environment_profile_sha256(route_profile)
        environment_profile_id = route_profile["profile_id"]
    else:
        args.docker_network = args.docker_network or os.environ.get(
            "ALF_DOCKER_NETWORK", "bridge"
        )
        args.https_proxy = args.https_proxy or os.environ.get("HTTPS_PROXY")
        args.http_proxy = args.http_proxy or os.environ.get("HTTP_PROXY")
        args.no_proxy = args.no_proxy or os.environ.get("NO_PROXY")
    if args.prompt is not None:
        task = args.prompt
    elif args.prompt_file:
        task = Path(args.prompt_file).read_text(encoding="utf-8")
    else:
        task = sys.stdin.read()
    auth_source = resolve_auth_path(args.auth)
    host_memory = None
    try:
        host_requirement = parse_requirement(os.environ.get("ALF_HOST_MEMORY"))
        host_memory = evaluate_host_memory(host_requirement) if host_requirement else None
    except Exception as exc:
        host_memory = {"observed_at": datetime.now(timezone.utc).isoformat(),
                       "platform": platform.system(), "thresholds": {},
                       "probe_error": str(exc), "ok": False}
    if host_memory is not None and not host_memory["ok"]:
        target = workspace / ".alf" / "usage.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps({"model": args.model, "host_memory": host_memory,
                                      "host_memory_gate": "failed", "returncode": 75,
                                      "image": args.image, "image_id": "not-probed",
                                      "docker_network": args.docker_network,
                                      "proxy_configured": bool(args.https_proxy or args.http_proxy),
                                      "environment_profile_id": environment_profile_id,
                                      "route_profile_sha256": route_profile_sha256,
                                      "reasoning_effort": args.reasoning_effort,
                                      "container_limits": {"memory": args.memory, "cpus": args.cpus, "pids": args.pids_limit},
                                      "auth_ok": None, "auth_cache_staged": False,
                                      "auth_cleanup_ok": None, "timed_out": False,
                                      "derived_from_codex_jsonl": False,
                                      "input_tokens": 0, "cached_input_tokens": 0,
                                      "cache_write_input_tokens": 0, "output_tokens": 0,
                                      "reasoning_output_tokens": 0, "tool_calls": 0,
                                      "accounting_valid": False, "usage_available": False,
                                      "usage_record_count": 0, "event_count": 0,
                                      "command_count": 0, "file_change_count": 0,
                                      "failed_event_count": 0, "file_reads": 0,
                                      "unique_file_reads": 0, "file_revisits": 0}) + "\n", encoding="utf-8")
        return 75
    auth = temporary_auth_copy(auth_source)
    image_id = image_identifier(args.image)
    cleanup_error: RuntimeError | None = None
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
            docker_network=args.docker_network,
            https_proxy=args.https_proxy,
            http_proxy=args.http_proxy,
            no_proxy=args.no_proxy,
        )
    except Exception:
        remove_temporary_auth_home(auth)
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
                    build_login_status_argv(
                        auth,
                        args.image,
                        docker_network=args.docker_network,
                        https_proxy=args.https_proxy,
                        http_proxy=args.http_proxy,
                        no_proxy=args.no_proxy,
                    ),
                    text=True,
                    encoding="utf-8",
                    errors="replace",
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
                encoding="utf-8",
                errors="replace",
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
        try:
            remove_temporary_auth_home(auth)
        except RuntimeError as exc:
            cleanup_error = exc
    write_output(sys.stdout, completed.stdout)
    write_output(sys.stderr, completed.stderr)
    if cleanup_error is not None:
        write_output(sys.stderr, "Codex authentication cleanup failed\n")
    write_usage(workspace, completed.stdout, args.model, args.image)
    sidecar = workspace / ".alf" / "usage.json"
    data = json.loads(sidecar.read_text(encoding="utf-8"))
    data["image_id"] = image_id
    data["reasoning_effort"] = args.reasoning_effort
    data["docker_network"] = args.docker_network
    data["proxy_configured"] = bool(args.https_proxy or args.http_proxy)
    data["environment_profile_id"] = environment_profile_id
    data["route_profile_sha256"] = route_profile_sha256
    data["timed_out"] = timed_out
    # Cleanup is part of the authentication lifecycle. Treat a retained cache
    # as an authentication-infrastructure failure so it cannot become a
    # candidate outcome merely because the model request itself completed.
    data["auth_ok"] = False if cleanup_error is not None else auth_ok
    data["auth_cache_staged"] = auth is not None
    data["auth_cleanup_ok"] = None if auth is None else cleanup_error is None
    data["container_limits"] = {
        "memory": args.memory,
        "cpus": args.cpus,
        "pids": args.pids_limit,
    }
    if host_memory is not None:
        data["host_memory"] = host_memory
    sidecar.write_text(json.dumps(data, sort_keys=True) + "\n", encoding="utf-8")
    return 79 if cleanup_error is not None else completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
