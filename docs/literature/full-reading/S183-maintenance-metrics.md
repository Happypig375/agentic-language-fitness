# S183 — system metrics and observed professional maintenance

## Identity and actual coverage

Dag I. K. Sjøberg, Bente Anda and Audris Mockus, *Questioning Software Maintenance Metrics: A Comparative Case Study*, ESEM 2012, pp. 107–110, [DOI 10.1145/2372251.2372269](https://doi.org/10.1145/2372251.2372269). [Author university PDF](https://www.mn.uio.no/ifi/personer/vit/dagsj/sjoberg.anda.mockus.esem.2012.pdf): four pages, 441,702 bytes, SHA-256 `f6c90e96442d08842031d16da107ff5a0715b3656bb89fb7653839ba420b0776`. Native Zotero parent `GWEUAWS4`, PDF `PLKNQPYU`, note `L9TUFIIN`. Crossref/native title omits the subtitle printed on the PDF; it is the same DOI/work.

All four pages, both tables, inverse-metric expressions and nineteen references read; all pages extracted, rendered and visually inspected. No figures, appendices or numbered footnotes. Parent/DOI/attachment and stored bytes reverified after Zotero's native service restarted; no JavaScript window or computer use. No author analysis, software-maintenance task or experiment executed. Own arithmetic below uses only the printed table, not original participant data. Complete publisher/author file correspondence is unverified.

Live B01/B10/B12 question: do structural maintainability metrics agree with one another and with actual professional maintenance effort, rather than only diagram ratings?

## Case, assignment and endpoints

Four companies independently develop web information systems, mainly in Java, against common requirements. The paper describes them as functionally equivalent and industry quality. Development costs range from €18,000 to €61,000. Common requirements/domain/language reduce several sources of variation, but do not isolate a single design dimension or establish exhaustive semantic equivalence.

Six professionals from two companies—three in the Czech Republic and three in Poland—are hired for €50,000. They are selected from 65 earlier skill-study participants for medium-to-high reliable performance, motivation and availability. This is deliberately selected professional evidence, not a random population sample. Maintenance lasts three to four weeks.

Each person performs the same three tasks on two different systems: two adaptations after web-platform changes and a user-requested task. Systems are said to be randomly assigned, with every system appearing in both rounds. A later sentence says each of the four systems was maintained twice by each developer, contradicting the two-system-per-person description. Six people times two systems implies twelve assignments; the sentence cannot establish a balanced assignment table. The exact allocation, task sequence and per-system denominators remain unresolved in this short report.

Round two averages 39% less time. The authors say they adjust Table 1 means for this difference, but give no adjustment formula or raw participant/round timings. Repeating requirements on a different implementation can produce task/domain learning; it is not a clean observation of familiarity with the same codebase.

An Eclipse plug-in records time on each file. The short paper does not specify idle handling, reading versus editing attribution, work outside the IDE, interruptions or missing logs. Acceptance tests find few defects, without enough detail to reconstruct their coverage. The authors consequently use revision counts from SVNKit as a quality proxy, motivated by other work relating changes to later defects. **These counts are observed changes, not observed post-maintenance defects or independent behavioral correctness.** They are also produced during maintenance, rather than a pretreatment quality covariate. No general causal effect is identified by conditioning on them.

## Printed outcomes and preserved positive result

Table 1 gives these system values and adjusted mean outcomes:

| Quantity | A | B | C | D |
| --- | --- | --- | --- | --- |
| Java files | 63 | 168 | 29 | 119 |
| Java LOC | 8,205 | 26,679 | 4,983 | 9,960 |
| Maintainability Index | 113 | 117 | 114 | 120 |
| Tight class cohesion | .26 | .17 | .20 | .11 |
| Mean effort, hours | 18 | 33 | 13 | 23 |
| Mean revisions | 148 | 125 | 76 | 124 |

**System C has the lowest reported effort and revision count; LOC and effort rank C, A, D, B identically.** This is useful positive within-case evidence for system size as an indicator under these tasks. The strongest contribution is a common-functionality comparison with measured professional work. It is more directly relevant to maintenance effort than [S161](S161-metrics-and-judgment.md)'s perceived-quality endpoint.

The tested structural measures include OMMIC coupling, TCC cohesion, WMC1 method count and DIT inheritance depth. The paper also compares Feature Envy and God Class density, selected from an earlier twelve-smell file-level analysis. The original MI combines per-module measures; OO thresholds are not calibrated here. None of the specialized measures selects C as best: it has the highest coupling, methods per class and God Class density, and zero inheritance. This supplies a concrete mismatch between the selected metric preferences and these observed tasks, not a universal refutation of coupling, inheritance or refactoring.

Own Spearman arithmetic from the four printed rows reproduces the effort correlations other than undefined inverse inheritance: LOC 1.0, inverse MI −.6, OMMIC −.8, inverse TCC .6, WMC1 −.4, Feature Envy −.8 and God Class −.4. Revision count versus effort is .4. These are four system-level observations, not hundreds of independent files or repeated developers. No held-out prediction, uncertainty interval or causal size-reduction intervention is reported.

## Reporting and analysis limits that remain

The final paragraph of section 4 says A has the highest effort and B the worst quality. Table 1 instead gives **B = 33 hours** as the highest effort and **A = 148 revisions** as the highest value of the proposed adverse quality proxy. Table colors agree with those numbers. C's favorable rank survives either disputed sentence; the discrepancy should not be silently repaired into a different table.

The authors invert MI, TCC and DIT so that larger values nominally imply worse maintainability. C's DIT is zero, making its reciprocal undefined. No handling rule is given. In Table 2, the LOC/1-DIT cell is .6, while the transposed 1-DIT/LOC cell is −.5; a correlation matrix must be symmetric. Omitting C and correlating the other three inverse-DIT values with effort yields −.5, matching a printed coefficient, but that is **one compatible reconstruction, not proof of the authors' analysis rule**. No universal corrected matrix or replacement significance result is asserted.

Random system assignment may help separate some developer/order effects. It does not randomize LOC, coupling, architecture or company process separately. Four independently developed implementations still bundle design, libraries, documentation and other choices. A favorable size association does not prove that deleting code from any one implementation would save effort or that minimal source always yields the best lifetime design.

The paper's earlier file-level smell finding reportedly disappears after adjusting for file size and changes. That statement comes from a related submitted report, not an independently repeated maintenance experiment. Whether these controls estimate a direct association, remove part of a mechanism, or introduce other bias requires its actual model and measurement timing. Likewise, the suggestion that splitting God Classes might increase overall maintenance costs is a plausible system-level concern, **not an observed randomized refactoring result**.

The authors explicitly acknowledge four sample points and limited transfer to larger systems. Their lack of authorship of the tested metrics does not itself eliminate experimenter or analytic bias. These limits bound the positive result; they do not erase the observed ranking or make all comparisons meaningless.

## Lineage, access and continuation

The four systems originate in *Variability and Reproducibility in Software Engineering* ([2009 DOI](https://doi.org/10.1109/TSE.2008.89)). Earlier structural rankings come from Benestad/Anda/Arisholm ([2006 DOI](https://doi.org/10.1007/11767718_11)); Anda's expert-versus-metric assessment ([2007 DOI](https://doi.org/10.1109/ICSM.2007.4362633)) is another related route. They concern shared systems and should not be counted as independent corroborating cases. Their full methods remain unread here.

**S184**, *Quantifying the Effect of Code Smells on Maintenance Effort* ([2013 DOI](https://doi.org/10.1109/TSE.2012.89)), is the selected fuller method dependency, with native parent `B6DMTQRT` and note `QMKG6JVD` created before intended body reading. Its primary abstract reports six developers and 298 modified files, and a conditional smell result. No full-body credit follows. The [SINTEF entry](https://www.sintef.no/en/publications/publication/0198cc4d73b1-a068fcc7-d14b-4d1f-b01f-a7ef5d88aa26/) resolves to NVA; an explicit JSON request to the [native repository API](https://api.nva.unit.no/publication/0198cc4d73b1-a068fcc7-d14b-4d1f-b01f-a7ef5d88aa26) succeeds, but lists no associated artifacts. Ordinary browser-shaped requests yield the JavaScript app shell. The 2025 repository import dates are distinct from the 2013 publication.

The author bibliography supplies a DOI link; its university counterpart resets. IEEE's older staging PDF URL returns 418; LibKey returns a JavaScript shell, not acquired bytes. ResearchGate's listed author upload returns 403 to a direct request. Simula's search entry advertises NVA migration, but its page returns 404; a teaching-schedule web open fails. Search abstracts and duplicate locators cannot resolve the missing allocation/timing/model details. No access purchase, access-control bypass or request to authors was made.

The [search ledger](../nu-background-searches-2026-09-30.md) records SC116 and W254–W261 plus primary HTTP/API probes. A narrow correction/data search finds no resolved correction or original package; that is not proof of global absence. Recent metric-guided refactoring and smell-relation methods remain conditional leads, including favorable results, without completed-method credit.

For Nu/ISE, this is scoped positive evidence that system size can matter for actual work even when class-level metrics suggest another ranking. It does not overcome the project's preserved adverse F# source-size observations, prove source count is an adequate maintenance oracle, or establish an agent/context-window benefit. S184 is an access-limited dependency; acquired S181's displayed-metric intervention and S162's industry workflow remain independent accessible work. Keep type/runtime/oracle gaps visible and all construction holds intact.

| Criterion | Disposition |
| --- | --- |
| Unique | Controlled-functionality maintenance and proxy comparisons have prior art; no Nu/ISE priority claim follows. |
| Valuable | Observed professional effort favors smaller systems in this case, while proxy choices would recommend differently. Net lifetime and Nu transfer remain unmeasured. |
| Scientifically valid | Four systems, selected developers, repeated tasks, ambiguous allocation/adjustment and reporting discrepancies bound inference; size correlation remains positive without causal identification. |
