# Research plan

> **Canonical continuation plan.** Maintainer agents must read this file before substantial work. `AGENTS.md` is the automatically discovered entry point and routes agents here. Update this plan whenever the checkpoint, ordering, assumptions, or decision gates change.

## Current checkpoint — 2026-08-30

The project remains in **Phase 1: measurement and feasibility**.

Completed milestones:

- **A — apparatus and provenance:** strict accounting, `alf audit`, exact toolchain/container pins, fail-closed protocol validation, external raw archives, retry/failure taxonomy, and green cross-platform CI;
- **B — variance-v2:** audited calibration plus 10 counterbalanced F#/C# pairs on the original two-task chain; stochastic/order variance overwhelmed a plausible 7–8% token effect at `n=10`, and correctness was near-saturated;
- **C — benchmark recalibration:** an independently reviewed matched eight-task F#/C# chain, descriptive/deterministic representation apparatus, and the frozen non-counting `difficulty-v1` pilot.

The `difficulty-v1` pilot retained four valid primary conditions. Three completed all eight tasks; C# descriptive stopped at the frozen Task 007 structural acceptance checks. The stronger configuration is therefore no longer fully saturated. The F# deterministic candidate reintroduced descriptive aliases, making that representation observation non-interpretable under the pilot's per-protocol rule. One Williams row supports no language, representation, causal, or significance claim.

The Windows UTF-8 subprocess defect exposed by an excluded attempt is fixed and covered by regression tests. Latest pre-plan validated head `460b0f6148808ece8901742f91a350726ea9f279` passed GitHub Actions run `33276330023` on Linux and Windows, including protocol and both representation-arm validation.

Durable evidence:

- `docs/variance-v2-results-2026-08-29.md`
- `docs/workstream-c-benchmark-design-2026-08-29.md`
- `docs/representation-treatment-v1-2026-08-29.md`
- `docs/difficulty-v1-protocol-2026-08-30.md`
- `docs/difficulty-v1-results-2026-08-30.md`
- `docs/workstream-d-feasibility-design-2026-08-30.md`

Historical and retired cells remain excluded as documented. Do not pool `difficulty-v1`, `variance-v2`, the historical Luna pair, or retired attempts.

## Current decision

Proceed to **Workstream D multi-configuration feasibility by design first**. No paid/model run is authorized until the Workstream D design has independent approval, required protocol support is implemented and reviewed, CI is green, and each child cell is frozen from a clean checkpoint.

The primary language question and the unstable representation treatment are now split:

- **D-Language first:** canonical descriptive representation, F# versus C#, three capability configurations on one scaffold;
- **D-Representation later:** a separate complete Williams-superblock study with intention-to-treat as the primary representation estimand and candidate-caused drift recorded as an outcome.

This avoids a costly 2 × 2 × configuration factorial before treatment adherence and the language × capability interaction are understood.

## Immediate continuation order

### D0. Independently review the Workstream D design

Review `docs/workstream-d-feasibility-design-2026-08-30.md` for:

- scientific estimands and scope split;
- configuration-selection and reverse-order boundary-confirmation rules;
- common-exposure-prefix handling of early chain stops;
- six-macroblock counterbalancing and the predeclared 4+2 continuation gate;
- inclusion, retry, and apparatus-stop rules;
- representation intention-to-treat and drift handling;
- feasibility sample size and decision gates.

Close every P1/P2 finding before implementing protocol cells. This review is the next task. It does not authorize data collection.

### D1. Implement a feasibility-family protocol

Use three child cells under one immutable parent schedule:

1. **H — reference/high:** the existing `gpt-5.4`, medium-reasoning configuration if its exact preflight remains available;
2. **M — reduced effort:** the same model/scaffold at a lower supported reasoning effort;
3. **L — lower capability:** a lower-capability model on the same scaffold and a preregistered effort setting.

The exact exposed IDs and settings are selected only after reviewed preflight criteria. Do not silently substitute aliases or change both model and scaffold in the first family.

