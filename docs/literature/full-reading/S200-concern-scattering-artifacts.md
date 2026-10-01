# S200 — Bounded online-appendix and released-data check

**2026-10-02 HKT; accompanies the [full publication reconstruction](S200-concern-scattering-defects.md).** Three study packages linked from the [author's ConcernTagger site](https://www.cs.columbia.edu/~eaddy/concerntagger/) were acquired and attached to existing Zotero parent `5RLF5HMP`. They were inspected read-only without executing author programs, binaries, tests, builds or analysis code. Archive acquisition, selected data reconstruction and reproduction remain distinct.

## Identities

The fetched author-index HTML is9,925 bytes, SHA-256 `41b5205583c22713143e4d94e163d0adff183ceb7d6f23dacb2bba6d33d02361`. Its text was read, and raw HTML recovered the image-linked study archives omitted by the web text view. Ordinary direct download was sufficient. The page includes dbviz as a fourth case; S200 analyzes three cases. The separate44MB tool distribution and candidate-project workbook were located but not acquired.

| Archive under the author site's `concerntagger_studies.` prefix | Bytes; SHA-256 | Native attachment; version after verified upload | Inventory |
| --- | --- | --- | --- |
| [Mylyn-Bugzilla.zip](https://www.cs.columbia.edu/~eaddy/concerntagger/concerntagger_studies.Mylyn-Bugzilla.zip) | 48,295,258; `8a52e3f6326b6a3995be020b0fce8680cc9b1da283fb7850b3b3d561ba3c8237` | `8C63KNDM`,4777 | 19,351 entries;11,300 files |
| [Rhino.zip](https://www.cs.columbia.edu/~eaddy/concerntagger/concerntagger_studies.Rhino.zip) | 75,259,063; `0633fce220c33c103c4fe6290b6892eb0b58ce7df66983f6dc2bb49e1b55210b` | `2N65XN8B`,4779 | 20,970 entries;12,919 files |
| [iBATIS.zip](https://www.cs.columbia.edu/~eaddy/concerntagger/concerntagger_studies.iBATIS.zip) | 53,414,789; `9ace0d7b018acda6c7be4c9abdcf5027eb40b40c44d8a5d988292e129d0aa615` | `DMD2E9PI`,4781 | 12,399 entries;4,348 files |

Native stored files were rehashed after upload. Existing parent keys, memberships and attachments were retained, and mutations used current-version checks. Inventories cover all archive names/sizes; file-content reading is only the bounded selection below. The archives were not bulk-extracted into the repository. No copyrighted body or extraction dump is committed.

## Actual file coverage

| Member, relative to its study directory | Coverage and consequence |
| --- | --- |
| Rhino `datasets/README.TXT`,630 bytes | Full text. Distinguishes referenced/mapped/ignored bugs and reports manual recovery of20 mapped bugs and reduction of174 false negatives. This is the author's recovery account, not a new issue-by-issue validation. |
| Mylyn `datasets/m-b.requirements.arff`,1,236 bytes | Complete28-concern list read. Mapping relation and issue files remain unvalidated. |
| iBATIS `datasets/iBATIS.Requirements.txt`,3,357 bytes | Complete reconstructed requirement hierarchy read; it does not prove prospective requirements provenance. |
| Rhino `results/depends-on-removal.pruned.metrics.csv`,38,286 bytes; SHA `7f0d9e8d3c7f084df653e37d197457e2e24bca170a31d82de6ad499d8447c8ea` | All357 rows/eight columns parsed and used for descriptive checks. Labels examined for selected examples; this is not a manual semantic validation of357 concerns. |
| Rhino `results/Raw/ECMA Spec (Depends-On-Removal)-Bugs (Fixed-For).metrics.csv` | All494 rows structurally parsed; each of the357 pruned concern names has the same bug count in this raw table. Header/opening passages inspected; underlying fix assignments and issue bodies unread. |
| iBATIS `results/Requirements (Depends-On-Removal).metrics.csv`,7,100 bytes; SHA `3c65ceaa27d787fd5f632f6dab0ee7324d289e668f87a824e8d55f2bffab61cb` | All186 rows/six columns parsed; no bug-count column. This is not yet identified with the publication's132-leaf fitted-analysis dataset. |
| Mylyn `results/mylyn_dbviz_metrics.xls`,164,352 bytes; SHA `f1bd6d6e53bd59ab430ef6e517d1e81d45f53bb908f730efafeb51066461a0dd` | All four sheets structurally parsed. Complete46-row/seven-column **Mylyn** sheet read, including28 observations, averages, unmapped-bug list and version warning. Other Mylyn-bug/dbviz sheets only headers/opening rows; no full issue-body or dbviz analysis. |
| Rhino `results/depends-on-removal.metrics.xls`,294,400 bytes; SHA `a9dabbcbf195267b01b498767ab24de23164b3db77acfdda795fcb337b425b9e` | All sheets structurally parsed. Complete30-row Overview and complete nonempty cached values of365-row Simple Correlation sheet read; other sheets opening/description passages only. Three chart sheets contain no returned cells; their charts were **not** rendered or read. |
| Rhino `results/executed-by.metrics.xls`,257,024 bytes; SHA `82e6adb77c3c1cd8dca536b99f557d173ba4da69e309d0a49fb75d4f7f1265a5` | All four sheets structurally parsed. Complete30-row Overview and opening descriptions read; dynamic/unit-test-based mapping is a separate method, not reanalyzed here. |
| Rhino bundled `mozilla/js/rhino/build.properties` and seven `build.xml` files | Selected version/release lines only. `version: 1_6R5` and implementation version1.6 release5 confirm the workbook's source identity. No build or source-program execution. |

The legacy `.xls` reader was **xlrd2.0.2**, loaded from its verified pure-Python wheel in the ignored artifact directory, without installing it into an environment. Wheel SHA-256 `ea762c3d29f4cca48d82df517b6d89fbce4db3107f9d78713e48cd321d5c9aa9`. The [official reader documentation](https://xlrd.readthedocs.io/en/latest/) and selected [API guidance](https://xlrd.readthedocs.io/en/latest/api.html#xlrd.open_workbook) support this limited use. Cached cell values were inspected; formulas, charts, macros and external links were not evaluated or refreshed. Opening a workbook this way is not reproducing the author's spreadsheet analysis.

The Rhino Simple Correlation sheet declares removal of nonleaves, NaN metrics and non-specification concerns, dated17August2007. Its cached data area is blank: the parsed365×8 cells comprise2,899 empty cells,14 text cells, six error cells and one numeric cell. Its average cells contain error code7 (`#DIV/0!`), and the total cache is0. **Those errors are not observed concern measurements.** The separate CSV is the source of the357-row reconstruction. We did not repair or recalculate this workbook.

The Mylyn sheet warns that its ConcernTagger1.5 values can differ from later versions: later code changed LOCC to SLOCC and corrected metric bugs. Both Rhino Overview sheets and mapping descriptions identify **1.6R5 / `1_6R5_RELEASE`**, whereas the publication and author-index case label say **1.5R6**. The bundled source supports the former. The archive also includes an unread April2007 draft, *On the Relationship between Crosscutting Concerns and Defects*,643,508 bytes, under Mylyn results. None of these identities is silently equated with the final2008 analysis.

## Descriptive reconstruction and what remains unresolved

Own tied-rank arithmetic over Mylyn's28 rows yields correlations with bug count of **.388660,.498216,.569308,.609016,.766975** for DOSC,DOSM,CDC,CDO,LOCC. These reproduce Table4a to two decimals. The rows contain231 concern-bug associations, not231 distinct bugs. Four DOSC and two DOSM values are zero.

The corresponding Rhino357-row values are **.671205,.654689,.731661,.774190,.902341**. These closely reproduce Table4b; DOSM's final displayed digit differs, consistent with a rounded-input limitation rather than an independently diagnosed error. Every row's count equals its number of distinct listed bug identifiers. Across rows there are **149 distinct bug IDs,2,556 concern-bug associations,129 IDs assigned to more than one leaf**, and maximum multiplicity140. The scope-chain row has73 bugs,CDC68,CDO265,SLOCC7,135,DOSC.908,DOSM.964. This supports the published illustrative case and establishes overlap between analyzed leaves.

Rhino has159 zero DOSC,32 zero DOSM and48 zero bug counts. The paper's LogDOSC/LogDOSM regression therefore requires an explicit zero convention or filtering rule. Searching parsed cell strings did not recover that rule or a model-fitting recipe. The selected results/dataset manifests locate other raw/dynamic/random-control data and a sibling-similarity script; these were not executed or read as substitutes for the published regression. Most program source, binaries, mappings and issue bodies remain uninspected. No whole-archive absence claim is made.

The identified iBATIS results/dataset files include requirement lists, mappings and the186-row metric table; a corresponding bug-count/fitted-analysis table has not been recovered in this bounded selection. Its132-row publication denominator and exact analysis lineage remain unresolved. The author-index mapping times31/102/18hours are reported preparation effort, not reconstructed stopwatch data.

**Result:** the selected data support the direction and approximate magnitude of the Mylyn/Rhino bivariate associations and make shared bug assignment concrete. They do not reproduce p-values, stepwise/PCA fits, the final iBATIS analysis, or an intervention's maintenance benefit. Version binding, transformation/zero handling, full mapping validation and independent empirical outcomes remain separate gaps. Preserving these limits does not discard the positive published evidence.
