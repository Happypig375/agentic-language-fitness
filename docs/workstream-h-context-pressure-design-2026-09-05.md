# Workstream H context-pressure design

**Date:** 2026-09-05  
**Status:** Future design note. This does not supersede the current E3a specification gate and authorizes no model call.

## Question

Can a semantically denser language fit more useful software into the same model context, and does that change agent performance when a repository comfortably fits, nearly fills, or exceeds the usable context window?

The answer cannot be inferred from total agent input tokens. Those combine source, instructions, prior model output, tool results, diagnostics, and replay. Workstream H must directly control candidate-visible source and tool feedback.

## Core refinement: context pressure has two axes

Whole-repository size and task-relevant working-set size are not interchangeable.

Let:

- `W_eff` be the effective usable model context observed under the frozen model/scaffold;
- `P_fixed` be the fixed system/task/instruction prefix;
- `R_output` be the reserved output/reasoning allowance;
- `R_tool` be the controlled tool-feedback allowance;
- `B_source = W_eff - P_fixed - R_output - R_tool` be the candidate-visible source budget;
- `T_repo,L(n)` be all candidate-visible repository tokens for language `L` at semantic scale `n`;
- `T_rel,L(n,t)` be the transitive task-relevant source closure for task `t`;
- `rho_repo = T_repo / B_source`;
- `rho_rel = T_rel / B_source`.

The primary design therefore varies both `rho_repo` and `rho_rel`.

| Repository | Relevant closure | Main bottleneck |
|---|---|---|
| small | small | fixed language/model/tool overhead |
| large or over-window | small enough to fit | search and retrieval selectivity |
| near-window | near-window | long-context utilization and positional effects |
| over-window | over-window | summarization, eviction, decomposition, or external memory |

A repository that exceeds the window while the relevant closure is small is chiefly a retrieval problem. A task whose relevant closure itself exceeds the window is a context-capacity and decomposition problem even with perfect retrieval.

## Can F# fit more?

This is an empirical outcome, not an assumption. For every semantic scale, tokenize the exact candidate-visible F# and C# sources using the frozen model tokenizer and report:

```text
T_repo,F#(n) / T_repo,C#(n)
T_rel,F#(n,t) / T_rel,C#(n,t)
```

Characters, lines, and lexical units remain explanatory secondary measures. The current small successor benchmark does not demonstrate an F# token advantage; its final F# and C# token proxies were near parity.

Define semantic capacity at source budget `B` as:

```text
Capacity_L(B) = maximum semantic scale n for which T_rel,L(n,t) <= B
```

and, where meaningful:

```text
Fit advantage(B) = Capacity_F#(B) / Capacity_C#(B)
```

The ecological effect of interest occurs when the same functionality fits under `B_source` in one language but not the other. This threshold result must be accompanied by continuous performance curves, not reported as a single hand-selected crossover.

## Pressure levels

Use at least five or six preregistered levels rather than only three points. Suggested targets are fractions of `B_source`, not the advertised context window:

### Full-source levels

- small: approximately 0.05–0.10;
- moderate: approximately 0.30–0.40;
- large but comfortable: approximately 0.60;
- near-fit: approximately 0.80;
- boundary: approximately 0.90–0.95 after all reserves.

### Over-window levels

- retrieval pressure: `rho_repo` approximately 1.25–2.0 while `rho_rel < 0.5`;
- mixed pressure: `rho_repo > 1` and `rho_rel` approximately 0.8–1.0;
- decomposition pressure: `rho_rel` approximately 1.25 and, if feasible, 2.0 or more.

Exact targets must be recalculated from the effective context window actually reported by the pinned harness. The model’s advertised window is not the source budget.

## Three access regimes

### H1 — Full-source, no-tool context

Use when the complete candidate-visible repository fits below `B_source`.

- Serialize all source directly into the initial context.
- Permit no source-reading, shell, build, test, or network tools.
- Ask for a structured localization answer and/or one patch.
- Build and evaluate externally after the model response.
- Disable automatic compaction or set its threshold above the frozen request while remaining safely below the hard context cap.
- Counterbalance the prompt position of relevant modules; do not let beginning/end placement become a language confound.

This is the cleanest test of whether one language represents the same semantic system more compactly and whether the model can use that long context.

