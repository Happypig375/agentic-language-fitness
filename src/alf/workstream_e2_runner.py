"""Single-path offline process runner for the Workstream E2 definition."""
from __future__ import annotations

from collections import Counter
import json
import os
import platform
import re
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any

from .benchmark_artifacts import check_workspace
from .config import REQUIRED_DOTNET_SDK, load_manifest
from .protocol import canonical_json_hash
from .workstream_e2 import (
    CHECK_KEYS,
    COMMAND_TIMEOUT_SECONDS,
    COMMAND_TEMPLATES,
    E2RunError,
    ENVIRONMENT_PROFILE,
    HEX_40_RE,
    HEX_64_RE,
    REPORT_SCHEMA,
    _assert_no_build_directories,
    _atomic_bytes,
    _atomic_json,
    _compile_obligations,
    _cumulative_checks,
    _get_encoding,
    _inside,
    _materialize,
    _read_json_object,
    _resolve,
    _sha,
    _snapshot,
    check_definition,
)
from .workstream_e2_report import (
    audit_report,
    distributions,
    failure_identity,
    inventory,
    inventory_summary,
    publish_report,
    validate_report,
    write_attempt,
    write_raw_inventory,
)


WARNING_RE = re.compile(rb"\bwarning(?:\s+([A-Za-z]+\d+))?\b", re.IGNORECASE)


def _cases(manifest: dict[str, Any], stage: int) -> list[dict[str, Any]]:
    return list(manifest["baseline_cases"]) + [
        case for task in manifest["tasks"][:stage] for case in task.get("cases", [])
    ]


def _case_payload(cases: list[dict[str, Any]]) -> bytes:
    return "".join(json.dumps(case["input"], separators=(",", ":")) + "\n" for case in cases).encode(
        "utf-8"
    )


def _network_snapshot() -> dict[str, Any]:
    net = Path("/sys/class/net")
    ipv4 = Path("/proc/net/route")
    ipv6 = Path("/proc/net/ipv6_route")
    if not net.is_dir() or not ipv4.is_file() or not ipv6.is_file():
        return {
            "ok": False,
            "interfaces": [],
            "ipv4_usable_default_routes": None,
            "ipv6_usable_default_routes": None,
            "reason": "linux network proof files unavailable",
        }
    interfaces = sorted(path.name for path in net.iterdir())
    ipv4_defaults = 0
    for line in ipv4.read_text(encoding="ascii", errors="replace").splitlines()[1:]:
        fields = line.split()
        if len(fields) >= 4 and fields[1] == "00000000":
            try:
                flags = int(fields[3], 16)
            except ValueError:
                continue
            if flags & 0x1 and not flags & 0x200:
                ipv4_defaults += 1
    ipv6_defaults = 0
    for line in ipv6.read_text(encoding="ascii", errors="replace").splitlines():
        fields = line.split()
        if len(fields) < 10 or fields[0] != "0" * 32 or fields[1] != "00":
            continue
        try:
            flags = int(fields[8], 16)
        except ValueError:
            continue
        if flags & 0x1 and not flags & 0x200:
            ipv6_defaults += 1
    ok = interfaces == ["lo"] and ipv4_defaults == 0 and ipv6_defaults == 0
    return {
        "ok": ok,
        "interfaces": interfaces,
        "ipv4_usable_default_routes": ipv4_defaults,
        "ipv6_usable_default_routes": ipv6_defaults,
        "reason": None if ok else "requires only loopback and no usable default route",
    }


def _host_load() -> dict[str, Any]:
    load: dict[str, Any] = {
        "cpu_count": os.cpu_count(),
        "load_1m": None,
        "load_5m": None,
        "load_15m": None,
        "memory_total_kib": None,
        "memory_available_kib": None,
    }
    try:
        values = Path("/proc/loadavg").read_text(encoding="ascii").split()[:3]
        load["load_1m"], load["load_5m"], load["load_15m"] = (float(value) for value in values)
    except (OSError, ValueError):
        pass
    try:
        for line in Path("/proc/meminfo").read_text(encoding="ascii").splitlines():
            key, _, value = line.partition(":")
            if key == "MemTotal":
                load["memory_total_kib"] = int(value.split()[0])
            elif key == "MemAvailable":
                load["memory_available_kib"] = int(value.split()[0])
    except (OSError, ValueError, IndexError):
        pass
    return load


