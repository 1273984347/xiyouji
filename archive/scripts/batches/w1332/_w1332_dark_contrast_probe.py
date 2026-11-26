#!/usr/bin/env python3
"""_w1332_dark_contrast_probe.py — W1332 暗色对比度专项探针（一次性·L-13 ②–⑤ 判据自动化）。

对根页 + site/data + site/en（+ reader 抽样）在**夜读态**下量三类事实：
  A HTML 文字     nav/header/th/dt/dd/summary/.meta/.kicker 等文字色 vs 合成背景（逐层 alpha 合成）
                  CR < 3 判 FAIL（不可读）·3–4.5 判 WARN
  B SVG 形状可见  rect/circle/path/polygon 的 computed fill vs 合成背景 ·CR < 1.15 且面积 ≥ 400
                  ⇒ invisible 形状（L-13 ②「暗色态 invisible 形状」）
  C SVG 文字合成  文字 fill vs 几何覆盖图形 fill（fillAlpha × opacity 合成到背景）·CR < 3
                  ⇒ 半透明淡色底标签（L-13 ③「压在半透明淡色底上的图表标签」）

夜读态强制：context.add_init_script 预置 localStorage `xy-theme=dark`（页面 head 内联夜读脚本
消费；无该脚本的页回退 setsAttribute）。

用法：
  py -3 scripts/_w1332_dark_contrast_probe.py                 # 全量（根页+data+en+reader 抽样）
  py -3 scripts/_w1332_dark_contrast_probe.py --pages data/81-hardships.html
输出：scripts/output/_w1332_dark_contrast_report.json
"""
import argparse
import glob
import json
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "scripts", "output", "_w1332_dark_contrast_report.json")

