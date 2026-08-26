# Literature review

Search date: **2026-08-26**

## Review question

Does prior work already measure the lifetime computational cost of maintaining semantically equivalent software in different programming languages with fresh coding-agent contexts?

The review searched combinations of: programming language, coding agent, token cost, repository maintenance, software evolution, context retrieval, multilingual issue resolution, functional programming, low-resource languages, compiler feedback, code compression, and longitudinal/chained tasks. We followed references and benchmark repositories from the closest papers. This is a scoped narrative review, not yet a PRISMA systematic review.

## Evidence map

| Work | Language comparison | Repository scale | Inherited sequence | Fresh-agent/context cost | Matched external behavior across languages | Main contribution |
|---|---:|---:|---:|---:|---:|---|
| Tokenmaxxing (2026) | Yes: Python, Java, Rust, OCaml | Small contest repositories | No | Full trajectories, chiefly output-token cost | Parallel problems, not maintained repositories | Language changes agent token expenditure and repair behavior |
| MultiPL-E / MultiPL-T | Many languages | Function-level | No | No long-lived agent process | Parallel translated tasks | Multilingual generation and low-resource transfer |
| Multi-SWE-bench / SWE-bench Multilingual | Yes | Real repositories | No | Agent trajectories vary by implementation | No: different repos and issues per language | Multilingual issue resolution |
| ContextBench | Eight languages | Real repositories | No | Context recall, precision, and efficiency | No | Process-level context retrieval evaluation |
| SWE Context Bench | Nine languages | Related issue sequences | Experience reuse, not inherited code evolution | Time and token efficiency | No | Retrieval/reuse of prior task experience |
| SWE-Chain | Python only | Real packages | Yes, release transitions inherit prior agent code | Agent outcomes over chains | No cross-language treatment | Continuous release-level maintenance |
| SWE-EVO | Python only | Large real projects | Long-horizon tasks | End-to-end agent performance | No | Large evolution tasks |
| RepoMod-Bench | Eight languages | Up to very large repositories | One modernization operation | Cost is not the language-treatment focus | Standardized interfaces, but different projects | Repository modernization and translation |
| LongCodeBench | Multiple languages/tasks | Long repository context | No | Long-context degradation | No | Context-length stress |
| FPEval | Haskell, OCaml, Scala, Java | Isolated tasks | No | Static-analysis-guided self-repair | Parallel tasks | Functional correctness, style, maintainability |
| Token Sugar / ShortCoder / Hidden Cost | Mostly code-generation/completion tasks | Snippets/files | No | Token efficiency | Semantic-equivalent transformations | Source representation and tokenizer cost |

## Findings

### 1. Language already affects agent cost

Tokenmaxxing is the closest direct predecessor. It controls task difficulty across Python, Java, Rust, and OCaml and analyzes complete coding-agent trajectories. It reports stable language-dependent token differences and attributes part of the effect to non-compiling attempts, unnecessary revision, and fallback to a familiar language. This establishes that language is an experimental treatment, not merely a stylistic choice.

Its scope is intentionally smaller than ours: contest-style tasks, no inherited maintenance chain, no matched F#/C# repository pair, and no lifetime context-recovery measure.

### 2. Multilingual repository benchmarks do not isolate language causally

Multi-SWE-bench and SWE-bench Multilingual provide realistic multilingual issue resolution, while ContextBench adds gold context and retrieval-efficiency measures. Their repositories, ecosystems, domains, issue types, and tests differ across languages. A performance difference cannot therefore be attributed cleanly to language representation.

This project uses F# and C# on the same runtime to reduce those confounds, and it supplies the same task wording and black-box behavioral oracle to both implementations.

### 3. Chained maintenance exists, but not as a cross-language treatment

SWE-Chain is the strongest overlap with longitudinal maintenance: each package-release transition inherits the code produced by earlier transitions. It is Python-only and studies package upgrades rather than matched representations. SWE-EVO similarly stresses long-horizon evolution but does not compare equivalent repositories across languages.

The present benchmark borrows the inherited-workspace idea while deliberately restarting the agent context at each step. That separates repository memory from conversational memory and measures the cost of semantic recovery by a new agent.

### 4. Context and representation have measurable costs

ContextBench, LongCodeBench, and cost studies show that repository retrieval, repeated input, and long context are material constraints. Token Sugar, ShortCoder, and Hidden Cost demonstrate that semantically equivalent source representations can change token consumption without necessarily changing correctness. TokDrift further warns that tokenization changes can alter model behavior even when program semantics are preserved.

Together these results justify recording both source-representation metrics and full trajectory cost. They also show why “fewest characters” is not an adequate objective: unfamiliar or semantically opaque compression may increase reasoning and repair cost.

### 5. Training familiarity and verification are major confounds

MultiPL-T and low-resource-language studies show that corpus scarcity substantially affects code-model performance. FPEval finds higher error rates and non-idiomatic output in functional languages, but also shows partial self-repair with static-analysis feedback. CoCoGen provides additional evidence that compiler/static-analysis feedback can improve generation.

Accordingly, the study must not interpret an F#–C# difference as pure syntax. It should separately measure model familiarity, compiler interactions, documentation/tool access, code style, and source size. F# is useful precisely because the pair shares .NET while differing in language representation and likely training frequency.

## Synthesis

The literature supports five separate propositions:

1. programming language changes agent cost;
2. repository context is a limiting resource;
3. inherited maintenance exposes failure compounding;
4. source representation and tokenization alter efficiency;
5. training familiarity and deterministic feedback mediate performance.

What remains missing is a controlled design that observes these mechanisms together over the lifetime of matched software. That is the viable gap pursued here.

## Limitations of this review

- Rapidly changing 2026 preprints may be superseded or revised.
- Search coverage is broad but not exhaustive across every digital library and non-English publication.
- Several relevant works are preprints rather than peer-reviewed final publications.
- “No prior benchmark found” is not proof that none exists; novelty should be rechecked before preregistration or submission.
- The initial pilot is too small to support claims about F# or language design; it validates measurement infrastructure only.
