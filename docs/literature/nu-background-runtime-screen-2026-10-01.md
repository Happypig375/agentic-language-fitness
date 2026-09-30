# Functional persistence and runtime-method continuation

**2026-10-01 HKT; in progress.** This B04/B06/B12 segment follows the weaker cost coverage identified by the [GPT-6 Pro review](../supervisor-review-2026-09-30.md). It extends C11 rather than replacing the wider [survey](nu-background-survey-2026-09-30.md). Collection layout, retained history, collector latency, workload context and maintenance effort are distinct questions. No theme is declared surveyed and no experimental work is authorized.

## Promoted records and actual coverage

Records were created/reused through Zotero 10's native API before intended body reading. Downloaded PDF bytes were read back from native attachments and hash-verified. Keys are parent / PDF / note; none of these PDFs or raw artifact files is committed.

| ID / primary identity | Native identity and edition | Reading state and live implication |
| --- | --- | --- |
| S143 CHAMP, [10.1145/2814270.2814312](https://doi.org/10.1145/2814270.2814312) | `34J3MDAP` / `6SIYJNYL` / `RX46EDUI`; CWI PDF, eighteen pages, 562,242bytes, SHA-256 `1bb08cc704281dcb0432d666aa37a9259f7ed69c6a1f30068459c165e34be436` | [Complete](full-reading/S143-champ-immutable-collections.md); all figures/tables, bounded pinned source and cached data arithmetic. Notices DOI `10.1145/2858965.2814312` is the same publication lineage. Positive representation costs coexist with slower operations and hash-policy effects |
| S144 Alligator collector, [10.1145/3381898.3397214](https://doi.org/10.1145/3381898.3397214) | `KTSUUDH9` / `JA2HIJDF` / `2AEVVKXW`; [institutional author PDF](https://www.cs.unh.edu/~dietz/papers/gamari2020alligator.pdf), thirteen pages, 527,541bytes, SHA-256 `effb875367bc8b565af3b0c721fd1aaf3292285cad75d38fc98cc3d345bd9ecd` | [Complete](full-reading/S144-alligator-collector.md); all thirteen pages, bounded source/notebook and selected design reading. Large major-pause gains coexist with higher minor pauses/CPU and unresolved release correspondence |
| S145 Counting Immutable Beans, [10.1145/3412932.3412935](https://doi.org/10.1145/3412932.3412935) | `JPGFLE52` / `7T475K65` / `U9NS75IB`; [KIT author PDF](https://pp.ipd.kit.edu/uploads/publikationen/ullrich19counting.pdf), twelve pages, 621,450bytes, SHA-256 `357f5e70164cdba0c0ba2ea1fbf6e0f51306468956cfff9486d4930a05e11589` | [Complete](full-reading/S145-counting-immutable-beans.md); thirteen complete source/config files, selected configuration and rounded-row arithmetic. Reuse/borrow benefits, adverse cases and retained roots reconstructed. Preprint metadata verified; PDF-edition correspondence remains untested |
| S146 Misleading Microbenchmarks, [10.1145/3748522.3779882](https://doi.org/10.1145/3748522.3779882) | `VY9YK2V2` / `NA4A53G2` / `MHKM8JJH`; arXiv `2605.23570v1`, nine pages, 674,406bytes, SHA-256 `20d07b7b149b1cb15c169bbad80ad6a957cc1eb1d9861f227dfa07d2333c4851` | [Complete author edition](full-reading/S146-jvm-benchmark-context.md); six figures/two tables. Profile-context intervention changes a hash-implementation ranking and other timings. No CHAMP rerun or exact artifact recovered |
| S147 Bad JMH Practices, [10.1109/TSE.2019.2925345](https://doi.org/10.1109/TSE.2019.2925345) | `GP4BQG7X` / no PDF / `2H26NKVR`; seventeen-page author manuscript accessible only as cached text; direct transfer resets and screenshots fail | [Partial](full-reading/S147-benchmark-practices-partial.md). Selected selection/rule/table passages and pinned artifact clarify that CHAMP was excluded from impact testing; most exported artifact warnings concern bundled JMH code. Broader study methods/results and final-issue correspondence remain incomplete |

Current holdings after these additions and the S148–S150 continuation below: **169 live parents = 166 literature + three public source records, 181 PDFs in seven subcollections**. Other existing attachment types remain. Complete-paper coverage is **116 works = thirteen P + three A + 100 S**; S147/S149/S150 are not in that total. Native S143/S144/S145/S146/S148 complete notes and S147 partial note reflect the canonical reconstructions.

S144's later design-supplement attachment `TEQG3DG7` accounts for the177th PDF, not another publication:31 pages,576,273bytes, SHA-256 `5a943ea0c9e5718c5ca43d801bf19fbdd44e681b1ef56643650ea9bdcf6daf46`. Selected pages1–3 and21–28 were read. Its canonical note records the pinned repository, ten complete source/config/doc files and33/83 notebook cells; missing raw inputs/launcher and changed saved Table2 values remain unresolved. Paper coverage and artifact reproduction are separate.

## S144 follow-up, 2026-10-01 HKT

| Route | Request / actual return | Disposition |
| --- | --- | --- |
| G19 | Incoming S144 DOI, depth1, cap150, snippets; five edges/six nodes, seed count5, no truncation or low-coverage flag. Same result verified by a repeated read; no additional discovery count | All titles and supplied contexts read. OCaml parallelism `10.1145/3408995` is a conditional runtime alternative; `10.17863/cam.56842` repeats its institutional edition. `10.1145/3473568` adapts Alligator for nonvolatile persistent STM, not retained functional versions. Code rationalization `10.1007/978-3-030-99584-3_11` and hardware collector Cloaca `10.1145/3677999.3678277` remain conditional; no full-method or independent-replication credit |
| SC82 | Four distinct non-Cambridge G19 DOIs plus the two Ueno foundation titles in one request, `limit:20`, offset0; four/four DOI records returned | The DOI filter did not return the title-only foundations. This is not six matched methods; title lookup was reformulated separately |
| SC83 | Exact titles *An efficient non-moving garbage collector for functional languages* and *A fully concurrent garbage collector for functional programs on multicore processors*, `limit:20`, offset0; four/four records | 2011 conference/Notices `10.1145/2034773.2034802` / `10.1145/2034574.2034802`;2016 conference/Notices `10.1145/2951913.2951944` / `10.1145/3022670.2951944`. Two underlying works, conditional foundations. No body/proof borrowed; edition notices are not corrections. Returned exact-identity set accounted, not field exhaustion |
| W160 and ordinary primary-file access | Author GitHub repository open; API pin `048f000e1261e86701e9a010bb48cbc1ed51f17b`,41 tree entries, twelve selected downloads | Main paper complete, design/notebook partial, ten other files complete. No build, notebook execution or runtime reproduction. Blank additional-results link and absent run/data files limit the released reproduction path |

Audit `nu_background_s144_20261001` records23 decisions:13 credited and10 excluded, comprising six conditional scope decisions and four duplicate identities/routes. Full-text-stage13 means one complete paper plus twelve bounded artifact files, including partial PDF/notebook coverage; it is not thirteen papers. Provenance: ten Scite, twelve ordinary pinned-file reads, one web locator. Report inspection found zero missing reasons, no unlinked-retrieval warning, no truncation and answer-scoped retrieved count null. S144's inclusion advances its earlier acquisition state; unchanged earlier screens were not submitted again. The repeated G19 verification produces no extra source decision.

S145 reference-counted reuse and S148's proof/reclamation dependency are now complete below; S149's reuse-space bound and S150's imperative snapshots are the next acquired dependencies. The broader .NET/game, retained-history and workload frontiers remain open alongside the other B themes. S144 establishes scoped latency benefits and explicit adverse costs, not a source-purity effect or Nu comparison. No experimental hold changes.

## Discovery routes and their limits

Every Scite literature request used `limit:20`, offset zero for these exact identity sets. The complete returned sets are accounted; none is a claim of field exhaustion. No new Consensus call was made in this segment; C11's unexamined continuation remains.

| Route | Exact request or scope | Actual return / examined boundary |
| --- | --- | --- |
| SC77 | Exact titles: CHAMP; Alligator collector; Counting Immutable Beans | Four/four: CHAMP conference/Notices, Alligator and Beans preprint. Supplied metadata/short passages only at discovery |
| SC78 | Exact final Beans DOI | One/one, publication identity verified against Crossref |
| G18 | Incoming depth one from both CHAMP DOIs, cap150, snippets | 36 edges, 31 nodes, seed counts29/7, no truncation/low-coverage flags. All titles and selected contexts inspected; alternate editions retained |
| SC79 | Six exact DOIs: Misleading Microbenchmarks, Persistent Iterators, RRB-vectors, Automatic Microbenchmark Generation, Runtime/compiler HAMTs, State-Based ADTs | Six/six; metadata, short/missing abstracts and supplied snippets. No missing abstract converted into full reading |
| SC80 | Exact S147 DOI | One/one; metadata identifies final TSE volume/pages, not complete methods |
| SC81 | Exact titles: MapReplay; Experimental Evaluation Methodology for the Era of No Steady Performance | Four/four: MapReplay publication/preprint and two artifact records for the latter title. The latter paper itself was not returned; artifact identity is not independent-study evidence |
| W144 | `"Optimizing Hash-Array Mapped Tries" CHAMP 2015`; `"Alligator collector" latency optimized garbage collector pdf`; `"Counting Immutable Beans" paper` | Seventeen search records; primary author/institutional routes, editions and secondary explanations separated |
| W145 | `site.ir.cwi.nl "Optimizing Hash-Array Mapped Tries"` (first query malformed); corrected `site:ir.cwi.nl "Optimizing Hash-Array Mapped Tries"`; KIT metadata open | Fourteen search records plus one open; CWI primary recovered |
| W146 | `"Counting immutable beans" "IFL" DOI`; arXiv abstract open | Seventeen search records plus one open; publication/preprint identities and conditional reuse/laziness leads |
| W147–149 | Advertised CHAMP artifact and author/project routes; `"oopsla15-artifact" Steindorfer` | W148 has seventeen search records plus Capsule open. Web cache misses do not imply absence: ordinary HTTP and GitHub API recover the renamed pinned repository. Author blog is bounded documentation; thesis/industry-replication claims remain unverified |
| W150 | `"Misleading Microbenchmarks on the Java Virtual Machines" pdf`; `"Persistence for the masses" pdf`; industry-blog open | Eighteen search records; blog web open fails. Primary arXiv/D3S and RRB routes recovered; no independent industry replication credited |
| W151–152 | `"What’s Wrong with My Benchmark Results" JMH paper`; `"Misleading Microbenchmarks" arxiv 2605.23570`; D3S opens | Twenty search records plus institutional metadata; older direct-artifact critique promoted as S147 |
| W153 | `"What’s Wrong with My Benchmark Results" pdf Leitner`; `"2925345" pdf` | Seventeen search records; six unrelated numerical matches excluded. Coauthor bibliography confirms DOI, no alternate PDF |
| W154 | `"10.1109/TSE.2019.2925345" "pdf"`; `"Misleading Microbenchmarks on the Java Virtual Machines" artifact github` | Nineteen search records. No exact S146 package recovered; MapReplay and newer non-steady-performance methods identified |
| W155–159 | S147 cached PDF open/find, selected methods/table opens and attempted two page screenshots | Text fragments available; screenshots fail with cache misses. No full-PDF or visual credit. Advertised author repository supplies the bounded evidence inspection described in the partial note |

The search queries return **139 search occurrences**. Including successful open/find entries, the saved responses contain **152 route occurrences across 119 distinct URLs**; failed opens/screenshots are separate access attempts. A repeated URL or a separately indexed DOI is not another independent empirical case. The raw responses, source hashes, exact thirteen-file CHAMP and five-file S147 scopes, and recalculated summaries remain in the ignored local evidence directory.

## Consequential frontiers carried forward

| Lead | Why it remains consequential / current disposition |
| --- | --- |
| RRB vectors, `10.1145/3110260`; Persistent Iterators, `10.1145/3808324` / arXiv `2604.14072` | Value semantics, transience, reference counts and retained sharing could change the update/history cost account. Metadata/selected citation contexts only; a CHAMP reference is not an independent HAMT measurement |
| Heterogeneous HAMTs, arXiv `1608.01036`; product-line tries, `10.1145/2993236.2993251` and alternate `10.1145/3093335.2993251` | Representation specialization and multimaps; overlapping author/benchmark lineage, no independent replication presumed |
| Runtime/compiler HAMTs, `10.1145/3486602.3486931` | C11 disposition reused; compiler/runtime cost methods remain unread. State-based ADTs `10.1007/978-3-032-24494-9_4` is a separate metadata lead |
| MapReplay, `10.1145/3777884.3797010` / arXiv `2603.14019` | Trace-driven operation mix is the closest newly identified method for the representativeness question left by S143/S146; body unread |
| Non-steady performance: `10.1007/s10664-022-10247-x`; primary institution lists `10.1145/3798236` | Fixed warmup and variance do not establish a representative regime. Earlier method and newer paper/artifact relationship remain unread; no result imported from titles |
| Automatic microbenchmark generation, `10.1145/2970276.2970346` | Conditional method for elimination/constant-folding concerns; not evidence that S143's blackhole-consumed operations were eliminated |
| Aggregate updates, `10.1109/CGO53902.2022.9741275`; PIE, `10.22152/programming-journal.org/2018/2/9` | Distinct dataflow/update and interactive-pipeline workloads; conditional B03/B08 methods, not collection-cost replications |
| Few versatile collections, `10.1145/3191697.3214334`; C♭, `10.1145/3276954.3276956` | Library-design and tuning choices may inform B10's integration costs; only metadata screened |
| Cache-tries and lock-free compaction; PHP/Rascal corpus; Yona and solver applications | Retain distinct concurrency, data-provenance and language/application roles. Citing CHAMP does not establish the same outcome or comparator |
| Mutable value semantics, functional binary trees and first-order laziness | Returned through S145's author/citer routes; concrete reuse/ownership alternatives to revisit after its primary method |

Nonvolatile/orthogonal durability, IoT routing and GPU triangle-counting results are not used to support cheap functional snapshots. This is a scoped exclusion, not a judgement that those fields lack value.

## Audit and current judgement

Audit `nu_background_runtime_20261001` records **152 distinct source dispositions: sixteen credited and 136 excluded**. Ten full-text-stage entries include repeated paper/access identities, bounded documentation/artifacts and the partial S147 reading; they do not represent ten complete papers. There are 142 metadata stages, 112 web sources, 38 Scite sources and two direct author repositories. Eight unchanged prior URL/DOI dispositions were reused rather than submitted as new screening.

Eight initially overbroad duplicate labels were corrected to conditional/out-of-scope. The service appends correction events: its inspected report therefore shows **160 events, sixteen credited/144 excluded**, not 160 distinct sources. The current unique-source dispositions are seventy duplicate routes, 55 conditional/out-of-scope and eleven off-topic exclusions. Both report calls accepted all submitted records, with zero skips. The inspected report has no missing reasons, unlinked retrieval warning or truncation; answer-scoped retrieval is null. Corrections do not add papers or independent evidence.

**Unique:** broad persistence and context-sensitive measurement mechanisms have predecessors; Nu/D1 priority is unconfirmed. **Valuable:** CHAMP supplies positive collection/application measurements with slower cases; S146 demonstrates consequential context sensitivity. Net Nu benefit, retention and latency remain separate empirical questions. **Scientifically valid:** complete S143/S146 and bounded S147/data reconstruction clarify what can be concluded; they do not reproduce timings or validate ISE apparatus. S144/S145 are now complete; continue S148 and the consequential representativeness/retention leads while preserving other B01–B12 gaps.

## S145 complete and the precise-reclamation frontier

**2026-10-01 HKT.** The [S145 note](full-reading/S145-counting-immutable-beans.md) reconstructs all twelve pages/seven figures and28 references, with the dated benchmark tag, thirteen complete files, selected configuration and independent arithmetic over rounded published rows. Reuse, borrowing and counter specialization supply measured benefits alongside adverse/near-null cases. Retained roots raise time without eliminating every reuse opportunity. Its specified compiler has no completed correctness proof in this paper; cross-language timings and GC fractions do not isolate memory-management effects.

| Route | Actual coverage | Continuation / interpretation |
| --- | --- | --- |
| G20 | Incoming S145 DOI, depth1, cap150, snippets;22 edges/23 nodes, seed count22, no truncation/low-coverage flag. All titles and supplied contexts inspected | Perceus promoted; other conditional identities below. The parkour DOI `10.3390/sports6010006`,2018, has unrelated later-formalization text: no reliable citation identity or support credited |
| SC84 | Six exact DOIs, `limit:20`, offset0; six/six returned: Perceus, frame-limited reuse, FP², PVS2C correctness, modal OCaml and lifetime inference | Supplied truncated abstracts/metadata and contexts read; no full-method credit. Exact returned set accounted; broader method/query coverage remains open |
| W161 | IFL19 benchmark URL open fails in web cache; arXiv1908.05647 metadata succeeds | Native GitHub API resolves tag to `c7e85e3cec929ac3e90e6126305e65200d6bfc06`, dated2020-03-05;2,499 tree entries. Preprint v3 has the same date; its PDF/earlier revisions not compared with KIT |
| W162 | Exact query `"Perceus: garbage free reference counting with reuse" pdf`;23 search records | Primary Microsoft/author/publication routes distinguished from mirrors, discussions and slides. Extended report v4 selected and acquired; other editions not independently counted |

G20's consequential conditional routes are explicit rather than interpreted as completed readings:

| Identity | Live role / disposition |
| --- | --- |
| `10.1145/3453483.3454032`, Perceus | **S148 promoted:** direct precise-reclamation, soundness and reuse successor |
| `10.1145/3547634`, frame-limited reuse; `10.1145/3607840`, FP² | Conditional stronger reuse/space premises and source obligations after Perceus |
| `10.1007/978-3-030-39322-9_4`, PVS2C correctness | Conditional independent code-generator correctness account; SC84 context says cycle-free languages, not proof coverage for Lean |
| `10.1145/3798221`, lifetime inference; `10.1145/3674642`, modal OCaml | Conditional annotation/inference and safe stack/in-place alternatives; no benefit estimate borrowed |
| `10.1007/978-981-97-2300-3_11`, Being Lazy When It Counts; `10.1145/3747530`, First-Order Laziness | Conditional eagerness/laziness transfer methods |
| `10.1145/3571233`, tail recursion modulo context; extended `10.1017/s0956796825100117` | Conditional stack/reuse method; extended edition is the same lineage, not a separate replication |
| `10.1145/3656398`, functional imperative trees; `10.5381/jot.2022.21.2.a2`, mutable value semantics | Conditional source/ownership alternatives and representation costs |
| `10.1007/978-3-030-34175-6_13`, Mimalloc | Conditional allocator rival for claimed allocation/locality effects |
| `10.1145/3735950.3735953`, arborescent collection | Conditional cycle-handling alternative to S145's cycle-free premise |
| `10.1109/iccins58907.2023.10450100`, reference-counting optimization survey | Conditional secondary recall check; primary estimates not replaced by its title |
| `10.1145/3408981`, evident effect handlers; `10.1007/978-3-030-79876-5_37`, Lean4 system | Conditional effect/runtime integration and system-evolution accounts |
| `10.1145/3372885.3373826`, continuum hypothesis; `10.1145/3372885.3373824`, mathematical library; `10.1007/978-3-031-70916-6_4`, De Zolt; `10.1145/3763167`, bitvector reasoning | Application/theorem/library records not selected for this runtime-method comparison; no runtime or retention effect credited |

S148 was DOI/title duplicate-checked and added before intended body reading. Parent `VHMT5KSM`, note `966QN2KX`, [Microsoft extended PDF](https://www.microsoft.com/en-us/research/wp-content/uploads/2020/11/perceus-tr-v4.pdf) `MEMVQQ6J`:40 pages,642,209bytes, SHA-256 `d891a354d2f055a4cf8e1369160cf40415df91e22d1d8135b729a471208d7973`. Primary metadata labels MSR-TR-2020-42 v4,2021-06-07, extended from PLDI2021. Its body and publication/extended correspondence remain unread. Native upload bytes were read back and hash-verified. Holdings become167 parents/178 PDFs; S145 advances full coverage to115, while S148 adds no full reading.

Audit `nu_background_s145_20261001` records62 decisions:19 credited/43 excluded, with29 conditional/scope decisions,13 duplicate editions/routes and one unreliable off-topic graph identity. Fifteen full-text-stage entries comprise one complete paper plus14 bounded files, one only partially read;47 entries are discovery/metadata. Provenance:23 Scite,14 ordinary pinned-file reads and25 web occurrences/locators. Report inspection found zero missing reasons, no unlinked retrieval warning or truncation; retrieved count is null. S145's state advances from acquisition, and S148 is credited as a selected unread method; neither is represented as a new independent replication.

## S148 complete — proof scope and source/result correspondence

[S148](full-reading/S148-perceus-precise-reclamation.md) now covers all forty extended pages, eleven figures, 53 references and appendices A–C. Selected published pages11–13 and eleven complete pinned files resolve the theorem/optimization distinction and expose two source/result discrepancies. The named release specifies4.2 million insertions versus42 million in both paper editions; its runner computes a mean after removing a unique slowest run rather than the reported ten-run median. These do not establish what actually ran. Positive throughput/RSS results, adverse cases and unequal C++ obligations are retained.

The published PDF adds attachment `34IQ4QF4`, sixteen pages,635,027 bytes, SHA-256 `7f134757623b2820b6e1f4d53fae845cfc413a92a449fb73895f4c952173839c`. Parent `VHMT5KSM` and note `966QN2KX` are reused and the complete note read back through the native API. This is an additional edition, not another work. The eleven source files remain ignored local evidence; no author code was run.

| Route | Actual return and inspection | Coverage disposition |
| --- | --- | --- |
| G21 | Incoming S148 DOI, depth1, cap150, intent/snippets;36 edges/37 nodes, seed count36, untruncated and no low-coverage flags. All titles/supplied contexts read | Thirteen citer dispositions reused unchanged; frame-limited reuse advances from conditional to S149;22 other citer identities are new to this screen. Graph resolution does not establish complete citation coverage |
| SC85 | Five exact DOIs: frame-limited reuse, FP², Snapshottable Stores, modal FRP and read-reclaim races; `limit:20`, offset0; five/five returned | Four truncated abstracts, identity metadata and supplied modal-FRP citation contexts only. Exact requested set accounted; no broad query or field exhaustion claim |
| W163 | Open primary Perceus publication and Koka `v2.0.3` repository pages | Publication disposition reused; API pin `0d7fb9b09e0c842e948d62b08014ad198de0c040`,2020-11-09,1,531 untruncated tree entries; selected files read |
| W164 | Queries `"Snapshottable Stores" pdf`, `"Reference Counting with Frame Limited Reuse" pdf`, `"FP2" "Fully in-Place Functional Programming" pdf`;15 returned records | Primary PDFs, author/institution pages and metadata distinguished from a talk, discussion and broad author list; two methods selected, FP² conditional |
| W165 | Author homepage/PDF resolution for Snapshottable Stores and Perceus published-PDF open | S150 resolver exposed opening pp1–4; native record precedes continued intended reading. S148 published comparison is bounded, not another complete reading |

G21's new or advanced decisions are grouped below. All unpromoted entries remain metadata/context-level; no result is inferred merely from a title.

| DOI identity | Live role / disposition |
| --- | --- |
| `10.1145/3547634` | **S149 promoted**: direct stronger space-bound successor; earlier conditional state changes because optimized retention is now a concrete issue |
| `10.1145/3674637` | **S150 promoted**: imperative store capture/restore alternative, with integration, cost and proof scope to reconstruct |
| `10.1007/978-3-031-69583-4_8` | Conditional concurrent read-reclaim race method; exact metadata recovered, body unread |
| `10.1145/3473576`, `10.1145/3563289`, `10.1145/3747529` | Conditional effect compilation, handler naming and multi-resumption/local-state semantics; the first also appears in S148's bibliography |
| `10.1145/3498685`, `10.1145/3572920`, `10.1007/978-3-031-95589-1_5`, `10.48550/arxiv.2510.20547` | Conditional certified coroutine compilation, sparse synchronous hardware and two Mimosa routes for B03/B06. Mimosa chapter and RTOS preprint are not assumed identical editions |
| `10.1145/3519939.3523706`, `10.1145/3689755`, `10.1145/3720507` | Conditional proof-producing compilation, ABI and sequent-calculus implementation alternatives; no whole-compiler correctness claim imported |
| `10.1145/3729313`, `10.1145/3764117`, `10.1145/3819821` | Conditional concurrency ownership, borrowing and linear dependent-type methods |
| `10.1145/3652024.3665507`, `10.1145/3808310` | Conditional immutable-cycle abstract and concurrent partial-tracing method; separate publication types and premises |
| `10.1145/3798264`, `10.1007/978-981-92-0184-6_8` | Conditional generic incremental calculus and lazy mesh-boolean application; no general state-history benefit credited |
| `10.4204/eptcs.428.1` | Conditional mailbox-protocol extended abstract for B03 |
| `10.1109/ubmk59864.2023.10286664` | UI navigation/framework comparison excluded from this reclamation segment; not a measured collector effect |
| `10.1145/3652024` | Proceedings-level record excluded as a paper/experiment unit; the separate cycle abstract remains identifiable |

The eleven unchanged G20 citer dispositions, earlier modal-FRP DOI `10.1017/s0956796822000132` and earlier lazy-proof DOI `10.4230/lipics.itp.2026.6` are reused rather than reported as new screens. FP² remains a stronger static-guarantee lead; the new web source does not confer full-method credit. Bibliographic linear-resource, uniqueness, aggregate-update and residual-reference-counting foundations retain conditional relevance; no new firstness assertion requires reopening all of them.

| Selected next reading | Native record / PDF / note | Edition, verified bytes and present coverage |
| --- | --- | --- |
| S149 frame-limited reuse | `LM67FLSH` / `UB75YUAF` / `FDMAE6C4` | [Microsoft-hosted published article](https://www.microsoft.com/en-us/research/wp-content/uploads/2023/07/flreuse.pdf),24 pages,651,593 bytes, SHA-256 `9bc0561d70eb87ee9a16c7b52993d25e8f45e5328922ef8153f90c00640131ff`; now fully read in the publication; ten extended pages and fourteen complete source files are reconstructed in the S149 continuation below |
| S150 Snapshottable Stores | `EKXV6FJ5` / `HJHT9XRB` / `APJ43MJF` | [Author edition with appendices](https://clef-men.github.io/publications/allain-clement-moine-scherer-24-store.pdf), 39 pages, 707,261 bytes, SHA-256 `2253465f8e52519a6e3a31f66ba10efa64e195bc93a42dfa67e4e41c8dcda281`; now fully read, with bounded source/proof reconstruction in the S150 continuation below |

Audit `nu_background_s148_20261001` records **53 decisions:18 credited/35 excluded**, with28 scope/conditional and seven duplicate-route decisions. Fourteen full-text-stage entries comprise one complete extended paper, one partial published-edition comparison, eleven complete source/config files and S150's partial opening—not fourteen complete works. The other39 entries are metadata/discovery. Provenance is24 Scite,11 ordinary pinned-file and18 web sources. All submissions were accepted, zero skips; report inspection has zero missing reasons, no unlinked-retrieval warning and no truncation, with retrieved count null. Thirteen unchanged DOI decisions and one unchanged primary metadata page were not resubmitted.

**Unique:** unconfirmed against established reuse and snapshot mechanisms. **Valuable:** competitive scoped runtime results and explicit costs, with unmeasured Nu/.NET/history transfer. **Scientifically valid:** complete S148 primary reconstruction with bounded edition/source checks; optimization guarantees and exact experiment correspondence retain stated limits. Continue S149/S150, then consequential runtime/discovery and other B01–B12 gaps. No experimental allocation changes.

## S149 continuation — complete method, bounded proof/source reconstruction

**2026-10-01 HKT.** [S149](full-reading/S149-frame-limited-reuse.md) now covers all24 publication pages/eight figures and the bibliography. Native parent/note `LM67FLSH` / `FDMAE6C4` are updated and read back. Extended report attachment `VPTKHEXU` has54 pages/795,976 bytes, SHA-256 `7bab587b8d3a3fff9d3b7d6781022efb5af54cec03324989348e636f2ffbad94`; only pages27–30 and49–54 were read, with27 and51–54 visually checked. The acquired report's proofs are appendixD, despite the publication's appendixC references.

| Route | Actual inspection | Disposition |
| --- | --- | --- |
| W166 | Open primary extended-report publication page | MSR-TR-2021-30/v2 identity and PDF route; partial report reading, not another work |
| W167 | Two exact web queries: `"flreuse" "tr" "pdf"` and `"Reference Counting with Frame Limited Reuse" "github"`; twelve returned records | Primary author/event/repository locators separated from four duplicate routes, current-manual/constant-time-fork leads, people/room pages and a forum snippet with incorrect venue/date and unsupported exclusivity |
| Named release APIs | `v2.3.3` -> `e371bf9d67931f3847288c595fb8095be242e1ee`,1,735 tree entries; `v2.3.3-old` -> `97df9e4fe47143062225170963b786483b3fe6e4`,1,634 entries; neither truncated | Fourteen complete selected files; two acquired legacy runners unread because README specifies `bench.kk`. Whole compiler and exact experiment invocation not reconstructed |

The source decision audit `nu_background_s149_20261001` has **31 decisions:20 credited,11 excluded**, with six scope/conditional, four duplicate and one low-quality secondary-context exclusions. Sixteen full-text-stage entries are one complete publication, one partial report and fourteen complete source files; fifteen are metadata/acquisition/discovery stages. Provenance is one Scite, fourteen web and sixteen ordinary source routes. Submission/report show zero skipped or missing reasons, no unlinked-retrieval warning and no truncation; retrieved count is null. S149's status advances; earlier unchanged DOI neighborhood decisions are not resubmitted.

The bound and positive/null/adverse results are retained alongside unresolved queens-size, aggregation and arm-correspondence limits. S149's bibliography leads back to already reconstructed S145/S148 and explicit conditional space/uniqueness foundations. No new firstness claim requires reading every predecessor now. Continue S150's imperative snapshot alternative, then consequential B01–B12 frontiers; FP² remains conditional on a stronger static-allocation question.

## S150 continuation — imperative snapshots and their resource tradeoffs

**2026-10-01 HKT.** [S150](full-reading/S150-snapshottable-stores.md) is now fully read: all 39 extended pages, seven figures, appendices A–C and bibliography. All 114 rows in seventeen detailed microbenchmark tables were reconstructed; the center ratios are compatible with printed rounding. Eleven pinned Store files, including all twenty notebook source cells, are fully read; the notebook has no saved outputs. A separate proof file has selected definitions/specifications read and its content hash matches the publication, without building or fully reviewing its dependencies. Native note `APJ43MJF` is updated/read back.

| Route | Actual inspection | Coverage / decision |
| --- | --- | --- |
| G22 attempted | Incoming S150 DOI, depth 1 / cap 150 / intent + snippets | **No graph returned:** monthly MCP 2,500-call quota reached; service states reset 2026-10-01 UTC. This is an access/resource failure, not zero citers. Retry remains pending |
| W168 | Pinned Store tree and Zoo proof-page opens | GitLab web 403; native HTTP API succeeds. Store pin `37a14f538e75eea3de930a797623e7f7fd036948`, 2024-06-12: 56 entries, 46 files/10 directories, second page empty. Zoo tag pin `831705d2a577c5807061d707f2375bf4395fa4da`, 2024-07-07; proof content SHA-1 `e637417fb4af3a462caa063a575e97905d32800b` matches the cited SWH content |
| W169 | `"Snapshottable Stores" "2025"` and `"Snapshottable Stores" "2026"`; eighteen returned records | Primary metadata/context screen; direct custom-type successor selected, conditional proof/framework/port leads retained, duplicate and secondary routes excluded; not citation exhaustion |

W169's substantive and excluded routes remain explicit:

- [Storable types: free, absorbing, custom](https://www.irif.fr/~scherer/research/store/store-custom-2025-paper.pdf): **S151 selected/acquired**, seventeen pages, 312,327 bytes, SHA-256 `58edf60e068b37327e7d4ae4dd16546e8336d7c2994a5cbc46f931018a954a2a`. Native parent/PDF/note `VD9SYCR5` / `EZA2HF4W` / `8I4W6VCP` precede intended body reading; body remains unread. Title/author/venue came from the primary author route, no DOI guessed.
- [Scherer publication page](https://gallium.inria.fr/~scherer/publications): primary locator, also exposing later benchmark-method and verification work; no method reading credited from the list.
- [Allain thesis](https://iris-project.org/pdfs/2025-phd-allain.pdf), [Zoo JFLA 2025](https://clef-men.github.io/publications/allain-25.pdf), and [Rust ghost-ownership verification](https://jhjourdan.mketjh.fr/pdf/golfouse2026ghost.pdf): conditional proof/edition/implementation-correspondence leads, returned contexts only. Related versions are not assumed independent evaluations.
- [Rust snapshot crate](https://docs.rs/crate/snapshottable/latest): April 2026 port metadata, conditional transfer lead; no measured safety/performance result credited. [String-diagram proof application](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ITP.2026.28): outside this cost segment; a citation is not validation of Store.
- [DBLP article](https://dblp.uni-trier.de/rec/journals/pacmpl/AllainC0S24.html), [DBLP author](https://dblp.org/pid/239/4197), [general event profile](https://conf.researchr.org/profile/conf/basileclement1), [ICFP profile](https://icfp24.sigplan.org/profile/basileclement1), [CAMBIUM report](https://radar.inria.fr/report/2024/cambium/index.html), [PICUBE report](https://radar.inria.fr/rapportsactivite/RA2024/picube/PICUBE-RA-2024.pdf), [ORCID](https://orcid.org/0009-0005-2972-5181), [ResearchGate record](https://www.researchgate.net/publication/383150214_Snapshottable_Stores): duplicate author/publication/activity contexts, not extra independent works. The [Allain author page](https://clef-men.github.io/) disposition is reused unchanged.
- [AD Scientific Index](https://adscientificindex.com/scientist/alexandre-moine/5152331/) and [Rust discussion](https://www.reddit.com/r/rust/comments/1sltart/snapshottable_a_store_of_mutable_references_that/): secondary rankings/discussion excluded from mechanism and benefit evidence.

**Local decisions prepared, not yet submitted:** `nu_background_s150_20261001` has 32 decisions, 17 credited/15 excluded (eight duplicate, seven scope/conditional), thirteen full-text-stage entries (one complete paper, eleven complete source files, one partial proof file) and nineteen metadata/discovery entries. Provenance: one Scite, twelve ordinary source routes, nineteen web. One unchanged author-page decision is reused. The monthly limit prevents `report_citations`/`citation_report`; no accepted-count or clean-report claim is made. The ignored JSON decisions and pending marker preserve the exact submission set.

The reconstruction preserves low overhead and large sparse-update gains, while showing copying-favorable cases, finite proof/test scope, alignment selection and missing raw data. The source's operation counts differ from several printed workload descriptions; this does not establish a reproduced failure. Continue S151's immediate custom-operation dependency, then weaker B01/B10 and wider runtime frontiers.
