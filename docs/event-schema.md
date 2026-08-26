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

The schema is versioned through `schema_version`. Consumers should ignore unknown fields and fail explicitly on unsupported major versions.
