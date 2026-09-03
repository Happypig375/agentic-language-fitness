# Post-v3 causal attribution and successor design

**Date:** 2026-09-03  
**Status:** independently reviewed and approved with no remaining P1/P2 findings. E1 archive-only implementation is the next gate; no paid/model run is authorized.

## Evidence boundary

Workstream D v3 produced ten preregistered, non-counting calibration runs over the eight-task descriptive F#/C# chain. Every retained run was protocol-valid, accounting-valid, successful 8/8, and free of terminal agent/evaluator failure. Across the five F#/C# pairs, F# used more total input, output, tool calls, and agent-process time, with geometric-mean F#/C# ratios near 1.38 for input and agent time.

Those totals are an **ecological trajectory-cost signal**, not an explanation. They do not distinguish:

- static source/context size;
- first-pass generation ability;
- syntax/type/API error rate;
- compiler and test feedback loops;
- project-system/toolchain obligations;
- model familiarity and exploratory behavior;
- repeated transcript/tool-output replay;
- context compaction or loss;
- harness architecture.

The v3 observations remain non-counting and excluded from future formal estimates. They are appropriate for deciding what to measure next, not for claiming a language effect.

## Critical interpretation correction

The current benchmark launches a **fresh candidate process and conversation for every maintenance task** while retaining only repository state. Therefore:

- diagnostics and tool history from Task 001 do not occupy the model conversation for Task 002;
- v3 can reveal within-task interaction/repair amplification;
- v3 cannot test whether compile loops accumulate across an eight-task persistent orchestrator and degrade later strategic decisions;
- “long-horizon context pollution” requires a separate persistent-context treatment.

Also, total input tokens are not unique source tokens. In an agent loop, a faulty patch can cause compiler output, further tool calls, and repeated cached prefixes to be presented to later model calls. A generation problem may therefore appear predominantly as extra **input** cost.

The final descriptive snapshots are only about two thousand offline proxy tokens and are similar in size. This small benchmark does not meaningfully test whether F# fits a large repository into model memory better than C#.

The conceptual decomposition `C_L(S) = A_L + B_L S` is a way to separate
questions, not a fitted model. One finite, small repository scale does not
identify the mathematical intercept `A_L`, and stage growth inside this small
chain does not estimate `B_L`. V3 shows a local ecological gap consistent with
higher fixed overhead under the tested setup. Any slope or crossover claim
requires externally defined, matched scale levels and must remain within the
observed or tightly interpolated range.

## Causal model

The successor work treats total trajectory cost as the endpoint of several pathways:

```text
language
  ├─> source representation / tokenizer fertility ─────────────┐
  ├─> model familiarity / idiom recall ─> initial patch quality│
  ├─> syntax + type-system interaction ─> compiler diagnostics  │
  ├─> project/build obligations ────────> tool calls + latency   │
  └─> documentation/search needs ───────> inspections            │
                                                               v
failed or uncertain step -> more edits/builds/tests/tool output -> longer transcript
                                                               |
harness memory/routing -----------------------------------------┘
                                                               v
total input/output/time, context pressure, and final correctness
```

A language may have compact source yet cost more today because the model repairs it more often. Conversely, an agent-friendly harness may contain repair chatter outside the strategic orchestrator while still incurring total worker cost. Both are scientifically relevant, but they answer different questions.

## Workstream E: attribute the existing cost gap

Workstream E precedes a registered cost replication. Its purpose is to determine what the v3 totals actually measure and which causal experiment is justified.

### E0 — Independent review

Review this design before implementation. Close all P1/P2 findings concerning:

- separation of comprehension, generation, repair, toolchain, and memory effects;
- use of non-counting v3 traces for mechanism discovery only;
- diagnostic classification and unsupported telemetry;
- controlled task-state construction;
- harness-routing estimands;
- anti-overengineering and stop rules.

No model call is authorized by this design.

#### Independent design-review disposition — 2026-09-03

Final disposition: **APPROVE**. The initial review found five P1 and three P2
issues; the final independent re-review found every one closed and no new
P1/P2 finding.

