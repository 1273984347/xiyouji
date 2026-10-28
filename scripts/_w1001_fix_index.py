# -*- coding: utf-8 -*-
"""_w1001_fix_index.py — 补 file-index 的 W1001 段 + 修 CHANGELOG 编号规则的嵌套双括号

索引健康判据（2 条）：
  ① file-index 缺 1 个 CHANGELOG 版段登记：['W1001'] ⇒ 补 `## W1001` 段（123 行）
  ② CHANGELOG 无法解析最新 W 段或编号规则段（W### ID（W001-W###））
     ⇒ 编号规则行当前是「唯一 W### ID（（W001-W1001））」**嵌套双括号** ⇒ 解析失败
     ⇒ 改为单层「唯一 W### ID（W001-W1001）」

用法：py -3 scripts/_w1001_fix_index.py [--dry-run]
"""
from __future__ import annotations

import io
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "scripts", "output")
CH = os.path.join(REPO, "CHANGELOG.md")
FI = os.path.join(OUT, "file-index.md")
SPEC = os.path.join(OUT, "_w1001_spec.json")


def read(p):
    raw = io.open(p, "rb").read()
    return raw.decode("utf-8"), ("\r\n" if b"\r\n" in raw else "\n")


def write(p, text, nl):
    tmp = p + ".tmp"
    io.open(tmp, "wb").write(text.encode("utf-8"))
    os.replace(tmp, p)


def main() -> int:
    dry = "--dry-run" in sys.argv
    with open(SPEC, encoding="utf-8") as fh:
        spec = json.load(fh)
    rows = spec["file_index_rows"]

    # ① CHANGELOG 编号规则：嵌套双括号 → 单层
    t, n = read(CH)
    lines = t.split("\n")
    changed = 0
    for i, ln in enumerate(lines):
        if "编号规则" in ln:
            new = re.sub(r"[（(]\s*[（(]W001-W\d{3,4}\s*[)）]\s*[)）]", "（W001-W1001）", ln)
            new = re.sub(r"[（(]\s*W001-W\d{3,4}\s*[)）]", "（W001-W1001）", new)
            if new != ln:
                lines[i] = new
                changed += 1
    t = "\n".join(lines)
    if changed:
        if dry:
            print("DRY  编号规则嵌套括号 → 单层")
        else:
            write(CH, t, n)
            print("OK   编号规则已改单层（%d 处）" % changed)

    # ② file-index 补 W1001 段
    t, n = read(FI)
    if "## W1001 " in t:
        print("SKIP  file-index 已有 W1001 段")
    else:
        seg = ("## W1001 回次 og:image 全覆盖批·第一轮试点（2026-10-28）\n\n"
               "| 文件 | W | 说明 |\n|---|---|---|\n" + "\n".join(rows) + "\n\n")
        heads = [(int(m.group(1)), m.start()) for m in re.finditer(r"^## W(\d{3,4}) ", t, re.M)]
        pos = None
        for w, s in heads:
            if w < 1001:
                pos = s
                break
        if pos is None:
            pos = 0
        t = t[:pos] + seg + t[pos:]
        if dry:
            print("DRY  file-index 将插 W1001 段（%d 行）" % len(rows))
        else:
            write(FI, t, n)
            print("OK   file-index W1001 段已插入（%d 行）" % len(rows))

    # 复核
    t, _ = read(CH)
    print("编号规则行：", [l[:110] for l in t.split("\n") if "编号规则" in l][:1])
    print("现役段：", re.findall(r"^### (W\d{3,4})", t, re.M)[:4])
    t, _ = read(FI)
    print("file-index 段序：", re.findall(r"^## (W\d{3,4})", t, re.M)[:5])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
