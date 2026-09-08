# E3a resumed native verification — 2026-09-08

The resumed bounded implementation passes native checks and all 120 affected
Python tests. Another AI session approved the repaired source, not live provider
behavior or human-expert research validity. Publication and exact implementing-
commit CI remain outstanding. `execution_authorized=false`; no OAuth staging,
experimental dispatch, shakedown or pilot occurred.

This continuation does not rewrite the [earlier five-failure stop](workstream-e3a-oauth-implementation-stop-2026-09-08.md).
The user explicitly resumed work. Preparation attempt 06 passed; its formatting
warnings concern stable rustfmt's nightly-only import option. Scoped clippy
removed an unrelated unused import, which was restored before source export;
the known warning is retained, not hidden by a test-source edit.

## Identities

The base repository commit remains `a6a22f701d412ce0a06262a9d760c67645f59452`;
there is no new published implementing commit in this record. Active unfrozen
specification canonical SHA-256:
`076493b2098f828ea84d2dadf1c7c685c8efbc13112dca2f9e6702ea48cbbf0e`.
Policy SHA, excluding only `status` and `execution_authorized`:
`95b1b7db184236c0b81982160f1c82394225bbc23a86762925a5c0a84771c13b`.
Normalized reviewed source-set SHA (the packet's text paths except active spec):
`c73023fc687c49a45704d78d0af1fd76fe6dab1595cad1e087d1a8628014ef0f`.
The [packet](../protocols/workstream-e3a-v1/review-packet.json) carries individual
LF file identities. These are separate from a future Git commit and CI result.

The implementing native binary is `72cf14453c1879996b970accc7de9aa114bf570e586230799a429d0741bb1959`, at `/tmp/alf-e3a-native-build-zavnIH/codex-native-single-response`. Additive patch identity is `5b1af9214058ab8ff74c463e61598e9dc4121b804774394f6b9dc0867e2c117b`; combined full patch is `00d54d4e7c1a22495382b609697149c508244cdb2731606114abe99f6d10b560`. Original no-tools patch `df6a1797f51f40a784544fe499e94c8706231f52cb867ae2d1d820954638a267` is unchanged.

Probe artifacts were downloaded and hashed: baseline `dfc371c1be33981fb641a3af938090d8d3ee3697ff423a06b69fc1dabba6ffdf`, hostile tool-call `6b8cb0431597350a17d1aa4142f49e49413f88c89d0bf000872879a7e5767bdd`. Each made one POST, no follow-up or tool marker, and had zero candidate-model/real-provider calls. Baseline exited normally; hostile input exited with the expected fatal result. No containers remained.

Source audit found generation retry, generation-time 401 recovery, WebSocket fallback, compaction/truncation, and post-completion follow-up disabled under the adopted no-tools/single-response combination. This is not a universal context-limit guarantee; only a high-usage session test and loopback probes were exercised. The supported `model_catalog_json` path now pins the bundled catalog SHA-256 `c18214b1ba88ab9bd164753115324a7a29c0582e8d071f7b3babf749d892f549` and disables catalog refresh (not non-generation OAuth refresh).

Auth staging is restricted to a complete `auth.json` file copied into an
ephemeral private home and removed afterward, not the surrounding `CODEX_HOME`
configuration, history or plugins. OpenAI's [authentication guidance](https://learn.chatgpt.com/docs/auth)
supports copying the complete cache file and treating it as a credential; the
existing route and normal non-generation refresh are retained. This use of
official guidance is not a provider compatibility test. No auth bytes were read
into reports, hashed, or published.

## Checks and retained attempts

All artifacts below are in [the evidence directory](../reports/workstream-e3a-oauth-implementation-2026-09-08/).

| Scope | Result | Evidence |
|---|---|---|
| Native preparation 06 | Pass; unrelated clippy change restored | `e3a-single-response-prepare-06.sh`, `single-response-format-06.log`, `single-response-lint-06.log`, `e3a-single-response-restore-unrelated.patch` |
| Native tests/build | 107 passed, 3,715 not selected, zero retries; build passed | `e3a-single-response-test.sh`, `single-response-tests-01.log`, `single-response-build-01.log` |
| Exact-binary loopback probes | Normal rc 0, hostile rc 1 (expected); each one POST, no follow-up/side effects | `e3a-single-response-probes.sh`, `native-single-response-baseline.json`, `native-single-response-tool-call.json` |
| Packaging attempt 01 | Version passed; catalogue command failed because the fixture omitted the home directory | `e3a-single-response-package-probe.sh`, `package-probe-01-catalog.stderr` |
| Packaging attempt 02 | Pass after mounting an empty private home, as production supplies | `e3a-single-response-package-probe-02.sh`, `package-probe-02-summary.json`, version/stdout and catalogue/stderr files |
| Python manifest 01 | Five modules passed; one test incorrectly expected the turn workspace to survive return | `python-*-01.log` |
| Python correction 02 | Corrected test observes existence during launch and absence afterward; affected modules passed | `python-test_e3a_run-02.log`, `python-test_workstream_e3a-02.log` |

The packaging probe uses the image's original entrypoint with the reviewed
binary mounted at `/usr/local/bin/codex`, fixed catalogue at
`/opt/alf/models.json`, network `none`, no credentials, read-only root and writable
256 MiB `/tmp`, nonroot UID, 2 CPUs, 6 GiB memory/swap and 512 PIDs. It validates
version and catalogue loading, not a generation through `run_e3a_cli`/`run.ps1`.
Luna/high is present; context metadata is 272,000 (max 872,000), not an
authoritative pre-dispatch tokenizer. Full repeated catalogue/scaffold stdout
is retained locally/remotely and hashed in the small summary, not duplicated
into the public report. Only the named probe containers were checked absent.

Final Python manifest: `test_e3a_codex.py` 10/10;
`test_e3a_implementation.py` 28/28; `test_workstream_e3a.py` 19/19;
`test_codex_docker.py` 26/26; `test_e3a_run.py` 14/14;
`test_e3a_codex_check.py` 23/23. Each ran using:

```text
.venv/Scripts/python.exe -m unittest discover -s tests -p <filename> -v
.venv/Scripts/python.exe scripts/e3a_check.py
git diff --check
```

The last two checks passed; packet reports `candidate_model_calls=0`.
No global unit suite or experimental candidate evaluation was substituted for
this affected manifest. The prior full manifest failure and corrected rerun
remain recorded. Preparation and packaging successes clear their respective
failure streaks; the historical five-failure stop remains unchanged.

## Native reproduction

Start from LF upstream `ff29a44391deccde0aba0f8390337d7f3c319ea4`, apply
`no-tools.patch`, then the additive `single-response.patch` (7 files, 308 additions,
11 deletions). Clean apply checks passed. The combined full patch is a comparison
artifact against upstream, not a third patch to apply after those two.

Use the builder/V8/tool inputs in the [native build record](../infra/codex-no-tools/README.md#original-no-tools-only-sourcebuild-record-historical).
Normalize the 139 workspace version labels with the documented isolated
`cargo update --offline --workspace` step; lock SHA remains
`46febaad4d299009603ea1fc4da19545d5b28eb562b2e654bec75024e5ca0b67`.
External dependency records are unchanged. The retained scripts show exact
format/lint/test/build arguments and package/loopback Docker invocations. The
focused native selector is:

```text
just test --cargo-profile dev-small -p codex-api -p codex-core -p codex-features --test-threads 3 -E 'test(client::tests::) | test(sse::responses::tests::) | test(no_tools_feature_fails_closed_in_session_without_followup) | test(single_response) | package(codex-features)'
```

Then, from `codex-rs`, `cargo build --locked --profile dev-small -p codex-cli`.
The build cache `/tmp/alf-e3a-native-build-zavnIH` is retained; it is not a secret
cache or a published reproducible-image guarantee. Extract the fixed catalogue
from upstream `codex-rs/models-manager/models.json`; no different image or
external dependency family was introduced.

## Implementation and review disposition

The adapter now retains exact encoded replay before launch, debits one shared
phase guard, accepts only the six-field bounded transport capture, and does not
replay JSONL/usage metadata. Completed under-cap answers remain scoreable when
usage is missing/invalid/excessive; further dispatch stops. Submission overflow
is not applied; replay overflow consumes no new submission or dispatch. Missing
usage stays null, optional unproven zeros stay null, and known zero repair cost
for successful first submissions is preserved. Every scheduled pilot slot
remains represented.

The wrapper stages only the complete auth file, validates native/catalogue pins
before staging, reserves cleanup time, bounds combined capture, removes its own
container and temporary auth home, and leaves legacy non-E3a behavior intact.
Active request/token maxima are null, explicit alarm fields replace misleading
hard caps, and hidden `reasoning_context` is null. Historical API fixture budget
semantics remain unchanged.

`scripts/e3a_run.py` composes the existing wrapper and evaluator. Its shakedown
uses only the approved project settings plus a separate tiny marker program,
not benchmark candidate source. It performs credential-free preflight, two
explicit integration steps, durable journal/report output, and evaluator
cleanup. The second exercise is explicitly not failure feedback or a measured
repair. There is no new service, proxy, backend or automatic reissue.

Another AI source review requested two integrity fixes: hard-pin the reviewed
native binary instead of trusting the caller's hash, and bind a future pilot to
the successful shakedown. Both were implemented and the narrowed rereview
approved them with no actionable findings. The small future `freeze.json`
contains `specification_sha256`, `policy_sha256`, `shakedown_report` and
`shakedown_report_sha256`. Pilot checks the successful live report's two completed,
applied, passing exercises and the same source/native/catalogue/image/profile
identities. Only status/activation may differ in the policy; a different Git
commit solely to record a freeze does not force a new runner identity. No freeze
record exists yet and no mock can qualify. This is mistake prevention in trusted
maintainer records, not a certificate service or protection from a maintainer
rewriting trusted code.

## Next boundary

Publish the reviewed implementation and verify Linux/Windows CI on that exact
commit; the older green `a6a22f7` result is not evidence for this change. Then
activate only the already approved ≤2-dispatch unrelated OAuth shakedown through
the canonical foreground SSH launcher. Retain any failure and stop on ambiguity;
do not reissue. A successful shakedown permits freeze and the fixed 24 trajectories
/ 12 pairs / ≤72-dispatch pilot, not sample extension. Post-turn alarms are
32,768 input / 8,192 output, not hard caps; USD/subscription cost and unreliable
provider-request counts remain null.

Publication/CI, actual OAuth/model access, live usage semantics, full canonical
launcher/evaluator integration and later rubric evidence remain distinct from
the completed model-free checks. No additional scientific or live-adoption
permission is being requested. The unrelated untracked `uv.lock` is preserved
and is not part of the reviewed runner identity or selected publication scope.
