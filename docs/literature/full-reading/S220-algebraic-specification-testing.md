# S220 — Algebraic testing: exhaustive sets, finite assumptions and observations

**Identity:** Marie-Claude Gaudel and Pascale Le Gall, *Testing Data Types Implementations from Algebraic Specifications*, in *Formal Methods and Testing*, LNCS 4949, 2008, pp.209–239, DOI [10.1007/978-3-540-78917-8_7](https://doi.org/10.1007/978-3-540-78917-8_7). C02 1-83 is the discovery lead. The selected body is [arXiv:0804.0970v1](https://arxiv.org/abs/0804.0970), dated 7 April 2008, with 32 physical pages. The publisher supplies chapter metadata and a bibliography, but its 31-page body has not been acquired. An earlier LRI report, RR1468 dated 8 February 2007, is encountered only through its opening search passage. These are a work/edition lineage, not independent studies; full final-copy equivalence is unverified.

**Library and coverage, 2026-10-02:** native collection `PKLXQNEE` (238 parents) and the global top-level inventory (1,232 items) were checked by DOI/title before reading. Parent **`7CX6WJKQ`**, PDF **`PEU6SSMP`** and note **`VFXT2UCB`** were created for the selected work; the record preceded intentional body reading. The attachment is **357,172 bytes**, SHA-256 **`661c0803a2b1501e05f6be14e3732841213930cd74506795bb3ccb28629efe07`**, MD5 **`2512a6bfced4a05926f00b4a581d9c68`**. Its stored bytes were read back and verified. Copyrighted bodies, extraction and page images remain in ignored local storage.

All **32 pages** are read, including nine sections, eight numbered definitions, seven numbered examples, the sole figure, displayed arguments, nineteen footnotes and all 57 references. Visual inspection covers **pages 1, 4–5, 7–10, 12–21, 25, 27 and 30–31**: 21 pages, including Figure 1 and the material mathematical/printed ambiguities below. There are no tables or appendices. The publisher's web bibliography has 58 entries, including a duplicate of *In black and white* at entries 20/21; that is not an additional selected-body reference. No author software, proof assistant, test generator or experiment is executed here.

## What the conformance argument requires

Sections 2–4 (pp.3–9) model the implementation as an algebra over the specification's sorts and operations. A test is an instantiated equation together with its experiment and verdict; an input alone is not a complete test. The basic exhaustive set contains ground instances of the axioms. Its adequacy depends on a reachable implementation algebra and reliable verdicts for ground equations. Reachability matters because concrete values outside those constructed by the specified operations otherwise escape this account. Treating implemented operations as mathematical functions also excludes arbitrary unmodeled hidden state, side effects or nondeterminism.

Under the stated minimum testability hypothesis, passing the exhaustive set characterizes satisfaction of the specification by the reachable implementation. This is a constructive, specification-relative result. It does not assert that a practical finite suite covers every implementation, or that the specification contains every requirement of an interactive system.

Constructor completeness supplies a further route: every ground term has a constructor representation, and the specified constructor equality has the required discriminating properties. With correct equality on the relevant constructor sorts, one can solve conditional premises in the specification and test their conclusions. Letting a faulty implementation decide which premises hold can instead suppress the very obligation being tested. The alternative ASTOOT route compares terms with normal forms and requires convergent rewriting and a compatible implementation interpretation; it changes the assumptions rather than removing them.

The running container specification has a generated empty value and insertion, membership and single-occurrence removal. Its first six axioms do not themselves impose the later order-insensitive equation. Keep the signature, chosen axioms and observational interface explicit when transferring a result to another representation.

## Why a finite suite needs more than specification coverage

Sections 5–6 distinguish three choices that must be justified separately:

| Choice | Claim needed to extend the observed result |
| --- | --- |
| Representative tests within a subdomain | Uniformity: a representative's passing verdict stands for the remaining members of that subdomain. The covering subdomains may overlap. |
| A finite term/input bound | Regularity: passing tests below that bound stands for the larger cases. A convenient bound is not evidence that this implication holds. |
| A finite set of observable contexts | An observation hypothesis: omitted contexts cannot distinguish an implementation that the selected ones accept. |

Unfolding conditional axioms refines the subdomains, weakening a coarse uniformity assumption by generating more tests. LOFT's account requires suitable constructor completeness and convergent conditional rewriting; its soundness and covering arguments have those premises. The cited extension to more general positive conditional specifications unfolds more occurrences and can produce many tests. The chapter's favorable experience with one or two unfolding steps is useful practice evidence, not a universal adequacy threshold. Random generation and premise filtering are alternatives with their own accepted-case distribution and rare-premise costs.

These methods make test selection explainable. They do not infer uniformity, regularity or coverage of every relevant effect merely from the selected tests passing. White-box knowledge can help choose a size bound or check a modeling assumption; it is a source of evidence to record, not an invisible guarantee.

## Observational equality and conditional premises

For abstract data, concrete representation equality is often unavailable or inappropriate. Section 6 (pp.14–21) instead compares results in observable sorts through contexts containing one abstract-data hole. Constructors followed by observers may be consequential: direct queries alone need not be enough. Without additional restrictions, a previously omitted context can be the one that distinguishes two values.

The resulting correctness notion allows an implementation to be observationally equivalent to a reachable model of the specification. A list representation can therefore implement an order-insensitive interface without identical internal values. The equivalence still quantifies over the relevant observations; agreement at a few chosen checkpoints is not its definition. The selected body's quotient construction is a proof sketch with dependencies elsewhere, not a complete independently checked proof here.

For equations, ground instances under the appropriate observable contexts give the exhaustive-test argument under the observational testability assumptions. Conditional specifications require extra care. If a premise concerns a nonobservable sort, replacing its equality by agreement under a finite set of contexts can make the premise too weak. An obligation can then be imposed when the actual abstract premise is false, so a correct implementation fails the constructed test. Solving premises using specification consequences under the stated assumptions avoids treating finite observed agreement as established abstract equality. Positive and negative positions, and literal axioms versus their semantic consequences, cannot be interchanged without an argument.

The practical implication for Nu's B02/B04/B07 questions is precise: a representation map, successful type check, replay, or finite state comparison supplies only its defined observation. None alone establishes every future operation, pending callback, resource effect or temporal obligation. Conversely, a justified observation abstraction can legitimately ignore concrete representation differences. Rejecting every such difference would discard valid implementations.

## Case evidence retained at its reported scope

The chapter summarizes earlier applications; it is not a new controlled experiment across them. Sections 8–9 report useful outcomes alongside a miss and a null result:

| Application | Reported result and scope |
| --- | --- |
| Lyon subway controllers | Door and speed specifications use 25 and 34 axioms, with shared modules containing 108 functions and hundreds of axioms. Different door uniformity choices yield 230, 95 or 47 tests; the speed selection yields 95. Certification used them as a checklist against developer tests and found a tricky untested combination of conditions. That is a coverage discovery, not a reported production-defect rate. |
| C component from a nuclear shutdown system | The chapter says all but one of the already known bugs were found, without giving the total. The miss involved hidden shared state and instances larger than the selected regularity bound; structural/static methods could expose it. The original comparison is reference 52; the S221/S222 follow-up below now qualifies its fault population and testability conditions. |
| Ada component library and transit node | The Ada application constructs axioms manually and uses LOFT, without a quantified result here. Transit-node testing finds an unwanted scenario in the specification. Specification discovery and implementation fault detection are different outcomes. |
| Two-phase commit | Data-type tests find no fault; formal derivation is offered as a possible explanation, not a measured cause. The later account separately reports a preprocessor defect and memory-management/timeout problems in the broader implementation. These results concern different layers and must not be collapsed into either universal success or universal failure. |

VDM applications require operation sequences, not merely isolated-operation partitions. Lustre/GATEL introduces environmental and test-purpose constraints for reachable scenarios. LOTOS integration depends on the modeled communication and timing assumptions; absent memory/time detail can matter in an implementation. Partial functions require a definedness/equality policy. Hiding and modular composition can alter available axioms and require structural/preservation assumptions. These extensions support a constructive account of reusable testing methods while leaving the specific oracle and integration work visible.

No pooled detection rate, controlled developer-effort effect, Nu-specific quality gain or independently reproduced application result is supplied by this reading.

## Printed ambiguities and their bounded consequences

Visual inspection confirms several material problems in this selected preprint; final publisher corrections have not been checked.

- On p.12, displayed unfolded membership cases contain `y :: isin(...)`, although Figure 1 assigns membership a Boolean result. This is ill-sorted as printed. The reconstruction uses the well-sorted original axioms; the displayed text is not executable evidence.
- Definition 6 on p.14 says that a minimal observable context contains a strict observable subcontext, while its following discussion and footnote 11 require the opposite. The discussion also gives an equivalence where ordinary congruence supplies only the implication from inner equality to outer equality. Own symbolic check: a constant Boolean outer function maps both unequal Boolean arguments to the same value. That defeats the reverse implication, while the intended minimal-context sufficiency argument needs only the forward one.
- On p.20, the nonobservable-premise example prints a reflexive container comparison and muddles the pass/fail wording around the impossible Boolean conclusion. The reconstructed warning follows the conditional logic: weakening the premise can reject a correct implementation. It does not rely on the inconsistent literal sentence.

These edition-local defects delimit what can be credited from the printed derivation; they do not erase the framework, its explicit assumptions or its scoped application results. Own checks are passive mathematical reasoning, not author-code execution or formal verification.

**Primary-case follow-up, 2026-10-02:** [S221](S221-formal-statistical-testing-access.md) resolves reference 52 and its revised chapter, but only the latter's two-page preview is acquired. [S222](S222-statistical-testing-thesis.md), the coauthor's thesis, reconstructs the same experiment in Chapter III pp.78–80. Its 1,345 eligible cases are mutants, not naturally occurring industrial defects. Five algebraic suites leave 0/0/1/2/0 survivors when calculated internal state is observed; filtered-output-only observation leaves 29–47. Direct state control in the statistical comparator changes the equivalent-mutant classification and eligible population to 1,416, while suite lengths differ (282 versus 405). This supports the favorable formal-testing result with explicit conditions; it does not identify a general real-fault detection rate or isolated strategy effect. Precise original LOFT bounds and final-edition wording remain unread.

**Disposition and continuation:** C02 1-83's primary selected-edition gap is closed. B02/B07/B12 gain a concrete separation of specification conformance, testability, finite selection and observable verdicts, now with primary same-case control/observation evidence. S222's integration chapter adds a positive initialization-interaction result and a prior-suite miss. Continue independent game/runtime alternatives and temporal-evolution synthesis; preserve S221's missing bodies, S218's visuals and S219's body as specific access tasks. Whole-survey coverage and empirical benefit remain open; no construction or experimental allocation follows.
