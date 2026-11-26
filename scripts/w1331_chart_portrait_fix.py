#!/usr/bin/env python3
"""_w1331_chart_portrait_fix.py — W1331 竖版图表根修注入（一次性·可重复运行）。

输入：scripts/output/_w1331_chart_portrait_report.json（375 竖版探针）
动作：对「被压缩到不可读」的图表 svg，在页面 </head> 前注入窄屏规则块：

  <style data-w1331="1">
  /* W1331 chart-portrait v1 */
  @media (max-width: 768px) {
    #radar-svg { min-width: 560px; }          /* 保持 1:1 可读比例，容器横向滚动 */
    section:has(> #sankey) { overflow-x: auto; }  /* 父容器不可滚时补滚动轴 */
  }
  </style>

判据：compressed = effFs < 9.5 或 scale < 0.75；容器已有 overflow-x:auto/scroll 的
不补滚动规则；无静态 svg id 的条目记入 skipped（不猜选择器）。
用法：
  py -3 scripts/_w1331_chart_portrait_fix.py --dry
  py -3 scripts/_w1331_chart_portrait_fix.py
  py -3 scripts/_w1331_chart_portrait_fix.py --revert   # 移除本批注入块
"""
import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT = os.path.join(ROOT, "scripts", "output", "_w1331_chart_portrait_report.json")
MARK = "W1331 chart-portrait v1"
BLOCK_RE = re.compile(r'\n?<style data-w1331="1">.*?</style>\n?', re.S)

# 动态 svg（源码无静态标签）与微压缩图的手工锚点：页 → [(svg选择器, vbw, 需补滚动的容器选择器或 None)]
MANUAL = {
    "data/graph-explorer.html": [("#graphBox > svg", 900, None)],
    # 竖屏 7.8px（FAIL 线 8）——双小图必须保 1:1
    "data/dialogue-sentiment.html": [("#chart-word-positive", 350, None), ("#chart-word-negative", 350, None)],
    "en/dialogue-sentiment.html": [("#chart-word-positive", 350, None), ("#chart-word-negative", 350, None)],
    # 320 视口 7.2px（FAIL 线 8）——竖向堆叠柱保 1:1
    "data/hardship-heatmap.html": [("#cause-bar-svg", 360, None)],
    "en/hardship-heatmap.html": [("#cause-bar-svg", 360, None)],
}


def rd(p):
    with open(p, encoding="utf-8", errors="ignore") as f:
        return f.read()


def wr(p, t):
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(t)


def problems(report_path=None):
    """返回 {page: {"compressed": [...], "overflow": [...]}}。

    两类判据（与探针 grade 的 FAIL 线同源）：
      compressed = effFs < 8 或 scale < 0.6（窄屏被压到不可读 ⇒ min-width 兜底；
                   WARN 级 8–9.5px 只记录不修，避免给响应式小图强加 min-width）
      overflow   = outOfViewport > 0（标签画到 svg 外且越出视口 ⇒ overflow:visible + 容器可滚）
    """
    d = json.load(open(report_path or REPORT, encoding="utf-8"))
    out = {}
    for rec in d["pages"]:
        comp, ovf = [], []
        for c in rec.get("svgCharts", []):
            if (c["effFs"] is not None and c["effFs"] < 8.0) or (c.get("scale") or 1) < 0.6:
                comp.append(c)
            if c.get("outOfViewport"):
                ovf.append(c)
        if comp or ovf:
            out[rec["page"]] = {"compressed": comp, "overflow": ovf}
    return out


