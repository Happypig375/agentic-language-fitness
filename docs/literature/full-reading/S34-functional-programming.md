# S34 — Functional-programming generation, style and repair

**Full read, 2026-09-16:** Nguyet-Anh H. Lang, Eric Lang, Thanh Le-Cong, Bach Le and Quyet-Thang Huynh, *Perish or Flourish? A Holistic Evaluation of Large Language Models for Code Generation in Functional Programming*. [arXiv 2601.02060v1](https://arxiv.org/abs/2601.02060v1), 5 January 2026; DOI `10.48550/arXiv.2601.02060`. Primary PDF/arXiv correct Scite's attribution of Eric as Evan Lang. No publication equivalence asserted.

Zotero `PKLXQNEE`: parent `KLVL5BID`, PDF `ADNSMCJJ`; 18 pages, 594,856 bytes, SHA-256 `e0e619215b655503472b7ed8298f3f6d22762ec101531ef0745e3736ba42bc77`. All pages, references, appendices A–G, two figures, nine tables and code/prompt listings consumed; figures/tables and consequential examples visually checked. Main-paper reading complete; model runs and test-oracle validation not reproduced.

## Purpose, mechanism and observations

FPEval/FPBench uses 721 public LeetCode problems, 184 easy/346 medium/191 hard, with Haskell/OCaml/Scala templates and a Java comparison. Python-derived input generators add private cases. One generated solution per task is classified by tests, compilation and timeout. Separate static tools and keyword rules define code cleanliness and an imperative-pattern indicator. These are operational metrics; future maintenance changes were not executed. The authors explicitly limit generalization to iterative evolution and industrial repositories (p. 9).

The paper reports generation differences across three GPT labels and improvement from repair, with several reversals between ordinary and instruction-guided repair. Cleanliness is evaluated among passing solutions, whose membership changes by model/repair. Consequently the reported conditional proportions cannot identify whether a fixed set of programs became easier to maintain, nor establish a correctness–maintainability causal tradeoff. Unknown training exposure cannot be inferred from language comparisons or the chronological plot alone.

Instruction-guided repair combines diagnostics with language-specific advice. In Table 8, the exhaustiveness advice explicitly permits adding missing cases **or a catch-all**. This establishes an existing diagnostic-repair strategy, not observed evidence that catch-alls caused behavioral failure. Generic type feedback, stylistic prompting and functional-language repair are prior art.

## Checks and limits that affect reuse

- **Denominators and labels:** Table 1's Haskell GPT-3.5 pass rate is 14.15%, whereas prose says 14.5%; its GPT-4o/GPT-5 Scala rates are 38.83%/58.36%, while prose assigns the OCaml values 36.20%/52.16% to Scala. Table 4's original counts do not uniformly equal Table 1 percentages times 721: Haskell GPT-3.5 reports 93 versus approximately 102, Haskell GPT-5 287 versus approximately 305, Scala GPT-3.5 118 versus approximately 139. Do not import an unreconciled effect or sample size.
- **Style construct:** Haskell `let`, `if` and pure list operations are not by themselves mutation or imperative semantics. Classifying them as such cannot establish reward hacking or technical debt. Domain-appropriate use of state/effects is not measured by demanding maximal stylistic purity.
- **Examples are not reference implementations:** The displayed preferred OCaml example references `row` inside its own nonrecursive binding; the Haskell alternative changes the recursion and lacks a check of the required equal-score condition. These are source-level observations, not executed counterexample tests. Neither example is adopted as an oracle.
- **Oracle:** Appendix A specifies generated inputs, but independent validation of all expected outputs and constraints is not established by the main paper. The exact exclusion/repair populations and per-task transitions need raw records before causal or paired claims.
- **Model identity:** The paper labels GPT-5 and describes reasoning disabled. The current pinned artifact maps the `gpt-5` option to `gpt-5.1`; the separate basic-repair file also names `gpt-5.1`. This does not establish which model produced the paper's tables. Freeze actual response model/version and parameters in any later study.

## Bounded artifact inspection

[FPEval](https://github.com/thanhlecongg/FPEval/tree/ba40e99dff2bba0c776be55da3a74cac9c5b3823) pinned at `ba40e99dff2bba0c776be55da3a74cac9c5b3823`; untruncated tree inspected. Fully read README, Haskell imperative checker, OCaml quality checker and OCaml instruction-repair script; inspected model-construction lines in `assistants.py` and basic GPT repair. Other downloaded files are not claimed fully reconstructed; no pickle, author code, container or model was executed.

The Haskell checker uses raw regular expressions, including ordinary `let` and `if`, without semantic validation. The OCaml quality script selects records when `pass_count > 8`, rather than verifying all recorded tests; its final clean/issue grouping depends on compiler and Dune results, while collected formatting flags do not enter that grouping. Whether this implements the table's exact population is unresolved. The instruction-repair script contains the catch-all advice and the same threshold-based classification. These concrete differences restrict replication claims; they do not invalidate every observation in the paper.

## Consequence for question discovery

Reject a contribution framed as first functional-language LLM repair, first use of type feedback, or proof that cleaner code is more maintainable. D1/D5 can remain candidates only as **behavioral evolution** questions with a real maintainer decision, common observable requirements and independent tests. Treat added catch-alls, defaults, type weakening and warning suppression as possible patch pathways; allow correct alternatives and do not equate their presence with failure. If claiming that a convention helps future changes, execute those changes under a fixed policy rather than substitute lint scores.

The Haskell-refactoring source S37 is promoted to test closer maintenance claims. Generic code-quality, Haskell completion and synthesis references remain conditional unless their mechanisms enter the recommended comparison. Reconstructing one paper's limitations is not evidence of ALF's uniqueness or validity.
