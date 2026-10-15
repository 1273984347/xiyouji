$files = @(
  "D:\xiyouji\docs\S4-学术投稿\01-论文\可验证性方向-投稿版.docx",
  "D:\xiyouji\docs\S4-学术投稿\05-投稿\数字人文研究投稿\可验证性方向-数字人文研究适配版.docx"
)
$word = New-Object -ComObject Word.Application
$word.Visible = $false
foreach ($f in $files) {
  $doc = $word.Documents.Open($f, $false, $true)
  $pages = $doc.ComputeStatistics(2)
  $words = $doc.ComputeStatistics(0)
  Write-Output ("{0} | pages={1} words={2}" -f (Split-Path $f -Leaf), $pages, $words)
  $doc.Close($false)
}
$word.Quit()