The material resolutions are:

- an explicit v3 observability matrix makes unavailable event timing,
  per-interaction usage, phase-specific reasoning, source exposure, replay,
  peak context, and compaction `null` rather than estimated;
- a fail-closed ten-attempt/80-task archive-identity gate and a bounded,
  multi-label Bash classifier replace underspecified command/build inference;
- candidate and evaluator activity, first post-edit build status, diagnostics,
  repair cycles, output volume, and missingness now have operational rules;
- E2 now has 18 hashed states, five fixed paired rounds, deterministic
  interleaving, exact command shapes, fresh/repeat workspace definitions, and a
  complete exit criterion;
- E3 gold predecessors and read-only/one-diff modes are controller-enforced and
  remain non-counting; and
- any later inline/delegated comparison uses the same controller, feedback
  schedule, budget, and accounting boundary, so routing is not confounded with
  a different workflow.

The archive-schema check also confirmed all ten current `result.json` hashes
against the calibration report. It observed ordered events but no command
timing, one aggregate usage record per task, and frequent compound commands;
those facts directly motivate the conservative E1 contract below. This approval
covers the design only. It does not approve implementation, a scientific
specification, or a model-bearing run.

### E1 — Archive-only forensic attribution

Use the preserved raw v3 trajectories; do not issue new model requests. E1 is
one deterministic analyzer and one report schema, not a new telemetry framework.

#### Fail-closed input identity

Before classification, require exactly the ten attempt IDs in the closed
calibration report. Recompute and match the report self-hash, every raw
`result.json` hash, every raw-inventory tree hash, the artifact/source-tree
identities, all 80 task envelopes and event/usage sidecars, and the existing
`alf audit` result. Record the calibration-report hash, input inventory hashes,
analyzer Git SHA, and analyzer schema version in the derived report. An absent,
extra, changed, or unauditable input fails E1 as a whole; do not publish a
partial mechanism aggregate.

#### V3 observability contract

| Construct | V3 status | E1 rule |
|---|---|---|
| Candidate event order, completed command text, outer exit status, and recorded aggregate output | Available | Report event ordinals and derived classes/volumes without publishing raw text. |
| Candidate command or event duration | Unavailable | Emit `null` with reason; do not estimate time to or before/after a build. |
| Task-level input, cached input, output, reasoning output, agent-process time, and task time | Available | Preserve the provider/harness aggregates. Cached input is a cache-hit component, not identified replayed source or diagnostics. |
| Model-interaction count, per-interaction usage, first-patch tokens, and phase-specific reasoning | Unavailable | Emit `null`; `agent_message` items are not model-call records. |
| Unique/repeated source exposure, replayed transcript/tool tokens, peak context, and compaction | Unavailable | Emit `null`; never infer these from aggregate input or command counts. |
| File-change path/kind and committed task-boundary diff/tree | Available | Report derived path/count/diff/source metrics; intermediate patch contents are unavailable. |
| Harness evaluator outcome and duration | Available | Keep separate from candidate commands. Only retained evaluator tails are available, so full evaluator-output volume is `null`. |

The v3 streams have ordered events but no event timestamps or command durations,
and one aggregate usage record per task. Those limitations are properties of
the frozen evidence and must not be repaired retrospectively.

#### Conservative classifier contract

Scope the parser to the actual v3 Linux/Bash event forms. Do not build a generic
shell parser or add PowerShell compatibility. Consume completed items in
recorded order, deduplicate by item ID, and assign each command event zero or
more safely recognized atomic labels—source inspection, search, edit, build,
test/run, project configuration, environment, or other—plus an explicit
`ambiguous_or_unparsed` disposition. Compound commands are multi-label; the
outer exit code must not be inherited by an inner operation whose result is not
unambiguous.

Treat a completed file-change item, or a fixture-covered write-capable shell
form, as a mutation. The initial edit batch is the mutations after the first
mutation and before the first subsequent recognized compiler invocation. Define
`first_post_edit_candidate_build` as that first recognized candidate build—not
a pre-edit probe and not the external evaluator build. Its outcome is success
only when exit/status and zero-error evidence are unambiguous; otherwise it is
`null`. Warnings are reported separately, and the term “clean build” is not
used. Candidate builds/runs, smoke probes, and tests remain distinct from the
harness evaluator build/run.

