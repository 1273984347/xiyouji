#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_w988_precheck.py — W988 接入前预检（只读·不写盘）

核对四件事：
  A. 27 张 card 源图：尺寸 + 主体带 + 1200×500 横幅裁切信息 + 1200×630 og 裁切信息
  B. 27 个落位页：存在性 / 已有 plate·scene·banner / CSS 规则有无 / <h1> 后紧邻内容 / 当前 og:image
  C. 81 个既有题图页：plate 源图 + og 裁切信息（页面不改动·只换 og:image）
  D. 汇总：og:image 待改页清单（唯一化后）

输出：scripts/output/_w988_precheck.json
"""
from __future__ import annotations

import json
import os
import re
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _w988_plan import ALL, BANNERS, SCENES  # noqa: E402
from _w988_subject import crop_band, subject_band  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "site", "static", "images")
OUT = os.path.join(ROOT, "scripts", "output", "_w988_precheck.json")
OG_W, OG_H = 1200, 630
BAN_W, BAN_H = 1200, 500

RE_H1 = re.compile(r"<h1[^>]*>.*?</h1>", re.S)
RE_H2 = re.compile(r"<h2[^>]*>.*?</h2>", re.S)
RE_OG = re.compile(r'<meta property="og:image" content="([^"]+)"')


def read(p: str) -> str:
    with open(p, encoding="utf-8", errors="ignore") as fh:
        return fh.read()


def plan_for(target: str):
    for item in ALL:
        if item["target"] == target:
            return item
    return None


def main() -> None:
    data = {"cards": [], "pages": [], "og_plan": [], "errors": []}
    BANNER_TARGETS = {b["target"] for b in BANNERS}

    # ---------- A. 27 张源图 ----------
    for item in ALL:
        item = dict(item)
        item["slot"] = "banner" if item["target"] in BANNER_TARGETS else "scene"
        src = os.path.join(IMG, item["card"] + ".webp")
        if not os.path.exists(src):
            data["errors"].append("源图缺失: " + src)
            continue
        im = Image.open(src).convert("RGB")
        top, bottom, npix = subject_band(im)
        rec = {"card": item["card"], "target": item["target"], "slot": item["slot"],
               "src_size": list(im.size), "subject_top": top, "subject_bottom": bottom,
               "subject_px": npix, "subject": item["subject"]}
        try:
            _, bi = crop_band(im, BAN_W, BAN_H, "banner")
            rec["banner_crop"] = bi
        except Exception as e:  # noqa: BLE001
            rec["banner_error"] = str(e)
            data["errors"].append("banner 裁切失败 %s: %s" % (item["card"], e))
        try:
            _, oi = crop_band(im, OG_W, OG_H, "og")
            rec["og_crop"] = oi
        except Exception as e:  # noqa: BLE001
            rec["og_error"] = str(e)
            data["errors"].append("og 裁切失败 %s: %s" % (item["card"], e))
        data["cards"].append(rec)

    # ---------- B. 27 个落位页 ----------
    seen_targets = set()
    for item in ALL:
        item = dict(item)
        item["slot"] = "banner" if item["target"] in BANNER_TARGETS else "scene"
        tp = os.path.join(ROOT, item["target"])
        if not os.path.exists(tp):
            data["errors"].append("目标页缺失: " + item["target"])
            continue
        if item["target"] in seen_targets:
            data["errors"].append("目标页重复: " + item["target"])
        seen_targets.add(item["target"])
        s = read(tp)
        h1 = RE_H1.search(s)
        h2 = RE_H2.search(s)
        after = s[h1.end():h1.end() + 160].strip() if h1 else ""
        og = RE_OG.search(s)
        data["pages"].append({
            "target": item["target"], "slot": item["slot"], "card": item["card"],
            "has_plate": "chapter-plate" in s, "has_scene": "chapter-scene" in s,
            "has_banner": "chapter-banner" in s,
            "css_plate": ".chapter-plate" in s, "css_scene": ".chapter-scene" in s,
            "css_banner": ".chapter-banner" in s,
            "h1_found": bool(h1), "h2_found": bool(h2),
            "after_h1": after[:120],
            "og_now": og.group(1) if og else None,
            "style_blocks": len(re.findall(r"<style", s)),
        })

    # ---------- C. 81 个既有题图页 ----------
    import glob
    plate_pages = []
    for f in sorted(glob.glob(os.path.join(ROOT, "site", "**", "*.html"), recursive=True)):
        s = read(f)
        m = re.search(r'<figure class="chapter-plate">\s*<img src="([^"]+)"', s)
        if not m:
            continue
        rel = os.path.relpath(f, ROOT).replace("\\", "/")
        src_rel = m.group(1)
        src_abs = os.path.normpath(os.path.join(os.path.dirname(f), src_rel))
        plate_pages.append({"page": rel, "img": src_rel, "img_abs": src_abs})
    data["plate_pages"] = len(plate_pages)

    # ---------- D. og:image 待改清单 ----------
    # 口径：og:image = 该页「首屏第一张配图」的 1200×630 裁切版
    og_seen = {}
    for item in ALL:
        item = dict(item)
        item["slot"] = "banner" if item["target"] in BANNER_TARGETS else "scene"
        pg = next((p for p in data["pages"] if p["target"] == item["target"]), None)
        if pg is None:
            continue
        if pg["has_plate"]:
            src_rel = None
            for pp in plate_pages:
                if pp["page"] == item["target"]:
                    src_rel = pp["img"]
                    break
            if src_rel:
                abs_p = os.path.normpath(os.path.join(os.path.dirname(
                    os.path.join(ROOT, item["target"])), src_rel))
                stem = os.path.splitext(os.path.basename(abs_p))[0]
                og_seen[item["target"]] = {"kind": "plate", "src": abs_p,
                                          "out": "og-" + stem + ".webp"}
                continue
        if item["slot"] == "banner":
            og_seen[item["target"]] = {"kind": "banner", "card": item["card"],
                                      "out": "og-banner-" + item["card"] + ".webp"}
        else:
            og_seen[item["target"]] = {"kind": "scene", "card": item["card"],
                                      "out": "og-scene-" + item["card"] + ".webp"}
    for pp in plate_pages:
        if pp["page"] in og_seen:
            continue
        stem = os.path.splitext(os.path.basename(pp["img_abs"]))[0]
        og_seen[pp["page"]] = {"kind": "plate", "src": pp["img_abs"], "out": "og-" + stem + ".webp"}

    data["og_plan"] = [{"page": k, **v} for k, v in sorted(og_seen.items())]
    data["og_pages"] = len(og_seen)

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)

    print("=== W988 预检 ===")
    print("源图核对 %d 张 · 落位页 %d 个 · 既有题图页 %d · og 待改页 %d"
          % (len(data["cards"]), len(data["pages"]), data["plate_pages"], data["og_pages"]))
    print("\n-- 27 张源图主体带与裁切 --")
    for c in data["cards"]:
        bc = c.get("banner_crop", {})
        print("  %-28s %-11s 主体 %4d..%-4d 横幅裁 %s 头顶余量 %s"
              % (c["card"], "%dx%d" % tuple(c["src_size"]), c["subject_top"], c["subject_bottom"],
                 bc.get("crop_y"), bc.get("head_room")))
    print("\n-- 落位页现状 --")
    for p in data["pages"]:
        flags = "".join(k[0].upper() for k in ("has_plate", "has_scene", "has_banner") if p[k])
        css = "".join(k[0].upper() for k in ("css_plate", "css_scene", "css_banner") if p[k])
        print("  %-8s img:%-5s css:%-5s h1:%-5s h2:%-5s  %s"
              % (p["slot"], flags or "-", css or "-", p["h1_found"], p["h2_found"], p["target"]))
    if data["errors"]:
        print("\n!! 错误 %d 条：" % len(data["errors"]))
        for e in data["errors"]:
            print("   ", e)
    print("\n写出:", os.path.relpath(OUT, ROOT).replace("\\", "/"))
    return 1 if data["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
