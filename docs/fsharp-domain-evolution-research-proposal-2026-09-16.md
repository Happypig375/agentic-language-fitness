# Do exhaustive domain matches improve Codex maintenance of evolving F# state machines?

**Recommendation, 2026-09-16:** select this narrower question for human review; **defer experimental construction and live runs** until the feasibility requirements below are met and separately authorized. The literature supports investigating a consequential convention, not asserting its benefit or firstness. [PLAN](../PLAN.md) owns authority. The [candidate comparison](research-question-discovery-2026-09-16.md), [search and source ledger](literature/question-discovery-sources-2026-09-16.md) and [full-reading index](literature/full-reading/INDEX.md) expose the evidence and its limits.

## Introduction and practical problem

F# discriminated unions let a program name its domain states. Explicit matches over all current cases can make an added case produce an incomplete-match diagnostic. A wildcard can legitimately handle many cases, including newly added ones, without that diagnostic. Both are ordinary F# mechanisms: Microsoft's [FS0025 documentation](https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/compiler-messages/fs0025) describes both repairs. Neither establishes whether a later feature behaves correctly.

For a maintainer delegating changes to a coding agent, the consequential choice is whether to preserve explicit case handling at domain boundaries, accepting the associated editing and review work, or permit a shared fallback. A new gameplay state can require coordinated changes to movement, time, rendering, input and lifecycle. Some obligations occur in pattern matches; others occur in equality tests, guards or effects that remain type-correct. The useful answer is whether the convention improves complete behavior under ordinary source/tool access, at an acceptable cost, and which obligations it leaves unprotected.

Nu supplies a concrete F# motivation. Its pinned [coding standard](https://github.com/bryanedds/Nu/blob/064f7ae92a8506689cd91aff5e6804a375d6ef3d/Standard.md) favors domain types and exhaustiveness where appropriate. In the same revision's [Breakout MMCC gameplay](https://github.com/bryanedds/Nu/blob/064f7ae92a8506689cd91aff5e6804a375d6ef3d/Projects/Breakout%20Mmcc/Gameplay.fs), `GameplayState` is explicitly matched during updating, while content uses equality with `Playing` and time is advanced through a separate message. This source combination makes the question concrete; no new state was implemented and no agent failure was observed here. MMCC also performs sound effects during updating, so it must not be described as an entirely pure effect-free boundary.

