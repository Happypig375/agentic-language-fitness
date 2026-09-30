# S134 — What the LYG mechanization proves

**Targeted dependency reading, 2026-10-01 HKT; not a full thesis or proof reproduction.** Henning Dieterichs, *Formal Verification of Pattern Matching Analyses*, KIT master's thesis, submitted 2021-04-06. The [institutional record](https://pp.ipd.kit.edu/publication.php?id=dieterichs21masterarbeit) identifies the work; no DOI is invented.

## Acquisition and selected coverage

Zotero parent `SIB2KGEF` and attachment `GGRSMPBH` preceded body reading; partial note `3DWTJ5SP` preserves the scope. The [institutional PDF](https://pp.ipd.kit.edu/uploads/publikationen/dieterichs21masterarbeit.pdf) has 51 pages and 263,340 bytes, SHA-256 `fd8fff806497a7b51ca9221e6a3d63b5be22cb020b455acb22c846fd8398b636`.

Pages **1–8, 19–33 and 45–51** were read completely: 30 physical pages including blank separators, introduction, formal definitions, theorem statements, conclusion and all eight bibliography entries. Opening, scoping counterexample p.23 and theorems pp.31–32 were visually checked. The background pp.9–18 and detailed proof chapter pp.34–44 remain unread. The full thesis is excluded from the complete-reading count. Four explicitly pinned source/configuration files were read; imported proof lemmas and dependencies were not fully inspected or executed.

## Formal boundary

The model avoids formalizing all of Haskell. Its `GuardModule` abstracts environments, RHS identifiers, total guards, variables and a bottom predicate. A total guard can fail or return an updated environment; possible divergence belongs to a separate bang guard. Branch failure restarts the next branch with the incoming environment. Type information could be encoded in an instantiation, but the thesis does not certify GHC's type solver, desugaring, implementation or extension machinery.

The uncovered theorem characterizes **exactly fallthrough**, excluding divergence. An empty uncovered predicate therefore means every input matches or diverges; it is not a termination or intended-result theorem. The practical emptiness decision is a parameter: `CorrectCanProveEmpty` requires that a reported empty predicate really has no satisfying environment. It may fail to prove emptiness. The thesis expressly does **not** prove that LYG's implemented inhabitant generator satisfies this premise (pp.26,45).

The redundancy theorem additionally requires distinct RHS identifiers throughout the guard tree. Every actually reached RHS belongs to the reported accessible group, and removing the **entire reported redundant set** preserves the modeled evaluation result. Marking some truly redundant RHSs accessible/inaccessible is allowed by the theorem; completeness is not automatic. The file also states that a combined U/A traversal equals the separate computations.

## Scoping correction and correspondence

Pages23–25 identify a binding ambiguity in the original refinement-conjunction notation. A failed first branch binds a shadowing variable; if that binding leaks into a later branch's constraints, the symbolic uncovered set can become empty although the later branch falls through for the original input. The thesis replaces implicit scope propagation with an explicit nested binding constructor, `tgrd_in`, and uses functions as context accumulators in U/A. The proof concerns this precise formulation.

This is not a reproduced GHC bug. The thesis states that GHC uses a different refinement encoding and is unaffected by the illustrated scoping flaw. S119's updated account acknowledges the scoping issue and unique-name requirement. The theorem cannot be described as an unconditional certification of every printed equation or the complete compiler. Conversely, this correspondence limit does not negate the useful mechanized branch/removal results.

The conclusion reports 48 definitions and 143 lemmas/theorems. These are the author's development counts, not independently enumerated proof obligations or new compiler tests. Its explicit caveat remains: mechanization alone cannot establish that the chosen abstractions correctly represent the intended source system.

## Pinned source check

The thesis's exact [proof revision](https://github.com/hediet/masters-thesis/tree/9524e79f09771a6d9d74f75556a3adbff683ed35/code), `9524e79f09771a6d9d74f75556a3adbff683ed35`, was recovered with the ordinary GitHub API after the web-cache route failed. Complete inspected files:

| File | Bytes / SHA-256 |
| --- | --- |
| `code/README.md`, 3 lines | 83 / `13f16906de37d7c0b08f06d1e19875299cf3390b39e389f93e44d7b3a98eef8d` |
| `code/leanpkg.toml`, 8 lines | 249 / `d5c72b57858d5eae07a138442663c81eb7aace998916cc0afae9147121305b0c` |
| `code/src/theorems.lean`, 62 lines | 2,016 / `1a0d0c7022ee84fd6f42804b768a1325597d87bf3c3e5b7f6b2137a64fbabac0` |
| `code/src/definitions.lean`, 206 lines | 6,715 / `41f6c8f453c3f50ec8c5f488066ae9f1ee688dcd55daaad721d3179c7d90c043` |

The manifest pins Lean3.21.0 and mathlib revision `01c1e6fb62418cf562512da606350f6f6a1f24d5`. Definitions and public theorem statements agree with the selected thesis scope, including the oracle and distinct-RHS premises, explicit binding constructor and simultaneous removal. The theorem bodies delegate to imported lemmas that were not independently audited here. No Lean installation, proof checking, compilation, generator or candidate execution occurred.

This resolves S119's proof-scope question without promoting the whole thesis to a full reading or treating a theorem as a maintenance-effect estimate. Concrete analyzer failures remain the separate S135 question; higher-order program safety remains S136. All experimental holds remain.
