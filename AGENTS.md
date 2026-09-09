# Maintainer agent entry point

Read [PLAN.md](PLAN.md) before substantive work. It owns the current checkpoint and next assignment.

**Current authorization (2026-09-09 HKT):** the user explicitly approved
continuation and increased the proposed fresh shakedown allowance to **five
dispatches**. This authorizes one fresh integration allocation (0/5 used) and,
after a matching successful two-step shakedown and freeze, one fresh fixed
24-trajectory/72-dispatch pilot (0/72 used). The [renewal record](docs/workstream-e3a-oauth-renewal-2026-09-09.md)
owns the current assignment. Prior unused balances do not stack; every earlier
attempt and debit remains retained. No automatic retry or later replacement
is authorized. Keep local OAuth, the canonical launcher and all hard stops.

**Prior checkpoint (2026-09-09 HKT):** pilot attempt 02 on exact-CI-green
`c79bc1c` stopped after one dispatch with `multiple-final-replies`: one complete
native turn contained a preamble and JSON in two assistant-message items.
The [retained stop and policy-correct repair](docs/workstream-e3a-complete-response-fix-2026-09-09.md)
own the next assignment. The ordinary fix now assembles all assistant text
unchanged and uses existing format/byte/repair controls; 81 affected tests and
separate AI review passed. Do not strip commentary or select the last JSON.
The repair was published as `bc00062` and its exact Linux/Windows CI passed.
The explicit renewal above resolves that checkpoint's allocation decision;
it does not promote, resume or rescore the stopped attempt. Preserve its null scores.
Pilot usage is **one of 72 dispatches**; 23 of 24 slots remain unstarted.
The old freeze correctly rejects the repaired source; do not bypass it.
Missing Task 007 rubric judgement stays unknown and cannot drive continuation.

The prior resumed integration ceiling was **five dispatches**, with **four
used and one remaining**. The guard is per invocation, not persistent:
before any later integration invocation, calculate cumulative debits and the
remaining allowance from retained journals and honor required stop decisions.
A fresh guard does not reset or stack authorization. Attempt 01 remains
separately failed, debited, unapplied and unscored. No ambiguous reissues or
relaxed hard stops are authorized. One remaining integration dispatch cannot
fund a fresh two-step shakedown; that old remainder is not added to the new five.
Temporary auth cleanup is verified for the
two successful shakedowns and both pilot attempts; no proxy listeners or E3a
containers remained in the scoped checks. Earlier cleanup records are retained.

Do not ask for renewed adoption, ordinary bug-fix or direct-push permission.
The earlier two-dispatch allowance/hold narratives below remain history and
are superseded by this explicit allowance and current repair checkpoint.

## Current boundary

E1/E2/E2a are complete. The E3a packet at `19b1902be59324b98741ccb6c3a8396de962f5f7` passed its Linux/Windows fixture checks and has received a second AI-session review. The [disposition](docs/workstream-e3a-review-disposition-2026-09-06.md) accepts the narrow design **for bounded implementation with R1–R4 corrections**, not as a working or authorized live experiment.

The bounded E3a no-tools controller/adapter and isolated evaluator contain R1–R4 corrections. After explicit permission to resume model-free fixes on the reachable remote host, dependency export was repaired and the sandbox checks passed there with the exact specified image. Read the [remote fix and evidence](docs/workstream-e3a-remote-sandbox-fix-2026-09-06.md); the [earlier handoff](docs/workstream-e3a-implementation-handoff-2026-09-06.md) preserves the two failed CI attempts. Verify CI on the exact implementing commit, not an earlier green check.

The pinned image is now restored on the remote host. Standalone sandbox evidence is not end-to-end Windows/API-to-remote integration. Wiring, account access, provider behavior and counting remain unverified. The dated [OAuth adoption record](docs/workstream-e3a-oauth-adoption-2026-09-08.md) permits implementation, an at-most-two-dispatch unrelated-task shakedown after prerequisites, and continuation after successful freeze to the fixed pilot; no automatic reissue/replacement is allowed. Do not switch images, scaffolds or subscription backends silently.

**Current boundary:** the [OAuth/Codex amendment](protocols/workstream-e3a-v1/oauth-amendment.md) remains adopted. Existing local OAuth and the canonical remote launcher remain required; no API key or new relay. The failed live shakedown is now an explicit stop, not a successful freeze or a pilot prerequisite. Earlier readiness/activation paragraphs below describe the path to that attempt, not permission to repeat it.

**Technical hold (2026-09-08):** the implementing binary is now `72cf14453…`,
with opt-in no-tools and single-response controls. The original `f7942933…`
binary is historical. Packaging and model-free tests do not establish OAuth or
live provider behavior. After implementing-commit CI and remaining prerequisites,
the permitted sequence is ≤2-dispatch shakedown, successful freeze, then the fixed
24-trajectory/72-dispatch pilot. Stage only the complete `auth.json` file into a
private temporary home, not the rest of `CODEX_HOME`; cleanup is mandatory.
No new auth relay, toolful fallback, reissue or replacement is authorized.

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
- Missing usage remains null; token subsets are not added twice. OAuth debits dispatches before launch and retains ambiguous debits; token thresholds are post-turn alarms and subscription cost stays null. Historical API protocols retain their own reservation rules.
- No new remote/proxy layers or generic agent framework. H does not require optional F/G completion.

## Automatic bug fixes

Fix confirmed implementation bugs automatically within the authorized plan;
do not stop merely to ask whether to fix them. Reproduce the defect, make the
smallest appropriate repair, add regression coverage, and complete applicable
validation/review. Record the cause, changes, checks and source identities so
the repair is traceable and reproducible. Preserve failed attempts and archived
results; ordinary runner fixes do not require a new scientific version.

A live-execution hold does not itself prohibit safe model-free diagnosis or
repair. This direction does not authorize new live dispatch allowances,
automatic reissues/replacements, scientific treatment changes, relaxed security
boundaries, or bypassing another explicit stop. If the fix requires one of
those changes or the intended behavior is ambiguous, report that specific
decision instead of treating it as an ordinary bug fix.

## Publishing

For completed, validated work within the authorized plan, commit and push directly
to the current branch's configured upstream **without creating a pull request**.
This is standing authorization for routine in-scope commits and pushes; do not
ask for publication approval again at each checkpoint. Stage only in-scope files,
preserve unrelated work, and verify CI on the exact pushed commit. This does not
authorize force-pushing, rewriting history, or bypassing scientific, security,
or live-execution gates.

## Handoff and stops

Finish ordinary code, tests, documentation and applicable CI within the bounded assignment. Report exact source/spec identities, checks actually run, unresolved conditions, request/spend ceilings and next decision. Identify reviews honestly as self-review, another AI session or human review.

**Project-scoped apparatus rule (2026-09-08):** for one unchanged unresolved
apparatus gate, permit up to **five** failed apparatus attempts, retaining every
attempt; a success clears that gate's failure streak. This replaces the prior
two-failure engineering stop for this repository only and does not rewrite
historical reports. Stop immediately for safety or material scientific choice,
unknown live usage/ambiguity, budget exhaustion, or another explicit hard gate.
Candidate maximum two repairs/three submissions and automatic live reissue
prohibition are unchanged.

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
