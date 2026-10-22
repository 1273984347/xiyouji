#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_w826_migration_plan_check.py — 迁移批次清单对拍（一次性取证脚本·只读）

口径：解析《界面视觉重设计细化规格-v4-2026-10-20.md》§6 批次表格 → 与磁盘实算对拍。
判据：① site/data 87 页（不含 _shell.html）+ site 根 8 页（不含 _template.html）覆盖 0 漏 0 重
      ② 每批 ≤10 页（B11 reader 批除外） ③ reader 622 页单批
输出：scripts/output/_w826_migration_plan_check.json + 控制台摘要
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOC = ROOT / "docs" / "11-方案报告" / "界面视觉重设计细化规格-v4-2026-10-20.md"
SITE = ROOT / "site"

ROW_RE = re.compile(r"^\|\s*(B\d+)\s*\|([^|]*)\|\s*(\d+)\s*\|([^|]*)\|")
CODE_RE = re.compile(r"`([^`]+)`")


def parse_batches() -> dict:
    text = DOC.read_text(encoding="utf-8")
    sec = text.split("## 6. 迁移批次清单")[1].split("## 7.")[0]
    out = {}
    for line in sec.splitlines():
        m = ROW_RE.match(line.strip())
        if not m:
            continue
        bid, theme, declared, cells = m.group(1), m.group(2).strip(), int(m.group(3)), m.group(4)
        pages = [c for c in CODE_RE.findall(cells) if c.endswith(".html") or "/" not in c]
        out[bid] = {"theme": theme, "declared": declared, "pages": pages}
    return out


def main() -> int:
    batches = parse_batches()
    disk_data = sorted(p.name for p in (SITE / "data").glob("*.html") if p.name != "_shell.html")
    disk_root = sorted(p.name for p in SITE.glob("*.html") if p.name != "_template.html")
    disk_reader = sorted(p for p in (SITE / "reader").rglob("*.html"))

    listed: list[str] = []
    for bid, b in batches.items():
        listed.extend(b["pages"])
    listed_norm = [x if x.endswith(".html") else x + ".html" for x in listed]

    # B11 是 reader 批（写法为 site/reader/**），不计入文件名集合
    listed_norm = [x for x in listed_norm if "reader" not in x]

    target = set(disk_data) | set(disk_root)
    got = set(listed_norm)
    missing = sorted(target - got)
    extra = sorted(got - target)
    dup = sorted({x for x in listed_norm if listed_norm.count(x) > 1})

    oversized = {bid: len(b["pages"]) for bid, b in batches.items()
                 if bid != "B11" and len(b["pages"]) > 10}
    declared_mismatch = {bid: (b["declared"], len(b["pages"])) for bid, b in batches.items()
                         if b["declared"] != len(b["pages"]) and bid != "B11"}
    # B11 为 reader 整目录批（写法 site/reader/**）——按递归实算页数计，不逐页列举
    for bid in ("B11",):
        if bid in batches:
            batches[bid]["pages"] = [f"site/reader/**（递归 {len(disk_reader)} 页）"]

    reader_ok = abs(len(disk_reader) - 622) == 0 and "B11" in batches
    reader_declared = batches.get("B11", {}).get("declared")

    ok = not missing and not extra and not dup and not oversized and not declared_mismatch and reader_ok

    out = {
        "batches": {b: {"theme": v["theme"], "declared": v["declared"], "pages": v["pages"]}
                    for b, v in batches.items()},
        "disk": {"data_pages": len(disk_data), "root_pages": len(disk_root), "reader_pages": len(disk_reader)},
        "missing": missing, "extra": extra, "duplicated": dup,
        "oversized_batches": oversized, "declared_mismatch": declared_mismatch,
        "reader_check": {"disk": len(disk_reader), "declared": reader_declared, "ok": reader_ok},
        "verdict": "PASS" if ok else "FAIL",
    }
    p = ROOT / "scripts" / "output" / "_w826_migration_plan_check.json"
    p.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== 迁移批次清单对拍 ===")
    print(f"磁盘：data {len(disk_data)} 页 · 根 {len(disk_root)} 页 · reader {len(disk_reader)} 页")
    print(f"清单批次：{len(batches)} 批 · 列出页面 {len(listed_norm)} 个")
    print(f"漏 {len(missing)}：{missing[:8]}")
    print(f"多 {len(extra)}：{extra[:8]}")
    print(f"重 {len(dup)}：{dup[:8]}")
    print(f"超 10 页的批：{oversized or '无'}")
    print(f"声明页数不符：{declared_mismatch or '无'}")
    print(f"reader 批：声明 {reader_declared} · 实算 {len(disk_reader)} · {'OK' if reader_ok else 'FAIL'}")
    for bid, b in batches.items():
        print(f"  {bid:<4} {b['theme']:<14} 声明 {b['declared']:>3} · 列出 {len(b['pages']):>3}")
    print(f"\n判定：{out['verdict']}")
    print(f"JSON：{p}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
