# S125 — GameLogicBench: runtime observations, judge validation and release boundaries

**Complete publication reading, 2026-09-30; bounded passive artifact inspection, no reproduction.** Xinyu Che et al., *GameLogicBench: Evaluating Coding Agents on Runtime Game Logic with Tick-Level State Assertions*, [arXiv record](https://arxiv.org/abs/2609.21562), DOI `10.48550/arXiv.2609.21562`. Read **v2**, revised 21 September 2026; v1 was submitted 18 September. The PDF's header says 22 September while its revision sidebar says 21 September. No peer-review status or equivalence to v1 is assumed. Scite's January date is not adopted.

## Identity, coverage and live question

Zotero parent `XMYGZCHB`, PDF `TLB4XKHR`, note `Q7G3A92G`. The record existed before intentional PDF reading. The [versioned PDF](https://arxiv.org/pdf/2609.21562v2) is **36 pages, 4,672,029 bytes**, SHA-256 `51672aa64d2822ddfa674b880851df713b93829175d627a939d73971ec07879d`; native upload and stored bytes were checked. All 36 pages, nine figures, twelve tables, three example briefs, all construction/review standards and 33 references were read. Visual inspection covered pages 1/2/4–9/13–17/20/21/27/28/30/32/36. Figure 9's dense 72-by-20 grid was inspected for its structure, legend and patterns; its 1,440 cells were not individually transcribed. Truncated text outputs were reread before coverage credit. Author prompts are evidence about their procedure, not instructions to this project.

This reading changes B07/B09/B12: what does a temporal game evaluator observe, how are valid and faulty implementations distinguished, and which denominators and information boundaries support the reported benefit? It supplies a close agent-evaluation method beyond S123's trace language and S124's human contract case. It does not answer D1's future-case source-convention comparison.

## What is assigned, observed and selected

The benchmark contains **72 tasks: 21 Atom, 28 Combo, 23 Repo**, with **403 scenarios and 1,451 scenario/seed cases**. A task has 2–12 scenarios and 10–38 cases. Atom isolates a mechanic, Combo couples mechanics in a purpose-built game, and Repo adds project integration. Multiple tasks reuse upstream projects; tasks and seeds are not independent games. The author describes twenty Repo tasks derived from public projects, not twenty-three independent public codebases.

An agent receives a Godot project, a brief, a stub and one public preview. It may edit/debug local files, but the integration target and delivered paths are fixed. After solving, the frozen judge is overlaid into a separate network-disabled container. The main solve runs also block egress except the model API. Rule families must be disclosed or discoverable; hidden scenarios vary legal calls, structure and parameters. A hidden new requirement is a construction defect under the authors' own standard. Correct implementations need not reproduce the reference's internal structure or tie-breaking.

Scenarios are hand-designed; seeds vary bounded parameters. Admission is selective: roughly 200 ideas, 122 constructed/calibrated/reviewed candidates, and 72 admitted tasks. Three human annotators bracket four construction-agent roles. Stable reference/naive separation, determinism and sufficient difficulty are admission conditions. This is a curated challenge set, not a sample of ordinary game-maintenance episodes. The fixed tasks complete or extend a mechanism; they do not follow successive requirement changes through a maintenance trajectory.

Each scored case runs a fixed-step game and observes state/events. Success requires every case of a task to pass. Temporal windows, conservation, ordering and external consumers' observations can expose faults that a terminal state misses. The guarantee remains relative to the implemented predicates, observation projection and finite scenarios. It does not cover every possible play sequence, unobserved side effect or arbitrary concurrent environment. The paper explicitly excludes network synchronization and limits itself to Godot/GDScript.

## Construction and oracle independence

Appendix G requires four calibration forms: a correct reference, a plausible classic-bug implementation, mutants removing one capability, and a behavior-preserving refactoring or second legal implementation. It requires individual dispositions for surviving mutants and measured margins. A random stub checks whether the candidate actually owns the mechanism or merely selects actions in an already implemented game.

The review agent receives a separate acceptance standard and is instructed to rerun calibration through the regular container path. Human reviewers decide admission and scope but do **not** rerun calibration themselves. These are distinct author-reported roles. They are not independent human execution, an independent research replication, or proof of a separately derived semantic oracle. The specification-ambiguity review explicitly imposes no independent-implementation gate; facts may deliberately require reading the project. A passing rewrite is useful evidence against one over-specific assertion pattern, not exhaustive acceptance of all valid implementations.

The standards distinguish new-mechanism obligations from retained upstream invariants. The latter are mandatory for extensions, usual for partial completions and optional for carve-outs. Construction may compare against upstream traces to choose invariant quantities; exact differential output is not supposed to become a general scoring requirement when legal implementations can differ. This is a concrete predecessor for separating retained and new behavior, with a different assignment from D1.

Determinism is established locally by three identical reruns and agreement with the container. Navigation map updates and avoidance threads are pinned where necessary; uncontrolled mechanics are discarded. This is a condition imposed on the selected workload, not evidence that general asynchronous games are deterministic. Scenario names enter random-stream derivation, so renaming one invalidates old calibration. Judge resource limits are part of the frozen case contract.

Candidate and judge execute in the same game process. The appendix proposes runtime-node/channel checks, conservation and retained-reference checks, but explicitly excludes modification of judge internals through reflection. Frozen file overlay alone is not a proof that untrusted code cannot inspect or influence an in-process oracle. No security experiment was performed here, and this design does not replace ISE's existing sandbox and information boundaries.

## Measured positive results and their units

The main evaluation has **twenty model/scaffold configurations**, not twenty independent models: twelve Claude Code, four Codex and four OpenCode configurations, with thirteen distinct model identifiers. The stated scaffold versions are 2.1.177, 0.144.1 and 1.17.18 respectively; Godot is 4.4, effort is high and the solve limit is one hour. The main table has one attempt per configuration/task. The best configuration, Claude Opus 5 with Claude Code, solves **38/72 = 52.78%**. Qwen solves 32/72; GPT-5.6-Sol and DeepSeek-V4-Pro-0813 each solve 30/72 in that scaffold. These are dated author results, not current model recommendations.

Table 3 records inference cost across all 72 tasks, including $443.16 for the best configuration, $83.97 for GPT-5.6-Sol/Claude Code and $19.68 for DeepSeek-V4-Pro-0813/Claude Code. Appendix token/cache/rate tables support the accounting; rounding explains approximately one-cent reconstruction differences. They do not include human task construction, judge computation or a net maintenance benefit. Total token traffic, newly charged input, cache use and peak context are different quantities. Figure 1's displayed cost ordering is descriptive; an equal-score, higher-cost point is not strict Pareto improvement.

Nearly all configurations decline from Atom to Combo to Repo. Those selected tiers differ in mechanisms, project context and difficulty; this is not a randomized isolated effect of codebase size. Qwen's score varies from 26.39% to 44.44% across scaffolds. Model/scaffold interaction is consequential, but equal wall time and effort labels do not equate tool affordances, token use or effective opportunity. The comparisons do not isolate a single interface mechanism.

Three configurations have three repeated attempts (Table 4). Qwen's mean pass@1 is 45.37%, any-of-three 62.50%, and all-three 27.78%; GLM's are 34.72%, 48.61%, 22.22%; Kimi's are 34.72%, 51.39%, 15.28%. Single-attempt standard deviations are 3.67–4.24 percentage points. These expose changing solved-task sets. They are not independent task-family replications or a general reliability guarantee. The release's leaderboard requires all three attempts to close before its three-attempt denominator is formed.

The authors report engine invocation in about 99% of sessions and self-authored Godot test scripts in 39.2%. Tool-count analysis classifies compound calls by a primary-operation priority, while facets can overlap. A call is not a primitive edit or a common amount of work across scaffolds. Execution frequency alone does not establish testing effectiveness.

## Judge ablations: positive evidence with conditional denominators

Section 4.6 rescored fixed submissions on a **36-task audit subset**. Holding tasks/solutions fixed is a useful direct comparison of the information retained by the judge.

| Quantity | Terminal assertions only, all scenarios/seeds | Full temporal criterion, public preview only |
| --- | --- | --- |
| Deliberate mutants escaping | 236/666 (35.4%) | 508/666 (76.3%) |
| Tasks with at least one escape | 34/36 | 36/36 |
| Previously failing agent solutions becoming passes | 64/488 (13.1%) | 418/488 (85.7%) |
| Mean task-solve-rate increase across twenty configurations | 8.9 percentage points | 58.1 percentage points |

The last row uses 20 × 36 = 720 possible configuration/task submissions: 64/720 and 418/720 reproduce the displayed increments. **488 is the subset failing the full evaluator**, not all submissions or all 72 tasks. These results favor both intermediate observations and varied scenarios for these faults/cases; they do not measure a population false-pass rate or universally rank oracle designs.

The separate criterion-development comparison begins with **127/666 mutants escaping**, exposing 24 missing checks on 19/36 tasks. After repairs, three agent task outcomes change from pass to fail, affecting two tasks and three models, while proper solutions and behavior-preserving controls still pass. This is constructive evidence that passing known-correct programs is insufficient to validate a judge. The fault set helped develop the criterion; it is not an independent held-out sample of future faults. The paper says nine models under two scaffolds for this rejudging, without a complete configuration/cell roster. Do not silently turn that into eighteen complete configurations or reuse the twenty-configuration denominator.

Section 4.5 reports failed scenarios as 74.3% runnable mechanism failures, 17.2% without judgeable solutions and 8.5% nonviable computations. Capability groups overlap and use strict all-seed scenario passes. Their denominators require more than the labels printed in Figure 8: for example, the Qwen/Claude Code baseline percentage 98.59 is consistent with 70/71 rather than an integer out of 72. The public scoring code excludes designated unusable infrastructure/configuration outcomes, but the released data do not establish the exact paper-level capability/failure aggregation. Preserve the percentages as author reports; do not invent missing cells or infer intrinsic capability difficulty from them.

The open-network audit covers five configurations on 23 Repo tasks each. Four retrieve upstream source, with direct reuse found in reviewed traces. Their sealed-to-open solved counts are Kimi 3→12, GPT-5.6-Sol/Codex 6→11, GLM 7→11 and Opus 10→11; DeepSeek-V4-Pro stays 3→3 without retrieval. Successful/attempted retrieval sessions are 9/10, 9/9, 9/9, 5/7 and 0/0 respectively. This supports exposure as a material benchmark condition. Network access changes a bundle of opportunities, and the sealed-only prompt note also differs. The score changes do not isolate copying's causal effect or remove prior training exposure.

## What the public artifacts independently establish

Passive GitHub inspection pinned [harness `d9854d616e4f7beaa6c4321b7c8452c6509e41c2`](https://github.com/NJU-LINK/GameLogicBench/tree/d9854d616e4f7beaa6c4321b7c8452c6509e41c2) and [task library `18c54e69cf962fd402e245811d4925d129f4b33c`](https://github.com/NJU-LINK/GameLogicBench-Tasks/tree/18c54e69cf962fd402e245811d4925d129f4b33c), both dated **25 August 2026**. Recursive trees were untruncated: 41 and 37,333 files. These precede both paper deposits; the paper does not bind its results to these hashes. No author code, installer, container, model or test was run.

**106 selected files, 430,342 bytes** were acquired with Git-blob verification and local SHA-256 manifests. Acquisition is not whole-source reading. A strict data-only parser examined all 72 task definitions' name, tier, scenario and seed fields and reproduced **21/28/23, 403, 1,451 and the stated ranges**. It required exactly one public baseline per task. Source-family locator passages in nineteen upstream notes identify repeated OpenRPG, Open RTS, Slay the Robot, WorldWarII and YouTD2 families. The dothop task definition separately identifies its upstream. Three other Repo entries describe composed damage-control, watch-rotation and tower-defense allocation systems; they explain the twenty-derived-versus-twenty-three-Repo distinction but leave the uniform real-repository tier interpretation in need of qualification.

The [release commit](https://github.com/NJU-LINK/GameLogicBench-Tasks/commit/18c54e69cf962fd402e245811d4925d129f4b33c) expressly excludes construction-only mutants, behavior-preserving controls, diagnostic variants, calibration records and authoring scripts. Tree inspection found no benchmark result/ablation archive. Thus the strongest reported ablations cannot be independently recomputed from the inspected release. Repository availability does not close that gap. The commit's description of 36 tasks using the `press` mapping also does not match the **31 enabled by the released schema/metadata** (28 Combo plus three explicit Repo overrides); this is not assumed to identify the paper's separate 36-task audit subset.

Bounded reading covered `scripts/score.py` lines 25–110/160–279, `scripts/leaderboard.py` 1–110, `geb/pipeline/judge.py` 205–285, `geb/schema.py` 62–119, `docs/status-fields.md` 127–163 and `docs/structure.md` 87–113. The scorer distinguishes usable failures from infrastructure/configuration exclusions. A task cannot be solved while an excluded cell awaits rejudging. The live leaderboard further excludes not-yet-closed attempts. These are useful state distinctions, but neither source alone recovers the publication's denominators or validates an ISE missingness policy. Overlay descriptions preserve declared deliverables through a final authoritative copy; low-level copy/security behavior was not audited.

Two task examples sharpen observation boundaries:

- **Navigation:** all of `assertions.gd` and `judge.gd` lines 105–173 were inspected. The loop fails for excessive collision penetration or timeout and passes on reaching a goal radius. The implementation observes intermediate positions, but arrival within a budget remains an outcome bound. This concrete release/example does not cleanly implement the appendix's universal prohibition on threshold/outcome-only hard gates. It is a release/standard correspondence issue, not a reproduced incorrect verdict.
- **AMSG movement:** `judge_core.gd` lines 1–90 and the inspected assertion ranges 229–385 observe position/velocity, capsule height, animation consumption and geometry-derived support loss. Checks include plateau averages, stopping, gravity-onset windows and selected per-tick constraints. **Sampling every tick does not imply every obligation is asserted at every tick.** The full upstream-provenance note was read; it records a hollowed component, compatibility adjustments and intentional preservation of some upstream behavior. Other judge routines, source equivalence and all valid alternative movements remain unverified.

Selected artifact hashes make those checks recoverable without committing source dumps:

| File in the pinned repository | SHA-256 |
| --- | --- |
| Harness `scripts/score.py` | `173567753cadcd3a75ea7e6cfd0de1811a78854fb01aab99bdc508f212373312` |
| Harness `scripts/leaderboard.py` | `50161a3b425d75cfebaff931d64b77a9d6c703bc1d1b0fc9596348651e11bd67` |
| Harness `geb/pipeline/judge.py` | `a0f7289240b0b821b32125597a6cd53d2850919b8f95ac4617526dcc0087834b` |
| Harness `geb/schema.py` | `ab7e9aa1d6c7e356f66b07aa96c9487bef63611f20f74948976f638769edd442` |
| Tasks `atom_move_navigation/judge/assertions.gd` | `33a5156936b54772a29358264b1e6a285d1b54a216273061096e02cff0a0ce9a` |
| Tasks `atom_move_navigation/judge/judge.gd` | `d80493997e85d49c1340c8ffc2cd4ceb71e6799073f10665a126d5d2b27b47f1` |
| Tasks `repo_amsg_movement_engine/judge/judge_core.gd` | `eee13cf3b0c2faeaec353a349d84f3ef966671bdce077e659bc483f0f9181300` |

The other acquired task briefs, helper routines, upstream text beyond the stated passages and most of the 37,333-file tree remain unread. Proper/naive execution, raw solver traces, model calls, ablations, all candidate programs and v1/v2 comparison were not reproduced or silently completed.

## Consequences, contrary evidence and next sources

**Unique:** deterministic temporal game assertions, hidden legal scenarios, oracle mutation checks and retained obligations are existing methods. S125 is a direct contemporary agent benchmark predecessor; it does not test the assigned explicit-enumeration/fallback source convention. D1 priority remains unconfirmed, and the broad Nu survey remains open.

**Valuable:** fixed-submission ablations provide positive, bounded evidence for richer temporal/scenario observation and fault-sensitive criterion validation. Measured agent difficulty and tool/cost variation justify taking implementation and evaluation burdens seriously. They do not establish a net benefit of Nu, functional representation or D1, and missing artifacts do not erase the positive author-reported results.

**Scientifically valid:** connect each obligation to a disclosed rule, independent observation, finite ending and fault/validity check. Preserve valid alternatives, failure versus missing evidence, shared task families, trigger coverage and source/version binding. Mutation-guided criterion development must be separate from later independent validation. The public release illustrates these controls and unresolved correspondence problems; it does not certify the ISE oracle or authorize constructing one.

G04 found zero Scite edges and flagged low coverage, so the actual bibliography and primary records were used. SC45 (`limit:20`, offset0) returned three records for four exact titles: **GameDevBench** `10.48550/arXiv.2602.11103` (v2, 30 June), **GameCraft-Bench** `10.48550/arXiv.2606.17861` (v1, 16 June), and **GUI Agents for Continual Game Generation** `10.48550/arXiv.2605.28258` (v1, 27 May). Their primary abstracts were inspected; their effects are not yet accepted full-method evidence. GameDevBench's visual-feedback comparison and the continual playtesting loop can challenge narrow feedback/evolution claims. GameCraft's complete-game/rubric route remains a conditional comparator. [Roblox's OpenGameEval introduction](https://about.roblox.com/newsroom/2025/12/opengameeval-benchmark-agentic-ai-assistants-roblox-studio), 17 December 2025, was located and screened through its dataset description, not fully reconstructed; it is a consequential industry/temporal-test route outside this empty graph. Existing P11/A03 readings are reused rather than counted anew.

Next continue the C02 coverage/extensibility and positive maintenance methods while retaining these concrete B07/B09 leads, the Hughes temporal-relation method, and the missing S125 calibration/result/source-version packet. No theme is closed by this paper, and every experimental hold remains.
