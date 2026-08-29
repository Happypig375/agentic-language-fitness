# Workstream C benchmark design

Status: C2 implementation and model-free validation complete and independently
approved, including the material legacy-behavior clarification below. No paid
or model-backed run is authorized by this document; C3 is the next gate.

## C2 implementation acceptance and evidence

The successor is a cumulative eight-task chain with 90 final black-box cases
per language. It preserves the pilot baseline and Tasks 001/002 exactly,
supports legacy and multi-file gold manifests, cumulative workspace checks, and
fail-closed cross-platform path validation. Evidence includes 126 unit tests,
strict doctor, legacy/successor validation and scripted matrices, serialized
Task 007/008 checks, focused path suites (Windows 25; Linux 24 plus one
expected junction skip), and 18 isolated gold builds. Independent harness
security and gold/equivalence reviews approve with no P1/P2 findings; the
amendment review is also approved.

## Scope and invariants

The successor benchmark is one cumulative eight-task `OrderFlow` chain. Tasks
`001-priority` and `002-overdue` are retained byte-for-byte (task text, cases,
gold, and historical cells are unchanged). Tasks 003–008 below are additive
or cross-cutting changes. The F# and C# task text, ordered changes, evaluator,
resource limits, and agent protocol are identical. Gold implementations and
hidden evaluator cases remain external to candidate workspaces; only the public
line-oriented JSON contract is exposed. Use the .NET standard library, ordinal
IDs, and `DateTimeOffset` instants. Every old request and response shape must
remain valid. The runner must support an arbitrary cumulative chain, not a
hard-coded two-task schedule.

Each task is specified by purpose/category, exact contract, adversarial cases,
gold expectation, dependency, and fairness risks. Case matrices are cumulative:
all earlier cases continue to run after every later task.

## Material legacy-behavior clarification (C2 review amendment)

The retained pilot C# and F# golds expose language-specific `ArgumentException`
diagnostics (including parameter-name casing and suffixes), making exact
language-neutral error cases impossible to match. Stable explicit strings are
scientifically preferable and symmetric. Accordingly, the successor contract
is amended as follows:

- By Task 003, an unknown operation returns exactly `Unknown operation:
  <operation>`, with no language/runtime parameter-name suffix. The
  candidate-visible Task 003 text states this requirement, and the oracle tests
  the exact serialized error.
- By Task 005, missing or null `asOf` for `overdue` returns exactly `asOf is
  required for overdue`; `atRisk` retains its already exact `asOf is required
  for atRisk` string. Candidate-visible acceptance text states both
  requirements, and precedence tests cover them.

This is a material legacy-behavior clarification, not a retrospective change
to the retained pilot. The limited independent review is approved with no
P1/P2 findings: retained C#/F# Task 002 `ArgumentException` parameter casing
differs, while the candidate-visible suffix-free exact strings are symmetric.
Task 001/002 remain unchanged. The language-equivalence/error review gate is
closed; C2 implementation and model-free validation may continue, while the
representation treatment, protocol freeze, and paid/model runs remain blocked.

## Task 003 — at-risk window

**Purpose/category.** Additive query and boundary/temporal reasoning.

**Contract.** Add operation `atRisk`. It requires `asOf`; missing or null
`asOf` returns the stable error `asOf is required for atRisk`. `asOf` and
`dueAt` are parsed as `DateTimeOffset` instants, compared by instant rather than
offset spelling. Select only orders whose status is `pending` or `processing`
(case-insensitive), and whose dated `dueAt` is in the half-open interval
`[asOf, asOf + 24 hours)`. Undated orders and all other statuses are excluded.
Return exactly `{ "ids": [<matching order ids>] }`, as the existing query
operations do; do not echo order fields. Sort by `dueAt` ascending, then
priority descending (missing priority is 0),
then `id` ascending using ordinal comparison. Existing operations are unchanged.

Matched cases use syntactically valid, representable `DateTimeOffset` strings
for which the derived 24-hour upper bound is also representable, plus the
explicitly defined missing/null behavior; invalid or
out-of-range strings are excluded because serializer diagnostics are not a
matched cross-language contract.

**Cumulative/adversarial matrix.** Retain every 001/002 case; add a dueAt
exactly at `asOf` (included), exactly at `asOf+24h` (excluded), one instant just
inside/outside each boundary, offsets representing the same instant, missing or
null dueAt, pending/processing with mixed case, completed/cancelled/unknown
statuses, missing/negative/equal priorities, and ordinal IDs that differ only
by case. Include missing/null asOf and a request with an unknown operation.

