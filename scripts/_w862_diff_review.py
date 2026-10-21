#!/usr/bin/env python3
"""_w862_diff_review.py — W862 B1 迁移 diff 归渠审查（一次性件）。

迁移批的验收不是「零差异」而是「**有据变化**」：每处 diff 必须能归因到
W826 规格条目（A 容器归并 / B 朱砂合规 / C 对比度修法 / D 间距令牌化
=零视觉变化不应产生 diff）。本脚本把前后快照的全量 diff 按
（页 × 主题 × 类型 × 属性 × 前值→后值）聚合，输出可逐条核对的清单。

判定辅助：D 令牌化若值保留正确，不应产生任何 diff——出现的 diff 只能
来自 A/B/C 三渠。
"""

import json
import os
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "scripts", "output", "_w862_diff_review.json")

PROPS = None  # 由 before 快照载入


def _load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def diff_all(before, after):
    """全量 diff（不截断）→ [(page, theme, kind, prop, before, after, element)]。"""
    global PROPS
    PROPS = before["props"]
    diffs = []
    bp, ap = before["pages"], after["pages"]
    for rel in sorted(set(bp) & set(ap)):
        for theme in sorted(set(bp[rel]) & set(ap[rel])):
            eb, ea = bp[rel][theme], ap[rel][theme]
            if len(eb) != len(ea):
                diffs.append((rel, theme, "元素数", None, len(eb), len(ea), None))
            for i, (rb, ra) in enumerate(zip(eb, ea, strict=False)):
                if rb == ra:
                    continue
                if rb[:2] != ra[:2]:
                    diffs.append((rel, theme, "元素身份", None,
                                  str(rb[:2]), str(ra[:2]), i))
                else:
                    for pi in range(2, len(PROPS) + 2):
                        if rb[pi] != ra[pi]:
                            diffs.append((rel, theme, "属性", PROPS[pi - 2],
                                          rb[pi], ra[pi], "%s.%s" % (rb[0], rb[1])))
    return diffs


def main():
    global OUT
    argv = [x for x in sys.argv[1:] if x != "--out"]
    if "--out" in sys.argv:
        OUT = os.path.join(ROOT, sys.argv[sys.argv.index("--out") + 1])
    b = _load(argv[0])
    a = _load(argv[1])
    diffs = diff_all(b, a)
    # 聚合：page × theme × kind × prop × before→after
    groups = defaultdict(lambda: {"count": 0, "elements": []})
    for rel, theme, kind, prop, bv, av, el in diffs:
        key = (rel, theme, kind, prop, bv, av)
        g = groups[key]
        g["count"] += 1
        if el and len(g["elements"]) < 3:
            g["elements"].append(el)
    report = {
        "batch": "W862",
        "total_diffs": len(diffs),
        "pages_with_diffs": sorted({d[0] for d in diffs}),
        "groups": [
            {"page": k[0], "theme": k[1], "kind": k[2], "prop": k[3],
             "before": k[4], "after": k[5], "count": v["count"],
             "sample_elements": v["elements"]}
            for k, v in sorted(groups.items(),
                               key=lambda kv: -kv[1]["count"])
        ],
    }
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("总 diff %d 处·涉及页：%s" % (len(diffs),
          "、".join(report["pages_with_diffs"]) or "无"))
    for g in report["groups"][:25]:
        print("  %-26s %-5s %-4s %-18s %s → %s ×%d"
              % (g["page"], g["theme"], g["kind"], str(g["prop"]),
                 str(g["before"])[:24], str(g["after"])[:24], g["count"]))
    if len(report["groups"]) > 25:
        print("  …共 %d 组（全文见 %s）"
              % (len(report["groups"]), os.path.relpath(OUT, ROOT)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
