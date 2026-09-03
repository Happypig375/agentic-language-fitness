# Agent entry point

Read `PLAN.md` before substantial work. It is the canonical checkpoint and ordering document.

## Current checkpoint

Workstreams A–C are complete. Workstream D v3 completed ten audited non-counting calibrations: H (`gpt-5.6-terra` medium), M (`gpt-5.6-luna` high), and L (`gpt-5.6-luna` medium) all completed the eight-task chain; M/L remained too easy in reverse order. The frozen v3 stop condition was met, so formal v3 macroblocks are permanently blocked.

The calibration is not confirmatory language evidence. Exploratorily, however, F# used more input tokens and agent time in all five F#/C# pairs, with geometric-mean ratios near 1.38. The next scientific step is therefore a reviewed **successful-chain cost replication**, not another attempt to force task failures.

V4–V13 remain apparatus-development history. Do not create v14. Reuse the reviewed runner/environment identity unless a separately justified candidate-visible change is required.

## Next bounded task

Independently review:

```text
docs/post-v3-interpretation-and-workstream-e-design-2026-09-03.md
```

Review the significance boundary, cost estimands, 0.90–1.10 provisional equivalence margin, six-pair-per-configuration schedule, blinded precision extension, measurement gaps, ecological-versus-controlled language interpretation, and mechanism-study order. Close all P1/P2 findings before implementation.

No model or paid run is authorized by the draft.

## After design approval

Only then:

1. add task-level/cumulative report output;
2. make unsupported file-read/revisit telemetry explicitly unavailable unless real-event coverage is validated;
3. add model-free F#/C# build/evaluator baselines and per-stage source metrics;
4. audit language-specific obligations in Tasks 007–008;
5. implement and independently review the new `successful-maintenance-cost-v1` scientific specification;
6. obtain green exact-commit CI and a clean freeze;
7. run the registered paired schedule.

Scientific-specification changes are not runner versions. Do not modify remote transport, authentication, Docker routing, or environment machinery merely to implement analysis/reporting changes.

## Evidence boundaries

- V3 calibrations are non-counting and excluded from future formal estimates.
- All-success calibration means correctness cannot distinguish H/M/L, not that language cost is equivalent.
- Five same-direction pairs are hypothesis-generating, not statistically confirmatory.
- The old historical Luna pair, `variance-v2`, `difficulty-v1`, v3 calibration, and future Workstream E data must remain separate.
- Zero recorded file reads currently means unsupported telemetry, not literal absence of reading.
- No result yet establishes an F# advantage, C# advantage, universal ranking, or significance claim.

## Development agents versus benchmark candidates

These instructions guide agents maintaining the research repository. Candidate agents being measured must remain blind to `AGENTS.md`, `PLAN.md`, hypotheses, prior outcomes, and treatment labels. Preserve `--ignore-user-config`/`--ignore-rules` or the reviewed equivalent.

## Invariants

- Keep F# and C# task text, ordered changes, evaluator, limits, and candidate protocol matched.
- Start a fresh candidate process/container per task while retaining only the candidate workspace state.
- Never expose gold data, evaluator cases, research instructions, credentials, parent repositories, or unrelated host files.
- Record every attempt; never silently replace an ambiguous or billable request.
- Keep model, effort, CLI, image, environment, network policy, order, time, usage, diffs, and outcomes explicit.
- Do not pool changed scientific specifications or candidate-visible environments.
- Candidate correctness failures remain outcomes; only preregistered pre-candidate apparatus failures may be retried/excluded.
- Separate model-token cost, toolchain/evaluator cost, and end-to-end wall time.

## Autonomous stopping rules

- Every autonomous task must name one bounded artifact/gate and its acceptance criterion.
- After two failures of the same apparatus class, stop and report instead of adding another compatibility or recovery layer.
- Stop before changing candidate-visible semantics, model/prompt/task/evaluator, scientific estimands, or another frozen condition without approved design.
- Prefer simplifying a broken route over preserving parallel historical runtime paths; Git history is the audit trail.

## Validation

```text
python -m unittest discover -s tests -v
python scripts/alf.py doctor --strict
python scripts/alf.py validate
python scripts/alf.py matrix --agent scripted --output results/pilot
python scripts/alf.py audit <run-directory>
```
