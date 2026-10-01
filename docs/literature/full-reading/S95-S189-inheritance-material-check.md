# S95 / S189 — detailed report and released-data correspondence

Bounded passive inspection, 2026-10-01, supporting [S95](S95-inheritance-depth-maintenance.md). Acquisition, selected reading, arithmetic and experimental reproduction are separate. No Java program, author statistical script, model, participant task or candidate experiment was executed. Individual participant identifiers, questionnaire responses, source bodies and extraction dumps remain outside Git.

## Identities and reading coverage

**S189:** Barbara Unger and Lutz Prechelt, *The impact of inheritance depth on maintenance tasks: Detailed description and evaluation of two experiment replications*. The [KIT record](https://ps.ipd.kit.edu/english/176_665.php) leads to the [report PDF](https://ps.ipd.kit.edu/downloads/ta_1998_impact_inheritance_depth_maintenance_task.pdf). Native parent **`D4ZMZP66`**, PDF **`3QXJS3TF`**, note **`YACVKMUK`**, created/reused before body reading. **177 pages, 782,293 bytes**, SHA-256 **`9f532a4605e9212bf74ee9f16152595000786f4a51b8b45ca207cf29479b78af`**. Cover and running footer identify **Technical Report 18/1998, July 17, 1998**; the author's bibliography says 19/1998. Cover governs; native metadata was corrected with a fresh version and readback. The report and S95 describe the same experiments.

Selected text coverage: **PDF pages 1–4, 8–10, 19–25, 28–42, 50–70 and 177: 51 pages**. All 177 pages were extracted for locating material; that is not 177 pages read. Visual coverage: **1, 9, 20, 25, 31, 32, 34, 36, 38, 40, 41, 50, 68–70**. This covers the selected group diagram, program/task decomposition, result/attrition tables and solution listings. Other demographic/postmortem pages and the complete source/translation appendices remain unconsumed. S189 does not enter the full-paper count.

The [author-hosted package](https://page.mi.fu-berlin.de/prechelt/packages/inherit_package.zip) was bundled in July 1998, with raw-data formatting updated March 1999 according to the [bibliography](https://page.mi.fu-berlin.de/prechelt/Biblio/) and data READMEs. Native S95 ZIP **`CVVYIPVW`**, **375,848 bytes**, SHA-256 **`88b2f251e23d23fd3435dffaca41a5e7a0eef72b787c29edc2d5df5b2607b933`**. All **54 file members** inventoried and SHA-256 hashed; native stored archive verified after upload. No publisher manifest of member hashes was available for an independent integrity comparison.

Five READMEs were read completely. The package contains graduate/undergraduate Java sources, display inputs, candidate solution sources, German handouts/questionnaires, diagrams and task/questionnaire data. `Boerse1.java` is explicitly a misnamed depth-zero variant. File presence is not source execution or behavioral-equivalence verification. Source files, completed questionnaires, PostScript figures and every potential analysis route were not exhaustively read. Selected solution code and translated instructions were read in S189 instead.

## Aggregate arithmetic and schema

All **57 graduate** rows of `data/tasks.data`, their redundant `data/task.data` table, and **58 undergraduate** rows of `data2/tasks.data` were parsed for groups, time, grades, error codes and missingness. Own arithmetic compares aggregates with report tables/figures. The redundant graduate table agrees row by row on group, both times and both scores. Original files were preserved.

The undergraduate header has **eleven names for twelve data fields**: it omits the `time2b` label between `end2b` and `pts2b`. One row has a split final error code `EI K`; local parsing joins that final field to `EIK`, without changing numerical values. These correspondences follow field positions, timestamps and the report, and are explicitly local parsing decisions. They are not evidence of a repaired author analysis.

| Released member | Bytes | SHA-256 |
| --- | ---: | --- |
| `data/tasks.data` | 4,128 | `89b5e34e47dd88e6b387d11f897f8dd97cedaee320cb6c040599e9384a9c6649` |
| `data/task.data` | 1,572 | `71c84c7571382a785f6854aa90481f29b6b60c8748661b60ebda9b86465695dd` |
| `data2/tasks.data` | 3,814 | `6aff992a883d7a7e00cd5aef379e30c9a2e2952ea318cbb3903ad177af50565b` |
| `data/factors.data` | 2,184 | `5ba7a2915061b25967b3cf7cbb74c367f84f46c9cbd537ce5220af373b661fa6` |

| Endpoint, depth 0 / 3 / 5 | Recomputed value | Report correspondence |
| --- | --- | --- |
| Graduate Y2K mean minutes, n=19/18/20 | 71.1579 / 88.1667 / 69.4500 | Figure 3.2; one-decimal table truncation/rounding differs slightly. |
| Graduate combined-task mean minutes | 115.7368 / 132.2778 / 134.8500 | Figure 3.5 and Table 3.2. Task 2a and 2b are not separately timed. |
| Graduate Y2K fully correct | 19/19, 15/18, 14/20 | Table 3.1: 100%, 83%, 70%; distinct from mean grade 100%, 90%, 80%. |
| Graduate combined-task maximum score / error code A | 6/19, 7/18, 6/20 | Flat result is **31.6%**, consistent with plotted six cases but not Table 3.3's **37%**. Other groups match rounded 39%/30%. |
| Undergraduate 2a mean minutes, n=20/17/21 | 152.3500 / 154.0588 / 180.8571 | Figure 3.10 and Table 3.5. |
| Undergraduate observed 2b mean minutes, n=17/14/16 | 27.0000 / 30.9286 / 19.1250 | Figure 3.17 and Table 3.5. |
| Undergraduate missing 2b time / negative score | 3/20, 3/17, 5/21 | **15.0% / 17.6% / 23.8%**, differing from the report's stated 10% / 12% / 29% dropout. |

Report Table 3.8 marks two depth-zero, two depth-three and six depth-five participants as having given up. Its marked set differs from the released missing-time/negative-score set. Within each group, the preceding-task mean is higher for those with missing later time: **215.67 versus 141.18**, **226.33 versus 138.57**, and **247.00 versus 160.19 minutes**. These are descriptive comparisons after assignment, not causal adjustment. The report does not supply enough information to equate every marked dropout with every missing measurement; preserve both versions. The largest group-level missing proportion in released data remains depth five.

Undergraduate 2a error code A, including combined `AI`, yields 8/20, 5/17, 7/21, matching Table 3.6's 40%/29%/33%. Code I denotes two-digit input years; its presence alongside A shows that this classification is not unrestricted error freedom. For 2b, the A-bearing counts are 7/20, 4/17, 6/21, matching Table 3.9's 35%/24%/29% over the original groups. By contrast, maximum grades occur in **12/17, 9/14 and 13/16** observed-score rows. The report does not penalize several errors again when inherited from 2a (Figure 3.20). Thus maximum follow-on grade, newly introduced error, and complete retained behavior are different endpoints.

The main submission reports p=.200 for Y2K depth 0 versus 5. S189 Table 3.2's **untrimmed** row gives .447; its 10%-trimmed row gives .200. Both are nonsignificant, so the discrepancy does not reverse the qualitative result. No unpublished analysis history is inferred. Bootstrap p values, relative confidence intervals and model coefficients were not independently rerun.

## Task and model lineage

S189 pp. 20/33 explicitly time graduate 2a+2b together. Its translated instructions permit subjects to submit when finished or unable to improve further, allow new classes or changes to existing ones, and request testing against the supplied files. Instructions on p. 56 emphasize quality over speed. Consequently, time reflects a self-stopped attempt, not externally certified complete correctness; safe reorganization is not a failure by itself.

The report's solution listing on pp. 68–70 makes the depth-five follow-on reuse concrete: two display classes have corresponding input/selection methods but inherit different existing table behavior, with added menu entries. It also exhibits coupled substring-position changes in the Y2K solution. This is source inspection, not a runtime or oracle completeness check.

`data/factors.data`, marked changed **February 4, 1999**, contains **fourteen group rows**, not the later submission's sixteen. It includes six new groups and eight Daly groups, with no Cartwright rows. Graduate rows use combined-task means and relevant-method counts **15/18/19**; undergraduate rows use 2a means and counts **13/16/17**. S189's earlier Table 4.1 also uses 15/18/19 for the combined graduate task. The report's earlier correlations and the later multivariable models are distinct analyses; appending guessed Cartwright rows would not reproduce the final model. Original Daly individual data are reported lost in S189 p. 52, a statement about that historical contact, not a current global-access finding.

The result remains useful: anticipated navigation and reuse can explain task-specific costs better than a blanket preferred hierarchy depth. Residual data/report differences limit exact replication and effect interpretation; they do not justify discarding positive reuse, adverse understanding costs, or the unresolved outcomes. A complete final-journal/analysis-input correspondence and primary reconstruction of contrary predecessors remain independent follow-ups.
