# Literature-review addendum: matched representations

**Search update:** 2026-08-26

This addendum records three close 2026 predecessors found during an adversarial search after the main scoped review. They further narrow the novelty claim; they do not invalidate the controlled longitudinal language experiment.

## Does Code Cleanliness Affect Coding Agents?

Trivedi and Schmitt, **Does Code Cleanliness Affect Coding Agents? A Controlled Minimal-Pair Study** (arXiv:2605.20049, 2026), is the closest predecessor for the claim that source representation changes agent computation.

The study constructs minimal-pair repositories that match on architecture, dependencies, and external behavior but differ in static-analysis violations and cognitive complexity. It evaluates 33 tasks across six pairs through hidden public-surface tests, with 660 Claude Code trials. Code cleanliness does not materially change pass rate, but cleaner variants use roughly 7–8% fewer tokens and cause 34% fewer file revisitations.

This already establishes all of the following:

- behaviorally matched repository pairs;
- controlled source-quality variation;
- hidden black-box verification;
- repeated coding-agent trials;
- token and navigation-cost effects even where correctness is unchanged.

Accordingly, this project must **not** claim novelty for showing that maintainable or semantically clearer code can reduce coding-agent computation.

The remaining distinctions are that the minimal-pair study:

- varies cleanliness within a language rather than programming language;
- evaluates independent tasks rather than an ordered inherited maintenance chain;
- uses one agent product rather than testing language × model × scaffold interactions;
- does not compare cumulative creation, recovery, repair, and escaped-defect cost over a codebase lifetime;
- does not exploit a shared-runtime language pair such as F#/C# to control ecosystem variation.

This paper should become a primary methodological template. Its minimal-pair construction and file-revisitation metric are directly relevant, and its effect size provides a useful starting point for feasibility and power calculations.

Source: https://arxiv.org/abs/2605.20049

## A Jagged Frontier

Mahmud et al., **A Jagged Frontier: Evaluating Robustness of Code Agents to Semantics-Preserving Transformations** (arXiv:2608.18389, 2026) is the closest published work on controlled repository robustness under semantics-preserving source changes.

The study applies transformations—including control-flow rewrites, dead-code injection, and identifier renaming—to repository-level issue-repair instances. It repeatedly evaluates paired original and transformed repositories across two agent scaffolds and four models. The reported perturbation effects are usually modest but sometimes statistically significant, and robustness rankings vary by scaffold.

This establishes that all of the following already exist together:

- repository-level agent evaluation;
- behavior-preserving matched code variants;
- repeated paired runs that separate representation effects from stochasticity;
- controlled source-level transformations;
- model × scaffold interaction analysis.

Accordingly, this project must **not** claim novelty merely for showing that semantically equivalent source representations can change coding-agent performance.

The remaining distinctions are that *A Jagged Frontier*:

- varies source form within a programming language rather than changing programming language;
- evaluates isolated repair instances rather than an inherited ordered maintenance chain;
- focuses on resolve-rate robustness rather than cumulative token, context-recovery, compiler/test-repair, time, and escaped-defect cost;
- does not use a shared-runtime F#/C# contrast to study lifetime language economics.

Its paired-variant protocol should inform this project’s representation-ablation phase. In particular, language effects should be compared with within-language transformations so that a measured F#/C# difference is not overinterpreted as a uniquely linguistic effect.

Source: https://arxiv.org/abs/2608.18389

## RepoZero

Zhang et al., **RepoZero: Can LLMs Generate a Code Repository from Scratch?** (arXiv:2605.07122, 2026) evaluates repository reproduction from API specifications using hidden black-box output equivalence. It includes cross-language constraints and sandboxed execution.

RepoZero establishes that behaviorally equivalent repository implementations and language-neutral hidden verification can be scaled beyond toy function-generation tasks. It is therefore a close methodological predecessor for the common-oracle part of this project.

It does not evaluate inherited maintenance, fresh-context recovery of an evolving codebase, or programming language as a controlled independent variable over a shared ordered task chain.

Source: https://arxiv.org/abs/2605.07122

## Updated overlap statement

The broad component claims are now all occupied:

- language-dependent one-shot agent cost: **Tokenmaxxing**;
- inherited/fresh-context maintenance: **ChainSWE** and related evolution benchmarks;
- multilingual repository evaluation: **SWE-PolyBench**, **Multi-SWE-bench**, and related work;
- behaviorally equivalent cross-language repositories: **RepoZero**, **RepoMod-Bench**, and **RepoTransBench**;
- matched code-quality variants with token/navigation accounting: **Does Code Cleanliness Affect Coding Agents?**;
- controlled semantics-preserving repository variants: **A Jagged Frontier**;
- tokenization and semantics-preserving source transformations: **TokDrift**, **Token Sugar**, and related work.

The viable research gap is therefore only their controlled longitudinal intersection:

> No published study identified in the search treats programming language as the independent variable in a fresh-context inherited maintenance chain over semantically matched repositories while holding the runtime, ordered task sequence, external behavioral oracle, agent configuration, and trajectory-accounting protocol substantially constant.

The proposed contribution should be described as a **controlled experimental synthesis and extension**, not a new general benchmark paradigm.

## Consequences for experimental design

1. Use minimal-pair methods and include at least one within-language cleanliness or semantics-preserving representation treatment, so that cross-language effects can be calibrated against ordinary source-form sensitivity.
2. Record file reads and revisitations where the harness exposes them, in addition to provider token categories.
3. Use repeated paired runs and randomize run order; a single run cannot distinguish a language effect from agent stochasticity.
4. Analyze language × model × scaffold interactions rather than declaring one language universally superior.
5. Preserve language-neutral black-box verification, following repository-equivalence benchmarks.
6. Retain complete trajectory cost—input/cache/output/reasoning tokens where exposed, source/context reads, compiler and test loops, elapsed time, and later escaped regressions—because resolve rate alone does not answer the lifetime-economics question.
7. Treat the 7–8% token effect reported by the code-cleanliness study as a plausible pilot-scale effect, not as a guaranteed language effect; use pilot variance to determine the actual sample size.
8. Re-run the close-predecessor search immediately before preregistration and submission; the field is changing too quickly for a dated novelty claim to remain reliable indefinitely.

## Revised go/no-go judgment

**Go, but only on the narrowed claim.** The current pilot is useful infrastructure for testing this intersection. It is not yet evidence of an F# advantage, and the scientific study should be abandoned or reframed if a prior matched-language inherited-maintenance experiment is found or if parallel repositories cannot be made comparably idiomatic and behaviorally equivalent.
