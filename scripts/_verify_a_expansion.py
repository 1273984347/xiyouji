#!/usr/bin/env python3
"""A 轨扩写后核验（2026-09-27）：复算新增统计 + 两稿差异面 + 锚点抽验。

复算项（对照论文新增段落中的数字）：
  - 30 节点按二十回分段：1/5/5/8/11
  - 关文 15 节点相邻间距：min 2 / max 17 / 中位 6
  - 验讫 9 处按第 60 回二分为 4/5；未验 3 处均在 74 回后
  - 108000/5110 日均 ≈ 21
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
S = ROOT / "docs" / "S4-学术投稿" / "学术论文-西游记驿递交通书写的数字人文研究.md"
A = ROOT / "docs" / "S4-学术投稿" / "学术论文-西游记驿递交通书写的数字人文研究-匿名稿.md"


def parse_rows(path: Path, table_hint: str, start: int, end: int):
    t = path.read_text(encoding="utf-8").splitlines()
    rows = []
    for i in range(start, min(end, len(t))):
        m = re.match(r"^\| 第 (\d+)(?:-(\d+))? 回 \|", t[i])
        if m:
            rows.append((int(m.group(1)), t[i]))
    return rows


def main() -> int:
    t = S.read_text(encoding="utf-8").splitlines()
    # 表定位：表 1 以表头行定位；表 2 以加粗表题定位（两表题面格式不同）
    i1 = next(i for i, l in enumerate(t) if l.startswith("| 回目 | 地点 | 状态 | 类型 |"))
    i2 = next(i for i, l in enumerate(t) if l.startswith("**表 2"))
    t1 = parse_rows(S, "t1", i1, i2)
    t2 = parse_rows(S, "t2", i2, i2 + 30)
    print("表1 rows:", len(t1), "| 表2 rows:", len(t2))
    starts = sorted([r[0] for r in t1] + [r[0] for r in t2])
    print("total nodes:", len(starts))
    seg = [0] * 5
    for s in starts:
        seg[min((s - 1) // 20, 4)] += 1
    print("segment 1-20/21-40/41-60/61-80/81-100:", seg)
    ks = sorted(r[0] for r in t1)
    gaps = [ks[i + 1] - ks[i] for i in range(len(ks) - 1)]
    gaps_sorted = sorted(gaps)
    med = gaps_sorted[len(gaps_sorted) // 2]
    print("关文间距 min/max/median:", min(gaps), max(gaps), med)
    pass_rows = [r[0] for r in t1 if "pass" in r[1]]
    unv_rows = [r[0] for r in t1 if "| unv |" in r[1]]
    print("验讫 pass:", len(pass_rows), "<=60:", sum(1 for x in pass_rows if x <= 60), ">60:", sum(1 for x in pass_rows if x > 60))
    print("未验 unv:", unv_rows)
    print("日均(108000/5110):", round(108000 / 5110, 1))

    # 两稿差异面（应仅脱敏项）
    import difflib
    sa = S.read_text(encoding="utf-8")
    aa = A.read_text(encoding="utf-8")
    d = [l for l in difflib.unified_diff(sa.splitlines(), aa.splitlines(), lineterm="", n=0)
         if l.startswith(("+", "-")) and not l.startswith(("+++", "---"))]
    print("diff_lines:", len(d))
    return 0


if __name__ == "__main__":
    sys.exit(main())