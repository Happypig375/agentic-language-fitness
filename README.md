# Agentic Language Fitness

An auditable benchmark for measuring how programming language and agent configuration shape the reliability and lifetime computational cost of coding agents.

ALF studies inherited maintenance: an agent understands an existing repository, changes it, verifies it, and hands the changed workspace to a fresh agent for the next change. The first language family compares behaviorally matched F# and C# services on .NET, closely aligning semantic tasks, external behavior, evaluator, runtime family, and measurement protocol. Language-specific compiler, project, package, and tool behavior remain part of the ecological treatment and are controlled separately where the research question requires it. This is a research workbench, not a leaderboard or a claim that one language is universally best.

## Why it is different

Most coding-agent benchmarks measure isolated tasks. ALF makes accumulated repository state part of the treatment: later agents inherit previous edits, misunderstandings, tests, and technical debt. It retains terminal stops and failed tasks, not only successful completions, and records hidden behavioral evaluation, source/representation checks, diffs, commands, timing, and token usage when available.

The narrow question is:

> When semantically equivalent software is represented in different programming languages, how much agent computation is required to correctly understand, change, verify, and maintain it over inherited changes?

The research gap is deliberately modest. Sequential maintenance and multilingual repository benchmarks already exist, and Tokenmaxxing shows that language can change token expenditure. ALF targets their controlled intersection: language as the independent variable inside inherited maintenance over behaviorally matched repositories while holding task sequence, oracle, agent configuration, and measurement protocol substantially constant, while explicitly measuring ecological toolchain differences rather than pretending they do not exist. See the [literature review](docs/literature-review.md), [search log](docs/search-log.md), and [research-gap statement](docs/research-gap.md).

## Current evidence and status

The short `variance-v2` pilot found high stochastic and order variance on a two-task chain. The reviewed `difficulty-v1` successor is an eight-task chain that exposed candidate-caused representation drift. These are feasibility findings, not evidence that F# or C# is universally better.

Workstream D v3 used the canonical descriptive representation with Terra/Luna capability configurations. Its ten audited non-counting calibrations all completed 8/8 tasks, so the frozen difficulty rule blocked formal v3 macroblocks. Exploratorily, F# used more total input and agent time in all five F#/C# calibration pairs, with geometric-mean ratios near 1.38. These totals are ecological trajectory costs, not direct measurements of source compactness or model memory.

Workstream E1 reconstructed the archived trajectories. Among observable candidate operations, F# incurred 23 failed builds versus 2 for C#, 17 conservative repair cycles versus 2, all five committed project-file changes, nearly all compiler diagnostic output, and about twice the evaluator duration. Observable pre-edit inspection/search was much less separated. The failed-build total includes dependency/restore failures as well as genuine source syntax/type/project errors, so it cannot be read as 23 bad F# patches. The leading observed pathway is nevertheless first-patch/compiler/type/project difficulty followed by repair amplification, not static source size. Per-interaction usage, unique source exposure, replay, and context/compaction remain unavailable. See the [E1 disposition](docs/workstream-e1-v3-forensic-disposition-2026-09-03.md) and [forensic report](reports/workstream-e-v3/forensic-report.md).

Workstream E2 measured canonical source states and a fixed offline toolchain path. Source/token proxies and built-program execution were near parity, while F# builds were slower. Its large restore ratio was audit/source and host sensitive, so it was retained as a separate offline ecology rather than transported directly to v3. See the [E2 disposition](docs/workstream-e2-toolchain-disposition-2026-09-04.md) and [E2 report](reports/workstream-e2-toolchain-v1/report.md).

Workstream E2a then aligned command semantics and the v3 remote host/profile. It authenticated all 435 completed v3 command events and 258 benchmark `dotnet` operations, reducing them to 23 semantic forms, and executed 1,020 model-free samples in five paired rounds. Across the retained v3 runs, F# issued 163 benchmark tool operations versus 95 for C#. On the aligned host, restore/build-capable F# operations were substantially slower; pure tests and direct-DLL execution were near parity.

E2a isolated a major tool-policy amplifier: `NuGetAudit=false` reduced F# restore from about 7.8 seconds to about 2.1 seconds and removed repeated `NU1900` output. The authenticated v3 streams themselves contained 197 F# `NU1900` lines and zero C# lines. The v3 internal proxy allowed model traffic but blocked NuGet source reachability while audit remained enabled and homes/caches were fresh. The original v3 condition is therefore specifically a **legacy constrained-network audit-on** ecology, not a general default developer environment. A sizeable no-restore F# compiler/toolchain gap remained after audit was disabled.

