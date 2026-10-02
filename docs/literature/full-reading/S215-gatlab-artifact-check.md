# S215 — Publication-era migration and validation source

This passive inspection accompanies [S215](S215-gatlab-model-migration.md), 2026-10-02. Author code, tests, macros and package installation are **not executed**. The source resolves the model-wrapper and validation boundary, not an empirical performance claim.

## Identity and actual reading

The paper links [AlgebraicJulia/GATlab.jl](https://github.com/AlgebraicJulia/GATlab.jl) without an exact commit. A GitHub commit-history query capped at2024-12-11T23:59:59Z returns **[a129cb4259b6d844bd18f1a07de9d7cf95b9fa52](https://github.com/AlgebraicJulia/GATlab.jl/tree/a129cb4259b6d844bd18f1a07de9d7cf95b9fa52)**, dated23October2024. `Project.toml` declares version0.1.3 and Julia compatibility1.9. This is the selected dated pin, not a verified paper release or current-version audit.

Complete source archive: **115,980 bytes**,93 regular files/271,667 uncompressed bytes, SHA-256 `f01d4f6ff6d9133dca0c3ca6957540053a239e5c2598ee4a17eb8e0cd729b23f`, MD5 `e811bd8eb598b7c3ac6fa9d6114a1adf`. Native attachment **`UIDA5ZEC`v5124** under parent`84F4WMGD` is byte-verified. The entire inventory is inspected; acquisition is not a complete reading of all93 files.

| Fully read file | Lines | SHA-256 |
| --- | --- | --- |
| `README.md` | 1–19 | `84808b51117f8703068deb92cc66bb11a19d1c9504cbadbba0724c330816fe70` |
| `Project.toml` | 1–28 | `0b7d4852c17b7fccffe632da3c24a2fc83344520a5cc007c62dd0e77f54af136` |
| `docs/src/concepts/models.md` | 1–42 | `c57d61cb58048e18397957fe18083c482d103fd513068a1c225149997a60b85b` |
| `src/syntax/TheoryMaps.jl` | 1–428 | `b32f6b9b5233eae5d4109622a48b3d66025115752b8176d869b03387278735e8` |
| `src/stdlib/derivedmodels/DerivedModels.jl` | 1–17 | `0b0e32ffad4dd916e0e8f3b47ad533c8b34096d9bae1e9034b7e530631efec06` |
| `src/stdlib/theorymaps/Maps.jl` | 1–40 | `603b88911873a04f19b0c3f86daf3f2f234330aa4013f0b5758baa91cebb5b3a` |
| `src/stdlib/models/finsets.jl` | 1–30 | `7d7bd65b7e7d7873c0c3aea7f54f6d9e1cb171d5d70c933d4143e84e2bae4d29` |
| `src/stdlib/models/slicecategories.jl` | 1–55 | `c1b3a054748d1474fd3b9fe2dc86bfcbf002c4123d10cb0f94c1a08b652e14a9` |
| `test/syntax/TheoryMaps.jl` | 1–124 | `e2c97cd0df7255e88a1c04b29c64f91c2ff58de40d7c8fcdf792173a91fbb902` |

Additional **selected ranges** of `src/models/ModelInterface.jl`:58–90,191–220,268–299,306–468,584–607,628–787. Whole-file SHA-256 `2a9ce0ea0b025794b1679931d359fc601e8800dc01821834b3335b9743d35b08`; only those ranges plus displayed name-search contexts are credited. Other symbolic-model, scope, parsing and algorithm files are not fully read. The general validation-name search had truncated output and is not a complete source audit; the narrower `SimpleTheoryMap`/`InclTheoryMap`/`macro map` search is complete at this pin.

## Migration path

`TheoryMaps.jl` parses constructor mappings into types/terms in context, reorders bindings and substitutes translated terms. Its macro obtains source/target theory metadata and generates a `Migrator`. `ModelInterface.jl`633–751 generates source-interface implementations using target-model calls; the returned struct retains a field containing the original model. Line787 implements `migrate_model(theorymap,m)` by calling that constructor. This source supports the paper's **model pullback** interpretation, not a claim of arbitrary in-place data or live-process transformation.

`DerivedModels.jl` includes three concrete uses: opposite finite-set categories, an additive integer monoid and a category from an integer preorder. `Maps.jl` specifies the relevant constructor interpretations. For an opposite category, both endpoints and composition order are changed deliberately. The method reuses executable semantics under a new interface; it does not preserve an old application trace merely because both interfaces have laws.

The generated constructor checks `implements(model,target_theory)`. In the inspected source, this tests nonmissing per-theory-segment registration, supplied by generated `ImplementationNotes`; it is not a universal equation checker. Generated method signatures are checked separately. The source explicitly flags incomplete treatment of migration's `context` keyword/accessors, which matters when a dependent index cannot be inferred from a carrier value.

## Validation and assumptions

`TheoryMaps.jl`255–258 explicitly states that axioms are not mapped to proofs and leaves well-formedness/axiom-preservation checking as future work. The general map constructor stores mappings after checking their keys; parsing and context processing add structural checks. It contains no proof of each translated axiom in the read path. The paper's guarantee therefore retains its mathematical premises: a **valid** map and a **lawful** source model.

`typecheck_instance` checks declared Julia signatures and required term methods. Default type-constructor implementations simply return the provided carrier value; default accessors raise an error. Stronger dependent membership checks must be supplied where required. The model documentation assumes term arguments were already coerced/validated. `finsets.jl` and `slicecategories.jl` demonstrate actual validation bodies, including finite-function membership and the commuting-triangle condition. These constructive examples should not be replaced by a blanket claim that the system checks nothing.

The complete map test file specifies selected invalid contexts, lookup failures, term translation, endpoint reversal, binding-order independence, inclusion and identity composition. Reading assertions does not show that they passed, that an error is raised for the intended reason, or that every axiom is checked. No test result is credited.

## Edition boundary and consequence

The pin uses `@theorymap`, `TheoryIncl`, `IdTheoryMap` and `TheoryMap`. The paper uses `@map`, `InclTheoryMap` and describes `SimpleTheoryMap` as a fourth representation; a complete source-name search finds no latter class at this pin. The README also lists functionality at a broader level than the selected implementation establishes. The source archive is useful correspondence evidence with an explicit version boundary, not proof that every paper example compiles unchanged or that later versions have the same limits.

The resolved survey claim is narrow and constructive: explicit model values, algebraic maps, syntax translation and generated delegation are concrete alternatives for organizing domain semantics. Signature registration, dynamic coercion, equational validity and preservation of a running system's obligations require different evidence. Exact manuscript binding and modern-version behavior remain unresolved; neither is needed to invent a Nu benefit estimate or authorize execution.
