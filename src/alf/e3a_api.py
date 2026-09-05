"""One no-tools Responses path, exact-chain count, and conservative reservations.

The default transport is disabled. Tests inject a mock; neither import nor CLI
discovery reads an API key or makes a network request. There is no retry path.
"""
from __future__ import annotations

import copy
import http.client
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from typing import Callable

from .protocol import canonical_json_hash
from .workstream_e3a import normalize_usage


class GuardFailure(ValueError):
    pass


class BudgetGuard:
    def __init__(self, spec: dict, *, max_requests: int, usd_ceiling: str, rates: dict,
                 checked_date: str | None = None):
        limits = spec["budgets"]
        self.input_cap = limits["request_input_tokens"]
        self.output_cap = limits["request_output_tokens_including_reasoning"]
        self.max_requests = max_requests
        self.ceiling = Decimal(usd_ceiling)
        if (type(max_requests) is not int or not 0 < max_requests <= 72 or
                not self.ceiling.is_finite() or not 0 < self.ceiling <= Decimal(str(limits["pilot_usd_ceiling"]))):
            raise GuardFailure("authorization exceeds the fixed pilot envelope")
        expected = {"model": spec["model"]["requested"], "service_tier": limits["service_tier"],
                    "input_reservation_rate": str(limits["reservation_input_usd_per_million"]),
                    "output_rate": str(limits["output_usd_per_million"]),
                    "checked_date": checked_date or datetime.now(timezone.utc).date().isoformat()}
        if any(rates.get(k) != v for k, v in expected.items()):
            raise GuardFailure("unverified, stale, changed, or unbounded rate assumptions")
        self.rates = copy.deepcopy(rates)
        try:
            self.count_rate = Decimal(rates["count_call_upper_usd"])
        except (KeyError, TypeError, ValueError, InvalidOperation):
            raise GuardFailure("ancillary count-call billing must be bounded") from None
        if not self.count_rate.is_finite() or self.count_rate < 0:
            raise GuardFailure("invalid ancillary count-call rate")
        self.input_rate = Decimal(expected["input_reservation_rate"])
        self.output_rate = Decimal(expected["output_rate"])
        if self.input_rate != Decimal("0.25") or self.output_rate != Decimal("1.20"):
            raise GuardFailure("review required for a different rate card")
        self.entries: list[dict] = []
        self.count_calls = 0

    @property
    def committed(self) -> Decimal:
        return sum((Decimal(entry["committed_usd"]) for entry in self.entries), self.count_calls * self.count_rate)

    def before_count(self) -> None:
        if len(self.entries) >= self.max_requests or self.count_calls >= self.max_requests:
            raise GuardFailure("request/count-call ceiling")
        if self.committed + self.count_rate + self.cost(0, self.output_cap) > self.ceiling:
            raise GuardFailure("reservation ceiling")
        self.count_calls += 1

    def cost(self, inputs: int, outputs: int) -> Decimal:
        return (inputs * self.input_rate + outputs * self.output_rate) / Decimal(1_000_000)

    def reserve(self, count: int) -> dict:
        if type(count) is not int or not 0 <= count <= self.input_cap:
            raise GuardFailure("invalid or over-limit retained-chain input count")
        maximum = self.cost(count, self.output_cap)
        if len(self.entries) >= self.max_requests or self.committed + maximum > self.ceiling:
            raise GuardFailure("reservation ceiling")
        entry = {"number": len(self.entries) + 1, "counted_input_tokens": count,
                 "reserved_usd": str(maximum), "committed_usd": str(maximum),
                 "state": "reserved", "dispatch_attempted": False, "observed_charge_usd": None}
        self.entries.append(entry)
        return entry

    def reconcile(self, entry: dict, response: dict) -> dict:
        usage = normalize_usage(response.get("usage"))
        # Missing optional subsets do not prevent a conservative upper bound.
        # Malformed totals, count drift, tier changes and ambiguity keep the full
        # reservation. No cache/reasoning subset is added to its parent total.
        if (not usage["totals_available"] or usage["invalid_fields"] or
                usage["input_tokens"] != entry["counted_input_tokens"] or
                usage["output_tokens"] > self.output_cap or
                response.get("service_tier") != self.rates["service_tier"] or
                response.get("model") != self.rates["model"]):
            entry["state"] = "held-unreconciled"
            raise GuardFailure("usage/count/model/tier reconciliation failed")
        entry["state"] = "usage-upper-bound"
        entry["committed_usd"] = str(self.cost(usage["input_tokens"], usage["output_tokens"]))
        entry["usage"] = usage
        return usage


