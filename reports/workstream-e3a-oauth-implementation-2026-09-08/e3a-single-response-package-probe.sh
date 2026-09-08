#!/usr/bin/env bash
# Model-free packaging/configuration check; NOT the OAuth dispatch wrapper.
set -euo pipefail
probe_base=/tmp/alf-e3a-native-build-zavnIH
probe_output=$(mktemp -d "$probe_base/package-single-response-XXXXXX")
probe_container="alf-e3a-package-${probe_output##*-}"
trap 'docker rm -f "$probe_container" >/dev/null 2>&1 || true' EXIT
probe_args=(run --rm --name "$probe_container" --network none --pull=never
  --read-only --tmpfs /tmp:rw,size=256m,nosuid,nodev
  --user "$(id -u):$(id -g)" --cpus 2 --memory 6g --memory-swap 6g
  --pids-limit 512 --cap-drop ALL --security-opt no-new-privileges
  --env HOME=/tmp/alf-codex-home --env CODEX_HOME=/tmp/alf-codex-home
  --mount "type=bind,source=$probe_base/codex-native-single-response,target=/usr/local/bin/codex,readonly"
  --mount "type=bind,source=$probe_base/source-lf/codex-rs/models-manager/models.json,target=/opt/alf/models.json,readonly"
  sha256:5d3e97d195dbbe7e47e47055e46f8c6f15fb9553be0c7ef19ed0060756fc7116)
timeout 30s docker "${probe_args[@]}" --version >"$probe_output/version.stdout" 2>"$probe_output/version.stderr"
timeout 30s docker "${probe_args[@]}" --config features.no_tools=true \
  --config features.single_response=true --config features.code_mode_host=false \
  --config 'model_catalog_json="/opt/alf/models.json"' debug models \
  >"$probe_output/catalog.stdout" 2>"$probe_output/catalog.stderr"
printf 'PACKAGE_OUTPUT=%s\n' "$probe_output"
