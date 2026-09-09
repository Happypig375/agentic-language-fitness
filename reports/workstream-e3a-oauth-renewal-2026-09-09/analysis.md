# E3a pilot post-pilot analysis

Assigned slots: 24; started: 24.

trajectory_with_scoring_seconds includes model, evaluation, and scoring time; phases are not summed when they overlap.

Operational completion is distinct from candidate pass; these three selected tasks and four repetitions are descriptive, not population inference. Paired differences are F# minus C# in repetition order. No successful-only filtering or prior-pilot pooling was used.

## Review coverage

Blinded unique Task 007 packets: 7; reviews applied: 7.

## Endpoint outcomes


Outcome counts (completion only; counts include every assigned slot; 1=true, 0=false, ?=unknown):

- fsharp first: {'1': 6, '0': 6, '?': 0}
- fsharp terminal: {'1': 12, '0': 0, '?': 0}
- csharp first: {'1': 11, '0': 1, '?': 0}
- csharp terminal: {'1': 12, '0': 0, '?': 0}

## Per-slot endpoint vectors

FORMAT/BUILD/DEVELOPMENT/HOLDOUT/OBLIGATIONS/COMPLETION; ? is unknown. Effective values use validated source-bound reviews over raw values; raw scores remain unchanged.

| Slot ID | Endpoint | Raw completion | Effective vector |
|---|---|---|---|
| 01-006-transition-validation-fsharp-r1 | first | false | 0/0/0/?/1/0 |
| 01-006-transition-validation-fsharp-r1 | terminal | true | 1/1/1/1/1/1 |
| 02-006-transition-validation-csharp-r1 | first | true | 1/1/1/1/1/1 |
| 02-006-transition-validation-csharp-r1 | terminal | true | 1/1/1/1/1/1 |
| 03-007-query-engine-refactor-csharp-r1 | first | ? | 1/1/1/1/1/1 |
| 03-007-query-engine-refactor-csharp-r1 | terminal | ? | 1/1/1/1/1/1 |
| 04-007-query-engine-refactor-fsharp-r1 | first | ? | 1/1/1/1/1/1 |
| 04-007-query-engine-refactor-fsharp-r1 | terminal | ? | 1/1/1/1/1/1 |
| 05-001-priority-fsharp-r1 | first | true | 1/1/1/1/1/1 |
| 05-001-priority-fsharp-r1 | terminal | true | 1/1/1/1/1/1 |
| 06-001-priority-csharp-r1 | first | true | 1/1/1/1/1/1 |
| 06-001-priority-csharp-r1 | terminal | true | 1/1/1/1/1/1 |
| 07-006-transition-validation-csharp-r2 | first | true | 1/1/1/1/1/1 |
| 07-006-transition-validation-csharp-r2 | terminal | true | 1/1/1/1/1/1 |
| 08-006-transition-validation-fsharp-r2 | first | false | 0/0/0/?/1/0 |
| 08-006-transition-validation-fsharp-r2 | terminal | true | 1/1/1/1/1/1 |
| 09-001-priority-fsharp-r2 | first | true | 1/1/1/1/1/1 |
| 09-001-priority-fsharp-r2 | terminal | true | 1/1/1/1/1/1 |
| 10-001-priority-csharp-r2 | first | true | 1/1/1/1/1/1 |
| 10-001-priority-csharp-r2 | terminal | true | 1/1/1/1/1/1 |
| 11-007-query-engine-refactor-fsharp-r2 | first | ? | 1/1/1/1/1/1 |
| 11-007-query-engine-refactor-fsharp-r2 | terminal | ? | 1/1/1/1/1/1 |
| 12-007-query-engine-refactor-csharp-r2 | first | ? | 1/1/1/1/1/1 |
| 12-007-query-engine-refactor-csharp-r2 | terminal | ? | 1/1/1/1/1/1 |
| 13-006-transition-validation-csharp-r3 | first | true | 1/1/1/1/1/1 |
| 13-006-transition-validation-csharp-r3 | terminal | true | 1/1/1/1/1/1 |
| 14-006-transition-validation-fsharp-r3 | first | false | 1/1/0/0/1/0 |
| 14-006-transition-validation-fsharp-r3 | terminal | true | 1/1/1/1/1/1 |
| 15-007-query-engine-refactor-fsharp-r3 | first | false | 0/0/0/?/?/0 |
| 15-007-query-engine-refactor-fsharp-r3 | terminal | ? | 1/1/1/1/1/1 |
| 16-007-query-engine-refactor-csharp-r3 | first | ? | 1/1/1/1/1/1 |
| 16-007-query-engine-refactor-csharp-r3 | terminal | ? | 1/1/1/1/1/1 |
| 17-001-priority-csharp-r3 | first | true | 1/1/1/1/1/1 |
| 17-001-priority-csharp-r3 | terminal | true | 1/1/1/1/1/1 |
| 18-001-priority-fsharp-r3 | first | false | 1/1/0/0/1/0 |
| 18-001-priority-fsharp-r3 | terminal | true | 1/1/1/1/1/1 |
| 19-006-transition-validation-fsharp-r4 | first | false | 0/0/0/?/1/0 |
| 19-006-transition-validation-fsharp-r4 | terminal | true | 1/1/1/1/1/1 |
| 20-006-transition-validation-csharp-r4 | first | false | 0/0/0/?/1/0 |
| 20-006-transition-validation-csharp-r4 | terminal | true | 1/1/1/1/1/1 |
| 21-007-query-engine-refactor-csharp-r4 | first | ? | 1/1/1/1/1/1 |
| 21-007-query-engine-refactor-csharp-r4 | terminal | ? | 1/1/1/1/1/1 |
| 22-007-query-engine-refactor-fsharp-r4 | first | ? | 1/1/1/1/1/1 |
| 22-007-query-engine-refactor-fsharp-r4 | terminal | ? | 1/1/1/1/1/1 |
| 23-001-priority-csharp-r4 | first | true | 1/1/1/1/1/1 |
| 23-001-priority-csharp-r4 | terminal | true | 1/1/1/1/1/1 |
| 24-001-priority-fsharp-r4 | first | true | 1/1/1/1/1/1 |
| 24-001-priority-fsharp-r4 | terminal | true | 1/1/1/1/1/1 |

