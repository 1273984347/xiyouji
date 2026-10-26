#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""W954 一次性版本面同步脚本（升版面 → 现役 W954）

背景：W940–W953 批未做升版面同步（.github/workflows/README.md 停在 W939、CITATION.cff 与
      HANDOVER「当前 HEAD」停在 W950），致第 31/交付门禁判红「现役版本面 ≠ 最新 W 段」。
      `bump_version.py` 因方案 D 守卫已停用（它要求文档仍为「当前版本」形态），故按其提示
      「改用一次性脚本（参照 _w702_edits.py 形态）」自建本脚本。

纪律：
  · **只改版本面字面量**，不改历史段、不改叙述语义；
  · 每处替换**先断言命中数**，命中数不符即中止不写盘；
  · 幂等：已是目标值则跳过；
  · 行尾随文件主行尾归一（CRLF 共享面 / LF 文档面混用）；
  · **不动** site/dukou-engine.html 页脚（门禁仅 WARN·且会触发站点面 + CSP 重算）与
    归档面（archive/）。

用法：py -3 scripts/_w954_version_sync.py [--dry-run]
"""
import argparse
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET_W = "W954"

# (相对路径, 说明, 旧串或正则, 新串, 期望命中次数)
JOBS = [
    ("CHANGELOG.md", "编号规则段上限 W001-W953 → W001-W954",
     "W### ID（W001-W953）", "W### ID（W001-W954）", 1),
    ("HANDOVER.md", "「当前 HEAD」W950 → W954",
     re.compile(r"当前 HEAD = W950（[^）\n]*）"), None, 1),
    ("HANDOVER.md", "末尾「最后更新」链首 W953 → W954",
     "最后更新：2026-10-26（W953 themes 库专题题图批）",
     "最后更新：2026-10-26（W954 第 43 篇工作复盘批）", 1),
    ("CITATION.cff", "批次号形态 version W950 → W954",
     'version: "W950"', 'version: "W954"', 1),
    ("CITATION.cff", "发布日期 2026-10-25 → 2026-10-26",
     'date-released: "2026-10-25"', 'date-released: "2026-10-26"', 1),
    (".github/workflows/README.md", "头部版本链上限 W450-W939 → W450-W954",
     "→ W450-W939**", "→ W450-W954**", 1),
    (".github/workflows/README.md", "头部项目标识 W939 → W954",
     "（`D:\\xiyouji`，W939）", "（`D:\\xiyouji`，W954）", 1),
    (".github/workflows/README.md", "里程碑行上限 W450-W939 → W450-W954",
     "**W450-W939**：", "**W450-W954**：", 1),
]

# README：A4 计数叙述面（判据：A4_DOCS 四份文档各须命中 `209(?:<!--stats:a4_docs-->)?\\s*篇`）
README_A4_ANCHOR = "- **文档（Docs）**：以 Markdown 写就的逐回解读、人物分析、主题专题、文化背景、诗词赏析、个人随笔"
README_A4_NEW = ("- **A4 主题专题**：209<!--stats:a4_docs--> 篇（site/ 主题 hub 与专题页的事实源）"
                 "<!--doc-sync:exempt-->")

# STRUCTURE.md：里程碑 token（WARN 项·顺手补齐）
STRUCTURE_MILESTONE_ANCHOR = "## 顶层结构"
STRUCTURE_MILESTONE_NEW = (
    "## 里程碑\n\n"
    "- **W954（2026-10-26）**：《工作复盘与优化分析报告》入库（W795–W953 全区间·149 段 / 154 行 / 354 提交）<!--doc-sync:exempt-->\n"
    "- **W953（2026-10-26）**：themes 库专题题图批（12 张线描专题题图·站内累计 40 张）\n"
    "- **W952（2026-10-25）**：内页人物题图续批第二组（12 张·站内累计 28 张）\n"
    "- **W950（2026-10-25）**：图标集打磨优化批（重画 13 枚 + 光学尺寸归一 + 1967 处内联 SVG 图形同步）\n"
)


def read(p):
    with open(p, encoding="utf-8", newline="") as f:
        return f.read()


def write(p, s):
    with open(p, "w", encoding="utf-8", newline="") as f:
        f.write(s)


def eol_of(t):
    return "\r\n" if "\r\n" in t else "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    # 按文件聚合（同一文件多处改动一次写盘）
    per_file = {}
    for rel, desc, old, new, expect in JOBS:
        path = os.path.join(ROOT, rel)
        if not os.path.exists(path):
            print(f"ABORT {rel}: 文件不存在")
            return 1
        text = per_file.get(path)
        if text is None:
            text = read(path)
        if isinstance(old, str):
            n = text.count(old)
            if n != expect:
                print(f"ABORT {rel} · {desc}: 命中 {n} 次（期望 {expect}）")
                return 1
            if new == old:
                print(f"SKIP {rel} · {desc}（已是目标值）")
                per_file[path] = text
                continue
            text = text.replace(old, new)
        else:
            m = old.search(text)
            if not m:
                print(f"SKIP {rel} · {desc}（未命中·可能已是目标值）")
                per_file[path] = text
                continue
            repl = "当前 HEAD = W954（第 43 篇工作复盘批：W795–W953 全区间复盘 149 段 / 154 行 / 354 提交 + 登记面漂移五类量化与台账 8 行回写）"
            text = old.sub(repl, text, count=1)
        print(f"OK   {rel} · {desc}")
        per_file[path] = text

    # README：A4 计数行（幂等：已存在则跳过）
    p = os.path.join(ROOT, "README.md")
    t = per_file.get(p) or read(p)
    if "stats:a4_docs" in t:
        print("SKIP README.md · A4 计数行（已存在）")
    else:
        if t.count(README_A4_ANCHOR) != 1:
            print(f"ABORT README.md · A4 计数行: 锚点命中 {t.count(README_A4_ANCHOR)} 次（期望 1）")
            return 1
        eol = eol_of(t)
        t = t.replace(README_A4_ANCHOR, README_A4_ANCHOR + eol + README_A4_NEW, 1)
        print("OK   README.md · A4 计数行已补（209<!--stats:a4_docs--> 篇）")
    per_file[p] = t

    # STRUCTURE.md：里程碑 token（幂等）
    p = os.path.join(ROOT, "STRUCTURE.md")
    t = per_file.get(p) or read(p)
    if "## 里程碑" in t and "W954（2026-10-26）" in t:
        print("SKIP STRUCTURE.md · 里程碑 token（已存在）")
    else:
        eol = eol_of(t)
        if t.count(STRUCTURE_MILESTONE_ANCHOR) != 1:
            print(f"ABORT STRUCTURE.md · 里程碑: 锚点命中 {t.count(STRUCTURE_MILESTONE_ANCHOR)} 次（期望 1）")
            return 1
        block = STRUCTURE_MILESTONE_NEW.replace("\n", eol)
        t = t.replace(STRUCTURE_MILESTONE_ANCHOR, block + eol + STRUCTURE_MILESTONE_ANCHOR, 1)
        print("OK   STRUCTURE.md · 里程碑 token 已补（W954/W953/W952/W950）")
    per_file[p] = t

    if args.dry_run:
        print("DRY-RUN: 未写盘")
        return 0
    for path, text in per_file.items():
        write(path, text)
        print(f"已写盘: {os.path.relpath(path, ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
