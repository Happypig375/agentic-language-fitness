# S44 - Evolution of Functional UI Paradigms

**Full reading completed 2026-09-29.** Michael Sperber and Markus Schlegel, FUNARCH 2025, pp. 27-38, DOI [10.1145/3759163.3760429](https://doi.org/10.1145/3759163.3760429). Read the [author-hosted proceedings-formatted PDF](https://www.deinprogramm.de/sperber/papers/funarch-ui.pdf), all 12 pages, sections 1-14, code, acknowledgments and 24 references. Figures 1-4 and the unnumbered UI illustrations were inspected in rendered PDF pages 3-5 and 10-11. No tables or experimental results are reported. Reader: the main Codex session, not independent human review.

Zotero parent `N4HWHNFR`, PDF `FPMRHK7Z`; SHA-256 `36e51162c110eeedc3b745cafdbb26be76008c4f6577660296e6e7c2235f7e4b`. The first page identifies the title, authors, DOI and FUNARCH edition. Exact binary equivalence to a separately downloaded ACM file was not checked. The paper was attached before full reading. Text extraction was checked against the rendered figures and UI examples; no extraction gap remains for this paper.

## Question and evidence reconstruction

The paper traces functional UI architectures and develops an illustrative account of Reacl and reacl-c, both associated with the authors. It is an architectural and experience account, **not a controlled maintainability study, systematic review, game-engine benchmark or coding-agent experiment**. There is no participant denominator, randomized intervention, independent task sample, measured comparative effect or cost estimate to transfer to Nu.

Sections 3-4 distinguish initial view construction from later updates, component modularity, cyclic notifications and event-loop control. The MVC examples show how these obligations interact; subscription removal is explicitly omitted. Sections 5-8 trace eXene, Fudgets, Fruit, Haggis, Racket Universe, Elm and React, with different treatment of effects and dynamic views. Their historical and architectural interpretations should not be treated as current API specifications for every version of those systems.

Sections 9-10 make the principal adverse case explicit: a functional update scheme can remove duplicated view-update logic while leaving global state updates, local UI state and message dispatch difficult to modularize. The phonebook example separates editing a draft from committing a value. Reacl uses component messages, reactions, local state and outward-propagating actions; the text discusses Reacl version 2 around 2019.

Sections 11-13 then distinguish domain/view-model obligations that can be specified precisely from context-dependent presentation judgments. The reacl-c example uses component combinators and lenses to connect local state, while a pure `add-new-entry` operation maintains a view-model constraint. The conclusion presents complementary tradeoffs, rather than measured dominance of one paradigm.

## Consequences for Nu and D1

| Live claim | Source location | Limit and resulting control |
| --- | --- | --- |
| Explicit functional state makes coordination simpler | Sections 3, 6-10 | Treat global dispatch, component boundaries and draft-versus-committed state as possible costs as well as benefits. An immutable representation alone does not establish low coordination burden. |
| Pure update/view functions make behavior testable | Sections 11-13 | A testable function is not an independently justified oracle. Separate specified domain/lifecycle behavior from arbitrary reference markup or presentation choices. |
| Nu's MMCC or persistent world is a novel solution to these general problems | Sections 5-13 and references | Functional UI state, effect boundaries and compositional alternatives have substantial predecessors. Nu-specific engineering and measured transfer are separate possible contributions. |
| Exhaustive matches improve later agent changes | Not evaluated | S44 supplies adverse task motivation, not a result for the D1 convention contrast. Keep the common-source/tool and all-obligation endpoint already required by PLAN. |

These are design implications inferred from the architectural account. They do not establish task prevalence, a useful effect size, net benefit or a valid Nu source pair. The paper's strong abstract claims about maintainability are not accompanied by a controlled effect estimate.

## Reconstruction and follow-up limits

No Reacl/reacl-c release was executed or independently reproduced. The illustrative printed code is not a validated reference implementation: for example, Figure 3's Fahrenheit update calls `kToC`, although its constructor uses `kToF`. This bounded transcription observation does not refute the architectural argument and is not a basis for importing the example as an oracle.

The bibliography identifies functional reactive animation, the Racket functional I/O/world design, Parnas's modularization criterion, lenses and FRP refactoring as predecessor paths. Promote the particular primary method if a later Nu claim depends on it; no claim that every cited system was fully read is made. The newly retrieved temporal-testing/replay lineage (S46 and its journal follow-up) is more immediately consequential for Nu's snapshot and temporal-obligation claims than a general survey of every UI toolkit.

**Unique:** general functional state/effect separation is established; the narrowed D1 empirical question remains unconfirmed. **Valuable:** a concrete coordination/testability tradeoff is identified, with no measured Nu benefit. **Scientifically valid:** the paper improves the adverse-case and oracle rationale but does not validate the proposed apparatus. Experimental allocation stays zero.