## Usage and timing

Usage retains nulls and reports coverage. First-phase + repair-phase = total where all components are observed; cache/read and reasoning fields are subsets and are never added again.

| Language | Phase | Dispatches | Input | Output |
|---|---|---:|---:|---:|
| csharp | initial | 12 | 101448 | 19780 |
| csharp | repair | 1 | 11964 | 1950 |
| csharp | total | 13 | 113412 | 21730 |
| fsharp | initial | 12 | 101388 | 28297 |
| fsharp | repair | 7 | 87466 | 12888 |
| fsharp | total | 19 | 188854 | 41185 |

- observed_usage: `{"cache_write_input_tokens": null, "cached_input_tokens": null, "input_tokens": 302266, "output_tokens": 62915, "reasoning_output_tokens": 21028}`
- incremental_repair_usage: `{"cache_write_input_tokens": null, "cached_input_tokens": null, "input_tokens": 99430, "output_tokens": 14838, "reasoning_output_tokens": 2993}`
- usage_coverage: `{"cache_write_input_tokens": 0, "cached_input_tokens": 10, "input_tokens": 32, "output_tokens": 32, "reasoning_output_tokens": 32}`

## Per-task paired summaries

### 001-priority

- first_completion: differences=[0, 0, -1, 0]; coverage=4; mean=-0.25; min=-1; max=0
- first_phase_usage.input_tokens: differences=[-26, -26, -26, -26]; coverage=4; mean=-26.0; min=-26; max=-26
- first_phase_usage.output_tokens: differences=[357, 181, 314, 119]; coverage=4; mean=242.75; min=119; max=357
- repair_usage.input_tokens: differences=[0, 0, 8428, 0]; coverage=4; mean=2107.0; min=0; max=8428
- repair_usage.output_tokens: differences=[0, 0, 646, 0]; coverage=4; mean=161.5; min=0; max=646
- total_usage.input_tokens: differences=[-26, -26, 8402, -26]; coverage=4; mean=2081.0; min=-26; max=8402
- total_usage.output_tokens: differences=[357, 181, 960, 119]; coverage=4; mean=404.25; min=119; max=960
- trajectory_with_scoring_seconds: differences=[-2.2878356529399753, 2.8295962531119585, 31.535182260908186, 3.0822998816147447]; coverage=4; mean=8.789810685673729; min=-2.2878356529399753; max=31.535182260908186

### 006-transition-validation

