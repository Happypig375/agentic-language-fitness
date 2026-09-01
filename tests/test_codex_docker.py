import importlib.util
import json
import tempfile
import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import patch


SCRIPT = Path(__file__).parents[1] / "scripts" / "codex-docker.py"
PROFILE = Path(__file__).parents[1] / "infra" / "remote-runner" / "environment-profile.json"
SPEC = importlib.util.spec_from_file_location("codex_docker", SCRIPT)
assert SPEC and SPEC.loader
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


class CodexDockerTests(unittest.TestCase):
    def test_non_cp1252_output_does_not_block_usage_sidecar(self):
        class NarrowSink(StringIO):
            encoding = "cp1252"

            def write(self, value):
                value.encode(self.encoding)
                return super().write(value)

        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            stdout = json.dumps({"type": "turn.completed", "usage": {
                "input_tokens": 1, "cached_input_tokens": 0,
                "cache_write_input_tokens": 0, "output_tokens": 1,
                "reasoning_output_tokens": 0,
            }, "message": "你好 😀"}, ensure_ascii=False) + "\n"

            def run(command, **_kwargs):
                if command[0:3] == ["docker", "image", "inspect"]:
                    return type("Inspect", (), {"returncode": 0, "stdout": "sha256:test", "stderr": ""})()
                return type("Done", (), {"returncode": 0, "stdout": stdout, "stderr": "错误 😀\n"})()

            with (
                patch.object(module.subprocess, "run", side_effect=run),
                patch.object(module.sys, "stdout", NarrowSink()),
                patch.object(module.sys, "stderr", NarrowSink()),
            ):
                self.assertEqual(module.main(["--workspace", str(workspace), "--prompt", "task"]), 0)
            sidecar = json.loads((workspace / ".alf" / "usage.json").read_text(encoding="utf-8"))
            self.assertTrue(sidecar["usage_available"])
            self.assertTrue(sidecar["accounting_valid"])

    def test_reasoning_effort_is_pinned_in_wrapper_argv(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch.dict(
                module.os.environ,
                {"ALF_DOCKER_MEMORY": "9g", "ALF_DOCKER_CPUS": "9", "ALF_DOCKER_PIDS": "999"},
            ):
                command = module.build_docker_argv(
                    Path(directory),
                    "image",
                    model="gpt-test",
                    reasoning_effort="medium",
                    memory="2g",
                    cpus=2,
                    pids_limit=256,
                )
        self.assertIn("--ignore-user-config", command)
        self.assertIn(["--config", "model_reasoning_effort=medium"], [command[i:i + 2] for i in range(len(command) - 1)])
        self.assertEqual(command[command.index("--memory") + 1], "2g")
        self.assertEqual(command[command.index("--cpus") + 1], "2")
        self.assertEqual(command[command.index("--pids-limit") + 1], "256")

    def test_main_records_reasoning_image_and_image_id_in_sidecar(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            stdout = json.dumps(
                {
                    "type": "turn.completed",
                    "usage": {"input_tokens": 7, "output_tokens": 3},
                }
            )
            calls = []

            def run(command, **kwargs):
                calls.append((command, kwargs))
                if command[0:3] == ["docker", "image", "inspect"]:
                    return type(
                        "Inspect",
                        (),
                        {"returncode": 0, "stdout": "sha256:test\n", "stderr": ""},
                    )()
                return type(
                    "Done",
                    (),
                    {"returncode": 0, "stdout": stdout, "stderr": ""},
                )()

            with (
                patch.object(module.subprocess, "run", side_effect=run),
                patch.object(module.sys, "stdout", new_callable=StringIO),
            ):
                code = module.main(
                    [
                        "--workspace",
                        str(workspace),
                        "--prompt",
                        "task",
                        "--model",
                        "gpt-test",
                        "--reasoning-effort",
                        "medium",
                        "--image",
                        "test-image",
                    ]
                )
            sidecar = json.loads(
                (workspace / ".alf" / "usage.json").read_text(encoding="utf-8")
            )

        self.assertEqual(code, 0)
        self.assertEqual(sidecar["model"], "gpt-test")
        self.assertEqual(sidecar["reasoning_effort"], "medium")
        self.assertEqual(sidecar["image"], "test-image")
        self.assertEqual(sidecar["image_id"], "sha256:test")
        self.assertEqual(sidecar["docker_network"], "bridge")
        self.assertIsInstance(sidecar["proxy_configured"], bool)
        self.assertFalse(sidecar["timed_out"])
        self.assertEqual(
            sidecar["container_limits"], {"memory": "2g", "cpus": 2, "pids": 256}
        )
        self.assertEqual(calls[0][1]["encoding"], "utf-8")
        self.assertEqual(calls[0][1]["errors"], "replace")
        self.assertEqual(calls[1][1]["encoding"], "utf-8")
        self.assertEqual(calls[1][1]["errors"], "replace")

    def test_required_auth_preflight_failure_skips_candidate_call(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            calls = []

            def run(command, **_kwargs):
                calls.append(command)
                return type(
                    "Inspect",
                    (),
                    {"returncode": 0, "stdout": "sha256:test\n", "stderr": ""},
                )()

            with (
                patch.object(module, "resolve_auth_path", return_value=None),
                patch.object(module.subprocess, "run", side_effect=run),
                patch.object(module.sys, "stdout", new_callable=StringIO),
                patch.object(module.sys, "stderr", new_callable=StringIO),
            ):
                code = module.main(
                    [
                        "--workspace",
                        str(workspace),
                        "--prompt",
                        "task",
                        "--require-auth-preflight",
                    ]
                )
            sidecar = json.loads(
                (workspace / ".alf" / "usage.json").read_text(encoding="utf-8")
            )

        self.assertEqual(code, 78)
        self.assertFalse(sidecar["auth_ok"])
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0][0:3], ["docker", "image", "inspect"])

    def test_auth_preflight_uses_utf8_replacement_decoding(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            auth = workspace / "auth.json"
            auth.write_text("{}", encoding="utf-8")
            calls = []

            def run(command, **kwargs):
                calls.append((command, kwargs))
                if command[0:3] == ["docker", "image", "inspect"]:
                    return type("Inspect", (), {"returncode": 0, "stdout": "sha256:test", "stderr": ""})()
                if "login" in command:
                    return type("Auth", (), {"returncode": 0, "stdout": "", "stderr": ""})()
                return type("Done", (), {"returncode": 0, "stdout": "", "stderr": ""})()

            with (
                patch.object(module, "resolve_auth_path", return_value=auth),
                patch.object(module.subprocess, "run", side_effect=run),
                patch.object(module.sys, "stdout", new_callable=StringIO),
            ):
                self.assertEqual(module.main(["--workspace", str(workspace), "--prompt", "task", "--require-auth-preflight"]), 0)

        self.assertEqual(calls[1][1]["encoding"], "utf-8")
        self.assertEqual(calls[1][1]["errors"], "replace")

    def test_command_mounts_only_workspace_and_writable_auth_home(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / "workspace"
            workspace.mkdir()
            auth = Path(directory) / "auth-home"
            auth.mkdir()
            (auth / "auth.json").write_text("{}", encoding="utf-8")
            with patch.dict(module.os.environ, {}, clear=True):
                command = module.build_docker_argv(workspace, "test-image", auth, "gpt-test")
        self.assertEqual(command[0:2], ["docker", "run"])
        self.assertIn("-i", command)
        self.assertIn(f"type=bind,src={workspace.resolve()},dst=/workspace", command)
        self.assertIn(f"type=bind,src={auth.resolve()},dst={module.CONTAINER_CODEX_HOME}", command)
        self.assertNotIn("readonly", " ".join(command))
        self.assertIn(f"HOME={module.CONTAINER_CODEX_HOME}", command)
        self.assertIn(f"CODEX_HOME={module.CONTAINER_CODEX_HOME}", command)
        self.assertEqual(command[-1], "-")
        self.assertIn("--dangerously-bypass-approvals-and-sandbox", command)
        self.assertNotIn("--privileged", command)

    def test_remote_network_and_proxy_are_explicit_in_candidate_and_login(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / "workspace"
            auth = Path(directory) / "auth-home"
            workspace.mkdir()
            auth.mkdir()
            (auth / "auth.json").write_text("{}", encoding="utf-8")
            kwargs = {
                "docker_network": "alf-internal",
                "https_proxy": "http://172.17.0.1:43128",
                "http_proxy": "http://172.17.0.1:43128",
                "no_proxy": "127.0.0.1,localhost",
            }
            with patch.dict(module.os.environ, {}, clear=True):
                candidate = module.build_docker_argv(workspace, "image", auth, **kwargs)
                login = module.build_login_status_argv(auth, "image", **kwargs)
        for command in (candidate, login):
            self.assertEqual(command[command.index("--network") + 1], "alf-internal")
            self.assertIn("HTTPS_PROXY=http://172.17.0.1:43128", command)
            self.assertIn("HTTP_PROXY=http://172.17.0.1:43128", command)
            self.assertIn("NO_PROXY=127.0.0.1,localhost", command)
            self.assertNotIn("readonly", " ".join(command))

    def test_tracked_environment_profile_derives_and_records_exact_route(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            calls = []

            def run(command, **_kwargs):
                calls.append(command)
                if command[0:3] == ["docker", "image", "inspect"]:
                    return type("Inspect", (), {"returncode": 0, "stdout": "sha256:test", "stderr": ""})()
                return type("Done", (), {"returncode": 0, "stdout": "", "stderr": ""})()

            with (
                patch.dict(module.os.environ, {}, clear=True),
                patch.object(module.subprocess, "run", side_effect=run),
                patch.object(module.sys, "stdout", new_callable=StringIO),
            ):
                code = module.main([
                    "--workspace", str(workspace), "--prompt", "task",
                    "--environment-profile", str(PROFILE),
                ])
            sidecar = json.loads((workspace / ".alf" / "usage.json").read_text(encoding="utf-8"))

        self.assertEqual(code, 0)
        candidate = next(command for command in calls if command[0:2] == ["docker", "run"])
        self.assertEqual(candidate[candidate.index("--network") + 1], "alf-internal")
        self.assertIn("HTTPS_PROXY=http://172.30.0.1:43128", candidate)
        self.assertIn("HTTP_PROXY=http://172.30.0.1:43128", candidate)
        self.assertEqual(sidecar["environment_profile_id"], "remote-highmem-local-egress-r1")
        self.assertRegex(sidecar["route_profile_sha256"], r"^sha256:[0-9a-f]{64}$")

    def test_tracked_environment_profile_rejects_route_override(self):
        with tempfile.TemporaryDirectory() as directory, patch.dict(
            module.os.environ, {}, clear=True
        ):
            with self.assertRaisesRegex(ValueError, "proxy"):
                module.main([
                    "--workspace", directory, "--prompt", "task",
                    "--environment-profile", str(PROFILE),
                    "--https-proxy", "http://172.30.0.1:43129",
                ])

    def test_proxy_credentials_and_invalid_network_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            with patch.dict(module.os.environ, {}, clear=True):
                with self.assertRaisesRegex(ValueError, "unauthenticated"):
                    module.build_docker_argv(
                        workspace,
                        "image",
                        https_proxy="http://user:secret@127.0.0.1:8888",
                    )
                with self.assertRaisesRegex(ValueError, "network name"):
                    module.build_docker_argv(
                        workspace,
                        "image",
                        docker_network="--network=host",
                    )

    def test_usage_parser_writes_aggregate_sidecar(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            output = "\n".join([
                json.dumps({"type": "item.completed", "item": {"type": "command_execution"}}),
                json.dumps({"type": "turn.completed", "usage": {"input_tokens": 7, "output_tokens": 3}}),
            ])
            module.write_usage(workspace, output, "gpt-test")
            data = json.loads((workspace / ".alf" / "usage.json").read_text(encoding="utf-8"))
        self.assertEqual(data["input_tokens"], 7)
        self.assertEqual(data["output_tokens"], 3)
        self.assertEqual(data["tool_calls"], 1)
        self.assertEqual(data["command_count"], 1)
        self.assertEqual(data["usage_record_count"], 1)
        self.assertEqual(data["model"], "gpt-test")

    def test_image_identifier_handles_inspect_failure(self):
        with patch.object(module.subprocess, "run", side_effect=OSError("docker unavailable")):
            self.assertEqual(module.image_identifier("missing:tag"), "unavailable")

    def test_auth_resolution_does_not_require_printing_contents(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            auth = home / ".codex" / "auth.json"
            auth.parent.mkdir()
            auth.write_text('{"token":"secret"}', encoding="utf-8")
            resolved = module.resolve_auth_path(None, {"HOME": str(home)})
        self.assertEqual(resolved, auth.resolve())

    def test_auth_copy_retains_refresh_token_and_exact_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "auth.json"
            expected = b'{"access_token":"a","refresh_token":"SECRET","tokens":{"refresh_token":"S"}}\x00\xff'
            source.write_bytes(expected)
            projected = module.temporary_auth_copy(source)
            try:
                self.assertEqual((projected / "auth.json").read_bytes(), expected)
            finally:
                import shutil
                shutil.rmtree(projected, ignore_errors=True)
        self.assertFalse(projected.exists())

    def test_auth_copy_none_is_none(self):
        self.assertIsNone(module.temporary_auth_copy(None))

    def test_auth_cleanup_is_verified(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory) / "auth-home"
            home.mkdir()
            (home / "auth.json").write_text("secret", encoding="utf-8")
            module.remove_temporary_auth_home(home)
            self.assertFalse(home.exists())

        with patch.object(module.shutil, "rmtree", side_effect=OSError("denied")):
            with self.assertRaisesRegex(RuntimeError, "failed to remove"):
                module.remove_temporary_auth_home(Path("unremovable"))

    def test_auth_cleanup_failure_preserves_output_metadata_and_fails_run(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            auth_home = workspace / "auth-home"
            auth_home.mkdir()
            (auth_home / "auth.json").write_text("secret", encoding="utf-8")

            def run(command, **_kwargs):
                if command[0:3] == ["docker", "image", "inspect"]:
                    return type("Inspect", (), {"returncode": 0, "stdout": "sha256:test", "stderr": ""})()
                return type("Done", (), {"returncode": 0, "stdout": "", "stderr": ""})()

            with (
                patch.object(module, "temporary_auth_copy", return_value=auth_home),
                patch.object(module, "remove_temporary_auth_home", side_effect=RuntimeError("denied")),
                patch.object(module.subprocess, "run", side_effect=run),
                patch.object(module.sys, "stdout", new_callable=StringIO),
                patch.object(module.sys, "stderr", new_callable=StringIO),
            ):
                code = module.main(["--workspace", str(workspace), "--prompt", "task"])
            sidecar = json.loads((workspace / ".alf" / "usage.json").read_text(encoding="utf-8"))

        self.assertEqual(code, 79)
        self.assertTrue(sidecar["auth_cache_staged"])
        self.assertFalse(sidecar["auth_cleanup_ok"])
        self.assertFalse(sidecar["auth_ok"])

    def test_timeout_cleans_named_container_and_decodes_output(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            timeout = __import__("subprocess").TimeoutExpired(["docker"], 1, output=b"snowman \xe2\x98\x83\n", stderr=b"warn \xff\n")
            calls = []
            def run(*args, **kwargs):
                calls.append((args, kwargs))
                command = args[0]
                if command[0:3] == ["docker", "image", "inspect"]:
                    return type("Inspect", (), {"returncode": 0, "stdout": "sha256:test", "stderr": ""})()
                if command[0:2] == ["docker", "run"]:
                    raise timeout
                return type("Done", (), {"returncode": 0, "stdout": "", "stderr": ""})()
            with patch.object(module.subprocess, "run", side_effect=run), patch.object(module.sys, "stdout", new_callable=StringIO) as out:
                code = module.main(["--workspace", str(workspace), "--prompt", "task"])
            sidecar = json.loads(
                (workspace / ".alf" / "usage.json").read_text(encoding="utf-8")
            )
            self.assertEqual(code, 124)
            self.assertTrue(sidecar["timed_out"])
            self.assertIn("snowman", out.getvalue())
            cleanup = next(call for call in calls if call[0][0][0:3] == ["docker", "rm", "-f"])[0][0]
            self.assertEqual(cleanup[0:3], ["docker", "rm", "-f"])
            run_call = next(call for call in calls if call[0][0][0:2] == ["docker", "run"])
            self.assertEqual(cleanup[3], run_call[0][0][run_call[0][0].index("--name") + 1])


if __name__ == "__main__":
    unittest.main()
