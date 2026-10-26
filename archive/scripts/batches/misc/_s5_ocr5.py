"""5 份扫描件 OCR：PyMuPDF 渲染 → Windows 自带 OCR → md（质量声明在头）"""
import io
import os
import re
import subprocess
import sys
import fitz

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

LIT = r'D:\xiyouji\docs\S4-学术投稿\06-文献'
OUT = os.path.join(LIT, 'md')
TMP = r'D:\xiyouji\tmpe\ocr'
os.makedirs(TMP, exist_ok=True)
PS = r'D:\xiyouji\tmpe\_win_ocr.ps1'

FILES = [
    '2021_Ren-Li-Liu_中华传统家谱数据可视化研究_数字人文研究1-4.pdf',
    '2022_Hou-Yang-Wang_近代黄河流域邮政网络重建_数字人文研究2-1.pdf',
    '2023_Deng-Jia_传统服饰纹样元与源_艺术设计研究2023-5.pdf',
    '2023_Wang-Li_文化数字化遗产可持续传承_艺术设计研究2023-1.pdf',
    '2023_Xu-Zhou_苗族百褶裙纹样符号解读_艺术设计研究2023-5.pdf',
]

def clean(s):
    # 去掉 CJK 字符之间的空格；保留英文/数字间空格
    s = re.sub(r'(?<=[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef])\s+(?=[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef])', '', s)
    return s

only = sys.argv[1] if len(sys.argv) > 1 else None
for f in FILES:
    if only and only not in f:
        continue
    out = os.path.join(OUT, f[:-4] + '.md')
    if os.path.exists(out):
        print('skip(已有):', f[:40])
        continue
    d = fitz.open(os.path.join(LIT, f))
    parts = [f'# {f[:-4]}', '',
             f'> 来源：{f} · 共 {len(d)} 页 · **OCR 稿**（Windows 自带识别引擎·2026-10-08）',
             '> ⚠️ 质量声明：扫描件 OCR，错字/漏字显著多于文本层抽取，仅供检索定位；引用请以原 PDF 为准。', '']
    for i, page in enumerate(d, 1):
        png = os.path.join(TMP, f'{f[:6]}_p{i}.png')
        page.get_pixmap(dpi=150).save(png)
        r = subprocess.run(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass',
                            '-File', PS, '-ImagePath', png],
                           capture_output=True, text=True, timeout=120)
        txt = r.stdout.strip()
        if r.returncode != 0 or txt.startswith('[[NO-ENGINE]]') or txt.startswith('[[OCR-ERROR]]'):
            txt = f'（第 {i} 页 OCR 失败：{txt[:60]}）'
        parts.append(f'\n\n<!-- 第 {i} 页 -->\n\n' + clean(txt))
        os.remove(png)
        print(f'  {f[:24]} p{i}/{len(d)} ({len(txt)} chars)')
    open(out, 'w', encoding='utf-8', newline='').write(''.join(parts))
    print('DONE:', f[:40])
print('ALL FINISHED')
