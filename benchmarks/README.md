# Benchmarks

`pilot/` is an executable infrastructure benchmark, not a final research dataset.

It contains:

- behaviorally matched F# and C# baseline projects;
- an ordered two-task maintenance chain;
- cumulative black-box JSON cases;
- cumulative gold snapshots used only by the scripted CI adapter;
- a manifest consumed by the Python harness.

The agent workspace receives only the baseline/current code and task prompt. Gold and evaluator data stay outside the copied workspace. Publication-quality runs require stronger container isolation as described in `docs/environment.md`.