def _warning_summary(stdout: bytes, stderr: bytes) -> dict[str, Any]:
    codes: Counter[str] = Counter()
    line_hashes: list[str] = []
    for line in (stdout + b"\n" + stderr).splitlines():
        match = WARNING_RE.search(line)
        if not match:
            continue
        code = match.group(1).decode("ascii", errors="ignore").upper() if match.group(1) else "UNSPECIFIED"
        codes[code] += 1
        line_hashes.append(_sha(line))
    return {
        "count": sum(codes.values()),
        "codes": dict(sorted(codes.items())),
        "line_sha256": sorted(line_hashes),
    }


def _invoke(
    argv: list[str],
    *,
    cwd: Path,
    input_bytes: bytes | None,
    env: dict[str, str],
    timeout: int,
) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        argv,
        cwd=cwd,
        input=input_bytes,
        capture_output=True,
        env=env,
        timeout=timeout,
        check=False,
    )


def _coerce_bytes(value: bytes | str | None) -> bytes:
    if value is None:
        return b""
    return value if isinstance(value, bytes) else value.encode("utf-8", errors="replace")


def _execute_command(
    operation: str,
    argv: list[str],
    *,
    cwd: Path,
    input_bytes: bytes | None,
    env: dict[str, str],
    raw: Path,
    raw_stem: str,
    timeout: int,
) -> tuple[dict[str, Any], bytes, bytes]:
    start = time.perf_counter()
    timed_out = False
    try:
        result = _invoke(argv, cwd=cwd, input_bytes=input_bytes, env=env, timeout=timeout)
        stdout = _coerce_bytes(result.stdout)
        stderr = _coerce_bytes(result.stderr)
        exit_code: int | None = result.returncode
    except subprocess.TimeoutExpired as exc:
        stdout = _coerce_bytes(exc.stdout)
        stderr = _coerce_bytes(exc.stderr)
        exit_code = None
        timed_out = True
    stdout_path = Path(f"{raw_stem}.stdout.bin")
    stderr_path = Path(f"{raw_stem}.stderr.bin")
    metadata_path = Path(f"{raw_stem}.json")
    _atomic_bytes(raw / stdout_path, stdout)
    _atomic_bytes(raw / stderr_path, stderr)
    record = {
        "operation": operation,
        "argv": argv,
        "timeout_seconds": timeout,
        "wall_seconds": time.perf_counter() - start,
        "timed_out": timed_out,
        "exit_code": exit_code,
        "stdout": {"path": stdout_path.as_posix(), "bytes": len(stdout), "sha256": _sha(stdout)},
        "stderr": {"path": stderr_path.as_posix(), "bytes": len(stderr), "sha256": _sha(stderr)},
        "warnings": _warning_summary(stdout, stderr),
    }
    _atomic_json(raw / metadata_path, record)
    record["metadata_path"] = metadata_path.as_posix()
    if timed_out:
        raise E2RunError(f"{operation}_timeout")
    if exit_code != 0:
        raise E2RunError(f"{operation}_failed")
    return record, stdout, stderr


def _evaluate_output(stdout: bytes, cases: list[dict[str, Any]], workspace: Path, checks: dict[str, Any]) -> dict[str, Any]:
    start = time.perf_counter()
    try:
        lines = [line for line in stdout.decode("utf-8").splitlines() if line.strip()]
    except UnicodeDecodeError as exc:
        raise E2RunError("evaluator_output_not_utf8") from exc
    if len(lines) != len(cases):
        raise E2RunError("evaluator_output_count_mismatch")
    for line, case in zip(lines, cases):
        try:
            actual = json.loads(line)
        except json.JSONDecodeError as exc:
            raise E2RunError("evaluator_output_invalid_json") from exc
        if actual != case["expected"]:
            raise E2RunError("evaluator_case_mismatch")
    try:
        workspace_result = check_workspace(workspace, checks)
    except (OSError, ValueError) as exc:
        raise E2RunError("workspace_check_error") from exc
    if not workspace_result["ok"]:
        raise E2RunError("workspace_check_failed")
    return {
        "ok": True,
        "case_count": len(cases),
        "passed_case_count": len(cases),
        "workspace_check_counts": {key: len(checks[key]) for key in CHECK_KEYS},
        "wall_seconds": time.perf_counter() - start,
    }


def _artifact_size(workspace: Path) -> dict[str, int]:
    release = workspace / "bin" / "Release"
    files = [path for path in release.rglob("*") if path.is_file()] if release.is_dir() else []
    return {"file_count": len(files), "bytes": sum(path.stat().st_size for path in files)}


