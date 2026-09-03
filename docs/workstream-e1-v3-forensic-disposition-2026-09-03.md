# E1 v3 forensic disposition — 2026-09-03

E1 is complete and independently approved. Analyzer commit `82c8c6bdc429f0819a718ce6c4d567fe0a30e88a` passed exact-commit Linux/Windows CI. The transcript-free report records SHA `644273ac0f25a32138d50d919ff15677b6ed9639a23198e0c719d154da94901d` and preserved identities under `inputs`, `runs`, and `task_index`; its publication is accepted only after the report commit's own exact-commit CI is green. It reconciles 10 runs, 80 tasks, 435 completed commands, 11 event shapes, and 12 command-equivalence classes (`aggregates.overall`, `coverage`).

| Signal | Descriptive result |
|---|---|
| First post-edit build | 19 failures, 27 successes, 34 unavailable; F# failures exceeded C# in H/M/L (1/0, 3/1, 13/1). |
| Failed builds / repair | 25 failed candidate operations, all builds; 19 repair cycles. F# exceeded C# in every configuration. |
| Diagnostics | 107 error occurrences and 454 warning occurrences; errors F#/C# were H 2/0, L 64/2, M 35/4. Of the warnings, 450 are repeated FS3261 output occurrences, not independent defects. |
| Exploration | 83 searches and 155 source inspections overall; navigation cannot establish familiarity. |
| Project/evaluator | All 5 committed project-file changes were F#; evaluator duration was about twice F# vs C# in every configuration. |
| Proxies | Output, aggregate input, agent time, and evaluator time are ecological proxies, not unique exposure, per-interaction usage, or command timing. |

This routes descriptive follow-up toward compiler-repair and ecological toolchain mechanisms. It establishes no causal or universal language claim and no slope/intercept. For Task 007, the frozen runner diff omitted an untracked addition before `git add`; E1 preserves that frozen runner metric and separately recomputes the full committed boundary. Fresh-per-task v3 cannot identify cross-task context pollution.

E2 is the sole next bounded task: model-free/offline 18 canonical states × exactly five paired rounds, fresh-workspace and immediate repeat-workspace regimes, fixed commands, hashes, and source/project obligations. Stop after E2 reporting, independent review, and exact-commit CI; no E3/model calls or remote benchmark route.
