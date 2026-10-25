#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""W954 第 43 篇复盘批 · 登记面同步（README / CHANGELOG / HANDOVER / file-index）

幂等：每处插入前先断言目标不存在；已存在则跳过并打印。
用法：py -3 scripts/_w954_register_surfaces.py [--dry-run]
"""
import argparse
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README = os.path.join(ROOT, "docs", "11-方案报告", "README.md")
CHANGELOG = os.path.join(ROOT, "CHANGELOG.md")
HANDOVER = os.path.join(ROOT, "HANDOVER.md")
FILEINDEX = os.path.join(ROOT, "scripts", "output", "file-index.md")
PLAN_DIR = os.path.join(ROOT, "docs", "11-方案报告", "计划方案")

# ── README §五：第 43 篇登记行（续接本目录全局序号 25）────────────────
R43_ROW = (
    "| 25 | 工作复盘与优化分析报告（第 43 篇·2026-10-26·W795–W953 全区间） | "
    "[工作复盘与优化分析报告-2026-10-26.md](工作复盘与优化分析报告/工作复盘与优化分析报告-2026-10-26.md) | "
    "断档 **167.5 小时**（6 天 23 小时 32 分·跨 159 个 W 号 / 354 笔提交·该系列建立以来最长空窗）后补做全区间复盘："
    "CHANGELOG 现役面 + **归档面合看** 149 段 / 台账 154 行 / 提交 354 笔（8 天）/ 12 组主题分组（素材图 27·设计迁移 24·元规则门禁 20·工具链 17·审查 16…）；"
    "**五类登记漂移量化**（事实源=git·声明源=登记面）——CHANGELOG 段状态字段滞后 **91 批** / 台账滞后 **7 批** / 零提交 **6 批** / 有行无段 **6 批** / 有段无行 **1 批**；"
    "**本批开工即被 preflight 拒绝**（8 条 touches 交集 FAIL ⇒ 并发保护被自身欠账卡死）→ 按规则③回写后 **EXIT=0**；"
    "新经验 **E-25~E-31**（含「登记面不是事实源」「归档面须合看」「段状态串行错位」）/ 问题族 **FAM-40~42** / 工作流 **WF-08~09** / 改进项 **P-43-01~05**；"
    "取证脚本 `_w954_review_evidence.py`（全篇数字唯一源头·可复算） |\n"
)

# ── README §六：T-27 两行（续接本目录全局序号 31 / 32）─────────────────
R27_PLAN_ROW = (
    "| 31 | T-27《执行前计划》— 第 43 篇工作复盘批（W954：W795–W953 全区间复盘·2026-10-26·V1.0） | "
    "[执行前计划-T27-第43篇工作复盘批.md](计划方案/执行前计划-T27-第43篇工作复盘批.md) | "
    "框架第二十七次执行：用户 2026-10-26 问「多长时间没做复盘了」→ 实测断档 **167.5 小时** / 159 个 W 号 / 354 笔提交 → 问卷裁决「补做·全区间」；"
    "含 9 条 AC + 9 步 ST + 7 项 V 指标 + 6 条风险 + **8 条决策**（含「事实源=git·登记面降为声明面」「归档面须合看」「按 git 事实回写他方行」三条关键取舍）+ 12 项自包含检查 |\n"
)
R27_REPORT_ROW = (
    "| 32 | T-27《任务计划、执行与经验沉淀报告》— 第 43 篇工作复盘批（2026-10-26·V1.0·W954） | "
    "[T27-任务计划执行与经验沉淀报告-2026-10-26.md](计划方案/T27-任务计划执行与经验沉淀报告-2026-10-26.md) | "
    "框架第二十七次执行的终稿报告：① **取证脚本化**——新建 `_w954_review_evidence.py`（CHANGELOG 现役面 + 归档面 + 对账表 + git 提交图**四源合取**）作全篇数字唯一源头；"
    "② **五类登记漂移量化**（A 台账滞后 7 / B CHANGELOG 状态滞后 91 / C 零提交 6 / D 有行无段 6 / E 有段无行 1）——**登记面不是事实源**已被机器判据与并发门禁各撞一次；"
    "③ **止血**——按台账规则③回写 7 批陈旧在途状态 + W937 标「已停止·未收官」并清零 touches ⇒ **preflight 由 8 条 FAIL 恢复 EXIT=0**；"
    "④ **取证工具自纠 5 处**（归档漏读 / 前缀误判 / 闭合词三态 / 边界切分 / 分类覆盖不全）逐条留证；含 6 条经验沉淀（E-01~E-06·对应复盘全局 E-25~E-31）+ 6 条偏差留档 + 6 项未验证项显式声明 + 7 项后续行动 |\n"
)

# ── CHANGELOG W954 段 ────────────────────────────────────────────────
CHANGELOG_SEG = """### W954（2026-10-26）：第 43 篇《工作复盘与优化分析报告》入库批（W795–W953 全区间·149 段 / 154 行 / 354 提交）

