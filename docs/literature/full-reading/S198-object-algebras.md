# S198 — Factory interfaces as an extensibility boundary

**Complete author-manuscript reading, 2026-10-02 HKT.** Bruno C. d. S. Oliveira and William R. Cook, *Extensibility for the Masses: Practical Extensibility with Object Algebras*, ECOOP 2012, DOI [10.1007/978-3-642-31057-7_2](https://doi.org/10.1007/978-3-642-31057-7_2). Reader: the main Codex AI session. All **25 manuscript pages**, **15 figures** and **50 references** were consumed; every page was visually inspected. No appendix is present. This is a method reconstruction, not compilation, execution, independent review or experimental reproduction.

The record preceded reading: native parent `VYNUY9BT`, note `IB8UJYWJ`, author PDF `CNMSSXM5`; **350,621 bytes**, SHA-256 **`e866576757535b24286f74af6942225623bef9f4e6ebc8be58c1f82f2e8b67cc`**. Source: [Cook's author copy](https://www.cs.utexas.edu/~wcook/Drafts/2012/ecoop2012.pdf). The prior native read-back verified parent version 4694 and attachment version 4692, preserving collections `PKLXQNEE`, `MBYQJXUF` and `IPZX66LF`. The publisher and registered metadata give **pages 2–27, or 26 pages**; correspondence with this 25-page author manuscript is not established. The publisher currently supplies a subscription preview rather than the final body. Full author-copy coverage does not imply complete final-edition comparison.

**Library write limitation:** during the supplemental-source check, Zotero 10.0.3 was no longer running. Two ordinary launches exited before its enabled local API became available; the startup log mentions a missing loading-icon resource, without establishing the cause. The existing record/PDF remain the reading basis. Synchronizing this completed note and any later attachments is pending; no successful new native write is claimed.

## What the method establishes

The paper supplies a constructive alternative to fixing all variants and operations in one globally closed datatype or class hierarchy. A generic factory interface describes a selected set of constructors. Different implementations interpret the same construction recipe, and extended interfaces require additional constructor cases. Thus the type boundary can sit at the **factory required by a client**, rather than at a pattern-match expression in that client's final objects.

The useful positive result is concrete: adding an operation or language variant can reuse existing implementations and builders under the demonstrated interface relationships. Batches supplies a larger author-built application with five interpretations, multiple syntax categories and mutually recursive operations. Claims of low conceptual overhead, practical convenience and architecture separation are author assessments. The paper contains no controlled maintenance comparison, participant study, comparative runtime benchmark or quantified integration-effort result.

## Requirements and construction — §§2–5, pp.3–12

The expression-problem requirements are extension in both dimensions; statically preventing an operation from receiving an unsupported variant; preserving existing code without modification/duplication; separate compilation/type-checking; and composition of independent extensions. These are design requirements, not a behavioral oracle for an intended successor program.

`IntAlg<A>` has methods for integer literals and addition. A builder parameterized by `IntAlg<A>` constructs its expression solely through these methods. `IntFactory` chooses ordinary `Exp` objects as the carrier; another implementation chooses printable objects, and a third directly returns strings. The same builder can therefore produce different interpretations without requiring an `accept` method on the existing expression classes. The relation to constructive algebraic signatures, F-algebras and Church encodings explains why an abstract construction recipe can act like a fold. This exposition is not a mechanized soundness proof for arbitrary host-language programs.

Three integration boundaries matter:

- **Client preparation remains.** Existing classes need no visitor hook, but client construction must use the factory interface instead of concrete constructors. The recipe can then be rerun with another factory. This does not automatically add operations to an arbitrary already-created object whose construction history is unavailable.
- **Traversal style remains a choice.** Direct string-valued interpretation suits bottom-up operations. Producing objects with delayed methods supports other control patterns and mutually recursive operations, at the cost of constructing those objects. The paper does not measure that cost.
- **A supported variant is not necessarily a semantically valid expression.** The initial evaluator returns a `Value` interface with integer/Boolean accessors. A common carrier does not itself prevent every object-language type error, nor does implementing every factory method establish correct new-case behavior.

An extended `IntBoolAlg<A>` adds Boolean literals and conditionals. Extended evaluators/printers implement these constructors while inheriting integer behavior. A richer interpreter can process a builder requiring only `IntAlg`; an old integer-only interpreter cannot satisfy a builder requiring `IntBoolAlg`. The direction follows the factory parameter/interface relationship. The ability to distinguish a client's required cases is stronger than passing every term through one globally open `Exp` interface, but the new cases still need implementations.

The p.8 illustrative test assigns an `eval()` result directly to `int`, whereas the earlier declaration returns `Value`. This is a bounded listing inconsistency, not an executed failure or evidence against the construction principle. Exact source correspondence remains a supplemental-code question.

## Multiple sorts and state — §6, pp.13–15

`StmtAlg<E,S>` distinguishes expression and statement results. It adds variables, assignment, expression statements and sequential composition. Passing two expressions to statement composition is rejected by the illustrated generic interface. The footnote generalizes this arrangement to one type parameter per syntactic sort.

The evaluator factory owns a **mutable map from variable names to values**. Produced expression/statement objects capture that environment and access it when their evaluation methods run. Sequential statement composition invokes its children in sequence; expression statements discard their expression value. Objects created through the same factory share its map. This supplies an explicit state owner and supports the language example, but supplies neither immutable history nor a policy for migrating a live environment, pending work or external effects after an edit.

## Composition and its costs — §7, pp.15–19

| Construction | Mechanism demonstrated | Remaining obligation |
| --- | --- | --- |
| Interface union | Multiple interface inheritance combines independent integer and Boolean constructor interfaces | Agree on the carrier and resolve the meaning/ownership of overlapping cases |
| `Union<A>` | A schema-specific wrapper forwards each constructor to one component factory | Write the delegation methods; Java's single class inheritance does not automatically combine implementations |
| `Combine<A,B>` | A builder produces paired interpretations, forwarding each constructor to both factories | Preserve intended evaluation/effect order; pairing is not concurrent execution |
| `GUnion` / `GCombine` | Type parameters with refinable upper bounds preserve component-specific capabilities through later extension | Extend the appropriate combinator and implement its new cases; the body defers complete code to the author archive |
| Extensible values | A separately parameterized value factory constructs evaluation results; a bounded value interface supplies required observations | Extend value/expression interfaces and their bounds consistently; this is not automatic compatibility of arbitrary independently designed values |

The first union/combination classes are explicitly acknowledged to be insufficiently extensible. Section 7.4 adds **bounded polymorphism**, while avoiding recursive F-bounds. Consequently, “simple generics” does not mean that every extension uses only an unconstrained type parameter or requires no manual composition. The website additionally treats independent composition as optional for its **basic** cross-language examples; this is narrower than silently certifying every example against all five paper requirements.

The debug-combination example prints and evaluates child expressions during factory construction, before returning the paired result. This illustrates how a retroactive operation can use an existing evaluator and printer. **Our source-level inference:** transferring that eager/repeated evaluation unchanged to an effectful environment could alter when or how often effects occur. The paper's arithmetic demonstration does not establish that such a transfer preserves semantics. No author implementation or counterexample was executed. This is consistent with the transformation-specific effect obligations already reconstructed in [S138](S138-compositional-data-types.md) and [S140](S140-monadic-maps-folds.md).

## Batches — §8, pp.19–21

The reported application interprets a scripting language used to batch remote operations. Its five implementations cover direct evaluation, secure evaluation, SQL translation, partitioning and code generation. Figure 13 displays twelve constructor methods, with redundant helpers omitted; Figure 14 lists nine mutually recursive SQL-translation operations. Secure evaluation carries additional state for authorization checks. SQL translation builds a specialized object hierarchy, allowing ordinary method calls between those operations.

Partitioning extends the syntax with three displayed constructors for external expressions, dynamic calls and mobile data. It constructs an intermediate program and uses visitor-like processing to rebuild the final code-generation algebra. Thus the architectural claim is specialized representations and interfaces for different tasks, not removal of every visitor or intermediate representation. Some constructors still accept general objects or string names; the factory type signatures alone do not prove database, security or remote-effect correctness.

The authors describe subsystem separation as a subjective benefit. There is no measured before/after change task, alternative implementation with equal behavior, startup/training cost, latency/memory result or adoption sample here. The demonstration remains meaningful evidence that the technique was used beyond the minimal arithmetic example, without converting it into a measured net benefit.

## Primary supplement and discovery coverage

The paper's old `ropas.snu.ac.kr/~bruno/oa` and Batches wiki routes did not yield readable pages through the web tool. The [current author-hosted index](https://i.cs.hku.hk/~bruno/oa/) was fully read, including its requirements and attributions: Java by Oliveira/Cook, F# by Parkinson/Bierman, C# by Moritz, plus Scala/Haskell/C++ examples. **These are source listings advertised by the author page, not inspected implementations.**

The index links `OA_Java.zip`, `OA_Fsharp.zip` and `CSharp.zip`. The web tool returned an unsupported-ZIP response, cache miss and unusable fetch response respectively; ordinary local HTTPS downloads for all three ended with connection resets. A second ordinary Java download using Windows curl also reset. No archive, source-file inventory, hash, attachment or source execution was obtained. Two exploratory alternate-page URLs also failed; they are not confirmed author locators. The exact §7.4 implementation, F#/C# feature requirements and dated Batches source therefore remain **access/reading gaps**, not evidence of absence or incorrectness.

SC133 uses the exact DOI with `limit:20, offset:0` and returns **one of one** metadata records, content denied, with no abstract, full-text passage or quoted citation context. This resolves the earlier subtitle-search miss. The tally is not a verdict. W316–W320 record the primary-page/locator checks, supplied search passages and unsuccessful source retrievals in the [ledger](../nu-background-searches-2026-09-30.md). A practitioner's C# translation and author-answer route remain conditional follow-ups from supplied indexed passages; neither full account nor repository was read in this segment. No graph or new Consensus page was retrieved.

## Consequence for the wider survey

S198 makes an additional type/evolution mechanism concrete: selectively required factory interfaces and reusable interpretations can support both new cases and new operations in ordinary generic OO languages. It complements [S137's composable signatures](S137-data-types-a-la-carte.md), while moving representation and integration work into factories, wrappers and specialized objects. The paper explicitly excludes a straightforward Java Church encoding of general GADTs because that would require higher-kinded abstraction; it does not solve every richer type-evolution problem.

For Nu/ISE, distinguish the required syntax, the implementation of each operation, state ownership, semantic laws and actual task outcomes. Factory-based extensibility is neither an immutable-world guarantee nor measured superiority to Nu, F#, C#, ECS or conventional classes. It also does not settle D1's explicit-current-case versus equivalent-catch-all comparison: both candidates may be exhaustive, and appropriate catch-alls remain valid. New interface obligations can identify implementation sites without specifying desired behavior.

**Next consequential work:** read the already recorded/acquired S199 live-documentation comparison to connect source visibility with measured task outcomes, preserving its favorable signal while reconstructing allocation, correctness and tool preparation. S194's original modularity replication and S200's positive concern/defect method remain accessible independent priorities. Restore the native note write and inspect the author archives if ordinary access becomes available; neither requirement closes the broader discovery, runtime or oracle frontiers.
