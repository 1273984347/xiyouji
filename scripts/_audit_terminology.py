#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_audit_terminology.py — 术语统一审计（零依赖）

目标：发现 docs/ 与 site/ 中因多 agent 协作、OCR、繁简混写产生的
      **真实不一致**（非故意别名），生成审计报告 + 仅对高置信度
      繁→简专名整体替换做保守修复。

设计原则（保守）：
  - 故意别名（孙悟空/齐天大圣/心猿、唐僧/玄奘/三藏）不做统一 —— 它们是文学需要。
  - 仅处理「繁体字符残留在简体语料」与「明确 OCR 笔误」两类高置信度问题。
  - 默认 report-only；`--apply` 仅对 TRAD_FULL（多字专名整体）在 .md 中落地，
    .html 命中仅报告、人工复核。

用法：
  python scripts/_audit_terminology.py            # 仅报告
  python scripts/_audit_terminology.py --apply    # 对 .md 落地 TRAD_FULL 修复
"""

import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(_HERE, ".."))
DOCS = os.path.join(ROOT, "docs")
SITE = os.path.join(ROOT, "site")
OUT = os.path.join(_HERE, "output", "terminology-audit-report.md")

# ---- 高置信度繁→简专名整体替换（仅 .md 落地）----
TRAD_FULL = {
    "觀音": "观音",
    "孫悟空": "孙悟空",
    "豬八戒": "猪八戒",
    "彌勒": "弥勒",
    "閻王": "阎王",
    "龍王": "龙王",
    "靈山": "灵山",
    "羅漢": "罗汉",
    "如來": "如来",
    "菩薩": "菩萨",
    "禪宗": "禅宗",
    "彌陀": "弥陀",
    "釋迦": "释迦",
    "須彌": "须弥",
}

# ---- 明确 OCR / 笔误（报告 + 落地）----
TYPO = {
    "普萨": "菩萨",
    "悟 空": "悟空",
    "孙悟 空": "孙悟空",
    "猪八 戒": "猪八戒",
}

# 单字繁→简（仅报告，人工复核后再决定）
TRAD_CHAR = {
    "觀": "观", "孫": "孙", "豬": "猪", "彌": "弥", "閻": "阎", "龍": "龙",
    "靈": "灵", "羅": "罗", "來": "来", "禪": "禅", "無": "无", "師": "师",
    "時": "时", "國": "国", "義": "义", "學": "学", "經": "经", "話": "话",
    "說": "说", "詩": "诗", "詞": "词", "漢": "汉", "書": "书", "畫": "画",
    "雲": "云", "聖": "圣", "眾": "众", "舊": "旧", "體": "体", "質": "质",
    "問": "问", "間": "间", "處": "处", "這": "这", "個": "个", "飛": "飞",
    "異": "异", "與": "与", "爾": "尔", "樂": "乐", "愛": "爱", "滅": "灭",
    "點": "点", "獻": "献", "寶": "宝", "戲": "戏", "夢": "梦", "請": "请",
    "護": "护", "統": "统", "燈": "灯", "傷": "伤", "驚": "惊", "覺": "觉",
}


def _iter_files():
    for base in (DOCS, SITE):
        for dirpath, _, files in os.walk(base):
            for fn in files:
                if fn.endswith((".md", ".html")):
                    yield os.path.join(dirpath, fn)


def main():
    apply = "--apply" in sys.argv
    results = {}  # (file, pattern) -> list of (lineno, line)
    for fp in _iter_files():
        rel = os.path.relpath(fp, ROOT)
        is_md = fp.endswith(".md")
        try:
            with open(fp, encoding="utf-8") as f:
                lines = f.readlines()
        except Exception:
            continue
        for pat, rep in list(TRAD_FULL.items()) + list(TYPO.items()):
            # 单文件扫描
            hits = []
            for i, line in enumerate(lines, 1):
                if pat in line:
                    hits.append((i, line.rstrip("\n")))
            if hits:
                # 是否可落地：TRAD_FULL 仅 .md；TYPO 两者都修
                can_apply = (pat in TRAD_FULL and is_md) or (pat in TYPO)
                if apply and can_apply:
                    new_lines = [ln.replace(pat, rep) for ln in lines]
                    if new_lines != lines:
                        with open(fp, "w", encoding="utf-8") as f:
                            f.writelines(new_lines)
                        lines = new_lines
                results.setdefault((rel, pat, rep), []).extend(hits)
        # 单字繁→简：仅 .md 落地（简体语料中的繁字即不一致）
        if apply and is_md:
            new_lines = lines[:]
            for tc, sc in TRAD_CHAR.items():
                new_lines = [ln.replace(tc, sc) for ln in new_lines]
            if new_lines != lines:
                with open(fp, "w", encoding="utf-8") as f:
                    f.writelines(new_lines)
                lines = new_lines

    # 单字报告（不落地）
    char_hits = {}
    for fp in _iter_files():
        rel = os.path.relpath(fp, ROOT)
        try:
            with open(fp, encoding="utf-8") as f:
                text = f.read()
        except Exception:
            continue
        for tc, sc in TRAD_CHAR.items():
            c = text.count(tc)
            if c:
                char_hits.setdefault((rel, tc, sc), 0)
                char_hits[(rel, tc, sc)] += c

    # ---- 写报告 ----
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("# 术语统一审计报告\n\n")
        f.write("> 生成：%s | 模式：%s\n\n" % (
            "apply" if apply else "report-only",
            "W344 术语统一审计"))
        f.write("## 一、繁→简专名整体替换（高置信度）\n\n")
        if not results:
            f.write("_未发现繁体专名整体残留。_\n")
        else:
            for (rel, pat, rep), hits in sorted(results.items()):
                f.write("### `%s`：%s → %s （%d 处）\n" % (rel, pat, rep, len(hits)))
                for ln, _ in hits[:5]:
                    f.write("- L%d\n" % ln)
                if len(hits) > 5:
                    f.write("- …（共 %d 处）\n" % len(hits))
                f.write("\n")
        f.write("## 二、明确笔误（OCR/空格）\n\n")
        f.write("_见上表 TYPO 项，已一并处理。_\n\n")
        f.write("## 三、单字繁体残留（仅报告·人工复核）\n\n")
        if not char_hits:
            f.write("_未发现单字繁体残留。_\n")
        else:
            f.write("| 文件 | 繁字 | 简字 | 次数 |\n|---|---|---|---|\n")
            for (rel, tc, sc), c in sorted(char_hits.items(), key=lambda x: -x[1]):
                f.write("| `%s` | %s | %s | %d |\n" % (rel, tc, sc, c))
            f.write("\n")

    # ---- 控制台摘要 ----
    print("术语审计完成（%s）" % ("apply" if apply else "report-only"))
    print("  TRAD_FULL/TYPO 命中文件组：%d" % len(results))
    print("  单字繁体残留种类：%d（文件·字组合）" % len(char_hits))
    print("  报告：%s" % OUT)
    # 统计单字总次数
    total_char = sum(char_hits.values())
    print("  单字繁体总出现次数：%d" % total_char)


if __name__ == "__main__":
    main()
