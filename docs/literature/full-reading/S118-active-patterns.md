# S118 — Active patterns, abstraction and coverage obligations

**Reading completed 2026-10-01 HKT.** Don Syme, Gregory Neverov and James Margetson, *Extensible pattern matching via a lightweight language extension*, ICFP 2007, pp. 29–40, [DOI 10.1145/1291151.1291159](https://doi.org/10.1145/1291151.1291159). This addresses B01/B02/B03/B05: how can clients match abstract data, what does case coverage guarantee, and where does extension work move?

## Acquisition and coverage

Existing Zotero parent `3UEMZCZT` preceded this reading. The [Microsoft author PDF](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/p29-syme.pdf), attachment `HQEGZXTE`, contains twelve pages and 257,201 bytes, SHA-256 `d3a51282a6856c865d4b0d50e622b07dc6c9d9fee54a0b84c7fa2d79d4c0c1dd`. All twelve pages, four figures, Table 1, the related-work comparison, Appendix A and all thirty references were read. Pages 5, 6, 9, 10 and 12 were visually inspected, covering the figures, table, operational rules and appendix code. Native note `LWJF4BXS` stores this reconstruction. No compiler, historical source implementation or author example was executed.

The conference paper is the reading unit. The April MSR report *Combining Total and Ad Hoc Extensible Pattern Matching in a Lightweight Language Extension* and SIGPLAN DOI `10.1145/1291220.1291159` are associated records, not independently read replications. The [Microsoft publication page](https://www.microsoft.com/en-us/research/publication/extensible-pattern-matching-via-a-lightweight-language-extension/) identifies the authors, venue and PDF; it does not locate an exact historical compiler artifact. This reading does not establish current F# implementation behavior.

## Mechanism: a public view over a private representation

Ordinary algebraic constructors make nested decomposition convenient but can expose representation choices. Active patterns supply the destructuring interface through ordinary functions. A structured binding name introduces both the recognizer and its pattern names. Inputs can be abstract types, objects, primitive values or unions; clients can compose the resulting patterns with ordinary matches.

| Form in the 2007 design | Recognition and coverage boundary |
| --- | --- |
| Total, single case | Returns a residual value; the recognizer name is one view of every successfully recognized input. |
| Total, multiple cases | Returns a tagged choice. Declared cases are mutually exclusive for that recognition; a consumer can cover the declared family. |
| Partial, single case | Returns an option. Recognition can fail; separate recognizers can overlap, and ordered rule matching matters. |
| Partial, multiple cases | Table 1 describes an optional tagged choice, but the then-current F# implementation does not support it. It supplies no completeness promise. |

Here “total” classifies the pattern interface. It does not prove that the function terminates, avoids exceptions or computes the intended partition. The paper's own `Type` recognizer contains an explicit exceptional fallback. Coverage of its result cases therefore does not establish all-input safe recognition, let alone correctness after a domain change.

The distinction between partial and total families changes behavior. With separate partial integer and floating recognizers, an input representing one can fail an integer pattern constrained to zero and then match the floating pattern. A combined total family may first classify it as integer; a later floating case of that same family then cannot match. Reorganizing these interfaces needs behavioral equivalence evidence, not merely similar names or exhaustive consumers.

Parameterized recognizers support such queries as a particular XML name, regular expression or bit position. In this design, parameterization loses the common identity used for coverage and redundant-case reasoning: even syntactically identical argument expressions receive fresh identities. They can be reevaluated. Pattern parameters also cannot refer to variables introduced elsewhere in the same pattern, since those bindings extend the environment only after matching succeeds.

Several views can coexist over one representation. A join-list view exposes `Cons`/`Nil` over `Empty`/`Single`/`Join`; XML examples compose element, attribute, numeric and recursive shape recognition; quotations expose an abstract representation of code. These are concrete expressiveness and information-hiding examples. They do not measure time, error rates, maintenance effort or library adoption.

For evolution, three changes must remain separate: adding a concrete representation case, adding a public view case, and changing the mapping from representation to view. A stable view can absorb a representation change locally. It can also conceal a new behavioral obligation if the mapping simply routes it to an old case. Exhaustively consuming the view proves neither that mapping nor each branch's intended behavior. This is directly relevant to D1's independent old/new obligations and to Nu's domain-modeling claims.

## Effects, caching and the compiler described in the paper

Figures 1–3 give an interpreter with explicit environment, state, recognizer application and tag resolution. Conjunction requires both patterns; disjunction tries the left alternative first and constrains bound names/types. Failed ordinary recognition does not provide a general transaction rollback: state and variable bindings have distinct handling. Repeated recognizer calls can therefore matter even if returned pattern values agree.

Section 3.2 sketches Okasaki-style at-most-once recognition for an unparameterized recognizer at the same input path within one rule-set match. Paths distinguish tuple projections, data constructors and active families. This is neither global memoization nor arbitrary pointer equality. Parameterized patterns receive fresh paths.

**Footnote 8, printed p. 34/PDF p. 6, says the F# compiler does not implement that proposed semantics.** It instead assumes effects absent or benign and may reevaluate recognizers. Preserve the semantic proposal, optimization assumptions and actual implementation claim separately. An at-most-once guarantee cannot be attributed to this historical compiler from the article.

The compiler adapts generalized pattern compilation with left-to-right matching, common-pattern prefixes and fresh identities for parameterized queries. It splits a rule list at partial patterns to avoid potentially exponential decision-tree growth. This can repeat recognizer calls across chunks. The paper cites practical motivation but supplies no benchmark corpus, quantitative code-growth comparison or measured tradeoff.

Section 3.3 deliberately omits formal static semantics and does not specify or prove its completeness/redundancy checker. Extending a prior warning-correctness result is a proposed avenue. Neither S113's nor S119's later theorem should be transferred to this implementation without its own correspondence argument.

The described representation can allocate tagged-choice boxes and tuples; option uses null for `None` and a box for `Some`. Value-type optimizations are proposed. Performance is explicitly not the paper's focus. Possible inlining and conversion elimination are implementation opportunities, not a measured general zero-cost claim.

## Examples are demonstrations, not equivalent maintenance comparisons

Appendix A contrasts the pattern interface with direct reflection calls. Its printed baseline has a material behavioral difference. The generic-or-no-element-type branch also admits ordinary nongeneric named types, but unconditionally calls `GetGenericTypeDefinition()`. Section 2.2 itself says that call throws when `IsGenericType` is false. The active-pattern version handles the nongeneric named case separately.

The current [Microsoft API contract](https://learn.microsoft.com/en-us/dotnet/api/system.type.getgenerictypedefinition?view=net-10.0) corroborates that exception condition. This is a bounded API check, not execution of the historical example or evidence that every historical runtime detail is unchanged. The printed alternatives cannot be assumed initially behaviorally equivalent on that class of inputs. Their difference supports a useful error-localization illustration, but cannot estimate a causal maintenance or safety advantage under an equal-behavior comparison.

Other examples are illustrative sketches rather than a certified regression suite. Their readability and modular composition are useful design observations; their presence supplies neither a realistic task distribution nor a net benefit estimate. Recognizers, view contracts, ordering, allocation and client updates all contribute integration obligations.

## Future constructs and consequential follow-up

The paper discusses polymorphic variants, existential/GADT-related patterns and generalized monadic matching as future directions. Figure 4 sketches a partial translation for a chosen `MonadPlus`: list-like combination may accumulate matches, option takes a first success, and STM introduces transactional behavior. These are not established features of ordinary active matching. First-class recognizers can express recursive unfolding, but progress and termination still require conditions on the supplied recognizer.

G15's selected citation contexts expose a consequential follow-up: *Joinads* contrasts its first-success rule with earlier `MonadPlus` proposals, while *Extending monads with pattern matching* revisits backtracking, committing and transactions. *Implementing Joins Using Extensible Pattern Matching* reports a Scala implementation and only an expectation about F# transfer. These remain metadata/citation-context leads for B03 alongside acquired S121/S122; no new coordination method has been fully reconstructed here.

Coverage-preserving abstraction also has follow-ups in *Reconciling exhaustive pattern matching with objects*, extractor typing, pattern synonyms and object-pattern languages. The F# history paper supplies an author adoption claim, not independent prevalence evidence. The bibliography recovers lawful primary routes for Okasaki's *Views for Standard ML* and Scott/Ramsey's compilation report; those bodies were not read. Tullsen's publisher metadata mixes a 1999 copyright/citation year with PADL 2000 and January 2000 publication, so the Scite year difference is preserved rather than “corrected” by guesswork. The [type screen](../nu-background-types-search-2026-09-30.md) and [search ledger](../nu-background-searches-2026-09-30.md) account exact routes, editions and reading states.

## Evidence disposition

**Unique:** unconfirmed for ISE. Abstract pattern views, partial/total recognition and composable destructuring have concrete predecessors; the method itself cites earlier views and pattern abstractions.

**Valuable:** the paper demonstrates useful abstraction, interoperability and composable queries. Representation-independent clients are a concrete mechanism. Runtime, prevalence and human/agent maintenance benefits remain unmeasured here; neither lack of a comparative estimate nor a printed baseline defect establishes no benefit.

**Scientifically valid:** the complete method is reconstructed with explicit proposed-versus-implemented caching, absent checker proof, effect/termination boundaries and example-equivalence limits. Independent intended behavior remains essential. Continue S116's acquired practice study and the wider thematic frontier; retain S140's effect-law dependency without allowing one inaccessible format to block independent work. All experimental holds remain.
