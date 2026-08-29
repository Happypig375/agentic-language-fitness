# Variance and power decision report

Cell: `variance-v2`  
Frozen manifest: `892cbd5416f8827a8c363b63b97cde8e7365687162996eb9961b61db597c6cd4`  
Report SHA-256: `0c158dd47f9cc82e6e89b9fc77f3dec550af8048484da87953b9c9c200497ede`

This report is post-hoc, deterministic, and transcript-free. Input tokens already include cached input tokens.

## Dataset and verification

Structural verification: **passed**. Retained attempts: 23; formal primaries: 20; calibration primaries: 2; complete paired blocks: 10/10; excluded infrastructure attempts: 1.

Formal run accounting: 20/20. Formal task accounting: 40/40.

## Correctness outcomes

| Language | Chains | Chain successes | Tasks | Task successes | Failure reasons |
|---|---:|---:|---:|---:|---|
| fsharp | 10 | 9 | 20 | 19 | {"agent":1,"behavioral_case_failure":1} |
| csharp | 10 | 10 | 20 | 20 | {} |

### Per-task outcomes and input-token variation

| Task | Language | Successes / attempts | Input mean | Input median | Input sample SD |
|---|---|---:|---:|---:|---:|
| 001-priority | fsharp | 10 / 10 | 103,195.600 | 98,692.000 | 21,594.024 |
| 001-priority | csharp | 10 / 10 | 108,593.100 | 105,313.000 | 27,178.159 |
| 002-overdue | fsharp | 9 / 10 | 122,014.700 | 107,948.500 | 51,599.166 |
| 002-overdue | csharp | 10 / 10 | 112,036.900 | 90,944.000 | 59,394.096 |

## Aggregate metrics by language

| Metric | F# mean | F# median | F# sample SD | C# mean | C# median | C# sample SD |
|---|---:|---:|---:|---:|---:|---:|
| input_tokens | 225,210.300 | 227,264.500 | 50,448.305 | 220,630 | 208,350.000 | 77,678.350 |
| cached_input_tokens | 209,536 | 212,736.000 | 46,089.678 | 202,419.200 | 193,152.000 | 71,311.311 |
| output_tokens | 3,686.900 | 3,647.000 | 479.987 | 3,846.800 | 3,536.000 | 986.579 |
| reasoning_output_tokens | 336.300 | 347.500 | 126.716 | 225.500 | 211.000 | 97.594 |
| tool_calls | 16.500 | 16.500 | 2.224 | 18.100 | 17.500 | 4.886 |
| commands | 14.400 | 14.000 | 2.221 | 15.500 | 15.000 | 4.601 |
| changed_files | 2 | 2.000 | 0.000 | 2 | 2.000 | 0.000 |
| added_lines | 29.800 | 23.500 | 12.309 | 34.300 | 34.500 | 2.312 |
| deleted_lines | 3.600 | 4.000 | 0.516 | 6.600 | 7.000 | 2.757 |
| diff_bytes | 2,857.800 | 2,629.500 | 587.853 | 3,594.200 | 3,560.500 | 132.813 |
| file_reads | 0 | 0.000 | 0.000 | 0 | 0.000 | 0.000 |
| unique_file_reads | 0 | 0.000 | 0.000 | 0 | 0.000 | 0.000 |
| file_revisits | 0 | 0.000 | 0.000 | 0 | 0.000 | 0.000 |
| agent_process_wall_seconds | 175.319 | 173.703 | 24.854 | 164.552 | 146.664 | 47.932 |
| evaluator_wall_seconds | 30.225 | 30.367 | 4.828 | 17.308 | 14.679 | 5.534 |
| task_total_wall_seconds | 197.364 | 191.836 | 29.011 | 176.764 | 157.500 | 49.766 |
| run_total_wall_seconds | 207.942 | 205.672 | 28.752 | 183.866 | 162.765 | 53.767 |

## Paired effects and uncertainty

Positive values mean F# used more of the metric than C#.