### H2 — Controlled selective retrieval

Use when the whole repository exceeds `B_source` but a useful task-relevant subset can fit.

Expose only a fixed repository map/index initially. Replace arbitrary shell access with controller-owned tools such as:

```text
list_tree()
search_symbols(query)
search_text(query)
read_chunk(file_id, start, end)
```

Controls:

- identical tool schemas and per-call token limits across languages;
- canonical, language-neutral file IDs where possible;
- fixed chunk serialization and line-number overhead;
- a fixed total retrieval-token budget or a preregistered free-budget ecological condition;
- duplicate chunks returned as short references instead of replaying their full text, while logging reread requests;
- raw tool output stored outside model context;
- no build/test feedback during the primary retrieval measurement;
- no arbitrary `cat`, `rg`, shell pipelines, or unbounded diagnostics.

The model may choose which source to retrieve. Call count, unique source tokens, repeated-read requests, and retrieval precision are outcomes, not nuisances.

### H3 — Managed over-window working set

Use when the task-relevant closure itself exceeds `B_source`.

A perfect retriever cannot place all required source in one request. The harness must therefore freeze an explicit memory policy, for example:

- model-selected chunk retention and eviction;
- deterministic LRU retention;
- structured summaries with immutable source references;
- hierarchical module/interface summaries;
- decomposed subproblems with externally retained intermediate state.

Do not silently rely on whatever compaction behavior a general-purpose agent happens to use. Compaction, eviction, summary creation, and source rereads become named experimental mechanisms with separate accounting.

## Controlling tool-call context pollution

Tool pollution can be strongly controlled, although the model’s need to request more source remains a valid outcome.

Primary controls:

1. The controller owns restore, build, test, and evaluation.
2. Dependencies are pre-restored and vulnerability audit is disabled inside the edit–compile loop.
3. Candidate-visible compiler/test feedback is absent in the full-source and retrieval-primary arms, or is supplied only through a fixed versioned diagnostic packet in a separately named repair arm.
4. Source tools have fixed per-result and total token budgets.
5. Repeated identical chunks are not resent verbatim.
6. Full raw outputs remain outside the model transcript.
7. `tool_output_token_limit`, effective context, and auto-compaction settings are pinned and recorded where the scaffold exposes them.
8. Every request records fixed-prefix tokens, source tokens, tool-output tokens, prior-model-output tokens, and total active-context tokens separately where available.

This creates a clean source/context study. A normal free-tool Codex run may be retained as a secondary ecological stratum, but it must not be pooled with the controlled arm.

## Context-window control

For current OpenAI models, the advertised model window is larger than the source budget because instructions, output, reasoning, and tools also consume capacity. Codex additionally exposes configuration for model context, auto-compaction threshold, and tool-output retention, but the experiment must verify the effective window and compaction events from the actual pinned session rather than assuming configuration equals behavior.

Two stages are recommended:

### H0 — Budget-capped apparatus pilot

Use artificial effective budgets such as 32K, 64K, and 128K to validate scaling, retrieval, eviction, and accounting cheaply. This can establish algorithmic threshold behavior but not million-token model quality.

### H1/H2 — Absolute-length validation

Repeat a bounded subset at real long-context lengths under the actual model window. Include levels below and above any provider pricing or compaction thresholds. Do not generalize a small artificial cap to absolute million-token attention behavior without this validation.

## Scalable repository family

Do not add inert filler. Construct one language-neutral semantic specification that produces or governs idiomatic paired implementations with active modules and known dependency edges.

Every added module must:

- participate in baseline behavior or invariants;
- be exercised by tests;
- be eligible to become relevant to a task;
- contribute realistic symbols, types, calls, and dependencies;
- be independently reviewed for comparable F#/C# architecture and idiomaticity.

Use at least three task families:

1. **Local:** a constant-size relevant closure hidden among increasing distractors. This tests retrieval.
2. **Distributed:** several distant modules and dependency paths are relevant. This tests architectural navigation and integration.
3. **Global:** the relevant closure grows with repository scale. This tests source capacity, long-context use, and decomposition.

A language cannot receive credit for fitting the whole repository when the task only needs one obvious file; conversely, retrieval cannot solve a genuinely global task whose required closure exceeds the window.

