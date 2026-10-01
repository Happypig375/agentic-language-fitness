# S200 — Concern scattering and defects

**Full publication reading, 2026-10-02 HKT.** Marc Eaddy, Thomas Zimmermann, Kaitlin D. Sherwood, Vibhav Garg, Gail C. Murphy, Nachiappan Nagappan and Alfred V. Aho, *Do Crosscutting Concerns Cause Defects?*, IEEE TSE 34(4), July/August 2008, pp.497–515, DOI [10.1109/TSE.2008.36](https://doi.org/10.1109/TSE.2008.36). The final nineteen-page journal edition reports positive concern-scattering/bug associations in three Java systems, including fitted analyses addressing size. It neither observes an intervention reducing scattering nor establishes its net maintenance benefit.

Existing Zotero parent `5RLF5HMP`, note `5INWPP3V` and PDF `GA6NBKWA` preceded this reading. The [ICSE2009-hosted final copy](https://www.cs.uoregon.edu/events/icse2009/specialSessions/Do%20Crosscutting%20Concerns%20Cause%20Defects.pdf) is **3,222,584 bytes**, SHA-256 `43bc074182fd7899451cee6a479848c2e76a8ad4ae898f6914e8b5fea787040f`. All nineteen pages were read as text and visually, including seven figures, seven numbered tables, seven numbered equations, two worked DOS calculations, eighteen numbered footnotes, sixty-five references and biographies. The appendix notice on printed p.513 points to external material; reading that notice is not reading the external archive. The [bounded supplement check](S200-concern-scattering-artifacts.md) records three acquired packages, actual file coverage, descriptive reconstruction and a version discrepancy. No author program or experimental system was executed.

## Mechanism and operational definitions

The proposed mechanism runs from requirements through an implementation plan to scattered code that is harder to find, comprehend and update consistently. The three case studies measure code/issue associations; they do not observe those intervening developer activities. In the analysis, a concern is an item in a nonexecutable specification. Concerns form a hierarchy, program elements form a lexical containment tree, and a manually assigned relation connects them. Program containment is not inheritance.

The assignment rule asks whether an element would need removal or alteration if the concern were removed while preserving the other concerns, without redesigning the program. Configuration flags, preprocessing and generative toggles do not satisfy the intended pruning exercise. Analysts judge the dependency; they do not actually prune and validate every possible program. ConcernTagger extends Eclipse's ConcernMapper to record these assignments. The study uses classes, methods and fields, not statement-level assignments.

Concern size counts the lines in assigned elements; overlapping assignments are allowed. Whole methods and fields contribute, and the treatment of inner/anonymous classes follows containment/contribution rules. Mylyn's LOCC includes comments and whitespace; Rhino and iBATIS use source lines excluding them. These are not interchangeable denominators across systems.

CDC/CDO count the classes/methods involved in a concern. DOSC/DOSM summarize how its contributions are distributed. For a given set of eligible containers, with normalized contributions `p_t` and `n` containers, the concentration-based definition is `1 − n Σ(p_t − 1/n)²/(n − 1)`, with boundary cases requiring care. Zero denotes concentration in one container; a uniform distribution approaches one. The authors warn against directly comparing scores across programs/versions with different concern or element sets. Binary classification as crosscutting reduces to scattering for this analysis; it does not establish every semantic property discussed in aspect-oriented design.

Only leaf concerns enter the reported statistical analysis, avoiding parent rows that simply aggregate their children. **Distinct leaves may still share source elements and bugs.** The authors acknowledge that method-level aggregation, including large switch statements, can assign one bug to many concerns and bias results toward the hypothesis. Removing parent rows does not make all observations independent; the released Rhino data demonstrate the overlap directly.

## Cases, sampling and defect linkage

The authors considered 75 candidate projects and selected three with suitable requirement documentation and disciplined issue identifiers in commit messages. These are selected Java cases, not a random sample of software practice. Mylyn concerns come from feature documentation and an author's prior familiarity; Rhino concerns derive from normative ECMAScript sections; iBATIS uses reconstructed requirements based on a postimplementation developer guide. The latter does not establish that the analyzed requirements predated the implementation.

| Case as named in paper | Program and mapped coverage | Concern coverage | Issue coverage |
| --- | --- | --- | --- |
| Mylyn-Bugzilla 1.0.1, two components | 56 classes,427 methods,457 fields,13,649 LOC;44/253/230 elements and5,914 lines mapped,43% of code | 28 flat requirements, all analyzed | 110 bugs,101 mapped,92% |
| Rhino **1.5R6** | 138 types,1,870 methods,1,339 fields,32,134 SLOC;80/1,415/962 and28,308 lines mapped,88% | 480 specification concerns,417 mapped;357 mapped leaves analyzed | 241 bugs,160 mapped,66% |
| iBATIS 2.3 | 212 classes,1,844 methods,536 fields,13,314 SLOC;207/1,807/529 and13,144 lines mapped,98% | 183 reconstructed concerns,173 mapped;132 leaves analyzed | 87 bugs,47 mapped,53% |

The supplement's Rhino workbook and bundled source instead identify **1.6R5**. The discrepancy is preserved rather than silently changing the published case name. It limits exact publication-to-archive correspondence despite close agreement in correlations.

The outcome is a count of qualifying fixed issue identifiers associated with each concern, not a count of independently verified defect locations. Issue metadata exclude enhancements and retain specified fixed/closed states. The history traversal covers CVS/SVN branches and deduplicates issue identifiers. Comment/whitespace-only changes, first-version additions and commits naming multiple bug IDs are excluded under the mapping rules. Such rules reduce some false matches while also changing coverage.

A fix associates a bug with changed program elements. A concern receives that bug if any of its assigned elements intersects the fix mapping; the relation is binary, not weighted by the fraction affected. Fixes can be workarounds away from the actual defect. Mapping historical signatures onto current elements loses renamed/removed elements; a manual Rhino renaming pass recovered part of the missing mapping. Mylyn's manual/automatic bug-mapping agreement of .87 is a Jaccard comparison, not a gold-standard validation of concern assignment. Separate analysts performed its concern and bug assignments; the other bug mappings were automated.

The analysis relates a snapshot's concern mapping to earlier fixed-issue history. It is not a longitudinal intervention measuring a change in scattering before subsequent defect introduction. The claimed time ordering rests partly on the theoretical implementation-plan account.

## Positive results and size analyses

Table4 reports the following Spearman correlations with bug count. The supplied Mylyn and Rhino rows reproduce these to the precision of their rounded metrics, with the Rhino DOSM value differing in the last displayed digit. The descriptive check does not reproduce significance tests or fitted models.

| Case, analyzed leaves | DOSC | DOSM | CDC | CDO | LOCC/SLOCC |
| --- | --- | --- | --- | --- | --- |
| Mylyn,28 | .39 | .50 | .57 | .61 | .77 |
| Rhino,357 | .67 | .66 | .73 | .77 | .90 |
| iBATIS,132 | .46 | .29 | .58 | .44 | .53 |

The direction is consistently positive. Simple counts often correlate more strongly than the weighted DOS measures, contrary to the authors' expectation. Class-level versus method-level superiority is inconclusive across cases. Rhino's scope-chain concern is an illustrative highly scattered, bug-associated case, not an independent mechanism experiment. The prose's Rhino range .65–.74 does not include Table4's .77; the table and released-data comparison govern this reconstruction. Published significance statements are author claims, not independently recomputed probabilities that the substantive hypothesis is true.

Size is often the strongest correlate. The paper explicitly checks it; describing the work as merely ignoring size would be wrong.

| Fitted analysis | Reported result and interpretation |
| --- | --- |
| Mylyn stepwise regression, Table5a | LOCC alone `R²=.73`; adding CDC gives `.79`, adjusted `.77`, standard error3.49. Scattering adds fitted information beyond the selected size-only model. |
| Rhino stepwise regression, Table5b | LogDOSC alone `.92`; final LogDOSC+CDC+LogDOSM `.93` (prose `.928`), adjusted `.93`, standard error10.96. LOCC is not selected in this model. |
| iBATIS stepwise regression, Table5c | SLOCC alone `.80`; sequential additions of CDO,CDC,DOSM,DOSC reach `.85`, adjusted `.85`, standard error1.54. Size remains a large part of the fit. |
| PCA and component regression, Tables6–7 | Three/four/three components retain over95% of predictor variance in Mylyn/Rhino/iBATIS. Component regressions report `R²=.78/.92/.78`, adjusted `.75/.92/.78`, and standard errors3.69/3.03/1.86. Components mix size and scattering information. |

These are fits to the analyzed cases. No held-out or cross-project prediction validation is reported. Stepwise model selection and orthogonalizing predictors do not create independent concern observations or identify a causal effect. Similar adjusted and unadjusted `R²` values cannot establish the absence of all bias. The PCA variance retained is variance in the predictors, distinct from variance explained in bug counts.

Two reconstruction limits matter. The Rhino CSV has159 zero DOSC and32 zero DOSM values, while the paper uses logarithms without specifying zero handling sufficiently to reconstruct the fit. The reported Rhino standard errors differ markedly between the stepwise and PCA models; the complete transformation/model specification needed to reconcile them has not been recovered. Neither a guessed pseudocount nor a preferred refit should replace the reported method. The selected archive files contain no recovered fitted-analysis recipe resolving those questions; this is a bounded inspection, not proof that no such material exists elsewhere.

## Evidence disposition and transfer

The paper supplies **positive observational evidence**, with explicit size analyses, for concern scattering carrying information about historical bug associations in these three systems. Its theory offers a plausible mechanism. The authors themselves call for independent empirical studies and controlled experiments before confidence in causation. The results do not show that aspect-oriented refactoring, a functional architecture, or Nu's organization would reduce defects or maintenance effort after accounting for integration cost.

Assignment reliability, overlapping fix mappings, changing history, requirement reconstruction and project selection limit interpretation. Complexity, developer/process differences, churn and exposure are not eliminated by the size analyses. Spearman tolerates some measurement error only if relevant ordering is preserved; a significant association does not validate the mapping instrument. Planned inter-analyst and reference-assignment checks remain future work in this paper.

The [author appendix site](https://www.cs.columbia.edu/~eaddy/concerntagger/) reports31,102 and18 hours of concern-assignment effort for Mylyn, Rhino and iBATIS. These are useful reported preparation costs, not independently timed observations or the cost of a deployed maintenance intervention. They make mapping burden concrete without converting it into a total cost-benefit estimate.

This work differs from [S195's latent lexical topics](S195-aspects-latent-topics.md), [S196's patch/revision history](S196-crosscutting-patch-history.md) and [S120's functional-modularity critique](S120-functional-modularity-critique.md). Different concern definitions, outcomes and units explain why their findings need not mutually refute one another. Preserve S200's positive associations and the other works' scoped null/adverse evidence. No source proves that compactness, type coverage or semantic/temporal obligations follow from a scattering score.

The incoming graph is capped and its contexts include background, metric reuse and reuse of Rhino data; those are not independent confirmations. Selected S203, *Framing program comprehension as fault localization*, can test an observed developer-benefit mechanism; S204's large industrial coupling study can challenge transfer across size, activity and defect categories. Both have native records before body reading. S202's maintainer-diagram method and independent runtime/oracle/type frontiers remain open. The next work is primary method reconstruction, with all construction and experimental holds preserved.
