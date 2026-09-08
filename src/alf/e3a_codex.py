"""Strict model-free boundary for the adopted OAuth/Codex E3a controller."""
from __future__ import annotations
import copy, hashlib, json, time
from dataclasses import dataclass
from typing import Any, Callable

MAX_SUBMISSION_BYTES = 49_152
MAX_CAPTURE_BYTES = 1_048_576

_STARTUP_DIAGNOSTICS = (
    {"type": "item.completed", "item": {"id": "item_0", "type": "error", "message":
        "Under-development features enabled: no_tools, single_response. Under-development features are incomplete and may behave unpredictably. To suppress this warning, set `suppress_unstable_features_warning = true` in /tmp/alf-codex-home/config.toml."}},
    {"type": "item.completed", "item": {"id": "item_1", "type": "error", "message":
        "Code Mode is unavailable because code-mode host is disabled. Code mode will fail closed; enable `features.code_mode_host` and install `codex-code-mode-host`."}},
)

class CodexBoundaryError(ValueError): pass

@dataclass
class DispatchGuard:
    ceiling: int
    dispatched: int = 0
    def debit(self) -> int:
        if type(self.ceiling) is not int or not 0 < self.ceiling <= 72:
            raise CodexBoundaryError("invalid dispatch ceiling")
        if self.dispatched >= self.ceiling:
            raise CodexBoundaryError("dispatch ceiling exhausted")
        self.dispatched += 1
        return self.dispatched

def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))

def build_replay(instructions: str, entries: list[dict[str, Any]], final: dict[str, Any]) -> bytes:
    if not isinstance(instructions, str): raise CodexBoundaryError("instructions must be text")
    value = {"instructions": instructions, "transcript": [*copy.deepcopy(entries), {"role": "user", "data": copy.deepcopy(final)}]}
    return (_json(value) + "\n").encode()

def normalize_cli_usage(raw: Any) -> dict[str, Any]:
    source = copy.deepcopy(raw)
    raw = raw if isinstance(raw, dict) else {}
    values, invalid = {}, []
    for name in ("input_tokens", "cached_input_tokens", "cache_write_input_tokens", "output_tokens", "reasoning_output_tokens"):
        value = raw.get(name)
        if value is not None and (type(value) is not int or value < 0): invalid.append(name); value = None
        elif name not in {"input_tokens", "output_tokens"} and value == 0: value = None
        values[name] = value
    for total, subset in (("input_tokens", "cached_input_tokens"), ("input_tokens", "cache_write_input_tokens"), ("output_tokens", "reasoning_output_tokens")):
        if values[total] is not None and values[subset] is not None and values[subset] > values[total]: invalid.append(subset)
    if all(values[k] is not None for k in ("input_tokens", "cached_input_tokens", "cache_write_input_tokens")) and values["cached_input_tokens"] + values["cache_write_input_tokens"] > values["input_tokens"]:
        invalid.append("input_token_subsets")
    total = raw.get("total_tokens")
    if total is not None and (type(total) is not int or total < 0 or (values["input_tokens"] is not None and values["output_tokens"] is not None and total != values["input_tokens"] + values["output_tokens"])): invalid.append("total_tokens")
    return {**values, "invalid_fields": sorted(set(invalid)), "totals_available": values["input_tokens"] is not None and values["output_tokens"] is not None, "raw": source}

def _failed(reason: str, raw: str, usage: Any = None) -> dict:
    return {"status": "failed", "failure": reason, "raw": raw, "usage": normalize_cli_usage(usage)}

