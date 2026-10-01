# S192 — a datatype-specific law and an effect-order mismatch

Selected reading on 2026-10-01 by the main Codex session. Ralf Hinze and Nicolas Wu, *Unifying structured recursion schemes: An Extended Study*, JFP **26, e1, 2016**, [DOI](https://doi.org/10.1017/S0956796815000258). Native parent **`SINX4HU9`**, note **`7L7735BW`**, created after DOI/title duplicate checks and **before selected body reading**. The same-title three-author 2013 conference paper is a predecessor, not this edition.

| Native attachment | Identity | Actual coverage |
| --- | --- | --- |
| **`684S83T2`**, Bristol peer-reviewed copy | **48 pages, 584,662 bytes**; SHA-256 `2a3b10c0a7643ff9c4adcfe9e86bd5a56aed783a5294ae54cf7a59508725fa29`. One repository cover plus a manuscript dated **September 15, 2015**; [primary file](https://research-information.bris.ac.uk/ws/portalfiles/portal/65842535/Nicolas_Wu_Unifying_Structured_Recursion_Schemes.pdf). | Physical **1–3, 7, 34, 36–41 and 44**: **twelve pages** consumed. Nine visual pages **7, 34, 36–41, 44**. Covers/introduction, the example, coherence equations, all Section 9, selected calculation/fusion and table context. |
| **`JHNKAE4S`**, final Cambridge edition | **49 pages, 393,880 bytes**; SHA-256 `b69b1064b2be35c1cd20e2478eb84f6efa58a889ca31dafca8e01d6c7efefcbd`; [primary file](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/2CF2B29B85890E893F9761EA1C3B709E/S0956796815000258a.pdf/unifying_structured_recursion_schemes.pdf). | Physical **1, 7, 39–40**: **four pages**, with **7, 39–40** visually checked. Cover and both disputed definitions compared. Whole-edition equivalence is unverified. |

The author PDF failed Python certificate validation; ordinary Windows `Invoke-WebRequest` succeeded without a verification override. The final publisher PDF was also publicly downloadable through that client. Both stored hashes were verified. Most pages, other recursion schemes, underlying proofs and bibliography remain unread; this adds **no full-paper count** or machine-checked theorem claim. All-page extraction supplies locators only. Download-service identifiers remain outside the public record.

## The useful qualification to S140

Section 9 assumes a distributive law for **one specified endofunctor** and obtains its monadic catamorphism through the Kleisli adjunction. The law must satisfy unit/multiplication coherence; the selected fusion calculation also retains a homomorphism premise. Example 9.2 uses the one-layer signature `List a x = Nil | Cons a x`, with only the recursive position sequenced by the distribution. It therefore does not require S140's universal product distribution over two arbitrary effectful components.

Our inference is that S140's failed general state assumption must not become a blanket ban on stateful folds. The chosen signature, effect sequencing and algebra matter. This preserves a positive lawful construction without assuming that it implements every desired execution order.

## Own symbolic comparison of the two printed definitions

The introductory definition (author physical p. 7; final p. 7) executes the head action before recursively accumulating the tail. Example 9.2 (author physical pp. 38–39; final pp. 39–40) defines a fold using `join ∘ fmap b ∘ λ`, where `λ` executes the recursive-tail action before constructing the node and `b` then executes its stored head action. Both versions retain these definitions; this is not just an obsolete-draft difference.

Unfolding that latter algebra yields:

```text
derived(mx : mxs):
    xs <- derived(mxs)
    x  <- mx
    return (x : xs)
```

For two Writer actions, let the first emit `A` and return 0, and the second emit `B` and return 1. The introductory function returns `[0, 1]` with log `AB`; the displayed derived fold returns `[0, 1]` with log `BA`. This is our finite symbolic calculation, **not an executed test, an author-confirmed erratum or a defect in every theorem of the paper**. It does not rely on unsafe functions or divergent evaluation. The list of returned values alone hides the effect-order difference.

The distribution can be lawful while the advertised example correspondence is wrong for noncommuting effects. Commuting effects may conceal this discrepancy; they are not assumed in the example's general monad constraint. W282's two targeted queries did not locate a correction, which does not establish global absence. No author was contacted and no code or proof assistant ran.

This bounded check strengthens the S140/S138 synthesis: distinguish a well-typed definition, a lawful lifting, a transformation-specific equation and the intended observable behavior. It leaves the paper's broader unification results outside this selected audit. Continue the older S90 modularity/change-task method; further theory or effect-handler readings remain conditional on a concrete unresolved claim.
