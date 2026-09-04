# Agent entry point

Read `PLAN.md` before substantial work. It is the canonical checkpoint and continuation order.

## Current checkpoint

Workstreams E1, E2, and E2a are complete and accepted within their stated evidence boundaries. E2a authenticated 435 v3 command events and 258 benchmark `dotnet` operations, then ran 1,020 model-free samples in five paired rounds on the v3 remote host/profile.

The joint evidence now shows two compounding ecological effects:

- F# trajectories invoked more benchmark tool operations: 163 versus 95 for C# across the retained v3 runs;
- restore/build-capable F# operations were slower, with a major `NU1900` vulnerability-audit component and a remaining no-restore compiler/toolchain gap after audit was disabled.

Pure test and direct-DLL execution were near parity. The mechanical invocation-count × duration envelope is large relative to the observed wall-time gap, but it is descriptive, not mediation, and is never subtracted from agent cost. Model-token differences still require additional turns, diagnostics, feedback, and replay.

Read:

```text
docs/workstream-e2a-review-and-successor-revision-2026-09-05.md
docs/workstream-e2a-disposition-2026-09-04.md
reports/workstream-e2a-host-aligned-v1/report.md
```

V4–V13 are apparatus-development history. Do not create v14. Preserve immutable E1/E2/E2a evidence; corrections belong in addenda or new reports.

## Next bounded task

Specify and independently review **E3a: controlled first-patch and bounded repair**. Produce the scientific specification, deterministic fixtures/identities, clean freeze, and exact-commit CI only. Do not invoke a model or execute the pilot without a separate maintainer/user decision.

E3a must:

1. use matched canonical gold predecessors and a minimal simple/type/multi-file task set;
2. use one frozen model/scaffold configuration, provisionally Luna high because archived first-build outcomes were nondegenerate;
3. compare one-shot patch with controller-mediated bounded repair;
4. make the controller own the first patch, audit-off restore, fixed no-restore build, and direct/no-build evaluator path;
5. prevent candidates from choosing arbitrary build/run/test commands in this controlled mechanism treatment;
6. record usage, patch identity, diagnostics, candidate-visible feedback, and controller tool time separately for every repair round;
7. treat localization as auxiliary or conditional rather than another co-primary arm;
8. remain non-confirmatory and stop after its frozen sample.

## Later ordering

Test deterministic single-agent tool hygiene before repair subagents:

```text
E3a controlled first-patch/repair
  -> E3b/F0 audit/restore/output hygiene
  -> F1 fresh isolated repair only if hygiene is insufficient
  -> F2 persistent context only if F1 works
```

Tool hygiene includes moving vulnerability audit out of the edit–compile loop, avoiding implicit restores and rebuilding `dotnet run` forms, and bounding/deduplicating irrelevant repeated warnings while preserving raw evidence outside model context.

Do not build a generic multi-agent framework, recursive subagents, dynamic routing, or a cheaper-worker arm prematurely.

## Evidence boundaries

- V3 calibrations are non-counting and excluded from future formal estimates.
- E1/E2/E2a are descriptive mechanism evidence, not causal language inference.
- E2 and E2a are separate ecologies and are not pooled.
- Unweighted command-cell ratios are not the frequency-weighted v3 effect.
- The mechanical exposure envelope is not a causal percentage explained.
- Aggregate input is total trajectory usage, not unique source memory.
- A generation error can create much larger later input through diagnostics and replay.
- `NU1900` line counts are repeated output, not independent defects.
- The current repository is too small to test context-window fit or a semantic-density crossover.
- Fresh-per-task v3 cannot test cross-task context pollution.
- No current result establishes a universal F#, C#, model, or harness ranking.

## Development agents versus benchmark candidates

Candidate agents must remain blind to `AGENTS.md`, `PLAN.md`, hypotheses, prior outcomes, treatment labels, gold states, and hidden evaluator cases. Preserve `--ignore-user-config`/`--ignore-rules` or the reviewed equivalent.

## Research invariants

- Match semantic tasks, starting states, evaluator, limits, and candidate authority within each treatment.
- Record every attempt; never silently replace an ambiguous or potentially billable request.
- Keep scientific-specification, runner, environment, model, effort, schedule, and attempt identities separate.
- Separate source exposure, model output, tool feedback, total input, direct tool time, orchestrator cost, worker cost, and end-to-end cost.
- Unsupported telemetry is null/unavailable, never zero.
- Preserve full raw tool output outside candidate context when a bounded feedback packet is used.

## Autonomous stopping rules

- The current task ends after E3a specification/review/freeze/CI; it may not execute the pilot or invoke a model.
- After two failures of one apparatus class, stop and report instead of adding another route or compatibility layer.
- Stop before changing candidate-visible semantics, model/prompt/task/evaluator, tool-feedback policy, harness memory/routing, or a frozen scientific condition without reviewed authorization.
- Prefer deterministic tool hygiene before multi-agent infrastructure.

## Validation

```text
python -m unittest discover -s tests -v
python scripts/alf.py doctor --strict
python scripts/alf.py validate
python scripts/alf.py matrix --agent scripted --output results/pilot
python scripts/alf.py audit <run-directory>
```
