# S227 — GUI playtesting, repair memory and the unit of improvement

Yixu Huang, Bo Li, Na Li, Zhe Wang, Kaijie Chen, Haonan Ge, Qingyi Si, Yuanzhe Shen, Ruihan Yang, Guangjing Wang and Hongcheng Guo. **GUI Agents for Continual Game Generation.** [arXiv2605.28258v1](https://arxiv.org/abs/2605.28258), 27 May 2026, DOI10.48550/arXiv.2605.28258. Read 2026-10-02. [Bo Li's publication page](https://primerl.github.io/) reports August acceptance to Findings of EMNLP2026; the exact-title ACL Anthology search returns no record. This reading covers the identified preprint, without inferring correspondence to a final conference edition.

## Identity and coverage

Native parent **`28BG5ATZ`**, note **`8EWIM8MT`**, PDF **`54YSM7FI`**, collection `PKLXQNEE`. The record precedes selected reading; parent/PDF versions5236/5243, parentage, membership and stored bytes are freshly verified before continuation. The PDF is **19 pages, 23,073,155 bytes**, SHA-256 **`8e3f708dd4cc272f1f67bc3c95601660ea28aa36e9a45a2965d7324b75020ced`**.

All19 pages are read, including eight main sections, Limitations, AppendicesA–H, seven figures, seven tables and58 references. Thirteen pages are inspected visually:1–8,13–15,18–19. Initial sorted extraction interleaves columns; visual inspection and ordinary extraction resolve the affected passages. Truncated middle-page outputs are recovered before coverage credit. Figures establish printed contents, not authenticity of the illustrated gameplay traces. No game, browser demo, agent, author analysis or benchmark is run.

## What is built and evaluated

PlaytestArena has **200 HTML/CSS/JS game-generation prompts in eight genres**, derived from an initial247 candidates. Five non-author graduate/recent-graduate experts write prompts and observable rubrics, with second-expert and lead-author checks for concreteness, observability and faithfulness to the prompt. Three calibration topics are discarded; a peer re-review of10% of criteria reports95.3% acceptance before revision. These are useful specification-quality procedures, not proof that every criterion has a valid executable observation.

The reported corpus has **1,548 criteria**, mean7.7 per game. The score for a game is the fraction a GUI judge marks passed after playing; it is neither whole-game correctness nor user enjoyment. Mechanics, controls, progression, interface and visual feedback are separate rubric dimensions. Topics are curated for a self-contained generation task, not sampled professional maintenance episodes. One game is repeatedly repaired against its original prompt; this is not a sequence of independently introduced requirements or verified live-state migrations.

A separate feasibility study has20 simple games—ten generated and lightly debugged, ten public static web games—decomposed into **118 levels**, rounded to roughly120 in the main text. It excludes action/shooter genres because inference latency complicates real-time play. Agents receive a guide and screen, no rubric or memory, and have20 episodes per level, each up to five minutes. Three humans get matched viewport/browser/time limits and repeat until success or20 attempts. Pass@k is a level with at least one successful episode, not success on an arbitrary single playthrough. GPT-5.4's pass@20 is.82 versus human.92; Sonnet.79 and Kimi.72. Timing and low-contrast recognition failures remain. This supports limited playing feasibility, not judge correctness on the full200-task population.

## Feedback and memory contract

Play2Code couples a coding agent to a GUI playtester. The coding agent designs the game and guide, generates assets, implements, performs build/headless checks and stores lessons. In later rounds it usually skips design/assets, considers the previous play summary/fix list and chooses which suggestions to apply. Its guide describes controls, mechanics and intended endings.

The GUI playtester receives that guide, screenshots and relevant memory. It has browser input/screenshot tools but is described as lacking source, DOM, console and internal-state access. It observes loading, starts the game, attempts interactions and retries, then emits a structured outcome, confidence, chronological log, assessments, severity-tagged findings and fix direction. For platformers it must try materially different retries before declaring blockage. The coding agent may accept or reject advice.

Crucially, **the development playtester does not receive the evaluation rubric**; the separate scoring role does. Reported rubric scores after each round are measurements, not specified repair inputs. A high-confidence `completed` or `reached-ending` development outcome can stop repair; otherwise the loop ends at five rounds. The release does not provide the full evaluator/scaffold needed to verify this information boundary. There is no evidence here that final rubric scores were fed back, and no basis to certify their isolation from source alone.

Episode memory retains within-task rounds and attempts; role-specific skill memory and shared world memory carry lessons across tasks. Entries have layer, owner, kind and archetype tags. Cross-task experience makes task order, initialization, reset and reuse relevant to the experimental unit. Their full schedule and held-out transfer protocol are not supplied. Shared memory is an implemented design claim in the paper, distinct from a verified released agent implementation.

## Positive results and what the comparisons identify

The reported method means are **29.7% Direct LLM,52.2% OpenGame and66.8% Play2Code**. The Play2Code scores for GPT-5.4/Sonnet4.6/KimiK2.5 are72.3/71.1/56.9. Every genre/model comparison in Table3 favors Play2Code over its corresponding baseline, a substantial favorable result on these rubrics.

Table3's reported model averages track equal-weight genre means. For example, our arithmetic on its eight GPT-5.4 Play2Code cells gives72.325%, whereas weighting those cells by Figure3's game counts gives73.5925%. These are calculations on printed aggregates, not raw-data reproduction. The66.8% headline is not established as the proportion of all1,548 criteria passed or the proportion of games fully correct.

Direct LLM gets one generation. OpenGame has up to five build/inspection rounds and stops when it compiles and reaches a stable running state; Play2Code has up to five coding/play rounds and a different stopping criterion. A common round cap does not equalize inference calls, token cost, wall time, assets, memory or information. AppendixE reports mean effective rounds3.24, median3.05 and93.5% early termination without resolving the fractional-round aggregation unit. The pipeline comparison cannot by itself isolate a pure playtesting-signal effect or establish net efficiency.

The GPT-5.4 ablations, judged with GPT-5.5 per AppendixF, provide a closer component comparison:

| Configuration | Rubric score |
| --- | --- |
| No accumulated memory; previous build/report retained |64.1%|
| Episode memory only |69.3%|
| Episode plus role-specific skill |71.8%|
| Episode, skill and world memory |72.3%|
| Full memory, GUI replaced by code self-verification |58.7%|

Thus reported nested increments are5.2,2.5 and.5 percentage points; full versus no-GUI is13.6 points. Preserve these favorable contrasts. They do not establish statistically independent/additive memory effects, interaction-free transfer or necessity for every task. There are no supplied repeated-run intervals, cost-normalized results or raw observations supporting stronger claims. The self-verification variant also removes an external role's observation and work.

## Judge validation and the human comparison

Three non-construction annotators blindly score32 generated builds, four per genre with methods/quality represented. They receive prompt and rubric, have ten minutes like the GUI judge, and cannot answer “unclear.” They are blind to method, machine verdicts and traces. Average GUI–human agreement is **84.2%, κ=.64**, with game-score Spearmanρ=.87 and Pearsonr=.88; Table2 reports human–human90.7%, κ=.66. This is useful human-alignment evidence, not proof of method-comparison robustness, population equivalence or an infallible oracle. Forced binary decisions collapse failure-to-observe and observed failure; aggregate correlation does not exclude method-specific scoring bias.

The selected edition has material correspondence problems:

- AppendixB says5–11 criteria per game, while the32-game validation subset has375 criteria, mean11.7 and range9–15. Even32×11 is only352. Figure3's boxplots also extend beyond11. The validation subset's exact rubric version/unit is unresolved.
- Table5 prints85.7% for average human–human agreement, while its three rows91.6/89.8/90.7 average90.7%, matching Table2. This arithmetic discrepancy does not erase the reported favorable GUI agreement.
- AppendixH says human-driven repair outperforms GUI repair at every round. **Figure6b's legend labels the green upper curve GPT-5.4 and the gray lower curve Human.** The direction is unresolved between plot and prose; neither an author correction nor a reversal is invented.

The repair comparison uses five students on50 “moderate” tasks, one human per task, without rubric access. Humans supply free-form reports and no explicit human-side memory entries; the coding agent retains its memories. Reports, guide/prompt exposure and logging are not identical to the structured GUI condition. Claimed greater traceability comes from the logging design, not a controlled test showing humans cannot provide recorded traces or a measure of report accuracy. Figure7's different feedback-category shares are descriptive; their classification procedure and raw denominator are not reconstructed.

## Post-outcome groups and time-dependent coverage

AppendixG defines complexity tiers **from the observed five-round score gain**, averaged over three backbones: high Δ≤10, moderate10<Δ≤15, lowΔ>15, described as terciles. The authors explicitly call this descriptive, not causal. These groups cannot establish that independently measured complexity causes smaller gains or that GUI capability is the sole bottleneck. The50-task human subset's relationship to an approximately one-third tier is unspecified.

The plot's “low” average trajectories gain less than15 points, whereas “moderate” trajectories gain more than15, contrary to those printed threshold definitions; the text likewise describes moderate as having the largest gain. With93.5% early stopping, the five-round trajectory population/carry-forward rule also matters and is not supplied. Monotone group averages cannot show that every individual trajectory preserves prior behavior. Reset, latency, unvisited states and inaccessible endings remain observation limits even when the GUI agent plays successfully.

The broader rhetoric that code/specification-based evaluation cannot establish gameplay behavior is too strong: [S123](S123-playspecs-trace-semantics.md), [S125](S125-game-logic-bench.md) and [S226](S226-gamedevbench.md) already distinguish formal/temporal assertions, finite state checks and rendered observations. GUI testing adds valuable surface coverage; it does not displace every other behavioral oracle.

## Released artifact and remaining action

The [project website](https://continual-game-generation.vercel.app/) offers eight demos. Its live HTML is byte-identical to `public/index.html` at discovered [gallery pin `8c5e1675fc25da0876e48dcbe1da5f5f4e57bed7`](https://github.com/RunRiotComeOn/gui-agents-for-continual-game-generation/tree/8c5e1675fc25da0876e48dcbe1da5f5f4e57bed7),27May2026. The untruncated tree has296 blobs. README, package and deployment configuration are fully read; HTML links are parsed, not executed. They identify a static gallery, not the full200-task/rubric/evaluator/result release. Other game bodies are not read or run.

The119,393-byte `code2play.txt` is an anonymous submission text ending on numbered page17, not an agent implementation. An initially oversized output is truncated; only its visible opening/tail plus explicit first/last20-line recovery are credited. Its full alternative edition is unread. SHA-256 **`64184e7c44a11575911f109ca682a6e797c9d0784e6c9b3b100ca2e3d23ab121`**. Gallery README hash **`51d0b537adb43ad67fdff214b76ce9f37897440cca6172133e61cf56372720f1`**; live/source HTML hash **`d1ece8916a9346649807e17a727b6c600d4012966190f3495970c16c62cf67e2`**. This bounded release inspection does not prove that no other artifact exists.

**Disposition:** prior game-coding/playtesting/memory loops and favorable curated-rubric outcomes are established at the paper's reported scope. Actual benchmark release, judge/version binding, trajectory accounting and matched resource effects remain separate gaps. No Nu-specific architecture, source-convention benefit, live-state guarantee or net human replacement benefit follows.

**Next:** reconstruct already-recorded S228's industrial edit/play and client/server temporal tests. OpenGame's primary baseline behavior and the cited incremental knowledge-graph playtesting method are conditional dependencies if they change the contrast; C05's unconsumed abstracts remain a separate discovery frontier. Reading these sources authorizes no new agent worker or experiment.
