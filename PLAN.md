# Research plan

This is the canonical continuation plan. The scientific Workstream D design is approved; no paid/model run is authorized yet.

## Scientific checkpoint

V3 is the active scientific configuration family and preserves the reviewed Terra/Luna configuration change. Its first H/F# calibration predecessor is unresolved because of host memory; do not infer an outcome or run later slots. Earlier v1/v2 cells remain excluded as documented in their incident notes.

V4–V13 are not scientific families. They were apparatus-development attempts covering Docker portability, egress, authentication, readiness, and SSH transport. Their rationale and disposition are summarized in the postmortem. There will be no v14.

The replacement runner, environment-profile split, and failure reconciliation
have passed the full 224-test local model-free suite, strict doctor, benchmark
validation, PowerShell parsing, and independent review with no remaining
P0–P3 findings. No Docker, SSH, provider authentication, candidate, or model
activity occurred. Publication and exact-commit CI are the next gate.

## Ordered gates

1. Publish the reviewed history cleanup and pass exact-commit Linux/Windows CI.
2. Run one real container-level, non-counting shakedown through the exact route; test readiness and streaming without a study prompt or pooled observation.
3. Tag/pin the runner Git revision, container digest, and environment profile.
4. Create clean v3 freezes and perform only the approved non-counting calibration, then resume the predeclared schedule if its gates pass.

## Identity and retry policy

Every record carries four independent IDs: `scientific_spec_sha256`, `runner_revision`, `environment_profile`, and `attempt_id`. A pre-candidate apparatus failure is retained and may be repaired/retried under the same scientific specification. A candidate-observable runner or environment change requires a new runner/environment revision and fresh calibration; a change to scientific treatment or semantics requires a new scientific specification. Never silently replace an attempt or rerun a billable request after an ambiguous transport failure.

See `docs/remote-execution.md` and `docs/apparatus-versioning-postmortem-2026-09-02.md`.
