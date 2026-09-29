# Interactive Software Evolution

Interactive Software Evolution (ISE) is the internal codename for research starting from **Nu's claimed innovations**: what its approach to state, domain modeling, coordination and development tools contributes, which mechanisms have predecessors, and what evidence could establish useful differences. The current assignment surveys that background across functional design, game architectures, types, runtime costs, testing, maintenance and coding agents.

The [background survey](docs/literature/nu-background-survey-2026-09-30.md) and [search ledger](docs/literature/nu-background-searches-2026-09-30.md) record the active work and unresolved coverage. Novelty, value and scientific validity are assessed separately; Nu-specific benefits and priority remain unconfirmed. Experimental construction and live allocation remain on hold.

The project was previously named Agentic Language Fitness. Its F#/C# experiments remain historical evidence with their original records and identifiers. The [rename record](docs/project-rename-2026-09-30.md) describes the current `ise` commands and the compatibility needed to reproduce that evidence.

## Start here

[PLAN.md](PLAN.md) is the canonical checkpoint and next assignment. [AGENTS.md](AGENTS.md) routes maintainer agents to it. The active assignment characterizes Nu's claimed innovations against the wider research background. The [D1 proposal](docs/fsharp-domain-evolution-research-proposal-2026-09-16.md) remains a deferred-start recommendation; it does not delimit the survey.

**Earlier experimental evidence:** E1, E2 and E2a are complete. The [E3a no-tools first-submission/repair pilot](docs/workstream-e3a-oauth-renewal-2026-09-09.md) has now run all 24 fixed trajectories using 32 dispatches, with no batch stop. It compares three selected maintenance tasks, two languages and four repetitions per pair. Operational completion is not universal task success: first and terminal correctness, failed submissions, repair usage and Task 007 architecture evidence are reported separately. This is a small diagnostic pilot, not a language ranking.

The [reproducible descriptive report](reports/workstream-e3a-oauth-renewal-2026-09-09/analysis.md) finds first completion of **6/12 F# and 11/12 C#**, with **12/12 terminal completion in each language** after permitted repairs and a source-bound AI architecture-review addendum. F# used seven repair dispatches versus one for C#. Raw missing-review scores remain unchanged; the report includes all failures and separates initial, repair and total resources.

**Earlier construction checkpoint (2026-09-12):** [maintenance/context construction](docs/maintenance-sim-construction-2026-09-12.md) has model-free validation for one original headless simulation in F# and modern C#, followed by eight interacting maintenance changes. The question is whether architectural coherence preserves useful context and correct decisions as obligations accumulate. The proposed episodes retain the candidate's software but reset the conversation, with no tool-error or diagnostic-repair loop filling the context. The [standalone human-review packet](docs/maintenance-sim-human-review-2026-09-12.md) lists exact sources, settings and remaining decisions. All 18 trusted checkpoints and eight semantic faults pass; these are not candidate results. F# reference inputs are larger at every episode in this pair, so the construction does not establish the hypothesized compactness advantage. This is feasibility preparation, not a large-project or language-ranking result.

The earlier [H1/H2 human-review packet](docs/workstream-h1-h2-human-review-2026-09-10.md) and completed [H0 audit](docs/workstream-h0-preparation-2026-09-09.md) remain identifiable preparation. Live collection and OAuth staging remain disabled. Authored-byte budgets and offline token proxies do not establish a physical provider context-capacity advantage for either language.

The adopted [OAuth/Codex amendment](protocols/workstream-e3a-v1/oauth-amendment.md) uses the existing **local OAuth-backed Codex** route, a pinned no-tools native client and isolated remote evaluation. The successful shakedown, exact runner/image identities, full attempt journals and temporary-credential cleanup are retained in the [execution record](docs/workstream-e3a-oauth-renewal-2026-09-09.md). Earlier failed attempts remain unchanged and separately charged. Further live batches require their own authorization; unused allowance is not permission to expand the sample.

The preserved experimental rules are in [experimental design](docs/experimental-design.md), [metrics](docs/metrics.md), [workload validity and review gates](docs/workload-validity-and-review-gates-2026-09-05.md), and the future [context-pressure design](docs/workstream-h-context-pressure-design-2026-09-05.md). Dated predecessor proposals explain history; they are not competing current plans. Already frozen protocols/results retain their original identities and must not be retrospectively changed.

## Earlier experimental question and evidence

> For the same semantic maintenance task, how do particular language implementations, models, and tool policies change first-patch quality, repair burden, source retrieval, and total trajectory resources?

Inherited maintenance, multilingual benchmarks, and token-cost studies already exist. The earlier experimental program explored their controlled intersection; it does not claim to have invented those components. The [literature review](docs/literature-review.md), [search log](docs/search-log.md), and [gap statement](docs/research-gap.md) are dated working material, not proof of exhaustive novelty. Primary citations and scope should be reverified before publication.

