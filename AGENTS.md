# Agent entry point

This file is the repository-level instruction entry point for maintainer coding agents.

## Start here

Before substantial work:

1. Read `PLAN.md`; it is the canonical checkpoint, ordering, and decision-gate document.
2. Read `docs/workstream-d-feasibility-design-2026-08-30.md`; it is the independently reviewed and approved design for the next milestone.
3. Read `docs/difficulty-v1-results-2026-08-30.md` and `docs/variance-v2-results-2026-08-29.md` before interpreting the pilot evidence.
4. Read `docs/protocol.md`, `docs/event-schema.md`, and `docs/environment.md` before changing isolation, telemetry, protocol, or run procedures.
5. Read `docs/research-gap.md` and the literature-review addendum before changing novelty or contribution claims.
6. Inspect the latest commit and CI status. Never launch paid/model experiments while `main` is red or before the relevant cell is independently reviewed and cleanly frozen.

When work changes status, ordering, assumptions, acceptance criteria, or the selected configuration family, update `PLAN.md` in the same change. Keep this file concise; put durable design detail in `docs/`.

## Current priority

Workstreams A–C are complete for the current pilot methodology. `variance-v2` established high stochastic/order variance on the short chain; `difficulty-v1` established that the reviewed eight-task chain is no longer fully saturated and exposed candidate-caused deterministic-representation drift.

D0 design review is closed **approved** with no remaining P0–P3 findings. D1 v1 was pushed directly to `main` at `965b44716470fc3f97cdd144aa0425594ceee8d9`; CI run `33308054052` passed on Linux/Windows, and v1 freezes plus manifest validation passed. Its first D2 attempt is an unresolved apparatus incident documented in `docs/workstream-d-v1-retirement-incident-2026-08-30.md`; v1 is retired and must not be retried, pooled, or synthesized. The schema-aware D1 v2 replacement was pushed at `eed5b4dc9657366822cd3833a990dfd569b921e9` and passed CI `33309932298` with clean freezes. Its calibration is closed after confirmed-too-easy M and a host OOM apparatus stop in L/C# (see `docs/workstream-d-v2-calibration-incident-2026-08-31.md`). The next task is independent review/validation of v3—not a model run:

1. independently review and fully model-free validate the v3 parent family, six-macroblock schedule, three child cells, and host-memory pins;
2. commit/push v3 directly to `main`, require green Linux/Windows CI, then freeze each child from the clean committed head and verify resolved manifests/hashes;
3. only then run non-counting configuration calibrations, including reverse-order confirmation before replacing a boundary configuration.

The v3 catalog settings are H `gpt-5.6-terra` medium, M `gpt-5.6-luna` high, and L
`gpt-5.6-luna` medium; runtime availability is deferred to calibration. No
v3 manifest is frozen and no further model call is authorized until review,
validation, CI, independent clean-freeze checks, and memory-headroom probes pass.

The first D-Language family deliberately uses only the canonical descriptive representation. Do not multiply the unstable representation treatment across model configurations. A later D-Representation family must use complete Williams superblocks and intention-to-treat as its primary estimand; candidate-caused drift is an outcome, not an automatic primary-analysis exclusion.

The formal D-Language schedule is staged but fully predeclared: execute macroblocks 1–4, then use only apparatus stability and saturation/impossibility criteria to decide whether to complete macroblocks 5–6. Never use the sign or magnitude of the F#–C# difference as the continuation rule.

No paid/model run is authorized until D1 implementation review, model-free validation, green CI, and clean child freezes are complete.

## Development agents versus benchmarked agents

This file guides agents **developing this repository**. Candidate agents being measured must not receive repository-level research instructions. The experimental launcher uses `--ignore-user-config` and `--ignore-rules`; preserve that separation unless a reviewed protocol explicitly introduces an instruction treatment.

## Research invariants

- Keep F# and C# task text, ordered changes, external behavior, evaluator, resource limits, and agent protocol matched.
- Start a fresh candidate-agent process/container per task while retaining only the changed candidate workspace.
- Never expose gold snapshots, evaluator cases, parent repositories, credentials, or unrelated host files to a candidate agent.
- Record every attempt, including candidate, provider, authentication, host, evaluator, timeout, protocol, accounting, and archive failures; never silently replace an attempt.
- Preserve raw JSON/JSONL and exact environment metadata outside Git as appropriate; commit curated redacted fixtures, definitions, hashes, and reports.
- Keep model, reasoning effort, CLI, image digest, toolchain, network policy, order, timestamps, tokens, timings, commands, diffs, and outcomes explicit.
- Treat language, configuration, order, task, time, and chain position as interacting factors rather than seeking a universal ranking.
- Increment the protocol/cell identifier after any change that could affect measured trajectories; never pool across changed cells without explicitly modeling the change.
- Candidate correctness failures are valid outcomes. Only preregistered pre-candidate infrastructure failures may be retried/excluded.
- Do not condition cost interpretation only on completed chains; retain terminal-stop and paired common-exposure-prefix outcomes.

## Validation commands

Install with `python -m pip install -e .`, then run:

```text
python -m unittest discover -s tests -v
python scripts/alf.py doctor --strict
python scripts/alf.py validate
python scripts/alf.py matrix --agent scripted --output results/pilot
python scripts/alf.py audit <run-directory>
```

For isolated Codex execution, build with `make docker-build`, smoke-test with `make docker-smoke`, and follow `README.md` plus `docs/environment.md`. Require usage for accepted command-adapter runs and never broaden Docker mounts or weaken the evaluator boundary.

## Evidence boundaries

- The historical 2026-08-26 pair is recovered and hash-preserved but fails the current audit schema; it remains excluded.
- `variance-v2` is a variance pilot on the two-task chain, not successor-chain evidence.
- `difficulty-v1` is one non-counting Williams row, not a language or representation estimate.
- The F# deterministic difficulty primary remains valid for correctness/time/usage but not for the pilot's per-protocol representation comparison because the candidate reintroduced descriptive aliases.
- No existing result supports an F# advantage, a deterministic-representation advantage, significance, or cross-cell pooling.
