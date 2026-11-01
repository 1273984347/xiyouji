#!/usr/bin/env python3
"""_w1076_space_tokens.py — W1076 B1 手术 7：8 根页间距字面量 → v4 间距令牌。

## 口径（W826 §4 令牌终稿 + 任务书 §4 手术 7/8）

- **仅刻度内值**：0/2/4/8/12/20/24/32/40/48/64/80/96px → `var(--space-0..12)`
  （刻度外值 10/16/22/28/30/36/44/56/88px 等一律不动——规格卡未裁决·勿自创）；
- **仅 spacing 声明**：padding / margin / gap 及其长写（padding-top…margin-right）；
  font-size / border-radius / top / left 不在间距消费范围（任务书手术 8）；
- **calc()/clamp() 内的 px 不替换**（任务书手术 8）——被保护区间内的字面量原样保留；
- **负值不替换**（`-20px` → `-var(--space-5)` 是非法 CSS）——保留原字面量并登记；
- 替换在 `<style>` 块内进行（内联 `style=""` 属性不计入任务书 82 处口径）。

## 幂等与换行

- 幂等：已替换的 `var(--space-N)` 不含 px → 二次运行命中 0；
- 换行：读用 `newline=""`、写用 `newline=""`（Windows 文本模式会把 `\n` 转 `\r\n`·
  与 `.gitattributes` 的 `text=auto eol=lf` 契约背离——W1022 实证）。

用法：
    python scripts/_w1076_space_tokens.py --check     # 只报告不落盘
    python scripts/_w1076_space_tokens.py --apply     # 落盘
"""
import argparse
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
PAGES = ["index", "guide", "curated", "dashboard", "dukou-engine",
         "rum-viewer", "visit-viewer", "404"]

# W826 §4 间距刻度：px 值 → --space-N 的 N
SCALE = {0: 0, 2: 1, 4: 2, 8: 3, 12: 4, 20: 5, 24: 6, 32: 7, 40: 8, 48: 9,
         64: 10, 80: 11, 96: 12}

SPACING_PROPS = (
    "padding-top", "padding-right", "padding-bottom", "padding-left",
    "margin-top", "margin-right", "margin-bottom", "margin-left",
    "row-gap", "column-gap", "padding", "margin", "gap",
)
DECL_RE = re.compile(
    r"(?<![\w-])(%s)\s*:\s*([^;{}]+);" % "|".join(SPACING_PROPS))
PX_RE = re.compile(r"(?<![\w.])(\d+(?:\.\d+)?)px")
FUNC_RE = re.compile(r"\b(?:clamp|calc|min|max)\([^()]*\)")
STYLE_RE = re.compile(r"(<style[^>]*>)(.*?)(</style>)", re.S)

# 404.html 是自含小页（不链接 tokens.css）——页内 :root 副本须补足被用到的两个刻度
FOUR04_ROOT_OLD = ":root { --space-6: 24px; --space-8: 40px; --space-9: 48px; }"
FOUR04_ROOT_NEW = (":root { --space-3: 8px; --space-4: 12px; --space-6: 24px; "
                    "--space-8: 40px; --space-9: 48px; }")


def _protected_spans(value):
    return [(m.start(), m.end()) for m in FUNC_RE.finditer(value)]


def _in_protected(pos, spans):
    return any(s <= pos < e for s, e in spans)


def convert_value(value):
    """返回 (新值, 替换数, 跳过明细)。"""
    spans = _protected_spans(value)
    out, last, hits, skipped = [], 0, 0, []

    def _sub(m):
        nonlocal last, hits
        raw, num = m.group(0), m.group(1)
        start = m.start()
        if _in_protected(start, spans):
            skipped.append(("calc/clamp 内", raw, value.strip()))
            return raw
        if start > 0 and value[start - 1] == "-":
            skipped.append(("负值", raw, value.strip()))
            return raw
        if float(num) != int(num) or int(num) not in SCALE:
            return raw
        hits += 1
        return "var(--space-%d)" % SCALE[int(num)]

    new = PX_RE.sub(_sub, value)
    return new, hits, skipped


def process(path):
    with open(path, encoding="utf-8", newline="") as fh:
        html = fh.read()
    stats = {"candidates": 0, "replaced": 0, "skipped": [], "page": os.path.basename(path)}

    def _style_sub(m):
        body = m.group(2)

        def _decl_sub(dm):
            prop, value = dm.group(1), dm.group(2)
            candidates = len(PX_RE.findall(value))
            new, hits, skipped = convert_value(value)
            stats["candidates"] += candidates
            stats["replaced"] += hits
            for why, raw, ctx in skipped:
                stats["skipped"].append(
                    {"prop": prop, "value": ctx, "literal": raw, "reason": why})
            if hits == 0:
                return dm.group(0)
            return "%s: %s;" % (prop, new)

        return m.group(1) + DECL_RE.sub(_decl_sub, body) + m.group(3)

    new_html = STYLE_RE.sub(_style_sub, html)
    return html, new_html, stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--report", default="")
    ns = ap.parse_args()

    total = {"candidates": 0, "replaced": 0}
    report = []
    for p in PAGES:
        path = os.path.join(SITE, p + ".html")
        old, new, stats = process(path)
        if p == "404" and ns.apply:
            if FOUR04_ROOT_OLD not in new:
                raise SystemExit("404.html 的 :root 副本形态与预期不符——拒绝盲改")
            new = new.replace(FOUR04_ROOT_OLD, FOUR04_ROOT_NEW)
        stats["changed"] = old != new
        if ns.apply and old != new:
            with open(path, "w", encoding="utf-8", newline="") as fh:
                fh.write(new)
        total["candidates"] += stats["candidates"]
        total["replaced"] += stats["replaced"]
        report.append(stats)
        print("%-18s 候选 %3d · 替换 %3d · 跳过 %d · 文件变化=%s"
              % (p + ".html", stats["candidates"], stats["replaced"],
                 len(stats["skipped"]), stats["changed"]))
        for s in stats["skipped"]:
            print("      跳过(%s): %s → %s" % (s["reason"], s["literal"], s["value"][:70]))

    print("---- 合计：候选 %d · 实际替换 %d（差 %d 处为任务书手术 8 排除项）----"
          % (total["candidates"], total["replaced"],
             total["candidates"] - total["replaced"]))
    if ns.report:
        with open(ns.report, "w", encoding="utf-8", newline="") as fh:
            json.dump({"pages": report, "total": total}, fh,
                      ensure_ascii=False, indent=2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
