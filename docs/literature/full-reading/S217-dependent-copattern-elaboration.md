# S217 — Dependent copattern elaboration and source meaning

**Identity:** Jesper Cockx and Andreas Abel, *Elaborating dependent (co)pattern matching: No pattern left behind*, Journal of Functional Programming30,e2(2020), DOI [10.1017/S0956796819000182](https://doi.org/10.1017/S0956796819000182). Selected body: [Chalmers institutional version of record](https://research.chalmers.se/publication/515222/file/515222_Fulltext.pdf), with an institutional cover followed by43 article pages. The publisher lists online publication21January2020. The 2018 ICFP/PACMPL precursor, DOI [10.1145/3236770](https://doi.org/10.1145/3236770), has30 pages and lacks this subtitle. Journal p.4 explicitly identifies the extension: finer small-step semantics and preservation without a normalization assumption, a new catch-all discussion, and detailed proofs. These are one method lineage, not independent replications; the 2018 body is not separately read.

**Library and actual coverage, 2026-10-02:** native parent/note/PDF **`TH4T6VLV` / `CIYFYCNX` / `YZ2NGIG3`**, collection`PKLXQNEE`; the record preceded selected body reading. PDF **44 physical pages,2,560,777 bytes**, SHA-256 `56c78feeae93e78f87ccc16d3c7cfe1628893bd9dc2410db9b97d1ed6b8856bd`, MD5 `c449766373fee9f1d73fe90b1e4c160a`. **All43 article pages plus the institutional cover are read as text**, including Figures1–16/A.1–A.4, Tables1–2, examples, displayed proofs, footnotes and38 references. Visual coverage: cover and article pages **1–13,15–18,20,23–29,31–38,42–43** (36 physical pages). Formula images resolve missing Greek symbols and figure rules in extraction. Acquisition metadata records the original2020 PDF creation and the2026 institutional wrapper; these are not two publications. No Agda program, compiler, proof assistant or author test is executed.

## Problem and contribution

A dependently typed frontend can elaborate an apparently meaningful source theorem into a well-typed core term that expresses something else. Core typechecking can establish properties of that translation without establishing fidelity to the source clauses. The paper isolates the first translation step, **ordered dependent pattern/copattern clauses to case trees**. Translation from case trees to primitive eliminators is a different step studied elsewhere; Agda retains case trees in its core.

The method constructs a typed case tree while refining ordered source clauses and their constraints. Its formal contribution separates type preservation/progress from correspondence to source matching. Its implementation contribution is a reworked Agda left-hand-side checker with more flexible forced patterns and reported bug fixes. This is constructive and formal evidence with public implementation cases, without a comparative maintenance, agent-repair or productivity estimate.

## Language, dependent observations and ordered checking

Sections3–4 define a core with dependent function types, a predicative noncumulative universe hierarchy, parameterized inductive datatypes, coinductive records, an identity type and named functions. Terms introduce data and eliminate functions/records; case trees supply function/record introduction and data/equality elimination. Source patterns include constructors, variables, forced arguments, forced constructors and absurd patterns. Copatterns include observations through record projections.

Dependent record fields may refer to earlier observations of the same `self`. The cozero and countdown examples(pp.7–8) require the earlier head/iszero branch's checked equations before checking later tail/pred branches. Case-tree checking therefore threads the signature through branches in the required order. Matching an equality proof invokes proof-relevant unification: a strong unifier refines the context, a disunifier justifies an impossible case, and unresolved unification causes elaboration failure. An arbitrary most-general substitution alone is insufficient; the specified substitutions must also satisfy the computational inverse properties in Definition8.

Forced patterns mark arguments whose values follow from typing and must not be inspected to choose a branch. Forced constructors additionally allow variable binding inside that argument. After an equality split, the case tree records which accumulated bindings can be discarded. The p.8 example shows why discarding the user's entire forced constructor pattern can incorrectly leave a variable unbound; the intended elaboration instead substitutes its type-determined value in the body.

The core omits anonymous lambdas, general indexed families, eta equality and several practical features. Section3.5 discusses encodings/extensions rather than silently including them in the proved language. Positivity, termination and productivity checks are not developed here. Hence preservation/progress must not be upgraded to a complete totality, normalization or consistency proof for all Agda features.

## Matching is not just success or failure

The matching relation distinguishes a successful substitution, a **definite mismatch**, and a computation that is stuck. A fallback may be used only after all earlier clauses definitely mismatch. A blocked match on an open term is not such a mismatch.

There is a further restriction: a mismatch on one component does not short-circuit a stuck match on another component. To classify an earlier multi-argument clause as mismatching, the relevant submatches must all resolve to match or mismatch, with at least one mismatch. This conservative policy supports different well-typed splitting orders. It differs from lazy matching that chooses the next clause as soon as one component fails.

In the p.9 example, an argument has abstract type A until an equality witness refines A to Bool. The checker cannot inspect that argument as a Boolean first. A liberal source rule would reduce an application with one false argument even while other arguments remain open; the actual case tree must inspect another argument or the equality witness and can get stuck. Restricting matching makes the source rule agree with every permitted splitting order. It does not demonstrate that a more eager source semantics has been preserved unchanged.

This issue concerns definitional computation of open terms in dependent typing. It is not evidence that F#'s ordinary closed-value pattern matching has the same defect or that every catch-all is semantically suspect.

## Elaboration and guarantees

The algorithm(Figures10–16,pp.31–37) maintains the current context, target type, partial source left-hand side, signature and an ordered list of partly decomposed user clauses. Introducing an argument turns its pattern into a constraint; projection splitting partitions by observation; constructor/equality splitting specializes constraints and removes impossible clauses. Once the first remaining clause's constraints are solved, DONE checks its substituted body and creates the leaf. This is not a search over arbitrary successor implementations.

Three guarantees have different premises and roles:

| Result | Scope and consequence |
| --- | --- |
| Lemma12, simulation | A well-typed case tree and the checked clauses generated from that tree simulate one another under the stated matching/evaluation relations. Those generated clauses are distinct from the original overlapping user clauses. |
| Theorem17, preservation | When all functions in the signature are given by well-typed case trees, evaluation respects definitional equality and preserves types. The journal develops this without assuming normalization. |
| Theorem18, progress | With a well-formed signature of well-typed case trees, a function applied to closed eliminations can take a step when its resulting type is neither a function nor record type. This does not assert termination or reduction of every open application. |
| Theorem22, source correspondence | If well-scoped user clauses successfully elaborate, earlier clauses definitely mismatch under the conservative relation, and clause i matches, evaluating the resulting tree yields that clause's substituted body. Successful elaboration/typing alone is not this semantic-correspondence argument. |

The displayed proofs include the simulation cases, respectful-pattern/signature argument, progress lemma, and the elaboration induction in Lemma25. The proof depends on scope checking, specified unification behavior, typed substitutions and the stated core. This reading reconstructs the printed arguments; it is not an independently machine-checked proof or certification of the implementation.

The formal algorithm does not diagnose unreachable source clauses. An absurd split can also leave some source patterns uninspected; Remark20 proposes checking the whole left-hand side as a term to reject ill-typed unused patterns. Thus coverage, redundant-clause diagnostics and checking every surface fragment remain distinct concerns.

Signature extension has a closed-world restriction relevant to evolution: constructors/projections may be added only while their declaration is the incomplete final entry. Adding constructors to a previously completed datatype could invalidate coverage of already checked functions(pp.15,19). The monotonicity lemma for allowed signature extensions is therefore **not** an open-world datatype-evolution theorem.

## Catch-all compression and the interactive-hole boundary

Section2.6(pp.10–11) gives an explicit difference between the formal algorithm and the reported Agda implementation. The formal algorithm checks a clause body after splitting has refined its branch context. A fallback can therefore expand into several correctly typed branches even if the original unrefined clause cannot be checked on its own.

For the three-constructor binary-number example, the formal algorithm accepts a two-clause soundness proof whose second clause eliminates impossible residual cases; the reported Agda approach needs three source clauses. For a datatype with n constructors, a decidable-equality definition can use n matching-constructor clauses plus one fallback, while the latter expands into n(n−1) unequal-constructor leaves. The n+1 versus n² comparison is the paper's source-clause construction, **not a measured reduction in runtime work, editing effort or inference cost**.

Agda keeps an extra preliminary pass that checks each source clause individually. A hole in a shared right-hand side could otherwise have multiple incompatible branch-refined types, and the authors leave presentation/interaction for that situation unresolved. Their formal behavior can model Agda by requiring individual-clause elaboration before processing the whole definition again. The implementation therefore does not realize every compact catch-all accepted by the more liberal formal presentation.

For B02/B07, this supplies constructive prior art for safe branch expansion and a concrete integration cost in interactive editing. It supports neither a universal preference for enumeration nor one for catch-alls. D1 still fixes the F# toolchain and initially equivalent arms, with both potentially exhaustive; it does not change elaboration semantics or add a dependent editor.

## Bounded implementation evidence and chronology

The paper reports integration in Agda2.5.4(released2June2018) and references six issues. This segment follows **two** consequential cases and selected release-note passages; it does not audit all six fixes, the complete changelog, all source code or a test suite.

- [Issue2896](https://github.com/agda/agda/issues/2896), opened12January2018 and closed13April2018, supplies the discarded-pattern/unbound-variable example and attributes its fix to left-hand-side refactoring2866. Its API record has zero comments and milestone2.5.4. The [2.5.4 changelog](https://hackage.haskell.org/package/Agda-2.5.4/changelog) lists it among closed issues and documents forced-constructor patterns. These corroborate a concrete accepted-feature/defect account without our executing the example or inspecting the linked refactoring.
- [Issue2964](https://github.com/agda/agda/issues/2964) supplies the open-term source/case-tree mismatch and subject-reduction failure. The issue body and **all9 returned comments** are read through the public GitHub API. A17February2018 comment proposes conservative matching and reports that its basic implementation passes the author's tests; subsequent comments report a projection/application internal error and eta-expansion problems under speculative matching. The closing14November2018 comment says the original problem is fixed; the current issue milestone is2.6.0. These are author observations and revision history, not our reproduced tests.

The 2.5.4 changelog's returned text has no2964 hit. Its later closure/milestone does not by itself date the first successful patch or prove the original fix was absent from2.5.4. We therefore preserve the paper's release statement and the finer issue chronology without claiming that all six fixes belong to one verified release or that the implementation exactly equals the formal algorithm.

Ignored public-API snapshots preserve this bounded inspection:

| Snapshot | Bytes | SHA-256 |
| --- | --- | --- |
| Issue2896 object | 8,339 | `d04fb3857a45173c439d3f6670cffc56339618c64fc113f8b79e15a9e9ab5773` |
| Issue2964 object | 9,394 | `7b1cb2b8ffcb773876ab7e99c2535132549730beaf510ead4ee6a00a88f5ef90` |
| Issue2964 comments, requested100/returned9 | 20,186 | `ccbc7073e64384ba46167258300552053d887f6b118e6fa4332d0f3b5682caee` |

The inspected release-note passages concern forced patterns and the located issue list; other returned headings/code are not promoted to verified performance evidence. No repository clone, build, package installation, regression execution or candidate experiment occurs. Public source excerpts and API bodies stay outside committed documentation.

## Survey consequence and next action

S216 established that defaults can retain residual type information. S217 adds that a frontend must preserve the intended relation between source clauses and core behavior; coverage and core well-typedness do not replace that relation. Conversely, a semantics-preserving elaborator does not supply future application requirements that the source/specification omits. Compact clauses, generated branches, diagnostic opportunities, editing-state information and behavioral obligations are separate units.

The strongest next independent gap is the already acquired **S187 expanded practice review**: its58-page journal edition covers a materially larger sample than the older preprint and remains incompletely read. That reading can improve B04/B08/B10/B12's account of live patching, operational recovery and evidence coverage, balancing this completed type-mechanism continuation. Algebraic testing, .NET/game transfer and temporal-oracle discovery remain available by consequence. This paper closes its edition/method gap without closing any whole background theme or reopening experimental work.
