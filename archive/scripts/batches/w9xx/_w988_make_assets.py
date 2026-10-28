#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_w988_make_assets.py — W988 派生两类资产（不碰页面·只写图）

派生一：**角色页顶部横幅** 13 张 —— 1:1（1200×1200）源 → 1200×500 宽幅
  口径：裁切带上边 = 主体顶 − 30 px（头顶留呼吸空间）·保「头顶 + 上半身」·不缩放变形。
派生二：**分回次 og:image** 102 张 —— 该页「首屏第一张配图」→ 1200×630
  口径：主体跨高 ≤ 630 ⇒ 居中带（主体完整）；> 630 ⇒ 头部带 [主体顶−30, +630]（保头与胸腹）。

产物名：
  site/static/images/banner-<card>.webp          （横幅·1200×500）
  site/static/images/og-<plate-stem>.webp        （og·来自线描题图）
  site/static/images/og-banner-<card>.webp       （og·来自横幅源卡）
  site/static/images/og-scene-<card>.webp        （og·来自场景源卡）

用法：py -3 scripts/_w988_make_assets.py [--dry-run]
"""
from __future__ import annotations

import json
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _w988_subject import crop_band  # noqa: E402
from _w988_plan import BANNERS  # noqa: E402

# 裁切特例（落位表 banner_crop 字段）：通用「主体顶−30」在这张上会把人物整段切掉
OVERRIDE = {b["card"]: b["banner_crop"] for b in BANNERS if b.get("banner_crop")}

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "site", "static", "images")
PRE = os.path.join(ROOT, "scripts", "output", "_w988_precheck.json")
BAN_W, BAN_H = 1200, 500
OG_W, OG_H = 1200, 630
Q = 90


def save_webp(im: Image.Image, path: str) -> int:
    tmp = path + ".tmp"
    im.save(tmp, "WEBP", quality=Q, method=6)
    os.replace(tmp, path)
    return os.path.getsize(path)


def main() -> int:
    dry = "--dry-run" in sys.argv
    with open(PRE, encoding="utf-8") as fh:
        pre = json.load(fh)

    jobs = []          # (out_name, src_path, mode, out_w, out_h)

    # ① 横幅 13 张
    for c in pre["cards"]:
        if c["slot"] != "banner":
            continue
        src = os.path.join(IMG, c["card"] + ".webp")
        jobs.append(("banner-" + c["card"], src, "banner", BAN_W, BAN_H))

    # ② og 102 张
    for o in pre["og_plan"]:
        if o["kind"] == "plate":
            jobs.append((o["out"][:-5], o["src"], "og", OG_W, OG_H))
        else:
            src = os.path.join(IMG, o["card"] + ".webp")
            jobs.append((o["out"][:-5], src, "og", OG_W, OG_H))

    n_ok = n_skip = 0
    total = 0
    report = []
    for out_name, src, mode, w, h in jobs:
        out_path = os.path.join(IMG, out_name + ".webp")
        if not os.path.exists(src):
            print("FAIL  源图缺失: " + src)
            n_skip += 1
            continue
        im = Image.open(src).convert("RGB")
        if im.size == (w, h) and os.path.exists(out_path):
            print("SKIP  已是目标尺寸且已存在: " + out_name)
            n_skip += 1
            continue
        card = os.path.basename(src)[:-5]
        ov = OVERRIDE.get(card) if mode == "banner" else None
        if ov:
            y0, y1 = ov
            cropped = im.crop((0, y0, im.width, y1)).resize((w, h), Image.LANCZOS)
            info = {"src_size": list(im.size), "crop_y": [y0, y1], "subject_top": -1,
                    "subject_bottom": -1, "head_room": -1, "span": -1, "mode": "banner-override"}
        else:
            cropped, info = crop_band(im, w, h, mode)
        if dry:
            print("DRY   %-46s <- %-34s 裁 %s 主体 %d..%d 头顶余量 %d"
                  % (out_name, os.path.basename(src), info["crop_y"],
                     info["subject_top"], info["subject_bottom"], info["head_room"]))
        else:
            size = save_webp(cropped, out_path)
            total += size
            print("OK    %-46s <- %-34s %6.1f KB 裁 %s 主体 %d..%d 头顶余量 %d"
                  % (out_name, os.path.basename(src), size / 1024.0, info["crop_y"],
                     info["subject_top"], info["subject_bottom"], info["head_room"]))
        n_ok += 1
        report.append({"out": out_name, "src": os.path.basename(src), "size": [w, h], **info})

    with open(os.path.join(ROOT, "scripts", "output", "_w988_assets.json"), "w", encoding="utf-8") as fh:
        json.dump(report, fh, ensure_ascii=False, indent=1)

    print("\n合计：派生 %d 张 · 跳过 %d 张 · 合计 %.1f MB"
          % (n_ok, n_skip, total / 1048576.0))
    return 0


if __name__ == "__main__":
    sys.exit(main())
