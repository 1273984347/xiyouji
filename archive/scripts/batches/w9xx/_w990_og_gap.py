import glob
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "scripts", "output", "_w990_og_gap.json")

rows = []
for f in sorted(glob.glob(os.path.join(ROOT, "site", "reader", "ch*.html"))):
    s = open(f, encoding="utf-8", errors="ignore").read()
    rel = os.path.relpath(f, ROOT).replace("\\", "/")
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
    m = re.search(r'<figure class="chapter-plate">\s*<img src="([^"]+)"', s)
    sc = re.search(r'<figure class="chapter-scene">\s*<img src="([^"]+)"', s)
    og = re.search(r'<meta property="og:image" content="([^"]+)"', s)
    rows.append({
        "page": rel,
        "ch": os.path.basename(f)[2:5],
        "title": re.sub(r"<[^>]+>", "", h1.group(1)).strip() if h1 else "",
        "plate": m.group(1).split("/")[-1] if m else None,
        "scene": sc.group(1).split("/")[-1] if sc else None,
        "og": og.group(1).split("/")[-1] if og else None,
        "og_is_cover": bool(og and "og-cover" in og.group(1)),
    })

covered = [r for r in rows if r["plate"] or r["scene"]]
gap = [r for r in rows if not r["plate"] and not r["scene"]]
gap_og_cover = [r for r in gap if r["og_is_cover"]]

data = {
    "chapters_total": len(rows),
    "with_plate_or_scene": len(covered),
    "covered": covered,
    "gap_total": len(gap),
    "gap": gap,
    "gap_still_cover_og": len(gap_og_cover),
}
with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(data, fh, ensure_ascii=False, indent=1)

print("回目页 %d 个 · 已有配图 %d · 无配图缺口 %d"
      % (data["chapters_total"], data["with_plate_or_scene"], data["gap_total"]))
print("\n--- 已有配图的回（%d）---" % len(covered))
for r in covered:
    print("  ch%s %-34s plate=%-32s scene=%s" % (r["ch"], r["title"][:34], r["plate"] or "-", r["scene"] or "-"))
print("\n--- 缺口前 20 回 ---")
for r in gap[:20]:
    print("  ch%s %s" % (r["ch"], r["title"][:44]))
print("  …（共 %d 回）" % len(gap))
print("\n写出:", os.path.relpath(OUT, ROOT).replace("\\", "/"))
