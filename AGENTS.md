# Maintainer agent entry point

Read [PLAN.md](PLAN.md) before substantive work. It owns the current checkpoint and next assignment; do not copy its evidence tables into this file.

## Current boundary

E1/E2/E2a are complete. The [E3a review packet](protocols/workstream-e3a-v1/README.md) and minimal model-free fixtures are prepared for independent review and maintainer disposition, not experimental execution. Its oracle limitation, proposed no-tools scaffold, and unverified live gates are explicit. Follow `PLAN.md`; no model-consuming continuation or new adapter is authorized by this handoff.

Do not launch live candidate requests, continuation smoke tests, new paid review agents, E3b/F0, subagents, or H runs without explicit authorization. This does not prohibit the already authorized maintainer assistant from reading, editing, reasoning, or running ordinary model-free tests. A local freeze or self-review cannot authorize model consumption.

## Read only what applies

- Design/analysis changes: [experimental design](docs/experimental-design.md), [metrics](docs/metrics.md).
- Workload or review scope: [validity and gates](docs/workload-validity-and-review-gates-2026-09-05.md).
- Context-pressure work: [H design](docs/workstream-h-context-pressure-design-2026-09-05.md).
- Why this plan changed: [review findings](docs/plan-review-2026-09-05.md).
- E2a evidence: [disposition](docs/workstream-e2a-disposition-2026-09-04.md), [report](reports/workstream-e2a-host-aligned-v1/report.md).

Current governance applies to future work. Authorized frozen protocols govern their own experiments. Older dated design proposals are historical, not alternative instructions. Stop to reconcile a conflict rather than silently changing a frozen treatment.

## Essential invariants

- Separate maintainer and candidate contexts. A candidate may see its approved predecessor source; it must not see target/successor gold, future tasks, research instructions/outcomes, or final holdout cases. Blinding cannot hide which programming language the source uses.
- Final holdout results must not influence candidate feedback or repair stopping. Use the declared development checks for continuation.
- Preserve submissions, every attempt, raw evidence, and provenance. Do not repair candidate patches manually, exclude failures opportunistically, or rewrite old reports.
- Evaluation of candidate code/project files is sandboxed and has no model credentials, host secrets, or writable scoring machinery. Keep authentication infrastructure outside candidate-readable paths.
- Missing/unsupported telemetry is null. Provider totals, token subsets, visible-text estimates, context occupancy, and monetary/subscription cost are different measures.
- No new remote runner/proxy layers or generic multi-agent framework. H need not wait for optional repair-routing or G replication.

## Handoff and stop rules

Finish ordinary implementation, tests, documentation, and applicable CI within the authorized packet; do not stop after every small commit. Return with the exact head/specification identity, changed scope, checks actually run, unresolved issues, budget/request ceiling, and next decision. State when review is self-review, another AI session, or human review; never invent independent sign-off.

For a later explicitly authorized frozen batch, follow its registered operational checkpoints and produce its fixed report. Do not redesign or extend sampling after seeing which language wins. Return for material changes, spend limits, unsafe/ambiguous requests, repeated unresolved apparatus failures, or the planned handoff.

Pending CI or a mocked continuation fixture is not proof of live success. Live continuation/usage validation belongs to a separately authorized capped integration step.

## Existing model-free entry points

```text
python -m unittest discover -s tests -v
python scripts/alf.py doctor --strict
python scripts/alf.py validate
python scripts/alf.py matrix --agent scripted --output results/pilot
python scripts/alf.py audit <run-directory>
```

Use only the checks relevant to the change and report their scope. Do not run a candidate adapter as a substitute for a model-free test.
