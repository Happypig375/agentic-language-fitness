# Historical raw-run recovery (2026-08-29)

The exact exploratory run directory was recovered intact from the original ChatGPT project mirror. The tracked repository does not record the username or project identifier; the working audit copy is the gitignored path:

```text
results/codex-docker-dotnet10-gpt-5.6-luna-seed20260826-rerun3/
```

A read-only external archival copy is retained at `X:/backup20260827/Archives/SourceRepos/agentic-language-fitness-raw-runs/` alongside a sibling full SHA-256 manifest. The source mirror, working copy, and archive each contain 211 files totaling 7,673,060 bytes. Their canonical tree hash is identical: `89053d0ec51410e1732699e807039180ab1a59e3f09df5214813075b42b62335`. The canonical form is sorted relative paths with file sizes and lowercase SHA-256 digests, one UTF-8 line per file. The external manifest hash is `8f90a420f16a877dbc39ca26cd88af968681bd49de90dd3a3ba6695d1f2c79ef`; archived files and manifest are read-only.

The recovery pass checked the current repository and source tree, Orca workspace and terminal metadata, user temporary and standard document/download/desktop/OneDrive locations, WSL `kali-linux` and `docker-desktop`, conventional backup roots and C/V/X recycle bins, and the dated `X:/backup20260827` backup. Archived 26 August session metadata identified the original project mirror. No original artifact was modified or reconstructed.

Running `python scripts/alf.py audit <child-run-directory>` on each child language run produces `ok=false` and exits with status 1, with 21 errors per run. Both runs have the same seven per-task discrepancies (14 total): `accounting_errors` type, invalid accounting status, missing actionable error, `agent.ok` contradiction, task-success contradiction, usage null/availability disagreement, and missing task timing; plus seven run-level discrepancies: aggregate accounting flag, aggregate usage flag, aggregate-usage null rule, run-success rule, and three split run-timing fields. These failures are reported findings, not repaired records.

Disposition: recovered, hash-preserved legacy exploratory evidence. The pair remains excluded from formal aggregates, variance estimation, and power analysis because it predates the accounting/provenance freeze and used only one F# -> C# order with one stochastic observation per language. It may support derivation of a raw accounting fixture and descriptive historical checks, provided its audit failure remains explicit. It is never one of the planned 10 variance blocks.
