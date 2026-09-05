"""E3a submission policy, controller, and post-trajectory scoring.

Transport and isolated evaluation are injected; this module never executes code
or interprets candidate text as a command. Mocks do not verify provider behavior.
"""
from __future__ import annotations

import copy
import hashlib
import json
import random
import re
import time
import xml.etree.ElementTree as ET
from decimal import Decimal
from pathlib import Path
from typing import Any, Callable

from .protocol import canonical_json_hash
from .workstream_e2 import _materialize

PACKET_DIR = "protocols/workstream-e3a-v1"
ERROR_LINE = re.compile(r"\b(?:fatal\s+)?error\b", re.I)
USAGE_FIELDS = ("input_tokens", "cached_input_tokens", "cache_write_input_tokens", "output_tokens", "reasoning_output_tokens")


class SubmissionError(ValueError):
    """Candidate output did not meet the declared format."""


class PolicyViolation(SubmissionError):
    """Candidate attempted a forbidden change."""


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def snapshot(root: Path, manifest: dict, language: str, stage: int) -> dict[str, str]:
    """Reuse the accepted gold materializer; return source only, never build output."""
    import tempfile
    with tempfile.TemporaryDirectory(prefix="alf-e3a-source-") as tmp:
        work = Path(tmp)
        _materialize(root, manifest, language, stage, work)
        return {
            p.relative_to(work).as_posix(): p.read_text(encoding="utf-8")
            for p in sorted(work.iterdir()) if p.suffix in {".cs", ".fs", ".csproj", ".fsproj"}
        }


