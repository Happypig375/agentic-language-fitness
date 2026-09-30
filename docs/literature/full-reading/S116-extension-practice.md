# S116 — Data and operation extensions in Smalltalk practice

**Reading completed 2026-10-01 HKT.** Romain Robbes, David Röthlisberger and Éric Tanter, *Object-oriented software extensions in practice*, Empirical Software Engineering 20(3), 745–782 (2015; online 29 January 2014), [DOI 10.1007/s10664-013-9298-0](https://doi.org/10.1007/s10664-013-9298-0). This addresses B01/B02/B10/B12: whether both extension directions occur in practice, what the observations measure, and whether they establish maintenance benefits of another representation or tool.

## Acquisition, editions and actual coverage

Existing native Zotero parent `JSIWRRCZ` preceded body reading. All 38 pages of the [2014 author copy](https://pleiad.cl/papers/2014/robbesAl-emse2014.pdf), attachment `TLVGATP4`, were read, including all 21 numbered figures, the entropy equation, 39 references and author biographies. All figures were visually inspected on PDF pages 4/5/7/8/11/13/14/15/17/18/19/22/23/25/27/30/31; the equation on page 26 was also inspected. There are no numbered tables or appendices. The PDF has 2,880,023 bytes, SHA-256 `202befac74693f8eb86c453ddb63a54cd1bdf8af15d2f08db33fb51b17ebe8ee`. Native note `X7SKBR5R` stores this reconstruction.

The author's publication-metadata file subsequently located the [final 2015 issue PDF](https://pleiad.cl/papers/2015/robbesAl-emse2015.pdf), now attachment `JDNAANW6`: 38 pages, 2,747,493 bytes, SHA-256 `598d6ac40d89e7f7761d776c8757abe7f80beb952f9403cd60cf4c133074e8c6`. Native bytes were read back and hash-verified. A page-by-page extracted-text comparison removes the publication header, the matching printed page number and whitespace. Pages 2–38 then match exactly; page 1 differs in the online date and an author-name accent. Final-issue pages 1, 11 and 26 were also visually checked. This is a bounded edition comparison, not an independent second full reading or certification of every graphical detail. The reporting conflicts below persist in the final issue text. Final printed page numbers equal PDF page plus 744.

[S141](S141-extensions-predecessor-partial.md), the ECOOP 2012 predecessor, has its own record and PDF before intentional comparison. Nine selected pages establish shared methods/corpus characteristics and changed counts. S116 explicitly adds stability and third-party questions to that predecessor; the author bibliography marks the earlier paper superseded. They are not independent replications, and their observations are not pooled.

The paper advertises CSV data and R scripts through [its short link](https://tinyurl.com/p6usq9c). Ordinary HTTP resolves it to `https://dl.dropboxusercontent.com/u/31624577/ADTOO-data.zip`, which returns 404. Targeted filename/title searches and author metadata recover no replacement archive. A public archive-index request fails through the web tool and times out through HTTP; this is not proof that no archived copy exists. The U-papers PDF route returns a 260-byte HTML response rather than a PDF. The author copies provide the paper, not the missing data/scripts. No author mining tool, R script, project, experiment or test was executed. Printed arithmetic checks are distinct from data reproduction.

## What counts as an extension

The corpus is a Squeaksource snapshot of open-source Squeak/Pharo projects over roughly eight years, ending July 2011. Its approximately 600 million lines sum source across versions; they are not that many unique lines. Monticello versions language entities and allows methods of a class to belong to other packages. Ecco retains changes between package versions and ancestry links, including forks/merges; detailed source is available through Monticello. This infrastructure supports method/class-level observations, not a record of every developer action, failed attempt or non-code resource change.

The local extension classifier uses hierarchy changes, without reading method bodies:

- A new class in an existing hierarchy is a data extension. A direct subclass of `Object` is excluded.
- A new method name appearing in at least two classes in the hierarchy is an operation extension. A one-method addition also qualifies if another implementation occurs in an earlier or later version. This is a retrospective label, not information necessarily available at that commit.
- Methods introduced inside a newly added class count toward its data extension, taking precedence over an operation-extension interpretation.
- A permanently unique method addition is excluded from the focal extension category, even though it adds functionality. A single inherited implementation is not the scattered-operation case the study targets.
- Root-class renaming is inferred when a removed root and a newly added class in the same change share at least 80% of their method sets. The rule does not compare subclasses.

Selected commits exclude initial commits and commits adding more than 50 classes/methods. Selected hierarchies have at least two classes and five changes. The stated large-hierarchy threshold is more than five classes; large projects have more than 50. Some figure captions and the flow diagram conflict with these boundaries, as recorded below. The filters intentionally omit substantial work: the authors identify a genuine operation added to 61 classes in one excluded commit.

Weight is the number of methods introduced, used as a size/scattering proxy. It is not observed effort. The journal paper acknowledges that inspecting scattered locations might cost more but that this was not measured. The predecessor had called the proxy an effort estimate; the journal wording is narrower. Method-body dispatch, field changes, composition-based alternatives and later additions to an initially introduced class can escape or change the classifier's interpretation.

## Corpus and principal prevalence findings

| Unit in the journal report | Reported count or result | Interpretation |
| --- | --- | --- |
| All / selected commits | 131,544 / 118,396 | 13,148 initial or large commits excluded from most local analyses |
| Classes / all hierarchy groups | 95,662 / 48,595 | 20,045 groups have at least two classes; 10,390 pass size/activity selection |
| Selected / large hierarchies with local extensions | 2,879 / 1,883 | Denominators 10,390 / 2,360; the paper reports about 27.7% / 79.8% |
| Projects / large projects | 2,505 / 569 | 1,036 projects reported with a local extension; about 41% overall, 84.02% of large projects |
| All commits with a local extension | 11,802, or 8.97% | Data in 5.49%, operations in 6.56%; categories overlap |
| Selected commits with a local extension | 9.41% | Data in 5.54%, operations reported as both 6.86% and 6.87% in adjacent prose |
| Operation extensions in hierarchies | 19.35% selected; 62.48% large | Observed participation under the selected definition, not a failure rate or effort estimate |

The central positive finding is that both forms occur repeatedly in this ecosystem, including in many large projects. Data extension does not overwhelmingly dominate the observed local extension distribution. This challenges motivating examples that silently assume most future work will add subclasses. It does not establish that functional decomposition, Nu, an extensible datatype implementation or a particular IDE would perform that work better.

Among hierarchies featuring either extension type, the median unweighted counts are two for each type; method-weighted medians are seven for data and three for operations. The reported Vargha–Delaney `A12` values favor data at 0.5554 unweighted and 0.6197 weighted; project-level values are 0.5514 and 0.6307. Commit, hierarchy and project distributions are distinct analyses, with substantial overlap. These are neither equivalence tests nor an equal-probability distribution over future maintenance requests. We retain `A12` as reported, without reproducing the authors' “equivalent d” conversions or treating significance as practical benefit.

Hierarchy size correlates with the counts of data and operation extensions (`rho` 0.48 and 0.55); project-size correlations are 0.60 and 0.61. The operation/all-extension ratio has no clear size relationship. More observed extensions in larger structures does not identify a causal burden of their organization: size is also an exposure measure, and the analyses share dependent project/hierarchy histories.

## Evolution, visitors and change stability

The time analysis divides each hierarchy's changes into 50 ordered slices, spreading short histories as evenly as possible, then pools corresponding slices. Project histories are treated similarly. These are relative commit-progress positions, not equal calendar periods or 50 independent cohorts. The reported operation-share correlations are 0.60 for hierarchies and 0.51 for projects; weighting reduces them to 0.38 and 0.33. This is an observed aggregate trend under that normalization. It does not by itself establish architectural decay, unanticipated requirements, or the trajectory of a typical individual project. Section 6.1 says data-share while the question, figures and results say operation-share; the missing scripts prevent resolving that implementation detail independently.

Visitor detection uses `accept`/`visit` name conventions and class-name associations. The authors manually validate every detected positive and report no false positives; recall is unmeasured. They report 34 visitor and 49 visited hierarchies among those with extensions, and 57/62 overall, using a conflicting overall denominator discussed below. Low detected adoption does not establish low utility or why developers chose another design.

After dividing extension counts by hierarchy size, visitors show fewer data extensions than ordinary hierarchies (`p < 0.02`). Other comparisons are nonsignificant (`p` around 0.2–0.4). Preserve this favorable stability observation as well as observed retrofit examples. Failure to reject a difference does not show visitor/visited structures equivalent to other structures, and an observational choice of Visitor is not a controlled intervention. The paper contrasts an earlier three-system pattern study that found more stable visited structures; that contrary method remains a conditional source, not refuted by this corpus.

For stability, the paper changes inclusion rules: initial and large commits return, methods must occur in at least five versions, and modifications are counted. Change proneness is changed revisions divided by revisions in which the method is present, excluding its introduction. Methods introduced in both ways can belong to both categories. Median proneness is 2.9% for operation-introduced methods, 3.3% for data-introduced methods and 4.8% for other methods. The between-extension `A12` is 0.514; other-versus-data/operation values are 0.571/0.586. The favorable observation is slightly greater stability of extension-introduced methods in this corpus. It does not measure the severity or cost of each change.

The entropy analysis uses change proneness across implementations of an operation. Reported median entropy is zero, with the upper quartile at 0.91. Medians rise across low/medium/high change-proneness bins (0, 0.30, 0.80) and implementation-count bins (0, 0.58, 0.62). These exploratory thresholds were chosen after inspecting distributions. The printed formula lacks the normalization needed for its stated range, so exact numeric reconstruction remains open.

Even a correctly normalized distribution of marginal change frequencies does not identify browsing effort or the joint change process. Equally frequent implementation changes could occur together in predictable coordinated edits, or separately; the same marginal entropy can describe both. Thus scattering and entropy motivate a question about maintenance, without establishing the claimed difficulty or an alternative's benefit. The authors themselves propose IDE views of all implementors, an important tool-mediated rival to a language-only explanation.

## Third-party extensions use a different counting unit

Smalltalk class extensions let a package add methods to externally defined classes, including access to their instance variables. External subclassing is the data-extension comparator. For this analysis the authors cannot recover exact external-library versions or reliably group method additions into the same external hierarchy. **Each third-party operation method is therefore an individual extension of weight one**, unlike the grouped local operation event. Third-party data extensions retain a weight equal to methods in the introduced class. Direct subclasses of `Object` are excluded, but subclasses of core `TestCase` or `Exception` can count.

| Reported third-party prevalence | All commits | Selected commits | All projects | Large projects |
| --- | ---: | ---: | ---: | ---: |
| Operation | 8.81% | 6.87% | 45.96% | 78.45% |
| Data | 13.08% | 7.73% | 85.40% | 100% |
| Both | 3.07% | 0.87% | 42.66% | Not separately numerically reported |
| Either | 19.29% | 13.84% | 88.69% | Not separately numerically reported |

These are the article's values, **not a reconciled contingency table**. In particular the commit marginals and intersections fail the union identity beyond rounding, as shown below. The large-project columns are distinct from selected-commit filtering, despite the figure's “Selected projects” label.

Among observations with third-party extensions, weighted data medians exceed operation medians: eight versus two methods per commit, 47 versus eleven per project, with reported `A12` 0.73 and 0.69 favoring larger data extensions. This preserves the favorable evidence for ordinary external subclassing alongside uptake of open-class methods. The observations demonstrate use where the mechanism exists; they do not identify what the same developers would do or prefer if that mechanism were removed, nor predict adoption in another language/community.

## Reporting limits that affect reuse

| Location (PDF page) | Reconstructed limit |
| --- | --- |
| Figure 5, p. 11; thresholds pp. 10/14/15/32 | The diagram labels the large-hierarchy split at 50 classes, while methods use five. Strict/non-strict threshold wording also varies. The analysis code is needed for exact cutoffs. |
| Visitor prevalence, pp. 22–23 | The earlier selected hierarchy total is 10,390; the visitor section uses 10,271. Their difference equals the 119 reported visitor/visited counts, but this arithmetic does not establish the intended denominator or explain possible overlap. |
| Effect-size discussion, p. 18 | The footnote incorrectly bounds Cohen's `d` by −1 and 1; a standardized mean difference is not bounded that way. Its conversions from `A12` are not independently reproducible from the reported summaries. |
| Time aggregation, p. 21 | Method prose names data/all while results and Figure 16 name operation/all. Preserve the displayed/result direction as author-reported rather than claiming recovered implementation. |
| Entropy equation, p. 26/printed 770 | The displayed `-sum(p log2 p)` has maximum `log2(n)`, not one. Three equal probabilities give approximately 1.585. Division by `log2(n)` would normalize it, but the unavailable code prevents confirming what was used, how proneness was normalized to probabilities, or how all-zero cases were handled. |
| Third-party counts, p. 29 | All-commit marginals minus overlap give 18.82%, not reported 19.29%; selected-commit values give 13.73%, not 13.84%. These are arithmetic conflicts, not corrected estimates. |
| Project summary, p. 30; conclusion, p. 34 | The summary reuses 85.40% as total third-party prevalence although it was the data-only marginal. The conclusion's “one out of eight” local commits conflicts with the journal's 8.97%/9.41%; the predecessor reports 11.76%/12.99%. A carry-over is plausible but not author-confirmed. |

Small percentage/count rounding differences are also present; no synthetic exact dataset is manufactured to reconcile them. The paper acknowledges approximately 10–15% duplicated code, ambiguous same-name methods in a dynamic language, incomplete rename detection, unknown Visitor recall, omitted dispatch/body/field changes and uncertain external-library versioning. Its open-source Smalltalk setting does not establish representativeness for F#, games, industrial work or agent edits. The missing archive limits exact reproduction, but it does not erase the method or the repeated observation of both extension directions.

## Survey implication and next sources

**Unique:** unconfirmed for ISE. Both extension directions and practice-oriented comparisons are established questions; pattern views, open functions and compositional representations address an existing design problem.

**Valuable:** S116 supplies concrete prevalence motivation and evidence that both open-class methods and conventional subclassing are used. It also preserves favorable extension stability and a visitor stability comparison. A net maintenance benefit, realistic distribution of Nu changes, or agent benefit is not measured by method counts or entropy.

**Scientifically valid:** the complete journal method, figures and selected predecessor comparison are reconstructed. Edition/corpus dependence, proxy endpoints, selection, reporting conflicts and missing data remain explicit. These limits motivate appropriate interpretation, not a claim that all results are invalid or that criticism establishes an ISE contribution.

G16 returns fourteen incoming edges/fifteen nodes across the two publication seeds; no truncation or low-coverage flag. All returned titles and supplied contexts were inspected. Two deprecation-tool contexts discuss API-deprecation findings, not these extension measurements, despite edges to the 2012 extension paper; they receive no confirming-evidence credit. Type-predicate practice, work fragmentation, fragile-base-class observations, and the earlier Visitor study are conditional B01/B02/B10 follow-ups. C++ template practice retains its earlier disposition. Continue the acquired S121/S122 coordination methods and the persistent-structure/runtime frontier, while preserving these specific practice and corpus limits. All experimental holds remain.
