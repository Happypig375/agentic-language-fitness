# Workstream H: source capacity, context use, and retrieval

**Revised:** 2026-09-05. Future design under [PLAN.md](../PLAN.md). This document does not authorize construction of a large suite or any live model run.

## Questions, not assumed advantages

At the same semantic task and source-access budget, does one implementation fit more useful material, use it more reliably, or retrieve it more economically? F# brevity in lines is not evidence of fewer model tokens, and fewer tokens is not evidence of better understanding.

Distinguish three outcomes: serialized capacity; task correctness under a budget; and ecological trajectory cost. A small-repository penalty cannot identify an intercept or scale slope across unobserved sizes. Any linear cost/crossover sketch is illustrative; fit flexible curves or preregistered contrasts once multiple scales exist.

## Size is not simultaneous necessity

Record separately:

- `T_repo`: eligible repository source, build metadata, and documentation;
- `T_ref`: source in a reviewed reference solution's conservative relevance/dependency set;
- `T_exposed`: source actually returned to the candidate;
- `T_resident`: source and summaries still present in each active request;
- cumulative model input, which includes replay and is not any of the above.

A transitive dependency closure is neither a minimal sufficient explanation nor a lower bound on memory. A global change may be solved by interfaces, a fold over modules, streaming checks, or a compact summary. Even when `T_ref` exceeds the window, do not claim all of it must be resident simultaneously. The scientific question is how well a declared retrieval/memory policy solves the task.

Relevance annotations may have multiple sufficient alternatives. Validate them using independent solutions, sensitivity/fault checks, dependency analysis, and documented uncertainty. Do not score valid alternative navigation as failure merely because it differs from one gold patch.

## Request budget and observability

For an endpoint where context is a joint input-plus-output limit, reserve output once and enforce:

```text
fixed prefix + current source + retained summaries/history
+ tool wrappers/feedback + output reserve <= verified request cap
```

For an input-only endpoint cap, use its documented accounting instead. Do not subtract output or a safety allowance twice from an already-reduced effective limit. The per-request ledger must state the convention, safety margin, treatment cap, and any provider-hidden/unattributed remainder.

`B_source` is the source allocation after fixed prefix, retained-memory, feedback, and endpoint-appropriate output allowances. These allocations are experimental choices and remain separate from the model's physical maximum. A harness context setting or early auto-compaction threshold does not change model architecture and may not enforce the requested cap. Verify actual request behavior; fail closed on unexpected overflow/truncation.

Use the endpoint's exact input counter/tokenizer if supported. Otherwise pin and label a proxy and bound its error against observed request totals. Approximate source-size results remain useful, but an exact claim that one language physically fits and the other does not requires verified full-request accounting near that boundary. Do not require access to hidden reasoning text or invent its token decomposition. Cached input remains context occupancy even when billing differs.

Separate the hard accepted request limit from the empirically useful length at a stated accuracy criterion. Useful length is an outcome, can be task/position dependent, and may be far below the accepted limit. A cap at 32K on a larger model is a software-budget intervention, not evidence about native 32K or million-token model behavior.

## Start small and identify one contrast

H0 is model-free: one paired exemplar, exact/proxy serialization audit, synthetic controller fixtures, budget enforcement, and known eviction/reread cases. Do not initially build all domains, sizes, retrieval algorithms, and memory policies.

Then propose a bounded non-counting pilot on the same model with a few semantic sizes and a few software-enforced budgets. Example budgets of 32K/64K/128K are provisional cost choices, not defaults or authorizations. Replicate absolute long inputs only after the accounting and workload review pass.

Vary repository distractor load separately from task-required semantic work where possible. Useful task families are local changes with bounded evidence; distributed integration; and broader transformations that may or may not admit compact contracts. All added modules must do real tested work, not merely contain active-looking repeated boilerplate. Report template duplication and generator ancestry; generated sizes are not independent real repositories.

## Access conditions

### H1: supplied source, no retrieval or execution feedback

Where the full eligible source fits the declared source budget, serialize it into the first request. Use a fixed task response format, normally one patch, and score externally. No source tools, hidden language-server checks, compiler feedback, or automatic compaction in this condition. Refuse an oversized prompt rather than silently truncate it.

Counterbalance relevant material's prompt positions using the same semantic order/permutations for both languages. Preserve project compile-order metadata separately. Report normalized token position as well as file order. Avoid forcing identical byte offsets through padding in the primary comparison.

### H2: bounded selective retrieval

Expose a realistic, reproducible repository map and a small tool set such as tree listing, text/symbol search, and token-bounded chunk reading. Index preparation and map size count toward resource/context accounting. Keep semantic mappings used by the evaluator out of candidate-visible tools.

Freeze indexing, ranking, top-k/results caps, serialization, source eligibility, documentation access, and search/read budgets. Equal schemas alone do not ensure equal retrieval quality. Freeze comparable language-service support, or name differences as part of a separate ecological treatment.

