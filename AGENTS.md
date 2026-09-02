# Agent entry point

Read `PLAN.md` before substantial work. It is the canonical checkpoint and ordering document. Read the approved Workstream D design and relevant protocol/environment/research documents before changing those areas.

## Current checkpoint

Workstreams A–C and the Workstream D scientific design are complete. V3 is the current scientific configuration family (H=`gpt-5.6-terra` medium, M=`gpt-5.6-luna` high, L=`gpt-5.6-luna` medium). Its ten-run non-counting calibration is complete: H is saturated; M/L are too easy in both primary and reverse order. No language conclusion is available.

V4–V13 were apparatus-development attempts, not scientific families. Do not create v14. The replacement remote runner passed exact-commit CI, route shakedown, clean freezes, and calibration; formal macroblocks 1–6 are blocked pending a reviewed successor design.

## Active gates

1. Preserve the completed runner, route, freeze, and calibration evidence.
2. Stop pending an explicitly reviewed successor scientific design/new specification; no paid/model run and no v14.

Pre-candidate infrastructure failures are retained as attempts and may be fixed and retried under the same scientific specification. Change the scientific specification only when model, prompt, task, evaluator, candidate-visible semantics, or analysis changes. Keep candidate agents separate from these maintainer instructions.

See `docs/apparatus-versioning-postmortem-2026-09-02.md` for retired apparatus history and `docs/remote-execution.md` for transport design.

## Autonomous stopping rules

These rules specifically prevent a broad `/goal` or day-long agent task from turning one apparatus problem into another version cascade.

- Every autonomous task must name one bounded artifact/gate, its acceptance criterion, and the conditions under which the agent must stop and report instead of continuing.
- Do not interpret "make progress today", "finish this", or a similar open-ended goal as permission to redesign scientific protocol, runner architecture, transport, authentication, or environment indefinitely.
- A pre-candidate infrastructure/transport/authentication failure is an apparatus failure. It does **not** create a new scientific version.
- After **two failed attempts of the same failure class**, stop and return: the observed evidence/logs, the likely cause, what was already tried, and the smallest next options. Do not add another compatibility layer, alternate route, protocol version, or recovery subsystem on your own.
- Stop immediately if the next step would change candidate-visible semantics, the scientific specification, the model/prompt/task/evaluator, or another frozen experimental condition.
- Prefer simplifying or replacing a broken apparatus path over preserving multiple historical runtime routes. Git history is the audit trail.
- Do not retry an ambiguous potentially billable candidate/model request automatically.

## Invariants

- Keep F# and C# task text, ordered changes, evaluation, limits, and agent protocol matched.
- Start a fresh candidate process/container per task and never expose gold data or credentials.
- Record every attempt and preserve raw JSONL/metadata outside Git where appropriate.
- Keep model, CLI, image, toolchain, network policy, order, timing, usage, and outcomes explicit.
- Do not pool observations across changed scientific specs or candidate-visible runner environments.
- No paid/model run while a required gate is red or the cell is not cleanly frozen.

## Validation

```text
python -m unittest discover -s tests -v
python scripts/alf.py doctor --strict
python scripts/alf.py validate
python scripts/alf.py matrix --agent scripted --output results/pilot
python scripts/alf.py audit <run-directory>
```
