# Agent entry point

This file is the repository-level instruction entry point for maintainer coding agents.

## Start here

Before substantial work:

1. Read `PLAN.md`. It is the canonical current checkpoint, ordered continuation plan, decision gates, and definition of the next milestone.
2. Read `docs/preliminary-results-2026-08-26.md` before referring to the historical paired run.
3. Read `docs/protocol.md`, `docs/event-schema.md`, and `docs/environment.md` before changing the harness, isolation, telemetry, or run procedure.
4. Read `docs/research-gap.md` and the literature-review addendum before changing novelty or contribution claims.
5. Inspect the latest commit and CI status. Do not launch paid/model experiments while `main` is red.

When work changes project status, ordering, assumptions, or acceptance criteria, update `PLAN.md` in the same change. Keep this file concise; route durable detail to the appropriate document.

## Current priority

`variance-v2` is complete and documented in `docs/variance-v2-results-2026-08-29.md`; its formal observations are a variance pilot, not evidence of a language advantage. Workstream C's matched eight-task design review and C2 implementation/validation are complete. C2 commit `4e58677e0bfff18c2104298ad35fc4e801bbd052` has green GitHub Actions run `33258119571` (Linux 2m20s, Windows 2m23s; Node 20 deprecation warnings only). Follow the next gate in `PLAN.md`: design, implement, and independently review the C3 representation treatment, then define and freeze a new protocol cell. Keep the historical pair and retired v1 attempt excluded, and do not launch another paid/model run while the remaining gates are blocked.

The Workstream C design in
`docs/workstream-c-benchmark-design-2026-08-29.md` is independently reviewed;
its material legacy-behavior clarification was independently reviewed and
approved with no P1/P2 findings. Retained C#/F# Task 002 parameter casing
differs, but the candidate-visible suffix-free exact strings are symmetric;
Task 001/002 remain unchanged. The language-equivalence/error review gate is
closed. C2 implementation and model-free validation are complete and approved.
C3 representation treatment is the immediate next step; its design is now
preregistered and independently approved with no remaining P1/P2 findings;
implementation and implementation review remain pending. The new protocol
freeze, difficulty pilot, and paid/model runs remain blocked until
their gates are complete. Main CI for C2 is green as recorded above.

The historical raw artifacts are recovered and hash-preserved, but fail the current audit schema; see `docs/historical-run-recovery-2026-08-29.md`. Do not use their legacy Markdown token totals as validated data.

## Development agents versus benchmarked agents

This file guides agents **developing this repository**. Candidate agents being measured by the benchmark must not receive repository-level research instructions. The experimental Codex launch deliberately uses `--ignore-user-config` and `--ignore-rules`; preserve that separation unless the protocol explicitly introduces an instruction treatment.

## Research invariants

- Keep F# and C# task text, ordered changes, external behavior, evaluator, resource limits, and agent protocol matched.
- Start a fresh candidate-agent process/container per task while retaining only the changed candidate workspace.
- Never expose gold snapshots, evaluator cases, parent repositories, credentials, or unrelated host files to a candidate agent.
- Record every attempt, including provider, host, authentication, evaluator, timeout, protocol, accounting, and agent failures; never silently replace failed attempts.
- Preserve raw JSON/JSONL and exact environment metadata outside Git as appropriate; commit curated redacted fixtures, manifests, hashes, and summaries.
- Keep model, CLI, image digest, toolchain, network policy, run order, timestamps, tokens, timings, commands, diffs, and outcomes explicit.
- Treat language, model, scaffold, order, task, time, and chain position as possible interacting factors rather than seeking a universal ranking.
- Increment the protocol/cell identifier after any change that could affect measured trajectories; do not pool across changed cells without modeling the change.

## Validation commands

Install first with `python -m pip install -e .`, then run:

```text
python -m unittest discover -s tests -v
python scripts/alf.py doctor --strict
python scripts/alf.py validate
python scripts/alf.py matrix --agent scripted --output results/pilot
python scripts/alf.py audit <run-directory>
```

For the isolated Codex path, build with `make docker-build`, smoke-test with `make docker-smoke`, and follow `README.md` plus `docs/environment.md`. Require usage for accepted command-adapter runs and do not broaden Docker mounts or weaken the evaluator boundary.

## Historical exploratory result

The 2026-08-26 pair is summarized in `docs/preliminary-results-2026-08-26.md`. Its exact raw directory is recovered at `results/codex-docker-dotnet10-gpt-5.6-luna-seed20260826-rerun3/`, but the legacy artifacts fail `alf audit`; the pair remains an unaudited smoke-test observation excluded from formal aggregates, variance estimation, and power analysis.
