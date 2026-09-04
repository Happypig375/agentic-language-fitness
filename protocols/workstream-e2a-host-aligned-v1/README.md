# Workstream E2a: host-aligned exact-command baseline

E2a is a model-free follow-up to the accepted E1 and E2 descriptive work. It
measures the materially distinct `dotnet` command forms authenticated from the
retained v3 event streams on the v3 remote host/profile. It does not start a
candidate or Codex process, mount authentication, or call a model endpoint.

## Frozen identities

- runner commit: `901260d7473648f67ee6dd9e469a922023866e2c`
- inventory: `794591e97d150bdc13d7a9079cee72cbd92f3057a639f71addc71c3f5fad4de3`
- definition: `8e1f417f2355c169102b68495dc083a0c61e0ea3e180914568be7603651448df`
- schedule: `c1e4b3c97c03b910f02fe39d19be9eaa608005359e81174b96acbf4c69b70308`

The inventory authenticates 10 runs, 80 tasks, all 435 completed command
events, and all 258 benchmark `dotnet` operations. It reduces them to 23
semantic forms: 3 restore, 6 build, 11 run, 2 test, and 1 direct-DLL form. The
frequency table remains stratified by v3 configuration, language, task, and
form without publishing raw commands, paths, transcripts, or output.

The deterministic schedule covers all 80 observed task/form cells in five
paired rounds for both languages. Its 800 audit-on samples are supplemented by
220 otherwise matched `NuGetAudit=false` samples for the 22 restore-capable
cells, for 1,020 samples in total.

Each sample uses the matched accepted E2 gold successor, a fresh workspace,
home, and NuGet cache, the pinned v3 image and SDK, 2 GiB memory, 2 CPUs, 256
PIDs, ext4-backed work storage, and the v3 internal-network proxy ecology. Raw
argv, output, and per-sample evidence remain outside Git. The published report
contains absolute timing/output summaries, paired ratios and differences, the
audit contrast, and an invocation-count times duration exposure envelope; the
envelope is never subtracted from agent cost.

Known bounds are frozen in `definition.json`: candidate interaction is absent,
gold successors replace unavailable intermediate candidate states, exact
within-task cache history is unavailable, host load is observed rather than
controlled, and shell syntax is replayed as fixed argv plus equivalent stdin
transport.

## Validation

```text
python scripts/alf.py --manifest benchmarks/successor/manifest.json e2a check \
  --definition protocols/workstream-e2a-host-aligned-v1/definition.json \
  --inventory protocols/workstream-e2a-host-aligned-v1/inventory.json \
  --e2-definition protocols/workstream-e2-toolchain-v1/definition.json
```

The remote run uses `infra/remote-runner/run-e2a.sh`. That wrapper executes the
entire source tree archived from the runner commit and keeps the archive
read-only inside the container.
