# Agentic Language Fitness

ALF investigates how programming-language implementation, model configuration, and harness policy affect the cost and reliability of coding-agent maintenance. Its first paired workload uses F# and C# on .NET. This is a research workbench, not a leaderboard or evidence that one language is universally best.

## Start here

[PLAN.md](PLAN.md) is the canonical checkpoint and next assignment. [AGENTS.md](AGENTS.md) routes maintainer agents to it. The [plan review](docs/plan-review-2026-09-05.md) records the latest methodological corrections.

**Current evidence:** E1, E2 and E2a are complete. The [E3a no-tools first-submission/repair pilot](docs/workstream-e3a-oauth-renewal-2026-09-09.md) has now run all 24 fixed trajectories using 32 dispatches, with no batch stop. It compares three selected maintenance tasks, two languages and four repetitions per pair. Operational completion is not universal task success: first and terminal correctness, failed submissions, repair usage and Task 007 architecture evidence are reported separately. This is a small diagnostic pilot, not a language ranking.

The [reproducible descriptive report](reports/workstream-e3a-oauth-renewal-2026-09-09/analysis.md) finds first completion of **6/12 F# and 11/12 C#**, with **12/12 terminal completion in each language** after permitted repairs and a source-bound AI architecture-review addendum. F# used seven repair dispatches versus one for C#. Raw missing-review scores remain unchanged; the report includes all failures and separates initial, repair and total resources.

**Current work:** [H1/H2 construction and pre-execution review](docs/workstream-h1-h2-implementation-2026-09-09.md) implements the adopted comparison of supplied source with selective file reads under software byte budgets. It adds one functioning workload extension; live collection and OAuth staging remain disabled pending human review and separate approval. The completed [H0 audit](docs/workstream-h0-preparation-2026-09-09.md) has 17 passing tests and byte-identical Linux/Windows artifacts. These byte budgets do not establish a physical context-capacity advantage for either language.

The adopted [OAuth/Codex amendment](protocols/workstream-e3a-v1/oauth-amendment.md) uses the existing **local OAuth-backed Codex** route, a pinned no-tools native client and isolated remote evaluation. The successful shakedown, exact runner/image identities, full attempt journals and temporary-credential cleanup are retained in the [execution record](docs/workstream-e3a-oauth-renewal-2026-09-09.md). Earlier failed attempts remain unchanged and separately charged. Further live batches require their own authorization; unused allowance is not permission to expand the sample.

The current rules are in [experimental design](docs/experimental-design.md), [metrics](docs/metrics.md), [workload validity and review gates](docs/workload-validity-and-review-gates-2026-09-05.md), and the future [context-pressure design](docs/workstream-h-context-pressure-design-2026-09-05.md). Dated predecessor proposals explain history; they are not competing current plans. Already frozen protocols/results retain their original identities and must not be retrospectively changed.

## Question and evidence

> For the same semantic maintenance task, how do particular language implementations, models, and tool policies change first-patch quality, repair burden, source retrieval, and total trajectory resources?

Inherited maintenance, multilingual benchmarks, and token-cost studies already exist. ALF explores their controlled intersection; it does not claim to have invented those components. The [literature review](docs/literature-review.md), [search log](docs/search-log.md), and [gap statement](docs/research-gap.md) are dated working material, not proof of exhaustive novelty. Primary citations and scope should be reverified before publication.

The short `variance-v2` pilot found substantial stochastic/order variation. The eight-task `difficulty-v1` successor exposed representation drift. D v3's ten non-counting calibrations all passed the eight-task chain; exploratory F#/C# input and agent-time ratios were near 1.38. These are aggregate costs in a particular ecology, not direct measurements of source density or context capacity.

[E1](docs/workstream-e1-v3-forensic-disposition-2026-09-03.md) recovered more F# failed builds, repair cycles, and project edits. Those failures include dependency/environment problems as well as source errors; missing first-build boundaries were not imputed. [E2](docs/workstream-e2-toolchain-disposition-2026-09-04.md) measured an offline model-free toolchain baseline. [E2a](docs/workstream-e2a-disposition-2026-09-04.md) aligned command forms and the v3 host, finding both more F# dotnet invocations and slower restore/build-capable commands.

