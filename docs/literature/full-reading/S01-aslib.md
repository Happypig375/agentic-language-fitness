# S01 — ASlib and the limits of selection benchmarks

**Full arXiv-v3 reading completed 2026-09-16 HKT by the main Codex AI session.** Bernd Bischl et al., *ASlib: A Benchmark Library for Algorithm Selection*. [Publisher identity](https://doi.org/10.1016/j.artint.2016.04.003); [read edition](https://arxiv.org/pdf/1506.02465v3), submitted 6 April 2016, manuscript dated 7 April 2016. The publisher body has not been compared; no edition equivalence is asserted.

## Asset and coverage

| Field | Evidence |
| --- | --- |
| Zotero | Parent `IQXQNNN7`, PDF `ZJPH5PL3`, collection `PKLXQNEE` |
| PDF | 36 pages, 698,249 bytes; SHA-256 `08d9eff968d0311cfafbf21601986424fdee7f087a01ba473bf19893119d0e1b` |
| Reading | All 36 pages, including all 121 references; no appendix. Earlier partial status is superseded only for this edition |
| Visual checks | Identity p. 1; formal definition p. 4; all five figures pp. 8, 15–17, 22; all six tables pp. 9–10, 18–19, 23–24; p. 16's plot-heavy extraction checked against the full rendered page |
| Artifact | [aslib-r](https://github.com/coseal/aslib-r/tree/bf25e92ec6efa2b37112d6a6785c25cbf6df9ec4), commit `bf25e92ec6efa2b37112d6a6785c25cbf6df9ec4`; untruncated inventory and bounded conversion, costs, imputation, CV, runner and summary source inspection |
| Limit | No R/package installation, cluster submission, model fitting or solver reproduction; current code is not identified as the publication-producing revision. The separate complete format technical report and every original scenario paper are not claimed as read |

## What the paper establishes

The paper formalizes selection as a mapping from an instance to an algorithm that optimizes expected performance over a stated distribution (p. 4). Features may be cheap static descriptors, expensive graph analyses, probing runs or historical observations; obtaining them has a cost (pp. 5–6). A one-time choice, restart schedule and online adaptive policy are already distinct established options. ALF cannot claim firstness for any of this general formulation.

ASlib release 2.0 supplies precomputed performance, features, run statuses, folds and optional feature costs for **17 scenarios across six domains** (pp. 7–13). Its reusable outcome tables avoid rerunning the underlying solvers when comparing selectors. This convenience does not reproduce the original solver experiment, provide binaries/instances for arbitrary new configurations, or automatically validate a new stochastic maintenance outcome panel.

The demonstration compares seven classification/regression/clustering approaches, using the supplied ten outer folds. SVM and forest parameters receive 250 random-search configurations and three inner folds; other settings are defaults, apart from a preliminary choice of 30 maximum XMeans clusters (pp. 19–21). Outcomes are fraction solved, PAR10 runtime and misclassification penalty. The single best reference is selected by PAR10 over **all instances in the scenario**; the virtual best picks the recorded best per instance (p. 21). Those references are descriptive hindsight comparators, not necessarily deployable policies learned only from development data.

Figure 5 reports the proportion of the single-best/virtual-best PAR10 gap closed, including negative values. Regression forests lead on 13 of 17 scenarios and average .65 on that normalization. This is not 65% lower runtime or a predicted maintenance improvement. Most scenarios were deliberately taken from publications already demonstrating complementary algorithms/selection gains (pp. 10, 21). CSP-2010 nevertheless illustrates a two-algorithm comparison sharing a common core with a strong default; shared infrastructure alone is not a new study design or proof of useful headroom.

## Controls to adopt and conventions to reject

- **Separate development from confirmation.** The primary tuned-model comparison uses nested CV. The later forward feature/algorithm subset analysis explicitly uses ordinary CV and acknowledges optimistic selected-subset estimates (pp. 22–24). ALF must not choose its rules/profiles from the same observations used to confirm their value. Repeated public-benchmark tuning is also identified as a risk (p. 25).
- **Charge the information actually used.** Feature costs can exhaust a timeout or solve the instance during probing. The paper discusses sequential feature groups and conversion-cost reuse. ALF should separately account for analysis and implementation, and treat useful probes as interventions. It does not inherit an unallocated probe arm or an arbitrary PAR10 penalty.
- **Preserve missingness semantics.** The paper imputes absent performance with the timeout and uses status information. That runtime convention does not make an unrun ALF slot, lost accounting record or blocked apparatus a candidate failure. Known behavioral failure, missing observation and invalid apparatus remain different states.
- **Keep deployable defaults separate from hindsight.** A development-selected default, both fixed packages, and an evaluation-best constant answer different questions. ALF's opportunity is conditional expected value from permitted information, not the maximum noisy realized outcome. Do not normalize a gain by an uncertain or near-zero opportunity denominator.
- **Do not select confirmation cases for observed complementarity.** Published ASlib scenarios demonstrate selection methods on a purpose-built corpus. That is useful for their declared objective; it does not establish the prevalence of profitable choices among ordinary maintenance demands. ALF retains ties, uniformly successful/failed profiles and contrary outcomes.

## Bounded artifact reconstruction

The inspected runner distinguishes real-selector feature costs from VBS/single-best costs, wraps learners for imputation, and implements outer-fold training with inner tuning. `convertPerf.R` retains a separate success mask, sets unsuccessful runtime entries to the cutoff, and **rejects repeated algorithm measurements** with `max(repetition) == 1`; `convertToLlamaCVFolds.R` also rejects repeated CV. The paper's data format can represent repetitions, while this conversion path cannot handle them. It is therefore unsuitable as an unmodified estimator for stochastic ALF repeats.

`convertToLlama.R` supplies the globally single-best label for instances unsolved by every algorithm; `convertFeats.R` removes constant features during conversion. The runner's presolving helper treats successful feature computation as part of selector evaluation, while baseline calls omit it. The separate generic imputation helper's defaults are not assumed to be the settings used by the benchmark. Static inspection supports these bounded statements, not full fold-by-fold reproduction or identification of the original runtime environment.

## Next source decisions

S06 (meta-level selection) and S16 (selection survey) remain consequential for noisy expected value, available information and broader method coverage. Rice is correctly credited as the historical origin through ASlib's explicit attribution; no novel equation is claimed and no Rice full reading is fabricated. LLAMA, the full format specification, forward-selection and individual SAT/CSP scenario papers become necessary if their machinery, exact numerical effects or particular preprocessing rules are adopted. The current qualitative selector and existing ALF runner do not adopt them.

**Uniqueness remains unconfirmed; practical value requires useful conditional differences after information cost; methodological rigor requires independent profiles, explicit missingness and uncertainty.** ASlib supplies established conventions and cautions, not a validated ALF protocol or sample-size allocation.
