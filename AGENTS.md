# Agent entry point

Read `PLAN.md` before substantial work. It is the canonical checkpoint and continuation order.

## Current checkpoint

Workstreams E1 and E2 are complete and accepted within their stated evidence boundaries.

E1’s archive-only report reconciled 10 v3 runs and 80 tasks. The leading observed difference is repair/compiler interaction, not static source size:

- F# had 23 observable failed builds versus 2 for C#;
- F# had 17 conservative repair cycles versus 2 for C#;
- all five committed project-file changes were F#;
- evaluator time was approximately twice as large for F#;
- observable pre-edit inspection/search differences were comparatively modest and cannot identify training familiarity.

E2’s model-free offline baseline found near-parity source/token proxies and built-program run time, but F# restore/build was slower. The repeat-build ratio was about 3.1× and is the cleaner direct toolchain signal. The 8.403× restore ratio is audit/source sensitive: the offline run emitted 225 repeated F# `NU1900` lines. Do not transport E2 timing to v3 without matching command semantics, package-cache and audit behavior, source/network access, host hardware, storage/filesystem, container, and resource limits.

The joint evidence supports a coupled working hypothesis:

```text
first-pass/type/project difficulty
  -> more failed builds and repairs
  -> more diagnostics, commands, and model turns
  -> more input/output/time

slower compiler/toolchain
  -> amplifies each extra repair cycle
```

This is descriptive mechanism routing, not a causal or universal language result. See:

```text
docs/workstream-e1-e2-synthesis-review-2026-09-04.md
reports/workstream-e-v3/forensic-report.md
reports/workstream-e2-toolchain-v1/report.md
```

V4–V13 are apparatus-development history. Do not create v14. Reuse `runner-remote-highmem-local-egress-r1` unless a separately reviewed candidate-visible change is required.

## Next bounded task

Implement and independently review **E2a: exact-command, host, and environment-aligned model-free baseline**.

E2a must use no candidate agent or model endpoint. It should:

1. reconstruct a redacted frequency table of the command-equivalence classes actually observed in E1;
2. collapse only semantically equivalent variants and benchmark every materially observed distinct build/restore/run/test form;
3. execute on the v3 remote host/profile when safely reproducible, matching image, CPU/memory/PID limits, storage/filesystem, build configuration, package cache, environment, audit behavior, and source/network reachability; explicitly bound any mismatch;
4. add an otherwise matched `NuGetAudit=false` restore control;
5. preserve the accepted offline E2 result as a separate ecology;
6. report absolute seconds/output volume beside ratios;
7. calculate a mechanical invocation-count × duration tool-exposure envelope without subtracting it from agent cost;
8. state whether `NU1900` appeared in v3 or is unavailable;
9. pass independent review and exact-commit Linux/Windows CI.

Stop after E2a publication. Do not continue automatically into E3 and do not issue a model request.

## After E2a

Design and independently review E3 under a new scientific specification:

- matched gold predecessor snapshots;
- one exact model/scaffold configuration selected for nondegenerate first-patch outcomes; M (`gpt-5.6-luna`, high) is the provisional default, while L is near a first-build floor and H has too much missingness;
- one simple task, one type/validation task, and one multi-file/project/API task;
- controller-defined first patch and external first build;
- comprehension/localization auxiliary arm;
- one-shot patch primary arm;
- monolithic full-repair primary arm;
- failed-build episodes, unique diagnostic categories, first-patch correctness, repair cycles, and full trajectory cost as separate outcomes.

The one-shot/full comparison is a harness-policy contrast, not literal mediation subtraction. E3 remains non-confirmatory and cannot expand into a large factorial.

Only if E3 confirms repair amplification should Workstream F test routing. Stage it:

1. fresh inline versus fresh isolated repair worker;
2. persistent inline versus persistent isolated worker only after separate-context accounting works.

Use the same model for orchestrator and worker first. Do not build a generic multi-agent framework, recursive subagents, dynamic routing, or a cheaper-worker arm prematurely.

## Evidence boundaries

- V3 calibrations are non-counting and excluded from future formal estimates.
- E1/E2 are descriptive and model-free/archival mechanism evidence, not causal language inference.
- Aggregate input is total trajectory usage, not unique source memory.
- A generation error can create much larger later input through diagnostics and replay.
- Diagnostic occurrence counts are not independent defect counts.
- E2 restore is offline, audit-sensitive, and host-sensitive; repeat build is the cleaner toolchain result within that apparatus.
- Current repositories are too small to test context-window fit or semantic-density crossover.
- Fresh-per-task v3 cannot test cross-task context pollution.
- No result establishes a universal F#, C#, model, or harness ranking.

## Development agents versus benchmark candidates

These instructions guide agents maintaining the research repository. Candidate agents must remain blind to `AGENTS.md`, `PLAN.md`, hypotheses, prior outcomes, treatment labels, gold states, and hidden evaluator cases. Preserve `--ignore-user-config`/`--ignore-rules` or the reviewed equivalent.

## Research invariants

- Match semantic tasks, starting states, evaluator, limits, and candidate authority within each treatment.
- Record every attempt; never silently replace an ambiguous or potentially billable request.
- Keep scientific-specification, runner, environment, model, effort, schedule, and attempt identities separate.
- Separate source exposure, model output, tool feedback, total input, toolchain time, orchestrator cost, worker cost, and end-to-end cost.
- Unsupported telemetry is null/unavailable, never zero.
- Preserve immutable E1/E2 evidence; corrections belong in addenda/new reports rather than rewriting accepted outputs.

## Autonomous stopping rules

- Every autonomous task must name one bounded artifact/gate and its acceptance criterion.
- The current task ends after E2a report/review/CI; it may not start E3 or invoke a model.
- After two failures of one apparatus class, stop and report instead of adding another route or compatibility layer.
- Stop before changing candidate-visible semantics, model/prompt/task/evaluator, harness memory/routing, or a frozen scientific condition without reviewed authorization.
- Prefer the smallest deterministic measurement that resolves the decision.

## Validation

```text
python -m unittest discover -s tests -v
python scripts/alf.py doctor --strict
python scripts/alf.py validate
python scripts/alf.py matrix --agent scripted --output results/pilot
python scripts/alf.py audit <run-directory>
```
