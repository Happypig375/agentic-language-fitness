# Literature review

Search date: **2026-08-26**

## Review question

Has prior work already measured how programming-language choice changes the cumulative computation, correctness, and repair burden of coding agents maintaining semantically equivalent software through an inherited sequence of changes?

This is a scoped, reproducible narrative review rather than a completed PRISMA systematic review. The search covered arXiv, the ACL Anthology, official benchmark sites and repositories, and backward/forward links from the closest papers. Query families combined terms for coding agents, programming languages, multilingual benchmarks, repository maintenance, sequential or iterative evolution, fresh context, token cost, context retrieval, low-resource languages, compiler feedback, and code/token compression. See `search-log.md`.

## Closest work by experimental axis

| Work | Treats language as a comparison factor | Repository or project scale | Inherited multi-step state | Fresh-context condition | Behavior matched across languages | Primary focus |
|---|---:|---:|---:|---:|---:|---|
| Tokenmaxxing (2026) | Yes: Python, Java, Rust, OCaml | Small programming tasks in agent workspaces | No | Per-task fresh runs | Parallel problems | Complete agent token trajectories by language |
| MultiPL-E / MultiPL-T / MultiOOP | Yes | Function to project/class scale | No | Not longitudinal | Translated or parallel tasks | Multilingual generation and low-resource transfer |
| SWE-PolyBench / Multi-SWE-bench / SWE-bench Multilingual | Yes | Real repositories | No | Per-issue runs | No: repositories and issues differ by language | Multilingual issue resolution |
| ContextBench | Yes, eight languages | Real repositories | No | Per-issue runs | No | Context recall, precision, and efficiency |
| RepoMod-Bench / RepoTransBench | Yes | Whole repositories | One translation or modernization episode | No maintenance chain | Implementation-agnostic tests, but different source projects/language pairs | Cross-language functional equivalence and translation |
| SlopCodeBench (2026) | Language-agnostic interface; published results are not a controlled language study | Greenfield projects | Yes, iterative specification checkpoints | Workspace-only persistence is supported | Could be adapted, but no published paired-language treatment found | Code erosion and verbosity under iterative extension |
| ChainSWE (2026) | No; Python only | 54 real repositories | Yes, dependent bug-fix chains | Yes: sequential mode uses accumulated code with a fresh agent per bug | No | Failure compounding from self-generated repository state |
| SWE-Chain (2026) | No; Python only | 9 real packages | Yes, release transitions | Longitudinal agent evaluation | No | Chained package upgrades |
| SWE-CI (2026) | No; Python only | 68 real repositories | Yes, multi-round CI loop | Repeated architect/programmer rounds | No | Maintainability over long evolutionary spans |
| SWE-EVO (2025) | No; Python only | Large real projects | Long-horizon evolution tasks | One long task | No | Multi-file release-level evolution |
| SWE Context Bench | Multiple repositories, not a language treatment | Related issue sequences | Prior experience, not necessarily inherited agent code | Multiple memory conditions | No | Retrieval and reuse of prior task experience |
| Token Sugar / Hidden Cost / ShortCoder / TokDrift | Several languages | Snippets or files | No | No | Semantics-preserving source variants | Representation and tokenizer efficiency |
| FPEval | Haskell, OCaml, Scala, Java | Isolated tasks | No | Static-analysis repair loops | Parallel tasks | Functional-language correctness and maintainability |

## Findings

### 1. Programming language already has a measurable agent cost

*The Best Programming Language for Tokenmaxxing* is the direct predecessor for the language-cost question. It holds problem difficulty substantially constant across Python, Java, Rust, and OCaml, records complete coding-agent trajectories, and finds stable language-dependent token expenditure across models. Its analysis attributes cost partly to non-compiling attempts, unnecessary revisions, and prototyping in a familiar language before translating.

This establishes that language is not merely a stylistic label. However, the experiment is based on small contest-style problems rather than inherited repository maintenance, so it cannot determine whether a concise or strongly checked representation pays back over repeated future changes.

Source: https://arxiv.org/abs/2607.22807

### 2. Sequential maintenance and fresh-context inheritance are not novel by themselves

The initial project framing overstated this gap. Several 2026 benchmarks now directly evaluate accumulated software state:

- **ChainSWE** constructs dependent bug-fix chains across Python repositories and explicitly compares oracle prior fixes with sequential runs over the agent's own accumulated patches. Its sequential condition uses a fresh agent for each bug, making it especially close to this project's maintenance protocol. https://arxiv.org/abs/2607.02606
- **SlopCodeBench** repeatedly extends an agent's own prior solution under evolving black-box specifications and measures structural erosion and verbosity. Its task interface is described as language-agnostic, although published results do not provide a controlled by-language comparison. https://arxiv.org/abs/2603.24755
- **SWE-CI** evaluates long-term evolution through a multi-round architect/programmer CI loop over 100 Python tasks derived from long commit spans. https://arxiv.org/abs/2603.03823
- **SWE-Chain** chains package-release upgrades in real Python packages. https://arxiv.org/abs/2605.14415
- **SWE-EVO** evaluates large release-level evolution tasks in Python projects. https://arxiv.org/abs/2512.18470

Accordingly, this project should not claim to invent inherited maintenance, fresh-context chains, or future-change evaluation. It combines those established designs with a controlled programming-language treatment.

