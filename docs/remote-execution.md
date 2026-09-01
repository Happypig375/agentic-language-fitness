# Remote execution

The memory-heavy service runs on a remote host while model egress uses the
local machine. The supported topology is deliberately small:

```text
remote container -> Docker bridge gateway:<remote proxy port>
                 -> SSH reverse -R
                 -> local 127.0.0.1:<proxy port>
                 -> HTTP CONNECT proxy -> chatgpt.com:443
```

The local process is a forward HTTP CONNECT proxy, not an HTTP reverse proxy.
It listens only on loopback, permits only the documented provider destination,
and passes TLS through unchanged. The remote endpoint is the Docker bridge
gateway, so the container can reach it without public exposure.

One foreground `ssh.exe` owns the fixed `-R` forward and launches the remote
command. `-F none` disables ambient SSH configuration; `ExitOnForwardFailure`,
`BatchMode`, and keepalive options make setup fail closed. `run.ps1` requires
the proxy to publish an atomic ready file containing the launched process ID
before it checks the socket. The real container-level HTTPS/model shakedown is
a separate pre-freeze gate, not part of launcher readiness. Explicit identity
and known-hosts paths are optional inputs, but recommended.
Normal benchmark execution does not need `-L`, SOCKS, a custom relay, a port
broker, or a transport certificate/nonce protocol. `PermitRemoteOpen` is not a
control for a fixed-destination `-R`; use server-side `AllowTcpForwarding
remote`, `GatewayPorts clientspecified`, and `PermitListen` where available.

Create a dedicated internal Docker network once on the remote host. The tracked
`infra/remote-runner/environment-profile.json` is the authority for its name,
gateway, ports, destination allowlist, SSH mode, and authentication lifecycle.
The remote wrapper sets `ALF_ENVIRONMENT_PROFILE_PATH` to that tracked file;
`scripts/codex-docker.py` validates it and derives the following container
route before invoking Docker:

```text
ALF_DOCKER_NETWORK=alf-internal
HTTPS_PROXY=http://172.30.0.1:43128
HTTP_PROXY=http://172.30.0.1:43128
NO_PROXY=127.0.0.1,localhost
```

`scripts/codex-docker.py` passes those values into both the authentication
preflight and candidate container. The launcher accepts only a fixed command
with simple arguments, so put environment setup and the reviewed ALF command
in a remote wrapper such as `/opt/alf/run.sh` rather than composing a shell
program on the PowerShell command line:

```powershell
.\infra\remote-runner\run.ps1 `
  -RemoteHost user@host -RemoteSshPort 830 `
  -EnvironmentProfilePath .\infra\remote-runner\environment-profile.json `
  -RemoteCommand 'exec /opt/alf/run.sh'
```

A minimal server restriction is:

```text
Match User alf-runner
    AllowTcpForwarding remote
    GatewayPorts clientspecified
    PermitListen 172.30.0.1:43128
    AllowAgentForwarding no
    X11Forwarding no
```

The remote account should be restricted to the runner and the exact listener.
The complete Codex `auth.json` may be staged only in an ephemeral `0600` path
or tmpfs, treated as a password, and removed in cleanup. Never hash, commit, or
log its contents. Device authentication is preferable on a headless host.

Before a clean scientific freeze, run a tiny unrelated request through the exact
container route and verify HTTPS/streaming. This separate engineering shakedown
is not a study observation.
