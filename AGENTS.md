# Agent entry point

This file is the repository-level instruction entry point for maintainer coding agents.

## Start here

Before substantial work:

1. Read `PLAN.md`. It is the canonical current checkpoint, ordered continuation plan, decision gates, and definition of the next milestone.
2. Read `docs/preliminary-results-2026-08-26.md` before interpreting or extending the first paired run.
3. Read `docs/protocol.md` and `docs/environment.md` before changing the harness, isolation, telemetry, or run procedure.
4. Read `docs/research-gap.md` and the literature-review addendum before changing novelty or contribution claims.
5. Inspect the latest commit and CI status. Do not launch paid/model experiments while `main` is red.

When work changes project status, ordering, assumptions, or acceptance criteria, update `PLAN.md` in the same change. Keep this file concise; route durable detail to the appropriate document.

## Current priority

Cross-platform CI is green at commit `41252deb4ac84df36f5887a23bc198d91bd24fbd`. Stay in Phase 1 and begin with the usage/event-accounting audit in `PLAN.md`, then freeze result provenance before running the 10 counterbalanced paired blocks. Do not infer an F# advantage from the single 2-task pair, and do not jump to broad repository expansion before the measurement and variance gates are met.

## Development agents versus benchmarked agents

This file guides agents **developing this repository**. Candidate agents being measured by the benchmark must not receive repository-level research instructions. The experimental Codex launch deliberately uses `--ignore-user-config` and `--ignore-rules`; preserve that separation unless the protocol explicitly introduces an instruction treatment.

## Research invariants

- Keep F# and C# task text, ordered changes, external behavior, evaluator, resource limits, and agent protocol matched.
- Start a fresh candidate-agent process/container per task while retaining only the changed candidate workspace.
- Never expose gold snapshots, evaluator cases, parent repositories, credentials, or unrelated host files to a candidate agent.
- Record every attempt, including provider, host, authentication, evaluator, timeout, and agent failures; never silently replace failed attempts.
- Preserve raw JSON/JSONL and exact environment metadata outside Git as appropriate; commit only curated, redacted summaries, manifests, and hashes.
- Keep model, CLI, image digest, toolchain, network policy, run order, timestamps, tokens, timings, commands, diffs, and outcomes explicit.
- Treat language, model, scaffold, order, task, and chain position as possible interacting factors rather than seeking a universal ranking.

## Validation commands

Install first with `python -m pip install -e .`, then run:

```text
python -m unittest discover -s tests -v
python scripts/alf.py doctor --strict
python scripts/alf.py validate
python scripts/alf.py matrix --agent scripted --output results/pilot
```

For the isolated Codex path, build with `make docker-build`, smoke-test with `make docker-smoke`, and follow `README.md` plus `docs/environment.md`. Do not broaden Docker mounts or weaken the evaluator boundary.

## Current accepted result

The accepted preliminary run is summarized in `docs/preliminary-results-2026-08-26.md`. Its raw local directory is `results/codex-docker-dotnet10-gpt-5.6-luna-seed20260826-rerun3/`. Earlier runs listed in the summary and prior `AGENTS.md` history are infrastructure diagnostics, not substitutable treatment observations.
