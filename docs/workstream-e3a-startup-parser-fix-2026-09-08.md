# E3a startup-envelope parser repair — 2026-09-08

## Authority and scope

After the [stopped shakedown](workstream-e3a-oauth-shakedown-2026-09-08.md#live-attempt-01--stopped),
the user directed: “If it's a bug, automatically fix it. Write this into agentic
instructions”. [AGENTS.md](../AGENTS.md#automatic-bug-fixes) now records that
standing direction. Confirmed bugs receive bounded repairs, regression tests,
applicable review and validation without another repair-approval question.
Scientific/security decisions and additional live allowances remain distinct.

This is a model-free runner repair based on held revision
`05800b921b37bb725aa4875f7dd2779d8c20d354`, not a new scientific protocol or a
repeat of the failed live attempt. The parser incorrectly required every item
event to occur inside the turn. The pinned client emitted two local startup
diagnostics before `turn.started`, then completed normally.

## Narrow correction

Admit only the captured diagnostic event shapes and exact messages, in their
startup position and without duplicates or reordering. Keep them separately
from the assistant reply and visible replay. Unknown errors, pre-turn assistant
or tool events, misplaced diagnostics, extra turns and other invalid sequences
still fail closed. No warning-suppression setting, tool enablement, new proxy,
authentication path or native-client rebuild is part of this repair.

The regression fixture is
[`e3a-codex-startup-envelope.jsonl`](../tests/fixtures/e3a-codex-startup-envelope.jsonl),
copied from attempt 01's `raw_stdout` and asserted equal after checkout newline
normalization only. Its normalized SHA-256 is
`28e453a4f4fe4e68e64f396e5fc53c2ef03aa4a1b45ababe50ab200f2a82eaf7`
and is included in the existing generated review packet. The tests also run a
model-free two-step shakedown composition check. The earlier native capture checker alone
did not exercise this envelope through the strict adapter. The new regression
closes that specific coverage gap; it does not prove a fresh live run works.
The original report and journal remain unchanged, failed and debited. Parsing
their public trace offline does not apply/score the old reply, refund usage,
replace a sample or retrospectively complete a shakedown step.

The OpenAI Docs skill prompted a check of the official
[non-interactive JSONL documentation](https://learn.chatgpt.com/docs/non-interactive-mode#make-output-machine-readable).
It confirms the event-stream interface, but does not specify these customized
startup messages or their ordering. The exact captured pinned-client trace,
not a generic assumption that errors are harmless, determines this exception.

## Validation and identities

The bounded parser/fixture change received a separate AI-session source review
with no actionable findings. This is not human review or provider validation.
An initial validator summary cited pre-fix logs and was rejected as evidence
for this patch. A fresh independent validator executed all four affected test
modules sequentially: adapter **12**, shakedown runner **15**, review packet
**19**, controller/sandbox implementation **29** — **75 passing tests**.
The new captured-prefix two-step test is included in the runner's 15 tests.
Packet reproduction reported `packet: matches` / `candidate_model_calls: 0`;
`git diff --check` passed. Fresh local command output is under ignored
`results/e3a-startup-parser-fix-2026-09-08/`; CI provides published execution
evidence tied to the exact implementing commit, not the older activation/hold.

Reproduce the affected Windows checks from the repository root:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -p test_e3a_codex.py -v
.\.venv\Scripts\python.exe -m unittest discover -s tests -p test_e3a_run.py -v
.\.venv\Scripts\python.exe -m unittest discover -s tests -p test_workstream_e3a.py -v
.\.venv\Scripts\python.exe -m unittest discover -s tests -p test_e3a_implementation.py -v
.\.venv\Scripts\python.exe scripts/e3a_check.py
git diff --check
```

No live calls, OAuth staging, remote execution or candidate scoring are part
of these checks. The native code, auth staging and transport are unchanged;
their earlier checks were not rerun or relabelled as new evidence.

Normalized reviewed source-set SHA-256 (packet paths except the specification):
`b78dff8628e610eda4afc857a6a57ecbd7124cd533fbc13953fcc727c97319e9`.
The implementing Git revision is the commit introducing this record and those
source changes; its attached Linux/Windows CI must pass before live activation.

Unchanged identities:

- Held specification canonical SHA-256:
  `4d4457251726a2381a6a7e6a949a641c9741b02c7e3bf3160005bd2d93a6ed8b`.
- Scientific policy SHA-256 (excluding only status/activation):
  `95b1b7db184236c0b81982160f1c82394225bbc23a86762925a5c0a84771c13b`.
- Native binary SHA-256:
  `72cf14453c1879996b970accc7de9aa114bf570e586230799a429d0741bb1959`.
- Catalogue SHA-256:
  `c18214b1ba88ab9bd164753115324a7a29c0582e8d071f7b3babf749d892f549`.
- Image ID:
  `sha256:5d3e97d195dbbe7e47e47055e46f8c6f15fb9553be0c7ef19ed0060756fc7116`.

## Remaining live boundary

`execution_authorized=false` and `shakedown-stopped-awaiting-review` remain.
One original integration dispatch remains; a fresh two-step shakedown needs a
new bounded two-dispatch allowance. The automatic-bug-fix instruction does not
expand that allowance or permit reissuing an ambiguous attempt. There is no
freeze or pilot result. Do not ask for renewed scientific adoption, ordinary
bug-fix permission or routine direct-push permission.
