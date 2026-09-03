# Agent entry point

Read `PLAN.md` before substantial work. It is the canonical checkpoint and ordering document.

## Current checkpoint

Workstreams A–C are complete. Workstream D v3 completed ten audited non-counting calibrations: H (`gpt-5.6-terra` medium), M (`gpt-5.6-luna` high), and L (`gpt-5.6-luna` medium) all completed the eight-task chain; M/L remained too easy in reverse order. The frozen v3 stop condition was met, so formal v3 macroblocks are permanently blocked.

Exploratorily, F# used more total input tokens and agent time in all five F#/C# pairs, with geometric-mean ratios near 1.38. These totals are ecological trajectory costs, not direct measurements of source compactness or model memory.

Interpret the current result as a possible **small-repository ecological overhead** under the tested models/scaffold: the project was only about two thousand proxy source tokens, correctness was saturated, and repository capacity was not limiting. In the conceptual decomposition `C_L(S) = A_L + B_L S`, v3 shows a local small-scale gap consistent with higher fixed overhead; one finite scale identifies neither `A` nor the context-scale slope `B`. It neither establishes nor rules out a later F#/C# crossover under genuine retrieval, persistent-history, or compaction pressure.

The current candidate harness starts a fresh process/conversation per task. It can show within-task repair amplification, but it cannot show compile/tool history accumulating across the full eight-task chain. Long-horizon context pollution and repair delegation require separate persistent-context/harness treatments.

V4–V13 remain apparatus-development history. Do not create v14. Reuse the reviewed runner/environment identity unless a separately justified candidate-visible change is required.

Workstream E1 archive-only attribution is complete and independently approved.
The analyzer reconciled all ten runs, 80 tasks, 435 completed commands, all 11
observed event shapes, and all 12 observed command-equivalence classes. Analyzer
commit `82c8c6bdc429f0819a718ce6c4d567fe0a30e88a` passed exact-commit
Linux/Windows CI. The transcript-free report hash is
`644273ac0f25a32138d50d919ff15677b6ed9639a23198e0c719d154da94901d`.
The report publication commit is accepted only after its own exact-commit
Linux/Windows CI is green.

E1 routes attention toward compiler-repair and ecological toolchain pathways:
all 25 observable failed candidate operations were builds, with 19 conservative
repair cycles; F# had the larger failed-build/repair burden in every
configuration, all five project-file changes, and about twice the evaluator
time. This is descriptive hypothesis routing, not a causal or universal
language claim. See `reports/workstream-e-v3/forensic-report.md` and
`docs/workstream-e1-v3-forensic-disposition-2026-09-03.md`.

## Next bounded task

After the E1 report publication commit passes exact-commit CI, execute **E2
model-free language/toolchain baselines** under:

```text
docs/post-v3-interpretation-and-workstream-e-design-2026-09-03.md
```

E2 is offline and model-free: do not invoke the remote runner, proxy route, or
any model endpoint. Materialize and hash the baseline plus eight cumulative gold
states for each language (18 states total). Run exactly five preregistered paired
rounds in the hashed interleaved order. Each state/round gets a fresh workspace
without `bin`/`obj` followed by one immediate same-workspace repeat; call these
fresh-workspace and repeat-workspace, never machine-cold/warm.

Use only the fixed restore, Release no-incremental/no-restore build, and no-build
evaluator commands in the approved design. Keep package cache and network policy
fixed. Record the specified timing/output/warning measures, source/token proxies,
project-file changes, diffs, and task obligations. Every state/repetition must
pass its cumulative evaluator and identity checks; there is no adaptive extension
or selective silent retry.

E2 closes only after its deterministic report passes independent implementation
review and exact-commit Linux/Windows CI. Stop before E3 or any paid/model call.

## After E2

Proceed in this order:

1. **Bounded mechanism pilot:** only under a new reviewed specification, compare comprehension/localization, one-shot patching, and monolithic full repair from matched gold predecessor snapshots.
2. **Causal decision:** choose familiarity, repair, toolchain, context-scale, or harness-routing follow-up from the observed signatures.
3. **Routing experiment when justified:** compare fresh/persistent orchestrator memory and inline/delegated repair with explicit per-agent accounting.
4. **Registered small-repository cost replication:** estimate the local cost gap at the frozen small-repository scale under equal successful task exposure; do not describe it as an identified intercept or context-density test.
5. **Multi-scale context study:** test the original semantic-density hypothesis only across preregistered repository/working-set sizes that produce real retrieval or compaction pressure.

Do not build a generic multi-agent framework. A routing prompt alone is not a controlled treatment; any routing study must enforce separate contexts and record orchestrator and worker usage separately.

## Evidence boundaries

- V3 calibrations are non-counting and excluded from future formal estimates.
- Five same-direction pairs are hypothesis-generating, not statistically confirmatory.
- Aggregate input tokens are total model input processed over a trajectory, not unique source tokens.
- A syntax/type error can inflate later input through diagnostics and repeated history; it is not confined to output tokens.
- Zero recorded file reads currently means unsupported telemetry, not literal absence of reading; E1 may classify bounded command evidence but cannot recover unique source exposure.
- The small final repositories are similarly sized and do not test context-window fit.
- Easy/all-success tasks permit equal-exposure cost comparison; they do not establish why one language costs more.
- The current signal is a local small-scale ecological gap, not an identified mathematical intercept or language-by-scale slope.
- Any crossover must be observed or tightly bounded in a registered scale experiment; never extrapolate it from source concision.
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
- Separate local small-scale cost estimates from language-by-scale estimates; neither substitutes for the other, and one finite scale does not identify an intercept.
- Unsupported telemetry is null/unavailable, never a fabricated zero.

## Autonomous stopping rules

- Every autonomous task must name one bounded artifact/gate and its acceptance criterion.
- The next task ends after E2 reporting, independent implementation review, and exact-commit CI; it does not proceed automatically into E3 or model runs.
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
