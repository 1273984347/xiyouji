# -*- coding: utf-8 -*-
"""W1100 补充：档 3（调色板色口径）逐页 × 层分布 + 补偿规则明细 ⇒ 切批依据。"""
import collections
import io
import json
import os
import pathlib
import re

HEX12 = ["C8463A", "E46250", "3A6B8C", "6B8E5A", "B38F58", "D8CFBC",
         "8A6D3B", "E9B885", "7FA8C9", "E0604F", "C9A96B", "9DB98A"]
PAL = set(h.lower() for h in HEX12)
ANY = r"#[0-9a-fA-F]{6}"

# W1113 实证·E-138：L4 原正则要求色值带引号 ⇒ HTML 内联 style 的**无引号形态**
# （style= background:#c8463a）漏判 ⇒ 「残留归零」成为**假零**（实测真残留 18 处·图例/色块 10 处
# + noscript/tooltip 8 处）⇒ 修法：引号改为**可选**·互斥归类优先序不变（L2 → L4 → L5·先命中者归层）。
LAYERS = [
    ("L2 echarts", re.compile(
        r"(color|colors|palette|itemStyle|backgroundColor|borderColor)\s*:\s*\[?\s*['\"](" + ANY + r")", re.I)),
    ("L4 CSS属性值", re.compile(
        r"(color|background|backgroundColor|borderColor|fill|stroke)\s*[:=]\s*(?:['\"])?(" + ANY + r")", re.I)),
    ("L5 裸hex", re.compile(r"['\"](" + ANY + r")", re.I)),
]

COMP = [
    ("C1前缀型", re.compile(r"\[fill\^=", re.I)),
    ("C2字面值型", re.compile(r"\[fill\s*=\s*['\"]?#", re.I)),
]


def find_root(start):
    p = pathlib.Path(start).resolve()
    for cand in [p] + list(p.parents):
        if (cand / "site").is_dir() and (cand / "scripts").is_dir():
            return cand
    raise SystemExit("未找到仓库根")


def main():
    root = find_root(pathlib.Path(__file__).resolve().parent)
    site = root / "site"
    per = collections.defaultdict(collections.Counter)
    comp_pages = collections.Counter()
    comp_kind = collections.Counter()
    for dirpath, _d, files in os.walk(site):
        if any(p.startswith(".") for p in dirpath.split(os.path.sep)):
            continue
        for fn in files:
            if not fn.endswith(".html"):
                continue
            p = pathlib.Path(dirpath) / fn
            rel = str(p.relative_to(site)).replace("\\", "/")
            txt = p.read_text(encoding="utf-8", errors="ignore")
            for m in re.finditer(r"<[Ss][Cc][Rr][Ii][Pp][Tt]\b[^>]*>(.*?)</[Ss][Cc][Rr][Ii][Pp][Tt][^>]*>", txt, re.S | re.I):
                js = m.group(1)
                spans = []
                for name, rx in LAYERS:
                    for mm in rx.finditer(js):
                        gi = mm.re.groups
                        s, e = mm.span(gi)
                        if any(not (e <= a or s >= b) for a, b in spans):
                            continue
                        spans.append((s, e))
                        hexv = mm.group(gi).lower()
                        if hexv[1:] in PAL:
                            per[rel][name] += 1
            styles = "\n".join(x.group(1) for x in
                               re.finditer(r"<[Ss][Tt][Yy][Ll][Ee]\b[^>]*>(.*?)</[Ss][Tt][Yy][Ll][Ee][^>]*>", txt, re.S | re.I))
            for name, rx in COMP:
                n = len(rx.findall(styles))
                if n:
                    comp_kind[name] += n
                    comp_pages[rel] += n

    total = sum(sum(c.values()) for c in per.values())
    print("=== 档 3（调色板色·互斥归类）逐页分布：%d 页 / %d 处 ===" % (len(per), total))
    agg = sorted(((rel, sum(c.values()), dict(c)) for rel, c in per.items()),
                  key=lambda x: (-x[1], x[0]))
    for rel, n, c in agg[:30]:
        print("   %-46s %4d  %s" % (rel, n, c))
    print("\n--- 页数分档（切批建议用·≤10 页/批）---")
    buckets = collections.Counter()
    for rel, n, c in agg:
        buckets[n // 10 * 10 + 10] += 1
    for k in sorted(buckets):
        print("   每页 %3d-%3d 处：%3d 页" % (k - 9, k, buckets[k]))
    print("\n=== 补偿规则形态 ===")
    for name, _rx in COMP:
        print("   %-12s %5d 条" % (name, comp_kind.get(name, 0)))
    print("   含补偿规则页数：%d" % len(comp_pages))
    print("   top 10 页：")
    for rel, n in comp_pages.most_common(10):
        print("      %-46s %3d 条" % (rel, n))

    dst = root / "scripts" / "output" / "_w1100_layer3_pages.json"
    with io.open(dst, "w", encoding="utf-8", newline="\n") as f:
        json.dump({"per_page": {k: dict(v) for k, v in per.items()},
                   "total": total, "page_count": len(per),
                   "comp_kind": dict(comp_kind),
                   "comp_pages": dict(comp_pages)}, f,
                  ensure_ascii=False, indent=1)
        f.write("\n")
    print("\n（落盘：scripts/output/_w1100_layer3_pages.json）")


if __name__ == "__main__":
    main()
