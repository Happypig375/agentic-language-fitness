# Experimental protocol

## Workstream E1 disposition

E1 reconciled ten preserved v3 runs and 80 tasks using analyzer commit
`82c8c6bdc429f0819a718ce6c4d567fe0a30e88a`; report SHA:
`644273ac0f25a32138d50d919ff15677b6ed9639a23198e0c719d154da94901d`.
The implementation commit passed exact-commit Linux/Windows CI; report
publication is accepted only when its own exact-commit CI is green. All 25
observable failed candidate operations were builds, with 19 conservative repair
cycles; F# carried the larger failed-build/repair burden in every configuration,
all five project-file changes, and about twice the evaluator time. These are
archive-only descriptive routing signals, not causal or universal findings.
Per-command timing, per-interaction usage, unique source exposure, replay, peak
context, and compaction are unavailable. See
`reports/workstream-e-v3/forensic-report.md` and
`docs/workstream-e1-v3-forensic-disposition-2026-09-03.md`.
E2 is the next gate: 18 canonical states, exactly five paired rounds,
fresh/repeat workspaces, model-free/offline, then review and exact-commit CI.

## Unit of execution

A **run** is one language implementation traversing an ordered task chain. The workspace begins from that language's baseline and retains successful code changes. Each task launches a new agent process and a new model conversation.

## Per-task sequence

1. Snapshot repository metrics and current commit.
2. Write the task request to `.alf/TASK.md` inside the workspace.
3. Start a fresh agent process.
4. Capture stdout, stderr, JSONL events, usage, duration, and exit status. Codex
   usage sums every `turn.completed.usage` record; missing, malformed, or negative
   fields invalidate accounting. Docker sidecars are marked as derived from raw
   JSONL and copied per task; generic commands report usage unavailable, never zero.
5. Build the project with the pinned toolchain.
6. Run all cumulative black-box cases through the line-oriented JSON protocol.
7. Record git diff and post-task repository metrics.
8. Commit the workspace only if evaluation passes; otherwise stop the chain by default.

## Agent adapters

### Scripted

Copies the checked-in cumulative gold source for the task. It is not an experimental treatment. It verifies that the chain, evaluator, and result serialization work.

### Codex

The adapter invokes a fresh process resembling:

```text
codex exec --json --ephemeral --ignore-user-config --ignore-rules \
  --sandbox workspace-write --cd WORKSPACE -
```

The task prompt is supplied on stdin. `--model` is added when specified. JSONL events are preserved and `turn.completed.usage` values are aggregated.

### Generic command

The command template supports:

- `{workspace}`
- `{root}` (harness repository, for locating a host-side wrapper)
- `{prompt_file}`
- `{task_id}`
- `{language}`

Equivalent environment variables are exported:

- `ALF_WORKSPACE`
- `ALF_ROOT`
- `ALF_PROMPT_FILE`
- `ALF_TASK_ID`
- `ALF_LANGUAGE`

The agent may write `.alf/usage.json`:

```json
{
  "input_tokens": 12000,
  "cached_input_tokens": 8000,
  "cache_write_input_tokens": 0,
  "output_tokens": 2400,
  "reasoning_output_tokens": 600,
  "tool_calls": 17,
  "model": "provider/model-snapshot"
}
```

Use `alf run --agent command --require-usage --agent-command ...` when the command
wrapper must produce usage. The adapter clears stale sidecars before each task;
missing or malformed fresh artifacts make the task unsuccessful while preserving
result artifacts. Without the flag, generic usage is optional and unavailable is
distinct from measured zero.