The parent schedule contains all six permutations of H/M/L, one per chronological macroblock. This gives each configuration two appearances in every within-macroblock position. Within each configuration, six paired blocks balance language order 3/3.

Protocol work must:

- pin each child configuration, source commit, descriptive manifest, task hashes, model/effort, CLI/image/archive, limits, network/documentation policy, and raw-retention policy;
- generate and hash the complete six-macroblock parent schedule before freeze;
- balance F# → C# and C# → F# 3/3 within each configuration;
- fail closed on configuration drift or telemetry incompatibility;
- keep candidate agents blind to research instructions.

Obtain model-free validation, independent implementation review, green Linux/Windows CI, and a clean freeze before any model call.

### D2. Run non-counting configuration calibrations

After freezing, run one audited descriptive F#/C# pair per candidate configuration.

Selection uses only preregistered difficulty/apparatus criteria, never the sign or magnitude of the language cost difference:

- H is retained as an upper anchor if apparatus-valid;
- M/L are provisionally too easy if both languages complete 8/8 without a substantive failure;
- M/L are provisionally too hard if neither reaches Task 006 or fewer than 8/16 possible task envelopes pass;
- a provisionally informative configuration has at least one chain reach Task 007 and combined completion between those extremes.

A single pair cannot replace a boundary configuration. When M/L is provisionally too easy or too hard, run a second non-counting pair in reverse language order. Replace it only if the same boundary classification repeats. All calibrations remain non-counting; replacement configurations require reviewed new child cells and freezes.

### D3. Collect the staged feasibility sample

Execute macroblocks 1–4 first. This produces four paired blocks per configuration—12 pairs and 24 language runs—with language order balanced 2/2 inside each configuration.

After auditing stage 1, continue to macroblocks 5–6 only when:

- accounting, protocol, provenance, and backend identity remain stable;
- at least one retained configuration is informative rather than uniformly saturated or impossible;
- no preregistered apparatus-stop condition has occurred.

This gate uses no F#–C# direction or effect magnitude. If it passes, complete all six macroblocks: six paired blocks per configuration, 18 pairs and 36 language runs, with language order balanced 3/3 and all H/M/L permutations represented. If it fails, close the family as a documented feasibility fragment and redesign rather than pretending the four-macroblock stage is fully balanced.

Execute the immutable parent schedule, run both languages in a pair close together, preserve every attempt, and make no outcome-driven changes inside the family.

### D4. Analyze configuration-dependent feasibility

Primary outcomes:

1. full-chain success;
2. tasks passed and first failure/stopping position;
3. task survival through 001–008;
4. unconditional cumulative input tokens and agent wall time to terminal stop;
5. paired **common-exposure-prefix** cost through the highest task both languages entered, retaining whether either failed that task.

Common-exposure-prefix cost prevents an early-stopping language from appearing artificially cheap while retaining the cost of its failing task. Report the last task both languages passed as a separate descriptive checkpoint, and report both measures jointly with terminal-stop cost and correctness.

Secondary outcomes include cached/cache-write/output/reasoning tokens, evaluator/task/run time, commands and tool calls, compiler/test interactions, file changes, observed reads/revisits, diffs, structural failures, and classified infrastructure failures.

Report configuration-specific paired differences/log ratios and language × configuration uncertainty. No pooled universal language coefficient, p-value, significance, or advantage claim is authorized from either four or six pairs per configuration.

### D5. Make the next scientific decision

After stage 1—and after the full family when continued:

- **all configurations saturated:** use lower capability or strengthen late tasks;
- **all impossible:** step capability upward or simplify the problematic task contract;
- **stable informative configurations:** complete macroblocks 5–6, then select the smallest scientifically useful confirmatory set and derive repetitions from observed variance;
- **large/sign-changing language × configuration variation:** make capability interaction central and stratify future inference;
- **configuration effects dominate unstable language differences:** reframe toward agent/configuration sensitivity;
- **representation drift frequent:** study treatment adherence as an outcome before estimating a representation effect.

No matched-repository expansion or confirmatory study begins before this decision report.

## Workstream D design constraints