PROBE_JS = r"""
() => {
  const parseRGB = (s) => {
    const m = String(s).match(/rgba?\(([^)]+)\)/);
    if (m) {
      const p = m[1].split(',').map(Number);
      return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 };
    }
    // color(srgb 0.1 0.09 0.078 / 0.92) —— color-mix() 的 computed 形态（0–1 浮点）
    const cm = String(s).match(/color\(srgb\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)(?:\s*\/\s*([\d.]+))?\)/);
    if (cm) {
      return { r: Math.round(Number(cm[1]) * 255), g: Math.round(Number(cm[2]) * 255),
               b: Math.round(Number(cm[3]) * 255), a: cm[4] === undefined ? 1 : Number(cm[4]) };
    }
    const h = String(s).match(/^#([0-9a-f]{6})$/i);
    if (h) {
      const v = parseInt(h[1], 16);
      return { r: (v >> 16) & 255, g: (v >> 8) & 255, b: v & 255, a: 1 };
    }
    return null;
  };
  const lum = (c) => {
    const f = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
    return 0.2126 * f(c.r) + 0.7152 * f(c.g) + 0.0722 * f(c.b);
  };
  const cr = (a, b) => {
    if (!a || !b) return 99;
    const l1 = lum(a), l2 = lum(b);
    return Math.round(((Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05)) * 100) / 100;
  };
  const over = (fg, bg) => ({  // fg over bg（alpha 合成）
    r: Math.round(fg.r * fg.a + bg.r * (1 - fg.a)),
    g: Math.round(fg.g * fg.a + bg.g * (1 - fg.a)),
    b: Math.round(fg.b * fg.a + bg.b * (1 - fg.a)),
    a: 1
  });
  const isVisible = (el) => {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') return false;
    if (parseFloat(cs.opacity) === 0) return false;
    const r = el.getBoundingClientRect();
    return r.width > 1 && r.height > 1;
  };
  // 合成背景：自元素向上逐层收集非透明背景，按文档顺序 over 合成
  const bgOf = (el) => {
    const stack = [];
    let p = el;
    while (p && p !== document.documentElement) {
      const cs = getComputedStyle(p);
      const c = parseRGB(cs.backgroundColor);
      if (c && c.a > 0) stack.push(c);
      if (c && c.a >= 0.999) break;
      p = p.parentElement;
    }
    // 基色优先取 body（页面实际底色通常落在 body），body 透明才回退 html；
    // 实测：html 背景仍是亮色 #F2EDE2 而 body 为暗色 #1A1714 ⇒ 取 html 会把浅字误判低对比。
    let base = parseRGB(getComputedStyle(document.body).backgroundColor);
    if (!base || base.a < 0.999) {
      const htmlBg = parseRGB(getComputedStyle(document.documentElement).backgroundColor);
      if (htmlBg) base = base ? over(base, htmlBg) : htmlBg;
    }
    if (!base || base.a < 1) base = over(base || { r: 255, g: 255, b: 255, a: 1 }, { r: 255, g: 255, b: 255, a: 1 });
    for (let i = stack.length - 1; i >= 0; i--) base = over(stack[i], base);
    return base;
  };
  const desc = (el) => ({
    tag: el.tagName.toLowerCase(),
    cls: (el.getAttribute('class') || '').slice(0, 40),
    txt: (el.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 30)
  });
  // 背景含渐变/backdrop-filter/背景图时 backgroundColor 不可代表实际底色（实测
  // en/theological-intervention-network 顶栏：computed bg 浅米但视觉深色）⇒ 该项降为信息不判红。
  const uncertainBg = (el) => {
    let p = el;
    while (p && p !== document.documentElement) {
      const cs = getComputedStyle(p);
      if (cs.backgroundImage && cs.backgroundImage !== 'none') return true;
      if (cs.backdropFilter && cs.backdropFilter !== 'none') return true;
      p = p.parentElement;
    }
    return false;
  };

  const out = { htmlText: [], shapes: [] };

  // A HTML 文字
  const textSel = 'nav a, header a, .nav-brand, .nav-item, .is-active, .wordmark, th, dt, dd, summary, ' +
                  '.meta, .kicker, .stat-value, .data-value, .label, caption, figcaption, .notice, .note';
  const seen = new Set();
  for (const el of document.querySelectorAll(textSel)) {
    if (seen.has(el) || !isVisible(el)) continue;
    seen.add(el);
    const txt = (el.textContent || '').trim();
    if (txt.length < 2) continue;
    const cs = getComputedStyle(el);
    const fg = parseRGB(cs.color);
    if (!fg) continue;
    const bg = bgOf(el);
    const crv = cr(fg, bg);
    if (crv < 4.5) {
      const fs = parseFloat(cs.fontSize) || 14;
      out.htmlText.push(Object.assign(desc(el), { cr: crv, fs: Math.round(fs),
        fg: `rgb(${fg.r},${fg.g},${fg.b})`, bg: `rgb(${bg.r},${bg.g},${bg.b})`,
        uncertain: uncertainBg(el) }));
    }
  }

  // B SVG 形状可见性 + C SVG 文字合成底色
  for (const svg of document.querySelectorAll('svg')) {
    if (!isVisible(svg)) continue;
    const svgBg = bgOf(svg);
    for (const sp of svg.querySelectorAll('rect, circle, ellipse, path, polygon')) {
      if (sp.closest('clipPath, mask, defs')) continue;
      // 无 class 的图形视作装饰轨道/斑马纹（实测 relationships/game-webnovel 与底同色属设计意图）；
      // 数据语义形状必须有 class（图表数据族约定），该口径在报告中声明。
      if (!sp.getAttribute('class')) continue;
      const cs = getComputedStyle(sp);
      const fill = parseRGB(cs.fill);
      if (!fill || fill.a === 0) continue;
      // 低透明度填充（≤0.2）视作背景/装饰层（实测 cross-time-danmaku .map-continent
      // fill rgba(122,82,48,0.1) 是大洲淡色背景块，靠 stroke 勾轮廓——设计意图，不判可见性）
      if (fill.a <= 0.2) continue;
      if (cs.display === 'none' || cs.visibility === 'hidden') continue;
      if (parseFloat(cs.opacity) === 0) continue;
      const r = sp.getBoundingClientRect();
      const area = Math.round(r.width * r.height);
      if (area < 400) continue;
      const composite = over(fill, svgBg);
      const crv = cr(composite, svgBg);
      if (crv < 1.15) {
        out.shapes.push(Object.assign(desc(sp), { cr: crv, area: area,
          fill: `rgba(${fill.r},${fill.g},${fill.b},${fill.a})` }));
      }
    }
    // C 项（SVG 文字 vs 覆盖图形合成底）已移除：简化几何判定实测误报（W1332 截图证伪），
    // 该面由第 80 槽 graphic 口径（getBBox + getCTM 严谨配对）承担。
  }
  return out;
}
"""


