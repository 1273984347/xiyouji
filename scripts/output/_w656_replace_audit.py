#!/usr/bin/env python3
"""W656 临时脚本：85 页六族 audit 补丁块 → 单块 chart-audit 内联（按页家族集保留时序）

输出触达文件清单 scripts/output/_cascade_files_W656_pages.txt（W654 教训：非级联批量页
改动必须自带清单供 git add）。--check 只报差异不写盘。
"""
import re
import sys
from pathlib import Path

ROOT = Path(".").resolve()
SITE_DATA = ROOT / "site" / "data"
MODULE = (ROOT / "site" / "static" / "js" / "chart-audit.js").read_text(encoding="utf-8")
SKIP = {"_shell", "_template"}

# 原块 id → 家族键（audit-axisfix2/3 → axesvar 同键·运行时去重）
ID2KEY = {
    "audit-axisfix": "axisfix",
    "audit-axisfix2": "axesvar",
    "audit-axisfix3": "axesvar",
    "audit-axisfix4": "numfix",
    "audit-labelavoid": "netlabels",
    "audit-labelavoid-all": "avoidall",
    "audit-contentavoid": "content",
}
# 家族键出现顺序（保持原脚本块顺序语义·axesvar 只保留首次）
ORDER = ["axisfix", "axesvar", "avoidall", "numfix", "netlabels", "content"]

RE_BLOCK = re.compile(r'[ \t]*<script id="audit-[^"]+">[\s\S]*?</script>\n?')

check_only = "--check" in sys.argv
touched, report = [], []
for p in sorted(SITE_DATA.glob("*.html")):
    if p.stem in SKIP:
        continue
    s = p.read_text(encoding="utf-8", errors="ignore")
    blocks = list(re.finditer(r'<script id="(audit-[^"]+)">', s))
    if not blocks:
        continue
    keys = []
    for m in blocks:
        k = ID2KEY.get(m.group(1))
        if k and k not in keys:
            keys.append(k)
    keys.sort(key=ORDER.index)
    new_block = (
        '<script id="chart-audit">\n'
        "/* chart-audit.js（源 site/static/js/chart-audit.js · B-9① W656 六族合并·内联副本勿手改） */\n"
        + MODULE
        + "ChartAudit.run(" + repr(keys).replace("'", '"') + ");\n"
        + "</script>\n"
    )
    s2, n = RE_BLOCK.subn("", s)
    # 插到第一个原块位置（原第一块起点前的缩进已随块删除——在其原行位置回插）
    first = blocks[0]
    # 计算第一块在删除后文本中的近似位置：用第一块之前的原文长度不变
    head = s[: RE_BLOCK.search(s).start()]
    s2 = head + new_block + s2[len(head):]
    if check_only:
        report.append(f"{p.name}: {len(blocks)} 块 → 1 块（{'+'.join(keys)}）")
        continue
    p.write_text(s2, encoding="utf-8", newline="")
    touched.append(str(p.relative_to(ROOT)).replace("\\", "/"))
    report.append(f"{p.name}: {len(blocks)} 块 → 1 块（{'+'.join(keys)}）")

for line in report:
    print(line)
manifest = ROOT / "scripts" / "output" / "_cascade_files_W656_pages.txt"
manifest.write_text("\n".join(touched) + "\n", encoding="utf-8")
print(f"--- {len(touched)} 页触达 · 清单 → {manifest.relative_to(ROOT)}{'（check 未写盘）' if check_only else ''}")
