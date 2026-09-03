# Agent entry point

Read `PLAN.md` before substantial work. It is the canonical checkpoint and ordering document.

## Current checkpoint

Workstreams A–C are complete. Workstream D v3 completed ten audited non-counting calibrations: H (`gpt-5.6-terra` medium), M (`gpt-5.6-luna` high), and L (`gpt-5.6-luna` medium) all completed the eight-task chain; M/L remained too easy in reverse order. The frozen v3 stop condition was met, so formal v3 macroblocks are permanently blocked.

Exploratorily, F# used more total input tokens and agent time in all five F#/C# pairs, with geometric-mean ratios near 1.38. These totals are ecological trajectory costs, not direct measurements of source compactness or model memory.

The current candidate harness starts a fresh process/conversation per task. It can show within-task repair amplification, but it cannot show compile/tool history accumulating across the full eight-task chain. Long-horizon context pollution and repair delegation require separate persistent-context/harness treatments.

V4–V13 remain apparatus-development history. Do not create v14. Reuse the reviewed runner/environment identity unless a separately justified candidate-visible change is required.

## Next bounded task

Independently review:

```text
docs/post-v3-interpretation-and-workstream-e-design-2026-09-03.md
```

The design now makes causal attribution precede cost replication. Review:

- unique source context versus aggregate input/replayed cached history;
- first-pass generation and compiler diagnostic classification;
- build/test repair-loop attribution;
- model familiarity and pre-edit exploration;
- ecological project/toolchain obligations;
- fresh versus persistent context;
- inline versus isolated repair workers;
- total-system versus orchestrator-only cost;
- controlled use of gold predecessor snapshots;
- anti-overengineering and stop rules.

Close all P1/P2 findings before implementation. No paid/model run is authorized by the draft.

## After design approval

Proceed in this order:

1. **Archive-only forensics:** classify existing v3 command events, builds, diagnostics, tests, edits, and repair cycles; generate task-level/cumulative reports without a model call.
2. **Model-free baselines:** repeatedly build/evaluate every F#/C# stage and record source/token/project obligations.
3. **Bounded mechanism pilot:** only under a new reviewed specification, compare comprehension/localization, one-shot patching, and monolithic full repair from matched gold predecessor snapshots.
4. **Causal decision:** choose familiarity, repair, toolchain, context-scale, or harness-routing follow-up from the observed signatures.
5. **Routing experiment when justified:** compare fresh/persistent orchestrator memory and inline/delegated repair with explicit per-agent accounting.
6. **Registered cost replication:** follow only after the endpoint can be decomposed and interpreted.
7. **Medium-repository context study:** test the original semantic-density hypothesis only when real retrieval/compaction pressure exists.

Do not build a generic multi-agent framework. A routing prompt alone is not a controlled treatment; any routing study must enforce separate contexts and record orchestrator and worker usage separately.

## Evidence boundaries

- V3 calibrations are non-counting and excluded from future formal estimates.
- Five same-direction pairs are hypothesis-generating, not statistically confirmatory.
- Aggregate input tokens are total model input processed over a trajectory, not unique source tokens.
- A syntax/type error can inflate later input through diagnostics and repeated history; it is not confined to output tokens.
- Zero recorded file reads currently means unsupported telemetry, not literal absence of reading.
- The small final repositories are similarly sized and do not test context-window fit.
- Current fresh-per-task runs do not test cross-task context degradation.
- No result establishes an F#, C#, model, or harness advantage universally.

## Development agents versus benchmark candidates

These instructions guide agents maintaining the research repository. Candidate agents being measured must remain blind to `AGENTS.md`, `PLAN.md`, hypotheses, prior outcomes, and treatment labels. Preserve `--ignore-user-config`/`--ignore-rules` or the reviewed equivalent.

## Research invariants

- Keep F# and C# task text, ordered changes, evaluator, limits, and candidate protocol matched.
- Start a fresh candidate process/container per task in the ecological baseline; persistent-context conditions require separate reviewed specifications.
- Never expose gold data, evaluator cases, research instructions, credentials, parent repositories, or unrelated host files.
- Record every attempt; never silently replace an ambiguous or billable request.
- Keep model, effort, CLI, image, environment, network policy, order, time, usage, diagnostics, diffs, and outcomes explicit.
- Do not pool changed scientific specifications or candidate-visible environments.
- Candidate correctness failures remain outcomes; only preregistered pre-candidate apparatus failures may be retried/excluded.
- Separate static/source exposure, model output, tool feedback, total model input, toolchain time, orchestrator cost, worker cost, and end-to-end cost.
- Unsupported telemetry is null/unavailable, never a fabricated zero.

## Autonomous stopping rules

- Every autonomous task must name one bounded artifact/gate and its acceptance criterion.
- The next task ends after independent review and closure of design findings; it does not proceed automatically into implementation or model runs.
- After two failures of the same apparatus class, stop and report instead of adding another compatibility or recovery layer.
- Stop before changing candidate-visible semantics, model/prompt/task/evaluator, scientific estimands, harness memory/routing, or another frozen condition without approved design.
- Prefer deterministic archive analysis and model-free evidence before constructing new agent infrastructure.

## Validation

```text
python -m unittest discover -s tests -v
python scripts/alf.py doctor --strict
python scripts/alf.py validate
python scripts/alf.py matrix --agent scripted --output results/pilot
python scripts/alf.py audit <run-directory>
```