**Gold/dependency/fairness.** Both golds add the operation through the same
observable protocol and standard-library parsing; no culture-local clock or
local-time conversion is permitted. This depends on the 002 order model and
ordering helpers. Risks are offset/time-zone assumptions, unstable sort
tie-breaks, and an F# or C# convenience API changing null semantics; the oracle
must compare parsed JSON, not source shape.

## Task 004 — VIP-ready eligibility

**Purpose/category.** Additive nested-schema change and backward compatibility.

**Contract.** Add optional nested `customer` with optional `id` and `tier`.
Add operation `vipReady`: apply the existing `ready` eligibility, then require
`customer` and `customer.tier` to be present and equal to `gold` or `platinum`
(case-insensitive). Missing/null customer or tier is excluded. Use the existing
ready ordering (priority descending, then creation time ascending, then ordinal
ID), and return exactly `{ "ids": [...] }`; customer is an input-only filter
and is not echoed. All old payloads and operations remain valid.

**Matrix.** Retain all earlier cases; add gold/platinum mixed-case tiers,
silver/unknown/empty tiers, missing/null customer, missing/null tier, ready and
non-ready statuses, absent customer on old payloads, nested extra fields, and
ordering ties. Verify `ready` still returns non-VIP orders and that 001/002
responses are byte/schema compatible after the model extension.

**Gold/dependency/fairness.** Golds add the same optional fields and operation;
standard-library JSON is sufficient. This depends on 001 ready ordering and
003's stable model conventions. Risks include treating customer presence as
eligibility, case-sensitive tiers, and language-specific optional-record
defaults. Hidden cases must exercise null, omission, and unknown properties.

## Task 005 — null-order robustness

**Purpose/category.** Production bug diagnosis and cross-operation robustness.

**Contract.** For every currently recognized operation (`ready`, `overdue`,
`atRisk`, and `vipReady`), missing `orders` or `orders: null` means an empty
order collection; null elements within an orders array are ignored. Required
operation fields remain required and validated: `asOf` for `overdue`/`atRisk`.
Task 006 must inherit this normalization for `transition` while retaining its
own required `id`/`toStatus` validation. Do not turn missing required fields
into empty results. This is a real gold behavior change, and must not contradict
any earlier non-null cases.

The candidate-visible prompt is a symptom/reproduction report: omitted or null
orders, and null elements in an orders array, cause failures or inconsistent
responses across existing operations; fix the defect while preserving valid
behavior and required-field errors. It must not disclose where normalization is
implemented or the suspected cause. The private gold/evaluator contract may
specify the empty-collection and ignore-null normalization and exact precedence
above.

**Matrix.** For each operation (`ready`, `overdue`, `atRisk`, and `vipReady`),
test omitted orders, null orders, arrays containing null before/between/after
valid orders, all-null arrays, and the same requests with required fields
missing/null. Malformed JSON field types are outside this task's oracle because
serializer diagnostics are not a matched cross-language contract. Retain all previous cases and prove valid orders are
unaffected. Task 006 adds transition-specific cases while inheriting this
normalization; those cases are deliberately not attributed to Task 005.

**Gold/dependency/fairness.** Both golds implement the same input normalization
at the request boundary, while preserving validation order and exact errors.
This depends on the complete 001–004 model. Risks are one language throwing on
null array elements, silently accepting absent required fields, or accidentally
changing error precedence; cross-operation cases are mandatory.

## Task 006 — stateless transition

**Purpose/category.** Stateful-looking API constraint with explicit validation.

**Contract.** Add stateless operation `transition` with request `id` and
`toStatus`. Empty strings, as well as missing or null values, are missing. Apply
validation in exactly this precedence: (1) missing `id` → `id is required for
transition`; (2) missing `toStatus` → `toStatus is required for transition`;
(3) normalize orders as in 005, then find an ordinal, case-sensitive ID match:
zero matches → `order not found for transition`, more than one → `duplicate
order id for transition`; (4) check the case-insensitive status transition,
allowing only pending→processing/cancelled and processing→completed/cancelled;
failure → `invalid transition`. IDs match using ordinal, case-sensitive
comparison. The response is exactly `{ "id": <matched id>, "status":
<canonical lowercase target> }`. There is no cross-line or cross-request
mutation. Malformed non-string field types are outside the matched task
contract and evaluator cases. All prior response shapes are unchanged.

