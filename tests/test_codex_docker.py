import importlib.util
import json
import tempfile
import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import patch


SCRIPT = Path(__file__).parents[1] / "scripts" / "codex-docker.py"
SPEC = importlib.util.spec_from_file_location("codex_docker", SCRIPT)
assert SPEC and SPEC.loader
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


class CodexDockerTests(unittest.TestCase):
    def test_command_mounts_only_workspace_and_auth_read_only(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / "workspace"
            workspace.mkdir()
            auth = Path(directory) / "auth.json"
            auth.write_text("{}", encoding="utf-8")
            command = module.build_docker_argv(workspace, "test-image", auth, "gpt-test")
        self.assertEqual(command[0:2], ["docker", "run"])
        self.assertIn("-i", command)
        self.assertIn(f"type=bind,src={workspace.resolve()},dst=/workspace", command)
        self.assertIn(f"type=bind,src={auth.resolve()},dst=/home/codex/.codex/auth.json,readonly", command)
        self.assertEqual(command[-1], "-")
        self.assertIn("--dangerously-bypass-approvals-and-sandbox", command)
        self.assertNotIn("--privileged", command)

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

    def test_auth_projection_removes_refresh_token(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "auth.json"
            source.write_text('{"access_token":"a","refresh_token":"SECRET","tokens":{"refresh_token":"S"}}', encoding="utf-8")
            projected = module.minimized_auth(source)
            try:
                text = projected.read_text(encoding="utf-8")
            finally:
                projected.unlink(missing_ok=True)
        self.assertIn("access_token", text)
        self.assertIn("refresh_token", text)
        self.assertNotIn("SECRET", text)
        self.assertNotIn('"S"', text)

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
            self.assertEqual(code, 124)
            self.assertIn("snowman", out.getvalue())
            cleanup = next(call for call in calls if call[0][0][0:3] == ["docker", "rm", "-f"])[0][0]
            self.assertEqual(cleanup[0:3], ["docker", "rm", "-f"])
            run_call = next(call for call in calls if call[0][0][0:2] == ["docker", "run"])
            self.assertEqual(cleanup[3], run_call[0][0][run_call[0][0].index("--name") + 1])


if __name__ == "__main__":
    unittest.main()