> **来源**：用户 2026-10-26 问「多长时间没做复盘了」→ 实测主线复盘断档 **167.5 小时**（6 天 23 小时 32 分·跨 159 个 W 号 / 354 笔提交）→ 经问卷裁决「**补做 · 覆盖 W795–W953 全区间**」。

> - **文件**：docs/11-方案报告/工作复盘与优化分析报告/工作复盘与优化分析报告-2026-10-26.md、docs/11-方案报告/计划方案/执行前计划-T27-第43篇工作复盘批.md、docs/11-方案报告/计划方案/T27-任务计划执行与经验沉淀报告-2026-10-26.md、scripts/_w954_review_evidence.py、scripts/_w954_ledger_backfill.py、scripts/output/_w954_review_evidence.json、docs/11-方案报告/README.md、docs/00-导读/W批次编号对账表.md、HANDOVER.md、scripts/output/file-index.md

**断档事实**：第 42 篇（2026-10-19 01:10）至本篇 **167.5 小时零复盘**——该系列建立以来最长空窗（历史节奏 2026-10-07→10-19 共 12 天 14 篇·约 0.85 篇/天·本空窗约等欠 **6 篇**）。

**取证脚本化**：新建 `scripts/_w954_review_evidence.py` 作全篇统计数字的**唯一源头**——CHANGELOG 现役面 + **归档面** + 对账表 + git 提交图**四源合取**（只读现役面会漏 W795–W802 共 8 段·归档面须合看）；产物 `scripts/output/_w954_review_evidence.json`。

**五类登记漂移量化（事实源=git·声明源=登记面）**：CHANGELOG 段状态字段滞后 **91 批** / 台账滞后 **7 批**（W931/936/938/940/942/943/944·各有 1–3 笔提交已落库）/ 零提交 **6 批**（W907/908/910/911/929/937）/ 台账有行两面无段 **6 批** / 有段台账无行 **1 批**（W895）。

**本批开工即被 preflight 拒绝**：8 个陈旧「在途」批次的 touches 与本批交集非空（CHANGELOG.md / scripts/output/file-index.md）⇒ **并发保护被自身历史欠账卡死**；按台账规则③「以 git 历史为唯一事实源判定并回写」订正 7 批状态 + W937 标「已停止·未收官」并清零其 touches（残留经 git 核实为零改动）⇒ preflight 由 **8 条 FAIL 恢复 EXIT=0**。

**新经验与改进项**：E-25~E-31（登记面不是事实源 / 并发保护被欠账阻塞 / 归档面须合看 / 段状态串行错位 / 用户二次复核是第四道门 / 同族由构造保证 / 人工判据边界）· FAM-40~42 · WF-08~09 · P-43-01~05。

> - **验证**：取证脚本实跑 ⇒ 149 段 / 154 行 / 354 提交 / 12 组主题分组 / 五类漂移分档全部可复算（复算命令见报告附录 B）· preflight 回写后 **EXIT=0** 且 touches 交集检查 OK · 台账 8 行状态逐行 grep 核对 · 文档面门禁见 T27 报告 §4.4。
> - **状态**：已收官（提交 hash 见文末回填）

