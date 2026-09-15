# Selection evidence closure: uniqueness, value and validity

**Date:** 2026-09-15. **Reviewed head:** `f1bea15451d14b1027c356e0b2830acd85a86aa6`.

This is the requested continued evidence/methods review. It does not certify new complete-paper readings, human independence, runtime equivalence or experiment allocation. [PLAN](../PLAN.md) and the [proposal](architecture-maintenance-research-proposal-2026-09-15.md) contain the live corrections. The [source audit](selection-evidence-closure-sources-2026-09-15.md) records access, pagination and actual reading; the [DOI queue](literature/selection-priority-reading-2026-09-15.md) assigns worthwhile full reads. Earlier full-reading notes and experiments are unchanged.

## Verdict by the three criteria

| Criterion | Progress in this pass | Limit and disposition |
| --- | --- | --- |
| **Unique** | MicroRec's official description and the pattern paper's linked artifact now identify retrieval/ranking and pattern-suggestion targets, distinct from the proposed maintenance endpoint. Algorithm-selection methods, however, already supply the general choice-value framework. | A defensible difference from the inspected targets is clearer; global priority remains unproved. Position the contribution as empirical architectural-information value and boundary conditions, not a new recommender/evaluation formula. |
| **Valuable** | The plan now distinguishes improvement that the actual decision information permits from hindsight that sees the future or a lucky run. It also separates advice costs and alternative uses of those resources. | No usable headroom, useful gain, amortization or beneficiary uptake is established. A0 can test a credible decision opportunity, not measure a model effect. |
| **Scientifically valid** | The analysis distinguishes expected response from realized maxima, predictor variability from executor variability, and prospective covariates from post-assignment pathways. | Actual profiles, tests, policies, sample and uncertainty remain unfrozen. Useful theoretical distinctions are not implementation or validation evidence. |

Keep the question, adapt known methods and avoid a new broad pivot. The strongest contribution would explain when source-grounded organization information helps a maintainer choose and when a simpler default is enough. It need not claim a new algorithm or prove an F# advantage.

## 1. What the direct recommendation predecessors actually target

### MicroRec: recommendation is not necessarily architectural choice

The official MSR abstract describes natural-language microservice discovery using registry information and ranking metrics (MRR, MAP and precision@k). This resolves the earlier title ambiguity. It is relevant recommendation prior art, but the inspected description is not an experiment observing an adopted package through future code maintenance. The ACM body was unavailable, so the statement is limited to the reported target; no claim about every uninspected analysis is made.

Its reported large improvement concerns its own relevance task. It must not be copied as a maintenance-benefit effect or used to calibrate an ALF sample. The full paper remains useful to reconstruct candidate sets, relevance judgments, baselines, splits and whether any additional downstream evidence exists.

### Architecture-pattern suggestions: inspect outputs, not just a headline

The publisher abstract reports named-pattern prediction. Its linked author `Results.md` contains ten expected/actual pattern-and-explanation examples. In the inspected artifact, Test 2 has multiple returned labels, and Test 3's input already contains a pattern/explanation different from the separately listed expectation. These facts warrant checking input generation and adjudication; they do not establish what the unpublished details or full paper say, nor justify calling the study invalid.

The key distinction is that agreement with a selected label does not establish which of several valid implementations will survive later changes. ALF should retain executable obligations and accept valid alternatives, not build its own single-label architectural ground truth. The artifact is evidence about those examples, not a substitute for the paper or a reproduced 70% calculation.

### Another advisory framework already derives rules from coding outcomes

The newly screened Failure-Aware Enhancements paper constructs a failure-type-to-enhancement decision table. Its selected v1 methods use six selected incomplete projects, different model/information pipelines, and manual code inspection without execution testing. The advice is derived from those observations; that design is not a prospective evaluation of a frozen package selector on new profiles.

This is relevant overlap, not a duplicate or a refutation. It makes 'conditional guidance for LLM development' an inadequate novelty claim. It also reinforces the need to keep outcome definition, selection history and policy bundles explicit. Its numeric claims are not imported into ALF; complete reading and artifact reconstruction remain pending.

## 2. A missing foundational comparison: algorithm selection

ASlib and later algorithm-selection work already frame per-instance choices using observed performance, compare them with fixed and oracle choices, and account for information/feature costs. Selected ASlib sections also distinguish tuning/evaluation and acknowledge that many collected scenarios already favored selection. These are methodological predecessors, not new ALF contributions.

The next full methods reading should extract what transfers and what does not. In particular, code-maintenance trajectories contain stochastic generation, partially specified future requirements and inherited state. Do not mechanically import a timeout penalty, impute all missing performance as failure, exclude unsolved cases, or treat one realized run as the package's expected performance. The proposed state of the application is not a SAT instance, but its adoption decision can reuse established selection logic.

The useful novelty candidate is now bounded: **do specific architectural facts supply information that predicts differences in later executable maintenance, with demonstrable value beyond credible simpler advice?** A selector-value equation or a new testbed name cannot carry that contribution alone. Independent-profile evaluation is necessary for a procedural-transfer claim, and independent package families for architectural portability.

## 3. Usable choice opportunity is not a lucky-run oracle

This is a new correction beyond the preceding always-A/B baseline fix. Define the comparison at what the maintainer actually knows.

Let X be permitted decision information, Z unknown future details and omega executor randomness. With fixed harness H:

```text
p_a(x) = E[Y(a,H,Z,omega) | X=x]
V*_X = E_X[max_a p_a(X)]
V_const = max_a E_X[p_a(X)]
H_X = V*_X - V_const
```