| Metric | Blocks | Mean F#−C# | Difference sample SD | Bootstrap 95% CI | Mean log(F#/C#) | Bootstrap 95% CI |
|---|---:|---:|---:|---:|---:|---:|
| input_tokens | 10 | 4,580.300 | 92,533.223 | [-51,209.332, 57,855.333] | 0.04843 | [-0.17130, 0.27238] |
| cached_input_tokens | 10 | 7,116.800 | 83,380.125 | [-42,316.800, 54,734.080] | 0.06197 | [-0.15814, 0.27666] |
| output_tokens | 10 | -159.900 | 1,183.681 | [-872.305, 508.602] | -0.02316 | [-0.20052, 0.15201] |
| reasoning_output_tokens | 10 | 110.800 | 152.961 | [19.500, 198.000] | 0.39612 | [0.03330, 0.74045] |
| tool_calls | 10 | -1.600 | 5.582 | [-4.900, 1.600] | -0.06871 | [-0.24300, 0.10206] |
| commands | 10 | -1.100 | 5.425 | [-4.200, 2.000] | -0.04463 | [-0.23861, 0.15568] |
| changed_files | 10 | 0.000 | 0.000 | [0.000, 0.000] | 0.00000 | [0.00000, 0.00000] |
| added_lines | 10 | -4.500 | 12.834 | [-11.600, 3.100] | -0.20798 | [-0.43134, 0.03117] |
| deleted_lines | 10 | -3.000 | 2.828 | [-4.700, -1.300] | -0.52983 | [-0.80301, -0.22139] |
| diff_bytes | 10 | -736.400 | 526.511 | [-1,039.100, -430.898] | -0.24714 | [-0.35200, -0.13989] |
| file_reads | 10 | 0.000 | 0.000 | [0.000, 0.000] | — | [—, —] |
| unique_file_reads | 10 | 0.000 | 0.000 | [0.000, 0.000] | — | [—, —] |
| file_revisits | 10 | 0.000 | 0.000 | [0.000, 0.000] | — | [—, —] |
| agent_process_wall_seconds | 10 | 10.767 | 59.667 | [-24.430, 45.031] | 0.08850 | [-0.11210, 0.28548] |
| evaluator_wall_seconds | 10 | 12.918 | 6.415 | [9.354, 16.875] | 0.58371 | [0.41668, 0.74617] |
| task_total_wall_seconds | 10 | 20.600 | 64.534 | [-17.701, 57.797] | 0.13264 | [-0.06475, 0.33032] |
| run_total_wall_seconds | 10 | 24.076 | 66.107 | [-15.854, 62.310] | 0.14821 | [-0.04153, 0.34201] |

## Order, position, and temporal diagnostics

Mean paired input-token difference was 41,252.800 when F# ran first and -32,092.200 when F# ran second. JSON preserves position strata, within-block spacing, block-index/UTC trends, and cross-metric sign/Pearson agreement.

## Frozen-rule sensitivity and exclusions

Frozen analysis retains candidate failures and excludes preregistered infrastructure-invalid attempts; successful-only results are a labeled, non-preregistered sensitivity check.

Calibration is separate and non-counting. 1 infrastructure-invalid attempt(s) remain retained with classifications and hashes.

## Power planning

Order-residual paired input-token log-ratio SD: 0.368294 with 8 residual degrees of freedom. Fixed-seed simulation used 20,000 draws per displayed grid size as a cross-check only.

| Plausible ratio | Log effect | Analytic minimum pairs at 80% power |
|---:|---:|---:|
| 1.07 | 0.067659 | 233 |
| 1.08 | 0.076961 | 180 |

Analytic method: Monotone closed-form two-sided known-SD z-test power using NormalDist.cdf; analytic minima drive the decision.

Simulation cross-check: Fixed-seed normal Monte Carlo at displayed grid sizes is a cross-check only and does not define the minimum.

Limits:

- The ten-block pilot residual SD has only the reported residual degrees of freedom and is uncertain.
- Known-SD z power assumes independent normal order-residual log ratios and is a planning approximation.
- Planning should allow for SD estimation, attrition, temporal drift, and multiplicity.
- Power describes token log ratios, not correctness or a universal language effect.

## Decision

Formal success: 19/20 chains (95.0%) and 39/40 tasks (97.5%); the explicit pilot near-saturation threshold is ≥95% task success.

**variance_overwhelms_plausible_effects_and_correctness_near_saturated**

- The monotone analytic token power curve needs approximately 180–233 paired blocks for 80% power.
- Formal task success is 39/40 (97.5%), meeting the explicit ≥95% near-saturation threshold; formal chain success is 19/20 (95.0%).
- Extend or recalibrate the maintenance chain while improving temporal blocking and increasing paired repetitions.
- This variance pilot does not establish a causal or universal language ranking.
