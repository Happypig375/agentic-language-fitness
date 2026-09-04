#!/usr/bin/env bash
set -Eeuo pipefail

# E2a model-free runner.  This is intentionally a host-side wrapper: the
# container receives only source, definition/inventory, and writable evidence
# directories.  It never mounts Codex credentials or invokes a model.

V3_RUNNER_SHA='b180ed938b6286764e06ffee85a86381e8a14850'
IMAGE='alf-codex:0.149.1'
IMAGE_ID='sha256:5d3e97d195dbbe7e47e47055e46f8c6f15fb9553be0c7ef19ed0060756fc7116'
IMAGE_TAR_SIZE='630053888'
IMAGE_TAR_SHA='55ee85f0656cef429d1cd40edced79782d54abb7b2180c9770c14bea06828ddf'
NETWORK='alf-internal'
GATEWAY='172.30.0.1'
ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd -P)"
die() { echo "run-e2a: $*" >&2; exit 2; }
[[ "$#" -eq 6 ]] || die 'usage: run-e2a.sh E2A_SHA DEFINITION INVENTORY V3_REPO OUTPUT_DIR WORK_DIR'
E2A_SHA=$1; DEFINITION=$2; INVENTORY=$3; V3_REPO=$4; OUT=$5; WORK=$6

[[ "$E2A_SHA" =~ ^[0-9a-f]{40}$ ]] || die 'E2A_SHA must be a 40-character commit SHA'
for p in "$DEFINITION" "$INVENTORY" "$V3_REPO" "$OUT" "$WORK"; do [[ "$p" = /* && "$p" != *[[:space:]]* ]] || die 'paths must be absolute and contain no whitespace'; done
out_parent=$(dirname -- "$OUT"); work_parent=$(dirname -- "$WORK")
[[ -d "$out_parent" && -d "$work_parent" && "$out_parent" == "$work_parent" ]] || die 'output/work must share an existing parent'
root_abs=$(realpath -e -- "$ROOT"); v3_abs=$(realpath -e -- "$V3_REPO"); parent_abs=$(realpath -e -- "$out_parent")
case "$parent_abs/" in "$root_abs/"*|"$v3_abs/"*) die 'output/work parent must be outside repositories';; esac
[[ "$OUT" != "$WORK" ]] || die 'output/work must be distinct'
[[ "$parent_abs" != '/' && "$parent_abs" != '/home' && "$parent_abs" != "$(realpath -e -- "${HOME:-/nonexistent}" 2>/dev/null || true)" ]] || die 'unsafe output/work parent'
out_name=$(basename -- "$OUT"); work_name=$(basename -- "$WORK")
[[ "$out_name" =~ ^[A-Za-z0-9._-]+$ && "$work_name" =~ ^[A-Za-z0-9._-]+$ ]] || die 'unsafe output/work basename'
OUT="$parent_abs/$out_name"; WORK="$parent_abs/$work_name"
[[ "$OUT" != "$WORK" ]] || die 'canonical output/work paths must be distinct'
[[ -f "$DEFINITION" && -f "$INVENTORY" ]] || die 'definition and inventory files are required'
[[ ! -L "$DEFINITION" && ! -L "$INVENTORY" ]] || die 'definition/inventory symlinks are forbidden'
DEFINITION=$(realpath -e -- "$DEFINITION")
INVENTORY=$(realpath -e -- "$INVENTORY")
[[ "$DEFINITION" == "$root_abs/"* && "$INVENTORY" == "$root_abs/"* ]] || die 'definition/inventory must be inside clean source repository'
[[ -d "$V3_REPO/.git" || -f "$V3_REPO/.git" ]] || die 'v3 repo is not a Git checkout'
[[ -d "$ROOT/.git" || -f "$ROOT/.git" ]] || die 'source repository is not a Git checkout'

case "$OUT$WORK" in *$'\n'*|*$'\r'*) die 'output/work path contains a newline';; esac
[[ ! -e "$OUT" ]] || die 'output directory must be absent'
[[ ! -e "$WORK" ]] || die 'work root must be absent/fresh'
mkdir -- "$OUT" "$WORK"
work_created="$WORK"
[[ "$(stat -c %F "$WORK")" == 'directory' ]] || die 'work root is not a directory'
[[ "$(findmnt -T "$ROOT" -n -o FSTYPE 2>/dev/null || true)" == ext4 ]] || die 'source filesystem is not ext4'
[[ "$(findmnt -T "$WORK" -n -o FSTYPE 2>/dev/null || true)" == ext4 ]] || die 'work filesystem is not ext4'

[[ -z "$(git -C "$ROOT" status --porcelain)" ]] || die 'source checkout is dirty'
[[ -z "$(git -C "$V3_REPO" status --porcelain)" ]] || die 'v3 repo is dirty'
v3actual=$(git -C "$V3_REPO" rev-parse HEAD)
[[ "$v3actual" == "$V3_RUNNER_SHA" ]] || die 'v3 repo HEAD mismatch'
git -C "$ROOT" cat-file -e "$E2A_SHA^{commit}" || die 'E2a commit unavailable'
git -C "$ROOT" show "$E2A_SHA:infra/remote-runner/run-e2a.sh" | cmp -s - "$ROOT/infra/remote-runner/run-e2a.sh" || die 'wrapper differs from implementation commit'
docker info --format '{{.Driver}}' | grep -qx overlay2 || die 'Docker storage driver is not overlay2'
docker_root=$(docker info --format '{{.DockerRootDir}}'); [[ "$(findmnt -T "$docker_root" -n -o FSTYPE 2>/dev/null || true)" == ext4 ]] || die 'Docker data filesystem is not ext4'
docker image inspect "$IMAGE" --format '{{.Id}}' | grep -qx "$IMAGE_ID" || die 'Docker image identity mismatch'
docker network inspect "$NETWORK" --format '{{.Internal}} {{(index .IPAM.Config 0).Gateway}}' | grep -Fxq 'true '$GATEWAY || die 'Docker network identity mismatch'

tar_file="$V3_REPO/.artifacts/images/alf-codex-0.149.1-sha256-0320a60c5b2628ce.tar"
[[ -f "$tar_file" ]] || die 'portable image archive is required'
[[ "$(stat -c %s "$tar_file")" == "$IMAGE_TAR_SIZE" ]] || die 'portable image archive size mismatch'
[[ "$(sha256sum "$tar_file" | awk '{print $1}')" == "$IMAGE_TAR_SHA" ]] || die 'portable image archive hash mismatch'

env_json="$OUT/observed-environment.json"
python3 - "$env_json" "$E2A_SHA" <<'PY'
import json, sys
out, commit = sys.argv[1:]
data = {'schema_version':'alf.workstream-e2a.environment-observation.v1','e2a_runner_git_sha':commit,'profile_id':'remote-highmem-local-egress-r1','runner_profile_id':'runner-remote-highmem-local-egress-r1','v3_runner_git_sha':'b180ed938b6286764e06ffee85a86381e8a14850','container_image_id':'sha256:5d3e97d195dbbe7e47e47055e46f8c6f15fb9553be0c7ef19ed0060756fc7116','portable_image_archive':{'sha256':'55ee85f0656cef429d1cd40edced79782d54abb7b2180c9770c14bea06828ddf','bytes':630053888},'dotnet_sdk':'10.0.302','resource_limits':{'memory':'2g','memory_swap':'2g','cpus':2,'pids':256},'storage':{'workspace_filesystem':'ext4','work_root_filesystem':'ext4','docker_data_filesystem':'ext4','docker_storage_driver':'overlay2','container_root_filesystem':'overlayfs','tmp_filesystem':'overlayfs','root_read_only':False,'tmp_writable_uid_1000':True},'network':{'docker_network':'alf-internal','internal':True,'bridge_gateway':'172.30.0.1','http_proxy':'http://172.30.0.1:43128','https_proxy':'http://172.30.0.1:43128','no_proxy':['127.0.0.1','localhost'],'allowed_authority':'chatgpt.com:443','nuget_source_reachability':'blocked-by-connect-proxy-allowlist'},'process':{'uid':1000,'gid':1000,'candidate_present':False,'codex_present':False,'model_endpoint_configured':False,'auth_present':False},'cache':{'home_fresh_per_sample':True,'nuget_cache_fresh_per_sample':True,'home_under_ext4_work_root':True},'source':{'canonical_gold_successors':True}}
with open(out, 'w', encoding='utf-8') as f: json.dump(data, f, indent=2, sort_keys=True); f.write('\n')
PY

cleanup() {
  rc=$?
  # Revalidate the stored leaf; never recompute cleanup from an input path.
  work_abs=$(realpath -e -- "$work_created" 2>/dev/null || true)
  work_parent_now=$(realpath -e -- "$parent_abs" 2>/dev/null || true)
  [[ "$work_parent_now" == "$parent_abs" && "$(dirname -- "$work_abs")" == "$parent_abs" && "$(basename -- "$work_abs")" == "$work_name" && "$work_abs" != '/' ]] && rm -rf -- "$work_abs"
  exit "$rc"
}
trap cleanup EXIT INT TERM
mkdir -p -- "$WORK/run/home" "$WORK/run/tmp"
mkdir -- "$WORK/source"
git -C "$ROOT" archive "$E2A_SHA" | tar -x -C "$WORK/source"
args=(run --rm --name "alf-e2a-${E2A_SHA:0:12}" --entrypoint /bin/bash
  --network "$NETWORK" --cap-drop ALL --security-opt no-new-privileges
  --memory 2g --memory-swap 2g --cpus 2 --pids-limit 256 --user 1000:1000
  -v "$WORK/source:/repo:ro" -v "$DEFINITION:/e2a/definition.json:ro" -v "$INVENTORY:/e2a/inventory.json:ro"
  -v "$OUT:/e2a/output" -v "$WORK/run:/e2a/work"
  -e HOME=/e2a/work/home -e CODEX_HOME=/e2a/work/home -e E2A_SHA="$E2A_SHA"
  -e TMPDIR=/e2a/work/tmp -e HTTP_PROXY=http://$GATEWAY:43128 -e HTTPS_PROXY=http://$GATEWAY:43128 -e NO_PROXY=127.0.0.1,localhost
  "$IMAGE" -c 'set -e
python3 /repo/scripts/alf.py --root /repo --manifest benchmarks/successor/manifest.json e2a run --definition /e2a/definition.json --inventory /e2a/inventory.json --e2-definition protocols/workstream-e2-toolchain-v1/definition.json --observed-environment /e2a/output/observed-environment.json --runner-git-sha "$E2A_SHA" --work-root /e2a/work --raw-output /e2a/output/raw
python3 /repo/scripts/alf.py --root /repo --manifest benchmarks/successor/manifest.json e2a report --definition /e2a/definition.json --inventory /e2a/inventory.json --raw-output /e2a/output/raw --output-json /e2a/output/report.json --output-markdown /e2a/output/report.md
python3 /repo/scripts/alf.py --root /repo --manifest benchmarks/successor/manifest.json e2a audit --definition /e2a/definition.json --inventory /e2a/inventory.json --report /e2a/output/report.json --raw-output /e2a/output/raw')
docker "${args[@]}"
