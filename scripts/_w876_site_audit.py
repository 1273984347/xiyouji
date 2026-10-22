#!/usr/bin/env python3
"""_w876_site_audit.py — C 渠（朱砂文字落 --bg）+ 朱砂实底审计器（W876 重建件）。

**为什么重建**：W876 原审计器未随批入库（只有产物 JSON·复现缺口）——本脚本按
committed 产物（_w876_site_audit.json：1087 处 / 64 页 + fill 457 处 / 89 页）
的口径重建，④ en 138 页迁移直接复用。

**口径（与 v4 规格 §3.1/§3.2 对齐）**：
- 扫描面：site/data/*.html（88）+ site/ 根 8 页（除 _template.html）= 96 页；
- 浅色主题（--accent #C8463A = rgb(200,70,58)·--bg #FAF7F0 = rgb(250,247,240)）；
- text_on_bg（C 渠）：元素**渲染文本**（textContent 去空白非空·含 SVG text——
  容器与其文本子节点可能双计数·与原审计口径一致·W876 实证校准：1087/64 页复现）、
  计算色 = --accent、**有效背景** = --bg（沿祖先链找第一个非透明背景·含自身）
  ——即「朱砂文字落在页面底上」（落 --paper 的按规格豁免：--accent 4.78:1 已过 AA）；
- fill（朱砂实底·阶段 5 门禁同款测量）：元素**自身** background-color = --accent
  且盒面积 > 400px²（kind=background），或自身 border-top-color = --accent、
  border-top-width **≥ 2px** 且**条带面积**（宽 × 边框宽）> 400px²（kind=border-top·
  KPI 顶条族·口径与 _w864_accent_audit.py 及豁免登记簿 criterion 逐字对齐）；
-  settle：networkidle + 2s 地板（chart-audit.js 修复波最远 14s·但其只动尺寸/避让
  不动色·2s 足以覆盖首波；对拍场景另用 15s 地板的 W851 探针）。

**用法**：
    py -3 scripts/_w876_site_audit.py                     # 审计在役站（site/）
    py -3 scripts/_w876_site_audit.py --root <dir>/site   # 审计指定树（如 HEAD 快照）
    py -3 scripts/_w876_site_audit.py --out <path.json>   # 指定产物路径
产物：scripts/output/_w876_site_audit_<tag>.json（tag 默认 live·快照传 --tag head）
"""

import argparse
import json
import os
import sys
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ACCENT = "rgb(200, 70, 58)"      # --accent 浅色
BG = "rgb(250, 247, 240)"        # --bg 浅色
FILL_MIN_AREA = 400              # v4 §3.2：> 400px²

_AUDIT_JS = """
(args) => {
  const [accent, bg] = args;
  const out = {text_on_bg: [], fill: []};
  const els = document.querySelectorAll('*');
  for (const el of els) {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') continue;
    const r = el.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) continue;
    const tag = el.tagName.toLowerCase();
    const cls = el.getAttribute('class') || '';
    // 渲染文本：textContent 去空白非空（容器与其文本子节点可能双计数·原审计口径）
    const txtAll = (el.textContent || '').trim();
    const hasText = !!txtAll;
    if (hasText) txt = txtAll.slice(0, 20);
    // 有效背景：沿祖先链（含自身）第一个非透明背景
    let effBg = 'none', node = el;
    while (node && node.nodeType === 1) {
      const c = getComputedStyle(node).backgroundColor;
      if (c && c !== 'transparent' && c !== 'rgba(0, 0, 0, 0)') { effBg = c; break; }
      node = node.parentElement;
    }
    if (hasText && cs.color === accent && effBg === bg) {
      out.text_on_bg.push({tag: tag, cls: cls, txt: txt});
    }
    const area = r.width * r.height;
    if (area > 400) {
      if (cs.backgroundColor === accent) {
        out.fill.push({tag: tag, cls: cls, kind: 'background', area: Math.round(area)});
      } else if (cs.borderTopColor === accent && parseFloat(cs.borderTopWidth) >= 2) {
        const strip = r.width * parseFloat(cs.borderTopWidth);
        if (strip > 400) {
          out.fill.push({tag: tag, cls: cls, kind: 'border-top', area: Math.round(strip)});
        }
      }
    }
  }
  return out;
}
"""


def _pages(site_dir):
    """扫描面：data 88 + 根 8（_template 不入站·与迁移清单同口径）。"""
    rels = []
    data_dir = os.path.join(site_dir, "data")
    for fn in sorted(os.listdir(data_dir)):
        if fn.endswith(".html"):
            rels.append("data/" + fn)
    for fn in sorted(os.listdir(site_dir)):
        if fn.endswith(".html") and fn != "_template.html":
            rels.append(fn)
    return rels


def main(argv):
    ap = argparse.ArgumentParser(description="W876 C 渠 + 朱砂实底审计器")
    ap.add_argument("--root", default=os.path.join(ROOT, "site"),
                    help="站点根（默认在役 site/·传 HEAD 快照的 .../site）")
    ap.add_argument("--out", default="")
    ap.add_argument("--tag", default="live")
    args = ap.parse_args(argv[1:])

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("FAIL playwright 不可用——审计器拒绝在无浏览器环境下出具数字")
        return 1

    site_dir = os.path.abspath(args.root)
    rels = _pages(site_dir)
    missing = [r for r in rels if not os.path.isfile(os.path.join(site_dir, r.replace("/", os.sep)))]
    if missing:
        print("FAIL 扫描面缺页：%s" % "、".join(missing[:5]))
        return 1

    result = {}
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(reduced_motion="reduce", color_scheme="light")
        page = ctx.new_page()
        for i, rel in enumerate(rels):
            path = os.path.join(site_dir, rel.replace("/", os.sep))
            page.goto("file:///" + path.replace("\\", "/"),
                      wait_until="networkidle", timeout=30000)
            page.wait_for_timeout(2000)
            result[rel] = page.evaluate(_AUDIT_JS, [ACCENT, BG])
            if (i + 1) % 24 == 0:
                print("  ... %d/%d" % (i + 1, len(rels)))
        browser.close()

    out = args.out or os.path.join(ROOT, "scripts", "output",
                                   "_w876_site_audit_%s.json" % args.tag)
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    tb = sum(len(v["text_on_bg"]) for v in result.values())
    pb = sum(1 for v in result.values() if v["text_on_bg"])
    fl = sum(len(v["fill"]) for v in result.values())
    pf = sum(1 for v in result.values() if v["fill"])
    print("=== 审计完成（%d 页）→ %s" % (len(result), os.path.basename(out)))
    print("text_on_bg %d 处 / %d 页 · fill %d 处 / %d 页" % (tb, pb, fl, pf))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
