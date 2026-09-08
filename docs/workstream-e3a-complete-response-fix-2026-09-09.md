# E3a complete multi-message response repair — 2026-09-09

## Pilot attempt 02: retained hard stop

The renewed freeze commit `c79bc1c36593a4658da56d0b00656c31dc438248`
passed exact [CI 34251358861](https://github.com/Happypig375/agentic-language-fitness/actions/runs/34251358861)
(Linux 6m13s, Windows 7m53s). The canonical local-OAuth wrapper then invoked
the fixed pilot once on the fresh `/tmp/alf-e3a-shakedown-uJ169U` checkout.
The transcript starts at 00:38:29 HKT. The first predecessor preflight passed;
the first model dispatch then stopped the batch with `multiple-final-replies`.

All 24 slots are retained: one started/finished controller trajectory with one
attempted round, 23 unstarted. No candidate source was applied or evaluated;
first and terminal format/build/holdout/completion scores remain null. The
original report is not retrospectively reclassified or promoted. There is no
paired F#/C# result or language-performance conclusion from this attempt.

Usage is known: **8,840 input / 3,813 output tokens**, including 2,070 reasoning
tokens as an output subset. One dispatch remains charged to the pilot; it is
not refunded. Cache/cache-write fields, reliable provider-request counts and
subscription USD remain null. The recorded single completed native turn is
not a claim that all provider-side HTTP activity was counted.

Immutable evidence in
[`reports/workstream-e3a-oauth-pilot-2026-09-08/`](../reports/workstream-e3a-oauth-pilot-2026-09-08/):

- `attempt-02-report.json`, SHA-256
  `c493fd524b5f05af1a9c0c6be20e2e2265e87482f305276a77e845a6c886581a`.
- `attempt-02-journal.jsonl`, SHA-256
  `67cee6fb9a95c730d4c6736dca763c5fd1e894fb238bd4449aea369eaaaf05ef`.
- `attempt-02-invocation.log`, `attempt-02-cleanup.json` and
  `renewed-freeze-ci.json`.

The wrapper verified removal of its temporary full OAuth file/directory and
copied output. Fresh successful scoped checks at 16:41:47–16:41:49 UTC
(00:41:47–00:41:49 HKT on September 9) found no selected proxy listeners or
running E3a containers. The original local auth file remains untouched. A
publication scan found no token-shaped fields/strings. This is scoped cleanup
evidence, not a global credential-absence proof.

## Diagnosis: repair policy, not a new native client

The captured stream has one thread, one started turn and one completed turn,
process return code 0 and reliable terminal usage. It contains two distinct
completed `agent_message` items: a natural-language preamble followed by a
JSON file submission. The pinned CLI exposes no phase/channel label that would
justify selecting one message as the final answer. The existing parser rejects
any two completed assistant messages as `multiple-final-replies`.

An initial read-only AI diagnosis correctly identified that implementation
and its regression test, but concluded a native/channel-contract amendment
was necessary. A separate AI policy review found the controlling adopted
rule in [the OAuth amendment](../protocols/workstream-e3a-v1/oauth-amendment.md):
complete outputs below 49,152 bytes, including malformed outputs, remain
repairable under the existing submission budget. The capture here is complete,
not an incomplete turn or unknown-usage failure. Treating its malformed
assistant content as a fatal transport failure contradicts that rule.

The ordinary correction is deterministic whole-response assembly: concatenate
all completed in-turn assistant-message text in event order, adding or removing
no characters. Preserve the entire raw JSONL, including item boundaries. Apply
the existing aggregate reply-byte limit and strict submission parser to that
whole text, and retain the same text in visible replay. The actual preamble
plus JSON must fail `patch-format` and consume a submission, with only the
already allowed bounded repair feedback. Do not select the last JSON, remove
commentary, clean syntax, parse fragments separately or modify candidate code.

Tool/unexpected items, non-string text, multiple turns/completions, incomplete
capture, invalid/missing usage, overflow, timeout and existing independent
alarms retain their original handling. No prompt, native binary, model,
scientific policy, sandbox, auth or proxy change is needed. This is another-AI
policy/source review, not human review or independent provider verification.

## Current boundary

The parser now uses exact `"".join(messages)` in event order; no native or
controller framework change was needed. The two archived assistant messages
contain **7,006 aggregate UTF-8 bytes**, below the existing cap. Their joined
text remains invalid JSON; the repair does not salvage the file submission
by discarding the preamble. Raw event/item boundaries are preserved separately.

Fresh independent validation passed **81 tests**: `test_e3a_codex.py` 14,
`test_e3a_implementation.py` 30, `test_e3a_run.py` 18 and
`test_workstream_e3a.py` 19, each selected sequentially using
`.venv\Scripts\python.exe -m unittest discover -s tests -p <filename> -v`.
`scripts/e3a_check.py` reproduced the packet with zero new model calls, and
`git diff --check` passed. All commands exited 0. Fresh logs are retained in
ignored `results/e3a-complete-response-fix-2026-09-09/`.

Regressions cover exact Unicode/whitespace/order preservation, the actual
archived capture, adjacent independent JSON objects remaining invalid,
aggregate limits across items, and a synthetic adapter/controller trajectory:
first `patch-format` failure with no applied source, ordinary feedback, whole
unchanged reply in visible replay, and a separately debited allowed mock repair.
No archived candidate was executed, evaluated, promoted or rescored. Existing
sequence/tool/usage/capture guards remain in force. Another AI session reviewed
the implementing diff and found no actionable issue.

Specification SHA-256 remains
`d33b0f7ed317b4f1792ab22bdf82086bb25a11cebf93781aedd6ebfff5701996`;
policy remains `4c5d1345662555563e054b6124c44195382e93412be9c1e6d8dda7bf503f493f`.
The repaired source-set SHA-256 is
`8b549b678337ade391ef7b95a3c484413589c6031f3e50998ebe88856ff12164`.
The old freeze is preserved and correctly rejects that new source identity;
this is not a new freeze or authorization. Complete publication and verify CI
on the exact pushed repair commit before handoff. Preserve the failed report
and its original null scores unchanged.

Then return for a live continuation/allocation decision. The resumed integration
allocation is **four of five used, one remaining**; the fixed pilot has **one
of 72 used, 71 remaining**. Those balances are not fresh allocations. A changed
source needs a matching two-step shakedown, which does not fit the remaining
single integration dispatch. Do not automatically reissue the stopped candidate,
resume the 23 remaining slots, replace a slot or launch a fresh pilot. The
five-apparatus-failure rule does not override this retained live hard stop.
