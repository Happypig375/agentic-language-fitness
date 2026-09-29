# S66 — Replay and debugging behavior

**Reading completed 2026-09-30.** Ruochen Wang and Thomas D. LaToza, *How Omniscient Debuggers Impact Debugging Behavior*, VL/HCC 2025, pp. 57–67, [DOI 10.1109/VL-HCC65237.2025.00016](https://doi.org/10.1109/VL-HCC65237.2025.00016). This is a direct human comparison relevant to the claim that execution history lowers debugging effort. It is not a Nu, F#, coding-agent or maintenance study.

## Identity, acquisition and coverage

Zotero `EYL8YNRG`, PDF `I9W5U6MZ`, acquisition note `8NJRY97W`, under root `PKLXQNEE` and temporal/game-tools `NDU9BTP7`. The [Wang author copy](https://mason.gmu.edu/~rwang29/assets/pdf/VLHCC25-omniscient-debugging.pdf) has eleven pages, 1,126,295 bytes, SHA-256 `873453284642bea24f0ddff4d43d2f1ccf23e90af4a205d2ab24183ba06d939e`. All eleven pages, nine figures, nine tables and 47 references were read; rendered pages 3–9 were inspected. The LaToza `cs.gmu.edu` PDF route returned 403 with ordinary requests; the alternate author copy was obtained with normal TLS verification. Search-index spelling differs from the downloaded author identity, which governs this record.

The [Figshare v1 supplement](https://doi.org/10.6084/m9.figshare.29852750.v1) is a CC BY 4.0 archive, 3,347,371 bytes, MD5 `5850b66c83244fca4a71db31206ea6cd`, SHA-256 `a0896da9bbafd8b49a9893ac23e8e04f71212068e05d7dcddca4e0ae2373b8ab`. Native API attachment `X3XWB7RT` was uploaded and its stored bytes verified. It is one archive, not three additional stored PDF attachments or an independent study.

All README text, ten participant-material pages, six codebook pages and 22 strategy-summary pages were read. Participant-material renders 3/5/7 and codebook renders 3–6 were inspected. Remaining supplemental screenshot/table layouts were not all visually audited. Three XLSX files were read without modifying or exporting them. Independent local XML arithmetic checked the selected aggregates below; it did not recode recordings. Of the 70 notebook cells, complete source cells 4/7/8/9/12/13/15/16/22/30/34/45/49/55/59/60/64/65/68 were inspected, plus stored text outputs of 34/60/64/65. Other cells received only an initial structural inventory. The notebook, Google authentication, Replay and Excalidraw were not executed. No recordings were reacquired or independently scored.

| Supplement member | SHA-256 |
| --- | --- |
| `README.md` | `d60d49b1af386f5a64eda46479f5f2a5580a5ece9e0f45028760eb8973b3a0b6` |
| `participant-material.pdf` | `c40f6ad247ff6a25c94f158e872a0885f4d7e8ef1b034e5ed0c355d5e7d1adbb` |
| `code-book.pdf` | `b069b6015426c723d49f1d72776c388ddda0a2b4a8d8531f91d45868b7995534` |
| `strategies.pdf` | `fd48b9c53ac58cf145764070bfb77f9487dbec1ced8be53af6695bc889fc9bf5` |
| `navigation codes.xlsx` | `4e1ac15fc291435e5f2dbcccf5bbac24819d5eb5593a75a89f01341068a3e277` |
| `demographics.xlsx` | `2516846f497ced227117144a386bcfa1574564371461763740cb9f5d17671821` |
| `view rerun codes.xlsx` | `67b36e8aa85246e3bd2a5327679a0e4b21b4e6fe23d1d49802a984ea3e93a559` |
| `code_analysis.ipynb` | `44c9ce73ed8f77f1c2b58d29eb1bb3a9cfeaf06def1a875b145fb167682ba4a7` |

## Intervention, assignment and endpoint

Sections III–IV compare commercial Replay with Chrome DevTools. Twenty retained participants each attempted two different bugs, one with each tool. Four Excalidraw bugs cross small/large cause–symptom distance and presence/absence of an error message. Two came from issue reports and two were introduced by the researchers. Task sets and tool/task order form eight counterbalanced conditions, assigned sequentially by session date. This is not randomized assignment. Each bug/tool cell has five attempts; the 40 sessions are not 40 independent people.

The retained sample consists of graduate students/junior engineers recruited through a course, mailing list, LinkedIn and personal contacts. A minimum seven-year programming-experience threshold was introduced after some early participants could not progress. Nonprogressing participants were replaced within their condition; the number excluded is not reported in the paper or recoverable from the 20 retained demographic rows. This selection limits novice/general-population inference. The workbook confirms programming experience 7–20 years, median 8; professional experience 0–10 years, median 3.2917; React 0–4 years, median 1. The unusual professional median is supported by month-to-year conversion, not a presumed mean. Prior JS/TS code-volume categories contain 2, 9 and 9 people.

Participants controlled the researcher's computer remotely, received both tool tutorials and warmups, and could use VSCode, web search and syntax clarification. The participant instructions, p. 8, explicitly require identifying/explaining the cause and locating the necessary change, **not a complete validated repair**. Optional edits can confirm a hypothesis. Bug 1 supplies a rendering-function pointer; other tips clarify application terminology. The paper's printed `80,000 kLOC` unit and the tutorial's approximately 100k TypeScript lines are not reconciled by counting the application here. The codebook identifies Excalidraw revision `79d9dc2f8f86b38d1784519eb765d1a13416fdab` without establishing that every session used identical bytes.

Replay removed breakpoint and rewind/resume controls during the study. The paper acknowledges this version change; the released material does not supply a complete per-session version allocation. Thus the treatment includes training, interface and version conditions, not an isolated ability to move backward. Four tasks contain no preexisting console-log outputs for testing Replay's output-to-code advantage; console errors and added prints are distinct.

## Outcomes and reconstruction

Table VI and the two coded workbooks agree on the following retained attempts. Unsuccessful task times are assigned 40 minutes by notebook cell 12, including early give-ups, and some strategy notes describe success after the cap. These are capped task scores, not actual uncensored time to success.

| Bug | Chrome success / 5 | Replay success / 5 | Chrome / Replay median capped minutes |
| --- | --- | --- | --- |
| 1: empty frame name | 2 | 1 | 40 / 40 |
| 2: bound-text alignment | 4 | 4 | 11.93 / 24.23 |
| 3: arrow library insertion | 3 | 2 | 34.58 / 40 |
| 4: image identifier | 2 | 2 | 40 / 40 |

Across retained sessions, successes are 11/20 Chrome and 9/20 Replay. The four reported time-comparison p-values are .239, .917, .106 and .504. Nonsignificance does not establish equivalence or prove that replay can never help. The first relevant-code milestone uses a 40-minute value if unreached and excludes Bug 1 because of its supplied pointer. Different bugs, only four task instances, selection and paired participants constrain generalization.

The strongest observed behavior difference is fewer reruns: median 10 Chrome versus 2 Replay, with 219 versus 50 total coded reruns. Per-bug medians are 15/3, 5/2, 12/2 and 10/2. Stored notebook output reports the pooled Mann–Whitney result `p=0.00001927`; the arithmetic reconstruction checks counts/medians, not a fresh statistical replication. The notebook's pooled tests use tool-level samples rather than a participant-paired model, despite each person contributing to both tools on different tasks. Multiple exploratory outcomes are tested without a stated multiplicity adjustment.

The paper describes Replay reruns as initial recordings or checks after behavior changes. Figure 7 and the raw rows are more qualified: Replay has 30 initial, 9 behavior-change and **11 other** reruns, the latter spread over six sessions. Chrome has 15 initial, 19 behavior-change, 77 value-collection, 29 execution-check and 79 other reruns. Thus zero Replay reruns coded as value collection/execution checks is supported; a literal claim of only two rerun purposes is not. These categories infer purpose from surrounding actions, not direct complete measurement of intent.

Debugger-mediated navigation medians are 3.5 Chrome and 10.5 Replay, matching the reported threefold ratio and stored `p=.04394`. Overall navigation and nondebugger actions are nonsignificant (`p=.409` and `.776`). Navigation coding requires a visible declaration/tool change lasting over one second; an unchanged-location step is not counted. More recorded navigation actions do not directly measure more mental effort.

Value-view rows total 215 Chrome and 326 Replay. Print rows are 16/215 (7.44%) versus 60/326 (18.40%), matching Figure 9; the stored per-session proportion test is `p=.0002999`. These are actions/expressions, not all printed runtime instances: the notebook counts rows without multiplying the separate repeated-output field. Automatic local-variable displays are excluded; hover/expansion are deliberate actions, and unique values are operationalized using expression strings. Most views are simple variable/field expressions. More print use is not evidence of more distinct information, and the reported per-bug total/unique-view comparisons are nonsignificant. Replay feature-user counts independently match 17 jumping, 19 rerunning and 17 printing.

## Qualitative explanation and limitations

Sections V–VI and the strategy summaries distinguish execution access from finding the relevant cause. Event jumps can land before a fault or in a callback whose next displayed line does not execute next. An operating-system file-picker action is absent from the recorded browser-event list. Breakpoint versus timeline controls, hidden navigation menus, print placement before a declaration and hit-count interpretation cause difficulties. Replay can avoid interference between reproducing an edit and interacting with a conventional debugger, yet still leave the decisive function unidentified.

The error-message-search comparison (8 versus 12 error-task sessions; median first-location times 1.8 versus 14 minutes, reported `p=.0033`) is an observational strategy association, not randomized evidence that telling users to search will produce that effect. Supplemental strategy prose sometimes discusses post-cap successes; it must not replace the frozen success counts with a favorable subset.

Two authors developed codes from four recordings and iterated reliability coding on seven recordings. Reported kappas are .7525 navigation, .817 value viewing and .7794 reruns; the first author then coded all sessions. Two navigation codes were added after reliability assessment, as marked in codebook p. 6. No new reliability estimate for the extended scheme is supplied. We did not independently validate the coding or all notebook analyses.

## Consequences for Nu and the frontier

- **Unique:** execution history and navigation interventions have substantial prior art. A new Nu claim must specify its state/effect/lifecycle contract and incremental contrast, not claim the invention of reversible debugging.
- **Valuable:** rerun reduction is a plausible mechanism, but it does not establish faster successful diagnosis, complete repair or net maintenance benefit. Interface discoverability, output-to-cause navigation and ordinary search are credible rivals. This is contrary evidence to an automatic productivity inference, not evidence that Nu is ineffective.
- **Scientifically valid:** preserve all assigned attempts, exclusions, participant/task dependence, endpoint definitions, tool versions, training and unobserved effects. Do not replace behavioral success with trace availability or action counts. No effect here licenses a Nu sample size or experimental start.

The incoming Scite graph has one edge/two nodes and is explicitly low coverage. Its 2026 FSM-Rewind neighbor, DOI `10.1109/ITET70052.2026.11650998`, remains a title-level educational visual-programming lead; a secondary abstract was located but is not primary methodological evidence. Four exact backward identities were verified with `limit:20`: Java Whyline (`10.1145/1518701.1518942`), Hypothesizer (`10.1145/3586183.3606781`), omission finding (`10.1145/2695664.2695735`) and time-travel queries (`10.1109/QRS54544.2021.00074`). Their full methods become necessary if causal-query/navigation interventions or their positive numerical effects enter the proposed contrast. No such effect is imported here. S67's direct game-prototyping comparison remains the next promoted read; generic debugger collection is not a substitute for resolving that claim.
