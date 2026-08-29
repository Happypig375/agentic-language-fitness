# Variance-v2 results — 2026-08-29

## Cell and provenance

The accepted variance-v2 cell was frozen from Git commit
`5363e4be8fa6e6ebbcafe24e31f1ec152353b10e`. Its resolved-manifest SHA-256 is
`892cbd5416f8827a8c363b63b97cde8e7365687162996eb9961b61db597c6cd4`.
The provider-exposed model identifier is `gpt-5.4` with medium reasoning; this
identifies the requested configuration but does not independently establish an
immutable backend. The image ID is
`sha256:0320a60c5b2628cebeb2c897bbf80da949f3b9bb99fa61f5a3475c7276328756`.
The verified read-only image archive has SHA-256
`55ee85f0656cef429d1cd40edced79782d54abb7b2180c9770c14bea06828ddf`.

Raw v2 data are archived outside Git at
`X:\backup20260827\Archives\SourceRepos\agentic-language-fitness-raw-runs\variance-v2`,
with its checksum manifest at the sibling path
`variance-v2.sha256-manifest.json`:
2,482 files and 81,421,371 bytes, tree SHA-256
`98401e2a3a9bc4615486760d68912fee22842d2259400a52c2c32c76012fd25e`, and
manifest-file SHA-256
`45e9308667572f35def4f2e4c0a9c5c93a8dcd6b223870870d77c41dc9cbc8e3`.
Source and destination match exactly; the archive is read-only.

## Observations

The non-counting calibration had two language runs, one C# and one F#, and each
run passed both tasks, with exactly one usage record per task, fresh
conversations, and the intended inherited chain. The formal cell contains
10/10 paired blocks, balanced five
per first-language order, with 20/20 primary attempts and 40/40 task records.
C# completed 10/10 chains and 20/20 tasks. F# completed 9/10 chains and 19/20
tasks because one retained primary had a behavioral ordering failure. One
pre-candidate authentication-preflight timeout is retained as a retryable,
infrastructure-invalid attempt and excluded; its sequential retry is the
primary for that slot. Thus 22/23 raw audits pass, with only that expected
excluded attempt failing the full audit.

The paired mean input-token difference (F# − C#) is 4,580.3 tokens (SD
92,533.223). Input includes cached input as a reported component, not an
additional quantity. The order means are +41,252.8 tokens with F# first and
−32,092.2 with F# second. Analytic power calculations require approximately
233 pairs for a 7% effect and 180 pairs for an 8% effect under the observed
variance assumptions.

Correctness is near-saturated at 39/40 tasks. At n=10, stochastic and order
variance overwhelm plausible 7–8% effects. These observations support no
causal, significance, or language-advantage claim.

## Curated reports and next action

The reproducible machine-readable report is
`reports/variance-v2/report.json` (self-hash
`0c158dd47f9cc82e6e89b9fc77f3dec550af8048484da87953b9c9c200497ede`), with
the rendered Markdown report beside it. The calibration audit is
`reports/variance-v2/calibration-audit.json` (self-hash
`25e74c0cdaf542b67f2469565e3cccac1c2590af4bf8d58508388ee921ead6ae`).

The variance gate is met and Workstream B is complete. Because correctness is
near-saturated, the next step is Workstream C: design and independently review
a matched cumulative 5–10-task chain containing additive change, a
cross-cutting schema change, bug diagnosis, behavior-preserving refactor, and
an API/backward-compatibility constraint, plus a within-language
representation treatment. Implement and validate the benchmark changes after
design review and green CI, then define and freeze a new protocol cell; do not
launch another paid/model run before then.

The historical exploratory pair and retired variance-v1 attempt remain
excluded from all formal aggregates and power calculations.
