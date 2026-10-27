"""06-文献 PDF → markdown 批量抽取（PyMuPDF 文本层·扫描件如实标记）"""
import io
import os
import sys
import fitz

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

LIT = r'D:\xiyouji\docs\S4-学术投稿\06-文献'
OUT = os.path.join(LIT, 'md')
os.makedirs(OUT, exist_ok=True)
today = '2026-10-08'

pdfs = sorted(f for f in os.listdir(LIT) if f.lower().endswith('.pdf'))
ok, empty, fail = [], [], []
for f in pdfs:
    src = os.path.join(LIT, f)
    out = os.path.join(OUT, f[:-4] + '.md')
    try:
        d = fitz.open(src)
        parts = [f'# {f[:-4]}', '',
                 f'> 来源：{f} · 共 {len(d)} 页 · 文本层抽取 PyMuPDF {fitz.__doc__.split()[1] if fitz.__doc__ else ""} · {today}',
                 '> 说明：机器抽取稿，供检索与速读；引文核对以原 PDF 为准。扫描件/公式表格可能有损。', '']
        total = 0
        for i, page in enumerate(d, 1):
            txt = page.get_text('text').strip()
            total += len(txt)
            parts.append(f'\n\n<!-- 第 {i} 页 -->\n\n{txt}')
        if total < 200:
            empty.append(f'{f}（文本层 {total} 字符·疑扫描件）')
            continue
        open(out, 'w', encoding='utf-8', newline='').write(''.join(parts))
        ok.append(f)
    except Exception as e:
        fail.append(f'{f}: {str(e)[:80]}')

print(f'抽取成功 {len(ok)} · 疑扫描件/空文本 {len(empty)} · 失败 {len(fail)}')
for e in empty:
    print('  [扫描?]', e)
for f_ in fail:
    print('  [失败]', f_)
print('输出目录:', OUT)
