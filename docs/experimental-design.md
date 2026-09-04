# Experimental design

**Revised:** 2026-09-05. Companion to [PLAN.md](../PLAN.md). Frozen historical protocols keep their original analysis; these rules govern new specifications.

## Estimand before apparatus

Specify the target population or narrow case, assigned treatment, starting state, candidate authority, feedback, budget, endpoints, and inference unit. A matched F#/C# pair estimates a contrast between particular implementations with their idioms and model familiarity. It is not random assignment of programming languages to all possible software and does not isolate syntax.

Distinguish maintenance from creation. E3a starts at fixed canonical predecessors and estimates local first-patch/repair behavior; inherited-chain studies estimate evolution from previous agent outputs. Neither is automatically a lifetime ownership estimate. Do not mix them or add unmeasured creation/defect costs to a headline total.

## Units, pairing, and selection

Pair languages on semantic task, predecessor contract, model/effort, harness, resource policy, and temporal block. Randomize and counterbalance language order; record wall-clock/provider/configuration metadata. A scheduling seed is not a reproducible model seed unless the endpoint supports it.

A model trajectory is an observation, not an independently sampled real-world task. Tasks inside one evolving chain, sizes emitted by one generator, and multiple runs on one repository are dependent. Repetitions estimate stochastic variation within that workload. Generalization needs independent tasks/repositories and defensible sampling, not merely more runs.

Freeze task selection, exclusions, outcome hierarchy, sample ceiling, and resource limits before new outcomes. The E3a diagnostic sample is deliberately enriched using earlier findings and is exploratory. Do not present it as a random workload sample. A familiar model name does not guarantee a fixed backend; retain aliases, exact versions when exposed, and dates without claiming unavailable identity precision.

## Analysis proportional to the data

For the E3a pilot, report counts and task-paired distributions before fitting a model: first-submission joint correctness, compilation/behavioral components, terminal correctness, failure classes, and first-phase versus incremental repair resources. Primary and secondary endpoints belong in the frozen specification, not a growing menu of significant metrics.

Report all valid assigned attempts, including output-format failures, wrong programs, and timeouts. Keep apparatus/permission/accounting validity separate from candidate correctness. Success-only costs and repair-only costs are selected-population descriptions, not the primary language-cost effect.

For later chains, retain task survival and terminal cost. A common-exposure prefix may be descriptive, but it is determined by outcomes and does not by itself remove censoring or selection. Do not rank a cheap early failure as efficient completion.

Use paired uncertainty estimates with the independent block/repository as the resampling unit. With very few independent tasks or repositories, report that limitation rather than fitting a large mixed-effects interaction model. A future multilevel model must have enough independent levels to estimate its variance components. Equal-occupancy comparisons across different semantic tasks require task-complexity controls and remain limited; see the [H design](workstream-h-context-pressure-design-2026-09-05.md).

Practical equivalence needs a justified, preregistered margin and an uncertainty interval sufficiently inside it; lack of significance is not equivalence. Multiple confirmatory contrasts need a declared testing hierarchy or multiplicity adjustment. Exploratory p-values, if shown, must not be promoted to preregistered confirmation.

## Fixed collection and adaptations

Use a fixed sample initially. A precision-based or difficulty-based adaptation needs a predeclared rule with an inferential justification; calling a look 'blinded' does not automatically remove optional-stopping or selection effects. Prefer simulation of the exact analysis/stopping procedure before authorizing a confirmatory adaptive run.

Within an authorized frozen batch, operational health checks can be automatic. No task/model/harness replacement because the emerging language effect is inconvenient. Exclusions and retries follow predeclared failure classes, retain all attempt IDs, and distinguish a confirmed unsubmitted request from one that may already have consumed quota. Stop rather than blindly replay an ambiguous request.

## Information and evaluation

Approved predecessor code and development checks are candidate-visible inputs. Successor gold and final holdout cases are not. Final holdout scores cannot guide feedback, repair stopping, task selection, or runtime decisions. Record first and terminal submissions before sealed scoring.

Common tests are not a proof of equivalent implementations. Audit the behavioral contract, expected outputs, plausible faults, and explicit API requirements; allow valid alternative internal implementations. Code and project-file execution must remain sandboxed, with the scorer and credentials outside candidate control.

## References and linked rules

See [metrics](metrics.md) for accounting, [validity and review gates](workload-validity-and-review-gates-2026-09-05.md) for workload/reviewer evidence, and [H](workstream-h-context-pressure-design-2026-09-05.md) for context controls.

Liu et al., *Is Your Code Generated by ChatGPT Really Correct?* (EvalPlus), https://arxiv.org/abs/2305.01210 , demonstrates why inadequate tests can miss incorrect code and change model rankings. This motivates evaluator fault checks; it does not validate ALF's existing oracle or an F#/C# effect.
