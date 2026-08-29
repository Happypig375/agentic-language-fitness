# Benchmarks

`pilot/` is the original two-task executable infrastructure benchmark, not a
final research dataset. `successor/` is the validated eight-task cumulative
chain with 90 final cases per language; it is currently scripted-only
(gold/evaluator validation, not model runs).

It contains:

- behaviorally matched F# and C# baseline projects;
The pilot contains behaviorally matched F# and C# baseline projects, cumulative
black-box JSON cases, gold snapshots used only by the scripted CI adapter, and
a manifest consumed by the Python harness.

The successor retains the pilot baseline and Tasks 001/002, and uses cumulative
workspace checks and multi-file golds. Golds remain outside candidate
workspaces; neither benchmark authorizes paid/model-backed runs.

The agent workspace receives only the baseline/current code and task prompt. Gold and evaluator data stay outside the copied workspace. Publication-quality runs require stronger container isolation as described in `docs/environment.md`.
