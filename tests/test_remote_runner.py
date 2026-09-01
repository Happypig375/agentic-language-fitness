import ctypes
import importlib.util
import json
import os
import pathlib
import shutil
import socket
import subprocess
import sys
import threading
import tempfile
import time
import unittest


ROOT = pathlib.Path(__file__).parents[1]
SPEC = importlib.util.spec_from_file_location(
    "connect_proxy", ROOT / "infra" / "remote-runner" / "connect_proxy.py"
)
proxy = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(proxy)


def canonical_temporary_path(value):
    path = pathlib.Path(value)
    if os.name != "nt":
        return path
    buffer = ctypes.create_unicode_buffer(32768)
    length = ctypes.windll.kernel32.GetLongPathNameW(str(path), buffer, len(buffer))
    if length == 0 or length >= len(buffer):
        raise OSError(ctypes.get_last_error(), "could not expand temporary path")
    return pathlib.Path(buffer.value)


class ConnectProxyTests(unittest.TestCase):
    def test_allowlist_and_method(self):
        proxy.parse_connect(b"CONNECT chatgpt.com:443 HTTP/1.1\r\nHost: chatgpt.com\r\n\r\n")
        for request in (
            b"GET chatgpt.com:443 HTTP/1.1\r\n\r\n",
            b"CONNECT example.com:443 HTTP/1.1\r\n\r\n",
            b"CONNECT chatgpt.com:443 HTTP/1.1\r\nProxy-Authorization: x\r\n\r\n",
        ):
            with self.assertRaises(ValueError):
                proxy.parse_connect(request)

    def test_relay_forwards_bytes(self):
        left, peer = socket.socketpair()
        right, upstream_peer = socket.socketpair()
        try:
            worker = threading.Thread(target=proxy.relay, args=(left, right))
            worker.start()
            peer.sendall(b"request")
            self.assertEqual(upstream_peer.recv(7), b"request")
            upstream_peer.sendall(b"response")
            self.assertEqual(peer.recv(8), b"response")
            peer.shutdown(socket.SHUT_WR)
            worker.join(2)
            self.assertFalse(worker.is_alive())
        finally:
            for sock in (left, peer, right, upstream_peer):
                sock.close()

    def test_idle_timeout_exceeds_candidate_task_timeout(self):
        self.assertGreater(proxy.DEFAULT_IDLE_TIMEOUT, 600)

    def test_ready_file_proves_the_bound_listener_owner(self):
        with tempfile.TemporaryDirectory() as directory:
            ready = pathlib.Path(directory) / "proxy.ready"
            server = proxy.Proxy(0, ready_file=ready)
            worker = threading.Thread(target=server.run)
            worker.start()
            try:
                deadline = time.monotonic() + 2
                while not ready.exists() and time.monotonic() < deadline:
                    time.sleep(0.01)
                self.assertEqual(ready.read_text(encoding="ascii").strip(), str(os.getpid()))
                self.assertIsNotNone(server.listener)
            finally:
                server.stop.set()
                worker.join(2)
            self.assertFalse(worker.is_alive())

    def test_occupied_port_never_publishes_readiness(self):
        with tempfile.TemporaryDirectory() as directory, socket.socket() as occupied:
            occupied.bind(("127.0.0.1", 0))
            occupied.listen(1)
            ready = pathlib.Path(directory) / "proxy.ready"
            with self.assertRaises(OSError):
                proxy.Proxy(occupied.getsockname()[1], ready_file=ready).run()
            self.assertFalse(ready.exists())


class LauncherShapeTests(unittest.TestCase):
    def test_launcher_uses_existing_base_python_executable(self):
        text = (ROOT / "infra" / "remote-runner" / "run.ps1").read_text()
        self.assertIn("_base_executable", text)
        self.assertIn("$pythonProbe.Count -ne 1", text)
        self.assertIn("Test-Path -LiteralPath $pythonExecutable -PathType Leaf", text)
        self.assertIn("Start-Process -FilePath $pythonExecutable", text)
        self.assertNotIn("Start-Process -FilePath python ", text)

    def test_single_foreground_reverse_forward(self):
        text = (ROOT / "infra" / "remote-runner" / "run.ps1").read_text()
        self.assertEqual(text.count("-FilePath ssh.exe"), 1)
        self.assertEqual(text.count("'-R'"), 1)
        self.assertNotIn("ClearAllForwardings", text)
        self.assertNotIn("'-N'", text)
        self.assertNotIn("'-L'", text)
        self.assertIn("ExitOnForwardFailure=yes", text)
        self.assertIn("RemoteSshPort = 22", text)
        self.assertIn("'-p', $RemoteSshPort", text)
        self.assertIn("'-F','none'", text)
        self.assertIn("EnvironmentProfilePath", text)
        self.assertIn("BeginConnect('127.0.0.1', $LocalProxyPort", text)
        self.assertIn("proxy readiness owner does not match", text)
        self.assertIn("proxy did not become ready before timeout", text)
        self.assertIn("Join-NativeArguments", text)
        self.assertIn("-WindowStyle Hidden", text)
        self.assertIn("finally", text)

    def test_launcher_rejects_injection_sensitive_inputs(self):
        text = (ROOT / "infra" / "remote-runner" / "run.ps1").read_text()
        self.assertIn("RemoteHost -notmatch", text)
        self.assertIn("bridge_gateway must be IPv4", text)
        self.assertIn("RemoteCommand -notmatch", text)
        self.assertIn("RemoteSshPort out of range", text)


