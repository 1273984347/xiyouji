"""W465 决策闸门判定脚本（Phase 3 路线图 v7 · W530 落地）。

输入 7 日 UV 与 30 日 UV（GoatCounter 后台实测值），按路线图 §1.2 阈值输出
分发 / 归档 / 中间态 三选一分支，可复算（输入 + 阈值 + 分支 + 时间全记录）。

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
REPORT = ROOT / "docs" / "10-方法论沉淀" / "读者数据复盘.md"

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
    ap.add_argument("--uv7", type=int, required=True, help="GoatCounter 后台 7 日 UV 实测值")
    ap.add_argument("--uv30", type=int, required=True, help="GoatCounter 后台 30 日 UV 实测值")
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
