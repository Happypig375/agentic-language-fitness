# Maintainer agent entry point

Read [PLAN.md](PLAN.md) before substantive work. It owns the current checkpoint and next assignment.

## Current boundary

E1/E2/E2a are complete. The E3a packet at `19b1902be59324b98741ccb6c3a8396de962f5f7` passed its Linux/Windows fixture checks and has received a second AI-session review. The [disposition](docs/workstream-e3a-review-disposition-2026-09-06.md) accepts the narrow design **for bounded implementation with R1–R4 corrections**, not as a working or authorized live experiment.

The bounded E3a no-tools controller/adapter and isolated evaluator contain R1–R4 corrections. After explicit permission to resume model-free fixes on the reachable remote host, dependency export was repaired and the sandbox checks passed there with the exact specified image. Read the [remote fix and evidence](docs/workstream-e3a-remote-sandbox-fix-2026-09-06.md); the [earlier handoff](docs/workstream-e3a-implementation-handoff-2026-09-06.md) preserves the two failed CI attempts. Verify CI on the exact implementing commit, not an earlier green check.

The pinned image is now restored on the remote host. Standalone sandbox evidence is not end-to-end Windows/API-to-remote integration. That wiring, account access, rates/count charges and provider continuation/counting remain unverified. No live call is authorized: the later two-generation/$0.05 integration and pilot still require separate approval. Do not switch images, scaffolds or subscription backends silently.

**Current boundary:** the [OAuth/Codex amendment](protocols/workstream-e3a-v1/oauth-amendment.md) is review-ready after separate maintainer-AI review, not adopted or activated. The user requires existing local OAuth and the canonical remote launcher; no API key or new relay. Visible-history replay and turn/time/byte limits require explicit maintainer adoption of their scientific and overshoot-risk changes. No-tools enforcement remains a prerequisite. Adoption, model-free implementation evidence, and separate live-run permission remain distinct gates; see [PLAN.md](PLAN.md#maintainer-authentication-direction-2026-09-06).

**Technical hold (2026-09-06):** the [no-tools prerequisite check](docs/workstream-e3a-no-tools-check-2026-09-06.md) is now bounded model-free evidence that the customized native scaffold is ready for the next maintainer decision; it is not a global unsupported-tool guarantee. Final native tests/build/probes and separate AI review passed as documented there. Production adoption, amendment activation, and live authorization remain held. The next distinct step is explicit adoption of this customized native client plus visible replay, dispatch/byte/time controls, and overshoot-risk treatment, followed by model-free OAuth-adapter implementation/review; this is not automatic pilot authorization. No automatic toolful fallback, relay, or OAuth staging is authorized.

## Read only what applies

- Current E3a decision: [review disposition](docs/workstream-e3a-review-disposition-2026-09-06.md) and [reviewed packet](protocols/workstream-e3a-v1/README.md).
- Design/analysis: [experimental design](docs/experimental-design.md), [metrics](docs/metrics.md).
- Workload/review scope: [validity and gates](docs/workload-validity-and-review-gates-2026-09-05.md).
- Context-pressure work, when assigned: [H design](docs/workstream-h-context-pressure-design-2026-09-05.md).

Current governance applies to future work. Older proposals and their checked-in review packets remain identifiable history; they do not override the current disposition. Already authorized frozen protocols govern their own experiments. Reconcile conflicts rather than silently changing a frozen treatment.

## Essential invariants

- Candidates may see the approved predecessor, never successor gold, future tasks, research outcomes or final holdout cases.
- Holdout scores must not influence feedback, continuation or retries. Task 007 behavioral success alone is not completed refactoring; missing required rubric evidence stays unknown.
- Distinguish unsafe project changes from safe but wrong F# Compile lists: the latter are repairable project failures, not terminal safety violations.
- Valid feedback exceeding its allowance terminates that trajectory under its fixed budget; controller faults are different. Never discard failures or let a language's long diagnostic output silently cancel unrelated samples.
- Preserve every submission and attempt. Do not manually fix candidate code or rewrite archived gold/results.
- Candidate code/project execution is sandboxed without model credentials, host secrets or writable scoring machinery. No fallback to executing untrusted code on the host.
- Missing usage remains null; token subsets are not added twice. Reserve request costs before dispatch and keep ambiguous attempts charged against the guard until reconciled.
- No new remote/proxy layers or generic agent framework. H does not require optional F/G completion.

## Handoff and stops

Finish ordinary code, tests, documentation and applicable CI within the bounded assignment. Report exact source/spec identities, checks actually run, unresolved conditions, request/spend ceilings and next decision. Identify reviews honestly as self-review, another AI session or human review.

Return at implementation completion, material scientific/security change, exhausted authorized resources, ambiguous requests or repeated unresolved apparatus failure. Mock success is not proof of provider behavior. A later explicitly authorized frozen batch can use automatic health checks; no redesign or sample extension after seeing which language wins.

## Existing model-free entry points

```text
python -m unittest discover -s tests -v
python scripts/e3a_check.py
python scripts/e3a_check.py --build-fixtures --output results/e3a-review-fixtures.json
python scripts/e3a_sandbox_check.py --output results/e3a-sandbox.json
python scripts/alf.py doctor --strict
```

e3a_check builds trusted fixtures only; it is not an arbitrary-candidate evaluator. e3a_sandbox_check requires Linux Docker and the exact image; its explicit CI SDK-fixture mode is model-free, non-experimental evidence only. Use checks appropriate to the change and report their actual scope.
