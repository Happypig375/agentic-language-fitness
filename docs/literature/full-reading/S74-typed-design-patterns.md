# S74 — Typed design patterns and their assurance boundaries

**Complete author-paper reading, 2026-09-30.** Will Crichton, *Typed Design Patterns for the Functional Era*, FUNARCH 2023, pp. 40–48, [DOI 10.1145/3609025.3609477](https://doi.org/10.1145/3609025.3609477). The [arXiv v1 author edition](https://arxiv.org/abs/2307.07069v1) is dated 2023-07-13; publication metadata gives 2023-08-30 and the workshop date is September 8. These dates describe different events. Zotero parent `5N995MVS`, PDF `ZB9JAF3Z`, note `KC8JKIPU`.

All nine PDF pages, seventeen listings, the state-machine figure and all 24 bibliography entries were read. Pages 2–8 were rendered and inspected, covering all listings and the figure. The PDF is 545,296 bytes, SHA-256 `6ac5437e4b5de50255eeee198a1e9d813f80e850769695395dd706143333bfbc`. No example was compiled, no listed library was audited, and no experiment was reproduced. The author edition is the reading target; byte/text equivalence with the publisher version is not established.

## Live claim and reconstruction

B02/B03/B05 ask whether mapping domain conditions, transitions and event identities into types is distinctive to Nu, and what those checks actually guarantee. The paper is a design argument with worked Rust examples, not a comparative maintenance experiment. It explicitly draws on older typestate, heterogeneous-list and domain-modeling work. It organizes knowledge that is not fully captured by a reusable language abstraction.

| Pattern / pages | Mechanism reconstructed | Boundary relevant to ISE |
| --- | --- | --- |
| Witness, 2–3 | A restricted constructor produces a capability required by an operation | Construction must actually be restricted. A token for some administrator does not identify the current user or prove authorization remains valid later. |
| State Machine, 3–5 | Distinct state types and consuming transitions prevent reuse of an old handle; generics reduce duplicated fields/methods | Ownership participates in the guarantee. Algebraic variants alone do not supply affine consumption in F#. Legal calls also do not ensure eventual resource release. |
| Parallel Lists, 5–6 | Type-level heterogeneous lists relate formatting positions to argument count/types | The paper acknowledges more complex implementation and potentially difficult diagnostics. Coverage of encoded relationships is not evidence of lower total development effort. |
| Registry, 6–8 | A type identifier joins callback registration and payload dispatch through a type-erased internal map | Payload compatibility does not establish delivery, timing, cancellation, subscription cleanup or the programmer's intended event. |

The examples are useful prior mechanisms even when an implementation needs correction. Named production libraries illustrate claimed usage; this reading did not independently verify their versions or establish adoption rates. The paper supplies no participant sample, maintenance-task comparison, defect-rate estimate, runtime measurement or compile-time benchmark. Its discussion leaves larger architectural tradeoffs open.

## Printed-example checks and limits

Visual inspection confirmed two material inconsistencies in the author PDF. These are deductions from the printed code and language/API documentation, not reported execution results or an author correction.

- **Listing 2, page 3:** `pub struct Admin {}` contains no private field. Once its name is accessible, the advertised prevention of manual construction does not follow from putting this public empty struct in a module. The [Rust visibility rules](https://doc.rust-lang.org/reference/visibility-and-privacy.html) and [struct-expression examples](https://doc.rust-lang.org/reference/expressions/struct-expr.html) permit naming accessible items and constructing empty braced structs. An actual constructor boundary is necessary before this becomes a trustworthy witness. Omitted imports and route syntax are separate presentation issues.
- **Listing 16, page 7:** `ListenerVec<E>` already denotes a vector of boxed listeners, but the initializer puts `Vec<ListenerVec<E>>` into the erased map and then downcasts to `ListenerVec<E>`. Those concrete types differ. Under the documented [Any downcast contract](https://doc.rust-lang.org/std/any/trait.Any.html#method.downcast_mut), that downcast returns `None`; its subsequent unwrap cannot justify the example's claimed successful registration. This does not refute a correctly implemented typed registry.

These documentation checks used the current Rust documentation (the standard-library page identifies 1.98.1), not a reproduced 2023 compiler environment. Listing 9 explicitly acknowledges omitting `PhantomData`; that stated simplification is different from an unacknowledged guarantee failure. The enum file wrapper also opens directly into `Read` and checks EOF only after reading, whereas the typestate wrapper checks before reading: the displayed interfaces do not establish an identical low-level precondition for an initially empty file. Do not treat the examples as a behaviorally equivalent controlled contrast.

## Implications and follow-up

**Unique:** the constituent domain-to-type mechanisms have clear predecessors; Nu's combination and any narrower empirical question still require comparison. **Valuable:** preventing particular interface mistakes is plausible, while diagnostic burden, migration effort and net benefit are unmeasured. **Scientifically valid:** a later study must distinguish public API discipline, internal invariant correctness, ownership, and independent temporal behavior. No experiment is authorized here.

For D1, an exhaustive-versus-fallback convention remains narrower than these API redesigns: changing an operation's signature, adding ownership consumption or redesigning an event registry would introduce additional treatments. Incorrect program rejection and complete successful maintenance are separate outcomes. The paper's diagnostic-complexity concern supplies adverse cases worth considering, without inventing an effect size.

Consequential bibliography leads are Strom/Yemini's typestate (`10.1109/TSE.1986.6312929`), Aldrich et al.'s typestate-oriented programming (`10.1145/1639950.1640073`), Rust retrofitting (`10.1145/3475061.3475082`), heterogeneous collections (`10.1145/1017472.1017488`), Linear Haskell (`10.1145/3158093`), and datatype-generic patterns (`10.1145/1159861.1159863`). Their primary bodies are not read here. Prioritize those that change an active ownership, evolution, abstraction or usability claim; neither a bibliography entry nor a citation label establishes its result. Wlaschin's F# modeling book is a specific domain-modeling lineage lead, not a new full-book reading. S72 remains the selected empirical authoring study.
