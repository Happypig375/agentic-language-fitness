# S105 — Temporal breakpoints and the scope of a history witness

## Identity and actual coverage

Matthias Pasquier, Ciprian Teodorov, Frédéric Jouault, Matthias Brun, Luka Le Roux and Loïc Lagadec, *Temporal Breakpoints for Multiverse Debugging*, **SLE 2023, pp. 125–137**, DOI [10.1145/3623476.3623526](https://doi.org/10.1145/3623476.3623526). Native parent/note/PDF **`DT7UEB7I` / `ZEF5JYKG` / `JJY9ZFC2`** already exist and were reverified before continuing beyond the earlier first-page/abstract coverage. Memberships `PKLXQNEE`, `NDU9BTP7` and `MBYQJXUF` are retained. Earlier ACM/HAL failures are historical acquisition attempts; the user's library attachment resolves access.

The publisher-formatted PDF has **13 pages, 1,428,899 bytes**, SHA-256 **`0484255a9bea5b635657fff00c5cdd42f907d7096498187c6f1c6b621b4542ed`**, MD5 `c2a004561f0cc02d616ab3ce8f9e057b`. Local bytes match the previously verified native attachment identity. **All 13 text pages, seven sections, eight figures, five listings and 21 references are read.** Ten physical pages are visually inspected: **1 and 4–12**; pages 2–3 and 13 have text coverage. Natural-order extraction resolves the initially interleaved columns. There are no numbered tables or appendices. The two released repositories are inspected at the pinned, bounded scopes below; no Lean, author JavaScript, model, test or example is executed.

## The mechanism and its useful capability

This paper extends multiverse debugging from state-local predicates to **step, safety and liveness breakpoints**. A multiverse debugger explores alternative nondeterministic continuations, rather than only replaying one recorded trace. The user can step, select among outcomes, jump to a stored history entry or request a witness leading to a breakpoint. This is direct prior capability evidence for expressive interactive exploration; it is not a measured improvement in debugging time or defect removal.

The subject language exposes a semantic language interface: initial configurations, enabled actions, successor configurations and expression evaluation. Evaluation is extended from one configuration to a **source/action/target step**, including a distinguished stuttering action. A dependent interface exposes the breakpoint language's own state and transitions, but delegates predicates about the subject to that subject-language evaluator (Sections 3.2–3.4; Listings 1–3).

The finder forms a synchronous product of **subject state and breakpoint state**. This matters when two histories reach equal subject values but have different event counts or pending monitor progress: a single global hit counter cannot represent both branches. A regular-language breakpoint is searched by reachability; a Büchi breakpoint additionally needs an accepting-cycle search. The subject's acceptance predicate is unrestricted, leaving acceptance to the breakpoint. A found witness is projected back to subject configurations and added to the debugger's history.

Three implemented breakpoint languages demonstrate the separation: regular expressions compiled through Thompson construction to an NFA with epsilon transitions removed; AnimUML statecharts with variables/control structure; and statechart-based Büchi automata. Reusing statechart syntax can express repeated-event conditions more compactly than a long regular expression. This is a demonstrated representation/design choice, not a comparative usability result.

The examples use mutual exclusion. Step breakpoints identify a named transition or a changed variable; a repeated-entry breakpoint counts critical-section entries; sequence breakpoints combine conditions over states and transitions. The liveness example seeks a loop witnessing an indefinitely unfulfilled critical-section request in a deliberately faulty model (Figures 6–8). The supplied LTL condition is a **negated response property**, and its Büchi conversion is manual in the paper's example. An accepting loop is stronger evidence about an infinite continuation in the represented transition system than merely failing to see a response during a finite replay.

Do not turn that example into an unconditional fairness theorem. The checked transition system, scheduler/environment assumptions, progress enabledness and acceptance condition determine what a loop means. The paper does not establish real-world scheduling fairness or every external effect of an arbitrary implementation language. Figure 6's actual Peterson guards include the turn/other-flag disjunction; the abbreviated prose description should not replace those transition conditions.

## Start state, pending obligations and deadlocks

The finder replaces the subject's initial set with the **selected current configuration(s)**. It does not automatically replay all history preceding the lookup into the monitor. The formal debugger passes the selected configuration to the finder (`rmd_bridge.lean`, lines 105–111); the temporal finder instantiates the breakpoint from its syntax and returns only projected subject states (`rmd_step.lean`, lines 44–53). In the prototype, `main.js` 43–45 constructs the breakpoint anew for each finder call; `DebugSTR` passes the current subject state at 147–150. Stored history and state within one search therefore have different scopes.

**Consequence:** a request issued before the lookup is not automatically a pending obligation in the fresh monitor. It must be recoverable from the chosen subject state, restored in the monitor or replayed according to an explicit contract. This is a source-located interface consequence, not an executed failure of the prototype. The same distinction was derived in [S100](S100-live-model-checking.md); S105 now supplies its primary temporal-witness dependency.

When the subject has no enabled successor, the described product permits a **stuttering subject step while the monitor advances**. This lets normal termination and deadlock participate in the chosen infinite-trace interpretation. Stuttering is a semantic convention, not proof that a real program or device can safely repeat a physical action. The observation adapter, termination policy and intended liveness property must agree. Similarly, a finite safety witness, an accepting liveness cycle, an exhausted finite search and an incomplete search are different outcomes.

The paper permits one breakpoint lookup at a time and has no step-in action. A coarse subject step can therefore hide internal behavior. Multiple monitors may interfere by restricting paths; the discussion does not promise that arbitrary composition preserves every witness. Reductions also require care: merging or pruning states can remove the very history a breakpoint needs. Section 6 explicitly leaves the interaction of temporal breakpoints with scalable user reductions for further investigation. A smaller explored space alone is not completeness evidence.

## Demonstration and transfer boundary

The prototype wraps the AnimUML execution engine, adds step evaluation and implements the finder with a separate Z2MC library. The paper reports that JavaScript's dynamic features eased adapter construction. Its demonstrated language independence is limited to AnimUML and a guard/action language; TLA+ integration is in progress, and Erlang/standard debugger-interface integration is future work. Capturing/comparing configurations and evaluating execution steps are required capabilities, with their implementation cost still to be investigated.

There is **no participant study, controlled defect/time comparison, runtime/memory table or measured net integration budget** in this publication. Figures 5–8 demonstrate architecture and example witnesses. Preserve that positive mechanism evidence without calling absent comparative benefit a measured null. The missing graphical interface, manual LTL conversion, exposed state boundary and unmeasured adapter costs qualify deployment claims. This work does not migrate program state through a code edit or repair an external environment.

## Pinned formalization and prototype

The paper's formalization URL redirects to [teodorov/temporal-multiverse-debugging](https://github.com/teodorov/temporal-multiverse-debugging), pin **`f404bd277f69805fac7865f39d7dca857b60dbef`**, **22 October 2023**. Its complete tree has **21 entries**. The [prototype](https://github.com/MatthiasPasquier97/temporal-breakpoints-for-multiverse-debugging), pin **`3902ec7f092155013a9d66a5d346061040d02a2b`**, **12 May 2023**, has **211 entries**. Both inventories are complete/nontruncated. Neither tree inventory is a whole-repository reading. The prototype predates submission, and the formalization postdates the final PDF's creation; neither is automatically the exact demonstrated execution packet.

All six selected formalization files and eleven selected prototype files below are completely read. The minified bundle is acquired but only selected ranges are read. Each downloaded member's byte size and Git blob identity are verified; SHA-256 identities follow.

| Formalization member | Bytes / SHA-256 |
| --- | --- |
| `README.md` | 2,226 / `28e7f705d1ff937a879d62de0a0cdb274a6cdefb90a4932f307ae0d8bfd9ccdb` |
| `leanpkg.toml` | 261 / `e80fb59804d34ce22d95deb4139c265854a2829d945fc298aea1b5e2d89828f7` |
| `src/sli/sli.lean` | 1,672 / `878b8ded68647ce3ac18ebf15a9ef369e02fc4bfd3de77f9ac20161f404b4152` |
| `src/composition/synchronous.lean` | 3,445 / `7139aae26c83d101ba0bac3cb2551565ed7356fb8aa59c6bc358f01e6e729911` |
| `src/debugging/rmd_step.lean` | 3,637 / `cc8f35c8f3fc61b0df2dfc0817c2fb16acb162bce487668372ec63496fa8c691` |
| `src/debugging/rmd_bridge.lean` | 6,506 / `1a9652b7205ebad0701506f84ba1b15807276da5c777eac89e93b9671ba2132d` |

| Prototype member | Bytes / SHA-256 |
| --- | --- |
| `README.md` | 1,168 / `ff4bfb290a5ed90985baec19720ff851c04679e55524ff8239e000845cffa864` |
| `package.json` | 146 / `f5b30f7e7314357ee96c3822c7b24a1f8394a6403fb647990dc7eef9d3f25612` |
| `finder.js` | 3,373 / `43dff3e4579f48d1a90851a57d732a8bd23be4b464895a9ef06dbcb7d4d05f18` |
| `debugging/rmd_step.js` | 1,045 / `31a9cf66e58d41a1e3aff73c599501ece231062f7911db209d337941453fc3d4` |
| `STR/replaceInitialStr.js` | 1,198 / `670c928c3d5751cae76a6ec53f85ecca87dcd6ba9cead045fb274ddf28ca5c20` |
| `STR/animuml2Str.js` | 3,722 / `ba4f0350912dcd2f40c6b55fe898d7a801227d26e121751976f4e2390b55d227` |
| `breakpointLoader.js` | 2,083 / `3e7c48471965edaa80fe7dfa9e7ab3abe9a43aad0f66415a3ceb422749488996` |
| `samples/breakpoints/AnimUMLLiveness/starvation.js` | 666 / `0aaae60a5cf58828939f15528f1c114e33d1864bc8e708eba7e3a072b70f3b41` |
| `samples/configuration.json` | 2,062 / `94596af4237f2739188f14d4f70ad731a2c0eda916b85d5aa44b941319d57b04` |
| `STR/debugSTR.js` | 7,386 / `452cd6230532b3d312e8f57d036a84d351c6abc646ee2484bc8e8aede7cbd9f1` |
| `main.js` | 5,379 / `db9cc05818d6732afbbbc9546900da938cff6781e4f1d9656d88ea72209cb591` |
| `AnimUMLUtils.min.js` — **partial** | 271,622 / `552539c09ffa51239dfcf8b5ab79fcdbee7d85b8243fb2bb98a8572bc94be9ed` |

Bundle reading covers decoded-character intervals **[63,000,64,000), [75,700,78,200), [268,641,271,567)** and short exact-name navigation contexts. This includes the complete step/state product module and dependent evaluator module, not the complete model checker or AnimUML engine. Interval positions are decoded characters, not UTF-8 byte offsets. The source body is not executed or imported. No dependency installation is performed.

Three observations constrain claims that the publication, formalization and runnable snapshot are interchangeable:

1. **Literal formal definitions differ from the described union/product.** Paper Listing 3 and `synchronous.lean` line 53 use a bounded universal quantifier inside the initial-set predicate. With two distinct subject initial states and one monitor initial state, this requires one pair to equal both different pairs, yielding no initial element rather than the intended Cartesian product. `sli.lean` line 67 similarly quantifies over all enabled actions for successor membership, rather than selecting a successor from any action. This is a direct mathematical reading of the displayed definitions; it is not a Lean compilation or proof rerun. The bundled JavaScript instead uses nested loops to construct initial pairs and enumerates steps. Thus the code-level definitions cannot be treated as an inspected proof that the implementation realizes the intended nondeterministic semantics. The useful product construction remains recognizable.
2. **Actual history/reset and reduction behavior is bounded.** `main.js` creates a fresh breakpoint at each lookup; the finder projects away monitor state. The bundle compares **both** product components and retains the selected target in its step object. `finder.js` 28–30 computes an unused hash remainder but returns the entire configuration as its reduction: the active function is effectively identity, not a demonstrated lossy `%1000` reduction. The formal reduction parameter and the prototype's active route retain different scopes.
3. **Some snapshot interfaces/examples do not match the final exposition.** The bundle's step evaluator substitutes `@...@` expressions on the **source** configuration, fires the action and evaluates the remaining expression afterward; page 134 describes that notation as referring to the target. A symmetric changed-value comparison can work under either convention, but a directional assertion needs the actual convention. Two of ten sample configurations reference absent breakpoint files. The selected `starvation.js` is not the paper's request/response Büchi diagram. The liveness loader also references a different binding from the bundled checker export; without execution or a complete dependency audit, this is a reconstruction gap, not a claimed observed crash. The unexported `debugging/rmd_step.js` draft is not the route imported by `main.js`.

These limitations justify withholding reproduction or machine-checked correctness credit. They do not erase the paper's useful separation of subject and monitor semantics or its reported witnesses. Further source verification would require the exact demonstrated artifact/version and its dependencies; runtime verification remains outside this reading's authority.

## Consequence for Nu and next coverage

For **B03/B04/B07/B08/B12**, the positive mechanism is branch-specific temporal observation composed with an existing semantic engine. The relevant obligations are explicit: which subject state starts the lookup; what history initializes the monitor; what a step exposes; how termination/stuttering works; what acceptance and scheduler assumptions mean; and what the reduction preserves. History retention, witness generation and safe live evolution remain separate capabilities.

For the prospective fixed-F# D1 comparison, this supports keeping trigger coverage and pending obligations separate from compiler diagnostics or finite replay success. It does not require adopting this debugger, establish a benefit from explicit cases, or authorize construction. Nu-specific maintenance benefit remains unmeasured, while the unread verification/monitoring method is an identifiable primary gap.

Next reconstruct acquired **S106, Unified verification and monitoring of executable UML specifications**, to compare the abstract exploration environment with monitored execution and its observation contract. S99/S107 retain distinct live/remote questions; the user-defined-reduction predecessor remains a conditional method if a reduction claim requires it. An unused literature list is not a stopping boundary. All experimental and additional-worker holds remain.
