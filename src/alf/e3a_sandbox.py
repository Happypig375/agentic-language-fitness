"""Disposable Docker evaluation on a Linux Docker host. Never a host fallback.

Only trusted dependency preparation gets a writable cache. Each candidate build
gets read-only inputs/seed/cache and fresh bounded tmpfs. Scoring stays outside.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import tempfile
import threading
import time
import uuid
from pathlib import Path

from .process import run_process
from .protocol import canonical_json_hash
from .workstream_e3a import apply_submission, project_development, snapshot


class SandboxFailure(RuntimeError):
    pass


def bounded_process(argv: list[str], *, input_text: str = "", timeout: float,
                    output_limit: int = 1_048_576) -> dict:
    """Capture a bounded prefix; timeout/output exhaustion kills the local client.

    The Docker owner MUST remove its container in finally, including descendants.
    This helper is not used to run candidate programs directly on the host.
    """
    if timeout <= 0 or output_limit <= 0:
        raise SandboxFailure("operation budget exhausted before launch")
    started = time.monotonic()
    process = subprocess.Popen(argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               env={k: os.environ[k] for k in ("PATH", "SystemRoot") if k in os.environ})
    chunks = [bytearray(), bytearray()]
    total = 0
    lock = threading.Lock()
    overflow = threading.Event()

    def read(pipe, number):
        nonlocal total
        try:
            while chunk := pipe.read1(4096):
                with lock:
                    take = min(len(chunk), max(0, output_limit - total))
                    chunks[number].extend(chunk[:take])
                    total += len(chunk)
                    if total > output_limit:
                        overflow.set()
                        return
        finally:
            pipe.close()

    def write():
        try:
            process.stdin.write(input_text.encode("utf-8"))
            process.stdin.close()
        except (BrokenPipeError, OSError):
            pass

    readers = [threading.Thread(target=read, args=(pipe, i), daemon=True)
               for i, pipe in enumerate([process.stdout, process.stderr])]
    writer = threading.Thread(target=write, daemon=True)
    for thread in [*readers, writer]:
        thread.start()
    timed_out = False
    try:
        while process.poll() is None:
            timed_out = time.monotonic() - started >= timeout
            if timed_out or overflow.wait(0.01):
                process.kill()
                break
        process.wait(timeout=5)
    finally:
        if process.poll() is None:
            process.kill()
            process.wait(timeout=5)
        for thread in [*readers, writer]:
            thread.join(timeout=1)
    return {"returncode": process.returncode, "stdout": chunks[0].decode("utf-8", errors="replace"),
            "stderr": chunks[1].decode("utf-8", errors="replace"), "observed_output_bytes": total,
            "output_limit_exceeded": overflow.is_set(), "timed_out": timed_out,
            "duration_seconds": time.monotonic() - started}


def tree_identity(root: Path) -> str:
    records = {}
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise SandboxFailure("symlink in prepared inputs/cache")
        if path.is_file():
            records[path.relative_to(root).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return canonical_json_hash(records)


def container_arguments(name: str, image: str, limits: dict, mounts: list[tuple[Path, str, bool]]) -> list[str]:
    if not re.fullmatch(r"sha256:[0-9a-f]{64}", image):
        raise SandboxFailure("image must be an exact local image ID")
    args = ["create", "--name", name, "--network", "none", "--read-only", "--user", "1000:1000",
            "--cap-drop", "ALL", "--security-opt", "no-new-privileges", "--pids-limit", str(limits["pids"]),
            "--memory", str(limits["memory_bytes"]), "--memory-swap", str(limits["memory_bytes"]),
            "--cpus", str(limits["cpus"]), "--ulimit", "core=0", "--workdir", "/work", "--entrypoint", "/bin/sleep",
            "--tmpfs", "/work:rw,nosuid,nodev,size=268435456,uid=1000,gid=1000,mode=0700",
            "--tmpfs", "/tmp:rw,nosuid,nodev,size=268435456,uid=1000,gid=1000,mode=0700"]
    for key, value in {"HOME": "/tmp", "DOTNET_CLI_HOME": "/tmp", "DOTNET_CLI_UI_LANGUAGE": "en-US",
                       "DOTNET_CLI_TELEMETRY_OPTOUT": "1", "DOTNET_NOLOGO": "1", "NUGET_PACKAGES": "/packages"}.items():
        args += ["--env", f"{key}={value}"]
    for source, target, writable in mounts:
        if "," in str(source) or not source.is_dir() or source.is_symlink():
            raise SandboxFailure("invalid private input mount")
        args += ["--mount", f"type=bind,src={source.resolve()},dst={target}" + ("" if writable else ",readonly")]
    return args + [image, "600"]


class DockerEvaluator:
    def __init__(self, root: Path, manifest: dict, spec: dict, language: str,
                 *, fixture_image_id: str | None = None):
        if os.name != "posix":
            raise SandboxFailure("candidate evaluation requires a Linux Docker host; no host fallback")
        if fixture_image_id and spec["execution_authorized"]:
            raise SandboxFailure("fixture image cannot replace the approved experimental image")
        self.spec, self.language = spec, language
        self.image = fixture_image_id or spec["environment"]["container_image_id"]
        self.fixture_only = fixture_image_id is not None
        self.docker = ["docker", "--host", "unix:///var/run/docker.sock"]
        self.baseline = snapshot(root, manifest, language, 0)
        self.project = "OrderFlow.fsproj" if language == "fsharp" else "OrderFlow.csproj"
        self._temporary = tempfile.TemporaryDirectory(prefix="alf-e3a-sandbox-")
        self.base = Path(self._temporary.name).resolve()
        self.cache, self.seed = self.base / "packages", self.base / "seed"
        self.cache.mkdir(mode=0o777)
        self.cache.chmod(0o777)  # fresh private parent is 0700; trusted preparer only
        self.seed.mkdir()
        self.seed.chmod(0o755)
        self.prepared_identity = None
        self.active: set[str] = set()
        self.evidence: list[dict] = []

    def _admin(self, args: list[str], *, required=True) -> str:
        result = run_process(self.docker + args, cwd=self.base, timeout=15)
        if required and not result.ok:
            raise SandboxFailure("Docker administration failed: " + " ".join(args[:2]))
        return result.stdout.strip() if result.ok else ""

    def _create(self, mounts: list[tuple[Path, str, bool]]) -> str:
        name = "alf-e3a-" + uuid.uuid4().hex
        self.active.add(name)  # covers ambiguous create/start as well
        self._admin(container_arguments(name, self.image, self.spec["environment"], mounts))
        self._admin(["start", name])
        return name

    def _remove(self, name: str) -> None:
        self._admin(["rm", "--force", name], required=False)
        # Inspect by the exact generated name; never kill another container.
        if self._admin(["ps", "--all", "--filter", f"name=^/{name}$", "--format", "{{.Names}}"]):
            raise SandboxFailure("container cleanup not confirmed")
        self.active.discard(name)

    def _exec(self, name: str, command: list[str], timeout: float, input_text="") -> dict:
        return bounded_process(self.docker + ["exec", "-i", name] + command, input_text=input_text, timeout=timeout,
                               output_limit=self.spec["budgets"]["controller_output_bytes"])

    @staticmethod
    def _ok(result: dict) -> bool:
        return result["returncode"] == 0 and not result["timed_out"] and not result["output_limit_exceeded"]

    def prepare(self) -> dict:
        """Trusted, offline SDK-library-pack restore at the same fixed /work path."""
        if self.prepared_identity is not None:
            raise SandboxFailure("dependency preparation is single-use")
        image = self._admin(["image", "inspect", self.image, "--format", "{{.Id}}"])
        if image != self.image:
            raise SandboxFailure("pinned image unavailable")
        inputs = self.base / "restore-input"
        inputs.mkdir()
        inputs.chmod(0o755)
        (inputs / self.project).write_text(self.baseline[self.project], encoding="utf-8", newline="\n")
        (inputs / self.project).chmod(0o644)
        name = self._create([(inputs, "/input", False), (self.cache, "/packages", True)])
        try:
            sdk = self._exec(name, ["dotnet", "--version"], 15)
            if not self._ok(sdk) or sdk["stdout"].strip() != self.spec["environment"]["sdk"]:
                raise SandboxFailure("SDK differs from specification")
            # The reviewed projects only need the SDK's bundled FSharp.Core.
            # No network, audit, candidate project, model credentials or source.
            script = (f"cp /input/{self.project} /work/{self.project}; exec dotnet restore {self.project} "
                      "--use-lock-file --nologo -p:NuGetAudit=false --source "
                      f"/usr/share/dotnet/sdk/{self.spec['environment']['sdk']}/FSharp/library-packs")
            restored = self._exec(name, ["/bin/sh", "-c", script], 60)
            if not self._ok(restored):
                raise SandboxFailure("offline dependency preparation failed: " + restored["stdout"] + restored["stderr"])
            # Cache is inside our private 0700 host directory. Make its trusted
            # preparer's files removable by the host owner; candidate mounts
            # remain read-only, regardless of these filesystem permissions.
            if not self._ok(self._exec(name, ["chmod", "-R", "a+rwX", "/packages"], 10)):
                raise SandboxFailure("trusted cache cleanup permissions failed")
            self._admin(["cp", f"{name}:/work/obj", str(self.seed / "obj")])
            self._admin(["cp", f"{name}:/work/packages.lock.json", str(self.seed / "packages.lock.json")])
            self.prepared_identity = (tree_identity(self.seed), tree_identity(self.cache))
            result = {"seed_sha256": self.prepared_identity[0], "cache_sha256": self.prepared_identity[1],
                      "image": self.image, "fixture_only": self.fixture_only, "restore": restored}
            self.evidence.append({"preparation": result})
            return result
        finally:
            self._remove(name)

    def evaluate(self, source: dict[str, str], cases: list[dict], deadline: float) -> dict:
        # Defense in depth for direct evaluator callers, not only the controller.
        serialized = json.dumps({"files": source})
        # A complete workspace can legitimately exceed ONE response's envelope
        # after several incremental replacements. Keep workspace/path/project
        # policy, but do not misapply the per-submission response-byte cap here.
        validation_spec = {**self.spec, "authority": {**self.spec["authority"],
            "max_submission_bytes": len(serialized.encode("utf-8"))}}
        validated = apply_submission(self.baseline, serialized, self.language, validation_spec,
                                     project_reference=self.baseline[self.project])
        if validated != source:
            raise SandboxFailure("evaluator input is not a complete submitted snapshot")
        project_result = project_development(source, self.language)
        if not project_result["passed"]:
            return project_result
        if self.prepared_identity is None or self.prepared_identity != (tree_identity(self.seed), tree_identity(self.cache)):
            raise SandboxFailure("prepared dependency inputs missing or changed")
        if time.monotonic() >= deadline:
            return {"passed": False, "build_passed": None, "category": "trajectory-deadline", "output": ""}
        inputs = Path(tempfile.mkdtemp(prefix="submission-", dir=self.base))
        inputs.chmod(0o755)
        for path, text in source.items():
            (inputs / path).write_text(text, encoding="utf-8", newline="\n")
            (inputs / path).chmod(0o644)
        source_hash = canonical_json_hash(source)
        name = self._create([(inputs, "/input", False), (self.seed, "/seed", False), (self.cache, "/packages", False)])
        result = {"passed": False, "build_passed": None, "category": "build", "output": "",
                  "submitted_sha256": source_hash, "binary_sha256": None, "operations": []}
        try:
            if time.monotonic() >= deadline:
                result.update(category="trajectory-deadline")
                return result
            copy_result = self._exec(name, ["/bin/sh", "-c", "cp -R /seed/. /work/ && cp /input/* /work/"],
                                     min(15, deadline - time.monotonic()))
            if not self._ok(copy_result):
                raise SandboxFailure("fresh evaluation workspace copy failed")
            # /work is a new tmpfs. The seed is restore metadata only: never bin
            # or configuration intermediates, and no path is reused across rounds.
            if (self.seed / "bin").exists() or (self.seed / "obj/Debug").exists():
                raise SandboxFailure("stale build output in trusted seed")
            command = [part.replace("{project}", self.project) for part in self.spec["environment"]["build"]]
            built = self._exec(name, command, min(self.spec["budgets"]["controller_build_timeout_seconds"], deadline - time.monotonic()))
            result["operations"].append({"build": built})
            result["output"] = built["stdout"] + built["stderr"]
            result["build_passed"] = self._ok(built)
            if not result["build_passed"]:
                return result
            paths = sorted(source) + ["bin/Debug/net10.0/OrderFlow.dll"]
            hashes = self._exec(name, ["sha256sum", *paths], min(10, deadline - time.monotonic()))
            if not self._ok(hashes):
                raise SandboxFailure("fresh binary/source identities unavailable")
            observed = dict((line.split(maxsplit=1)[1].strip(), line.split()[0]) for line in hashes["stdout"].splitlines())
            if any(observed.get(p) != hashlib.sha256(text.encode("utf-8")).hexdigest() for p, text in source.items()):
                raise SandboxFailure("compiled source differs from submitted source")
            result["binary_sha256"] = observed[paths[-1]]
            program = self._exec(name, self.spec["environment"]["execute"], min(
                self.spec["budgets"]["development_execution_timeout_seconds"], deadline - time.monotonic()),
                "".join(json.dumps(case["input"]) + "\n" for case in cases))
            result["operations"].append({"program": program})
            result["category"] = "development"
            errors = []
            if not self._ok(program):
                errors.append("ERROR program: execution/time/output limit failure")
            else:
                try:
                    actual = [json.loads(line) for line in program["stdout"].splitlines()]
                    if len(actual) != len(cases):
                        errors.append("ERROR program: wrong JSON response line count")
                    for case, value in zip(cases, actual):
                        if canonical_json_hash(value) != canonical_json_hash(case["expected"]):
                            errors.append(f"ERROR {case['name']}: expected {json.dumps(case['expected'])}; received {json.dumps(value)}")
                except ValueError:
                    errors.append("ERROR program: invalid JSON output")
            result["passed"] = not errors
            result["output"] += "\n" + "\n".join(errors)
            return result
        except SandboxFailure:
            if time.monotonic() < deadline:
                raise
            result.update(category="trajectory-deadline", passed=False)
            return result
        finally:
            self.evidence.append({"evaluation": result})
            self._remove(name)  # removes every candidate descendant on ALL exits

    def close(self) -> None:
        for name in list(self.active):
            self._remove(name)
        self._temporary.cleanup()  # only the owned mkdtemp root, never a caller path
