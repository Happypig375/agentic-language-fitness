# S173 — observed mutant coupling and fault sensitivity

**Full publication reading, 2026-10-02 HKT.** Thomas Laurent, Stephen Gaffney and Anthony Ventresque, *Re-visiting the coupling between mutants and real faults with Defects4J 2.0*, ICSTW2022, pp.189–198, DOI [10.1109/ICSTW55395.2022.00042](https://doi.org/10.1109/ICSTW55395.2022.00042). On a selected337-fault Java cohort,272 faults have at least one mutant coupled to the fault under the observed tests. Both mutation tools contribute cases the other misses. This is positive evidence about a particular mutant/test relationship, distinct from a correlation between mutation score and future fault detection or a measured repair benefit.

Native Zotero **`IM8RL7LX` / note `P9CVNVQ3` / PDF `W2S6ANMC`** was verified before body reading, versions4483/4473/4437, in collection `PKLXQNEE`. The existing publisher-layout PDF has **ten pages,922,733bytes**, SHA-256 `046affb3f67082ea2f9dcc57beb8d2d46ce0ac9e48806c5dcdc540fe1b5103ec`. All ten pages, all sections and23 references were read. Visual pages **1,3–8** cover all six figures, six tables, operator examples and the page8 footnote; pages2,9,10 are text-only. There is no appendix. The publisher DOI web route remains unavailable; it does not prevent the existing native full reading. No author tool or experiment was executed.

## The relation being measured

A triggering test passes against the fixed program and fails against the historical faulty program. Mutation is performed on the fixed program, restricted to classes changed by the known fault patch. A test kills a mutant when it passes on the fixed original and fails after the mutation. The paper calls a mutant coupled when only triggering tests detect it.

For a finite inspected test pool, the intended useful relation can be written `nonempty K(m) ⊆ F`, where `K(m)` is the set of tests killing mutantm and `F` the set exposing the real fault. This is directional: observed tests killing that mutant also expose the real fault. It does not say that every fault-detecting test kills the mutant, that every mutant is useful, or that the implication holds for inputs outside the test pool. The nonempty requirement distinguishes an observed witness from vacuous inclusion by an undetected mutant.

At least one such mutant is an **existence result** for a fault under a pool that already contains a triggering test. It does not quantify a test generator's probability or cost of finding that mutant's useful tests. Nor does a high aggregate mutation score necessarily include the few coupled mutants. The authors explicitly distinguish their question from S170's score/fault-detection correlation and the later test-size methods.

## Population, suites and tools

Defects4J2.0.0 supplies835 reproducible faults from17 projects with buggy/fixed revisions, patches and developer suites. This study retains337 faults from15 projects. It uses Major1.3.1 at the Java AST level and Pitest1.5.2 at JVM bytecode level. Pitest is integrated into the framework, including an EvoSuite plugin; duplicate Pitest operators are filtered. TableII describes nine Major operators and TableIII the reported Pitest transformations. These include control, arithmetic, value, call and switch changes. They are not a calibrated distribution of Nu/F# semantic, lifecycle or external-effect failures.

The authors attempt five EvoSuite1.0.6 and five Randoop3.1.0 suites per fixed program, with different seeds and up to three generation attempts per seed. Generation targets the classes identified by the known fix. After flaky-test filtering, they report7,641 suites for831 faults. They then describe excluding suites without a triggering test, combining developer suites and retaining only faults with enough suites. Both mutation tools must operate on the same surviving suite set; faults below five valid suites are removed. Final reported size is2,828 suites for337 faults.

The intermediate text says423 faults have at least five suites, totaling3,013. The released `count_bugs_triggering_suites` instead identifies423 faults with **at least one** generated triggering suite. The printed423→337 transition cannot be interpreted literally as nested filtering of at-least-five cohorts while losing only185 suites: removing86 such faults alone would remove at least430. The [artifact reconstruction](S173-coupling-artifact-check.md) confirms the final337/2,828 counts and two raw coupling counts, but retains this intermediate-unit discrepancy. Chart-2f's raw map includes three retained suites absent from its triggering-test list, so the printed suite filter and released observations do not fully correspond.

Mutation matrices record individual test outcomes and are aggregated across the suites per fault/tool. Identical test pools make the two tools more comparable within the retained cohort. Shared faults, classes and repeated suites remain related observations. Tool failures, generation success, triggering tests and flakiness restrictions condition the population;337/835 is not the fraction of all faults that mutation detects.

Execution uses heterogeneous HPC nodes. The authors deliberately do not record mutation runtime. More generated mutants imply more work to consider, but no measured tool-speed ratio, net testing cost or developer burden is available.

## Positive results and their denominators

| Observed category | Faults out of337 |
| --- | ---: |
| Coupled to mutants from both tools | 199 |
| Major only | 38 |
| Pitest only | 35 |
| Neither | 65 |
| Either tool | 272 (80.7%) |

Major therefore couples237 faults and Pitest234. Their similar totals conceal different covered cases, so the complementarity finding is useful. It does not establish an interchangeable operator set or one uniformly superior tool. The pinned `report.csv` reproduces these four categories, every project's fault count and all TableIV descriptive values to printed precision.

TableIV conditions **separately on coupling for each tool**, yielding237 Major and234 Pitest rows. Median mutant counts are300 and990.5; median coupled counts4 and9. Mean per-fault coupled proportions are3.56% and3.02%, with medians1.67% and1.12%. These conditional means are neither an overall fraction of mutants nor an expected real-fault detection rate. The printed maxima41.67%/37.5% are exceptional cases, not typical effectiveness.

Figure2 divides coupled mutants among operators. Figure3 addresses the different denominator of mutants produced by each operator. The released operator tables reproduce the leading coupled shares and Figure4's exclusive-fault counts, while Figure3's leading bars align with **covered-mutant**, rather than all-generated-mutant, denominators. Eleven Major total-count rows and one Major coupled-count row do not reconcile between the two released tables; all Pitest rows do. These are bounded correspondence limits, not grounds to discard the reproduced fault-level result.

Figure4 identifies faults whose coupled mutants all come from one operator within a tool: Major ROR29,COR28,STD15,LVR9,AOR2; Pitest RemoveConditional7,NonVoidMethodCall5,UOI5,VoidMethodCall4,CRCR2,ROR2 and five single-fault operators. These counts describe exclusive contributions in this population. Removing an operator with little exclusive contribution does not establish no cost to other faults, mutant interactions or future inputs. No optimized operator-selection intervention is evaluated.

## Location, non-coupled faults and null evidence

Coupled mutants are reported closer to patch lines: average77.96 lines versus343.3 for non-coupled mutants, with wide distributions. Figure5 removes outlier marks for readability; TableV retains maxima903/3,238. This is not an experimentally varied distance effect. Mutation already targets changed classes, and a known patch supplies the reference location.

For within-fault distance comparisons, only97 faults have at least20 coupled and20 uncoupled mutants. Ninety-two comparisons have unadjusted `p < .05`; the paper reports Cohen'sd−.55. This supports an observed proximity pattern in the eligible subset. It is not evidence from92 independent projects, nor a universal location-based selection policy. The remaining faults and unreproduced raw-distance calculations remain separate.

Non-coupled faults have smaller plotted patches, with a **nonsignificant** Mann–Whitney result `p = .1`. Released patch rows reproduce medians6 versus4 changed lines for coupled/non-coupled faults, with maxima225/38. Preserve the descriptive direction and inconclusive comparison rather than promoting the abstract's smaller-patch wording into an established effect.

TableVI reports that all272 coupled faults and58 of65 non-coupled faults have at least one mutation on patched lines; seven non-coupled faults do not. Thus location coverage alone does not imply coupling. Additional or different operators are a plausible continuation, but their completeness and practical benefit were not tested. The observation pool, oracle and existing operator semantics can all matter.

## What the result can support

The paper acknowledges the clean-program assumption and uses the fixed version because its full assertions must initially pass. Test generation and mutation both use known fixed code and patch locations. This is legitimate retrospective proxy investigation; it does not establish the information available while repairing an unknown successor defect. S188's old-source/successor-test distinction remains relevant.

Under the described procedure, discarding a suite because it lacks a fault-triggering test can also discard mutant-killing tests that would disconfirm `K(m) ⊆ F`. That is a logical sensitivity of the relation to observation selection, not a measured correction to the80.7% rate. The raw Chart-2f check shows such non-trigger-list suites contributing kill observations, so their removal cannot be assumed from the prose. Own set arithmetic reproduces its10 coupled mutants and Closure-50f's25, corroborating the report while leaving the selection documentation and one operator-table row unresolved.

For **B07/B12**, retain the positive evidence for targeted mutant witnesses and complementary tools alongside the65 uncoupled faults. Separate mutant existence, test-generation success, score correlation, suite selection and independent behavioral validity. For **B06/B10**, runtime and maintenance benefit remain unmeasured despite a concrete implementation and data contribution. Ordinary mutation operators do not automatically probe finite observation, pending work, subscription lifetime, retained state or irreversible effects.

S166, S170 and S176 ask related but different questions. Their positive trigger, conditional-selection and cross-model findings can coexist with this observed coupling relation and its selection limits. None establishes a D1 convention benefit, a complete temporal oracle or a measured Nu effect. No experimental hold changes.

**Next consequential action:** return to acquired S132's longer scanner/parser development experiment to balance the type/evolution evidence beyond small API tasks. S168/S169/S174/S175/S177/S178 remain concrete oracle/method dependencies; the S187 review and game/runtime/persistence frontiers remain open. The selected S173 publication is complete, while its artifact correspondence and any broader empirical benefit retain their stated limits.