def _expanded_commands(config: dict[str, Any]) -> dict[str, list[str]]:
    project = config["project_file"]
    return {
        operation: [project if value == "<project>" else value for value in template]
        for operation, template in COMMAND_TEMPLATES.items()
    }


def _run_regime(
    *,
    workspace: Path,
    config: dict[str, Any],
    cases: list[dict[str, Any]],
    checks: dict[str, list[Any]],
    fresh: bool,
    env: dict[str, str],
    raw: Path,
    raw_prefix: str,
    timeout: int,
) -> dict[str, Any]:
    commands = _expanded_commands(config)
    regime = "fresh-workspace" if fresh else "repeat-workspace"
    load_before = _host_load()
    started = time.perf_counter()
    operations: list[dict[str, Any]] = []
    names = ["restore", "build", "run"] if fresh else ["build", "run"]
    run_stdout = b""
    for operation in names:
        record, stdout, _ = _execute_command(
            operation,
            commands[operation],
            cwd=workspace,
            input_bytes=_case_payload(cases) if operation == "run" else None,
            env=env,
            raw=raw,
            raw_stem=f"{raw_prefix}/{operation}",
            timeout=timeout,
        )
        operations.append(record)
        if operation == "run":
            run_stdout = stdout
    evaluator = _evaluate_output(run_stdout, cases, workspace, checks)
    return {
        "regime": regime,
        "operations": operations,
        "evaluator": evaluator,
        "composite_wall_seconds": time.perf_counter() - started,
        "artifact": _artifact_size(workspace),
        "load_before": load_before,
        "load_after": _host_load(),
    }


def _process_environment(cache: Path, runtime_home: Path) -> dict[str, str]:
    return {
        "PATH": os.environ.get("PATH", ""),
        "HOME": str(runtime_home),
        "TMPDIR": str(runtime_home / "tmp"),
        "DOTNET_CLI_HOME": str(runtime_home / "dotnet-home"),
        "DOTNET_CLI_TELEMETRY_OPTOUT": "1",
        "DOTNET_NOLOGO": "1",
        "DOTNET_SKIP_FIRST_TIME_EXPERIENCE": "1",
        "DOTNET_MULTILEVEL_LOOKUP": "0",
        "NUGET_PACKAGES": str(cache),
        "NUGET_HTTP_CACHE_PATH": str(runtime_home / "nuget-http-cache"),
        "NUGET_XMLDOC_MODE": "skip",
        "TIKTOKEN_CACHE_DIR": "/opt/tiktoken-cache",
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
    }


def _static_preflight(
    root: Path,
    manifest: dict[str, Any],
    definition: dict[str, Any],
    encoding: Any,
    cache: Path,
    cache_before: dict[str, Any],
    raw: Path,
    attempt: dict[str, Any],
) -> None:
    records: list[dict[str, Any]] = []
    for number, state in enumerate(definition["states"], 1):
        language = state["language"]
        stage = state["stage"]
        attempt["current_position"] = state["state_id"]
        with tempfile.TemporaryDirectory(prefix="alf-e2-preflight-") as temporary:
            workspace = Path(temporary)
            _materialize(root, manifest, language, stage, workspace)
            observed, _ = _snapshot(workspace, encoding)
            checks = _cumulative_checks(manifest, language, stage)
            if (
                observed != {
                    key: state[key] for key in ("source_tree_sha256", "files", "metrics")
                }
                or _compile_obligations(workspace, manifest["languages"][language], language)
                != state["compile_obligations"]
                or not check_workspace(workspace, checks)["ok"]
                or len(_cases(manifest, stage)) != state["case_count"]
            ):
                raise E2RunError("preflight_state_validation_failed")
            _case_payload(_cases(manifest, stage))
            records.append(
                {
                    "state_id": state["state_id"],
                    "source_tree_sha256": state["source_tree_sha256"],
                    "case_count": state["case_count"],
                    "workspace_check_counts": state["workspace_checks"]["counts"],
                }
            )
        if inventory(cache) != cache_before:
            raise E2RunError("package_cache_changed")
        attempt["completed_preflight_states"] = number
    _atomic_json(raw / "preflight/states.json", {"mode": "static-only", "states": records})


