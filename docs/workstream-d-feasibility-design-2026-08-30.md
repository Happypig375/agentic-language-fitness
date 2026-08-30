# Workstream D multi-configuration feasibility design

**Status:** independently reviewed and approved design; no paid/model run is authorized by this document.

**Date:** 2026-08-30

## Motivation

The completed `variance-v2` cell showed that the original two-task benchmark was nearly saturated and that stochastic/order variation overwhelmed a plausible 7–8% token effect at ten pairs. The completed `difficulty-v1` pilot then showed that the new eight-task chain is no longer saturated: three of four retained primaries completed the chain, while C# descriptive failed the frozen Task 007 structural acceptance checks.

The difficulty pilot also exposed a separate problem. The F# deterministic candidate reintroduced descriptive aliases, so the representation treatment did not remain intact. Carrying the full language × representation factorial across several model configurations would therefore multiply cost before the primary language question or the treatment-adherence estimand is settled.

Workstream D should first determine whether the language comparison is feasible and stable across capability configurations. Representation becomes a separate follow-up family.

## Scientific scope

### Primary feasibility question

Does the direction, magnitude, variance, or failure pattern of the F#–C# comparison materially change across agent capability configurations when the repository representation, tasks, runtime, evaluator, scaffold, and protocol are held fixed?

This is not a universal-language ranking and is not a confirmatory effect estimate.

### Secondary feasibility questions

- Which configurations produce informative rather than saturated or impossible task survival on the eight-task chain?
- Do configuration differences dominate language differences?
- Does language interact with chain position, especially the structural/API tasks 007 and 008?
- Are token, wall-time, navigation, compiler/test, and correctness outcomes directionally consistent?
- Can the same frozen accounting/provenance apparatus support multiple configuration cells without backend or telemetry drift?

## Split the language and representation studies

### D-Language: first family

Use only the canonical **descriptive** successor representation. Factors are:

- language: F# / C#;
- configuration: three capability configurations;
- task/chain position: 001–008;
- language order and chronological macroblock.

This is the ecologically relevant language comparison and avoids informative loss of representation integrity.

### D-Representation: separate later family

Do not include deterministic representation in the first multi-configuration family. A later representation study must use complete four-row Williams superblocks and preregister treatment adherence explicitly.

Its primary representation estimand should be **intention-to-treat**: assignment of the starting representation remains the treatment even if the candidate later introduces descriptive identifiers. Candidate-caused drift is a post-treatment outcome—record first drift task, count, persistence, and affected roles—rather than a reason to drop that run from the primary analysis. A per-protocol analysis may be reported only as secondary and potentially selected. Do not re-transform candidate code between tasks; an enforced-retransformation intervention would be a different treatment.

## Configuration family

Keep the scaffold, Codex CLI/image, isolation, task chain, descriptive manifest, tool access, network/documentation policy, and resource limits constant in the first family. Vary capability before varying scaffold.

Define three child cells after probing what the frozen CLI/provider currently exposes:

1. **H — reference/high:** the existing `gpt-5.4`, medium-reasoning configuration if it remains available and passes the exact preflight. It is an upper anchor even if it is close to saturation.
2. **M — reduced effort:** the same model and scaffold at a lower supported reasoning effort. This changes one capability control while preserving model family and training familiarity.
3. **L — lower-capability model:** a lower-capability model on the same scaffold and a preregistered reasoning setting. Freeze the exact provider-exposed identifier; do not substitute a later alias inside the cell.

If a proposed configuration is unavailable or fails preflight, define a new reviewed child cell. Do not silently replace it. An alternate scaffold is deferred until it can expose comparable usage/accounting and run the same isolated protocol; it should later be tested as a separate matched-scaffold family with the model/settings held constant.

Each configuration is a separate versioned child cell with its own clean freeze, resolved manifest, image/archive verification, calibration, raw archive, and report. A parent family definition records the three cells and a shared macroblock schedule. Never pool cells merely because their displayed model names are similar.

## Non-counting configuration screening

After design review and implementation, run one audited non-counting F#/C# descriptive pair for each candidate configuration. Configuration selection must use only preregistered difficulty and apparatus criteria—not the sign or size of the F#–C# token difference.

- H remains the upper reference if apparatus/accounting are valid.
- A candidate M/L configuration is provisionally too easy if both chains complete 8/8 without a substantive acceptance or behavioral failure.
- It is provisionally too hard if neither language reaches Task 006 or fewer than 8 of the 16 possible task envelopes pass.
- It is provisionally informative when at least one chain reaches Task 007 and combined completion lies between those extremes.
- Any protocol, accounting, authentication, provider, host, evaluator, or archive failure follows the frozen retry/disposition policy and cannot be used for configuration selection.

A single stochastic pair is too weak to replace a boundary configuration. If M/L is provisionally classified as too easy or too hard, run one additional non-counting pair in the reverse language order under the same child cell. Replace the configuration only if the same boundary classification repeats. This confirmatory calibration is still non-counting, and selection remains independent of the language cost direction.

## Formal feasibility schedule

