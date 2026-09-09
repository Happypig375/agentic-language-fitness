# Source-bound paired workload review

Review type: separate AI-session source review, not human language-expert approval
or a candidate-performance score. The reviewer did not author the final paired
language sources; it previously worked on controller/checker/fixture code. Both
languages' initial authoring was separate, but the same subsequent AI session
repaired both. Final authorship is not independent.

The review reported no source-level blocking findings, conditional on successful
trusted behavioral and mutation checks. Both Expanded predecessors expose real
reconciliation and dependency-order APIs without a summary implementation or
helper. Gold adds Task 008 while preserving those APIs. C# uses static modules
and LINQ; F# uses records, modules and collections. The review found no forced
line/file-count parity. These are judgments about these sources, not a general
comparison of language idioms.

## Reviewed identities

Hashes are `alf.protocol.canonical_json_hash` of each filename-to-LF-source
mapping returned by `alf.h_workload.source_for`, not concatenated file hashes.
The construction report additionally records every individual file identity.

| Level/language | Predecessor | Gold |
| --- | --- | --- |
| Core C# | `7bed422fb8ae11147939973bb89bd5fc10ed26856a3aa8502123eee59f909f6f` | `5f378f63f9891753736993eaee2b4f7091df7ff4bebedec964ada00c59e4c7aa` |
| Core F# | `53a20231120cd69ed2d540c47b9dff1d5b77a37391381445c8b8ec875ad9495b` | `6b8a3de461fd2cd21ff77d8d1341baacf6f504208fc99bc9ac59ca17bc544ede` |
| Expanded C# | `fcf44bbc5f05e525ccd3bb59603ad3d526d897ecd0832d42a261bc033cba5f9d` | `35436e5475838723d1d6f8bcd050f16b6bcb3c300ca70294cf4c021bbc6803a3` |
| Expanded F# | `9ab51cdbca67a5c52f48eb411034d859857361c18d24fb09d9b825bc5bbbd159` | `4d04fe0e41497da2167ec19b202a627673a299471e2ed935038219b24de87f65` |

Core is materialized from the unchanged [H0 definition](../../protocols/workstream-h0/definition.json).
Expanded sources are [C# predecessor](../../benchmarks/workstream-h/repos/csharp/expanded/),
[F# predecessor](../../benchmarks/workstream-h/repos/fsharp/expanded/),
[C# gold](../../benchmarks/workstream-h/gold/csharp/summary/) and
[F# gold](../../benchmarks/workstream-h/gold/fsharp/summary/).

## Evaluator-only rubric and relevance map

This section, gold and sealed cases must never be included in candidate source
maps or requests. Alternative correct names, file arrangements and internal
representations are allowed; matching these example names is not the rubric.

| Obligation | Evidence to inspect |
| --- | --- |
| `domain_model_in_engine` | Order/request/response types and engine-owned domain operations |
| `live_dispatch_in_engine` | Actual operation routing, including both Expanded APIs |
| `program_io_boundary` | Program deserializes, delegates and serializes/errors; domain logic stays in the engine |
| `summary_in_engine` | Live Task 008 summary behavior in the engine; applicable to gold/final submissions, not predecessors |

The AI review judged the applicable obligations satisfied in these trusted
bundles. It inspected strict Int32/date handling, UTF-16 ordinal ID ordering,
right-side exact ties, validation precedence, topological ready-set ordering,
case-insensitive status counts, strictly earlier active overdue counts and
overlapping status/overdue totals. Passing this review is not an independent
proof of the oracle and cannot replace behavioral or fault-injection evidence.

Future final-source judgments remain separate. Arrange reviewers blind to
per-slot behavioral/resource outcomes, identify human versus AI review, reuse
identical source-hash judgments, and keep missing required judgments unknown.