"""

# ── HANDOVER 同步 ───────────────────────────────────────────────────
HANDOVER_ITEM = (
    "- **W954 第 43 篇工作复盘批**：补做第 43 篇《工作复盘与优化分析报告》（W795–W953 全区间·149 段 / 154 行 / 354 提交·"
    "167.5 小时断档后一次性补齐）；新建取证脚本 `_w954_review_evidence.py` 作数字唯一源头；量化五类登记漂移"
    "（CHANGELOG 段状态滞后 91 批 / 台账滞后 7 批 / 零提交 6 批 / 有行无段 6 批 / 有段无行 1 批）⇒ **登记面不是事实源**；"
    "按 git 事实回写台账 8 行 ⇒ preflight 由 8 条 FAIL 恢复 EXIT=0。\n"
)

# ── file-index W954 段 ──────────────────────────────────────────────
FILEINDEX_SEG = """## W954 第 43 篇工作复盘批（2026-10-26）

| 文件 | W | 说明 |
|---|---|---|
| docs/11-方案报告/工作复盘与优化分析报告/工作复盘与优化分析报告-2026-10-26.md | W954 | 新增：第 43 篇复盘（W795–W953 全区间·149 段 / 154 行 / 354 提交·八条核心发现·E-25~E-31 / FAM-40~42 / WF-08~09 / P-43-01~05） |
| docs/11-方案报告/计划方案/执行前计划-T27-第43篇工作复盘批.md | W954 | 新增：T-27 执行前计划（9 条 AC / 9 步 ST / 7 项 V 指标 / 8 条决策 / 12 项自包含检查） |
| docs/11-方案报告/计划方案/T27-任务计划执行与经验沉淀报告-2026-10-26.md | W954 | 新增：T-27 执行与经验沉淀报告（9 步执行记录 / 验收表 / 6 条偏差 / 6 条经验 E-01~E-06） |
| scripts/_w954_review_evidence.py | W954 | 新增：复盘取证脚本（CHANGELOG 现役面 + 归档面 + 对账表 + git 提交图四源合取 + 五类漂移分类 + 12 组主题分组） |
| scripts/_w954_ledger_backfill.py | W954 | 新增：台账回写脚本（8 行状态订正 + 认领行追加·先断言后写·幂等可重跑） |
| scripts/output/_w954_review_evidence.json | W954 | 新增：取证产物（区间事实与漂移分档的机器可读快照） |
| docs/11-方案报告/README.md | W954 | 登记：§五 增第 43 篇行（序号 25）+ §六 增 T-27 两行（序号 31/32）+ 件数刷新 |
| docs/00-导读/W批次编号对账表.md | W954 | 登记：W954 认领行 + 回写 7 批陈旧在途状态 + W937 标「已停止」并清零 touches |
| HANDOVER.md | W954 | 同步：一、当前进度增 W954 条目 + 最后更新链前置 W954 |
| CHANGELOG.md | W954 | 新增：W954 版段（四件套） |
| scripts/output/file-index.md | W954 | 登记：W954 段（本段） |