The parent schedule contains **six chronological macroblocks**, using every permutation of H/M/L exactly once. The per-configuration language directions are fixed in advance:

- H: F#→C#, C#→F#, F#→C#, C#→F#, F#→C#, C#→F#;
- M: C#→F#, F#→C#, F#→C#, C#→F#, C#→F#, F#→C#;
- L: F#→C#, C#→F#, C#→F#, F#→C#, C#→F#, F#→C#.

The exact 18-slot schedule is:

| Macroblock | Configuration | Language direction |
|---:|:---:|:---:|
| 1 | H | F#→C# |
| 1 | M | C#→F# |
| 1 | L | F#→C# |
| 2 | M | F#→C# |
| 2 | L | C#→F# |
| 2 | H | C#→F# |
| 3 | L | C#→F# |
| 3 | H | F#→C# |
| 3 | M | F#→C# |
| 4 | H | C#→F# |
| 4 | L | F#→C# |
| 4 | M | C#→F# |
| 5 | L | C#→F# |
| 5 | M | C#→F# |
| 5 | H | F#→C# |
| 6 | M | F#→C# |
| 6 | H | C#→F# |
| 6 | L | F#→C# |

For the specified table, the canonical schedule SHA-256 is
`3bc3eaab8cc61097f59b098dc7753a9d452374d45438a31b8f465d85a56c1bd1`.

The freeze artifact MUST state, hash, and validate all 18 assignments. Its canonical hash input is the UTF-8 bytes of newline-delimited ASCII records in table order, with a final newline and no header: `mb<macroblock>|<configuration>|<direction>`, where direction is `F#>C#` or `C#>F#`. The resulting SHA-256 is recorded in the parent and each child definition; any assignment, order, or direction mismatch fails closed. Model-free validation must confirm that macroblocks 1–4 contain 2/2 directions per configuration, all six macroblocks contain 3/3 per configuration, every macroblock mixes directions, and the overall schedule contains 9/9 directions.

```text
H M L
M L H
L H M
H L M
L M H
M H L
```

Across six macroblocks, each configuration appears twice in every within-macroblock position and every ordered configuration pair is balanced. Within each configuration, language order is balanced across six paired blocks:

- three F# → C#;
- three C# → F#.

The maximum completed family therefore contains 18 paired blocks and 36 language runs, plus non-counting calibrations.

### Predeclared 4+2 feasibility gate

The first stage executes macroblocks 1–4: four paired blocks per configuration, 12 pairs total. After auditing that stage, make one predeclared continuation decision using only apparatus stability and configuration difficulty—not the sign, magnitude, or apparent favorability of any F#–C# contrast.

Continue to macroblocks 5–6 when:

- accounting, protocol, provenance, and backend identity remain stable;
- at least one retained configuration is informative rather than uniformly saturated or impossible;
- no apparatus-stop condition has occurred.

Stop and redesign rather than completing 5–6 when every retained configuration is saturated, every retained configuration is impossible, or a material apparatus/configuration change is required. The stage-1 observations remain a documented feasibility fragment and are never represented as a complete balanced family.

The preceding qualitative description is superseded by this deterministic Boolean gate. The stage-1 analysis population is the first protocol-valid candidate outcome for all eight scheduled language slots per configuration. Retryable pre-candidate infrastructure-invalid attempts remain retained in the ledger but are excluded from this population. Every slot must be resolved and audited; otherwise trigger an apparatus stop. Calibration observations are excluded.

For each configuration, record survival/entry separately from completion. There are 64 possible task positions per configuration (8 slots × 8 tasks); an unentered position is not passed for the completion total. Let `passed_positions` be the number of positions passed by the first valid outcome in each slot. Classify deterministically:

- **SATURATED** iff all eight chains complete 8/8;
- **IMPOSSIBLE** iff no chain enters Task 006 **OR** `passed_positions < 32` of 64;
- **INFORMATIVE** iff neither prior class applies, at least one chain enters Task 007, and at least one chain fails/stops before 8/8;
- **INDETERMINATE** otherwise.

Continue to macroblocks 5–6 iff there is no apparatus stop and at least one configuration is **INFORMATIVE**. Otherwise stop/redesign. This gate never uses language contrast direction or magnitude. An unresolved or unaudited stage-1 slot is an apparatus stop, not an `INDETERMINATE` outcome. The stage-1 observations remain a documented feasibility fragment and are never represented as a complete balanced family.

If continued, the full six macroblocks become the Workstream D feasibility sample. Generate and hash the complete schedule before freezing any child cell. Run the two languages within a pair as close together as practical and record provider/quota timestamps.

Do not adapt prompts, tasks, evaluator, harness, model, effort, scaffold, limits, or schedule after inspecting outcomes. Apparatus changes require a new protocol version and new cells.

## Outcomes and estimands

Correctness and cost remain separate; cheap failure is not success.

### Primary feasibility outcomes

1. Full-chain success.
2. Number of tasks passed and first failed/stopped task.
3. Discrete task survival through chain positions 001–008.
4. Unconditional cumulative input tokens and agent-process wall time to terminal stop.
5. Paired **common-exposure-prefix** cost through the highest task both languages entered in the pair, retaining whether either failed that task.

