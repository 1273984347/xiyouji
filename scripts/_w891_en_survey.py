#!/usr/bin/env python3
"""_w891_en_survey.py — W891 前置盘点（A 渠容器值 / nav-back 变体 / D 渠可令牌化量）。

只读取，不写盘。结果打印供迁移脚本定参。
"""
import collections
import os
import re

EN = "site/en"

VAL = re.compile(r"max-width:\s*(\d+)px")
NAV = re.compile(r"\.nav-back\s*\{([^}]*)\}")
NAV_HOVER = re.compile(r"\.nav-back:hover\s*\{([^}]*)\}")
SPACING = re.compile(r"(padding|margin)(?:-top|-right|-bottom|-left)?:\s*([^;{}]+);")


def main():
    vals = collections.Counter()
    special = []
    nav_variants = collections.Counter()
    nav_pages = []
    sp_total = 0
    scale = {"2px", "4px", "8px", "12px", "20px", "24px", "32px", "40px", "48px", "64px", "80px", "96px"}
    for fn in sorted(os.listdir(EN)):
        if not fn.endswith(".html"):
            continue
        s = open(os.path.join(EN, fn), encoding="utf-8").read()
        m = collections.Counter(VAL.findall(s))
        for k, n in m.items():
            vals[k] += n
        if any(k in ("1024", "1280", "1536", "768") for k in m):
            special.append((fn, dict(m)))
        nm = NAV.search(s)
        if nm:
            nav_pages.append(fn)
            body = nm.group(1)
            bg = re.search(r"background:\s*([^;]+);", body)
            col = re.search(r"(?<!-)color:\s*([^;]+);", body)
            nav_variants[(bg.group(1).strip() if bg else "-", col.group(1).strip() if col else "-")] += 1
        # 页级（INLINED 块外）间距等值字面量计数
        body = s
        if "<!-- INLINED CSS" in s:
            st = s.find("<!-- INLINED CSS")
            end = s.find("</style>", st)
            body = s[:st] + s[end:]
        for mm in SPACING.finditer(body):
            for tok in mm.group(2).split():
                if tok in scale:
                    sp_total += 1
    print("max-width 值分布（处）:", dict(vals.most_common()))
    print("含 1024/1280/1536/768 的页:", len(special))
    for fn, v in special:
        print("  ", fn, v)
    print("nav-back 页数:", len(nav_pages))
    print("nav-back 变体（background, color）:")
    for k, n in nav_variants.most_common():
        print("  ", k, n)
    print("页级间距刻度内字面量（可令牌化·值保留）:", sp_total, "处")


if __name__ == "__main__":
    main()
