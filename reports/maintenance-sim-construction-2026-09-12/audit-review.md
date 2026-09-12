# Maintenance construction apparatus audit review

**Review type:** independent static AI review; **original verdict: REQUEST_CHANGES**.
The finding was subsequently resolved in the provenance recheck below. The final
integration disposition records later independent behavioral acceptance; it does
not rewrite the original review or imply human approval.
No build, runtime, model, or remote execution was performed. Another validator
owns behavioral execution. I previously authored contract-derived additions to
`fixtures/cases.json`; I did not implement the helper, CLI, tests, fault
manifest, or fault patches. That prior oracle authorship limits independence
for judging the witness expectations, so this review focuses on apparatus and
evidence semantics.

## Scope and source identity

SHA-256 hashes of every reviewed source/input:

| File | SHA-256 |
|---|---|
| `src/alf/maintenance.py` | `16c5513ef83a5e120aef33e8ee64240d47a4c9ea034977c482c00730ce421184` |
| `scripts/maintenance_check.py` | `353dbffb044fd7a462ca1e005c6606f5b97b6b1745f2ebe6abd3e75cd9259c56` |
| `tests/test_maintenance.py` | `32a148684b41734fc8c3e954f99fe7096010856646cdce555aea7c606cf87ab2` |
| `benchmarks/maintenance-sim/construction.json` | `7d32a4cc943500e614434c56a2f02c06d466068accb7255530db982ca16e266e` |
| `benchmarks/maintenance-sim/fixtures/cases.json` | `7131882aa7fac3b6f5305ea75c7080de18c5bec22dbd86be60036c4a9433f2f5` |
| `benchmarks/maintenance-sim/fixtures/faults.json` | `ceefcdb7e74023ed6675c9ba18fd8ee3b1e1bd7dbdab09bcea20b45a49451185` |
| `docs/maintenance-sim-construction-2026-09-12.md` | `704ba977090f04a75fc443725da210e791f133ea0f25a6233f9e9a955e480ef1` |
| `faults/csharp/bypass-policy.patch` | `030948498867f6f5e41eadf3ee65a2dc169b13480bc7ae42b5c0b50fe89efd81` |
| `faults/csharp/drop-due-effects.patch` | `b08b9e765e2aed35503405a84526c5d7f55ccccc2d79c35c5b18295a419f3a04` |
| `faults/csharp/leak-replay-registry.patch` | `6740f727adc261cfd1e58c3ea09350a749f72597fba42a6085fd7bab425d9bd8` |
| `faults/csharp/omit-future-cancel.patch` | `480682c7d78e5cbb232c32ca7ef5c4c10495703635c40298f7b4ffb7835ce8c1` |
| `faults/fsharp/bypass-policy.patch` | `ceab48accc6abf1175427dc263fdfa8175086be7c611dcdca5c2dcc2d0ba90c6` |
| `faults/fsharp/drop-due-effects.patch` | `d5750780e1322c4455f0b64a3e3902a9cac6a42e0c9159709464f6f50f6e8e06` |
| `faults/fsharp/leak-replay-registry.patch` | `621e1a0e0b0fc8eba7c9ddbfbe3d1136312e085971fea097c1d29a6967cef79b` |
| `faults/fsharp/omit-future-cancel.patch` | `d17231598f3497290b692dd8259d8fd8799e0b537179caf8baa65999b2225a9d` |

## Finding

### P1 — emitted audit provenance does not bind the apparatus or raw fault selection

`scripts/maintenance_check.py:19-27` constructs top-level
`provenance.content_sha256` from the contracts, guidance, cases, seeds, and
reference patches. It omits `scripts/maintenance_check.py`,
`src/alf/maintenance.py`, and raw `fixtures/faults.json`. Per-fault records bind
the applied patch and canonical witness, but not the manifest bytes or the code
that classifies and reports the outcome (`src/alf/maintenance.py:403-438`). A
report therefore cannot establish which classifier/helper or manifest mapping
produced it. This blocks accepting the report as source-bound evidence. Add
those three raw hashes and the focused `tests/test_maintenance.py` source hash
to emitted provenance, and cover their presence with a CLI test.