class HttpTransport:
    """Fixed HTTPS endpoint in a killable local helper, with no ambient proxy.

    A killed request is ambiguous, not free. Keys go over stdin, never command
    arguments, request evidence, candidate execution, or environment variables.
    """
    is_live = True

    def __init__(self, api_key: str, *, enabled: bool = False):
        if not enabled:
            raise GuardFailure("live HTTP transport is not authorized")
        if not api_key or any(c in api_key for c in "\r\n\0"):
            raise ValueError("invalid API credential")
        self._key = api_key

    def post(self, path: str, body: dict, timeout: float) -> dict:
        if path not in {"/v1/responses", "/v1/responses/input_tokens"} or timeout <= 0:
            raise ValueError("invalid request path/deadline")
        process = subprocess.Popen([sys.executable, "-m", "alf.e3a_api", "--http-worker"],
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            out, _ = process.communicate(json.dumps({"key": self._key, "path": path, "body": body,
                                                    "timeout": timeout}).encode("utf-8"), timeout=timeout)
        except BaseException:
            process.kill()
            process.communicate()
            raise
        if process.returncode:
            raise OSError("HTTP worker failed; request may be ambiguous")
        return json.loads(out)


def _http_worker() -> None:
    request = json.load(sys.stdin)
    if request["path"] not in {"/v1/responses", "/v1/responses/input_tokens"}:
        raise ValueError("unsupported endpoint")
    connection = http.client.HTTPSConnection("api.openai.com", timeout=request["timeout"])
    try:
        connection.request("POST", request["path"], json.dumps(request["body"]),
                           {"Authorization": "Bearer " + request["key"], "Content-Type": "application/json"})
        response = connection.getresponse()
        raw = response.read(1_048_577)
        if len(raw) > 1_048_576:
            raise ValueError("provider response byte ceiling")
        # Do not retain a credential echoed by an authentication error.
        text = raw.decode("utf-8").replace(request["key"], "[REDACTED]")
        print(json.dumps({"http_status": response.status, "request_id": response.getheader("x-request-id"),
                          "body": json.loads(text)}, ensure_ascii=True))
    finally:
        connection.close()


class ResponsesAdapter:
    def __init__(self, spec: dict, transport, guard: BudgetGuard, *, record: Callable,
                 clock: Callable = time.monotonic, authorization_id: str | None = None):
        if getattr(transport, "is_live", True) and (not authorization_id or
                not spec["execution_authorized"] or not spec["model"]["account_access_verified"] or
                not guard.rates.get("account_verified") or
                guard.max_requests > spec["budgets"]["current_authorized_requests"] or
                guard.ceiling > Decimal(str(spec["budgets"]["current_authorized_experiment_spend_usd"]))):
            raise GuardFailure("separate live authorization and verified account/rates required")
        self.spec, self.transport, self.guard = spec, transport, guard
        self.record, self.clock = record, clock

    def generate(self, payload: dict, previous_id: str | None, source: dict, feedback: dict | None,
                 deadline: float) -> dict:
        started = self.clock()
        request_deadline = min(deadline, started + self.spec["budgets"]["request_timeout_seconds"])
        user_input = {k: v for k, v in payload.items() if k not in {"instructions", "source"}}
        user_input.update(source=source, development_feedback=feedback)
        common = {"model": self.spec["model"]["requested"], "instructions": payload["instructions"],
                  "input": [{"role": "user", "content": json.dumps(user_input, ensure_ascii=False)}],
                  "tools": [], "tool_choice": "none", "parallel_tool_calls": False,
                  "reasoning": {"effort": self.spec["model"]["reasoning_effort"],
                                "context": self.spec["model"]["reasoning_context"]},
                  "truncation": "disabled"}
        if previous_id:
            common["previous_response_id"] = previous_id
        entry = None
        raw = None
        result = {"id": None, "status": "failed", "text": None, "usage": None}

        def post(path, body):
            remaining = request_deadline - self.clock()
            if remaining <= 0:
                raise GuardFailure("request/trajectory deadline before dispatch")
            if path.endswith("input_tokens"):
                self.guard.before_count()
                self.record({"event": "count-dispatch", "body": body, "sha256": canonical_json_hash(body)})
            else:
                entry.update(state="dispatched", dispatch_attempted=True)
                self.record({"event": "generation-dispatch", "reservation": copy.deepcopy(entry)})
            reply = self.transport.post(path, copy.deepcopy(body), remaining)
            self.record({"event": "http-response", "path": path, "reply": reply})
            if self.clock() >= request_deadline:
                raise GuardFailure("request/trajectory deadline exceeded")
            if not isinstance(reply, dict) or reply.get("http_status") != 200 or not isinstance(reply.get("body"), dict):
                raise GuardFailure("provider HTTP/format failure")
            return reply["body"]

        try:
            if request_deadline <= self.clock():
                raise GuardFailure("trajectory deadline before count")
            counted = post("/v1/responses/input_tokens", common)
            if counted.get("object") != "response.input_tokens":
                raise GuardFailure("unexpected count response")
            entry = self.guard.reserve(counted.get("input_tokens"))
            body = {**common, "service_tier": self.spec["budgets"]["service_tier"],
                    "max_output_tokens": self.guard.output_cap, "store": True, "stream": False}
            self.record({"event": "generation-reserved", "reservation": copy.deepcopy(entry), "body": body})
            raw = post("/v1/responses", body)
            result.update(id=raw.get("id"), status=raw.get("status"), usage=raw.get("usage"))
            texts = []
            for item in raw.get("output", []):
                if item.get("type") == "reasoning":
                    continue
                if item.get("type") != "message" or item.get("role") != "assistant":
                    raise GuardFailure("unexpected provider tool/output item")
                for content in item.get("content", []):
                    if content.get("type") == "output_text" and isinstance(content.get("text"), str):
                        texts.append(content["text"])
                    elif content.get("type") == "refusal":
                        texts.append("")  # retained raw refusal; an output-format failure
                    else:
                        raise GuardFailure("unexpected provider content")
            result["text"] = "".join(texts)
            if not isinstance(raw.get("id"), str) or not raw["id"] or raw.get("previous_response_id") != previous_id:
                raise GuardFailure("missing/mismatched response lineage")
            if raw.get("status") != "completed":
                raise GuardFailure("incomplete or ambiguous generation")
            if any(raw.get("reasoning", {}).get(k) != v for k, v in common["reasoning"].items()):
                raise GuardFailure("effective reasoning context/effort is unverified")
            self.guard.reconcile(entry, raw)
        except (GuardFailure, OSError, ValueError, TypeError, AttributeError, subprocess.TimeoutExpired) as exc:
            if entry is not None and entry["state"] != "usage-upper-bound":
                if entry["dispatch_attempted"]:
                    entry["state"] = "held-unreconciled"
                else:
                    entry.update(state="not-dispatched", committed_usd="0")
            result.update(batch_stop=True, failure=str(exc) if isinstance(exc, GuardFailure) else type(exc).__name__)
        result.update(elapsed_seconds=self.clock() - started, raw_response=raw,
                      reservation=copy.deepcopy(entry), mock=not getattr(self.transport, "is_live", True))
        self.record({"event": "request-finished", "result": result})
        return result


if __name__ == "__main__":
    if sys.argv[1:] != ["--http-worker"]:
        raise SystemExit("No live command is exposed; use the reviewed controller after authorization.")
    _http_worker()
