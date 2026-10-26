#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_w930_layout_attr.py — W854 vs W928 增量归因（区分「布局劣化」与「内容增量的连带效应」）

问题：W928 对拍显示首屏元素数普遍 +1~+7、整页高度普遍 +20~+215px。
      若直接读作"4 天里布局劣化"，结论会是错的——W926 批次（2026-10-25 14:34）
      往页脚级联注入了工程批次行，会同时抬高页高与元素数。
方法：逐区块对比旧/新几何（top/h/w/text），把差值归因到**具体区块**，
      再按区块语义（页脚 vs 正文 vs 导航）判定增量性质。

输出：scripts/output/_w930_layout_attr.json
用法：py -3 scripts/_w930_layout_attr.py
"""
from __future__ import annotations

import io
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OLD = REPO / "scripts" / "output" / "_w854_layout_metrics.json"
NEW = REPO / "scripts" / "output" / "_w930_layout_metrics.json"
OUT = REPO / "scripts" / "output" / "_w930_layout_attr.json"


def load(p: Path) -> dict:
    rows = json.load(io.open(p, encoding="utf-8"))
    return {f"{r.get('file')}@{r.get('width')}": r for r in rows}


def main() -> int:
    omap, nmap = load(OLD), load(NEW)
    common = sorted(set(omap) & set(nmap))
    report = {}

    for k in common:
        o, n = omap[k], nmap[k]
        ob, nb = o.get("blocks") or [], n.get("blocks") or []
        rows = []
        # 以区块序号对齐（结构未变时序号稳定）
        for i in range(max(len(ob), len(nb))):
            a = ob[i] if i < len(ob) else None
            b = nb[i] if i < len(nb) else None
            row = {
                "idx": i,
                "old": a,
                "new": b,
                "d_top": (b["top"] - a["top"]) if (a and b) else None,
                "d_h": (b["h"] - a["h"]) if (a and b) else None,
            }
            if a and b:
                # 同一序号的区块，文本是否一致（文本变了说明内容被改过，不是纯测量噪声）
                row["text_same"] = a.get("text") == b.get("text")
                row["cls_same"] = a.get("cls") == b.get("cls")
            rows.append(row)

        doc_delta = n.get("docH", 0) - o.get("docH", 0)
        # 归因：末区块（通常是页脚/尾部容器）的增量
        tail = rows[-1] if rows else None
        report[k] = {
            "docH_old": o.get("docH"),
            "docH_new": n.get("docH"),
            "docH_delta": doc_delta,
            "blocks_old": len(ob),
            "blocks_new": len(nb),
            "aboveFold_old": o.get("aboveFoldEls"),
            "aboveFold_new": n.get("aboveFoldEls"),
            "aboveFold_delta": (n.get("aboveFoldEls") or 0) - (o.get("aboveFoldEls") or 0),
            "tail_block": tail,
            "block_rows": rows,
        }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    io.open(OUT, "w", encoding="utf-8").write(json.dumps(report, ensure_ascii=False, indent=1))

    print(f"{'测点':<42}{'页高Δ':>8}{'末区块Δh':>11}{'末区块类名':>28}{'末区块文本(新)':>34}")
    print("-" * 130)
    for k, v in report.items():
        t = v.get("tail_block") or {}
        nh = t.get("new") or {}
        oh = t.get("old") or {}
        print(
            f"{k:<42}{v['docH_delta']:>8}{str(t.get('d_h')):>11}"
            f"{str(nh.get('cls'))[:26]:>28}{str(nh.get('text'))[:32]:>34}"
        )
    print("\n=== 末区块 old→new 几何（逐测点）===")
    for k, v in report.items():
        t = v.get("tail_block") or {}
        o_, n_ = t.get("old") or {}, t.get("new") or {}
        print(
            f"{k:<42} top {o_.get('top')}->{n_.get('top')}  h {o_.get('h')}->{n_.get('h')}"
            f"  w {o_.get('w')}->{n_.get('w')}  text_same={t.get('text_same')}"
        )
    print(f"\nDONE -> {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
