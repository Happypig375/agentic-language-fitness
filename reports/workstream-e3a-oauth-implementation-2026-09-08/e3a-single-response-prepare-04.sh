#!/usr/bin/env bash
set -euo pipefail
cd /build/source-lf
git apply --check /build/e3a-single-response-repair-04.patch
git apply /build/e3a-single-response-repair-04.patch
# Full just fmt and schema generation passed in attempt 03. This repair is Rust only.
cargo fmt --manifest-path codex-rs/Cargo.toml -- --config imports_granularity=Item
just fix -p codex-core -p codex-api -p codex-features --locked --profile dev-small \
    2>&1 | tee /build/single-response-lint-04.log
git diff --check
