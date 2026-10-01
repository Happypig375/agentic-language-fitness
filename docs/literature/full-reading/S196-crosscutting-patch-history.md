# S196 — Crosscutting concerns, patch scattering and revision

**Complete reading, 2026-10-02 HKT.** Robert J. Walker, Shreya Rawal and Jonathan Sillito, *Do Crosscutting Concerns Cause Modularity Problems?*, FSE 2012, article 49, eleven pages, DOI [10.1145/2393596.2393654](https://doi.org/10.1145/2393596.2393654). Reader: the main Codex AI session. All eleven PDF pages, five figures, three tables, six numbered equations and the additional normalization expression, six footnotes and 41 references were consumed; every page was visually inspected. No appendix is present. This is a publication reconstruction and own arithmetic on printed summaries, not independent review, source execution or experimental reproduction.

Existing native parent `UYYU37KC`, note `ZIN64AT7`, user attachment `QQBUZFZ8`: **163,968 bytes**, SHA-256 **`fb8f99cdfb9fbabfab6f03d870f21c8d6241808e0ecbb53c5fc75d97e22347a3`**. The existing record preceded intentional reading. Native attachment verification and first-page inspection closed the earlier access gap on 1 October; complete reading followed on 2 October. The attachment supplies no source URL. The FSE imprint and author-lab bibliographic record corroborate the identity. Earlier publisher/Scite denials remain access history, not the current reading state.

## Question and useful result

Does observed crosscutting necessarily produce serious evolutionary problems in a large conventional system? This retrospective Mozilla study challenges that broad prediction. Most patches affect few files/directories, the distribution has a substantial tail, and review leaves the extent of most revised issues unchanged. The average extent falls slightly, while its frequency of increasing is greater than its frequency of decreasing. Greater scattering also has a positive association with revision counts, and mean scattering rises over the later years. Preserve all of these findings.

The measured objects are patches, unions of changed files for an issue, obsolete/non-obsolete patch counts and annual repository/issue summaries. There is no assigned architecture treatment, aspect-oriented comparator, direct effort/comprehension measure or independently measured defect rate. Thus the study informs the distribution and practical interpretation of change locality; it does not establish that scattering is harmless or that separating a concern cannot help.

## Data, units and proxies — §§3–4.3, pp.3–5

The paper collects **93,006 issues and 221,508 patches**, from 8 April 1999 through 17 June 2010. This is one Mozilla project family, not 93,006 independent systems. Bugzilla issues include enhancements as well as defects. A patch may be approved, rejected, superseded, compete with another solution or coexist with other non-obsolete patches. The analysis classifies **91,085 obsolete, 130,256 non-obsolete and 167 unknown-obsolescence patches**; unknowns are excluded where that status matters. Their sum reproduces 221,508.

| Measure | Construction | Interpretation boundary |
| --- | --- | --- |
| FPP | Unique files modified/added in a patch | File extent, not semantic concern count, cognitive difficulty or effort |
| MPP | Unique affected modules inferred from paths | Directory organization; developer-local paths complicate correspondence |
| FPIobs / FPInob | Union of affected files over obsolete/non-obsolete patches for one issue | Sets aggregated by final status, not necessarily one chronological before/after patch pair |
| Revision proxies | Obsolete-patch count or total-patch count per issue | Parallel proposals, patch splitting and complementary patches need not be failed sequential repairs |
| Change size | Added/removed/modified lines in individual patches | The exact unioned issue-change size is not reconstructed |

No module-per-issue measure is used because inconsistent local paths make unioning ambiguous. FPP has mean 5.09, median 2, mode 1, SD12.99 and range 1–872; MPP has mean 1.48, median/mode 1, SD1.81 and range 1–136. Thus a mean alone obscures the tail.

The qualitative check samples **50 issues from 943 candidates**: Firefox, resolved/verified fixed, with at least one patch affecting **11 or more files**. This differs from the earlier statement that 5.93% of all issues have patches affecting **more than 11 files in total**. The six classifications sum to 50: arbitrary combined issues 5; dead-code removal 9; new features 12; ripple effects 4; user-facing changes 11; trivial formatting/comment fixes 9. These support multiple explanations for broad file extent. They do not estimate each explanation’s prevalence among all Mozilla changes. Cross-platform/theme edits and polyglot UI changes are concrete interactive-software examples. Even mechanically simple multi-module edits can require additional owners’ reviews; no hours are measured.

## Distribution and validation — §4.4, pp.5–7

The reported thresholds are **79% of patches affect at most 5 files and 90% at most 10;79% affect one directory and 95% at most 3**. These make the headline “little” scattering operationally interpretable;90% is not the fraction with no crosscutting. The authors also report roughly half of patches having at least some file scattering. There is no empirically privileged binary cutoff separating harmful from harmless concerns.

Figures 1–5 show the small-count concentration and long tails, including log axes and logarithmic bins. The authors compare the power law with six other candidate distributions and use simulated goodness-of-fit checks based on KS distances. For the best reported discrete log-normal fits at xmin 1:

| Data | μ / σ | Simulation result | Scoped disposition |
| --- | --- | --- | --- |
| FPP | −.26 /1.69 | p̃0,1,000 samples | Closest of the considered candidates, still a poor fit |
| MPP | −3.52 /1.68 | p̃.20,10,000 samples | Not rejected by their .1 criterion; not proof of the generating mechanism |
| FPInob | −.69 /1.74 | p̃0,1,000 samples | Poor fit despite a visually heavy tail |

This is useful contrary evidence to assuming every heavy tail is a power law. A simulation return of zero means no counted exceedances in the specified finite simulation, not a mathematical probability of zero. Failure of these candidate distributions does not establish that no useful process model can exist. The paper’s suggestion that the module-level fit supports S195’s entropy model is interpretive; patch-directory counts do not directly validate a lexical topic/entropy measurement.

Printed mathematical definitions also need care: p.6’s expression equating `1/ζ` with a sum of positive powers cannot be the displayed probability normalizer, and its empirical CDF expression counts observations without dividing by sample size. These are visible presentation discrepancies. The paper says it used Clauset’s R scripts; without the actual invocation/data, they are not evidence that the numerical fitting used those erroneous expressions. No replacement fitting is claimed here.

## Revision associations and review changes — §§4.5–4.6, pp.7–9

The positive correlations are retained:

| Paired quantities | Pearson r | Spearman ρ | Unit/scope |
| --- | --- | --- | --- |
| Obsolete-patch count versus FPInob | .21 | .34 |93,006 issues |
| Total-patch count versus FPInob | .29 | .45 |93,006 issues |
| FPP versus patch change size | .48 | .72 |221,508 patches |
| MPP versus patch change size | .19 | .37 |221,508 patches |

All are reported significant at p<2.2×10⁻¹⁶. The paper explicitly leaves size confounding unresolved: merging changes to compute issue-level change size is deferred, so there is no presented size-adjusted scattering-to-revision estimate. Moreover, non-obsolete file unions and total patch counts are related constructions. These facts qualify causal attribution without erasing the observed associations. The later threats paragraph’s statement that neither extra revision nor extra issues is observed should not replace the positive revision results in §4.5.

For **34,726 issues with both obsolete and non-obsolete patches**, Table 1 gives:

| Change in unioned file extent | Issues | Own share of revised issues |
| --- | --- | --- |
| Unchanged |18,198 |52.40% |
| Increased |8,908 |25.65% |
| Decreased |7,620 |21.94% |

The totals reproduce 34,726, or 37.34% of all issues. Among the 16,528 whose extent changes, **53.90% increase and 46.10% decrease**. Meanwhile mean FPI falls **7.09→6.58**, an absolute .51 files or **7.19% relative to 7.09**, and the median rises **2→3**. These statements can all be true in a heavy-tailed distribution. The non-revised issue mean is 3.27. They are observed group/status contrasts, not effects of an assigned review intervention. The prose sometimes calls the reused 7.09/6.58 figures FPP, but their earlier definition is the per-issue FPI union.

The symmetry test uses only the upper-left **24×24** count matrix:32,580 issues, **93.82%**, with **2,146** larger-extent cases excluded as outliers to address sparsity. Reported χ²782.86,276df establishes rejection of symmetry for that retained matrix under the test assumptions; it does not determine which direction is more frequent. The [R documentation](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/mcnemar.test.html), read at its description/details sections, states the cell-pair symmetry null. This is current documentation, not the study’s pinned R version.

There are two related presentation limits: given the paper’s row=obsolete and column=non-obsolete definition, the upper triangle represents an increase, although the prose labels it a decrease; and the matrix discussion says decrease is favored, whereas Table 1 and the final summary correctly report increases as more frequent among changed cases. The slightly lower mean remains a different, supported descriptive statement. No raw matrix is available to recompute the test, assess the tail exclusion or estimate a controlled review effect.

## Time and decay — §4.7/Table 2–3, pp.9–10

The twelve printed annual issue counts sum exactly to 93,006.1999 and 2010 are partial years. Repository-size snapshots use CVS throughout; after the 2007 Mercurial migration, the authors cannot establish that CVS contains every relevant change. Issue counts mix bugs and requested enhancements, and reporting/exposure/developer effort can change. Normalized issue counts therefore are not a measured defect incidence or proof of stable reliability.

Own arithmetic narrows a denominator question: Table 2’s rates generally agree with dividing by the **average of adjacent annual size snapshots**, rather than its same-row file/MB value. For example,2008’s 12,377 issues divided by(508+533)/2 MB gives 23.779, matching 23.78; division by 533 gives 23.221. The 2000–2010 file rates all match the adjacent-average calculation at displayed precision; MB rates agree to .01, allowing rounded size values. This is a reconstruction from the printed values, not a recovered author script.1999 lacks the preceding snapshot needed for the same check.

The revised-issue proportion is reported around .42 after startup. For 2002–2010, each annual FPInob distribution differs from the fitted across-year mixture under their 1,000-sample test. The latter uses the same years to construct the reference distribution, not a held-out temporal prediction.

From 2005 to 2010, mean FPInob rises **3.89→5.11**, or **31.36%** by own arithmetic; the printed power-law shape parameter falls 1.89→1.72. That is a later-period upward pattern, not a monotonic decade-wide trend:2001’s mean is 5.13. The authors use the power-law parameter descriptively despite having rejected that distribution as a good fit, and explicitly acknowledge the limitation. Increasing change extent is observed; causal architectural decay or additional maintenance effort is not directly measured. Do not turn either “slow” or 31% into a calibrated practical-cost estimate.

## Consequence for the wider survey

S196 closes the original-method dependency behind [S120](S120-functional-modularity-critique.md) and [S195](S195-aspects-latent-topics.md). It gives a concrete large-system counterexample to treating every scattered change as severe failure and demonstrates why event frequency, mean extent, revision proxies and developer cost must remain separate. It also preserves an adverse association and a later increase in scattering. These observations concern issue-linked changes, not GHC lexical topics, an FP/OO comparison, live-state correctness or a Nu advantage.

Developer effort, subtype-specific harm and independent defect/correctness outcomes remain distinct unknowns. The authors explicitly allow harmful kinds of concern to be hidden by aggregation. Their premise that disproportionate effort would necessarily manifest as poorer changes is an assumption; additional effort could instead sustain quality. There is no treatment comparison from which to estimate the effect of adopting aspects or another representation.

The targeted search did not identify S196’s original issue/patch table, parser or fitted-analysis invocation. This bounded access result is not proof that the materials never existed. Preserve the published summaries and request/recover an actual release if a stronger causal or numeric claim depends on them; no rerun is authorized.

SC132 and primary follow-up retain important counterpoints: **S200**, Eaddy et al.’s three-case scattering/defect method, now has a native record and acquired 19-page conference-hosted final copy; its full method is unread. **S201**, Bartsch/Harrison’s 11-professional Java/AspectJ comparison, has a native record and primary abstract but no readable body from the attempted publisher/repository routes. Its null is not evidence of equivalence. The Aversano design-pattern/defect method is a further conditional metadata lead. These cannot be accepted or dismissed through S196’s account alone. The next cross-theme reading remains acquired S198’s object-algebra alternative; S199’s newly found user PDF also makes its positive live-documentation method accessible. No theme closes or experiment begins.
