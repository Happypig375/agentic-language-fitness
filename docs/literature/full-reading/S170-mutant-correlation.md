# S170 — mutation correlation and high-score selection are different questions

## Identity, coverage and authority

Mike Papadakis, Donghwan Shin, Shin Yoo and Doo-Hwan Bae, *Are Mutation Scores Correlated with Real Fault Detection? A Large Scale Empirical Study on the Relationship Between Mutants and Real Faults*, ICSE 2018, [DOI 10.1145/3180155.3180183](https://doi.org/10.1145/3180155.3180183). Chosen [institutional PDF](https://orbilu.uni.lu/bitstream/10993/34950/1/ICSE-main18b%20%281%29.pdf): twelve pages, 1,832,762 bytes, SHA-256 `b82f326e01460fbdf9b6af13e387bfeb159e089bed90cdebe24185829577967c`. Native Zotero parent `HKDGDHKF`, PDF `5JLQKLWR`, note `DYT5HZDN`; native attachment identity/hash reverified on 2026-10-01.

All twelve pages, six figures, two tables, four footnotes and 44 references read. All pages extracted/rendered; visual checks on PDF pages 3, 4, 7, 8, 9 and 10 cover every table/figure, including dense axes and the Figure 5/prose discrepancy below. Extraction order interleaves columns/plot labels; visual inspection resolves layout, not missing analysis code. The alternate COINSE PDF returned a selected passage with a Conference 2017 placeholder header; exact file/edition correspondence and publisher binding remain unchecked. No author code, benchmark, generator or model ran.

Live B07/B12 question: does weak mutation–fault correlation invalidate useful test selection, and what does controlling suite size actually identify? This is a full-method dependency for [S165](S165-adequacy-size-methodology.md) and comparison with [S166](S166-mutants-real-faults.md), not a new ISE experiment.

## Reconstructed population and generation

Table 2 lists four C projects (Coreutils, Findutils, Grep and Make) and five Java projects (JFreeChart, Closure, Commons Lang, Commons Math and Joda-Time). The starting pools contain seventy CoreBench faults and 357 Defects4J faults. Two Make instances fail to compile and 126 Java instances exceed the one-hour suite criterion, leaving **68 C + 231 Java = 299 faults** in the main analysis. Table 1's own-study entry says 420 faults; Table 2's C rows still sum to seventy. Neither count silently replaces the exclusions and explicit 68/231 denominators in the method/results. Faults share projects and test pools; treating isolated faults as subjects does not make them independent projects.

CoreBench combines developer tests, manual triggers and generated tests inherited from earlier work. The paper reports seventy initial triggers, 96 additional manual tests and 22,208 KLEE tests. Java generation uses Randoop and EvoSuite with branch, weak-mutation and strong-mutation goals: five independent runs per configuration, 300 seconds per class and a maximum 2,000 tests per run. Twenty generated suites plus the developer suite form the pool for each fixed version. The text reports 1,375,341 generated tests. These are author-reported pool quantities, not separately verified unique test identities or an execution-cost denominator.

The Defects4J pipeline removes compilation/runtime/nondeterministic failures; fixed programs supply the basis for mutation and generation, while corresponding buggy programs supply real-fault detection. Seven familiar mutation-operator classes are used, with Major for Java and the C machinery/settings inherited from Chekam and colleagues. Exact executable/version bindings are not supplied by this reading. The treatment of equivalent mutants depends on the available composed test pools; a mutant surviving those pools is not thereby proven semantically equivalent.

This is retrospective, fault-specific analysis. The validity discussion restricts relevant tests by dependence on the faulty component and checks ten Coreutils faults with mutants on faulty or directly dependent statements. Known faults, selected components and generator goals affect the observed distribution. A high score on these pools is not a prospective score for arbitrary future faults or interactive obligations.

## Sampling, statistics and positive results

The initial analysis randomly selects **10,000 suites** with sizes from zero to 20% of the pool. The fixed-size analysis selects **10,000 suites for each size**, from 2.5% through 50% in 2.5-point increments. Resampled suites can share tests and faults. These sample counts are neither independent development attempts nor human or agent effort.

The paper fits fault detection against mutation score, size and their combined/interacting form, and compares fit measures. It reports significant contributions and improved combined fit, but low overall explanatory power. The exact pseudo-`R²` convention, complete fitted coefficients and out-of-sample validation are not established by the paper. A better in-sample fit is not independently validated future-fault prediction.

Across its projects, the reported uncontrolled correlations are commonly about .35–.75 and the fixed-size correlations about .05–.20. This supports a large size-associated change **under this sampling procedure**. It does not establish that size dominates every testing workflow or that fixed-size selection identifies a universal causal architecture effect.

The crucial positive result uses another estimand. For each size, the top 25% or 10% of suites by mutation score are compared with all randomly sampled suites of that size. Higher-scoring suites can detect more faults despite a weak overall correlation. The same-sized baseline includes the high-scoring subset; the exact handling of that overlap in the stated chi-squared probability/interval calculation is not available. It would be inappropriate to assume two independent groups without checking the implementation.

Figure 4 and its discussion concern **138/231 Java and 59/68 C faults with statistically significant improvements**. The other 93 and nine cases lack evidence for a significant improvement; that is not evidence of zero effect. The reported average gains of 8%/11% for Java and 18%/46% for C, respectively for top 25%/10%, appear in this selected-case discussion. The figure defines probability *differences*, but the exact averaging across faults and size groups is not reconstructed. These values must not be presented as an unconditional population mean or a cost-normalized effect.

Equal test counts are not equal generation, execution, inspection or mutation-analysis costs. This comparison also chooses from pre-existing scored suites; it does not directly measure the cost of building a high-scoring suite prospectively. Still, the observed positive selection result is substantive counterevidence to dismissing the method merely because its correlation is weak.

## Behavioral similarity, sensitivity checks and unresolved reporting

Section 5.1 compares each mutant's kill vector with the known real fault's detection vector using Ochiai/cosine similarity over available tests. It contrasts the maximum per fault with all mutants. Few mutants have high similarity; roughly 1% are reported above .5, while some faults have a close-matching mutant. A mutant unrelated to one known fault can remain relevant to an unknown fault, a limit the authors explicitly acknowledge. “Irrelevant” in this calculation is not proof of global uselessness.

The prose says half of the data have maximum similarity at least .9. Figure 5's Java median is visibly below .9, approximately .7, whereas the C median is around .9. Do not repeat that sentence as a verified statement about both datasets; the precise aggregation/source of the discrepancy remains unresolved.

Section 5.2 correlates correlation coefficients with high-score improvements **only where improvements were significant**. This selected analysis can show that the metrics are not interchangeable; it does not validate their relationship over all faults. Its coefficient paragraph also leaves the mapping of the second numerical set to the 10% comparison unclear, so this reconstruction does not relabel those numbers.

Sensitivity checks use developer-only and generated-only pools, an expanded developer-only Java analysis excluding five very slow faults, a small relevant-mutant subset and PIT with two generator suites. The five-fault footnote uses an hour *per test case*, whereas the initial 126 exclusions concern suite execution. These are different criteria. The authors report similar trends or nonsignificant differences; these checks are not independent external replications or formal equivalence tests.

The discussion calls S166's correlation “Biserial,” while S166 distinguishes point-/rank-biserial procedures. S170 reports its alternative calculation differed by less than .001, but the exact routine and stated variance rationale cannot be resolved from those labels alone. Preserve the reported sensitivity check without treating a terminology difference as a verified statistical diagnosis.

The study uses fixed programs and historical repository faults. Its authors acknowledge possible differences for buggy originals, industrial/pre-release faults and incomplete fault sets. Those limits become concrete in the newly promoted S176 replication: its primary abstract distinguishes clean regression inputs from already-buggy inputs and challenges size dominance for LLM-generated suites. S176 is a twenty-four-page acquired preprint, not yet a completed method at this checkpoint.

## Reconciliation and design implications

S166's trigger additions and selected generated suites, S170's random fixed-size subsets, and S165's goal-directed sampling ask different questions. Positive added fault sensitivity, weak conditional correlation and useful selection at the top of a score distribution can coexist. The generator, candidate pool, known-fault scope, score denominator and decision rule must accompany any validity claim.

For the Nu/ISE background, mutation can help probe oracle sensitivity without becoming a complete oracle. Independent old/new obligations, temporal/environmental triggers, test construction and observation costs still require separate evidence. Neither favorable mutation scores nor criticism of their correlation proves source-convention benefit. No empirical effect or priority claim for D1 follows.

| Criterion | Disposition |
| --- | --- |
| Unique | Proxy validation, fixed-size controls and high-score selection have substantial prior methods. ISE priority remains unconfirmed. |
| Valuable | The positive same-count selection result is useful under its scope. Prospective burden, unknown-fault transfer and Nu benefit remain unmeasured. |
| Scientifically valid | Correlation and selection effects must remain distinct; shared sampling, selected significant cases, unknown analysis implementation and edition/count discrepancies limit stronger inference. |

## Source continuation

W236–W238 and SC109 are recorded in the [search ledger](../nu-background-searches-2026-09-30.md). Four bounded original-title/artifact queries and the primary author entry did not locate an original 2018 analysis release. The entry links a PDF and BibTeX; absence there is not proof that no artifact exists. The newly found [2026 replication repository](https://github.com/drixs2050/Cov_mut_bug_detect_correlation) belongs to S176, not S170; selected search passages do not constitute package inspection.

S176 has a native record and verified PDF before continued reading. S169's evaluation framework, S174's subsumption/weighting method and S175's commit relevance remain acquired dependencies; S168/S173 remain access-limited. Earlier CoreBench, clean-original and coverage-guidance bibliography routes retain conditional status rather than being reported as newly completed. The new GBGallery title is a conditional B05/B07 game-oracle lead with only a selected reference passage inspected. Broader practice, type/evolution and runtime frontiers remain open. No theme closes and no experimental allocation changes.