Missing fields remain unavailable according to the result schema; they are never
inferred silently. Official OpenAI usage defines `input_tokens` as including cached
and cache-write input tokens (not additive); see https://developers.openai.com/api/reference/resources/admin/subresources/organization/subresources/usage .
Exact Codex CLI 0.149.1 artifacts still require reconciliation against raw JSONL.
Agent-process time covers the child process only; evaluator time includes baseline
and cumulative evaluator calls; task time runs from task start through commit
attempt and immediately before task-result serialization; run time starts before
initialization and ends immediately before result serialization. These are monotonic
elapsed intervals and are not additive substitutes for one another. Read telemetry
supports only simple `cat/head/tail/less/more`, `sed -n`, and `rg PATTERN PATH`
forms with shell operators/options rejected; it does not infer semantic recovery.
The container wrapper additionally records `event_count`, tool-specific counts, and the
configured image identifier. If authentication is staged, project the complete Codex
home into an ephemeral writable directory (including refresh credentials), mode 0600,
and remove it after the run. Treat it as a password: never hash, log, commit, or expose
it in a manifest. A credential-free model-free gate may validate the launcher separately;
authentication is only used after the approved freeze gates.

## Fair-comparison rules

- Use identical task wording and cumulative behavioral tests.
- Randomize language order within model/agent blocks.
- Start from clean baseline copies.
- Do not reuse conversation state between maintenance tasks.
- Hold timeout, tools, documentation access, network policy, and compute limits constant.
- Repeat stochastic cells and report uncertainty.
- Review paired implementations for comparable architecture rather than mechanically forcing equal lines of code.
- Keep hidden tests external to the agent environment.

## Version and apparatus boundary

The scientific protocol identity covers the treatment and candidate-visible
semantics: model/effort, prompts, task chain, evaluator, schedule, estimand,
and analysis. Runner Git revision, container digest, host/network profile, and
attempt ID are separate provenance fields. A pre-candidate apparatus failure
is retained and may be repaired/retried under the same scientific specification.
Only candidate-observable runner/environment changes require a new apparatus
identity and fresh calibration; only scientific treatment or semantic changes
require a new scientific specification. Do not create a protocol version for
ordinary launcher, Docker, SSH, authentication, or readiness fixes.

For the remote profile, use the documented loopback CONNECT proxy and one
foreground SSH fixed `-R` session. See `docs/remote-execution.md`.

## Pilot line protocol

Each input line is one JSON request; each output line is one JSON response. The evaluator starts one process per cumulative case batch and compares parsed JSON values, avoiding language-specific unit-test frameworks.

## Workstream D schema v3

The current schema-v3 family is `workstream-d-language-v3`. The earlier v1
and v2 families are retired and retained only for audit history. v2 calibration
closed after M was confirmed too easy and L/C# hit a host OOM apparatus stop;
the unresolved attempt is not a candidate outcome and must not be retried,
pooled, or synthesized.

The v3 parent definition and H/M/L child definitions
use schema v3. They share the immutable six-macroblock assignment hash and
canonical descriptive manifest; each child selects only its configuration.
Frozen provenance records family, configuration, pair execution position,
macroblock or calibration ID, within-macroblock placement, stage, role, and
counting status. `model.requested_id` and reasoning effort are checked against
the tracked model-catalog preflight; the requested ID is not represented as a
resolved backend snapshot. Execution remains unauthorized until the clean
freeze and non-counting calibration gates pass. Conditional M/L reverse rows
are runnable only after their primary calibration has a separately audited and
documented boundary classification; the runner validates the frozen row but
does not derive that classification.

The v3 non-counting calibration is complete and recorded in
`reports/workstream-d-language-v3/calibration-report.json`. Ten audited retained
calibration outcomes are protocol-valid, accounting-valid, successful 8/8, with zero
agent/evaluator failures. H is saturated; M and L are too easy in primary and
reverse order. Formal macroblocks 1–6 are not authorized and no language-effect
claim may be made. Any next model run requires an explicitly reviewed successor
scientific design/new specification.

The v1 family was clean-frozen, then retired after its first H/F# calibration
ended as an apparatus-terminated unresolved attempt: post-process snapshot
validation crashed while the sidecar had timed out and no usage record. It has
no analyzable outcome and must not be pooled. The current family is
`workstream-d-language-v3`; v2 calibration is closed after M was confirmed too
easy and L/C# encountered host OOM pressure. Do not synthesize missing
result/log files or retry unresolved attempts. See
`docs/workstream-d-v2-calibration-incident-2026-08-31.md`.
