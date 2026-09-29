"""Finite, model-free H1/H2 controller and guarded dispatch boundary."""
from __future__ import annotations

import copy
import hashlib
import json
import re
import time
from types import MappingProxyType
from typing import Any, Callable, Mapping

from .e3a_codex import DispatchGuard, build_replay, normalize_cli_usage, parse_cli_jsonl
from .workstream_e3a import PolicyViolation, apply_submission, project_development

MAX_REPLY_BYTES = 49_152
MAX_WORKSPACE_BYTES = 65_536
MAX_AUTHORED_BYTES = 131_072
MAX_CAPTURE_BYTES = 1_048_576
MAX_DISPATCH_SECONDS = 120.0
MAX_TRAJECTORY_SECONDS = 600.0
EXECUTION_AUTHORIZED = False
USER_LIVE_EXECUTION_APPROVED = False


class HBoundaryError(ValueError):
    pass


def _constant(_: str) -> None:
    raise HBoundaryError("non-finite JSON number")


def _object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result = {}
    for key, value in pairs:
        if key in result:
            raise HBoundaryError("duplicate JSON key")
        result[key] = value
    return result


def _filename(value: Any) -> bool:
    return isinstance(value, str) and bool(re.fullmatch(
        r"[A-Za-z][A-Za-z0-9_]*\.(?:cs|fs|csproj|fsproj)", value))


def _text(raw: str | bytes) -> str:
    try:
        value = raw.decode("utf-8") if isinstance(raw, bytes) else raw
    except UnicodeError as exc:
        raise HBoundaryError("reply is not UTF-8") from exc
    if not isinstance(value, str) or any(0xD800 <= ord(char) <= 0xDFFF for char in value):
        raise HBoundaryError("reply is not Unicode text")
    return value


def parse_action(raw: str | bytes) -> dict[str, Any]:
    text = _text(raw)
    if len(text.encode("utf-8")) > MAX_REPLY_BYTES:
        raise HBoundaryError("reply byte ceiling exceeded")
    try:
        value = json.loads(text, object_pairs_hook=_object, parse_constant=_constant)
    except HBoundaryError:
        raise
    except (TypeError, ValueError, RecursionError) as exc:
        raise HBoundaryError("malformed JSON") from exc
    if not isinstance(value, dict) or not isinstance(value.get("action"), str) or value["action"] not in {"read", "submit"}:
        raise HBoundaryError("invalid action envelope")
    if value["action"] == "read":
        paths = value.get("paths")
        if (set(value) != {"action", "paths"} or not isinstance(paths, list)
                or not 1 <= len(paths) <= 8 or not all(isinstance(path, str) for path in paths)
                or len(paths) != len(set(paths))
                or not all(_filename(path) for path in paths)):
            raise HBoundaryError("invalid read envelope")
    else:
        files = value.get("files")
        if set(value) != {"action", "files"} or not isinstance(files, dict):
            raise HBoundaryError("invalid submit envelope")
        for path, content in files.items():
            if (not _filename(path) or not isinstance(content, str) or "\x00" in content
                    or "\r" in content or any(0xD800 <= ord(c) <= 0xDFFF for c in content)):
                raise HBoundaryError("invalid submission")
    return value