Measure calls, bytes/tokens returned, unique material, repeated requests, reference-set recall/precision with uncertainty, and final task quality. A token limit can split a function; preserve context/continuation markers consistently. Budget exhaustion is a treatment outcome, not a reason to silently raise the cap.

**Deduplicate only resident, unchanged chunks.** Use content/version identities, not path alone. After eviction, compaction, or edits, a repeated read must be able to return actual current content and is charged/logged again. A pointer to missing text is not memory. Blanket suppression of rereads would selectively damage the over-window condition.

### H3: managed memory when evidence does not all remain resident

Choose one simple declared retention/summary policy first. Preserve raw material externally, expose only retained state, and record eviction, summary production, retrieval, and recomputation costs. Test whether compact contracts or streaming solve the task before labeling it capacity-limited.

A model-made summary or subagent is an additional model intervention and has its own budget/accounting; it is not a free preprocessing step. No silent general-purpose compaction. Fresh-per-task versus persistent history is a separate factor, introduced only when required by the question.

### Required overlap

Use at least some identical below-boundary tasks under both H1 and H2. Otherwise access regime is perfectly confounded with size: an apparent boundary effect could be a switch from supplied source to retrieval. Above the H1 limit, record H1 as infeasible under that budget, not as an executed model failure. Do not estimate an unconstrained language × scale × access factorial where cells cannot exist.

## Fair comparison and scale selection

Primary paired comparisons use the same semantic workload, model, budget, output allowance, task, and access policy. Serialization lengths are outcomes; do not equalize them by adding code or removing behavior. Freeze scales independently of the direction of F#/C# results.

Plot performance against semantic size and measured occupancy, but equal occupancy achieved by different-sized systems is not a clean test of ease of understanding. It changes task complexity. Use within-task budget sweeps, an explicit semantic-size term, or cautiously labelled descriptive interpolation; do not conclude superior reasoning from equal-occupancy plots alone.

Define serialized capacity as the largest measured semantic configuration whose **specified source bundle** fits a verified request. This is not the largest program the model can maintain: selective retrieval and abstractions can exceed it. Report capacity separately from accuracy and cost. The original fit hypothesis is unsupported for any tested family/tokenizer without a measured token advantage; do not discard that family to search only for favorable examples.

Near-boundary levels, multiple useful-length measurements, and wider absolute lengths belong to a later reviewed design. No obligatory five/six-level or three-domain factorial is imposed on the initial feasibility pilot. A crossover claim requires an observed, replicated change within the tested range with uncertainty, not extrapolation from the small-repository result.

## Tools, feedback, and endpoints

Compiler/test feedback is absent from the primary source-context comparison. A separately named repair condition may use the clean E3a controller and development feedback, never final-holdout feedback. Source inspection itself is not pollution; it is the mechanism being measured. Log retrieval wrappers, previous model output, stale-source versions, diagnostics, and summaries separately from current source.

The primary H1/H2 patch endpoint is joint build and final-holdout behavioral correctness at fixed budget. Report format/build/API failures separately so generation difficulty is not mistaken for retrieval failure. A bounded auxiliary read-only task may help distinguish localization from patch generation, but it changes the intervention and must be specified rather than silently added to every prompt.

Other outcomes include total/provider input and output; declared token subsets; source exposure/retention; search/read budget use; tool and model latency; compaction events; defects; and output truncation. Missing telemetry limits only the claims that depend on it. A context-mechanism arm cannot proceed if its own visible request composition is unauditable.

## Sequence and decision

H may be proposed after a usable controller and workload gate, without completing optional F or G studies. Present authorization remains E3a preparation only. A small source-only H pilot does not require exhaustive explanation of repair behavior because its primary arm has no repair feedback.

```text
reviewed workload/exemplar + H0 model-free budget checks
  -> separately authorized bounded H1/H2 overlap pilot
  -> review accuracy, generation failures, size and retrieval evidence
  -> justified absolute-length or H3 memory study
```

Stop for leakage, untracked context/compaction, invalid workload equivalence, exhausted limits, or a material policy change. A disappointing language effect is a reportable finding, not permission to alter tasks or keep adding levels. Evidence about this family/model/harness is not an intrinsic language ranking.

## Supporting sources and limits

- Hsieh et al., RULER, https://arxiv.org/abs/2404.06654 : accepted/advertised length and successful task use are different; the paper is not evidence of an F# effect.
- OpenAI reasoning guide, https://developers.openai.com/api/docs/guides/reasoning : verify endpoint-specific context/output accounting and retained state for the pinned model.
- Codex configuration reference, https://developers.openai.com/codex/config-reference/ : configuration is version dependent; pin and test the installed harness rather than importing a current default into a historical run.

Sources checked 2026-09-05. These support the accounting/evaluation cautions, not the proposed language hypothesis or an already completed H experiment.
