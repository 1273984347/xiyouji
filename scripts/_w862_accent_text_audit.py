#!/usr/bin/env python3
"""_w862_accent_text_audit.py — W862 B1 朱砂文字落点审计（一次性件）。

裁决 1 修法：朱砂**文字**落在 `--bg` 上时用 `--accent-text`；落在 `--paper`
上仍用 `--accent`。本脚本用计算样式做机器分类：可见元素中 color == 浅色朱砂
（#C8463A）且**有效背景**为 --bg（#FAF7F0·含透明链一直到根）的，即
`--accent-text` 的迁移对象；其余（落 paper/深色带/自有底）不动。

暗色主题无需审计：暗色 `--accent-text` 与暗色 `--accent` 同值（#E0604F），
换令牌在暗色是零视觉变化。

产出：scripts/output/_w862_accent_text_audit.json（按页列元素定位信息）。
"""

import json
import os
import sys

from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
OUT = os.path.join(ROOT, "scripts", "output",
                   "_w862_accent_text_audit.json")

PAGES = ["index.html", "guide.html", "curated.html", "dashboard.html",
         "dukou-engine.html", "rum-viewer.html", "visit-viewer.html",
         "404.html"]

ACCENT = "rgb(200, 70, 58)"      # 浅色 --accent #C8463A
BG = "rgb(250, 247, 240)"        # 浅色 --bg #FAF7F0
TRANSPARENT = ("rgba(0, 0, 0, 0)", "transparent")

AUDIT_JS = """
() => {
  const out = [];
  const els = document.querySelectorAll('*');
  for (const el of els) {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') continue;
    const r = el.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) continue;
    if (cs.color !== %s) continue;
    // 有效背景：自身上溯首个非透明 background-color
    let bg = null, node = el;
    while (node && node.nodeType === 1) {
      const b = getComputedStyle(node).backgroundColor;
      if (b !== 'rgba(0, 0, 0, 0)' && b !== 'transparent') { bg = b; break; }
      node = node.parentElement;
    }
    const onBg = (bg === null) || (bg === %s);
    // 定位信息：tag + class + 文本片段
    const txt = (el.textContent || '').replace(/\\s+/g, ' ').trim().slice(0, 30);
    out.push({tag: el.tagName.toLowerCase(),
              cls: el.getAttribute('class') || '',
              id: el.id || '',
              txt: txt,
              ownBg: cs.backgroundColor,
              effBg: bg,
              onBg: onBg});
  }
  return out;
}
""" % (json.dumps(ACCENT), json.dumps(BG))


def main():
    result = {}
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(reduced_motion="reduce",
                                  color_scheme="light")
        page = ctx.new_page()
        for rel in PAGES:
            path = os.path.join(SITE, rel)
            page.goto("file:///" + path.replace("\\", "/"),
                      wait_until="networkidle", timeout=30000)
            page.wait_for_timeout(2500)
            hits = page.evaluate(AUDIT_JS)
            on_bg = [h for h in hits if h["onBg"]]
            result[rel] = {"accent_text_total": len(hits),
                           "on_bg": len(on_bg),
                           "on_bg_elements": on_bg}
            print("%-20s 朱砂文字 %d 处·落 --bg %d 处"
                  % (rel, len(hits), len(on_bg)))
        browser.close()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("审计产物 → %s" % os.path.relpath(OUT, ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
