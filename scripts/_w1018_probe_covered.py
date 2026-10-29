# -*- coding: utf-8 -*-
"""_w1018_probe_covered.py — 查当前有配图的回目页与归属（本批 12 vs 其他）"""
import io
import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
READER = os.path.join(REPO, "site", "reader")
MINE = {"ch020", "ch024", "ch034", "ch043", "ch044", "ch049",
        "ch051", "ch064", "ch074", "ch091", "ch096", "ch008"}
PAT = re.compile(r'<figure class="chapter-(plate|scene)">\s*<img src="[^"]*/([^"]+)"')


def main() -> int:
    rows = []
    for fn in sorted(os.listdir(READER)):
        if not (fn.startswith("ch") and fn.endswith(".html")):
            continue
        s = io.open(os.path.join(READER, fn), encoding="utf-8", errors="ignore").read()
        m = PAT.search(s)
        if m:
            rows.append((fn[:5], m.group(2)))
    print("有配图 %d 回：" % len(rows))
    for ch, img in rows:
        print("  %s %s  %s" % ("【本批】" if ch in MINE else "      ", ch, img))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
