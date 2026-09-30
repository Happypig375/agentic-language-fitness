# S122 — Join-token demonstrations and the Ruby comparison

**Reading completed 2026-10-01 HKT.** Taketoshi Nishimori and Yasushi Kuno, *Join Token-Based Event Handling: A Comprehensive Framework for Game Programming*, SLE 2011 revised selected papers, LNCS 6940, 119–138 (2012), [DOI 10.1007/978-3-642-28830-2_7](https://doi.org/10.1007/978-3-642-28830-2_7). This addresses B03/B05/B06/B10/B12: what join tokens demonstrably simplify, what their comparison holds constant, and which scheduling/lifecycle costs remain.

## Acquisition, lineage and coverage

Native Zotero `VPHW6NDA`, attachment `XF5PMYFW` and note `UE8YHYX8` preceded reading. The PDF is the complete 398-page proceedings: 9,161,975 bytes, SHA-256 `046715329855c46bbe0d9b9a6ce8082044503d44852be27324e23ac2c5f8317a`. Only this chapter is a full reading: **physical PDF pages 129–148, printed 119–138**, twenty pages. All sections, three figures, code examples and sixteen references were read; physical pages 131/136/138/143 were visually inspected for figures, preservation marks and the comparison listing. No numbered tables or appendix. The rest of the proceedings is not credited. An institutional accepted-manuscript route was located during follow-up, but was not substituted or compared.

The paper calls its evaluation interim and identifies [S121](S121-join-token-mechanism.md) as the prior mechanism account. Same authors, language and implementation lineage; the two publications are not independent replications. S121's shooting game differs from the Balloon and Descender demonstrations here.

The [author sample page](https://www.nisnis.jp/mogemoge/sample_games.html) supplies both languages' Balloon files. All 357 physical lines of [Balloon in Mogemoge](https://www.nisnis.jp/mogemoge/balloon.moge) and all 436 of [Balloon in Ruby](https://www.nisnis.jp/mogemoge/balloon.rb) were passively read. The former matches the file inside S121's source archive. The Ruby file is native attachment `UX4XBVGV`, 9,333 bytes, SHA-256 `7fa3d5049d148b817e2fe9d35f81844e80d4ca02e63bee4b81b09258511dee57`; the Mogemoge file is 7,830 bytes, SHA-256 `c26da3972baddecab8c5cda09358ffa2b0a2ad357cd8705ce6afa481ff95e3bb`. Native uploads were hash-verified. Descender's 847-line file was inspected selectively for handlers, ordering and cleanup, not fully read; 19,119 bytes, SHA-256 `a0b9899c324447509e50267676688752c1401622fac2060133e67ea0d27f8da4`. HTTP dates place these game files on 15 April 2011. No author code or game was executed; exact correspondence to the measured publication revision is not proved by timestamps and line counts.

## What the demonstrations establish

Join tokens combine named participation/state, object identities, arguments, guards and ordered handlers. They support interactions independently of the class that would otherwise own a method. Mogemoge retains ordinary methods, mutable object fields and a Java graphics interface. The work is an alternative to conventional object interaction code, not a pure-state implementation or an effect-isolation theorem.

Balloon has nine stated rules. Missiles and explosions affect balloons, bombs and buildings; a balloon also keeps its associated bomb at the end of a string. Retained tokens allow repeated participation or many partners; consumption limits one-shot participation. The one-explosion/one-building rule consumes the explosion token, while other explosion rules preserve it. The relationship handler matches a balloon token's bomb argument to a bomb object's token, so it avoids the particular two-way reference bookkeeping of the Ruby version. It still stores an object reference in the token; the method does not eliminate references or lifetime obligations generally.

Descender has more coordination structure: player movement modes, horizontal/vertical ropes, scrolling, obstacles and rope cutting. Command tokens are matched against available geometry/state. Several concrete obligations remain visible:

- Handlers emitting a scroll token must precede its consumers. Preserved scroll tokens broadcast to relevant object kinds; a final empty handler consumes the token.
- Empty fallback handlers discard commands that no earlier rule handled. Otherwise a command can remain available on a later frame.
- Absence of a nearby conflicting rope is implemented by earlier consuming blocker handlers followed by a construction handler. The language is not computing unrestricted negative conditions automatically.
- Rope cuts and collisions explicitly change the player's update method/mode. Objects explicitly withdraw relevant tokens during destruction. Naming conventions, rather than an enforced module/ownership boundary, are proposed to prevent large-program interference.

These examples substantiate a useful representation of the rules. They also show that program order and cleanup code remain part of behavior; concise handlers do not establish complete lifecycle safety.

## Reconstructing the comparison

The authors implement Balloon in Mogemoge and Ruby/Tk, describing their behavior as mostly alike apart from speed and graphics-dependent appearance. They report 357 versus 436 lines: 79 fewer, about 18.1% of the Ruby count. The public files have exactly these physical line counts, including comments and blank lines. That correspondence supports the reported size observation; it does not identify a common semantic or effort denominator.

The Ruby collision helper selects objects by class from a global list and iterates candidate pairs, calling a supplied block when a collision test succeeds. Mogemoge selects token roles and places the guard in each handler. The Ruby program adds an active flag for the one-building explosion rule and explicit parent/bomb reference maintenance. Those are concrete differences in these implementations, not proof that a Ruby library or another ordinary design cannot provide role-based selection and lifecycle helpers.

The acquired files expose further comparator boundaries:

- Ruby includes Tk setup, key-state bookkeeping and widget creation/update code. Mogemoge calls host graphics, object-list and game-loop helpers. Counting only the two game files does not charge the same amount of support infrastructure to both sides.
- The Mogemoge setup creates six buildings; Ruby's inclusive range creates seven. Explosion/bomb and explosion/balloon handler order also differs. Mogemoge's balloon/bomb position adjustment occurs in a join handler, whereas Ruby performs it during the balloon update. These source differences require an independent obligation/equivalence account before treating maintenance outcomes as a language effect.
- The Ruby helper snapshots the selected lists before iterating; removing an object from the global list inside a block does not itself remove it from those already selected arrays. The join runtime has its own snapshot/consumption boundaries reconstructed in S121. Neither listing is a behavioral oracle for the other.

No controlled participant assignment, modification task, correctness oracle, error denominator, development-time comparison or independent replication is reported. Descender is 847 lines in Mogemoge, but there is no corresponding Ruby implementation comparison. Anticipated readability gains for more complex games are projections. The examples' positive expressiveness result should be preserved without converting it into measured maintenance productivity.

## Runtime, effects and transfer

The paper deliberately excludes true parallel execution to retain controllable ordering. Its favorable debugging experience is an author report, not a measured error reduction. New tokens can affect later handlers in the same ignition; earlier handlers are not automatically rerun. S121's dated source inspection further distinguishes intended consumption/regeneration from actual cleanup order and per-handler snapshots.

Section 6 gives `O(MN)` for `M` handlers and `N` tokens of a particular name. It does not account for general multi-pattern candidate products. The released nested-loop code can inspect every pair for two retained token populations. No runtime benchmark in this paper measures that growth, the cost of guard calls or garbage collection. Statements about graphics dominating logic and no problems in small examples do not establish a transferable real-time bound.

Rete is proposed as a future optimization, with acknowledged need to notice when guard values change. Restricting guards to participating objects' fields is a proposal, not a demonstrated dependency-invalidation mechanism for mutable fields and called methods. The Rete primary paper has been metadata-identified, not body-read or credited with a measured Mogemoge improvement.

For the Nu background, the useful distinction is between declaring an interaction and correctly implementing its lifecycle, timing and host integration. The mechanism relocates enumeration and participation handling while preserving obligations that need explicit testing. The results neither isolate immutability nor demonstrate migration, undo, deterministic replay, exhaustive static coverage or a coding-agent effect.

**Unique:** declarative object coordination and game-rule-oriented code have established predecessors; Nu/D1 priority remains unresolved. **Valuable:** working examples and the stated file-size difference are positive, scoped observations; net maintenance and general runtime benefits remain empirical questions. **Scientifically valid:** full chapter and bounded artifact reconstruction clarify the comparison, but do not establish behavioral equivalence, execution results or scientific acceptance of ISE. All experimental holds remain.

G17/SC75–76 and W139–143 account for this segment's identity and follow-up routes in the [background ledger](../nu-background-searches-2026-09-30.md). JEScala (S142) now has a deduplicated native record and an unread author PDF for its object/event coordination and performance comparison. The next broader balancing step is the recorded functional-persistence/runtime frontier; neither this pair nor a low-coverage citation graph completes a background theme.