### 3. Existing multilingual repository benchmarks do not isolate language causally

SWE-PolyBench, Multi-SWE-bench, SWE-bench Multilingual, and ContextBench broaden repository evaluation beyond Python. They are essential evidence that agent performance and context use vary across language ecosystems. But each language is represented by different repositories, domains, issue types, build systems, libraries, and tests. A by-language difference therefore mixes language representation with repository and ecosystem difficulty.

Sources:

- https://arxiv.org/abs/2504.08703
- https://arxiv.org/abs/2504.02605
- https://www.swebench.com/multilingual.html
- https://arxiv.org/abs/2602.05892

The first experiment here uses F# and C# on .NET 10 so the runtime, standard library, package system, external protocol, task text, and black-box oracle can be held substantially constant. This does not remove every confound—compiler quality, idioms, tooling, and training exposure remain real mechanisms—but it makes the language contrast more interpretable.

### 4. Cross-language behavioral equivalence is feasible, but prior work applies it to translation

RepoMod-Bench and RepoTransBench use implementation-agnostic or executable tests to evaluate whole-repository translation across languages. They demonstrate that a common external oracle can compare implementations without exposing language-specific tests. Their treatment is a one-time translation/modernization task, not the cumulative cost of maintaining parallel implementations through the same future requirements.

Sources:

- https://arxiv.org/abs/2602.22518
- https://doi.org/10.1109/TSE.2025.3645056

This project reuses the black-box equivalence principle while changing the outcome from translation success to cumulative maintenance cost.

### 5. Context, representation, and tokenization are independently consequential

ContextBench measures context recall, precision, and efficiency during repository issue resolution; LongCodeBench shows substantial degradation under very long code contexts; and agent-cost work finds that input tokens dominate many coding-agent trajectories and vary greatly even on repeated attempts.

At the representation level, Token Sugar, Hidden Cost of Readability, ShortCoder, and TokDrift show that semantics-preserving changes to source representation or tokenization can alter token count and model behavior. These findings support measuring full trajectories rather than final source length alone: a shorter representation can still be more expensive if it is unfamiliar, ambiguous, or repair-heavy.

Sources:

- https://arxiv.org/abs/2602.05892
- https://arxiv.org/abs/2505.07897
- https://arxiv.org/abs/2604.22750
- https://arxiv.org/abs/2512.08266
- https://arxiv.org/abs/2508.13666
- https://arxiv.org/abs/2601.09703
- https://aclanthology.org/2026.acl-long.2199/

### 6. Training familiarity and deterministic feedback are central confounds

MultiPL-T shows that code models struggle on languages with little training data and that validated synthetic transfer can improve them. FPEval reports higher error rates and non-idiomatic output in functional languages, while also finding partial self-repair from static-analysis feedback. CoCoGen and execution-cost studies show that compiler/tests can improve or reshape agent behavior, but those feedback loops themselves consume time and tokens.

Sources:

- https://arxiv.org/abs/2308.09895
- https://arxiv.org/abs/2601.02060
- https://arxiv.org/abs/2403.16792
- https://arxiv.org/abs/2606.26978

An F#–C# result must therefore be decomposed rather than described as a pure syntax effect. Relevant mediators include native training exposure, shared .NET knowledge transfer, tokenizer fertility, compiler diagnostics, language-server quality, source size, idiomaticity, and the number of repair iterations.

## Defensible research gap

The viable gap is narrower than the original intuition:

> No published study found in this search treats programming language as the controlled independent variable inside an inherited, fresh-context maintenance experiment over semantically matched repositories, while holding the runtime, task sequence, external behavioral oracle, agent configuration, and measurement protocol constant.

This is best framed as a **controlled experimental synthesis and extension** of Tokenmaxxing, ChainSWE/SlopCodeBench, and implementation-agnostic cross-language testing—not as an entirely new maintenance-benchmark paradigm.

The core question is whether one-shot language rankings change when software is read and modified repeatedly:

\[
C_{lifetime}=C_{creation}+\sum_i C_{fresh\text{-}context\ maintenance,i}+C_{defects}.
\]

A language may be harder on the first patch but cheaper over many later patches, or the reverse. Existing studies do not yet identify that crossover under a matched language treatment.

## What would close the gap convincingly

A publishable study should include:

1. several independently reviewed F#/C# repository pairs, not one translated toy;
2. identical evolving specifications and external black-box tests;
3. inherited agent-written code with both fresh-context and persistent-memory conditions;
4. complete raw trajectories, token categories, tool calls, compiler/test iterations, elapsed time, and escaped regressions;
5. repeated randomized runs across multiple model families and harnesses;
6. ablations for formatting, identifiers, type annotations/inference, compiler feedback, documentation access, and idiomatic versus mechanical implementations;
7. explicit modeling of task, repository, chain position, model, and run dependence;
8. container isolation that prevents access to hidden tests and gold code.

## Limitations of this review

- The field is moving quickly; ChainSWE appeared only in July 2026, and new benchmarks may change the novelty assessment before submission.
- The search is broad but not a formal systematic review across every bibliographic database or non-English venue.
- Several closest sources are preprints rather than peer-reviewed final publications.
- “No published study found” is not proof of nonexistence; the claim must be rerun before preregistration and paper submission.
- The current two-task pilot validates infrastructure only. It provides no evidence that F# is cheaper, more maintainable, or more agent-friendly than C#.
