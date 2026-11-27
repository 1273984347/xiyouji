#!/usr/bin/env python3
"""history_grep.py — 归档面检索（W1340 · P1-3「迁出后正本不可检索」根修）。

背景：版段迁出正本后，CHANGELOG / file-index 里查不到老批次的内容；此前只能手工打开
archive/docs 下的多个分卷逐个 Ctrl+F。本工具把「查 W### 在哪 / 某关键词在哪」变成一条命令。

检索面（默认）：
  archive/docs/*ARCHIVE*.md          —— 一级归档正本（含 tier2 分卷）
  archive/docs/ARCHIVE-MANIFEST.md   —— 分卷清单
  archive/docs/ARCHIVE-T5-EXEMPTIONS.md —— 豁免簿
  archive/docs/archive-log.jsonl     —— 迁移台账（哪批、何时、按什么水位迁的）

用法：
  py -3 scripts/history_grep.py W1253
  py -3 scripts/history_grep.py "段数窗" --ignore-case
  py -3 scripts/history_grep.py "W12\\d\\d" --regex --json
  py -3 scripts/history_grep.py W1253 --root <临时目录>     # 测试用
退出码：0 = 有命中；1 = 无命中；2 = 参数/目录错误。
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_PATTERNS = [
    os.path.join("archive", "docs", "*.md"),
    os.path.join("archive", "docs", "archive-log.jsonl"),
]
EXCLUDE_NAMES = {"README.md", "INDEX.md"}


def _default_files(root: str) -> list[str]:
    out = []
    for pat in DEFAULT_PATTERNS:
        for p in glob.glob(os.path.join(root, pat)):
            name = os.path.basename(p)
            if name in EXCLUDE_NAMES:
                continue
            if "ARCHIVE" not in name.upper() and name != "archive-log.jsonl":
                continue
            out.append(p)
    return sorted(set(out))


def _scan_file(path_: str, root: str, match, limit: int) -> list[dict]:
    """单文件扫描（每文件上限 limit）——独立成函数以压嵌套深度（ruff 结构档）。"""
    try:
        f = open(path_, encoding="utf-8", errors="replace")
    except OSError:
        return []
    hits: list[dict] = []
    with f:
        for i, line in enumerate(f, 1):
            if not match(line):
                continue
            hits.append({
                "file": os.path.relpath(path_, root).replace(os.sep, "/"),
                "line": i,
                "text": line.rstrip("\n")[:240],
            })
            if len(hits) >= limit:
                break
    return hits


def search(root: str, pattern: str, *, regex: bool = False, ignore_case: bool = False,
           limit: int = 20, files: list[str] | None = None) -> list[dict]:
    """返回命中列表 [{file, line, text}]；每文件最多 limit 条。"""
    flags = re.IGNORECASE if ignore_case else 0
    if regex:
        rx = re.compile(pattern, flags)
        match = lambda s: rx.search(s) is not None  # noqa: E731
    else:
        needle = pattern.lower() if ignore_case else pattern
        match = lambda s: needle in (s.lower() if ignore_case else s)  # noqa: E731

    hits: list[dict] = []
    for path_ in (files or _default_files(root)):
        hits.extend(_scan_file(path_, root, match, limit))
    return hits


def main() -> int:
    ap = argparse.ArgumentParser(description="归档面检索（W1340·history_grep）")
    ap.add_argument("pattern", help="检索词（默认按字面量；--regex 时按正则）")
    ap.add_argument("--root", default=ROOT, help="仓库根（测试可覆盖）")
    ap.add_argument("--regex", action="store_true", help="按正则解释 pattern")
    ap.add_argument("-i", "--ignore-case", action="store_true", help="忽略大小写")
    ap.add_argument("--limit", type=int, default=20, help="每个文件最多返回条数（默认 20）")
    ap.add_argument("--files", default="", help="逗号分隔的显式文件清单（相对 --root；缺省用默认检索面）")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    args = ap.parse_args()

    if not os.path.isdir(args.root):
        print("目录不存在：%s" % args.root, file=sys.stderr)
        return 2
    files = None
    if args.files.strip():
        files = [os.path.join(args.root, p.strip()) for p in args.files.split(",") if p.strip()]
    try:
        hits = search(args.root, args.pattern, regex=args.regex, ignore_case=args.ignore_case,
                      limit=max(1, args.limit), files=files)
    except re.error as e:
        print("正则非法：%s" % e, file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps({"pattern": args.pattern, "count": len(hits), "hits": hits},
                         ensure_ascii=False, indent=2))
    else:
        for h in hits:
            print("%s:%d: %s" % (h["file"], h["line"], h["text"]))
        print("---- 命中 %d 条（检索面：archive/docs）----" % len(hits))
    return 0 if hits else 1


if __name__ == "__main__":
    sys.exit(main())
