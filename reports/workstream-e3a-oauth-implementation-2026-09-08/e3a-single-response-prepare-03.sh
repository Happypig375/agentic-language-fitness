#!/usr/bin/env bash
set -euo pipefail
cd /build/source-lf
# Attempt 02 applied the patch and ran Rust formatting before Buildifier failed.
# Only trusted pinned formatting tools may use build-container egress here.
just fmt 2>&1 | tee /build/single-response-format-03.log
just write-config-schema 2>&1 | tee /build/single-response-schema-03.log
just fix -p codex-core -p codex-api -p codex-features --locked --profile dev-small \
    2>&1 | tee /build/single-response-lint-03.log
git diff --check
