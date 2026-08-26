# Preliminary paired result (2026-08-26)

The container-isolated rerun completed both inherited tasks for both languages: F# 2/2 and C# 2/2, with all cumulative behavioral cases passing. This is one stochastic run per language over two small tasks; it does not estimate a language effect, uncertainty interval, significance, or causal conclusion.

Run conditions: seed `20260826`, F# then C#, model `gpt-5.6-luna`, Codex CLI `0.149.1`, fresh ephemeral process and container per task, .NET SDK `10.0.302`, Python `3.11.15`, Git `2.46.2.windows.1`, and image `alf-codex:0.149.1` with immutable ID `sha256:0320a60c5b2628cebeb2c897bbf80da949f3b9bb99fa61f5a3475c7276328756`.

| Metric | F# | C# |
|---|---:|---:|
| Input tokens | 317,078 | 312,958 |
| Output tokens | 5,963 | 4,717 |
| Reasoning output tokens | 2,251 | 1,354 |
| Tool calls | 18 | 17 |
| Agent wall time | 272.470 s | 200.109 s |

Aggregate input was nearly tied (F# +1.3%), but task direction reversed: `001-priority` used 233,794 F# versus 95,401 C# input tokens, while `002-overdue` used 83,284 F# versus 217,557 C#. This is compatible with trajectory variance and task-specific choices; no stable language interpretation is warranted.

All four processes exited successfully; builds had zero warnings/errors and artifact scans found no credential leakage. The complete raw report and machine-readable results remain in the local, ignored run directory `results/codex-docker-dotnet10-gpt-5.6-luna-seed20260826-rerun3/`; they are intentionally not forced into Git. Repeated randomized blocks, more tasks, and ideally more models remain necessary.
