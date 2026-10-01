# S186 — interview materials, review coding and bounded count checks

This supports the [full-paper reconstruction](S186-runtime-anomaly-practice.md). Reader: main Codex session, 2026-10-01. These are passive document/data checks, not detector reproduction, independent recoding of private interviews or execution of author experiments.

## Identity, acquisition and scope

The paper cites concept DOI [10.5281/zenodo.10637562](https://doi.org/10.5281/zenodo.10637562). The primary API resolves it to [record 12658560](https://zenodo.org/records/12658560), dated **5 July 2024**. Metadata for older records `10639158` and `11232679` links them to the same concept; they are package versions, not independent studies. Earlier coding files include Markdown where this release has PDFs, and the RQ3 workbook changes. Older file bodies were not read or silently substituted.

The seven-file archive was acquired from the version-specific Zenodo API and attached to existing native parent `BBVLN5T2` as **`87CS7S86`**. Download and stored file agree: **5,198,639 bytes**, SHA-256 `7502296ef4fe9a567720d407c0cc9f860f34fee8c59ff01274105d6750af06ce`. All seven member sizes and MD5s match the release metadata; per-file SHA-256 values follow. No raw video, full transcript, runtime telemetry, executable detector or evaluation dataset occurs in this archive.

| Released file | Bytes / SHA-256 | Actual inspection |
| --- | --- | --- |
| `RQ3_Overview_Interviews_IndustryPaper.xlsx` | 166,678 / `8f027167aa67037799370d57ec4e73e63915ef91374d7e6524e0b5e3ecdc2dcd` | All nonempty cell text/cached values in four sheets: parameter coding, exclusions, criteria and sample blind review. OOXML decoded with the standard library; formulas not recalculated and workbook not visually rendered. |
| `RQ2_Inductive_Coding.pdf` | 188,136 / `07c26607f4c4285b41b07c7212094dc7d23d8f7f6560d86755c2fa30b22bbb04` | All six pages, including blank final page; page 5 visually checked. |
| `Procedure_Interview_Participant_Selection.pdf` | 4,275,553 / `9324aae7556ac62e8c8eccbd49afd3f89bde8f149f65769de492c2fdbbdc09ea` | All three pages; page 3 participant/duration table visually checked. |
| `RQ1_Inductive_Coding.pdf` | 245,822 / `0304b0c9e62e48495ddcc808d5699012385ce0ca03cfe7ea4b67c5706f58a13a` | All eight pages; page 1 coding legend visually checked. Text coverage does not independently verify each later color assignment. |
| `Overview_AllPapers.xlsx` | 60,020 / `5cbacfbd26b416963f98b9098917ad593b50c11bdb143375463450c3dd03a9d7` | Inventory/count/identity screen: all 91 populated citation cells, the separate DeepTraLog title row, and selected evaluation cells around rows 50–65. Other evaluation/anomaly cells only partially inspected; no complete workbook-content claim. |
| `RQ1_IEEE_Definitions_over_Years.pdf` | 126,940 / `638a345312387fac3b3d745d74521b45e1dcfde739dfc5fce98c2551316d2c2c` | Both pages of the authors' historical definition compilation; underlying standards not independently obtained/read. |
| `Interview_Guidlines.pdf` | 134,196 / `531eab5da6494e831215d32f2e6f9de9c16e8ffb66fd55a9779847bdf89e833b` | Both pages; page 1 introduction/model exposure visually checked. Filename spelling retained. |

All **21 supplement PDF pages** were extracted/rendered and text-read, with the four listed visual checks. This is complete text coverage of those PDFs plus bounded spreadsheet inspection, not a complete independent review of the 92 cited entries. Blank formatting extends the spreadsheets to roughly row 1,000; it does not create additional observations. An unavailable optional spreadsheet library was avoided by decoding ZIP/XML directly; nothing was installed.

## What the instruments and coding establish

The recruitment material explicitly seeks monitoring/anomaly experience and a mix of industries/company sizes, with microservice experience preferred. Recruitment and introduction describe the planned explainability research. The interview guide shows an early model before case elicitation and asks directly about energy. Participants could describe practices in depth, but prompted responses should not be treated as spontaneous priority ranking.

The duration table gives **28–67 minutes** across fifteen IDs, versus the article's approximate 30–60. Check marks for transcripts/videos/extractions describe materials available to the authors. They do not indicate public release or our access. E has a written extension. RQ1/RQ2 explicitly describe their public content as partial extraction limited by confidentiality.

The coded accounts preserve positive rule-based diagnoses, fast event-based analysis and AI-assisted root-cause/time-saving reports. They also preserve rule-based false alarms, unclear logs, difficult thresholds, AI training/explainability costs and aggregation loss. Participant-level and summary attributions occasionally differ: for example, the AI summary's root-cause entry is labeled F although the detailed account appears under H. Use the detailed attributed account with that discrepancy, not invented participant counts or a pooled effect.

The historical-definition compilation distinguishes expectation deviations from narrower faults/failures and shows why participants use different meanings. It is a secondary compilation within this study, not an independent verification of current IEEE standards. No long standard quotations are reproduced here.

## Own arithmetic and unresolved units

The parameter workbook has **36 literature rows**, with 23 `yes` and 13 `no` AI flags. Using the years printed in its bibliography cells, the 2021–2023 subset has **16 yes / 4 no**, reproducing 80%. This is arithmetic on the released coding, not an independent validation of its classifications or publication dates. The overview has **92 populated tool/title rows** (91 full citation cells plus DeepTraLog without one), consistent with its cached total. These are not necessarily 92 distinct publications: some cells bundle editions, the Nobre title recurs, and the TrinityRCL row carries the FacGraph citation. The latter mismatch prevents silently treating its printed year as a verified TrinityRCL publication year.

The `sample-based dual blind review` sheet has nineteen rows, with **sixteen explicit YES, one NO and two blank agreement cells**. Counting explicit judgments gives **16/17 = 94.1%**. The article's **94.7%** equals **18/19**, but the package does not explicitly encode agreement for those two blanks. The NO concerns Sage's benchmark setting; the blank rows have scope comments. The intended treatment of blanks may explain the printed statistic, but that is an inference, not a documented reconciliation. Neither arithmetic estimates independent full-corpus selection reliability or resolves differences in the underlying data classification.

The RQ3 sheet also sums parameter mentions across fifteen interviewees and the literature rows. Positive/negative marks represent coding, not necessarily instrumented use, measured accuracy or comparable independent observations. Adding interview and publication frequencies does not yield adoption prevalence. Shared-company respondents, multiple modalities for one signal, reused benchmark data and review exclusions must remain visible. Excluding benchmark-only studies here does not discredit their ability to test controlled fault sensitivity elsewhere.

These checks support a bounded practitioner taxonomy and recover the reported recent-literature AI proportion. They leave review recall, exact agreement handling, primary method quality and empirical benefit unresolved. No author scripts, model calls, telemetry collection or new runtime tests were executed; copyrighted materials remain outside Git in native attachments and ignored local caches.
