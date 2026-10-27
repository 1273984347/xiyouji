#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_w930_layout_diff.py — W854(2026-10-21) vs W928(今天) 渲染侧指标对拍

目的：把"4 天前 W854 界面布局审计的渲染实测"与"今天同一批页面的渲染实测"逐项对比，
      得出 18 条问题里每一条的**当前状态**（已修 / 仍存 / 变化），而非复述 4 天前结论。

判据纪律：
  · 两份 JSON 的测点必须**同一批页面同一分辨率**，否则不构成对拍（下方 assert 校验）；
  · 只比较**两边都有**的字段，缺字段标注 MISSING 而不是填 0（填 0 会伪装成"已修"）；
  · 差异方向由每条指标的语义决定（越小越好 / 越大越好 / 目标值），
    不用"变化率"这种无方向的指标糊弄。

用法：py -3 scripts/_w930_layout_diff.py
产出：scripts/output/_w930_layout_diff.json + 控制台对比表
"""
from __future__ import annotations

import io
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OLD = REPO / "scripts" / "output" / "_w854_layout_metrics.json"
NEW = REPO / "scripts" / "output" / "_w930_layout_metrics.json"
OUT = REPO / "scripts" / "output" / "_w930_layout_diff.json"

# (字段, 语义) —— lower_better=越小越好；higher_better=越大越好；none=只报变化
FIELDS = [
    ("aboveFoldEls", "首屏可见元素数", "lower_better"),
    ("blocks", "顶层区块数", "none"),
    ("interactive", "交互元素数", "none"),
    ("smallTargets", "小于 32px 触达目标", "lower_better"),
    ("textEls", "文本节点数", "none"),
    ("docH", "整页高度 px", "lower_better"),
    ("overflowX", "横向溢出", "lower_better"),
    ("gridCols", "网格列数", "none"),
]


def load(p: Path) -> list[dict]:
    if not p.exists():
        raise SystemExit(f"FATAL: 缺证据文件 {p}（无法对拍，拒绝输出假结论）")
    return json.load(io.open(p, encoding="utf-8"))


def key_of(r: dict) -> str:
    return f"{r.get('file')}@{r.get('width')}"


def main() -> int:
    old = load(OLD)
    new = load(NEW)
    omap = {key_of(r): r for r in old}
    nmap = {key_of(r): r for r in new}

    common = sorted(set(omap) & set(nmap))
    only_old = sorted(set(omap) - set(nmap))
    only_new = sorted(set(nmap) - set(omap))
    if not common:
        raise SystemExit("FATAL: 两份证据无共同测点，拒绝输出空对拍")

    rows = []
    for k in common:
        o, n = omap[k], nmap[k]
        item = {"probe": k, "fields": {}}
        for f, label, direction in FIELDS:
            if f not in o or f not in n:
                item["fields"][f] = {
                    "label": label,
                    "direction": direction,
                    "old": o.get(f, "MISSING"),
                    "new": n.get(f, "MISSING"),
                    "delta": "MISSING",
                    "verdict": "MISSING",
                }
                continue
            ov, nv = o[f], n[f]
            if isinstance(ov, (int, float)) and isinstance(nv, (int, float)):
                d = nv - ov
                if d == 0:
                    verdict = "UNCHANGED"
                elif direction == "lower_better":
                    verdict = "IMPROVED" if d < 0 else "REGRESSED"
                elif direction == "higher_better":
                    verdict = "IMPROVED" if d > 0 else "REGRESSED"
                else:
                    verdict = "CHANGED"
                item["fields"][f] = {
                    "label": label,
                    "direction": direction,
                    "old": ov,
                    "new": nv,
                    "delta": d,
                    "verdict": verdict,
                }
            else:
                item["fields"][f] = {
                    "label": label,
                    "direction": direction,
                    "old": ov,
                    "new": nv,
                    "delta": "N/A",
                    "verdict": "CHANGED" if ov != nv else "UNCHANGED",
                }
        # 容器宽度（层级收敛的代理）
        oc, nc = o.get("containers") or {}, n.get("containers") or {}
        cw = {}
        for sel in sorted(set(oc) | set(nc)):
            ow = (oc.get(sel) or {}).get("w")
            nw = (nc.get(sel) or {}).get("w")
            cw[sel] = {
                "old": ow,
                "new": nw,
                "delta": (nw - ow)
                if isinstance(ow, (int, float)) and isinstance(nw, (int, float))
                else "N/A",
            }
        item["containers"] = cw
        # 标题字号序列（层级倒挂的代理）
        oh = [(h.get("t"), h.get("fs")) for h in (o.get("heads") or [])]
        nh = [(h.get("t"), h.get("fs")) for h in (n.get("heads") or [])]
        item["head_fs_old"] = oh
        item["head_fs_new"] = nh
        item["head_fs_changed"] = oh != nh
        rows.append(item)

    summary = {
        "batch": "W928",
        "compare": "W854(2026-10-21) vs W928(2026-10-25) 渲染侧",
        "old_probes": len(omap),
        "new_probes": len(nmap),
        "common_probes": len(common),
        "only_old": only_old,
        "only_new": only_new,
        "rows": rows,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    io.open(OUT, "w", encoding="utf-8").write(json.dumps(summary, ensure_ascii=False, indent=1))

    # ---- 控制台表 ----
    print(f"共同测点 {len(common)} 个（共同 / 旧 {len(omap)} / 新 {len(nmap)}）")
    if only_old:
        print(f"  仅 W854 有：{only_old}")
    if only_new:
        print(f"  仅 W928 有：{only_new}")
    print()
    hdr = f"{'测点':<44}" + "".join(f"{f[2]:>14}" for f in FIELDS)
    print(hdr)
    print("-" * len(hdr))
    for r in rows:
        cells = []
        for f, _, _ in FIELDS:
            fd = r["fields"][f]
            if fd["delta"] == "MISSING":
                cells.append("MISSING".rjust(14))
            elif isinstance(fd["delta"], (int, float)):
                mark = {
                    "IMPROVED": "+",
                    "REGRESSED": "!",
                    "UNCHANGED": "=",
                    "CHANGED": "~",
                }[fd["verdict"]]
                cells.append(f"{mark}{fd['old']}->{fd['new']}".rjust(14))
            else:
                cells.append("N/A".rjust(14))
        print(f"{r['probe']:<44}" + "".join(cells))
    print("\n图例：+=改善  !=不变  !=恶化  ~=变化")
    print(f"DONE -> {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
