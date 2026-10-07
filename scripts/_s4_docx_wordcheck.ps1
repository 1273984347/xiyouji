# _s4_docx_wordcheck.ps1 — 一次性：Word COM 渲染统计（字符/词/页），供 B/C 轨 docx 复测
param([Parameter(ValueFromRemainingArguments = $true)][string[]]$Files)
$word = $null
try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0
    $rows = foreach ($f in $Files) {
        $doc = $word.Documents.Open($f, $false, $true)
        $o = [ordered]@{
            file    = (Split-Path $f -Leaf)
            chars   = $doc.ComputeStatistics(3)   # 字符数（不计空格）
            charsSp = $doc.ComputeStatistics(5)   # 字符数（计空格）
            words   = $doc.ComputeStatistics(0)   # 字数
            pages   = $doc.ComputeStatistics(2)   # 页数
        }
        $doc.Close($false)
        [pscustomobject]$o
    }
    $rows | Format-Table -AutoSize
}
finally {
    if ($word) { $word.Quit() }
}