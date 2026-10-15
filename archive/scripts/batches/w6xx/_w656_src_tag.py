#!/usr/bin/env python3
"""W656 临时脚本（v2）：84 页 chart-audit 内联大块 → 1 行 defer src + data-families
（d3 同款 src 形态·file:// 与 Pages 双态验证可行·vis-tools 内联注释系历史遗留）
输出触达清单 scripts/output/_cascade_files_W656_pages.txt。"""
import re
from pathlib import Path

ROOT = Path(".").resolve()
SITE_DATA = ROOT / "site" / "data"
SKIP = {"_shell", "_template"}
ORDER = ["axisfix", "axesvar", "avoidall", "numfix", "netlabels", "content"]

RE_INLINE = re.compile(
    r'[ \t]*<script id="chart-audit">[\s\S]*?ChartAudit\.run\(\[([^\]]*)\]\);[\s\S]*?</script>\n?'
)

touched = []
for p in sorted(SITE_DATA.glob("*.html")):
    if p.stem in SKIP:
        continue
    s = p.read_text(encoding="utf-8", errors="ignore")
    m = RE_INLINE.search(s)
    if not m:
        continue
    keys = [k.strip().strip('"') for k in m.group(1).split(",") if k.strip()]
    keys.sort(key=ORDER.index)
    tag = '<script id="chart-audit" defer src="../static/js/chart-audit.js" data-families="' + ",".join(keys) + '"></script>\n'
    s2 = s[: m.start()] + tag + s[m.end():]
    p.write_text(s2, encoding="utf-8", newline="")
    touched.append(str(p.relative_to(ROOT)).replace("\\", "/"))

manifest = ROOT / "scripts" / "output" / "_cascade_files_W656_pages.txt"
manifest.write_text("\n".join(touched) + "\n", encoding="utf-8")
print(f"{len(touched)} 页 → 1 行 defer src（data-families 传参）· 清单已更新")
