#!/usr/bin/env python3
"""_w864_accent_audit.py — W864 B2 朱砂落点审计（朱砂文字 + 朱砂实底·一次性件）。

两把尺子（都按计算样式量·不目测）：
1. **朱砂文字落 --bg**（裁决 1 修法）：color == 浅色朱砂 且有效背景解析到 --bg
   → 改 `--accent-text`；
2. **朱砂实底**（裁决 2）：背景色 == 朱砂且面积 >400px²，或 top 边框色 == 朱砂
   且宽 ≥2px 且面积 >400px²（KPI 顶条形态——现役最常见实现）→ 每页计数须 ≤3。

产出：scripts/output/_w864_accent_audit.json
"""

import json
import os
import sys

from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
OUT = os.path.join(ROOT, "scripts", "output", "_w864_accent_audit.json")

DEFAULT_PAGES = [
    "data/chapter-structure-graph.html", "data/chapter-stats.html",
    "data/story-timeline.html", "data/timeline.html",
    "data/relationships.html", "data/81-hardships.html",
    "data/81-hardships-view.html", "data/hardship-heatmap.html",
    "data/hardship-difficulty-heatmap.html", "data/methodology-matrix.html",
]

AUDIT_JS = """
() => {
  const ACCENT = 'rgb(200, 70, 58)';
  const BG = 'rgb(250, 247, 240)';
  const transparent = (c) => c === 'rgba(0, 0, 0, 0)' || c === 'transparent';
  const out = {text_on_bg: [], fill: []};
  for (const el of document.querySelectorAll('*')) {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') continue;
    const r = el.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) continue;
    // 1) 朱砂文字落 bg
    if (cs.color === ACCENT) {
      let bg = null, node = el;
      while (node && node.nodeType === 1) {
        const b = getComputedStyle(node).backgroundColor;
        if (!transparent(b)) { bg = b; break; }
        node = node.parentElement;
      }
      if (bg === null || bg === BG) {
        out.text_on_bg.push({tag: el.tagName.toLowerCase(),
          cls: el.getAttribute('class') || '',
          txt: (el.textContent || '').replace(/\\s+/g, ' ').trim().slice(0, 24)});
      }
    }
    // 2) 朱砂实底（背景 或 ≥2px 顶条·面积 >400）
    const bgArea = (cs.backgroundColor === ACCENT) ? r.width * r.height : 0;
    const bw = parseFloat(cs.borderTopWidth) || 0;
    const borderArea = (cs.borderTopColor === ACCENT && bw >= 2)
      ? r.width * bw : 0;
    const area = Math.max(bgArea, borderArea);
    if (area > 400) {
      out.fill.push({tag: el.tagName.toLowerCase(),
        cls: el.getAttribute('class') || '',
        kind: bgArea > 0 ? 'background' : 'border-top',
        area: Math.round(area)});
    }
  }
  return out;
}
"""


def main(argv):
    pages = DEFAULT_PAGES
    if "--pages" in argv:
        raw = argv[argv.index("--pages") + 1]
        pages = [p.strip() for p in raw.split(",") if p.strip()]
    result = {}
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(reduced_motion="reduce",
                                  color_scheme="light")
        page = ctx.new_page()
        for rel in pages:
            page.goto("file:///" + os.path.join(SITE, rel).replace("\\", "/"),
                      wait_until="networkidle", timeout=30000)
            page.wait_for_timeout(2500)
            hits = page.evaluate(AUDIT_JS)
            result[rel] = hits
            print("%-42s 文字落bg %2d · 实底 %d 处%s"
                  % (rel, len(hits["text_on_bg"]), len(hits["fill"]),
                     "" if len(hits["fill"]) <= 3 else "  ← 超限!"))
        browser.close()
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("审计产物 → %s" % os.path.relpath(OUT, ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