@unittest.skipUnless(os.name == "nt", "Windows PowerShell launcher integration test")
class LauncherWindowsIntegrationTests(unittest.TestCase):
    def _bundle(self, directory):
        runner = pathlib.Path(directory) / "runner"
        runner.mkdir()
        for name in ("run.ps1", "connect_proxy.py", "environment-profile.json"):
            shutil.copy2(ROOT / "infra" / "remote-runner" / name, runner / name)
        profile_path = runner / "environment-profile.json"
        profile = json.loads(profile_path.read_text(encoding="utf-8"))
        with socket.socket() as probe:
            probe.bind(("127.0.0.1", 0))
            profile["connect_proxy"]["local_port"] = probe.getsockname()[1]
        profile_path.write_text(json.dumps(profile), encoding="utf-8")
        return runner, profile["connect_proxy"]["local_port"]

    def _invoke(self, runner, environment):
        powershell = shutil.which("powershell.exe")
        if not powershell:
            self.skipTest("Windows PowerShell is unavailable")
        with socket.socket() as probe:
            probe.bind(("127.0.0.1", 0))
            ssh_port = probe.getsockname()[1]
        return subprocess.run(
            [
                powershell,
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                str(runner / "run.ps1"),
                "-RemoteHost",
                "127.0.0.1",
                "-RemoteCommand",
                "true",
                "-EnvironmentProfilePath",
                str(runner / "environment-profile.json"),
                "-RemoteSshPort",
                str(ssh_port),
                "-StartupTimeoutSeconds",
                "5",
            ],
            capture_output=True,
            text=True,
            timeout=45,
            env=environment,
        )

    def test_venv_redirector_uses_base_interpreter_pid_and_cleans_up(self):
        before = set(pathlib.Path(tempfile.gettempdir()).glob("alf-connect-proxy-*.ready*"))
        with tempfile.TemporaryDirectory() as directory:
            directory = canonical_temporary_path(directory)
            runner, local_port = self._bundle(directory)
            venv = pathlib.Path(directory) / "venv"
            subprocess.run(
                [sys.executable, "-m", "venv", str(venv)],
                check=True,
                capture_output=True,
                text=True,
                timeout=45,
            )
            scripts = venv / "Scripts"
            environment = os.environ.copy()
            environment["PATH"] = str(scripts) + os.pathsep + environment.get("PATH", "")
            result = self._invoke(runner, environment)
            output = result.stdout + result.stderr
            self.assertNotEqual(result.returncode, 0)
            self.assertRegex(output.lower(), r"\bssh\b")
            self.assertNotIn("proxy readiness owner does not match", output)
            with socket.socket() as client:
                client.settimeout(1)
                with self.assertRaises(OSError):
                    client.connect(("127.0.0.1", local_port))
        after = set(pathlib.Path(tempfile.gettempdir()).glob("alf-connect-proxy-*.ready*"))
        self.assertEqual(after - before, set())

    def test_python_probe_failure_starts_no_proxy_or_artifacts(self):
        before = set(pathlib.Path(tempfile.gettempdir()).glob("alf-connect-proxy-*.ready*"))
        with tempfile.TemporaryDirectory() as directory:
            directory = canonical_temporary_path(directory)
            runner, _ = self._bundle(directory)
            fake_bin = pathlib.Path(directory) / "fake-bin"
            fake_bin.mkdir()
            (fake_bin / "python.cmd").write_text("@exit /b 7\n", encoding="ascii")
            environment = os.environ.copy()
            environment["PATH"] = str(fake_bin) + os.pathsep + environment.get("PATH", "")
            result = self._invoke(runner, environment)
            output = result.stdout + result.stderr
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("could not resolve the base Python executable", output)
            self.assertNotIn("proxy readiness owner does not match", output)
        after = set(pathlib.Path(tempfile.gettempdir()).glob("alf-connect-proxy-*.ready*"))
        self.assertEqual(after - before, set())


if __name__ == "__main__":
    unittest.main()
