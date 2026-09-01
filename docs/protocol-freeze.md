# Protocol freeze

A freeze captures the scientific specification and the exact apparatus used to
collect it. It is not a release of every launcher implementation.

## Freeze inputs

Record the scientific definition, complete schedule, task and benchmark hashes,
model/effort, evaluator, toolchain, resource limits, network policy, runner Git
revision, container digest, environment profile, and raw-retention policy.
Canonical text hashes normalize CRLF and lone CR to LF before SHA-256; binary
artifacts retain raw-byte hashes.

Every attempt additionally records `scientific_spec_sha256`, `runner_revision`,
`environment_profile`, and `attempt_id`, plus its phase and terminal status.
Secrets, including Codex authentication caches, never enter manifests or logs.

## Gates

1. Validate the scientific definition and runner model-free.
2. Obtain independent review and green Linux/Windows CI.
3. Complete one real, non-counting container-level route/authentication
   shakedown before freezing.
4. Freeze from a clean tree and pin the runner/environment identities.
5. Perform non-counting calibration; only then begin formal candidate runs.

The shakedown may use a trivial prompt and is not evidence for the study.
Calibration is always non-counting.

## Failure and retry rules

Record every started attempt. Pre-candidate protocol, authentication, provider,
host, evaluator, or transport failures are infrastructure attempts and may be
repaired/retried under the same scientific specification. The first valid
candidate outcome is immutable for its slot; do not silently replace it.

A runner correction before any valid candidate outcome is ordinary engineering
history. A candidate-observable runner or environment correction requires a new
runner/environment identity and fresh calibration. Only a change to treatment,
prompt, task, evaluator, candidate-visible semantics, schedule, estimand, or
analysis creates a new scientific specification.

The old rule that every harness correction increments the cell version is
retired; it caused the v4–v13 apparatus version ratchet. See
`docs/apparatus-versioning-postmortem-2026-09-02.md` and
`docs/remote-execution.md`.
