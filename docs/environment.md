# Environmental assumptions

## Minimum local environment

- Python 3.11 or newer
- .NET SDK 10.0.302
- Git 2.x
- a POSIX-like shell for the Makefile (the Python CLI itself is cross-platform)
- optional: Codex CLI for the `codex` adapter
- optional: Docker for stronger isolation and reproducibility

The benchmark projects use only the .NET standard library and no third-party NuGet packages.

## Agent authentication

The harness never stores API keys. A real-agent command inherits the caller's environment. For Codex, authenticate the CLI beforehand or expose credentials through the normal Codex mechanism. Record the CLI version, model identifier, account mode, and reasoning settings with every study run.

`--ignore-user-config` and `--ignore-rules` are used by the Codex adapter to reduce hidden configuration variance; authentication still comes from the normal Codex home. The adapter uses an ephemeral session and starts a new process for each task.

## Reproducibility assumptions

The executable pilot records exact detected versions, and the checked-in project requires SDK `10.0.302`. A publishable experiment should additionally pin:

- OS/container image digest;
- CPU architecture and resource limits;
- exact .NET SDK, Python, Git, agent CLI, and tokenizer versions;
- exact model snapshot where the provider exposes one;
- temperature/sampling and reasoning settings;
- network policy and available documentation;
- timeout and retry policy;
- run order and random seeds.

## Isolation and leakage

The local pilot keeps hidden tests and gold snapshots outside the copied workspace, but this is not an adversarial security boundary. An unrestricted host agent may be able to inspect parent directories or the benchmark repository.

For credible measurements, run each task in a disposable container or VM that mounts only:

1. the task workspace as writable;
2. the language toolchain as read-only;
3. an agent endpoint or narrowly scoped network route.

The evaluator should run outside that environment after the agent exits. Gold snapshots and hidden cases must never be mounted into the agent container.

## Network assumptions

- `scripted` validation needs no model network access.
- Initial SDK/container installation may require network access.
- Real cloud agents require their provider endpoint.
- During task execution, unrestricted web access is a treatment variable. Disable it by default or record it explicitly.

## Cost-accounting assumptions

Exact model tokens are available only when the agent exposes them. The Codex adapter parses JSONL `turn.completed` usage fields. A generic command can write `.alf/usage.json`. When exact usage is absent, the result marks fields as unavailable rather than estimating them from source text.

Provider billing and token counts are not perfectly interchangeable. Report raw token categories, wall time, tool calls, and monetary cost separately; do not collapse them prematurely into one score.

## Windows

The Python harness and .NET projects are cross-platform. For consistent real-agent isolation, WSL2 or Linux containers are recommended. Native Windows runs should record shell, path, sandbox, and filesystem differences as environmental factors.

## Workstream D configuration validation

Each child uses the difficulty-v1 image, toolchain, limits, isolation, and
accounting pins. `model.requested_id` is the exact string passed to the pinned
Codex CLI; it is not a resolved-backend assertion. The model catalog is tracked
and hashed, but provider/runtime identity is confirmed only by a later
non-counting calibration after clean freezes. Conditional reverse calibration
rows additionally require the audited primary-pair boundary decision described
in the design. No model run is authorized during D1.

The v1 family was clean-frozen and then retired after the first H/F# calibration
became an unresolved apparatus-terminated attempt due to a post-process
snapshot/requested_id validation crash. It has no analyzable outcome and is not
pooled; do not synthesize missing logs/results or retry it. New calibration work
uses v3: H=`gpt-5.6-terra` medium, M=`gpt-5.6-luna` high, and
L=`gpt-5.6-luna` medium. A host-memory probe runs immediately before every
candidate task and requires 2,147,483,648 physical and 6,442,450,944 commit
bytes. Failed probes are host-invalid and retryable; missing artifacts never
justify inferring OOM.
