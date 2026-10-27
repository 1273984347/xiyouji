#!/usr/bin/env python3
"""_w864_migrate.py — W864 B2 迁移施工（A 容器 + B 朱砂·一次性件）。

三件事（都不经 INLINED CSS 块——按 `.kpi-card {` / `.seal {` 块定位·落在页面自有
样式块内）：
1. A：`max-width: 1320px` → `var(--container-wide)`（10 页均 1320 = 目标档·零视觉变化）；
2. B-顶条：在 `.kpi-card {}` 块后插入收敛规则——非首张非 alt 变体卡片的顶条由
   3px 朱砂降为 1px 线（裁决 2：整页仅首屏首卡与主行动区可带；alt-2/3/4 非朱砂不动）；
3. B-seal：`.seal` 徽章实底 → `--accent-tint` 淡底 + 朱砂字（同 W862 dukou 处置）。

用法：py -3 scripts/_w864_migrate.py --dry|<无> [file...]
"""

import re
import sys

BAR_RULE = (
    "        /* {W} {B} 裁决 2：朱砂顶条收敛——整页仅首屏首卡可带（alt-2/3/4 非朱砂不动） */\n"
    "        .kpi-row > .kpi-card:not([class*=\"alt-\"]) ~ "
    ".kpi-card:not([class*=\"alt-\"]) { border-top: 1px solid var(--line); }\n"
)


def _block_end(text, start):
    """从 start（块开头 { 之后）找到匹配的 } 位置（跳过嵌套·此处块无嵌套）。"""
    depth = 0
    for i in range(start, len(text)):
        c = text[i]
        if c == "{":
            depth += 1
        elif c == "}":
            if depth == 0:
                return i
            depth -= 1
    return -1


def migrate(text, wtag="W864", blabel="B2"):
    """返回 (新文本, 报告 dict)。"""
    report = {"A": 0, "B_bar": False, "B_seal": False}

    # A：容器令牌化
    text, n = re.subn(r"max-width:\s*1320px", "max-width: var(--container-wide)", text)
    report["A"] = n

    # B-顶条：在 .kpi-card { } 块后插入规则
    m = re.search(r"\.kpi-card\s*\{", text)
    if m:
        end = _block_end(text, m.end())
        if end != -1:
            line_end = text.find("\n", end)
            insert_at = (line_end + 1) if line_end != -1 else end + 1
            rule = BAR_RULE.replace("{W}", wtag).replace("{B}", blabel)
            text = text[:insert_at] + rule + text[insert_at:]
            report["B_bar"] = True

    # B-seal：实底 → 淡底 + 朱砂字
    m = re.search(r"\.seal\s*\{", text)
    if m:
        end = _block_end(text, m.end())
        block = text[m.end():end]
        nb = block.replace("background: var(--accent);",
                           "background: var(--accent-tint);")
        nb = nb.replace("color: #fff;", "color: var(--accent);")
        if nb != block:
            text = text[:m.end()] + nb + text[end:]
            report["B_seal"] = True
    return text, report


def main(argv):
    dry = "--dry" in argv
    wtag = argv[argv.index("--wtag") + 1] if "--wtag" in argv else "W864"
    blabel = argv[argv.index("--blabel") + 1] if "--blabel" in argv else "B2"
    files = [a for a in argv[1:] if not a.startswith("--") and a != wtag
             and a != blabel]
    if not files:
        print("用法：--dry|<无> <file...>")
        return 2
    for path in files:
        with open(path, encoding="utf-8") as f:
            text = f.read()
        new, rep = migrate(text, wtag, blabel)
        print("%s %s：A=%d·顶条规则=%s·seal=%s"
              % ("[DRY]" if dry else "[APPLY]", path, rep["A"],
                 "✓" if rep["B_bar"] else "✗", "✓" if rep["B_seal"] else "✗"))
        if not dry and new != text:
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(new)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
