#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_w826_container_survey.py — 容器宽度现状分布（一次性取证脚本·只读）

口径：按目录统计页面内联/外链 CSS 中出现的 max-width 声明取值组合，
输出 v4「容器三档」迁移映射的现状底数。
"""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
WIDTH_RE = re.compile(r"max-width:\s*(\d+)px")
# 视口宽度型（媒体查询内）不计
CONTAINER_RE = re.compile(r"\.([a-z0-9-]*(?:container|wrap|page-wrap)[a-z0-9-]*)\s*\{([^}]*)\}", re.I)


def main() -> int:
    groups: dict[str, Counter] = {}
    per_page: dict[str, list[str]] = {}
    for d in ["data", "en", "reader", "(root)"]:
        groups[d] = Counter()
    for f in sorted(SITE.rglob("*.html")):
        rel = f.relative_to(SITE).as_posix()
        grp = rel.split("/")[0] if "/" in rel else "(root)"
        html = f.read_text(encoding="utf-8", errors="replace")
        # 只看容器类选择器里的 max-width（排除媒体查询内的视口宽）
        widths = []
        for m in CONTAINER_RE.finditer(html):
            for w in WIDTH_RE.findall(m.group(2)):
                widths.append(w)
        key = ",".join(sorted(set(widths))) or "(无内联容器声明)"
        groups.setdefault(grp, Counter())[key] += 1
        per_page[rel] = sorted(set(widths))

    out = {"groups": {k: dict(v) for k, v in groups.items()}, "per_page_container_widths": per_page}
    p = ROOT / "scripts" / "output" / "_w826_container_survey.json"
    p.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print("=== 容器宽度现状分布（按目录） ===")
    for grp, c in groups.items():
        total = sum(c.values())
        print(f"\n[{grp}] 共 {total} 页")
        for k, v in c.most_common():
            print(f"   {v:>4} 页  max-width = {k}")
    print(f"\nJSON：{p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
