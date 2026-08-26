# Metrics

## Unit of analysis

One **agent trajectory** = all model/tool interactions from receiving a task until success, failure, or budget exhaustion.

Store every event so aggregate metrics remain reproducible.

## Correctness metrics

- `success`: all required hidden tests pass.
- `compile_success`: final repository compiles/type-checks.
- `regressions`: pre-existing hidden tests newly failing.
- `static_findings`: normalized severity/count where available.
- `defect_escape`: failure found only by later tasks/additional tests.

## Compute metrics

- `input_tokens_total`
- `output_tokens_total`
- `reasoning_tokens_total` (when exposed)
- `cached_input_tokens` (when exposed)
- `source_tokens_read_total`
- `source_tokens_read_unique`
- `max_context_tokens`
- `tool_calls_total`
- `wall_clock_seconds`
- `provider_cost` (secondary; provider pricing changes over time)

## Repair metrics

- `compile_attempts`
- `compile_failures`
- `test_runs`
- `test_failures`
- `patch_iterations`
- `reverted_edits`
- `failed_tool_calls`

## Representation metrics

Measure final repository and task-relevant working set:

- bytes / characters;
- tokenizer tokens for each tested model;
- lines (secondary only);
- AST nodes;
- declarations;
- type annotations;
- dependency edges;
- number of files/modules loaded for successful repair.

## Maintenance metrics

### Semantic Recovery Cost (SRC)

For maintenance task \(M\):

\[
SRC(M)=\text{source/context tokens consumed before the first correct patch}
\]

Also record unique source tokens separately from repeated reads.

### Lifetime Agent Cost (LAC)

For a project history with tasks \(1...N\):

\[
LAC_N=C_{initial}+\sum_{i=1}^N C_i
\]

Report this in raw token/compute components rather than hiding it behind one conversion factor.

## Efficiency ratios

Useful derived metrics:

- total tokens per successful task;
- source tokens read per successful task;
- retries per success;
- successful modifications per million model tokens;
- regression-free modifications per million model tokens.

Avoid defining “semantic density” directly. Treat it as a latent property inferred from observable recovery and maintenance costs.