class HController:
    def __init__(self, source: Mapping[str, str], ordered_filenames: list[str] | tuple[str, ...],
                 contracts: Mapping[str, Any] | None = None, task: Mapping[str, Any] | None = None,
                 language: str = "csharp", access: str = "H2", byte_cap: int = MAX_AUTHORED_BYTES,
                 *, submission_spec: Mapping[str, Any], evaluator: Callable[[dict[str, str]], Any] | None = None):
        access = access.upper()
        names = tuple(ordered_filenames)
        if language not in {"csharp", "fsharp"} or access not in {"H1", "H2"}:
            raise HBoundaryError("invalid language/access")
        if type(byte_cap) is not int or not 0 <= byte_cap <= MAX_AUTHORED_BYTES:
            raise HBoundaryError("invalid authored-byte cap")
        if (not 1 <= len(names) <= 8 or len(names) != len(set(names))
                or len(names) != len({name.casefold() for name in names}) or set(names) != set(source)):
            raise HBoundaryError("filename/source mismatch")
        ordered = {}
        for name in names:
            value = source[name]
            if not _filename(name) or not isinstance(value, str) or "\x00" in value or "\r" in value:
                raise HBoundaryError("invalid pinned source")
            try:
                value.encode("utf-8")
            except UnicodeError as exc:
                raise HBoundaryError("source is not UTF-8") from exc
            ordered[name] = value
        if sum(len(value.encode("utf-8")) for value in ordered.values()) > MAX_WORKSPACE_BYTES:
            raise HBoundaryError("workspace ceiling exceeded")
        if not isinstance(submission_spec, Mapping) or "authority" not in submission_spec:
            raise HBoundaryError("submission authority is required")
        self._source = MappingProxyType(ordered)
        self.filenames, self.contracts, self.task = names, copy.deepcopy(dict(contracts or {})), copy.deepcopy(dict(task or {}))
        self.language, self.access, self.byte_cap = language, access, byte_cap
        self.submission_spec, self.evaluator = copy.deepcopy(dict(submission_spec)), evaluator
        self._resident: set[str] = set()
        self.reads = 0
        self.done = False
        self.raw_actions: list[str] = []
        self.history: list[dict[str, Any]] = []
        self.events: list[dict[str, Any]] = []
        self.requests: list[dict[str, Any]] = []
        self.hard_stop = False

    @property
    def source(self) -> dict[str, str]:
        return dict(self._source)

    def _serialize(self, resident: set[str], history: list[dict[str, Any]], reads: int) -> bytes:
        entries = []
        for name in self.filenames:
            value = self._source[name]
            entry = {"filename": name, "bytes": len(value.encode()),
                     "sha256": hashlib.sha256(value.encode()).hexdigest()}
            if self.access == "H1" or name in resident:
                entry["text"] = value
            entries.append(entry)
        phase = ("Return exactly one submit envelope now; reads are forbidden."
                 if self.access == "H1" else
                 ("Return exactly one read or submit envelope." if reads < 2
                  else "Return exactly one submit envelope now; no further read is allowed."))
        instructions = ("Complete the requested source edit without tools or commands. Reply with only compact JSON, "
            "with no markdown or extra text. Actions are exactly "
            "{\"action\":\"read\",\"paths\":[\"RootFile.cs\"]} or "
            "{\"action\":\"submit\",\"files\":{\"RootFile.cs\":\"full replacement text\"}}. "
            "Read paths must be 1-8 distinct eligible root filenames. Submit only eligible source/project files, "
            "using complete replacement text; do not delete files or change dependencies/build settings. " + phase)
        body = {"contracts": self.contracts, "task": self.task, "language": self.language,
                "access": self.access, "read_remaining": max(0, 2 - reads),
                "source": entries, "history": history}
        replay = build_replay(instructions, [], body)
        if len(replay) > self.byte_cap:
            raise HBoundaryError("authored-budget-exhausted")
        return replay

    def request(self) -> bytes:
        return self._serialize(set(self._resident), copy.deepcopy(self.history), self.reads)

    def _fail(self, raw: str | bytes, reason: str, retained: bool = False) -> None:
        try:
            text = _text(raw)
        except HBoundaryError:
            text = bytes(raw).decode("utf-8", "replace") if isinstance(raw, bytes) else str(raw)
        if not retained:
            self.raw_actions.append(text)
        self.history.append({"raw": text, "result": {"failure": reason}})
        self.done = True
        raise HBoundaryError(reason)

    def apply(self, raw: str | bytes) -> dict[str, Any]:
        if self.done:
            raise HBoundaryError("trajectory already finished")
        try:
            action = parse_action(raw)
        except HBoundaryError as exc:
            return self._fail(raw, str(exc))
        text = _text(raw)
        if action["action"] == "read":
            if self.access != "H2" or self.reads >= 2:
                return self._fail(text, "read-quota-exhausted")
            if any(path not in self._source for path in action["paths"]):
                return self._fail(text, "unknown-file")
            prospective = self._resident | set(action["paths"])
            results = []
            for name in self.filenames:
                if name in action["paths"]:
                    value = self._source[name]
                    results.append({"path": name, "returned": "reference" if name in self._resident else "full",
                                    "bytes": len(value.encode()), "sha256": hashlib.sha256(value.encode()).hexdigest()})
            event = {"action": "read", "paths": list(action["paths"]), "results": results}
            next_history = [*copy.deepcopy(self.history), {"raw": text, "result": copy.deepcopy(event)}]
            try:
                replay = self._serialize(prospective, next_history, self.reads + 1)
            except HBoundaryError as exc:
                return self._fail(text, str(exc))
            self.raw_actions.append(text)
            self._resident, self.reads, self.history = prospective, self.reads + 1, next_history
            self.events.append(copy.deepcopy(event))
            return {**event, "request": replay}
        self.raw_actions.append(text)
        try:
            encoded = json.dumps({"files": action["files"]}, ensure_ascii=False, separators=(",", ":"))
            workspace = apply_submission(dict(self._source), encoded, self.language, self.submission_spec)
            max_total_files = self.submission_spec["authority"]["max_total_files"]
            if type(max_total_files) is not int or not 1 <= max_total_files <= 8:
                raise HBoundaryError("invalid total-file authority")
            if len(workspace) > max_total_files:
                raise HBoundaryError("workspace file ceiling exceeded")
        except Exception as exc:
            if isinstance(exc, PolicyViolation):
                self.hard_stop = True
            return self._fail(text, f"{type(exc).__name__}:{exc}", retained=True)
        development = project_development(workspace, self.language)
        event = {"action": "submit", "files": copy.deepcopy(action["files"]),
                 "workspace": copy.deepcopy(workspace), "project_development": development}
        self.history.append({"raw": text, "result": copy.deepcopy(event)})
        self.events.append(copy.deepcopy(event))
        self.done = True
        return event

    def run_trajectory(self, transport: Any = None, deadline: float | None = None, *,
                       dispatcher: "TrajectoryDispatcher | None" = None) -> dict[str, Any]:
        if self.evaluator is None:
            return {"failure": "isolated-evaluator-required", "dispatches": [], "events": []}
        active = dispatcher or TrajectoryDispatcher(transport)
        now = active.clock()
        end = min(deadline if deadline is not None else now + MAX_TRAJECTORY_SECONDS,
                  now + MAX_TRAJECTORY_SECONDS)
        try:
            replay = self.request()
        except HBoundaryError as exc:
            return {"failure": str(exc), "dispatches": [], "events": []}
        dispatches = []
        while not self.done:
            result = active.dispatch(replay, end)
            dispatches.append(result)
            self.requests.append({"bytes": len(replay), "sha256": hashlib.sha256(replay).hexdigest(), "replay": replay})
            if result.get("status") != "completed":
                return {"failure": result.get("failure"), "dispatches": dispatches, "events": copy.deepcopy(self.events)}
            try:
                outcome = self.apply(result["text"])
            except HBoundaryError as exc:
                return {"failure": str(exc), "batch_stop": self.hard_stop,
                        "dispatches": dispatches, "events": copy.deepcopy(self.events)}
            if outcome["action"] == "submit":
                try:
                    evaluation = self.evaluator(copy.deepcopy(outcome["workspace"]), end) if self.evaluator else None
                except Exception as exc:
                    return {"failure": f"evaluator-infrastructure-{type(exc).__name__}", "batch_stop": True,
                            "submission": outcome, "dispatches": dispatches, "events": copy.deepcopy(self.events)}
                return {"submission": outcome, "evaluation": evaluation, "dispatches": dispatches, "events": copy.deepcopy(self.events)}
            replay = outcome["request"]
        raise AssertionError("unreachable")


