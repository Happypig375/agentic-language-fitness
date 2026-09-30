# S115 — Open data types, defaults and global extension

**Reading completed 2026-10-01 HKT.** Andres Löh and Ralf Hinze, *Open Data Types and Open Functions*, PPDP 2006, pp. 133–144, [DOI 10.1145/1140335.1140352](https://doi.org/10.1145/1140335.1140352). This addresses B02/B05: extending constructors and operations without changing existing definitions is an established alternative to a closed datatype. The question is what dispatch, composition and checking obligations that alternative introduces.

## Acquisition and actual coverage

Existing Zotero parent `J6PMJPLP` preceded reading. Its [Oxford author PDF](https://www.cs.ox.ac.uk/ralf.hinze/publications/PPDP06.pdf), attachment `CBZDUVET`, has 12 pages, 200,343 bytes and SHA-256 `a8748158212db8d3de11bd2a1b03955b691bc9262b20ef59a005ad1356418262`. Native local-API readback confirmed the attachment bytes. All 12 pages, ten figures and 28 references were read; every figure was visually inspected, including the pattern-ordering and module-translation examples. PDF page numbers below are 1–12. There is no appendix or empirical result table. Zotero note `5MCLEYZK` holds this reconstruction.

The paper proposes a language extension and sketches two implementation schemes. No author compiler, generated program or experiment was run. Its discussion of then-current GHC, OCaml and Haskell features is historical, not a check of today's implementations.

## Reconstructed mechanism

The expression problem has two extension directions: add constructors to a datatype, and add operations over it. A closed sum makes the latter straightforward but normally requires revisiting existing consumers for the former. S115 marks a datatype and/or a top-level function `open`; constructors and equations can then live in different modules. Every open function has an explicit type signature. Calls, including recursive calls inside earlier equations, refer to the final assembled function. This avoids the naive wrapper problem in which an added outer case delegates recursion back to the old function.

This is **global extension**, not a menu of independent local meanings for one type. All constructors and equations in the assembled program contribute, regardless of whether their names are exported for other modules to use. Name hiding cannot remove their semantic contribution. The core model assumes a root Main module reaching the program, qualified unique names, fully applied constructor patterns and consistent equation arities. Local functions cannot be open. These restrictions matter when mapping the proposal onto actual libraries or interactive systems.

Sections 4–5 define the meaning by translation to a closed program: rename entities to avoid module-name collisions, collect constructors, collect and order open equations, then use the ordinary language's types and evaluation. The simple translation gathers the program in one module. It is a definition of the proposed construct's semantics, not a proof that an arbitrary source edit preserves the old program's behavior.

### Defaults and dispatch

Ordinary first-match textual order is awkward for equations contributed across modules. S115 instead uses **best-fit, left-to-right ordering**: a constructor pattern is more specific than a variable or wildcard; nested patterns and function arguments are compared lexicographically. Equations equivalent under this pattern comparison are rejected as duplicate cases. Different constructors do not match the same constructor value, so their relative ordering is immaterial to which such clause applies.

A default therefore does not permanently intercept a later constructor-specific equation. That is a concrete extension benefit over simply appending a case after an ordinary wildcard. It still leaves a behavioral obligation: the default may be intentional, or it may quietly assign the wrong behavior to an unhandled new constructor. Without a matching equation or default, runtime pattern failure remains possible. Neither ordinary type correctness nor the existence of a fallback proves the intended new behavior.

Left-to-right ordering is a dispatch policy, not a claim that every overlapping pair has a unique globally most-specific pattern. For example, reasoning directly from the rule, a clause specific in its first argument can outrank another clause specific in its second argument when both apply. That observation is a reconstruction of the ordering, not an executed conflict experiment. Figure 6 makes the lexicographic ordering visible across lists, literals and multiple arguments.

Constructor order is separately defined by a depth-first traversal of the import graph, visiting dependencies before importers and using import/declaration order to resolve choices. That order can affect derived ordering, enumeration and bounds. Thus global assembly also introduces dependencies beyond the obvious function equations.

The full-language discussion does not finish every design choice. As-patterns are ignored for specificity; wildcards behave like variables; lazy patterns can postpone decomposition failure. For guards, pp. 7–8 offer alternatives: select the best pattern before checking its guards, combine guards in a chosen order, or disallow them for open functions. The paper does not select and validate one complete guard semantics. Do not import S119's later coverage treatment into this proposal.

### Compilation and checking

| Scheme or property | What the paper supplies | Boundary |
| --- | --- | --- |
| Whole-program translation | Collect open entities into one closed program; ordinary compiler then handles it | Recompilation of the transformed program and source distribution of relevant libraries; possible optimization benefits are conjectural here |
| Separate compilation sketch | Preserve transformed modules, gather open dispatch in Main, and use mutually recursive modules | Main remains the assembly point; this is not independent selection of which extension a caller sees |
| Split equations | Keep pattern selection in Main and move each right-hand side into a fresh module-local helper receiving the bound variables | Body compilation can be separate while dispatch structure still depends on assembled cases |
| Stable interfaces | A transformed module imports only the types, constructors and function signatures it needs | The described GHC interface mechanism cannot expose individual constructors without the full concrete datatype; the proposal requires additional interface/compiler support |
| Ordinary type checking | A function accepts values of the correct datatype | A well-typed partial function can still fail to match |
| Exhaustiveness checking | Check the assembled open function when Main is compiled | Explicitly global, not modular per-extension exhaustiveness checking |

The paper claims the usual expression-problem criteria, including separate compilation, for its proposed translation. Section 5.2 nevertheless describes the missing constructor-interface capability and a possible representation/performance cost. Those are implementation obligations, not measured overhead or a verified delivered compiler. The paper's optimization remarks about other whole-program tools do not benchmark this extension.

## Examples, comparisons and benefit evidence

The expression evaluator demonstrates both extension directions. Open type representations and overloaded functions illustrate generic programming; a structural view can centralize work that otherwise appears in several overloaded operations. The exception example shows another legitimate use of a default: a local closed handler can rethrow exceptions it does not handle. Open functions are unnecessary for that particular handler. These examples explain expressiveness and integration choices; none measures edits, developer time, reliability or runtime cost.

The type-class comparison retains a positive alternative. Encoding constructors as types can make method-instance availability a static obligation, stronger in that respect than S115's ordinary typing of an open function. It also complicates direct pattern syntax, local exception handlers and values whose variant is chosen at runtime. These are properties of the encodings discussed, not a universal ranking of all modern Haskell or OO techniques. Likewise, the polymorphic-variant comparison says recursive wrappers need explicit recursion management; its primary counterparts remain separate reading leads.

S115 explicitly identifies Millstein, Bleckner and Chambers' EML as a stronger modular-checking comparator with hierarchical datatypes, subtyping and pattern restrictions. The [author's primary publication page](https://web.cs.ucla.edu/~todd/research/pub.php?id=icfp02) identifies the 2002 proceedings paper and a superseding 2004 journal article. This pass verified that lineage and abstract, **not EML's full proof or implementation**. The supplied Scite citation from *Data types à la carte* identifies a further consequential distinction: selecting datatype components instead of globally extending one datatype. Its method remains the next primary check.

## Survey consequences and remaining work

| Criterion | Updated judgement |
| --- | --- |
| Unique | Unconfirmed. Open constructor/operation extension, defaults, recursive dispatch and their modularity tradeoffs are established prior mechanisms. S115 supplies no first-study claim for ISE. |
| Valuable | A concrete capability exists: extend both axes while retaining old definitions, with later specific cases able to outrank defaults. Global conflict, compilation and behavioral obligations remain; practical benefit is unmeasured here. |
| Scientifically valid | The core translation, ordering and implementation assumptions are reconstructed. No completed full-Haskell guard design, measured separate-compilation implementation, or maintenance/agent effect follows. |

For D1, record a default's intended behavior and future-case obligations separately from exhaustiveness. For the wider Nu assessment, separate extending a source-level representation from selecting components, validating independently authored extensions, and migrating live state. This paper does not address complete external effects, running-state conversion or net interactive-development benefit.

G10 and SC58–62 are recorded in the [search ledger](../nu-background-searches-2026-09-30.md) and [type-method screen](../nu-background-types-search-2026-09-30.md). The 49 indexed incoming DOI records were paginated and screened; off-topic open-data/open-science results and edition notices remain visible. This exhausts that returned DOI set, not field coverage. Follow selectable composition first, then the acquired S118 pattern-view and S116 practice sources; retain EML's modular-checking dependency and the broader Join Token, persistence and oracle frontiers. All experimental holds remain.
