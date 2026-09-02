# Research plan

This is the canonical continuation plan. The scientific Workstream D design is approved; no further paid/model run is authorized under v3.

## Scientific checkpoint

V3 is the active scientific configuration family and preserves the reviewed Terra/Luna configuration change. Its ten-run non-counting calibration is complete: H is saturated; M and L were too easy in both primary and reverse order. No language effect is identified.

V4–V13 are not scientific families. They were apparatus-development attempts covering Docker portability, egress, authentication, readiness, and SSH transport. Their rationale and disposition are summarized in the postmortem. There will be no v14.

The replacement runner, environment-profile split, and failure reconciliation
have passed the full 224-test local model-free suite, strict doctor, benchmark
validation, PowerShell parsing, and independent review with no remaining
P0–P3 findings. Exact-commit CI, route shakedown, clean freezes, and the
non-counting calibration are complete; formal macroblocks 1-6 are blocked
pending a reviewed successor design.

## Ordered gates

1. Preserve the completed runner, route, freeze, and calibration evidence.
2. Stop: the next action changes scientific treatment and requires an explicitly reviewed successor design/new scientific specification.
3. No paid/model activity under v3; do not create v14.

## Identity and retry policy

Every record carries four independent IDs: `scientific_spec_sha256`, `runner_revision`, `environment_profile`, and `attempt_id`. A pre-candidate apparatus failure is retained and may be repaired/retried under the same scientific specification. A candidate-observable runner or environment change requires a new runner/environment revision and fresh calibration; a change to scientific treatment or semantics requires a new scientific specification. Never silently replace an attempt or rerun a billable request after an ambiguous transport failure.

See `docs/remote-execution.md` and `docs/apparatus-versioning-postmortem-2026-09-02.md`.
