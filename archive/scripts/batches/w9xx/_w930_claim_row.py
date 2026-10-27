#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_w930_claim_row.py — 在 W 批次编号对账表主表登记 W930 认领行

纪律（来自 AGENTS.md §4.3 / 对账表「登记 ASCII 纪律」）：
  · 追加行用表格行追加，禁改历史行；
  · 插入位置 = W929 行之后（号序相邻），避免打乱既有升序；
  · 文件读写一律 io.open(encoding='utf-8')，禁 PowerShell Set-Content（会写 UTF-8 BOM）；
  · 「关联 commit」「CHANGELOG 版段」两列施工后回填，先占位；
  · 幂等：若该号已有行则直接退出，**绝不覆盖他人已认领的号**。

用法：py -3 scripts/_w930_claim_row.py
"""
from __future__ import annotations

import io
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TABLE = REPO / "docs" / "00-导读" / "W批次编号对账表.md"

BATCH_NO = "W930"
PREV_NO = "W929"

ROW = (
    "| W930 | 界面布局复核与落地方案批（用户 2026-10-25 令「帮我优化现有界面布局：先帮我做好信息层级梳理、"
    "区块分布与留白、操作动线、不同屏幕适配都过一遍，每处调整讲清理由」；问卷答复 = **范围全站都做**"
    "（site/ 静态站 + site/reader/ + xiyouji-agent-web/）· **主攻信息层级（一屏信息量过载）** · "
    "**先出审查报告与落地方案、用户过一遍再动代码**）：① **定位判据**——用户指令与 W854（2026-10-21 "
    "界面布局审计）的四维（信息层级/区块留白/操作动线/多屏适配）几乎逐字相同，按 W926 §7.1 E-03"
    "「同一条指令重复下达时先查历史再动手」判为**复核 + 补审**而非重做；本批增量 = ①W854 18 条"
    "四天后现状复核（重跑 W854 探针：站点 11 组 + 应用 6 组，新旧 metrics JSON 逐项对拍）"
    "②W854 与 W926 均未覆盖的维度补审（v4 令牌落地进度差 / 页面级内联断点分布 / 375px 下装饰图"
    "压字重叠）③可施工落地方案（每条带理由 + 可机检验收判据 + 批次序）；② **W 号二次让号**——W928 已被"
    "并行「D-1 实跑批」会话**先行落地认领**（主表已有 W928 行 + 工作树 `xiyouji-agent-web/deploy/pg/` "
    "改动在途），W929 又被并行「Hero 素材图成套批」会话占位（该行在本批登记脚本运行期间落地）；"
    "两次均按「先落地者保留」让号，本批取 **W930**；③ **框架号 T21**（现有最大 T20）；"
    "④ **只出报告与方案、不改 site/ 与应用代码**（用户本轮明示「过一遍再动代码」） | "
    "—（待回填） | —（待回填） | 在途（认领·未收官） | "
    "本会话（主会话 · 界面布局复核批） | "
    "`docs/11-方案报告/计划方案/T21-任务计划执行与经验沉淀报告-2026-10-25.md`（新增）· "
    "`docs/11-方案报告/README.md`（§六 登记行）· `docs/00-导读/W批次编号对账表.md`（本行）· "
    "`scripts/_w928_layout_static.py` / `_w928_layout_diff.py` / `_w928_layout_attr.py` / "
    "`_w928_layout_detail.py` / `_w928_layout_residual.py` / `_w928_layout_probe.mjs` / "
    "`_w928_layout_probe_app.mjs`（新增·一次性诊断件）· `scripts/output/_w928_*.json`（新增·证据） |"
)


def main() -> int:
    text = io.open(TABLE, encoding="utf-8").read()
    if re.search(r"^\| " + BATCH_NO + r" \|", text, re.M):
        print(BATCH_NO + " 认领行已存在，幂等退出（不重复插入、不覆盖他人认领）")
        return 0
    lines = text.split("\n")
    idx = None
    for i, ln in enumerate(lines):
        if ln.startswith("| " + PREV_NO + " |"):
            idx = i
            break
    if idx is None:
        print("FATAL: 未找到 " + PREV_NO + " 行，拒绝盲目插入")
        return 2
    lines.insert(idx + 1, ROW)
    io.open(TABLE, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
    print(BATCH_NO + " 认领行已插入（表内第 " + str(idx + 2) + " 行）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
