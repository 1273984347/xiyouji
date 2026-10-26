#!/usr/bin/env python3
"""_w876_c_text_swap.py — W876 C 渠规则级换色（一次性件）。

**做什么**：把全站审计（_w876_site_audit.json）里「朱砂文字落在 --bg 上」的
DOM 元素（排除 SVG text=图表数据文字）按**类名 → 规则**归集，把对应 CSS 规则里的
`color: var(--accent)` 换成 `var(--accent-text)`（#C8463A→#C7463A·5.93:1 on bg）。

**口径（边界写清）**：
- 只动 `color:` 声明，不动 border/background/box-shadow（3px 线与面填充另属 B 渠）；
- **规则级替换**：同一条规则若还命中 paper 上下文实例，一并换色——`--accent-text`
  在 paper 上同样过 AA（≥5.93:1），不做逐实例分裂（逐实例会碎成 inline style）；
- 无类名元素（SVG text 之外的散件）与找不到唯一规则的类 → 进「复评清单」不改。

用法：py -3 scripts/_w876_c_text_swap.py --dry|--apply
"""

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIT = os.path.join(ROOT, "scripts", "output", "_w876_site_audit.json")
REPORT = os.path.join(ROOT, "scripts", "output", "_w876_c_swap_report.json")

DECL = re.compile(r"(color\s*:\s*)var\(--accent\)")
BLOCK = re.compile(r"([^{}]+)\{([^{}]*)\}", re.S)


def swap_page(path, classes, dry, tags=()):
    """把含给定类名的选择器块里 color: var(--accent) 换成 --accent-text。"""
    s = open(path, encoding="utf-8").read()
    hits = []

    def repl(m):
        sel, body = m.group(1), m.group(2)
        hit = any(("." + c) in sel for c in classes)
        if not hit and tags:
            for t in tags:
                if re.search(r"(^|[\s,>])" + re.escape(t) + r"($|[\s,{:])", sel.strip()):
                    hit = True
                    break
        if not hit:
            return m.group(0)
        nb, n = DECL.subn(r"\1var(--accent-text)", body)
        if n:
            hits.append(sel.strip().replace("\n", " ")[:80])
            return sel + "{" + nb + "}"
        return m.group(0)

    new = BLOCK.sub(repl, s)
    if not dry and new != s:
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(new)
    return hits


def main(argv):
    dry = "--apply" not in argv
    audit_path = AUDIT
    if "--audit" in argv:
        audit_path = os.path.join(ROOT, argv[argv.index("--audit") + 1])
    audit = json.load(open(audit_path, encoding="utf-8"))
    report = {"dry": dry, "pages": {}, "review": []}
    total_rules = 0

    for rel, v in sorted(audit.items()):
        if rel.startswith("data/_") or rel.startswith("_"):
            continue  # 脚手架/模板页不动
        dom = [t for t in v["text_on_bg"] if t["tag"] != "text"]
        if not dom:
            continue
        classes = sorted({t["cls"].split()[0] for t in dom if t["cls"].strip()})
        unclassed = sum(1 for t in dom if not t["cls"].strip())
        tags = sorted({t["tag"] for t in dom if not t["cls"].strip()})
        path = os.path.join(ROOT, "site", rel)
        hits = swap_page(path, classes, dry, tags)
        total_rules += len(hits)
        report["pages"][rel] = {"classes": classes, "elements": len(dom),
                                "unclassed": unclassed, "rules": hits}
        if unclassed and not hits:
            report["review"].append({"page": rel, "reason": "无类名且标签规则未命中",
                                     "count": unclassed})

    json.dump(report, open(REPORT, "w", encoding="utf-8", newline="\n"),
              ensure_ascii=False, indent=1)
    print("[%s] 页 %d · 规则换色 %d 条 · 复评 %d 项"
          % ("DRY" if dry else "APPLY", len(report["pages"]), total_rules,
             len(report["review"])))
    for rel, x in list(report["pages"].items())[:12]:
        print("  %-44s 元素%3d 规则%d" % (rel, x["elements"], len(x["rules"])))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
