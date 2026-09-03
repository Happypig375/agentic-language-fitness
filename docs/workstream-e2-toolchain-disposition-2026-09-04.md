# Workstream E2 model-free toolchain disposition

Date: 2026-09-04

## Status and identity

Workstream E2 completed its frozen, model-free measurement and independent
report review. The successful attempt was GitHub Actions run
[`33799957422`](https://github.com/Happypig375/agentic-language-fitness/actions/runs/33799957422)
at runner commit `b953dac54c03087ae46689bc62a3221c3c9d3f97`.

The accepted identities are:

- definition SHA-256:
  `09d5669fd554e611b4df505454a40f06a0e9b2a23c4a16a28c9cc94d640067f7`;
- schedule SHA-256:
  `c6915378561201778e6cfdc139bd9deff0cb58d7621da3e45b5ec8dda27c37e1`;
- container image ID:
  `sha256:a07394d59b0182a95c95cb82ad044fd777491cdf924f066f678238e3a09c4022`;
- report self-hash:
  `2e4381ab67dd4cc7aed24c323e8edbd30bf83dd29bafc58554615bcd6f24c49a`;
- raw inventory SHA-256:
  `59b3e3c11ed10dbd7e0e5172b8761d3a257684eb0d8bf983a2cdfd93787729e6`;
- environment profile:
  `github-actions-ubuntu-24.04-dotnet10.0.302-offline-v1`.

The checked-in [JSON report](../reports/workstream-e2-toolchain-v1/report.json)
is the immutable audited run output. The compact
[Markdown report](../reports/workstream-e2-toolchain-v1/report.md) contains its
operation-timing table. Raw streams and command metadata remain outside Git.

No model, Codex candidate, remote runner, proxy route, or model credential was
used.

This report publication is accepted only if the exact commit containing it
passes both Linux and Windows CI. Until then, E3 is not active. Once both jobs
are green, this condition is satisfied without a status-only follow-up commit.

## Attempt ledger

These were apparatus attempts under the same E2 scientific definition, not new
scientific versions:

| Actions run | Runner commit | Disposition |
|---:|---|---|
| `33788142628` | `0548a1f6d5d539cc102f8ddc85e0e87c69fdf40f` | Pre-measurement failure: dropped capabilities prevented container UID 0 from writing runner-owned work/raw mounts. No sample completed. |
| `33789713621` | `41eb23ab90d0407c763caa58d1aea4a5cf3a7d6e` | Pre-candidate failure after all 18 static preflights: the first restore could not create .NET's named-mutex directory on read-only `/tmp`. No sample completed. |
| `33799957422` | `b953dac54c03087ae46689bc62a3221c3c9d3f97` | Success after the explicitly authorized bounded `/tmp` tmpfs correction. |

The successful implementation maps the container to the runner UID/GID and
mounts a bounded 256 MiB tmpfs at `/tmp`. The rest of the image remains
read-only; the measurement and audit containers have only loopback networking,
no usable default route, dropped capabilities, and a read-only package cache.

## Exit audit

The Actions audit and a separate local audit both passed. The successful
attempt established:

- all 18 canonical states matched the frozen definition;
- all 90 schedule entries completed in the frozen interleaved order;
- all fresh-workspace and immediate repeat-workspace commands succeeded without
  timeout;
- all 180 evaluator invocations passed all 6,940 cumulative case exposures and
  their cumulative workspace checks;
- the package cache was byte-identical before and after measurement;
- 1,354 raw-evidence files (633,162 bytes) reconciled through the raw inventory
  and terminal-attempt hashes; and
- compiler-phase timing, observed compiler inputs, and machine-cold state remain
  explicitly unavailable rather than estimated.

## Descriptive result

The table uses all 45 matched F#/C# stage-by-round pairs. Means are across the
45 observations per language; the ratio is the geometric mean of the 45 paired
F#/C# ratios.

| Measure | F# mean (s) | C# mean (s) | Paired F#/C# ratio |
|---|---:|---:|---:|
| Fresh restore | 6.410 | 0.763 | 8.403 |
| Fresh build | 2.107 | 0.706 | 3.037 |
| Fresh run | 0.538 | 0.545 | 0.988 |
| Fresh restore-through-evaluator composite | 9.060 | 2.025 | 4.490 |
| Repeat build | 2.102 | 0.674 | 3.117 |
| Repeat run | 0.537 | 0.546 | 0.984 |
| Repeat build-through-evaluator composite | 2.643 | 1.231 | 2.148 |

Restore, build, and both composites favored C# in all 45 matched pairs. Run
timing was near parity and favored F# in 32 of 45 pairs. Stage-level ratios were
stable apart from one C# fresh-build outlier: fresh restore ranged from 8.35 to
8.48, repeat build from 3.01 to 3.25, and repeat composite from 2.02 to 2.21.

This local environment therefore exposes a large F# ecological toolchain cost
before and during compilation, not during execution of the built program. The
repeat result is important: F# build time remained about 3.1 times C# after the
workspace had already been restored and built once.

## Static source and project obligations

The static comparison does not show a comparably large representation-size
difference:

- at baseline, F#/C# whole-tree tokenizer-proxy tokens were 414/424 (ratio
  0.976);
