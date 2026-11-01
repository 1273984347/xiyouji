<#
.SYNOPSIS
    agent-guardrails 改动面检查（Windows PowerShell 主力入口）。
.DESCRIPTION
    只检查本次改动涉及的 .py 文件，不追责存量：
      1) ruff（阻塞）：scripts/guardrails/ruff-structure.toml 宽档阈值
      2) 嵌套推导式（阻塞）：check_nested_comprehension.py（ruff 无对应规则）
      3) 一次性函数（提示）：once_call.py，只报告不阻断
      4) 公开 API 变化（提示）：api_diff.py，-Strict / -StrictApi 时阻断
.PARAMETER Strict
    收紧档（nested 3 / C901 12 / branches 12 / statements 60），API 破坏性变化判失败。
.PARAMETER StrictApi
    只把 api_diff 转阻断，阈值保持宽档（pre-commit 用）。
.PARAMETER All
    全仓扫描（CI / 批收尾用），忽略改动集（此模式跳过 api_diff：它对全仓逐文件跑 git show，代价过高）。
.PARAMETER Paths
    定向文件列表（排障 / CI 指定目标用）；缺省从 git 改动集取。
.EXAMPLE
    pwsh -File scripts/guardrails/check_changed.ps1
.EXAMPLE
    pwsh -File scripts/guardrails/check_changed.ps1 -Strict
.NOTES
    退出码：0 通过（或无可检查文件）；1 有阻断项；2 环境缺工具（ruff/Python 不可用）。
#>
param(
    [switch]$Strict,
    [switch]$StrictApi,
    [switch]$All,
    [string]$Root,
    [string[]]$Paths
)

$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

function Get-RepoRoot {
    param([string]$Explicit)
    if ($Explicit) { return (Resolve-Path -LiteralPath $Explicit).Path }
    $top = (& git rev-parse --show-toplevel 2>$null)
    if ($LASTEXITCODE -ne 0 -or -not $top) { throw "不在 git 仓库内：git rev-parse --show-toplevel 失败" }
    return $top.Trim()
}

function Get-Python {
    # 本机 PowerShell 侧 `python` 可能是应用执行存根（rc=9009），故 py -3 优先；与 .git/hooks/pre-commit 同口径。
    if (Get-Command py -ErrorAction SilentlyContinue) {
        & py -3 -c "import sys" *> $null
        if ($LASTEXITCODE -eq 0) { return @{ Exe = 'py'; Prefix = @('-3') } }
    }
    foreach ($name in @('python', 'python3')) {
        if (Get-Command $name -ErrorAction SilentlyContinue) {
            & $name -c "import sys" *> $null
            if ($LASTEXITCODE -eq 0) { return @{ Exe = $name; Prefix = @() } }
        }
    }
    return $null
}

function Get-Ruff {
    $cmd = Get-Command ruff -ErrorAction SilentlyContinue
    if ($cmd) { return @{ Exe = $cmd.Source; Prefix = @() } }
    return $null
}

function Invoke-Tool {
    param([hashtable]$Tool, [string[]]$ToolArgs, [string[]]$Files, [int]$Chunk = 100)
    $rc = 0
    for ($i = 0; $i -lt $Files.Count; $i += $Chunk) {
        $slice = $Files[$i..([Math]::Min($i + $Chunk - 1, $Files.Count - 1))]
        # Out-Host：让工具输出直接打到控制台，而不是混进函数返回值（否则返回值变成「输出+退出码」数组）。
        & $Tool.Exe @($Tool.Prefix + $ToolArgs + $slice) | Out-Host
        if ($LASTEXITCODE -ne 0) { $rc = $LASTEXITCODE }
    }
    return $rc
}

function Get-RepoFileList {
    param([string]$RepoRoot)
    $tracked = & git -C $RepoRoot -c core.quotepath=false ls-files -- '*.py'
    return @($tracked | Where-Object { $_ })
}

function Get-ChangedPyFiles {
    param([string]$RepoRoot)
    $diff = & git -C $RepoRoot -c core.quotepath=false diff --name-only HEAD 2>$null
    $new = & git -C $RepoRoot -c core.quotepath=false ls-files --others --exclude-standard
    $names = @($diff) + @($new) | Where-Object { $_ }
    return @($names | Sort-Object -Unique)
}

# ---------------------------------------------------------------- 主流程
try { $repo = Get-RepoRoot -Explicit $Root } catch { Write-Host "[FAIL] $($_.Exception.Message)"; exit 2 }
Set-Location -LiteralPath $repo

$python = Get-Python
$ruff = Get-Ruff
if (-not $python) { Write-Host "[FAIL] 找不到可运行的 Python（py -3 / python / python3 均不可用）"; exit 2 }
if (-not $ruff) {
    # 兜底：ruff 作为 Python 模块调用（若已 pip 安装）。
    & $python.Exe @($python.Prefix + @('-m', 'ruff', '--version')) *> $null
    if ($LASTEXITCODE -eq 0) { $ruff = @{ Exe = $python.Exe; Prefix = @($python.Prefix + @('-m', 'ruff')) } }
}
if (-not $ruff) {
    Write-Host "[FAIL] 找不到 ruff（ruff 未安装且 python -m ruff 不可用）。安装：py -3 -m pip install ruff"
    exit 2
}

