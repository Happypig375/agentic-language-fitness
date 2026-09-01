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

## Schema v3 identity fields

Workstream D events carry `family_id`, `configuration_id`, `pair_block_id`,
`execution_position`, `macroblock` or `calibration_id`,
`within_macroblock_position`, `stage`, `role`, `counting`,
`family_definition_sha256`, `parent_schedule_sha256`, `catalog_sha256`, and
`assignment_sha256`. Protocol attempt records additionally carry
`scientific_spec_sha256`, `runner_revision`, `environment_profile`,
`route_profile_sha256`, and `attempt_id`; these identities change
independently. Task agent records reconcile the route profile plus
`auth_cache_staged` and `auth_cleanup_ok` from the container sidecar.
Calibration events use an explicit non-counting role and
never enter the formal assignment hash.

Current events use `workstream-d-language-v3`; v1/v2 remain auditable. Each
candidate task records an explicit immediately-before-task host-memory probe,
thresholds, and pass/fail disposition. Missing, empty, or truncated artifacts
are unresolved apparatus state and are never inferred to be OOM or a candidate
outcome without explicit evidence.