- first_completion: differences=[-1, -1, -1, 0]; coverage=4; mean=-0.75; min=-1; max=0
- first_phase_usage.input_tokens: differences=[41, 41, 41, 41]; coverage=4; mean=41.0; min=41; max=41
- first_phase_usage.output_tokens: differences=[1326, 943, 2218, 1444]; coverage=4; mean=1482.75; min=943; max=2218
- repair_usage.input_tokens: differences=[12074, 12023, 13951, 15851]; coverage=4; mean=13474.75; min=12023; max=15851
- repair_usage.output_tokens: differences=[2159, 1974, 1965, 2142]; coverage=4; mean=2060.0; min=1965; max=2159
- total_usage.input_tokens: differences=[12115, 12064, 13992, 15892]; coverage=4; mean=13515.75; min=12064; max=15892
- total_usage.output_tokens: differences=[3485, 2917, 4183, 3586]; coverage=4; mean=3542.75; min=2917; max=4183
- trajectory_with_scoring_seconds: differences=[69.58360840100795, 61.84677778091282, 91.06090330053121, 79.80975026357919]; coverage=4; mean=75.57525993650779; min=61.84677778091282; max=91.06090330053121

### 007-query-engine-refactor

- first_completion: differences=[0, 0, -1, 0]; coverage=4; mean=-0.25; min=-1; max=0
- first_phase_usage.input_tokens: differences=[-30, -30, -30, -30]; coverage=4; mean=-30.0; min=-30; max=-30
- first_phase_usage.output_tokens: differences=[171, 361, 671, 412]; coverage=4; mean=403.75; min=171; max=671
- repair_usage.input_tokens: differences=[0, 0, 13175, 0]; coverage=4; mean=3293.75; min=0; max=13175
- repair_usage.output_tokens: differences=[0, 0, 2052, 0]; coverage=4; mean=513.0; min=0; max=2052
- total_usage.input_tokens: differences=[-30, -30, 13145, -30]; coverage=4; mean=3263.75; min=-30; max=13145
- total_usage.output_tokens: differences=[171, 361, 2723, 412]; coverage=4; mean=916.75; min=171; max=2723
- trajectory_with_scoring_seconds: differences=[5.48671399615705, 9.043896462768316, 57.331061334349215, 8.492283252999187]; coverage=4; mean=20.088488761568442; min=5.48671399615705; max=57.331061334349215

## Equal-task means

`{"first_completion": -0.4166666666666667, "first_phase_usage.input_tokens": -5.0, "first_phase_usage.output_tokens": 709.75, "repair_usage.input_tokens": 6291.833333333333, "repair_usage.output_tokens": 911.5, "total_usage.input_tokens": 6286.833333333333, "total_usage.output_tokens": 1621.25, "trajectory_with_scoring_seconds": 34.817853127916656}`

## Slot status

- 01-006-transition-validation-fsharp-r1: finished (development-passed); first/terminal scores retained separately
- 02-006-transition-validation-csharp-r1: finished (development-passed); first/terminal scores retained separately
- 03-007-query-engine-refactor-csharp-r1: finished (development-passed); first/terminal scores retained separately
- 04-007-query-engine-refactor-fsharp-r1: finished (development-passed); first/terminal scores retained separately
- 05-001-priority-fsharp-r1: finished (development-passed); first/terminal scores retained separately
- 06-001-priority-csharp-r1: finished (development-passed); first/terminal scores retained separately
- 07-006-transition-validation-csharp-r2: finished (development-passed); first/terminal scores retained separately
- 08-006-transition-validation-fsharp-r2: finished (development-passed); first/terminal scores retained separately
- 09-001-priority-fsharp-r2: finished (development-passed); first/terminal scores retained separately
- 10-001-priority-csharp-r2: finished (development-passed); first/terminal scores retained separately
- 11-007-query-engine-refactor-fsharp-r2: finished (development-passed); first/terminal scores retained separately
- 12-007-query-engine-refactor-csharp-r2: finished (development-passed); first/terminal scores retained separately
- 13-006-transition-validation-csharp-r3: finished (development-passed); first/terminal scores retained separately
- 14-006-transition-validation-fsharp-r3: finished (development-passed); first/terminal scores retained separately
- 15-007-query-engine-refactor-fsharp-r3: finished (development-passed); first/terminal scores retained separately
- 16-007-query-engine-refactor-csharp-r3: finished (development-passed); first/terminal scores retained separately
- 17-001-priority-csharp-r3: finished (development-passed); first/terminal scores retained separately
- 18-001-priority-fsharp-r3: finished (development-passed); first/terminal scores retained separately
- 19-006-transition-validation-fsharp-r4: finished (development-passed); first/terminal scores retained separately
- 20-006-transition-validation-csharp-r4: finished (development-passed); first/terminal scores retained separately
- 21-007-query-engine-refactor-csharp-r4: finished (development-passed); first/terminal scores retained separately
- 22-007-query-engine-refactor-fsharp-r4: finished (development-passed); first/terminal scores retained separately
- 23-001-priority-csharp-r4: finished (development-passed); first/terminal scores retained separately
- 24-001-priority-fsharp-r4: finished (development-passed); first/terminal scores retained separately
