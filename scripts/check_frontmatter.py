#!/usr/bin/env python3
"""元信息块 v2 门禁（W501 第 18 门禁）：校验 docs/01-06 新文件含血缘 + 核验状态 4 字段。

基线豁免：`scripts/output/frontmatter-baseline.txt` 列出的存量 611 篇不追溯；
新文件（不在清单内）必须含以下 4 行（blockquote）：

    > 生成来源：<skill短名@commit短哈希> 或 人工撰写
    > 生成模型：<模型名> 或 未记录 / 不适用
    > 生成日期：YYYY-MM-DD
    > 核验状态：未核验 | 引文已核验 | 专家已核验

口径见 docs/00-导读/文档规范.md §4.6。
"""
import argparse
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASELINE = os.path.join(ROOT, "scripts", "output", "frontmatter-baseline.txt")
CONTENT_DIRS = [
    "01-全书逐回解读",
    "02-人物深度分析",
    "03-主题与情节专题",
    "04-文化与历史背景",
    "05-诗词歌赋",
    "06-个人随笔",
]
STATES = {"未核验", "引文已核验", "专家已核验"}


def check_file(path):
    """返回问题清单（空 = 通过）。"""
    errs = []
    try:
        c = open(path, encoding="utf-8").read()
    except Exception as e:
        return ["读取失败: %s" % e]

    m = re.search(r"^> 生成来源：([^\r\n]+)", c, re.M)
    if not m:
        errs.append("缺 '> 生成来源：' 行")
    else:
        v = m.group(1).strip()
        if not (v == "人工撰写" or "@" in v):
            errs.append("生成来源格式非法（应为 skill短名@commit 或 人工撰写）: %r" % v)

    m = re.search(r"^> 生成模型：([^\r\n]+)", c, re.M)
    if not m:
        errs.append("缺 '> 生成模型：' 行")
    elif not m.group(1).strip():
        errs.append("生成模型为空（无法自报时填 未记录）")

    m = re.search(r"^> 生成日期：([^\r\n]+)", c, re.M)
    if not m:
        errs.append("缺 '> 生成日期：' 行")
    elif not re.fullmatch(r"\d{4}-\d{2}-\d{2}", m.group(1).strip()):
        errs.append("生成日期非 YYYY-MM-DD: %r" % m.group(1).strip())

    m = re.search(r"^> 核验状态：([^\r\n]+)", c, re.M)
    if not m:
        errs.append("缺 '> 核验状态：' 行")
    elif m.group(1).strip() not in STATES:
        errs.append("核验状态非三值枚举: %r" % m.group(1).strip())

    return errs


def load_baseline():
    if not os.path.exists(BASELINE):
        return set()
    with open(BASELINE, encoding="utf-8") as f:
        return {ln.strip().replace("\\", "/") for ln in f if ln.strip()}


def iter_content_files():
    for d in CONTENT_DIRS:
        dp = os.path.join(ROOT, "docs", d)
        if not os.path.isdir(dp):
            continue
        for fn in sorted(os.listdir(dp)):
            if fn.endswith(".md") and fn != "README.md":
                yield os.path.join("docs", d, fn).replace("\\", "/")


def main():
    ap = argparse.ArgumentParser(description="元信息块 v2 门禁（W501）")
    ap.add_argument("--file", help="单文件模式：只检查该文件（不走基线豁免）")
    args = ap.parse_args()

    base = load_baseline()
    if args.file:
        targets = [args.file.replace("\\", "/")]
    else:
        targets = [p for p in iter_content_files() if p not in base]

    fails = 0
    for p in targets:
        errs = check_file(os.path.join(ROOT, p) if not os.path.isabs(p) else p)
        if errs:
            fails += 1
            print("FAIL %s: %s" % (p, "; ".join(errs)))

    if fails:
        print("元信息块 v2 门禁：检查 %d 个新文件 · FAIL %d" % (len(targets), fails))
        return 1
    print("元信息块 v2 门禁通过：检查 %d 个新文件（基线豁免 %d 篇存量）" % (len(targets), len(base)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
