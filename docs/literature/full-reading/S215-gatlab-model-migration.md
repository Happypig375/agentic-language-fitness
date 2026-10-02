# S215 — GATlab: algebraic interfaces and model reinterpretation

**Identity:** Owen Lynch, Kris Brown, James Fairbanks and Evan Patterson, *GATlab: Modeling and Programming with Generalized Algebraic Theories*, ENTICS volume4, MFPS2024, DOI [10.46298/entics.14666](https://doi.org/10.46298/entics.14666). Selected body: [publisher PDF](https://entics.episciences.org/14666/pdf), **19 pages**, printed17–1 through17–19. Publisher/Crossref date is11December2024; the PDF cover prints15December2024. The [arXiv history](https://arxiv.org/abs/2404.04837) has v1 April7, v2 June8 and v3 December7,2024. This reading uses the publisher body; preprints are not additional publications or independently compared bodies.

**Library and actual coverage, 2026-10-02:** native parent/note/PDF **`84F4WMGD` / `WFA64KBV` / `299XCYJW`**, collection`PKLXQNEE`. Collection and global DOI/title inventories found no existing match; parent/note creation precedes body reading. PDF **426,219 bytes**, SHA-256 `21838076b483d981a3ba39bfc295044edf0f42c9d64a0597fcbae6e0456cecc2`, MD5 `0944657ba29a4e09b5a82f9d558590ab`. **All19 pages**, Figure1, Table1, all mathematical/code examples, footnotes,40references and AppendixA.1/A.2 are read. Visual coverage is **14 pages:1,4–14,18–19**; remaining pages are read as text. A [bounded source inspection](S215-gatlab-artifact-check.md) reads nine complete files and selected ranges of one implementation file. No Julia, author tests or model construction is executed.

## Mechanism and contribution

GATlab embeds generalized algebraic theories (GATs) in Julia. Its purpose is to express the mathematical structure of a subject domain in a technical-computing environment. A GAT supplies ordered dependent contexts, type constructors, term constructors and equational axioms. For categories, `Hom(a,b)` depends on two objects; identity and composition have corresponding signatures, with associativity and unit laws. This supports domain structure richer than an unstructured list of operations.

The paper's contributions are an embedded specification language, a reported library of over90 reusable theories, symbolic and ordinary computational models, and theory maps for deriving models. The library count is an author report, not an independently counted set of validated theories. The formal foundations predate this implementation: Cartmell's GATs, algebraic specification, ML modules, OBJ/Clear/Maude and related theory-morphism systems are explicitly acknowledged. GATlab's engineering contribution should not be recast as invention of algebraic specification or categorical modeling.

Figure1 and Table1 distinguish declarations from equations. GATlab excludes explicit **type equalities**, simplifying sort inference without making general dependent-type equality decidable: equations between the terms on which types depend can still matter. Its routine sort check determines a constructor such as object versus morphism; it need not establish a morphism's exact domain/codomain or prove every equation.

## Implementations and their obligations

Theories act as interfaces/specifications; computational models provide Julia types and methods. GATlab supports both implicit dispatch on carrier types and explicit model values, including multiple interpretations over the same carrier. For example, integers can support additive and multiplicative monoid models without forcing a single interpretation. `WithModel` wrappers guide dispatch; models can carry parameters such as a modulus.

The `@instance` machinery checks that required method signatures are supplied. This is useful interface feedback, distinct from checking the implementation's algebraic laws. The publication's finite-set and slice-category examples include explicit runtime coercion/validation methods. Two representations place their costs differently:

| Representation | Mechanism | Obligation / cost boundary |
| --- | --- | --- |
| Fibered | Morphism values carry domain/codomain information | Direct access supports checking, with potentially redundant stored objects |
| Indexed | A carrier value is checked/coerced against separately supplied indices | Reduces representation redundancy; callers must retain/provide the relevant context and establish membership |

For the indexed finite-set model, `Hom` verifies vector length and codomain membership. The composition body indexes one vector by another. The source documentation expressly assumes term-constructor arguments have already been validated. Slice-category membership additionally checks a commuting triangle; ordinary identity/composition delegate to the base model. These are concrete implementations of particular constraints, not a claim that arbitrary Julia code is automatically a lawful category. The paper provides no measured memory or latency comparison between representations.

Symbolic models generate expression types and operations. User-supplied normalization can enforce selected associative/unit/inverse laws syntactically. The paper explicitly warns in footnote12 that its so-called free models may satisfy equations only up to rewriting and thus need not be literal models under raw expression equality. Implemented normalization strategies are useful machinery; their presence is not a complete decision procedure for arbitrary theories.

## What model migration means

An interpretation **I:A→B** maps A's constructors to well-typed expressions in B. It must also preserve A's axioms: each translated equation must follow from B's equations. Substitution then translates terms from A to B. A correct computational B-model **M** supplies their meaning, producing an A-model by precomposition:

`A expressions → B expressions → values in M`, hence `Models(B) → Models(A)`.

The model direction is **opposite** to the theory-map direction. The additive monoid example interprets multiplication notation as arithmetic addition and its unit as zero. The opposite-category map reverses morphism endpoints and composition order. These are deliberate semantic interpretations; “preserves the specified laws” does not mean “leaves every old operation's meaning unchanged.”

The implementation's `migrate_model` constructs a wrapper holding the existing model and generates delegated operations from the theory map. It does not, in the inspected path, copy or transform an application's running heap, reconcile subscriptions, drain events, recover external effects, or impose a temporal relation between old and new application executions. This is an interface/model derivation mechanism with meaningful algebraic guarantees **conditional on a valid interpretation and a lawful input model**.

The paper distinguishes identity, inclusion, simple constructor maps and general expression maps. General map validation requires equational reasoning that is semidecidable in general; specialized maps admit simpler checks. Theory composition can use renamed unions/pushouts for simple maps. General-map pushouts are explicitly unimplemented in the paper. Its invalid-unit example is especially relevant: mapping a monoid unit to one while mapping its operation to addition can preserve carrier/signature compatibility while violating the unit law. A checker of shapes alone cannot settle that obligation.

## Publication versus source guarantees

The [source pin](S215-gatlab-artifact-check.md) is the last main-history commit returned before the publisher's December11 date, **a129cb4259b6d844bd18f1a07de9d7cf95b9fa52**, dated23October2024, package0.1.3. It is a bounded publication-era comparator; the paper supplies no commit binding proving it is the exact manuscript implementation.

The pin confirms model wrappers, generated method signatures, context-dependent coercions and concrete theory-map examples. It also explicitly leaves proof mapping/axiom preservation unfinished in `TheoryMaps.jl`. Instance registration and `implements` metadata are not law proofs. Included tests check selected context errors, substitution and map composition; they are source evidence only and have not been run here. The pin uses `@theorymap`/`TheoryIncl`, while the paper presents `@map`/`InclTheoryMap` and an additional `SimpleTheoryMap` class not found by the source-name search. These differences constrain exact correspondence; neither source nor paper is silently substituted for the other.

AppendixA supplies practical implementation detail: UUID-tagged lexical scopes distinguish bindings during syntax movement/substitution, avoiding accidental name capture, and nested macro expansion retrieves parent-theory metadata before runtime. These techniques support reliable DSL implementation. The appendix does not present an independent end-to-end soundness proof or an empirical maintenance comparison.

## Evidence disposition and consequence for Nu

S215 is a constructive language/tool account with worked examples and inspectable source. It reports incremental adoption in the AlgebraicJulia ecosystem and preliminary symbolic dynamical-system applications. Faster generated code, broader symbolic analysis, cross-language transfer, richer rewriting and randomized testing appear as capabilities to develop or future directions, without a controlled benefit estimate in this paper. Absence of that estimate does not negate its implemented abstraction and reuse mechanisms.

For **B02/B04**, S215 changes the alternatives map: declarative domain interfaces, explicit law-bearing theory maps and derived model implementations are established design options beyond a closed ADT and handwritten adapters. It does not resolve D1's source-convention comparison, claim exhaustiveness after future cases, or establish safe live migration. For **B07/B12**, distinguish a formal obligation, a partial syntactic check, a programmer-supplied runtime check and proof/behavioral evidence. This supports a more precise account of which Nu obligations are represented and which require independent verification.

The next consequential B02 method is C02 2-71, *Inductive types deconstructed: the calculus of united constructions*: reconstruct its typed default branches as an alternative relevant to future-case handling. Dependent matching, algebraic testing, S187's expanded practice review and .NET/game/temporal transfer remain separate frontiers. No experiment or new adapter is authorized.