- across all nine states, the geometric-mean F#/C# source-token and whole-tree
  token ratios were approximately 0.997 and 1.025;
- at stage 8, F# had fewer source bytes, lines, and lexical units
  (7,650/253/1,378 versus 8,100/274/1,525) but more source proxy tokens
  (1,695 versus 1,635) and more whole-tree proxy tokens (1,790 versus 1,700);
- both final states contained two source files; and
- Task 007 required F# to edit its project file and declare the new module in
  compile order, while C# used SDK-default discovery. Final project proxy tokens
  were 95 for F# and 65 for C#.

Release artifact trees averaged 19 files and 2,967,145 bytes for F#, versus five
files and 105,073 bytes for C# (paired size ratio about 28.25). The report does
not decompose those artifact bytes, so it does not assign that difference to a
specific component.

## Warning-field correction

The immutable JSON report has one known derived-field defect. Its original
generic matcher classified .NET summary footers such as `0 Warning(s)` as one
`UNSPECIFIED` warning. This did not affect commands, timing, correctness,
identities, raw streams, or code-bearing diagnostic records.

Accordingly:

- exclude all 180 `UNSPECIFIED` footer matches from interpretation;
- C# emitted no code-bearing warning line;
- F# emitted 225 code-bearing `NU1900` lines: 45 during restore and 180 across
  fresh and repeat builds. Build output repeats the same diagnostic line, so
  this is an emitted-line count rather than 225 unique conditions; and
- the warning parser is corrected prospectively in the report-publication
  change, with regression coverage for zero/nonzero summary footers, coded
  diagnostics, and uncoded warning text.

`NU1900` reflects unavailable package-vulnerability data in this deliberately
offline environment. Its presence only for the F# path makes the fresh restore
gap environment-specific and potentially entangled with NuGet audit behavior.
The baseline does not identify how much of the restore gap is audit waiting,
package handling, SDK behavior, or another component. The repeat-build gap does
not include restore and remains the cleaner compiler/toolchain signal.

## Interpretation and next decision

E2 strengthens the toolchain/project-and-repair-feedback route for a bounded E3
mechanism pilot:

- source/token proxy size was near parity and cannot by itself explain a
  threefold build-time or 4.5-fold fresh-composite gap;
- built-program run time was near parity;
- build latency remained substantially higher for F# in both workspace regimes;
- F# alone carried an explicit project compile-order edit at the multi-file
  stage; and
- offline NuGet behavior is a measured ecological difference that a later
  controlled-core treatment would need to separate explicitly.

Do not subtract E2 timing mechanically from the v3 agent totals: tool latency
and diagnostics can change agent decisions, repair cycles, and replayed input.
E2 does not identify model familiarity, first-pass generation ability,
causality, a mathematical intercept or scale slope, a context-density
crossover, or a universal F#/C# ranking.

The next allowed work is specification and independent review of the bounded E3
comprehension/one-shot/full-repair pilot from matched gold predecessors. This
disposition does not authorize a model call; stop before any paid/model activity
until that specification is independently approved and cleanly frozen.
