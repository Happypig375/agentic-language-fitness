# Agent entry point

Read `PLAN.md` before substantial work. It is the canonical checkpoint and continuation order.

## Current checkpoint

Workstreams E1, E2, and E2a are complete and accepted within their stated evidence boundaries. E2a completed 1,020 model-free samples in five paired rounds, with no candidate agent, Codex process, authentication, model endpoint, or paid request. See `docs/workstream-e1-e2-synthesis-review-2026-09-04.md`, `docs/workstream-e2a-disposition-2026-09-04.md`, and `reports/workstream-e2a-host-aligned-v1/report.md`.

E2a strengthens the coupled repair/invocation-count plus compiler/audit amplification hypothesis. Its mechanical invocation-count × duration envelope is descriptive and is never subtracted from agent cost or called mediation. E2 remains a separate offline ecology. Near-parity test, direct-DLL, and most built-program run behavior remain. No result establishes a causal or universal F#/C# ranking.

V4–V13 are apparatus-development history. Do not create v14. Preserve immutable E1/E2/E2a artifacts; corrections belong in addenda or new reports.

## Next separately reviewed step

The next step is an E3 scientific specification. It must receive independent review, clean freeze, and exact-commit CI before any model call. No model or paid run is authorized without a separate maintainer/user decision. Do not begin E3 automatically, and do not build routing/delegation infrastructure prematurely.

## Development agents versus benchmark candidates

Candidate agents must remain blind to `AGENTS.md`, `PLAN.md`, hypotheses, prior outcomes, treatment labels, gold states, and hidden evaluator cases. Preserve `--ignore-user-config`/`--ignore-rules` or the reviewed equivalent.

## Research invariants

- Match semantic tasks, starting states, evaluator, limits, and candidate authority within each treatment.
- Record every attempt; never silently replace an ambiguous or potentially billable request.
- Keep scientific-specification, runner, environment, model, effort, schedule, and attempt identities separate.
- Separate source exposure, model output, tool feedback, total input, toolchain time, orchestrator cost, worker cost, and end-to-end cost.
- Unsupported telemetry is null/unavailable, never zero.

## Autonomous stopping rules

- The current bounded task ends after E2a publication.
- Do not invoke a model or continue into E3 without separate reviewed authorization.
- After two failures of one apparatus class, stop and report instead of adding another compatibility or recovery layer.
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
