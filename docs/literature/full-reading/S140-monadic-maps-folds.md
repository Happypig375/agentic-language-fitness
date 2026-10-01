# S140 — effectful folds need the stated composition laws

Read 2026-10-01 by the main Codex session. Maarten M. Fokkinga, *Monadic Maps and Folds for Arbitrary Datatypes*, University of Twente, Memoranda Informatica **94–28**, June 1994; [institutional record](https://research.utwente.nl/en/publications/monadic-maps-and-folds-for-arbitrary-datatypes/). The governing PDF cover says **version of June 1, 1994**. The primary record and author's bibliography agree on the report identity; ResearchGate's December label does not override the cover.

Existing native parent **`ESPYW2U7`**, PDF **`8DW9XIWD`**, canonical note **`AYVC6YZP`**. Parent/attachment relation, title and stored bytes reverified before continuing. **23 pages, 227,700 bytes**, SHA-256 **`10ca6f0b62fcc5ace0e66adce4160ec4da19ed2b6472c3c926e72d96d1e5edbd`**. Every page was extracted, rendered and **visually read**, including all definitions, displayed calculations, the single author-address footnote, twenty references and Appendix A. The PDF's mathematical text extraction is unreliable; the page images govern. There are no numbered empirical tables or figures. This is a complete report reading, not machine-checked proof certification or program execution. The earlier PostScript acquisition remains a separate object; no byte/semantic equivalence with it is certified here.

The reading resolves the explicit theorem dependency in [S138](S138-compositional-data-types.md). It supplies conditional mathematical mechanisms, without a runtime benchmark, human-maintenance comparison, agent evaluation or Nu implementation claim.

## Construction and scope — pp. 1–12

The report separates two ideas: defining a well-typed effectful traversal, and deriving its algebraic transformation laws. An ordinary fold replaces a datatype's constructors by operations. A monadic fold also sequences recursive results inside an effect representation. A monadic map changes stored elements using effectful functions while retaining the datatype's shape.

The setup uses initial algebras and regular functors built from constants, projections, sums, products, composition and induced datatype functors. Lists illustrate how several constructors can be represented by one sum-shaped signature. Existence of the required initial algebra is a premise; the result is not an assertion about every possible runtime heap, nonterminating computation, higher-order object graph or externally mutable resource. The categorical formulation is not confined to sets, but applying it in another semantic category still requires its assumptions.

A monad supplies a unit and multiplication and therefore associative Kleisli composition. That alone does not lift every datatype functor with all ordinary fold/map laws. The extra operation distributes a structure of effectful values into one effectful structure. Write it in conventional right-to-left composition notation as

`λ_A : F(M A) → M(F A)`.

Given an effectful algebra `α : F B → M B`, the proposed traversal is the ordinary fold with algebra `μ ∘ Mα ∘ λ`. This distinguishes sequencing child effects from applying the local algebra. The report derives matching types directly in Appendix A; that derivation does not establish the later fusion premises.

For regular functors, distribution is constructed inductively: constants use the monad unit, projections use identity, sums dispatch through the corresponding injection, composition combines existing distributions, and induced datatypes use the monadic map. The product case is supplied separately for the chosen monad. The mutual definitions are justified by induction on the regular-functor construction, not by an unrestricted circular definition.

## The additional law — pp. 12–17

Section 5.1 assumes a natural product distribution `M X × M Y → M(X × Y)` that preserves both unit and multiplication. Section 4.3 propagates those properties to regular functors. For a fixed unary functor, the familiar forms are:

- **Unit:** `λ ∘ Fη = η_F`.
- **Multiplication:** `λ ∘ Fμ = μ_F ∘ Mλ ∘ λ_M`.

The second equation compares flattening nested effects before collecting children with collecting the outer and then inner effects before flattening. Merely having a function of the right type, a `Monad` instance or an executable traversal does not establish that equality. The paper also requires naturality.

Under these premises, the lifted operation `Fᴹ f = λ ∘ F f` is a functor on the Kleisli category. Lifting extends to categories of algebras; the report constructs an adjunction whose left adjoint preserves initiality. That gives the monadic fold its uniqueness and transformation laws through the initial-algebra argument. This is a useful positive result: valid local equations support compositional reasoning instead of a fresh whole-program argument for every instance.

The report explicitly says in **Section 5.1 and the conclusion** that its general product assumption fails for the ordinary state monad. Section 4.4 presents both left-first and right-first state sequencing, already showing that choosing a product traversal determines an order. The multiplication law can interleave nested state actions differently; associativity of monadic bind does not authorize swapping them.

This is a limit on the report's **general lifting argument**, not a prohibition on all stateful folds or all state-preserving optimizations. Section 6.5 retains meaningful direct definitions and several laws even without the assumption, and notes a product-free sufficient case. A particular datatype may admit a lawful distribution even when the universal product construction does not. Its actual signature and local algebra therefore matter.

## Fusion has a transformation-specific premise — pp. 17–21

The report's monadic fold fusion law retains a homomorphism condition. In notation where `g ⋆ f` first executes `f` and then `g`, an effectful result transformation `k : A → M B` can fuse with the fold of `α : F A → M A` into the fold of `β : F B → M B` when

`k ⋆ α = β ⋆ Fᴹ k`.

Under the lawful-lifting premises, the conclusion is `k ⋆ cataM α = cataM β`. This equality is about the effectful computation, not just its returned tree. It does not follow from compatible types, monadic associativity, or a pure stage alone.

Section 6.4 gives another composition law using a signature transformation `ε`. Crucially, `ε` must be natural **in the Kleisli category**, with the displayed condition quantified over effectful functions. Naturality only with respect to pure functions is weaker. This condition matters for transformations that duplicate or discard recursive results: they may also duplicate, suppress or prematurely execute effects.

That resolves S138's pending attribution. Its previously recorded finite symbolic cases concern a bottom-up tree-homomorphism composition: duplicating a subtree changes an additive Writer count, while discarding a subtree can suppress a `Maybe` failure in the sequential version but expose it in the fused version. Those cases do **not** refute S140's conditional theorem. A monad supporting an appropriate distribution is still insufficient to establish the transformation-specific equation. The actual traversal, effect multiplicity and discarded work need checking.

S138's dated source also distinguishes its generic pure-first traversal from the bottom-up rule; the counterexamples must stay attached to the correct definitions. No new compiler execution, rewrite-rule-firing claim, current-library defect claim or measured regression follows from this report reading.

The conclusion explicitly distinguishes generally retained characterization/self/identity/uniqueness laws from the fusion argument that needs a functorial lifting. It also warns that the displayed monadic-map calculation uses the distributivity assumption. One cannot import every law from the earlier pages after dropping that premise.

## Consequence for evolving interactive software

The established mechanism is structured traversal plus explicit effect sequencing, with conditional algebraic laws for transformations. Equal returned state representations need not imply equal events, failures, I/O, pending work or effect order. The report does not claim that a pure description restores the external world, that type correctness establishes intended behavior, or that source compactness measures benefit.

**Unique:** monadic maps, folds and conditional effect-preserving transformation laws are longstanding prior mechanisms. **Valuable:** the law can justify eliminating an intermediate traversal when its premises hold; no speed or maintenance effect is measured here. **Scientifically valid:** preserve the distribution, semantic category, signature and transformation-specific equation. Failure of a general premise is neither a runtime failure of every instance nor evidence against functional programming as a whole.

The [selected S192 comparison](S192-monadic-fold-dependency-partial.md) makes the fixed-signature qualification concrete and identifies a separate head/tail effect-order mismatch in both its author and final editions. That bounded symbolic check does not refute its broader theory or certify either whole edition. The [search ledger](../nu-background-searches-2026-09-30.md) records SC124 and W279–282, including wider unexamined retrieval and related-law follow-ups. The complete S140 report closes this particular unread-method dependency; next return to S90's modularity/change-task method. The wider survey and empirical benefit questions remain open.
