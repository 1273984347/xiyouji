#!/usr/bin/env python3
"""check_audit_trigger.py — 对抗式审查触发器（W1000 建·与复盘触发器同族的第三哨）。

背景：W998 批的 subagent 对抗式审查（迁移守恒/门禁实跑/代码缺陷全查）一次抓出
P1×2/P2×4——证明「写哨兵的人也需要被哨兵盯」。本触发器把这类审查从「想起来才派」
变成「每 ≥20 批机器点名」。条款与触发点双件套（W824 纪律·防干扰日志断档模式复发）。

判据（单一·台账即事实源）：
  A1 台账最新含「对抗式审查」的认领行距当前 max(W) ≥ 20 批 → 触发。
  找不到登记行 → 按「从未审查」处理，直接触发（fail-closed·宁假警不漏警）。

只提示不拦截：exit 恒 0；派发动作 = 会话按 docs/agent/adversarial-audit-prompt.md
模板派发 subagent，修复与审查登记同批或次批落台账（desc 含「对抗式审查」即被本器认得）。

用法：
  py -3 scripts/check_audit_trigger.py            # 打印状态（exit 0）
  py -3 scripts/check_audit_trigger.py --self-test
"""
from __future__ import annotations

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import preflight_check as pf  # noqa: E402 — 复用台账路径与行解析

THRESHOLD = 20
MARK = "对抗式审查"


def last_audit_batch(ledger_text):
    """台账最新含「对抗式审查」的认领行 W 号；无 → None。"""
    found = None
    for ln in ledger_text.split("\n"):
        m = re.match(r"^\|\s*W(\d{3,4})\s*\|", ln)
        if m and MARK in ln:
            found = int(m.group(1))
    return found


def evaluate(ledger_text):
    """→ (触发?, 提示行)。纯逻辑入口供单测。"""
    max_w = pf.parse_ledger(ledger_text)["max_w"]
    last = last_audit_batch(ledger_text)
    if max_w is None:
        return True, ["⚠ 对抗审查触发器不可判定：台账无 W 行（fail-closed）"]
    if last is None:
        return True, ["⚠ 对抗审查触发：台账从未登记对抗式审查批——按模板派发（docs/agent/adversarial-audit-prompt.md）"]
    gap = max_w - last
    if gap >= THRESHOLD:
        return True, ["⚠ 对抗审查触发：距上次对抗式审查（W%d）已 %d 批 ≥ %d"
                      "——按 docs/agent/adversarial-audit-prompt.md 模板派发 subagent，登记行 desc 含「对抗式审查」"
                      % (last, gap, THRESHOLD)]
    return False, ["对抗审查触发器：距上次（W%d）%d 批 < %d——未触发" % (last, gap, THRESHOLD)]


def notice_lines():
    """preflight 提示位入口。"""
    try:
        text = open(os.path.join(pf.ROOT, pf.LEDGER), encoding="utf-8", newline="").read()
    except OSError as e:
        return ["⚠ 对抗审查触发器不可读台账（%s）——fail-closed 按已触发处理" % e]
    _, lines = evaluate(text)
    return lines


def _self_test() -> int:
    fails = []
    rows = "\n".join(
        ["| W1000 | 对抗式审查常驻化批 | a | b | 已收官 | s | x |"]
        + ["| W%03d | 常规批 | a | b | 已收官 | s | y |" % w for w in range(1001, 1022)]
    )
    # 21 批间隔 → 触发
    ok, lines = evaluate(rows)
    if not ok or not lines[0].startswith("⚠"):
        fails.append("21 批间隔应触发")
    # 5 批间隔 → 不触发
    rows5 = "\n".join([
        "| W1000 | 对抗式审查常驻化批 | a | b | 已收官 | s | x |",
        "| W1001 | 常规批 | a | b | 已收官 | s | y |",
        "| W1002 | 常规批 | a | b | 已收官 | s | z |",
        "| W1003 | 常规批 | a | b | 已收官 | s | w |",
        "| W1004 | 常规批 | a | b | 已收官 | s | v |",
        "| W1005 | 常规批 | a | b | 已收官 | s | u |",
    ])
    ok5, lines5 = evaluate(rows5)
    if ok5 or not lines5[0].endswith("未触发"):
        fails.append("5 批间隔不应触发：%s" % lines5)
    # 从未审查 → 触发（fail-closed）
    ok0, lines0 = evaluate("| W1005 | 常规批 | a | b | 已收官 | s | x |")
    if not ok0:
        fails.append("从未审查应触发（fail-closed）")
    # 描述列散文提及「对抗式审查」不算登记行（须在认领行任意格——实现为整行 grep，
    # 但行首必须是台账行；非台账行不算）
    ok9, _ = evaluate("散文里提对抗式审查但不是台账行\n| W1005 | 常规批 | a | b | 已收官 | s | x |")
    if not ok9:
        fails.append("非台账行提及不应计为登记")
    print()
    if fails:
        print("自测 %d 项不一致：%s" % (len(fails), fails))
        return 1
    print("自测通过：触发/未触发/从未审查/散文豁免 四态（判据可证伪）")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="对抗式审查触发器（W1000）")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return _self_test()
    for line in notice_lines():
        print(("WARN  " if line.startswith("⚠") else "NOTE  ") + line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
