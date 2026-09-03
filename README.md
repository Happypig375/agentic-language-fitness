# Agentic Language Fitness

An auditable benchmark for measuring how programming language and agent
configuration shape the reliability and lifetime computational cost of coding
agents.

ALF studies inherited maintenance: an agent understands an existing repository,
changes it, verifies it, and hands the changed workspace to a fresh agent for
the next change. The first language family compares semantically matched F# and
C# services on .NET, holding runtime, packages, build system, external
behavior, evaluator, and task chain closely aligned. This is a research
workbench, not a leaderboard or a claim that one language is universally best.

## Why it is different

Most coding-agent benchmarks measure isolated tasks. ALF makes accumulated
repository state part of the treatment: later agents inherit previous edits,
misunderstandings, tests, and technical debt. It retains terminal stops and
failed tasks, not only successful completions, and records hidden behavioral
evaluation, source/representation checks, diffs, commands, timing, and token
usage when available.

The narrow question is:

> When semantically equivalent software is represented in different programming
> languages, how much agent computation is required to correctly understand,
> change, verify, and maintain it over inherited changes?

The research gap is deliberately modest. Sequential maintenance and
multilingual repository benchmarks already exist, and Tokenmaxxing shows that
language can change token expenditure. ALF targets their controlled
intersection: language as the independent variable inside inherited maintenance
over behaviorally matched repositories while holding runtime, task sequence,
oracle, agent configuration, and measurement protocol substantially constant.
See the [literature review](docs/literature-review.md), [search
log](docs/search-log.md), and [research-gap statement](docs/research-gap.md).

## Current evidence and status

The short `variance-v2` pilot found high stochastic and order variance on a
two-task chain. The reviewed `difficulty-v1` successor is an eight-task chain
that is no longer fully saturated, but it exposed candidate-caused
representation drift. These are feasibility findings, not evidence that F# or
C# is better.

Workstream D v3 used the canonical descriptive representation with Terra/Luna
capability configurations. Its ten audited non-counting calibrations all
completed 8/8 tasks, so the frozen difficulty rule blocked formal v3
macroblocks. Exploratorily, F# used more total input and agent time in all five
F#/C# calibration pairs, with geometric-mean ratios near 1.38. These totals are
ecological trajectory costs, not direct measurements of source compactness or
model memory.

The current phase is **Workstream E causal attribution**. Before any larger
cost replication, the project will analyze the preserved v3 command/build/test
traces, establish model-free toolchain baselines, and—only under a new reviewed
specification—separate comprehension, one-shot generation, and repair-loop
cost. Persistent orchestrator context and isolated repair workers are later
harness treatments because the current benchmark starts a fresh conversation
for every task. No paid/model run is presently authorized. See the
[causal-attribution design](docs/post-v3-interpretation-and-workstream-e-design-2026-09-03.md),
[calibration report](reports/workstream-d-language-v3/calibration-report.md),
and [canonical plan](PLAN.md).

V4–V13 were apparatus-development attempts, not additional scientific
treatments; their history and failure categories are summarized in the
[postmortem](docs/apparatus-versioning-postmortem-2026-09-02.md). No v14 exists.

## How a chain works

For each language and ordered task, ALF creates a baseline workspace, starts a
fresh agent process, retains successful changes, runs cumulative hidden
behavioral and structural checks, and records the attempt. In container runs,
gold snapshots, evaluator cases, parent repositories, credentials, and
unrelated host files remain outside the candidate boundary. Primary analysis
retains correctness and terminal-stop outcomes alongside unconditional cost;
paired common-exposure-prefix cost prevents an early failure from looking
artificially cheap.

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

The scripted adapter applies checked-in gold snapshots without model/API calls,
credentials, or paid usage. It is the recommended first check on a new machine.

## Real agents and remote execution

After the required review, validation, freeze, and calibration gates:

```text
alf run --language fsharp --agent codex --model YOUR_MODEL --output results/codex
```

For a memory-rich remote host whose model egress must use this machine, use the
single foreground PowerShell runner (exact paths and command are environment
specific):

```powershell
.\infra\remote-runner\run.ps1 -RemoteHost user@host -RemoteSshPort 830 -EnvironmentProfilePath .\infra\remote-runner\environment-profile.json -RemoteCommand 'exec /opt/alf/run.sh'
```

The tracked environment profile selects the dedicated internal Docker network,
local proxy port, and exact bridge listener. `scripts/codex-docker.py` derives
`HTTPS_PROXY` and `HTTP_PROXY` as `http://172.30.0.1:43128` from that profile.
The server should restrict the account with
`AllowTcpForwarding remote`, `GatewayPorts clientspecified`, and
`PermitListen 172.30.0.1:43128`. Use explicit identity and known-hosts paths
when possible. See [remote execution](docs/remote-execution.md).

For Codex container authentication, stage the complete `auth.json` in an
ephemeral writable `CODEX_HOME` with mode 0600, treat it as a password, and
remove it after the run. Do not minimize, blank, hash, log, or commit it.

## Repository map

- `src/alf/` — harness, adapters, protocol, accounting, and audit logic
- `benchmarks/pilot/` — matched .NET projects, tasks, evaluators, and snapshots
- `docs/` — protocol, environment, design, results, and research context
- `tests/` — unit and model-free regression tests
- `scripts/alf.py` — command-line entry point
- `PLAN.md` — canonical continuation order and decision gates

No open-source license has yet been selected. Public visibility alone does not
grant permission to redistribute or modify this code.