def parse_cli_jsonl(raw: bytes | str) -> dict[str, Any]:
    data = raw.encode() if isinstance(raw, str) else bytes(raw)
    if len(data) > MAX_CAPTURE_BYTES: return _failed("raw-capture-overflow", data[:MAX_CAPTURE_BYTES].decode("utf-8", "replace"))
    text = data.decode("utf-8", "replace")
    try: events = [json.loads(line) for line in text.splitlines() if line.strip()]
    except json.JSONDecodeError: return _failed("invalid-jsonl", text)
    if not all(isinstance(e, dict) for e in events): return _failed("invalid-cli-event", text)
    types = [e.get("type") for e in events]
    if any(types.count(k) != 1 for k in ("thread.started", "turn.started", "turn.completed")): return _failed("unexpected-cli-sequence", text)
    thread_index, turn_index, completed_index = (types.index(k) for k in ("thread.started", "turn.started", "turn.completed"))
    if thread_index != 0 or not (thread_index < turn_index < completed_index) or completed_index != len(types) - 1:
        return _failed("unexpected-cli-sequence", text)
    startup = events[1:turn_index]
    if startup not in ([], list(_STARTUP_DIAGNOSTICS)):
        return _failed("unexpected-cli-sequence", text)
    if any(k not in {"thread.started", "turn.started", "item.started", "item.updated", "item.completed", "turn.completed"} for k in types): return _failed("unexpected-cli-event", text)
    messages = []
    for event in events[turn_index + 1:completed_index]:
        if event.get("type") not in {"item.started", "item.updated", "item.completed"}: continue
        item = event.get("item")
        if not isinstance(item, dict): return _failed("invalid-cli-item", text)
        if item.get("type") == "reasoning": continue
        if item.get("type") != "agent_message": return _failed("unexpected-cli-item", text)
        if event["type"] == "item.completed":
            if not isinstance(item.get("text"), str): return _failed("missing-final-reply", text)
            messages.append(item["text"])
    completed = next(e for e in events if e.get("type") == "turn.completed")
    if len(messages) > 1: return _failed("multiple-final-replies", text, completed.get("usage"))
    return {"status": "completed", "text": messages[0] if messages else "", "usage": normalize_cli_usage(completed.get("usage")), "raw": text, "response_id": completed.get("id"), "model": completed.get("model"), "startup_diagnostics": copy.deepcopy(startup)}

def _get(capture: Any, key: str) -> Any:
    return capture.get(key) if isinstance(capture, dict) else getattr(capture, key, None)

