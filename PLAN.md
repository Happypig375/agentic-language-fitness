# Research plan

This is the canonical continuation plan. Workstream D v3 is closed at its preregistered calibration stop. The next phase investigates **why** F# cost more in the exploratory calibration before registering a larger language-cost comparison.

## Scientific checkpoint — 2026-09-04

Completed:

- Workstreams A–C: accounting/provenance, variance-v2, the matched eight-task successor chain, and representation apparatus;
- Workstream D scientific design, remote high-memory runner, route shakedown, exact-commit CI, clean v3 freezes, and ten audited non-counting calibrations;
- v3 calibration disposition: H (`gpt-5.6-terra`, medium) saturated; M (`gpt-5.6-luna`, high) and L (`gpt-5.6-luna`, medium) were too easy in both primary and reverse order;
- all ten retained v3 calibration runs were protocol-valid, accounting-valid, successful 8/8, and free of terminal agent/evaluator failure;
- exploratory v3 finding: F# used more input tokens and agent-process time in all five F#/C# pairs, with geometric-mean ratios near 1.38;
- Workstream E causal-attribution design independently approved with every P1/P2 finding closed; its archive-schema review established the exact v3 observability and missingness boundary; and
- Workstream E1 archive-only forensic attribution: ten runs/80 tasks reconciled, transcript-free report SHA `644273ac0f25a32138d50d919ff15677b6ed9639a23198e0c719d154da94901d`, and implementation independently approved; and
- Workstream E2 model-free toolchain/source measurement and report review: all 18 frozen states, 90 schedule entries, 180 evaluator invocations, and 6,940 cumulative case exposures passed; report self-hash `2e4381ab67dd4cc7aed24c323e8edbd30bf83dd29bafc58554615bcd6f24c49a`.

V4–V13 remain apparatus-development history, not scientific families. Do not create v14. The reviewed runner/environment identity remains `runner-remote-highmem-local-egress-r1`. Scientific changes receive scientific-specification IDs; they do not trigger another runner-version cascade.

Analyzer implementation head `82c8c6bdc429f0819a718ce6c4d567fe0a30e88a` and E2 runner head `b953dac54c03087ae46689bc62a3221c3c9d3f97` passed exact-commit Linux and Windows CI. Every new implementation or report publication still requires its own exact-commit green CI before use.

E2 publication acceptance, and therefore activation of E3 as the next gate, is
conditional on exact-commit Linux and Windows CI for the commit containing this
report publication. Until both jobs are green, stop at E2.

## Interpretation boundary

The v3 totals are **ecological trajectory costs**, not direct measurements of source compactness or model memory.

The current harness starts a fresh candidate process and conversation for every task. Therefore:

- tool and compiler history can inflate context within a task;
- that history does not carry from Task 001 into Task 002;
- v3 does not test cumulative cross-task orchestrator context pollution;
- persistent long-horizon memory and repair delegation require separate harness treatments.

Total input tokens can be inflated by generation problems. A faulty patch leads to diagnostics, more tool calls, and repeated cached history, so a syntax/type failure may appear mainly as extra input rather than only extra output.

The final source snapshots are small and similarly sized—roughly two thousand offline proxy tokens and two or three source/project files. Repository capacity was not a meaningful limiting factor. The agent could inspect the whole project without choosing among a large set of distant modules, although the current telemetry does not prove that every file was included in every model request.

### Local small-repository gap versus context-scale slope

Use the following as a conceptual decomposition, not a claim that cost is literally linear:

\[
C_L(S) = A_L + B_L S,
\]

where:

- `C_L(S)` is agent cost for language `L` at repository/context scale `S`;
- `A_L` is the small-project overhead from model familiarity, first-pass generation, compiler/type interaction, project mechanics, repair behavior, and fixed toolchain cost;
- `B_L` is the marginal cost of recovering and maintaining additional source, dependencies, tool history, and architectural state as the relevant working set grows.

The current small, correctness-saturated benchmark provides exploratory evidence
only about the observed cost at its tested scale `S_small`:

\[
C_{F\#}(S_{small}) > C_{C\#}(S_{small})
\]

under the tested models, scaffold, tasks, and .NET ecology. This local gap is
consistent with higher fixed overhead, but one finite scale identifies neither
mathematical intercept. It also does not estimate either language's scale slope.
In particular, it does not establish whether:

\[
B_{F\#} < B_{C\#},\quad B_{F\#} = B_{C\#},\quad\text{or}\quad B_{F\#} > B_{C\#}.
\]

A delayed semantic-density crossover remains conceptually possible if F# has a
higher fixed overhead but a lower marginal context/recovery cost. If those
unidentified terms followed the simple model, the crossover would occur at:

\[
S^* = \frac{A_{F\#}-A_{C\#}}{B_{C\#}-B_{F\#}},
\]

but no crossover may be reported from extrapolation. It must be observed or tightly bounded in a preregistered scale experiment with real retrieval, context, or compaction pressure.

The tasks being easy enough for every retained run to succeed is useful for **equal-exposure cost measurement**: both languages completed the same eight changes, so neither appears cheaper because it failed early. It is not evidence that easy tasks inherently make F# expensive. Rather, the lack of context pressure gives source compactness little opportunity to offset familiarity, generation, repair, and tooling overhead.

Accordingly, maintain two separate questions:

1. **Small-repository ecological cost:** which language currently costs more when the whole relevant project is comfortably manageable and both chains succeed?
2. **Scale-dependent context efficiency:** how does the relative cost and reliability change as repository size, relevant working set, persistent history, retrieval burden, and compaction pressure grow?

Workstream E attributes the first question's overhead pathways. Workstream H estimates the second question's language-by-scale interaction and tests for a crossover.

## Current decision

After the E2 report-publication commit passes exact-commit Linux and Windows CI,
proceed only to **Workstream E3 specification and independent review**, not yet
to a model-backed mechanism run or larger cost replication.

The immediate question is whether the exploratory F# excess came from:

1. static source/tokenization size;
2. pre-edit comprehension or model familiarity;
3. first-pass generation/syntax/type/API errors;
4. compiler/test repair loops;
5. F# project/build obligations and toolchain latency;
6. repeated tool output and transcript replay;
7. a combination of these.

E1 found that all 25 observable failed candidate operations were builds, with 19
conservative repair cycles. F# had the larger failed-build/repair burden in each
configuration, all five project-file changes, and approximately twice the
evaluator time. This prioritizes compiler-repair and ecological toolchain
pathways, but remains descriptive hypothesis routing. It identifies no cause,
training familiarity, universal language effect, intercept `A`, or
scale-dependent term `B`.

E2 then found near-parity source/token proxy size and built-program run time,
while F# restore, build, and restore-through-evaluator composite time were
substantially higher in the pinned offline .NET environment. Repeat-workspace
build time remained about 3.1 times C#, and Task 007 alone required an explicit
F# project compile-order edit. These results strengthen the toolchain/project
and repair-feedback route, but do not isolate causality or identify model
familiarity. See
`docs/workstream-e2-toolchain-disposition-2026-09-04.md`.

A registered successful-chain cost replication remains valuable, but only after the measurement can explain what its total-token endpoint contains. A repository-scale experiment remains necessary even if the small-repository penalty replicates.

No paid/model run is presently authorized. The next bounded artifact is an E3
scientific specification that must be independently reviewed and cleanly frozen;
executing it is a separate continuation decision.

## Immediate continuation order

### E0. Independent causal-attribution design review — complete

Review:

```text
docs/post-v3-interpretation-and-workstream-e-design-2026-09-03.md
```

The independent review is **APPROVED** with no remaining P1/P2 finding. It
closed the following areas:

- distinction between unique source context, generated output, tool feedback, and replayed transcript;
- distinction between the local small-repository gap, conceptual intercept, and context-scale slope/crossover;
- fact that v3 is fresh-per-task and cannot establish cross-task context pollution;
- diagnostic and command classification;
- controlled use of gold predecessor snapshots;
- comprehension, one-shot, and full-repair modes;
- persistent-orchestrator and delegated-repair design;
- total-system versus orchestrator-only cost;
- anti-overengineering and stopping rules.

The approved resolution is recorded in the design. In particular, v3 has event
order and task-level usage/timing but no per-command timing, model-interaction
usage, phase-specific reasoning, unique/repeated source exposure, replayed
source/diagnostic tokens, peak context, or compaction. Compound commands require
bounded multi-label classification and explicit ambiguity. No model call was
made during review.

### E1. Forensically attribute the existing v3 trajectories — complete

The deterministic analyzer used only the preserved raw v3 archive and issued no
model or outbound network request. Analyzer commit
`82c8c6bdc429f0819a718ce6c4d567fe0a30e88a` passed independent review and
exact-commit Linux/Windows CI. Ordinary Git publication and CI control-plane
activity remain allowed; they must not invoke the remote benchmark/model route.

First fail closed on the calibration-report self-hash, the exact ten-attempt
roster, every result/raw-inventory/artifact/source-tree identity, all 80 task
envelopes and sidecars, task-boundary commits, and `alf audit`. Record the input
hashes plus analyzer Git SHA/schema version; an integrity mismatch forbids a
partial aggregate.

Classify only the observed v3 Linux/Bash forms. Completed compound command
events receive zero or more bounded operation labels plus an explicit
ambiguous/unparsed disposition; their outer exit is never assigned to an
uncertain inner operation. Separate candidate activity from evaluator activity,
and define pre-edit builds, the first post-edit candidate build, diagnostics,
and repair cycles through recorded event order. Candidate event/command timing
is unavailable.

Report only derived command/diagnostic/repair counts, canonical recorded-output
volumes, task aggregate usage/time, committed boundary source/diff/project
metrics, codes/categories, and hashes. Use synthetic/redacted fixtures for every
actual event shape and bounded compound/redirection equivalence class. Publish
no raw command, output, message, thread ID, absolute path, inline test input, or
real transcript excerpt.

The following remain explicitly `null` with reasons: per-command/event elapsed
time; time to/before/after a build; model-interaction count and per-interaction
usage; first-patch or phase-specific tokens/reasoning; unique/repeated source
exposure; replayed source/diagnostic tokens; peak context; compaction; full
evaluator-output volume; and intermediate patch content. Cached input is not a
measure of replayed diagnostics.

Use the report only to route hypotheses:

- lower first-post-edit build success and skewed diagnostics → first-pass generation candidate;
- more failed build/test–edit cycles and recorded diagnostics → repair-amplification candidate;
- more observable inspection/search before first mutation → familiarity/comprehension candidate, not training-familiarity attribution;
- extra project-file work or evaluator latency → ecological toolchain candidate;
- source/proxy size and task aggregate input co-vary without observable repair/exploration growth → static/scale candidate for Workstream H;
- cross-task context pollution → not identifiable from v3.

The stage trend is descriptive only. It cannot estimate the repository-scale
slope `B`.

**Exit satisfied:** every retained task reconciled to its artifact hashes and
boundary commits; every completed command has a versioned
classification/disposition; diagnostic/repair rules cover every observed
bounded event equivalence class; candidate/evaluator activity is separate; and
the missingness ledger is complete. The implementation passed independent review
and exact-commit CI. The transcript-free report publication commit is accepted
only when its own exact-commit Linux/Windows CI is green. See
`docs/workstream-e1-v3-forensic-disposition-2026-09-03.md` and
`reports/workstream-e-v3/forensic-report.md`.

### E2. Establish model-free toolchain and source baselines — measurement complete; publication CI-gated

As a separate bounded continuation under the pinned environment, materialize and
hash all 18 canonical states (baseline plus eight cumulative gold stages per
language). Execute exactly five preregistered paired rounds in a hashed,
interleaved order. Each round uses a fresh workspace without `bin`/`obj` and one
immediate same-workspace repeat; call them fresh-workspace and repeat-workspace,
not machine-cold/warm. Keep package cache/network policy fixed.

Use the exact restore, Release no-incremental/no-restore build, and no-build
evaluator commands in the approved design. Record restore only for the fresh
regime, build/run/evaluator measures for both regimes, the fresh composite,
recorded output volume/warnings, and static project/source obligations. Internal
compiler phases remain unavailable unless directly exposed; do not add binary
logging merely to obtain them.

At every stage record:

- source files, bytes, lines, lexical units, and tokenizer-proxy counts;
- project-file changes;
- diff size;
- task-specific obligations.

Treat this as explanatory ecological cost. Do not mechanically subtract it from agent time, because compiler latency can change agent behavior. Every state/repetition must pass its cumulative evaluator and integrity checks; there is no adaptive extension or selective silent retry.

The primary estimand is **ecological language-stack cost**: idiomatic F#/C# plus
their real .NET project/tooling behavior. A controlled-core representation-cost
variant that neutralizes project mechanics is a later, separately reviewed
treatment.

**Measurement exit satisfied:** the accepted attempt at runner commit
`b953dac54c03087ae46689bc62a3221c3c9d3f97` matched all 18 frozen states and
completed all 90 schedule entries. Both regimes and all 180 evaluator
invocations passed, covering 6,940 cumulative cases; the package cache was
unchanged and the raw inventory reconciled. Across 45 matched stage-by-round
pairs, the geometric-mean F#/C# ratios were 8.403 for fresh restore, 3.037 for
fresh build, 3.117 for repeat build, 4.490 for the fresh composite, and 0.988
and 0.984 for fresh and repeat run time. The immutable report's generic warning
field includes 180 false matches from `.NET` summary footers; raw diagnostics
show zero code-bearing C# warning lines and 225 F# `NU1900` lines. The parser is
corrected prospectively without altering or rerunning the accepted baseline.
See `reports/workstream-e2-toolchain-v1/` and
`docs/workstream-e2-toolchain-disposition-2026-09-04.md`.

The report becomes an accepted publication only when the exact commit containing
it passes Linux and Windows CI. That condition does not require another run or
another status-only commit.

### E3. Specify a bounded causal mechanism pilot — next design gate

Create a new reviewed scientific specification using matched gold predecessor snapshots: Task 001 uses the clean baseline and Task `n` uses the canonical gold state after Task `n-1`. Hash and validate each predecessor and never expose current/future gold, evaluator cases, or obligation maps. Use one preregistered model/scaffold configuration and a small task subset spanning simple, type/validation, and multi-file/API work.

Compare:

1. **Comprehension/localization:** controller-enforced read-only source inspection; no build/test/execution/write/network; score a structured response outside the candidate boundary against a frozen blinded obligation map.
2. **One-shot patch:** the same read-only inspection followed by exactly one controller-applied multi-file diff; no candidate build/test or feedback before frozen evaluation.
3. **Monolithic full agent:** normal inspect–edit–compile/test–repair.

All modes start from the same predecessor and hold the semantic task, visible source, model/effort, limits, and environment fixed. This separates semantic recovery, first-pass output ability, and repair amplification. Because E1 informs task selection, the pilot is non-counting and may only choose the next causal treatment and estimate variance; do not build a large factorial.

The comprehension condition estimates small-project semantic recovery, not context-window pressure. It becomes a context-density test only when repeated at preregistered repository/working-set scales in Workstream H.

### E4. Make the mechanism decision

- Repair errors dominate → test compiler-feedback containment and repair delegation.
- Observable pre-edit exploration dominates → treat familiarity/comprehension as a candidate and test a separately reviewed documentation/familiarity or retrieval intervention.
- Project/toolchain obligations dominate → retain ecological study and add a controlled-core variant only if worthwhile.
- Boundary source/proxy size and task aggregate input co-vary without corresponding observable repair/exploration growth → treat it only as a static/scale candidate, then test it under real repository pressure in Workstream H.
- No stable attribution → replicate only if the required sample remains worthwhile; otherwise report ambiguity and measurement limits.

## Workstream F — Context containment and repair delegation

Run only if Workstream E shows meaningful repair/tool-output amplification.

### Scientific question

Can an explicit harness keep compiler/test repair chatter out of the strategic orchestrator’s context, and does this change later decision quality or the F#/C# cost ratio?

A routing prompt alone is insufficient. The harness must enforce and separately account for contexts.

### Minimal 2 × 2 harness design

Factors:

- memory: fresh orchestrator per task versus persistent orchestrator across the chain;
- repair routing: inline/monolithic versus isolated repair worker.

Conditions:

| Condition | Purpose |
|---|---|
| Fresh + inline | Controlled inline baseline |
| Fresh + delegated | Tests within-task context containment |
| Persistent + inline | Tests cumulative cross-task tool/repair pollution |
| Persistent + delegated | Tests whether repair isolation preserves strategic context |

Use the same model for orchestrator and worker first. Varying worker model is a later practical intervention.

Use the same deterministic controller in both routing arms. Hold the initial
patch boundary, build/test schedule, diagnostic payload, retry count, and repair
budget fixed. Inline repair returns raw diagnostics to the orchestrator;
delegated repair gives the identical payload to one ephemeral worker and returns
only a frozen controller-generated summary to the orchestrator. The worker sees
the full candidate-visible workspace/task/diff unless one candidate-blind,
preregistered selector is shared across languages. Never make an ad hoc
“relevant files” choice or expose gold/evaluator material. The current
autonomous harness is an external ecological reference, not the controlled
inline arm.

Report separately:

- total system input/output across all agents;
- orchestrator-only cost and available context/compaction telemetry;
- worker cost;
- controller toolchain time/output, summed agent-process time, and end-to-end wall time separately;
- diagnostic/tool-output volume withheld from the orchestrator;
- repairs, escalations, correctness, task survival, and late-task decision quality;
- language × memory × routing interactions.

A delegated harness may improve orchestrator quality while increasing total cost. Both outcomes must remain visible. Define late-task decision quality before freezing through objective evaluator correctness, escaped regressions, task survival, and repair burden—not subjective post-hoc scoring.

This workstream tests transcript containment, not source semantic density by itself. A smaller persistent-orchestrator F#/C# gap under delegation would show that repair history mediates part of the ecological gap; it would not establish a source-size crossover.

### Anti-overengineering constraint

Do not construct a general multi-agent framework. Implement only the explicit controller required for the four conditions. Reuse the current remote route and runner. If symmetric controller behavior or per-agent accounting cannot be audited, stop rather than infer it; otherwise label the comparison a bundled harness intervention, not a routing effect. No recursive agents or dynamic routing in the first experiment.

## Workstream G — Registered small-repository ecological cost replication

After Workstream E—and Workstream F if indicated—register a successful-chain cost study on the current benchmark.

This workstream estimates the current regime's paired cost gap at the frozen
small-repository scale. It should not be described as an identified intercept or
a test of which language uses a large context window more efficiently.

Primary outcomes should include:

1. full-chain correctness;
2. paired full-chain total input under the specified harness;
3. first-pass compilation and repair-cycle burden;
4. paired agent-process time;
5. per-task and cumulative trajectory curves.

Interpret total input as **model input processed over the complete trajectory**, not unique source context. Keep configuration strata separate. Exclude v3 calibration observations from formal estimates. A monolithic and delegated harness, if both studied, are separate harness strata rather than silently interchangeable implementations.

A replicated F# penalty would support
`C_F#(S_small) > C_C#(S_small)` for the tested ecology. It would not identify
either intercept, determine the relative scale slopes, or rule out a later
crossover.

## Workstream H — Test the original context-density hypothesis across scale

The current repository is too small to test whether concise or semantically dense source preserves agent memory. Build one matched, scalable repository architecture before multiplying independent repository families.

### Scientific question

How does the paired F#/C# cost and reliability ratio change as the candidate-visible repository, task-relevant working set, architectural distance, persistent history, and tool-output burden grow?

The primary target is the **language × scale interaction**, not the average language coefficient.

### Scale design

Use several preregistered size/pressure levels generated from one reviewed matched architecture, for example:

1. current small baseline;
2. medium multi-module repository;
3. large repository with distributed but known relevant dependencies;
4. a pressure level at which retrieval omissions, compaction, or working-set tradeoffs are actually observed.

Do not inflate size with inert filler. Added modules must create realistic navigation or dependency obligations, and the evaluator must know the gold relevant-file/symbol set. Keep external behavior and task families matched across languages.

Pilot only enough to locate meaningful pressure levels, then freeze the scale points before formal collection. If every level remains comfortably retrievable with no compaction or relevant-context tradeoff, the study has not tested the context-density hypothesis and must not report a null crossover conclusion.

### Context regimes

Separate rather than silently combine:

- fresh context per task;
- persistent orchestrator context across the chain;
- inline repair;
- delegated repair when Workstream F establishes an auditable implementation.

Do not begin with the full factorial. First choose the smallest set needed to estimate the language-by-scale interaction under the practical baseline; add memory/routing strata only when justified by Workstream F.

### Required measurements

- candidate-visible repository and task-relevant token size;
- relevant-file and symbol retrieval recall/precision;
- architectural distance between task entry point and affected code;
- unique and repeated source/tool-output exposure where measurable;
- number of model interactions and input per interaction;
- maximum/terminal orchestrator context and compaction events where exposed;
- diagnostic/tool-output volume;
- fresh versus persistent context state;
- orchestrator and worker cost separately when delegated;
- task success, escaped regressions, and late-chain decision quality;
- total ecological cost as chain depth and scale grow.

Unsupported telemetry remains unavailable rather than estimated.

### Analysis

Use paired, configuration-specific models that expose the interaction, conceptually:

```text
log(cost) ~ language * log(repository_or_relevant_working_set_tokens)
            + task + order + time + configuration
            + (1 | matched_pair) + (1 | task_family)
```

Model correctness/retrieval with suitable hierarchical binary or ordinal models. Report observed scale-specific ratios and uncertainty before any fitted crossover.

A semantic-density crossover is supported only when:

- the language × scale interaction is stable across preregistered tasks/blocks;
- F# becomes relatively cheaper or more reliable as genuine context pressure increases;
- repair, toolchain, and familiarity pathways are measured or modeled;
- the estimated crossover lies inside the observed scale range or a narrowly supported interpolation range.

Do not claim a crossover from extrapolating the local small-scale gap. If F# remains more expensive at all observed scales, report the range over which no crossover was found rather than claiming none can ever exist.

## Decision logic after causal work

### F# excess is mainly first-pass/repair difficulty

The practical conclusion is that current models/tooling make F# more expensive under the tested small-project ecology. Test documentation/familiarity and isolated repair before making a broader language claim.

### Delegation reduces orchestrator pollution but not total cost

Report that harness architecture can preserve strategic context while language-specific repair burden remains. Optimize orchestration separately from total compute.

### Delegation reduces both total and orchestrator cost

Treat repair routing as a major agentic-language interaction and include harness design in future language comparisons.

### F# relative cost improves with real scale/context pressure

The original context-density thesis gains support. Estimate the observed slope and crossover range rather than generalizing beyond the tested models, repositories, and harnesses.

### F# small-project gap persists without scale improvement

Conclude that model familiarity, generation, repair, and/or tooling dominate semantic-density benefits throughout the observed range. This remains conditional on the tested ecology.

### Gap disappears after attribution controls

Treat v3 as a calibration cluster or toolchain artifact. Reframe toward configuration/harness sensitivity if that is the stable finding.

## Overall sequence

```text
E0 independent review (complete)
  -> E1 archive-only forensic attribution (complete)
  -> E2 model-free toolchain/source baseline (measurement complete; publication CI-gated)
  -> E3 bounded comprehension / one-shot / repair specification (next after green publication CI)
  -> E4 causal decision
  -> F explicit memory/routing experiment when justified
  -> G registered small-repository ecological cost replication
  -> H preregistered multi-scale context-pressure experiment
```

## Evidence and claim boundaries

- V3 calibration is non-counting and excluded from future formal estimates.
- The five same-direction pairs are a strong exploratory small-repository signal, not confirmatory significance.
- Aggregate input tokens do not measure unique source memory.
- The current result is a local small-scale ecological gap consistent with fixed overhead, not an identified mathematical intercept or marginal context-cost slope.
- Easy/all-success tasks provide equal exposure for cost comparison but do not test capability boundaries or context pressure.
- Zero file-read/revisit values currently mean unsupported telemetry, not literal absence; bounded command evidence still cannot recover unique source exposure.
- Current fresh-per-task runs do not test cross-task context degradation.
- A later crossover remains possible but unestablished; it must be tested across observed pressure levels rather than inferred from source concision.
- No result establishes an intrinsic or universal F#, C#, model, or harness ranking.

## Stop and anti-overengineering rules

- Preserve the v3 evidence; do not reopen its blocked formal schedule.
- Do not create v14 for a scientific-analysis change.
- After this publication's exact-commit CI is green, the next autonomous task is only the E3 scientific specification through independent review and clean freeze; stop before implementation or any model run.
- After two failures of one apparatus class, stop and report instead of building another recovery subsystem.
- Stop before changing candidate-visible semantics, model/prompt/task/evaluator, scientific estimands, or frozen conditions without approved design.
- No paid/model call is presently authorized; E3 execution requires a separately approved continuation after its specification is independently approved and cleanly frozen.
