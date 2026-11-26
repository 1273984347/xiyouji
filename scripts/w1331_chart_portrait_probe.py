#!/usr/bin/env python3
"""_w1331_chart_portrait_probe.py — W1331 竖版图表专项·渲染探针（一次性）。

对含图表的页面在 375（竖版）视口下量五类事实：
  A 图表载体（svg/canvas）清单与容器可滚动性
  B 压缩比 = 载体渲染宽 / viewBox 宽（<0.75 ⇒ 图表被显著压缩）
  C 有效字号 = svg 内 text 最小 font-size × 压缩比（<9 ⇒ 竖屏不可读）
  D 文字越界 = text.getBBox() 超出 viewBox 的文本数（T112「SVG 文字越出视口」口径）
  E 不可达裁切 = 载体溢出视口且无 overflow-x 可滚祖先（T112「固定宽 980 溢出」口径）

用法：
  py -3 scripts/_w1331_chart_portrait_probe.py --width 375
  py -3 scripts/_w1331_chart_portrait_probe.py --pages data/journey-spacetime.html
输出：scripts/output/_w1331_chart_portrait_report.json
"""
import argparse
import glob
import json
import os
import re
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "scripts", "output", "_w1331_chart_portrait_report.json")

PROBE_JS = r"""
() => {
  const VW = window.innerWidth;
  const svgCharts = [];
  const scrollAnc = (el) => {
    let p = el.parentElement;
    while (p && p !== document.body && p !== document.documentElement) {
      const cs = getComputedStyle(p);
      if (/(auto|scroll)/.test(cs.overflowX)) return (p.className || p.tagName).toString().slice(0, 48);
      p = p.parentElement;
    }
    return null;
  };
  const svgs = Array.from(document.querySelectorAll('svg')).filter((s) => {
    const r = s.getBoundingClientRect();
    const cs = getComputedStyle(s);
    if (cs.display === 'none' || cs.visibility === 'hidden') return false;
    if (r.width < 60 || r.height < 50) return false;
    return true;
  });
  for (const s of svgs) {
    const r = s.getBoundingClientRect();
    const vb = s.viewBox && s.viewBox.baseVal ? s.viewBox.baseVal : null;
    const vbw = vb && vb.width ? vb.width : (parseFloat(s.getAttribute('width')) || r.width);
    const scale = vbw ? r.width / vbw : 1;
    // C 有效字号
    let minFs = 99, textCount = 0;
    for (const t of s.querySelectorAll('text')) {
      const fs = parseFloat(getComputedStyle(t).fontSize);
      if (!isFinite(fs)) continue;
      textCount++;
      if (fs < minFs) minFs = fs;
    }
    // D 文字越界：用渲染态 rect 与 svg 自身 rect 比较（getBBox 是元素局部坐标系，
    // 未含祖先 transform，直接与 viewBox 比会系统性误报）。留 6px 容差。
    let outOfSvg = 0, outOfViewport = 0, overflowSample = null;
    for (const t of s.querySelectorAll('text')) {
      const tr = t.getBoundingClientRect();
      if (tr.width < 1 || tr.height < 1) continue;
      const past = Math.max(r.left - tr.left, tr.right - r.right, r.top - tr.top, tr.bottom - r.bottom);
      if (past > 6) {
        outOfSvg++;
        if (tr.right > VW + 2 && !scrollAnc(s)) outOfViewport++;
        if (!overflowSample) {
          overflowSample = {txt: (t.textContent || '').trim().slice(0, 18), past: Math.round(past)};
        }
      }
    }
    svgCharts.push({
      cls: (s.getAttribute('class') || '').slice(0, 40),
      id: (s.getAttribute('id') || '').slice(0, 40),
      parentCls: (s.parentElement && s.parentElement.getAttribute('class') || '').slice(0, 60),
      parentOverflowX: s.parentElement ? getComputedStyle(s.parentElement).overflowX : null,
      cssMinW: getComputedStyle(s).minWidth,
      w: Math.round(r.width), h: Math.round(r.height),
      vbw: Math.round(vbw), scale: Math.round(scale * 1000) / 1000,
      effFs: textCount ? Math.round(minFs * scale * 10) / 10 : null,
      texts: textCount, outOfSvg, outOfViewport, overflowSample,
      scroll: scrollAnc(s),
      right: Math.round(r.right),
      widthAttr: (s.getAttribute('width') || '').slice(0, 12) || null
    });
  }
  const canvases = Array.from(document.querySelectorAll('canvas')).map((c) => {
    const r = c.getBoundingClientRect();
    const cs = getComputedStyle(c);
    return {
      w: Math.round(r.width), h: Math.round(r.height),
      attrW: c.width, attrH: c.height,
      hidden: cs.display === 'none' || r.width < 60,
      scroll: scrollAnc(c), right: Math.round(r.right)
    };
  }).filter((c) => !c.hidden);
  const doc = document.documentElement;
  return {
    vw: VW,
    overflow: Math.max(0, doc.scrollWidth - VW),
    svgCharts, canvases
  };
}
"""


