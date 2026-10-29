# -*- coding: utf-8 -*-
"""_w1013_shot.py — W1013 浏览器实跑（本地 HTTP + Playwright·AC-12）

三件实测（不是截图好看就算）：
  ① 题图**真的加载**（img.naturalWidth > 0 ⇒ 非 404/空图）；
  ② 题图位置在 <h1> 之后（DOM 顺序断言）；
  ③ **暗色模式隐藏**（切 data-theme="dark" ⇒ 题图 offsetParent 为 null·即 display:none）。

另存 2 张截图（tmpe/·gitignored·不入库）供目视复核。

用法：py -3 scripts/_w1013_shot.py
"""
from __future__ import annotations

import functools
import http.server
import io
import os
import socketserver
import sys
import threading

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOTS = os.path.join(REPO, "tmpe")
PAGES = [("ch002", "立像"), ("ch045", "场面")]


def main() -> int:
    try:
        from playwright.sync_api import sync_playwright
    except Exception as e:  # noqa: BLE001
        print("FAIL  playwright 不可用：%r" % (e,))
        return 1
    os.makedirs(SHOTS, exist_ok=True)

    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=REPO)

    class Q(socketserver.TCPServer):
        allow_reuse_address = True

        def log_message(self, *a):  # 静音
            pass

    srv = Q(("127.0.0.1", 0), handler)
    port = srv.server_address[1]
    th = threading.Thread(target=srv.serve_forever, daemon=True)
    th.start()
    base = "http://127.0.0.1:%d" % port
    print("本地服务:", base)

    fails = []
    try:
        with sync_playwright() as pw:
            br = pw.chromium.launch()
            ctx = br.new_context(viewport={"width": 1280, "height": 900}, device_scale_factor=1)
            for ch, kind in PAGES:
                pg = ctx.new_page()
                pg.goto("%s/site/reader/%s.html" % (base, ch), wait_until="load")
                pg.wait_for_timeout(600)
                info = pg.evaluate("""() => {
                  const f = document.querySelector('figure.chapter-plate');
                  const img = f ? f.querySelector('img') : null;
                  const h1 = document.querySelector('h1');
                  return {
                    hasFig: !!f,
                    naturalWidth: img ? img.naturalWidth : 0,
                    complete: img ? img.complete : false,
                    afterH1: !!(h1 && f && (f.compareDocumentPosition(h1) & Node.DOCUMENT_POSITION_PRECEDING)),
                    alt: img ? (img.getAttribute('alt') || '').length : 0,
                    og: (document.querySelector('meta[property=\"og:image\"]')||{}).content || '',
                    display: f ? getComputedStyle(f).display : 'NONE',
                  };
                }""")
                if not info["hasFig"]:
                    fails.append("%s 页面无题图 figure" % ch)
                if info["naturalWidth"] <= 0 or not info["complete"]:
                    fails.append("%s 题图未真实加载（naturalWidth=%s）" % (ch, info["naturalWidth"]))
                if not info["afterH1"]:
                    fails.append("%s 题图不在 <h1> 之后" % ch)
                if info["alt"] <= 10:
                    fails.append("%s 题图 alt 过短（%d）" % (ch, info["alt"]))
                if "og-" not in info["og"]:
                    fails.append("%s og:image 非专属：%s" % (ch, info["og"]))
                # 亮色截图（**必须在切暗色之前**——暗色下题图被隐藏·截不到题图）
                out = os.path.join(SHOTS, "_w1013_shot_%s.png" % ch)
                pg.screenshot(path=out)
                print("[SHOT] %s（%s·亮色）→ %s" % (ch, kind, os.path.relpath(out, REPO).replace("\\", "/")))
                # 暗色模式隐藏
                pg.evaluate("document.documentElement.setAttribute('data-theme','dark')")
                pg.wait_for_timeout(300)
                dark = pg.evaluate("""() => {
                  const f = document.querySelector('figure.chapter-plate');
                  if (!f) return 'NOFIG';
                  return getComputedStyle(f).display;
                }""")
                if dark != "none":
                    fails.append("%s 暗色模式未隐藏题图（display=%s）" % (ch, dark))
                else:
                    print("[OK]   %s 暗色模式隐藏生效（display=none）" % ch)
                pg.close()
            br.close()
    finally:
        srv.shutdown()
        srv.server_close()

    for f in fails:
        print("FAIL  " + f)
    print("---- 浏览器实跑：%d FAIL ----" % len(fails))
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
