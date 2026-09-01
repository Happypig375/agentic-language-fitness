[CmdletBinding()]
param(
    [Parameter(Mandatory)] [string] $RemoteHost,
    [Parameter(Mandatory)] [string] $RemoteCommand,
    [Parameter(Mandatory)] [string] $EnvironmentProfilePath,
    [int] $RemoteSshPort = 22,
    [string] $IdentityFile,
    [string] $KnownHostsFile,
    [int] $StartupTimeoutSeconds = 15
)

$ErrorActionPreference = 'Stop'
function Assert-Safe([string] $Value, [string] $Name) {
    if ([string]::IsNullOrWhiteSpace($Value) -or $Value.Contains("`r") -or $Value.Contains("`n") -or $Value.Contains([char]0)) { throw "$Name contains unsafe characters" }
}
Assert-Safe $RemoteHost 'RemoteHost'; Assert-Safe $RemoteCommand 'RemoteCommand'; Assert-Safe $EnvironmentProfilePath 'EnvironmentProfilePath'
if ($RemoteHost -notmatch '^(?:[A-Za-z0-9_][A-Za-z0-9._-]*@)?[A-Za-z0-9][A-Za-z0-9.-]*$') { throw 'RemoteHost must be a plain host or user@host' }
if ($RemoteCommand -notmatch '^[A-Za-z0-9_./:=,@%+-]+(?: [A-Za-z0-9_./:=,@%+-]+)*$') { throw 'RemoteCommand must be a fixed command with simple arguments' }
foreach ($path in @($EnvironmentProfilePath, $IdentityFile, $KnownHostsFile)) {
    if ($path) {
        Assert-Safe $path 'SSH path'
        if ($path.Contains('"')) { throw 'SSH paths contain unsafe quoting characters' }
        if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw "SSH path is not a file: $path" }
    }
}