The short `variance-v2` pilot found substantial stochastic/order variation. The eight-task `difficulty-v1` successor exposed representation drift. D v3's ten non-counting calibrations all passed the eight-task chain; exploratory F#/C# input and agent-time ratios were near 1.38. These are aggregate costs in a particular ecology, not direct measurements of source density or context capacity.

[E1](docs/workstream-e1-v3-forensic-disposition-2026-09-03.md) recovered more F# failed builds, repair cycles, and project edits. Those failures include dependency/environment problems as well as source errors; missing first-build boundaries were not imputed. [E2](docs/workstream-e2-toolchain-disposition-2026-09-04.md) measured an offline model-free toolchain baseline. [E2a](docs/workstream-e2a-disposition-2026-09-04.md) aligned command forms and the v3 host, finding both more F# dotnet invocations and slower restore/build-capable commands.

E2a also identified a major deployment-specific amplifier: vulnerability audit was enabled while NuGet reachability was blocked and caches were fresh. Removing audit from the repair loop removed much of the restore delay and warning output, while a no-restore compilation gap remained. The legacy constrained-network audit-on condition is historical/stress evidence, not a normal developer baseline. Mechanical timing envelopes do not identify how many model tokens or seconds were causally attributable to each mechanism.

The [maintenance design](docs/maintenance-context-design-review-2026-09-12.md) separates representation size, cumulative correctness, inherited regressions and source-bound architectural diagnostics. Modern C# records and pattern matching are allowed; few lines or resemblance to the reference architecture are not success criteria. Broader language and long-term-maintenance claims need independent project families and expert review. See [PLAN.md](PLAN.md) for the current bounded assignment.

## Evaluation principles

Candidates receive the approved predecessor and task, not successor gold, future tasks, research outcomes, or final holdout cases. Development checks may supply feedback; final holdout results may not guide feedback or stopping. Candidate source and project files execute in restricted sandboxes with model credentials and scoring machinery outside their reach.

Report all valid assigned attempts jointly with correctness. A cheap early failure is not efficient completion. Provider token totals, visible-source estimates, active context, direct tool latency, and end-to-end cost are separate measures. Matched implementations do not establish an intrinsic language effect, and public/native repositories need a sampling frame before claims of representativeness.

## Model-free quick start

Requirements: Python 3.11+, Git, and .NET SDK 10.0.302.

```text
python -m pip install -e .
python -m unittest discover -s tests -v
python scripts/ise.py doctor --strict
python scripts/ise.py validate
python scripts/ise.py matrix --agent scripted --output results/pilot
python scripts/ise.py audit PATH_TO_RUN_DIRECTORY
python scripts/ise.py summarize results/pilot
```

The scripted adapter copies gold snapshots to validate machinery without a model request. Its passing results are not coding-agent performance. E3a has separate mock/controller and sandbox checks; the generic commands above do not launch its explicitly gated OAuth pilot.

To reproduce the trusted maintenance construction (not candidate execution):

```text
python -m unittest discover -s tests -p test_maintenance.py -v
python scripts/maintenance_check.py --build-fixtures --audit-failures --output-dir results/maintenance-check
```

Use a fresh output directory. This audits the fixed trusted references, complete
input envelopes, semantic faults and inherited-failure applicability. A future
maintenance candidate controller still needs separate isolated implementation
and review; the general host-subprocess evaluator is not that controller.

For the H1/H2 pre-execution packet, `python scripts/h_check.py --output-dir
results/h-review` writes the source identities, counted request examples, derived
caps and fixed feasibility schedule. Add `--build-fixtures` to build the trusted
predecessors, gold and named semantic faults. Use a fresh output directory each
time. Neither command makes a model request; the live runner is disabled.

## Real agents and remote execution

Only after explicit approval of the relevant protocol, resource ceiling, and exact validated implementation:

```text
ise run --language fsharp --agent codex --model YOUR_MODEL --output results/codex
```

This generic adapter command is not a frozen scientific run and does not implement future E3a/H controls by itself.

For the existing high-memory remote host/local-egress arrangement, use the canonical foreground launcher documented in [remote execution](docs/remote-execution.md) and the [environment](docs/environment.md). Reuse it rather than creating new proxy/version layers. The [apparatus postmortem](docs/apparatus-versioning-postmortem-2026-09-02.md) distinguishes V4–V13 development attempts from scientific specifications.

Authentication files are secrets: never log or commit them, and keep them inaccessible to candidate code/tools. Verify credential isolation before running a new controlled candidate; an instruction not to read credentials is not an access boundary. Do not alter existing remote security/network policy during a documentation or scientific-design task.

## Repository map

- `src/ise/`, `scripts/ise.py`: harness, adapters, accounting, audit, and CLI;
- `benchmarks/`: paired applications, tasks, development/evaluator material, and gold snapshots; the full tree is never a candidate mount;
- `protocols/`: named frozen definitions and schedules;
- `reports/`: curated aggregates; raw evidence storage follows each protocol;
- `docs/`: current linked rules plus dated historical designs/dispositions;
- `tests/`: unit and model-free regression tests;
- `infra/remote-runner/`: existing remote apparatus.

No open-source license has been selected.
