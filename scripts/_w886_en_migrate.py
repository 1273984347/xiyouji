#!/usr/bin/env python3
"""_w886_en_migrate.py — ④ en 迁移批驱动（B 渠机械化两步·一次性件·W886 建）。

**en 与 zh 数据页的差异决定做法**：en 页的 C 渠换色可直接复用 `_w876_c_text_swap.py`
（审计格式同构），令牌值 W876 已顺带同步（138 页在 326 页内）；剩下的大头是 B 渠
朱砂实底——en 从未收敛过（实测 767 处/135 页·zh 同口径 457 处/89 页）。本驱动只做
**两条可机械化的收敛**，其余语义/功能实底按四类口径进豁免登记簿（人工裁决）：

1. **`.seal` 徽章实底 → 淡底**（v4 §3.2「徽章实底改为朱砂字 + 8% 淡底」）：
   改页内 `.seal` 规则块的 `background: var(--accent)` → `var(--accent-tint)`、
   `color: var(--paper)` → `color: var(--accent)`（与 W864 批 zh 页同模式）。
2. **KPI 顶条按行收敛**（v4「卡片顶条保留（1 处/卡）」+「整页仅首屏首卡」折中的
   zh 现行实现）：页内有 `.kpi-row` 且无收敛规则时，在页尾 `<style>` 末尾追加
   `.kpi-row > .kpi-card:not([class*="alt-"]) ~ .kpi-card:not([class*="alt-"]) { border-top: 1px solid var(--line); }`
   ——同排首个 kpi-card 保顶条、其余转细线（与 W870/W871 等批 zh 页逐字同规则）。

用法：
    py -3 scripts/_w886_en_migrate.py --pages a.html,b.html [--dry-run]
    py -3 scripts/_w886_en_migrate.py --batch 1 [--dry-run]
"""

import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EN = os.path.join(ROOT, "site", "en")
OUT = os.path.join(ROOT, "scripts", "output")

KPI_RULE = ('/* en 迁移批：KPI 顶条按行收敛（同排首卡保顶条·其余转细线·口径同 zh 页 W870） */\n'
            '.kpi-row > .kpi-card:not([class*="alt-"]) ~ .kpi-card:not([class*="alt-"]) '
            '{ border-top: 1px solid var(--line); }')
KPI_SIG = '.kpi-row > .kpi-card:not([class*="alt-"]) ~ .kpi-card:not([class*="alt-"])'

_SEAL_BLOCK = re.compile(r"\.seal\s*\{([^}]*)\}")


def seal_to_tint(html):
    """页内 .seal 规则块：实底→淡底 + 白字→朱砂字（幂等）。返回 (html, changed)。"""
    changed = False

    def repl(m):
        nonlocal changed
        body = m.group(1)
        nb = re.sub(r"background:\s*var\(--accent\)\s*;", "background: var(--accent-tint);", body)
        nb = re.sub(r"color:\s*var\(--paper\)\s*;", "color: var(--accent);", nb)
        if nb != body:
            changed = True
        return ".seal {" + nb + "}"

    return _SEAL_BLOCK.sub(repl, html), changed


def add_kpi_rule(html):
    """页尾 <style> 末尾追加收敛规则（幂等）。返回 (html, changed)。"""
    if KPI_SIG in html:
        return html, False
    if "kpi-row" not in html:  # HTML class 用法即可（选择器 .kpi-row 由本规则引入）
        return html, False
    idx = html.rfind("</style>")
    if idx < 0:
        return html, False
    return html[:idx] + "\n" + KPI_RULE + "\n" + html[idx:], True


def load_batches():
    """五批切分（与审计分桶一致·确定性）：core 76 / character 12 / myth 14 / essay 36。"""
    pages = sorted(fn for fn in os.listdir(EN) if fn.endswith(".html"))

    def bucket(fn):
        if fn.startswith("essay-"):
            return "essay"
        if fn.startswith("character-"):
            return "character"
        if re.match(r"(bestiary|monster-|heaven-|four-heavenly|magic-|theolog|underworld|"
                    r"immortal|artifact|weapon|ecology)", fn):
            return "myth"
        return "core"

    g = {"core": [], "character": [], "myth": [], "essay": []}
    for p in pages:
        g[bucket(p)].append(p)
    b = [
        g["core"][:28],
        g["core"][28:56],
        g["core"][56:] + g["character"][:8],
        g["character"][8:] + g["myth"][:14] + g["essay"][:10],
        g["essay"][10:],
    ]
    return b


def main(argv):
    ap = argparse.ArgumentParser(description="en 迁移批 B 渠机械化驱动")
    ap.add_argument("--pages", default="")
    ap.add_argument("--batch", type=int, default=0, choices=(0, 1, 2, 3, 4, 5))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv[1:])

    batches = load_batches()
    if args.batch:
        pages = batches[args.batch - 1]
    elif args.pages:
        pages = [p.strip() for p in args.pages.split(",") if p.strip()]
    else:
        ap.error("须指定 --pages 或 --batch")

    # 同步导出一份批内审计子集（供 _w876_c_text_swap.py --audit 使用）
    audit_all = json.load(open(os.path.join(OUT, "_w886_en_audit.json"), encoding="utf-8"))
    subset = {("en/" + p): audit_all.get("en/" + p, {"text_on_bg": [], "fill": [], "static": {}})
              for p in pages}
    sub_path = os.path.join(OUT, "_w886_en_audit_b%d.json" % (args.batch or 0))
    with open(sub_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(subset, f, ensure_ascii=False, indent=1)

    seal_n = kpi_n = 0
    for p in pages:
        fp = os.path.join(EN, p)
        html = open(fp, encoding="utf-8").read()
        html2, c1 = seal_to_tint(html)
        html2, c2 = add_kpi_rule(html2)
        if c1:
            seal_n += 1
        if c2:
            kpi_n += 1
        if (c1 or c2) and not args.dry_run:
            with open(fp, "w", encoding="utf-8", newline="") as f:
                f.write(html2)
    print("[%s] 批 %s · %d 页 · seal→淡底 %d 页 · KPI 顶条规则 +%d 页 · 审计子集 → %s"
          % ("DRY" if args.dry_run else "APPLY", args.batch or "-", len(pages),
             seal_n, kpi_n, os.path.basename(sub_path)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