$EnvironmentProfilePath = (Resolve-Path -LiteralPath $EnvironmentProfilePath).Path
$TrackedEnvironmentProfilePath = (Resolve-Path -LiteralPath "$PSScriptRoot\environment-profile.json").Path
if (-not [string]::Equals($EnvironmentProfilePath, $TrackedEnvironmentProfilePath, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw 'EnvironmentProfilePath must be the tracked remote-runner profile'
}
try { $profile = Get-Content -LiteralPath $EnvironmentProfilePath -Raw -Encoding UTF8 | ConvertFrom-Json }
catch { throw "EnvironmentProfilePath is not valid JSON: $($_.Exception.Message)" }
if (
    $profile.schema_version -ne 1 -or
    $profile.docker_network.internal -ne $true -or
    $profile.connect_proxy.local_bind -ne '127.0.0.1' -or
    $profile.connect_proxy.allowed_authority -ne 'chatgpt.com:443' -or
    $profile.connect_proxy.tls -ne 'passthrough' -or
    $profile.ssh.forward -ne 'fixed-reverse' -or
    $profile.ssh.owns_remote_command -ne $true -or
    $profile.ssh.ambient_config -ne $false -or
    $profile.authentication.cache -ne 'complete-ephemeral-writable' -or
    $profile.authentication.cleanup -ne 'required'
) { throw 'Environment profile does not describe the supported route' }
$RemoteBridgeAddress = "$($profile.docker_network.bridge_gateway)"
if ($RemoteBridgeAddress -notmatch '^(25[0-5]|2[0-4][0-9]|1?[0-9]{1,2})(\.(25[0-5]|2[0-4][0-9]|1?[0-9]{1,2})){3}$') { throw 'Environment profile bridge_gateway must be IPv4' }
function Convert-ProfilePort($Value, [string] $Name) {
    if ($Value -is [bool] -or "$Value" -notmatch '^\d{1,5}$') { throw "$Name is not an integer port" }
    $port = [int]$Value
    if ($port -lt 1 -or $port -gt 65535) { throw "$Name out of range" }
    return $port
}
$RemoteProxyPort = Convert-ProfilePort $profile.connect_proxy.remote_port 'environment remote_port'
$LocalProxyPort = Convert-ProfilePort $profile.connect_proxy.local_port 'environment local_port'
if ($RemoteSshPort -lt 1 -or $RemoteSshPort -gt 65535) { throw 'RemoteSshPort out of range' }
if ($StartupTimeoutSeconds -lt 1 -or $StartupTimeoutSeconds -gt 300) { throw 'StartupTimeoutSeconds out of range' }

function Join-NativeArguments([string[]] $Values) {
    # Windows PowerShell 5.1 joins Start-Process arguments into one command line.
    # Quote whitespace-bearing values explicitly; quote characters were rejected above.
    return (($Values | ForEach-Object {
        if ($_ -match '[\s"]') { '"' + $_ + '"' } else { $_ }
    }) -join ' ')
}

$proxy = $null; $ssh = $null
$readyPath = Join-Path ([System.IO.Path]::GetTempPath()) ("alf-connect-proxy-{0}.ready" -f [Guid]::NewGuid().ToString('N'))
$readyTempPath = $null
try {
    # A venv's `python` command may be a redirector whose PID differs from the
    # interpreter process that writes connect_proxy.py's readiness owner.
    $pythonProbe = @(& python -c 'import sys; print(sys._base_executable or sys.executable)')
    if ($LASTEXITCODE -ne 0 -or $pythonProbe.Count -ne 1 -or [string]::IsNullOrWhiteSpace($pythonProbe[0])) {
        throw 'could not resolve the base Python executable'
    }
    $pythonExecutable = $pythonProbe[0].Trim()
    if (-not (Test-Path -LiteralPath $pythonExecutable -PathType Leaf)) {
        throw "base Python executable is not an existing file: $pythonExecutable"
    }
    $pythonExecutable = (Resolve-Path -LiteralPath $pythonExecutable).Path
    $proxyArgs = Join-NativeArguments @('-u', "$PSScriptRoot\connect_proxy.py", '--port', "$LocalProxyPort", '--ready-file', $readyPath)
    $proxy = Start-Process -FilePath $pythonExecutable -ArgumentList $proxyArgs -PassThru -WindowStyle Hidden
    $readyTempPath = "$readyPath.$($proxy.Id).tmp"
    $deadline = (Get-Date).AddSeconds($StartupTimeoutSeconds)
    $ownedReady = $false
    do {
        if ($proxy.HasExited) { throw "proxy exited with $($proxy.ExitCode)" }
        if (Test-Path -LiteralPath $readyPath -PathType Leaf) {
            $owner = (Get-Content -LiteralPath $readyPath -Raw -Encoding ASCII).Trim()
            if ($owner -ne "$($proxy.Id)") { throw 'proxy readiness owner does not match the launched process' }
            $ownedReady = $true
        }
        if (-not $ownedReady) { Start-Sleep -Milliseconds 100 }
    } while (-not $ownedReady -and (Get-Date) -lt $deadline)
    if (-not $ownedReady) { throw 'proxy did not publish readiness before timeout' }

    $ready = $false
    do {
        if ($proxy.HasExited) { throw "proxy exited with $($proxy.ExitCode)" }
        $client = New-Object System.Net.Sockets.TcpClient
        $waitHandle = $null
        try {
            $async = $client.BeginConnect('127.0.0.1', $LocalProxyPort, $null, $null)
            $waitHandle = $async.AsyncWaitHandle
            $ready = $waitHandle.WaitOne(100)
            if ($ready) { $client.EndConnect($async) }
        }
        catch [System.Net.Sockets.SocketException] { $ready = $false }
        finally {
            if ($waitHandle) { $waitHandle.Close() }
            $client.Close()
        }
        if (-not $ready) { Start-Sleep -Milliseconds 100 }
    } while (-not $ready -and (Get-Date) -lt $deadline)
    if (-not $ready) { throw 'proxy did not become ready before timeout' }
    $sshArgs = @('-F','none','-T','-n','-o','BatchMode=yes','-o','IdentitiesOnly=yes','-o','StrictHostKeyChecking=yes','-o','ExitOnForwardFailure=yes','-o','ServerAliveInterval=30','-o','ServerAliveCountMax=3','-o','ForwardAgent=no','-o','RequestTTY=no')
    $sshArgs += @('-p', $RemoteSshPort)
    if ($IdentityFile) { $sshArgs += @('-i', (Resolve-Path -LiteralPath $IdentityFile).Path) }
    if ($KnownHostsFile) { $sshArgs += @('-o', "UserKnownHostsFile=$((Resolve-Path -LiteralPath $KnownHostsFile).Path)") }
    $sshArgs += @('-R', "$RemoteBridgeAddress`:$RemoteProxyPort`:127.0.0.1`:$LocalProxyPort", $RemoteHost, $RemoteCommand)
    $ssh = Start-Process -FilePath ssh.exe -ArgumentList (Join-NativeArguments $sshArgs) -Wait -PassThru -NoNewWindow
    exit $ssh.ExitCode
} finally {
    if ($ssh -and -not $ssh.HasExited) { Stop-Process -Id $ssh.Id -Force -ErrorAction SilentlyContinue; $ssh.WaitForExit() }
    if ($proxy -and -not $proxy.HasExited) { Stop-Process -Id $proxy.Id -Force -ErrorAction SilentlyContinue; $proxy.WaitForExit() }
    foreach ($path in @($readyPath, $readyTempPath)) {
        if ($path -and (Test-Path -LiteralPath $path)) { Remove-Item -LiteralPath $path -Force -ErrorAction SilentlyContinue }
    }
}