The common-exposure-prefix estimand prevents an early-stopping language from appearing artificially cheap while preserving the cost of its failing task. Report it alongside, not instead of, full-chain outcomes and terminal-stop cost. Also report the last task both languages passed as a separate descriptive checkpoint.

### Secondary outcomes

- cached input as a component of input;
- cache-write, output, and reasoning tokens;
- evaluator, task-total, and run-total wall time;
- tool/command calls, compiler/test interactions, file changes;
- observed file reads, unique reads, and revisitations under the conservative parser;
- build warnings/errors, behavioral regressions, structural acceptance failures;
- diff/source metrics and failure taxonomy.

### Pairing and analysis

Report configuration-specific paired differences and log ratios by task, common exposure prefix, and aggregate. Show language order, macroblock, timestamp, and chain position. Use exploratory hierarchical or mixed models only to estimate variance components and interactions:

```text
outcome ~ language * configuration + order + chain_position + macroblock_time
          + (1 | paired_block) + (1 | task)
```

Use an appropriate binary/discrete-time model for task survival. Do not report a single pooled language coefficient without its configuration interaction, and do not condition all cost analysis on complete chains.

No p-value, significance, or language-advantage claim is authorized from either four or six pairs per configuration.

## Inclusion, retries, and stopping

Reuse the frozen failure taxonomy and fail-closed accounting rules. Candidate correctness failures are valid primary outcomes. Pre-candidate infrastructure-invalid attempts remain in the ledger and may be retried only under the preregistered sequential retry rule.

There is no outcome-driven early stop based on language contrasts. Stop the family only for:

- the predeclared 4+2 difficulty/apparatus gate above;
- protocol/provenance violation affecting comparability;
- invalid or changed backend/configuration identification;
- accounting schema incompatibility;
- credential/isolation failure;
- loss of the immutable image/archive/toolchain;
- an external safety or quota condition specified before the run.

After a material apparatus change, close the affected cell and begin a new version rather than resuming it under the old identifier.

## Decision report

After stage 1—and again after the full family if continued—produce a feasibility report covering:

- configuration-specific task survival and failure modes;
- paired common-exposure-prefix and terminal-stop costs;
- within-configuration stochastic/order variance;
- language × configuration interaction uncertainty;
- temporal/provider drift diagnostics;
- agreement among correctness, tokens, time, and navigation metrics;
- projected sample sizes for a future confirmatory cell;
- whether an alternate scaffold is worth instrumenting;
- whether the representation follow-up is feasible under intention-to-treat.

Decision rules:

- **All configurations saturated:** add a lower capability configuration or strengthen the late chain before confirmatory work.
- **All configurations impossible:** step capability upward or simplify the problematic task contract.
- **One or more informative configurations with stable apparatus:** complete macroblocks 5–6 if at stage 1, then select the smallest scientifically useful configuration set for confirmatory design.
- **Large or sign-changing language × configuration variation:** treat capability interaction as central and stratify confirmatory inference.
- **Configuration/scaffold variation dwarfs unstable language differences:** reframe the primary contribution toward agent/configuration sensitivity rather than a language ranking.
- **Representation drift is frequent:** study drift/adherence as an outcome before attempting a representation-effect claim.

## Implementation and review sequence

1. Independently review this design; close all P1/P2 findings before implementation.
2. Add a parent feasibility-family definition and deterministic six-macroblock schedule, or document that existing protocol machinery can validate equivalent child-cell files without extension.
3. Add model/configuration preflight and fail-closed validation for the exact reasoning/model settings selected.
4. Generate three child definitions and the shared schedule; model-free validate hashes, manifests, task identity, descriptive-only scope, limits, balance, and archive policy.
5. Commit from a clean checkpoint and obtain green Linux/Windows CI.
6. Freeze each child cell and archive its image/toolchain evidence.
7. Run and audit one non-counting pair per candidate configuration; apply only the preregistered screening rules and reverse-order boundary confirmation.
8. If configuration selection changes, review and freeze replacement child cells.
9. Execute macroblocks 1–4 according to the immutable parent schedule.
10. Apply only the predeclared apparatus/difficulty continuation gate.
11. If continued, execute macroblocks 5–6 without any protocol change.
12. Audit/archive every attempt and produce the Workstream D feasibility report before any confirmatory, scaffold, representation, or repository-expansion run.

## Definition of done

Workstream D feasibility is complete when:

- the design and analysis plan have independent approval with no unresolved P1/P2 findings;
- three capability child cells and their complete six-macroblock parent schedule are cleanly frozen and auditable;
- each retained configuration has a passing non-counting calibration and any boundary classification has reverse-order confirmation;
- macroblocks 1–4 are complete and the preregistered continuation decision is recorded;
- macroblocks 5–6 are complete when the continuation gate passes, or a preregistered redesign/stop disposition is documented;
- all raw attempts are hash-preserved and every included run passes audit;
- the feasibility report makes a documented confirmatory/reframe decision;
- no claim exceeds the feasibility sample.
