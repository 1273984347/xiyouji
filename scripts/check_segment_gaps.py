#!/usr/bin/env python3
"""check_segment_gaps.py — 历史缺口体检（W1127·T74 遗留 B 的前置）

## 为什么要有这个工具

W1122 批把「立段/落段判定只看一面」根修成两面分判之后，暴露出一类**历史缺口**：
某些批次在台账有认领行，但 CHANGELOG 与 file-index **两面正本皆无段**
⇒ 该批次的交付内容在任何正本面都查不到（只可能留在归档件里）。

- 现状：backfill_changelog 只在「待补 W 号低于已立段 max」时**提示**（历史缺口保护·
  默认不自动补）⇒ 缺口清单散落在运行输出里，没有可复核的清单，也无法判断
  「这些批次的内容是否还能复原」。
- 本工具：把缺口做成**可复核的体检项**——盘点台账（正本 + 归档）出现过的批次号，
  与两面正本的段集合做差集，输出缺口清单，并逐件给出**可复原来源提示**
  （CHANGELOG 归档 / file-index 归档 / 台账归档里是否含该批号）⇒ 为「按序补段」提供依据。
- 纪律：本工具**只体检不补段**（补段须先评估可复原性，避免造段）。

用法：
  py -3 scripts/check_segment_gaps.py            # 文本清单（退出码 0）
  py -3 scripts/check_segment_gaps.py --strict   # 有缺口则退出码 1（供未来接入门禁）
  py -3 scripts/check_segment_gaps.py --json     # JSON 输出
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if os.path.join(ROOT, "scripts") not in sys.path:
    sys.path.insert(0, os.path.join(ROOT, "scripts"))

import backfill_changelog as bf  # noqa: E402

LEDGER = os.path.join("docs", "00-导读", "W批次编号对账表.md")
LEDGER_ARCHIVE = os.path.join("archive", "docs", "W批次编号对账表-ARCHIVE.md")
CL = "CHANGELOG.md"
FI = os.path.join("scripts", "output", "file-index.md")
CL_ARCHIVES = [
    os.path.join("archive", "docs", "CHANGELOG-ARCHIVE.md"),
    os.path.join("archive", "docs", "CHANGELOG-ARCHIVE-tier2.md"),
    os.path.join("archive", "docs", "CHANGELOG-ARCHIVE-tier2-W400-W559.md"),
]
FI_ARCHIVES = [
    os.path.join("archive", "docs", "file-index-ARCHIVE.md"),
    os.path.join("archive", "docs", "file-index-ARCHIVE-tier2.md"),
]
ROW_RE = re.compile(r"^\| W(\d{3,4}) ")


def read(rel):
    """读仓内相对路径文件（不存在返回空串·归档件可能缺席）。"""
    p = os.path.join(ROOT, rel)
    if not os.path.isfile(p):
        return ""
    with open(p, encoding="utf-8") as f:
        return f.read()


def ledger_batches(text_ledger, text_ledger_archive):
    """台账（正本 + 归档）里出现过的批次号集合。"""
    out = set()
    for text in (text_ledger, text_ledger_archive):
        for m in ROW_RE.finditer(text or ""):
            out.add(int(m.group(1)))
    return out


def cl_segments(text):
    """CHANGELOG 类文本的段号集合（复用 backfill_changelog 的段解析·不重复正则）。"""
    if not text:
        return set()
    return {w for w, _st in bf.segments(text)}


def fi_segments(text):
    """file-index 类文本的段号集合。"""
    if not text:
        return set()
    return {int(m.group(1)[1:]) for m in bf.RE_FI_SEG.finditer(text)}


def hint(cl_arc, fi_arc, led_arc):
    """可复原来源提示（决定「能否按序补段」）。"""
    if cl_arc or fi_arc:
        return "正本两面皆无段，但归档件含该批号 ⇒ 内容可从归档迁回"
    if led_arc:
        return "正本两面皆无段，台账行已归档 ⇒ 内容须人工判定（不可自动补）"
    return "正本两面皆无段且归档无来源 ⇒ 无可复原来源（补段会造段·须人工裁决）"


def scan_in(ledger, cl_main, fi_main, cl_arc, fi_arc, led_arc):
    """纯逻辑：→ 缺口清单（按号升序）。

    缺口判据 = 台账有认领行 **且** CHANGELOG 与 file-index 两面**正本**皆无段。
    归档件不计入「有段」，但用于给可复原来源提示。
    """
    gaps = []
    for w in sorted(ledger):
        if w in cl_main or w in fi_main:
            continue
        gaps.append({
            "w": w,
            "batch": "W%d" % w,
            "in_ledger_archive": w in led_arc,
            "recoverable_from_cl_archive": w in cl_arc,
            "recoverable_from_fi_archive": w in fi_arc,
            "hint": hint(w in cl_arc, w in fi_arc, w in led_arc),
        })
    return gaps


def scan():
    """读盘扫描 → 缺口清单。"""
    ledger = ledger_batches(read(LEDGER), read(LEDGER_ARCHIVE))
    cl_main = cl_segments(read(CL))
    fi_main = fi_segments(read(FI))
    cl_arc = set()
    for rel in CL_ARCHIVES:
        cl_arc |= cl_segments(read(rel))
    fi_arc = set()
    for rel in FI_ARCHIVES:
        fi_arc |= fi_segments(read(rel))
    led_arc = {int(m.group(1)) for m in ROW_RE.finditer(read(LEDGER_ARCHIVE))}
    return scan_in(ledger, cl_main, fi_main, cl_arc, fi_arc, led_arc)


def main(argv=None):
    ap = argparse.ArgumentParser(description="历史缺口体检（两面正本皆无段）")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    ap.add_argument("--strict", action="store_true", help="有缺口则退出码 1")
    args = ap.parse_args(argv)
    gaps = scan()
    if args.json:
        print(json.dumps({"count": len(gaps), "gaps": gaps}, ensure_ascii=False, indent=2))
    else:
        print("=== 历史缺口体检（台账有认领行 · CHANGELOG 与 file-index 两面正本皆无段）===")
        if not gaps:
            print("0 项：两面正本覆盖台账全部批次")
        for g in gaps:
            print("  %s：%s" % (g["batch"], g["hint"]))
        print("---- 历史缺口体检：%d 项 ----" % len(gaps))
    if args.strict and gaps:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
