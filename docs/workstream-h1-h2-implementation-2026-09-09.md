# H1/H2 model-free construction and pre-execution review

## Authority and provenance

The user approved construction with: "Continue until before execution, then tell
what to human review before approving execution." The adopted scope is the
[bounded H1/H2 proposal](workstream-h1-h2-overlap-design-2026-09-09.md), published
at `8408cd55d0fea183d56c3ecceec022a7d8505c14` with successful exact Linux/Windows
CI `34321797392`. Upstream was unchanged when construction began.

This record concerns model-free authoring and tests, not candidate observations.
No live H request, OAuth staging, new model/client, relay or experimental candidate
execution is authorized. The proposed five integration and 64 pilot dispatches
are unallocated. E3a balances and frozen evidence remain unchanged.

Before either language implementation, another AI session authored the common
[operation contract](../benchmarks/workstream-h/contract.md) and
[public examples](../benchmarks/workstream-h/public-examples.json). Parent review
corrected an accidental change to legacy dispatch/errors and specified exact
new-operation validation precedence, Unicode ordering, integer/date domain and
null behavior. These are finalizations of the adopted two operations, not new
features or size tuning. Accepted UTF-8 file hashes before implementation:

- Contract: `da32ed556af71b49129a929e8b71a725dae3ad3f18343fbabde18a934cf0cc8b`.
- Public examples: `6eef969deb83fd032af5deecef6292ba20e22c6695f212a591ecbcb79c64dc70`.

Separate AI authoring sessions began each language from that common contract
and the exact H0 predecessor, without instructions to imitate the other new
implementation. Subsequent repairs to both languages were made by the same
AI session; their final authorship is therefore not independent. Core/public
Task 008 are historical material; neither separate initial authoring nor new
source establishes independence from model training or decontamination.
No language-size measurements selected or changed the two new operations.

