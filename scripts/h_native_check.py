"""Model-free native composition acceptance for the H1/H2 replays.

This deliberately composes the frozen E3a loopback probe.  It does not add a
transport, contact a provider, or infer anything about provider context limits.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from alf import h_check, h_workload  # noqa: E402

NATIVE_SHA256 = "72cf14453c1879996b970accc7de9aa114bf570e586230799a429d0741bb1959"
NO_TOOLS_CONFIG = ("features.no_tools=true", "features.single_response=true",
                   "features.code_mode_host=false")


def _load_probe():
    path = ROOT / "scripts" / "e3a_codex_check.py"
    spec = importlib.util.spec_from_file_location("h_e3a_codex_check", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load unchanged E3a native probe")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_replays(root: Path, specification: Path) -> list[dict[str, Any]]:
    """Build references through the H checker; never duplicate serialization."""
    spec = json.loads(specification.read_text(encoding="utf-8"))
    result = []
    for level in h_check.LEVELS:
        payload = h_workload.public_payload(root, level)
        for language in h_check.LANGUAGES:
            source = h_workload.source_for(root, level, language)
            for reverse in (False, True):
                order = h_workload.ordered_filenames(source, language, reverse)
                for access in h_check.ACCESSES:
                    requests, _ = h_check.reference_requests(
                        source, order, payload, language, access, spec, include_token_proxy=False)
                    for index, replay in enumerate(requests):
                        phase = "initial" if index == 0 else "final" if index == len(requests) - 1 else "read"
                        result.append({"level": level, "language": language,
                            "file_order": "reverse" if reverse else "forward", "access": access,
                            "phase": phase, "request_index": index, "replay": replay})
    return result


def _authored_text(data: object) -> list[str]:
    if not isinstance(data, dict) or not isinstance(data.get("input"), list):
        return []
    texts = []
    for message in data["input"]:
        if not isinstance(message, dict) or message.get("role") != "user":
            continue
        content = message.get("content")
        for part in content if isinstance(content, list) else [content]:
            text = part.get("text") if isinstance(part, dict) else part
            if isinstance(text, str):
                texts.append(text)
    return texts


def run_one(probe: Any, codex: str, replay: bytes, fixture: str, timeout: float) -> dict[str, Any]:
    try:
        prompt = replay.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("canonical H replay is not UTF-8") from exc
    if not prompt.endswith("\n"):
        raise ValueError("canonical H replay must end in one LF")
    # The unchanged loopback probe appends one LF while constructing stdin.
    # Remove exactly the canonical terminal LF here so captured authored bytes
    # equal the already measured replay rather than replay plus another LF.
    probe_prompt = prompt[:-1]
    original_prompt, original_summary = probe.PROMPT, probe._summarize_body

    def summarize(raw: bytes) -> dict[str, object]:
        summary = original_summary(raw)
        try:
            texts = _authored_text(json.loads(raw.decode("utf-8")))
        except (UnicodeDecodeError, json.JSONDecodeError):
            texts = []
        summary["authored_user_texts"] = [
            {"bytes": len(text.encode("utf-8")), "sha256": _sha(text.encode("utf-8"))}
            for text in texts]
        return summary

    probe.PROMPT, probe._summarize_body = probe_prompt, summarize
    try:
        report = probe.run_probe(codex, timeout=timeout, configs=NO_TOOLS_CONFIG,
                                 fixture_mode=fixture, expect_no_tools=True)
    finally:
        probe.PROMPT, probe._summarize_body = original_prompt, original_summary
    bodies = report.get("request_bodies")
    request = bodies[0] if isinstance(bodies, list) and len(bodies) == 1 else {}
    observed = request.get("authored_user_texts", []) if isinstance(request, dict) else []
    exact = {"bytes": len(replay), "sha256": _sha(replay)}
    occurrences = sum(item == exact for item in observed)
    text_match = bool(observed and observed[-1] == exact and occurrences == 1)
    native_messages = observed[:-1] if text_match else [item for item in observed if item != exact]
    passed = bool(probe.probe_passed(report) and text_match)
    return {"fixture": fixture, "passed": passed, "text_match": text_match,
            "expected": exact, "canonical_occurrences": occurrences,
            "observed": observed, "probe_passed": bool(probe.probe_passed(report)),
            "native_added_user_messages": native_messages,
            "native_added_user_message_count": len(native_messages),
            "request_count": report.get("request_count"),
            "total_post_attempts": report.get("total_post_attempts"),
            "no_tools_verified": report.get("no_tools_verified"),
            "gate_violations": report.get("gate_violations"),
            "returncode": report.get("returncode"), "safety_error": report.get("safety_error"),
            "candidate_model_calls": report.get("candidate_model_calls"),
            "real_provider_http_calls": report.get("real_provider_http_calls")}


def audit(codex: Path, specification: Path, timeout: float,
          fixtures: Iterable[str] = ("baseline", "tool-call")) -> dict[str, Any]:
    digest = _sha(codex.read_bytes()) if codex.is_file() else None
    failures = []
    if digest != NATIVE_SHA256:
        failures.append("native-sha256-mismatch")
        return {"status": "failed", "failures": failures, "native_sha256": digest,
                "expected_native_sha256": NATIVE_SHA256, "checks": [],
                "external_provider_requests": 0, "oauth_staged": False}
    probe, checks = _load_probe(), []
    for item in canonical_replays(ROOT, specification):
        replay = item.pop("replay")
        for fixture in fixtures:
            check = {**item, **run_one(probe, str(codex), replay, fixture, timeout)}
            checks.append(check)
            if not check["passed"]:
                failures.append("probe:" + ":".join(str(check[k]) for k in
                    ("level", "language", "file_order", "access", "request_index", "fixture")))
    return {"status": "passed" if not failures else "failed", "failures": failures,
            "native_sha256": digest, "expected_native_sha256": NATIVE_SHA256,
            "checks": checks, "external_provider_requests": 0, "oauth_staged": False,
            "provider_context_limit": None, "subscription_usd": None}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--codex", required=True, type=Path)
    parser.add_argument("--specification", type=Path,
                        default=ROOT / "protocols/workstream-h1-h2/specification.json")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--timeout", type=float, default=120.0)
    args = parser.parse_args(argv)
    if args.output.exists():
        parser.error("refusing to overwrite native-probe evidence")
    report = audit(args.codex, args.specification, args.timeout)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes((json.dumps(report, indent=2, sort_keys=True) + "\n").encode("utf-8"))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
