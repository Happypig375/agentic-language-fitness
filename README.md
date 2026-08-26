# Agentic Language Fitness

A reproducible pilot for measuring how programming-language choice changes the **lifetime computational cost and reliability of coding agents**.

The project does not assume that F# is better than C#, Python, Rust, or any other language. It tests a narrower causal question:

> When semantically equivalent software is represented in different programming languages, how much agent computation is required to correctly understand, change, verify, and maintain it over a sequence of inherited changes?

The first controlled comparison is **F# versus C# on .NET 8**. Sharing the runtime, standard library, package ecosystem, build system, and external behavior removes many confounds that affect ordinary multilingual benchmarks.

## Research gap

Existing work separately studies language-dependent token cost on small programming tasks, multilingual repository issue resolution, context retrieval, chained maintenance, low-resource languages, and token-efficient source transformations. As of the literature search dated **2026-08-26**, we found no benchmark that combines all of the following:

1. semantically matched repositories in different languages;
2. a shared runtime and external test oracle;
3. an inherited sequence of maintenance changes;
4. a fresh agent context for each change;
5. complete trajectory, context, repair, and correctness measurements.

See [the literature review](docs/literature-review.md) and [gap statement](docs/research-gap.md). The novelty claim is deliberately scoped and falsifiable rather than “which language is best.”

## What is executable now

The repository contains a two-step pilot benchmark with behaviorally equivalent F# and C# implementations of a line-oriented JSON order-processing service.

```text
baseline -> 001-priority -> 002-overdue
```

The harness:

- creates an isolated workspace from the language baseline;
- starts a fresh agent process for every task while retaining the changed codebase;
- builds with the .NET SDK;
- evaluates cumulative hidden behavioral cases;
- records source metrics, git diffs, process durations, tool/command counts, and token usage when exposed by the agent;
- writes machine-readable JSON and JSONL artifacts.

Three adapters are included:

- `scripted`: applies checked-in gold snapshots to validate the harness without an LLM;
- `codex`: runs a fresh non-interactive `codex exec --json --ephemeral` process per task;
- `command`: invokes any external agent command and optionally reads a standard usage sidecar.

## Quick start

Requirements: Python 3.11+, Git, and .NET SDK 8.x.

```bash
python scripts/alf.py doctor --strict
python scripts/alf.py validate
python scripts/alf.py matrix --agent scripted --output results/pilot
python scripts/alf.py summarize results/pilot

# Optional editable installation exposes the shorter `alf` command:
python -m pip install -e .
```

Run a real Codex pilot after authenticating the Codex CLI:

```bash
alf run --language fsharp --agent codex --model YOUR_MODEL --output results/codex
alf run --language csharp --agent codex --model YOUR_MODEL --output results/codex
alf summarize results/codex
```

A provider-neutral command adapter is also available:

```bash
alf run \
  --language fsharp \
  --agent command \
  --agent-command 'your-agent --workspace {workspace} --prompt-file {prompt_file}'
```

The command receives `ALF_WORKSPACE`, `ALF_TASK_ID`, `ALF_LANGUAGE`, and `ALF_PROMPT_FILE`. It may write `.alf/usage.json`; see [the protocol](docs/protocol.md).

## Reproducibility and safety

The default pilot is suitable for harness development, not yet for a publication-quality causal estimate. A credible experiment must pin the model and agent versions, randomize run order, repeat stochastic runs, isolate the workspace so the agent cannot read gold data or evaluator cases, and record exact toolchain/container versions. See [environmental assumptions](docs/environment.md).

## Repository map

- `src/alf/` — Python harness and agent adapters
- `benchmarks/pilot/` — matched .NET projects, task specifications, tests, and gold snapshots
- `docs/` — literature review, hypotheses, protocol, metrics, and experimental design
- `tests/` — harness unit tests
- `.github/workflows/ci.yml` — end-to-end scripted validation on Python 3.12 and .NET 8

## Status

- [x] scoped literature review
- [x] defensible gap statement
- [x] executable paired-language pilot
- [x] fresh-process chain runner
- [x] Codex JSONL usage parser
- [x] CI validation
- [ ] container-isolated real-agent runs
- [ ] larger matched repository family
- [ ] preregistration and power analysis
- [ ] multi-model repeated study
