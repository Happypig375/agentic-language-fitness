# E3a OAuth/no-tools adoption and bounded live permission

**Recorded:** 2026-09-08

**Resumed implementation:** after the retained five-failure apparatus stop, the
user explicitly authorized continuation. Native verification now passed; see the
[resumed implementation record](workstream-e3a-oauth-resumed-verification-2026-09-08.md)
and `PLAN.md` for the active checkpoint. The [stop record](workstream-e3a-oauth-implementation-stop-2026-09-08.md)
is historical, not a renewed permission gate. No live result is claimed.

The maintainer records the user's explicit adoption of the customized native
no-tools Codex client and the OAuth/Codex amendment. A distinct second user
message also explicitly authorizes OAuth staging, live calls, the bounded
shakedown, and continuation through the pilot/completion question. This is adoption, not a
human-expert review or a claim that implementation, packaging, provider
behavior, or remote wiring has been verified. Existing local OAuth and the
canonical remote launcher remain required; no API key, relay, proxy, backend,
image, or silent scaffold substitution is authorized. OAuth staging is limited
to the canonical ephemeral complete `auth.json` file (not the rest of `CODEX_HOME`) once prerequisites pass, with
mandatory cleanup; no new auth relay, toolful fallback, or secret relay is
allowed.

Immutable provenance: source patch
`df6a1797f51f40a784544fe499e94c8706231f52cb867ae2d1d820954638a267`, native
binary `f7942933b353186ea7cb216c47cddc321c5c4d120fde5a8df9e75122e2fc8816`,
upstream peeled commit `ff29a44391deccde0aba0f8390337d7f3c319ea4`, base repo
`a6a22f701d412ce0a06262a9d760c67645f59452`, and original specification
`8bc53d30e45dfa72b087225f89c9e5547266f05b47e4306e2b326d951888bc62`.

The permitted sequence is ordered: implement and review the adopted amendment;
run at most two dispatches on an unrelated trivial task as an OAuth shakedown;
only after success, freeze the adopted scientific specification against exact
runner/environment/image identities; then run the fixed 24-trajectory,
72-dispatch pilot. No automatic reissue, retry, replacement, or slot
substitution is permitted. Retained byte/time/dispatch limits, ambiguity stop,
null subscription cost, and post-turn overshoot risk remain accepted.

This record does not activate the experiment. Execution remains technically
held until the consistent implementation/specification revision, model-free
checks, packaging, canonical-launcher path, no-tools enforcement, and other
prerequisites are verified. The explicit adoption and bounded live permission
are the required authorization; do not request a redundant second gate.
Historic reports and the original amendment semantics remain unchanged.

## Methodological hold: authoritative context fit

Before any runtime or active-specification activation, the adapter must prove
strict pre-dispatch context fit. The current audit found the Luna model context
metadata at 272,000 tokens, but only the fixed approximate byte heuristic in
upstream commit `ff29a44391deccde0aba0f8390337d7f3c319ea4`,
`utils/string/src/truncate.rs:4,71` (`APPROX_BYTES_PER_TOKEN=4` and
`approx_token_count`), is available; there is no authoritative full-CLI-
scaffold-plus-request tokenizer/count before POST. Therefore no byte-to-token
bound, approximate count, or current `f794…` binary is integration proof. The
source audit of the client/session/context-window and model-provider-info merge
paths is another-AI/implementation-feasibility
review, not a test or provider proof. Existing `e3a_check` packet evidence
matches with `candidate_model_calls=0`; the 2026-09-08 remote read-only check
confirmed only the pinned binary/image identities. No OAuth staging was
performed as part of that check; remote auth locations were not inspected and
absence was not proved. The check did not establish live behavior.

The preceding strict-context-fit decision point is superseded by the user's
approved fixed-byte-cap choice below; it was a methodological alternative, not
a reason to re-request adoption or live permission.

The user has now approved that methodological choice: replace the strict
pre-dispatch token-fit guarantee with fixed authored-byte caps, native
compaction/truncation disabled, and any provider context-limit rejection
retained as a failed attempt that stops the batch without reissue. This is a
dated addendum to the adoption, not a new permission request. The active
specification remains `execution_authorized=false` until implementation and
review complete. It records visible-transcript replay, `max_replay_bytes=131072`,
post-turn alarms for 32,768 input / 8,192 output (not hard provider caps),
dispatch ceilings of 72 pilot / 2 integration, and null OAuth USD/count-call
fields. Existing environment, SDK, tasks, source and scoring identities are
unchanged; native single-response control work is an additive patch separate
from immutable `df6a…`.

The dated authorization record separately marks the user permission for a
two-dispatch live integration and, contingent on its successful checks and
freeze, the 72-dispatch pilot as approved. This is bounded permission, not
unlimited calls or current execution authorization; the active JSON remains
`execution_authorized=false` until the technical gate is implemented and
reviewed.

## Current implementation evidence: normal environment and route

On 2026-09-08 the remote host initially exposed only Docker `bridge`, `host`,
and `none`; the canonical `alf-internal` network was absent. A parent-side
read-only check found no `172.30` overlap and no listener on port `43128`, then
the canonical SSH path created the unchanged internal network:
`docker network create --internal --subnet 172.30.0.0/24 --gateway 172.30.0.1 alf-internal`.
The resulting network ID was
`a21f4952ad3edf2e6551abca91ecef384e81af948aa6f9832d0bbfd1179938bb`, marked
`internal=true`, gateway `172.30.0.1`, with no containers. This is normal
setup on the existing profile, not a new environment family.

The canonical foreground command
`powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\infra\remote-runner\run.ps1 -RemoteHost user@cez083.ce.ust.hk -RemoteSshPort 830 -EnvironmentProfilePath .\infra\remote-runner\environment-profile.json -RemoteCommand 'ss -ltn'`
returned exit 0 and showed `172.30.0.1:43128` bound (not public). This proves foreground
SSH listener creation only; it does not prove container TLS, provider/model
routing, native proxy behavior, or remote-auth absence. An initial read-only
`alf-egress` lookup failed; the later check established only that
`alf-internal` had been absent before creation. No OAuth staging or model call
occurred, and no formal E3a shakedown attempt/dispatch occurred.

## Dated change ledger: apparatus failures

The user's 2026-09-08 instruction raises this repository's engineering stop
from two to **five failed apparatus attempts** for the same unresolved gate.
Every attempt must be retained, and a success clears that gate's streak. This
is project-scoped and does not rewrite historical reports or their actual
two-failure counts. It does not permit five pointless retries when a
methodological contract is missing, and it does not alter the candidate's
maximum two repairs/three submissions or automatic-reissue prohibition.
Safety/material-scientific decisions, unknown live usage or ambiguity, budget
exhaustion, and other immediate hard stops remain immediate.

## Reproducibility and change taxonomy

All modifications must remain traceable and reproducible: retain the base
commit, additive patch hashes, normalized-LF source identity, code/scientific/
environment/runner identities as separate fields, exact rebuild commands,
focused test scope, and every attempt/outcome. Never publish auth material or
an auth hash. Do not claim deterministic provider completion from source,
fixtures, or a binary. The original `df6a…` no-tools patch is immutable; any
additional control patch must be recorded as a separate additive identity, not
as a replacement of that artifact.

See
the [amendment](../protocols/workstream-e3a-v1/oauth-amendment.md), [packet](../protocols/workstream-e3a-v1/README.md),
and [native record](../infra/codex-no-tools/README.md).
