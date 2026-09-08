[CmdletBinding()]
param(
    [Parameter(Mandatory)] [ValidatePattern('^[0-9a-f]{40}$')] [string] $ExpectedCommit,
    [Parameter(Mandatory)] [ValidatePattern('^/tmp/alf-e3a-shakedown-[A-Za-z0-9]{6}$')] [string] $RemoteRunRoot,
    [Parameter(Mandatory)] [string] $LocalAuthFile,
    [Parameter(Mandatory)] [string] $LocalOutputDirectory,
    [ValidateSet('shakedown','pilot')] [string] $Phase = 'shakedown'
)

$Phase = $Phase.ToLowerInvariant()
$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$profilePath = Join-Path $repoRoot 'infra\remote-runner\environment-profile.json'
$launcherPath = Join-Path $repoRoot 'infra\remote-runner\run.ps1'
$checkPath = Join-Path $repoRoot 'scripts\e3a_check.py'
$oldPath = $env:PATH
$primaryError = $null; $cleanupError = $null; $exitCode = 1; $remoteAuthRoot = $null
$transcriptStarted = $false
$nativeSha256 = '72cf14453c1879996b970accc7de9aa114bf570e586230799a429d0741bb1959'
$catalogSha256 = 'c18214b1ba88ab9bd164753115324a7a29c0582e8d071f7b3babf749d892f549'
$imageId = 'sha256:5d3e97d195dbbe7e47e47055e46f8c6f15fb9553be0c7ef19ed0060756fc7116'
$remoteHost = 'user@cez083.ce.ust.hk'
$sshArgs = @('-T','-p','830','-o','BatchMode=yes','-o','StrictHostKeyChecking=yes','-o','ConnectTimeout=10',$remoteHost)
$scpArgs = @('-P','830','-o','BatchMode=yes','-o','StrictHostKeyChecking=yes','-o','ConnectTimeout=10')

function Invoke-CheckedRemote([string] $Command) {
    $result = @(& ssh.exe @sshArgs $Command)
    if ($LASTEXITCODE -ne 0) { throw "remote command failed: $Command" }
    return $result
}

function Get-RemoteSha256([string] $Path, [string] $Name) {
    $lines = Invoke-CheckedRemote "sha256sum -- $Path"
    $match = $lines | Where-Object { $_ -match '^([0-9a-f]{64})\s+' } | Select-Object -First 1
    if (-not $match) { throw "remote $Name sha256sum output was invalid" }
    return ([regex]::Match($match, '^([0-9a-f]{64})\s+')).Groups[1].Value
}

if (-not (Test-Path -LiteralPath $LocalAuthFile -PathType Leaf)) { throw 'LocalAuthFile must be a regular file' }
if ((Get-Item -LiteralPath $LocalAuthFile).LinkType) { throw 'LocalAuthFile must not be a symlink' }
if (Test-Path -LiteralPath $LocalOutputDirectory) { throw 'LocalOutputDirectory must not already exist' }
New-Item -ItemType Directory -Path $LocalOutputDirectory | Out-Null
$transcriptPath = Join-Path $LocalOutputDirectory 'invocation.log'
Start-Transcript -LiteralPath $transcriptPath -Force | Out-Null
$transcriptStarted = $true

