#!/usr/bin/env python3
"""_w886_en_audit.py — ④ en 138 页迁移现状审计（四渠一次性件·W886 建）。

**目的**：en 138 页从未进过迁移面（v4 §6 只覆盖 95 数据+根 + 622 reader），本审计为
「5 批 × 28 页」分批提供实测依据（先量后切，不拍脑袋分组）。

**四渠测量**（浏览器计算样式 + 静态 CSS 扫描，双轨）：
1. C 渠（朱砂文字落 --bg）：textContent 非空 + color == --accent + 有效背景 == --bg
   → 待换 --accent-text 的规则级候选（口径同 _w876_site_audit.py 校准版）。
2. B 渠（朱砂实底）：背景=朱砂且盒面积 >400px²，或 ≥2px 朱砂顶条条带面积 >400px²
   （口径同第 49 门禁 check_vermilion_solid.js 与豁免登记簿 criterion）。
3. 令牌陈旧（静态）：页内是否残留旧值 --chart-3:#C9A063 / 暗色 --accent:#E0604F
   → 需要靶向值同步的页（W876 只同步了 326 个中/reader 页）。
4. A 渠（静态）：容器字面量（1320px/1536px/1024px）与 var(--container-*) 用量
   → 容器令牌化候选规模。

产出：scripts/output/_w886_en_audit.json（逐页）+ stdout 分组概览（供分批）。
用法：py -3 scripts/_w886_en_audit.py [--dir site/en] [--out ...]
"""

import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ACCENT = "rgb(200, 70, 58)"
BG = "rgb(250, 247, 240)"
FILL_MIN_AREA = 400
BORDER_MIN_PX = 2

_AUDIT_JS = """
(cfg) => {
  const {accent, bg, areaMin, borderMin} = cfg;
  const out = {text_on_bg: [], fill: []};
  const transparent = (c) => c === 'rgba(0, 0, 0, 0)' || c === 'transparent';
  for (const el of document.querySelectorAll('*')) {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') continue;
    const r = el.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) continue;
    const tag = el.tagName.toLowerCase();
    const txtAll = (el.textContent || '').trim();
    // C 渠：朱砂文字落 --bg
    if (txtAll && cs.color === accent) {
      let eff = null, node = el;
      while (node && node.nodeType === 1) {
        const b = getComputedStyle(node).backgroundColor;
        if (!transparent(b)) { eff = b; break; }
        node = node.parentElement;
      }
      if (eff === null || eff === bg) {
        out.text_on_bg.push({tag: tag, cls: el.getAttribute('class') || '',
                             txt: txtAll.slice(0, 20)});
      }
    }
    // B 渠：朱砂实底
    const bgA = (cs.backgroundColor === accent) ? r.width * r.height : 0;
    const bw = parseFloat(cs.borderTopWidth) || 0;
    const bdA = (cs.borderTopColor === accent && bw >= borderMin) ? r.width * bw : 0;
    const area = Math.max(bgA, bdA);
    if (area > areaMin) {
      out.fill.push({tag: tag, cls: el.getAttribute('class') || '',
                     kind: bgA > 0 ? 'background' : 'border-top', area: Math.round(area)});
    }
  }
  return out;
}
"""

_TOKEN_OLD = re.compile(r"--chart-3:\s*#C9A063|--accent:\s*#E0604F")
_CONTAINER_LIT = re.compile(r"max-width:\s*(?:1320px|1536px|1024px)")
_CONTAINER_TOK = re.compile(r"var\(--container-[a-z]+\)")
_ACCENT_TEXT = re.compile(r"--accent-text:")


def static_probe(html):
    return {
        "token_old": bool(_TOKEN_OLD.search(html)),
        "container_lit": len(_CONTAINER_LIT.findall(html)),
        "container_tok": len(_CONTAINER_TOK.findall(html)),
        "accent_text_def": bool(_ACCENT_TEXT.search(html)),
    }


def main(argv):
    ap = argparse.ArgumentParser(description="en 138 页迁移现状审计")
    ap.add_argument("--dir", default="site/en")
    ap.add_argument("--out", default="scripts/output/_w886_en_audit.json")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--pages", default="")
    args = ap.parse_args(argv[1:])

    en_dir = os.path.join(ROOT, args.dir)
    pages = sorted(fn for fn in os.listdir(en_dir) if fn.endswith(".html"))
    if args.pages:
        want = {p.strip() for p in args.pages.split(",") if p.strip()}
        pages = [p for p in pages if p in want]
    if args.limit:
        pages = pages[: args.limit]
    result = {}
    for fn in pages:
        rel = "en/" + fn
        html = open(os.path.join(en_dir, fn), encoding="utf-8").read()
        st = static_probe(html)
        result[rel] = {"static": st, "text_on_bg": [], "fill": []}

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("FAIL playwright 不可用——本审计需要浏览器实测（拒绝无据下结论）")
        return 2

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(reduced_motion="reduce", color_scheme="light")
        page = ctx.new_page()
        for i, rel in enumerate(result):
            abs_p = os.path.join(ROOT, "site", rel.replace("/", os.sep))
            page.goto("file:///" + os.path.abspath(abs_p).replace("\\", "/"),
                      wait_until="networkidle", timeout=30000)
            page.wait_for_timeout(2000)
            hits = page.evaluate(_AUDIT_JS, {"accent": ACCENT, "bg": BG,
                                             "areaMin": FILL_MIN_AREA,
                                             "borderMin": BORDER_MIN_PX})
            result[rel]["text_on_bg"] = hits["text_on_bg"]
            result[rel]["fill"] = hits["fill"]
            if (i + 1) % 28 == 0:
                print("  ... %d/%d" % (i + 1, len(result)))
        browser.close()

    out = os.path.join(ROOT, args.out)
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)

    # 概览（供分批）
    tot_text = sum(len(v["text_on_bg"]) for v in result.values())
    pg_text = sum(1 for v in result.values() if v["text_on_bg"])
    tot_fill = sum(len(v["fill"]) for v in result.values())
    pg_fill = sum(1 for v in result.values() if v["fill"])
    pg_old = sum(1 for v in result.values() if v["static"]["token_old"])
    pg_clit = sum(1 for v in result.values() if v["static"]["container_lit"])
    print("=== en 审计完成（%d 页）→ %s" % (len(result), os.path.basename(out)))
    print("C 渠落 bg 朱砂文字 %d 处 / %d 页 · 朱砂实底 %d 处 / %d 页" % (tot_text, pg_text, tot_fill, pg_fill))
    print("令牌旧值残留 %d 页 · 容器字面量页 %d 页" % (pg_old, pg_clit))
    print("--- 逐页 C/实底/旧值/容器字面量（供分批）---")
    for rel, v in result.items():
        print("%-44s C %3d · F %2d · old %d · lit %2d"
              % (rel, len(v["text_on_bg"]), len(v["fill"]),
                 v["static"]["token_old"], v["static"]["container_lit"]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
