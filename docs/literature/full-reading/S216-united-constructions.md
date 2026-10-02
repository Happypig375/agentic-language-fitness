# S216 — United Constructions and typed default branches

**Identity:** Stefan Monnier, *Inductive Types Deconstructed: The Calculus of United Constructions*, TyDe2019, pp.52–63, DOI [10.1145/3331554.3342607](https://doi.org/10.1145/3331554.3342607). Selected body: [author-hosted proceedings-formatted PDF](https://www.iro.umontreal.ca/~monnier/itd-tyde-2019.pdf), created17July2019. Crossref and SIGPLAN metadata identify18August2019 publication. The publisher DOI route returned403 and the author homepage denied access, but the exact public PDF route succeeded through an ordinary request. Final publisher-body equality is not independently verified.

**Library and actual coverage, 2026-10-02:** native parent/note/PDF **`MVMYNL4N` / `FSFFPECM` / `ERDS7FUU`**, collection`PKLXQNEE`. The DOI/title inventory found no match and the record preceded body reading. PDF **12 pages,803,782 bytes**, SHA-256 `dd7bc8adbab11c31519e6672931b252f5477ae58f987a6ea6f1ed0c3c8c5e778`, MD5 `a77cf540db475918b097447603efee46`. **All12 pages are read both as text and visually**, including all12 numbered figures, every displayed rule/example, Lemmas4.1/5.1, Corollary5.2 and26references. Unsorted column extraction plus page images resolves mathematical layout; text extraction alone is not used to infer the rules. No compiler, proof assistant or author code is run, and no machine-checked proof is acquired or credited.

## Problem and constructive contribution

The Calculus of United Constructions (CUC) separates the components that conventional inductive types bundle: labeled tuples, sums, recursion and equality/index evidence. It is motivated as a typed core/compiler representation for Typer, where testing a constructor tag and extracting fields should be separately expressible. Conventional case analysis can force a large elimination form even when one field is needed. The paper explicitly acknowledges that compilers often optimize such costs later; its aim is to express those transformations at a typed level with a small implementation burden.

CUC is **larger** than the base calculus and CIC. Its design favors separable primitives over the fewest constructs. The intended contribution is a concrete language/semantics design and relative metatheoretic account, not a measurement of developer productivity, source compactness, game performance or agent repair.

## How the pieces fit

Figures1–4 define a fully predicative universe hierarchy, dependent functions, labeled dependent tuples and explicit equality witnesses. Labels attach to tuples themselves, allowing sums to use untagged union types instead of an extra tagged wrapper. The paper argues that existing object metadata can often store labels; this is a representation rationale rather than an observed allocation benchmark. Tuple construction is saturated so allocation and any curried-closure costs remain explicit. Indexed families can be represented with ordinary parameters plus equality-witness fields.

Figures5–7 supply unions, weakening casts and a single-label `switch`. The auxiliary split judgment divides an input union into the types whose tuple label matches and those whose labels do not. It also ensures the scrutinee is made from tuples whose runtime tag can be inspected. The cast relation is a restricted explicit union-inclusion relation; this is not unrestricted semantic subtyping over arbitrary types. Union order remains significant in the presented syntax/translation.

The switch checks one tag and chooses either the matching or default branch. It binds, in **both branches**, the original value at the corresponding refined type plus an equality witness relating that binding to the scrutinee. Field extraction is a subsequent operation. Repeated switches can test further labels because the default retains the information that preceding labels failed. Both branches have the same result type; explicit equality evidence supplies dependent refinements that would otherwise be encoded in a dependent eliminator's result annotation.

The printed typing rule requires both split components to be nonempty. This avoids presenting an unreachable branch as an ordinary inhabited case; the translation has boundary clauses for recursively reached empty components. More general multi-branch switches are discussed as extensions of the single-label construction.

Figures8–9 add separate recursive types and recursive functions. Strict positivity constrains type recursion; a syntactic decreasing-argument judgment constrains function recursion. The tuple positivity rule prohibits later fields from depending on a recursive field. The translation relies on a predicative CIC variant with the stated nesting/termination accommodations; an impredicative universe requires additional restrictions and is discussed as an extension, not covered by the demonstrated calculus.

## What a default branch learns

For an illustrative union `A ∪ B ∪ C`, a failed test of A's distinct label leaves a default binding typed by `B ∪ C`. This example is our direct reading of the split rules, not an executed program. The default can pass that value to an operation designed for precisely the residual union or perform another test without repeating the excluded alternative.

That mechanism refutes an unqualified statement that every catch-all necessarily discards all case information. It does **not** show that a catch-all implements the required behavior for a newly introduced case. If the domain grows, the remaining type may grow too; an operation that requires a narrower residual type may need adaptation, while an appropriately general fallback can remain valid. The paper evaluates neither that maintenance process nor how often either outcome occurs.

This differs from the proposed F# source treatment. CUC changes the core language's typing and elimination rules. [D1](../../fsharp-domain-evolution-research-proposal-2026-09-16.md) holds the language/tool policy fixed and compares initially equivalent enumeration with catch-all coverage; both can already be exhaustive. S216 is prior art for stronger default-branch information, not an observed result for the fixed F# convention or an instruction to introduce a new language/adapter.

## Erasure and relative consistency

Section4 removes `cast` from terms and defines the corresponding erased reduction relation. **Lemma4.1** states two directions: a typed source step either disappears under erasure or corresponds to an erased step, and an erased step can be matched by a source reduction sequence. The proof is summarized as induction on reduction derivations. This supports the particular weakening cast's no-op implementation under the formal semantics. It does not erase every equality/type construct, measure a real compiler, or prove zero whole-program overhead.

Section5 maps CUC **typing derivations** to a predicative CIC, using nested dependent pairs for tuples, ordinary sums for unions, explicit equality and inductive encodings for recursion. In this translation, casts can introduce actual sum constructors; tuple labels instead become redundant. It serves a different purpose from the efficient erasure semantics. The publisher programme's broad equivalence wording should not replace the paper's more specific one-way type-preserving translation.

**Lemma5.1** asserts preservation of types by this translation. Its printed proof outlines induction and identifies necessary positivity, termination, reduction and preservation lemmas; it does not give every derivation. **Corollary5.2** concludes relative consistency: if the chosen CIC cannot derive falsehood, neither can CUC. Preserve that conditional formal contribution without promoting this reading into a mechanically verified metatheory or a guarantee about arbitrary implementation behavior.

Two visual checks locate presentation issues relevant to exact reconstruction: Figure5 repeats the `τ1 : Typeℓ1` premise where the union rule would need the second type's premise, and Figure11 prints both `Either` alternatives with `τ1`. The intended role of `τ2` is clear from the surrounding mapping, but those corrections are our interpretation, not an acquired erratum. These located notation issues are not an executed inconsistency counterexample and do not erase the typed-default construction. Full formal verification remains separate from reading the provided proof sketches.

An exact DOI/file proof-or-erratum search recovers the paper and a Typer repository lead, without resolving a separate CUC proof package. A primary GitLab inventory lists three files in `doc/formal`. Its `typer_theory.tex` blob `65ecbcd7a56a2b02cefead756698cdf792b8bab3` is53,383 bytes, SHA-256 `f179cc0f58eddd7d202ebe2671f9b2f2ada9fbeb5bb5f7fb8d3d7a952f961451`. **Header/overview lines1–33 and displayed keyword hits only** identify a distinct *Exposition of Typer's Type Theory* by Nathaniel Bos and Monnier, covering broader universe/impredicative machinery. Keyword output is truncated; the1,110-line document is not fully read, linked to the CUC lemmas or credited as another work. No TeX build is run. This bounded check does not prove that no fuller proof exists.

## Costs, limits and future mechanisms

Section6 acknowledges that tuple projection is still syntactic sugar of size proportional to its position. A primitive projection would fix that representation cost and require a corresponding termination rule. Thus the motivating constant-size field-selection goal is not fully realized by every displayed core construct as written.

More flexible unions, extensible sum types, first-class cases, row-like abstraction, bidirectional typing, additional erasure and reified subtyping/splitting proofs are proposed directions. They must not be attributed to the current calculus as completed features. In particular, **precise default typing over the presented union does not establish open-world variant extensibility**.

The related-work section places the mechanism among algebraic datatype representations, equality coercions and decomposed dependent datatypes. The whole paper contains no participant study, maintenance task sample, measured runtime comparison or coding-agent experiment. This is appropriate for its language-design evidence role; unknown empirical benefit is distinct from an unread mechanism.

## Consequence and continuation

For B02/B07, the useful distinction is between **coverage of possible alternatives**, **type information within a chosen branch**, and **the required semantics of that branch**. CUC gives a constructive way to preserve negative tag information and equality evidence in defaults. Neither that refinement nor explicit enumeration specifies application obligations that the type does not express. B05/B06 also gain a concrete typed-representation alternative, with formal cast erasure kept separate from measured runtime savings.

The next consequential type-method route is C02 1-78/2-91, *Elaborating dependent (co)pattern matching: No pattern left behind*. Resolve the edition relationship and reconstruct how source clauses, first-match semantics and core elaboration are checked. This addresses enforcement correctness beyond a catalogue of type expressiveness. S187's expanded practice review and independent temporal/runtime routes remain live. All construction and execution holds remain.
