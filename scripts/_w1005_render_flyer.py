# -*- coding: utf-8 -*-
"""_w1005_render_flyer.py — 重渲染宣传单页 A4 正面 PNG（中英各一）

为什么必须重渲染：`assets/promo/output/xiyouji-flyer-a4-front.png` 是 flyer HTML 的
**静态渲染快照**，而 flyer HTML 内嵌 `ink-mountains-hero.webp` 与 `hero-01-xihai-yunhai.webp`
——本批（W1005）原地替换了这两张图 ⇒ 快照不会自动跟着变 ⇒ README 里仍会显示旧图（旧图有七个人）。

尺寸口径：沿用既有产物 1240×1756（A4 竖版比例 1:1.416）· PNG 无损。
用法：py -3 scripts/_w1005_render_flyer.py [--dry-run]
"""
from __future__ import annotations

import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(REPO, "assets", "promo", "output")
W, H = 1240, 1756
JOBS = [
    ("assets/promo/xiyouji-flyer-a4.html", "assets/promo/output/xiyouji-flyer-a4-front.png"),
    ("assets/promo/xiyouji-flyer-a4-en.html", "assets/promo/output/xiyouji-flyer-a4-en-front.png"),
]


def main() -> int:
    dry = "--dry-run" in sys.argv
    try:
        from playwright.sync_api import sync_playwright
    except Exception as e:  # noqa: BLE001
        print("FAIL  playwright 不可用：", e)
        return 1

    os.makedirs(OUT_DIR, exist_ok=True)
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for src_rel, dst_rel in JOBS:
            src = os.path.join(REPO, src_rel.replace("/", os.sep))
            dst = os.path.join(REPO, dst_rel.replace("/", os.sep))
            if not os.path.exists(src):
                print("FAIL  源 HTML 缺失:", src_rel)
                continue
            if not os.path.exists(dst):
                print("SKIP  产物不存在（不新建）:", dst_rel)
                continue
            page = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
            page.goto("file:///" + src.replace("\\", "/"))
            page.wait_for_load_state("networkidle")
            if dry:
                print("DRY  将渲染 %s → %s" % (src_rel, dst_rel))
            else:
                # 固定单页尺寸（1240×1756）——**不用 full_page**（会截到两页版面·高度变 2396）
                page.screenshot(path=dst, clip={"x": 0, "y": 0, "width": W, "height": H})
                print("OK   %s → %s（%d KB）"
                      % (src_rel, os.path.basename(dst_rel), os.path.getsize(dst) // 1024))
            page.close()
        browser.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
