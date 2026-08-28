# Result and event schema

Every run writes:

```text
results/<run-id>/
  result.json
  workspace/
  tasks/<task-id>/
    agent.stdout
    agent.stderr
    events.jsonl
    task-result.json
```

`result.json` contains environment metadata, baseline evaluation, ordered task results, aggregate usage, and final status.

A task result records:

- task/language/agent/model identifiers;
- start/end timestamps and elapsed seconds;
- agent exit and failure information;
- token categories when available;
- event, tool, command, and file-change counts;
- build and behavioral-evaluation results;
- pre/post repository metrics;
- git diff statistics and commit identifiers;
- paths to raw logs.
- `agent.accounting_valid` and `agent.usage_available` indicate reconciled or
  explicitly unavailable usage. Agent-process, evaluator, task-total, and run-total
  wall-time fields are distinct. File-read, unique-read, and revisit counts use
  only recognizable command syntax/path tokens; unsupported shell constructs and
  semantic recovery are excluded.

The schema is versioned through `schema_version`. Consumers should ignore unknown fields and fail explicitly on unsupported major versions.
