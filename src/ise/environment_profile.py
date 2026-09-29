"""Validation and hashing for non-secret remote execution profiles."""
from __future__ import annotations

import hashlib
import ipaddress
import json
import re
from pathlib import Path
from typing import Any


class EnvironmentProfileError(ValueError):
    pass


def load_environment_profile(
    path: str | Path, *, repository_root: Path | None = None
) -> dict[str, Any]:
    candidate = Path(path).expanduser().resolve()
    if repository_root is not None:
        try:
            candidate.relative_to(repository_root.resolve())
        except ValueError as exc:
            raise EnvironmentProfileError("environment profile escapes repository") from exc
    try:
        value = json.loads(candidate.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise EnvironmentProfileError("environment profile is not valid JSON") from exc
    validate_environment_profile(value)
    return value


def validate_environment_profile(value: Any) -> None:
    if not isinstance(value, dict) or set(value) != {
        "schema_version",
        "profile_id",
        "docker_network",
        "connect_proxy",
        "ssh",
        "authentication",
    }:
        raise EnvironmentProfileError("environment profile fields are invalid")
    if value["schema_version"] != 1 or not re.fullmatch(
        r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}", value.get("profile_id", "")
    ):
        raise EnvironmentProfileError("environment profile identity is invalid")

    network = value["docker_network"]
    if not isinstance(network, dict) or set(network) != {
        "name", "internal", "bridge_gateway", "no_proxy"
    }:
        raise EnvironmentProfileError("docker network profile is invalid")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,127}", network.get("name", "")):
        raise EnvironmentProfileError("docker network name is invalid")
    try:
        gateway = ipaddress.ip_address(network.get("bridge_gateway", ""))
    except ValueError as exc:
        raise EnvironmentProfileError("docker bridge gateway is invalid") from exc
    if gateway.version != 4 or not gateway.is_private or network.get("internal") is not True:
        raise EnvironmentProfileError("docker network must be private and internal")
    if network.get("no_proxy") != ["127.0.0.1", "localhost"]:
        raise EnvironmentProfileError("NO_PROXY profile is invalid")

    proxy = value["connect_proxy"]
    if not isinstance(proxy, dict) or set(proxy) != {
        "local_bind", "local_port", "remote_port", "allowed_authority", "tls"
    }:
        raise EnvironmentProfileError("CONNECT proxy profile is invalid")
    if (
        proxy.get("local_bind") != "127.0.0.1"
        or proxy.get("allowed_authority") != "chatgpt.com:443"
        or proxy.get("tls") != "passthrough"
        or not all(
            isinstance(proxy.get(field), int)
            and not isinstance(proxy.get(field), bool)
            and 1 <= proxy[field] <= 65535
            for field in ("local_port", "remote_port")
        )
    ):
        raise EnvironmentProfileError("CONNECT proxy contract is invalid")

    if value["ssh"] != {
        "forward": "fixed-reverse",
        "owns_remote_command": True,
        "ambient_config": False,
    }:
        raise EnvironmentProfileError("SSH profile is invalid")
    if value["authentication"] != {
        "cache": "complete-ephemeral-writable",
        "cleanup": "required",
    }:
        raise EnvironmentProfileError("authentication profile is invalid")


def environment_profile_sha256(value: dict[str, Any]) -> str:
    validate_environment_profile(value)
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def validate_container_route(
    value: dict[str, Any],
    *,
    docker_network: str,
    https_proxy: str | None,
    http_proxy: str | None,
    no_proxy: str | None,
) -> None:
    validate_environment_profile(value)
    network = value["docker_network"]
    proxy = value["connect_proxy"]
    expected_proxy = f"http://{network['bridge_gateway']}:{proxy['remote_port']}"
    expected_no_proxy = ",".join(network["no_proxy"])
    if docker_network != network["name"]:
        raise EnvironmentProfileError("Docker network does not match environment profile")
    if https_proxy != expected_proxy or http_proxy != expected_proxy:
        raise EnvironmentProfileError("container proxy does not match environment profile")
    if no_proxy != expected_no_proxy:
        raise EnvironmentProfileError("NO_PROXY does not match environment profile")
