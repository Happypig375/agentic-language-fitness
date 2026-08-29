# Variance-v2 protocol freeze

`protocols/variance-v2/definition.json` is the tracked draft for the new formal
cell. It pins `gpt-5.4` with medium reasoning, Codex CLI/image
0.149.1, the .NET 10.0.302 toolchain, matched tasks, limits, isolation, and
failure rules. `variance-v1`, which pinned `gpt-5.4-mini-2026-03-17`, was retired
after its first C# calibration attempt was classified provider-invalid because
the authenticated provider rejected that model before any candidate outcome.
This v2 cell is distinct both from v1 and from the unaudited 2026-08-26
`gpt-5.6-luna` pair.

The explicit schedule contains one non-counting calibration (`C#` then `F#`)
and ten formal blocks, balanced by first language with a maximum run of two.
The listed schedule is authoritative; the generator metadata records the two
sequential seeded shuffles used to produce it.

All tracked text hashes in the definition (definition, schedule, benchmark
manifest, and task prompts) use canonical UTF-8 bytes with CRLF and lone CR
line endings normalized to LF before SHA-256. Binary image archives retain
their raw-byte SHA-256.

Validate the draft with:

```text
python scripts/alf.py protocol validate --definition protocols/variance-v2/definition.json
```

After all protocol edits are committed, run from that clean checkout:

```text
python scripts/alf.py protocol freeze --definition protocols/variance-v2/definition.json --output results/variance-v2/resolved-manifest.json
```

The freeze command derives Git, host, Docker, and container probes itself and
fails closed on dirty Git, unavailable facts, hash mismatch, or a different
image. The command also verifies the retained archive's path, byte count, and
SHA-256 before writing the resolved manifest. The retained image archive is
`X:\backup20260827\Archives\SourceRepos\agentic-language-fitness-images\alf-codex-0.149.1-sha256-0320a60c5b2628ce.tar`
(630053888 bytes, SHA-256
`55ee85f0656cef429d1cd40edced79782d54abb7b2180c9770c14bea06828ddf`), with
expected local image ID
`sha256:0320a60c5b2628cebeb2c897bbf80da949f3b9bb99fa61f5a3475c7276328756`.

The definition remains draft/unfrozen until committed clean and a resolved
manifest is generated. Raw attempts are retained, including retries. Formal
success and time outcomes include protocol-valid candidate correctness
failures, agent failures, and candidate-caused timeouts. Metric aggregates are
availability-specific: token aggregates require valid usage accounting, while
a timeout without terminal usage remains in success/time outcomes with token
fields unavailable. Protocol, authentication, provider, host, and evaluator-
infrastructure invalid attempts are retained and reported but excluded from
paired performance estimates; accounting-invalid fields are excluded only from
their affected metric aggregates. The adjudication precedence is protocol,
authentication, provider, host, timeout, accounting, agent, evaluator.
Calibration is always non-counting.

The 2026-08-29 variance-v1 pre-freeze checkpoint passed independent review and all assigned
model-free checks: 67 affected unit tests, strict environment doctor, benchmark
snapshot validation, both scripted chains, Docker smoke, protocol validation,
the real retained-archive hash, the A3 fixture audit, and both expected legacy
audit failures. An initial freeze attempt correctly refused the dirty working
tree. After commit `7dda2bd232376b84968bd616a79d8043699c48c7` passed Linux and Windows
CI, the clean freeze succeeded with resolved-manifest SHA-256
`0afe05f37d5fbfbe51cf336af1f515680b84856c99921041e7ea4a4cf82e08ca`.
The subsequent retained v1 calibration attempt was provider-invalid because
`gpt-5.4-mini-2026-03-17` was unsupported; it produced no candidate outcome or
terminal usage. This evidence does not make the v2 draft frozen and did not
validate v2.

Accepted token accounting also requires a sidecar derived from the preserved
Codex JSONL and exactly one `turn.completed` usage record per ephemeral task
invocation. Zero or multiple terminal usage records are retained but marked
accounting-invalid; the harness does not guess whether duplicated totals should
be summed.

The runner pins the Docker memory, CPU, and PID limits directly in the wrapper
command and reconciles them from the task sidecar; ambient `ALF_DOCKER_*`
values cannot alter a protocol run. The wrapper also performs a model-free
authentication preflight. Classification uses recorded signals and the declared
precedence: sidecar pin mismatch is protocol; failed auth preflight is
authentication; an authenticated non-zero provider process without terminal
usage is provider; a missing agent or evaluator executable is host; an agent or
task-evaluation process timeout is a candidate timeout; other invalid usage is
accounting; a valid evaluator envelope containing a build, run, or case failure
is an agent/correctness outcome; and a malformed evaluator envelope or failed
baseline is evaluator infrastructure.

Retries are allowed only after an automatically classified, retryable
protocol/authentication/provider/host/evaluator-infrastructure attempt. Attempt
IDs are sequential per block position. The first candidate outcome—including
an agent or correctness failure, timeout, or accounting-invalid outcome—is the
immutable primary observation and cannot be retried or replaced. Every started
protocol run writes `attempt.json` before workspace initialization; an
unresolved started attempt blocks another attempt for that position. Protocol
run directories use the validated attempt ID and are created atomically, so
concurrent invocations cannot reserve the same attempt.

After freezing, the predeclared calibration commands are:

```text
python scripts/alf.py run --language csharp --agent command --model gpt-5.4 --require-usage --output results/variance-v2 --timeout 600 --protocol-manifest results/variance-v2/resolved-manifest.json --block-id calibration-01 --order csharp-first --attempt-id calibration-01-csharp-01 --position 1
python scripts/alf.py run --language fsharp --agent command --model gpt-5.4 --require-usage --output results/variance-v2 --timeout 600 --protocol-manifest results/variance-v2/resolved-manifest.json --block-id calibration-01 --order csharp-first --attempt-id calibration-01-fsharp-01 --position 2
```

Position 2 fails closed until a matching, retained position-1 primary outcome
has a passing baseline and a completed task record. This includes a primary
whose usage accounting is invalid: the pair proceeds for success/time outcomes,
while affected token metrics remain unavailable. Audit both resulting run
directories before treating calibration as apparatus evidence. Any harness or
protocol correction increments the cell version and requires a new clean freeze
and calibration.