def schedule(spec: dict) -> list[dict]:
    rng = random.Random(spec["schedule_seed"])
    orders = {}
    for task in spec["tasks"]:
        first = spec["languages"] * (spec["repetitions"] // 2)
        rng.shuffle(first)
        orders[task] = first
    result = []
    for repetition in range(spec["repetitions"]):
        tasks = list(spec["tasks"])
        rng.shuffle(tasks)
        for task in tasks:
            first = orders[task][repetition]
            for language in [first, next(x for x in spec["languages"] if x != first)]:
                result.append({"task_id": task, "repetition": repetition + 1, "language": language})
    return result


def budget(spec: dict) -> dict:
    limits = spec["budgets"]
    trajectories = len(schedule(spec))
    calls = trajectories * (1 + spec["controller"]["max_repair_rounds"])
    input_ceiling = calls * limits["request_input_tokens"]
    output_ceiling = calls * limits["request_output_tokens_including_reasoning"]
    return {
        "trajectories": trajectories, "task_pairs": trajectories // 2,
        "max_requests": calls, "max_input_tokens": input_ceiling,
        "max_output_tokens_including_reasoning": output_ceiling,
        "max_request_wait_seconds": calls * limits["request_timeout_seconds"],
        "max_trajectory_seconds": trajectories * limits["trajectory_timeout_seconds"],
        "generation_reservation_upper_usd": str((
            input_ceiling * Decimal(str(limits["reservation_input_usd_per_million"]))
            + output_ceiling * Decimal(str(limits["output_usd_per_million"]))
        ) / Decimal(1_000_000)),
        "authorized_requests": limits["current_authorized_requests"],
    }


def development_cases(manifest: dict, stage: int) -> list[dict]:
    """Existing contract cases through the current task, never final holdout."""
    return copy.deepcopy(manifest["baseline_cases"] + [
        case for task in manifest["tasks"][:stage] for case in task["cases"]
    ])


def candidate_payload(root: Path, manifest: dict, language: str, task_id: str) -> dict:
    stage = next(i for i, task in enumerate(manifest["tasks"]) if task["id"] == task_id)
    return {
        "instructions": (root / PACKET_DIR / "candidate-instructions.md").read_text(encoding="utf-8"),
        "baseline_contract": (root / PACKET_DIR / "baseline-contract.md").read_text(encoding="utf-8"),
        "earlier_contracts": [(root / task["prompt"]).read_text(encoding="utf-8")
                              for task in manifest["tasks"][:stage]],
        "current_task": (root / manifest["tasks"][stage]["prompt"]).read_text(encoding="utf-8"),
        "source": snapshot(root, manifest, language, stage),
    }


def holdout_cases(root: Path, task_id: str) -> list[dict]:
    """Scorer-only, independently authored cases and a fixed transition matrix."""
    cases = read_json(root / PACKET_DIR / "holdout-cases.json")
    result = copy.deepcopy(cases["priority"])
    if task_id != "001-priority":
        result += copy.deepcopy(cases["transitions"] + cases["inherited_queries"])
        permitted = {("pending", "processing"), ("pending", "cancelled"),
                     ("processing", "completed"), ("processing", "cancelled")}
        for source in ["pending", "processing", "completed", "cancelled", "other"]:
            for target in ["pending", "processing", "completed", "cancelled", "other"]:
                result.append({
                    "name": f"matrix-{source}-{target}",
                    "input": {"operation": "TrAnSiTiOn", "id": "matrix-47", "toStatus": target.upper(),
                              "orders": [None, {"id": "matrix-47", "status": source.upper()}]},
                    "expected": ({"id": "matrix-47", "status": target} if (source, target) in permitted
                                 else {"error": "invalid transition"}),
                })
    return result


def structural_development(source: dict[str, str], language: str, task_id: str) -> dict:
    """Only the declared engine file/order, not a claim of semantic architecture."""
    errors = []
    if task_id == "007-query-engine-refactor":
        ext = "fs" if language == "fsharp" else "cs"
        if f"OrderFlowEngine.{ext}" not in source:
            errors.append(f"ERROR architecture: required OrderFlowEngine.{ext} is missing")
        if language == "fsharp":
            try:
                includes = [n.get("Include") for n in ET.fromstring(source["OrderFlow.fsproj"]).iter("Compile")]
            except ET.ParseError:
                includes = []
            if "OrderFlowEngine.fs" not in includes or "Program.fs" not in includes or (
                includes.index("OrderFlowEngine.fs") > includes.index("Program.fs")
            ):
                errors.append("ERROR architecture: compile OrderFlowEngine.fs before Program.fs")
    return {"passed": not errors, "category": "declared-file-order", "output": "\n".join(errors)}


def _unique_object(pairs: list[tuple[str, Any]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise SubmissionError("duplicate JSON key")
        result[key] = value
    return result


def _project_shape(text: str, *, strip_compile: bool) -> bytes:
    if "<!" in text or "<?" in text:
        raise PolicyViolation("project declarations/entities are forbidden")
    try:
        tree = ET.fromstring(text)
    except ET.ParseError as exc:
        raise SubmissionError("invalid project XML") from exc
    if strip_compile:
        for group in list(tree):
            if group.tag == "ItemGroup" and not group.attrib:
                for child in list(group):
                    if child.tag == "Compile":
                        if set(child.attrib) != {"Include"} or list(child) or (child.text or "").strip():
                            raise PolicyViolation("only simple Compile Include entries are allowed")
                        group.remove(child)
                if not list(group):
                    tree.remove(group)
    for node in tree.iter():
        node.text = (node.text or "").strip() or None
        node.tail = None
    return ET.tostring(tree)


def project_development(source: dict[str, str], language: str) -> dict:
    """Safe project mistakes are failed submissions, never compiled or fixed here."""
    errors = []
    ext = "fs" if language == "fsharp" else "cs"
    try:
        tree = ET.fromstring(source[f"OrderFlow.{ext}proj"])
    except ET.ParseError:
        errors.append("ERROR project: malformed project XML")
    else:
        if language == "fsharp":
            includes = [node.get("Include") for node in tree.iter("Compile")]
            sources = {p for p in source if p.endswith(".fs")}
            if len(includes) != len(set(includes)):
                errors.append("ERROR project: duplicate Compile Include")
            for path in sorted(set(includes) - sources):
                errors.append(f"ERROR project: Compile source missing: {path}")
            for path in sorted(sources - set(includes)):
                errors.append(f"ERROR project: source omitted from Compile: {path}")
            if includes[-1:] != ["Program.fs"]:
                errors.append("ERROR project: Program.fs must compile last")
    return {"passed": not errors, "build_passed": False if errors else None,
            "category": "project", "output": "\n".join(errors)}


def apply_submission(before: dict[str, str], raw: str, language: str, spec: dict,
                     *, project_reference: str | None = None) -> dict[str, str]:
    """Atomic in-memory replacements. The caller retains original raw bytes first."""
    if language not in {"csharp", "fsharp"}:
        raise ValueError("unsupported language")
    try:
        raw_bytes = raw.encode("utf-8")
    except UnicodeError as exc:
        raise SubmissionError("submission is not UTF-8") from exc
    if len(raw_bytes) > spec["authority"]["max_submission_bytes"]:
        raise SubmissionError("submission byte ceiling exceeded")
    try:
        body = json.loads(raw, object_pairs_hook=_unique_object)
    except (json.JSONDecodeError, UnicodeError) as exc:
        raise SubmissionError("invalid JSON") from exc
    if not isinstance(body, dict) or set(body) != {"files"} or not isinstance(body["files"], dict):
        raise SubmissionError("expected exactly a files object")
    extension = "fs" if language == "fsharp" else "cs"
    project = f"OrderFlow.{extension}proj"
    after = dict(before)
    for path, value in body["files"].items():
        if path != project and not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*\." + extension, path):
            raise PolicyViolation("path or file type outside approved source")
        if not isinstance(value, str) or "\x00" in value or "\r" in value:
            raise SubmissionError("file content must be LF text without NUL")
        try:
            value.encode("utf-8")
        except UnicodeError as exc:
            raise SubmissionError("file content is not UTF-8") from exc
        after[path] = value
    if len({path.casefold() for path in after}) != len(after):
        raise PolicyViolation("case-colliding paths are forbidden on both platforms")
    sources = [path for path in after if path.endswith(f".{extension}")]
    if len(sources) > spec["authority"]["max_source_files"] or sum(
        len(text.encode("utf-8")) for text in after.values()
    ) > spec["authority"]["max_workspace_bytes"]:
        raise SubmissionError("workspace ceiling exceeded")
    text = after[project]
    # Screen forbidden constructs even when XML is malformed. Malformed allowed
    # syntax is retained but NEVER sent to MSBuild. Repairs use the original
    # canonical project reference, not the previous malformed project.
    allowed_tags = {"Project", "PropertyGroup", "OutputType", "TargetFramework", "ImplicitUsings", "Nullable"}
    if language == "fsharp":
        allowed_tags |= {"ItemGroup", "Compile"}
    if "<!" in text or "<?" in text or re.search(r"[$@%]\(", text) or any(
        tag not in allowed_tags for tag in re.findall(r"</?([\w:.-]+)", text)
    ):
        raise PolicyViolation("forbidden project construct or expansion")
    # Recognizable unsafe values stay terminal even if a later XML delimiter is
    # missing. Incomplete allowed XML is retained, but never compiled.
    for _, include in re.findall(r'''<Compile\b[^>]*\bInclude\s*=\s*(["'])(.*?)\1''', text, re.S):
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*\.fs", include):
            raise PolicyViolation("Compile must name a simple approved root-level source")
    reference = project_reference if project_reference is not None else before[project]
    for tag in ("OutputType", "TargetFramework", "ImplicitUsings", "Nullable"):
        actual = re.findall(r"<" + tag + r">\s*([^<]*?)\s*</" + tag + r">", text)
        expected = re.findall(r"<" + tag + r">\s*([^<]*?)\s*</" + tag + r">", reference)
        if actual and actual != expected:
            raise PolicyViolation("project framework/build settings changed")
    try:
        tree = ET.fromstring(text)
    except ET.ParseError:
        return after  # project_development emits a repairable failure
    for node in tree.iter("Compile"):
        if set(node.attrib) != {"Include"} or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*\.fs", node.get("Include", "")):
            raise PolicyViolation("Compile must name a simple approved root-level source")
    if _project_shape(reference, strip_compile=language == "fsharp") != _project_shape(
        text, strip_compile=language == "fsharp"
    ):
        raise PolicyViolation("project framework/dependencies/build settings changed")
    return after


def feedback_packet(raw: str, cap: int) -> dict:
    """Keep multiline diagnostics intact; exact-block dedup, errors first.

    For the pinned plain-text compiler output, a line containing error/warning
    starts a block. Following context lines belong to it until the next header.
    Over-grouping is conservative: an oversized error block stops the fixture.
    """
    blocks = []
    current = []
    for line in raw.replace("\r\n", "\n").splitlines():
        if re.search(r"\b(?:error|warning)\b", line, re.I) and current:
            blocks.append("\n".join(current).strip("\n"))
            current = []
        current.append(line)
    if current:
        blocks.append("\n".join(current).strip("\n"))
    blocks = sorted(set(blocks) - {""}, key=lambda block: (not bool(ERROR_LINE.search(block)), block))
    marker = "[TRUNCATED: additional development output omitted]\n"
    if cap < len(marker.encode("utf-8")):
        raise ValueError("feedback cap too small")
    full = "".join(block + "\n" for block in blocks)
    available = cap if len(full.encode("utf-8")) <= cap else cap - len(marker.encode("utf-8"))
    selected = []
    used = 0
    overflow_errors = False
    for block in blocks:
        size = len((block + "\n").encode("utf-8"))
        if used + size > available:
            overflow_errors |= bool(ERROR_LINE.search(block))
            continue
        selected.append(block)
        used += size
    truncated = len(selected) != len(blocks)
    visible = "".join(block + "\n" for block in selected) + (marker if truncated else "")
    return {"version": "e3a-diagnostics-v1", "text": visible,
            "bytes": len(visible.encode("utf-8")), "sha256": hashlib.sha256(visible.encode("utf-8")).hexdigest(),
            "raw_bytes": len(raw.encode("utf-8")), "unique_blocks": len(blocks),
            "unique_lines": sum(len(b.splitlines()) for b in blocks),
            "omitted_blocks": len(blocks) - len(selected), "truncated": truncated,
            "essential_error_overflow": overflow_errors}


def normalize_usage(raw: dict | None) -> dict:
    """Proposed Responses mapping; optional fields stay null, subsets are not added."""
    raw = raw if isinstance(raw, dict) else {}
    details_in = raw.get("input_tokens_details") or {}
    details_out = raw.get("output_tokens_details") or {}
    values = {
        "input_tokens": raw.get("input_tokens"),
        "cached_input_tokens": details_in.get("cached_tokens") if isinstance(details_in, dict) else None,
        "cache_write_input_tokens": details_in.get("cache_write_tokens") if isinstance(details_in, dict) else None,
        "output_tokens": raw.get("output_tokens"),
        "reasoning_output_tokens": details_out.get("reasoning_tokens") if isinstance(details_out, dict) else None,
    }
    invalid = []
    for name, value in values.items():
        if value is not None and (type(value) is not int or value < 0):
            invalid.append(name)
            values[name] = None
    for total, subset in [("input_tokens", "cached_input_tokens"), ("input_tokens", "cache_write_input_tokens"),
                          ("output_tokens", "reasoning_output_tokens")]:
        if values[total] is not None and values[subset] is not None and values[subset] > values[total]:
            invalid.append(subset)
            values[subset] = None
    if all(values[k] is not None for k in ["input_tokens", "cached_input_tokens", "cache_write_input_tokens"]) and (
        values["cached_input_tokens"] + values["cache_write_input_tokens"] > values["input_tokens"]
    ):
        invalid.append("input_token_subsets")
    total = raw.get("total_tokens")
    if total is not None and (type(total) is not int or total < 0 or (
        values["input_tokens"] is not None and values["output_tokens"] is not None
        and total != values["input_tokens"] + values["output_tokens"]
    )):
        invalid.append("total_tokens")
    return {**values, "totals_available": values["input_tokens"] is not None and values["output_tokens"] is not None,
            "invalid_fields": invalid, "raw": copy.deepcopy(raw)}


def usage_sum(rounds: list[dict]) -> dict:
    # An absent field in ANY attempted round prevents claiming a complete total.
    return {key: (sum(row["usage"][key] for row in rounds)
                  if all(row["usage"][key] is not None for row in rounds) else None)
            for key in USAGE_FIELDS}


def run_trajectory(before: dict[str, str], language: str, spec: dict,
                   session: Callable, develop: Callable, *, task_id: str,
                   record: Callable = lambda event: None,
                   clock: Callable = time.monotonic, deadline: float | None = None) -> dict:
    """One shared prefix; no holdout or rubric input can affect continuation.

    Session and evaluator enforce their own operation deadlines and isolation.
    A durable recorder must be supplied by the batch runner before dispatch.
    """
    current = copy.deepcopy(before)
    previous_id = None
    packet = None
    rounds = []
    stop = "repair-budget"
    batch_stop = False
    deadline = deadline if deadline is not None else clock() + spec["budgets"]["trajectory_timeout_seconds"]
    project = "OrderFlow.fsproj" if language == "fsharp" else "OrderFlow.csproj"
    for index in range(1 + spec["controller"]["max_repair_rounds"]):
        if clock() >= deadline:
            stop = "trajectory-deadline"
            break
        round_started = clock()
        response = session(previous_id, copy.deepcopy(current), copy.deepcopy(packet), deadline)
        row = {"round": index, "previous_response_id": previous_id,
               "response_id": response.get("id"), "status": response.get("status"),
               "submission": response.get("text"), "usage": normalize_usage(response.get("usage")),
               "request_elapsed_seconds": response.get("elapsed_seconds"), "phase_elapsed_seconds": clock() - round_started,
               "development": None, "feedback": None, "applied_sha256": None, "applied_source": None}
        rounds.append(row)  # retain timeouts/ambiguous requests and partial usage
        record({"event": "submission-received", "row": copy.deepcopy(row), "response": response})
        if response.get("status") != "completed" or not response.get("id") or not isinstance(response.get("text"), str):
            stop, batch_stop = response.get("failure", "request-incomplete-or-ambiguous"), True
            break
        previous_id = response["id"]
        try:
            current = apply_submission(current, response["text"], language, spec, project_reference=before[project])
        except PolicyViolation as exc:
            row["development"] = {"passed": False, "build_passed": False, "category": "protocol-violation", "output": str(exc)}
            stop = "protocol-violation"
            batch_stop = bool(response.get("batch_stop") or row["usage"]["invalid_fields"] or
                              not row["usage"]["totals_available"])
            break
        except SubmissionError as exc:
            development = {"passed": False, "build_passed": False, "category": "patch-format", "output": str(exc)}
        else:
            row["applied_sha256"] = canonical_json_hash(current)
            row["applied_source"] = copy.deepcopy(current)
            development = project_development(current, language)
            if development["passed"]:
                development = structural_development(current, language, task_id)
            if development["passed"]:
                try:
                    development = develop(copy.deepcopy(current), index, deadline)
                except Exception as exc:
                    development = {"passed": None, "build_passed": None, "category": "evaluator-failure",
                                   "output": type(exc).__name__, "batch_stop": True}
        if not isinstance(development, dict) or not isinstance(development.get("output"), str) or (
            development.get("passed") is not None and type(development.get("passed")) is not bool
        ) or not isinstance(development.get("category"), str) or (
            development.get("passed") is None and not development.get("batch_stop")
        ):
            development = {"passed": None, "build_passed": None, "category": "controller-feedback-failure",
                           "output": "malformed evaluator result", "batch_stop": True}
        row["development"] = copy.deepcopy(development)
        row["phase_elapsed_seconds"] = clock() - round_started
        record({"event": "development-finished", "round": index, "development": development})
        if response.get("batch_stop"):
            stop, batch_stop = response.get("failure", "provider-failure"), True
            break
        if development.get("batch_stop"):
            stop, batch_stop = development["category"], True
            break
        usage = row["usage"]
        if usage["invalid_fields"] or not usage["totals_available"]:
            stop, batch_stop = "accounting-unavailable-or-invalid", True
            break
        if (usage["input_tokens"] > spec["budgets"]["request_input_tokens"] or
                usage["output_tokens"] > spec["budgets"]["request_output_tokens_including_reasoning"]):
            stop, batch_stop = "reported-request-budget-exceeded", True
            break
        if development["passed"]:
            stop = "development-passed"
            break
        if clock() >= deadline or development["category"] == "trajectory-deadline":
            stop = "trajectory-deadline"
            break
        if index == spec["controller"]["max_repair_rounds"]:
            break  # no next recipient; raw output is already retained
        # Every failing development-case line must start with ERROR. Raw compiler
        # output is retained separately; the envelope guarantees a failure reason.
        try:
            raw_feedback = f"ERROR {development['category']}\n" + development["output"]
            packet = feedback_packet(raw_feedback, spec["controller"]["feedback_bytes"])
        except (TypeError, ValueError, UnicodeError):
            stop, batch_stop = "controller-feedback-failure", True
            break
        row["feedback"] = packet
        if packet["essential_error_overflow"]:
            stop = "feedback-budget-exhausted"
            break
    return {"rounds": rounds, "stop": stop, "batch_stop": batch_stop, "last_applied_source": current,
            "first_submission_source": rounds[0]["applied_source"] if rounds else None,
            "terminal_submission_source": rounds[-1]["applied_source"] if rounds else None,
            "first_phase_usage": usage_sum(rounds[:1]), "repair_usage": usage_sum(rounds[1:]),
            "total_usage": usage_sum(rounds)}


def all_required(values: list[bool | None]) -> bool | None:
    """Known failure dominates unavailable evidence; unknown is never success."""
    if any(value is False for value in values):
        return False
    return True if all(value is True for value in values) else None


def score_submission(row: dict | None, holdout: dict | None, *, task_id: str,
                     language: str, review: dict | None = None, allow_fixture_review: bool = False) -> dict:
    """Post-trajectory endpoint. Review is explicit source-bound evidence, not AI judging."""
    source = row.get("applied_source") if row else None
    development = (row or {}).get("development") or {}
    fmt = source is not None if row and isinstance(row.get("submission"), str) else None
    build = (holdout or {}).get("build_passed", development.get("build_passed"))
    behavior = (holdout or {}).get("passed")
    obligations = True
    if task_id == "007-query-engine-refactor":
        file_order = structural_development(source, language, task_id)["passed"] if source else None
        rubric = [None, None, None]
        if review is not None:
            if (not source or review.get("source_sha256") != canonical_json_hash(source)
                    or not review.get("reviewer_id") or review.get("reviewer_type") not in {"human", "ai-session", "scripted-fixture"}):
                raise ValueError("architecture review must identify its source and reviewer")
            if review["reviewer_type"] == "scripted-fixture" and not allow_fixture_review:
                raise ValueError("scripted review is evidence only for model-free fixture reports")
            rubric = [review.get(key) for key in ["domain_model_in_engine", "live_dispatch_in_engine", "program_io_boundary"]]
            if any(v is not None and type(v) is not bool for v in rubric):
                raise ValueError("architecture judgements must be true, false, or null")
        obligations = all_required([file_order, *rubric])
    return {"format": fmt, "build": build, "holdout_behavior": behavior,
            "declared_obligations": obligations, "architecture_review": copy.deepcopy(review),
            "build_and_behavior": all_required([build, behavior]),
            "task_completion": all_required([fmt, build, behavior, obligations])}
