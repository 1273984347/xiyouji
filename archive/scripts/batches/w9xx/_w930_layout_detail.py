#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_w930_layout_detail.py — 补齐两处复核细节（标题字号序列 / 应用侧几何对拍）

用途：
  ① 首页与关键页的 h1/h2/h3 计算字号序列（新旧对照）→ 判定 S2「字号层级倒挂」与
     S3「手机端层级坍塌」当前是否仍成立；
  ② agent-web 侧 6 组测点的旧/新几何对拍 → 判定 A1–A6 当前状态。

判据：标题序列按**标签 + 字号 + 文本**输出，便于直接看出"相邻两级是否同号"（S3 的判据是
      差 ≥4px）；应用侧只比较同一 URL 同一宽度的测点。

用法：py -3 scripts/_w930_layout_detail.py
"""
from __future__ import annotations

import io
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT_DIR = REPO / "scripts" / "output"


def load(name: str) -> list[dict]:
    p = OUT_DIR / name
    if not p.exists():
        raise SystemExit(f"FATAL: 缺证据 {p}")
    return json.load(io.open(p, encoding="utf-8"))


def main() -> int:
    old = {f"{r.get('file')}@{r.get('width')}": r for r in load("_w854_layout_metrics.json")}
    new = {f"{r.get('file')}@{r.get('width')}": r for r in load("_w930_layout_metrics.json")}

    print("======== ① 标题字号序列（新旧对照）========")
    for k in ("index.html@1440", "index.html@375"):
        for label, m in (("W854", old.get(k)), ("W928", new.get(k))):
            if not m:
                continue
            seq = [(h.get("t"), h.get("fs"), (h.get("text") or "")[:14]) for h in (m.get("heads") or [])]
            print(f"\n-- {k}  [{label}] --")
            for t, fs, txt in seq:
                print(f"   {t}  {fs:>6}  {txt}")

    # S3 判据：@375 下 h2 与 h3 的 computed font-size 差 ≥ 4px
    m375 = new.get("index.html@375") or {}
    fs_by_tag: dict[str, set] = {}
    for h in m375.get("heads") or []:
        fs_by_tag.setdefault(h.get("t"), set()).add(h.get("fs"))
    print("\n-- @375 标签 → 字号集合（判 S3：h2 与 h3 是否同号）--")
    for t in sorted(fs_by_tag):
        print(f"   {t}: {sorted(fs_by_tag[t])}")

    print("\n======== ② agent-web 侧几何对拍 =========")
    aold = {f"{r.get('url')}@{r.get('vw')}": r for r in load("_w854_layout_metrics_app.json")}
    anew = {f"{r.get('url')}@{r.get('vw')}": r for r in load("_w930_layout_metrics_app.json")}
    print(f"{'测点':<22}{'aside.w':>16}{'main.w':>16}{'小目标':>12}{'可点div':>12}")
    print("-" * 80)
    for k in sorted(set(aold) | set(anew)):
        o, n = aold.get(k) or {}, anew.get(k) or {}
        aw = lambda r: (r.get("aside") or {}).get("w")
        mw = lambda r: (r.get("main") or {}).get("w")
        print(
            f"{k:<22}{str(aw(o)) + '->' + str(aw(n)):>16}"
            f"{str(mw(o)) + '->' + str(mw(n)):>16}"
            f"{str(o.get('smallTargets')) + '->' + str(n.get('smallTargets')):>12}"
            f"{str(o.get('clickableDivs')) + '->' + str(n.get('clickableDivs')):>12}"
        )

    # 应用侧断点清点（源码层）
    src = REPO / "xiyouji-agent-web" / "src"
    css_files = sorted(src.rglob("*.css"))
    print(f"\n-- agent-web/src CSS 文件 {len(css_files)} 个：{[c.name for c in css_files]} --")
    import re
    bp = {}
    for c in css_files:
        t = io.open(c, encoding="utf-8", errors="replace").read()
        for m in re.finditer(r"@media\s*\(([^)]*)\)", t):
            bp.setdefault(m.group(1).strip(), 0)
            bp[m.group(1).strip()] += 1
    print(f"-- @media 断点清点：{bp or '（零断点）'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