The [Vsynchronicity essay](https://vsynchronicity.wordpress.com/2026/09/07/simplicity-aware-programming/) and the sibling `nu chat analysis` technical synthesis prompted attention to domain distinctions, state transitions and coordination over time. They are practitioner/derived hypothesis inputs, not controlled evidence of agent performance. Private transcripts are not study data or public exhibits. Public pinned Nu source is sufficient to inspect the motivation.

## Research gap and closest work

The broad claims are already occupied. Type feedback, typed context, functional-language repair, code-organization experiments and multi-file propagation have substantial prior work. The proposed residual contribution is **a controlled estimate of the behavioral and resource consequences of one existing source convention during later domain changes**, including cases where its additional diagnostics are unhelpful. A different language or model alone would not justify the study.

| Closest evidence | Purpose/mechanism/evaluation | Consequence for this proposal |
| --- | --- | --- |
| [P08, Type-Error Ablation](literature/full-reading/P08-type-error-ablation.md), arXiv 2606.01522v2 | Agent repair of selected single type faults in ten Shplait programs; diagnostic-detail interventions, dynamic test feedback and substantial conditional reversals | Do not claim first type-feedback benefit or universal improvement. New obligations and independently withheld final behavior are needed; its effect sizes do not calibrate this study |
| [S35, Typed Holes](literature/full-reading/S35-typed-holes.md), DOI 10.1145/3689728 | Types, relevant headers and error rounds for missing update functions in five MVU applications; behavioral tests, competitive exhaustive context and adverse header cases | MVU, sum types and behavior-tested type context already coexist. The comparison here concerns assigned source conventions during changes, with full source available to both arms |
| [P03, Code Cleanliness](literature/full-reading/P03-code-cleanliness.md), arXiv 2605.20049v1 | Behaviorally checked source transformations followed by coding-agent tasks; bundled organization changes, partial test scores, heterogeneous costs | Source-convention experiments are established. Isolate the declared contrast, retain regressions and adverse cases, and avoid resource-outlier or success filtering |
| [S34, FPEval](literature/full-reading/S34-functional-programming.md), arXiv 2601.02060v1 | Functional-language initial generation and repair; tests plus static style metrics; repair advice permits missing cases or a catch-all | First functional repair and lint-based maintainability claims are unavailable. Catch-alls are a possible valid repair, not a failure label |
| [S36, TRACE](literature/full-reading/S36-trace-subsequent-edits.md), DOI 10.1109/ASE63991.2025.00117 | Learned/LSP subsequent-edit propagation, reference-edit simulation, and a separate human study with task-dependent winners | Static location support does not settle semantic edits. Evaluate actual autonomous outcomes, retain failed patches, and do not insert reference edits into candidate runs |
| [S37, Haskell Refactoring](literature/full-reading/S37-haskell-refactoring.md), DOI 10.1007/978-3-032-12089-2_26 | Bundled agent refactoring already recommends exhaustive cases; before/after static/runtime metrics, with incomplete released verification provenance | The convention is prior advice. Its incremental value for later behavior remains a question; aggregate quality improvements are not a maintenance effect estimate |

All six papers are fully read at their recorded edition/coverage; this is not experimental reproduction. The discovery ledger also records abstract-only constrained-decoding and dependency-repair leads. Those different mechanisms prevent claiming first type-related semantic reliability; they are not established replications of the proposed contrast. Scite's useful functional-programming branch was paginated, and direct/citing methods were checked, but large noisy result sets and sparse citation graphs leave priority uncertain.

## Question, scope and useful implications

**For bounded domain-state changes in existing F# applications, does starting from explicit exhaustive matches, compared with an initially behaviorally equivalent catch-all convention, increase the probability that a fixed Codex coding-agent policy satisfies every new and retained behavioral obligation within the same resource allowance? Where do obligations outside those matches remain unsatisfied?**

The first target is a Nu-grounded feasibility case, not a comparison of Nu architectures or a language leaderboard. A contribution would be conditional practice guidance: when explicit case handling earns its maintenance cost, when a valid default suffices, and where independent behavioral verification remains necessary. A precise null or adverse result would also change that decision. It would not show that F# is intrinsically superior, that the model understands a state machine, or that compilation proves correctness.

The beneficiary is an F# maintainer setting a source/review convention for agent-assisted changes. Importance is supported by an existing public convention, concrete state-dependent responsibilities in Nu, and the closest studies' conditional outcomes. Frequency across industrial F# projects, willingness to pay the extra review cost, and the magnitude of any benefit are **not yet established**. Do not promise adoption or positive return on effort from this literature review.

## Proposed methodology

### Units, source contrast and tasks

Use two initial variants of the **same** pinned F# implementation. Preserve APIs, engine, dependencies, initial behavior, names, comments, helper organization and runtime facilities as far as the convention permits. In one variant, enumerate the existing domain cases at specified match sites; in the other, use a semantically appropriate fallback for the corresponding existing cases. Verify initial observational equivalence with common tests and source review. Record unavoidable token/branch differences. The primary estimand is the **total effect of that source convention**, including its information and diagnostic consequences; it does not isolate a pure compiler-information effect.

Do not use existing MMCC versus ImSim as these two arms. The fully inspected Breakout gameplay files differ in manual versus engine physics, lifecycle/API use and other implementation choices. Sharing F# and Nu does not control those differences.

Define change families from requirements before candidate outcomes. Include added domain cases requiring distinct behavior, cases for which an existing default remains correct, and matched changes that do not alter the union. Include coordinated temporal/lifecycle obligations beyond compiler-visible matches. Do not select final tasks because a preliminary model run showed an advantage. Separate development examples from evaluation families; cosmetic variations of one task are not independent evidence. If only one application/family is feasible, label the result a local case, not a general convention recommendation.

### Candidate policy and information

Pin the Codex CLI, returned model identity, settings, source snapshot, .NET/F# toolchain, dependencies and environment. Give each run a fresh isolated workspace/context, the same behavioral request, available current source, documentation and existing public tests. Allow the same ordinary source navigation, build/test feedback and bounded repair opportunities in both arms. Freeze compiler flags, including warning severity; do not turn warnings into errors after seeing results. An agent may use another correct organization or a catch-all. Preserve the assigned arm in analysis and record resulting changes descriptively.

Agents must not see the alternate arm, research predictions, reference patches, hidden evaluation cases or comparative outcomes. Within-run public test feedback is allowed by the proposed policy; held-out final scores never feed repair, stopping or sample extension. This proposed tool/repair policy differs from some historical ALF no-tools/no-repair packets and therefore needs its own approval. It is not retroactively applied to old data.

### Reference standard and outcomes

Before model evaluation, establish a common behavioral contract and an independent final oracle. Cover initial regressions, new behavior, relevant event ordering, repeated transitions and forbidden side effects where the requirement demands them. Validate the oracle against reviewed reference implementations, plausible faults and at least one alternative correct implementation. Count no extra credit for matching a reference patch. Faults must test obligations, not enforce source style. Keep test-author access and development/evaluation boundaries explicit.

The primary outcome is **all-obligation success for the assigned change within budget**, requiring the applicable old and new checks. Report partial obligation coverage separately. Also report compilation/diagnostic status, new failures versus retained failures, elapsed time, every attempted token debit and review-relevant patch size. A correct fallback is a success; clearing a warning is not automatically one. Infrastructure-blocked observations, time-budget exhaustion and unrun slots are distinct, under rules frozen before evaluation. Do not exclude slow or noncompiling candidates after assignment.

Classify obligations as compiler-visible or compiler-silent from the predeclared requirement/reference analysis, before model results. Their coverage is explanatory evidence; do not condition the primary effect on successful compilation or adjust it for post-assignment diagnostics, edits or repair counts. Those may be mechanisms through which the source convention acts.

### Uncertainty, cost and interpretation

Run both source conditions on each evaluation task, with randomized/interleaved dispatch order and independently fresh agent runs. Task-family/application clustering, not the number of API calls or test assertions, determines generalization. Prespecify the paired task-level success difference, task/family weighting, interval procedure, handling of missing observations and limited secondary comparisons. Repetitions estimate executor variability; they do not create new change families. Do not use unpaired participant tests from TRACE or prior studies' selected effect sizes as a power calculation.

Choose a smallest worthwhile improvement and acceptable cost with the intended maintainer before allocating runs. Model-free precision/sensitivity calculations should then determine how many independent families and repeats the intended claim needs. If feasible family counts cannot support useful uncertainty bounds, reduce the claim to descriptive feasibility or defer it. There is no sample allocation in this proposal, and the historical 192+5 cannot supply one.

Measure one-time source preparation/review separately from per-change execution cost. A fixed agent-budget comparison estimates quality under that budget; it does not establish overall budget superiority. Any claim that saved review effort is better spent on additional tests would require an explicitly designed comparison, not an assumed benefit.

## Feasibility, validation requirements and stopping decision

Existing local Codex integration supplies an authorized path to isolated noninteractive runs and event/usage records; static inspection of `src/alf/agents/codex.py` and [official noninteractive documentation](https://learn.chatgpt.com/docs/non-interactive-mode) supports apparatus plausibility. No live call established compatibility here. In particular, the local usage parser's required fields must be reconciled with the pinned CLI's actual event schema using approved model-free fixtures before claiming complete accounting. Do not change OAuth/backend choices or quietly launch a diagnostic call.

The next review must decide whether this question merits a **separately scoped, model-free feasibility packet**. It would need to establish: a legitimate convention contrast in public F# source; initial equivalence; enough meaningful independent changes; deterministic observation of temporal behavior through existing facilities; sensitive independent tests; and credible effort/precision requirements. No reference changes, new adapters or tests were constructed in this literature assignment. If Nu cannot satisfy those conditions without a substitute engine or a task-solving observation seam, defer the Nu case and return for a decision.

Abandon or substantially revise the question if:

1. Closer work already estimates this same convention contrast under comparable autonomous change/behavior conditions, leaving only a language/model substitution.
2. Source equivalence requires changing APIs, effects or architecture so extensively that the proposed convention cannot be distinguished from a package comparison.
3. Realistic changes rarely expose the distinction, both arms are at floor/ceiling, or only author-selected favorable changes produce an effect.
4. Explicit matches chiefly add diagnostic/editing work without useful behavioral improvement, or a precise effect is smaller than the predeclared worthwhile threshold. An imprecise null calls for a narrower conclusion, not an invented equivalence result.
5. Independent temporal tests, alternative-correct witnesses, usable accounting or sufficient task diversity cannot be established within a justified resource envelope.

## Three-criterion judgement

| Criterion | Answer at this handoff | Condition still required |
| --- | --- | --- |
| **Unique — Scite** | **Unconfirmed.** No exact duplicate was identified in the recorded screen; closest full methods leave a narrower empirical contrast. Exhaustiveness, type feedback and source-organization evaluation are established | Bound priority to this search. Follow any newly consequential duplicate; do not interpret unexamined records or low graph coverage as absence |
| **Valuable** | **Plausible, concretely motivated.** The result could change an F# maintainer's convention and verification effort, including a useful negative answer | Validate task prevalence, worthwhile effect and effort with the actual use case; no benefit or return is yet measured |
| **Scientifically valid** | **Credible proposed design, not a validated study.** Common behavior, controlled assignment, independent scoring, intention-to-treat and clustered uncertainty address the principal rivals | Case equivalence, test sensitivity, apparatus/accounting, task diversity and allocation remain unvalidated |

**Disposition: recommend D1 narrowed by Nu's temporal-obligation perspective; defer experimental start.** This is a completed research-discovery recommendation for human review, not human approval or an empirical proof. All existing construction, candidate, worker and H holds remain; new allocation is zero.