class CodexOAuthAdapter:
    is_live = True
    def __init__(self, spec: dict, transport: Any, *, record: Callable[[dict], None] = lambda _: None, clock: Callable[[], float] = time.monotonic, dispatch_guard: DispatchGuard | None = None):
        self.spec, self.transport, self.record, self.clock = spec, transport, record, clock
        self.is_live = bool(getattr(transport, "is_live", True))
        self.guard = dispatch_guard or DispatchGuard(spec.get("budgets", {}).get("pilot_dispatch_ceiling", 72))
        self._instructions = None; self._initial = None; self._entries = []; self._halt = False

    def generate(self, payload: dict, previous_id: str | None, source: dict, feedback: dict | None, deadline: float) -> dict:
        del previous_id
        started = self.clock()
        base = {"id": None, "status": "failed", "text": None, "dispatch_attempted": False, "usage": normalize_cli_usage(None)}
        if self.is_live and not (self.spec.get("execution_authorized") and self.spec.get("user_live_execution_approved")): return {**base, "batch_stop": True, "failure": "execution-not-authorized"}
        if self._halt: return {**base, "batch_stop": True, "failure": "accounting-alarm"}
        instructions = payload.get("instructions")
        if not isinstance(instructions, str): return {**base, "batch_stop": True, "failure": "missing-instructions"}
        if self._instructions is None:
            self._instructions = instructions
            self._initial = {k: copy.deepcopy(v) for k, v in payload.items() if k not in {"instructions", "source"}}
        elif instructions != self._instructions: return {**base, "batch_stop": True, "failure": "instructions-changed"}
        final = ({**copy.deepcopy(self._initial), "source": copy.deepcopy(source)} if not self._entries else {"source": copy.deepcopy(source), "development_feedback": copy.deepcopy(feedback)})
        replay = build_replay(instructions, self._entries, final); digest = hashlib.sha256(replay).hexdigest()
        if len(replay) > self.spec.get("authority", {}).get("max_replay_bytes", 131_072): return {**base, "batch_stop": False, "failure": "trajectory-input-byte-budget-exhausted", "elapsed_seconds": self.clock()-started, "stdin_bytes": len(replay), "stdin_sha256": digest}
        if deadline <= self.clock(): return {**base, "batch_stop": True, "failure": "trajectory-deadline"}
        try: number = self.guard.debit()
        except Exception as exc: return {**base, "batch_stop": True, "failure": type(exc).__name__}
        self.record({"event": "dispatch-debited", "dispatch": number, "stdin_bytes": len(replay),
                     "stdin_sha256": digest, "stdin_utf8": replay.decode("utf-8")})
        result = {**base, "id": f"local-dispatch-{number}", "dispatch_attempted": True, "stdin_bytes": len(replay), "stdin_sha256": digest}
        try:
            capture = self.transport.launch(replay, min(deadline-self.clock(), 120.0))
            stdout, stderr = _get(capture, "stdout"), _get(capture, "stderr")
            if not isinstance(stdout, (str, bytes)) or not isinstance(stderr, (str, bytes)): raise CodexBoundaryError("invalid transport capture")
            out = stdout.encode() if isinstance(stdout, str) else bytes(stdout); err = stderr.encode() if isinstance(stderr, str) else bytes(stderr)
            retained_out = out[:MAX_CAPTURE_BYTES]
            retained_err = err[:max(0, MAX_CAPTURE_BYTES-len(retained_out))]
            result.update(raw_stdout=retained_out.decode("utf-8", "replace"), raw_stderr=retained_err.decode("utf-8", "replace"), returncode=_get(capture,"returncode"), timed_out=_get(capture,"timed_out"), output_overflow=_get(capture,"output_overflow"), cleanup_confirmed=_get(capture,"cleanup_confirmed"))
            if type(result["returncode"]) is not int or any(type(result[k]) is not bool for k in ("timed_out","output_overflow","cleanup_confirmed")): result.update(failure="invalid-transport-metadata", batch_stop=True)
            elif result["timed_out"]: result.update(failure="transport-timeout", batch_stop=True)
            elif result["output_overflow"] or len(out) + len(err) > MAX_CAPTURE_BYTES: result.update(failure="raw-capture-overflow", batch_stop=True)
            elif not result["cleanup_confirmed"]: result.update(failure="cleanup-unconfirmed", batch_stop=True)
            elif result["returncode"] != 0: result.update(failure="transport-nonzero-exit", batch_stop=True)
            else: result.update(parse_cli_jsonl(out)); result["batch_stop"] = result["status"] != "completed"
            usage = result.get("usage") or normalize_cli_usage(None)
            if result.get("status") == "completed" and (usage["invalid_fields"] or not usage["totals_available"]): result.update(failure="accounting-unavailable-or-invalid", batch_stop=True); self._halt=True
            elif result.get("status") == "completed" and (usage["input_tokens"] > self.spec["budgets"]["request_input_tokens"] or usage["output_tokens"] > self.spec["budgets"]["request_output_tokens_including_reasoning"]): result.update(failure="reported-request-budget-exceeded", batch_stop=True); self._halt=True
            text = result.get("text")
            if result.get("status") == "completed" and len(text.encode()) > MAX_SUBMISSION_BYTES:
                result["status"] = "failed"
                result["submission_byte_overflow"] = True
                if not result.get("batch_stop"):
                    result.update(failure="terminal-submission-byte-budget-exhausted", batch_stop=False)
            if result.get("status") == "completed": self._entries.extend(({"role":"user","data":copy.deepcopy(final)}, {"role":"assistant","data":text}))
        except Exception as exc: result.update(failure=type(exc).__name__, batch_stop=True)
        result["elapsed_seconds"] = self.clock()-started
        self.record({"event":"dispatch-finished", "dispatch":number, "result":copy.deepcopy(result)})
        return result

    @staticmethod
    def replay_size(payload: dict) -> int:
        final = {k:copy.deepcopy(v) for k,v in payload.items() if k not in {"instructions","source"}}; final["source"] = copy.deepcopy(payload.get("source"))
        return len(build_replay(payload.get("instructions"), [], final))

OAuthCodexAdapter = CodexOAuthAdapter
