# Maintenance simulation: seed contract v1

This is the complete public, language-neutral JSON-lines contract for a small
headless deterministic kernel. A request is one UTF-8 JSON object on one line;
one response is one JSON object on one line. Requests start independent state.
No network, clock, randomness, graphics, floating point, or external package
is permitted.

## Wire shape and domain

The request is `{"version":1,"operations":[...]}` and `version` is exactly 1.
Each operation is an object with an `op` string and only its specified fields.
Integers are signed 64-bit. Spawn `x` and `velocity` are each in
`[-1000000,1000000]`; tick `count` is 1..1000; operations has at most 256
items. IDs and snapshot names are ordinal strings matching
`[a-z][a-z0-9_-]{0,31}`. IDs are strings, not numbers. Arithmetic overflow is
an error and never wraps.

Allowed operations are `spawn` (`id`,`x`,`velocity`), `remove` (`id`), `tick`
(`count`), `save` (`name`), and `load` (`name`). Spawn creates a mover and
tick applies its velocity once per internal tick. Remove requires an existing
mover. Save overwrites an existing name with a deep snapshot. Load replaces
the live tick/entities with that snapshot; it does not erase prior effects,
errors, or snapshots.

The top-level keys must be exactly `version` and `operations`; malformed JSON,
a non-object request, wrong top-level fields/types/version or more than 256
operations produces a fresh empty response with one `invalid_shape` error.
An empty operations array is valid. Each nonblank input line gets one response;
blank lines are ignored. Duplicate JSON keys are outside the input domain.

Within a valid request, validate each operation separately. A missing/non-string
`op`, non-object operation, missing/wrong field types or extra operation fields
is an atomic `invalid_shape` operation error, NOT a reset of the whole request.
An unrecognized string `op` is `unknown_operation` before other field checks.
JSON booleans are not numbers. Numeric fields must be JSON integer literals
(no decimal point or exponent); non-integer or out-of-range numeric values and
ID-regex violations produce `invalid_value`. Validate shape, then values, then
state-dependent preconditions. Duplicate spawn IDs produce `duplicate_id`.
Removing an absent ID produces `missing_entity`; loading an absent name produces
`missing_snapshot`. Other
errors are `duplicate_id`, `missing_entity`, `missing_snapshot`, `overflow`,
and `snapshot_version`. Semantic errors are atomic per operation: state, tick,
snapshots, effects, and errors before that operation are unchanged. Processing
continues with later operations. A malformed whole request has only its one
`invalid_shape` error.

The response is
`{"version":1,"state":{"tick":n,"entities":[...]},"effects":[string,...],"errors":[string,...],"snapshots":[{"name":string,"tick":n,"entities":[...]}]}`.
Entities and snapshots are sorted by ordinal ID/name. An entity is
`{"id":string,"x":integer,"velocity":integer}`. Effects preserve occurrence
order and are `spawn:<id>`, `remove:<id>`, `tick:<count>`, `save:<name>`, or
`load:<name>`. A successful tick emits one effect for the operation, not one
per internal step. A failed operation emits no effect. Checked signed-64-bit
addition is required at every internal tick, including the tick counter. Output
positions may exceed the spawn input bounds but must remain signed 64-bit.
The initial state is tick zero, no entities and no saved snapshots. Semantic
error rollback preserves all earlier operation effects/errors, then appends the
current error code exactly once. Tick overflow rolls back the whole count.

## Public examples

Input: `{"version":1,"operations":[{"op":"spawn","id":"a","x":2,"velocity":3},{"op":"tick","count":2},{"op":"save","name":"s"},{"op":"remove","id":"a"},{"op":"load","name":"s"}]}`

Output: `{"version":1,"state":{"tick":2,"entities":[{"id":"a","x":8,"velocity":3}]},"effects":["spawn:a","tick:2","save:s","remove:a","load:s"],"errors":[],"snapshots":[{"name":"s","tick":2,"entities":[{"id":"a","x":8,"velocity":3}]}]}`

Input: `{"version":1,"operations":[{"op":"remove","id":"z"},{"op":"tick","count":0},{"op":"spawn","id":"b","x":0,"velocity":1},{"op":"spawn","id":"b","x":4,"velocity":1}]}`

Output: `{"version":1,"state":{"tick":0,"entities":[{"id":"b","x":0,"velocity":1}]},"effects":["spawn:b"],"errors":["missing_entity","invalid_value","duplicate_id"],"snapshots":[]}`
