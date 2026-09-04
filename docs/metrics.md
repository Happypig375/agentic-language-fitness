# Metrics and interpretation

**Revised:** 2026-09-05. Measurement rules for new studies; historical schemas/results remain unchanged. Read [PLAN.md](../PLAN.md) and the frozen protocol for the specific experiment.

## Preserve outcome dimensions

For each assigned trajectory retain: request/attempt status; protocol and accounting validity; submission-format/application status; build status; declared API/development-test status; sealed holdout correctness; terminal reason; and resource use. Do not reduce all of these to one success flag for scientific analysis.

For E3a, the proposed primary endpoint is first-submission joint build and holdout behavioral correctness. Terminal correctness and cost remain important secondary outcomes. A passing compiler is not proof of correct behavior; an unavailable outcome is not a pass. First-pass refers to the submitted patch boundary, not the first internal editing action.

## Model usage

Record provider-reported input, cache-read, cache-write, output, reasoning, and request identifiers when exposed. Document subset semantics for the exact adapter/version. Cached input is often a component of input and reasoning often a component of output; never add subset fields again without evidence of disjointness.

Keep raw usage, normalized usage, aggregation rules, and reconciliation results. Distinguish absent fields from measured zero. If a timeout or interrupted request has incomplete usage, preserve known usage and mark the total incomplete rather than report an exact cheap failure. A summary with partial coverage must report its coverage.

Token totals, provider billing, subscription consumption, and machine computation are not interchangeable. Report priced cost only under a dated explicit pricing/caching rule; do not invent a currency or quota conversion. No single unweighted sum of tokens, seconds, and defects is meaningful.

## Time and tool behavior

Record elapsed model/agent process, controller build/test execution, total trajectory, and infrastructure setup separately. Concurrent/nested timings are not necessarily additive. Tools waiting longer do not automatically use more model tokens; polling, feedback, and extra model requests may do so.

Classify build/restore/run/test commands by actual semantics. Count failed operation episodes and repair transitions, not repeated diagnostic lines as independent bugs. Retain diagnostic codes/categories, raw output volume, exact candidate-visible packet volume, truncation, and duplicate handling. Model-free invocation-count × duration envelopes are descriptive, not causal fractions to subtract from agent time.

Separate syntax/type/API/project failures from dependency/audit/host failures. Attribute candidate-induced forbidden project/dependency changes according to frozen rules, not automatically to infrastructure.

## First-phase and repair resources

For every trajectory:

```text
total observed resources = initial-phase resources + subsequent repair-phase resources
```

This is accounting over disjoint observed phases, not causal mediation. Successful initial submissions have zero repair resources in the unconditional mean. Report failure-conditioned repair distributions separately because different languages may produce different kinds of first failures.

Primary summaries retain failed and timed-out valid attempts. A ratio such as total tokens across all assigned attempts divided by completed tasks can be descriptive, but is not an unbiased expected cost-to-success unless an explicit retry policy is being evaluated; it is undefined when no tasks succeed. Never replace the main distribution with successful-runs-only averages.

## Source, context, and information

Record separately:

- source bytes/lines and declared tokenizer/proxy counts;
- current full-repository and reviewed reference-evidence sizes;
- source chunks actually returned, their versions, and unique/repeated reads;
- active request size, retained source/summaries, and removed/compacted content where observable;
- cumulative input across calls and final output/patch size.

Provider input totals include wrappers/history and possibly opaque state. A visible-source proxy is not exact provider context. Exact attribution to hidden reasoning is not required and must not be invented. Treat an unexplained remainder as unexplained.

A full successful maintenance trajectory is a proxy for overall recovery-and-edit cost, not an isolated measurement of comprehension. Distinguishing comprehension, generation, retrieval, and repair needs the interventions and evidence described in the plan.

## Chains and generalization

Report task-position survival, terminal failure, cumulative cost, regressions, and paired common-exposure summaries. Common-exposure or completed-chain subsets are descriptive selected outcomes. Preserve the unconditional assigned sample and do not infer universal language effects from them.

Creation cost and long-term escaped defects are not measured by starting from canonical predecessor code. Call current totals maintenance-trajectory cost. A future lifetime/amortized metric must state which phases were actually observed and which weights are assumptions.

Use repetitions to estimate variability within tasks and independent repository/task samples for workload generalization. Keep historical exploratory calibration, controlled feedback, free-tool ecology, and native-repository strata identifiable. See [experimental design](experimental-design.md) for inference and stopping rules.
