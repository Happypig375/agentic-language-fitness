# Expanded public operation contract

This file adds only `reconcile` and `dependencyOrder` to the existing
line-delimited JSON protocol. Existing dispatch remains unchanged: operation
matching is case-insensitive, and the existing deserializer and null/missing
operation behavior and errors remain authoritative. A JSON `null` request still
returns exactly `{"error":"Request was null"}`. These rules apply only after
an existing dispatcher recognizes one of the two new operation names.

JSON property names for the new operation payloads are matched
case-insensitively, consistent with the existing adapter. Unknown properties
are ignored. Duplicate JSON property names and unpaired UTF-16 surrogates are
outside this contract's input domain. Requests remain stateless and use only
the standard library.

## Shared values

An ID is any JSON string, including the empty string, containing valid Unicode
scalars. IDs are never trimmed or normalized. Equality and ordering are
ordinal and case-sensitive by UTF-16 code units (the runtime ordinal string
comparison), including supplementary characters. `true`/`false` are not
numbers. An accepted integer is a JSON number whose lexical form is
`-?(0|[1-9][0-9]*)`, has value in `[-2147483648,2147483647]`, and is not a
fraction or exponent form.

`createdAt` is an ISO-8601 subset: year 0001 through 9999, real calendar date
and time, uppercase `T`, seconds, no leap seconds or `24:00`, one to seven
fraction digits when present, and either uppercase `Z` or a signed `HH:MM`
offset from -14:00 through +14:00. The resulting instant must fit the
`DateTimeOffset` range. Other spellings, lowercase separators, missing offsets,
and invalid dates are invalid.

## `reconcile`

Request: `{"operation":"reconcile","left":[...],"right":[...]}`.
Missing or JSON-null `left`/`right` means an empty side; any other non-array
side returns `{"error":"<side> must be an array"}`. Validation is strictly:

1. Validate every left element in order. A null/non-object element returns
   `invalid left record`; then missing/wrong-type `id`, `priority`, or
   `createdAt` returns respectively `invalid left id`, `invalid left priority`,
   or `invalid left createdAt`.
2. Apply the same rules to every right element with `right` in the message.
3. Duplicate IDs within left return `duplicate left id`; duplicates within
   right return `duplicate right id`.

Each valid record has `id`, signed Int32 `priority`, and valid `createdAt`.
For an ID present on one side, retain that record. For an ID on both sides,
choose higher priority, then later instant, then the right record on an exact
tie. Return `{"items":[{"id":"...","origin":"left"|"right"}]}` with IDs
ordinal-ascending. Empty sides may therefore yield `{"items":[]}`.

## `dependencyOrder`

Request: `{"operation":"dependencyOrder","ids":[...],"edges":[...]}`.
Missing or JSON-null `ids` means empty IDs; a non-array or any non-string element
in an array returns `{"error":"invalid ids"}`. Duplicate IDs return
`{"error":"duplicate id"}`. Missing or JSON-null `edges` means no edges; a
non-array returns `{"error":"invalid edges"}`. A null/non-object edge or an
edge with missing/non-string `before` or `after` returns `{"error":"invalid
edge"}`. Duplicate directed edges return `{"error":"duplicate edge"}`.
Unknown endpoints return `{"error":"unknown dependency"}`; this precedes the
self-edge check, which returns `{"error":"self dependency"}`. A remaining
cycle returns `{"error":"dependency cycle"}`. This is the complete precedence:
IDs, duplicate IDs, edges, edge shape, duplicate edges, unknown endpoints,
self-edges, cycles.

With valid input, repeatedly select the ready ID with smallest ordinal UTF-16
value, remove its outgoing edges, and return `{"ids":[...]}`. Empty IDs with
nonempty edges consequently produce `unknown dependency`; both empty produce
`{"ids":[]}`. A cycle returns no partial order.
