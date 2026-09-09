# H1/H2 pre-execution packet

This is the bounded model-free implementation of the
[adopted proposal](../../docs/workstream-h1-h2-overlap-design-2026-09-09.md).
It is not a live freeze or permission to consume model quota. The
[specification](specification.json) keeps both execution approvals false and both
H dispatch allocations zero. No E3a balance transfers to H.

Start with the [implementation and human-review checklist](../../docs/workstream-h1-h2-implementation-2026-09-09.md)
and the [paired source review](../../reports/workstream-h1-h2-preexecution-2026-09-09/source-review.md).
The source/contract/case/public-prompt identities, two byte caps and fixed schedule
are construction measurements. Scientific-policy, runner, environment and actual
attempt identities remain separate; failed apparatus checks do not create new
scientific versions.

The live runner is `scripts/h_run.py`. It reuses the existing native transport,
local OAuth direction, foreground SSH route and isolated evaluator. It refuses
the current specification before inspecting auth/native paths or constructing a
transport. Do not invoke it as a model-free test by changing approval flags.

After human review, a separate approval may allocate at most five integration
dispatches (three planned: H1 submit, then H2 read and submit). A pilot needs its
own allocation of at most 64 dispatches and a matching successful integration
report bound by a tracked freeze. All 32 planned slots remain identifiable;
infeasible slots, early completion and failures reduce use, never add samples.
Unknown subscription USD and post-turn-only token alarms are explicit limitations.

The `human_review_approved` and `h_live_integration_verified` fields record
approval/evidence bookkeeping, not scientific treatment. They are excluded from
the policy hash, but the full specification and integration report retain their
exact identities. Model, workload, public instructions, cases, caps and schedule
remain policy-bearing. A report's successful integration flag alone cannot
substitute for matching policy/runtime hashes or confirmed cleanup.

CI is model-free even after a future activation. Its explicit `--permit-activation`
allows only read-only auditing of such a specification. SDK-fixture checks use a
private disabled copy and label the substituted image non-experimental; the
production sandbox still refuses a fixture-image override on an activated spec.
No OAuth cache or model credential is used in CI.