Derive a repair cycle only from an unambiguously failed recognized build/test,
a later completed mutation, and the next recognized attempt. Preserve ambiguous
chains as unclassified rather than guessing. Report command/event ordinals and
counts before and after the first post-edit build, never phase elapsed time.

Version the compiler diagnostic mapping, severity rules, and categories.
Report both canonical recorded-output bytes/lines/offline-proxy tokens and
deduplicated diagnostic instances keyed by severity, code, normalized
file/span, and normalized message; keep unmatched material `unclassified`.
Call these recorded-output volumes because redirection can hide subprocess
output. Pin source and output proxy counts to `tiktoken==0.14.0`, `o200k_base`,
LF-normalized UTF-8, sorted relative paths, and a documented canonical
serialization. Also retain the existing approximate lexical-unit metric and
file-inclusion grammar; neither proxy is provider billing or unique model
context.

The report records, per task and run: multi-label command counts; pre-edit,
first-post-edit, and later build outcomes; diagnostic and recorded-output
volumes; conservative repair cycles; candidate versus evaluator checks;
task-level usage/timing; committed boundary source/diff/project-file metrics;
and the complete missingness ledger above. Validate every actual event shape
and each bounded compound/redirection equivalence class observed in v3 through synthetic or redacted
fixtures. Publish no raw commands, outputs, messages, thread IDs, absolute host
paths, inline test inputs, or real transcript excerpts. Raw transcripts remain
outside Git.

#### Attribution signatures

Interpret the forensic report through preregistered signatures rather than a single correlation:

| Candidate cause | Expected signature |
|---|---|
| Static/context-size candidate | Boundary source/proxy size and task-level aggregate input move together across stages without a corresponding increase in observable repair activity. Per-cycle input is unavailable, so v3 can only route this hypothesis to a later scale treatment. |
| First-pass output ability | Lower success of the first unambiguous post-edit candidate build and language-skewed syntax/type/API diagnostics. First-patch token usage is unavailable. |
| Repair amplification | More failed builds/tests, edit–build cycles, diagnostic volume, cached input, and commands after the first patch |
| Familiarity/comprehension candidate | More observable inspection/search commands before the first mutation even when the first post-edit build succeeds. This can also reflect task ambiguity, source organization, or strategy; pre-edit reasoning tokens are unavailable and training familiarity requires a separate intervention. |
| Toolchain/project obligations | Extra project-file operations or harness evaluator latency, concentrated in tasks such as the multi-file refactor. Candidate build duration is unavailable; E2 supplies controlled timing. |
| Context pollution | Cannot be established from fresh-per-task v3; requires the persistent-context experiment below |

The first report is descriptive and hypothesis-routing. It must not use post-hoc
p-values, cached-token totals, or stage trends to declare a mechanism or estimate
the context-scale slope.

**E1 exit:** every retained task reconciles to its artifact hashes and
task-boundary commits; every completed command event receives zero or more
versioned multi-label classifications plus an explicit ambiguous/unparsed
disposition; diagnostic and repair rules are covered by redacted fixtures for
every actual v3 event shape and bounded compound/redirection equivalence class;
candidate
activity is separated from harness evaluation; and every unsupported temporal,
interaction, context, source-exposure, evaluator-volume, or intermediate-patch
field is `null` with a reason. The report identifies only which mechanisms are
observable and which require new treatments.

### E2 — Model-free language/toolchain baseline

Under the exact pinned environment, build and evaluate all 18 controlled
states: the clean baseline and each of eight cumulative canonical gold stages
for each language. Materialize states through the validated manifest/gold
helper, verify every cumulative case and workspace check, and hash each source
tree before timing. Candidate-produced states are not inputs to E2.

