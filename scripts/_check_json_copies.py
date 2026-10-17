#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_check_json_copies.py — W563/A-3：site/data/json/ 部署副本 ↔ scripts/output/data/ 原件对账。

断言：47 个副本逐一字节相等；副本集合与「原件中应部署的集合」双向一致。
（第 9 门禁的副本对账子检查只比数组长度＝CI 跨平台安全版；**字节级强对账由本脚本承担**·
W770 自 archive 恢复——W770 实证：副本曾含 W678/W691 修复而原件未回灌，sync_data_json
单向同步会把修复反灌回副本；W770 已 20 件回灌对齐 + 本项目本批后副本与原件字节全等。）
用法：python scripts/_check_json_copies.py（本地自检·CI 无原件时由门禁跳过语义覆盖）
"""
import filecmp
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "scripts", "output", "data")
DST = os.path.join(ROOT, "site", "data", "json")


def main():
    copies = sorted(f for f in os.listdir(DST) if f.endswith(".json"))
    problems = []
    for f in copies:
        src = os.path.join(SRC, f)
        if not os.path.exists(src):
            problems.append("副本无原件: " + f)
        elif not filecmp.cmp(os.path.join(DST, f), src, shallow=False):
            problems.append("内容漂移: " + f)
    print(f"副本 {len(copies)} 个（预期 47） · 问题 {len(problems)}")
    if len(copies) != 47:
        problems.append("副本数 %d != 47——出现新增 fetch 目标但未同步副本，或残留历史副本" % len(copies))
    for p in problems:
        print("  FAIL", p)
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
