import importlib.util
import json
from pathlib import Path
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).parents[1] / "scripts" / "e3a_codex_check.py"
SPEC = importlib.util.spec_from_file_location("e3a_codex_check", SCRIPT)
assert SPEC and SPEC.loader
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


class E3aCodexCheckTests(unittest.TestCase):
    def test_argv_is_fixture_only_and_has_security_guards(self):
        argv = module.build_argv("fake-codex", Path("C:/tmp/work"), "http://127.0.0.1:321/v1")
        self.assertEqual(argv[0:3], ["fake-codex", "exec", "--json"])
        for flag in ("--ephemeral", "--ignore-user-config", "--ignore-rules", "--sandbox", "workspace-write", "--color", "never", "--model", module.MODEL):
            self.assertIn(flag, argv)
        joined = " ".join(argv)
        self.assertIn("model_provider=fixture", joined)
        self.assertIn("requires_openai_auth=false", joined)
        self.assertIn("request_max_retries=0", joined)
        self.assertIn("stream_max_retries=0", joined)
        self.assertNotIn("OPENAI_API_KEY", joined)

    def test_deterministic_sse_is_valid_and_bounded(self):
        raw = module.deterministic_sse()
        self.assertLess(len(raw), 4096)
        self.assertEqual(raw.count(b"data:"), 6)
        self.assertIn(b"response.completed", raw)
        self.assertIn(b"fixture capability probe.", raw)

    def test_environment_scrubs_credentials_and_proxy_overrides(self):
        with patch.dict(module.os.environ, {"OPENAI_API_KEY": "secret", "HTTPS_PROXY": "http://proxy", "PATH": "p"}, clear=True):
            env = module.clean_environment(Path("C:/temporary/codex"))
        self.assertNotIn("OPENAI_API_KEY", env)
        self.assertNotIn("HTTPS_PROXY", env)
        self.assertEqual(env["CODEX_HOME"], str(Path("C:/temporary/codex")))
        self.assertEqual(env["NO_PROXY"], "127.0.0.1,localhost")

    def test_summary_keeps_hashes_and_relevant_values_without_prompt_text(self):
        private = "private prompt prose\n## Tools\nnamespace functions\ntype ShellTool\nfunctions.exec_command\napply_patch"
        raw = json.dumps({"input": [{"role": "developer", "content": [{"type": "input_text", "text": private}]},
                                     {"role": "user", "content": "user secret"}],
                          "instructions": "large built-in text", "tools": [
            {"type": "function", "name": "shell"},
            {"type": "namespace", "name": "mcp", "tools": [{"type": "function", "name": "lookup"}]},
        ], "tool_choice": "auto", "parallel_tool_calls": False, "text": {"format": {"type": "text"}},
                          "include": ["reasoning.encrypted_content"], "store": False, "max_output_tokens": 20}).encode()
        result = module._summarize_body(raw)
        self.assertEqual(result["tools"], {"count": 2,
            "types": ["function", "namespace", "function"],
            "names": ["shell", "mcp", "lookup"]})
        self.assertEqual(result["max_output_tokens"], 20)
        self.assertNotIn("private prompt prose", json.dumps(result))
        self.assertNotIn("user secret", json.dumps(result))
        self.assertIn("input_sha256", result)
        self.assertIn("instructions_sha256", result)
        self.assertEqual(result["input_messages"], [
            {"role": "developer", "content_types": ["input_text"], "content_bytes": [len(private.encode())]},
            {"role": "user", "content_types": ["text"], "content_bytes": [len("user secret".encode())]},
        ])
        self.assertTrue(result["input_lexical_markers"]["namespace functions"])
        self.assertTrue(result["input_lexical_markers"]["functions."])
        self.assertFalse(result["input_lexical_markers"]["shell_command"])
        self.assertEqual(result["input_declaration_names"], ["ShellTool", "functions"])
        self.assertEqual(result["tool_choice"], "auto")
        self.assertFalse(result["parallel_tool_calls"])
        self.assertEqual(result["text"], {"format": {"type": "text"}})

    def test_configs_are_restricted_to_non_secret_enums(self):
        for config in ("features.example=secret", "model_reasoning_effort=secret", "wire_api=chat"):
            with self.subTest(config=config), self.assertRaises(ValueError):
                module.build_argv("codex", Path("/work"), "http://127.0.0.1/v1", [config])
        argv = module.build_argv("codex", Path("/work"), "http://127.0.0.1/v1",
                                 ["features.example=false", "model_reasoning_effort=low"])
        self.assertIn("features.example=false", argv)

    def test_probe_passed_requires_complete_fixture_evidence(self):
        request = {"path": "/v1/responses", "json": True, "model": module.MODEL,
                   "reasoning": {"effort": "high"}, "fields_present": {"input": True},
                   "authorization_header_present": False, "api_key_header_present": False}
        report = {"returncode": 0, "timed_out": False, "fixture_error": [],
                  "request_bodies": [request], "fixture_final_text": "fixture capability probe.",
                  "cli_turn_completed_usage": {"input_tokens": 11, "output_tokens": 4}}
        self.assertTrue(module.probe_passed(report))
        mutations = (
            ("request_bodies", []),
            ("request_bodies", [request, request]),
            ("fixture_final_text", None),
            ("cli_turn_completed_usage", {"input_tokens": 10, "output_tokens": 4}),
            ("fixture_error", ["unexpected_path_or_extra_request"]),
        )
        for key, value in mutations:
            with self.subTest(key=key, value=value):
                changed = dict(report); changed[key] = value
                self.assertFalse(module.probe_passed(changed))
        authorized = dict(request); authorized["authorization_header_present"] = True
        changed = dict(report); changed["request_bodies"] = [authorized]
        self.assertFalse(module.probe_passed(changed))

    def test_loopback_refusal_never_spawns_codex(self):
        with patch.object(module, "loopback_only", return_value=False), \
                patch.object(module.subprocess, "Popen") as popen:
            report = module.run_probe("fake-codex")
        popen.assert_not_called()
        self.assertEqual(report["safety_error"], "loopback-only Linux network required")
        self.assertFalse(report["probe_passed"])

    def test_linux_timeout_kills_process_group_and_retains_bounded_report(self):
        class Done:
            stdout = "codex 0.149.1"

        class Proc:
            pid = 321
            returncode = -9
            calls = 0

            def __init__(self, *_args, **kwargs):
                self.stdout_file = kwargs["stdout"]
                self.stderr_file = kwargs["stderr"]

            def communicate(self, *_args, **_kwargs):
                self.calls += 1
                if self.calls == 1:
                    raise module.subprocess.TimeoutExpired("fake-codex", 1)
                self.stderr_file.write(b"stopped")
                self.stderr_file.flush()
                return None, None

        with patch.object(module, "loopback_only", return_value=True), \
                patch.object(module.subprocess, "run", return_value=Done()), \
                patch.object(module.subprocess, "Popen", side_effect=Proc), \
                patch.object(module.sys, "platform", "linux"), \
                patch.object(module.signal, "SIGKILL", 9, create=True), \
                patch.object(module.os, "killpg", create=True) as killpg:
            report = module.run_probe("fake-codex", timeout=1)
        killpg.assert_called_once_with(321, 9)
        self.assertTrue(report["timed_out"])
        self.assertEqual(report["stderr_bytes"], 7)
        self.assertIsNone(report["returncode"])

    def test_spawn_error_has_safe_null_returncode(self):
        class Done:
            stdout = "codex 0.149.1"

        with patch.object(module, "loopback_only", return_value=True), \
                patch.object(module.subprocess, "run", return_value=Done()), \
                patch.object(module.subprocess, "Popen", side_effect=OSError("missing")):
            report = module.run_probe("fake-codex")
        self.assertIsNone(report["returncode"])

    def test_run_probe_failure_path_does_not_make_network_or_model_call(self):
        class Done:
            returncode = 2
            stdout = ""
            stderr = "failed"

        class Proc:
            returncode = 2
            def communicate(self, *_args, **_kwargs):
                return "", "failed"

        with patch.object(module, "loopback_only", return_value=True), patch.object(module.subprocess, "run", return_value=Done()), patch.object(module.subprocess, "Popen", return_value=Proc()):
            report = module.run_probe("fake-codex", timeout=1)
        self.assertTrue(report["fixture_only"])
        self.assertEqual(report["candidate_model_calls"], 0)
        self.assertFalse(report["oauth_integration_verified"])
        self.assertEqual(report["returncode"], 2)


if __name__ == "__main__":
    unittest.main()
