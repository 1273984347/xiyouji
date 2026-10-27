#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_w930_rename_prefix.py — 把本批产物前缀从 _w928_ 统一改为 _w930_

起因（W926 会话 mvs_0c526aed73554be9a8a69f64b20c11a2 跨会话协调·2026-10-25）：
  W928 号已归属并行「D-1 实跑批」会话（提交 57762fa3·CHANGELOG 顶段 = W928）。
  本批取 W930（已二次让号并登记），但产物文件名前缀仍挂 _w928_ ⇒
  ①观感撞号；②第 31 门禁 C4「提交-版段对账」按 repo 相对路径的号段 token 解析，
    文件名里的 928 与版段号 W930 不一致 ⇒ 可能判「号段对不上」。

本脚本做四件事（顺序固定）：
  1. 改 13 件文件的**文件名**；
  2. 改脚本**内部自引用**（输出路径 / 输入路径 / 截图目录 / profile 目录）；
  3. 改**报告与台账认领行**中的 `_w928_` 字面引用（只动小写下划线形式，
     **不动大写 `W928`** —— 后者是 D-1 实跑批的批次号，属他人成果）；
  4. 顺带给两个 CDP 探针补 `fs.mkdir(OUT, {recursive:true})`（上一轮探针因
     截图目录不存在而首组即退出，本批把它固化成脚本自愈能力）。

用法：py -3 scripts/_w930_rename_prefix.py
"""
from __future__ import annotations

import io
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# 文件名映射：旧名 → 新名（相对 REPO）
FILES = [
    "scripts/_w928_layout_attr.py",
    "scripts/_w928_layout_detail.py",
    "scripts/_w928_layout_diff.py",
    "scripts/_w928_layout_probe.mjs",
    "scripts/_w928_layout_probe_app.mjs",
    "scripts/_w928_layout_residual.py",
    "scripts/_w928_layout_static.py",
    "scripts/output/_w928_layout_attr.json",
    "scripts/output/_w928_layout_diff.json",
    "scripts/output/_w928_layout_metrics.json",
    "scripts/output/_w928_layout_metrics_app.json",
    "scripts/output/_w928_layout_static.json",
    "scripts/output/_w928_visible_leak.json",
]

# 文本替换规则：只替换小写下划线形式，保留大写 W928（他人批次号）
TEXT_SUBS = [
    ("_w928_", "_w930_"),
    ("ui-audit-2026-10-25-w928", "ui-audit-2026-10-25-w930"),
    ("tmpe/w928/_profile", "tmpe/w930/_profile"),
    ("tmpe/w928/_profile_app", "tmpe/w930/_profile_app"),
]

# 需要改文本的文件（含报告与台账）
TEXT_TARGETS = [
    "scripts/_w930_layout_attr.py",
    "scripts/_w930_layout_detail.py",
    "scripts/_w930_layout_diff.py",
    "scripts/_w930_layout_probe.mjs",
    "scripts/_w930_layout_probe_app.mjs",
    "scripts/_w930_layout_residual.py",
    "scripts/_w930_layout_static.py",
    "docs/11-方案报告/计划方案/T21-任务计划执行与经验沉淀报告-2026-10-25.md",
    "docs/00-导读/W批次编号对账表.md",
]

# 探针脚本补目录自建（幂等：已存在则跳过）
MKDIR_SNIPPETS = [
    (
        "scripts/_w930_layout_probe.mjs",
        "const results = [];",
        "await fs.mkdir(OUT, { recursive: true });\nconst results = [];",
    ),
    (
        "scripts/_w930_layout_probe_app.mjs",
        "const results = [];",
        "await fs.mkdir(OUT, { recursive: true });\nconst results = [];",
    ),
]


def main() -> int:
    # 1) 改名
    renamed = 0
    for rel in FILES:
        old = REPO / rel
        new_rel = rel.replace("_w928_", "_w930_")
        new = REPO / new_rel
        if not old.exists():
            if new.exists():
                continue  # 幂等：已改名
            print(f"FATAL: 源文件不存在 {rel}")
            return 2
        os.replace(old, new)
        renamed += 1
    print(f"① 改名 {renamed} 件")

    # 2) 文本替换
    changed = 0
    for rel in TEXT_TARGETS:
        p = REPO / rel
        if not p.exists():
            print(f"  跳过（不存在）：{rel}")
            continue
        s = io.open(p, encoding="utf-8").read()
        orig = s
        for a, b in TEXT_SUBS:
            s = s.replace(a, b)
        if s != orig:
            io.open(p, "w", encoding="utf-8", newline="\n").write(s)
            changed += 1
    print(f"② 文本内引用改写 {changed} 件")

    # 3) 探针脚本补目录自建
    patched = 0
    for rel, anchor, repl in MKDIR_SNIPPETS:
        p = REPO / rel
        if not p.exists():
            continue
        s = io.open(p, encoding="utf-8").read()
        if "fs.mkdir(OUT" in s:
            continue
        if anchor not in s:
            print(f"  WARN: 未找到锚点，跳过 {rel}")
            continue
        s = s.replace(anchor, repl, 1)
        io.open(p, "w", encoding="utf-8", newline="\n").write(s)
        patched += 1
    print(f"③ 探针补目录自建 {patched} 件")

    # 4) 校验：① 新名文件内容无 _w928_ 残留；② 旧名文件应已不存在
    leftover = []
    for rel in TEXT_TARGETS:
        p = REPO / rel
        if p.exists() and "_w928_" in io.open(p, encoding="utf-8").read():
            leftover.append(rel)
    for rel in FILES:
        if (REPO / rel).exists():
            leftover.append(f"旧名未清: {rel}")
    if leftover:
        print("FATAL: 校验未过：" + ", ".join(leftover))
        return 3
    print("④ 校验通过：新名文件内容无 _w928_ 残留 · 旧名文件已全部消失")
    return 0


if __name__ == "__main__":
    sys.exit(main())
