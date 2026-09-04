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

Workstream E1 is complete. Its archive-only analyzer reconciled all ten v3 runs
and 80 tasks. Among observable candidate operations, F# incurred 23 failed
builds versus 2 for C#, 17 conservative repair cycles versus 2, all five
committed project-file changes, nearly all compiler error/warning output, and
about twice the evaluator duration. Observable pre-edit inspection/search was
much less separated. The leading observed pathway is therefore first-pass and
compiler/type/project difficulty followed by repair amplification, not static
source size. Per-command timing, per-interaction usage, unique source exposure,
replay, and context/compaction remain unavailable. See the
[E1 disposition](docs/workstream-e1-v3-forensic-disposition-2026-09-03.md) and
[forensic report](reports/workstream-e-v3/forensic-report.md).

Workstream E2 is also complete. Its frozen model-free offline baseline passed
all 18 canonical states and 90 scheduled entries. Source/token proxies and
built-program execution were near parity, while F# repeat builds took about 3.1
times as long as C# in that apparatus. The much larger 8.403 restore ratio is
not yet transportable to v3: the offline condition emitted 225 repeated F#
`NU1900` audit/source warnings, and E2's explicit restore/build/run commands may
not match the forms candidates actually used. Toolchain latency can amplify a
repair-heavy trajectory, but it cannot be mechanically subtracted from agent
cost or assumed to explain model-token usage. See the
[E2 disposition](docs/workstream-e2-toolchain-disposition-2026-09-04.md),
[audited report](reports/workstream-e2-toolchain-v1/report.md), and
[E1/E2 synthesis review](docs/workstream-e1-e2-synthesis-review-2026-09-04.md).

V4–V13 were apparatus-development attempts, not additional scientific
treatments; their history and failure categories are summarized in the
[postmortem](docs/apparatus-versioning-postmortem-2026-09-02.md). No v14 exists.

Workstream E2a is complete and published: 1,020 model-free samples in five
paired rounds reconstructed redacted E1 command-equivalence classes, replayed
materially observed forms under the v3 environment, added a `NuGetAudit=false`
control, and calculated an absolute command-count × duration exposure envelope.
See the [E2a disposition](docs/workstream-e2a-disposition-2026-09-04.md) and
[published report](reports/workstream-e2a-host-aligned-v1/report.md). The next
permissible work is a separately reviewed E3 specification; no model call is
authorized without a separate maintainer/user decision.

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
- `protocols/workstream-e2-toolchain-v1/` — frozen offline E2 source/toolchain baseline
- `reports/` — publishable audited aggregates; raw evidence remains outside Git
- `tests/` — unit and model-free regression tests
- `scripts/alf.py` — command-line entry point
- `PLAN.md` — canonical continuation order and decision gates

No open-source license has yet been selected. Public visibility alone does not
grant permission to redistribute or modify this code.
