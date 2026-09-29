# S67 — Pronto's single-view game prototyping tradeoff

**Reading completed 2026-09-30.** Eva Krebs, Tom Beckmann, Leonard Geier, Jonathan Grenda, Stefan Ramson and Robert Hirschfeld, *All in One: Rapid Game Prototyping in a Single View*, CHI 2025, seventeen pages, [DOI 10.1145/3706598.3714251](https://doi.org/10.1145/3706598.3714251). This direct Pronto/Godot comparison can qualify claims that fewer context switches and more immediate feedback improve game development. It studies human throwaway prototyping, not Nu maintenance or coding-agent performance.

## Identity and actual coverage

Zotero `B7WRUVZZ`, PDF `JAMTP6XJ`, acquisition note `2X699TQN`, in root `PKLXQNEE` and temporal/game-tools `NDU9BTP7`. The [author-hosted publisher PDF](https://www.hirschfeld.org/writings/media/KrebsBeckmannGeierGrendaRamsonHirschfeld_AllInOneRapidGamePrototypingInASingleView_AcmDL.pdf) is CC BY 4.0, 1,858,477 bytes, SHA-256 `8e21a56cd8d09fe232e9bd5ea993b65ad4af868e3f7736f99b6a869151daccf6`. All seventeen pages, sections 1–7, appendices A–C, ten figures, four tables and 42 references were read. Renders of pages 3–6, 9–10 and 15–17 were inspected, including the timeline, full participant table and rotated interview-dimension headings.

The ACM landing page returned 403; Crossref supplied paper links and no supplementary relation. A targeted title/DOI/material search and the author's project page led to [the public repository](https://github.com/hpi-swa-lab/godot-pronto). A dated default-branch check selected commit `d2afe885f6ecd98cfcb10b188454c390309d379f` (2024-02-10), the latest returned before 2025-04-26. Its recursive tree has 205 entries and is not truncated. The complete [README at that revision](https://github.com/hpi-swa-lab/godot-pronto/blob/d2afe885f6ecd98cfcb10b188454c390309d379f/README.md) was read, SHA-256 `b53ac7cd52076b14e40ab737de79fe4d978a1e4de84dec26b30f2ce273037d5a`. A path screen for study/participant/evaluation/supplement/questionnaire/interview/results and CSV/XLSX found no candidates in that tree. This bounded check does not prove data absence on other branches or servers, or equivalence to the study build. Unauthenticated GitHub API rate limiting was resolved using the existing authenticated read-only CLI.

No original recordings, transcripts, raw timings or coding files were acquired. No program, game, deployment or author experiment was executed. The paper's table arithmetic was reconstructed independently; the repository check is documentation/tree coverage, not an implementation audit. The README's deployment instructions were read as source material and not followed.

## Mechanism and explicit limits

Sections 3.1–3.5 place game objects and visual representations of behavior together in Godot's scene view. Connections combine signals with methods/expressions and optional conditions. Behaviors expose input, actions, state, visualization and debugging facilities; arbitrary Godot functionality remains available. The platform controller and health bar are specialized conveniences, so the comparison bundles spatial organization with higher-level APIs, discoverability and live visualization.

The running game still has a separate view. A HUD exposes selected constant Values for editing and synchronizes those edits back to the initial scene. It does not solve arbitrary runtime-state migration: lowering jump distance after reaching a high platform can leave a state unreachable from the new initial parameters. Store/Watch/Inspect display state and connection arrows flash on signals, but the paper does not establish full trace fidelity or replay. Spawner subtrees support linked copies and local state; a changed copy property stops tracking the template. Local/global connections ease access while adding dependency obligations.

The design deliberately prioritizes immediate access for one or a few mechanics. A duplicated condition must be edited in several connections or moved into a separate Code behavior. Dense scenes reduce label readability and make flashes less useful; abstractions/subscenes could reduce clutter while losing the single-view advantage. The paper reports that stepping through connections introduces framework stack frames and may obscure some bugs. No such obscured bug occurred in this selected study, which is not evidence that the risk is absent.

Godot already supports live synchronization and relevant input helpers. Some participants requested features already available but did not use them. The defensible comparison is experienced use of these tool bundles under the supplied training/tasks, not availability versus absence of live editing. The older README also documents reparenting/connection and instance-edit pitfalls, reinforcing the need to specify actual versions rather than infer universal safety from visual proximity.

## Two distinct evaluations

**Cognitive walkthrough, section 4:** one Pronto developer performed an expert walkthrough twice over three days. It assumes an experienced user, chooses a direct path, includes no mistakes and uses only six of 32 behavior nodes. The 64 actions crossed with seventeen questions produce 1,088 potential judgments, of which 115 were noted as consequential. These are not 1,088 independent participants, failures or trials. Insights concern component granularity, repeated-condition edits, persistent parameter changes, mouse interaction and documentation. The single evaluator and constrained actions limit coverage.

**User study, section 5:** eight volunteers from 25 eligible seminar students, seven male, four bachelor/four master students, 4–7 years of software development and no professional game-development experience. Five had extended Pronto behaviors and contributed fixes, although not its core design. Three additional pilots led to task/time adjustments. Familiarity, contribution and volunteer selection limit beginner and professional inference; the fifteen-minute refresher did not restore all participants' prior knowledge.

Each participant completed a driving/sliding task and a platformer-dash task, one with each tool, in four manually assigned order conditions used twice each. This is within-person counterbalancing, not random assignment or a regular Latin square. Each tool/task cell contains four attempts. Figure 7 separates **45 minutes implementation plus 15 minutes interview** in each one-hour task block. Work stopped after more than ten extra implementation minutes; incomplete rows in Table 3 are 55 minutes. Each task introduces two later environments requiring adaptation/tuning. This is a small related set of mechanics, not broad maintenance-task diversity.

Hints were provided after at least two minutes stuck, an independent attempt and participant request/agreement, where the researcher judged further struggle uninformative. Hence outcomes are assisted, with a discretionary intervention. Interviews have fifteen questions, thirteen mapped to cognitive dimensions; repeated questions emphasize change friction. Transcripts were machine-transcribed/corrected, thematically analyzed in MAXQDA, and quoted German passages machine-translated then corrected. The paper reports fifteen themes and presents eleven; four failed verification or were less relevant, without a complete public coding trail here. The authors explicitly did not reach saturation.

## Quantitative boundaries and arithmetic

Table 3 permits the following reconstruction. The paper's average progress score is not the percentage of fully successful attempts. The timing means in the prose exclude incomplete tasks.

| Quantity | Pronto | Godot |
| --- | ---: | ---: |
| Assigned attempts | 8 | 8 |
| Rows with 100% progress | 6 | 5 |
| Rows with 66% progress | 2 | 3 |
| Mean printed progress | 91.50% | 87.25% |
| Mean minutes, complete rows only | 39.83 | 36.80 |
| Mean recorded minutes, all rows including 55-minute incomplete rows | 43.625 | 43.625 |
| Total recorded hints | 16 | 11 |

This independently matches the rounded completion means (40/37 minutes) and explains 91.5/87.2 progress scores, with rounding limits retained. Across eleven complete rows the mean is 38.45 minutes. From printed integer minutes, complete-only population/sample standard deviations are 11.16/12.22 for Pronto and 6.91/7.73 for Godot; the prose reports 11.68 and 9.49. Those per-tool dispersion figures are not reconciled by these ordinary conventions. Exact unrounded timings and the analysis denominator would be needed; do not silently replace the source's values. The combined population deviation is approximately 9.586, close to but not exactly its 9.56. There is no fresh significance test or inferred treatment effect here.

The authors explicitly state in section 6.2 that their study cannot determine whether participants prototype faster. They also explain that time to a prescribed endpoint can miss useful experimentation. Equal all-row recorded means are descriptive arithmetic, not equivalence evidence. Complete-only means neither establish Pronto speedup nor show it is slower for the general population. Independent quality, useful iteration count, long-term maintenance and end-to-end learning/support costs are unmeasured.

## Qualitative findings and implications

Six participants praised runtime visualizations; six described an overview of progress, while five criticized connection-label readability. Three explicitly perceived faster prototyping. Five praised helpful predefined behaviors, but three reported ambiguous overlapping components. Godot received praise for documentation from four and criticism of debugging from seven; some criticism concerned undiscovered existing features. These counts are theme mentions from eight selected people, not prevalence estimates or independent effect measures.

The value is a concrete tradeoff: direct access, visible state and a task-suited vocabulary can encourage experimentation, while distributed snippets, hidden data dependencies, absent documentation and crowded scenes create costs. The prior author/seminar examples demonstrate feasibility; they do not independently validate the later study.

- **Unique:** single-view composition, live parameter tuning and visualization have close game-development predecessors outside functional engines. Nu cannot claim these generic mechanisms as new. The 2023 Pronto paper is a precursor, not an independent replication; this later paper explicitly adds high-level behaviors, HUD and evaluation.
- **Valuable:** interface/API fit and documentation are plausible rivals to architectural simplicity. Perceived progress and more visible events do not establish complete correct maintenance or net effort savings. A useful question may concern boundary conditions and adverse changes rather than a universal architecture ranking.
- **Scientifically valid:** distinguish tool bundles from source conventions; retain all attempts, assistance, learning, task/participant dependence and initial/runtime-state inconsistencies. Measure a beneficiary-relevant endpoint and the cost of support. An expert cognitive walkthrough can generate risks but cannot replace independent behavioral tests or substantiate coding-agent outcomes.

## Follow-up disposition

The incoming Scite graph returned two edges/three nodes, explicitly low coverage. Exact DOI lookup requested twenty and returned both: `10.35970/jinita.v8i1.3021` concerns a facial-classification exhibition client and is outside the maintenance/prototyping contrast; `10.1145/3772318.3791263` concerns creative-activity traces and remains conditional if creative-process outcomes are adopted. A primary author announcement establishes that latter scope, not its full methods or an effect size. The sparse graph does not establish complete forward coverage.

Four backward identities were verified in one twenty-record request: Ko et al.'s human-tool experiment guide (`10.1007/s10664-013-9279-3`), the memory-tool walkthrough/user study (`10.1145/3394977`), the liveness literature study (`10.22152/programming-journal.org/2019/3/1`) and model-driven game prototyping (`10.1145/1541895.1541909`). They remain conditional on adopting their human-study, liveness-taxonomy or generation mechanism. S38's cognitive-dimensions record already exists; no new scale is adopted for coding agents. The earlier PPIG Pronto account remains conditional on historical details not covered here. None of these uncompleted sources supplies a borrowed positive effect or a claim of global novelty.

The promoted Pronto/Godot comparison is now resolved at full-paper scope. The next work is reconciliation of the Nu/public-essay/derived-sibling claim map and remaining explicit access/conditional gaps, before further formalization. No construction or experimental allocation is authorized by this reading.
