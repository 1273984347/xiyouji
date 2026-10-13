#!/usr/bin/env python3
"""fix_links_w341_part3.py — W341 死链专项·第三批修复

处理用户已决策的两类剩余死链：
  A 类（改链到新位置）：9 个深化专题中指向已重组的 source/原文/*.txt 的引用。
      W286 将原名整文件（原著逐回深读.txt / 原著逐回深读二.txt / 详解.txt）按章拆分进
      source/原文/分回/（逐回原文）与 source/原文/shendu/（深读）。
      每个引用的链接文字都带明确「第X回」，故确定性映射到 分回/第0XX回.md（逐回原文，
      与「第X回」链接文字及剧情点引用语义一致）。
  B 类 + C 类（删链先消死链）：指向尚不存在的专题文件的链接，去掉超链接、保留显示文字为纯文本。

不处理（用户未决策 / 属排除项）：
  D 类 .github/workflows/README.md → deploy.yml（需核对真实 workflow 文件名）
  E 类 scripts/node_modules/**（第三方包内部链接，CI 排除）
  F 类 site/_template.html（生成器模板，CI 排除）

用法：
  python scripts/fix_links_w341_part3.py            # 应用修复
  python scripts/fix_links_w341_part3.py --dry-run  # 仅打印，不改写
"""
import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ---- A 类：source/原文/*.txt  → 分回/第0XX回.md ----
A_FILES = [
    "docs/02-人物深度分析/二郎神深化专题.md",
    "docs/02-人物深度分析/六耳猕猴深化专题.md",
    "docs/02-人物深度分析/哪吒深化专题.md",
    "docs/02-人物深度分析/太上老君深化专题.md",
    "docs/02-人物深度分析/明代历史原型对照专题.md",
    "docs/02-人物深度分析/牛魔王深化专题.md",
    "docs/02-人物深度分析/玉帝深化专题.md",
    "docs/02-人物深度分析/红孩儿深化专题.md",
    "docs/02-人物深度分析/菩提祖师深化专题.md",
]
A_RE = re.compile(r"\[([^\]]*)\]\(\.\./\.\./source/原文/[^)]+\.txt\)")


def a_repl(m):
    text = m.group(1)
    ch = re.search(r"第\s*(\d+)\s*回", text)
    if not ch:
        return m.group(0)  # 无回目号则不改（理论上不会发生）
    c = int(ch.group(1))
    return f"[{text}](../../source/原文/分回/第{c:03d}回.md)"


# ---- B/C 类：去掉链接、保留显示文字 ----
STRIP = {
    "docs/02-人物深度分析/明代历史原型对照专题.md": [
        "../04-文化与历史背景/西游与三教合一明代思想史专题.md",
        "./西游与弗洛伊德精神分析专题.md",
        "./西游与荣格分析心理学专题.md",
        "./西游与拉康精神分析专题.md",
    ],
    "docs/03-主题与情节专题/取经神话政治学专题.md": [
        "权力五联对照专题.md",
    ],
    "docs/03-主题与情节专题/空间政治学专题.md": [
        "妖怪身份政治专题.md",
    ],
}


def strip_repl(target):
    rx = re.compile(r"\[([^\]]*)\]\(" + re.escape(target) + r"\)")
    return rx


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    total = 0
    for frel in A_FILES:
        p = ROOT / frel
        text = p.read_text(encoding="utf-8")
        new, n = A_RE.subn(a_repl, text)
        if n:
            total += n
            print(f"[A] {frel}: {n} 处 → 分回/第0XX回.md")
            if not args.dry_run:
                p.write_text(new, encoding="utf-8")

    for frel, targets in STRIP.items():
        p = ROOT / frel
        text = p.read_text(encoding="utf-8")
        changed = 0
        for t in targets:
            rx = strip_repl(t)
            text, k = rx.subn(r"\1", text)
            changed += k
        if changed:
            total += changed
            print(f"[B/C] {frel}: {changed} 处链接去超链（保留文字）")
            if not args.dry_run:
                p.write_text(text, encoding="utf-8")

    print(f"\n合计改动：{total} 处" + ("（dry-run，未写入）" if args.dry_run else "（已写入）"))


if __name__ == "__main__":
    main()
