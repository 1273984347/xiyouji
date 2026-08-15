#!/usr/bin/env python3
"""西游记论文 line 号锚点批量校核与重定位（读 text-search.json，去空白匹配）。

数据源：dataset/text-search.json（chapters[].text 为正文，title/fullTitle 为回目）。
口径：单回内行号（1-based）= 第 N 回 text 按 "\\n" 拆行后的第 X 行。
关键：text 字段约 1700 行含「中文字符间空格」，匹配前必须去空白，否则误报 NO_MATCH。

用法：
  python verify_anchors.py peek <回号> <line>             # 查看某回某行原文
  python verify_anchors.py locate <回号> <关键词...>       # 在该回内去空白搜关键词，返回行号
  python verify_anchors.py batch <anchors.json>           # 批量校验 + 重定位
  python verify_anchors.py --root D:/1/xiyouji ...        # 覆盖默认项目根目录

anchors.json 格式：
  [
    {"num": 29, "line": 3, "desc": "呈递关文遇黄袍怪", "kws": ["倒换文牒", "关文"]},
    {"num": 14, "line": 1459, "desc": "心猿归正回目", "kws": ["心猿归正"]}
  ]
"""

import argparse
import json
import re
import sys
from pathlib import Path

DEFAULT_ROOT = Path("D:/1/xiyouji")
TS_JSON = "dataset/text-search.json"


def norm(s: str) -> str:
    """去掉所有空白，用于容错匹配（text 字段含中文字符间空格）。"""
    return re.sub(r"\s+", "", s)


def load_chapters(root: Path) -> dict:
    data = json.loads((root / TS_JSON).read_text(encoding="utf-8"))
    return {c["num"]: c for c in data["chapters"]}


def lines_of(ch: dict) -> list:
    return ch["text"].split("\n")


def peek(ch: dict, line: int) -> str:
    lines = lines_of(ch)
    if 1 <= line <= len(lines):
        return lines[line - 1].strip()
    return f"<OUT_OF_RANGE: 本回仅 {len(lines)} 行>"


def locate(ch: dict, kws: list, limit: int = 15) -> list:
    lines = lines_of(ch)
    nkws = [norm(k) for k in kws]
    out = []
    for i, l in enumerate(lines, 1):
        nl = norm(l)
        if any(nk in nl for nk in nkws):
            out.append((i, l.strip()))
    return out[:limit]


def title_hit(ch: dict, kws: list) -> bool:
    title_text = (ch.get("title") or "") + (ch.get("fullTitle") or "")
    nt = norm(title_text)
    return any(norm(k) in nt for k in kws)


def main() -> int:
    ap = argparse.ArgumentParser(description="西游记论文 line 号锚点批量校核与重定位")
    ap.add_argument("--root", type=Path, default=DEFAULT_ROOT,
                    help="项目根目录，默认 D:/1/xiyouji")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_peek = sub.add_parser("peek", help="查看某回某行原文")
    p_peek.add_argument("num", type=int)
    p_peek.add_argument("line", type=int)

    p_loc = sub.add_parser("locate", help="在回内去空白搜关键词，返回行号")
    p_loc.add_argument("num", type=int)
    p_loc.add_argument("kws", nargs="+")

    p_batch = sub.add_parser("batch", help="批量校验 anchors.json")
    p_batch.add_argument("file", type=Path)

    args = ap.parse_args()
    chapters = load_chapters(args.root)

    if args.cmd == "peek":
        ch = chapters.get(args.num)
        if ch is None:
            print("OUT_OF_RANGE")
            return 1
        print(f"第{args.num}回 line {args.line}: {peek(ch, args.line)}")
        print(f"（本回共 {len(lines_of(ch))} 行）")
        return 0

    if args.cmd == "locate":
        ch = chapters.get(args.num)
        if ch is None:
            print("OUT_OF_RANGE")
            return 1
        hits = locate(ch, args.kws)
        if not hits:
            if title_hit(ch, args.kws):
                print(f"NO_MATCH_IN_TEXT 但命中回目「{ch.get('fullTitle', '')}」"
                      f"——回目在 title/fullTitle 字段，不在 text，line 号不成立")
            else:
                print("NO_MATCH")
            return 1
        for i, t in hits:
            print(f"line {i}: {t}")
        return 0

    if args.cmd == "batch":
        anchors = json.loads(args.file.read_text(encoding="utf-8"))
        n_fix = 0
        for a in anchors:
            num = a["num"]
            line = a.get("line")
            desc = a.get("desc", "")
            kws = a.get("kws", [])
            ch = chapters.get(num)
            print(f"【第{num}回 line {line}】{desc}" if line is not None else f"【第{num}回】{desc}")
            if ch is None:
                print("  → 回号越界")
                n_fix += 1
                continue
            if line is not None:
                print(f"  原行实际: {peek(ch, line)[:60]}")
            hits = locate(ch, kws) if kws else []
            if not hits:
                if title_hit(ch, kws):
                    print(f"  判定: 回目+line 不成立（回目「{ch.get('fullTitle', '')}」在 title 字段，不在 text）")
                else:
                    print("  判定: 无匹配（需人工确认原意）")
                n_fix += 1
            else:
                first = hits[0]
                print(f"  建议改为: 第{num}回 line {first[0]}（\"{first[1][:40]}\"）")
                if len(hits) > 1:
                    for i, t in hits[1:4]:
                        print(f"            或 line {i}: {t[:40]}")
                if line is not None and first[0] == line:
                    print("  ✓ 行号与关键词命中一致")
                else:
                    n_fix += 1
            print()
        print(f"===== 共 {len(anchors)} 条，建议处理 {n_fix} 条 =====")
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