def list_chart_pages():
    """静态筛含图表载体的页（site/data + site/en）。"""
    out = []
    for sub in ("data", "en"):
        d = os.path.join(ROOT, "site", sub)
        for p in sorted(glob.glob(os.path.join(d, "*.html"))):
            name = os.path.basename(p)
            if name.startswith("_"):
                continue
            t = open(p, encoding="utf-8", errors="ignore").read()
            if re.search(r"<svg\b|<canvas\b|THREE|three(?:\.min)?\.js", t):
                out.append(os.path.relpath(p, os.path.join(ROOT, "site")).replace("\\", "/"))
    return out


def grade(rec):
    """单页分级：FAIL=不可读/不可达；WARN=压缩或标签越界；OK=无图表事实问题。

    压缩判据与滚动容器解耦：有 overflow-x 容器但 svg 未设 min-width 时仍会被压扁
    （实测 pilgrim-team-psychology-arc：容器 chart-wrap 可滚，svg 仍缩到 319/720 ⇒ 文字 4.4px），
    这类「假滚动」正是竖版图表专项要抓的。
    """
    fails, warns = [], []
    for c in rec.get("svgCharts", []):
        if c["right"] > rec["vw"] + 1 and not c["scroll"]:
            fails.append("svg 不可达裁切 %dpx（无滚动容器·%s）" % (c["right"] - rec["vw"], c["cls"] or "?"))
        if c["effFs"] is not None and c["effFs"] < 8:
            fails.append("svg 压缩不可读 有效字号 %.1fpx（scale %.2f·%s）" % (c["effFs"], c["scale"], c["cls"] or "?"))
        elif c["effFs"] is not None and c["effFs"] < 9.5:
            warns.append("svg 有效字号 %.1fpx（scale %.2f·%s）" % (c["effFs"], c["scale"], c["cls"] or "?"))
        elif c["scale"] < 0.75:
            warns.append("svg 压缩 scale %.2f（%s）" % (c["scale"], c["cls"] or "?"))
        if c["outOfViewport"]:
            fails.append("svg 文字越出视口 %d 处（%s）" % (c["outOfViewport"], c["cls"] or "?"))
        elif c["outOfSvg"]:
            warns.append("svg 标签越出边界 %d 处（%s）" % (c["outOfSvg"], c["cls"] or "?"))
    for c in rec.get("canvases", []):
        if c["right"] > rec["vw"] + 1 and not c["scroll"]:
            fails.append("canvas 不可达裁切 %dpx（无滚动容器）" % (c["right"] - rec["vw"]))
    if rec["overflow"] > 1:
        fails.append("页面水平溢出 %dpx" % rec["overflow"])
    if fails:
        return "FAIL", fails + warns
    if warns:
        return "WARN", warns
    return "OK", []


def run(pages, width, height, settle):
    from playwright.sync_api import sync_playwright

    out = {"viewport": {"width": width, "height": height},
           "generated": time.strftime("%Y-%m-%dT%H:%M:%S"), "pages": [], "summary": {}}
    t0 = time.time()
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={"width": width, "height": height},
                                  device_scale_factor=2, is_mobile=True, has_touch=True)
        for rel in pages:
            path = os.path.join(ROOT, "site", rel.replace("/", os.sep))
            rec = {"page": rel}
            pg = ctx.new_page()
            try:
                pg.goto("file:///" + path.replace("\\", "/"), wait_until="load", timeout=25000)
                pg.wait_for_timeout(settle)
                rec.update(pg.evaluate(PROBE_JS))
                g, why = grade(rec)
                rec["grade"], rec["reasons"] = g, why
            except Exception as exc:  # noqa: BLE001
                rec["grade"], rec["reasons"] = "ERROR", ["%s: %s" % (type(exc).__name__, str(exc)[:120])]
            finally:
                pg.close()
            out["pages"].append(rec)
            sys.stdout.write({"OK": ".", "WARN": "w", "FAIL": "F", "ERROR": "E"}[rec["grade"]])
            sys.stdout.flush()
        browser.close()
    agg = {"OK": 0, "WARN": 0, "FAIL": 0, "ERROR": 0}
    for rec in out["pages"]:
        agg[rec["grade"]] += 1
    out["summary"] = {"total": len(out["pages"]), "counts": agg, "elapsedSec": round(time.time() - t0, 1)}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--width", type=int, default=375)
    ap.add_argument("--height", type=int, default=812)
    ap.add_argument("--pages", nargs="*", default=None)
    ap.add_argument("--settle", type=int, default=700)
    args = ap.parse_args()
    pages = args.pages or list_chart_pages()
    print("视口 %dx%d · 图表页 %d" % (args.width, args.height, len(pages)))
    report = run(pages, args.width, args.height, args.settle)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(report, f, ensure_ascii=False, indent=1)
    c = report["summary"]["counts"]
    print("\n汇总：OK %d · WARN %d · FAIL %d · ERROR %d · 耗时 %ss" % (
        c["OK"], c["WARN"], c["FAIL"], c["ERROR"], report["summary"]["elapsedSec"]))
    for rec in report["pages"]:
        if rec["grade"] in ("FAIL", "ERROR"):
            print("[%s] %s: %s" % (rec["grade"], rec["page"], "; ".join(rec["reasons"][:4])))
    print("报告：scripts/output/_w1331_chart_portrait_report.json")
    return 0 if not (c["FAIL"] or c["ERROR"]) else 1


if __name__ == "__main__":
    sys.exit(main())
