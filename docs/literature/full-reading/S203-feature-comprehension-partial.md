# S203 — Feature comprehension: complete returned text, visual and edition limits

**Historical access checkpoint.** A newly available native final PDF has since been fully read. The [final-edition reconstruction](S203-spectrum-feature-comprehension.md) supersedes the access/next-action state below, confirms the localization tradeoff and records material table/formula discrepancies. The following account preserves what was actually available during the earlier manuscript phase; it does not describe current holdings.

**Partial publication reconstruction,2026-10-02 HKT.** Alexandre Perez and Rui Abreu, *Framing program comprehension as fault localization*, final journal identity [10.1002/smr.1799](https://doi.org/10.1002/smr.1799), JSEP28(10),2016,pp.840–862. Existing native parent `YPBBW6XP` and note `ELS84ZMT` preceded body reading. **No full-reading credit is added:** the available institutional manuscript's complete returned text was consumed, but its figures and exact correspondence to the final edition remain unchecked.

The [INESC institutional manuscript](https://repositorio.inesctec.pt/bitstreams/f3a8b9e5-2651-4f52-a32e-c0d14821af39/download) has24 pages and placeholder2014 journal metadata/DOI. Four overlapping web-text ranges cover all1,171 returned lines, including the conclusion,55 references, eleven figure captions, TableI, Algorithm1 and four numbered equations. This is coverage of the returned extraction, not proof of every graphical symbol or image. Native HTTP downloads from both public repository routes closed the connection; a normal curl request timed out. Screenshot requests for pages17–18 returned cache misses. The indexed mirror has the same opening manuscript identity, but its direct download returns405 and a screenshot also fails. **No PDF bytes, attachment, hash or visual reading are claimed.** Wiley's final full/PDF routes were unavailable; the final primary abstract/metadata are readable.

## Mechanism and actual comparison

Spectrum-based Feature Comprehension replaces a fault-localization failure vector with labels indicating whether each observed run exercises a feature. Binary execution coverage and those labels produce an Ochiai similarity score for each component. PANGOLIN presents scores in a navigable Eclipse sunburst and adds class-term summaries. The score is an association with selected executions, not a calibrated causal probability or a guarantee that unobserved behavior is irrelevant. Its storage/time discussion is asymptotic and assumes comparable execution cost; it is not a measured instrumentation-overhead study.

The manuscript reports108 students working as54 pairs:26 PANGOLIN pairs and28 EclEmma pairs. Attendance was mandatory in a course lab; pairs chose their partners within groups. How participants were allocated between tool groups is not specified in the consumed text, so randomization must not be assumed. Both groups received tutorials and the same author-selected feature tests, with20minutes to study materials and100minutes for the task.

The task was to locate code for Rhino's continuation-context creation, separating exclusive implementation from shared use. The expected results were three exclusive and41 shared classes. The authors manually selected two relevant test classes from a441-test suite. PANGOLIN automates the association computation and supplies the sunburst; EclEmma users must combine/intersect coverage reports themselves. This comparison bundles computation, interaction and visualization. It does not isolate the effect of a sunburst, language, source architecture or type checking.

The reported medians establish a mixed localization result:

| Outcome | EclEmma | PANGOLIN |
| --- | --- | --- |
| Correct exclusive classes, of3 | .5 | 2.5 |
| Correct shared classes, of41 | 35 | 13.5 |
| False exclusive reports | 6 | 0 |
| False shared reports | 53.5 | 1 |
| Elapsed minutes | 60 | 50 |

TableI's extracted means likewise favor PANGOLIN for exclusive detections, false positives and elapsed time, but EclEmma for shared detections. The paper reports Mann–Whitney differences and Cohen's d; neither test nor raw pair-level results has been reproduced. Two pairs reached the100-minute limit; the available description does not settle how a capped incomplete submission would be treated. The extracted Figure6 axis says seconds while the prose says minutes; visual confirmation remains necessary before classifying that as a printed labeling error.

The authors explain many control false positives by failure to perform the required coverage intersections. That is relevant observed difficulty with this workflow, not grounds to remove those pairs. They also reduce scoring to classes because the EclEmma group had difficulty reporting finer locations. The expected class sets and pre-experiment checking are described, but the original scoring material and its independence from the treatment's analysis have not been recovered. No repair was implemented or tested as the measured task, and correctness of future behavior is not an outcome.

## Interactive extension and separate evaluation

The manuscript reports that participants subsequently struggled with projects lacking tests or a feature-to-test mapping. Participatory Feature Detection addresses that prerequisite by letting a user delimit interactions, label them as associated/dissociated and receive an updated visualization. This provides a concrete alternative for interactive software when automated tests are absent. Capturing the right feature and correctly delimiting/labeling its execution remain obligations; replacing tests with interaction does not supply a temporal oracle.

The PFD evaluation is a separate author-operated JHotDraw7 revision789 case, locating triangle creation. One author chose the feature and the other conducted the analysis without prior knowledge of the code. It is not another108-student trial or independent replication. The described runs vary associated/dissociated transactions and injected misclassification probabilities. The authors report improved localization with additional dissociated runs, modest degradation at .05/.10 and substantially poorer results at .50. The plotted curves and exact generating data remain unread/unavailable; no numeric curve reconstruction is credited.

The extracted accuracy definition averages signed association scores over only the components with nonzero scores. That target differs from recall of all required implementation components: a missed component outside the reported set need not incur a direct penalty. The rendered equation, plot correspondence, transaction selection, truth set and exact handling of zero scores need checking before this measure can support a completeness or general robustness claim. The authors also note that real misclassification rates were unknown. Their recommendation to add dissociated interactions is a result scoped to this feature and acquisition process, not a universal optimal stopping rule.

## Access, lineage and next consequence

The original `gzoltar.com/pangolin/replication-package/` and tool-page routes were unavailable through the attempted web interface. The current [TQRG tool site](https://tqrg.github.io/pangolin/) is readable and identifies a later2019 demonstration paper. The public [TQRG/pangolin repository](https://github.com/TQRG/pangolin) was inspected at **tree-name/metadata scope only**, pinned master `d0e2e816d09491e67f10b168934efce035f6646a`:376 entries, not truncated. It contains an ASE2019 paper locator, but neither that body nor source implementation, binaries or plugin was read/executed here. The author's homepage/research page and a15-repository public username lookup did not recover the selected manuscript/package. These bounded searches do not establish permanent absence.

The manuscript explicitly extends the2014 ICPC *A diagnosis-based approach to software comprehension*. That earlier method, the2019 tool paper, and a later feature-localization-for-system-families lead require separate identity/method work before any independent-study credit. S200's Rhino case is a benchmark-selection precedent here, not a replication of its concern/defect analysis.

For B01/B08/B10, preserve the faster, more selective localization result alongside the lower shared-code detection count. For B07/B09/B11, observed execution associations and a feedback display do not establish completeness, semantic preservation or correct treatment of delayed/external effects. Nu's visibility claims need the same mechanism-to-outcome distinction. The figure/edition/package gaps are access/reading gaps; the unmeasured effect on correct maintenance is an empirical question.

**Executable continuation:** recover a renderable author/final PDF and the original tutorial/scoring/run data if an exact effect or PFD metric claim depends on them. Continue with the already acquired final S204 industrial study in the meantime, retaining S202 and independent runtime/type/oracle alternatives. No construction, worker or experiment is authorized.