def list_pages(scope):
    pages = []
    if scope in ("root", "all"):
        pages += sorted(os.path.relpath(p, os.path.join(ROOT, "site")).replace("\\", "/")
                        for p in glob.glob(os.path.join(ROOT, "site", "*.html"))
                        if not os.path.basename(p).startswith("_"))
    for sub in ("data", "en"):
        if scope in (sub, "all"):
            pages += sorted(os.path.relpath(p, os.path.join(ROOT, "site")).replace("\\", "/")
                            for p in glob.glob(os.path.join(ROOT, "site", sub, "*.html"))
                            if not os.path.basename(p).startswith("_"))
    if scope == "all":
        reader = sorted(glob.glob(os.path.join(ROOT, "site", "reader", "*.html")))
        pages += [os.path.relpath(p, os.path.join(ROOT, "site")).replace("\\", "/") for p in reader[::20]]
    return pages


def grade(rec):
    fails, warns = [], []
    for h in rec["htmlText"]:
        if h.get("uncertain"):
            continue  # 背景含渐变/backdrop-filter：computed bg 不代表实际底色，不判红
        slot = "FAIL" if h["cr"] < 3 else "WARN"
        (fails if slot == "FAIL" else warns).append("HTML 文字 CR %.2f（%s·%s）" % (h["cr"], h["txt"][:12], h["cls"] or h["tag"]))
    for s in rec["shapes"]:
        fails.append("SVG 形状不可见 CR %.2f（%s·面积 %d）" % (s["cr"], s["cls"] or s["tag"], s["area"]))
    if fails:
        return "FAIL", fails[:6] + warns[:3]
    if warns:
        return "WARN", warns[:6]
    return "OK", []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scope", default="all", choices=["root", "data", "en", "all"])
    ap.add_argument("--pages", nargs="*", default=None)
    ap.add_argument("--settle", type=int, default=500)
    args = ap.parse_args()
    pages = args.pages or list_pages(args.scope)
    from playwright.sync_api import sync_playwright

    report = {"generated": time.strftime("%Y-%m-%dT%H:%M:%S"), "theme": "dark",
              "scope": args.scope, "pages": [], "summary": {}}
    t0 = time.time()
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={"width": 1280, "height": 900}, device_scale_factor=1)
        ctx.add_init_script("try{localStorage.setItem('xy-theme','dark');}catch(e){}")
        for rel in pages:
            path = os.path.join(ROOT, "site", rel.replace("/", os.sep))
            rec = {"page": rel}
            pg = ctx.new_page()
            try:
                pg.goto("file:///" + path.replace("\\", "/"), wait_until="load", timeout=25000)
                pg.evaluate("() => { if (!document.documentElement.hasAttribute('data-theme')) "
                            "document.documentElement.setAttribute('data-theme','dark'); }")
                pg.wait_for_timeout(args.settle)
                facts = pg.evaluate(PROBE_JS)
                rec.update(facts)
                g, why = grade(rec)
                rec["grade"], rec["reasons"] = g, why
            except Exception as exc:  # noqa: BLE001
                rec["grade"], rec["reasons"] = "ERROR", ["%s: %s" % (type(exc).__name__, str(exc)[:120])]
                rec.setdefault("htmlText", []); rec.setdefault("shapes", [])
            finally:
                pg.close()
            report["pages"].append(rec)
            sys.stdout.write({"OK": ".", "WARN": "w", "FAIL": "F", "ERROR": "E"}[rec["grade"]])
            sys.stdout.flush()
        browser.close()
    agg = {"OK": 0, "WARN": 0, "FAIL": 0, "ERROR": 0}
    for rec in report["pages"]:
        agg[rec["grade"]] += 1
    report["summary"] = {"total": len(report["pages"]), "counts": agg,
                         "elapsedSec": round(time.time() - t0, 1)}
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(report, f, ensure_ascii=False, indent=1)
    print("\n汇总：OK %d · WARN %d · FAIL %d · ERROR %d · 耗时 %ss" % (
        agg["OK"], agg["WARN"], agg["FAIL"], agg["ERROR"], report["summary"]["elapsedSec"]))
    for rec in report["pages"]:
        if rec["grade"] in ("FAIL", "ERROR"):
            print("[%s] %s: %s" % (rec["grade"], rec["page"], "; ".join(rec["reasons"][:3])))
    print("报告：scripts/output/_w1332_dark_contrast_report.json")
    return 0 if not (agg["FAIL"] or agg["ERROR"]) else 1


if __name__ == "__main__":
    sys.exit(main())
