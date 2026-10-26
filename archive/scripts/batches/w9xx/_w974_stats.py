# -*- coding: utf-8 -*-
"""_w974_stats.py — 本批与全目录的实测汇总（README / 报告数字的唯一源头）

输出：scripts/output/_w974_stats.json
口径：
  · 母版 J1–J10 各项在本批 12 张 / 全目录 52 张上的实测区间
  · 站点版高度区间（批次内浮动 / 全目录浮动）
  · 题图覆盖页数

用法：py -3 scripts/_w974_stats.py
"""
import glob
import importlib.util
import json
import os
import re

REPO = r"D:\xiyouji"
SET_DIR = os.path.join(REPO, "assets", "promo", "plate-set")
SITE_IMG = os.path.join(REPO, "site", "static", "images")

spec = importlib.util.spec_from_file_location("v", os.path.join(REPO, "scripts", "_w945_plates_verify.py"))
V = importlib.util.module_from_spec(spec)
spec.loader.exec_module(V)

BATCH = [
    "plate-line-13-jinjiaodawang", "plate-line-14-yinjiaodawang",
    "plate-line-15-huangmeidawang", "plate-line-16-heixiongjing",
    "plate-line-17-tuota-lijing", "plate-line-18-yutujing",
    "plate-line-19-nvziguo-topic", "plate-line-20-chelingguo-topic",
    "plate-line-21-shituoling-topic", "plate-line-22-tonghehe-topic",
    "plate-line-23-pansidong-topic", "plate-line-24-wudidong-topic",
]


def measure(stem):
    from PIL import Image
    p = os.path.join(SET_DIR, stem + ".png")
    im = Image.open(p).convert("RGB")
    w, h = im.size
    site = os.path.join(SITE_IMG, stem + ".webp")
    sh = Image.open(site).size[1] if os.path.exists(site) else None
    return {
        "stem": stem,
        "size": "%dx%d" % (w, h),
        "top_ink": round(V.ink_ratio(im, (0, 0, w, int(h * 0.10))), 4),
        "whole_ink": round(V.ink_ratio(im), 4),
        "lower_ink": round(V.ink_ratio(im, (0, int(h * 0.28), w, h)), 4),
        "verm_px": V.near_px(im, V.VERM, V.VERM_TOL),
        "dense": round(V.max_dense_block(im, (0, int(h * 0.28), w, h)), 3),
        "paper_resid": round(V.paper_residual(im), 2),
        "bg_diff": round(V.bg_band_diff(im), 2),
        "site_h": sh,
    }


def rng(rows, key):
    vals = [r[key] for r in rows if r.get(key) is not None]
    return (min(vals), max(vals)) if vals else None


def main():
    all_stems = sorted(f[:-4] for f in os.listdir(SET_DIR)
                       if f.startswith("plate-line-") and f.endswith(".png"))
    batch_rows = [measure(s) for s in BATCH]
    all_rows = [measure(s) for s in all_stems]
    covered = 0
    for f in glob.glob(os.path.join(REPO, "site", "reader", "**", "*.html"), recursive=True):
        with open(f, "rb") as fh:
            if b"chapter-plate" in fh.read():
                covered += 1
    out = {
        "batch_stems": BATCH,
        "batch_count": len(BATCH),
        "all_masters": len(all_stems),
        "batch_metrics": {k: rng(batch_rows, k) for k in
                           ("top_ink", "whole_ink", "lower_ink", "verm_px", "dense", "paper_resid", "bg_diff")},
        "all_metrics": {k: rng(all_rows, k) for k in
                        ("top_ink", "whole_ink", "lower_ink", "verm_px", "dense", "paper_resid", "bg_diff")},
        "batch_site_h": rng(batch_rows, "site_h"),
        "all_site_h": rng(all_rows, "site_h"),
        "reader_pages_with_plate": covered,
        "batch_rows": batch_rows,
    }
    p = os.path.join(REPO, "scripts", "output", "_w974_stats.json")
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
    print("母版本批 %d 张 / 全目录 %d 张 · reader 有题图页 %d 页" % (
        len(BATCH), len(all_stems), covered))
    print("本批站点版高 %s · 全目录站点版高 %s" % (out["batch_site_h"], out["all_site_h"]))
    for k, v in out["batch_metrics"].items():
        print("  本批 %-12s %s" % (k, v))
    print("产出：scripts/output/_w974_stats.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
