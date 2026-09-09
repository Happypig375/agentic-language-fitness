# H1/H2: bounded supplied-source versus file-read pilot proposal

## Status and decision

**Construction adoption (2026-09-09):** following publication at
`8408cd55d0fea183d56c3ecceec022a7d8505c14` and passing exact Linux/Windows CI
`34321797392`, the user said "Continue until before execution, then tell what to
human review before approving execution." This adopts the bounded model-free
workload/controller implementation, including the authored-byte and visible-state
policies below. It does not authorize OAuth staging or any live H request. Finish
implementation and evidence, then present the human-review packet. The original
proposal status below records its pre-adoption boundary; no live ceiling has been
allocated and no historical experiment is changed.

The user replied "continuecontinue" after the H0 completion handoff named bounded
H1/H2 design as the next step. This authorizes this design/preparation packet,
not workload construction, a new native client, OAuth staging or live collection.
**Status: proposal for review and maintainer adoption; zero H dispatches authorized.**
Do not turn the ceilings below into executable permission flags.

**Review disposition:** a separate AI session reviewed the workload, cap rule,
pairing, controller/memory policy, scoring and resource boundaries and reported
no actionable design blockers: approved as a **model-free construction proposal
only**. This is not human language-expert review, maintainer adoption, validation
of the not-yet-built Expanded pair or authorization to run a candidate.

