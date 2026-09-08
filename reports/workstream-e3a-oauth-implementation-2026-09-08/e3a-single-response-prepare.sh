#!/usr/bin/env bash
set -euo pipefail
cd /build/source-lf
# The caller supplies an additive patch against the retained no-tools source.
git apply --check /build/single-response-candidate.patch
git apply /build/single-response-candidate.patch
just fmt 2>&1 | tee /build/single-response-format-02.log
just write-config-schema 2>&1 | tee /build/single-response-schema-02.log
just fix -p codex-core -p codex-api -p codex-features --locked --profile dev-small \
    2>&1 | tee /build/single-response-lint-02.log
git diff --check
