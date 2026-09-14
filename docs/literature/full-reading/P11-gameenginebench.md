# P11 - GameEngineBench

## Identity and coverage

Brian La, Sejoon Chang, Ben Kim, Junyoung Bae, Aamish Ahmad Beg, Sei Chang, Gonzalo Gonzalez-Pumariega and Kanav Goyal, *GameEngineBench: Evaluating Coding Agents on Real C++ Runtime Environments*, DOI `10.48550/arXiv.2607.03525`, v2, July 15, 2026. Main Codex AI reader consumed all 17 pages, references and appendices A-D. Rendered pp. 2-16 include all thirteen figures and both tables. Zotero `WRJ2UKZ3`; hashes in [assets](assets.json).

Historical v1 `A696WU9C` was compared through a normalized text diff and direct inspection of its changed pp. 1, 15-16, not counted as another full read. V2 adds Kanav Goyal, corrects Dartmouth's affiliation, replaces figure 9's 1-120 task-ID display with original benchmark order 1-110 and explicit counts, and revises figure 13's cost-frontier presentation. The [arXiv history](https://arxiv.org/abs/2607.03525) confirms both edition dates. Catalog v1 authors must not be silently attributed to v2.

## Workload and protocol

The authors select nine public Unreal Engine projects for diversity: HordeTemplateV2Native, ActionRoguelike, Bomber, TargetVector, GASShooter, EternalCrusadeResurrection, LASAA, PBMovementBench and NanoGSBench. The 110 tasks edit scoped native C++ files in existing projects; required assets remain part of the runtime but are not editable task outputs. Reference additions average 511 lines, median 362. This is a purposive engine-application/plugin task set, not random projects, engine-internal architecture replacement or a language comparison.

Each task has a buildable starting state with missing behavior, public behavioral requirements, explicit editable files, hidden tests and a reference solution. Authoring requires package/harness build, reference pass and starting-state failure on the intended behavior. A strong model then attempts the task; an LLM audits specification, tests, outputs, model edits and reference to guide task/test revision and revalidation. This is model-assisted calibration with selection consequences, not independent human certification (figure 1).

Each solver receives a fresh isolated copy of the starting project and one attempt, without retries or majority vote. Native CLI wrappers retain their standard tool behavior. Solver timeout is 3,600 seconds; compile and test timeouts 600 seconds each. The tests are injected only after solving and run through Unreal Play-in-Editor listen-server automation. Logs, workspace and judge output are intended to be retained. This design has no inherited candidate predecessor chain or cross-task conversational memory.

The primary pass@1 is the fraction **judged behaviorally correct by an LLM**, which may accept a solution despite failed tests. The judge sees the behavior specification, test source/outcomes, submitted edits and reference. Cross-family judging is supported when multiple families are available; that does not establish which family judged each run. Exact judge identities, calibration error, acceptance rule and disagreement resolution are not sufficiently reported. The paper itself calls for improved tests to reduce judge intervention (pp. 6, 9-10). It is incorrect to describe its headline as simply passing all executable tests.

Table 2 names Codex for GPT-5.5 (medium/high/xhigh), Claude Code for Fable 5/Opus 4.8/4.7/Sonnet 4.6, Antigravity for Gemini 3.1 Pro, Qwen Code for DeepSeek 4 Pro/Qwen 3.7 Plus, and Kimi Code for Kimi. Wrapper versions, hardware/OS and full prompt metadata are acknowledged release gaps (appendix D). Native wrapper and reasoning-effort differences are bundled with model identity.

## Results and unresolved reporting issues

Figures 4/9/11 report thirteen configurations, despite the abstract and prose saying twelve and table 2 omitting GLM 5.2. Solved counts are 61, 32, 26, 21, 20, 14, 11, 10, 9, 8, 4, 3 and 3 out of 110; these reproduce the rounded 55.5% to 2.7% rates. The union is 79/110 (71.82%), with 31 unsolved by all and none solved by all. This is one trial per task/configuration, without repeated-seed or repository-cluster uncertainty; observed complementarity does not by itself rule out stochastic contributions.

The examples concern meaningful runtime obligations: server authority, replication, local-controller UI, object initialization and teardown, pooled actor reuse, asynchronous generation and exactly-once readiness. They motivate observable task requirements. They do not establish that one architecture causes those failures. Task 19 is described as unsolved by all in §6.4/appendix A, but appendix C says Fable 5 alone solves it. Retain this conflict; do not use either story as a verified task-level result without raw records. Section 6.4 also lists serialization among unresolved areas although figure 8 shows 3/3 covered. V2's figure 9 caption still says nonpasses are red although its revised display uses a neutral fill.

Figures 6/12/13 explicitly use available wrapper-visible accounting. Fable 5's reported mean cost $17.2/task, GPT xhigh $9.9 and Gemini $3.3 do not establish a complete common accounting basis. Compile traces are missing for some wrappers; output-token means omit input/cache/auxiliary details. Avoid projecting these historical incomplete values as an ALF budget. Domain and overlapping requirement breakdowns have small, unequal samples; their cells are diagnostics, not independent trials.

## Artifact status and ALF implication

The paper-linked [Nitrode-Research/GameEngineBench](https://github.com/Nitrode-Research/GameEngineBench) returned HTTP 404 through both the GitHub API and browser retrieval on 2026-09-15. Thus no task manifests, runner, judge prompt, raw matrix or license could be inspected; appendix D's named scripts and directory structure are publication claims, not verified released artifacts. This access failure is a limit on exact reproduction, not evidence that the paper's data are invalid.

Use this paper to justify separating compile success from runtime behavior and to suggest lifecycle/authority obligations for a future bounded case. Keep engine-internal versus application scope explicit. It supplies neither an architecture treatment nor evidence that Nu/MMCC/ImSim represent paradigms. ALF should retain executable behavior and declared rubric evidence separately, audit semantic faults and alternate valid implementations before calibration, and never silently replace its frozen scoring rule with an LLM override. No new task construction or candidate execution follows from this reading.
