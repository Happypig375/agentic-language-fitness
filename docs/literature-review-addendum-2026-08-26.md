# Literature-review addendum: matched representations

**Search update:** 2026-08-26

This addendum records two close 2026 predecessors found during an adversarial search after the main scoped review. It further narrows the novelty claim; it does not invalidate the controlled longitudinal language experiment.

## A Jagged Frontier

Mahmud et al., **A Jagged Frontier: Evaluating Robustness of Code Agents to Semantics-Preserving Transformations** (arXiv:2608.18389, 2026) is the closest published work on controlled repository representation.

The study applies semantics-preserving transformations—including control-flow rewrites, dead-code injection, and identifier renaming—to repository-level issue-repair instances. It repeatedly evaluates paired original and transformed repositories across two agent scaffolds and four models. The reported perturbation effects are usually modest but sometimes statistically significant, and robustness rankings vary by scaffold.

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
- controlled semantics-preserving repository variants: **A Jagged Frontier**;
- tokenization and semantics-preserving source transformations: **TokDrift**, **Token Sugar**, and related work.

The viable research gap is therefore only their controlled longitudinal intersection:

> No published study identified in the search treats programming language as the independent variable in a fresh-context inherited maintenance chain over semantically matched repositories while holding the runtime, ordered task sequence, external behavioral oracle, agent configuration, and trajectory-accounting protocol substantially constant.

The proposed contribution should be described as a **controlled experimental synthesis and extension**, not a new general benchmark paradigm.

## Consequences for experimental design

1. Include at least one within-language semantics-preserving representation treatment, drawing on *A Jagged Frontier*, so that cross-language effects can be calibrated against ordinary source-form sensitivity.
2. Use repeated paired runs and randomize run order; a single run cannot distinguish a language effect from agent stochasticity.
3. Analyze language × model × scaffold interactions rather than declaring one language universally superior.
4. Preserve language-neutral black-box verification, following repository-equivalence benchmarks.
5. Retain complete trajectory cost—input/cache/output/reasoning tokens where exposed, source/context reads, compiler and test loops, elapsed time, and later escaped regressions—because resolve rate alone does not answer the lifetime-economics question.
6. Re-run the close-predecessor search immediately before preregistration and submission; the field is changing too quickly for a dated novelty claim to remain reliable indefinitely.

## Revised go/no-go judgment

**Go, but only on the narrowed claim.** The current pilot is useful infrastructure for testing this intersection. It is not yet evidence of an F# advantage, and the scientific study should be abandoned or reframed if a prior matched-language inherited-maintenance experiment is found or if parallel repositories cannot be made comparably idiomatic and behaviorally equivalent.