try {
    foreach ($path in @($profilePath,$launcherPath,$checkPath)) {
        if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw "required tracked file is missing: $path" }
    }
    $head = (Invoke-CheckedRemote "git -C $RemoteRunRoot/repo rev-parse HEAD").Trim()
    if ($head -cne $ExpectedCommit) { throw 'remote checkout commit preflight failed' }
    if (Invoke-CheckedRemote "git -C $RemoteRunRoot/repo status --porcelain --untracked-files=all") { throw 'remote checkout is dirty' }
    Invoke-CheckedRemote "test ! -e $RemoteRunRoot/output" | Out-Null
    $specJson = (Invoke-CheckedRemote "cat $RemoteRunRoot/repo/protocols/workstream-e3a-v1/specification.json") -join "`n"
    try { $spec = $specJson | ConvertFrom-Json } catch { throw 'remote active specification JSON was invalid' }
    $requiredSpecStatus = if ($Phase -ceq 'pilot') { 'frozen' } else { 'shakedown-ready-not-frozen' }
    if (-not $spec -or $spec.status -cne $requiredSpecStatus -or $spec.execution_authorized -ne $true -or $spec.user_live_execution_approved -ne $true) {
        throw 'remote active specification gate failed'
    }
    Invoke-CheckedRemote "$RemoteRunRoot/venv/bin/python $RemoteRunRoot/repo/scripts/e3a_check.py" | Out-Null
    if ((Get-RemoteSha256 '/tmp/alf-e3a-native-build-zavnIH/codex-native-single-response' 'native binary') -cne $nativeSha256) { throw 'remote native binary identity mismatch' }
    if ((Get-RemoteSha256 '/tmp/alf-e3a-native-build-zavnIH/source-lf/codex-rs/models-manager/models.json' 'model catalog') -cne $catalogSha256) { throw 'remote model catalog identity mismatch' }
    $imageJson = ((Invoke-CheckedRemote 'docker image inspect 5d3e97d195dbbe7e47e47055e46f8c6f15fb9553be0c7ef19ed0060756fc7116') -join "`n").Trim()
    try { $image = $imageJson | ConvertFrom-Json } catch { throw 'remote Docker image inspect output was invalid' }
    if (-not $image -or @($image).Count -ne 1 -or $image[0].Id -cne $imageId) { throw 'remote Docker image identity mismatch' }

    $candidate = (Invoke-CheckedRemote 'mktemp -d /dev/shm/alf-e3a-auth-XXXXXX').Trim()
    if ($candidate -notmatch '^/dev/shm/alf-e3a-auth-[A-Za-z0-9]{6}$') { throw 'unexpected remote auth directory' }
    $remoteAuthRoot = $candidate
    Invoke-CheckedRemote "chmod 700 $remoteAuthRoot" | Out-Null
    & scp.exe @scpArgs -- $LocalAuthFile "$remoteHost`:$remoteAuthRoot/auth.json"
    if ($LASTEXITCODE -ne 0) { throw 'auth staging failed' }
    Invoke-CheckedRemote "chmod 600 $remoteAuthRoot/auth.json" | Out-Null

    $env:PATH = (Join-Path $repoRoot '.venv\Scripts') + [IO.Path]::PathSeparator + $oldPath
    $remoteCommand = "$RemoteRunRoot/venv/bin/python $RemoteRunRoot/repo/scripts/e3a_run.py --phase $Phase --native-binary /tmp/alf-e3a-native-build-zavnIH/codex-native-single-response --native-sha256 $nativeSha256 --model-catalog /tmp/alf-e3a-native-build-zavnIH/source-lf/codex-rs/models-manager/models.json --auth-file $remoteAuthRoot/auth.json --output $RemoteRunRoot/output"
    & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $launcherPath -EnvironmentProfilePath $profilePath -RemoteHost $remoteHost -RemoteSshPort 830 -RemoteCommand $remoteCommand
    $exitCode = $LASTEXITCODE
}
catch {
    $primaryError = $_; $exitCode = 1
    Write-Error -ErrorAction Continue ("primary $Phase failure: " + $_.Exception.Message)
}
finally {
    $env:PATH = $oldPath
    if ($remoteAuthRoot) {
        try {
            Invoke-CheckedRemote "rm -f $remoteAuthRoot/auth.json; rmdir $remoteAuthRoot" | Out-Null
            Invoke-CheckedRemote "test ! -e $remoteAuthRoot/auth.json && test ! -e $remoteAuthRoot" | Out-Null
            Write-Host 'remote auth cleanup: verified'
        } catch {
            $cleanupError = $_
            Write-Error -ErrorAction Continue ('remote auth cleanup failure: ' + $_.Exception.Message)
            if (-not $primaryError) { $exitCode = 1 }
        }
    }
    try {
        Invoke-CheckedRemote "test -e $RemoteRunRoot/output" | Out-Null
        & scp.exe @scpArgs -r "$remoteHost`:$RemoteRunRoot/output" $LocalOutputDirectory
        if ($LASTEXITCODE -ne 0) { throw 'retained output copy failed' }
        Write-Host 'remote output retention: copied'
    } catch {
        Write-Error -ErrorAction Continue ('remote output retention notice: ' + $_.Exception.Message)
        if (-not $primaryError) { $exitCode = 1 }
    }
    if ($transcriptStarted) {
        try { Stop-Transcript | Out-Null } catch { Write-Error -ErrorAction Continue ('transcript stop failure: ' + $_.Exception.Message) }
    }
}
if ($primaryError -or $cleanupError) { exit 1 }
exit $exitCode
