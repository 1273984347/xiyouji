"""三篇国内新 PDF 的许可线索探测（2026-10-05·一次性脚本）。"""
import logging
import os
import re

logging.disable(logging.CRITICAL)
DEST = r"d:\xiyouji\docs\S4-学术投稿\06-文献"
FILES = [
    "2026_Li-Su-Zhou_中国科技期刊AI使用政策研究_科技与出版2026-2.pdf",
    "2025_Liu_文学情感计算的五大方向及其问题_中国比较文学2025-2.pdf",
    "2025_Bao_AI类主体与文艺批评话语范式转型_首都师范大学学报【页面转存版】.pdf",
]
from pypdf import PdfReader

for f in FILES:
    p = os.path.join(DEST, f)
    r = PdfReader(p)
    print("=====", f, "|", len(r.pages), "页")
    txt = ""
    for i in [0, len(r.pages) - 1]:
        txt += (r.pages[i].extract_text() or "") + "\n"
    hits = re.findall(r"(?i)(creative commons[^\n]{0,90}|CC[ -]BY[^\n]{0,60}|open access[^\n]{0,60}|版权[^\n]{0,60}|许可[^\n]{0,60}|DOI[^\n]{0,40})", txt)
    print("  线索:", hits[:6] if hits else "无")
    # 首页头部 200 字
    t0 = re.sub(r"\s+", " ", (r.pages[0].extract_text() or ""))
    print("  首页头:", t0[:200])
