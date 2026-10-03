# S103 — Coexisting writable schemas and explicit preservation policy

**Complete publisher reading, 2026-10-03.** Kai Herrmann, Hannes Voigt, Andreas Behrend, Jonas Rausch and Wolfgang Lehner, *Living in Parallel Realities — Co-Existing Schema Versions with a Bidirectional Database Evolution Language*, SIGMOD 2017, pp. 1101–1116, [DOI 10.1145/3035918.3064046](https://doi.org/10.1145/3035918.3064046). Native/Crossref metadata use the shorter title *Living in Parallel Realities*. Online publication 9 May and the printed conference dates 14–19 May 2017 are distinct. Existing native parent **`6Y52QFF2`**, note **`DFT3WGWR`** and five collection memberships, including `PKLXQNEE`, precede this selected reading.

| Native source | File identity | Actual coverage |
| --- | --- | --- |
| User-library publisher PDF `8FDCWCMW` | **16 pages, 2,706,108 bytes**, SHA-256 `e0b436140f9bd34ddc9fe92ba65d1475021a6c68b4191b34444ff63fe69b5a71`, MD5 `169da539240529a4bfe66f16fb40a0fc` | All 16 text and visual pages: ten substantive sections, 13 figures, five tables, 18 references and complete Appendices A–B, including the numbered rules/equations through 205. Figure 13 also receives an enlarged axis/legend inspection. |
| Institutional [arXiv v2 copy](https://fis.tu-dresden.de/portal/files/10694008/1608.05564v2.pdf), `XCWDF767` | **16 pages, 2,905,399 bytes**, SHA-256 `53dbe2da3326be0894c3db3a038ab6f444b346a9267ba3ad71f3a00bf487a0c9`, MD5 `cd122ae9216c5dfab94d1bcd8c8113b0` | Cover text/visual inspection plus all-page extracted-text comparison. After Unicode/whitespace normalization and removal of the publisher's exact terminal page numbers, pages 2–16 match; page 1 differs in publication/permission notices and the arXiv stamp. The remaining v2 pages are not independently visually read. |

Both native stored files are hash-verified. The [arXiv history](https://arxiv.org/abs/1608.05564v2) dates v1 to 19 August 2016 and v2 to 19 September 2017. Matching extracted body text does not establish byte, figure-image or executable-artifact equivalence. The differently titled 2016 web excerpt is not merged with the final evaluation or counted as an independent study. No database, author implementation, benchmark or formal checker is run.

## Question and mechanism

The target is a database serving **several writable logical schema versions simultaneously**, with shared underlying data. This differs from keeping immutable snapshots, rewriting a query over a historical schema, or replacing a running program's state once. Developers declare how a schema evolves; a database administrator can independently change where its data is physically stored.

BiDEL supplies schema modification operations (SMOs): table/column creation, deletion and renaming, adding/dropping columns with supplied functions/defaults, horizontal split/merge and vertical decomposition/join. Its expressiveness claim is relational algebra; evolving constraints and functions is explicitly future work (§3). An operation is a declared transformation with parameters, not a semantic correspondence inferred solely from two resulting schemas.

The catalog is a directed acyclic hypergraph of table versions and SMOs. Each table version has one incoming operation and may have several outgoing operations; a schema names a subset of table versions. Dropping a schema removes its visible name but retains data and connecting operations still needed by other versions. Acyclicity supports bounded-direction propagation; it does not eliminate the cost of long transformation chains.

In the TasKy example (§2, Figures 1–2), a mobile view selects priority-one tasks and drops the priority column. Its declared default restores priority **1** when a new mobile task is written back. A later desktop schema normalizes authors into their own table and foreign key. Applications can read and write all three schemas. The default and decomposition semantics are part of what the developer supplies; their appropriateness is not established by generating SQL successfully.

## What must be retained

Each SMO has source-to-target and target-to-source mappings, written in Datalog templates. The data is materialized on one side; the opposite logical side is implemented through mappings. This **nonredundant payload placement still requires auxiliary storage**. Every tuple has an InVerDa-managed identity `p`, including when visible payload values coincide; identity bridges Datalog set semantics and relational multiset behavior.

| Operation/problem | Information or policy required |
| --- | --- |
| Split predicates leave a row in neither target table | An auxiliary table retains the otherwise invisible row. |
| Overlapping split predicates produce two independently writable copies with the same identity | The first target `R` is the preferred replica when reconstructing the source. A separate auxiliary table retains the conflicting value from `S`. |
| One copy is deleted while its twin remains | Tombstone-like identity sets prevent the deleted copy being recreated on the next mapping. |
| A target write violates its original split predicate | Identity sets retain explicit target membership despite the predicate. |
| Add/drop a column | A supplied function/default creates missing values; an auxiliary column-value table retains existing values and supports repeatable reads. A dropped visible column is not necessarily discarded globally. |
| Decompose/join, including unmatched sides | Padding values, retained unmatched rows and identity mappings preserve information that the visible join/projection would lose. Generated identifiers must be reused, rather than regenerated inconsistently on each read. |

The split example (§4, rules 12–25) is particularly useful: preferred-replica visibility is not full equality between every version's visible payload. The paper expressly allows a value in one redundant version to be unavailable in another view. Its positive guarantee is that a version's own admissible data can be stored through the chosen representation and read back, using the auxiliary information. Thus “all versions share data” does not mean every version exposes every conflicting value simultaneously.

Appendix B extends the mappings to column changes and primary-key, foreign-key and conditional joins/decompositions. Foreign-key generation uses SQL sequences with recorded identity assignments and sequential old/new evaluation. Conditional decomposition can deliberately expose separate author/book sets while retaining correspondence information outside the visible relation. These obligations resemble correspondence/complement state in bidirectional transformations; they are additional maintained state, not free consequences of persistence.

## Scope of the formal argument

Sections 4–5 require the two round trips:

`Dtgt = gamma_tgt_data(gamma_src(Dtgt))`

`Dsrc = gamma_src_data(gamma_tgt(Dsrc))`

The `data` projection hides auxiliary tables. The paper derives one split direction using five simplification lemmas and completes the reverse direction in Appendix A. It obtains merge by inversion; Appendix B gives the remaining mappings and simplified outcomes. Write propagation applies an insertion/update/deletion to a reconstructed logical relation and maps it back; the argument reduces its observed result using the same round-trip law. Composition along acyclic SMO chains relies on the stated absence of cross-SMO side effects.

This is a substantive formal design argument, with a detailed worked split proof. It is not a supplied machine-checked proof of the PostgreSQL generator, transactions, SQL null handling or every production database state. In particular, Appendix B.2 suppresses decomposition sides equal to the padding sentinel `omega_R`. Taken without an admissible-state restriction, a row padded on **both** sides would be suppressed by both printed rules 133–134. The text introduces this sentinel to represent an absent join partner but does not state a separate complete validity predicate there. Distinguishing reserved padding from ordinary data, and specifying allowable all-padding rows, is therefore necessary before adopting a universal round-trip claim. This is a static observation about the written rules, not an executed implementation failure or a rejection of the intended construction.

Preserving a declared round trip also does not prove that the supplied default, preferred replica or new schema embodies the user's intended future behavior. There is no inference here about F# constructor coverage, pending game events, clocks, effect compensation or safe continuation of an arbitrary running program.

## Generated access and physical migration

Section 6 translates rule heads into SQL projections, positive predicates into sources/joins, negative predicates into `NOT EXISTS`, and alternative rules into unions. Three triggers per table version handle inserts, deletes and updates. Delta propagation distinguishes old/new data and avoids rewriting unaffected tuples, instead of recomputing every whole relation after each update. Normal queries run through these generated objects in the existing DBMS, reusing its optimizer, indexes and transaction engine.

The materialization schema must be valid: materialized operations have materialized predecessors at their source tables, and competing outgoing branches cannot both claim the same source placement (§7, conditions 55–56). A DBA command names desired physical table versions. InVerDa checks validity, creates the new data/auxiliary tables, migrates data, regenerates access objects and removes the old physical tables. All logical schema interfaces remain represented after migration. The example's one-line command is a real simplification of authored migration instructions; it is not a measurement of migration latency or operational effort.

The system description invokes transaction guarantees, but **zero-downtime migration is explicitly future work** in §10. Logical availability of schema versions should not be turned into a measured guarantee of uninterrupted service, bounded lock time or concurrent-update throughput. Automated choice of the best materialization is also outside this conference paper; the experimental switch is instructed when the alternative becomes faster.

## Positive evaluation and its denominators

Section 8 uses single-thread PostgreSQL 9.4 on a 2.4 GHz Core i7 with 8 GB RAM. It combines the authors' TasKy example, a Wikimedia schema-history workload and synthetic two-SMO combinations. These are three complementary workload types, not independent developer trials.

For TasKy, the authors manually write and optimize SQL for the same initial schema, evolution and physical migration. Table 3 gives:

| Stage | BiDEL / SQL lines | SQL-to-BiDEL line ratio | BiDEL / SQL statements | BiDEL / SQL characters |
| --- | --- | --- | --- | --- |
| Initial creation | 1 / 1 | 1 | 1 / 1 | 54 / 54 |
| Evolution to TasKy2 | 3 / 359 | **119.67** | 3 / 148 | 152 / 9,477 |
| Physical migration | 1 / 182 | **182** | 1 / 79 | 19 / 4,229 |

The paper's repeated “359×” wording does not match its own evolution denominator of three BiDEL lines; use the table's **359 versus 3**, not a 359-fold effort estimate. The substantial authored-code reduction remains positive evidence. Statements and whitespace-normalized characters provide additional size measures, but neither identifies development time, defect reduction or lifecycle robustness. Generator/runtime/auxiliary-state costs are not counted as developer-authored BiDEL source.

Initial creation takes **154 ms**; generating and executing TasKy2's evolution takes **230 ms**, and Do!'s **177 ms** (§8.1). The stated linearity in SMO/table-version counts concerns the generation structure; physical data movement is not independent of data size. No participant effort or comparative defect-rate study accompanies these times.

The Wikimedia reconstruction represents **171 schema versions with 211 SMOs**: 42 table creations, ten table drops, one table rename, 95 added columns, 21 dropped columns, 36 column renames, four decompositions and two merges; no split or join occurs in this history (Table 4). This supports breadth across a long real history while making its simple-column-operation predominance explicit. It is not 171 independent applications or demonstrations of all primitives in real use.

The principal runtime results are:

- **Generated versus handwritten access:** TasKy contains 100,000 tasks. Figure 8 separates reads from batches of 100 task inserts and distinguishes both logical access schema and physical materialization. Generated SQL has small reported overhead, described both as “up to 4%” and “4% in average”; the publication does not provide a raw aggregation resolving that wording. Reading a matching physical representation is up to twice as fast. Evolved storage also reduces an auxiliary foreign-key-table cost for writes.
- **Changing workload:** Figures 9–10 simulate adoption across 1,000 time slices with 1,000 queries each. The mix is 50% reads, 20% inserts, 20% updates and 10% deletes. An instructed change of physical representation lowers accumulated propagation overhead, **including migration cost**, relative to fixed placements. The second scenario moves Do! → TasKy → TasKy2. This demonstrates a benefit from adapting placement; it is not a fair comparison with an equally adaptive, cost-free handwritten implementation or a demonstrated autonomous advisor.
- **Placement sensitivity:** Figure 11 compares all five valid TasKy placements under mixed, read-only and insert-only workloads. The reported **49×** write contrast is TasKy2 access from its matching placement versus the remote Do! placement. It is not the generated-versus-handwritten SQL effect.
- **Long history:** Akan Wiki contributes 14,359 pages and 536,283 links, loaded at the 109th schema version. Template queries address the 28th and 171st versions under three physical placements. Differences reach about two orders of magnitude; forward added-column reconstruction needs joins, while backward access can project away columns. Figure 12's last placement label says `v25636`, whereas the prose names `v25635`; that literal discrepancy remains unresolved.
- **Two-operation microbenchmarks:** after excluding create/drop/rename operations as having negligible relevant overhead, the paper reports all remaining two-SMO combinations and shows six examples with `ADD COLUMN` second (Figure 13, up to 100,000 tuples). Local access has reported average speedup **2.1**. The combined-time prediction sums individual costs and subtracts the shared local read; measured time differs by **6.3% on average**. This supports the tested combinations' cost account, not a proof that arbitrary chains, workloads or concurrency cannot introduce additional overhead.

The article does not provide the repeated-run counts, uncertainty estimates, cache protocol, full query/DDL packet or all raw timings needed to reproduce these comparisons from the text. Its meaningful positive mechanism and performance findings survive those limits. There is no human/agent net-maintenance estimate, modern PostgreSQL replication or .NET/game measurement in this inspection.

## Survey consequence and next source

For B02/B08, S103 supplies a concrete predecessor for **coexisting writable versions with explicit correspondence, hidden complements and placement-independent logical views**. It narrows any generic claim that representation preservation or bidirectional evolution is novel. For B06/B10/B12, it shows both very short authored transformations and substantial placement-dependent speedups, while keeping source size, generated-code overhead, physical optimization and human effort separate.

For Nu, the consequential comparison is which identity/default/conflict/history policy a proposed change actually guarantees. S103 can preserve what a schema hides by storing more information; a Nu snapshot or explicit world value does not automatically provide this contract. Conversely, the relational model does not cover Nu's queues, physics or irreversible effects. An independently intended-behavior oracle and a complete cost boundary remain required for a future comparison; all construction and experimental holds remain.

SC152 supplies one exact DOI record, metadata and a truncated abstract with denied full-text access. Its three returned citation records point **outward from S103** and contain no citation-statement text; seven mentioning statements and 35 citing publications are provider tallies, not a graph review. The existing PDFs supply the reading. The printed project URL fails in the web reader; two targeted artifact/project queries return 16 displayed hits without recovering the source/run packet. These are bounded retrieval outcomes, not proof that no artifact exists.

Those queries recover the institutional record for **S236**, *Multi-schema-version data management: data independence in the twenty-first century*, [DOI 10.1007/s00778-018-0508-7](https://doi.org/10.1007/s00778-018-0508-7), VLDB Journal 27(4), 547–571 (2018). Its abstract adds a materialization advisor, changing the next consequential action. Native **`SW7VJFA6` / `WJWPQGM9`** is created before selected body reading after DOI/title checks and a 1,261-item library inventory find no existing match. This segment credits **metadata only**; the journal's additions, relationship to S103, valid-state assumptions and measured advisor costs are next. S102 remains a separate document-schema companion rather than an automatic next-paper obligation.
