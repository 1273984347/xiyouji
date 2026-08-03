#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为 28 篇「跨章对比型」SD 深度解读切片补充图谱/检索标注：
在切片末尾追加结构化交叉引用 footer（> 关联：），链接
  - A1 逐回解读：取自头部「推测对应原著回号」声明回号区间（权威）
  - A3 人物深度分析：取自正文命中的 ALIAS 人物（≤5）
路径基点为 source/原文/shendu/，到 docs 用 ../../../docs/...

幂等：文件已含 sentinel 注释则跳过。仅处理 CROSS 列表中的 28 篇。
"""
import os, re, glob

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SHENDU = os.path.join(ROOT, "source", "原文", "shendu")
A1 = os.path.join(ROOT, "docs", "01-全书逐回解读")
A3 = os.path.join(ROOT, "docs", "02-人物深度分析")
SENTINEL = "<!-- sd-crossref -->"

CROSS = [
    "SD002","SD007","SD010","SD015","SD019","SD022","SD027","SD028",
    "SD031","SD035","SD039","SD044","SD049","SD051","SD052","SD055",
    "SD056","SD058","SD060","SD062","SD065","SD067","SD069","SD071",
    "SD073","SD076","SD083","SD085",
]

ALIAS = {
    "悟空": "孙悟空", "孙猴子": "孙悟空", "美猴王": "孙悟空", "斗战胜佛": "孙悟空",
    "玄奘": "唐僧", "三藏": "唐僧", "唐僧": "唐僧",
    "八戒": "猪八戒", "猪八戒": "猪八戒", "老猪": "猪八戒",
    "沙僧": "沙僧", "沙和尚": "沙僧", "卷帘": "沙僧",
    "小白龙": "白龙马", "白龙马": "白龙马", "小龙": "白龙马",
    "菩提": "菩提祖师", "菩提祖师": "菩提祖师", "须菩提": "菩提祖师",
    "玉帝": "玉帝", "玉皇": "玉帝", "玉皇大帝": "玉帝",
    "如来": "如来", "佛祖": "如来", "如来佛祖": "如来",
    "观音": "观音", "菩萨": "观音", "观世音": "观音",
    "太上老君": "太上老君", "老君": "太上老君",
    "二郎神": "二郎神", "杨戬": "二郎神",
    "哪吒": "哪吒",
    "铁扇公主": "铁扇公主", "罗刹": "铁扇公主", "芭蕉扇": "铁扇公主",
    "牛魔王": "牛魔王",
    "红孩儿": "红孩儿", "圣婴": "红孩儿",
    "镇元大仙": "镇元大仙", "镇元子": "镇元大仙",
    "六耳猕猴": "六耳猕猴",
    "白骨精": "白骨精", "白骨夫人": "白骨精",
    "金箍棒": "孙悟空",
}

HEADER_RE = re.compile(r"推测对应原著回号:\s*第(\d+)(?:-(\d+))?回")


def a1_chapters_from_header(txt):
    m = HEADER_RE.search(txt)
    if not m:
        return []
    a = int(m.group(1))
    b = int(m.group(2)) if m.group(2) else a
    return list(range(a, b + 1))


def a3_characters(txt, cap=5):
    out, seen = [], set()
    for alias, canon in ALIAS.items():
        if canon in seen:
            continue
        if alias in txt:
            f = os.path.join(A3, canon + ".md")
            if os.path.exists(f):
                out.append(canon)
                seen.add(canon)
        if len(out) >= cap:
            break
    return out


def a1_doc_for(ch):
    ms = [os.path.basename(m) for m in glob.glob(os.path.join(A1, f"第{ch:03d}回-*.md"))]
    ms = [m for m in ms if m != "README.md"]
    return ms[0] if ms else None


def build_footer(txt):
    chapters = a1_chapters_from_header(txt)
    chars = a3_characters(txt)
    parts = []
    for ch in chapters:
        d = a1_doc_for(ch)
        if d:
            parts.append(f"[第{ch}回](../../../docs/01-全书逐回解读/{d})")
    for c in chars:
        parts.append(f"[{c}](../../../docs/02-人物深度分析/{c}.md)")
    if not parts:
        return None
    return "> 关联：" + " · ".join(parts) + " " + SENTINEL


def main():
    applied, skipped_empty, skipped_done = [], [], []
    for sd in CROSS:
        p = os.path.join(SHENDU, sd + ".md")
        if not os.path.exists(p):
            print(f"  ! 缺失 {sd}.md")
            continue
        txt = open(p, encoding="utf-8").read()
        if SENTINEL in txt:
            skipped_done.append(sd)
            continue
        footer = build_footer(txt)
        if not footer:
            skipped_empty.append(sd)
            continue
        # 去掉尾部空行后追加
        lines = txt.rstrip("\n").split("\n")
        while lines and lines[-1].strip() == "":
            lines.pop()
        lines.append("")
        lines.append(footer)
        open(p, "w", encoding="utf-8").write("\n".join(lines) + "\n")
        applied.append((sd, footer.count("](")))

    print(f"已补 footer: {len(applied)} 篇")
    for sd, n in applied:
        print(f"  + {sd} ({n} 链接)")
    print(f"跳过(已标注): {len(skipped_done)} -> {skipped_done}")
    print(f"跳过(无链接可生成): {len(skipped_empty)} -> {skipped_empty}")


if __name__ == "__main__":
    main()