E2a also identified a major deployment-specific amplifier: vulnerability audit was enabled while NuGet reachability was blocked and caches were fresh. Removing audit from the repair loop removed much of the restore delay and warning output, while a no-restore compilation gap remained. The legacy constrained-network audit-on condition is historical/stress evidence, not a normal developer baseline. Mechanical timing envelopes do not identify how many model tokens or seconds were causally attributable to each mechanism.

Current work separates controlled first-patch/repair behavior from tool policy. Future H work tests source capacity and retrieval without assuming F# is shorter or that an entire dependency closure must fit simultaneously. H does not have to wait for optional subagent or large cost-replication studies. See [PLAN.md](PLAN.md) for the conditional branches.

## Evaluation principles

Candidates receive the approved predecessor and task, not successor gold, future tasks, research outcomes, or final holdout cases. Development checks may supply feedback; final holdout results may not guide feedback or stopping. Candidate source and project files execute in restricted sandboxes with model credentials and scoring machinery outside their reach.

Report all valid assigned attempts jointly with correctness. A cheap early failure is not efficient completion. Provider token totals, visible-source estimates, active context, direct tool latency, and end-to-end cost are separate measures. Matched implementations do not establish an intrinsic language effect, and public/native repositories need a sampling frame before claims of representativeness.

## Model-free quick start

Requirements: Python 3.11+, Git, and .NET SDK 10.0.302.

```text
python -m pip install -e .
python -m unittest discover -s tests -v
python scripts/alf.py doctor --strict
python scripts/alf.py validate
python scripts/alf.py matrix --agent scripted --output results/pilot
python scripts/alf.py audit PATH_TO_RUN_DIRECTORY
python scripts/alf.py summarize results/pilot
```

The scripted adapter copies gold snapshots to validate machinery without a model request. Its passing results are not coding-agent performance. E3a has separate mock/controller and sandbox checks; the generic commands above do not launch its explicitly gated OAuth pilot.

For the H1/H2 pre-execution packet, `python scripts/h_check.py --output-dir
results/h-review` writes the source identities, counted request examples, derived
caps and fixed feasibility schedule. Add `--build-fixtures` to build the trusted
predecessors, gold and named semantic faults. Use a fresh output directory each
time. Neither command makes a model request; the live runner is disabled.

## Real agents and remote execution

Only after explicit approval of the relevant protocol, resource ceiling, and exact validated implementation:

```text
alf run --language fsharp --agent codex --model YOUR_MODEL --output results/codex
```

This generic adapter command is not a frozen scientific run and does not implement future E3a/H controls by itself.

For the existing high-memory remote host/local-egress arrangement, use the canonical foreground launcher documented in [remote execution](docs/remote-execution.md) and the [environment](docs/environment.md). Reuse it rather than creating new proxy/version layers. The [apparatus postmortem](docs/apparatus-versioning-postmortem-2026-09-02.md) distinguishes V4–V13 development attempts from scientific specifications.

Authentication files are secrets: never log or commit them, and keep them inaccessible to candidate code/tools. Verify credential isolation before running a new controlled candidate; an instruction not to read credentials is not an access boundary. Do not alter existing remote security/network policy during a documentation or scientific-design task.

## Repository map

- `src/alf/`, `scripts/alf.py`: harness, adapters, accounting, audit, and CLI;
- `benchmarks/`: paired applications, tasks, development/evaluator material, and gold snapshots; the full tree is never a candidate mount;
- `protocols/`: named frozen definitions and schedules;
- `reports/`: curated aggregates; raw evidence storage follows each protocol;
- `docs/`: current linked rules plus dated historical designs/dispositions;
- `tests/`: unit and model-free regression tests;
- `infra/remote-runner/`: existing remote apparatus.

No open-source license has been selected.
