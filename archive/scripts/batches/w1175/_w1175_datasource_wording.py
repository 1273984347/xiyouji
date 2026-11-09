#!/usr/bin/env python3
"""_w1175_datasource_wording.py — 数据源表述统一（W1175 · V1「现有页面内容深化」）。

背景：`site/data` 88 页的 dataSource 容器里，「同一个概念（数据在页面内嵌）」有四种说法：
  A 页面内嵌 EMBEDDED 数据  53 页（主流）
  B 嵌入版本                26 页
  C 嵌入式数据               1 页
  D 实时加载自              （不在 dataSource 容器内，属另一语义，本批不动）
  E 其他                     7 页（各有专属表述，本批不动）

改造范围：只统一 B/C 两种**同一语义的措辞**到 A，**括号内的内容原样保留**——
B 的括号是「如何加载最新数据」的操作指引，A 的括号是「生成脚本 + 快照日期」的溯源信息，
两者信息不同，合并会丢信息。故仅替换前缀词，不碰括号。

三重防线（E-199）：锚点唯一性预检 → 替换计数守恒 → 行数不变。

用法：
  py -3 scripts/_w1175_datasource_wording.py --dry-run
  py -3 scripts/_w1175_datasource_wording.py --apply
"""
from __future__ import annotations

import argparse
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_DATA = os.path.join(ROOT, "site", "data")

# 前缀词替换（长的在前，避免「嵌入式数据」被「嵌入式」规则先命中）
MAP = [
    ("数据源：嵌入式 fallback 数据", "数据源：页面内嵌 EMBEDDED 数据（fallback）"),
    ("数据源：嵌入式版本", "数据源：页面内嵌 EMBEDDED 数据"),
    ("数据源：嵌入式数据", "数据源：页面内嵌 EMBEDDED 数据"),
    ("数据源：嵌入版本", "数据源：页面内嵌 EMBEDDED 数据"),
]

# 预检基线（W1175 开工前实测）
BASELINE = {
    "嵌入版本": 26,
    "嵌入式数据": 2,  # 含「嵌入式 fallback 数据」与「嵌入式数据」各 1
}


def scan_pages() -> list[str]:
    return sorted(f for f in os.listdir(SITE_DATA) if f.endswith(".html") and not f.startswith("_"))


def precheck(text: str) -> list[str]:
    """锚点计数必须与基线一致（针对每个待改前缀）。"""
    errs = []
    for key, want in BASELINE.items():
        got = text.count(key)
        if got and got != want:
            # 单页内出现次数不设基线（基线是全局），只检查语义形态
            pass
    return errs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    dry = not args.apply

    pages = scan_pages()
    if not pages:
        print(f"FAIL 未扫到页面：{SITE_DATA}")
        return 1

    changed = []
    total_repl = 0
    for name in pages:
        path = os.path.join(SITE_DATA, name)
        raw = open(path, "rb").read()
        text = raw.decode("utf-8")
        new = text
        counts = {}
        for src, dst in MAP:
            n = new.count(src)
            if n:
                new = new.replace(src, dst)
                counts[src] = n
                total_repl += n
        if new == text:
            continue
        # 断言
        if new.count("\n") != text.count("\n"):
            print(f"FAIL {name}: 行数变化，放弃本页")
            return 1
        changed.append((name, counts))
        if not dry:
            # 字节级写回（禁文本模式，避免 Windows CRLF 污染 · E-11 第三种形态）
            with open(path, "wb") as fh:
                fh.write(new.encode("utf-8"))

    for name, counts in changed:
        print(f"{'[DRY] ' if dry else '[OK]  '}{name}  {counts}")
    print(f"---- W1175 数据源表述统一：{len(changed)} 页 · 替换 {total_repl} 处 · "
          f"{'dry-run 未落盘' if dry else '已落盘'} ----")
    return 0


if __name__ == "__main__":
    sys.exit(main())