Use exactly five paired rounds per state and no adaptive extension. Check in and
hash a deterministic interleaved language/stage order before execution so one
language or stage is not always first. Each round uses a fresh temporary
workspace with no `bin` or `obj`, followed immediately by one repeat in that
same workspace. Call these **fresh-workspace** and **repeat-workspace** results,
not machine-cold and machine-warm: the OS page cache is not controlled.

The checked-in E2 manifest must expand the exact project path and preserve these
literal command shapes:

```text
dotnet restore <project> --nologo
dotnet build <project> --configuration Release --no-incremental --no-restore --nologo
dotnet run --project <project> --configuration Release --no-build
```

Feed the run command the exact cumulative JSONL cases and apply the same
workspace checks as the benchmark evaluator. Repeat build/run immediately in
the same workspace; do not repeat restore. Keep the pinned global package cache
constant, disable external network access, do not clear the OS cache, and record
toolchain/environment identity plus basic host-load metadata. Record full
stdout/stderr byte counts while keeping their text outside Git. Actual compiler
input/module counts are `null` unless the command output directly supports
them; report static source/project compile obligations separately rather than
adding a binary-log subsystem.

Record restore time/output only for the fresh-workspace regime. Record build,
run/evaluator, and output measures for both regimes, plus a fresh-workspace
restore-through-evaluator composite. Specifically report:

- fresh-workspace restore wall time and both-regime build/run/evaluator wall time;
- build wall time plus static project/source obligations; internal compiler-phase timing remains `null` unless directly exposed;
- emitted warnings;
- statically declared source/module obligations and any directly observed compile records;
- output volume;
- final artifact size where useful.

This estimates ecological toolchain cost independently of model behavior. Do not subtract it mechanically from agent time: compile latency can alter agent decisions and retry behavior. Report it as an explanatory pathway.

Audit candidate-visible obligations task by task. In particular, record that F# multi-file compile order may require explicit project-file edits while ordinary C# SDK source discovery does not. The primary estimand is:

- **ecological language-stack cost** (language plus idiomatic toolchain obligations).

A **controlled-core representation cost** variant that neutralizes project
mechanics is deferred to a separately reviewed mechanism treatment.

**E2 exit:** all 18 source states match their reviewed hashes, all five paired
rounds and both workspace regimes complete without integrity error, every
cumulative evaluator invocation passes, and the report contains timing/output
distributions, project/source obligations, environment/load metadata, and an
explicit missingness ledger. Any failed gold evaluation or changed environment
fails the baseline rather than being silently rerun.

### E3 — Minimal controlled mechanism pilot

Only after E1–E2 and review, define a new scientific specification using matched
**gold predecessor snapshots** so each task starts from identical intended state
rather than inherited candidate drift. Task 001 starts from the clean canonical
baseline; Task `n` starts from the canonical cumulative gold state after Task
`n-1`. Hash each language-specific predecessor, verify all prior cumulative
cases and matched public obligations, exclude the current task's successor gold,
and never mount future gold, evaluator cases, or obligation maps inside the
candidate boundary. Use one preregistered model/scaffold configuration initially
and a small task set spanning simple change, type/validation logic, and
multi-file/API work.

Evaluate three modes:

1. **Comprehension/localization:** use a read-only workspace and an enforced source-inspection allowlist; forbid build, test, execution, writes, and network. Produce a structured list of relevant files/symbols, invariants, and planned changes. Score outside the candidate boundary with a frozen, blinded, language-neutral obligation map that accepts reviewed equivalent implementations.
2. **One-shot patch:** use the same read-only inspection boundary, then accept exactly one controller-applied multi-file diff. The candidate cannot execute builds/tests or receive compiler/test feedback. After the response ends, the controller applies the diff once and performs the frozen build/evaluation. Measure aggregate output/reasoning, first-pass correctness, and diagnostic categories.
3. **Monolithic agentic repair:** the current inspect–edit–compile/test–repair loop. Measure total trajectory and repair amplification.

All three modes start from the same predecessor and hold task text, visible
source, model, reasoning effort, limits, and environment fixed; mode-specific
tool authority is the intended treatment. The controller must enforce the
read-only/one-diff boundaries rather than relying on prompt compliance.

