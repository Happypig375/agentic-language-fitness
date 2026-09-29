# S63 — interactive replay and observed debugging behavior

**Full author-file reading completed 2026-09-29.** Brian Burg, Richard Bailey, Amy J. Ko and Michael D. Ernst, *Interactive record/replay for web application debugging*, UIST 2013, [DOI 10.1145/2501988.2502050](https://doi.org/10.1145/2501988.2502050). Zotero `HRGZQ95K`, attachment `7Y9WI5WZ`. The [author-hosted PDF](https://faculty.washington.edu/ajko/papers/Burg2013Timelapse.pdf) contains eleven pages, 955,771 bytes, SHA-256 `cd5fa1b96df5b125bc8cd3135674a1b728feae60bb96ae51ed81500d13fd63e3`. All pages, eight figures, two tables and 36 references were read; pages 2–9 were rendered and inspected. No browser, benchmark or participant experiment was executed.

The file has a 2021-06-25 update stamp and printed pages 473–483. Bibliographic metadata gives 473–484; the second author-hosted route also exposes an eleven-page file. Preserve this edition discrepancy rather than inventing a missing page or claiming publisher-file equivalence. The selected coauthor landing page confirms the paper and links its implementation. This reading supports claims about the actual author file.

## Mechanism and boundaries

Dolos modifies WebKit to record inputs at the embedder/platform interfaces; Timelapse provides timelines, breakpoint history and bookmarks. Incoming events include user actions, timers and network responses. Environmental calls such as time and random values are memoized. Recorded input and re-execution reconstruct a prior state; this is not storage of every intermediate state or inverse execution. Bookmarks combine a preceding input, breakpoint and replayed stepping commands. The fictional Claire walkthrough illustrates affordances, not a participant outcome.

Replaying blocks actual network requests and supplies recorded headers/data. This controls client-side observations, not remote server state or arbitrary external effects. The fidelity claim covers DOM-event order/content; it expressly excludes identical layout/paint counts. Touch, Battery, Sensor, Screen and Clipboard APIs are among unsupported prototype inputs. Plugins and the architecture of other browser engines impose additional boundaries. DOM-node/event-count checks detect some divergences; they are not a complete independent behavioral oracle. Users may ignore divergence warnings.

Breakpoints are disabled while recording or seeking and enabled during real-time playback. Adding logging in the example requires a new capture. Do not generalize the paper to replay after arbitrary source edits, restored external effects or unconstrained persistent snapshots. It requires neither FRP nor immutable game state, making it a direct rival to any claim that those language mechanisms are necessary for replay tooling.

The reported implementation adds 7.6K SLOC across 74 new and 75 modified files against about 1.38M WebKit SLOC. Deployment uses a custom dynamic library/load path. Those figures describe code and setup, not engineering effort or an intervention with zero cost.

## Runtime measurements

Table 2 separates three noninteractive workloads from four interactive workloads. The Space Invaders entry uses **scripted gameplay**, despite being a game. Reported relative times are:

| Workload | Baseline seconds | Recording | Replaying | Seeking |
| --- | --- | --- | --- | --- |
| JSLinux | 10.5 | 1.65 | 1.65 | 0.37 |
| JS Raytracer | 6.3 | 1.01 | 1.17 | 1.02 |
| Space Invaders | 25.8 | 1.03 | 1.22 | 0.25 |
| Mozilla.org | 22.3 | 1.00 | 1.09 | 0.23 |
| CodeMirror | 16.6 | 1.00 | 1.03 | 0.07 |
| Colorpicker | 15.3 | 1.00 | 1.07 | 0.13 |
| DuckDuckGo | 14.1 | 1.00 | 1.08 | 0.19 |

Values are reported geometric means of ten runs, except interactive executions were recorded once and replayed ten times. Local site copies and cleared network caches bound the workload. Disabled instrumentation is reported as 1.00 throughout. Faster seeking omits waits; it does not show faster underlying computation, and the ray tracer does not speed up. The under-1.1 interactive replay claim excludes the scripted game and other noninteractive cases. The conclusion's broad performance language must retain these nonzero overheads.

Logs occupy memory; recording length is memory-limited. The table distinguishes in-memory, uncompressed and compressed log sizes from site assets. The timeline's usability for long runs is an acknowledged limitation. Neither compact compressed files nor this small workload set establishes free history, complete I/O coverage or acceptable overhead for Nu.

## User-study reconstruction

The paper reports fourteen recruits, two used in pilots. Twelve main-study participants is the natural subtraction, **not a separately verified analytic denominator**: participant-level data and exact analysis counts were not located in the bounded artifact check. Half of the fourteen recruits were professionals and half researchers; do not automatically apply that split to the remaining sample. Prior jQuery/Glow experience was uncontrolled.

Each participant performed two tasks, one with standard Safari debugging and one with Timelapse additionally available. Task order and the task receiving Timelapse were randomized. Immediately before that task, participants received thirty minutes of training, had to demonstrate tool mastery and could consult the tutorial. Each task allowed 45 minutes. These training costs were outside timed task work; completion was demonstrated to the study authors, without reported independent blinded scoring.

Space Invaders contained 625 SLOC across six files, excluding libraries. Participants were to fix two defects: an API-property change introduced while preparing the study, which masked an existing double-event/bullet defect. Six progress milestones included reproduction, locating/fixing the API problem, reproducing/explaining the second defect and fixing it. Colorpicker contained about 500 lines excluding library/example code; participants were asked to **write a regression test**, rather than repair the RGB/HSV rounding defect. Its five milestones covered reproduction, explanation, test form, triggering input and verification. Percentage completion combines different milestones and cannot be equated with complete repair of all obligations.

Task time ran from initial reproduction to completion or the time cap. Video/audio coding identified reproduction attention through window focus, mouse position and interface modality. Figure 8 plots task seconds and milestone completion by task/condition using medians, quartiles and outliers. It supplies no participant-level denominator, confidence interval or exact statistical test. No exact test statistic, p-value or equivalence margin was found in the read paper. The published claim is **no statistically significant difference** in task time, success or reproduction-time fraction; this does not establish equal effectiveness or absence of a worthwhile effect.

Participants spent 8–25% of measured time reproducing behavior, typically 10–15%, with a reported median of 22 reproduction instances. The authors explicitly limit ecological validity: reproduction steps were supplied, many tasks were unfinished, and bug-reporting/triage/testing outside the task was excluded. Easier reproduction sometimes encouraged more reproduction. Thus a reduction in effort per replay need not reduce total time spent replaying or total maintenance time.

The qualitative distinction between successful and less successful developers is based on achieved progress. High performers integrated replay into systematic hypotheses; others were distracted or retained ad hoc tactics. This is an observed strategy account, not a randomized expertise intervention or a validated pre-treatment moderator. Figure 8 and this account qualify S51's abbreviated “no effect” summary.

## Bounded artifact and search checks

The paper links [burg/timelapse](https://github.com/burg/timelapse). At commit `b0a4c3d93ea84ff2cf0d5f0721fa68e65d12a032`, the recursive API tree returned 59,072 entries and was truncated. A separate root tree returned all 23 entries. The complete [README](https://github.com/burg/timelapse/blob/b0a4c3d93ea84ff2cf0d5f0721fa68e65d12a032/README.md), SHA-256 `b041db1884d8d2286f75ce0e00a05550a2105922da471cb3b30385355eb68c68`, documents a WebKit fork and Mac-only tested builds; the current wiki home lists developer/build notes. Neither inspected route supplied the promised study tables/materials. This is a retrieval gap, not proof the data never existed or an exhaustive source-code audit. No participant values were inferred from box-plot pixels.

Scite's incoming graph, capped at twenty, returned twenty edges/21 nodes and was truncated; it has no offset. All twenty returned citing identities were checked separately. The reformulated `"Timelapse" AND "debugging"` search requested twenty at offsets 0, 20, 40, 60 and 62, returning 20/20/20/2/0 records. There were 61 unique DOIs across 62 records despite a reported total of 66. Retain this service-count/overlap gap; an empty final response is not proof of complete citer coverage. Many results concerned biological time-lapse imaging and were excluded. Exact checks and primary author routes addressed consequential software leads.

Promote the directly relevant 2025 controlled study [How Omniscient Debuggers Impact Debugging Behavior](https://doi.org/10.1109/VL-HCC65237.2025.00016), with an accessible author preprint, for contemporary replay-tool benefit and behavior. Its abstract is not a completed methods reading. Vega's visual reactive-debugging study (`10.1111/cgf.12903`) remains conditional on visualization-specific comprehension claims; Pinpoint (`10.1109/VL/HCC53370.2022.9833105`) on block-based reuse; McFly, Tardis, WebRR and TimelyRep on replay implementation, browser-state fidelity or cost. Cross-device/cloud migration and tracing/undo studies are retained for their respective mechanism boundaries, not credited as Nu effectiveness evidence.

**Unique:** replay/navigation is established beyond FRP and game-engine purity. **Valuable:** the tasks motivate observable-state navigation, but this exploratory study supplies neither a general benefit nor an equivalence result. **Scientifically valid:** distinguish reproduction effort, total time, partial progress and full behavioral success; retain training, censoring, paired assignments, strategy differences and input/effect coverage. Nu-specific and coding-agent effects remain unmeasured. No experimental allocation is authorized.
