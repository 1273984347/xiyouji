#!/usr/bin/env python3
"""_w960_pilot_shots.py — W960 试点页实跑截图（推广决策的观感依据）。

产出：
  ① 5 个试点页 × 2 视口（1440×900 / 375×812）的**终态截图**（证明「不坏」）；
  ② 首页首屏的**入场序列分解帧**（慢速播放抓帧，展示 Timeline 编排的真实效果）；
  ③ 每页「被 GSAP 编排的元素清单 + 终态可见性」的 JSON。

实现要点：
  · 本地 HTTP server + 补 MIME（.js / .webp）——file:// 与缺 MIME 是本地验收的两个假故障源；
  · 动效为一次性进场 ⇒ 截图前须「等时长 + 滚全程触发 sections + 回顶」；
  · 分帧用 `gsap.globalTimeline.timeScale(0.15)` 慢放后按固定间隔抓帧（非改产品代码）。

用法：py -3 scripts/_w960_pilot_shots.py [--outdir <目录>]
"""
from __future__ import annotations

import argparse
import functools
import json
import os
import sys
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"

PAGES = [
    ("首页", "index.html"),
    ("回目正文·第007回", "reader/ch007.html"),
    ("专题·西游与死亡研究", "reader/themes/西游与死亡研究专题.html"),
    ("人物·黄风怪外传", "reader/people/黄风怪外传.html"),
    ("人物·白骨精", "reader/people/白骨精.html"),
]
VIEWPORTS = [("1440", 1440, 900), ("375", 375, 812)]

# 入场序列分解：首页首屏的编排单元（与载体 intro 模式一致）
INTRO_UNITS = [
    ".masthead-copy > .kicker", ".masthead-copy > h1", ".masthead-copy > .eng",
    ".masthead-copy > .tagline", ".masthead-copy > .masthead-facts",
    ".masthead-copy > .meta-line", ".masthead-copy > .masthead-cta",
    ".masthead-copy > .hero-dots-row",
]


class Handler(SimpleHTTPRequestHandler):
    extensions_map = {
        **SimpleHTTPRequestHandler.extensions_map,
        ".js": "text/javascript; charset=utf-8",
        ".mjs": "text/javascript; charset=utf-8",
        ".webp": "image/webp",
        ".woff2": "font/woff2",
        ".json": "application/json; charset=utf-8",
    }

    def log_message(self, *args):
        pass


def serve(port: int):
    handler = functools.partial(Handler, directory=str(SITE))
    httpd = ThreadingHTTPServer(("127.0.0.1", port), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", default=os.path.join(os.environ.get("TEMP", "."), "xiyouji_pilot_shots"))
    ap.add_argument("--port", type=int, default=8932)
    args = ap.parse_args()
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    try:
        from playwright.sync_api import sync_playwright
    except ImportError as e:
        print("FAIL playwright 不可用：%s" % e)
        return 1

    httpd = serve(args.port)
    base = "http://127.0.0.1:%d/" % args.port
    report = {"shots": [], "pages": {}}

    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            try:
                for label, rel in PAGES:
                    report["pages"][rel] = {"label": label, "viewports": {}}
                    for vname, vw, vh in VIEWPORTS:
                        ctx = browser.new_context(viewport={"width": vw, "height": vh},
                                                reduced_motion="no-preference")
                        page = ctx.new_page()
                        page.goto(base + rel, wait_until="load", timeout=30000)
                        page.wait_for_timeout(1500)
                        page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
                        page.wait_for_timeout(900)
                        page.evaluate("() => window.scrollTo(0, 0)")
                        page.wait_for_timeout(500)

                        info = page.evaluate("""() => {
                          const out = {gsap: !!window.gsap, units: [], heroOpacity: null};
                          const hero = document.querySelector('.masthead-copy');
                          if (hero) { out.heroOpacity = getComputedStyle(hero).opacity; }
                          document.querySelectorAll('[data-gsap]').forEach(box => {
                            const modes = (box.getAttribute('data-gsap') || '').split(/\\s+/);
                            const units = [];
                            if (modes.indexOf('intro') >= 0) {
                              for (const c of box.children) { units.push(c); }
                            }
                            if (modes.indexOf('sections') >= 0) {
                              box.querySelectorAll('h2, details').forEach(e => units.push(e));
                            }
                            units.forEach(u => {
                              const cs = getComputedStyle(u);
                              out.units.push({
                                tag: u.tagName, cls: String(u.className || '').slice(0, 40),
                                opacity: parseFloat(cs.opacity),
                                visibility: cs.visibility
                              });
                            });
                          });
                          return out;
                        }""")
                        shot = outdir / ("%s-%s.png" % (rel.replace("/", "_").replace(".html", ""), vname))
                        page.screenshot(path=str(shot), full_page=False)
                        report["pages"][rel]["viewports"][vname] = {
                            "shot": str(shot),
                            "gsap": info.get("gsap"),
                            "heroOpacity": info.get("heroOpacity"),
                            "unit_count": len(info.get("units", [])),
                            "min_unit_opacity": min([u["opacity"] for u in info["units"]], default=None),
                        }
                        report["shots"].append(str(shot))
                        page.close()
                        ctx.close()

                # —— 首页入场序列分解（慢放抓帧）——
                ctx = browser.new_context(viewport={"width": 1440, "height": 900},
                                        reduced_motion="no-preference")
                page = ctx.new_page()
                page.goto(base + "index.html", wait_until="load", timeout=30000)
                page.wait_for_timeout(900)
                page.evaluate("""() => {
                  if (window.gsap) { window.gsap.globalTimeline.timeScale(0.12); }
                }""")
                frames = []
                for i in range(5):
                    page.wait_for_timeout(700)
                    f = outdir / ("intro-seq-%d.png" % (i + 1))
                    page.screenshot(path=str(f), full_page=False)
                    frames.append(str(f))
                    report["shots"].append(str(f))
                page.close()
                ctx.close()
                report["intro_frames"] = frames
                report["intro_units"] = INTRO_UNITS
            finally:
                browser.close()
    finally:
        httpd.shutdown()

    rp = outdir / "_pilot_shots.json"
    rp.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print("shots dir: %s" % outdir)
    for s in report["shots"]:
        print("  %s" % s)
    for rel, v in report["pages"].items():
        for vw, d in v["viewports"].items():
            print("  [%s %s] gsap=%s units=%d 最小 opacity=%s"
                  % (rel, vw, d["gsap"], d["unit_count"], d["min_unit_opacity"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
