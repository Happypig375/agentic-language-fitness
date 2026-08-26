# Research gap and contribution claim

## Corrected narrow claim

Sequential maintenance, accumulated repository state, fresh-context agent chains, multilingual repository evaluation, and token-cost analysis all already exist in the literature. This project does **not** claim novelty for any one of those ideas.

To the best of the scoped search completed on **2026-08-26**, the remaining gap is their controlled intersection:

> No published study found treats programming language as the independent variable in an inherited maintenance chain over semantically matched repositories while holding the runtime, task sequence, external behavioral oracle, agent configuration, and measurement protocol substantially constant.

The closest pieces are:

- **Tokenmaxxing:** controlled language-dependent agent cost, but on small one-shot programming tasks;
- **ChainSWE / SlopCodeBench / SWE-Chain / SWE-CI:** inherited or iterative maintenance, but not a controlled cross-language treatment;
- **Multi-SWE-bench / SWE-PolyBench / ContextBench:** multilingual repositories, but different repositories and tasks per language;
- **RepoMod-Bench / RepoTransBench:** common external behavior across language implementations, but one-time translation rather than repeated maintenance.

The project is therefore best described as a **controlled experimental extension and synthesis**, not a wholly new benchmark paradigm.

## Proposed contribution

1. **Paired-language maintenance design.** F# and C# implementations target .NET 10 and expose the same protocol, allowing identical evolving requirements and black-box cases.
2. **Cumulative language-cost measurement.** Language is compared over creation and repeated fresh-context maintenance rather than only one-shot generation.
3. **Mechanism decomposition.** Training familiarity, semantic density, tokenizer behavior, type inference, compiler feedback, idiomaticity, documentation access, and source footprint are measured or ablated instead of being collapsed into a language label.
4. **Complete trajectory accounting.** Correctness, tokens, tool calls, compilation/test iterations, wall time, diffs, and regressions remain separate observable outcomes.
5. **Open provider-neutral harness.** The same protocol can drive Codex or another command-line agent and preserves raw logs for reanalysis.

## Strongest alternative designs

The main study should compare three approaches before committing to a large custom benchmark:

- port a subset of language-agnostic SlopCodeBench problems to matched F#/C# build templates;
- construct matched .NET applications with deliberately paired architecture and shared black-box tests;
- translate/modernize an existing implementation into both languages, then apply the same future maintenance chain.

Using or extending an established benchmark would strengthen comparability, while custom paired repositories give tighter control over the .NET runtime and task semantics. A mixed design may be best.

## Falsification conditions

The novelty claim weakens materially if prior work is found that already performs a controlled by-language comparison over inherited fresh-context maintenance with matched behavior.

The substantive hypothesis weakens if:

- language effects disappear after controlling for model familiarity and toolchain feedback;
- source/context footprint does not predict trajectory cost as repositories grow;
- paired implementations cannot be made comparably idiomatic or architecturally equivalent;
- results do not replicate across model families and agent harnesses;
- any apparent savings are dominated by stochastic variation, environment setup, or evaluator artifacts;
- one-shot rankings and lifetime rankings remain effectively identical.

## What the pilot establishes

The two-task pilot establishes that:

- paired F#/C# projects can share a black-box protocol and cumulative cases;
- repository state can persist while each task receives a fresh agent process;
- builds, evaluation, diffs, logs, and available usage fields can be captured reproducibly;
- the scripted control passes end to end in CI.

It does **not** estimate a language effect, validate the semantic-density hypothesis, or justify a claim that F# is preferable. Those require larger repository pairs, longer chains, repeated randomized real-agent runs, isolation, preregistration, and power analysis.
