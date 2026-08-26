# Metrics

No single score is sufficient. Correctness is primary; cost metrics are interpreted conditional on correctness.

## Primary outcomes

### Correct completion

- project builds;
- all cumulative hidden behavioral cases pass;
- no timeout or agent failure;
- no forbidden test/gold access in isolated runs.

### Complete trajectory usage

- input tokens;
- cached input tokens;
- cache-write input tokens;
- output tokens;
- reasoning output tokens;
- elapsed agent time;
- tool/command calls;
- build/test invocations where observable;
- process failures and retries.

Report **tokens per correct task** and model success jointly rather than rewarding cheap failures.

## Repository/context metrics

- source files, bytes, lines, and approximate lexical tokens;
- changed files, added/deleted lines, and diff bytes;
- unique files read and repeated reads when the agent event stream exposes them;
- maximum and cumulative context tokens where available;
- dependency and declaration counts in later benchmark versions.

## Repair burden

- non-zero agent subprocesses;
- failed builds;
- failed behavioral evaluations;
- patch iterations;
- time between first compilable and final correct state where observable.

## Longitudinal metrics

For a chain of tasks:

\[
C_{lifetime}=C_{baseline}+\sum_i C_{task_i}+C_{escaped\ defects}
\]

The pilot records the observable terms and leaves defect weighting explicit.

### Semantic recovery cost

Operational definition: resources consumed by a fresh agent before it produces a correct maintenance patch in an inherited repository. It is measured by complete trajectory cost, not an unobservable quantity called “meaning.”

### Lifetime amortized cost

\[
LAC = \frac{C_{creation}+\sum_i C_{maintenance,i}}{1+n_{maintenance}}
\]

Use only for descriptive reporting; preserve the underlying distribution and success outcomes.

## Representation metrics are explanatory, not objectives

Characters, bytes, tokenizer tokens, and AST nodes can help explain differences but cannot replace trajectory measurements. A code-golf representation may be short while being expensive to recover or repair.
