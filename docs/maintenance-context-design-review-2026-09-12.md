# Maintenance and context: design decision packet

**Date:** 2026-09-12 HKT

**Status:** assistant recommendation for construction review; not adopted or executable

**Inspected repository:** `663d4ac97e0870d5b44d5d0e0b2d1e3db7601f70`

## Decision in one place

Recommend studying **maintenance of supplied, idiomatic existing architectures
first**, with persistent candidate repositories and fresh conversations between
episodes. The question is whether F#/modern-C# implementations remain easier to
understand and evolve as interacting obligations accumulate under an explicit
information budget. This is not an initial architecture-generation contest.

The next proposed construction is **one paired, headless simulation workload and
eight dependent maintenance episodes**, model-free only, ending in a workload
and measurement review. It is a feasibility case, not evidence about large
projects or long-term maintenance in general. Do not start this construction
merely because the present document has been published or passed CI.

The material choice for the maintainer is whether to adopt this maintenance-first
construction, leaving architecture creation and a broader repository sample for
separate design decisions. Choosing creation-first would change the estimand,
support assumptions and workload; it is not an ordinary runner fix.

| Item | Current prepared H value and location | Proposed maintenance-first construction |
| --- | --- | --- |
| Scientific task | `008-summary-api`, one approved predecessor; [specification](../protocols/workstream-h1-h2/specification.json), `workload` | One existing system, then eight cumulative changes; no gold resets |
| Workload scale | Core/Expanded OrderFlow, one authored family | One headless simulation family, two independently idiomatic seeds; feasibility only |
| Source access | H1 all supplied; H2 map plus at most two reads, `controller` | Initially all eligible source/contracts/docs supplied; no retrieval or repair arm in this construction |
| Candidate interaction | H1 one submit; H2 reads then submit; zero repairs | One no-tools submission per episode; no compiler/test feedback |
| Cross-episode state | No eight-episode inherited maintenance chain | Retain candidate code/docs and requirement history; reset chat, not software |
| Context measurement | Authored UTF-8 input caps 18,432/35,840; not a verified provider limit, `budgets` | Audit complete envelopes and coverage offline first; new numeric cap **not selected** |
| Model/backend | `gpt-5.6-luna`, high effort, pinned native no-tools/local OAuth, `model` | No replacement model/backend proposed; any future use requires a new source-bound review |
| Sample | 32 slots/16 pairs; 28 feasible starts, `schedule` | One construction pair, **zero experimental trajectories allocated**; replication count not selected |
| Live authority | `execution_authorized=false`, `user_live_execution_approved=false`; `analysis.human_review_approved=false` | Unchanged: **no live authority** |
| Dispatch allocations | `approved_integration_dispatches=0`, `approved_pilot_dispatches=0` | **0 integration, 0 pilot**; eight episodes are not eight allocated calls |
| Review | Prepared [H human-review packet](workstream-h1-h2-human-review-2026-09-10.md) | This document is a design proposal; no human adoption recorded |

Current H's construction approval applies to its existing workload/controller,
not this replacement. Its original specification, evidence and interpretation
remain intact. Do not run H and relabel its summary-API results as longitudinal
architecture evidence. The earlier proposed five/64 H ceilings and unused E3a
balances grant no permission here.

## What the evidence changes

The [literature ledger](maintenance-literature-review-2026-09-12.md) records exact
queries, reading extent, revisions and exclusions. It is a targeted scoping
review, not a systematic search. The following are design implications, not
results of this repository's experiment:

- Persistent code with a fresh conversation is already an explicit [ChainSWE](https://arxiv.org/html/2607.02606v2#S4.SS3)
  condition; it must not be claimed as our invention. Release-sized evolution
  is also addressed by [SWE-EVO](https://arxiv.org/html/2512.18470v6#S3.SS2). Our proposed contribution is the matched
  F#/modern-C# maintenance, architectural-coherence and useful-context question,
  not the existence of longitudinal evaluation.
- [Cognitive Dimensions](https://www.cl.cam.ac.uk/users/afb21/publications/CT2001.pdf) offers a vocabulary for consistency, change resistance
  and hidden dependencies. It does not supply a validated LLM cognition score
  or prove that F# is superior. Measure consequences of decisions, not whether
  code looks functional.
- The [language-quality reanalysis](https://doi.org/10.1145/3340571) illustrates measurement and
  confounding risks. This comparison must identify the implementation,
  expertise, framework and model package actually tested, rather than claiming
  an intrinsic language effect.

The [pinned public Nu evidence](research-direction-2026-09-12.md#evidence-leads-and-limits)
motivates an explicit state model, transitions and effect boundaries, alongside
performance-sensitive mutable internals. It does **not** establish purity:
Nu's `World` is mutable and both Message and Command receive it. Do not copy
private sibling transcripts or assume architectural know-how comes free.

## What “consistent design” would mean operationally

The hypothesis is not “F# has records and C# does not.” Both implementations may
use their strongest supported idioms, including modern C# records, pattern
matching, functional composition and ordinary object-oriented boundaries.
Neither a class nor a mutable buffer is automatically an architectural defect.

The proposed mechanism is that a maintainable representation makes related
concepts behave predictably, puts invariants in identifiable places, and lets
changes compose without re-learning unrelated conventions. Consistency can
reduce required explanation, but an abstraction can also hide a dependency or
require considerable expertise. These are competing, task-dependent effects.

| Review question | Concrete evidence to record | Do not substitute |
| --- | --- | --- |
| Does an invariant have a clear owner? | Definition, validation boundary and all mutation/transition paths; a witnessed violation or preservation case | Count of unions, records, classes or mutable fields |
| Do state changes compose with effects? | Named ordering/cancellation obligations and observed cross-boundary behavior | Assuming a `World` parameter proves purity |
| Can a change stay behind its public boundary? | Necessary contract changes, consumers actually affected, documented exceptions and regressions | Fewest edited files or closest gold patch |
| Can the next maintainer find the relevant facts? | Submitted impact explanation with source/contract references; missing or incorrect dependencies | Eloquence, explanation length or inferred hidden reasoning |
| Does a convention survive later changes? | Same obligation checked over successive snapshots; contradictory representations or duplicated policy with behavioral consequences | A language-preference or “cleanliness” score |

These are proposed, separate diagnostic fields, not a weighted architecture
index. Accept alternative correct designs and justified changes to an earlier
boundary. Reference implementations establish feasibility and tests, not the
only permissible architecture. A short submitted impact explanation is an
observable artifact, not access to the model's internal reasoning.

Use independent qualified F# and C# review for idiomatic plausibility and domain
review for workload realism before freezing. Preserve reviewer identities/roles,
instructions, disagreements and source references. Code reveals the language;
claim only blinding to model identity, usage, behavioral scores and aggregate
language outcomes where actually achieved. Another AI session is not a human
expert sign-off. Until rubric reliability is assessed, architecture diagnostics
remain exploratory and cannot replace behavioral outcomes.

## Bound the first construction

The recommended example is a **headless stateful simulation kernel**, inspired
by Nu's architectural questions but not a port or reimplementation of Nu. It
needs interacting state, effects, persistence and an extension boundary, but no
graphics, networking service, new agent framework or new remote layer. Pin the
existing toolchain; any extra dependency or runtime change needs justification.

Write a language-neutral seed contract first. It should cover deterministic
ticks, entity lifetime, event ordering, observable effects and snapshot round
trips. Then construct two independently idiomatic implementations satisfying
the same externally observable contract. Do not translate F# mechanically into
C#, equalize source length, or improve one candidate's later architecture by
hand. Freeze seed source, documentation, review and all future task/test material
before candidate activity.

The following eight change themes bound authoring; they are **not yet executable
task contracts**. Model-free construction must resolve each into precise public
requirements, examples, invariant tests and a private evaluation packet:

1. Deferred commands with deterministic ordering across ticks.
2. Removal during a tick, including cleanup of references and queued effects.
3. A second entity behavior that interacts with existing lifecycle rules.
4. Snapshot-schema evolution with explicit old-format compatibility.
5. A new implementation behind an existing extension contract.
6. Asynchronous completion/cancellation represented by deterministic input
   events, including stale completions; no external service is necessary.
7. A batched hot path with the same observable semantics and an explicitly
   justified performance requirement; mutation is allowed in both languages.
8. Replay across the earlier features, exercising their combined obligations.

Include countervailing pressures: extension boundaries, mutable hot paths,
interoperability and abstraction costs, not only closed-state pattern matching.
Future tasks must not depend on matching a particular reference patch or exact
private file layout. Prior requirements remain binding unless a scheduled public
change explicitly supersedes them; version the obligation ledger accordingly.

Provide each language with reviewed domain/API guidance covering equivalent
obligations, not necessarily equal words or the same implementation recipe.
Include language-specific idiom guidance and framework prerequisites when
needed, record their authorship, and charge all supplied material to context.
Do not add tutoring after seeing one language struggle. This supported condition
does not measure unsupported architectural discovery or equalize latent model
familiarity with the two languages.

Authors necessarily know the future chain. Mitigate hindsight tailoring by
documenting that limitation, reviewing seeds against seed-only requirements,
and separating seed and change authors/reviewers where available. Do not call
this equivalent to decades of unanticipated production change.

One pair and eight episodes can check whether the mechanism is measurable. They
cannot estimate a population language effect, establish “large project” validity,
or justify a powered main study. A later sampling frame needs independent
project families/authoring blocks, actual interacting obligations and realistic
maintenance histories, selected before model outcomes. Episodes, seeds derived
from one family and repeated model draws are not independent repositories.
Do not choose the main sample by which language succeeds, or use padding/LOC
thresholds to manufacture scale. The main-study repository count and horizon
remain unset, not implicitly eight tasks forever.

## Clean episodes, inherited software

Proposed episode lifecycle:

```text
approved seed or previous candidate snapshot
  -> current requirement + past public obligations + eligible code/docs
  -> fresh no-tools conversation; one submission
  -> isolated evaluation, archived privately from the candidate
  -> next episode starts from the submitted safe repository state
```

The candidate may edit allowed code and durable documentation, including its
architecture notes. All of that text counts when supplied. Researcher-authored
summaries of earlier candidate decisions are not free memory. No future tasks,
gold, holdout results, private architecture rubric or research conclusions enter
the candidate workspace or prompt.

There are no shell calls, edit-tool retries, diagnostic self-repair conversations
or automatic model reissues in this primary proposal. A strict full-file-change
submission is applied atomically; unchanged files carry forward. Output limits
are separate from input limits and must accommodate legitimate multi-file work.
Candidate documentation and tests cannot replace protected evaluator machinery.

Recommend continuing the fixed chain after ordinary wrong or non-compiling
submissions, with no score feedback. Retain the faulty code so architectural
damage is not erased. A malformed or inapplicable submission is retained, records
an interface failure and makes no repository change; the next scheduled episode
is not a retry of that dispatch. Report such failures explicitly, including their
language distribution; absence of a repair loop does not prove the interface is
scientifically neutral. Never repair serialization by another model or manual
candidate editing.

Security violations terminate the affected chain; unknown usage, ambiguous
dispatch or apparatus faults pause under the existing hard gates. No continuation
decision may inspect private holdout scores. Evaluate every safely retained
snapshot out of band, including later ordinary failures. No automatic rollback,
gold replacement or dropping failed chains. This continuation policy differs
from older stop-on-failure paths and must be adopted explicitly before coding it.

Construction must test **downstream applicability after failure**, not just the
all-correct reference chain. Use representative safe no-op/malformed-output,
non-compiling, missing-prerequisite and wrong-behavior predecessors. Each task
must state its required cumulative external behavior even if an earlier feature
is absent; a later scheduled submission may also repair inherited defects within
its ordinary budget. It is not an extra repair dispatch. If a task presupposes a
private API/file layout or cannot be meaningfully evaluated from these states,
repair the task contract before freeze, not the live candidate afterward.

Predeclare separate diagnostic fields for submission disposition (unchanged
versus applied), prerequisite satisfaction, current-obligation correctness and
evaluation availability. An earlier missing prerequisite and a new defect are
not automatically the same failure class. Preserve both and mark attribution
unknown without a witness; never infer architectural decay merely from position
in the chain. A later correct state can recover cumulative correctness but does
not erase the prior failure or make the all-episode chain successful. None of
these private classifications controls continuation or reaches the candidate.

This is intentionally a no-feedback maintenance condition, not a claim about
fully tool-assisted developer productivity. Compiler assistance, test feedback
and repair efficiency would require a separate later condition, not pooled
results or a hidden fallback.

## Context and outcomes without inflated claims

For the first construction, audit **complete authored input**: instructions,
current request, cumulative public obligations, eligible source, documentation,
framework/API contracts and serialization overhead. Record input bytes, an
identified offline token proxy, actual provider usage when later available,
output allowance, and the framework knowledge assumed. Do not assume a library
name provides its contract for free. Human preparation/support effort is recorded
separately; a maintenance-only comparison is not a total creation/training-cost
comparison. No experimental “expertise score” is inferred from a model name.

A smaller representation is only useful if it retains the relevant semantics.
Audit which obligations a source/contract packet supports, then measure preserved
behavior and decision evidence. Dependency closure and text length alone cannot
prove a minimum sufficient context. Strong abstractions may make some source
unnecessary, and overly compressed source may obscure it.

Initially supply all eligible material or declare it infeasible; do not silently
truncate. Select any later common cap from a language-symmetric model-free rule,
publish the full fit table, and freeze before outcomes. Neither H's byte caps nor
the new audit establishes the provider's physical context window. If the exact
same prompt fits several offline labels, analyze coverage once: do not redispatch
it as several distinct context treatments. Demonstrating that additional context
*causes* better decisions requires a separately reviewed actual information
availability intervention; byte savings and outcome association alone do not.

Report at least these separate quantities; do not collapse them into one winner:

- Complete-obligation correctness at each episode, including prior invariants;
  first regression, recovered correctness and strict all-episode chain success.
  Missing evaluation is unknown, never silently false or successful.
- Context feasibility/coverage separately from correctness conditional on the
  common feasible set. One-language-only fit is a coverage result, not a wrong
  answer for the unqueried language. Candidate-grown overflow is retained as a
  policy outcome; later unexecuted episodes are identifiable, not discarded.
- Cumulative resource use with every dispatched attempt and failed chain,
  reported alongside completion/survival. A cheap early failure is not an
  efficiency win. OAuth subscription cost remains null.
- The source-bound architectural diagnostics above, including uncertainty and
  reviewer disagreement. These may suggest a mechanism but cannot establish
  causal mediation from this small construction.

Main-study analysis must use paired repository trajectories and account for
within-family dependence. Do not multiply the apparent sample by tests, episodes,
budget labels or snapshots. Freeze exclusions, continuation and primary outcomes
before any language results, not after selecting promising pilot behavior.

## Implementation feasibility and boundaries

The existing H path already avoids the E3a repair loop. Its mismatch is primarily
the summary task and lack of a longitudinal architectural workload, not an
undiscovered diagnostic feedback loop. See the [source-bound finding](research-direction-2026-09-12.md#read-only-h-finding).

Read-only inspection at the source above found that the general
[runner](../src/alf/runner.py) preserves a workspace and snapshots across tasks,
then stops at the first failed task. Its
[scripted agent](../src/alf/agents/scripted.py) copies cumulative gold for harness
checks; those copies are not inherited-candidate evidence. Crucially,
[evaluate_project](../src/alf/evaluator.py) calls
[run_process](../src/alf/process.py), which runs host subprocesses. Timeouts and
captured output are **not a sandbox**. Docker used for a command-agent transport
does not automatically protect that evaluator.

Reuse persistence ideas only, not that path for untrusted candidate execution.
Any later implementation must compose with the existing isolated
[H sandbox](../src/alf/h_sandbox.py)/[E3a sandbox](../src/alf/e3a_sandbox.py) boundary
after specific review; their mere existence proves no new runner is protected.
Do not add a second remote orchestration system, proxy or generic agent framework.
Runner corrections use ordinary Git revisions, not a new scientific version for
each apparatus bug. No code or safety boundary is changed by this proposal.

## Adoption and next handoff

**Decision record:** maintenance-first construction not yet approved; new workload
not constructed; rubric not validated; human expert review not completed; numeric
context cap/main-study sample unset; live approval false; integration/pilot
allocation zero. These are actual current states, not boxes pre-marked for review.

If the maintainer adopts this recommendation, the next bounded assignment is
model-free workload construction and contract/rubric validation for the one pair
and eight episodes above. Return with seed/task/test source identities, symmetric
context audit and proposed numeric settings, semantic fault checks, reviewer
findings, the exact safe runner adaptation needed, and a new self-contained
review packet. Do not stage OAuth, make a count/model request or execute an
experimental candidate as part of that assignment. Do not infer construction,
scientific freeze and live allocation from one another.

Traceability: the accompanying literature ledger and
[context record](research-direction-2026-09-12.md) explain how the recommendation
was reached; [PLAN.md](../PLAN.md) and [AGENTS.md](../AGENTS.md) point here. This
publication changes documentation only and preserves every frozen protocol,
source artifact and report. Review/validation below concerns this document, not
human scientific adoption or proof of provider behavior.

## Documentation review and validation

Another AI review identified that continuation after failed submissions needed
an explicit downstream-applicability audit. The revised lifecycle now requires
representative failed predecessors and separates prerequisite, submission,
current-obligation and evaluation-availability diagnostics without holdout-driven
continuation. That reviewer rechecked the change and reported no remaining
findings. This is AI methodological review, not human design approval.

The first independent documentation check found three trailing-space Markdown
hard breaks in the two new files; these were removed. The repeated check passed:
five files valid UTF-8, no tracked/untracked whitespace errors, 83 relative file
links with no missing targets, no changes to code/protocols/workloads/reports,
and unchanged false H approval flags with zero dispatch allocations. Fragment
semantics were not fully checked by that automated link pass. `uv.lock` remained
untracked and untouched; the inspected HEAD matched upstream. No model, OAuth,
candidate, full build or experimental test was run for this documentation change.
This additive record was self-checked after the independent pass. Publication CI
must be identified by the containing Git commit, never an earlier green run.