The contrasts answer different questions:

```text
comprehension mode      -> semantic recovery / localization
one-shot mode           -> generation and first-pass language ability
full agent mode         -> ecological cost after feedback and repair amplification
full minus one-shot     -> approximate repair-loop contribution (descriptive, not literal subtraction of independent components)
```

Do not run a large factorial initially. E1-informed task selection makes this a
non-counting mechanism pilot: use it to choose the next causal treatment and
derive variance, not as a confirmatory mechanism estimate. Treat full-versus-
one-shot differences as paired mode contrasts, not literal subtraction of
independent cost components. Stop after two repeated apparatus failures of one
class.

### E4 — Causal decision gate

After E1–E3:

- **F# excess dominated by failed compilation/type/syntax repair:** prioritize compiler-feedback and isolated-repair harness experiments.
- **F# excess accompanied by more pre-edit inspection with similar first-pass accuracy:** treat familiarity/comprehension as a candidate mechanism and prioritize a separately reviewed documentation/familiarity or retrieval intervention.
- **Gap concentrated in project-file/build obligations:** separate ecological and controlled-core studies.
- **Boundary source/proxy size and task-level aggregate input co-vary across stages without corresponding observable repair or exploration growth:** treat this only as a static/scale candidate and route it to Workstream H.
- **No stable attribution:** replicate only if the required sample remains scientifically and economically worthwhile; otherwise publish the ambiguity and apparatus limits.

## Workstream F: test context containment and repair delegation

This workstream is conditional on E showing meaningful repair/tool-output amplification. It is a **harness experiment**, not part of the pure language treatment.

### Why routing matters

A monolithic persistent agent may accumulate raw compiler diagnostics, test output, failed patches, and repair reasoning. A repair worker can keep this material out of the strategic orchestrator’s context. That may improve later decisions even if total system tokens do not fall.

A prompt telling an agent to “use a subagent” is not sufficient for causal inference. The harness should enforce separate processes/contexts and account for each independently.

### Initial routing design

Use the same model for orchestrator and repair worker first, so routing is varied without simultaneously changing model capability. Compare a compact 2 × 2 design:

- memory: fresh orchestrator per task vs persistent orchestrator across the chain;
- repair routing: inline/monolithic vs isolated repair worker.

This yields:

| Condition | Meaning |
|---|---|
| Fresh + inline | Controlled inline baseline; within-task repair only |
| Fresh + delegated | Tests within-task context containment |
| Persistent + inline | Tests cumulative tool/repair pollution and long-horizon degradation |
| Persistent + delegated | Tests whether isolated repair preserves strategic context |

Use the same deterministic repair controller in both routing arms. Hold the
initial orchestrator patch boundary, build/test schedule, diagnostic generation,
retry count, and repair budget fixed. On the same controller-detected failure:

1. **Inline:** return the raw frozen diagnostic payload to the orchestrator for its repair turn.
2. **Delegated:** give that identical payload to one ephemeral worker; return only a frozen controller-generated summary to the orchestrator.

The worker receives the full candidate-visible workspace, task, and current
diff by default. A smaller input is permitted only through one preregistered,
candidate-blind deterministic selector shared across languages—never an ad hoc
“relevant files” choice. Gold and evaluator material remain unavailable. Raw
worker transcripts and diagnostics are not inserted into orchestrator context
unless a preregistered semantic-escalation condition is met. The current
autonomous harness may be reported as an external ecological reference, but it
is not substituted for the controlled inline arm.

A later practical arm may use a cheaper repair model, but only after the same-model routing effect is understood.

### Routing outcomes

Report separately:

- total system input/output across orchestrator and all workers, summed without treating cached input as additional input;
- orchestrator-only input, output, and context/compaction telemetry where exposed;
- worker cost and number of repair attempts;
- controller toolchain time/output, summed agent-process time, and end-to-end wall time as separate non-additive measures;
- raw diagnostic/tool-output volume withheld from the orchestrator;
- correctness, task survival, and late-chain decision quality;
- escalations and semantic regressions;
- F#/C# interaction with memory and routing.