The [official non-interactive client documentation](https://learn.chatgpt.com/docs/non-interactive-mode)
describes JSONL as an event stream, which may include tool events. The OpenAI Docs
check therefore supports reusing the exact native event parser and explicit
no-tools boundary, not treating JSON output alone as enforcement. The pinned
client and local-OAuth transport are unchanged; current docs do not prove their
live behavior or grant execution permission.

## Retained engineering checks

Initial controller validation is retained in
`results/h1-h2-implementation-validation-01/controller/`: eight unit tests and
the targeted whitespace check passed. Parent architecture inspection nevertheless
found an H2 read exposing all source, missing retained action/result history and
incomplete dispatch/accounting and submission authority checks. This shallow
test result is **not acceptance evidence**. The initial implementation needs
repair and a complete affected test manifest before independent revalidation.

The first C# construction draft also failed source inspection: it included the
summary target in the Expanded predecessor, rewrote legacy source unnecessarily,
and did not preserve the new operations in the separate trusted gold bundle.
That draft is not eligible workload material. Repair must start from the exact
H0 predecessor and leave summary absent there; only the evaluator-only target
may contain its implementation. No candidate saw this draft and no live result
was collected from it.

Further rejected engineering checks and corrections are retained rather than
counted as experimental observations:

- Early F# drafts omitted required validation and preservation; subsequent
  repairs restored the common contract and the existing engine/I/O split.
- A duplicate-method error prevented a C# gold build. A separate first Windows
  comparison script mishandled Unicode transport and compared serialized JSON
  rather than semantic values. The compile error was real; the comparison
  failures were not valid behavioral evidence. The replacement source-bound
  harness uses UTF-8 bytes and semantic JSON comparison.
- Source loading initially mishandled manifest roots, generated build folders,
  and CRLF normalization. An overbroad check also rejected the legitimate VIP
  tier string `gold`. None of these is a candidate failure or a scientific
  protocol change.
- Controller repairs retain full resident source in every subsequent authored
  request, count exact accepted read actions, reject an over-budget multi-file
  read atomically, and enforce eight total files after merging a submission.
- The neutral reconciliation oracle initially checked left duplicates before
  validating right records. The contract requires all left records, all right
  records, then left/right duplicate checks. Regression cases now cover that
  precedence and compare the literal addition corpus with the neutral oracle.
- The first audit used duplicate slot IDs and excluded H2 cells using the
  read-all reference maximum. H2 feasibility is instead its initial map-only
  request; a later read overflow is a retained policy outcome. The rejected
  24-feasible-slot artifact remains in
  `results/h1-h2-implementation-validation-04/audit-run-01/`; it must not be
  promoted into the final schedule or interpreted as an observed model outcome.
- Initial entry-point tests covered refusal and limits but not the composed
  journal/runner. Review found raw bytes in a JSON event, an activation/audit
  conflict, and an integration path that did not require its behavioral result.
  These require composed regression tests, not another protocol version.

The first complete trusted workload check is retained at
`results/h1-h2-implementation-validation-02/workloads-full/`, with its source-bound
harness at `results/h1-h2-implementation-validation-02_runner.py`. All eight
fresh builds passed: Core predecessor/gold have 79/90 cases per language and
Expanded predecessor/gold have 122/137, totaling 856 JSON responses. This is
trusted fixture evidence, not arbitrary-candidate sandbox or model evidence.
Generated `results/` paths are local engineering evidence; the final public
packet must contain its own reproducible summaries and accepted artifacts.

The complete fixture wrapper initially encountered a Windows temporary-directory
cleanup error from a background .NET workload-advertising log. Trusted fixture
commands now set `DOTNET_CLI_WORKLOAD_UPDATE_NOTIFY_DISABLE=true`, as documented
by [Microsoft](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-environment-variables#dotnet_cli_workload_update_notify_disable).
This is a fixture-only environment correction, not a change to frozen E3a or the
production evaluator. A later validation wrapper prematurely described a normal
running-process tool yield as a hang and used a pre-existing output directory;
its final `FileExistsError` is retained, not evidence of a semantic fault. Fresh
acceptance must use a never-created output directory and wait for the real exit.

Remote native checks also exposed probe-only assumptions. The exact image lacks
the offline tokenizer package, so the native composition path now skips optional
proxy counting while preserving byte-identical canonical replay; the ordinary
construction audit still requires the pinned tokenizer. A retained exit-137
attempt produced no report and remains unscored; its container was subsequently
confirmed absent. A one-request diagnostic then passed the unchanged native
probe but rejected the new witness because Codex adds a native environment user
message before the authored request. The witness now checks the exact authored
bytes as the final, unique matching user entry and retains the native-added
prefix identities separately. It removes the helper's extra newline, not any
candidate content. Native-added/provider-hidden bytes remain outside the adopted
authored-byte cap; none of this proves physical provider fit or OAuth behavior.

## Fixed construction choices

With the complete counted protocol instructions, the prescribed formula gives
**18,432 bytes (low)** and **35,840 bytes (high)**. The earlier 17,408/34,816 draft
omitted those instructions and is not the accepted cap measurement. This is the
same max-plus-1,024/round-up-to-1,024 rule, not outcome-driven cap selection.

There are 26 model-free reference requests in 16 envelope records, 32 planned
slots and 16 adjacent language pairs. **28 slots are initially feasible.** The
only four preflight exclusions are Expanded/H1/low (both languages and orders).
Expanded/H2's map-only request can start at the low cap; its later read decisions
can exhaust the cap and must remain policy outcomes. With this fixed mask, even
maximal allowed trajectories use at most 60 pilot dispatches; the proposed 64
ceiling grants no extra slot, retry or replacement.

The [specification](../protocols/workstream-h1-h2/specification.json) records
source, sealed-case, public-prompt and schedule/mask pins. Same-byte-length task
wording changes are rejected by the public-payload identity check. The policy
hash excludes explicitly identified approval/integration-evidence bookkeeping,
not scientific settings. CI's read-only activation option and private disabled
SDK-fixture copy avoid making future activation incompatible with model-free
CI; they never enable the live runner or grant a new allowance.

The [source-bound paired AI review](../reports/workstream-h1-h2-preexecution-2026-09-09/source-review.md)
records all eight bundle hashes and the evaluator-only architecture/relevance
map. Separate AI reviews checked the other session's implementation changes;
earlier controller participation is disclosed. They are not human approval.

## Accepted model-free evidence and remaining gate

The implementation is ready for human review, subject to exact implementing
publication CI. The [retained evidence index](../reports/workstream-h1-h2-preexecution-2026-09-09/evidence/index.json)
links raw fixture/native evidence, original identities and reproduction commands.
The [construction audit](../reports/workstream-h1-h2-preexecution-2026-09-09/construction/report.json)
contains source, public-prompt, case and code identities, all reference envelopes,
cap derivation, schedule and feasibility mask. It is not a live freeze.

Review identities (source-code file hashes are in the construction report):

- Canonical specification: `2c2dde84e6261b2578bf21944a3a0ad932403c89ec0bd4490713f367dbd1a07e`.
- Scientific policy: `ec2638862df05cda74bf415d86a9e1b8dbeb24f9f504ccd00767253daa38d7d9`.
- Construction report bytes: `eea708fb2e79eba1e96aaf2e25593dfd769d08fb52b6fc11b575509bffd549da`.

Final separate AI review closed the activation-reporting issue: the audit reports
actual zero model-free activity separately from specification authorization, and
the pre-execution status refuses any enabled approval/verification flag or nonzero
allocation even when read-only activated-spec auditing is permitted.

- The complete affected test manifest has **66 tests**: a separate validator
  passed 60, followed by the 11-test fixture file and 21-test checker/runner
  scope covering binding/bookkeeping regressions, then the final independently
  validated 29-test controller/fixture scope. These targeted rechecks cover the
  changed entries; no global local suite substituted for the affected manifest.
- Both host and exact-image full fixture attempts passed all eight positive
  predecessor/gold targets and caught 27/28 semantic faults. The sole initial
  failure was a malformed Core F# mutation, correctly rejected as a compile
  failure rather than credited as a semantic test. Those aggregates remain
  failed in the raw records.
- The repaired mutation helper changed two F# variant byte identities (including
  equivalent Expanded conditional spelling). An independent comparison retained
  the 26 unchanged variants; both changed variants were then freshly rebuilt and
  semantically caught in the exact sandbox. This is **26 unchanged plus two
  verified replays**, not a rewritten 28/28 original attempt. Publication CI
  rebuilds the entire current matrix on Windows/Linux, with Linux CI's explicitly
  non-experimental SDK-fixture sandbox reported separately from the remote image.
- The pinned native binary passed **52/52** baseline/hostile loopback checks over
  the 26 reference requests. Each used one fixture POST; external provider calls
  and OAuth staging were zero. The unchanged probe's global `no_tools_verified`
  field remains false: these are bounded hostile-fixture checks, not a universal
  unsupported-tool guarantee.
- The E3a packet still matches and frozen H0/E3a source, specifications and
  reports are unchanged. Seven changed Markdown entry points passed a local
  link scan; final publication CI remains an exact-revision gate.

Remote tests used image
`sha256:5d3e97d195dbbe7e47e47055e46f8c6f15fb9553be0c7ef19ed0060756fc7116`
and native binary
`72cf14453c1879996b970accc7de9aa114bf570e586230799a429d0741bb1959`.
Owned evaluator/native container absence was checked. No model OAuth cache was
staged or read; the original local login was untouched. Source-only evidence
roots remain retained, not secret authentication homes. No new proxy, listener,
image or provider/backend was introduced.

Passing these checks cannot substitute for human scientific review or a real,
separately approved route/model shakedown. All H execution/user/human approvals
remain false and both H allocations remain zero.

### First publication and ordinary CI/parser corrections

Initial implementing commit `6d2696857b38d00513404f2059ac095a871a53ea` is retained.
[CI 34334525905](https://github.com/Happypig375/agentic-language-fitness/actions/runs/34334525905)
passed unit tests and the pure construction audit, then both platforms failed
the trusted-fixture SDK check: temporary directories outside the checkout lost
the repository's `global.json` selection policy. The
[failed-step log](../reports/workstream-h1-h2-preexecution-2026-09-09/evidence/ci-attempt1-failure.log)
is preserved. Fresh trusted fixture directories now receive that same exact SDK
pin, disabled roll-forward and no prerelease selection before any `dotnet` call.
This neither changes the image nor relaxes the strict SDK identity check.

A final parser check also found that non-string action values, deeply nested
JSON and oversized integer literals could raise Python exceptions and be
misclassified as batch-stopping apparatus faults. They now remain retained,
charged, per-trajectory format failures. Memory/system exceptions are not hidden.
Another AI session reviewed both corrections; all 29 affected controller/fixture
tests passed. These are ordinary pre-execution code fixes, not scientific revisions.

The refreshed construction report changes only code-identity bookkeeping; all
other 18 artifact files, including every reference envelope, cap and schedule,
remain byte-identical to the first publication. The original construction report
SHA was `c4d518f27b6ac9a37209a28bcd20050f5c8680073aafbacb7cd87a0319a0fc06`
and remains available in that commit. Scientific specification/policy hashes and
all false/zero execution gates are unchanged. Approval requires the corrective
publication's exact CI, not the failed earlier run.

## What to human-review before approving execution

Human review should address these substantive questions, not just green tests:

1. **Matched workload:** are both implementations ordinary, maintainable examples
   of their language, and do the two added operations have equivalent observable
   behavior? Confirm that neither predecessor contains the summary solution and
   that preservation tests genuinely exercise the added functionality.
2. **Scientific interpretation:** accept two dependent levels of one authored
   family, functioning off-task feature load, and the extra H2 reasoning/dispatch
   opportunities. These do not isolate retrieval, estimate a scaling slope or
   establish a general language advantage.
3. **Budget and selection:** inspect every reference request, the symmetric cap
   formula, numerical caps and precomputed infeasible-slot mask. A controller byte
   limit is not a verified provider context limit; no padding or outcome-driven
   cap selection is allowed.
4. **Interaction and scoring:** inspect actual H1/H2 request examples, counted
   read history, two-read/final-only behavior and atomic refusal. Confirm the
   single-submission/no-feedback policy, sealed behavioral cases and source-bound
   architecture rubric. Arrange reviewers who do not see per-slot outcomes/costs;
   unknown required judgement must remain unknown.
5. **Security and reproducibility:** review source/spec/schedule/runtime hashes,
   native no-tools evidence, isolated evaluation and cleanup, and exact CI.
   Candidates must have neither credentials nor writable scoring machinery.
   No model-backed workflow or OAuth secret belongs in public CI.
6. **Execution allocation:** decide explicitly whether to authorize only the
   unrelated integration or also a pilot contingent on matching successful
   integration and freeze. Proposed maxima are five integration dispatches
   (three planned) and 64 pilot dispatches across 32 planned trajectories.
   Subscription USD is unknown, ambiguous calls remain debited, and no automatic
   reissue, replacement, extra sample or relaxed immediate stop is included.

The human decision must bind the final reviewed revision and exact CI, not an
earlier draft or green check. Real account/model access, the current route
and provider usage behavior can be established only after separate live approval.
