#!/usr/bin/env python3
"""_w988_inventory.py — W988 前置盘点（只读·不改任何文件）

盘点两块：
  A. 全站 og:image 现状（写法变体 / 取值分布 / 缺页）
  B. 可落位页清单（people/themes/reader 各库）·每页已有 plate / scene / banner 状态

输出：scripts/output/_w988_inventory.json
"""
from __future__ import annotations

import glob
import json
import os
import re
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "scripts", "output", "_w988_inventory.json")

RE_META = re.compile(r"<meta[^>]*og:image[^>]*>", re.I)
RE_CONTENT = re.compile(r"content=[\"']([^\"']+)[\"']", re.I)


def read(p: str) -> str:
    with open(p, encoding="utf-8", errors="ignore") as fh:
        return fh.read()


def rel(p: str) -> str:
    return os.path.relpath(p, ROOT).replace("\\", "/")


def main() -> None:
    files = sorted(glob.glob(os.path.join(ROOT, "site", "**", "*.html"), recursive=True))

    # ---------- A. og:image ----------
    og_vals: Counter = Counter()
    og_first: dict[str, str] = {}
    og_pages: dict[str, list[str]] = defaultdict(list)
    meta_shapes: Counter = Counter()
    no_og: list[str] = []
    for f in files:
        s = read(f)
        tags = RE_META.findall(s)
        if not tags:
            no_og.append(rel(f))
            continue
        for t in tags:
            shape = re.sub(r"content=[\"'][^\"']*[\"']", "content=..", t)
            shape = re.sub(r"\s+", " ", shape).strip()
            meta_shapes[shape] += 1
            m = RE_CONTENT.search(t)
            if m:
                og_vals[m.group(1)] += 1
                og_first.setdefault(m.group(1), rel(f))
                og_pages[m.group(1)].append(rel(f))

    # ---------- B. 页面清单 ----------
    pages = []
    for f in files:
        r = rel(f)
        s = read(f)
        h1 = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
        title = re.search(r"<title[^>]*>(.*?)</title>", s, re.S)
        lib = r.split("/")[2] if r.startswith("site/reader/") else r.split("/")[1]
        pages.append({
            "path": r,
            "lib": lib,
            "h1": re.sub(r"<[^>]+>", "", h1.group(1)).strip() if h1 else "",
            "title": re.sub(r"<[^>]+>", "", title.group(1)).strip() if title else "",
            "has_plate": "chapter-plate" in s,
            "has_scene": "chapter-scene" in s,
            "has_banner": "chapter-banner" in s,
            "og": next((RE_CONTENT.search(t).group(1) for t in RE_META.findall(s)
                        if RE_CONTENT.search(t)), None),
        })

    by_lib: Counter = Counter()
    for p in pages:
        by_lib[p["lib"]] += 1

    data = {
        "pages_total": len(pages),
        "by_lib": dict(by_lib),
        "og": {
            "distinct_values": len(og_vals),
            "values": [{"value": k, "count": v, "first_page": og_first[k]} for k, v in og_vals.most_common()],
            "meta_shapes": dict(meta_shapes),
            "pages_without_og": len(no_og),
            "pages_without_og_sample": no_og[:30],
        },
        "flags": {
            "plate_pages": sum(1 for p in pages if p["has_plate"]),
            "scene_pages": sum(1 for p in pages if p["has_scene"]),
            "banner_pages": sum(1 for p in pages if p["has_banner"]),
        },
        "pages": pages,
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)

    print("pages_total =", len(pages), "| by_lib =", dict(by_lib))
    print("og distinct =", len(og_vals), "| 无 og 的页 =", len(no_og))
    for v in og_vals.most_common():
        print("   ", v[1], v[0], "| 例:", og_first[v[0]])
    print("meta shapes:")
    for k, v in meta_shapes.most_common():
        print("   ", v, k)
    print("plate/scene/banner 页数 =", data["flags"])
    print("写出:", rel(OUT))


if __name__ == "__main__":
    main()
