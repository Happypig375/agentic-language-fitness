# Opt-in native Codex no-tools client (design/build record)

**Resumed native verification passed (2026-09-08):** the original no-tools patch
plus [`single-response.patch`](single-response.patch) now passes 107 focused
native tests, build, two loopback probes, and the original-image native-mount /
pinned-catalogue packaging check. The implementing binary is `72cf14453…`, not
the original `f7942933…` below. See the [resumed evidence and reproduction commands](../../docs/workstream-e3a-oauth-resumed-verification-2026-09-08.md).
The [five-failure stop](../../docs/workstream-e3a-oauth-implementation-stop-2026-09-08.md)
remains identifiable history. No OAuth/provider shakedown is claimed.

**Status: adopted on 2026-09-08; bounded model-free implementation and packaging checks passed, exact-commit CI and live prerequisites remain.** This is an opt-in modification of the pinned Codex source, not stock `0.149.1`. The patch leaves the existing OAuth, refresh, endpoints, proxy and canonical remote launcher unchanged. The user's permission covers the bounded OAuth shakedown and subsequent pilot sequence in the [adoption record](../../docs/workstream-e3a-oauth-adoption-2026-09-08.md), but no call is made until required checks pass. No API key, relay, image replacement, or toolful fallback is authorized.

## Control

`features.no_tools=true` is opt-in and defaults to `false`. Enabled requests remove normal tools, lite `additional_tools`, and inherited `AdditionalTools`; they set `tool_choice` to `none` and `parallel_tool_calls` to `false`. A shared HTTP/WebSocket guard runs before dispatch and follow-up. Tool output/delta, `Other`, malformed output, and tool-specific ignored events are fatal under the policy. `UnparseableOutputItem` and `ToolCallInputEvent` are distinct internal markers; the default mapper drops only the new markers, preserving default behavior. The internal error is unprefixed; the CLI serializes exactly:

`Fatal error: no-tools policy rejected an unsolicited tool response item`

## Original no-tools-only source/build record (historical)

Source is tag `rust-v0.149.1` (tag `980a6d12110b110d29ec13bdcbe14011100b3566`), peeled commit `ff29a44391deccde0aba0f8390337d7f3c319ea4`. This does not prove stock-binary reproduction. The builder is `rust:1.95.0-bookworm`, digest `sha256:6258907abe69656e41cd992e0b705cdcfabcbbe3db374f92ed2d47121282d4a1`; local format-builder image ID `e1b5606d6b1d9f1401ddb5dbc6005559842249bf4443374348e3849f4845466c` is not a published registry digest. Review uses the existing `just 1.51.0`, `nextest 0.9.143`, `dotslash 0.5.7`, and `uv 0.12.10`; the dev-small GNU review binary is not a packaged client.

The verified upstream V8 archive/bindings are supplied through `RUSTY_V8_ARCHIVE` and `RUSTY_V8_SRC_BINDING_PATH`, following `.github/actions/setup-rusty-v8/action.yml` and release `rusty-v8-v150.4.0`.

Authoritative input is a fresh Linux LF checkout, not a CRLF archive. `cargo update --offline --workspace` was run in an isolated copy; `--locked` is used thereafter. Only the 139 workspace version labels were normalized from `0.0.0` to `0.149.1`; external records are unchanged. Lock SHA-256: `46febaad4d299009603ea1fc4da19545d5b28eb562b2e654bec75024e5ca0b67`.

The final exported patch is [`no-tools.patch`](no-tools.patch), SHA-256 `df6a1797f51f40a784544fe499e94c8706231f52cb867ae2d1d820954638a267` (11 files, 514 insertions, 14 deletions). Reverse-apply `--check` passes against the patched checkout. Reproduction starts from tag `rust-v0.149.1`, applies this patch, runs `cargo update --offline --workspace` only in an isolated copy for the documented 139 workspace-version labels, then uses `--locked`. The focused selector from the upstream root is:

```text
just test --cargo-profile dev-small -p codex-api -p codex-core -p codex-features --test-threads 3 -E 'test(client::tests::) | test(sse::responses::tests::) | test(no_tools_feature_fails_closed_in_session_without_followup) | package(codex-features)'
```

Final verification passed: native tests `100/100`, zero failures/retries, 3,715 not selected, four Session fixture cases; Python checker `23/23`; `e3a_check` matched with `candidate_model_calls=0`; scoped clippy (`core`, `api`, `features`, `otel`), `just fmt`, config-schema regeneration, and `cargo build --locked --profile dev-small -p codex-cli` passed. Final binary SHA-256 is `f7942933b353186ea7cb216c47cddc321c5c4d120fde5a8df9e75122e2fc8816`; helper remains `cbd85c192f4ecbf092a6f8b8b16a5b764d05c86c08cf2e8e5af8be439d174e06`. See the linked [native verification summary](../../reports/workstream-e3a-codex-capability-2026-09-06/native-verification.json). No exact-commit CI status is claimed here.

Both exact-final-binary probes passed their expected outcomes: baseline `native-resumed-baseline.json` (`rc=0`, SHA-256 `6b43a377534c995e63fcd67c94dfe4dc4b27bc2c3a22f6e2c948d2a91e5a0dff`) and hostile `native-resumed-tool-call.json` (`rc=1`, expected fatal, SHA-256 `f8fbd444ad9674902a662049840e77393a3679bc5db435a923bb32a08e83a327`). Each made one loopback POST with no tool output/marker/follow-up and no auth/model/provider call. Direct PowerShell SSH/Docker used the pinned image, network-none, read-only root, 256 MiB tmpfs, UID 1000, 2 CPUs, 6 GiB, and 512 PIDs. The single-binary overlay lacked the code-mode-host sibling and generated a fail-closed warning; packaged readiness and real WebSocket/OAuth/canonical `run.ps1` proof remain unestablished. No OAuth material was staged for these checks, and their containers are absent.

The resumed native verification is recorded in [`oauth-resumed-verification`](../../docs/workstream-e3a-oauth-resumed-verification-2026-09-08.md). It supersedes neither the historical stop nor this original artifact identity.

Separate AI code review approved the source/helper after final checks, with no correctness or security findings. Remaining limits are packaging, real provider/WebSocket/OAuth integration, canonical-launcher proof, and consistent active-spec implementation. Existing source preserves the OAuth/transport route; no route change is claimed. Build/source cache remains at `/tmp/alf-e3a-native-build-zavnIH`.
