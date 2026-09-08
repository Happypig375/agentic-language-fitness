"""Finite, model-free Docker probes. No HTTP client, model key, or host fallback.

Default: the specified experimental image on the intended Linux Docker host.
--ci-sdk-fixture: explicitly non-experimental SDK-only image, never remote proof.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import platform
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from alf.config import load_manifest  # noqa: E402
from alf.e3a_sandbox import DockerEvaluator, SandboxFailure  # noqa: E402
from alf.protocol import canonical_json_hash  # noqa: E402
from alf.workstream_e2 import _atomic_json  # noqa: E402
from alf.workstream_e3a import PACKET_DIR, development_cases, read_json, snapshot  # noqa: E402

# Exactly the SDK base of Dockerfile.codex-agent; not the research image, which
# contains gold/scorers. This fixture override never changes the specification.
SDK_FIXTURE = "mcr.microsoft.com/dotnet/sdk:10.0.302@sha256:72dd743782f2ae7e5476fd64f6a460045e3998dc862218b80e6944cba79a01b0"


def model_free_spec(spec: dict) -> dict:
    """Return an isolated spec for non-experimental fixture probes."""
    fixture_spec = copy.deepcopy(spec)
    fixture_spec["execution_authorized"] = False
    return fixture_spec


def check(output: Path, *, ci_sdk_fixture=False) -> dict:
    spec = read_json(ROOT / PACKET_DIR / "specification.json")
    specification_sha256 = canonical_json_hash(spec)
    fixture_spec = model_free_spec(spec)
    manifest = load_manifest(ROOT, spec["manifest"])
    result = {"candidate_model_calls": 0, "count_http_calls": 0, "platform": sys.platform,
              "python_version": platform.python_version(), "host_platform": platform.platform(),
              "specification_sha256": specification_sha256,
              "model_free_specification_sha256": canonical_json_hash(fixture_spec),
              "fixture_execution_authorized": fixture_spec["execution_authorized"],
              "source_lf_sha256": {path: hashlib.sha256((ROOT / path).read_text(encoding="utf-8").encode("utf-8")).hexdigest()
                  for path in ("src/alf/e3a_sandbox.py", "src/alf/workstream_e3a.py", "scripts/e3a_sandbox_check.py")},
              "scope": "ci-sdk-fixture" if ci_sdk_fixture else "specified-image-on-current-linux-host",
              "intended_remote_environment_verified": False, "checks": {}, "evaluations": []}
    evaluators = []
    try:
        first = DockerEvaluator(ROOT, manifest, fixture_spec, "csharp")
        evaluators.append(first)
        image = None
        if ci_sdk_fixture:
            # Deliberately requires the caller to pull the exact image first.
            image = first._admin(["image", "inspect", SDK_FIXTURE, "--format", "{{.Id}}"])
            first.image, first.fixture_only = image, True
        for language in spec["languages"]:
            evaluator = first if language == "csharp" else DockerEvaluator(ROOT, manifest, fixture_spec, language, fixture_image_id=image)
            if evaluator is not first:
                evaluators.append(evaluator)
            result["evaluations"].append({"language": language, "preparation": evaluator.prepare()})
            source = snapshot(ROOT, manifest, language, 1)
            good = evaluator.evaluate(source, development_cases(manifest, 1), time.monotonic() + 120)
            if not good["passed"] or not good["binary_sha256"]:
                raise SandboxFailure("trusted sandbox positive build/execution failed: " + json.dumps(good))
            broken = {**source, "Program.cs" if language == "csharp" else "Program.fs": "this cannot compile\n"}
            bad = evaluator.evaluate(broken, development_cases(manifest, 1), time.monotonic() + 120)
            if bad["build_passed"] or bad["binary_sha256"] or any("program" in op for op in bad["operations"]):
                raise SandboxFailure("failed build executed or inherited a binary")
            result["evaluations"][-1].update(positive=good, failed_build=bad)
        result["checks"]["fresh_binary_and_failed_build_no_execution"] = True

        name = first._create([(first.base / "restore-input", "/input", False),
                              (first.seed, "/seed", False), (first.cache, "/packages", False)])
        try:
            inspected = json.loads(first._admin(["inspect", name]))[0]
            host = inspected["HostConfig"]
            if not (host["NetworkMode"] == "none" and host["ReadonlyRootfs"] and host["Memory"] == 6442450944
                    and host["MemorySwap"] == 6442450944 and host["PidsLimit"] == 512 and host["NanoCpus"] == 2000000000
                    and inspected["Config"]["User"] == "1000:1000" and "ALL" in host["CapDrop"]):
                raise SandboxFailure("effective container policy mismatch")
            binds = [mount for mount in inspected["Mounts"] if mount["Type"] == "bind"]
            if {m["Destination"] for m in binds} != {"/input", "/seed", "/packages"} or any(m["RW"] for m in binds):
                raise SandboxFailure("unexpected or writable host mount")
            result["checks"]["effective_policy"] = {k: host[k] for k in (
                "NetworkMode", "ReadonlyRootfs", "Memory", "MemorySwap", "PidsLimit", "NanoCpus", "CapDrop", "SecurityOpt")}
            checks = {
                "effective_privilege_bounds": "grep -Eq '^NoNewPrivs:[[:space:]]+1$' /proc/self/status && "
                    "grep -Eq '^CapEff:[[:space:]]+0+$' /proc/self/status",
                "writable_tmp_and_work": "touch /tmp/probe /work/probe",
                "readonly_source_seed_cache_root": "! touch /input/probe && ! touch /seed/probe && ! touch /packages/probe && ! touch /probe",
                "credentials_scorer_socket_absent": 'test -z "${OPENAI_API_KEY+x}${CODEX_HOME+x}${HTTPS_PROXY+x}" && '
                    'test ! -e /root/.codex/auth.json && test ! -e /home/codex/.codex/auth.json && '
                    'test ! -e /tmp/auth.json && test ! -e /var/run/docker.sock && '
                    'test ! -e /app/src/alf && test ! -e /workspace/src/alf && test ! -e /workspace/benchmarks && '
                    'test ! -e /workspace/AGENTS.md && test ! -e /input/AGENTS.md && test ! -e /input/holdout-cases.json',
                "network_route_blocked": "! /bin/bash -c 'exec 3<>/dev/tcp/1.1.1.1/443'",
            }
            for label, command in checks.items():
                probe = first._exec(name, ["/bin/sh", "-c", command], 5)
                if not first._ok(probe):
                    raise SandboxFailure("sandbox probe failed: " + label)
                result["checks"][label] = probe
            flood = first._exec(name, ["/bin/sh", "-c", "yes fixture-output"], 5)
            if not flood["output_limit_exceeded"]:
                raise SandboxFailure("output limit was not enforced")
            # Output beyond the retained prefix is explicitly unavailable.
            result["checks"]["output_limit"] = {k: v for k, v in flood.items() if k not in {"stdout", "stderr"}}
            child = first._exec(name, ["/bin/sh", "-c", "sleep 30 & wait"], 0.25)
            if not child["timed_out"]:
                raise SandboxFailure("subprocess timeout was not enforced")
            result["checks"]["timeout_with_descendant"] = child
        finally:
            first._remove(name)
        result["checks"]["descendant_container_removed"] = True

        # Bounded stress at a smaller fixture-only limit protects the CI host.
        # Effective experimental 6 GiB/512-pid settings were inspected above.
        small = copy.deepcopy(fixture_spec)
        small["environment"]["memory_bytes"] = 134217728
        probe = DockerEvaluator(ROOT, manifest, small, "csharp", fixture_image_id=first.image)
        evaluators.append(probe)
        name = probe._create([])
        try:
            stress = probe._exec(name, ["/bin/bash", "-c",
                "v=$(head -c 268435456 /dev/zero | tr '\\0' x); echo ${#v}"], 10)
            counters = probe._exec(name, ["/bin/sh", "-c", "cat /sys/fs/cgroup/memory.events"], 5)
            events = dict(line.split() for line in counters["stdout"].splitlines())
            if not probe._ok(counters) or int(events.get("oom_kill", "0")) < 1:
                raise SandboxFailure("fixture memory exhaustion was not observed in cgroup counters")
            result["checks"]["memory_bound_probe"] = {"fixture_limit_bytes": 134217728, "events": events, "process": stress}
        finally:
            probe._remove(name)
        result["passed"] = True
    except BaseException as exc:
        result.update(passed=False, failure_type=type(exc).__name__, failure=str(exc))
        raise
    finally:
        for evaluator in evaluators:
            try:
                evaluator.close()
            except Exception as exc:
                result.update(passed=False, cleanup_failure=type(exc).__name__)
        _atomic_json(output, result)
    if not result["passed"]:
        raise SandboxFailure("cleanup not confirmed")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--ci-sdk-fixture", action="store_true")
    arguments = parser.parse_args()
    result = check(arguments.output, ci_sdk_fixture=arguments.ci_sdk_fixture)
    print(json.dumps({"passed": result["passed"], "scope": result["scope"], "candidate_model_calls": 0}))
