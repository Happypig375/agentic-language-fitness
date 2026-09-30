# S114 — Partial matches, reachable inputs and the limits of verification

**Complete author-version reading, 2026-10-01 HKT; bounded thesis/source follow-up, no execution.** Neil Mitchell and Colin Runciman, *Not All Patterns, But Enough—an automatic verifier for partial but sufficient pattern matching*, Haskell2008,49–60. DOI [10.1145/1411286.1411293](https://doi.org/10.1145/1411286.1411293).

## Identity and coverage

Zotero parent `2JBHV9IK` preceded reading. The [author PDF](https://ndmitchell.com/downloads/paper-not_all_patterns_but_enough-25_sep_2008.pdf), attachment `Q56F9ZGA`, has twelve pages and223,798 bytes, SHA-256 `b49632a956d42a826756a0f9887555b822b53fc2a0fa8132714393b0c5fa08cd`. The opening names the September2008 publication; page footers say2008/12/6. All twelve pages, sixteen figures, Table1, code examples and28 references were read. Figures/rules on pp.2–7 and11–12, the constraint comparison p.8 and results table p.9 were visually checked; opening identity was checked earlier. Full note `9U9D8W96` preserves the selected author edition. SIGPLAN DOI `10.1145/1543134.1411293` is linked publication lineage, not a new case.

The linked thesis was added as S133 before its selected sections were read. [Its partial-reading note](S133-catch-proof-and-translation-partial.md) records exact pages and formal limits; the225-page thesis is not a full reading. Four files at one pinned author-repository revision were inspected completely. No author code, compiler, tests, benchmark or dependency installation was run.

## What Catch establishes

A function can have intentionally partial patterns and still be safely called by a whole program. Catch follows this distinction: it computes sufficient input conditions under which modeled error calls cannot be reached. A local checker warning on the definition of `head` and safety of a particular caller are different questions. Conversely, merely calling an existing partial library function need not trigger a local missing-case warning. This provides a concrete rival to treating syntactic enumeration as necessary for safe behavior.

Catch08 translates Haskell98 through **Yhc Core**, removes let bindings and higher-order structure, and analyzes a small first-order language. Every internal case enumerates its datatype's constructors; originally missing alternatives become explicit error calls. It reasons backward from these error sites, rather than only comparing the written patterns with constructor sets. S113 §8.5 describes Catch as working on GHC Core; this primary account and the later repository README identify Yhc instead. The proposed GHC port in that README is not an implemented capability established here.

The algorithm distinguishes a function-safety precondition from an entailment connecting its inputs to a requested result constraint. Preconditions start at true except for error, which starts at false. Repeated conjunction with reduced body constraints makes the conditions stronger until a fixed point. Selector lifting transfers constraints from bound components to their parent structure; constructor splitting transfers them back to fields. Call dependencies, strongly connected components and cached entailments limit repeated work.

Basic pattern constraints are explanatory but can form unbounded refinement chains. Restricted regular-expression (RE) and multipattern (MP) constraints each have finitely many possibilities per datatype. MP constraints distinguish root shape and uniformly constrained recursive descendants; after uncurrying, they can absorb propositional combinations on one argument into single constraints. This improves the demonstrated scalability. Neither RE nor MP subsumes the other: MP separates certain finite list lengths, while RE can distinguish selected paths through recursive trees.

The finite representation loses information. MP cannot express a general list having at least two elements; one resulting sufficient approximation requires an infinite list. Bounds relative to array/list lengths, number-theoretic relations and some tree/path distinctions are outside the implemented model. Primitive integers are abstracted to four constructor classes and characters to one; most IO sources may return any value of their modeled type. Type-class methods may be assumed not to fail or instantiated at a chosen type. Those are model assumptions, not proofs about arbitrary external effects or instances.

The safety calculation is deliberately too strict about laziness: it demands safe arguments even when a callee may ignore them. Inlining Boolean operators handles some examples, but `False && error ...` illustrates a potential false alarm. Infinite inputs may avoid a particular error through nontermination; the paper explicitly illustrates this with reverse. **Absence of the modeled failure is not termination, total intended behavior or a successful interaction.**

## Formal and translation dependencies resolved in S133

The thesis states the soundness theorem for closed, well-formed first-order expressions **that evaluate to normal form**. Its explicit Bottom constructor denotes program failure, separately from evaluator divergence. The argument requires the constraint operators to satisfy two consistency properties; it does not turn successful analysis into a termination proof.

The MP argument uses lemma MP2, explicitly not proved: the author reports Lazy SmallCheck exploration through depth4,446,105,404 tests representing a larger input space, without a counterexample. AppendixA's summary calls the whole development a detailed argument with limited type checking, not a fully machine-checked proof. RE's corresponding lemmas were not attempted there. These are material proof-status limits, not evidence of an actual counterexample.

The thesis also bounds the broad conversion claim. Its first-order reduction can retain higher-order residues when termination bounds intervene, primitives expose functions or unbounded information is stored in closures. In its separate transformation evaluation,66 nofib programs compile under Yhc;25 other programs do not, four transformations are curtailed and five further programs retain higher-order expressions. These are not additional Catch safety successes. The later README likewise makes Yhc acceptance a prerequisite and cautions about higher-order/type-class roots.

## Evaluation, changes and positive findings

Table1 contains fourteen nofib Imaginary programs plus FiniteMap and HsColour. All sixteen rows were reconstructed. The original Imaginary sources range from9 to91 lines, excluding libraries; the measured Core includes required Prelude/library code. Six Imaginary rows are starred for additional changes and four have no error calls. General command-line parsing changes are discussed separately, so an unstarred row must not automatically be called an untouched end-to-end executable.

MP transformation/analysis times span0.1–7.5 seconds for the fourteen examples. The paper reports that RE verifies only eight modified examples within ten minutes, without a complete paired timing table. FiniteMap is reported at1.6 seconds and1.0MB maximum residency at collection; HsColour at2.1 seconds and2.7MB. These are checker-resource observations on selected programs, not developer time, application performance or a modern scalability guarantee. Hardware/repetition/dispersion for this table are not specified in the paper. Thesis chapter5's timing environment is not silently assigned to chapter6 or this table.

There are two ways to satisfy a failure obligation: restrict calls to the valid input domain, or extend the function's definition with behavior on formerly failing inputs. The authors prefer small local changes and often choose the latter. Examples replace tail with drop, add default head/modulo behavior, or replace an unused undefined argument. Such edits may make verification easier but require a separate decision about intended behavior. The average-of-empty-list example returns zero after modification; the proof does not establish that zero is the desired result.

Positive findings remain concrete. Catch verifies the complicated partial matches in Digits of E2, including recursive result destructuring and arithmetic preconditions, without the extra algorithm edits required in other examples. FiniteMap's remaining issue concerns assuming total-order laws from an Ord interface that does not enforce them; changing the implementation to branch on the three-way comparison result makes the structural choice explicit. The claimed speed improvement for that edit is not separately measured here. Its prose describes fourteen incomplete patterns while Table1 records thirteen error calls for the changed version; these are different stages/units, not an independently reconstructed fault count.

HsColour needs four patches. The authors give three concrete crash-triggering inputs involving preferences, LaTeX formatting and HTML anchoring; the fourth is not established as a real bug. This is useful defect-discovery and repair evidence, without a randomized comparator or independent reproduction. The XMonad account covers a36-export pure layout-data API, with six initially concerning issues reportedly fixed and repeat use during evolution. It does not verify the complete window manager, external interaction or every future edit. The quoted developer experience is a practitioner account relayed by the authors, not independent measured effort.

## Bounded source inspection and behavior correspondence

The [author repository](https://github.com/ndmitchell/catch/tree/5d834416a27b4df3f7ce7830c4757d4505aaf96e) was pinned at `5d834416a27b4df3f7ce7830c4757d4505aaf96e`, dated2015-03-26. The paper-era version was not identified. Complete inspected files:

| File | Bytes / SHA-256 |
| --- | --- |
| `README.md`,100 lines |4,599 / `5594efa19fb9a1b9c9e5ed0a260ae529eba3c278f8c1422bab6f7fb71bf2607e`|
| `examples/Nofib/Primes.hs`,17 lines |320 / `a9a25bec8fc81392d4280ae2dc5bb05b51165250fedc4f5d6be310c8b5e8ca82`|
| `examples/Nofib/Wheel2.hs`,45 lines |1,117 / `fa4bfbd933d9b9967b1e29d3505f8f9ab686ee5c33149cc219f6c68c6fd63562`|
| `examples/Nofib/Wheel2_Safe.hs`,47 lines |1,208 / `5a806d40f77970208b69ce31714e7f1aaa2b0051483843493cde1e5afaa19a35`|

The README says the tool is unmaintained, difficult to compile because of version incompatibilities, and dependent on Yhc. This qualifies present-day usability without negating historical results. Primes exposes an argument-taking root and a natural-number constraint comment; it is not the paper's command-line parsing wrapper.

The later Wheel2 pair adds defaults and an empty-list catch-all, but it also changes the nonzero modulo branch to return its dividend and changes main from selecting an indexed prime to printing the whole prime list, ignoring its argument. The modulo helper therefore is not generally equivalent even away from division by zero: for inputs5 and2 it denotes5 rather than remainder1. This is a static reading of the file, not a program execution or proof that the paper measured this revision. **The recovered safe-named file is not a certified behavior-preserving successor or a reproduction of the reported benchmark.** No replacement artifact or corrected historical outcome is invented.

## Synthesis and follow-up

Together S113/S114 separate local coverage from sufficient whole-program inputs, and both from intended behavior. Catch supplies positive proof-of-capability and reported defect findings, while its expressiveness, translation, proof status, preparation edits and version limits constrain transfer. These distinctions matter to D1's independent old/new obligations, but do not authorize construction or establish an agent effect.

The full bibliography was examined. Catch05's2005 symposium/2007 publication lineage, Reach input generation, Maranget coverage, explicit contracts and type-encoded nonempty structures remain conditional methods. The author page corroborates the delayed Catch05 publication and links the thesis; neither preliminary edition becomes an independent replication. S119 is the acquired next checker method; S115/S118 extension, S116 practice and the now-acquired S131 contrary task design remain active. Whole-background coverage is not complete.

**Unique:** unresolved; safe partial matching and program-context reasoning are established predecessors. **Valuable:** concrete verified examples and reported crash repairs coexist with adaptation costs and limited current usability; net maintenance benefit and Nu/agent transfer remain unmeasured. **Scientifically valid:** selected methods/results and proof/translation limits are reconstructed; exact historical artifacts and independent intended behavior remain open. All experimental holds remain.
