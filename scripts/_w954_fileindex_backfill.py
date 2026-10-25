#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""W954 file-index 版段补录（W946 / W947 / W949 / W950 四段）

背景：第 17 门禁「索引健康」判「file-index 缺 N 个 CHANGELOG 版段登记」——W940–W953 批
      有 4 批（图标治理四连批 W946/W947/W949/W950）落了 CHANGELOG 段但未在反向索引登记，
      属既有登记欠账（与 W954 批的登记面漂移同族）。

做法：**从 CHANGELOG 对应段的「文件」字段自动抽取文件清单**生成索引段——不手写清单
      （手写会与 CHANGELOG 产生第二份事实；自动抽取保证二者同源）。
纪律：只新增缺失段，不改既有段（索引历史禁改）；按 W 号序插入；行尾随文件主行尾归一。

用法：py -3 scripts/_w954_fileindex_backfill.py [--dry-run]
"""
import argparse
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHANGELOG = os.path.join(ROOT, "CHANGELOG.md")
FILEINDEX = os.path.join(ROOT, "scripts", "output", "file-index.md")
TARGETS = ["W946", "W947", "W949", "W950"]


def read(p):
    with open(p, encoding="utf-8", newline="") as f:
        return f.read()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    cl = read(CHANGELOG)
    fi = read(FILEINDEX)
    eol = "\r\n" if "\r\n" in fi else "\n"

    segs = {}
    for w in TARGETS:
        m = re.search(r"^### " + w + r"（(\d{4}-\d{2}-\d{2})）：(.+?)$", cl, re.M)
        if not m:
            print(f"ABORT {w}: CHANGELOG 未找到段")
            return 1
        date, title = m.group(1), m.group(2)
        # 取该段「文件」字段（段内第一处 `> - **文件**：`）
        body = cl[m.end():]
        next_seg = re.search(r"^### W\d{3,4}（", body, re.M)
        if next_seg:
            body = body[:next_seg.start()]
        fm = re.search(r">\s*-\s*\*\*文件\*\*[：:]\s*(.+)", body)
        if not fm:
            print(f"ABORT {w}: 段内未找到「文件」字段")
            return 1
        files = [x.strip() for x in fm.group(1).split("、") if x.strip()]
        segs[w] = (date, title, files)
        print(f"{w}: {date} · 文件 {len(files)} 件 · {title[:52]}")

    def build(w, date, title, files):
        lines = [f"## {w} {title}（{date}）", "", "| 文件 | W | 说明 |", "|---|---|---|"]
        for f in files:
            lines.append(f"| {f} | {w} | 批次产物（据 CHANGELOG {w} 段「文件」字段补录） |")
        return "\n".join(lines) + "\n"

    for w in TARGETS:
        if re.search(r"^## " + w + r" ", fi, re.M):
            print(f"SKIP {w}: file-index 已有该段")
            continue
        date, title, files = segs[w]
        block = build(w, date, title, files).replace("\n", eol)
        # 插入点 = 第一个 W 号小于本段号的段标题之前（无则追加到末尾）
        nums = [(int(m.group(1)), m.start()) for m in re.finditer(r"^## W(\d{3,4}) ", fi, re.M)]
        pos = None
        for n, p in nums:
            if n < int(w[1:]):
                pos = p
                break
        if pos is None:
            fi = fi.rstrip("\r\n") + eol + eol + block
            print(f"OK   {w}: 段已追加到末尾")
        else:
            fi = fi[:pos] + block + eol + fi[pos:]
            print(f"OK   {w}: 段已插入（按 W 号序）")

    if args.dry_run:
        print("DRY-RUN: 未写盘")
        return 0
    with open(FILEINDEX, "w", encoding="utf-8", newline="") as f:
        f.write(fi)
    print(f"已写盘: {os.path.relpath(FILEINDEX, ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
