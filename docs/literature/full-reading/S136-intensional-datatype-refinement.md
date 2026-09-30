# S136 — Intensional datatype refinement and program-level match safety

**Reading completed 2026-10-01 HKT.** Eddie Jones and Steven Ramsay, *Intensional Datatype Refinement: With Application to Scalable Verification of Pattern-Match Safety*, PACMPL 5/POPL, article 55 (2021), [DOI 10.1145/3434336](https://doi.org/10.1145/3434336). This supplies B02/B07 with a program-level safety method distinct from S119's local coverage analysis and S135's analyzer validation. It also supplies a concrete analysis-cost boundary for B06/B12.

## Acquisition, editions and actual coverage

Existing Zotero parent `MB7MAPR7` preceded body reading. The [Bristol publisher copy](https://research-information.bris.ac.uk/ws/portalfiles/portal/265849562/3434336.pdf), attachment `YYJNXUNY`, is 30 physical pages: one repository cover and29 article pages. All were read, including all nine figures, Table 1 and the three bibliography pages. All figures and the table were visually inspected; additional formal/example pages were rendered to resolve extraction ambiguities. The 477, 333-byte file has SHA-256 `9ed8ff952473279fd05fc1f3128f043702684e5b78685be2679a914bdfd106ce`.

The wrapper gives a reversed title and DOI`10.1145/3445980`, while the article, Crossref and arXiv identify`10.1145/3434336`. The former Crossref lookup returned404 in the acquisition pass. Keep the wrapper discrepancy visible; it does not establish a second publication. The article's Available/Functional/Reusable badges are publisher claims, not this pass's reproduction.

The publisher file refers to appendices it does not contain. [arXiv v3](https://arxiv.org/abs/2008.01452v3), dated 2020-11-25, supplies them: 50 pages, 583, 370 bytes, SHA-256 `93ad93bb48af8943eb7411f8d0d832d5e30803c2cf7b5ef8b46cacbdcb749a91`. It is attached to the same parent as `BHVGYC3P` after native API upload/hash readback. **All appendix pages 30–50 were read and visually inspected**, covering A–G, the proof arguments and all 334 module rows in ten package tables. Its earlier29 pages were not independently reread or certified identical to the publisher edition. The combined claim is complete publisher coverage plus complete v3 appendices, not two independently read publications. Full reconstruction note: `VZBSTGLH`.

Additional passive scope: six complete files at [public repository commit`ce6e7f5069530ea21a3e19c8e9e17fc23dc8e66c`](https://github.com/bristolpl/intensional-datatys/tree/ce6e7f5069530ea21a3e19c8e9e17fc23dc8e66c), dated 2020-08-05: README, Cabal file, `src/Intensional.hs`, `benchmark/Benchmark.hs`, `src/Intensional/InferCoreExpr.hs` and `src/Intensional/FromCore.hs`. The untruncated tree has 41 entries. Remaining source modules/tests were not read or executed; this is not an implementation audit.

## Mechanism and guarantees

Local coverage asks whether patterns cover a function's declared input type. Program-level safety asks whether any actual call can reach a missing case. In §11's example, a function defined only on `True` fails a `Bool` coverage check but can be safe if every caller supplies `True`. Neither property establishes termination or correct returned behavior. A successful catch-all can satisfy both while producing behavior inappropriate for a newly added case.

The motivating normal-form conversion composes `nnf` with a partial `nnf2dnf`. Constructors `Not` and `Imp` are absent from the latter's accepted fragment. A refinement records their absence throughout the recursive datatype; the intermediate producer's inferred type establishes the consumer precondition. The README also shows a faulty producer that lets `Not` escape and an input that does not exercise that faulty path. These are illustrative examples, not measured maintenance tasks.

Starting with an already typed ML-style program, the method constructs refinements by erasing selected constructors from each datatype definition. Constructor argument definitions otherwise stay fixed. Structural subtyping includes contravariant function arguments. Environment-level intersections let one function be used at multiple refinements; constrained refinement polymorphism represents these possibilities compactly. Guarded constraints make inference path-sensitive: a branch contributes only if its constructor is possible. Exhaustiveness is required with respect to the refined scrutinee type.

The formal language has first-order datatype definitions, explicit underlying type applications/annotations and one-level case patterns after desugaring. Recursive definitions are allowed; mutually recursive groups are omitted from the presentation but handled together by the prototype. Underlying typing and preprocessing are inputs, not costs solved by this refinement algorithm. Unknown library functions receive conservative underlying-type information; their own safe implementation is a separate assumption.

Sections 6–9 reduce subtyping and expression/module inference to guarded constructor-set inclusions. Saturation applies transitivity, guard satisfaction and weakening. Unsatisfiability is exposed by an unconditional constructor-membership contradiction. Crucially, **saturate before discarding internal variables**: Theorem 32 says that a solution over the retained interface extends to the full saturated system. Example 31 explicitly shows why restricting an unsaturated system loses a necessary condition.

The interface comprises refinement variables free in the environment and result type. Generalizing module-level definitions prevents their internal variables accumulating in later summaries. Theorems 23–25 concern sound/complete inference **relative to this refinement type system**; they do not decide safety for arbitrary programs. Appendices A–F supplies coinductive subtyping arguments, inference induction, a partial-solution extension construction and the complexity calculation. These arguments were reconstructed, not machine checked. They do not certify GHC Core translation or every prototype feature.

There are visible presentation defects: Example 5 adds an `Arith` argument to a constructor declared nullary in Example 2; Definition 9's second subtype-equivalence conjunct is reflexive instead of the expected reverse inequality. Several appendix proof lines retain mismatched symbols/labels. These were checked against rendering rather than silently repaired. They warrant care in a literal formalization; this reading has not established a counterexample to the intended method.

## Expressiveness and cost boundaries

The restriction is substantial and understandable. Constructor erasure throughout a recursive ordinary list can describe empty lists, infinite lists or the original datatype, but **cannot describe finite non-empty lists in general**. Dropping the empty constructor recursively also drops the finite tail terminator. Section 12 proposes separately unfolding the outer list definition to enable that invariant; it is future work. Base-value predicates and arbitrary relational invariants are outside this system. Refinement failure therefore need not mean a runtime defect.

Let N be the number of function definitions, S their maximum size, K the largest constructor count, D the largest datatype-dependency slice, Q the largest underlying type and M the maximum case nesting. Appendix F uses V=M+2Q and derives

`O(N S K^5 V^4 D^2 × 2^[K(VD(K+1)+2)])`.

The linear-in-N corollary fixes the other dimensions. The derivation also assumes the described normal form and bounded nesting/type growth. Its V is the bound on interface variables; Table 1's V counts **all generated refinement variables**, a different statistic. Compositional summaries alone would not guarantee efficient analysis; their bounded interface is the critical restriction. No rival-tool comparison or maintenance-change series estimates the practical advantage of this architecture.

The implementation saves interface binaries for separate module compilation. That is a concrete reuse mechanism. The reported benchmark analyzes modules independently; it does not measure incremental invalidation, turnaround after evolving a datatype or interactive editing. Public source loads available dependency summaries from `interface/<module>`, uses ordinary GHC recompilation unless its force option is supplied, and saves exported schemes afterward. Correct version/invalidation handling across changing packages is not established by these observations.

## Evaluation reconstruction, including positive and adverse results

Section 10 reports a 2.20 GHz i5-5200U machine with 8 GB RAM, averages across ten runs per module and sums of module times excluding startup. Table 1 has **ten packages**, including `pretty`, which is absent from the preceding nine-bullet package list. The table is incorrectly called Figure 1 in the prose; the actual Figure 1 is the normal-form example.

| Package/version from appendix | Included modules | N | Generated V | Largest interface I | Warnings in Table 1 | Reported package time, ms | Sum of rounded appendix times |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| aeson 1.5.2.0 | 24 | 728 | 20, 466 | 14 | 0 | 79.37 | 79.34 |
| containers 0.6.2.1 | 33 | 1, 792 | 25, 237 | 23 | 18 | 118.26 | 118.28 |
| extra 1.7.3 | 20 | 332 | 5, 438 | 7 | 0 | 61.53 | 61.54 |
| fgl 5.7.0.2 | 29 | 700 | 18, 403 | 12 | 8 | 94.32 | 94.32 |
| haskeline 0.8.0.1 | 27 | 1, 384 | 29, 389 | 27 | 0 | 111.67 | 111.65 |
| parallel 3.2.2.0 | 3 | 110 | 959 | 18 | 0 | 10.18 | 10.19 |
| pretty 1.1.3.6 | 6 | 222 | 3, 675 | 16 | 11 | 23.86 | 23.86 |
| sbv 8.7.5 | 139 | 5, 076 | 171, 869 | 46 | 79 | 518.91 | 518.93 |
| time 1.10 | 43 | 484 | 9, 753 | 10 | 9 | 134.16 | 134.13 |
| unordered-containers 0.2.11.0 | 10 | 474 | 7, 761 | 24 | 2 | 30.56 | 30.56 |

Independent arithmetic over all 334 printed rows reproduces **every N/V sum and K/D/I maximum**. Totals are11, 302 N and292, 950 generated variables; 41 rows have N=0. Rounded times sum to 1, 182.80 versus 1, 182.82 for the package table. Individual differences up to 0.03 fit the rounding of module averages and are not evidence of an inconsistent experiment. The displayed module range is 1.77–19.58 ms. These are printed aggregates, not the ten-run raw measurements or a fresh performance run.

The positive finding is small reported analysis time and much smaller retained interfaces than cumulative variable creation for these retained modules. The adverse case is explicit: generated `Data.Sequence` has six mutually recursive functions, complex types/deep matching and an interface above 80 variables; it did not finish in the authors' acceptable small time and was **omitted**. No numeric timeout or omitted runtime is supplied. This directly illustrates sensitivity to dimensions held fixed by the linear corollary.

Warnings total 127; 70 of sbv's79 occur in one function. The authors found **no true positives**, attributing warnings to conservative handling of unsupported features and module encapsulation. This is useful negative evidence about diagnostic precision on the selected mature packages. It is not127 independent bugs, a measured sensitivity estimate, a formal safety certificate for every package or evidence of no safety bugs in Hackage. There is no seeded-fault benchmark, comparison with existing analyzers, user-effort study or uncertainty interval here.

## Prototype, timing and artifact limits

The formal fragment and prototype differ. Higher-ranked/existential types, casts/coercions and type classes are not fully treated; the README also names GADTs. Non-home-package datatypes such as standard `Maybe` and `Bool` are not refined. Single-constructor types cannot receive empty refinements. Safety is therefore conditional on safe dependency use and supported features. The inspected source exposes these boundaries through ambiguous/base representations, conservative unknown-function output, skipped derived bindings and GHC's bottoming-expression analysis. It can treat an explicit `error` fallback as potentially unsafe rather than accepting it just because syntax covers every constructor.

There is an **unresolved measurement-version issue**. In the inspected August 2020 source, `Intensional.hs` samples `getCPUTime` around `runInferM`, after loading interfaces and before printing errors or saving summaries. This measures a bounded CPU-time interval, not whole compilation or interactive wall time; evaluation forcing has not been independently audited. The companion formatter divides raw differences by1, 000, 000 while labeling them milliseconds. [GHC 8.8.3's own CPUTime documentation](https://downloads.haskell.org/~ghc/8.8.3/docs/html/libraries/base-4.13.0.0/System-CPUTime.html) specifies picoseconds, for which that divisor gives microseconds and milliseconds require1, 000, 000, 000. The repository version therefore has a unit-label discrepancy. **Do not multiply or divide the paper's numbers on that basis:** correspondence to the later evaluation artifact is unverified.

The paper's concept DOI[10.5281/zenodo.4072906](https://doi.org/10.5281/zenodo.4072906) resolves through the public API to version[10.5281/zenodo.4141684](https://doi.org/10.5281/zenodo.4141684). Metadata describes an Ubuntu 20.04.1 VM with GHC 8.8.3, Cabal 3.0 and the exact evaluation data/tool version. Its sole `intensional.ova` is 5, 211, 030, 528 bytes, advertised MD5`4a7be94cc5646e7f615f5cf0df4445c7`. **Metadata only was inspected; this available large image was not acquired, mounted or run.** It is not an access block, a verified local hash or an inspected raw dataset. Resolving the timing-version correspondence requires that exact artifact or equivalent author material. No dependency installation, compiler run, analyzer execution or new experiment occurred.

## Follow-up and implications

G09's incoming graph has four edges, expands to the arXiv DOI and explicitly flags low coverage. SC55 retrieves all four incoming metadata records with requested`limit: 20`: *Structural refinement types*, *Contextual Refinement Types*, *Ill-Typed Programs Don't Evaluate* and a French thesis on transformations for pattern elimination. They remain conditional method/expressiveness leads, not four full readings. The contextual paper's citation snippet describes termination; S136's target is match safety, so that wording is not adopted as evidence of termination.

SC56 retrieves four backward methods: Mitchell/Runciman 2008's iterative partial-match safety (already completed S114, reused), Ong/Ramsay 2011's pattern-matching recursion schemes, Eremondi's set-constraint/SMT method and extensible datasort refinements. The Eremondi Springer 2020 DOI resolves the previously screened2019 preprint lineage; it is not a new independent study. Scite's two alternate ACM notices also remain edition locators, not independent evidence. SC57's exact title phrase returns publisher/preprint only, 2/2 at limit 20; it exhausts that narrow retrieval, not the sparse citation frontier. General set-analysis and finite-semilattice solving remain supporting-method leads.

| Criterion / claim | Disposition and next consequence |
| --- | --- |
| Unique | Unconfirmed for ISE. Call-sensitive partial-match safety and automatically inferred constructor refinements are established antecedents; local coverage cannot stand in for all static reasoning. Continue the acquired extension/practice methods and relevant refinement alternatives. |
| Valuable | The producer/consumer invariant and conditional fast analysis are concrete benefits. Precision limits, an omitted difficult module and integration obligations remain visible; no Nu/F#/agent-maintenance benefit is measured. |
| Scientifically valid | Formal inference/saturation/restriction arguments and all printed structural aggregates are reconstructed. Complete semantic/implementation verification, exact timing-artifact correspondence and fault sensitivity remain unestablished. |
| D1 boundary | Future-case diagnostics, reachability safety and old/new required behavior need separate records. This paper does not compare explicit enumeration with an initially equivalent fallback under evolution. |
| B06/B12 cost | Number of functions, interface size, datatype size and nesting are distinct dimensions. Preserve excluded/generated workloads and total integration cost before transferring a linear-time claim. |

The next accessible comparison is S115/S118's extension and matching discipline with S116's practice evidence. The available VM/source discrepancy is retained as a specific unresolved artifact question; it does not block those independent background readings. All experimental holds remain.
