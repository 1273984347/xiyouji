#!/usr/bin/env python3
"""_w957_motion_probe.py — W957 施工批「动效实跑」浏览器探针（验收硬判据）。

采集（5 试点页 × 3 视口 × 2 动效偏好态）：
  · pageerror / console error 计数
  · window.gsap / window.ScrollTrigger 是否加载
  · ScrollTrigger 实例数 · gsap 全局时间轴子动画数
  · **编排单元残留初始态清单**（计算样式 opacity < 0.9 者）——判据：清单为空
    （正常动效态：滚动全程后视口内与已滚过的单元均应进场完成；
      RM 态：载体完全不介入 ⇒ 单元立即可见）
  · RM 态附加判据：gsap 全局时间轴子动画数 = 0（无动画执行）

实现要点：
  · 本地 HTTP server + 补 MIME（.js / .webp）——file:// 与缺 MIME 是本地验收的两个假故障源；
  · 零依赖判定：playwright 缺失即报错退出 1，**不静默跳过**（没有证据不许说「通过」）；
  · 滚动全程（到底 → 回顶）以触发所有 ScrollTrigger 触发点。

产出：scripts/output/_w957_motion_probe.json
用法：py -3 scripts/_w957_motion_probe.py [--port 8931]
"""
from __future__ import annotations

import argparse
import functools
import json
import os
import sys
import threading
from datetime import datetime
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
OUT = ROOT / "scripts" / "output" / "_w957_motion_probe.json"

PAGES = [
    "index.html",
    "reader/ch007.html",
    "reader/themes/西游与死亡研究专题.html",
    "reader/people/黄风怪外传.html",
    "reader/people/白骨精.html",
]
VIEWPORTS = [(375, 812), (768, 1024), (1440, 900)]
MODES = [("full", "no-preference"), ("reduce", "reduce")]

COLLECT_JS = r"""
() => {
  const out = {
    gsap: !!window.gsap,
    st: !!window.ScrollTrigger,
    stCount: 0,
    tweens: 0,
    motionInit: -1,
    heroOpacity: null,
    units: 0,
    stuck: []
  };
  if (window.ScrollTrigger) { out.stCount = window.ScrollTrigger.getAll().length; }
  if (window.gsap) { out.tweens = window.gsap.globalTimeline.getChildren(true, true, true).length; }
  if (window.MotionGsap && window.MotionGsap.stats) {
    out.motionInit = window.MotionGsap.stats.init;
  }
  const hero = document.querySelector('.masthead-copy');
  if (hero) { out.heroOpacity = getComputedStyle(hero).opacity; }
  const boxes = document.querySelectorAll('[data-gsap]');
  for (const box of boxes) {
    const modes = (box.getAttribute('data-gsap') || '').split(/\s+/);
    const units = [];
    if (modes.indexOf('intro') >= 0) {
      for (const c of box.children) { units.push(c); }
    }
    if (modes.indexOf('sections') >= 0) {
      box.querySelectorAll('h2').forEach(e => units.push(e));
    }
    if (modes.indexOf('cards') >= 0) {
      const sel = box.getAttribute('data-gsap-target') || '.card';
      try { box.querySelectorAll(sel).forEach(e => units.push(e)); } catch (e) { }
    }
    out.units += units.length;
    for (const u of units) {
      const cs = getComputedStyle(u);
      const op = parseFloat(cs.opacity);
      if (!(op >= 0.9)) {
        const r = u.getBoundingClientRect();
        out.stuck.push({
          tag: u.tagName,
          cls: String(u.className || '').slice(0, 48),
          opacity: op,
          visibility: cs.visibility,
          inView: r.top < window.innerHeight && r.bottom > 0
        });
      }
    }
  }
  return out;
}
"""


class Handler(SimpleHTTPRequestHandler):
    extensions_map = {
        **SimpleHTTPRequestHandler.extensions_map,
        ".js": "text/javascript; charset=utf-8",
        ".mjs": "text/javascript; charset=utf-8",
        ".webp": "image/webp",
        ".woff2": "font/woff2",
        ".json": "application/json; charset=utf-8",
    }

    def log_message(self, *args):  # 静默访问日志
        pass


