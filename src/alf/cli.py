from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any

from .config import DEFAULT_MANIFEST, REQUIRED_DOTNET_SDK, find_repo_root, load_manifest
from .runner import environment_snapshot, run_chain, validate_benchmark
from .audit import audit_run
from .protocol import validate_cell, write_frozen_manifest
from .workstream_d import validate_family
from .variance import calibration_fixture, markdown_report, variance_report
from .representation import build_representation, check_representation
from .workstream_e import analyze_archive, write_report
from .workstream_e2 import check_definition, freeze_definition
from .workstream_e2_report import audit_report
from .workstream_e2_runner import run_baseline


def _root_and_manifest(args: argparse.Namespace) -> tuple[Path, dict[str, Any]]:
    root = Path(args.root).resolve() if getattr(args, "root", None) else find_repo_root()
    return root, load_manifest(root, args.manifest)


def cmd_doctor(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve() if args.root else find_repo_root()
    data = environment_snapshot(root, args.require_agent or "")
    checks = {
        "python_3_11_plus": sys.version_info >= (3, 11),
        "git_available": shutil.which("git") is not None,
        "dotnet_available": shutil.which("dotnet") is not None,
        "dotnet_sdk_required": data.get("dotnet") == REQUIRED_DOTNET_SDK,
    }
    if args.require_agent == "codex":
        checks["codex_available"] = shutil.which("codex") is not None
    data["checks"] = checks
    data["ok"] = all(checks.values())
    print(json.dumps(data, indent=2, sort_keys=True))
    return 0 if data["ok"] or not args.strict else 1


def cmd_validate(args: argparse.Namespace) -> int:
    root, manifest = _root_and_manifest(args)
    report = validate_benchmark(root, manifest, timeout=args.timeout)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["ok"] else 1


def cmd_run(args: argparse.Namespace) -> int:
    if args.require_usage and args.agent != "command":
        raise ValueError("--require-usage is valid only with --agent command")
    root, manifest = _root_and_manifest(args)
    output = Path(args.output)
    if not output.is_absolute():
        output = root / output
    run_dir = run_chain(
        root=root,
        manifest=manifest,
        language=args.language,
        agent_name=args.agent,
        output_root=output,
        model=args.model,
        agent_command=args.agent_command,
        require_usage=args.require_usage,
        timeout=args.timeout,
        max_tasks=args.max_tasks,
        protocol_manifest=Path(args.protocol_manifest).resolve() if args.protocol_manifest else None,
        block_id=args.block_id,
        order=args.order,
        attempt_id=args.attempt_id,
        position=args.position,
    )
    result = json.loads((run_dir / "result.json").read_text(encoding="utf-8"))
    print(json.dumps({"run_dir": str(run_dir), "success": result["success"]}, indent=2))
    return 0 if result["success"] else 1


def cmd_matrix(args: argparse.Namespace) -> int:
    if args.protocol_manifest or args.block_id or args.attempt_id or args.order or args.position:
        raise ValueError("protocol runs must be invoked with `alf run`; matrix does not accept protocol position arguments")
    if args.require_usage and args.agent != "command":
        raise ValueError("--require-usage is valid only with --agent command")
    root, manifest = _root_and_manifest(args)
    output = Path(args.output)
    if not output.is_absolute():
        output = root / output
    languages = args.languages.split(",") if args.languages else list(manifest["languages"])
    rows = []
    all_ok = True
    for language in languages:
        run_dir = run_chain(
            root=root,
            manifest=manifest,
            language=language.strip(),
            agent_name=args.agent,
            output_root=output,
            model=args.model,
            agent_command=args.agent_command,
            require_usage=args.require_usage,
            timeout=args.timeout,
            max_tasks=args.max_tasks,
            protocol_manifest=Path(args.protocol_manifest).resolve() if args.protocol_manifest else None,
            block_id=args.block_id,
            order=args.order,
            attempt_id=args.attempt_id,
            position=args.position,
        )
        result = json.loads((run_dir / "result.json").read_text(encoding="utf-8"))
        rows.append({"language": language.strip(), "run_dir": str(run_dir), "success": result["success"]})
        all_ok = all_ok and result["success"]
    print(json.dumps(rows, indent=2))
    return 0 if all_ok else 1


def _result_files(path: Path) -> list[Path]:
    if path.is_file() and path.name == "result.json":
        return [path]
    return sorted(path.rglob("result.json"))


def cmd_summarize(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve() if args.root else find_repo_root()
    path = Path(args.path)
    if not path.is_absolute():
        path = root / path
    rows = []
    for result_path in _result_files(path):
        data = json.loads(result_path.read_text(encoding="utf-8"))
        usage = data.get("aggregate_usage") if isinstance(data.get("aggregate_usage"), dict) else {}
        rows.append(
            {
                "run_id": data.get("run_id"),
                "language": data.get("language"),
                "agent": data.get("agent"),
                "model": data.get("requested_model"),
                "tasks_completed": len(data.get("tasks") or []),
                "success": bool(data.get("success")),
                "input_tokens": usage.get("input_tokens"),
                "cached_input_tokens": usage.get("cached_input_tokens"),
                "output_tokens": usage.get("output_tokens"),
                "reasoning_output_tokens": usage.get("reasoning_output_tokens"),
            }
        )
    if args.json:
        print(json.dumps(rows, indent=2, sort_keys=True))
    else:
        if not rows:
            print("No result.json files found", file=sys.stderr)
            return 1
        columns = ["language", "agent", "success", "tasks_completed", "input_tokens", "output_tokens", "reasoning_output_tokens"]
        widths = {col: max(len(col), *(len(str(row.get(col, ""))) for row in rows)) for col in columns}
        print("  ".join(col.ljust(widths[col]) for col in columns))
        print("  ".join("-" * widths[col] for col in columns))
        for row in rows:
            print("  ".join(str(row.get(col, "")).ljust(widths[col]) for col in columns))
    return 0

def cmd_audit(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve() if args.root else find_repo_root()
    path = Path(args.path)
    if not path.is_absolute():
        path = root / path
    report = audit_run(path)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["ok"] else 1

def cmd_protocol_validate(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve() if args.root else find_repo_root()
    report = validate_cell(root, args.definition)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["ok"] else 1

def cmd_protocol_family_validate(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve() if args.root else find_repo_root()
    report = validate_family(root, args.definition)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["ok"] else 1

def cmd_protocol_freeze(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve() if args.root else find_repo_root()
    path = write_frozen_manifest(root, args.definition, Path(args.output))
    print(json.dumps({"manifest": str(path), "manifest_sha256": json.loads(path.read_text())["manifest_sha256"]}, indent=2))
    return 0

def cmd_variance_report(args: argparse.Namespace) -> int:
    if args.bootstrap_samples <= 0 or args.power_simulations <= 0:
        raise ValueError("bootstrap and power simulation counts must be positive")
    report = variance_report(args.cell_root, bootstrap_samples=args.bootstrap_samples,
                             power_simulations=args.power_simulations, seed=args.seed)
    out_json, out_md = Path(args.output_json), Path(args.output_markdown)
    out_json.parent.mkdir(parents=True, exist_ok=True); out_md.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    out_md.write_text(markdown_report(report), encoding="utf-8")
    summary = {"output_json": str(out_json), "output_markdown": str(out_md),
               "report_sha256": report["report_sha256"]}
    if args.output_calibration:
        calibration = calibration_fixture(report)
        calibration_path = Path(args.output_calibration)
        calibration_path.parent.mkdir(parents=True, exist_ok=True)
        calibration_path.write_text(json.dumps(calibration, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        summary.update({"output_calibration": str(calibration_path),
                        "calibration_sha256": calibration["calibration_sha256"]})
    print(json.dumps(summary, sort_keys=True))
    return 0 if report["structural_validation"]["ok"] else 1

def cmd_representation(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve() if args.root else find_repo_root()
    output = Path(args.output) if args.output else None
    if output is not None and not output.is_absolute():
        output = root / output
    report = build_representation(root, output) if args.representation_command == "build" else check_representation(root, output)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0

def cmd_workstream_e(args: argparse.Namespace) -> int:
    report = analyze_archive(args.calibration_report, args.archive_root, args.analyzer_git_sha)
    write_report(report, args.output_json, args.output_markdown)
    print(json.dumps({"output_json": args.output_json,
                      "output_markdown": args.output_markdown,
                      "report_sha256": report["report_sha256"],
                      "runs": report["totals"]["run_count"],
                      "tasks": report["totals"]["task_count"]}, sort_keys=True))
    return 0

def cmd_e2_freeze(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve() if args.root else find_repo_root()
    output = Path(args.output)
    output = output if output.is_absolute() else root / output
    definition = freeze_definition(root, args.manifest, output)
    print(
        json.dumps(
            {
                "definition": str(output),
                "definition_sha256": definition["definition_sha256"],
                "states": len(definition["states"]),
                "schedule": len(definition["schedule"]),
            },
            sort_keys=True,
        )
    )
    return 0


def cmd_e2_check(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve() if args.root else find_repo_root()
    result = check_definition(root, args.definition, args.manifest)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["ok"] else 1


def cmd_e2_run(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve() if args.root else find_repo_root()
    report = run_baseline(
        root=root,
        definition=args.definition,
        manifest=args.manifest,
        runner_git_sha=args.runner_git_sha,
        container_image_id=args.container_image_id,
        package_cache=args.package_cache,
        raw_output=args.raw_output,
        output_json=args.output_json,
        output_markdown=args.output_markdown,
    )
    print(
        json.dumps(
            {
                "output_json": args.output_json,
                "output_markdown": args.output_markdown,
                "report_sha256": report["report_sha256"],
                "samples": len(report["samples"]),
            },
            sort_keys=True,
        )
    )
    return 0


def cmd_e2_audit(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve() if args.root else find_repo_root()
    definition_path = Path(args.definition)
    definition_path = definition_path if definition_path.is_absolute() else root / definition_path
    report_path = Path(args.report)
    report_path = report_path if report_path.is_absolute() else root / report_path
    definition = json.loads(definition_path.read_text(encoding="utf-8"))
    report = json.loads(report_path.read_text(encoding="utf-8"))
    result = audit_report(report, definition, Path(args.raw_output).resolve())
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["ok"] else 1


def _sha40(value: str) -> str:
    if re.fullmatch(r"[0-9a-fA-F]{40}", value) is None:
        raise argparse.ArgumentTypeError("must be exactly 40 hexadecimal characters")
    return value.lower()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="alf", description="Agentic Language Fitness benchmark harness")
    parser.add_argument("--root", help="Repository root; auto-detected by default")
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST), help="Manifest path relative to root")
    sub = parser.add_subparsers(dest="command", required=True)

    doctor = sub.add_parser("doctor", help="Check the local environment")
    doctor.add_argument("--strict", action="store_true", help="Exit non-zero when a required tool is missing")
    doctor.add_argument("--require-agent", choices=["codex"], help="Also require the named agent CLI")
    doctor.set_defaults(func=cmd_doctor)

    validate = sub.add_parser("validate", help="Build and evaluate all baseline/gold snapshots")
    validate.add_argument("--timeout", type=float, default=300)
    validate.set_defaults(func=cmd_validate)

    def add_run_arguments(p: argparse.ArgumentParser, include_language: bool) -> None:
        if include_language:
            p.add_argument("--language", required=True)
        p.add_argument("--agent", choices=["scripted", "codex", "command"], default="scripted")
        p.add_argument("--model")
        p.add_argument("--agent-command")
        p.add_argument("--require-usage", action="store_true", help="Require a fresh valid command-adapter usage sidecar")
        p.add_argument("--output", default="results")
        p.add_argument("--timeout", type=float, default=600)
        p.add_argument("--max-tasks", type=int)
        p.add_argument("--protocol-manifest", help="Resolved frozen protocol manifest for an auditable run")
        p.add_argument("--block-id")
        p.add_argument("--order")
        p.add_argument("--attempt-id")
        p.add_argument("--position", type=int)

    run = sub.add_parser("run", help="Run one language through the maintenance chain")
    add_run_arguments(run, True)
    run.set_defaults(func=cmd_run)

    matrix = sub.add_parser("matrix", help="Run multiple languages sequentially")
    add_run_arguments(matrix, False)
    matrix.add_argument("--languages", help="Comma-separated languages; defaults to all manifest languages")
    matrix.set_defaults(func=cmd_matrix)

    summarize = sub.add_parser("summarize", help="Summarize result.json files")
    summarize.add_argument("path")
    summarize.add_argument("--json", action="store_true")
    summarize.set_defaults(func=cmd_summarize)
    audit = sub.add_parser("audit", help="Reconcile a run's task and aggregate artifacts")
    audit.add_argument("path")
    audit.set_defaults(func=cmd_audit)
    protocol = sub.add_parser("protocol", help="Validate or freeze an experimental protocol cell")
    protocol_sub = protocol.add_subparsers(dest="protocol_command", required=True)
    pv = protocol_sub.add_parser("validate")
    pv.add_argument("--definition", required=True)
    pv.set_defaults(func=cmd_protocol_validate)
    pfam = protocol_sub.add_parser("family-validate")
    pfam.add_argument("--definition", required=True)
    pfam.set_defaults(func=cmd_protocol_family_validate)
    pf = protocol_sub.add_parser("freeze")
    pf.add_argument("--definition", required=True)
    pf.add_argument("--output", required=True)
    pf.set_defaults(func=cmd_protocol_freeze)
    vr = sub.add_parser("variance-report", help="Generate a deterministic post-hoc variance report")
    vr.add_argument("cell_root")
    vr.add_argument("--output-json", required=True)
    vr.add_argument("--output-markdown", required=True)
    vr.add_argument("--output-calibration", help="Optional redacted, self-hashed calibration fixture")
    vr.add_argument("--bootstrap-samples", type=int, default=2000)
    vr.add_argument("--power-simulations", type=int, default=2000)
    vr.add_argument("--seed", type=int, default=20260829)
    vr.set_defaults(func=cmd_variance_report)
    representation = sub.add_parser("representation", help="Build or check the C3 representation treatment")
    representation_sub = representation.add_subparsers(dest="representation_command", required=True)
    for name in ("build", "check"):
        rp = representation_sub.add_parser(name)
        rp.add_argument("--output", help="Treatment artifact directory (defaults to benchmarks/successor/representation-v1)")
        rp.set_defaults(func=cmd_representation)
    e1 = sub.add_parser("e1-report", aliases=["e1"], help="Analyze preserved v3 archives (archive-only, no model/network access)")
    e1.add_argument("--calibration-report", required=True)
    e1.add_argument("--archive-root", required=True)
    e1.add_argument("--analyzer-git-sha", required=True, type=_sha40)
    e1.add_argument("--output-json", required=True)
    e1.add_argument("--output-markdown", required=True)
    e1.set_defaults(func=cmd_workstream_e)
    e2 = sub.add_parser("e2", help="Run the offline model-free Workstream E2 baseline")
    e2sub = e2.add_subparsers(dest="e2_command", required=True)
    ef = e2sub.add_parser("freeze")
    ef.add_argument("--output", required=True)
    ef.set_defaults(func=cmd_e2_freeze)
    ec = e2sub.add_parser("check")
    ec.add_argument("--definition", required=True)
    ec.set_defaults(func=cmd_e2_check)
    er = e2sub.add_parser("run")
    er.add_argument("--definition", required=True)
    er.add_argument("--runner-git-sha", required=True, type=_sha40)
    er.add_argument("--container-image-id", required=True)
    er.add_argument("--package-cache", required=True)
    er.add_argument("--raw-output", required=True)
    er.add_argument("--output-json", required=True)
    er.add_argument("--output-markdown", required=True)
    er.set_defaults(func=cmd_e2_run)
    ea = e2sub.add_parser("audit")
    ea.add_argument("--definition", required=True)
    ea.add_argument("--report", required=True)
    ea.add_argument("--raw-output", required=True)
    ea.set_defaults(func=cmd_e2_audit)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except (FileNotFoundError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
        return 2
