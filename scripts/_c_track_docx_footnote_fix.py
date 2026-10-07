# 一次性脚本：C 轨 docx 脚注编号补丁（①②③圈号·连续编号）+ 结构验收（不入库门禁）
# 2026-10-07 review 修正：Word 实渲染无视 settings.xml 注入的 numFmt（COM 实探 NumberStyle=0·阿拉伯），
# 故补丁后追加 Word COM 强制步（NumberStyle=58 wdNoteNumberStyleArabicEnclosedCircle）；
# 每页重排（numRestart eachPage）撤除——连续编号下「同注 N」的 N 才保持可解析。
import re
import shutil
import subprocess
import zipfile

DOCX = r'D:\xiyouji\docs\S4-学术投稿\01-论文\可验证性方向-投稿版.docx'
TMP = DOCX + '.tmp'

with zipfile.ZipFile(DOCX, 'r') as z:
    names = z.namelist()
    settings = z.read('word/settings.xml').decode('utf-8')
    document = z.read('word/document.xml').decode('utf-8')
    footnotes = z.read('word/footnotes.xml').decode('utf-8') if 'word/footnotes.xml' in names else ''
    media = [n for n in names if n.startswith('word/media/')]

# settings.xml 注入脚注编号格式（①②③）·连续编号——CT_Settings 为 sequence，
# footnotePr 须位于 compat 之前（插在开标签后会被 Word 判「文件可能已经损坏」）
if 'footnotePr' not in settings:
    inject = '<w:footnotePr><w:numFmt w:val="decimalEnclosedCircle"/><w:numRestart w:val="continuous"/></w:footnotePr>'
    if '<w:compat>' in settings:
        settings = settings.replace('<w:compat>', inject + '<w:compat>', 1)
    else:
        settings = settings.replace('</w:settings>', inject + '</w:settings>', 1)

with zipfile.ZipFile(DOCX, 'r') as zin, zipfile.ZipFile(TMP, 'w', zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        if item.filename == 'word/settings.xml':
            zout.writestr(item, settings)
        else:
            zout.writestr(item, zin.read(item.filename))
shutil.move(TMP, DOCX)

media_files = [n for n in media if n != 'word/media/']
n_refs = len(re.findall(r'<w:footnoteReference[^>]*>', document))
ok_refs = n_refs == 20  # 2026-10-07 增引 HALLMARK 并入注⑧定义（独立脚注会使总数 21·超出圈号字形域①—⑳）
ok_defs = len([m for m in re.finditer(r'<w:footnote [^>]*w:id="(\d+)"', footnotes)
               if int(m.group(1)) >= 1]) == n_refs  # 引用与定义 1:1（含同注条目）
ok_media = len(media_files) == 4

# Word COM 强制步：settings.xml 注入的 numFmt 曾被 Word 实渲染无视——由 Word 自身写入并回读断言。
# 圈号枚举 = wdNoteNumberStyleNumberInCircle(18)（WdNoteNumberStyle 官方表无「ArabicEnclosedCircle」；
# 58 会写成 russianLower 西里尔小写——2026-10-07 二犯实证，枚举值必须取自官方表）
PS = """param([string]$Path)
$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
  $doc = $word.Documents.Open($Path, $false, $false)
  $doc.Footnotes.NumberStyle = 18
  $doc.Footnotes.NumberingRule = 0
  $doc.Save()
  $s = $doc.Footnotes.NumberStyle
  $r = $doc.Footnotes.NumberingRule
  $doc.Close($false)
  Write-Output "STYLE=$s RULE=$r"
} finally { $word.Quit() }
"""
ps_path = r'D:\xiyouji\tmpe\_c_track_set_footnote_style.ps1'
with open(ps_path, 'w', encoding='ascii') as f:
    f.write(PS)
r = subprocess.run(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass',
                    '-File', ps_path, '-Path', DOCX], capture_output=True, text=True, timeout=300)
m = re.search(r'STYLE=(\d+) RULE=(\d+)', r.stdout)
ok_com = bool(m) and m.group(1) == '18' and m.group(2) == '0'

print(f'footnoteReference in body: {n_refs} (期望 20·37=20行内+17定义) -> {"OK" if ok_refs else "FAIL"}')
print(f'footnote defs (id>=1): 17 -> {"OK" if ok_defs else "FAIL"}')
print(f'media images: {len(media_files)} (期望 4) -> {"OK" if ok_media else "FAIL"}')
print(f'COM 圈号强制步 (期望回读 STYLE=18 RULE=0): {r.stdout.strip() or r.stderr.strip()[:200]} -> {"OK" if ok_com else "FAIL"}')
print('RESULT:', 'PASS' if all([ok_refs, ok_defs, ok_media, ok_com]) else 'FAIL')
