# S119 — Compositional coverage, implementation costs and proof boundaries

**Complete updated author-edition reading, 2026-10-01 HKT; no compiler/proof execution.** Sebastian Graf, Simon Peyton Jones and Ryan G. Scott, *Lower Your Guards: A Compositional Pattern-Match Coverage Checker*. Publication DOI [10.1145/3408989](https://doi.org/10.1145/3408989), PACMPL4/ICFP article107 (2020); the selected file includes later additions.

## Edition and coverage

Existing Zotero parent `YBATUYR4`, PDF `HHKDS82Q`, full note `H734543M`. The [author PDF](https://simon.peytonjones.org/assets/pdfs/lower-your-guards.pdf) has 39 pages and 877,488 bytes, SHA-256 `0679a56c6fffe63f62a251fc4e4fdd160abe28a9aa6282ab114eea561ec74081`. All39 pages, twelve numbered figures, Table1, unnumbered code/guard diagrams and the complete72-entry bibliography were read. Every numbered figure and the table were visually checked, together with the examples on their pages; opening identity had been checked at acquisition.

The [author publication page](https://simon.peytonjones.org/lower-your-guards/) explicitly says the linked version adds soundness and or-pattern sections after ICFP2020. The PDF's embedded creation/modification time is2024-03-29; its body mentions2021 proof work, a2023 reference, GHC9.12 or-patterns and four years of maintenance. The metadata timestamp is not a certified revision history. These additions are **not backdated to2020**, and the catalog's original thirty-page extent is not silently equated with this file or treated as nine supplementary pages. Unresolved cross-references in the author copy are retained as edition limits.

## Mechanism and source-convention implication

LYG separates desugaring, coverage analysis and diagnostics. Source patterns become small guard trees with RHS leaves, ordered alternatives and guarded subtrees. Guards bind values, test constructors or force evaluation. The uncovered function U carries only nondiverging fallthrough into later alternatives; A annotates successful RHS reachability and possible divergence. R then classifies accessible, inaccessible and removable redundant RHSs using an inhabitant/emptiness procedure.

This makes coverage depend on actual matching semantics. A RHS can never be reached while the containing clause still performs necessary evaluation. Removing it can change divergence or effects. Shared guarding evaluation may require retaining one inaccessible RHS even when several sibling RHSs are unreachable; classifying each leaf independently is insufficient. Newtype matching differs from data-constructor matching, strict fields can remove potential inhabitants, and GADT equalities can rule out constructor combinations before ordinary constructor enumeration.

Refinement predicates track type and term equalities, positive and negative constructor facts, and bottom/nonbottom information. Normalization maintains compatible constraints, possible inhabitants, variable representatives and constructor solutions. Negative facts avoid expanding every not-yet-matched constructor combination. Long-distance information carries the context of an enclosing match into nested matches, catching redundancies that isolated checks miss. Repeated view expressions can be identified, although the implementation's expression trie gives less equivalence reasoning than the general formulation.

The later or-pattern section (§4.9, pp.23–26) **explicitly motivates enumeration over a wildcard when a new constructor is added**. In its log-level example, the new Warning case should prompt a decision, whereas a wildcard silently supplies the old fallback result. This is a direct predecessor for the diagnostic mechanism behind D1, alongside S113's earlier discussion. The paper's preference does not measure a maintenance benefit and does not prove that the fallback result would be wrong. Both D1 baselines may initially cover every input, and a correct future fallback remains legitimate.

Or-patterns motivate guard DAGs: sequential and alternative guard combinations share a continuation instead of duplicating later patterns exponentially. A separate covered-set function is needed, while the core inhabitant machinery remains reusable. Syntax-specific guard-tree variants also improve correspondence to source RHSs and extraction of enclosing context. These are concrete compiler extensibility mechanisms, not a measured application-maintenance effect.

## Assumptions, approximation and effects

General guards and views can contain arbitrary computation; their coverage is undecidable in general. Fuel-bounded inhabitation treats unresolved cases as inhabited. The stated implementation uses100 iterations for list-like constructors and1 otherwise. A configurable model-count threshold, reported as30, drops selected refinements when splitting would grow too far. This deliberately overapproximates reaching values, trading precision for compiler resources. It does not change the worst-case underlying difficulty into a general polynomial completeness result.

Under a sound emptiness procedure, this overapproximation can report extra missing cases or miss redundancies; it must not dismiss a genuinely reachable RHS as removable. The guarantee remains conditional on the modeled language and implementation. Pattern synonyms may overlap; user `COMPLETE` declarations assert coverage that the compiler does not generally verify. The implementation also compromises by assuming strict pattern synonyms. These premises cannot be replaced with an unconditional no-warning-implies-safety claim.

Strict languages do not eliminate every subtlety. A guard can throw, diverge or perform an external effect even if its RHS is impossible. Such a clause may need to remain, and equating repeated effectful expressions as if pure is unsafe. The paper proposes adapting desugaring for this distinction; it does not implement or evaluate a C#/F# version in this study. Exhaustiveness also does not prove termination, intended results or fulfillment of temporal obligations.

## Mechanized dependency

The updated §7 summarizes Dieterichs2021. [S134's selected thesis/source reading](S134-lyg-proof-scope-partial.md) resolves its scope: exact fallthrough characterization and safe removal of the entire redundant set in an abstract guard model, with distinct RHS identifiers and a sound emptiness checker supplied as premises. The actual inhabitant generator is not proved correct there; types, source-to-guard correspondence and the compiler are not fully formalized.

The thesis corrects a variable-scoping ambiguity by introducing explicit nested bindings and contextual accumulators. It says the corresponding GHC encoding is unaffected. Four files at the thesis's pinned Lean3 revision corroborate definitions, theorem interfaces and dependency versions, without reading every imported lemma or rerunning Lean. This is useful mechanized support under explicit assumptions, not complete-compiler certification or independent reproduction.

## Evaluation and bounded arithmetic

The package survey considers361 head.hackage libraries, with minimal patches for a development compiler, and examines those with no coverage warnings under GHC8.8.3 that gain warnings under LYG. Seven libraries exhibit newly reported issues: pandoc/pandoc-types guard/term redundancies, geniplate-mirror enclosing-context redundancy, generic-data strictness, and Cabal/HsYAML/network intentionally retained debugging-like branches. These are seven **libraries**, not seven independent latent behavioral bugs or a representative estimate of defect prevalence. The selection does not comprehensively enumerate false negatives or every warning difference. The exact head.hackage revision is given, but its manifest was not recovered in this pass.

Table1 has **ten printed stress-test rows**, despite prose saying eleven. All ten rows and both measured outcomes were reconstructed. Nine favor LYG for desugarer time and allocation; T11276 is adverse. Examples retain their absolute units:

| Case | Desugarer milliseconds, GHC8.8.3 / pre8.10 HEAD | Allocated MB, old / new |
| --- | --- | --- |
| T11276 | 1.16 / 1.69 | 1.86 / 2.39 |
| T11822 | 1,060 / 16.0 | 2,010 / 27.9 |
| T11195 | 2,680 / 22.3 | 3,080 / 39.5 |
| T17096 | 7,470 / 16.6 | 17,300 / 35.4 |

The other six printed cases and percentage calculations are retained in the local reconstruction. Small differences between recomputed percentages and printed percentages can reflect undisclosed rounding. No missing eleventh row or new raw timing dataset is invented. These tests deliberately stress known bad cases, including user reports and Maranget-derived examples. They measure the **whole desugaring phase**, not an isolated checker intervention, total build time or runtime application memory. Allocation is not peak retained memory. Hardware, repeated-run uncertainty and a general package timing distribution are not supplied for this table. The authors attribute T11276's regression to a type-equality solver cost; no local rerun confirms that decomposition.

The paper reports more than thirty fixed coverage-related issues and favorable four-year maintenance experience. Those issue/experience reports are useful engineering evidence, without a measured developer-effort comparator or an independently verified count of all fixes. A higher-quality diagnostic can also expose deliberately retained dead code, requiring a supported workflow rather than automatic removal.

## Versioned correction and source inspection

Page30 describes `considerAccessible` as False and suggests using it in place of a false debugging guard. The [official GHC9.2.1 source](https://downloads.haskell.org/ghc/9.2.1/docs/html/libraries/base-4.16.0.0/src/GHC-Exts.html) instead defines it as **True** and documents warning suppression. Directly replacing the printed False guard would enable that branch, changing the described behavior. This source check corrects the example; it does not negate the valid use of a true suppression guard on a clause already unreachable for other reasons. Warning suppression and preserved behavior remain separate questions.

Two paper-linked GHC commits were resolved through the official GitHub mirror after GitLab web opens failed. Commit `1207576ac0cfdd3fe1ea00b5505f7c874613451e` (2020-09-10) describes source-shaped guard trees and a structural panic fix. Its metadata/file list, not all fourteen changed files, were inspected. Commit `fd7ea0fee92a60f9658254cc4fe3abdb4ff299b1` (2020-05-01) describes propagation of wrapper evidence and lazy constraint work after a T3064 regression. Its message/list and complete PmCheck patch were read; the other five patches were not. This corroborates integration work, without independently establishing the paper's T11276 timing/fix attribution or recovering the benchmark HEAD. No author code, compiler, proof or benchmark was executed.

## Search disposition and next question

G07 returns eleven incoming edges; SC50 requests `limit:20` and resolves all eleven supplied DOIs. The graph includes a publication/preprint pair for linked visualizations and an implausible2016→2020 edge for the session-type survey; the latter is not credited as a real citation chronology. Graph labels do not validate the linked methods or field coverage.

Two consequential methods are promoted with native records before continued body reading: S135, `10.1145/3763171`, tests actual pattern-match analyzers and could expose the gap between theorem and implementation; S136, `10.1145/3434336`, studies compositional program-level pattern safety and could change S114's first-order/expressiveness tradeoff. Their acquired editions and partial coverage are in the search ledger. Live typed holes, pattern algebra, total type classes, in-place compilation, visualization dependencies and Julia protocol checking remain conditional, not measured effects inferred from titles. Automatic inversion is outside this coverage/maintenance question. The complete bibliography additionally retains the SMT-guard, dependent/refinement and pattern-synonym routes when their assumptions become consequential.

**Unique:** unconfirmed; constructor-evolution diagnostics and modular checker architecture have explicit predecessors. **Valuable:** better diagnostics and large selected compiler-phase improvements coexist with an adverse case, supported suppression needs and unmeasured maintenance transfer. **Scientifically valid:** algorithm, approximations, proof scope and visible timing rows are reconstructed; compiler-wide guarantees, historical benchmark binding and ISE feasibility remain unvalidated. S135 is the next consequential implementation check, followed by extension/practice and the other live background themes. All experimental holds remain.
