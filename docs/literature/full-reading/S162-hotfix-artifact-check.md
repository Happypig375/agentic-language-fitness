# S162 — bounded released-material and printed-count check

This supplements the [full paper reconstruction](S162-industry-hotfix-workflows.md). No author analysis or repair experiment ran. Own arithmetic uses graph counts, not unavailable respondent records.

## Pinned material

The paper's [repository](https://github.com/carolhanna01/HotFixIndustrialViews) resolves to commit **`5c3aaa34d77a3700e9acecffa6746fb71b96bb26`**, dated January 25, 2026. The recursive API tree is untruncated: **23 files**, comprising 21 PNG charts, one question-list PDF and one Python analysis script. The tree has no raw response workbook, coded text, interview recordings/transcripts or case-by-case coded dataset. The paper explicitly withholds raw coded data for ethical/confidentiality reasons. Only this pinned release was inventoried; no private data sought.

Full body coverage:

- [`statistical_tests.py`](https://github.com/carolhanna01/HotFixIndustrialViews/blob/5c3aaa34d77a3700e9acecffa6746fb71b96bb26/statistical_tests.py), 6,832 bytes, SHA-256 `689769692698cf292992be009ac24771cd798330c56fa28c2ba8d17f3e671109`: entire text read, never imported or run.
- [Question list](https://github.com/carolhanna01/HotFixIndustrialViews/blob/5c3aaa34d77a3700e9acecffa6746fb71b96bb26/Industrial_Views_on_Hot_Fixing_Questions.pdf), one page / 32,367 bytes, SHA-256 `8818c37c98560f835a2c27b910ff062fce27b56fa57b2b6c537f2a4f0b565ed3`: whole page extracted, rendered and visually read; native PDF `WV38PGDH` under `7NX2YAW4`, stored hash verified.
- Two released charts visually checked: `experience_years.png`, 93,312 bytes, SHA-256 `adf0da40c52912851f16e2ff2d7fea6b834bc85c5d11dfa34599f398f9fc3147`; public `automation.png`, 123,690 bytes, SHA-256 `36fc12551330714944b820141bdbf1adfc95f0f44933540046bf89000d5508a3`.

The other nineteen image bodies were not independently opened from the release. All sixteen paper figures were visually inspected in the manuscript. No whole-repository body-read or publisher-version equivalence is claimed.

## Analysis scope

The script reads an external Excel file, builds frequency tables for seven questions, and tests each against equal expected frequency across its selected categories. It combines lesser responsibility labels into Other; other questions generally use observed `value_counts` categories. Discovery strings are assigned to four groups with explicit substring rules. Without raw responses their classifications cannot be audited; for example, the user-report match precedes combined-source matches. No classification error in an actual respondent is asserted from code alone.

There is no company-by-response contingency test, covariate model, paired analysis, measured time comparison or multiple-testing correction in this file. Its seven tests concern concentration of categorical answers, not differences between demographic subgroups. It expects a workbook absent from the pinned tree. We installed no dependencies and did not run this script.

Own arithmetic on **seventeen count series** transcribed from manuscript charts checks totals and selected chi-square values. Monthly observations `[10,59,24,11,6,26]` yield **84.1471**; deployment-time categories `[46,51,7,5,17,10]` yield **92.5294**; people involved `[14,12,37,67,4,2]` yield **138.3235**. These match the three reported rounded statistics. No p-values were recomputed and the other four published test statistics are not all independently reproduced.

Monthly contributions `[37,61,2,0,1,35]` yield **142.8235** if all six plotted categories are retained in a uniform null. Dropping the zero-count category gives **96.3529**, matching the paper's 96.35 and consistent with the released script's observed-category default. This is a reconstructable analysis choice, not an unexplained numerical error. It also illustrates why a uniform-null result depends on how categories are defined, rather than quantifying the importance of the dominant practice.

## Descriptive results and correspondence limits

Public automation counts, ordered definitely yes / probably yes / uncertain / probably not / definitely not, are:

| Stage | Five counts | Probably or definitely present |
| --- | --- | --- |
| Detection | 18, 26, 26, 40, 26 | 44/136 = 32.35% |
| Creation | 19, 15, 14, 36, 52 | 34/136 = 25.00% |
| Verification | 36, 37, 18, 20, 25 | 73/136 = 53.68% |
| Deployment | 46, 31, 17, 21, 21 | 77/136 = 56.62% |

The primary qualitative ordering is preserved; the paper's deployment 56.7% is slightly different from the printed-count percentage. The analogous Zühlke positive shares are 25.0%, 20.83%, 37.5% and 41.67% of 24. Later-stage automation is more often reported in both samples, without being a majority response in the company sample. A combined probably/definitely-not share should not be relabeled certain nonexistence.

Figure 1's programming-experience counts `[96,32,9,2]` and professional-experience counts `[84,29,20,6]` each total **139**, despite the caption's N = 136. The released experience chart contains the same numbers. The initial response count was 139 and three were excluded, but the release does not establish which rows, if any, remained in that plot. Other inspected counts, including company count, tenure, timing, staffing and automation, total 136 as labeled. Preserve this specific denominator discrepancy rather than silently normalizing all demographic rates.

The released question list corresponds in content to the manuscript's table but contains numbering anomalies, including a repeated Q20 and a skip instruction embedded around Q13/Q14. It supplies prompts rather than the complete executable Forms branching/options or an interview guide. It therefore supports prompt inspection, not full reconstruction of the administered 38-question instrument. No new data or complete study reproduction follows from these checks.
