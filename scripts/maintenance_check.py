"""Audit trusted maintenance-simulation construction fixtures."""
from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from alf import maintenance  # noqa: E402


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--build-fixtures", action="store_true")
    parser.add_argument("--audit-failures", action="store_true")
    parser.add_argument("--output-dir", type=Path, default=Path("results/maintenance-sim-check"))
    args = parser.parse_args(argv)
    args.root = Path(__file__).resolve().parents[1]
    report = {"status": "passed", "trusted_source_only": True, "candidate_execution": False,
              "live": False, "allocations": {"integration": 0, "pilot": 0}, "actual_checks": []}
    try:
        report["layout"] = maintenance.validate_layout(args.root)
        base = args.root / "benchmarks" / "maintenance-sim"
        tracked = [base / "construction.json", base / "contract.md", base / "guidance" / "common.md"]
        tracked += [base / "guidance" / f"{x}.md" for x in maintenance.LANGUAGES]
        tracked += [base / "episodes" / f"{i:02d}.md" for i in range(1, 9)]
        tracked += [base / "fixtures" / "cases.json"]
        tracked += [args.root / "src" / "alf" / "maintenance.py",
                    args.root / "scripts" / "maintenance_check.py",
                    args.root / "tests" / "test_maintenance.py",
                    base / "fixtures" / "faults.json"]
        for language in maintenance.LANGUAGES:
            tracked += sorted((base / "seed" / language).glob("*"))
            tracked += [base / "reference" / language / f"{i:02d}.patch" for i in range(1, 9)]
        report["provenance"] = {"tokenizer": {"package": "tiktoken", "version": maintenance.TOKENIZER_VERSION,
                                                               "encoding": maintenance.TOKENIZER_ENCODING,
                                                               "note": "documented proxy, not provider context accounting"},
                                 "content_sha256": {p.relative_to(args.root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in tracked if p.is_file()},
                                 "reference_submission_bytes": maintenance.reference_submission_metrics(args.root)}
        report["actual_checks"].append("layout")
        cases = maintenance.load_cases(args.root)
        if set(c.get("introduced", 0) for c in cases) != set(range(9)):
            raise maintenance.MaintenanceFixtureError("complete audit requires cases introduced at every stage 0..8")
        report["case_count"] = len(cases)
        report["actual_checks"].append("cases")
        report["envelopes"] = []
        for language in maintenance.LANGUAGES:
            for checkpoint in range(9):
                source = maintenance.reconstruct(args.root, language, checkpoint)
                if checkpoint < 8:
                    artifact = maintenance.serialize_envelope(args.root, language, checkpoint, source, task_episode=checkpoint + 1)
                    path = args.output_dir / f"{language}-episode-{checkpoint + 1:02d}.json"
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(artifact["serialized"], encoding="utf-8", newline="\n")
                    artifact.pop("serialized", None)
                    artifact.pop("envelope", None)
                    report["envelopes"].append(artifact)
                else:
                    report.setdefault("reference_only", []).append({"language": language, "source_checkpoint": checkpoint})
        report["actual_checks"].append("reconstruction-and-envelope")
        if args.build_fixtures:
            # Trusted cases are intentionally the only executable inputs. This
            # is a fixture audit, never an externally supplied source runner.
            report["build"] = {"requested": True, "targets": []}
            for language in maintenance.LANGUAGES:
                for checkpoint in range(9):
                    selected = maintenance.applicable_cases(cases, checkpoint)
                    item = maintenance.build_checkpoint(args.root, language, checkpoint, selected)
                    report["build"]["targets"].append({"language": language, "checkpoint": checkpoint, **item})
            report["build"]["status"] = "passed" if all(x["passed"] for x in report["build"]["targets"]) else "failed"
            report["actual_checks"].append("trusted-build-runtime-semantic")
            if report["build"]["status"] != "passed": report["status"] = "failed"
        if args.audit_failures:
            report["fault_audit"] = maintenance.audit_faults(args.root, cases, require_complete=True)
            report["applicability"] = maintenance.audit_applicability(args.root, cases)
            report["actual_checks"].extend(["trusted-fault-audit", "trusted-applicability-audit"])
            if (report["fault_audit"]["status"] != "passed"
                    or report["applicability"]["status"] != "passed"):
                report["status"] = "failed"
    except (maintenance.MaintenanceFixtureError, ValueError, OSError, json.JSONDecodeError) as exc:
        report["status"] = "failed"
        report["failure"] = str(exc)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