A useful routing result may be:

- lower orchestrator context and better late-task decisions;
- unchanged or higher total system cost;
- a smaller F#/C# gap in the orchestrator but a persistent gap in total worker cost.

That would show mitigation of strategic-context pollution without pretending the underlying language/tooling burden vanished.

Before any Workstream F specification, define late-chain decision quality only
through preregistered objective outcomes such as evaluator correctness, escaped
regressions, task survival, and late-task repair burden. Do not introduce a
subjective post-hoc quality score.

### Routing stop rules

Do not build a general multi-agent framework. Implement only the minimal explicit controller needed for the four reviewed conditions. Reuse the existing runner/environment. If symmetric controller behavior or separate per-agent usage cannot be audited, stop rather than inferring it; otherwise label the result a bundled harness intervention, not a routing effect. No recursive subagents, dynamic model routing, or autonomous planner hierarchy is authorized in the first study.

## Workstream G: registered ecological cost replication

A registered successful-chain cost replication remains useful, but it follows causal telemetry rather than preceding it.

Use canonical descriptive F#/C# repositories and configuration-specific strata. Primary outcomes should include:

1. full-chain correctness;
2. paired full-chain total input under the frozen harness;
3. first-pass compile rate and repair-cycle burden;
4. paired agent-process time;
5. per-task/cumulative trajectory curves.

Total input is interpreted as **ecological model input processed over the trajectory**, not unique context size. Predeclare a practical-equivalence margin only after review of the mechanism metrics. Keep v3 calibration excluded.

If a delegated harness becomes the practical target, report it as a separate harness stratum rather than silently replacing the monolithic baseline.

## Workstream H: test the original context-density hypothesis at scale

The current repository is too small to test whether concise source preserves agent memory. Build one medium matched repository before creating many repository families. Pilot multiple repository/context sizes until retrieval or compaction pressure is observable.

Measure:

- repository and candidate-visible token size;
- relevant-file/symbol recall and precision;
- unique versus repeated source/tool-output exposure where measurable;
- maximum/terminal orchestrator context and compaction events where exposed;
- fresh versus persistent context;
- monolithic versus delegated repair;
- task success and cost as maintenance depth grows.

The predicted semantic-density crossover is supported only if F# becomes relatively cheaper or more reliable as repository/context pressure increases after repair/tooling/familiarity pathways are controlled or modeled. A small-source one-shot cost difference cannot establish that claim.

## Overall next-step sequence

```text
E0 independent review
  -> E1 forensic attribution of existing v3 traces
  -> E2 model-free toolchain/obligation baseline
  -> E3 bounded comprehension / one-shot / repair pilot
  -> E4 mechanism decision
  -> F harness memory/routing experiment when justified
  -> G registered ecological cost replication
  -> H medium-scale context-pressure experiment
```

## Scientific claims permitted by possible outcomes

- **More F# repair loops:** current models have greater first-pass or toolchain difficulty in F# under the tested setting.
- **More F# pre-edit exploration:** familiarity/comprehension is a candidate pathway, but training familiarity is not identified without a separate intervention.
- **Delegation helps orchestrator but not total cost:** context containment improves strategic agency while repair burden remains real.
- **F# gap shrinks under persistent delegated work or at larger scale:** harness/context interactions matter and simple small-task rankings are misleading.
- **F# remains costlier across modes and scale:** current language/tool/model ecology favors C# under those tested conditions.
- **No stable difference:** stochastic/configuration effects dominate language in the measured regime.

None supports a universal language ranking without broader models, scaffolds, repositories, and time periods.

## Gate

E0 is approved. The next bounded task is **E1 only**: implement and validate the
deterministic archive analyzer, fixtures, and transcript-free report under the
identity, observability, classifier, privacy, and exit contracts above. Close
independent implementation review and exact-commit Linux/Windows CI before
using the report. Stop after E1 is closed; E2 is a separate continuation. No
new model call, subagent framework, or scientific cell is authorized yet.
