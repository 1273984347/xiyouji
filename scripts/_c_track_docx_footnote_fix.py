# 一次性脚本：C 轨 docx 脚注编号补丁（①②③·每页重排）+ 结构验收（不入库门禁）
import re
import shutil
import zipfile

DOCX = r'D:\xiyouji\docs\S4-学术投稿\学术论文C轨-可验证性基础设施-投稿版.docx'
TMP = DOCX + '.tmp'

with zipfile.ZipFile(DOCX, 'r') as z:
    names = z.namelist()
    settings = z.read('word/settings.xml').decode('utf-8')
    document = z.read('word/document.xml').decode('utf-8')
    footnotes = z.read('word/footnotes.xml').decode('utf-8') if 'word/footnotes.xml' in names else ''
    media = [n for n in names if n.startswith('word/media/')]

# settings.xml 注入脚注编号格式（①②③）与每页重排——CT_Settings 为 sequence，
# footnotePr 须位于 compat 之前（插在开标签后会被 Word 判「文件可能已经损坏」）
if 'footnotePr' not in settings:
    inject = '<w:footnotePr><w:numFmt w:val="decimalEnclosedCircle"/><w:numRestart w:val="eachPage"/></w:footnotePr>'
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
ok_refs = n_refs == 20
ok_defs = len([m for m in re.finditer(r'<w:footnote [^>]*w:id="(\d+)"', footnotes)
               if int(m.group(1)) >= 1]) == n_refs  # 引用与定义 1:1（含同注条目）
ok_media = len(media_files) == 4
ok_set = 'decimalEnclosedCircle' in settings and 'eachPage' in settings
print(f'footnoteReference in body: {n_refs} (期望 20·37=20行内+17定义) -> {"OK" if ok_refs else "FAIL"}')
print(f'footnote defs (id>=1): 17 -> {"OK" if ok_defs else "FAIL"}')
print(f'media images: {len(media_files)} (期望 4) -> {"OK" if ok_media else "FAIL"}')
print(f'settings 补丁(①②③+每页重排): {"OK" if ok_set else "FAIL"}')
print('RESULT:', 'PASS' if all([ok_refs, ok_defs, ok_media, ok_set]) else 'FAIL')