"""


def read(p):
    with open(p, encoding="utf-8", newline="") as f:
        return f.read()


def write(p, s):
    with open(p, "w", encoding="utf-8", newline="") as f:
        f.write(s)


def eol_of(text):
    """文件主行尾（CRLF 共享面 / LF 文档面混用——插入内容必须随文件归一）。"""
    return "\r\n" if "\r\n" in text else "\n"


def to_eol(s, eol):
    """把插入串的行尾归一到目标文件的主行尾（先归一为 LF 再转）。"""
    return s.replace("\r\n", "\n").replace("\n", eol)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    changed = {}

    # ── README ───────────────────────────────────────────────────────
    p = README
    t = read(p)
    orig = t
    eol = eol_of(t)
    n_files = len([f for f in os.listdir(PLAN_DIR) if f.endswith(".md")])
    # §一 目录索引表 + §五 标题的「13 篇」计数
    t = t.replace("第 N 篇系列工作复盘（13 篇）", "第 N 篇系列工作复盘（14 篇）")
    t = t.replace("### 五、工作复盘与优化分析报告（13 篇·", "### 五、工作复盘与优化分析报告（14 篇·")
    # §六 件数（计划方案目录实际 md 文件数）
    t = re.sub(r"### 六、计划方案（\d+ 件）", f"### 六、计划方案（{n_files} 件）", t)
    # §五 表尾追加（第 42 篇行之后）
    if "工作复盘与优化分析报告-2026-10-26.md" not in t:
        anchor = "| 24 | 工作复盘与优化分析报告（第 42 篇"
        idx = t.find(anchor)
        assert idx != -1, "§五 表尾锚点未找到"
        end = t.find("\n", idx) + 1
        t = t[:end] + to_eol(R43_ROW, eol) + t[end:]
        print("README §五: 第 43 篇行已追加（序号 25）")
    else:
        print("README §五: 第 43 篇行已存在（幂等跳过）")
    # §六 表尾追加（T-26 执行报告行之后）
    if "执行前计划-T27-第43篇工作复盘批.md" not in t:
        anchor = "| 30 | T-26《任务计划、执行与经验沉淀报告》"
        idx = t.find(anchor)
        assert idx != -1, "§六 表尾锚点未找到"
        end = t.find("\n", idx) + 1
        t = t[:end] + to_eol(R27_PLAN_ROW, eol) + to_eol(R27_REPORT_ROW, eol) + t[end:]
        print("README §六: T-27 两行已追加（序号 31/32）")
    else:
        print("README §六: T-27 行已存在（幂等跳过）")
    assert t != orig
    changed[p] = t

    # ── CHANGELOG ────────────────────────────────────────────────────
    p = CHANGELOG
    t = read(p)
    eol = eol_of(t)
    if "### W954（2026-10-26）" in t:
        print("CHANGELOG: W954 段已存在（幂等跳过）")
    else:
        anchor = "### W953（2026-10-26）："
        idx = t.find(anchor)
        assert idx != -1, "CHANGELOG W953 段锚点未找到"
        t = t[:idx] + to_eol(CHANGELOG_SEG, eol) + t[idx:]
        print("CHANGELOG: W954 段已插入（置于顶段 W953 之前）")
    changed[p] = t

    # ── HANDOVER ─────────────────────────────────────────────────────
    p = HANDOVER
    t = read(p)
    eol = eol_of(t)
    if "W954 第 43 篇工作复盘批" not in t:
        t = t.replace("> 最后更新：2026-10-26（W953 themes 库专题题图批）",
                      "> 最后更新：2026-10-26（W954 第 43 篇工作复盘批）·2026-10-26（W953 themes 库专题题图批）")
        t = t.replace("## 一、当前进度（W953 themes 库专题题图批；更早批次详见 CHANGELOG.md）",
                      "## 一、当前进度（W954 第 43 篇工作复盘批；更早批次详见 CHANGELOG.md）")
        anchor = to_eol("## 一、当前进度（W954 第 43 篇工作复盘批；更早批次详见 CHANGELOG.md）\n", eol)
        idx = t.find(anchor)
        assert idx != -1, "HANDOVER §一 标题未替换成功"
        t = t[:idx + len(anchor)] + to_eol(HANDOVER_ITEM, eol) + t[idx + len(anchor):]
        print("HANDOVER: 一、当前进度条目 + 最后更新链已同步")
    else:
        print("HANDOVER: W954 条目已存在（幂等跳过）")
    changed[p] = t

    # ── file-index ───────────────────────────────────────────────────
    p = FILEINDEX
    t = read(p)
    eol = eol_of(t)
    if "## W954 第 43 篇工作复盘批" in t:
        print("file-index: W954 段已存在（幂等跳过）")
    else:
        anchor = "## W953 themes 库专题题图批"
        idx = t.find(anchor)
        assert idx != -1, "file-index W953 段锚点未找到"
        t = t[:idx] + to_eol(FILEINDEX_SEG, eol) + t[idx:]
        print("file-index: W954 段已插入（置于顶段之前）")
    changed[p] = t

    if args.dry_run:
        print("DRY-RUN: 未写盘")
        return 0
    for path, text in changed.items():
        write(path, text)
        print(f"已写盘: {os.path.relpath(path, ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
