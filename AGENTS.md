# Agent entry point

Read `PLAN.md` before substantial work. It is the canonical checkpoint and continuation order.

## Current checkpoint

Workstreams E1, E2, and E2a are complete and accepted within their stated evidence boundaries. E2a authenticated 435 v3 command events and 258 benchmark `dotnet` operations, then ran 1,020 model-free samples in five paired rounds on the v3 remote host/profile.

The joint evidence shows two compounding effects:

- F# trajectories invoked more benchmark tool operations: 163 versus 95 for C# across the retained v3 runs;
- restore/build-capable F# operations were slower, with a major vulnerability-audit component and a remaining no-restore compiler/toolchain gap after audit was disabled.

The v3/E2a proxy allowed model traffic but blocked NuGet source reachability while vulnerability audit remained enabled and homes/caches were fresh. Treat this as **legacy constrained-network audit-on**, not a general default developer ecology. The authenticated v3 streams contained 197 repeated F# `NU1900` lines and zero C# lines.

Pure tests and direct-DLL execution were near parity. The mechanical invocation-count × duration envelope is large relative to the observed wall-time gap, but it is descriptive, not mediation, and is never subtracted from agent cost. Model-token differences still require extra calls, diagnostics, feedback, and replay.

The 23-versus-2 failed-build headline also combines source-code failures with dependency/restore failures. Future work must classify them separately. In controlled first-patch measurement, pre-restore and baseline preflight outside candidate interaction, then build with `--no-restore`.

Read:

```text
docs/workstream-e2a-review-and-successor-revision-2026-09-05.md
docs/workstream-e2a-disposition-2026-09-04.md
reports/workstream-e2a-host-aligned-v1/report.md
```

V4–V13 are apparatus-development history. Do not create v14. Preserve immutable E1/E2/E2a evidence; corrections belong in addenda or new reports.

## Next bounded task

Specify and independently review **E3a: controlled shared-prefix first-patch and bounded repair**. Produce the scientific specification, deterministic fixtures/identities, clean freeze, and exact-commit CI only. Do not invoke a model or execute the pilot without a separate maintainer/user decision.

E3a must:

1. use matched canonical gold predecessors and a minimal simple/type/multi-file task set;
2. use one frozen model/scaffold configuration, provisionally Luna high because archived first-build outcomes were nondegenerate and E2a left a material unresolved agent-time gap;
3. give every trajectory one common first-patch phase without build/test feedback;
4. have the controller preflight/restore the predecessor with `NuGetAudit=false`, apply the patch once, build with `--no-restore`, and use a direct/no-build evaluator;
5. classify source syntax/type/API/project failures separately from dependency/restore/audit/environment failures;
6. let failed first patches continue only through a frozen repair budget, while successful first patches stop;
7. demonstrate same-context continuation before calling the repair condition monolithic; otherwise label it fresh-context repair;
8. record usage, patch identity, diagnostics, candidate-visible feedback, and controller tool time separately for every model round;
9. treat localization as auxiliary or conditional rather than another co-primary arm;
10. remain non-confirmatory and stop after its frozen sample.

Candidates may inspect allowed source but may not choose arbitrary build/run/test commands in this controlled mechanism treatment. Free tool choice is a separately named ecological treatment.

## Later ordering

Test deterministic single-agent tool policy before repair subagents:

```text
E3a controlled shared-prefix first-patch/repair
  -> E3b/F0 intended ecology versus hygienic tool policy
  -> F1 fresh isolated repair only if hygiene is insufficient
  -> F2 persistent context only if F1 works
```

Tool hygiene includes moving vulnerability audit out of the edit–compile loop, avoiding implicit restores and rebuilding `dotnet run` forms, and bounding/deduplicating irrelevant repeated warnings while preserving raw evidence outside model context.

The ecological comparator must be explicitly intended and reproducible—preferably online audit-reachable with cache behavior verified. Do not silently reuse the legacy blocked-source audit-on condition as “default”; it may remain a stress stratum.

Do not build a generic multi-agent framework, recursive subagents, dynamic routing, or a cheaper-worker arm prematurely.

## Evidence boundaries

- V3 calibrations are non-counting and excluded from future formal estimates.
- E1/E2/E2a are descriptive mechanism evidence, not causal language inference.
- E2 and E2a are separate ecologies and are not pooled.
- V3/E2a audit-on is a constrained-network stress ecology, not a universal default.
- Unweighted command-cell ratios are not the frequency-weighted v3 effect.
- The mechanical exposure envelope is not a causal percentage explained.
- Failed builds include dependency/environment failures as well as source failures.
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
- Never pool controlled offline/hygienic, online audit-reachable, legacy blocked-source, or delegated-agent strata.

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
