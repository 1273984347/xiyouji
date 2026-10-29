# -*- coding: utf-8 -*-
"""_w1013_inventory.py — W1013 批盘点：回目页配图缺口 + 已出主体清单 + og:image 覆盖现状

复刻 W1001 批管线（W990 批 `_w990_og_gap.py` + `_w990_roster.py`），修三点：
  ① ROOT 推导（归档区 dirname×2 会算错 ⇒ 本批脚本在 scripts/ 根，dirname×2 正确）；
  ② 配图匹配**放宽**（不要求 figure 紧跟 img——W988 批坑表 E-21·盘点正则过严致覆盖数虚高）；
  ③ 增列 og:image 现状（专属 og-cover vs 通用图）⇒ 扩量批的验收基线。

输出：scripts/output/_w1013_inventory.json
用法：py -3 scripts/_w1013_inventory.py
"""
import glob
import io
import json
import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "scripts", "output", "_w1013_inventory.json")
PLATE_README = os.path.join(REPO, "assets", "promo", "plate-set", "README.md")


def main() -> int:
    rows = []
    for f in sorted(glob.glob(os.path.join(REPO, "site", "reader", "ch*.html"))):
        s = io.open(f, encoding="utf-8", errors="ignore").read()
        rel = os.path.relpath(f, REPO).replace("\\", "/")
        h1 = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
        # 宽松匹配：figure 块内取第一张 img（不要求紧跟 <img src=）
        def _fig_img(cls):
            blk = re.search(r'<figure class="%s"[^>]*>(.*?)</figure>' % cls, s, re.S)
            if not blk:
                return None
            im = re.search(r'<img[^>]+src="([^"]+)"', blk.group(1))
            return im.group(1).split("/")[-1] if im else None
        plate = _fig_img("chapter-plate")
        scene = _fig_img("chapter-scene")
        og = re.search(r'<meta property="og:image" content="([^"]+)"', s)
        og_file = og.group(1).split("/")[-1] if og else None
        rows.append({
            "page": rel,
            "ch": os.path.basename(f)[2:5],
            "title": re.sub(r"<[^>]+>", "", h1.group(1)).strip() if h1 else "",
            "plate": plate,
            "scene": scene,
            "og": og_file,
            "og_is_generic": bool(og_file and "og-cover" in og_file),
        })

    covered = [r for r in rows if r["plate"] or r["scene"]]
    gap = [r for r in rows if not r["plate"] and not r["scene"]]

    # 已出主体清单（plate-set README 表格：| `stem` | 描述 |）
    stems, descs = [], {}
    if os.path.exists(PLATE_README):
        txt = io.open(PLATE_README, encoding="utf-8").read()
        for a, b in re.findall(r"^\| `([^`]+)` \| ([^|]+) \|", txt, re.M):
            stems.append(a.strip())
            descs[a.strip()] = b.strip()
    else:
        print("[WARN] plate-set README 不存在：%s" % PLATE_README)

    data = {
        "chapters_total": len(rows),
        "with_plate_or_scene": len(covered),
        "gap_total": len(gap),
        "gap_still_generic_og": sum(1 for r in gap if r["og_is_generic"]),
        "gap": gap,
        "covered": covered,
        "roster_stems": stems,
        "roster_desc": descs,
    }
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(json.dumps(data, ensure_ascii=False, indent=1))

    print("回目页 %d · 已有配图 %d · 无配图缺口 %d · 缺口中仍用通用 og-cover %d"
          % (data["chapters_total"], data["with_plate_or_scene"], data["gap_total"],
             data["gap_still_generic_og"]))
    print("\n--- 缺口前 24 回 ---")
    for r in gap[:24]:
        print("  ch%s %-40s og=%s" % (r["ch"], r["title"][:40], r["og"] or "-"))
    print("  …（共 %d 回）" % len(gap))
    print("\n--- 已出 plate-set 主体 %d 个 ---" % len(stems))
    for a in stems:
        print("  %-42s %s" % (a, descs.get(a, "")[:60]))
    print("\n写出:", os.path.relpath(OUT, REPO).replace("\\", "/"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
