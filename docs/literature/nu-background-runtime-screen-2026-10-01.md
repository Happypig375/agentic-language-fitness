# Functional persistence and runtime-method continuation

**2026-10-01 HKT; in progress.** This B04/B06/B12 segment follows the weaker cost coverage identified by the [GPT-6 Pro review](../supervisor-review-2026-09-30.md). It extends C11 rather than replacing the wider [survey](nu-background-survey-2026-09-30.md). Collection layout, retained history, collector latency, workload context and maintenance effort are distinct questions. No theme is declared surveyed and no experimental work is authorized.

## Promoted records and actual coverage

Records were created/reused through Zotero 10's native API before intended body reading. Downloaded PDF bytes were read back from native attachments and hash-verified. Keys are parent / PDF / note; none of these PDFs or raw artifact files is committed.

| ID / primary identity | Native identity and edition | Reading state and live implication |
| --- | --- | --- |
| S143 CHAMP, [10.1145/2814270.2814312](https://doi.org/10.1145/2814270.2814312) | `34J3MDAP` / `6SIYJNYL` / `RX46EDUI`; CWI PDF, eighteen pages, 562,242bytes, SHA-256 `1bb08cc704281dcb0432d666aa37a9259f7ed69c6a1f30068459c165e34be436` | [Complete](full-reading/S143-champ-immutable-collections.md); all figures/tables, bounded pinned source and cached data arithmetic. Notices DOI `10.1145/2858965.2814312` is the same publication lineage. Positive representation costs coexist with slower operations and hash-policy effects |
| S144 Alligator collector, [10.1145/3381898.3397214](https://doi.org/10.1145/3381898.3397214) | `KTSUUDH9` / `JA2HIJDF` / `2AEVVKXW`; [institutional author PDF](https://www.cs.unh.edu/~dietz/papers/gamari2020alligator.pdf), thirteen pages, 527,541bytes, SHA-256 `effb875367bc8b565af3b0c721fd1aaf3292285cad75d38fc98cc3d345bd9ecd` | [Complete](full-reading/S144-alligator-collector.md); all thirteen pages, bounded source/notebook and selected design reading. Large major-pause gains coexist with higher minor pauses/CPU and unresolved release correspondence |
| S145 Counting Immutable Beans, [10.1145/3412932.3412935](https://doi.org/10.1145/3412932.3412935) | `JPGFLE52` / `7T475K65` / `U9NS75IB`; [KIT author PDF](https://pp.ipd.kit.edu/uploads/publikationen/ullrich19counting.pdf), twelve pages, 621,450bytes, SHA-256 `357f5e70164cdba0c0ba2ea1fbf6e0f51306468956cfff9486d4930a05e11589` | Acquired/body-unread. Reference-count-driven reuse, borrowing, sharing and retention are the live questions. Publication/preprint `1908.05647` correspondence remains to inspect |
| S146 Misleading Microbenchmarks, [10.1145/3748522.3779882](https://doi.org/10.1145/3748522.3779882) | `VY9YK2V2` / `NA4A53G2` / `MHKM8JJH`; arXiv `2605.23570v1`, nine pages, 674,406bytes, SHA-256 `20d07b7b149b1cb15c169bbad80ad6a957cc1eb1d9861f227dfa07d2333c4851` | [Complete author edition](full-reading/S146-jvm-benchmark-context.md); six figures/two tables. Profile-context intervention changes a hash-implementation ranking and other timings. No CHAMP rerun or exact artifact recovered |
| S147 Bad JMH Practices, [10.1109/TSE.2019.2925345](https://doi.org/10.1109/TSE.2019.2925345) | `GP4BQG7X` / no PDF / `2H26NKVR`; seventeen-page author manuscript accessible only as cached text; direct transfer resets and screenshots fail | [Partial](full-reading/S147-benchmark-practices-partial.md). Selected selection/rule/table passages and pinned artifact clarify that CHAMP was excluded from impact testing; most exported artifact warnings concern bundled JMH code. Broader study methods/results and final-issue correspondence remain incomplete |

Current holdings after these additions: **166 live parents = 163 literature + three public source records, 177 PDFs in seven subcollections**. Other existing attachment types remain. Complete-paper coverage is **114 works = thirteen P + three A + 98 S**; S147 is not in that total. Native S143/S144/S146 complete notes and S147 partial note reflect the canonical reconstructions.

S144's later design-supplement attachment `TEQG3DG7` accounts for the177th PDF, not another publication:31 pages,576,273bytes, SHA-256 `5a943ea0c9e5718c5ca43d801bf19fbdd44e681b1ef56643650ea9bdcf6daf46`. Selected pages1–3 and21–28 were read. Its canonical note records the pinned repository, ten complete source/config/doc files and33/83 notebook cells; missing raw inputs/launcher and changed saved Table2 values remain unresolved. Paper coverage and artifact reproduction are separate.

## S144 follow-up, 2026-10-01 HKT

| Route | Request / actual return | Disposition |
| --- | --- | --- |
| G19 | Incoming S144 DOI, depth1, cap150, snippets; five edges/six nodes, seed count5, no truncation or low-coverage flag. Same result verified by a repeated read; no additional discovery count | All titles and supplied contexts read. OCaml parallelism `10.1145/3408995` is a conditional runtime alternative; `10.17863/cam.56842` repeats its institutional edition. `10.1145/3473568` adapts Alligator for nonvolatile persistent STM, not retained functional versions. Code rationalization `10.1007/978-3-030-99584-3_11` and hardware collector Cloaca `10.1145/3677999.3678277` remain conditional; no full-method or independent-replication credit |
| SC82 | Four distinct non-Cambridge G19 DOIs plus the two Ueno foundation titles in one request, `limit:20`, offset0; four/four DOI records returned | The DOI filter did not return the title-only foundations. This is not six matched methods; title lookup was reformulated separately |
| SC83 | Exact titles *An efficient non-moving garbage collector for functional languages* and *A fully concurrent garbage collector for functional programs on multicore processors*, `limit:20`, offset0; four/four records | 2011 conference/Notices `10.1145/2034773.2034802` / `10.1145/2034574.2034802`;2016 conference/Notices `10.1145/2951913.2951944` / `10.1145/3022670.2951944`. Two underlying works, conditional foundations. No body/proof borrowed; edition notices are not corrections. Returned exact-identity set accounted, not field exhaustion |
| W160 and ordinary primary-file access | Author GitHub repository open; API pin `048f000e1261e86701e9a010bb48cbc1ed51f17b`,41 tree entries, twelve selected downloads | Main paper complete, design/notebook partial, ten other files complete. No build, notebook execution or runtime reproduction. Blank additional-results link and absent run/data files limit the released reproduction path |

Audit `nu_background_s144_20261001` records23 decisions:13 credited and10 excluded, comprising six conditional scope decisions and four duplicate identities/routes. Full-text-stage13 means one complete paper plus twelve bounded artifact files, including partial PDF/notebook coverage; it is not thirteen papers. Provenance: ten Scite, twelve ordinary pinned-file reads, one web locator. Report inspection found zero missing reasons, no unlinked-retrieval warning, no truncation and answer-scoped retrieved count null. S144's inclusion advances its earlier acquisition state; unchanged earlier screens were not submitted again. The repeated G19 verification produces no extra source decision.

The next acquired primary dependency is S145 reference-counted reuse. The broader .NET/game, retained-history and workload frontiers remain open alongside the other B themes. S144 establishes scoped latency benefits and explicit adverse costs, not a source-purity effect or Nu comparison. No experimental hold changes.

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

**Unique:** broad persistence and context-sensitive measurement mechanisms have predecessors; Nu/D1 priority is unconfirmed. **Valuable:** CHAMP supplies positive collection/application measurements with slower cases; S146 demonstrates consequential context sensitivity. Net Nu benefit, retention and latency remain separate empirical questions. **Scientifically valid:** complete S143/S146 and bounded S147/data reconstruction clarify what can be concluded; they do not reproduce timings or validate ISE apparatus. Continue S144/S145's primary methods, then the consequential representativeness/retention leads while preserving other B01–B12 gaps.