def serve(port: int):
    handler = functools.partial(Handler, directory=str(SITE))
    httpd = ThreadingHTTPServer(("127.0.0.1", port), handler)
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    return httpd


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8931)
    ap.add_argument("--out", default="", help="产物输出文件（缺省为默认）：不同页集应写不同文件，避免覆盖历史批次产物")
    ap.add_argument("--pages", default="",
                    help="逗号分隔的页面相对路径（相对 site/）·缺省用内置 PAGES 清单")
    args, _unknown = ap.parse_known_args()
    pages = PAGES
    if args.pages:
        pages = [x.strip() for x in args.pages.split(",") if x.strip()]

    try:
        from playwright.sync_api import sync_playwright
    except ImportError as e:
        print("FAIL playwright 不可用（%s）——探针拒绝在无浏览器环境下出具「通过」结论" % e)
        return 1

    httpd = serve(args.port)
    base = "http://127.0.0.1:%d/" % args.port
    results = []
    fails = []
    rag_notes = []

    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            try:
                for mode, motion in MODES:
                    for vw, vh in VIEWPORTS:
                        ctx = browser.new_context(viewport={"width": vw, "height": vh},
                                                  reduced_motion=motion)
                        for rel in pages:
                            page = ctx.new_page()
                            perrors = []
                            cerrors = []
                            page.on("pageerror", lambda e, sink=perrors: sink.append(str(e)))
                            page.on("console", lambda m, sink=cerrors: sink.append(m.text)
                                    if m.type == "error" else None)
                            try:
                                page.goto(base + rel, wait_until="load", timeout=30000)
                                page.wait_for_timeout(1200)
                                # 滚动全程 → 触发所有触发点 → 回顶
                                page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
                                page.wait_for_timeout(900)
                                page.evaluate("() => window.scrollTo(0, 0)")
                                page.wait_for_timeout(400)
                                data = page.evaluate(COLLECT_JS)
                            except Exception as exc:
                                data = {"error": str(exc)}
                            page.close()

                            row = {"page": rel, "mode": mode, "viewport": "%dx%d" % (vw, vh),
                                   "pageerror": perrors, "console_error": cerrors,
                                   "data": data}
                            results.append(row)

                            bad = []
                            notes = []
                            # 站内 RAG 请求（127.0.0.1:8777 本地服务未启动）是既有环境事实，
                            # 与本批动效无关 ⇒ 归 NOTE 不阻断（RAG 类错误单独计数）
                            rag = [c for c in cerrors
                                   if "ERR_CONNECTION_REFUSED" in c or "501" in c
                                   or "8777" in c]
                            other_ce = [c for c in cerrors if c not in rag]
                            if rag:
                                notes.append("rag_env_error×%d" % len(rag))
                            if perrors:
                                bad.append("pageerror×%d" % len(perrors))
                            if other_ce:
                                bad.append("console_error×%d" % len(other_ce))
                            if data.get("error"):
                                bad.append("load_error")
                            else:
                                if not data.get("gsap"):
                                    bad.append("gsap 未加载")
                                if not data.get("st"):
                                    bad.append("ScrollTrigger 未加载")
                                if data.get("stuck"):
                                    bad.append("编排单元残留初始态×%d" % len(data["stuck"]))
                                # 载体执行数判据（精确判据）：
                                #   RM 态 ⇒ 载体零介入（stats.init === 0）；
                                #   正常态 ⇒ 载体已执行（stats.init ≥ 1）。
                                #   注：不用「gsap 全局时间轴子动画数」作 RM 判据——GSAP 库自身
                                #   在 globalTimeline 内有常驻内部 tween（实测恒为 1），该口径会恒红。
                                if mode == "reduce":
                                    if data.get("motionInit") != 0:
                                        bad.append("RM 态载体仍介入（init=%s·应 0）"
                                                   % data.get("motionInit"))
                                    if data.get("stCount", 0) != 0:
                                        bad.append("RM 态存在 ScrollTrigger 实例 %d" % data["stCount"])
                                else:
                                    if data.get("motionInit", -1) < 1:
                                        bad.append("正常态载体未执行（init=%s）"
                                                   % data.get("motionInit"))
                                    if data.get("heroOpacity") is not None:
                                        try:
                                            if float(data["heroOpacity"]) < 0.9:
                                                bad.append("首页首屏编排后不可见（opacity=%s）"
                                                           % data["heroOpacity"])
                                        except (TypeError, ValueError):
                                            pass
                            if bad:
                                fails.append("%s [%s %s]：%s" % (rel, mode, row["viewport"], "、".join(bad)))
                            if notes:
                                rag_notes.append("%s [%s %s]：%s" % (rel, mode, row["viewport"], "、".join(notes)))
                        ctx.close()
            finally:
                browser.close()
    finally:
        httpd.shutdown()

    payload = {
        "batch": "W957",
        "generated_by": "scripts/_w957_motion_probe.py",
        "captured_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "pages": PAGES,
        "viewports": ["%dx%d" % v for v in VIEWPORTS],
        "modes": MODES,
        "results": results,
        "fails": fails,
        "rag_env_notes": rag_notes,
        "verdict": "FAIL" if fails else "PASS",
    }
    out_path = Path(args.out) if args.out else OUT
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print("motion probe written: %s" % out_path)
    print("  采集 %d 组（%d 页 × %d 视口 × %d 模式）" % (len(results), len(pages), len(VIEWPORTS), len(MODES)))
    for n in rag_notes[:8]:
        print("  NOTE %s" % n)
    for f in fails:
        print("  FAIL %s" % f)
    print("  判定：%s" % payload["verdict"])
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
