# Trusted maintenance-simulation cases

`cases.json` contains 80 hand-derived model-free construction cases.
Each case is an independent request/response oracle with an introduced episode,
an optional inclusive `through` supersession bound, and visibility. The seed's
two public inputs are literal `contract.md` examples; later public-roundtrip
variants preserve that input while representing the episode 04, 05, and 06+
snapshot output shapes. Evaluation cases are not candidate context. No seed or
successor implementation, gold patch, model output, research result, or provider
observation was used to derive expected values.

Coverage is deliberately cross-feature: seed validation and sorting; deferred
ordering, cancellation, same-batch errors, and outer rollback; simultaneous
followers and chains; v1 migration and complete canonical v2 state; policy
ordering; request/issued ledgers; bounded fast-forward; and replay commit,
rollback, registry isolation, and nested-replay rejection.

The final ten evaluation-only cases strengthen the import and persistence
boundary without exposing new examples to candidates. They cover atomic
rejection of malformed, past-due, duplicate-order, and unknown-command pending
entries; successful load of `Int64.MaxValue` queue order, overflow on the next
enqueue, and reset to order zero after draining; nonempty policy registry and
assignment import, clamp behavior, and save/load restoration; missing,
duplicate, and unknown policy references; pending-request and issued-ledger
restoration plus inconsistent-ledger rejection; and follower direction at
opposite signed-64-bit extremes without subtraction overflow. Snapshot-bearing
episode-04 and episode-05 witnesses have explicit `through` bounds, with
episode-06+ variants carrying the cumulative fields through episode 08.
Two further evaluation witnesses preserve inherited cleanup semantics: a due
remove cancels a later queued remove for the same ID, and target removal
permanently nulls a follower target even when that ID is subsequently reused.
Ten evaluation-only validation witnesses cover the clarified nested-command
boundary: episode-sensitive operation-name recognition, immediate shape checks
before rejecting recognized-but-unsupported commands, no nested semantic or
world lookup, non-null follower spawn targets, and atomic v2 entity import
classification for unknown kinds, malformed/self/missing targets, and extra
mover fields.

Episode 07's clarified arithmetic rule is represented by a paired witness:
starting at `-9223372036854775807` with velocity `9223372036854775807`, both
two ordinary ticks and `fast_forward:2` finish at tick 2 and position
`9223372036854775807`. The fast-forward oracle therefore permits an exact wider
product intermediate and checks only the final signed-64-bit position, matching
the now-explicit contract while retaining the distinct operation effect.

## Initial oracle defects corrected in this audit

The initial 36 cases incorrectly extended the seed snapshot example through
episodes that changed its wire shape; emitted `kind` on live movers; rejected a
valid third enqueue; treated a duplicate follower ID as `invalid_value`; emitted
a remove for an absent same-batch entity; duplicated a tick effect; used an
invalid spawn to try to reach Int64 overflow; omitted a successful replay effect;
and omitted later v2 `policies`, `requests`, and `issued` fields. Several replay
and overflow snapshots also used obsolete shapes. The corrected cases retain
errors and rollback evidence rather than aligning them to either implementation.

The fixture rule is cumulative: absent `through` means episode 8. Explicit
`through` appears only where a later episode changes the expected snapshot wire
shape; paired episode-5 and episode-6+ variants preserve the same behavioral
request and assertions under the superseding schema.

## Public examples

The literal JSON I/O below has been copied into the corresponding episode
documents. Matching fixture inputs and their later schema variants are marked
`public`, never misrepresented as hidden evaluation cases. The summaries below
explain the examples; they add no execution approval.

1. Episode 01: `{"version":1,"operations":[{"op":"enqueue","at":1,"sequence":0,"command":{"op":"spawn","id":"a","x":0,"velocity":0}},{"op":"tick","count":1}]}` -> state tick 1 with mover `a`; effects are `enqueue:1:0`, `spawn:a`, `tick:1`; no errors.
2. Episode 02: spawn `a`, enqueue two removes for tick 1, then tick -> empty state; the first remove emits `remove:a`, the already extracted second remove emits `missing_entity`, and the outer `tick:1` effect is last.
3. Episode 03: mover `a` at 0 velocity 1, follower `b` at 3 targeting `a`, then tick -> `a.x=1`, `b.x=2`; effects are `spawn:a`, `spawn:b`, `tick:1`.
4. Episode 04: import legacy `{"tick":3,"entities":[{"id":"a","x":5,"velocity":2}]}` as `old`, then load it -> live tick 3 and mover `a`; snapshot `old` is rendered as v2 with mover kind and empty pending.
5. Episode 05: mover `a` at 9 velocity 3, register `cap`/`clamp10`, assign it, then tick -> `a.x=10` with policy `cap`; effects end in `tick:1`.
6. Episode 06: spawn `a`, request sequence 1, cancel it, then complete sequence 1 -> `stale_completion`; request and cancel effects remain and the issued ledger retains sequence 1.
7. Episode 07: mover `a` at 2 velocity 3, then fast-forward 1,000,000,000 -> tick 1,000,000,000 and `a.x=3000000002`, with one `fast_forward:1000000000` effect.
8. Episode 08: save `s`, then successfully replay a two-tick event list -> the replayed world commits and emits `replay:s`; the saved snapshot registry entry `s` remains unchanged.

