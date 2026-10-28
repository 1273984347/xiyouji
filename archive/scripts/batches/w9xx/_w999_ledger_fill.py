# -*- coding: utf-8 -*-
"""_w999_ledger_fill.py — 台账补登记 W999 行（必守纪律晋升批·其段已入库但台账缺行）

背景：并行会话的「必守纪律晋升批」以 `### W999` 段入库（提交 5870ec32·状态自写「已收官」），
但**台账没有对应行** ⇒ 第 31 门禁 C4「CHANGELOG 现役段 W 号须有对账表表格行」会判红。
本批让号到 W1001 时顺带**补齐该欠账**（内容据其 CHANGELOG 段与提交事实，注明代登记来源）。

用法：py -3 scripts/_w999_ledger_fill.py [--dry-run]
"""
from __future__ import annotations

import io
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LED = os.path.join(REPO, "docs", "00-导读", "W批次编号对账表.md")

ROW = (
    "| W999 | 必守纪律晋升批次（用户问责「pitfalls 优先级低导致惰性读取」·三层修正）："
    "① AGENTS §6 新增铁律 14「修实例必修根」② 铁律 14 写入 CLAUDE 第 12 条指针 ③ 第 32 门禁 0 FAIL·verify docs rc=0"
    "（**代登记**：本行由 W1001 批让号腾位时补登记·其 CHANGELOG W999 段与提交 `5870ec32` 已入库） | "
    "5870ec32 | —（待回填） | **已收官**（5870ec32·git 反填·纪律晋升三层落地） | "
    "并行 Agent 会话 2026-10-28 | AGENTS.md,CLAUDE.md,docs/agent/pitfalls.md,docs/00-导读/W批次编号对账表.md |")


def read(p):
    raw = io.open(p, "rb").read()
    return raw.decode("utf-8"), ("\r\n" if b"\r\n" in raw else "\n")


def write(p, text, nl):
    tmp = p + ".tmp"
    io.open(tmp, "wb").write(text.encode("utf-8"))
    os.replace(tmp, p)


def main() -> int:
    dry = "--dry-run" in sys.argv
    t, n = read(LED)
    if re.search(r"^\|\s*W999\s*\|", t, re.M):
        print("SKIP  台账已有 W999 行")
        return 0
    lines = t.split("\n")
    pos = None
    for i, ln in enumerate(lines):
        if re.match(r"^\|\s*W1000\s*\|", ln):
            pos = i
            break
    if pos is None:
        print("FAIL  未找到 W1000 行（插入锚点失配）")
        return 1
    lines.insert(pos, ROW)
    t = "\n".join(lines)
    if dry:
        print("DRY  台账将补 W999 行")
    else:
        write(LED, t, n)
        print("OK   台账已补 W999 行（必守纪律晋升批·代登记）")
    t2, _ = read(LED)
    print("台账 W99x-W100x：", re.findall(r"^\| (W(?:99[5-9]|100\d)) \|", t2, re.M))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
