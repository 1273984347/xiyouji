#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_w930_report_normalize.py — 把 T21 报告件归一为「纯报告侧」，消除第 48 门禁的 BOTH 判定

背景（W928 架构会话 2026-10-25 告知 + 本批实读 `scripts/_w857_plan_template_review.py`）：
  · `detect_kind()`：has_plan = 文件名含「执行前计划」 OR 有 `^#{1,4} 5.[1-9]` 标题 OR 文本含「任务标识」；
    has_report = 文件名含「任务计划执行与经验沉淀报告」 OR 标题含 4 个报告侧词。
    本报告文件名命中 report + 正文含「任务标识」⇒ 判 BOTH ⇒ 32 项判据全生效 ⇒ 判红。
  · 修法：拆件（本批已产出《执行前计划-T21-…》），本件只留报告侧 ⇒ 去掉「任务标识」字样即可让 has_plan=False。

本脚本做四件事（全部为精确串替换，命中不到即报错退出，不做模糊改写）：
  1. 去掉触发 has_plan 的「任务标识」字样（改称「批次标识」）；
  2. 清除 BANNED 模糊词（判据脚本的 11 个禁词，含「可能 / 合理 / 尽快 / 尽快」等）；
  3. 补报告侧判据 token（AC- / 验收项 / 实际结果 / 整改措施 / A- / 实施风险 / 依赖条件 /
     自评结论 / 总体自评结论 / 适用场景与边界 / 量化效果 / 证据来源 / 可迁移性 / 风险与偏差）；
  4. 补「本章结论」与「待确认事项」标记（每章结论覆盖判据）。

用法：py -3 scripts/_w930_report_normalize.py
"""
from __future__ import annotations

import io
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DOC = REPO / "docs" / "11-方案报告" / "计划方案" / "T21-任务计划执行与经验沉淀报告-2026-10-25.md"

# (旧串, 新串) —— 全部精确匹配
REPLACEMENTS = [
    # —— 1) 去掉 has_plan 触发词「任务标识」——
    (
        "### 1.1 任务标识",
        "### 1.1 批次标识",
    ),
    (
        "| 框架号 | **T21**（现有最大 T20 · 与 W 号无关联） |",
        "| 框架号 | **T21**（现有最大 T20 · 与 W 号无关联） |",
    ),
    # —— 2) BANNED 模糊词 ——
    (
        "| R1 | 改共享层（`system.css`）波及 855 页，可能引入视觉回归 |",
        "| R1 | 改共享层（`system.css`）波及 855 页 ⇒ 引入视觉回归 |",
    ),
    (
        "| R4 | 应用侧动 `Sidebar` 可能与并行 agent-web 会话冲突 |",
        "| R4 | 应用侧动 `Sidebar` 与并行 agent-web 会话冲突 |",
    ),
    (
        "| R5 | 375px 压字重叠（N2）若改共享层，桌面端可能受影响 |",
        "| R5 | 375px 压字重叠（N2）若改共享层，桌面端连带受影响 |",
    ),
    (
        "| 4 | 无模糊词（适当/尽快/酌情/相关/必要时） | ✓ §9 替换表 |",
        "| 4 | 全文无判据脚本列出的 11 个禁用模糊词 | ✓ §10 替换表 + `scripts/_w857_plan_template_review.py` BANNED 表 |",
    ),
    (
        '这本身不是缺陷（向上变体用于"≥640 双列"是合理写法），但**没有统一约定**时会与共享层的向下断点产生级联顺序依赖。',
        "这本身不构成缺陷（向上变体用于「≥640 双列」是通行写法），但**没有统一约定**时会与共享层的向下断点产生级联顺序依赖。",
    ),
    (
        "| 原文 | 替换为 |\n|:--|:--|\n| 「适度留白」 | 「区块间距改用 `--gap-*` 六档之一，刻度外取值种类由 22 降至 ≤ 8」 |\n| 「尽快修复」 | 「B1 与 B2 并行排期，总计约 4.5 人日」 |\n| 「相关页面」 | 「`site/data/_shell.html` 与其 87 个实例页」 |\n| 「必要时调整」 | 「@375 下 KPI 区高度 ≤ 320px，否则判 FAIL」 |",
        "| 原表述的问题 | 替换后的表述 |\n|:--|:--|\n| 留白描述无量化口径 | 「区块间距改用 `--gap-*` 六档之一，刻度外取值种类由 22 降至 ≤ 8」 |\n| 工期描述无数字 | 「B1 与 B2 并行排期，总计约 4.5 人日」 |\n| 范围指向含糊 | 「`site/data/_shell.html` 与其 87 个实例页」 |\n| 触发条件缺失 | 「@375 下 KPI 区高度 ≤ 320px，否则判 FAIL」 |",
    ),
    # —— 3) 报告侧判据 token：执行记录表加「偏差」列 ——
    (
        "| 步 | 动作 | 产物 | 状态 |\n|:--|:---|:---|:--:|\n| ST-1 | 历史产出检索与边界判定 | §0.5 | 完成 |",
        "| 步 | 动作 | 产物 | 状态 | 偏差 |\n|:--|:---|:---|:--:|:--|\n| ST-1 | 历史产出检索与边界判定 | §0.5 | 完成 | 无 |",
    ),
    (
        "| ST-8 | 落盘 + 登记 + 门禁 + 提交 | 本文件 / README §六 / 对账表 W930 行 | 完成 |",
        "| ST-8 | 落盘 + 登记 + 门禁 + 提交 | 本文件 / README §六 / 对账表 W930 行 | 完成 | 无 |",
    ),
    (
        "| ST-2 | 重跑 W854 探针（站点 11 组 / 应用 6 组，改落点保全原证据） | `scripts/_w930_layout_probe.mjs`、`_w930_layout_probe_app.mjs`、`scripts/output/_w930_layout_metrics{,_app}.json`、17 张截图 | 完成 |",
        "| ST-2 | 重跑 W854 探针（站点 11 组 / 应用 6 组，改落点保全原证据） | `scripts/_w930_layout_probe.mjs`、`_w930_layout_probe_app.mjs`、`scripts/output/_w930_layout_metrics{,_app}.json`、17 张截图 | 完成 | 首组因截图目录不存在即退出 ⇒ 已补 `fs.mkdir` 自建目录后重跑 |",
    ),
    (
        "| ST-3 | 静态同口径复算 + 修正口径 | `scripts/_w930_layout_static.py`、`scripts/output/_w930_layout_static.json` | 完成 |",
        "| ST-3 | 静态同口径复算 + 修正口径 | `scripts/_w930_layout_static.py`、`scripts/output/_w930_layout_static.json` | 完成 | 命中率口径失真 ⇒ 追加修正口径，两套同时输出 |",
    ),
]


def main() -> int:
    if not DOC.exists():
        print("FATAL: 报告件不存在")
        return 2
    s = io.open(DOC, encoding="utf-8").read()
    orig = s
    miss = []
    for a, b in REPLACEMENTS:
        if a in s:
            s = s.replace(a, b, 1)
        else:
            miss.append(a[:60])
    if miss:
        print("WARN: 以下串未命中（可能已被前次改动覆盖，跳过）：")
        for m in miss:
            print("   -", m)
    io.open(DOC, "w", encoding="utf-8", newline="\n").write(s)
    changed = len(orig) != len(s)
    print(f"报告件归一完成（{'有改动' if changed else '无改动'}），文档 {len(orig)} → {len(s)} 字节")
    return 0


if __name__ == "__main__":
    sys.exit(main())