class TrajectoryDispatcher:
    def __init__(self, transport: Any, ceiling: int = 64, *, allow_live: bool = False,
                 execution_authorized: bool = EXECUTION_AUTHORIZED,
                 user_live_execution_approved: bool = USER_LIVE_EXECUTION_APPROVED,
                 clock: Callable[[], float] = time.monotonic,
                 record: Callable[[dict[str, Any]], None] | None = None):
        if bool(getattr(transport, "is_live", True)) and not (
                allow_live is True and execution_authorized is True
                and user_live_execution_approved is True):
            raise HBoundaryError("live transport refused")
        self.transport, self.guard, self.clock = transport, DispatchGuard(ceiling), clock
        self.record, self.requests, self.halted = record or (lambda _: None), [], False

    @staticmethod
    def _get(capture: Any, key: str) -> Any:
        return capture.get(key) if isinstance(capture, dict) else getattr(capture, key, None)

    def dispatch(self, replay: bytes, deadline: float) -> dict[str, Any]:
        base = {"status": "failed", "usage": normalize_cli_usage(None), "usd": None}
        if self.halted:
            return {**base, "failure": "batch-stopped"}
        remaining = deadline - self.clock()
        if remaining <= 0:
            self.halted = True
            return {**base, "failure": "trajectory-deadline"}
        try:
            replay_text = bytes(replay).decode("utf-8")
        except UnicodeError:
            self.halted = True
            return {**base, "failure": "invalid-authored-replay-utf8"}
        try:
            number = self.guard.debit()
        except Exception as exc:
            self.halted = True
            return {**base, "failure": type(exc).__name__}
        kept = {"dispatch": number, "replay_utf8": replay_text, "bytes": len(replay),
                "sha256": hashlib.sha256(replay).hexdigest()}
        self.requests.append(kept)
        self.record({"event": "dispatch-debited", **copy.deepcopy(kept)})
        try:
            capture = self.transport.launch(replay, min(MAX_DISPATCH_SECONDS, remaining))
        except Exception as exc:
            result = {**base, "failure": f"launch-{type(exc).__name__}"}
        else:
            result = self._capture(capture, base)
            if self.clock() > deadline and not result.get("failure"):
                result.update(status="failed", failure="trajectory-deadline")
        if result.get("failure"):
            self.halted = True
        self.record({"event": "dispatch-finished", "dispatch": number, "result": copy.deepcopy(result)})
        return result

    def _capture(self, capture: Any, base: dict[str, Any]) -> dict[str, Any]:
        keys = ("stdout", "stderr", "returncode", "timed_out", "output_overflow", "cleanup_confirmed")
        values = {key: self._get(capture, key) for key in keys}
        if (not isinstance(values["stdout"], (bytes, str)) or not isinstance(values["stderr"], (bytes, str))
                or type(values["returncode"]) is not int or any(type(values[k]) is not bool for k in keys[3:])):
            return {**base, "failure": "invalid-transport-metadata"}
        stdout = values["stdout"].encode() if isinstance(values["stdout"], str) else values["stdout"]
        stderr = values["stderr"].encode() if isinstance(values["stderr"], str) else values["stderr"]
        result = {**base, "raw_stdout": stdout[:MAX_CAPTURE_BYTES].decode("utf-8", "replace"),
                  "raw_stderr": stderr[:MAX_CAPTURE_BYTES].decode("utf-8", "replace"),
                  **{key: values[key] for key in keys[2:]}}
        if values["timed_out"]:
            result["failure"] = "transport-timeout"
        elif values["output_overflow"] or len(stdout) + len(stderr) > MAX_CAPTURE_BYTES:
            result["failure"] = "raw-capture-overflow"
        elif not values["cleanup_confirmed"]:
            result["failure"] = "cleanup-unconfirmed"
        elif values["returncode"] != 0:
            result["failure"] = "transport-nonzero-exit"
        else:
            result.update(parse_cli_jsonl(stdout))
            if (result.get("status") == "completed"
                    and (not isinstance(result.get("response_id"), str)
                         or not result["response_id"]
                         or not isinstance(result.get("model"), str)
                         or not result["model"])):
                result.update(status="failed", failure="ambiguous-dispatch")
        usage = result.get("usage", normalize_cli_usage(None))
        if not result.get("failure") and (usage["invalid_fields"] or not usage["totals_available"]
                or usage["input_tokens"] > 32_768 or usage["output_tokens"] > 8_192):
            result.update(status="failed", failure="usage-alarm")
        return result