The frequency-weighted mechanical tool-time gap was large relative to observed agent wall-time differences, but it is descriptive—not a causal percentage or a value to subtract from agent cost. Model-token differences still require additional interactions, diagnostics, feedback, and replay. See the [E2a disposition](docs/workstream-e2a-disposition-2026-09-04.md), [published E2a report](reports/workstream-e2a-host-aligned-v1/report.md), and [successor review](docs/workstream-e2a-review-and-successor-revision-2026-09-05.md).

The next bounded step is specification and independent review of E3a, a controlled shared-prefix first-patch and bounded-repair pilot. Its controller will preflight dependencies, remove audit and implicit-restore variation, own the first patch/build boundary, distinguish source failures from environment failures, and retain round-level model and tool evidence. No model call is currently authorized.

Before any repair subagent is built, a later E3b/F0 treatment will test deterministic single-agent tool policy: audit outside the edit–compile loop, no implicit restore, no-build/direct execution, and bounded duplicate-free feedback with full raw evidence retained separately. Its ecological comparator must be explicitly intended and reproducible—preferably online with audit source reachability verified—rather than silently reusing the legacy blocked-source condition. See the [canonical plan](PLAN.md).

V4–V13 were apparatus-development attempts, not additional scientific treatments; their history and failure categories are summarized in the [postmortem](docs/apparatus-versioning-postmortem-2026-09-02.md). No v14 exists.

## How a chain works

For each language and ordered task, ALF creates a baseline workspace, starts a fresh agent process, retains successful changes, runs cumulative hidden behavioral and structural checks, and records the attempt. In container runs, gold snapshots, evaluator cases, parent repositories, credentials, and unrelated host files remain outside the candidate boundary. Primary analysis retains correctness and terminal-stop outcomes alongside unconditional cost; paired common-exposure-prefix cost prevents an early failure from looking artificially cheap.

Controlled mechanism treatments may deliberately replace free tool choice with a controller-owned compile/evaluation path. Those treatments are named separately from ecological free-tool runs and are never pooled as though they were the same harness.

## Quick start

Requirements: Python 3.11+, Git, and .NET SDK 10.0.302.

```text
python -m pip install -e .
python -m unittest discover -s tests -v
python scripts/alf.py doctor --strict
python scripts/alf.py validate
python scripts/alf.py matrix --agent scripted --output results/pilot
python scripts/alf.py audit PATH_TO_RUN_DIRECTORY
python scripts/alf.py summarize results/pilot
```

The scripted adapter applies checked-in gold snapshots without model/API calls, credentials, or paid usage. It is the recommended first check on a new machine.

## Real agents and remote execution

After the required review, validation, freeze, and calibration gates:

```text
alf run --language fsharp --agent codex --model YOUR_MODEL --output results/codex
```

For a memory-rich remote host whose model egress must use this machine, use the single foreground PowerShell runner; exact paths and commands are environment specific:

```powershell
.\infra\remote-runner\run.ps1 -RemoteHost user@host -RemoteSshPort 830 -EnvironmentProfilePath .\infra\remote-runner\environment-profile.json -RemoteCommand 'exec /opt/alf/run.sh'
```

The tracked environment profile selects the dedicated internal Docker network, local proxy port, and exact bridge listener. `scripts/codex-docker.py` derives `HTTPS_PROXY` and `HTTP_PROXY` from that profile. The server should restrict the account with `AllowTcpForwarding remote`, `GatewayPorts clientspecified`, and the corresponding `PermitListen`. Use explicit identity and known-hosts paths when possible. See [remote execution](docs/remote-execution.md).

For Codex container authentication, stage the complete `auth.json` in an ephemeral writable `CODEX_HOME` with mode 0600, treat it as a password, and remove it after the run. Do not minimize, blank, hash, log, or commit it.

## Repository map

- `src/alf/` — harness, adapters, protocol, accounting, and audit logic
- `benchmarks/pilot/` and `benchmarks/successor/` — matched .NET projects, tasks, evaluators, and snapshots
- `docs/` — protocol, environment, design, results, reviews, and research context
- `protocols/workstream-e2-toolchain-v1/` — frozen offline E2 source/toolchain baseline
- `protocols/workstream-e2a-host-aligned-v1/` — frozen host-aligned command baseline
- `reports/` — publishable audited aggregates; raw evidence remains outside Git
- `tests/` — unit and model-free regression tests
- `scripts/alf.py` — command-line entry point
- `PLAN.md` — canonical continuation order and decision gates

No open-source license has yet been selected. Public visibility alone does not grant permission to redistribute or modify this code.
