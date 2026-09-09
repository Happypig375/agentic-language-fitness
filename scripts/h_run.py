#!/usr/bin/env python3
"""Opt-in H runner; default repository state refuses before touching live inputs."""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from alf.environment_profile import environment_profile_sha256, load_environment_profile
from alf.h import HBoundaryError
from alf.h_run import (policy_sha, require_live_authority, run_integration, run_pilot,
                       verified_construction, verify_pilot_freeze)
from alf.protocol import canonical_json_hash
from alf.workstream_e2 import _atomic_json
from alf.h_sandbox import HSandboxEvaluator


def _read(path: Path): return json.loads(path.read_text(encoding="utf-8"))
def _sha(path: Path): return hashlib.sha256(path.read_bytes()).hexdigest()


def _transport_module():
    location = ROOT / "scripts/e3a_run.py"
    module_spec = importlib.util.spec_from_file_location("alf_existing_e3a_run", location)
    if not module_spec or not module_spec.loader:
        raise RuntimeError("existing E3a transport module is unavailable")
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", choices=("integration", "pilot"), required=True)
    parser.add_argument("--native-binary", type=Path, required=True)
    parser.add_argument("--native-sha256", required=True)
    parser.add_argument("--model-catalog", type=Path, required=True)
    parser.add_argument("--auth-file", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    spec = _read(ROOT / "protocols/workstream-h1-h2/specification.json")
    try: require_live_authority(spec, args.phase)
    except HBoundaryError as exc: parser.error(str(exc))
    # Everything below may inspect credentials, construct a transport, or create output.
    construction = verified_construction(ROOT, spec)
    if args.output.exists(): parser.error("refusing to overwrite output")
    status = subprocess.run(["git", "status", "--porcelain", "--untracked-files=all"], cwd=ROOT,
                            capture_output=True, text=True, check=True).stdout
    if status.strip(): parser.error("live H requires a clean reviewed commit")
    profile = load_environment_profile(ROOT / spec["environment"]["profile"], repository_root=ROOT)
    if (_sha(args.native_binary) != spec["model"]["native_sha256"]
            or args.native_sha256 != spec["model"]["native_sha256"]
            or _sha(args.model_catalog) != spec["model"]["catalog_sha256"]):
        parser.error("native binary/catalog identity mismatch")
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True,
                          text=True, check=True).stdout.strip()
    identity_paths = ("scripts/h_run.py", "scripts/e3a_run.py", "scripts/codex-docker.py",
        "src/alf/h.py", "src/alf/h_run.py", "src/alf/h_check.py",
        "src/alf/h_sandbox.py", "src/alf/h_workload.py", "src/alf/e3a_codex.py",
        "src/alf/e3a_runner.py", "src/alf/e3a_sandbox.py", "src/alf/workstream_e3a.py")
    identity_paths += ("src/alf/config.py", "src/alf/process.py", "src/alf/environment_profile.py",
                       "src/alf/protocol.py", "src/alf/workstream_e2.py")
    runtime = {"runner_git_commit": head,
        "source_sha256": {path: _sha(ROOT / path) for path in identity_paths},
        "native_sha256": _sha(args.native_binary), "catalog_sha256": _sha(args.model_catalog),
        "environment_profile_sha256": environment_profile_sha256(profile),
        "container_image_id": spec["environment"]["container_image_id"]}
    module = _transport_module()
    transport = module.DockerTransport(args, profile, spec)
    if (transport.wrapper.E3A_NATIVE_SHA256 != spec["model"]["native_sha256"]
            or transport.wrapper.E3A_MODEL_CATALOG_SHA256 != spec["model"]["catalog_sha256"]):
        parser.error("existing transport pins differ from H specification")
    if args.phase == "pilot":
        verify_pilot_freeze(ROOT, spec, runtime)
        report = run_pilot(ROOT, spec, construction, transport=transport,
            evaluator_factory=lambda _level, language, source: HSandboxEvaluator(source, language, spec),
            output=args.output, runtime=runtime)
    else:
        marker = {"OrderFlow.csproj": '<Project Sdk="Microsoft.NET.Sdk"><PropertyGroup><OutputType>Exe</OutputType><TargetFramework>net10.0</TargetFramework></PropertyGroup></Project>\n',
                  "Program.cs": 'using System;\nwhile (Console.ReadLine() is not null) Console.WriteLine("{\\"value\\":0}");\n'}
        report = {"phase": "integration", "scope": "unrelated-small-csharp-marker",
            "specification_sha256": canonical_json_hash(spec),
            "policy_sha256": policy_sha(spec), "runtime": runtime, "attempts": [],
            "batch_stop": None, "passed": False, "dispatches": 0, "subscription_cost_usd": None}
        evaluator = None
        try:
            evaluator = HSandboxEvaluator(marker, "csharp", spec)
            evaluator.prepare()
            report = run_integration(spec, transport=transport,
                evaluator=lambda source, deadline: evaluator.evaluate(source,
                    [{"name": "unrelated-marker", "input": {}, "expected": {"value": 1}}],
                    deadline),
                source=marker, order=["OrderFlow.csproj", "Program.cs"],
                submission_spec=spec, output=args.output, runtime=runtime)
        except Exception as exc:
            retained = args.output / "report.json"
            if retained.is_file():
                report = _read(retained)
            report.setdefault("attempts", []).append({"access": None, "stage": "pre-dispatch-apparatus",
                                                       "failure": type(exc).__name__})
            report.update(passed=False, batch_stop=f"integration-apparatus-{type(exc).__name__}")
            args.output.mkdir(parents=True, exist_ok=True)
            _atomic_json(args.output / "report.json", report)
        finally:
            if evaluator is not None:
                try:
                    evaluator.close()
                except Exception:
                    report.update(passed=False, batch_stop="cleanup-unconfirmed")
                    args.output.mkdir(parents=True, exist_ok=True)
                    _atomic_json(args.output / "report.json", report)
    print(json.dumps({"phase": args.phase, "passed": report["passed"],
                      "dispatches": report["dispatches"], "batch_stop": report["batch_stop"]}))
    return 0 if report["passed"] else 1


if __name__ == "__main__": raise SystemExit(main())
