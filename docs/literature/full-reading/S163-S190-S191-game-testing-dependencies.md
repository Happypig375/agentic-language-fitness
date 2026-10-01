# S163 / S190 / S191 — review lineage and a bounded audio oracle

Selected readings on 2026-10-01 by the main Codex session. These theses clarify [S163](S163-game-coverage-taxonomy.md); neither is fully read or an independent validation of the paper's taxonomy. Native DOI/title/edition duplicate checks preceded record creation, and records preceded PDF body reading. Existing memberships and attachments are preserved.

| ID / primary source | Native parent / PDF / note | File identity and actual coverage |
| --- | --- | --- |
| **S190**, Mattia Riola, *Test automation in video game development: Literature review and Sound testing implementation*, Politecnico di Torino, 2023, academic year 2022/23; [repository](https://webthesis.biblio.polito.it/27719/) | `W6QLSXQD` / `WPVFJBE3` / `VRC3YIHA` | **119 pages, 4,286,118 bytes**; SHA-256 `d6f06f53304727aba9cc66d75ffa2f2eec553e0a6b7be24a5f66bc105815d595`. Physical **1–8, 25–35, 91–101** text-read: **30 pages**, including blank pages. Eight visual pages **33, 92–95, 97–99**. Other result chapters and bibliography remain unread. |
| **S191**, Serenella Manzi, *How to Measure Game Testing: a Survey of Coverage Metrics and an Implementation on the iv4XR Framework*, Politecnico di Torino, 2024, academic year 2023/24; [repository](https://webthesis.biblio.polito.it/31758/) | `ELJDK92V` / `9RY73Q4N` / `IN2KPU5I` | **90 pages, 7,579,991 bytes**; SHA-256 `dc2e77715975199dacf047d5d3ce3eb6c36dd19e0816f080aa5b6f8ad833dbf9`. Physical **1–8, 29–44** text-read: **24 pages**, including blank pages. Seven visual pages **34, 37–39, 41, 43–44**. Implementation pp. 45–80, conclusion pp. 81–84 and bibliography pp. 85–90 remain unread. |

All-page text extraction supplies locators only; it is not all-page reading. S190 printed body pagination is physical minus fifteen. S191's inspected taxonomy uses its visible physical numbering. No software was installed or executed and no new detector/fault trial was conducted.

## S190's broader multivocal review — physical pp. 27–35

The review asks about testing levels, goals, metrics, tools and bug types. Its scope and source population differ from S163's later metric subset. The abstract reports 765 retrieved and 118 retained studies; Table 4.2's source counts sum to **766**, with **684** after deduplication and **113 retained = 57 white + 56 grey** in the method. The abstract also reports four levels, 24 goals, 43 metrics and 129 tools; the unconsumed result chapters have not been independently reconciled to those totals.

The declared period is 2012–2022, with English/Italian peer-reviewed accessible white literature and selected grey-literature tiers. Searches use Scopus, IEEE, ACM, ScienceDirect, Springer and Google Scholar, plus Google Search and GameDeveloper. Query syntax varies across repositories and title/abstract fields. Google Search covers ten pages/99 results. Springer export uses overlapping 2012–2020 and 2020–2022 ranges because of a 1,000-entry limit. Zotero and Notion support extraction. The selected method classifies white versus grey sources rather than assessing their actual empirical-method quality. It omits snowballing because the available volume was considered sufficient; this survey does not adopt that as a stopping rule.

The broader review is acknowledged in S163. Its differing numbers cannot be silently substituted for S163's 65/25 flow. No released row-level study list was acquired through the selected sections and metadata routes. A mentioned table-extraction repository is a locator, not inspected review data or a verified analysis release.

## S190's implemented sound check — physical pp. 91–101

The implemented demonstration records LabRecruits output and checks for expected sounds near observed in-game events. It is more specific than a played-sound coverage fraction: an expected asset and observation window define a verdict. The abstract reports six sounds and three levels; the chapter describes three levels with at least three sound checks per level. This is a small constructive evaluation, not a controlled comparison of testing strategies or a calibrated fault-detection study.

The Windows 11 setup records stereo-mix output through Python/Librosa. Reference assets are converted to 44.1 kHz, 16-bit mono little-endian WAV. The selected recordings last sixty seconds. Java `AudioSignal` represents samples as 16-bit values and computes windowed FFT information. Configuration controls chunk size and frequency fuzzing; reference chunk hashes store sound identity and timestamp.

The fingerprint combines four frequency-band peaks after rounding each down by its remainder modulo the fuzz factor, with weights **10^8, 10^5, 10^2 and 1**. Recognizing an expected sound counts matching hashes in a requested recording interval and accepts a count **greater than** a threshold. A hash may correspond to chunks from different assets. Match counts are not independently calibrated probabilities, even where the explanation uses probabilistic language.

The chapter reports favorable no-background configurations `(threshold, fuzz, chunk size)` of **(3, 2, 512), (11, 3, 512) and (2, 2, 1024)**. With background music reduced to **30% volume**, it selects **(13, 3, 512)**. Figures 5.2–5.3 show ROC curves; the underlying trial counts, held-out split and uncertainty needed to reconstruct their operating characteristics are not supplied in these selected pages. The exact false-positive/true-positive coordinates were not digitized. Calibration on this game is not evidence of stable sensitivity across audio mixes, assets or games.

Event observers record occurrences such as a button press, monster attack or fire damage. Tests start the game and recording, play the level, stop and save the recording, then check expected audio near the recorded events. Figure 5.4 confirms this post-execution pipeline and eventual recording deletion; it does not prove exact clock alignment or specify a universal event-window policy. The method depends on observation fidelity, trigger coverage, clock relation, selected window and asset discrimination. Detecting an expected sound near an event does not establish that the event caused it, that unintended sounds were absent, or that every sound obligation was checked.

The future-work section explicitly proposes **checking the temporal order of matching chunks**, background suppression, transformed sound recognition and simultaneous-sound overload tests. Thus the current hash-count threshold should not be described as validating the internal temporal sequence of a sound. The author also calls for more diverse projects to distinguish inherent efficacy from the simplicity of this example. Those are material method limits, not a reason to erase the implemented event-linked output check.

Physical pp. 25–26 describe RiverGame's spectrogram/statistical and speech-matching methods secondarily. Its primary paper remains unread; no RiverGame reconstruction or comparative superiority is claimed. A generic iv4XR demo repository reference does not by itself locate this custom implementation. No matching release was acquired and no source or audio trials were reproduced.

## S191's expanded taxonomy — physical pp. 29–44

The selected chapter repeats **65 initial / 25 retained, 22 white / three grey, 2012–2023**, English/Italian and game-specific metric use. It lists ResearchGate among white-literature routes and BrowserStack/GameDeveloper among grey routes, extending the short paper's named portals. It provides term families but not complete executed per-engine searches, dates or included rows.

Quality assessment and snowballing are said not to be reported because their application did not significantly improve results. This statement does not supply the procedure, assessed units or actual findings needed to certify either check. Open/axial coding merges related metrics, excludes generic unit-code coverage and assigns the same 26 definitions across six categories. Figure 3.1 and Tables 3.1–3.6 corroborate the taxonomy. Functional UI/gameplay form a higher-level grouping; multimedia, UX, performance and reliability retain separate targets.

Contextual discussion includes stress/soak, compatibility, regression, maintainability and recovery. The displayed measures are still the specific coverage/resource/bug/crash definitions. Merely naming fault tolerance above bug/crash counts does not measure successful recovery, and discussing realistic physics does not add a verified physics oracle. No aggregate metric or independent cross-game validation is established by the selected chapter.

The thesis summary promises an iv4XR/LabRecruits implementation with custom and demonstration tests and notes generalization limits. Its implementation chapters are **unread**. The summary is a reason to revisit those methods when consequential, not evidence that their instrumentation, data or claimed benefits have been reconstructed.

## What changes in the synthesis

The three records form a related review/implementation lineage. S190 offers a broader source pool and a narrow explicit external-output oracle; S191 expands the metric taxonomy and supplies an acquired but unread implementation route. They cannot be pooled as three independent validations of a coverage-to-quality relationship.

For B05/B07/B12, the positive contribution is concrete measurement vocabulary plus an example of translating an expected output into a bounded check. Coverage denominators, finite windows, environmental capture, calibration and independent fault sensitivity remain separate obligations. S123/S124 already show explicit game specifications; S163's broad implicit-oracle characterization must be qualified accordingly. No Nu, language, source-convention or agent-maintenance effect follows.

Next return to the older accessible S140 composition-law dependency; retain S191's implementation and the primary audio-method route only where they can resolve an explicit measurement uncertainty. Partial-thesis reading is recorded as partial rather than expanding the full-reading count.
