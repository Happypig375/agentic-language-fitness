# S113 — Coverage, redundancy and divergence in GADT matches

**Complete extended-author-version reading, 2026-10-01 HKT; bounded source inspection, no compiler reproduction.** Georgios Karachalias, Tom Schrijvers, Dimitrios Vytiniotis and Simon Peyton Jones, *GADTs meet their match: pattern-matching warnings that account for GADTs, guards, and laziness*, ICFP2015,424–436. DOI [10.1145/2784731.2784748](https://doi.org/10.1145/2784731.2784748).

## Identity and actual coverage

Zotero parent `J6N99GLC` preceded body reading. The [author PDF](https://people.cs.kuleuven.be/~tom.schrijvers/Research/papers/icfp2015.pdf), attachment `MWMCRPVB`, is a **fourteen-page extended version**, with a placeholder DOI, rather than a certified copy of the thirteen-page final layout. Size434,542 bytes; SHA-256 `f886370b8fae64cbd4fe454f26d6aa060b398a374bdbcf4a72a47df0109be816`. All fourteen pages, seven figures, main Table1, AppendixA's size table, both appendices and39 references were read. Formal diagrams/rules, evaluation/code and both appendices were visually checked against extraction. Full note `JNABSH85` records this scope. SIGPLAN DOI `10.1145/2858949.2784748` belongs to the linked publication lineage; it is not an independent study.

The reading resolves a B02/B07/B10 distinction: what a missing-case warning establishes, when an unreachable right-hand side is removable, and why an unnecessary fallback can hide later constructor additions. Compiler comparisons below concern the paper's historical implementations, not present-day GHC or F#.

## Mechanism and formal limits

The paper gives direct maintenance motivation (§2.2): an imprecise checker can induce programmers to add an error catch-all to silence a false warning, after which a future constructor is silently covered by that branch. This is prior articulation of the diagnostic-opportunity mechanism, not an evolution experiment. A correct fallback remains a legitimate implementation; the paper does not establish that all catch-alls are harmful.

Ordered lazy matching requires three distinct outcomes for each clause:

- **C:** matching succeeds and the right-hand side can be reached.
- **U:** matching fails without divergence, so subsequent clauses are tried.
- **D:** matching diverges, preventing later clauses from being tried.

Only U flows to the next clause. Empty final U means no fallthrough pattern-match failure for the modeled inputs; it does not guarantee termination, a correct right-hand side, or intended event/state behavior. A clause is safely redundant when both C and D are empty. C empty with D nonempty means an inaccessible right-hand side whose removal can change strictness and program behavior. The paper's Boolean example makes this concrete: a middle `True False` clause can diverge while inspecting a bottom first argument, even though an earlier clause already covers every successful match of that pattern.

The algorithm carries symbolic value abstractions with a typing environment, constructor/variable vector and constraints. C/U/D rules refine these sets; a satisfiability oracle removes impossible abstractions. The oracle must be conservative: rejecting an abstraction must imply that it denotes no value. Unknown constraints stay possible. This supports sound absence of missing-case warnings and sound redundancy/inaccessible-RHS reports, while permitting false missing-case warnings or missed redundancy when the oracle is weak. Dropping constraints can preserve soundness while losing precision.

GADT type equalities prune impossible constructor combinations. Bottom matters: an apparent mismatch between indexed constructors does not by itself prove that evaluating an earlier argument cannot diverge. Generalized pattern guards accommodate view patterns, literals and other source forms; AppendixB preserves forcing order when translating bang patterns and defers lazy bindings. The expression denotation and constraint-entailment details are left implicit in the stated theorem. The denotational correspondence argument is not an independently checked mechanized proof or proof of the concrete GHC implementation.

Signatures and enclosing matches can supply constraints to nested matches. The implementation propagates **type constraints only**, although the framework could propagate term constraints too (§4.6). Its term oracle recognizes only simple Boolean facts: an explicit `otherwise` can be resolved, but complementary arithmetic guards need not be. Thus the framework's expressiveness is wider than the demonstrated guard reasoning. Its historical placement after type inference and before desugaring preserves source-oriented diagnostics. The504-versus588-line comparison concerns one checker component, not net integration effort or user comprehension.

Worst-case symbolic expansion is exponential. Incremental constraint solving and state sharing are described optimizations; the paper does not measure a general compile-time benefit. Lazy Haskell semantics, GADT inhabitation and the selected oracle do not certify F# active patterns, effects, null behavior or any particular target compiler.

## Selected-corpus results

The authors asked Haskell library users for examples with GADT warning problems, yielding nine Hackage packages and three GitHub examples. This is a deliberately problem-enriched corpus, not a representative random sample or a controlled maintenance comparison. Table1 compares the old checker without a GADT workaround (GHC1), with it (GHC2), and the new implementation.

All twelve rows were transcribed and checked. Summed results are:

| Printed quantity | GHC1 | GHC2 | New |
| --- | --- | --- | --- |
| Missing-case reports |107|51|24|
| Redundancy reports |0|0|38|

The corpus totals20,804 reported source lines. Relative to GHC2, missing-case reports decrease by27; the new checker adds38 redundancy reports, which the authors identify as catch-alls introduced to suppress earlier warnings. These are diagnostic counts, not38 independent maintenance tasks or measured avoided defects. Remaining false warnings in accelerate/d-bus concern guard/view reasoning beyond the implemented term oracle. No observed guard benefit is established simply by the generalized formalism.

Three faulty warning-suppression examples are reported; one equality-witness example is explained in the paper. A witness inspected too late can allow divergence before an allegedly impossible case is ruled out. Moving that witness match changes the evaluation order; the argument is not a blanket license to delete unreachable-looking clauses. The claimed closure of nine compiler tickets is not independently audited here. No corpus example of an inaccessible-but-irredundant right-hand side was found; that does not establish population rarity or absence.

AppendixA records8,888 pattern matches by the maximum C/U set size encountered for each match:8,702 in1–9,181 in10–99, and5 in100–2,813. Recalculated shares are97.907%,2.036% and0.056%. This is a distribution of **per-match maxima**, not every intermediate set and not elapsed compilation time. The stated95%-plus fraction at size1 or2 lacks finer released counts. The text assigns the five largest cases to ad while its footnote names an accelerate module; that locator inconsistency remains unresolved. No raw match-level data, exact evaluated package versions or historical checker commit was recovered.

## Bounded public-source corroboration

W97 followed the three GitHub footnotes. The first URL failed in the web cache; ordinary pinned raw-file access succeeded. Four complete files were read, with no build, dependency installation, author code execution or warning rerun:

| Source and pinned revision | Complete inspected file; bytes / SHA-256 |
| --- | --- |
| [Heterogeneous-list example](https://github.com/gkaracha/gadtpm-example/tree/84cae9559549ee42bb6f88a8579f2a558b746785), commit dated2015-02-27 | `ErikHesselinkExample.hs`,50 lines,921 bytes; `4a4dabd4af051a48d4e5790be549edd317babf7961cb55484329056e2204af9d` |
| [Indexed-list example](https://github.com/amosr/merges/tree/bf8cb7bca2d859977d6fb8bf4a9d07ac780b7edd), head dated2017-07-13 | `stash/Lists.hs`,94 lines,2,100 bytes; `5d50a33dc47ea9b858e3b5682c604fc18b0a6f707d1520d273c9b85b7f06612e` |
| [Heap tutorial](https://github.com/jstolarek/dep-typed-wbl-heaps-hs/tree/0d6e354cbb71056a3eb9df9ebdc788182e137d1d), head dated2018-06-14 | `README.md`,81 lines,3,526 bytes; `41e495300856cf468c225fb3a91cf69fc77ffdb5e4255207af2bb78f463c7d07` |
| Same heap revision | `dep-typed-heaps-hs.cabal`,48 lines,1,956 bytes; `6bc21ed85b5b0648a0b7ecf8cf1c7b4374be18ac5fa6a25267c54c089914067e` |

The first two files contain respectively two and three error fallbacks after indexed-list cases, corroborating the source convention. They do not independently establish the paper's redundancy classifications. Physical line counts are not assumed to equal Table1's LOC convention. The heap README calls the project a tutorial/technology demonstration and disclaims intended production use; its configuration labels it experimental, depends on base and requests `-Wall`. The README lists historical GHC7.6.3/7.8.3 testing. No heap implementation module was read. Later pinned heads are not silently treated as the2015 evaluated corpus.

An inferred cabal filename returned404; the repository tree resolved the actual filename above. An anonymous API rate limit was handled through the existing authenticated read-only GitHub CLI. Neither event remains a paper-access blocker. The entire source corpus and historical branch were not reconstructed.

## Implications and next consequential readings

S113 establishes a concrete prior mechanism linking checker precision, fallback conventions and future diagnostic opportunity. It also shows why match coverage, branch removability and intended behavior need separate records. A warning-free match can compute the wrong result; an unreachable right-hand side can still affect evaluation. Proposed D1 comparisons therefore need site-level warning opportunity and independent old/new behavior, with correct fallback/reorganization allowed. No pure-versus-imperative, F#-versus-C#, Nu or agent effect follows.

The full bibliography was examined. [S114 Catch is now reconstructed](S114-partial-sufficient-matching.md): whole-program reachable-input sufficiency differs from locally covering every well-typed input. Its primary paper and pinned README identify Yhc Core, correcting this paper’s §8.5 characterization as GHC Core; the later README describes a GHC port as prospective. Acquired S119 is the compositional successor needed to understand algorithm/cost changes. Maranget's earlier coverage method, refinement/contract checking and the indexed-language predecessors remain conditional primary readings where their assumptions can change a live claim; S113's related-work characterizations are not substitutes for reading them. Extensibility methods S115/S118 and practice S116 remain open alongside contrary typing tasks and Join Token.

**Unique:** unresolved; the fallback/evolution diagnostic mechanism has an explicit predecessor. **Valuable:** improved diagnostics and concrete source examples are established in a selected corpus; maintenance benefit, prevalence and Nu/agent transfer remain unmeasured. **Scientifically valid:** the paper's formal and implementation boundaries are reconstructed, with static corroboration and historical-version limits; ISE feasibility remains unvalidated. No theme or experimental hold closes.
