# Plan review and corrections — 2026-09-05

**Reviewed starting head:** `b4d38f0c9213e472c2eec9c6ddbf795083e2502d`.

This is an assistant review/correction of the current planning documents, including previous assistant-authored proposals. It is not an independent human methods review, expert F#/C# sign-off, implementation audit, new literature review, or execution approval. No historical data, frozen protocol, runner, or benchmark code is changed.

## Findings and dispositions

| Finding in the prior plan | Correction |
|---|---|
| E3a coupled continuation to an external evaluator while also promising hidden cases never reach candidates. A holdout pass/fail bit can leak through another repair request. | Explicitly separate development feedback/stopping from sealed first/terminal holdout scoring; holdout never controls the trajectory. |
| Blanket blindness to gold states contradicted using a canonical gold predecessor. | Allow the approved predecessor only; hide current successor, future gold, research outcomes, and final holdouts. Language itself cannot be blinded. |
| No live calls were allowed, yet same-context provider behavior had to be proved before freeze. | Distinguish mock/controller evidence from pending live integration; live probes require capped authorization and cannot silently switch memory policy. |
| First-patch boundary and failure categories lacked application, stale-output, and candidate-caused dependency rules. | Preserve submission once; deterministic application; format failures remain output failures; verify binaries; distinguish preflight failures from candidate-caused violations. |
| Metrics started with cost conditional on correctness and called full trajectory cost semantic recovery. | Keep unconditional assigned attempts and separate correctness, generation, repair, and comprehension proxies; success-only/repair-only descriptions are selected subsets. |
| Transitive relevant closure was treated as all information needed simultaneously. | Distinguish repository, conservative reference evidence, exposed material, and resident state; permit interfaces, alternative evidence, streaming, and summaries. |
| Source requests were suppressed whenever previously read. | Suppress duplicates only while identical content is resident; allow versioned rereads after eviction, compaction, or edits. |
| Full-source below the boundary and retrieval only above it confounded access policy with scale. | Require overlapping below-boundary tasks under both policies; an oversized full-source request is an infeasible cell, not an executed failure. |
| Equal occupancy with different semantic sizes was interpreted as easier reasoning. | Same task/budget is primary; use within-task budget interventions or clearly descriptive size/occupancy curves. |
| Exact tokenizer, full hidden context, and model identity were treated as universally observable. | Use tiered observable evidence and labelled proxies; restrict exact physical-fit claims to verifiable full-request accounting. Missing essential evidence blocks that claim, not every other pilot. |
| Representation pairs were described too readily as causal language evidence; real repositories too readily as representative. | Limit claims to implementation/policy treatments; define the workload population and replicate across independent authoring/task/repository units. |
| Arbitrary half-real-task and three-domain quotas plus mandatory expert reviewers applied too broadly. | Use proportionate provenance/limitations records for E3a; broader claims need broader evidence. Record actual reviewer type; never invent human expertise or independent approval. |
| All workstreams and human checks after each block looked mandatory. | Use conditional branches and bounded authorization packets. H does not need F/G completion; a frozen authorized batch may use automatic health checks without outcome-driven extension. |
| Large duplicate instructions and stale metrics/design summaries offered competing plans. | Shorten AGENTS to a router, consolidate authority in PLAN, and align current methods, metrics, H, validity, and README. Historical proposals remain evidence, not executable orders. |

## Current decision

Next: E3a review-ready specification, a small selected-task audit, minimal model-free fixtures, and a proposed finite run budget. No live request, model-backed smoke test, subagent implementation, large benchmark construction, or successor experiment is authorized by this change.

The E3a authors must settle exact tasks, sample size, repair rounds, request/time/output ceilings, model identity policy, patch format, development/holdout partition, and memory semantics in the specification. This review deliberately does not invent those operational numbers or certify nonexistent integration evidence.

## Remaining limits

E1/E2/E2a interpretations remain descriptive and are not re-estimated here. The current OrderFlow oracle and implementations have not gained an expert equivalence certificate from a documentation edit. New hidden-case/fault checks, isolation enforcement, and per-round collection must be demonstrated in the implementation before experimental approval. Whether present authentication placement satisfies the stronger candidate boundary requires that implementation check.

No single same-language or F#/C# comparison identifies training-corpus familiarity. No number of repeated trajectories on one selected task makes it a representative task sample. A null or adverse F# result is valid evidence and must not trigger favorable workload selection.

## Verification scope

This change is documentation-only. Review the changed-file set and read back canonical documents before handoff. The existing CI may run its full workflow, but report exact status rather than infer success from a push or from earlier commits. Do not rerun paid experiments or mutate frozen manifests just to validate prose.

Primary references checked for the methodological cautions: RULER (https://arxiv.org/abs/2404.06654), EvalPlus (https://arxiv.org/abs/2305.01210), OpenAI reasoning documentation (https://developers.openai.com/api/docs/guides/reasoning), and Codex configuration reference (https://developers.openai.com/codex/config-reference/). These support the limited claims about long-context utilization, evaluation adequacy, and endpoint/version-specific accounting; they do not validate ALF's language hypothesis.
