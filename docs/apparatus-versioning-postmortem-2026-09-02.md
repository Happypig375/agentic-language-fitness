# Apparatus versioning postmortem

The repository previously treated each deployment correction as a new
scientific protocol. That inflated v2 into v13 without changing the measured
question. V3 is the last meaningful scientific configuration revision: it
changed the model family and effort settings. V4–V13 were apparatus attempts
for Docker-store identity, host portability, provider egress, CLI flags,
authentication projection, readiness, line endings, process ownership, and
SSH/firewall routing. None reached a valid candidate or model outcome.

Those attempts remain useful forensic history in the pre-rewrite repository,
but they are not pooled cells and must not produce v14. Git history is the
audit trail; runtime code should contain one supported route.

## Failure categories retained from v4–v13

| Attempts | Apparatus issue | Correct classification |
|---|---|---|
| v4–v5 | Docker-store image metadata and host portability | runner/environment validation |
| v5–v6 | Provider egress and proxy setup | pre-candidate transport attempt |
| v6–v8 | Unsupported CLI flags and authentication projection | runner/authentication defects |
| v9–v11 | Readiness, process scanning, and checkout line endings | test/preflight defects |
| v12–v13 | Firewall/NAT routing and oversized transition/evidence machinery | transport redesign and engineering cleanup |

No row above produced a valid candidate or model outcome.

## New identity model

Keep these independent:

- **Scientific specification:** model/effort, prompts, tasks, evaluator,
  schedule, estimand, inclusion rules, and candidate-visible semantics.
- **Runner revision:** launcher, proxy, container invocation, and telemetry code.
- **Environment profile:** host, OS, image digest, toolchain, network route,
  and resource limits.
- **Attempt ID:** one actual invocation and its terminal status.

A pre-candidate infrastructure failure is retained and can be fixed and retried
under the same scientific specification. A candidate-observable runner or
environment change gets a new runner/environment identity and fresh calibration.
Only a scientific treatment or semantic change gets a new scientific spec.

## Corrective policy

Develop and integration-test the apparatus before freezing a cell. Pin the
runner and environment only after one real, non-counting end-to-end shakedown.
Never silently replace an attempt or retry a potentially billable request after
an ambiguous transport failure. Keep detailed raw logs outside the public
repository and publish only redacted, useful provenance.
