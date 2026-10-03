# S236 — Workload-aware placement of coexisting writable schemas

**Complete accepted-manuscript reading, 2026-10-03.** Kai Herrmann, Hannes Voigt, Torben Bach Pedersen and Wolfgang Lehner, *Multi-schema-version data management: data independence in the twenty-first century*, VLDB Journal **27(4):547–571 (2018)**, [DOI 10.1007/s00778-018-0508-7](https://doi.org/10.1007/s00778-018-0508-7). Online publication **12 June 2018** and the August issue date are distinct. Native parent **`SW7VJFA6`** and note **`WJWPQGM9`**, in collection `PKLXQNEE`, were created before selected body reading after DOI/title and full-library duplicate checks.

| Source | Identity and actual coverage |
| --- | --- |
| Institutional [accepted manuscript](https://vbn.aau.dk/ws/files/310568148/KaiVLDBJrev.pdf), native attachment **`K2L794NP`** | **27 physical pages: two repository covers plus 25 article pages; 4,908,693 bytes**. SHA-256 **`c43f588546b350e993ddf399dc70a20dae992c11fadd7615b887bb5956196243`**; MD5 **`8c4dfd620411300ca812085f4d9f8d40`**. All 27 text and visual pages consumed, including ten sections, 19 figures, four tables, equations/rules through 41 and 27 references. There is no appendix in this manuscript. Local and native stored bytes agree. |
| Publisher and institutional metadata | Identity, authors, dates, volume and pages checked. The accepted manuscript calls itself post-peer-review/pre-copyedit, retains red revision text and publication placeholders, and writes “21st Century” in its title. The final publisher body has not been compared; its preview is not a full reading. |
| Scite body service | One response supplies characters **0–7,999 of 104,096**, `source:fulltext`, `contentDenied:false`, `hasMore:true`. This is partial service coverage. The acquired PDF supplies the complete reading. |

The covers' download dates **3 October 2026** and **9 September 2019** describe wrappers, not separate article editions. An introductory passage about sharing unchanged table versions appears on PDF physical page 4 but is omitted from the corresponding served opening text. The unconsumed remainder of the Scite body is not searched for it; the cause of the difference is unknown. The PDF governs this reconstruction.

No author implementation, database, benchmark, formal checker, container or model is executed. Own arithmetic only checks stated counts and ratios. The referenced thesis and other formal predecessors are not silently included in this reading.

## What the journal adds

Section 1.2 explicitly attributes the formal results to CoDEL, [S103's conference paper](S103-bidirectional-schema-versions.md) and the 2017 thesis. The journal consolidates the system and adds a **physical-design advisor**, including **partially and fully redundant** materializations. It is a later publication of the same research program, with inherited examples, measurements and formal methods—not an independent replication of S103.

S103's payload placement selected one side of an operation. The journal can persist **source, target or both**. Storing both removes some auxiliary-information work but introduces propagation between physical copies. Consequently, more redundancy can help reads and sometimes writes; its value depends on which auxiliary updates it replaces. There is no permanently materialized base schema outside this choice.

The logical contract remains several simultaneously readable and writable schemas, connected by declared BiDEL operations. A catalog shares unchanged table versions and represents transformations in an acyclic hypergraph. Each table version has one incoming and possibly several outgoing operations. Dropping a logical schema retains tables/data still needed elsewhere. The conference's `SPLIT` operation is called `PARTITION` here.

## Preservation and its boundary

Stable tuple identities, declared defaults, preferred replicas, hidden values, unmatched rows and membership/tombstone information support the two data-projected round trips. Overlapping partitions can have independent values: reconstruction prefers one replica while retaining the other in auxiliary state. A view's own write/read-back guarantee therefore does not imply that every other view sees every conflicting value.

The paper explicitly characterizes **propagation between schemas as best effort** and warns about applications that use multiple schema versions. Each schema is intended to behave like an ordinary single-schema database, using the DBMS's transaction guarantees; this differs from semantic agreement between every application view. SQL views and instead-of triggers implement access through nonmaterialized versions. Reads can take the cheapest path to stored data; writes may affect auxiliary state throughout the catalog.

Section 5 develops the `PARTITION` mappings. When both sides are stored, delta generation removes auxiliary-headed rules and auxiliary-positive rules, and drops negated auxiliary conditions from the remaining rules. Other operation proofs are referred to S103/the thesis. The **padding-domain admissibility question** recorded for S103's printed decomposition rules is not resolved by a new complete validity predicate here. This is a limit on a universal interpretation of the printed formal claim, not an executed implementation failure.

A small example also mixes predicates `prio=1` and `prio<=2` with a prose claim that priority-two tasks occur in both partitions (printed pp. 11–12); the predicates actually overlap at priority one. The formal mapping and explicit replica policy, rather than that inconsistent illustrative value, govern the reconstruction.

Relational completeness means expressing relational-algebra operations. The paper's practical-completeness argument is the represented Wikimedia history, not proof that all future schema changes are covered. Constraint evolution remains future work. **Zero-downtime migration also remains future work** in §10. Neither logical coexistence nor these round trips guarantees arbitrary live code migration, game queues/clocks, external-effect rollback or intended future behavior.

## Advisor inputs and algorithm

Section 7 gives the following concrete workflow and obligations:

| Component | Reconstructed method |
| --- | --- |
| Caller and objective | A DBA triggers the advisor, supplies a workload and storage threshold, reviews its proposed materialization and confirms migration. Minimize the sum of operation frequency times estimated cost over table versions and select/insert/update/delete operations, subject to valid coverage and the space cap. Unexposed internal table versions receive zero direct workload weight. |
| Calibration | Learn per-DBMS/hardware linear cost functions from synthetic tables. The independent variable is table size in bytes; tuple counts in figures hold the tuple shape fixed. Four direction/auxiliary-state cases summarize six source/target-access and source/target/both-storage scenarios. The selected example uses PostgreSQL 9.4. |
| Composition | Estimate a chain by combining operation costs and removing duplicated local-access cost. Added-column reads can require an auxiliary join in one direction but only projection in the other. An insertion through a join can scan its partner, so constant write cost is not universal. |
| Read-path selection | A nested shortest-path problem chooses the cheapest materialized access path. The stated monotone propagation-path costs permit Dijkstra-style search; writes instead propagate across the catalog as necessary. |
| Validity | Every logical table version must have a hyperpath ending at physical tables. For an operation with multiple opposite-side tables, all required tables must be covered. Recursive equation 39 is interpreted through this terminating-path definition, not as permission for circular self-support. |
| Global search | Table-version subsets grow exponentially. Six TasKy table versions give **59 valid placements**, including redundancy; Wikimedia has **203 table versions** and an approximately `10^61`-sized potential subset space. This is not enumeration of that many valid experiments. |
| Heuristic and stopping | Start with oldest/newest nonredundant, greedy partial and fully redundant placements. Evolve a population using local moves/copies/merges and coarser random toggles; discard high predicted costs. Stop at a maximum number of considered placements or a no-improvement bound. |

Monotone costs **along a propagation path** do not make the overall placement objective monotone: adding a physical copy changes both read paths and write propagation. The heuristic has no global-optimality guarantee. The article does not supply a full population/seed/mutation-parameter packet for independent reproduction.

The objective is workload execution cost under a storage constraint. Calibration, advisor search, physical migration, DBA review and system adoption remain distinct costs; they are not all included in a single end-to-end maintenance-benefit measure.

## Inherited evaluation, with corrected units

The evaluation uses single-thread PostgreSQL 9.4 on a **2.4 GHz Core i7, 8 GB RAM**, the authors' **100,000-task TasKy** example, and **14,359 Akan Wiki pages with 536,283 links** loaded at the 109th historical schema. These repeat S103's lineage.

Table 2 retains **three BiDEL versus 359 SQL evolution lines** and **one versus 182 migration lines**, alongside statement and character counts. The journal correctly prints evolution's **119.67** line ratio and emphasizes migration's **182** ratio. These are substantial authored-code reductions, not measured human effort or defects. Example creation/evolution times remain **154/230/177 ms**; generated-code overhead is again described both as up to 4% and 4% on average.

Table 3 represents **171 Wikimedia schema versions using 209 operations**: 42 create-table, ten drop-table, one rename-table, 93 add-column, 20 drop-column, 37 rename-column, four decompositions and two merges; no partition or join. S103 instead reports 211, with different column-operation counts. The accounting change is explicit and not pooled as another dataset or a demonstrated correction whose cause is known.

Figures 13–15 preserve favorable placement results. The changing-workload example includes migration cost across a million statements, but its switches are instructed when another placement becomes faster; it is not an autonomous-advisor deployment trial. The **49-fold** TasKy2 write contrast concerns physical placement. The long-history comparison reaches two orders of magnitude; Figure 15's terminal `v25636` label still differs from the prose's `v25635`. Read, insert-only and mixed workloads are separate conditions.

## Added cost-model and advisor results

**Calibration and prediction (§8.4, Figures 16–17).** Training uses 50 sizes from 1,000 to 100,000 tuples and takes **under ten minutes**. The two-operation evaluation uses 50 sizes from 5,000 to 100,000, with `ADD COLUMN` second in the displayed examples. The authors report roughly **5% mean error**, near-zero write error and about 10% read error; Figure 16 includes larger signed deviations, notably partition/delete and merge/read. The printed ranges overlap calibration; a disjoint-size holdout is not established.

Across TasKy's 59 placements, reported error is **14% for reading Do!** and **24.2% for mixed access**. Figure 17 preserves the read ordering in the displayed case; mixed estimated points visibly cross in rank despite a broadly useful trend. Approximate ranking is useful without converting these results into uniformly sub-10% prediction error.

An actual candidate measurement takes **8.21 s to migrate plus 33.32 s to measure**, totaling **41.53 s**. Measurement covers 12 schema/operation combinations, each executed five times. A cost prediction takes **132.56 microseconds**. The stated `2.5×10^5` factor matches measurement alone (own arithmetic about 251,358); including migration yields about 313,292. Either comparison supports very fast estimation, while calibration and total search remain separate.

**Small-system optimizer (§8.5, Figure 18).** Seven nonempty subsets of the three schemas, crossed with read-only, 50:50 read/write and write-only workloads, give **21 conditions**. For each, the figure compares the actual best over all 59 placements, the advisor's proposal, the best nonredundant placement and the worst placement. Its boxed millisecond labels belong to the **worst** bars, as the legend shows.

The advisor's proposal is **never more than 10% slower than the optimum in these tested conditions**. This qualifies the earlier prose promising the optimal solution: it is near-optimal here, not necessarily exact. Reported worst/best contrasts reach fivefold for reads and thirtyfold for writes; the best nonredundant placement can be tenfold slower than a suitable partial-redundancy proposal. Removing auxiliary-update work explains why selected redundant placements can also improve writes. The paper does not measure DBA decision time.

**Long-history optimizer (Figure 19).** One illustrated run considers **429 evolved members in 828 ms**, stopping after 30 steps without significant improvement. Physically applying the proposal changes measured workload execution from **2.35 s to 0.26 s**: own arithmetic **9.04-fold**, or **88.94% lower**. The paper's tenfold figure is the estimate. The workload mixes reads and writes on the 28th and 171st schemas; its precise mix and raw search packet are not supplied here. The global optimum is explicitly unknown.

These are meaningful positive measurements of the advisor and its cost model. They are not independent production replications, a universal latency bound, net lifecycle savings, or evidence that Nu/F# state representation causes a maintenance benefit.

## Consequence and next action

For B02/B08, S236 strengthens the distinction between a view's admissible data round trip, cross-view conflict visibility, and live program behavior. For B06/B10/B12, it resolves S103's absent automatic-selection method with a calibrated, bounded heuristic and measured improvements. The contribution remains useful while its shared dataset, computation/measurement denominators, DBA confirmation and cost boundary remain explicit.

The next consequential comparison is **S102 Cambria**, whose document-schema and patch-translation workflow is only partially read. It can clarify which defaults, complements and update policies survive beyond a centralized relational DBMS, and what concurrent document evolution adds. S87 Denicek, modern .NET/game evidence and type/context/multi-turn methods remain independent frontiers. The thesis is a conditional dependency for a more general formal or calibration claim; this paper does not require an indiscriminate neighboring-citation expansion.

SC153 returns one exact record with three **outgoing** citation statements from S236 to DOI `10.1007/s00778-012-0302-x`: constraint evolution, PRISM/PRISM++ forward migration, and the relation to earlier evolution languages. One sentence names two references but the returned edge identifies only one. The 16 mentioning statements/25 citing-publication tallies are not incoming validation or a reviewed graph. W454–W459 locate the accepted manuscript through its exact public `/ws/files/` URL after other routes fail; publisher preview, a LibKey HTML response and inaccessible project routes are not additional bodies or artifacts. The ledger records the bounded search and decision audit.
