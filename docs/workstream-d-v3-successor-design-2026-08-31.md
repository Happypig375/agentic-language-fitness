# Workstream D v3 successor design (2026-08-31)

v3 is a versioned successor to the closed v2 descriptive-language family. It
keeps the benchmark, task hashes, six-macroblock counterbalanced assignment,
Codex 0.149.1 image/archive, .NET 10.0.302 toolchain, limits, isolation, and
schedule semantics unchanged. The version also adds explicit per-task host
memory probes and telemetry, a material apparatus change, plus new catalog and
raw roots. Runtime availability remains deferred to non-counting calibration; this
document authorizes no model call.

The nominal capability settings are H=`gpt-5.6-terra` medium,
M=`gpt-5.6-luna` high, and L=`gpt-5.6-luna` medium. This is a capability
ordering hypothesis for calibration, not a monotonicity or language-effect
claim. M deliberately does not preserve v2's same-model reduced-effort role:
v2 M was confirmed too easy in both primary and reverse language orders, so a
higher effort on the lower-tier Luna is the proposed versioned boundary
replacement.
The cross-family difficulty classification informed this successor choice, but
never the sign or magnitude of a language contrast. No later result may change
these settings inside v3. Independent review remains pending.

The catalog was observed/fetched at `2026-08-30T16:45:00.468027400Z` by Codex
0.151.0. Terra exposed low/medium/high/xhigh/max/ultra and Luna exposed
low/medium/high/xhigh/max; both were visible and `supported_in_api`. Runtime
preflight is still required. Official references: [GPT-5.6 Terra](https://developers.openai.com/api/docs/models/gpt-5.6-terra)
and [GPT-5.6 Luna](https://developers.openai.com/api/docs/models/gpt-5.6-luna).

Every child pins host memory immediately before each candidate task: at least
2,147,483,648 physical bytes and 6,442,450,944 commit bytes. An explicit
failed probe is host infrastructure-invalid and retryable; missing artifacts
never imply OOM. No benchmark, maintainer subagent, or unrelated model run may
run concurrently.

The 2 GiB physical / 6 GiB commit thresholds leave headroom for the pinned 2
GiB candidate container, Docker and evaluator overhead, and the host itself;
they are preflight safety gates, not an OOM detector. An OOM after a passing
probe is an apparatus-stop/close event and is not automatically retried.

Required gates are independent review, model-free validation, direct commit to
`main`, green Linux/Windows CI, and clean child freezes with resolved hashes.
Only then may v3 calibrations run, with reverse-order confirmation before a
boundary replacement.
