# E3a canonical Codex capability handoff (2026-09-06)

This is model-free fixture evidence for reconciling E3a with the required local
OAuth-backed Codex implementation. It is not OAuth evidence, real-provider
integration, a protocol amendment, or permission for a live run. The checks ran
from repository base `c8a266b933b10d5ca455362e478620c9649eebc1` with Codex
`0.149.1` and the pinned image
`sha256:5d3e97d195dbbe7e47e47055e46f8c6f15fb9553be0c7ef19ed0060756fc7116`.

Two isolated fixture runs completed successfully with no remote failures:
[baseline](../reports/workstream-e3a-codex-capability-2026-09-06/baseline.json)
and [input-shape](../reports/workstream-e3a-codex-capability-2026-09-06/input-shape.json).
The baseline source raw SHA is
`f22c06dfb0a90377103daf49861282913786755a20bb8ac95f1fbf44283162df`; the
input-shape source raw SHA is
`6baa6f3cbeaa711f7dc39a06d8177b20f29e09700e884ac077bc9a330a1343ce`.
Raw report SHAs are respectively
`b04e5d41e495d0bed7878d8660e1f23924ff073491611e506678415ae94f8306` and
`40d234205f3c69afd9d8c6f6906a2fbfef8fa1683340b798d31c294d7fb19b07`.
The canonical specification identity remains
`8bc53d30e45dfa72b087225f89c9e5547266f05b47e4306e2b326d951888bc62`.

The [test-only checker](../scripts/e3a_codex_check.py) used an unrelated fixed
prompt and a custom loopback Responses SSE fixture without credentials. It
refuses to launch Codex outside Linux with only the loopback interface.
Containers used `--network none`, a read-only root, writable 256 MiB `/tmp`
tmpfs, UID/GID 1000, all capabilities dropped, no-new-privileges, 512 PIDs,
2 CPUs, `--memory 6g --memory-swap 6g` (6 GiB total, no extra swap).
Only the read-only checker and writable output directory were bind-mounted;
no auth, research, or gold material was exposed.
The outer remote script/tmp directory was removed after local hash verification;
both owned containers are gone and the image is retained.

Observed capability: model `gpt-5.6-luna`, high/all-turns reasoning, exact fake
output, and an 11-input/4-output round trip. The request used Responses-lite,
`store=false`, `tool_choice=auto`, and no `previous_response_id`. The CLI added
developer/environment text containing `exec_command` and `apply_patch` markers.
An absent `tools` field therefore does not prove no-tools authority. These first
turns had no output-token cap or count endpoint. CLI-reported cached/reasoning
zeros are not observed model usage because the fixture omitted those fields.
Likewise, absent `previous_response_id` on an initial request does not establish
that continuation is unsupported; the current adapter still creates fresh
ephemeral task sessions and lacks the reviewed repair-chain implementation.

Conclusion: preserve OAuth staging and the canonical remote runner; do not ask
for an API key, add a relay, switch to a toolful scaffold, or loosen ceilings.
The next decision is reviewed reconciliation of candidate authority/context,
Codex session/turn accounting, enforceable request/token/time ceilings, and
unknown/null subscription cost. Hold if canonical OAuth cannot support those
controls. Tasks, R1–R4, outcomes, packet/history, and live gates are unchanged.
This was maintainer AI review followed by implementation, not independent
approval of the scientific treatment. Focused tests (10 passed on Windows) and
`e3a_check` packet validation passed; CI for the new commit was pending.
