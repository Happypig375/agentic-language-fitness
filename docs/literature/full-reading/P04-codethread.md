# P04 - Is Agent Code Less Maintainable Than Human Code? (CodeThread)

## Identity and coverage

Shaswat Patel and colleagues, arXiv `2606.21804v1`, June 19, 2026, DOI `10.48550/arXiv.2606.21804`; Zotero `L7FG5XKP`, exact hash in [assets](assets.json). Main Codex AI reader consumed PDF pp. 1-21, including references and appendices A-D. Rendered pp. 2-3, 5-7 and 11-21 inspected: figures 1-3, A1-A3, all tables and image-based prompts. The bottom of the INCOMPLETE definition in the prompt image on p. 17 is clipped at the page boundary; its category is separately defined in table A5. Exact recovery of that prompt tail remains unavailable. Full paper read with that legibility limit; methods reconstructed, not experimentally reproduced.

Read-only artifact inspection: [repository at `158f6ab`](https://github.com/shaswatpatel123/CodeThread/tree/158f6abaadcf717f3175a8f402be7da4e8d48c76), README, complete recursive tree, `scripts/run_swebench.sh`, `scripts/utils/synthetic_chains.py`, `scripts/utils/get_instance_ids.py`, and `mini-swe-agent/src/minisweagent/config/mini_no_temp.yaml`. The released workflow differs from the paper's stated scaffold and has an unresolved producer/consumer mismatch below. No authors' scripts or candidate programs were executed.

## Counterfactual and information boundary

Each original benchmark issue becomes a two-stage chain (pp. 2-5). PR0 replaces relevant function bodies with stubs but preserves signatures. An LLM sees original source to derive detailed implementation instructions/docstrings, including algorithm steps, exceptions and edge cases (figure A1). An agent reconstructs those functions as PR1; PR2 is the original benchmark issue. HA starts PR2 from the historical human implementation, AA from an accepted agent reconstruction; HH is the historical gold patch, not recruited human labor. The same PR2 solver receives each accepted predecessor. The contrast bundles provenance and any surviving behavioral/structural differences, rather than randomizing one architecture property.

PR1 acceptance requires all original pass-to-pass tests to pass and all original fail-to-pass tests still to fail. Thus acceptance uses the *future task's tests* to select the predecessor population. It is a useful benchmark counterfactual, not universal behavioral equivalence or an admissible ALF rule for selecting live inherited histories. PR2 success requires all P2P and F2P tests. AA has only one generated predecessor and one downstream task per chain; longer compounding is a hypothesis.

Source benchmark selection is 1,687 instances to 1,377 function-editable candidates (table 1). Those are not the per-model accepted counts. Main comparisons use the intersection of valid predecessors across four models; appendix A1 reports larger model-specific accepted sets, with additional overlap restrictions for the closed models on three suites. Observations share repository, issue, model and task; treating them as independent random architectures would be incorrect.

## Execution and scoring reconstruction

Appendix C states SWE-Agent, 250 steps and US$3 per instance, high reasoning, one run per condition/model/instance. Models are Claude Sonnet 4.5, GPT-5, GLM-4.7-FP8 and MiniMax-M2.5; open models use vLLM. Evaluation uses benchmark harnesses and a specified FeatBench Harbor change. Repeated-sample uncertainty is not estimated.

The pinned artifact instead vendors and invokes **mini-swe-agent**, using Singularity, custom PR1 task text, generated initial patches and a filtered PR2 instance list. Its sample YAML has step/cost limits zero, so it is not sufficient evidence of the paper's effective 250/$3 settings. More directly, `synthetic_chains.py` ignores the supplied results argument, uses a hard-coded directory, and emits `success_all`, `success_all_reg_and_few_f2p`, and `success_all_reg_and_no_f2p`; `get_instance_ids.py` expects a key named `success`. The checked-in shell joins these files. Static inspection therefore does not establish an executable end-to-end reproduction or the exact published inclusion list. These are artifact gaps, not rerun failures and not grounds to alter the printed results.

## Effects, mechanism analysis and denominators

Table 2 reports an AA disadvantage in most shared-subset comparisons, largest reported 13.1 **percentage points** on SWE-bench Pro/GLM. Exceptions include GPT on Multilingual and Pro, Claude on FeatBench, and a MiniMax/FeatBench tie. Rounded cells and reported deltas sometimes differ by 0.1 point. These are selected two-stage package outcomes, not evidence that all generated code is harder to maintain.

The paired feature analysis retains discordant outcomes: 454 pairs, HA winning 64.3%; 405 with complete features, HA winning 64.7% (pp. 6-7, appendix B). Logistic regression includes model/benchmark effects and 12 code/task features. Input/error-contract divergence has odds ratio 1.83 (95% CI 1.15-2.92, p=.011), PR2 LLOC change 1.88 (1.02-3.46, p=.042), and leave-one-model-out task difficulty 1.42 (1.12-1.78, p=.003). Model fit is modest, McFadden R²=.069. PR2 edits are post-outcome features, the sample conditions on discordance, and feature scaling is not completely specified; these coefficients do not identify a causal mediated fraction or prospective predictor.

DeepSeek-V4-Pro assigns a primary divergence category with a fixed priority order and secondary indicators, then assesses survival and causal involvement using both patches and test-log tails. The second prompt requires a concrete failing-test/traceback witness and a divergent code line, otherwise uncertainty. This is more specific than a generic quality score, but no human calibration or intervention repair validates the inferred causal labels.

Table A4's 20.6% causal attribution is **54/262 selected divergent HA-win cases**, not 20.6% of all generated predecessors or all failures. The cohort excludes equivalent/style cases. Divergence survives unchanged in 225/262 (85.9%), partially in 19, and is rewritten in 18. Labels also include 195 noncausal, 12 unclear and one not-applicable/passed case, the last difficult to reconcile with an HA-win cohort. The broader judging discussion gives 2,517 records and 2,153 after exclusions; neither should be substituted for the 262 denominator.

Appendix A1 has additional unresolved arithmetic/reporting conflicts. MiniMax Multilingual prints N=86 with 54/52 successes but 65.9%/63.4% (those percentages imply about 82); MiniMax Pro prints N=395 and 171/150 but 42.3%/38.0% (171/395 is 43.3%). Listed A1 Ns sum to 2,560, not 2,517, although judging may have further undocumented exclusions. Main/shared, per-model, feature-complete and judged samples must remain separate; no pooled recalculated headline is warranted.

## Consequences for ALF

This is direct inherited-code counterfactual prior art. ALF cannot claim novelty for measuring downstream maintenance, comparing agent and reference predecessors, or retaining prior regression obligations. A useful narrower question would manipulate a named structural dependency while holding public behavior and task obligations fixed, with drift audited separately. It must preserve unsuccessful histories and avoid selecting them with future tests.

Adapt the explicit input/error-contract taxonomy, uncertain causal labels and code-plus-test witnesses as proposed diagnostics. Require an independently reviewable rule and human calibration before presenting an automated label as mechanism evidence. Keep all attempts and report selection/attrition denominators. Neither this study nor the released artifact establishes that Nu's MMCC/ImSim packages represent broad programming paradigms.