## Position and serialization controls

Long-context performance may depend on where relevant information appears. For direct full-source prompts:

- freeze a canonical serialization format;
- counterbalance relevant files across early, middle, and late prompt positions;
- separate prompt serialization order from language compilation order;
- preserve project/dependency metadata so reordering does not erase semantics;
- report language × scale × relevant-position interactions.

## Primary outcomes

### Representation and capacity

- exact model-token counts for full repository and task-relevant closure;
- semantic scale or number of active modules fitting in `B_source`;
- F#/C# fit-capacity ratio;
- source, project, interface, and documentation token decomposition.

### Full-context utilization

- localization accuracy;
- one-shot build and behavioral correctness;
- relevant-position sensitivity;
- output/reasoning cost at fixed semantic scale and fixed occupancy.

### Retrieval

- relevant-file and relevant-symbol recall/precision;
- unique source tokens retrieved;
- retrieval calls and repeated-read requests;
- irrelevant source tokens exposed;
- correctness per retrieved token;
- time to first relevant file and complete relevant closure.

### Context and memory

- active-context tokens per request;
- maximum and terminal context;
- fixed prefix, source, tool, prior-output, and diagnostic components;
- compaction/eviction/summary events;
- tokens dropped, summarized, and reread;
- fresh versus persistent context as separate treatments.

### Engineering outcomes

- first-patch compilation and behavioral success;
- later repair burden in a separately named feedback condition;
- regressions;
- total ecological model and tool cost.

## Analysis

The primary ecological analysis uses the same semantic scale in both languages and asks whether one implementation fits and performs better as the window boundary is approached.

A conceptual model is:

```text
outcome ~ language * scale * access_regime
        + task_family + relevant_position + order + model/scaffold
        + matched_repository/task effects
```

Report curves against both:

- semantic scale, which captures practical capacity per amount of software;
- normalized occupancy `rho_rel` and `rho_repo`, which captures model behavior at the same context pressure.

These answer different questions and must not be collapsed.

A crossover is supported only if it occurs inside the observed preregistered scale range with genuine context pressure. Do not extrapolate it from small repositories.

## Interpretation cases

- F# fits more semantic modules but performs similarly at equal occupancy: evidence for representational capacity, not superior long-context reasoning.
- F# performs better at the same occupancy: evidence that its representation is easier to use, conditional on tokenizer/model/scaffold.
- F# retrieves fewer tokens for equal correctness in over-window repositories: evidence for lower task-relevant recovery cost.
- F# remains costlier despite fitting more: fixed familiarity/generation/tool overhead dominates the tested range.
- No F# token advantage appears: the semantic-density premise fails for this repository family/tokenizer, even if lines or characters are fewer.
- A benefit appears only with controlled tools but disappears under free-tool ecology: harness/tool policy dominates the practical result.

## Sequencing

Workstream H remains downstream of E3a and the deterministic tool-policy decision:

```text
E3a first-patch/repair mechanism
  -> E3b/F0 deterministic tool policy when justified
  -> optional F1/F2 context containment
  -> H0 budget-capped context apparatus pilot
  -> H1 full-source small-to-near-window study
  -> H2 over-window controlled-retrieval study
  -> H3 over-window relevant-closure/decomposition study
```

The controlled/hygienic tool path is primary so audit, implicit restore, compiler feedback, and raw tool chatter do not swamp the language × context-pressure effect. Ecological free-tool conditions remain separately named secondary strata.

## Stop conditions

Stop or redesign if:

- F# and C# paired implementations cannot be made semantically and architecturally comparable;
- added modules are inert filler or template duplication rather than realistic active code;
- exact candidate-visible context composition cannot be reconstructed;
- the scaffold silently changes effective context or compaction policy;
- relevant-position effects dominate and cannot be counterbalanced;
- over-window retrieval tools differ materially by language;
- observed scale effects are only tool/repair effects already identified by E2a/E3 rather than source/context effects.

## Claim boundary

This design can test whether F# represents more useful software within a fixed candidate-visible context and whether that changes comprehension, patching, or retrieval as the repository crosses the context boundary. It cannot establish an intrinsic language ranking independent of tokenizer, model, scaffold, repository domain, tool policy, or implementation style.