The detailed normative draft is `docs/workstream-d-feasibility-design-2026-08-30.md`.

Key constraints:

- descriptive representation only in the first language family;
- same scaffold, isolation, tools, benchmark, evaluator, and policy across H/M/L;
- separate versioned child cells, not informal model switching;
- one audited non-counting calibration per candidate configuration, with a reverse-order confirmation before replacing a boundary M/L configuration;
- one complete six-macroblock parent schedule frozen in advance;
- a predeclared four-macroblock apparatus/difficulty gate, never an effect-direction gate;
- no adaptive stopping based on observed language favorability;
- candidate correctness failures remain valid outcomes;
- pre-candidate infrastructure-invalid attempts follow frozen retry rules;
- alternate scaffold comparison waits for equivalent accounting and becomes a separate matched-scaffold family;
- future representation analysis uses intention-to-treat, with drift timing/counts retained rather than silently excluding nonadherent candidates.

## Workstream D definition of done

Workstream D feasibility is complete when:

- the design has independent approval with no unresolved P1/P2 findings;
- three capability child cells and the complete six-macroblock parent schedule are cleanly frozen and auditable;
- each retained configuration passes a non-counting calibration and any boundary classification receives reverse-order confirmation;
- macroblocks 1–4 are completed and the preregistered continuation decision is recorded;
- macroblocks 5–6 are completed when that gate passes, or a preregistered redesign/stop disposition is documented;
- every included run passes audit and all raw attempts are hash-preserved;
- a feasibility report recommends confirmatory configuration(s), benchmark changes, scaffold work, representation follow-up, or a research reframe;
- no claim exceeds the feasibility sample.

## Completed workstreams

### A — apparatus/provenance: complete for frozen cells

Accounting, protocol validation, clean-freeze checks, isolation, exact environment capture, failure taxonomy, retry handling, artifact auditing, and raw archival are operational. Any new cell must still repeat review, CI, and clean freeze.

### B — variance-v2: complete

Ten balanced pairs on the original chain estimated stochastic/order variance and showed that a small language effect would require a much larger sample under that benchmark. See the variance report; do not reuse its observations as successor-chain data.

### C — benchmark recalibration: complete

The eight-task successor chain, language-neutral oracle, structural/API checks, idiomaticity/equivalence review, representation apparatus, and `difficulty-v1` pilot closed the chain-difficulty gate. See the Workstream C and difficulty documents.

## Later phases

### Phase 2 — matched repository expansion

Only after Workstream D, construct 3–5 independently reviewed paired applications at increasing sizes and architectural shapes. Each receives a preregistered 10–30-change chain with a common black-box oracle.

### Phase 3 — mechanism ablations

Separate the language label into formatting, names, type inference/annotations, idiomaticity, compiler feedback, documentation access, tokenizer fertility, source/context footprint, native training familiarity, and shared .NET transfer.

### Phase 4 — confirmatory longitudinal study

Use preregistered full chains, fresh agents, preserved repository state, hierarchical/paired analysis, and sample sizes derived from feasibility variance. Estimate creation versus maintenance cost, semantic recovery, error compounding, escaped defects, and language × capability/repository-size interactions.

### Phase 5 — generalization

Add languages chosen to separate mechanisms—such as Python, TypeScript, Rust, and OCaml—only after the F#/C# methodology is stable. The final deliverable is a mechanism map and Pareto frontier, not F# advocacy.

## Stop, reframe, or negative-result conditions

Reframe or stop if:

- prior work already performs the same controlled matched-language inherited-maintenance experiment;
- paired implementations cannot remain comparably idiomatic and behaviorally equivalent;
- provider/backend drift or measurement variance overwhelms plausible language effects;
- language differences disappear after controlling for configuration, tooling, representation quality, or order;
- cross-language differences are smaller or less stable than within-language representation perturbations;
- the required confirmatory sample is impractical relative to the scientific value.

These are useful outcomes: they may show that model/scaffold configuration, source quality, or stochastic trajectory is a stronger engineering lever than programming-language choice.
