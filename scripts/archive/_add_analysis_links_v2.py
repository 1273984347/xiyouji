#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""为 docs/01-全书逐回解读 中仍缺「关联分析」footer 的篇章补 footer。

与 a52e60b 的 _add_analysis_links.py 一致的逻辑，但：
1. 扩大人物字典（CHAR_MAP）——原 21 人白名单覆盖不到这些回的真实主角
   （黄风怪/灵吉/车迟国三国师/灵感大王/独角兕/蜘蛛精/老鼠精/玉兔精/蝎子精/
   奎木狼/金角/银角/六耳猕猴/狮驼岭三魔/大鹏金翅雕 等），全部使用真实存在的 A3 文件名。
2. 插入锚点泛化：「> 导航：」或「> 轨标：」之后均可（原脚本只认 导航，故这批用 轨标 的回被跳过）。
3. 仅处理缺失 footer 的篇章（README 除外），幂等（已存在则跳过）。

仅基于分析章节（截至 ## 深度解读 / ## 原文全文）做匹配，避免大段原文引文污染。
所有目标均为真实存在的 A3 文件；运行后由 lint_links.py 校验。
"""
import os
import re

_ROOT = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(_ROOT, ".."))
SRC_DIR = os.path.join(ROOT, "docs", "01-全书逐回解读")
A3_DIR = os.path.join(ROOT, "docs", "02-人物深度分析")

# (display, filename, [aliases])；filename 必须是 A3_DIR 下真实存在的文件。
# display 用于链接标签，filename 用于链接目标。
CHAR_MAP = [
    # —— 原 21 人（保留）——
    ("孙悟空", "孙悟空.md", ["孙悟空", "悟空", "美猴王", "齐天大圣", "孙行者", "心猿"]),
    ("唐僧", "唐僧.md", ["唐僧", "玄奘", "唐三藏", "圣僧"]),
    ("猪八戒", "猪八戒.md", ["猪八戒", "八戒", "猪悟能", "天蓬"]),
    ("沙僧", "沙僧.md", ["沙僧", "沙悟净", "沙和尚", "卷帘大将"]),
    ("白龙马", "白龙马.md", ["白龙马", "敖烈", "小白龙"]),
    ("菩提祖师", "菩提祖师.md", ["菩提祖师", "须菩提祖师"]),
    ("玉帝", "玉帝.md", ["玉帝", "玉皇大帝", "玉皇"]),
    ("如来", "如来.md", ["如来", "如来佛祖"]),
    ("观音", "观音.md", ["观音", "观世音", "观音菩萨"]),
    ("太上老君", "太上老君.md", ["太上老君", "老君"]),
    ("二郎神", "二郎神.md", ["二郎神", "二郎显圣真君", "二郎真君", "杨戬"]),
    ("哪吒", "哪吒.md", ["哪吒"]),
    ("铁扇公主", "铁扇公主.md", ["铁扇公主", "罗刹女", "铁扇仙"]),
    ("牛魔王", "牛魔王.md", ["牛魔王"]),
    ("红孩儿", "红孩儿.md", ["红孩儿", "圣婴大王"]),
    ("镇元大仙", "镇元大仙.md", ["镇元大仙", "镇元子"]),
    # —— 扩充：本批 23 回真实主角（均经核验存在于 A3_DIR）——
    ("黄风怪", "黄风怪-方向二深化.md", ["黄风怪"]),
    ("灵吉菩萨", "灵吉菩萨.md", ["灵吉菩萨", "灵吉"]),
    ("车迟国三国师", "车迟国三国师-方向二深化.md", ["车迟国三国师", "虎力", "鹿力", "羊力", "三国师"]),
    ("灵感大王", "灵感大王-方向二深化.md", ["灵感大王", "金鱼精", "通天河鱼精"]),
    ("独角兕大王", "独角兕大王.md", ["独角兕大王", "青牛精", "独角兕", "金兜洞"]),
    ("蜘蛛精", "蜘蛛精-方向二深化.md", ["蜘蛛精", "盘丝洞"]),
    ("老鼠精", "老鼠精-方向二深化.md", ["老鼠精", "地涌夫人", "半截观音", "无底洞"]),
    ("玉兔精", "玉兔精-方向二深化.md", ["玉兔精", "玉兔", "玉兔公主"]),
    ("蝎子精", "蝎子精-方向二深化.md", ["蝎子精", "琵琶精"]),
    ("奎木狼", "奎木狼-方向二深化.md", ["奎木狼"]),
    ("金角大王", "金角大王.md", ["金角大王", "金角"]),
    ("银角大王", "银角大王.md", ["银角大王", "银角"]),
    ("六耳猕猴", "六耳猕猴-方向二深化.md", ["六耳猕猴"]),
    ("狮驼岭三魔", "狮驼岭三魔-方向二深化.md", ["狮驼岭三魔", "狮驼岭", "三魔"]),
    ("大鹏金翅雕", "大鹏金翅雕.md", ["大鹏金翅雕", "大鹏", "金翅大鹏"]),
]

# 仅保留真实存在的 A3 文件
VALID = []
for display, fname, aliases in CHAR_MAP:
    if os.path.exists(os.path.join(A3_DIR, fname)):
        VALID.append((display, fname, aliases))


def analysis_scope(text):
    idx = len(text)
    for marker in ("## 深度解读", "## 原文全文"):
        i = text.find(marker)
        if i != -1:
            idx = min(idx, i)
    return text[:idx]


def anchor_insert_pos(text):
    """返回应插入 footer 的位置（锚点行末尾之后）。优先 导航，其次 轨标。"""
    for anchor in ("> 导航：", "> 轨标："):
        ni = text.find(anchor)
        if ni != -1:
            return text.find("\n", ni)  # 锚点行末尾
    # 兜底：H1 标题行之后第一个空行
    m = re.search(r"^# .*$", text, re.MULTILINE)
    if m:
        return m.end()
    return len(text)


def process():
    changed = 0
    skipped_existing = 0
    skipped_empty = 0
    for fn in sorted(os.listdir(SRC_DIR)):
        if not fn.endswith(".md"):
            continue
        if fn == "README.md":
            continue
        path = os.path.join(SRC_DIR, fn)
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        if "> 关联分析：" in text:
            skipped_existing += 1
            continue
        scope = analysis_scope(text)
        matched = []
        for display, fname, aliases in VALID:
            if any(al in scope for al in aliases):
                matched.append((display, fname))
        if not matched:
            skipped_empty += 1
            continue
        rel = "../02-人物深度分析/"
        links = " · ".join("[%s](%s%s)" % (d, rel, f) for d, f in matched)
        footer = "\n> 关联分析：" + links + "\n"
        pos = anchor_insert_pos(text)
        new_text = text[:pos] + footer + text[pos:]
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_text)
        changed += 1
        print("  + %s -> %d chars (%s)" % (fn, len(matched), " ".join(d for d, _ in matched)))
    print("changed=%d  skipped_existing=%d  skipped_empty=%d  valid_chars=%d"
          % (changed, skipped_existing, skipped_empty, len(VALID)))


if __name__ == "__main__":
    process()