This is gross selection opportunity for the stated bounded utility and information, not a newly discovered result or an ALF estimate. If one package is conditionally best for all permitted X, a profile selector has no gross advantage over that best constant. A procedure may still cheaply discover the default, but that is not profile-sensitive value.

**Algebra-only example 1:** two packages each independently succeed with probability 0.5. A legitimate fixed choice succeeds with probability 0.5. Selecting whichever succeeded after seeing both results succeeds with probability 0.75. The apparent 0.25 gain is hindsight exploiting random outcomes, not available advice. This independence assumption is solely for the example, not imposed on observed model runs.

**Algebra-only example 2:** two equally likely hidden task subtypes have success pairs (0.9,0.4) and (0.4,0.9). With identical visible X, both packages have expected success 0.65. An oracle told the subtype obtains 0.9. A selector without it cannot claim that 0.25 opportunity. Extra source/profile information might help, but would be a declared information intervention with its own cost.

Both examples were checked locally by elementary enumeration/arithmetic. No candidate call or empirical reproduction occurred.

A maximum of estimated per-profile means is also optimistic under noise. Headroom analysis needs its own uncertainty or held-out estimation, and a normalized 'gap closed' score is unstable when the gap is nearly zero. Preserve the already-declared fixed default and paired value differences as the main comparisons. Do not filter profiles by observed complementarity, choose a winner per replicate, or adapt the test set until both packages win somewhere.

If terminal correctness is saturated, there may be no headroom for that endpoint while cost differences still matter. Report that distinction rather than switch the primary outcome after seeing results or conclude that architecture is universally irrelevant.

## 4. Value needs an information and resource contract

Before A1, specify whether the adoption choice sees exact planned requests or coarse anticipated demands. It cannot see reference code, final tests, hidden task subtype labels or future failure diagnoses unless those would genuinely be available. The exact future profile can be a legitimate controlled decision input, but then the practical claim must say so.

Analysis may be a one-time cost for a reusable package family, a repeated per-profile task, or an expensive one-off inspection. Record those components and the reuse assumptions separately. The low online prediction cost of a trained algorithm selector cannot be assumed for source-intensive human/LLM review.

The current fixed-executor design can estimate behavioral choice value. A stronger system-efficiency claim also asks what else the analysis budget could buy. A simple default plus additional ordinary testing or bounded repair is a credible alternative, but changing that executor budget would be a separate policy comparison. No extra arm is adopted here; the immediate correction is to withhold the stronger economic claim without its evidence.

This protects research value from two weak successes: elaborate analysis that merely rediscovers a constant winner, and better choices purchased at a cost that would have improved the cheaper alternative more. The correct output can be conditional advice, a reliable default, an information-insufficiency finding, or an honestly inconclusive pilot.

## 5. Remaining methodological repairs

### S1 — Separate selector uncertainty from executor uncertainty

A frozen advice record scored over many implementation repeats estimates the value of those choices. It does not establish that the analyst or stochastic selector will reliably issue them again. If repeatable automated advice is claimed, specify pre-outcome selector repetitions, analyst/tool identity, information and budget, and preserve all choices. Do not add them after seeing a wrong recommendation or quietly substitute a majority vote.

### S2 — Do not control for consequences of assignment

Initial eligible source size, documented API fit and local complexity are pre-assignment rivals. Actual edit footprint, failed compilations, repairs and context traffic may be consequences of the package. Conditioning on them or restricting to successful/compiling histories can remove or distort the effect being studied. Use traces to test predicted pathways descriptively; a source-package contrast still bundles architecture, APIs, familiarity and authoring.

No special causal model is adopted. The rule is to label what is a baseline fact, an assigned intervention, an observed mediator/pathway or an outcome before analysis. Reference sentinels retain their starting-state-policy meaning.

### S3 — Preserve the full evaluation population

Some selection benchmarks legitimately define specialized solvable subsets or runtime penalties. ALF's main adoption utility cannot silently inherit those conventions. Keep all assigned profiles and known outcomes, including ties, both-package failures, timeouts and unrun/blocked states under the frozen rules. Report unknowns and coverage; final tests and recommendation holdouts remain separate.

### S4 — Outcome review must not reward the prediction

Keep the frozen behavioral oracle independent of the analyst's preferred mechanism. Where human/AI annotation of failure pathways is needed, hide prediction direction where feasible and disclose residual recognizability of package source. A valid alternative architecture or unexpected recovery remains a valid result. A pattern-label mismatch is not a behavioral failure.

## 6. Next bounded work and stopping condition

The committed queue has five priority/carry-forward full reads and two conditional method follow-ups. New high-priority material is ASlib and the failure-aware advisory study; meta-selection is the conditional source for oracle/uncertainty conventions. Direct recommendation and mapping papers remain focused acquisitions. Rice and the broader survey are provenance/discovery leads, not mandatory new detours.

For each read, reconstruct decision input, evaluated object, oracle, development/validation partition, estimator, information costs, exclusions, actual independent units, and what implication changes ALF. Stop the source pass when those defined decisions are resolved or explicitly access-blocked. More citations are not the objective. Do not restart the sixteen completed readings or expand into a generic portfolio/agent-routing system.

A0 still needs separate human disposition. Its two-baseline/four-successor cap can establish a credible source-level choice and oracle, not prove headroom or method benefit. A1 determines the actual held-out profiles, policies, primary comparison, allocation and uncertainty. No new experiment is authorized by this review.

## Verification scope

Six Markdown files are changed: PLAN, AGENTS, the active proposal and this review/source/reading packet. No runner, source fixture, scoring implementation, frozen protocol or allocation is changed. A local raw-file download failed DNS resolution; no full checkout tests are claimed. The algebra checks are model-free illustrations only. Exact publication and change-scoped CI are checked in the final handoff; documentation success is not runtime validation.
