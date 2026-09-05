# Maintainer agent entry point

Read [PLAN.md](PLAN.md) before substantive work. It owns the current checkpoint and next assignment.

## Current boundary

E1/E2/E2a are complete. The E3a packet at `19b1902be59324b98741ccb6c3a8396de962f5f7` passed its Linux/Windows fixture checks and has received a second AI-session review. The [disposition](docs/workstream-e3a-review-disposition-2026-09-06.md) accepts the narrow design **for bounded implementation with R1–R4 corrections**, not as a working or authorized live experiment.

The next assignment is the minimal E3a no-tools controller/adapter and isolated evaluator, with mock transport and model-free tests. Implement the disposition's task-completion rubric, repairable safe Compile mistakes, trajectory-local feedback exhaustion, and conservative pre-dispatch budget/count guard. Update the unfrozen specification, generated packet, and tests together. Do not restart design preparation or add tasks/scaffolds/workstreams.

No live candidate request or continuation smoke test is authorized by these files. Account access, actual provider continuation/counting and remote sandbox integration remain unverified. Return after implementation/model-free evidence and applicable exact-commit CI, before the separately capped live integration or pilot. Do not replace the API proposal with a subscription-backed adapter silently.

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
python scripts/alf.py doctor --strict
```

The current e3a_check script builds trusted fixtures only; it is not an arbitrary-candidate evaluator. Use checks appropriate to the change and report their actual scope.