## Reviewed behavior

The static flow otherwise uses reconstructed trusted sources for baseline and
mutant execution; requires a passing baseline plus a compile-successful semantic
failure for a kill; treats build/runtime/parse as unavailable with correctness
`null`; and keeps semantic failure available. No-op and malformed fixtures retain
identical source and are explicitly labelled fixed applicability evidence, not
controller/submission handling. Recovery keeps `prior_failure`,
`strict_chain_success=false`, `actual_candidate_repair=false`, and
`gold_reset=false`.

All eight fault mappings are present for both languages at episodes 1/2/5/8,
with due effects, future cancellation, policy bypass, and replay-registry
witnesses. All eight downstream episode mappings are explicit. Manifest paths
must be relative POSIX paths below `fixtures/faults`; resolved patches must remain
inside that directory and be regular non-symlink files. Envelope mapping enforces
predecessor N-1/current episode N and includes only seed contract, prior public
episodes, current task, guidance, and supplied source—no successor gold or
evaluation cases.

This is trusted-fixture host apparatus, not an arbitrary-candidate sandbox; no
new framework or candidate-isolation claim is warranted. Static inspection
cannot attest that patches apply, references compile, mutations survive
compilation, or expected runtime/semantic results occur; those claims depend on
the separately running exact CLI validation.

## Provenance repair recheck

**Disposition:** the original P1 `REQUEST_CHANGES` finding above is retained as
history and is **resolved for the reviewed provenance repair**. The repaired CLI
adds the raw helper, checker, focused-test, and fault-manifest files to
`content_sha256`, using `relative_to(args.root).as_posix()` for stable POSIX
relative keys. The focused regression checks all four expected keys and hashes
against raw file bytes. The author reports 27 focused tests passing; this static
recheck did not execute them.

Repaired identities:

| File | SHA-256 |
|---|---|
| `src/alf/maintenance.py` | `16c5513ef83a5e120aef33e8ee64240d47a4c9ea034977c482c00730ce421184` |
| `scripts/maintenance_check.py` | `82adbf649cf52fc3c4490d06a2eec7b0a153f5570dda529ffba6548ca25f68e5` |
| `tests/test_maintenance.py` | `7e4946b0260a430789e08be0d460a203680417e84715f6b46398ddb2d6891758` |
| `benchmarks/maintenance-sim/fixtures/faults.json` | `ceefcdb7e74023ed6675c9ba18fd8ee3b1e1bd7dbdab09bcea20b45a49451185` |

At that recheck, this resolved only apparatus provenance. The then-current full
behavioral report still found F# cancellation broken, and a separate session was
repairing the F# lineage. Future bytes and behavioral reruns were not approved by
that static recheck; source-review approval remained separate.

## Final integration disposition

This paragraph is the coordinating AI's outcome-unblinded evidence reconciliation,
not a new static review by the original apparatus reviewer or human sign-off.
The [final raw report](evidence/report.json), SHA-256
`ab6e5a53023929b7d731a6675a455c3c877f1b42064b9d258c84bce152f2fea5`, binds the
repaired apparatus identities above and all unchanged fault-patch bytes. The
independent validator passed 27 focused tests and the complete trusted audit:
18 checkpoints, 608 case evaluations, eight semantic faults, 12 transition
scenarios and 16 downstream witnesses. The separate
[reference review](reference-review.md) records the corrected F# identities and
its final acceptance. The old failed report remains in the
[evidence index](evidence/index.json).

The apparatus provenance finding is resolved and the required trusted behavioral
evidence now passes. These conclusions do not establish candidate isolation,
provider behavior, human expert approval or live authority. Exact-publication CI
is a separate publication check; allocations remain zero.
