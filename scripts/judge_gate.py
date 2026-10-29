"""W465 决策闸门判定脚本（Phase 3 路线图 v7 · W530 落地）。

输入 7 日 UV 与 30 日 UV（**人工输入**），按路线图 §1.2 阈值输出
分发 / 归档 / 中间态 三选一分支，可复算（输入 + 阈值 + 分支 + 时间全记录）。

数据源现状（W1014 语义订正·E1 声明≠落地）：原 W535 曾配套 `fetch_gate_stats.py`
走 GoatCounter API 自动取数，但 GoatCounter 已于 **W806 彻底退役**并被 CI 硬守卫
`check_no_goatcounter.py` 禁止回归，仓内**无可用服务端 UV 源**（`inject_visit_log.py`
仅写 localStorage·本浏览器可见·不能跨访客聚合）。故本脚本不作自动接线（伪造接不通的
源＝违 fail-closed），保留为人工输入复算器：UV 值须从当时的统计后台/快照人工读取代入。
W626 决策闸门已据当时实测（7 日 UV=1 / 30 日 UV=24）判定「归档」并冻结内容扩容批；
本脚本保留供未来若有新统计源时按同阈值复算同一结论。

判定优先级（v7 定案，消除两条件冲突歧义）：
  1. uv30 < 30                -> 归档   （止损优先：30 日口径稳定，
                                         单周脉冲不改变枯竭判断）
  2. uv7 >= 100 或 uv30 >= 200 -> 分发
  3. 其余                       -> 中间态

用法：
  py -3 scripts/judge_gate.py --uv7 120 --uv30 45            # 仅输出判定
  py -3 scripts/judge_gate.py --uv7 120 --uv30 45 --report   # 追加判定段到读者数据复盘.md
"""
from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORT = ROOT / "docs" / "11-方案报告" / "调研与数据复盘" / "读者数据复盘.md"  # W981：随 W737 目录分区修正（文件 2026-10-13 迁 11-方案报告·旧路径 --report 静默不落盘）

UV7_THRESHOLD = 100
UV30_DISTRIBUTE = 200
UV30_ARCHIVE = 30


def judge(uv7: int, uv30: int) -> str:
    if uv30 < UV30_ARCHIVE:
        return "归档"
    if uv7 >= UV7_THRESHOLD or uv30 >= UV30_DISTRIBUTE:
        return "分发"
    return "中间态"


def render_record(uv7: int, uv30: int, branch: str) -> str:
    return (
        f"\n### 判定记录（{date.today().isoformat()}）\n\n"
        f"- 输入值：7 日 UV = {uv7} · 30 日 UV = {uv30}\n"
        f"- 阈值：分发 = 7 日 ≥{UV7_THRESHOLD} 或 30 日 ≥{UV30_DISTRIBUTE} · 归档 = 30 日 <{UV30_ARCHIVE}\n"
        f"- 输出分支：**{branch}**\n"
        f"- 判定时间：{date.today().isoformat()}\n"
        f"- 复算：将上述输入值与阈值代入本脚本可得同一结论\n"
    )


def main() -> int:
    ap = argparse.ArgumentParser(description="W465 决策闸门判定（Phase 3 路线图 §1.2）")
    ap.add_argument("--uv7", type=int, required=True, help="7 日 UV（人工从统计后台/快照取代入·GoatCounter 已 W806 退役）")
    ap.add_argument("--uv30", type=int, required=True, help="30 日 UV（同上·人工取代入）")
    ap.add_argument("--report", action="store_true", help="追加判定记录到 读者数据复盘.md")
    args = ap.parse_args()

    branch = judge(args.uv7, args.uv30)
    record = render_record(args.uv7, args.uv30, branch)
    print(record.strip())
    if args.report:
        if not REPORT.exists():
            print(f"[WARN] {REPORT} 不存在，仅输出判定", file=sys.stderr)
        else:
            with REPORT.open("a", encoding="utf-8") as fh:
                fh.write(record)
            print(f"[OK] 判定记录已追加：{REPORT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
