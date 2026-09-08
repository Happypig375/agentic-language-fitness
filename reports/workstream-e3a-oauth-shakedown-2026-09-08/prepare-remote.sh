#!/usr/bin/env bash
set -u

COMMIT="${1:?exact 40-hex commit required}"
if [[ ! "$COMMIT" =~ ^[0-9a-f]{40}$ ]]; then
  echo "commit must be exact lowercase 40-hex" >&2; exit 2
fi
ROOT="$(mktemp -d /tmp/alf-e3a-shakedown-XXXXXX)"
exec > >(tee "$ROOT/setup.stdout.log") 2>&1
echo "root=$ROOT"
status=0
finish() { echo "setup_status=$status"; }
trap finish EXIT

git clone --no-checkout https://github.com/Happypig375/agentic-language-fitness.git "$ROOT/repo" || { status=$?; exit "$status"; }
git -C "$ROOT/repo" checkout --detach "$COMMIT" || { status=$?; exit "$status"; }
PY=/home/user/miniconda3/bin/python
"$PY" --version
"$PY" -m venv "$ROOT/venv" || { status=$?; exit "$status"; }
"$ROOT/venv/bin/python" -m pip install --disable-pip-version-check -e "$ROOT/repo" || { status=$?; exit "$status"; }
{
  echo "python=$ROOT/venv/bin/python"; "$ROOT/venv/bin/python" --version
  echo "pip-freeze"; "$ROOT/venv/bin/python" -m pip freeze
  echo "head=$(git -C "$ROOT/repo" rev-parse HEAD)"
  echo "native_sha256=$(sha256sum /tmp/alf-e3a-native-build-zavnIH/codex-native-single-response | awk '{print $1}')"
  echo "catalog_sha256=$(sha256sum /tmp/alf-e3a-native-build-zavnIH/source-lf/codex-rs/models-manager/models.json | awk '{print $1}')"
  echo "image_identity"; docker image inspect --format '{{.Id}} {{.RepoDigests}}' 'sha256:5d3e97d195dbbe7e47e47055e46f8c6f15fb9553be0c7ef19ed0060756fc7116' || { status=$?; exit "$status"; }
  echo "network_identity"; docker network inspect alf-internal --format '{{.Id}} {{range .IPAM.Config}}{{.Subnet}} {{end}}' || true
} > "$ROOT/setup-record.txt"
(
  cd "$ROOT/repo" || exit
  "$ROOT/venv/bin/python" scripts/e3a_check.py
) || { status=$?; exit "$status"; }
echo "setup_record=$ROOT/setup-record.txt"