if ($Paths) {
    $candidates = @($Paths)
    $mode = '定向'
} elseif ($All) {
    $candidates = Get-RepoFileList -RepoRoot $repo
    $mode = '全仓'
} else {
    $candidates = Get-ChangedPyFiles -RepoRoot $repo
    $mode = '改动集'
}

$pyFiles = @($candidates | Where-Object { $_ -match '\.py$' -and (Test-Path -LiteralPath (Join-Path $repo $_)) } | Sort-Object -Unique)
if (-not $Paths) {
    # 与根 pyproject.toml 的 `**/_*.py` 豁免一致：一次性/诊断脚本不参与门禁。
    # 定向模式（-Paths）不豁免：那是用户明确点名的文件。
    $pyFiles = @($pyFiles | Where-Object { -not ((Split-Path -Leaf $_).StartsWith('_')) })
    # tmpe/ 是 gitignored 的临时脚本区，永远不进门禁（否则历史脚本会刷屏噪声）。
    $pyFiles = @($pyFiles | Where-Object { -not ($_ -like 'tmpe/*') })
}
$skipped = @($candidates).Count - $pyFiles.Count

if ($pyFiles.Count -eq 0) {
    Write-Host "[SKIP] 本次改动没有可检查的 .py 文件（非 Python / 已删除文件 $skipped 个），无阻断项。"
    Write-Host "[SKIP] 非 Python 改动请另跑：py -3 scripts/generate_csp.py --check / py -3 scripts/verify_delivery.py --scope auto"
    exit 0
}

Write-Host "== check_changed（$mode）：$($pyFiles.Count) 个 .py 文件 =="

# 1) 项目风格/语法档（显式指向根 pyproject.toml，与 CI 同源；阻塞）
#    显式 --config 是为了避开 ruff 对子目录内 ruff.toml 的发现：否则 scripts/guardrails/ 下的文件
#    会被结构档配置接管，风格档结论就与 CI 不一致。
$rootCfg = Join-Path $repo 'pyproject.toml'
$rcStyle = Invoke-Tool -Tool $ruff -ToolArgs @('check', '--config', $rootCfg, '--output-format', 'concise', '--no-cache') -Files $pyFiles
Write-Host "[$(if ($rcStyle -eq 0) { 'OK' } else { 'FAIL' })] ruff 风格档（根 pyproject.toml，CI 同源）"

# 2) 结构档（scripts/guardrails/ruff-structure.toml；阻塞）
#    文件名刻意不用 ruff.toml：ruff 只自动发现 ruff.toml/.ruff.toml/pyproject.toml，
#    改成 ruff-structure.toml 后它不会介入任何常规 `ruff check .`，只由本脚本显式加载。
$cfg = Join-Path $repo 'scripts/guardrails/ruff-structure.toml'
$ruffArgs = @('check', '--config', $cfg, '--output-format', 'concise', '--no-cache')
if ($Strict) {
    $ruffArgs += @(
        '--config', 'lint.mccabe.max-complexity=12',
        '--config', 'lint.pylint.max-nested-blocks=3',
        '--config', 'lint.pylint.max-branches=12',
        '--config', 'lint.pylint.max-statements=60'
    )
}
$rcRuff = Invoke-Tool -Tool $ruff -ToolArgs $ruffArgs -Files $pyFiles
Write-Host "[$(if ($rcRuff -eq 0) { 'OK' } else { 'FAIL' })] ruff 结构档（$(if ($Strict) { '收紧档' } else { '宽档' })阈值）"

# 3) 嵌套推导式（阻塞）
$compArgs = @('scripts/guardrails/check_nested_comprehension.py')
$rcComp = Invoke-Tool -Tool $python -ToolArgs $compArgs -Files $pyFiles
Write-Host "[$(if ($rcComp -eq 0) { 'OK' } else { 'FAIL' })] 嵌套推导式检查"

# 4) 一次性函数（提示，不阻断）
$onceArgs = @('scripts/guardrails/once_call.py')
Invoke-Tool -Tool $python -ToolArgs $onceArgs -Files $pyFiles | Out-Null
Write-Host "[INFO] once_call（只报告，不计入阻断；判据见 self-check.md 第 1 条）"

# 5) 公开 API 变化（提示；-Strict 阻断；全仓模式跳过）
if ($All) {
    Write-Host "[SKIP] api_diff（全仓模式不跑逐文件 git show）"
    $rcApi = 0
} else {
    $apiArgs = @('scripts/guardrails/api_diff.py')
    if ($Strict -or $StrictApi) { $apiArgs += '--strict' }
    $rcApi = Invoke-Tool -Tool $python -ToolArgs $apiArgs -Files $pyFiles
    Write-Host "[$(if ($rcApi -eq 0) { 'OK' } else { 'FAIL' })] 公开 API 变化（$(if ($Strict -or $StrictApi) { '阻断' } else { '提示' })）"
}

$failed = @($rcStyle, $rcRuff, $rcComp, $rcApi) | Where-Object { $_ -ne 0 }
if ($failed.Count -gt 0) {
    Write-Host "== 结论：有阻断项，请修到 0 再提交 =="
    exit 1
}
Write-Host "== 结论：通过（提示类输出不阻断）=="
exit 0
