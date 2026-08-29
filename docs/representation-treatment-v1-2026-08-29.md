# C3 representation treatment v1 (preregistration)

Status: design and implementation are complete, model-free validation passes,
and independent implementation review is approved with no remaining P1/P2/P3
findings. No protocol freeze or model run is authorized by this document.
This is a separate artifact family for the inherited eight-task successor chain.
The pilot, historical pair, C2 successor, and existing golds remain unchanged.

## Treatment and mapping

The levels are `descriptive` (the immutable clean C2 source bytes) and
`deterministic` (opaque reproducible names). One language-neutral algorithm
consumes an
independently reviewed paired-role inventory. Each entry contains `role_id`,
`role_class`, both-language declaration/reference sets, eligibility, and reason.
Classes are `local-variable`, `private-member`, `private-helper-type`, and
`private-helper-function`. All DTO/domain type declarations that are public in
C# or public-by-default in F# (`Customer`, `Order`, `Request`, response types)
are excluded, as are serializer-bound properties/record fields. Public
inventory is exact and includes
JSON keys, values/errors/operation/status/tier literals, project/source/
namespace/module/`Program`/`Main`/`OrderFlowEngine`/`Handle`/`handle` names,
workspace-check literals, and filenames.

The normative public-identifier table is the final C2 gold source at every
stage: types `Customer`, `Order`, `Request`, `Response`, `TransitionResponse`,
`SummaryResponse`; C# entrypoints `OrderFlow`, `Program`, `Main`,
`OrderFlowEngine`, `Handle`; F# entrypoints `OrderFlow`, `Program`,
`OrderFlowEngine`, `handle`; and serializer-bound fields/properties (C# / F#)
`Id/id`, `Tier/tier`, `CreatedAt/createdAt`, `Status/status`,
`Priority/priority`, `DueAt/dueAt`, `Customer/customer`, `Operation/operation`,
`Orders/orders`, `AsOf/asOf`, `ToStatus/toStatus`, `Ids/ids`, plus
`Pending/pending`, `Processing/processing`, `Completed/completed`,
`Cancelled/cancelled`, `Overdue/overdue`, and `error/error`. The JSON key
`error` is public and serializer-bound. This table also includes every
public source/project/namespace/module name and all literal inventories in the
C2 manifest; its source and manifest hashes are recorded in `source-manifest`.
None is eligible for transformation. A machine-extracted and declared
identifier-level serializer-contract snapshot test must compare this table with
the clean C2 sources and both transformed gold sets; omissions fail closed in
addition to literal/source-hash checks.

Mapping rows carry each language's source/descriptive spelling and declaration
and reference occurrences. Only deterministic treatment renames eligible
identifiers. For deterministic names, compute SHA-256 over the exact bytes
`UTF8("alf-c3-role-v1") || 0x00 || UTF8(role_class) || 0x00 || UTF8(role_id)`;
encode the digest as lower-case base32 without padding, and use these exact
ASCII prefixes: `loc_`, `mem_`,
`typ_`, and `fun_`; append the first 10 characters and extend by 2 on collision
until unique, failing on exhaustion or a keyword. The exact same ASCII spelling
is used in both languages, so no casing realization is needed. There is no
randomness or independent perturbation.

## Source-pinned transformation

For every baseline and gold file, the inventory records canonical UTF-8
SHA-256, relative path, token text, identifier-token ordinal, zero-based byte
offset and byte length, line/column, declaration/reference kind, role, and
replacement. Hash, occurrence count/order, token, or language mismatch fails
closed. The C# and F# lexer excludes ordinary strings, chars, comments, and
preprocessor/directive text. In interpolated strings it excludes only literal
text: embedded interpolation expressions are lexed as normal code, including
escaped braces, nested delimiters/strings, and format/alignment clauses as
applicable in each language. Pinned lexer fixtures/tests cover the actual C#
and F# interpolations in every successor baseline/gold; unterminated or
ambiguous interpolation is a fail-closed error. Only listed identifier-token
occurrences change. Non-replaced bytes and line
endings are preserved. Regeneration from immutable source is byte-identical;
`--check` compares materialized outputs. Reapplying to an already transformed
output is a recognized hash-matched no-op (otherwise it fails), not a claim that
raw replacement is idempotent. Transform 100% of declarations/references for every matched role in
both languages. Compiler-reserved, unmatched, and language-specific roles are
an explicit exclusion ledger, never independently perturbed.

Representation is assigned once to a materialized baseline for the whole chain;
candidate code is never re-transformed between tasks. Materialize and hash the
transformed baseline and every transformed gold offline; golds stay hidden.

## Reports and invariants

Reports contain role/occurrence counts, with denominators per snapshot and
absent roles recorded as zero/absent rather than silently dropped, coverage,
exclusions, collisions,
keyword results, unchanged-public snapshot, and per-language/snapshot source
bytes, lines, approximate lexical units, and token deltas. Lexical units use
the existing `alf.metrics.snapshot_repository` metric, including its recorded
source/line/file counters; no new lexical classifier is introduced. The model
proxy is `tiktoken==0.14.0`, encoding `o200k_base`; record package version,
encoding name, and SHA-256 of each deterministic token-id stream/input, where
the stream is canonical compact UTF-8 JSON (`separators=(',',':')`) containing
the integer token IDs. This is
a preregistered offline proxy, not provider billing, hidden Codex accounting,
or the provider tokenizer.
Also report build, evaluator, workspace-check equivalence, idempotence, source
drift, and public diffs. Any public diff, collision, coverage deficit,
build/evaluator difference, failed idempotence, or drift invalidates the artifact.

## Checked-in artifacts and provenance

Implementation adds `benchmarks/successor/representation-v1/` with
`definition.json`, `role-inventory.json`, `exclusions.json`, `mapping.json`,
`generator-version.json`, `source-manifest.json`, `reports/{fsharp,csharp}/`,
`{descriptive,deterministic}.manifest.json`, and
`transformed/{descriptive,deterministic}/{baseline,gold/<task>/}`. The two
runnable manifests are existing-schema-compatible: task text, cases, and
workspace checks hash/equal C2; only repository/gold paths and explicit
treatment provenance differ. If needed, implementation adds backward-compatible
optional metadata without changing existing manifests. Deterministic generated
manifests pin `source_commit` to C2 commit
`4e58677e0bfff18c2104298ad35fc4e801bbd052` plus the source tree and all
input/output hashes,
but no containing commit hash, runtime timestamp, or reviewer disposition.
Review records and run timestamps stay outside generated artifacts.

## Assignment and analysis boundary

The cell is a 2x2 factorial with conditions `F#-descriptive`, `C#-descriptive`,
`F#-deterministic`, and `C#-deterministic`. Each whole superblock contains these
four conditions exactly once in each position using these Williams rows
(`FD` = F#-descriptive, `CD` = C#-descriptive, `FDet` = F#-deterministic,
`CDet` = C#-deterministic):
`[F#-descriptive,C#-descriptive,C#-deterministic,F#-deterministic]`,
`[C#-descriptive,F#-deterministic,F#-descriptive,C#-deterministic]`,
`[F#-deterministic,C#-deterministic,C#-descriptive,F#-descriptive]`, and
`[C#-deterministic,F#-descriptive,F#-deterministic,C#-descriptive]`. Each
condition occurs once per position and each ordered adjacent pair occurs once
across the four rows; repeat the four orders only as whole superblocks.
Repetition count remains a later protocol-freeze decision. Each run has one
language and representation and starts from its materialized baseline. Analyze within-language representation contrasts, then
language contrasts within each representation, and the interaction; retain
task/chain-position dependence. Do not pool pilot, v1, v2, or clean C2 data.
Protocol schema and freeze are later gates.

At every candidate checkpoint retain mapped deterministic occurrences, report
reintroduced descriptive aliases, and report unclassified new private
identifiers. This is observation only: never re-transform candidate code.
Any representation invariant failure makes the affected checkpoint and
interaction non-interpretable and aborts the relevant analysis.

Existing C2 directories and manifests are never edited; descriptive
materialization is byte-identical to those clean sources.

## Acceptance, aborts, and next gate

Acceptance requires independent review of inventory/mapping, lexer exclusions,
public snapshot, transformed golds, equivalence, leakage, and reports; full
cumulative scripted oracle/workspace checks and clean builds must pass. Abort
and regenerate this artifact family on invariant failure, hidden-gold exposure,
source drift, incomplete coverage, or unreviewed manual edit; retain failed
artifacts and hashes. This design does not run candidate agents, estimate
effects, or authorize a freeze. The implementation and review gates below are
now closed. Next: define and freeze a new cell, then run its non-counting
difficulty pilot.

## Independent design-review disposition

Final disposition: **APPROVE**. The two P1 findings were closed: (1) the lexer
now lexes embedded interpolation expressions while excluding only literal text,
with pinned C#/F# fixtures and fail-closed malformed-interpolation handling;
(2) the public `error/error` serializer identifier pair and JSON key are explicit,
with a machine-extracted identifier-level contract snapshot that fails on
omission or casing error. This approval covers the design only.

## Implementation validation and review — 2026-08-30

The checked-in generator materializes canonical Git-blob bytes from C2 commit
`4e58677e0bfff18c2104298ad35fc4e801bbd052`; `.gitattributes` preserves LF bytes
for the generator and generated artifact family across platforms. It records 15
paired roles and 964 eligible occurrences across 26 source snapshots (12 C# and
14 F#), with the declared public inventory exact in both source and
deterministic arms. Replacements, coverage ratios, collision checks, protected
lexical chunks, public sequences, manifest contracts, provenance, and per-stage
token metrics are computed and fail closed. Coverage is derived by independently
rescanning every deterministic artifact, not copied from eligibility.

Independent model-free evidence passed:

- 26 focused representation tests, including adversarial scanner, source-drift,
  stale-artifact, public/private `Overdue/overdue`, provenance, metric, and
  offsetting coverage-deficit/surplus cases;
- write-free deterministic regeneration of 64 artifact files, 100% coverage,
  and 32 safe language/task artifact plans;
- clean builds, cumulative evaluator cases, and workspace checks for both
  runnable manifests and both languages through Tasks 001–008;
- complete scripted C#/F# matrices for both descriptive and deterministic arms.

The final independent implementation disposition is **APPROVE**, with no
remaining P1/P2/P3 findings. The generated report deliberately retains
`pending-external-model-free-validation`: environment-dependent validation
results are review evidence recorded here rather than inputs to deterministic
artifact generation. The post-review coverage-accounting repair did not change
any transformed baseline or gold hash. Cross-platform CI remains the commit
gate before protocol work proceeds.
