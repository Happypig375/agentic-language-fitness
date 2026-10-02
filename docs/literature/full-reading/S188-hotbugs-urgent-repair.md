# S188 — urgent repair cases, test oracles and release lineage

**Full publication reading, 2026-10-02 HKT.** Carol Hanna, Federica Sarro, Mark Harman and Justyna Petke, *HotBugs.jar: A Benchmark of Hot Fixes for Time-Critical Bugs*, [arXiv:2510.07529v1](https://arxiv.org/abs/2510.07529), 8 October 2025, DOI [10.48550/arXiv.2510.07529](https://doi.org/10.48550/arXiv.2510.07529). The work contributes 679 manually validated urgent-fix records and reports 110 cases integrated with tests. It supplies useful repair-task provenance and setup information. Urgency, a failing regression test, live deployment and temporal correctness remain different properties.

## Identity and actual coverage

Existing native Zotero **`UXM3HM94` / note `RBX8Q5ZN` / PDF `46JHRQPV`**, versions **4373/4372/4371**, preceded body reading and were verified in collection `PKLXQNEE`. The [versioned PDF](https://arxiv.org/pdf/2510.07529v1) has **five pages, 519,312 bytes**, SHA-256 `cfcbbcb5c2f0834238a2d132b90afb99503de69edf5d39d625c03632cd79035d`. All text, sections and sixteen references were read. Visual pages **1,3,4,5** cover the one figure and four tables; page 2 is text-only. No appendix is present. The checked arXiv history lists v1; this is a preprint reading, without an inferred peer-review acceptance.

The [UCL project](https://solar.cs.ucl.ac.uk/os/hotfixbenchmark.html) and [repository](https://github.com/carolhanna01/HotBugs-dot-jar) were followed to the public workbook and one illustrative case. This is bounded artifact reconstruction, **not execution or reproduction**. No installation, project build, benchmark, candidate repair or author command was run.

| Artifact | Identity and inspection boundary |
| --- | --- |
| Root repository | Commit `67b6d9493a30987992b160011a12c8641ae18693`, dated 30 June 2026. All 142 README lines and 60 `.gitmodules` lines read. Complete root tree metadata has 17 gitlinks and four blobs; configured modules also include inherited/other projects. These are not 17 independent hot-fix populations |
| Public workbook | [Bug-information sheet](https://docs.google.com/spreadsheets/d/1DftX4Bm0wIn4wvv11edEUVYrNO5WpDy3DTkiIyZxaZs/edit?gid=579710219), exported read-only on 2 October 2026. Native attachment **`4UI4F3G6`**, version4972, 157,693 bytes, SHA-256 `37fe9641dc19cb1100ec0cd1433c6f0ed3b6d66aa5140632b0b00183697683fe`. All ten sheets' populated XML cells extracted; all 679 issue IDs and classification/integration fields counted. Selected setup/rationale cells read; not a manual rereading of all issues or all row narratives. No formulas found, recalculation or spreadsheet execution performed |
| FLINK-18425 case | Branch `bugs-dot-jar_FLINK-18425_00863a28_HOTFIX`, pinned at `b7c5a408bb1f798e5fa7c991fe82d502b53972da`, 28 July 2025. Complete 108-line issue export and 107-line developer patch read. Of the 1,700-line test log, the error/summary matches, lines1483–1506 and1653–1700 were inspected; remaining routine test output is not full-read credit |
| Case lineage | Three commit metadata/file lists inspected, the original fix's complete test-file diff read, and three file-blob identities compared between the pre-fix parent, developer fix and artifact. No complete repository/history or all110 branches inspected |

README SHA-256 is `146f541f3d862e7b1afe75fff95d25bf481181d955c7cb4709c266da10b9e264`; `.gitmodules` is `e186628984cb3d0d0a211a1895d4dc680f454296658a2c7c183c34f8f3bce514`. The current root/workbook are later snapshots, not established byte-identical publication inputs. The earlier web-rendered workbook exposed only rows1–70 of its selected tab; the native export supplies the broader counting coverage. Bodies and extraction intermediates remain outside public Git.

## How cases are selected

The ten Apache projects are Flink, Kafka, Hadoop, Solr, HBase, Jackrabbit, Karaf, Calcite, NiFi and Ambari. Table1 reports collection dates in 2024/2025, 193,721 commits, 150,585 issues and 2,071 releases. This is a purposive Java/GitHub/Jira sample, not a prevalence sample of production failures or Nu/game maintenance.

The declared project requirements include a last commit within a week, more than9,000 commits and more than100 releases. Table1 nevertheless lists99/85/90 releases for Karaf/Ambari/Calcite and6,208 commits for Calcite. Thus the stated threshold rule alone does not reconstruct the included population. No project is silently removed from our account to make the rule fit.

The operational hot-fix screen requires a Jira bug with Blocker/Major/Critical priority, creation on the same day as a release (also described as a24-hour delta), and resolution on its creation day. The authors motivate production relevance from mature, active public projects. They do not supply a per-case observation of deployed state, uninterrupted execution, actual maintenance deadlines or rollback effects. Calendar-day equality and a rolling24-hour interval also need an explicit implementation convention before exact replication.

Of746 metadata-screened candidates,679 survive manual validation. Two independent assessors are reported, with project-level percentage agreement and a weighted91% average. Disagreements are discussed; unresolved cases are excluded. CI/build and licensing issues are included after considering their operational implications. The reported percentage is agreement, not chance-adjusted reliability or proof that a deployment occurred. The acknowledgement names two helpers working with an author; it does not establish that the same pair independently rated every issue.

The taxonomy distinguishes configuration, database, GUI, network, performance, permissions/deprecation, security, program anomaly, test code and other. Program anomalies account for375/679. The retained heterogeneous categories are useful: urgent maintenance is broader than a production-method logic patch. Its Java/test-reproducible subset selects a materially different task population.

## What the released workbook resolves

Every sheet has unique Jira issue URLs, with no duplicate across the679 rows. Counts by project reproduce the paper's validated population:

| Project | Validated rows | `Yes` integration | Other integration disposition |
| --- | ---: | ---: | --- |
| Flink | 34 | 14 | 1 already in Bugs.jar,19 no |
| Kafka | 13 | 6 | 7 no |
| Hadoop | 95 | 21 | 74 no |
| Solr | 66 | 12 | 54 no |
| HBase | 22 | 5 | 17 no |
| Jackrabbit | 27 | 4 | 23 no |
| Karaf | 20 | 1 | 19 no |
| Calcite | 13 | 3 | 10 no |
| NiFi | 64 | 11 | 53 no |
| Ambari | 325 | 32 | 293 no |
| Total | 679 | 109 | 1 already in Bugs.jar,569 no |

Flink row31 identifies **FLINK-3684** as already in Bugs.jar. Counting that lineage with109 new `Yes` entries reconciles the reported110 integrated cases; it should not be described as110 newly independent repairs. The integration rate is110/679, approximately16.2%, conditional on the validated population.

The category totals also reconcile after explicit spelling/label normalization: `program anomaly`/`anomoly`375; `config`/`configuration`96; test73; GUI50; permission/deprecation26 including the three mixed deprecation/configuration labels; security14 including two configuration/security labels; performance14, network8, database7 and other16. This is reconstruction of the authors' categorization, not independent validation of each category.

There is a material **user-facing label discrepancy**. Table2 prints user-facing Yes121/No558, and the text defines external as user-facing. Workbook columnH gives **external558/internal120**, plus NiFi row40's misspelling `Interal`. Treating that one build-issue label as internal yields121. Every project's counts match the printed user-facing columns in reverse. Preserve this apparent transposition/version discrepancy; do not use the paper's18% user-facing rate or silently replace it with an independently validated82% rate.

Table4's printed exclusion columns sum to321 non-Java,141 no-tests,23 build,27 passing-on-buggy,48 test-only and10 other, plus110 integrated: **680**, not679. Its Solr row totals67 against66 validated cases. The workbook gives18 Solr no-tests entries versus the printed19, accounting for that difference in the current snapshot. Other reason labels are not uniformly harmonized: Jackrabbit has different build/other grouping, and all64 NiFi reason-columnF cells are blank despite details in columnE. A single consistent exclusion classifier cannot be inferred from these columns without additional interpretation.

## What the tests demonstrate, and how they are constructed

The paper identifies a developer fix through the issue/PR and defines the buggy revision as its immediate predecessor. It describes reversing the fix, repairing old build configurations, running buggy tests, excluding cases whose buggy tests pass, then running fixed tests. Tests failing on the fixed version are called flaky and removed. No repeated-run criterion is specified there; failure on a fixed revision alone does not establish nondeterminism. Nor does the paper explicitly describe rerunning the final reduced suite against the buggy revision after removing those tests.

This is a useful attempt to establish a failing-before/passing-after resource. It also conditions inclusion on buildability and a distinguishing suite. Missing tests, non-Java changes and difficult dependencies are part of the excluded maintenance burden. The retained tests are not an independent proof of every intended behavior, no-regression obligation, urgent deadline or production effect. The paper proposes partial amelioration, repair-tool evaluation and developer studies; it reports no comparative repair success, developer-time benefit or calibrated operational risk reduction.

### One concrete case: FLINK-18425

The [stored issue](https://github.com/carolhanna01/flink/blob/b7c5a408bb1f798e5fa7c991fe82d502b53972da/.bugs-dot-jar/bug-report.yml) is a Major bug created24June2020 at08:09:10UTC and resolved13:10:42UTC, an interval of **5h1m32s**. It concerns converting an object-backed array to a primitive array. The [developer patch](https://github.com/carolhanna01/flink/blob/b7c5a408bb1f798e5fa7c991fe82d502b53972da/.bugs-dot-jar/developer-patch.diff) distinguishes primitive/object backing, checks nulls, converts wrapper elements, and aligns an exception message. These are functional conversion obligations; the case's short resolution interval does not itself supply a temporal-behavior oracle.

The [stored log](https://github.com/carolhanna01/flink/blob/b7c5a408bb1f798e5fa7c991fe82d502b53972da/.bugs-dot-jar/test-results.txt), dated22May2025, records one `ClassCastException` in the integer-array conversion case. Its failing module summary is843 tests, zero assertion failures, one error, zero skipped; this is not the total number of tests across every reactor module. Four later modules are skipped after the failure. The complete listed `.bugs-dot-jar` directory contains issue, patch and this failing log, with no separate fixed-run log there. No present-day rerun or general absence elsewhere is claimed.

The branch suffix **`00863a28` is the pre-fix parent**, not the fixed commit as the current README's naming explanation says. The linked developer fix [7def95b6](https://github.com/carolhanna01/flink/commit/7def95b6c006f0407731be8ec139b54454dc3f97) directly follows that parent; [a05972f9](https://github.com/carolhanna01/flink/commit/a05972f98d3b939857d0c0911f68d97186d1cada) is the other version's fix. The artifact's two patched production-file blobs exactly match the pre-fix parent. Its `DataStructureConvertersTest.java` blob instead exactly matches the **post-fix** test blob, which adds the failing integer-array conversion fixture. The packaged patch contains only the two production files, while the original developer commit changes those files and the test.

This establishes a specific and useful reconstruction: **old production behavior with successor regression tests retained**. It does not establish that the artifact is the untouched historical buggy tree, that all110 cases follow the same transformation, or that the fixed result was independently reproduced. The distinction matters if a later authorized protocol separates currently available development feedback from successor solutions and final scoring. The README even uses the developer patch to locate the affected module; exposing that reference patch would change the information condition.

Case issue/patch/log SHA-256 values are respectively `b9dafdc60db6b5d31c9d123942a0fbc036715ba45cb821b7031917598e9602b6`, `86eddb0d8efaa03afb3e9d7d0ffe2645048a2a59fc57fb2046c3b357ce3cae64`, and `e3b5627b4ba7016331a32f8850d033b201b4f8dba765e8f1a30446ccf6d01262`, with3,909/3,188/162,650bytes. Exact source/test blob correspondences are retained in ignored inspection records.

## Consequence for the wider survey

**B07/B08:** urgency selection and a regression fixture can supply consequential repair scenarios. They do not measure retained-state migration, pending work, finite-trace liveness, external effects or live-deployment correctness. S46/S47/S53/S100/S104's temporal-oracle distinctions still apply. A static conversion regression is valid evidence at its own scope.

**B10/B12:** preserve the positive curation work, explicit setup burden and concrete failing case. Keep candidate screening, manual acceptance, build/test eligibility, old-source reconstruction, successor-test exposure and final outcomes separate. Neither a high-priority issue label nor the dataset's adoption claim is a measured architecture or tool benefit. The reviewed case supports source/test lineage checking as a necessary preparation step for any later approved use.

**Next consequential action:** acquired S173's mutant/real-fault coupling method can change the independent fault-sensitivity account; S168/S177/S178 remain further method alternatives. S187's expanded hot-fix review is still a distinct unread source, and S205/code access, type/evolution and runtime/persistence gaps remain open. The HotBugs publication gap is closed at v1 scope. No survey theme closes and no experiment is authorized by this reading.
