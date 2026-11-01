param(
    [string]$Root
)

# install_hooks.ps1 — install_hooks.sh 的薄封装（不复制任何安装逻辑）
$ErrorActionPreference = 'Stop'

$gitBash = 'C:\Program Files\Git\bin\bash.exe'
if (Test-Path -LiteralPath $gitBash) {
    $sh = $gitBash
} else {
    $cmd = Get-Command bash -ErrorAction SilentlyContinue
    if (-not $cmd) { throw '找不到 bash（Git for Windows 或 WSL 均可）' }
    $sh = $cmd.Source
}

$script = Join-Path $PSScriptRoot 'install_hooks.sh'
if ($Root) {
    & $sh $script $Root
} else {
    & $sh $script
}
exit $LASTEXITCODE
