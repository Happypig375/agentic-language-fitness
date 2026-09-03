# Workstream E1 archive-only forensic attribution

descriptive and hypothesis-routing only; excludes causal claims, post-hoc p-values, context-scale slopes, and mathematical intercept estimates.

## Integrity and provenance

- Schema: `workstream-e1-report-v1`
- Report SHA-256: `644273ac0f25a32138d50d919ff15677b6ed9639a23198e0c719d154da94901d`
- Calibration report SHA-256: `dffa1df5d0b5864a4a696219169f5c8a5419fd633db74f6e095be76c004337cc`
- Analyzer Git SHA: `82c8c6bdc429f0819a718ce6c4d567fe0a30e88a`
- Verified runs/tasks: `10` / `80`
- Every run passed result, raw-inventory, artifact, source-tree, task-envelope, usage, audit, and Git-boundary reconciliation.

## Observability and missingness

Task-level provider usage and agent/evaluator/task timing aggregates are retained. Candidate event and command timing, interaction-level usage, source exposure, replay, context, compaction, full evaluator volume, and intermediate patch content are unavailable.

- `candidate_command_duration_seconds`: v3 command events contain no timestamps or durations
- `candidate_event_duration_seconds`: v3 event streams contain no timestamps or durations
- `compaction`: compaction markers are not retained
- `first_patch_tokens`: first-patch provider usage is not retained
- `full_evaluator_output_volume`: only bounded evaluator tails are retained
- `intermediate_patch_content`: only completed file-change metadata and committed boundaries are retained
- `model_interaction_count`: agent-message items are not model interaction records
- `peak_context_tokens`: peak context size is not retained
- `per_interaction_usage`: v3 retains only one aggregate provider usage record per task
- `phase_input_tokens`: phase-specific provider input usage is not retained
- `phase_output_tokens`: phase-specific provider output usage is not retained
- `phase_reasoning_tokens`: phase-specific provider reasoning usage is not retained
- `repeated_source_exposure`: aggregate input cannot identify repeated source exposure
- `time_after_first_post_edit_build_seconds`: candidate event timing is unavailable
- `time_before_first_post_edit_build_seconds`: candidate event timing is unavailable
- `time_to_first_post_edit_build_seconds`: candidate event timing is unavailable
- `transcript_tool_replay_tokens`: replayed transcript and tool tokens are not observable
- `unique_source_exposure`: aggregate input cannot identify unique source exposure

## Descriptive measures by configuration and language

| Config | Language | Tasks | Pre-edit inspect/search | First build S/F/U | Failed build/test | Repairs | Diagnostics (occ/inst) | Output proxy tokens | Project changes | Evaluator S/F/U; seconds |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| H | csharp | 8 | 8/9 | 0/0/8 | 0/0 | 0 | 0/0 | 13135 | 0/0 | 8/0/0; 25.822 |
| H | fsharp | 8 | 11/10 | 1/1/6 | 1/0 | 0 | 52/18 | 20713 | 1/1 | 8/0/0; 50.400 |
| L | csharp | 16 | 32/16 | 4/1/11 | 1/0 | 1 | 4/2 | 28617 | 0/0 | 16/0/0; 51.625 |
| L | fsharp | 16 | 32/16 | 0/13/3 | 16/0 | 12 | 310/103 | 55739 | 2/2 | 16/0/0; 98.791 |
| M | csharp | 16 | 34/16 | 12/1/3 | 1/0 | 1 | 4/2 | 27544 | 0/0 | 16/0/0; 51.655 |
| M | fsharp | 16 | 38/16 | 10/3/3 | 6/0 | 5 | 191/58 | 54357 | 2/2 | 16/0/0; 101.950 |

## Attribution-signature routing

### static-context-size

Observable measures: task boundary source proxies, task aggregate input usage, observable repair and exploration counts.

Limitation: v3 identifies neither unique source exposure nor a context-scale relationship.

Required next treatment: model-free baselines and a preregistered multi-scale context study.

### first-pass-ability

Observable measures: first post-edit build outcomes, candidate diagnostic codes and categories.

Limitation: first-patch tokens and phase reasoning are unavailable.

Required next treatment: matched gold-predecessor one-shot patch pilot.

### repair-amplification

Observable measures: failed build and test operations, repair cycles, candidate diagnostic and command volumes.

Limitation: per-cycle provider usage and replay tokens are unavailable.

Required next treatment: matched monolithic full-repair pilot.

### familiarity-comprehension

Observable measures: source inspection and search commands before the first mutation.

Limitation: observable navigation cannot establish training familiarity or hidden reasoning.

Required next treatment: matched comprehension and localization pilot.

### toolchain-project-obligations

Observable measures: project-file mutations, committed project-file changes, evaluator duration.

Limitation: candidate build duration is unavailable in v3.

Required next treatment: model-free language and toolchain baselines.

### context-pollution

Observable measures: none in v3.

Limitation: v3 starts a fresh process and conversation per task and cannot identify cross-task context pollution.

Required next treatment: separately reviewed persistent-context routing experiment.

## Evidence and claim limits

The ten calibrations are non-counting and hypothesis-generating. Aggregate input is total provider input processed over a trajectory, not unique source tokens. Recorded-output and committed-source token counts are offline proxies, not provider billing or context. Fresh-per-task runs cannot establish cross-task context pollution. This report estimates no mechanism, post-hoc significance, mathematical intercept, context-scale slope, or crossover.