def run_baseline(
    *,
    root: Path,
    definition: str | Path,
    manifest: str | Path,
    runner_git_sha: str,
    container_image_id: str,
    package_cache: str | Path,
    raw_output: str | Path,
    output_json: str | Path,
    output_markdown: str | Path,
) -> dict[str, Any]:
    root = root.resolve()
    raw = Path(raw_output).resolve()
    cache = Path(package_cache).resolve()
    json_path = Path(output_json).resolve()
    markdown_path = Path(output_markdown).resolve()
    if _inside(root, raw):
        raise ValueError("raw output must be outside the repository")
    if raw.exists() and (not raw.is_dir() or any(raw.iterdir())):
        raise ValueError("raw output must be absent or an empty directory")
    raw.mkdir(parents=True, exist_ok=True)
    attempt: dict[str, Any] = {
        "status": "running",
        "phase": "initialization",
        "completed_preflight_states": 0,
        "completed_samples": 0,
        "current_position": None,
        "failure": None,
    }
    try:
        runner_git_sha = runner_git_sha.casefold()
        image = container_image_id.removeprefix("sha256:").casefold()
        if not HEX_40_RE.fullmatch(runner_git_sha):
            raise E2RunError("runner_git_sha_invalid")
        if not HEX_64_RE.fullmatch(image):
            raise E2RunError("container_image_id_invalid")
        if not cache.is_dir() or _inside(root, cache):
            raise E2RunError("package_cache_must_preexist_outside_repository")
        if json_path == markdown_path or _inside(raw, json_path) or _inside(raw, markdown_path):
            raise E2RunError("publishable_outputs_must_be_distinct_and_outside_raw")
        if json_path.exists() or markdown_path.exists():
            raise E2RunError("publishable_output_already_exists")

        attempt["phase"] = "definition"
        checked = check_definition(root, definition, manifest)
        if not checked["ok"]:
            raise E2RunError("definition_validation_failed")
        definition_data = _read_json_object(_resolve(root, definition), label="E2 definition")
        attempt.update(
            {
                "definition_sha256": definition_data["definition_sha256"],
                "runner_git_sha": runner_git_sha,
                "container_image_id": f"sha256:{image}",
            }
        )

        attempt["phase"] = "network"
        network = _network_snapshot()
        if not network["ok"]:
            raise E2RunError("network_isolation_proof_failed")
        run_start_load = _host_load()
        cache_before = inventory(cache)
        manifest_data = load_manifest(root, _resolve(root, manifest))
        states = {(state["language"], state["stage"]): state for state in definition_data["states"]}
        encoding = _get_encoding()

        with tempfile.TemporaryDirectory(prefix="alf-e2-runtime-") as runtime_temporary:
            runtime_home = Path(runtime_temporary)
            for directory in (runtime_home / "tmp", runtime_home / "dotnet-home", runtime_home / "nuget-http-cache"):
                directory.mkdir(parents=True, exist_ok=True)
            env = _process_environment(cache, runtime_home)
            if shutil.which("dotnet", path=env["PATH"]) is None:
                raise E2RunError("dotnet_unavailable")
            attempt["phase"] = "sdk"
            _, sdk_stdout, _ = _execute_command(
                "sdk-version",
                ["dotnet", "--version"],
                cwd=root,
                input_bytes=None,
                env=env,
                raw=raw,
                raw_stem="environment/sdk-version",
                timeout=COMMAND_TIMEOUT_SECONDS,
            )
            try:
                sdk_version = sdk_stdout.decode("ascii").strip()
            except UnicodeDecodeError as exc:
                raise E2RunError("dotnet_sdk_version_invalid") from exc
            if sdk_version != REQUIRED_DOTNET_SDK:
                raise E2RunError("dotnet_sdk_version_mismatch")
            if inventory(cache) != cache_before:
                raise E2RunError("package_cache_changed")

            attempt["phase"] = "preflight"
            _static_preflight(root, manifest_data, definition_data, encoding, cache, cache_before, raw, attempt)

            samples: list[dict[str, Any]] = []
            attempt["phase"] = "measurement"
            for row in definition_data["schedule"]:
                position = row["position"]
                language = row["language"]
                stage = row["stage"]
                state = states[(language, stage)]
                attempt["current_position"] = position
                with tempfile.TemporaryDirectory(prefix="alf-e2-sample-") as temporary:
                    workspace = Path(temporary)
                    _materialize(root, manifest_data, language, stage, workspace)
                    observed, _ = _snapshot(workspace, encoding)
                    if observed["source_tree_sha256"] != state["source_tree_sha256"] or observed["metrics"] != state["metrics"]:
                        raise E2RunError("measured_state_identity_mismatch")
                    prefix = f"samples/{position:03d}-{language}-s{stage:02d}"
                    fresh = _run_regime(
                        workspace=workspace,
                        config=manifest_data["languages"][language],
                        cases=_cases(manifest_data, stage),
                        checks=_cumulative_checks(manifest_data, language, stage),
                        fresh=True,
                        env=env,
                        raw=raw,
                        raw_prefix=f"{prefix}/fresh",
                        timeout=definition_data["commands"]["timeout_seconds"],
                    )
                    repeat = _run_regime(
                        workspace=workspace,
                        config=manifest_data["languages"][language],
                        cases=_cases(manifest_data, stage),
                        checks=_cumulative_checks(manifest_data, language, stage),
                        fresh=False,
                        env=env,
                        raw=raw,
                        raw_prefix=f"{prefix}/repeat",
                        timeout=definition_data["commands"]["timeout_seconds"],
                    )
                    final_snapshot, _ = _snapshot(workspace, encoding)
                    if final_snapshot["source_tree_sha256"] != state["source_tree_sha256"]:
                        raise E2RunError("source_changed_during_measurement")
                if inventory(cache) != cache_before:
                    raise E2RunError("package_cache_changed")
                samples.append({**row, "state_id": state["state_id"], "fresh": fresh, "repeat": repeat})
                attempt["completed_samples"] = position
            cache_after = inventory(cache)
            if cache_after != cache_before:
                raise E2RunError("package_cache_changed")

        raw_inventory = write_raw_inventory(raw)
        report: dict[str, Any] = {
            "schema_version": REPORT_SCHEMA,
            "definition_sha256": definition_data["definition_sha256"],
            "schedule_sha256": definition_data["schedule_sha256"],
            "runner_git_sha": runner_git_sha,
            "container_image_id": f"sha256:{image}",
            "environment": {
                "profile": ENVIRONMENT_PROFILE,
                "dotnet_sdk": sdk_version,
                "operating_system": platform.system(),
                "kernel_release": platform.release(),
                "network": network,
                "run_start_load": run_start_load,
                "run_end_load": _host_load(),
                "process_environment_contract": sorted(
                    key for key in _process_environment(Path("<package-cache>"), Path("<runtime-home>")) if key != "PATH"
                ),
                "inherited_environment_values_recorded": False,
                "os_page_cache_controlled": False,
            },
            "package_cache": {
                "before": inventory_summary(cache_before),
                "after": inventory_summary(cache_after),
                "unchanged": cache_before == cache_after,
            },
            "raw_evidence": {
                "inventory_path": "raw-inventory.json",
                "inventory_sha256": raw_inventory["inventory_sha256"],
                "file_count": raw_inventory["file_count"],
                "total_bytes": raw_inventory["total_bytes"],
            },
            "preflight": {"state_count": 18, "all_passed": True, "mode": "static-only"},
            "states": definition_data["states"],
            "samples": samples,
            "distributions": distributions(samples),
            "missingness": {
                "internal_compiler_phase_timing": {
                    "value": None,
                    "reason": "not directly exposed; binary logging was deliberately not added",
                },
                "observed_compiler_inputs": {
                    "value": None,
                    "reason": "not directly exposed; static source/project obligations are reported",
                },
                "machine_cold_state": {
                    "value": None,
                    "reason": "OS page cache was neither cleared nor controlled",
                },
            },
        }
        report["report_sha256"] = canonical_json_hash(report)
        if not validate_report(report, definition_data)["ok"]:
            raise E2RunError("report_validation_failed")

        attempt.update(
            {
                "status": "success",
                "phase": "complete",
                "current_position": None,
                "failure": None,
                "raw_inventory_sha256": raw_inventory["inventory_sha256"],
                "report_sha256": report["report_sha256"],
            }
        )
        write_attempt(raw, attempt)
        publish_report(report, json_path, markdown_path)
        if not audit_report(report, definition_data, raw)["ok"]:
            raise E2RunError("report_raw_audit_failed")
        return report
    except BaseException as exc:
        json_path.unlink(missing_ok=True)
        markdown_path.unlink(missing_ok=True)
        failure = failure_identity(exc)
        try:
            raw_inventory = write_raw_inventory(raw)
            attempt.update(
                {
                    "status": "failure",
                    "failure": failure,
                    "raw_inventory_sha256": raw_inventory["inventory_sha256"],
                }
            )
            write_attempt(raw, attempt)
        except BaseException as persistence_error:
            raise E2RunError(f"{failure['code']}_and_terminal_attempt_persistence_failed") from persistence_error
        raise
