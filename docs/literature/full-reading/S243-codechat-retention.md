# S243 — CodeChat-Eval: repeated refinement and retained correctness

Guoxiang (Aaron) Guo, Kla Tantithamthavorn, Neelofar Neelofar, Yuanyuan Qi and Aldeida Aleti, *CodeChat-Eval: Evaluating Large Language Models in Multi-Turn Code Refinement Dialogues*, [arXiv2606.25747v2](https://arxiv.org/abs/2606.25747v2), 30 June 2026, [DOI10.48550/arxiv.2606.25747](https://doi.org/10.48550/arxiv.2606.25747). Main-agent reading, 2026-10-04.

The study finds substantial losses of tested correctness during repeated refinements, alongside some recoveries and stronger retention by some models. It provides a useful method for separating current-instruction adherence from preservation of a function's original behavior. Its instructions adapt to each model's current code, its required function behavior stays fixed, and model budgets differ. It therefore does not estimate a source-convention effect, success on new functional requirements, or Nu's interactive-state benefit.

## Identity, acquisition and coverage

Read **all 11 pages as text and rendered pages**, sections I–IX, **seven figures, seven tables, Algorithm 1, two numbered equations and 38 references**. No appendix is present. The primary record states acceptance at ICSME 2026; the selected body remains arXiv v2. Version 1 is dated 24 June 2026 and is not separately read. A Crossref exact-title query with three returns finds no matched final publication; that limited result does not establish that no final edition exists. Scite's abbreviated/misparsed authors and January date do not override the primary metadata.

Native collection `PKLXQNEE` and top-level holdings were checked before creating parent **`IAQ38SMQ`** and note **`VN3D2I4H`**, both preceding the selected body reading. Verified local assets are:

| Asset | Native attachment and identity |
| --- | --- |
| [arXiv v2 PDF](https://arxiv.org/pdf/2606.25747v2) | **`EZBHHQHZ`**; 11 pages, **1,637,748 bytes**; SHA-256 **`068a8d823a9853c2f35579383e42ff634312415991caa4d11c44c6598bf877d7`**; MD5 `14aae08429d20d0c7373528c3e0c13e6`. |
| [Zenodo artifact](https://zenodo.org/records/18893780), DOI10.5281/zenodo.18893780 | **`2W7YIVIW`**; `CodeChatEval.zip`, **11,831,284 bytes**; SHA-256 **`3c658f0ad0d3d0d3d9ec6bccd54f89aede89dd7660eff0fcc9d678bfaec70af1`**; MD5 `91c3b44565eb2578661e7619327b8371`, matching Zenodo. Record v1 is dated **6 March 2026**, credited to Anonymous, before the selected June manuscript. |
| Archive member `CodeChatEval/supplimentary.pdf` | **`5VB5R6RJ`**; **one page, 77,430 bytes**, SHA-256 **`3434e3ba59549791575dd92fdfca91b869b153575bd8f1c0381844d78460855d`**. Entire prompt-supplement page read as text and visually; it is part of the same work. |

The archive has **410 entries /185 substantive files** after excluding directories, macOS resource forks and `.DS_Store`. Its 160 per-turn JSONL files contain generated code and instruction-adherence labels. The other 25 files include source, five notebooks, instruction catalogs, five SVGs and the supplement. The complete mechanical inventory is distinct from manual reading of every member. Raw bodies, extraction, generated programs and local manifests remain ignored; no author program, notebook cell, generated function, model or test suite is executed.

## Task and instruction-selection contract

Sections III–IV start from **164 HumanEval and 378 MBPP functions**, 542 tasks. Turn 0 generates a solution; nine follow-up turns request refinements while preserving the original signature and input/output behavior. The follow-ups cover cosmetic, structural and semantic/algorithmic scope, three turns each, in shuffled order. “Semantic” here can mean changing an algorithm or execution strategy while retaining the function's contract. “Add” concerns code features or constraints, not a new functional requirement.

The paper filters 11 of 169 instructions, retaining **158** from CodeAlignBench. Its authors review compatibility with function-level testing and classify actions using 59 verb keywords. That lexical coverage does not validate every instruction's applicability or behavioral neutrality. The released marked CSV confirms 169 rows, 158 accepted and 11 rejected. Matching accepted IDs back to the released catalog gives **24 cosmetic /62 structural /72 semantic**, and **89 Enforce /42 Prohibit /27 Transform** actions. All accepted instructions have a single effective scope. The broader bundled catalog contains 286 records, including 212 with Python in their language lists; its path to the marked 169-row subset is not independently recovered. The accepted evaluation pool is nevertheless identifiable.

For each follow-up, GPT-OSS20B checks shuffled candidates against the **current generated code**. Negative constraints require the forbidden construct to be present; positive constraints require the requested feature to be absent and applicable; refactoring/optimization have corresponding before-state checks. The first applicable instruction is selected. This creates a model- and history-dependent instruction sequence. Equal task IDs and scope balance do not give different models identical follow-up tasks. A no-applicable-instruction turn copies the preceding code and is skipped for instruction judging.

The evaluated model receives the full conversation history. The initial system prompt requests a Python implementation using the supplied signature/docstring and asks for code without explanation or tests. The default pass@1 path generates one candidate per turn and carries its first output forward. Adherence judgments are recorded but do not select a replacement or supply repair feedback. Functional testing occurs afterward through EvalPlus; its verdicts are not used to choose the next refinement or stop a trajectory. This is neither test-guided repair nor a controlled comparison against leaving the initial program untouched.

The authors justify ten total turns using a reported real-conversation length distribution. That dependency, arXiv2509.10402, remains an unread primary method; neither it nor balanced scope sampling establishes the prevalence of these refinement types in professional maintenance. Full conversation history also does not ensure that all earlier constraints remain satisfied.

## Oracles, units and model costs

The study names eight models: Llama3.1-8B, Llama3.3-70B, Qwen2.5-Coder7B/14B/32B, DeepSeekV3, GPT-5 Nano and GPT-5. Local inference uses vLLM/H100 hardware; remote services supply the other models. These are historical study configurations, not current-model recommendations or immutable service identities.

The paper describes temperature-zero generation. The released API wrappers reveal additional differences: the five evaluated Llama/Qwen wrappers specify **1,024 output tokens**, DeepSeek specifies **4,096**, and both GPT wrappers use **medium reasoning** on the default greedy path without specifying a common output-token cap or temperature. Judge calls allow up to 8,192 tokens; the local judge branch does not explicitly set temperature. Full token/call/latency logs are absent from the archive. A common ten-turn horizon is therefore not a common total resource allowance, and a stored temperature label is not sufficient to establish identical effective decoding rules.

| Endpoint | Actual meaning and boundary |
| --- | --- |
| Per-turn Pass@1 | Proportion of functions passing the selected tests at that turn, including initial failures and later recoveries. Table III reports means of 784/105 EvalPlus tests for HumanEval/MBPP, versus 10/3 original tests. More tests strengthen this selected functional oracle without making it exhaustive. The notebooks use `plus_status == "pass"`; they do not separately combine `base_status` in that expression. Missing verdict files prevent an independent check of the runner's realized statuses. |
| Mean Survival Turns, MST@10 | Length of the consecutive passing prefix beginning at turn 0, averaged over **all tasks**. Initial failures contribute zero; later recovery does not repair the prefix; continuously passing trajectories are capped at ten. The combined score is an **unweighted mean of the two dataset means**, not a pooled 542-task mean or survival conditional on initial correctness. It estimates neither uncapped lifetime nor preservation of all historical edit constraints. |
| Instruction adherence | GPT-OSS120B compares the current instruction and before/after code. Its prompt explicitly excludes functionality and includes an example where syntactically invalid code still adheres. It does not rejudge every earlier instruction. The authors' 100-sample checks report 91% applicability accuracy and 75% adherence accuracy, with Cohen's κ .709/.639. Author consensus is useful validation at that scope; no full annotation/confusion packet is released here. |
| Regression/recovery | Pass-to-Fail rates condition on the preceding program passing; Fail-to-Pass rates condition on it failing. These describe different model/history-dependent risk sets. Scope/action regressions average per-model rates; recovery bars pool both datasets per model. Recovery pie charts show the composition of successful recoveries, not recovery probabilities per opportunity. |

The judge parser maps ambiguous answers and call/parsing exceptions to `False`. Without the full judge logs, released false adherence labels cannot be divided into substantive noncompliance and operational/parse failures. Six `None` labels represent skipped follow-ups. The adherence plotting notebook includes those skipped rows in its denominator; the paper's binary contingency excludes them. These denominators should not be silently interchanged. The plotted zero at turn 0 is a placeholder for no refinement instruction, and the adherence trend test uses turns 1–9.

## Positive, null and adverse outcomes

Table IV reports relative changes in functional Pass@1 from turn 0 to turn 9:

| Model | HumanEval | MBPP |
| --- | ---: | ---: |
| Llama3.1-8B | −66.67% | −69.20% |
| Llama3.3-70B | −50.39% | −56.38% |
| Qwen2.5-Coder7B | −47.90% | −52.03% |
| Qwen2.5-Coder14B | −27.86% | −39.65% |
| Qwen2.5-Coder32B | −33.82% | −42.86% |
| DeepSeekV3 | −23.45% | −26.64% |
| GPT-5 Nano | −19.21% | −24.41% |
| GPT-5 | −20.26% | −27.12% |

The adverse trend is consequential even though it is not a causal source-convention comparison. Preserve the favorable relative outcomes too: GPT-5 has the highest reported combined MST, **6.894** (7.762 HumanEval /6.026 MBPP), versus **2.308** for Llama8B (2.439 /2.177). GPT-5 Nano has the smallest reported relative Pass@1 declines and combined MST **6.423**. Stronger initial correctness and subsequent retention both contribute to MST.

Figures 4–5 report higher mean conditional regression under semantic refinements (**.202/.232**, HumanEval/MBPP) than cosmetic (**.081/.071**) or structural (**.119/.144**) changes. Add actions have higher reported rates (**.163/.183**) than Remove (**.063/.062**) or Modify (**.095/.124**). These are useful risk descriptions under the benchmark's selection policy. Adaptive applicability, previous-success conditioning and unequal action opportunities prevent interpreting these contrasts as pure causal effects of instruction type.

Table VII finds no significant adherence trend on HumanEval; three MBPP models (Llama8B/70B and Qwen7B) have significant declines, while the other five do not. Nonsignificance is not equivalence. The notebooks apply the original Mann–Kendall test to nine or ten aggregate turn rates; no serial-dependence correction or task-cluster uncertainty is shown. Printed `.000` p-values are rounded values, not zero probabilities. The pass-rate prose appears to interchange HumanEval/MBPP aggregate labels relative to Figure 3; retain the explicitly labeled model tables rather than silently repairing those prose means.

The reported binary contingency contains **16,668 pass/adherent, 3,955 pass/nonadherent, 13,497 fail/adherent and 4,898 fail/nonadherent** follow-ups, totaling **39,018** after six skips. Own arithmetic gives φ **.088785**, agreeing with reported .089. The small aggregate association supports keeping the endpoints separate; it does not prove independence across models/tasks or eliminate judge error. The released adherence margins match this table, but its functional partition cannot be recalculated from the absent full verdict files.

Later edits sometimes repair prior failures without explicit failing-test feedback. The reported Fail-to-Pass rates range from about **5.1% to 12.6%**, highest for Qwen14B. Stored notebook summaries count **1,494** recoveries: 608 semantic, 550 structural and 336 cosmetic; 1,032 Add, 240 Remove and 222 Modify. The corresponding pie shares describe these recovered events. They do not show that an Add or semantic instruction is more likely to repair a failure after normalizing for available opportunities.

The horizon sensitivity check retains a material boundary: increasing the cap from eight to ten raises GPT-5's MST by approximately **20.0%/19.1%**. Diminishing relative increments do not establish convergence. Dynamic instruction sequences also do not eliminate possible exposure to the underlying HumanEval/MBPP problems. Neither these limits nor missing artifacts erase the observed adverse trajectories and positive recoveries.

## Bounded released-artifact correspondence

Complete source reading covers `README.md` (81 lines), `run_eval_plus.sh` (26), `1.multiturn_code.py` (419), `CodeAIP.py` (261) and `codealign.py` (448). All five notebook source exports are read: `2.1_rq1_plot` (438 lines), `2.2_rq2.plot` (233), `2.3_rq3_plot` (533), `3.sec6_1` (313) and `3.sec6_3` (372), including export cell markers. Their retained text outputs are inspected; embedded viewer metadata holds only a 50-row sample of the regression table and three-row recovery summaries, not the full functional verdict corpus. Notebook plots are not credited as an additional complete visual deck.

Partial source coverage is `MultiTurnConversation.py` **225–361 of361** and `llm_api_pipeline.py` **35–201 and297–394 of448**. Selected environment declarations bind EvalPlus0.3.1, Python3.11.14, vLLM0.13.0 and PyMannKendall1.4.3; the full environment, legacy conversation classes, unused wrappers and Slurm script are not claimed read. The archive hash binds all members; local member hashes and exact ranges remain in the ignored manifest. Passive parsing and arithmetic do not reproduce model generation or functional testing.

Own metadata/schema checks consume all **160 JSONL files /43,360 records**, representing **4,336 complete ten-turn model–task trajectories**, with 164 or 378 tasks consistently present at every turn. No duplicate task IDs, changing task sets, mismatched model/turn labels or repeated selected instruction IDs are found. The picker removes phase tags rather than unconditionally deleting an instruction, but the accepted single-scope pool and zero observed repeats mean this implementation possibility is not an observed protocol violation.

The records contain exactly **39,024 follow-ups**, with **30,165 true /8,853 false /six null** adherence labels. All 43,360 sanitization flags are true, although one completion is an empty string: the flag checks non-`None`, not executable correctness. The intended `None` fallback has a static variable-binding concern, but no false sanitization flag is observed; no published crash is inferred. Mechanical endpoint adherence calculations reproduce all 16 dataset/model percentage changes in Table VII. Generated function bodies are not exhaustively inspected or executed.

No `_eval_results.json`, `_full_log.jsonl`, complete human judge-validation packet or cumulative model-usage record is present in the inspected archive. The notebooks expect those functional-result files; their saved tables preserve reported summaries but cannot supply all missing verdicts. The artifact predates v2 and has some reused captions/section numbering, so source, saved summaries and paper are bound only at the explicitly checked points. Exact test outcomes, raw error causes, task-level uncertainty and complete costs remain reconstruction gaps; new execution is not authorized to fill them.

## Consequence for Nu and the survey

S243 strengthens B09/B12's reason to measure **retained behavior separately from successful application of the latest edit**. It supplies a concrete adaptive-refinement method, meaningful adverse functional trends and positive recovery evidence. Unlike D1, it does not add independently specified successor behavior or compare initially equivalent explicit cases and catch-alls. Its Python function tests do not check live state, subscriptions, ordering, delayed effects or interactive frame histories. No source-size, type-system, memory-retention or Nu-specific effect follows.

The next consequential primary route is retained **C05:18**, *When LLMs Lag Behind: Knowledge Conflicts from Evolving APIs in Code Generation*, DOI10.48550/arxiv.2604.09515. It can change understanding of externally changed requirements, supplied update context, executability and actual update adoption. Resolve edition/native holdings before body reading. C05's historical-instruction and verified-instruction methods remain conditional, alongside modern .NET history/tails and game-change evidence. S243's missing verdict/log files are an access/reconstruction task, distinct from unread methods and unknown Nu/D1 benefit. All construction, model and worker holds remain.

Audit **`nu_background_s243_20261004`** records one complete primary work and one bounded artifact/supplement unit, plus three metadata-only Crossref deferrals. The two credits are not two independent studies. Five decisions/30 provenance, reason and stage fields match inspected `citation_report`; zero skips or missing reasons, no linkage warning or truncation. C05's prior abstract decision is materially upgraded; unchanged retained leads and the 38 reference entries are not re-reported as newly screened bodies.