## Literal JSON I/O included in the episode documents

1. Episode 01 input: `{"version":1,"operations":[{"op":"enqueue","at":2,"sequence":9,"command":{"op":"spawn","id":"z","x":0,"velocity":0}},{"op":"enqueue","at":1,"sequence":4,"command":{"op":"spawn","id":"b","x":0,"velocity":0}},{"op":"enqueue","at":1,"sequence":2,"command":{"op":"spawn","id":"a","x":0,"velocity":0}},{"op":"tick","count":2}]}`
   Output: `{"version":1,"state":{"tick":2,"entities":[{"id":"a","x":0,"velocity":0},{"id":"b","x":0,"velocity":0},{"id":"z","x":0,"velocity":0}]},"effects":["enqueue:2:9","enqueue:1:4","enqueue:1:2","spawn:a","spawn:b","spawn:z","tick:2"],"errors":[],"snapshots":[]}`

2. Episode 02 input: `{"version":1,"operations":[{"op":"spawn","id":"a","x":0,"velocity":0},{"op":"enqueue","at":1,"sequence":1,"command":{"op":"remove","id":"a"}},{"op":"enqueue","at":1,"sequence":2,"command":{"op":"remove","id":"a"}},{"op":"tick","count":1}]}`
   Output: `{"version":1,"state":{"tick":1,"entities":[]},"effects":["spawn:a","enqueue:1:1","enqueue:1:2","remove:a","tick:1"],"errors":["missing_entity"],"snapshots":[]}`

3. Episode 03 input: `{"version":1,"operations":[{"op":"spawn","id":"a","x":0,"velocity":1},{"op":"spawn_follower","id":"b","target":"a","x":3},{"op":"tick","count":1}]}`
   Output: `{"version":1,"state":{"tick":1,"entities":[{"id":"a","x":1,"velocity":1},{"kind":"follower","id":"b","x":2,"velocity":0,"target":"a"}]},"effects":["spawn:a","spawn:b","tick:1"],"errors":[],"snapshots":[]}`

4. Episode 04 input: `{"version":1,"operations":[{"op":"import_snapshot","name":"old","data":{"tick":3,"entities":[{"id":"a","x":5,"velocity":2}]}},{"op":"load","name":"old"}]}`
   Output: `{"version":1,"state":{"tick":3,"entities":[{"id":"a","x":5,"velocity":2}]},"effects":["import:old","load:old"],"errors":[],"snapshots":[{"name":"old","data":{"version":2,"tick":3,"entities":[{"kind":"mover","id":"a","x":5,"velocity":2}],"pending":[]}}]}`

5. Episode 05 input: `{"version":1,"operations":[{"op":"spawn","id":"a","x":9,"velocity":3},{"op":"register_policy","name":"cap","kind":"clamp10"},{"op":"assign_policy","id":"a","name":"cap"},{"op":"tick","count":1}]}`
   Output: `{"version":1,"state":{"tick":1,"entities":[{"id":"a","x":10,"velocity":3,"policy":"cap"}]},"effects":["spawn:a","register:cap","policy:a:cap","tick:1"],"errors":[],"snapshots":[]}`

6. Episode 06 input: `{"version":1,"operations":[{"op":"spawn","id":"a","x":0,"velocity":0},{"op":"request","id":"a","sequence":1},{"op":"cancel","id":"a","sequence":1},{"op":"complete","id":"a","sequence":1,"value":7}]}`
   Output: `{"version":1,"state":{"tick":0,"entities":[{"id":"a","x":0,"velocity":0}]},"effects":["spawn:a","request:a:1","cancel:a"],"errors":["stale_completion"],"snapshots":[]}`

7. Episode 07 input: `{"version":1,"operations":[{"op":"spawn","id":"a","x":2,"velocity":3},{"op":"fast_forward","count":1000000000}]}`
   Output: `{"version":1,"state":{"tick":1000000000,"entities":[{"id":"a","x":3000000002,"velocity":3}]},"effects":["spawn:a","fast_forward:1000000000"],"errors":[],"snapshots":[]}`

8. Episode 08 input: `{"version":1,"operations":[{"op":"spawn","id":"a","x":0,"velocity":1},{"op":"save","name":"s"},{"op":"replay","snapshot":"s","events":[{"op":"tick","count":2}]}]}`
   Output: `{"version":1,"state":{"tick":2,"entities":[{"id":"a","x":2,"velocity":1}]},"effects":["spawn:a","save:s","replay:s"],"errors":[],"snapshots":[{"name":"s","data":{"version":2,"tick":0,"entities":[{"kind":"mover","id":"a","x":0,"velocity":1}],"pending":[],"policies":[],"requests":[],"issued":[]}}]}`
