#!/usr/bin/env python3
"""W504 一次性脚本：为 docs/01-06 全部 611 篇补「核验状态：未核验」字段（幂等）。

插入规则：
- 已有 `> 核验状态：` 行 → 跳过。
- 标题后首个 blockquote 连续块存在 → 插在该块最后一行之后。
- 无 blockquote 块 → 在 H1 标题行后插入（空行 + 字段行）。
"""
import os
import re
import sys

_W536_ROOT = os.path.realpath(os.path.dirname(os.path.abspath(__file__)))

def _w536_guard_open(path, *a, **k):
    _real = os.path.realpath(path)
    if not (_real == _W536_ROOT or _real.startswith(_W536_ROOT + os.sep)):
        raise SystemExit("W536 guard: path escapes project root: %s" % path)
    return open(_real, *a, **k)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_DIRS = [
    "01-全书逐回解读", "02-人物深度分析", "03-主题与情节专题",
    "04-文化与历史背景", "05-诗词歌赋", "06-个人随笔",
]
FIELD = "> 核验状态：未核验"


def process(path):
    """返回 'added' / 'skipped'。"""
    lines = open(path, encoding="utf-8").read().split("\n")
    if any(re.match(r"^> 核验状态：", ln) for ln in lines):
        return "skipped"

    # 找 H1
    h1 = next((i for i, ln in enumerate(lines) if ln.startswith("# ")), None)
    if h1 is None:
        h1 = 0

    # 找 H1 后首个 blockquote 连续块
    i = h1 + 1
    start = None
    while i < len(lines):
        if lines[i].startswith(">"):
            start = i
            break
        if lines[i].strip() and not lines[i].startswith(("#", ">")):
            break  # 正文已开始，无元信息块
        i += 1

    if start is not None:
        end = start
        while end + 1 < len(lines) and lines[end + 1].startswith(">"):
            end += 1
        lines.insert(end + 1, FIELD)
    else:
        lines.insert(h1 + 1, "")
        lines.insert(h1 + 2, FIELD)

    with _w536_guard_open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
    return "added"


def main():
    added = skipped = 0
    for d in CONTENT_DIRS:
        dp = os.path.join(ROOT, "docs", d)
        for fn in sorted(os.listdir(dp)):
            if not fn.endswith(".md") or fn == "README.md":
                continue
            r = process(os.path.join(dp, fn))
            if r == "added":
                added += 1
            else:
                skipped += 1
    print("完成：新增 %d · 已有跳过 %d · 合计 %d" % (added, skipped, added + skipped))
    return 0


if __name__ == "__main__":
    sys.exit(main())
