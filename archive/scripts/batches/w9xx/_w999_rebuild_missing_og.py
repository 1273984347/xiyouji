"""_w999_rebuild_missing_og.py — 重建全站缺失的 og 版（通用·按页面 og:image 反查）

起因：W999 批清理待重生成的 og 版时用了**过宽的 glob**（`og-plate-line-[4-6]*`）
⇒ 连带删掉了 W988 批既有的 9 个 og 版（plate-line-40..48）⇒ 那些页面的 og:image 会 404。

本脚本**按页面实际引用**反查：凡 og:image 指向 `og-<stem>.webp` 而文件不存在，
即从母版 `plate-set/<stem>.png` 重新裁 1200×630 写出（口径与 `_w999_insert.py` 一致：
主体跨高 ≤ 630 ⇒ 居中带；> 630 ⇒ 头部带 [主体顶−30, +630]）。

用法：py -3 scripts/_w999_rebuild_missing_og.py [--dry-run]
"""
from __future__ import annotations

import glob
import os
import re
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _w988_subject import crop_band  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SET_DIR = os.path.join(ROOT, "assets", "promo", "plate-set")
IMG = os.path.join(ROOT, "site", "static", "images")
OG_BASE = "https://1273984347.github.io/xiyouji/static/images/"
OG_W, OG_H = 1200, 630
RE_OG = re.compile(r'<meta property="og:image" content="([^"]+)"')


def main() -> int:
    dry = "--dry-run" in sys.argv
    need = {}
    for f in glob.glob(os.path.join(ROOT, "site", "**", "*.html"), recursive=True):
        s = open(f, encoding="utf-8", errors="ignore").read()
        m = RE_OG.search(s)
        if not m:
            continue
        url = m.group(1)
        if not url.startswith(OG_BASE):
            continue
        name = url[len(OG_BASE):]
        if not name.startswith("og-") or not name.endswith(".webp"):
            continue
        stem = name[3:-5]
        p = os.path.join(IMG, name)
        if not os.path.exists(p):
            need.setdefault(stem, []).append(os.path.relpath(f, ROOT).replace("\\", "/"))

    if not need:
        print("无缺失 og 版（全部在位）")
        return 0
    print("缺失 og 版 %d 个：" % len(need))
    ok = bad = 0
    for stem, pages in sorted(need.items()):
        src = os.path.join(SET_DIR, stem + ".png")
        out = os.path.join(IMG, "og-%s.webp" % stem)
        if not os.path.exists(src):
            print("  FAIL %-40s 母版缺失：%s" % (stem, os.path.basename(src)))
            bad += 1
            continue
        im = Image.open(src).convert("RGB")
        cropped, info = crop_band(im, OG_W, OG_H, "og")
        if dry:
            print("  DRY  %-40s ← %s（引用 %d 页）" % (stem, os.path.basename(src), len(pages)))
        else:
            tmp = out + ".tmp"
            cropped.save(tmp, "WEBP", quality=90, method=6)
            os.replace(tmp, out)
            print("  OK   %-40s ← %s（引用 %d 页·裁 %s）"
                  % (stem, os.path.basename(src), len(pages), info["crop_y"]))
        ok += 1
    print("\n重建 %d 个 · 失败 %d 个" % (ok, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
