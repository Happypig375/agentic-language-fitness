# Experimental design

## Core design

A repeated, blocked, paired experiment over semantically equivalent repositories.

Initial factors:

- language: F# / C#;
- model: multiple capability tiers and families;
- agent harness: at least two where feasible;
- repository size/chain stage;
- tool feedback condition;
- documentation condition.

Task and external behavior are matched. The first pair shares .NET 10, `System.Text.Json`, process protocol, and evaluator.

## Pilot

The executable pilot contains one small application and two cumulative changes. It validates infrastructure and reveals gross difficulty imbalances. It is not powered for substantive conclusions.

## Main-study sampling

- Create several paired repositories, not one translated toy.
- Use 10–30 maintenance steps per chain.
- Repeat stochastic runs at least 10 times per language × model × harness cell in the feasibility stage; determine the final count through simulation/power analysis using pilot variance.
- Randomize run order and block by model/harness/task chain.
- Use fresh agent processes and conversations at every step.

## Analysis

Correctness can be modeled with logistic mixed-effects or hierarchical models. Positive skewed cost outcomes can use log-normal/gamma models or robust paired comparisons, conditional on success and with failure handled explicitly.

A conceptual model is:

\[
Cost \sim Language + Model + Stage + Language\times Model + Language\times Stage + (1|Repository) + (1|Task) + (1|Run)
\]

Do not treat repeated tasks from the same evolving chain as independent observations.

## Confounds and controls

### Training exposure

Closed-model corpora are unknown. Use multiple models, code-corpus proxies, controlled documentation conditions, and—if feasible—matched continued-pretraining experiments with an open model.

### Implementation comparability

Equal lines of code is not the goal. Require identical external behavior and comparable architecture, then independently review whether either implementation is intentionally unidiomatic or artificially verbose.

### Tokenizer dependence

Record results under each model's native tokenizer. For representation ablations, also report characters/bytes/lexical units and avoid presenting one tokenizer as a language-intrinsic measure.

### Toolchain quality

Record diagnostic counts and messages. Shared .NET infrastructure reduces but does not eliminate compiler/language-service differences.

### Agent leakage

Use container/VM isolation and external evaluation in the main study. The local pilot is not a security boundary.

## Stopping and exclusion

Predefine timeouts, infrastructure-failure criteria, provider-error retries, and whether failed tasks stop or continue a chain. Never silently discard costly failed trajectories.
