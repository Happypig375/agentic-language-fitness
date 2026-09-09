"""Model-free post-pilot packet preparation and descriptive analysis.

This module deliberately never executes candidate code, calls a model, or edits
the supplied report.  It is a small consumer of the frozen report format.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from alf.e3a_runner import summarize  # noqa: E402
from alf.protocol import canonical_json_hash  # noqa: E402
from alf.workstream_e3a import score_submission, usage_sum  # noqa: E402


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _endpoint_source(slot: dict, endpoint: str) -> dict | None:
    rounds = ((slot.get("trajectory") or {}).get("rounds") or [])
    if not rounds:
        return None
    row = rounds[0] if endpoint == "first" else rounds[-1]
    source = row.get("applied_source") if isinstance(row, dict) else None
    if not isinstance(source, dict):
        return None
    claimed = row.get("applied_sha256")
    actual = canonical_json_hash(source)
    if claimed != actual:
        raise ValueError(f"{slot.get('slot_id', '<slot>')} {endpoint}: applied source hash mismatch")
    return source


def prepare_review_packets(report: dict) -> tuple[list[dict], list[dict]]:
    """Return blinded unique packets and a separate endpoint-to-hash map."""
    packets: dict[tuple[str, str], dict] = {}
    mapping: list[dict] = []
    for slot in report.get("slots", []):
        if slot.get("task_id") != "007-query-engine-refactor":
            continue
        language = slot.get("language")
        for endpoint in ("first", "terminal"):
            source = _endpoint_source(slot, endpoint)
            if source is None:
                mapping.append({"slot_id": slot.get("slot_id"), "endpoint": endpoint, "source_sha256": None})
                continue
            digest = canonical_json_hash(source)
            packets.setdefault((language, digest), {"source": copy.deepcopy(source), "source_sha256": digest, "language": language})
            mapping.append({"slot_id": slot.get("slot_id"), "endpoint": endpoint, "source_sha256": digest})
    return list(packets.values()), mapping


def _validate_reviews(reviews: dict | None, packets: list[dict]) -> dict[str, dict]:
    if reviews is None:
        return {}
    if not isinstance(reviews, dict):
        raise ValueError("reviews must be a JSON object keyed by source hash")
    packet_by_hash = {p["source_sha256"]: p for p in packets}
    accepted: dict[str, dict] = {}
    for digest, review in reviews.items():
        if digest not in packet_by_hash:
            raise ValueError(f"irrelevant or duplicate review source: {digest}")
        if digest in accepted:
            raise ValueError(f"duplicate review source: {digest}")
        if not isinstance(review, dict):
            raise ValueError("review must be an object")
        if review.get("source_sha256") != digest:
            raise ValueError("review source does not match its map key")
        candidate = dict(review)
        # This performs all reviewer/type/judgement validation.  A synthetic
        # row is sufficient because no candidate evaluation occurs here.
        score_submission({"submission": "{}", "applied_source": packet_by_hash[digest]["source"]}, {},
                         task_id="007-query-engine-refactor", language=packet_by_hash[digest]["language"],
                         review=candidate)
        accepted[digest] = candidate
    return accepted


def analyze(report: dict, spec: dict, reviews: dict | None = None, *, report_file_sha256: str | None = None) -> dict:
    expected_spec = canonical_json_hash(spec)
    if report.get("specification_sha256") != expected_spec:
        raise ValueError("report specification_sha256 is missing or does not match supplied spec")
    packets, mapping = prepare_review_packets(report)
    accepted = _validate_reviews(reviews, packets)
    slots = copy.deepcopy(report.get("slots", []))
    for slot in slots:
        if slot.get("task_id") != "007-query-engine-refactor":
            continue
        for endpoint in ("first", "terminal"):
            source = _endpoint_source(slot, endpoint)
            digest = canonical_json_hash(source) if source is not None else None
            if digest not in accepted:
                continue
            rounds = (slot.get("trajectory") or {}).get("rounds") or []
            row = rounds[0] if endpoint == "first" else rounds[-1]
            raw_score = ((slot.get("scores") or {}).get(endpoint) or {})
            holdout = raw_score.get("holdout_evaluation")
            derived = score_submission(row, holdout, task_id=slot["task_id"], language=slot["language"], review=accepted[digest])
            slot.setdefault("derived_scores", {})[endpoint] = derived
    summary_slots = copy.deepcopy(slots)
    for slot in summary_slots:
        if slot.get("derived_scores"):
            slot["scores"] = copy.deepcopy(slot.get("scores") or {})
            slot["scores"].update(slot["derived_scores"])
    summary = summarize(summary_slots, spec)
    return {
        "report_canonical_sha256": canonical_json_hash(report),
        "report_file_sha256": report_file_sha256,
        "specification_sha256": expected_spec,
        "review_packets": packets,
        "endpoint_to_source_hash": mapping,
        "reviews_applied": sorted(accepted),
        "slots": slots,
        "summary": summary,
        "timing_note": "trajectory_with_scoring_seconds includes model, evaluation, and scoring time; phases are not summed when they overlap.",
        "interpretation_note": "Operational completion is distinct from candidate pass; these three selected tasks and four repetitions are descriptive, not population inference. Paired differences are F# minus C# in repetition order. No successful-only filtering or prior-pilot pooling was used.",
    }


def render_markdown(analysis: dict) -> str:
    summary = analysis["summary"]
    lines = ["# E3a pilot post-pilot analysis", "", f"Assigned slots: {summary.get('assigned', 0)}; started: {summary.get('started', 0)}.", "", analysis["timing_note"], "", analysis["interpretation_note"], "", "## Review coverage", "", f"Blinded unique Task 007 packets: {len(analysis['review_packets'])}; reviews applied: {len(analysis['reviews_applied'])}.", "", "## Endpoint outcomes", ""]
    by_language = {}
    vector_rows = []
    for slot in analysis["slots"]:
        lang = slot.get("language")
        by_language.setdefault(lang, {})
        raw_scores = slot.get("scores") or {}
        derived_scores = slot.get("derived_scores") or {}
        for endpoint in ("first", "terminal"):
            score = dict(raw_scores.get(endpoint) or {})
            score.update(derived_scores.get(endpoint) or {})
            rounds = (slot.get("trajectory") or {}).get("rounds") or []
            row = rounds[0] if endpoint == "first" and rounds else (rounds[-1] if rounds else {})
            development = (row.get("development") or {}).get("passed")
            vector = [score.get("format"), score.get("build"), development, score.get("holdout_behavior"), score.get("declared_obligations"), score.get("task_completion")]
            values = "/".join("?" if v is None else ("1" if v else "0") for v in vector)
            by_language[lang].setdefault(endpoint, []).append(values)
            vector_rows.append((slot.get("slot_id"), lang, endpoint, values))
    lines.extend(["", "Outcome counts (completion only; counts include every assigned slot; 1=true, 0=false, ?=unknown):", ""])
    for lang, endpoints in by_language.items():
        for endpoint in ("first", "terminal"):
            completions = [row[3].split("/")[-1] for row in vector_rows if row[1] == lang and row[2] == endpoint]
            counts = {value: completions.count(value) for value in ("1", "0", "?")}
            lines.append(f"- {lang} {endpoint}: {counts}")
    lines.extend(["", "## Per-slot endpoint vectors", "", "FORMAT/BUILD/DEVELOPMENT/HOLDOUT/OBLIGATIONS/COMPLETION; ? is unknown. Effective values use validated source-bound reviews over raw values; raw scores remain unchanged.", "", "| Slot ID | Endpoint | Raw completion | Effective vector |", "|---|---|---|---|"])
    for slot_id, lang, endpoint, vector in vector_rows:
        source_slot = next(s for s in analysis["slots"] if s.get("slot_id") == slot_id)
        raw_completion = ((source_slot.get("scores") or {}).get(endpoint) or {}).get("task_completion")
        raw_completion = "?" if raw_completion is None else str(bool(raw_completion)).lower()
        lines.append(f"| {slot_id} | {endpoint} | {raw_completion} | {vector} |")
    lines.extend(["", "## Usage and timing", "", "Usage retains nulls and reports coverage. First-phase + repair-phase = total where all components are observed; cache/read and reasoning fields are subsets and are never added again.", "", "| Language | Phase | Dispatches | Input | Output |", "|---|---|---:|---:|---:|"])
    for language in sorted({s.get("language") for s in analysis["slots"]}):
        per_language_rounds = [((s.get("trajectory") or {}).get("rounds") or []) for s in analysis["slots"] if s.get("language") == language]
        initial = [r for rounds in per_language_rounds for r in rounds[:1]]
        repair = [r for rounds in per_language_rounds for r in rounds[1:]]
        total = initial + repair
        for phase, selected in (("initial", initial), ("repair", repair), ("total", total)):
            totals = usage_sum(selected)
            lines.append(f"| {language} | {phase} | {len(selected)} | {totals.get('input_tokens')} | {totals.get('output_tokens')} |")
    lines.append("")
    for key in ("observed_usage", "incremental_repair_usage", "usage_coverage"):
        lines.append(f"- {key}: `{json.dumps(summary.get(key, {}), sort_keys=True)}`")
    lines.extend(["", "## Per-task paired summaries", ""])
    for task, metrics in summary.get("per_task", {}).items():
        lines.extend([f"### {task}", ""])
        for metric, values in metrics.items():
            lines.append(f"- {metric}: differences={values['paired_differences']}; coverage={values['coverage']}; mean={values['complete_mean']}; min={values['observed_min']}; max={values['observed_max']}")
        lines.append("")
    lines.append("## Equal-task means")
    lines.append("")
    lines.append(f"`{json.dumps(summary.get('equal_task_complete_means', {}), sort_keys=True)}`")
    lines.extend(["", "## Slot status", ""])
    for slot in analysis["slots"]:
        lines.append(f"- {slot.get('slot_id')}: {slot.get('status')} ({slot.get('reason')}); first/terminal scores retained separately")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--spec", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--reviews", type=Path)
    args = parser.parse_args(argv)
    raw_report = args.report.read_bytes()
    report = json.loads(raw_report.decode("utf-8"))
    spec = json.loads(args.spec.read_text(encoding="utf-8"))
    reviews = json.loads(args.reviews.read_text(encoding="utf-8"), object_pairs_hook=_reject_duplicate_keys) if args.reviews else None
    result = analyze(report, spec, reviews, report_file_sha256=hashlib.sha256(raw_report).hexdigest())
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "review-packets.json").write_text(json.dumps(result["review_packets"], indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    (args.output_dir / "endpoint-to-source-hash.json").write_text(json.dumps(result["endpoint_to_source_hash"], indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    (args.output_dir / "analysis.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    (args.output_dir / "analysis.md").write_text(render_markdown(result), encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
