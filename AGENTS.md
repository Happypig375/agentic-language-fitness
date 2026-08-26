# Agent context

## Research scope

The study asks whether programming-language choice changes the cumulative computation, correctness, and repair burden of coding agents maintaining semantically matched software through inherited changes. The controlled pilot compares F# and C# on .NET 10. This is not a claim that F# is better, that sequential-maintenance benchmarking is novel, or that the preliminary run estimates a causal effect.

## Benchmark invariants

- Keep the F# and C# task sequence, behavioral oracle, baseline semantics, and agent protocol matched.
- Start a fresh agent process per task while retaining the changed candidate workspace.
- Do not expose gold snapshots, evaluator cases, parent repositories, credentials, or unrelated host files to an agent.
- Record model, agent, toolchain, container image, run order, seed, tokens, timings, commands, diffs, and evaluation outcomes.
- Treat artifacts as research data: preserve raw JSON/JSONL, redact credentials, and never commit secrets or reusable tokens.

## Reproduction environment

The validated host toolchain is .NET SDK `10.0.302`, Python `3.11.15`, and Git `2.46.2.windows.1`; the agent is Codex CLI `0.149.1`, model `gpt-5.6-luna`, using image `alf-codex:0.149.1` (image ID recorded in the report). Run `python scripts/alf.py doctor --strict` and `python scripts/alf.py validate` before experiments. Build isolation with `make docker-build`, smoke-test with `make docker-smoke`, then use `scripts/codex-docker.py` through the `command` adapter as documented in README and `docs/environment.md`.

Docker mounts only the candidate workspace read-write and uses a temporary read-only auth projection; bridge egress remains enabled. Access tokens can still be visible inside the trusted container, and Docker/daemon and task-prompt trust remain residual risks. Do not broaden mounts or bypass the evaluator boundary.

## Results and validation

The successful paired run is `results/codex-docker-dotnet10-gpt-5.6-luna-seed20260826-rerun3/`; its tracked summary is `docs/preliminary-results-2026-08-26.md`. Earlier directories `codex-docker-dotnet10-gpt-5.6-luna-seed20260826`, `codex-docker-dotnet10-gpt-5.6-luna-seed20260826-rerun1`, `codex-docker-dotnet10-gpt-5.6-luna-seed20260826-rerun2`, `codex-dotnet10-gpt-5.6-luna-seed20260826`, `codex-dotnet10-gpt-5.6-luna-seed20260826-rerun1`, and scripted runs are infrastructure/harness diagnostics, not valid paired treatment data.

Use `$env:PYTHONPATH='src'; python -m unittest discover -s tests -v` in PowerShell (or `PYTHONPATH=src python -m unittest discover -s tests -v` in a POSIX shell) for the full harness suite, and `python scripts/alf.py validate` for benchmark validation. Keep generated build outputs and ephemeral workspaces out of source control when possible; retain only intentionally curated result artifacts and reports.