H0 was published at `6e45e90a0cad34d34448b51eb3cba13e609b7337` and passed exact
[CI 34306769616](https://github.com/Happypig375/agentic-language-fitness/actions/runs/34306769616):
Linux 6m5s, Windows 7m49s. Each platform's four envelopes and report matched the
[published H0 files](../reports/workstream-h0-2026-09-09/report.json) byte-for-byte.
The [H0 record](workstream-h0-preparation-2026-09-09.md) retains its definition,
source and implementation hashes, failed engineering checks and limitations.
Neither H0 nor this proposal changes E3a's frozen sources, outcomes or charges.

The decision requested after review is **bounded model-free construction and
implementation of this proposal**. Numerical byte caps, new source/oracle pins,
working H integration and live permission do not exist yet. They must be recorded
before a later live activation, not inferred from the proposal or H0's success.

Documentation validation is retained in `results/h1-h2-design-validation-01/`:
seven changed Markdown files, 86 local file links, no missing links or trailing
whitespace, clean scope/whitespace checks and a matching E3a packet with zero
candidate calls. Product code, tests, frozen protocols, benchmark sources and
reports are unchanged. No unit suite was rerun locally for this documentation-only
change; exact publication CI is the post-push gate, not H1/H2 integration evidence.

## Question and scope

For the same summary-API maintenance task, how do these particular F#/C#
implementations behave under a common authored-input byte budget with either all
source supplied (H1) or selective whole-file reads (H2)? Add one larger, genuinely
functional predecessor to vary eligible-program feature load while keeping the
target summary operation fixed.

This first contrast concerns **functioning off-task feature load**, not an
increase in irreducible task-required memory. H2 can avoid reading unrelated
implementations. Interfaces or compact contracts may suffice; a conservative
reference set is not proof that all its source must be resident simultaneously.
The two access policies also differ in available model turns. Their comparison
is a policy-package comparison, not a causal isolation of retrieval or reasoning.
Primary language comparisons stay within the same size, budget and access policy.

This is one authored family, two dependent feature-load levels and a feasibility
pilot. There is no population-language inference, native-repository claim,
physical-context boundary, scale-slope estimate, crossover fit or H3 memory study.
H0's near-equal token proxies remain a finding; do not replace the family to seek
a favorable F# size advantage.

## One bounded workload extension

The existing [representation generator](../src/alf/representation.py) changes
identifiers/representation, not semantic size. The [successor chain](../benchmarks/successor/manifest.json)
changes tasks at each stage. Neither supplies a valid scale axis for one fixed
maintenance question. Do not call successive gold checkpoints size replications.

| Level | Approved starting point or proposed addition | Role in this pilot |
| --- | --- | --- |
| Core | H0's Task 007 predecessor, descriptive representation, three files per language | Reuse the exact reviewed source; no new summary implementation is present. |
| Expanded | Core plus independently implemented order reconciliation and dependency ordering APIs | Add real tested operations, not padding, cloned modules or historical solutions. |

Both levels receive the unchanged behavioral requirement of [Task 008](../benchmarks/successor/tasks/008-summary-api/task.md):
the five-key status/overdue summary, including nulls, case handling, strict time
comparison, overlapping overdue counts and preservation of earlier behavior and
the extracted engine/I/O boundary. Expanded adds preservation of its two new APIs.
This extra compatibility obligation is explicit, not evidence of a harder summary
algorithm. Do not supply future summary gold or final scoring cases as context.

The two additions are selected now, before their F#/C# size measurements:

- **Order reconciliation:** combine two order collections by ordinal ID, choose
  the higher-priority record for an overlapping ID, then the later creation
  instant, then the right-hand record on a tie; return ordered winning IDs and
  their left/right origins. Include Int32 extremes, time-zone-equivalent instants,
  case-distinct IDs, null/empty inputs and duplicate-ID handling in the neutral
  contract. This is not an implementation of status counting or overdue summary.
- **Dependency ordering:** return a deterministic topological order of supplied
  IDs and precedence edges, choosing the ordinal-smallest ready ID each time.
  Specify duplicate IDs/edges, unknown endpoints, null/empty inputs, self-edges,
  cycles and deterministic errors. This supplies a real graph operation rather
  than a copied summary helper or an unused code island.

Before either language implementation, write the complete common input/output
contract, error precedence and expected examples for these operations. That
model-free contract finalization is part of the proposed construction scope;
it is not permission to replace the chosen operations or add further features.
Use ordinary maintainable styles in each language; do not force equal lines,
file counts or internal graphs. Keep the same standard-library-only .NET ecology,
at most eight eligible source/project files and 65,536 source/workspace bytes per
language/level. If meaningful implementations cannot fit these bounds, stop for
a construction-scope decision rather than silently simplify or expand them.

Two explicit source checkpoints suffice; **no scalable generator is required**.
Record derivation from Core, authored modules, reused code and duplication. They
are not independent repositories. Freeze both source bundles and their common
contracts/oracles only after model-free validation and separate paired review.
Core and Task 008 are public historical material and may be familiar to models;
newly authoring Expanded or renaming identifiers would not prove decontamination.
Record the information cutoff and authoring/review provenance. No third-party
code import, native-project sampling or change to repository licensing is proposed.

Required workload evidence at both levels:

- baseline and every preserved operation pass the common oracle in both languages;
- the new summary target passes independently specified cases, including boundary
  and metamorphic/differential checks with independent expected behavior;
- semantic faults are caught: unchanged predecessor, missing/extra summary key,
  case-sensitive status counting, inclusive overdue boundary, subtracting overdue
  from status totals, and broken preservation of each added operation;
- the expanded operations are reachable and tested; removing or breaking one
  fails preservation checks, while no added helper supplies the summary solution;
- a source-bound engine/I/O and live-summary rubric is retained; name differences
  alone do not fail it, and missing review is unknown rather than completion;
- reviewed relevance maps permit alternative valid implementations; evaluator
  maps, gold and final-case identities never appear in candidate maps or source.

## Authored-byte budgets, not physical token limits

Retain the requested `gpt-5.6-luna` / `high` setting, pinned native no-tools,
single-response client and canonical local-OAuth/foreground-SSH route. Do not
upgrade the model/client or introduce an API key, native tools or a new relay.
Actual model identity and account availability require fresh evidence when live
integration is later authorized; an alias is not a guaranteed immutable backend.

The proposed hard cap is the UTF-8 length of the **complete caller-authored replay
submitted to the native client**, including instructions, public contracts, map,
resident source, retained read actions/results and controller framing. It is an
input-only software intervention. Native-added/provider-hidden material and the
physical input/output context ceiling are not verified by this measurement.
Do not describe this as an exact full-provider-request token budget.

H0's joint/input-only byte fixtures do not themselves adopt this H policy. This
explicit authored-input interpretation and its overshoot limitations need
maintainer adoption. There is no output-reserve subtraction from an input-only
authored-byte cap. The output bound is separate; a tokenizer proxy is descriptive.

Derive exactly two common caps after construction, before any H model outcome:

1. For each level, language and declared file order, serialize the complete H1
   request and every request of one fixed H2 read-all reference trajectory. That
   reference requests the first four mapped files, then all remaining files when
   needed, then submits; no more than two read actions. Skip an empty second read.
2. Let `A_core` be the largest of those Core authored requests, and `A_all` the
   largest across both levels and languages. Set `C_low = ceil((A_core + 1024) /
   1024) * 1024` and `C_high = ceil((A_all + 1024) / 1024) * 1024` bytes.
3. The 1,024 bytes are a once-only construction headroom allowance, not a proven
   tokenizer error bound or an additional runtime deduction. Admission compares
   actual complete authored bytes directly with the selected cap.
4. Freeze the resulting integers and every measured reference envelope. Require
   distinct caps, both no greater than 131,072 bytes; Core overlap at the low cap;
   all reference trajectories fitting the high cap; and at least one Expanded H1
   full envelope exceeding the low cap. If this fails, report that the planned
   pressure contrast is absent. Do not pad, choose a language-favoring cutoff,
   add features or launch a reduced/different design automatically.

The reference is a model-free feasibility witness, not a candidate policy or a
guarantee that every H2 action sequence fits. Real read decisions, whitespace and
history consume their actual bytes. Source allowance is the remaining serialized
capacity after non-source material, not raw file bytes alone. Report exact bytes,
the pinned `tiktoken==0.14.0` / `o200k_base` proxy and provider-reported usage
separately. Unknown physical fit, proxy error and subscription USD remain null.

The [official configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)
documents the context-window setting separately from the auto-compaction trigger;
these settings do not establish this pinned client's measured request accounting.
The [official input-count API](https://developers.openai.com/api/reference/typescript/resources/responses/subresources/input_tokens)
documents an API endpoint, not its availability for this OAuth route. The OpenAI
Docs check preserves those distinctions; this proposal makes no count call or
new claim of OAuth access to that endpoint.

## Access and memory policy

Both arms receive identical task/contracts, a counted filename/byte-size/content-
identity map, the same edit authority and final JSON full-file-replacement format.
The map contains only eligible files, no evaluator roles or relevance scores.
Use two opposite semantic-role file orders for each level, the same per language
pair; preserve actual F# compilation metadata. Record token-proxy positions, not
artificially padded equal byte offsets.

**H1:** supply all eligible source in one authored request and allow one final
submission. If that request exceeds its cap, record the planned cell as
`infeasible-authored-budget`, with zero dispatches, not an executed model failure.
Resolve the feasibility mask before the first live candidate request.

**H2:** initially supply the counted map and no source. Permit at most two
controller-side read actions followed by one final submission, or an earlier
final submission. The native client remains tool-free. The entire assistant
message must parse as exactly one of these JSON envelopes, with no extra keys:

```json
{"action":"read","paths":["OrderFlowEngine.cs"]}
{"action":"submit","files":{"OrderFlowEngine.cs":"full replacement text"}}
```

Use one to eight distinct, exact eligible root filenames per read. No globbing,
search index, host path resolution, URLs, arbitrary commands or candidate-visible
evaluator map. Reads select immutable pinned text from the controller's source
map. The final phase accepts only `submit`; a third read is a retained protocol
failure, not a request for more quota. H1 uses the same `submit` envelope.

Render selected source in its assigned file order, not requester path order.
Keep all successfully read source resident until the trajectory ends. Repeated
unchanged reads return identity-only references only while actual text remains
in the request. Retain the raw accepted read-action text and counted result
metadata; place returned full source once in the resident bundle. This is an
explicit visible-state reconstruction policy, not E3a's repair transcript.
There is no eviction, summarizer, arbitrary note field, hidden-state continuation
or resume session in this first H2 condition. H3 remains separate.

Batch-read admission is atomic: assemble all prospective source and framing
before returning or charging any new source. An overflowing valid read ends the
trajectory as authored-budget exhaustion; it does not evict/truncate, raise the
cap or dispatch again. Invalid JSON/path/action is a terminal format/authority
outcome. Preserve the raw reply, requested paths, refusals, cumulative and unique
exposure, resident contents and every assembled request/hash. Cached provider
input remains occupancy; never add cache/reasoning subsets twice.

Neither arm receives compiler/test feedback or patch repairs. A submitted source
is applied once and evaluated externally in the existing isolated sandbox.
Safe but wrong F# Compile entries remain project/build failures, not security
violations; the zero-repair policy supplies no additional attempt. Forbidden
project/dependency/path changes remain terminal authority violations.

## Bounded schedule and proposed resources

The proposed fixed grid is `2 levels x 2 caps x 2 access policies x 2 languages x
2 file orders = 32 planned trajectories`, or 16 language pairs. Each pair shares
level, cap, access and file order. Generate and retain a schedule with seed
`20260909`, adjacent language pairs, and complementary language-first order across
the two file orders in each level/cap/access cell. Permute pair blocks before
collection. File orders are controlled positions, not independent workload
replications or a reproducible provider RNG seed.

| Phase | Proposed ceiling | Currently authorized |
| --- | ---: | ---: |
| Unrelated H integration | 5 native dispatches; three planned for H1 and a read-then-submit H2 check | 0 |
| Fixed H pilot | 64 native dispatches: at most 16 H1 + 16 x 3 H2 | 0 |

No quota is borrowed from E3a's unused balances. These are maxima, not targets;
infeasible H1 slots, early final answers and failures reduce actual use. Unused
allowance never adds slots, retries or replacements. The integration's two spare
dispatches do not authorize automatic reissues. Retain ambiguous debits and stop.
These ceilings concern integration/candidates, not total research model usage.
Authoring and up to 32 distinct final-source reviews are recorded separately;
no automated reviewer backend is proposed or authorized by these ceilings.

Reuse the existing 120-second per-dispatch and 600-second trajectory deadlines,
49,152-byte complete assistant reply, 65,536-byte workspace and 1,048,576-byte
capture limits. Retain post-turn alarms at 32,768 input and 8,192 output tokens
including reasoning; they are not hard provider caps. Subscription USD and any
quota conversion remain unknown. The same native/image/environment identities,
isolated evaluator limits and cleanup checks must be pinned at activation.
If these limits cannot deliver every intended gold submission or the reference
requests, stop for a documented decision; do not silently relax them.

Pre-candidate setup failures are retained apparatus attempts. Invalid/absent usage,
ambiguous dispatch, unexpected native tool/compaction behavior, context rejection,
security failure or unconfirmed cleanup stops the live batch immediately.
Otherwise retain valid task failures and continue only the frozen schedule.
The five-failure apparatus rule does not override those immediate stops, refund
debits or permit outcome-driven sample extensions. No candidate code runs on the
host or has access to model credentials, scoring machinery or successor gold.

## Evaluation, reporting and minimum implementation

Retain all 32 planned slots and distinguish preflight infeasibility, started
trajectories, known submission/task failures and unscored/unknown outcomes.
Report model correctness over eligible started observations separately from
software-budget feasibility; do not count unexecuted H1 cells as model errors.
Paired correctness contrasts require jointly feasible cells, with their selection
mask and coverage reported. H2 budget exhaustion after a valid start is an access-
policy failure, not an excluded apparatus observation.

Task completion requires format, safe application, build, sealed behavioral
correctness and the declared source-bound architecture obligations. Report all
components; unknown required review stays unknown, and a known failure dominates
missingness. A final-source reviewer must not see per-slot resource/behavior
outcomes. Reuse identical source-hash judgments rather than fabricate independent
reviews. Identify human versus AI review honestly. Scoring follows interaction;
no hidden score decides another request, repair or replacement.

Report absolute paired outcomes and source/input/output/latency distributions,
including all valid failures and H2 inspection turns. Source exposure, residence,
authored bytes and cumulative provider input are separate populations/quantities.
Do not fit a scale slope or large factorial model to two correlated sizes. H1/H2
differences include extra deliberation and dispatch opportunities. This pilot
can establish feasibility and diagnose failure modes, not prove general context
capacity or superior language understanding.

After adoption, implement only the two source checkpoints/contracts/oracles and
one finite H controller/check command. Reuse H0 serialization/accounting primitives,
the strict native-response parser and dispatch guard, the existing transport and
isolated evaluator. `CodexOAuthAdapter.generate` assumes E3a repair-history replay;
do not directly reuse that memory policy for H2 or change E3a's frozen code to fit
H. No native tool schema, daemon, compatibility ladder or general agent framework
is needed. All H execution flags stay disabled during model-free implementation.

Model-free acceptance must cover workload/fault/architecture checks, exact byte-
cap and output deliverability, both language orders, empty/map-only requests,
atomic multi-read refusal, retained-text references, malformed output, the two-
read/final-only boundary, zero feedback/repairs, isolated fresh-source evaluation,
dispatch/usage/ambiguity controls and preservation of every planned slot. Test
the exact native request composition through the existing model-free probe where
available; do not infer provider behavior from mocks or invent an interception
service. Validate on exact implementing CI and review the paired artifacts.

Only then present the fixed numerical caps, source/spec/runner/image identities,
feasibility mask, schedule, source-review arrangements and separate live-request
proposal. The current decision is whether to adopt this bounded model-free build;
neither adoption nor a passing fixture would automatically authorize live H.
