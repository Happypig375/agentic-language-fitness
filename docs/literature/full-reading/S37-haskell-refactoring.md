# S37 — Multi-agent Haskell refactoring

**Full read, 2026-09-16:** Shahbaz Siddeeq and colleagues, *LLM-based Multi-Agent System for Intelligent Refactoring of Haskell Code*. Publisher identity DOI [10.1007/978-3-032-12089-2_26](https://doi.org/10.1007/978-3-032-12089-2_26); read [arXiv 2506.19481v1](https://arxiv.org/abs/2506.19481v1), 24 June 2025. Publisher and preprint are one work; publisher-edition equivalence is unverified.

Zotero `PKLXQNEE`: parent `6RIZBUHN`, PDF `HMR4J5CE`; 17 pages, 6,090,701 bytes, SHA-256 `b4a97aa4062208a1e9a9b63808749178543ec6207b07c440da35ac6cc2675ff0`. All pages/references, five figures and five tables consumed; figure/table pages 4–6, 8, 10–13 visually checked. No appendix in this PDF. Main-paper reading complete; artifact inspection is bounded and no experiment reproduced.

## Closest overlap

The paper describes GPT-4o agents for analysis, strategy, refactoring, verification and debugging, evaluated before/after on ten selected open-source Haskell projects. Table 1 already recommends explicit handling of every data constructor, stronger domain types, total functions and compiler warnings. Therefore functional-language agent refactoring, exhaustive patterns and warning-driven improvement are **prior art**, not inventions supplied by an F#/Codex port.

The outcomes are source size, cyclomatic complexity, branching depth, HLint/diagnostic counts, runtime and allocation. The paper describes semantic testing, but does not expose a held-out future-change comparison isolating a particular source convention. Its p. 14 limitations explicitly state that other models and existing refactoring tools were not compared. There is no same-budget single-agent arm establishing the incremental value of multi-agent organization. Future maintainability is inferred from metrics rather than measured by subsequent change success.

## Result and measurement checks

Table 4's columns matter: average **8.90% is lines of code**, **9.76% cyclomatic complexity**, and **14.42% branching depth**. Some prose assigns 8.90% to cyclomatic complexity and 9.76% to branching depth. Runtime and allocation columns are 5.28% and 21.27%; the abstract's separate 14.57% allocation claim is not reconciled. Its 11.03%/22.46%/13.27% grouped summaries are approximately arithmetic averages of heterogeneous percentage metrics, not three independent behavioral gains. Do not use them as an effect estimate for future maintenance.

Figure 3 displays distributions across metric values/projects, not a stated repeated-run uncertainty analysis. Figure 4 is one illustrative function profile, not the complete reproducible ten-project performance dataset. Figure 5's factorial/sum/unused-function examples do not match all patterns named in surrounding prose. These checks restrict interpretation; they are not an experimental refutation of the system.

## Bounded released-source inspection

[Public artifact](https://github.com/GPT-Laboratory/Intelligent-Haskell-Code-Refactoring/tree/5c023c8987ec7fd8d4aaca89ce3114c482d447a8) pinned at `5c023c8987ec7fd8d4aaca89ce3114c482d447a8`; untruncated tree inspected. Fully read README, `backend/refactor.py`, `analysis.py`, `report.py` and the expert/lead prompt files. Downloaded `homplexity_analysis.py` and the Bench JSON are **not** counted as fully read. No application, LLM call, test, profiling command or author code was executed.

The current refactor function selects `deepseek/deepseek-r1` through its `model2` option, whereas the paper says GPT-4o. It combines HLint suggestions with one model call and string replacements, then records static metrics. `analysis.py`/`refactor.py` explicitly populate **placeholder** coverage and performance fields; `report.py` also has placeholder report fields. HLint severity counts and `ghc -fno-code` error-line counts are separate. These released paths do not reproduce the paper's claimed semantic verification/performance pipeline; they do not establish that the paper's original runs used placeholders or a different model. Exact experimental revision, executed tests, workloads and raw measured runs remain necessary for reproduction.

## Consequence for discovery

Reject a claim that cleaner or shorter functional code has thereby been shown easier for coding agents to maintain. Retain this source as close prior advice and a reason to demand **executed later changes, independent behavioral checks, unchanged opportunity to inspect source, and a controlled convention comparison**. Correct catch-all behavior remains valid; fewer warnings and greater explicitness are process observations, not the endpoint. D1's residual contribution can only be a bounded empirical answer about that consequential practice, with costs and cases where it fails to help. D5 cannot be justified by the Haskell paper's aggregate percentages.
