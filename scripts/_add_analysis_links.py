#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""一次性脚本：为 docs/01-全书逐回解读 的每回文档补「关联分析」footer，
链接该回分析章节中实际出现的主要人物到其 A3 人物深度分析文档。
仅基于分析章节（剧情梗概/重点要点/伏笔/名句/札记，截至 ## 深度解读 或 ## 原文全文），
避免对大段原文引文做匹配（否则会把所有人都链上）。
所有目标均为真实存在的 A3 文件，运行后由 lint_links.py 校验。
"""
import os
import re

_ROOT = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(_ROOT, ".."))
SRC_DIR = os.path.join(ROOT, "docs", "01-全书逐回解读")
A3_DIR = os.path.join(ROOT, "docs", "02-人物深度分析")

# 规范 A3 文件名 -> 该人物在正文中的别名（用于匹配）。同一人物的别名都映射到同一文件，
# 故子串重叠（如来/如来佛祖、观音/观世音）只会去重为一条链接，不会错链。
CHAR_MAP = [
    ("孙悟空.md", ["孙悟空", "悟空", "美猴王", "齐天大圣", "孙行者", "心猿"]),
    ("唐僧.md", ["唐僧", "玄奘", "唐三藏", "圣僧"]),
    ("猪八戒.md", ["猪八戒", "八戒", "猪悟能", "天蓬"]),
    ("沙僧.md", ["沙僧", "沙悟净", "沙和尚", "卷帘大将"]),
    ("白龙马.md", ["白龙马", "敖烈", "小白龙"]),
    ("菩提祖师.md", ["菩提祖师", "须菩提祖师"]),
    ("玉帝.md", ["玉帝", "玉皇大帝", "玉皇"]),
    ("如来.md", ["如来", "如来佛祖"]),
    ("观音.md", ["观音", "观世音", "观音菩萨"]),
    ("太上老君.md", ["太上老君", "老君"]),
    ("二郎神.md", ["二郎神", "二郎显圣真君", "二郎真君", "杨戬"]),
    ("哪吒.md", ["哪吒"]),
    ("铁扇公主.md", ["铁扇公主", "罗刹女", "铁扇仙"]),
    ("牛魔王.md", ["牛魔王"]),
    ("红孩儿.md", ["红孩儿", "圣婴大王"]),
    ("镇元大仙.md", ["镇元大仙", "镇元子"]),
]

# 仅保留真实存在的 A3 文件，并生成展示名
VALID = []
for fname, aliases in CHAR_MAP:
    if os.path.exists(os.path.join(A3_DIR, fname)):
        VALID.append((fname[:-3], fname, aliases))  # (display, file, aliases)


def analysis_scope(text):
    # 取分析章节：截至 ## 深度解读 或 ## 原文全文（取最先出现者），排除大段原文引文
    idx = len(text)
    for marker in ("## 深度解读", "## 原文全文"):
        i = text.find(marker)
        if i != -1:
            idx = min(idx, i)
    return text[:idx]


def process():
    changed = 0
    skipped_no_nav = 0
    skipped_empty = 0
    for fn in sorted(os.listdir(SRC_DIR)):
        if not fn.endswith(".md"):
            continue
        path = os.path.join(SRC_DIR, fn)
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        if "> 导航：" not in text:
            skipped_no_nav += 1
            continue
        scope = analysis_scope(text)
        matched = []
        for display, fname, aliases in VALID:
            if any(al in scope for al in aliases):
                matched.append((display, fname))
        if not matched:
            skipped_empty += 1
            continue
        # 已存在关联分析 footer 则跳过（幂等）
        if "> 关联分析：" in text:
            continue
        rel = "../02-人物深度分析/"
        links = " · ".join("[%s](%s%s)" % (d, rel, f) for d, f in matched)
        footer = "\n> 关联分析：" + links + "\n"
        # 在 导航 行之后插入（保留其后空行与 ## 深度解读）
        nav_line = "> 导航："
        ni = text.find(nav_line)
        # 找到 导航 行末尾
        line_end = text.find("\n", ni)
        new_text = text[:line_end] + footer + text[line_end:]
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_text)
        changed += 1
    print("changed=%d  skipped_no_nav=%d  skipped_empty=%d  valid_chars=%d"
          % (changed, skipped_no_nav, skipped_empty, len(VALID)))


if __name__ == "__main__":
    process()
