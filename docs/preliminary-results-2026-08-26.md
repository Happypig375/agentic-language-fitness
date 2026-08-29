# Historical exploratory paired result (2026-08-26)

> **Provenance status as of 2026-08-29:** the exact raw run directory was recovered and hash-preserved; see `docs/historical-run-recovery-2026-08-29.md`. The legacy artifacts fail the hardened `alf audit` schema checks, so the figures below remain a historical smoke-test summary. Exclude this pair from formal aggregates, variance estimation, power calculations, and language-effect claims. Do not reconstruct or repair raw records from these totals.

The container-isolated rerun reportedly completed both inherited tasks for both languages: F# 2/2 and C# 2/2, with all cumulative behavioral cases passing. This was one stochastic run per language over two small tasks; it does not estimate a language effect, uncertainty interval, significance, or causal conclusion.

Reported run conditions: schedule label `20260826`, F# then C#, model `gpt-5.6-luna`, Codex CLI `0.149.1`, fresh ephemeral process and container per task, .NET SDK `10.0.302`, Python `3.11.15`, Git `2.46.2.windows.1`, and image `alf-codex:0.149.1` with immutable ID `sha256:0320a60c5b2628cebeb2c897bbf80da949f3b9bb99fa61f5a3475c7276328756`.

| Reported metric | F# | C# |
|---|---:|---:|
| Input tokens | 317,078 | 312,958 |
| Output tokens | 5,963 | 4,717 |
| Reasoning output tokens | 2,251 | 1,354 |
| Tool calls | 18 | 17 |
| Agent wall time | 272.470 s | 200.109 s |

The recorded aggregate input was nearly tied (F# +1.3%), but task direction reversed: `001-priority` recorded 233,794 F# versus 95,401 C# input tokens, while `002-overdue` recorded 83,284 F# versus 217,557 C#. Even if later verified, this pattern is compatible with trajectory variance, order effects, temporal/provider drift, and task-specific choices; no stable language interpretation is warranted.

The original note stated that all four processes exited successfully, builds had zero warnings/errors, and artifact scans found no credential leakage. Those statements also require the original artifacts for independent verification.

The recovered working copy is the local, ignored directory:

```text
results/codex-docker-dotnet10-gpt-5.6-luna-seed20260826-rerun3/
```

The exact artifacts are recovered, but the pair is permanently classified as unaudited legacy evidence because its schema predates the current accounting/provenance contract. Begin the formal dataset with a new frozen-protocol calibration and 10 new counterbalanced paired blocks.