def build_block(t, items, rel="", base_rules=None):
    """按页生成窄屏规则块；返回 (block, applied, skipped)。

    选择器优先级：静态 svg id → svg class（同页同类合并取最大 vbw）→ 父容器 class
    （`.parent > svg`，同父合并取最大 vbw）→ 跳过（不猜）。
    越界类：`#id { overflow: visible }` + 父容器补滚动（`*:has(> #id)`）。
    """
    rules, applied, skipped = [], [], []
    by_sel = {}  # selector -> {"minw": int, "ids": [...], "was": {...}}
    seen_rule = set()

    def push(rule):
        if rule not in seen_rule:
            seen_rule.add(rule)
            rules.append(rule)

    # 先继承旧块规则（同页两类问题分阶段修复时，后一次重建不能丢掉前一次的规则）
    for r in base_rules or []:
        push(r)

    for c in items.get("compressed", []):
        sid = c.get("id") or ""
        cls = (c.get("cls") or "").strip()
        parent = (c.get("parentCls") or "").strip().split()[0] if (c.get("parentCls") or "").strip() else ""
        vbw = int(c.get("vbw") or 0)
        if vbw <= 0:
            skipped.append({"id": sid, "why": "vbw=0"})
            continue
        if sid and re.search(r'<svg[^>]*\bid="%s"' % re.escape(sid), t):
            sel = "#" + sid
        elif cls and re.search(r'<svg[^>]*\bclass="[^"]*\b%s\b' % re.escape(cls), t):
            sel = "." + cls
        elif parent and re.search(r'class="[^"]*\b%s\b' % re.escape(parent), t):
            sel = "." + parent + " > svg"
        else:
            skipped.append({"id": sid or "(no-id)", "cls": cls, "parent": parent, "why": "无可定位选择器"})
            continue
        ent = by_sel.setdefault(sel, {"minw": 0, "ids": [], "was": None})
        ent["minw"] = max(ent["minw"], vbw)
        ent["ids"].append(sid or cls or parent)
        ent["was"] = (c.get("scale"), c.get("effFs"))
        # 容器不可滚 → 用 *:has() 精确给父容器补滚动轴
        if not c.get("scroll"):
            push('    *:has(> %s) { overflow-x: auto; }' % sel)
    for sel, ent in by_sel.items():
        push('    %s { min-width: %dpx; }' % (sel, ent["minw"]))
        applied.append({"sel": sel, "min_width": ent["minw"], "ids": ent["ids"], "was": ent["was"]})

    # 越界类：标签画到 svg 外 ⇒ 窄屏放开裁剪，父容器可横向滚动到达
    for c in items.get("overflow", []):
        sid = c.get("id") or ""
        if not sid or not re.search(r'<svg[^>]*\bid="%s"' % re.escape(sid), t):
            skipped.append({"id": sid or "(no-id)", "cls": c.get("cls"), "why": "越界项无可定位 svg id"})
            continue
        sel = "#" + sid
        if not c.get("scroll"):
            push('    *:has(> %s) { overflow-x: auto; }' % sel)
        push('    %s { overflow: visible; }' % sel)
        applied.append({"sel": sel, "mode": "overflow-visible", "ids": [sid],
                        "was": (c.get("scale"), c.get("effFs"))})

    for sel, minw, scroll_sel in MANUAL.get(rel, []):
        if scroll_sel:
            push('    %s { overflow-x: auto; }' % scroll_sel)
        push('    %s { min-width: %dpx; }' % (sel, minw))
        applied.append({"sel": sel, "min_width": minw, "ids": ["(manual)"], "was": None})

    if not rules:
        return None, applied, skipped
    block = ('<style data-w1331="1">\n/* %s */\n@media (max-width: 768px) {\n%s\n}\n</style>\n'
             % (MARK, "\n".join(rules)))
    return block, applied, skipped


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--revert", action="store_true")
    ap.add_argument("--only", nargs="*", default=None)
    ap.add_argument("--report", default=None, help="探针报告路径（默认 _w1331_chart_portrait_report.json）")
    args = ap.parse_args()

    probs = problems(args.report)
    if args.only:
        probs = {k: v for k, v in probs.items() if k in args.only}
    # MANUAL 页即使探针不再报问题也要重建（保证手工规则在位）
    if not args.only:
        for rel in MANUAL:
            probs.setdefault(rel, {"compressed": [], "overflow": []})
    total_pages = changed = 0
    report = {"applied": {}, "skipped": {}, "reverted": []}
    for rel, items in sorted(probs.items()):
        path = os.path.join(ROOT, "site", rel.replace("/", os.sep))
        if not os.path.exists(path):
            continue
        total_pages += 1
        t = rd(path)
        if args.revert:
            t2 = BLOCK_RE.sub("\n", t, count=1)
            if t2 != t:
                report["reverted"].append(rel)
                if not args.dry:
                    wr(path, t2)
            continue
        # 继承旧块规则（分阶段修复时后一次重建不丢前一次成果）
        m = BLOCK_RE.search(t)
        base_rules = []
        if m:
            for ln in m.group(0).splitlines():
                if ln.startswith("    ") and ";" in ln:  # 规则行缩进 4 空格（勿 strip 后判断）
                    base_rules.append(ln)
        block, applied, skipped = build_block(t, items, rel, base_rules)
        if applied:
            report["applied"][rel] = applied
        if skipped:
            report["skipped"][rel] = skipped
        if block:
            # 先移除旧块再插入（幂等）
            base = BLOCK_RE.sub("\n", t, count=1)
            if "</head>" not in base:
                report["skipped"].setdefault(rel, []).append({"why": "缺 </head>"})
                continue
            new = base.replace("</head>", block + "</head>", 1)
            changed += 1
            if not args.dry:
                wr(path, new)
    out = os.path.join(ROOT, "scripts", "output", "_w1331_chart_portrait_fix.json")
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(report, f, ensure_ascii=False, indent=1)
    print("候选页 %d · 注入页 %d%s" % (total_pages, changed, "（dry-run）" if args.dry else ""))
    for rel, items in report["applied"].items():
        print("  %s: %s" % (rel, ", ".join(
            ("%s→%dpx" % (i["sel"], i["min_width"])) if "min_width" in i else ("%s→overflow-visible" % i["sel"])
            for i in items)))
    for rel, items in report["skipped"].items():
        for i in items:
            print("  [skip] %s: %s" % (rel, json.dumps(i, ensure_ascii=False)))
    print("账本：scripts/output/_w1331_chart_portrait_fix.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
