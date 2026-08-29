# A3 accounting reconciliation (2026-08-29)

This note records the checked-in fixture made from the recovered 2026-08-26
F# command run. The fixture is explicitly `derived-redacted-not-accepted-observation`;
it is a parser/audit regression fixture, not a study observation and is excluded
from all aggregates, variance estimates, and power calculations.

## Reconciled evidence

The fixture now contains both recovered F# tasks. Task `001-priority` has 35
JSONL records, 12 completed commands, one file change, and one usage record;
task `002-overdue` has 17 records, four completed commands, one file change, and
one usage record. The exact full-run aggregate copied into the fixture is:

| input | cached input | cache write | output | reasoning | tool calls |
|---:|---:|---:|---:|---:|---:|
| 317078 | 276480 | 0 | 5963 | 2251 | 18 |

The redacted `agent.stdout` and `events.jsonl` preserve event order, event/item
types, completion counts, and the usage record. Prompts, paths, free text, IDs,
commands, and outputs are replaced with `[REDACTED]`. `usage.json`, the embedded
task result, and run aggregate all agree; `python -m alf audit tests/fixtures/a3-redacted-run`
therefore succeeds.

Task `001-priority` took 186.280462 seconds; task `002-overdue` started at
`2026-08-26T08:07:07.799629+00:00` and finished at
`2026-08-26T08:08:57.809324+00:00`, giving the checked-in 110.009695-second
task/run total for that task. The full run timestamp delta is 297.617385 seconds;
its traceable agent-process total is 272.4700000000048 seconds and task-evaluator
total is 23.327000000001136 seconds. The evaluator split intentionally excludes
baseline evaluation because the legacy timestamp boundary does not establish that
split. These timings are derived observations, not synthetic envelope values.

The source SHA-256 values and expected audit result are recorded in
`tests/fixtures/a3-redacted-run/provenance.json`. In the source evidence, raw
stdout for each task carries the usage record, the final workspace `.alf/usage.json`
for each task carries the same numeric usage, and each embedded task result carries
the same usage. The original task `events.jsonl` files are empty (their hashes are
recorded), which is one reason the unredacted legacy run does not pass the current
audit. The current-schema envelopes and redacted event copies are derived from
those authentic event shapes/numbers; they do not reconstruct missing events.

Cached-token semantics are not inferred from this run: the official usage
definition states that input tokens include cached and cache-write tokens, making
cached input a subset/breakdown rather than an additive quantity ([OpenAI usage
reference](https://developers.openai.com/api/reference/resources/admin/subresources/organization/subresources/usage)).

The original legacy run remains unaudited: its copied `events.jsonl` files are
empty while stdout contains events, and its task results predate the current
accounting fields. The fixture does not repair or overwrite those artifacts.

## Accounting conclusions and limits

Each recovered task contains one usage record, so the evidence itself does not
distinguish incremental from cumulative behavior across multiple terminal
records. The pinned Codex 0.149.1 event schema describes the counters as usage
for a turn, while its JSONL implementation constructs the terminal event from
`ThreadTokenUsage.total` ([pinned event schema](https://github.com/openai/codex/blob/rust-v0.149.1/codex-rs/exec/src/exec_events.rs),
[pinned JSONL implementation](https://github.com/openai/codex/blob/rust-v0.149.1/codex-rs/exec/src/event_processor_with_jsonl_output.rs)).
Because the protocol launches one ephemeral prompt/turn, `variance-v1` requires
exactly one derived `turn.completed` usage record. Zero or multiple records make
that attempt's accounting invalid rather than inviting an unverified summation
rule. The generic parser continues to expose and sum multiple valid records for
legacy diagnostics, but such a stream cannot enter accepted protocol token
aggregates.

The parser is deliberately conservative: it counts file reads only for the
documented simple `cat`, `head`, `tail`, `less`, `more`, `rg`, and `sed` command
grammar, and rejects shell operators. Because all commands are redacted in the
checked-in fixture, its file-read counts are zero; this is not a claim that the
original agent performed no reads. The four command and one file change counts
remain observable from their item types.

Malformed, missing, negative, and duplicated usage records remain invalid under
`parse_codex_jsonl`; existing audit tests cover missing/malformed sidecars and
contradictory accounting. Calibration must retain every `turn.completed` record;
if the pinned one-turn invocation emits anything other than exactly one, its
token accounting is unavailable and the protocol must be reviewed before formal
collection.