**Matrix.** Retain all prior cases; add each allowed transition with mixed-case
source/target, every disallowed source/target pair, missing/null/empty fields,
ID case mismatch, duplicate IDs, no match, null elements, missing/null orders,
two lines proving no mutation, and a subsequent query proving the original
status remains. Include duplicate IDs differing only by case (not duplicates
under ordinal comparison).

**Gold/dependency/fairness.** Both golds perform one request-local lookup and
emit only the two response keys. This depends on 005 normalization and the
status model. Risks are accidental statefulness, Unicode/culture comparison,
returning the whole order, and inconsistent validation/error precedence.

## Task 007 — behavior-preserving engine refactor

**Purpose/category.** Architecture/refactor with an automated minimum workspace
contract and a separate blinded compliance review.

**Contract.** Move domain/model/handler logic out of `Program` into
`OrderFlowEngine.cs` or `OrderFlowEngine.fs`. `Program` remains the line-I/O
and error adapter. Behavior and every earlier response/error must be preserved.
The evaluator must check black-box cumulative behavior *and* the workspace
contract: the engine file exists, builds, and operation string literals are not
in `Program`. Do not impose line-count or equal-LOC constraints.

The harness must add backward-compatible manifest support for per-task,
multi-file gold snapshots. For each language, `gold[language]` is the JSON
union of a legacy string path or `{ "files": [{ "source": <relative path>,
"target": <relative workspace path> }, ...] }`. Paths must be relative,
confined beneath their declared benchmark/workspace roots, and targets must be
unique; an empty file list is invalid. Define
`workspace_checks[language]` as `{ "file_exists": [<relative path>, ...],
"text_contains": [{ "path": <relative path>, "text": <string> }, ...],
"text_not_contains": [{ "path": <relative path>, "text": <string> }, ...] }`.
For this task require C# `OrderFlowEngine.cs` containing `public static class
OrderFlowEngine` and `Program.cs` containing `OrderFlowEngine.Handle`; use
`OrderFlowEngine.fs`, `module OrderFlowEngine`, and `OrderFlowEngine.handle` for
F#. Add language-specific `text_not_contains` entries for model/handler
declarations left in Program: C# forbids `class Order`, `class Customer`,
`class Request`, `record Response`, and ` Handle(`; F# forbids `type Order`,
`type Customer`, `type Request`, `type Response`, and `let handle`. Both also
forbid every quoted operation literal known through Task 007 (`"ready"`,
`"overdue"`, `"atRisk"`, `"vipReady"`, and `"transition"`, but not
`"summary"`). Checks are
cumulative from Task 007 onward, serialized in evaluation results, and
conjunct with build and black-box success. The scripted runner and `alf
validate` must share one copy/check helper so their results cannot drift. The
task is successful only when black-box equivalence plus this workspace contract
pass; black-box output alone is insufficient. These textual checks establish
only the declared minimum modularization evidence, not control/data flow or the
absence of dead delegation. They must not be described as proof of full
architectural extraction.

**Matrix.** Run every prior case, including all null/error/transition cases,
against both the refactored workspace and the gold. Add source-layout checks,
clean build checks, and operation-literal scans. Negative fixtures prove
rejection when the engine is missing or unreferenced, or when the enumerated
model/handler declarations or operation literals remain in `Program`. Verify
multi-file snapshots and old single-file manifest loading.

**Gold/dependency/fairness.** Golds use idiomatic language-specific modules,
the multi-file manifest form, equivalent public behavior, and the same required
engine filename (with the language extension). This depends on the complete API
and harness support. Risks are overfitting to file counts, penalizing idiomatic
syntax, or letting a superficial/dead delegation pass. Automated checks stay
narrow and explicit. Before release, both golds must pass independent
architecture and leakage review. For every Task 007 primary in a difficulty or
later pilot, two reviewers blinded to language-treatment conclusions separately
record `refactor_compliance`: whether `Program` is only the line-I/O/error
adapter and the engine owns the model and live dispatch. Preserve agreement,
disagreements, and adjudication as a separate outcome; never silently equate
automated task success with full refactor compliance.

**Path-safety contract.** The repository root is the checkout root and the
benchmark root is the manifest's parent. Legacy gold strings remain
repository-relative for compatibility, but must resolve (after real/final-path
resolution) to existing regular files beneath the benchmark root. Multi-file
`source` entries are also repository-relative and must meet the same benchmark-
root rule. Targets and all check paths are workspace-relative and must resolve
beneath the workspace. All such paths normalize both separators; reject
absolute, drive-qualified, UNC, empty, dot, or dot-dot segments. Reject
symlink/reparse/junction escapes (including components in mutable workspace
paths), case-folded normalized duplicate targets on every OS, and top-level
`.git`, `.alf`, `bin`, or `obj` destinations. Validate the entire copy/check
plan fail-closed before any copy or check. Tests must cover mixed separators,
traversal, Windows case aliases, supported symlink/junction escapes, metadata
paths, duplicates, and legacy strings.

The mandatory independent architecture review remains in force. Negative
fixtures cover exactly the violations detectable by the declared workspace
schema. A structurally passing dead-delegation fixture must instead demonstrate
the documented limit and exercise the separate `refactor_compliance` review.

## Task 008 — summary API

**Purpose/category.** Additive API and aggregate/backward-compatibility
constraint.

**Contract.** Add `summary`. Return exactly an object with keys `pending`,
`processing`, `completed`, `cancelled`, and `overdue`, whose values are
integers. Count statuses case-insensitively; unknown statuses are ignored. If
`asOf` is supplied and valid, set `overdue`
equal to the number of pending/processing orders with `dueAt < asOf` (strictly
less than, by instant); if asOf is absent, return `overdue: 0`. The overdue
count overlaps the status counts and is not subtracted from them. Missing/null
orders and null elements follow 005; a null `asOf` is treated as absent.
Matched cases use syntactically valid, representable `DateTimeOffset` strings
only, plus the defined missing/null behavior; invalid or out-of-range strings
are excluded because serializer diagnostics are not a matched cross-language
contract.
Preserve every earlier operation and schema; define the exact object key set in
the successor manifest and compare parsed values, with no extra status buckets.

**Matrix.** Retain all 001–007 cases; add empty/missing/null orders, null
elements, each recognized status in mixed case, unknown statuses, missing/null
dueAt, dueAt exactly at and just before asOf, offset-equivalent instants,
missing/valid/null asOf, and a request proving summary does not mutate data or
alter another operation's response.

**Gold/dependency/fairness.** Both golds implement one-pass-or-equivalent
standard-library aggregation and identical JSON semantics, using the Task 007
multi-file gold form and retaining its cumulative workspace checks. Task 008
appends a `text_not_contains` check that forbids the newly known quoted
`"summary"` literal in `Program`; Task 007 never exposes it early. This
depends on all prior status, time, and null rules. Risks are treating `overdue` as exclusive,
counting unknowns, and divergent absent-versus-null serialization.

## Representation successor cell

Only after the clean eight-task chain stabilizes, define a separate successor
protocol cell with a full inherited chain. Preserve all public JSON names,
task-facing names, strings/errors, file/project names, architecture, formatting,
and dependencies. Jointly review each language-specific application of one
descriptive-versus-deterministic private-identifier mapping algorithm; preserve public names
while transforming only the declared private identifiers. Version and hash the
mapping, generator, transformed baseline, and transformed golds. Representation
is a starting-state assignment for the entire inherited chain: never
re-transform candidate code between tasks. Measure representation drift and do
not pool language or treatment cells. Use factorial, counterbalanced assignment
and independent idiomaticity/leakage review. Preregister one language-neutral
algorithm over an independently reviewed inventory of paired semantic roles.
Transform 100% of declarations and references for each same paired role in
both languages, using role-class-stable names. Exclude and report unmatched
roles; do not independently perturb them. Record eligible/transformed roles and
occurrences, coverage, unchanged public inventory, collisions, and source,
lexical, and model-token deltas per language. Require zero collisions and zero
public changes; do not interpret an interaction if paired-role coverage or any
transformation invariant fails. This is a treatment design, not a reason to
alter the clean chain retrospectively.

## Review and release gates

Independent language-equivalence, temporal/null/error, architecture-fairness,
and information-leakage review of this design is complete. Any material contract
change reopens that gate. Before any paid/model run, implement and validate the
chain, run the full cumulative scripted oracle and workspace checks, review both
golds, implement/review the representation treatment, and freeze a new versioned
protocol/cell with hashes. Historical fixtures and variance-v2/v1 cells remain
unchanged and excluded from the successor cell. A frozen difficulty pilot must
show measurable but non-dominated correctness/trajectory variation before
confirmatory collection.
