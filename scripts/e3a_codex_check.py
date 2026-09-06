#!/usr/bin/env python3
"""Model-free capability probe for the canonical Codex Responses transport.

This is deliberately a test utility, not an adapter or authentication relay.  The
only server it starts is a deterministic loopback SSE fixture.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import subprocess
import socket
import sys
import signal
import tempfile
import threading
import time
from typing import Callable, Sequence

MODEL = "gpt-5.6-luna"
PROMPT = "Reply with exactly: fixture capability probe. Do not use tools."
MAX_BODY = 256 * 1024
MAX_OUTPUT = 512 * 1024
DEFAULT_TIMEOUT = 45.0
FIXTURE_MODES = ("baseline", "tool-call")
TOOL_CALL_MARKER = "E3A_EXECUTED_42"
TOOL_CALL_INPUT = 'text("E3A_" + "EXECUTED_" + (17 + 25))'
NO_TOOLS_POLICY_ERROR = "no-tools policy rejected an unsolicited tool response item"
NO_TOOLS_CLI_ERROR = f"Fatal error: {NO_TOOLS_POLICY_ERROR}"
MAX_METADATA_DEPTH = 8
MAX_METADATA_NODES = 256
_IDENTIFIER_KEYS = {"type", "name", "role"}
_IDENTIFIER_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_.:-]{0,63}$")


def deterministic_sse(mode: str = "baseline") -> bytes:
    if mode not in FIXTURE_MODES:
        raise ValueError("unknown fixture mode")
    if mode == "tool-call":
        item = {"id": "custom_fixture_1", "type": "custom_tool_call", "call_id": "call_fixture_1",
                "namespace": "functions", "name": "exec", "input": ""}
        events = [
            ("response.created", {"type": "response.created", "response": {"id": "resp_fixture_tool_1"}}),
            ("response.output_item.added", {"type": "response.output_item.added", "output_index": 0, "item": item}),
            ("response.custom_tool_call_input.delta", {"type": "response.custom_tool_call_input.delta", "item_id": item["id"], "output_index": 0, "delta": TOOL_CALL_INPUT}),
            ("response.custom_tool_call_input.done", {"type": "response.custom_tool_call_input.done", "item_id": item["id"], "output_index": 0, "input": TOOL_CALL_INPUT}),
            ("response.output_item.done", {"type": "response.output_item.done", "output_index": 0, "item": {**item, "input": TOOL_CALL_INPUT}}),
            ("response.completed", {"type": "response.completed", "response": {"id": "resp_fixture_tool_1", "status": "completed", "usage": {"input_tokens": 11, "output_tokens": 4, "total_tokens": 15}}}),
        ]
    else:
        events = [
            ("response.created", {"type": "response.created", "response": {"id": "resp_fixture_1"}}),
            ("response.output_item.added", {"type": "response.output_item.added", "output_index": 0, "item": {"id": "msg_fixture_1", "type": "message", "role": "assistant", "content": []}}),
            ("response.output_text.delta", {"type": "response.output_text.delta", "item_id": "msg_fixture_1", "output_index": 0, "content_index": 0, "delta": "fixture capability probe."}),
            ("response.output_text.done", {"type": "response.output_text.done", "item_id": "msg_fixture_1", "output_index": 0, "content_index": 0, "text": "fixture capability probe."}),
            ("response.output_item.done", {"type": "response.output_item.done", "output_index": 0, "item": {"id": "msg_fixture_1", "type": "message", "role": "assistant", "content": [{"type": "output_text", "text": "fixture capability probe.", "annotations": []}]}}),
            ("response.completed", {"type": "response.completed", "response": {"id": "resp_fixture_1", "status": "completed", "usage": {"input_tokens": 11, "output_tokens": 4, "total_tokens": 15}}}),
        ]
    return b"".join((f"event: {name}\ndata: {json.dumps(data, separators=(',', ':'))}\n\n").encode() for name, data in events)


class _FixtureHandler(BaseHTTPRequestHandler):
    server_version = "e3a-fixture/1"

    def do_POST(self) -> None:  # noqa: N802
        self.connection.settimeout(2.0)
        self.server.post_attempts += 1  # type: ignore[attr-defined]
        is_extra = len(self.server.captured) >= 1
        if self.path != "/v1/responses" or (is_extra and self.server.fixture_mode != "tool-call"):  # type: ignore[attr-defined]
            self.server.rejected_post_count += 1  # type: ignore[attr-defined]
            if len(self.server.errors) < 8:  # type: ignore[attr-defined]
                self.server.errors.append("unexpected_path_or_extra_request")  # type: ignore[attr-defined]
            self.send_error(404 if self.path != "/v1/responses" else 429)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self.server.rejected_post_count += 1  # type: ignore[attr-defined]
            if len(self.server.errors) < 8:  # type: ignore[attr-defined]
                self.server.errors.append("malformed_content_length")  # type: ignore[attr-defined]
            self.send_error(400)
            return
        if length < 0 or length > MAX_BODY:
            self.server.rejected_post_count += 1  # type: ignore[attr-defined]
            if len(self.server.errors) < 8:  # type: ignore[attr-defined]
                self.server.errors.append("body_too_large_or_negative")  # type: ignore[attr-defined]
            self.send_error(413)
            return
        body = self.rfile.read(length)
        if len(self.server.captured) < 2:  # type: ignore[attr-defined]
            self.server.captured.append(body)  # type: ignore[attr-defined]
            self.server.paths.append(self.path)  # type: ignore[attr-defined]
            self.server.header_names.append(sorted(self.headers.keys()))  # type: ignore[attr-defined]
            self.server.content_encoding.append(self.headers.get("Content-Encoding"))  # type: ignore[attr-defined]
        if is_extra:
            self.server.rejected_post_count += 1  # type: ignore[attr-defined]
            if len(self.server.errors) < 8:  # type: ignore[attr-defined]
                self.server.errors.append("extra_request_rejected")  # type: ignore[attr-defined]
            self.send_error(400)
            return
        payload = deterministic_sse(self.server.fixture_mode)  # type: ignore[attr-defined]
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(payload)
        self.wfile.flush()

    def log_message(self, *_args: object) -> None:
        return


def fixture_server(mode: str = "baseline") -> tuple[HTTPServer, threading.Thread, str]:
    if mode not in FIXTURE_MODES:
        raise ValueError("unknown fixture mode")
    server = HTTPServer(("127.0.0.1", 0), _FixtureHandler)
    server.fixture_mode = mode  # type: ignore[attr-defined]
    server.post_attempts = 0  # type: ignore[attr-defined]
    server.rejected_post_count = 0  # type: ignore[attr-defined]
    server.captured = []  # type: ignore[attr-defined]
    server.paths = []  # type: ignore[attr-defined]
    server.header_names = []  # type: ignore[attr-defined]
    server.content_encoding = []  # type: ignore[attr-defined]
    server.errors = []  # type: ignore[attr-defined]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread, f"http://127.0.0.1:{server.server_port}/v1"


def build_argv(codex: str, cwd: Path, base_url: str, configs: Sequence[str] = ()) -> list[str]:
    args = [codex, "exec", "--json", "--ephemeral", "--ignore-user-config", "--ignore-rules",
            "--sandbox", "workspace-write", "--cd", str(cwd), "--color", "never", "--model", MODEL]
    provider = [
        "model_provider=fixture",
        "model_providers.fixture.name=fixture",
        f"model_providers.fixture.base_url={base_url}",
        "model_providers.fixture.requires_openai_auth=false",
        "model_providers.fixture.request_max_retries=0",
        "model_providers.fixture.stream_max_retries=0",
    ]
    provider.extend(["model_providers.fixture.wire_api=responses", "model_reasoning_effort=high"])
    for value in (*provider, *configs):
        if any(ch in value for ch in "\r\n\x00") or "=" not in value:
            raise ValueError("config must be a KEY=VALUE without control characters")
        key = value.split("=", 1)[0]
        safe = (key.startswith("features.") and value.split("=", 1)[1] in {"true", "false"}) or key == "model_reasoning_effort"
        if key == "model_reasoning_effort" and value.split("=", 1)[1] not in {"low", "medium", "high", "xhigh", "max"}:
            safe = False
        if value not in provider and not safe:
            raise ValueError("additional config is restricted to features.* or safe model settings")
        args.extend(["--config", value])
    args.append("-")
    return args


def clean_environment(home: Path) -> dict[str, str]:
    keep = {"PATH", "SystemRoot", "WINDIR", "TEMP", "TMP", "LANG", "LC_ALL"}
    env = {k: v for k, v in os.environ.items() if k in keep}
    env.update({"HOME": str(home), "CODEX_HOME": str(home), "NO_PROXY": "127.0.0.1,localhost"})
    for key in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy",
                "OPENAI_API_KEY", "CODEX_AUTH_FILE", "OPENAI_ORG_ID", "OPENAI_BASE_URL"):
        env.pop(key, None)
    return env


def loopback_only() -> bool:
    """Require the Docker --network none shape before any child is spawned."""
    if sys.platform != "linux":
        return False
    try:
        return {name for _, name in socket.if_nameindex()} == {"lo"}
    except OSError:
        return False


def _usage(value: object) -> dict[str, int] | None:
    if not isinstance(value, dict):
        return None
    result = {}
    for key in ("input_tokens", "output_tokens", "total_tokens", "cached_input_tokens", "reasoning_output_tokens"):
        if isinstance(value.get(key), int):
            result[key] = value[key]
    return result or None


def _metadata_inventory(value: object, *, max_depth: int = MAX_METADATA_DEPTH,
                        max_nodes: int = MAX_METADATA_NODES) -> dict[str, object]:
    """Return bounded raw structural metadata for request ``input`` and ``tools``.

    This intentionally reports shape, not tool semantics: object keys are retained,
    while values are retained only for the short identifier fields type/name/role.
    Text, schemas, commands and other values are never copied into the inventory.
    """
    objects: list[dict[str, object]] = []
    truncated = False
    visited = 0

    def visit(current: object, path: str, depth: int) -> None:
        nonlocal truncated, visited
        if depth > max_depth:
            truncated = True
            return
        if isinstance(current, dict):
            if visited >= max_nodes:
                truncated = True
                return
            visited += 1
            keys = sorted(str(key) for key in current)
            identifiers = []
            for key in sorted(_IDENTIFIER_KEYS):
                candidate = current.get(key)
                if isinstance(candidate, str) and _IDENTIFIER_RE.fullmatch(candidate):
                    identifiers.append({"key": key, "value": candidate})
            objects.append({"path": path, "keys": keys, "identifiers": identifiers})
            for key in sorted(current, key=str):
                visit(current[key], f"{path}.{key}", depth + 1)
        elif isinstance(current, list):
            for index, item in enumerate(current):
                visit(item, f"{path}[{index}]", depth + 1)

    visit(value, "$", 0)
    return {"objects": objects, "truncated": truncated}


def _summarize_body(raw: bytes) -> dict[str, object]:
    try:
        # The fixture has already enforced MAX_BODY.  Decode the complete body so
        # no-tools assertions cannot be fooled by a truncated metadata summary.
        data = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return {"json": False, "bytes": min(len(raw), MAX_BODY)}
    if not isinstance(data, dict):
        return {"json": True, "object": type(data).__name__}
    fields = ("tools", "input", "instructions", "previous_response_id", "max_output_tokens", "reasoning", "store",
              "tool_choice", "parallel_tool_calls", "text", "include")
    result: dict[str, object] = {"json": True, "request_keys": sorted(data),
            "fields_present": {key: key in data for key in fields},
            "body_bytes": min(len(raw), MAX_BODY)}
    result["raw_structural_metadata"] = {
        "input": _metadata_inventory(data.get("input")),
        "tools": _metadata_inventory(data.get("tools")),
    }
    for key in ("input", "instructions"):
        if key in data:
            encoded = json.dumps(data[key], sort_keys=True, separators=(",", ":")).encode()
            result[f"{key}_bytes"] = len(encoded)
            result[f"{key}_sha256"] = hashlib.sha256(encoded).hexdigest()
    for key in ("tools", "previous_response_id", "max_output_tokens", "reasoning", "store"):
        if key in data:
            value = data[key]
            if key != "tools":
                result[key] = value
                continue
            tools = value if isinstance(value, list) else []
            described = [item for item in tools if isinstance(item, dict)]
            children = [child for item in described
                        for child in (item.get("tools") if isinstance(item.get("tools"), list) else [])
                        if isinstance(child, dict)]
            result[key] = {
                "count": len(value) if isinstance(value, list) else None,
                "types": [item["type"] for item in (*described, *children) if isinstance(item.get("type"), str)],
                "names": [item["name"] for item in (*described, *children) if isinstance(item.get("name"), str)],
            }
    for key in ("model", "service_tier"):
        if key in data and isinstance(data[key], (str, int, float, bool)):
            result[key] = data[key]
    for key in ("parallel_tool_calls", "include"):
        value = data.get(key)
        if isinstance(value, (str, int, float, bool)) or (isinstance(value, list) and all(isinstance(x, str) for x in value)):
            result[key] = value
    for key in ("tool_choice", "text"):
        value = data.get(key)
        if isinstance(value, (str, int, float, bool)):
            result[key] = value
        elif isinstance(value, dict):
            result[key] = {name: value[name] for name in ("type", "name", "strict")
                           if isinstance(value.get(name), (str, int, float, bool))}
            if key == "text" and isinstance(value.get("format"), dict):
                result[key]["format"] = {name: value["format"][name] for name in ("type", "name", "strict")
                                          if isinstance(value["format"].get(name), (str, int, float, bool))}
    messages = data.get("input") if isinstance(data.get("input"), list) else []
    input_shape = []
    text_parts = []
    for message in messages:
        if not isinstance(message, dict):
            continue
        content = message.get("content")
        parts = content if isinstance(content, list) else [content]
        types, sizes = [], []
        for part in parts:
            part_type = part.get("type") if isinstance(part, dict) else "text" if isinstance(part, str) else type(part).__name__
            text_value = part.get("text") if isinstance(part, dict) else part if isinstance(part, str) else None
            types.append(part_type if isinstance(part_type, str) else "unknown")
            sizes.append(len(text_value.encode()) if isinstance(text_value, str) else len(json.dumps(part, sort_keys=True, separators=(",", ":")).encode()))
            if isinstance(text_value, str):
                text_parts.append(text_value)
        input_shape.append({"role": message.get("role") if isinstance(message.get("role"), str) else None,
                            "content_types": types, "content_bytes": sizes})
    joined_text = "\n".join(text_parts)
    markers = ("namespace functions", "functions.", "shell_command", "exec_command", "apply_patch", "## Tools", "# Tools")
    result["input_messages"] = input_shape
    result["input_lexical_markers"] = {marker: marker in joined_text for marker in markers}
    result["input_declaration_names"] = sorted(set(re.findall(r"(?m)^(?:namespace|type)\s+([A-Za-z_][A-Za-z0-9_]*)\b", joined_text)))
    result["no_tools_request_valid"] = _no_tools_request_valid(data)
    return result


def _contains_additional_tools(value: object) -> bool:
    if isinstance(value, dict):
        for key, child in value.items():
            normalized = re.sub(r"[^a-z0-9]", "", str(key).lower())
            if normalized == "additionaltools":
                return True
            if (str(key).lower() in {"type", "name", "kind", "tool"}
                    and isinstance(child, str)
                    and re.sub(r"[^a-z0-9]", "", child.lower()) == "additionaltools"):
                return True
            if isinstance(child, (dict, list)) and _contains_additional_tools(child):
                return True
    elif isinstance(value, list):
        return any(_contains_additional_tools(item) for item in value)
    return False


def _no_tools_request_valid(data: dict[str, object]) -> bool:
    root_tools = data.get("tools")
    inputs = data.get("input")
    return (isinstance(inputs, list) and all(isinstance(item, dict) for item in inputs)
            and ("tools" not in data or root_tools == [])
            and data.get("tool_choice") == "none"
            and not _contains_additional_tools(inputs))


def _native_no_tools_error(events: Sequence[object]) -> bool:
    """Accept only the native structured error event, never arbitrary text."""
    def has_message(value: object) -> bool:
        if isinstance(value, str):
            return value == NO_TOOLS_CLI_ERROR
        if isinstance(value, dict):
            return any(has_message(child) for child in value.values())
        if isinstance(value, list):
            return any(has_message(child) for child in value)
        return False

    for event in events:
        if isinstance(event, dict) and event.get("type") in {"error", "turn.failed"} and has_message(event):
            return True
    return False


def probe_passed(report: dict[str, object]) -> bool:
    if report.get("expect_no_tools"):
        requests = report.get("request_bodies")
        usage = report.get("cli_turn_completed_usage")
        request = requests[0] if isinstance(requests, list) and len(requests) == 1 and isinstance(requests[0], dict) else None
        common = (not report.get("timed_out") and not report.get("fixture_error")
                  and request is not None and request.get("path") == "/v1/responses"
                  and request.get("json") is True and request.get("no_tools_request_valid") is True
                  and request.get("tool_choice") == "none"
                  and request.get("model") == MODEL
                  and (request.get("reasoning") == "high"
                       or (isinstance(request.get("reasoning"), dict)
                           and request["reasoning"].get("effort") == "high"))
                  and request.get("fields_present", {}).get("input") is True
                  and not request.get("authorization_header_present")
                  and not request.get("api_key_header_present")
                  and report.get("total_post_attempts") == 1
                  and not report.get("tool_output_observations")
                  and not report.get("computed_tool_output_marker"))
        if report.get("fixture_mode", "baseline") == "baseline":
            return bool(common and report.get("returncode") == 0
                        and "turn.completed" in report.get("cli_event_types", [])
                        and not any(event_type in {"error", "turn.failed"}
                                    for event_type in report.get("cli_event_types", []))
                        and report.get("fixture_final_text") == "fixture capability probe."
                        and isinstance(usage, dict) and usage.get("input_tokens") == 11
                        and usage.get("output_tokens") == 4)
        return bool(common and report.get("returncode") is not None and report.get("returncode") != 0
                    and not report.get("tool_output_observations")
                    and not report.get("computed_tool_output_marker")
                    and "turn.completed" not in report.get("cli_event_types", [])
                    and report.get("fixture_final_text") is None
                    and _native_no_tools_error(report.get("cli_events", [])) and usage is None)
    if report.get("fixture_mode", "baseline") == "tool-call":
        return False
    requests = report.get("request_bodies")
    usage = report.get("cli_turn_completed_usage")
    if report.get("returncode") != 0 or report.get("timed_out") or report.get("fixture_error"):
        return False
    if not isinstance(requests, list) or len(requests) != 1 or not isinstance(requests[0], dict):
        return False
    request = requests[0]
    reasoning = request.get("reasoning")
    high_reasoning = reasoning == "high" or (isinstance(reasoning, dict) and reasoning.get("effort") == "high")
    return (request.get("path") == "/v1/responses" and request.get("json") is True
            and request.get("model") == MODEL and high_reasoning
            and request.get("fields_present", {}).get("input") is True
            and not request.get("authorization_header_present") and not request.get("api_key_header_present")
            and report.get("fixture_final_text") == "fixture capability probe."
            and isinstance(usage, dict) and usage.get("input_tokens") == 11 and usage.get("output_tokens") == 4)


def _tool_output_observations(raw_bodies: Sequence[bytes]) -> list[dict[str, object]]:
    """Summarize only matching tool-output items from follow-up request inputs."""
    observations = []
    for raw in raw_bodies[1:]:
        try:
            body = json.loads(raw[:MAX_BODY].decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue
        inputs = body.get("input") if isinstance(body, dict) else None
        if not isinstance(inputs, list):
            continue
        for item in inputs:
            if not isinstance(item, dict) or item.get("type") not in {"custom_tool_call_output", "function_call_output"}:
                continue
            if item.get("call_id") != "call_fixture_1":
                continue
            output = item.get("output")
            texts = []
            if isinstance(output, str):
                texts.append(output)
            elif isinstance(output, list):
                for part in output:
                    if isinstance(part, dict) and part.get("type") in {"output_text", "text"} and isinstance(part.get("text"), str):
                        texts.append(part["text"])
            standalone_marker = any(line.strip() == TOOL_CALL_MARKER for text in texts for line in text.splitlines())
            observations.append({"type": item["type"], "call_id": item["call_id"],
                                 "marker_present": item["type"] == "custom_tool_call_output" and standalone_marker})
    return observations


def run_probe(codex: str = "codex", *, timeout: float = DEFAULT_TIMEOUT,
              configs: Sequence[str] = (), runner: Callable[..., object] | None = None,
              fixture_mode: str = "baseline", expect_no_tools: bool = False) -> dict[str, object]:
    server, thread, base_url = fixture_server(fixture_mode)
    started = time.monotonic()
    proc = None
    stdout_size = 0
    stderr_size = 0
    try:
        with tempfile.TemporaryDirectory(prefix="e3a-codex-check-") as directory:
            root = Path(directory)
            home = root / "codex-home"
            work = root / "work"
            home.mkdir(); work.mkdir()
            if expect_no_tools and "features.no_tools=true" not in configs:
                raise ValueError("--expect-no-tools requires features.no_tools=true")
            argv = build_argv(codex, work, base_url, configs)
            env = clean_environment(home)
            if not loopback_only():
                return {"argv": argv, "version": "not-run", "request_bodies": [], "request_count": 0,
                        "fixture_mode": fixture_mode, "expect_no_tools": expect_no_tools,
                        "fixture_usage": None, "cli_turn_completed_usage": None, "observed_tool_events": [],
                        "total_post_attempts": server.post_attempts, "rejected_post_count": server.rejected_post_count,
                        "computed_tool_output_marker": False, "no_tools_verified": False,
                        "tool_output_observations": [], "gate_violations": [],
                        "returncode": None, "timed_out": False, "safety_error": "loopback-only Linux network required",
                        "probe_passed": False,
                        "candidate_model_calls": 0, "real_provider_http_calls": 0, "fixture_only": True,
                        "oauth_integration_verified": False}
            call = runner or subprocess.run
            subprocess.run(["git", "init", "--quiet", str(work)], cwd=str(work), env=env,
                           capture_output=True, text=True, timeout=10, check=False)
            try:
                version_result = call([codex, "--version"], cwd=str(work), env=env,
                                      text=True, capture_output=True, timeout=10, check=False)
                version = (getattr(version_result, "stdout", "") or "").strip()[:200]
            except (OSError, subprocess.SubprocessError) as exc:
                version = f"unavailable:{type(exc).__name__}"
            try:
                stdout_raw = b""; stderr_raw = b""
                with tempfile.TemporaryFile(mode="w+b") as stdout_file, tempfile.TemporaryFile(mode="w+b") as stderr_file:
                    proc = subprocess.Popen(argv, cwd=str(work), env=env, stdin=subprocess.PIPE,
                                            stdout=stdout_file, stderr=stderr_file, text=True, start_new_session=True)
                    try:
                        result = proc.communicate(PROMPT + "\n", timeout=timeout)
                        timed_out = False
                    except subprocess.TimeoutExpired:
                        timed_out = True
                        if sys.platform == "linux" and proc.pid:
                            os.killpg(proc.pid, signal.SIGKILL)
                        else:
                            proc.kill()
                        result = proc.communicate()
                    stdout_size = os.fstat(stdout_file.fileno()).st_size
                    stderr_size = os.fstat(stderr_file.fileno()).st_size
                    stdout_file.seek(0); stderr_file.seek(0)
                    stdout_raw = stdout_file.read(MAX_OUTPUT + 1)
                    stderr_raw = stderr_file.read(MAX_OUTPUT + 1)
                stdout = stdout_raw.decode("utf-8", errors="replace")
                stderr = stderr_raw.decode("utf-8", errors="replace")
                if isinstance(result, tuple) and not stdout_raw and not stderr_raw:
                    stdout, stderr = result
            except (OSError, subprocess.SubprocessError) as exc:
                timed_out = False; stdout = ""; stderr = str(exc)
            if isinstance(stdout, bytes): stdout = stdout.decode("utf-8", errors="replace")
            if isinstance(stderr, bytes): stderr = stderr.decode("utf-8", errors="replace")
            stdout = (stdout or "")[:MAX_OUTPUT]
            stderr = (stderr or "")[:MAX_OUTPUT]
            events = []
            event_objects = []
            nested_items = []
            cli_final_text = None
            cli_usage = None
            for line in stdout.splitlines():
                try:
                    item = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if isinstance(item, dict):
                    event_objects.append(item)
                    events.append(item.get("type"))
                    nested = item.get("item")
                    if isinstance(nested, dict) and isinstance(nested.get("type"), str):
                        nested_items.append(nested["type"])
                    if item.get("type") == "turn.completed":
                        cli_usage = _usage(item.get("usage"))
                    if item.get("type") == "item.completed" and isinstance(item.get("item"), dict):
                        child = item["item"]
                        if child.get("type") == "agent_message":
                            content = child.get("text", child.get("content"))
                            if isinstance(content, str):
                                cli_final_text = content
                            elif isinstance(content, list):
                                texts = [part.get("text") for part in content if isinstance(part, dict) and isinstance(part.get("text"), str)]
                                cli_final_text = "".join(texts)
            captures = [_summarize_body(body) for body in server.captured]
            fixture_errors = list(server.errors)
            if any(capture.get("json") is not True for capture in captures):
                fixture_errors.append("malformed_json_body")
            for index, capture in enumerate(captures):
                capture["path"] = server.paths[index]
                names = server.header_names[index]
                capture["header_names"] = names
                capture["authorization_header_present"] = any(name.lower() == "authorization" for name in names)
                capture["api_key_header_present"] = any(name.lower() in {"api-key", "x-api-key"} for name in names)
                capture["content_encoding"] = server.content_encoding[index]
            tool_outputs = _tool_output_observations(server.captured)
            marker_seen = any(item["marker_present"] for item in tool_outputs)
            gate_violations = []
            if fixture_mode == "tool-call":
                if not tool_outputs and not expect_no_tools:
                    gate_violations.append("tool_output_not_observed")
                elif tool_outputs and not marker_seen:
                    gate_violations.append("tool_output_marker_not_verified")
                if marker_seen:
                    gate_violations.append("forbidden_tool_execution_observed")
                if server.post_attempts > 1:
                    gate_violations.append("provider_followup_observed")
                if fixture_errors:
                    gate_violations.append("fixture_error")
                if timed_out:
                    gate_violations.append("cli_timeout")
                elif (not expect_no_tools and isinstance(getattr(proc, "returncode", None), int)
                      and proc.returncode != 0):
                    gate_violations.append("cli_error")
                if server.rejected_post_count > 1:
                    gate_violations.append("more_than_one_extra_post_rejected")
            return {"argv": argv, "version": version, "fixture_mode": fixture_mode, "expect_no_tools": expect_no_tools,
                    "request_bodies": captures,
                    "request_count": len(captures), "total_post_attempts": server.post_attempts,
                    "rejected_post_count": server.rejected_post_count,
                    "fixture_usage": {"input_tokens": 11, "output_tokens": 4, "total_tokens": 15},
                    "fixture_error": fixture_errors,
                    "cli_turn_completed_usage": cli_usage,
                    "fixture_final_text": cli_final_text if cli_final_text == "fixture capability probe." else None,
                    "cli_event_types": events, "cli_events": event_objects,
                    "cli_nested_item_types": nested_items,
                    "returncode": None if timed_out else getattr(proc, "returncode", None), "timed_out": timed_out,
                    "stderr_bytes": stderr_size, "stdout_bytes": stdout_size, "elapsed_seconds": round(time.monotonic() - started, 3),
                    "candidate_model_calls": 0, "real_provider_http_calls": 0, "fixture_only": True,
                    "oauth_integration_verified": False,
                    "observed_tool_events": [item for item in nested_items if item != "agent_message"],
                    "tool_output_observations": tool_outputs,
                    "computed_tool_output_marker": marker_seen,
                    # Filled only by main after the complete predicate is evaluated.
                    "no_tools_verified": False,
                    "native_no_tools_fixture_passed": False,
                    "gate_violations": gate_violations,
                    "stderr_tail": stderr[-2048:] if proc and getattr(proc, "returncode", None) != 0 else None}
    finally:
        server.shutdown(); server.server_close(); thread.join(timeout=2)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--codex", default="codex")
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT)
    parser.add_argument("--config", action="append", default=[])
    parser.add_argument("--fixture", choices=FIXTURE_MODES, default="baseline")
    parser.add_argument("--expect-no-tools", action="store_true")
    args = parser.parse_args(argv)
    report = run_probe(args.codex, timeout=args.timeout, configs=args.config, fixture_mode=args.fixture,
                       expect_no_tools=args.expect_no_tools)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    report["probe_passed"] = probe_passed(report)
    report["native_no_tools_fixture_passed"] = bool(args.expect_no_tools and report["probe_passed"])
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if report["probe_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
