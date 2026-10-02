# S203 — Spectrum-based feature comprehension

**Full final-publication reading, 2026-10-02 HKT.** Alexandre Perez and Rui Abreu, *Framing program comprehension as fault localization*, JSEP 28(10), 2016, pp.840–862, DOI [10.1002/smr.1799](https://doi.org/10.1002/smr.1799). PANGOLIN users locate exclusive implementation more successfully, report fewer false positives and finish sooner than users manually combining coverage reports. The control identifies more shared implementation. These are localization outcomes, with prepared feature labels, rather than measured repair success. A separate interactive demonstration has an unresolved correspondence between its printed accuracy formula, procedure and curves.

The existing native Zotero parent `YPBBW6XP` and note `ELS84ZMT` preceded body reading. A newly available attachment **`VQF7VDJA`**, version4826, supplies the final publisher edition: **23 pages, 2,009,449 bytes**, SHA-256 `7fa583b577d4d84ada322d9d66051835219586fdcc8cafbf3e61b20c40328c9b`. Parent version4837 was verified before this final-edition read. The attachment has no URL; its acquisition route is not inferred. All23 pages were read as text, including all55 references and printed footnotes. Sixteen pages were inspected visually: **1,3–10,12–13,15–19**. This covers all eleven figures and their panels, TableI, Algorithm1, four numbered equations and the unnumbered information-foraging expression. Pages2,11,14,20–23 were text-only. There is no appendix in this file.

The [earlier partial reconstruction](S203-feature-comprehension-partial.md) records the separate24-page institutional manuscript and failed download/screenshot attempts. The final file now closes the publication/figure access gap. It does not recover the original tutorial, scoring sheets, pair-level data or PFD run package. Received2014, revised/accepted2016 and first-online20July2016 are distinct dates; the manuscript's placeholder2014 metadata do not identify the final publication year.

## Mechanism and integration obligations

Spectrum-based Feature Comprehension uses an execution-by-component binary hit matrix and labels each execution as associated or dissociated with the selected feature. The Ochiai association for a component is `n11 / sqrt((n11+n01)(n11+n10))`: `n11` counts associated hits, `n10` dissociated hits and `n01` associated misses. `n00` does not enter the score. The classification is supplied by the analyst or a prepared test mapping; coverage alone does not supply feature intent.

Algorithm1 collects executions, classifies them, accumulates the contingency counts and produces a report. PANGOLIN adds a hierarchical Eclipse sunburst spanning project, package root, package, file, class, method and line. Color depicts the association, while navigation, hover information and editor links aid inspection. Class summaries use term weighting. Information-foraging theory motivates the presentation, but the study does not independently measure the proposed navigation mechanism.

The score is similarity to the selected observed executions, not a calibrated causal probability. A zero score cannot establish irrelevance to every future interaction or prove a semantic or temporal obligation. Instrumentation, relevant execution selection, correct labels and interpretation of shared behavior remain part of using the method.

The storage discussion distinguishes a dense matrix from accumulating counts. The latter's described storage is linear in components plus executions. Final p.846/PDF7 nevertheless prints `O(4M+N)=O(M*N)`, whereas the manuscript simplifies to `O(M+N)`. The product is a loose bound rather than the stated simplification; do not use that printed equality to infer a measured cost. The time discussion assumes comparable execution cost and gives a matrix-sized analysis bound. No separate instrumentation-overhead benchmark or total adoption-cost measurement is supplied.

## The student comparison and its reference answers

The user study involves108 software-engineering MSc students at FEUP, working as54 pairs:26 with PANGOLIN and28 with EclEmma. Attendance was mandatory during the course laboratory, with no compensation. Partners were self-selected within groups. **Allocation to the two tool groups is not specified; randomization is not established.** The authors infer at least three years of Java experience from prerequisites and describe familiarity with Eclipse/JUnit, but no prior Rhino experience.

The prepared Rhino system has28 packages,433 classes and75,170 source lines. Its441 JUnit tests cover56% of statements and45% of branches. The paper does not pin a recoverable exact Rhino version; a release-related footnote is not sufficient to assign the experimental checkout. The task is to identify classes implementing context creation, split into exclusively involved classes (T1) and shared implementation (T2). The expected sets contain three and41 classes, respectively.

The authors manually inspect the suite, restrict attention to interpreted execution and select two **test classes**, `ContinuationsApiTest` and `Bug482203Test`. Calls involving `executeScriptWithContinuations` or `callFunctionWithContinuations` exercise the relevant continuation behavior. These are not merely two individual test cases. Both groups receive the feature-associated test selection. Its preparation effort is not part of the measured task time.

Participants receive20 minutes for tutorials/preparation and up to100 minutes for the task. PANGOLIN computes the feature association and supplies its visualization/navigation; EclEmma users manually combine coverage, including intersection and difference operations. The treatment bundles automation and interface features. It does not isolate a visualization, programming language, source architecture or type-checking effect.

Many control participants fail to perform the required coverage intersection correctly. That difficulty is an observed result of the comparator workflow, not a reason to remove those participants. The authors use class-level scoring because control users struggle with finer locations. The expected class sets and prior checking are described, but the original scoring materials and their independence from the treatment's analysis remain unrecovered. Two pairs reach the100-minute limit; the text does not fully resolve coding of capped, incomplete work.

## Positive, adverse and edition-sensitive outcomes

| Reported median | EclEmma | PANGOLIN | Scope of the result |
| --- | --- | --- | --- |
| Correct exclusive classes, out of3 | .5 | 2.5 | Higher detection with PANGOLIN |
| Correct shared classes, out of41 | 35 | 13.5 | Higher detection with the control |
| False exclusive reports | 6 | 0 | Fewer with PANGOLIN |
| False shared reports | 53.5 | 1 | Fewer with PANGOLIN |
| Elapsed minutes | 60 | 50 | Shorter PANGOLIN task time |

TableI gives the following printed statistics; they have not been recomputed from pair-level observations.

| Outcome | Mann–Whitney U | Reported p | Mean EclEmma / PANGOLIN | Cohen's d |
| --- | --- | --- | --- | --- |
| T1 correct | 127.5 | 1.12e−5 | .82 / 2.27 | 1.46 |
| T2 correct | 223.5 | .00760 | 25.07 / 15.03 | .75 |
| T1 false positives | 48 | 1.03e−8 | 19.14 / 1.65 | .83 |
| T2 false positives | 130 | 2.23e−5 | 57.93 / **.88** | 1.07 |
| Time | 234 | .0120 | 64.10 / 51.23 | .66 |

**Edition discrepancy:** final TableI/PDF13 prints a PANGOLIN T2 false-positive mean of **.88**, while the institutional manuscript's extracted table prints **10.88**. Other printed statistics in that row agree. The native final edition governs the transcription above, but neither value is promoted to a verified raw-data mean. The violin plot does not recover exact observations or resolve the discrepancy. Figure6 also labels the axis `Time(s)` while the prose and reported values use minutes; its caption describes sorted times although the display is a violin plot. These presentation issues are preserved rather than silently repaired.

The defensible finding is faster, more selective localization with better exclusive-code detection and worse shared-code detection under this prepared task. An unrestricted claim of greater accuracy conceals that tradeoff. No participant implements and validates a repair as the measured outcome, and subsequent maintenance success remains unmeasured.

## Participatory Feature Detection: a separate interactive case

PFD replaces pre-existing tests with manually delimited transactions. The user starts a transaction, interacts with the application and ends it as associated or dissociated; the report updates after each transaction. This is a concrete way to obtain spectra in an interactive application without an existing test suite. Correct boundaries and feature labels remain necessary. The demonstration does not validate delayed work or external effects crossing those boundaries.

The separate case uses JHotDraw7 revision789,688 classes,65 packages and over82,000 lines; the authors report no tests in this version. One author selects triangle creation; the other, unfamiliar with its code, performs the analysis. Associated actions include creating default/custom triangles and copying a triangle; dissociated actions include changing colors, resizing and saving. This is an author-operated case, not another student experiment or independent replication.

The study first adds dissociated transactions after one associated transaction, then varies both counts. It reports higher accuracy with more dissociated traces. It also injects classification errors at probabilities .05, .10 and .50. Here the probability specifically means that a transaction **labeled dissociated actually exercises the feature**; it is not a general model of every labeling error. The plotted .05/.10 curves show modest degradation recoverable with additional traces, while .50 is much poorer. Actual user misclassification rates are unknown. Transaction order, seeds, exact selected traces and raw generating results remain unavailable.

### What the printed accuracy formula can establish

Final p.856/PDF17 defines `A = sum(epsilon_i * s_i for i in R+) / |R+|`, where `R+` contains components with **nonzero** association and `epsilon_i` is +1 for true feature implementation and −1 otherwise. Statement granularity is used. A true feature component with score zero is outside the denominator and does not directly incur a missing-component penalty. This is not recall of all required feature implementation.

There is also a reproducible algebraic discrepancy under the procedure as written. Let the first associated trace hit `M` components, of which `K` belong to the feature. With only that trace, each hit has Ochiai score1, so `A1 = 2K/M − 1`. The reported initial value near−.7 implies `K/M` near .15. Adding **only dissociated traces**, without changing the program, truth set or component selection, cannot make an initially hit component's score zero: its score is `1/sqrt(1+n10)`. Components absent from the associated trace retain zero scores. Thus `R+` stays the same size, each true component contributes at most1, and false components contribute at most0. Consequently **`A <= K/M`, approximately .15**.

Figure9 visibly rises above .8. The printed formula, fixed-one-associated-trace procedure and curve therefore do not correspond under those explicit assumptions. An additional threshold, changing report membership, a different denominator, or an unreported procedure could alter the bound; none is reconstructed from the publication. This deduction is not a re-execution of the study and does not establish misconduct or erase the separately observed student comparison. It prevents treating the PFD curve as a verified quantitative robustness/completeness result until the exact analysis is recovered.

## Bounded source and artifact checks

The final PDF spells the old package path with uppercase `PANGOLIN`. Both HTTP/HTTPS and www/bare-host variants of that exact case were tried through the web interface; all were unavailable. The earlier failed lowercase routes remain a separate access history. No permanent-absence claim follows. The current [TQRG site](https://tqrg.github.io/pangolin/) identifies a later2019 tool demonstration; its34-line text was read. The2019 publication remains an unread separate edition/lineage lead.

The public [repository](https://github.com/TQRG/pangolin/tree/d0e2e816d09491e67f10b168934efce035f6646a) is pinned to `d0e2e816d09491e67f10b168934efce035f6646a`. Its complete376-entry tree was inspected, with no truncation. A bounded source follow-up read three complete files,405 lines total, after ordinary raw downloads; Git blob identities and SHA-256 were verified:

| File below `pangolin-core/src/main/java/pt/up/fe/pangolin/core/spectrum/` | Bytes / lines | SHA-256 | What it establishes |
| --- | --- | --- | --- |
| `diagnosis/SFL.java` | 863 / 37 | `848d4a1c42d780db817d554f7125b0e60e9ceff555c92ca4e1670f79489c5147` | Contingency counts and the printed Ochiai formula, with denominator-zero scores set to0 |
| `FilteredSpectrumBuilder.java` | 2,804 / 121 | `fd63b7a5df7dca559b38cf6703b6bff064aa286d8105e227b998e759e2349192` | Node/ancestor inclusion and exclusion can construct a restricted spectrum; no reconstructed historical accuracy procedure |
| `SpectrumImpl.java` | 5,515 / 247 | `48b5eb69b13627ec74e0f3a4fbb8549e592171222f423572a86664e199a04e33` | Bit-set activities and transaction labels; empty-activity transactions are dropped by the inspected add methods |

The inspected code supports the basic score reconstruction, but it does not bind this later checkout to the2016 experiment or resolve the accuracy formula/plot discrepancy. Other source files, binaries, the later paper and original run data remain unread. No plugin was installed and no author program was executed.

## Consequence for the survey

For B01/B08/B10, this supplies a scoped positive developer result and a concrete runtime-visibility alternative, with a shared-code detection tradeoff and preparation obligations. For B07/B09/B11, a useful execution display remains distinct from complete semantic/temporal feedback. The final publication gap is closed; raw outcome verification, exact PFD analysis and the original package remain evidence gaps. Correct-maintenance benefit is an empirical question, not an access failure.

The newly available S201 professional Java/AspectJ comparison is the next consequential reading: it can qualify architectural/modularity benefits using actual maintenance tasks in a different participant population. S202's maintainer practice study and S204's industrial coupling method are accessible independent continuations; runtime, type-evolution and temporal-oracle frontiers remain open. No construction or experiment is authorized by this reading.
