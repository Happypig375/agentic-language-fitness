# Experimental protocol

## Unit of execution

A **run** is one language implementation traversing an ordered task chain. The workspace begins from that language's baseline and retains successful code changes. Each task launches a new agent process and a new model conversation.

## Per-task sequence

1. Snapshot repository metrics and current commit.
2. Write the task request to `.alf/TASK.md` inside the workspace.
3. Start a fresh agent process.
4. Capture stdout, stderr, JSONL events, usage, duration, and exit status.
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

Missing fields remain null/zero according to the result schema; they are never inferred silently.
The container wrapper additionally records `event_count`, tool-specific counts, and the
configured image identifier. Its temporary auth projection retains the `refresh_token`
schema key but blanks its value; a short-lived access token can still be read by the
unprivileged container process.

To validate an auth projection without a model run, bind it read-only at
`/home/codex/.codex/auth.json` and invoke `codex login status` in the image; this is the
same path used by the wrapper.

## Fair-comparison rules

- Use identical task wording and cumulative behavioral tests.
- Randomize language order within model/agent blocks.
- Start from clean baseline copies.
- Do not reuse conversation state between maintenance tasks.
- Hold timeout, tools, documentation access, network policy, and compute limits constant.
- Repeat stochastic cells and report uncertainty.
- Review paired implementations for comparable architecture rather than mechanically forcing equal lines of code.
- Keep hidden tests external to the agent environment.

## Pilot line protocol

Each input line is one JSON request; each output line is one JSON response. The evaluator starts one process per cumulative case batch and compares parsed JSON values, avoiding language-specific unit-test frameworks.
