#!/usr/bin/env python3
"""_w959_version_sync.py — W959 版本面 + 登记面同步（W957 → W959·T10 V1.1 计数口径订正批）。

沿用 W957 批验证过的「**按文件聚合 · 逐文件读改写一次**」结构。
纪律：每处替换先断言命中数（fail-closed）· 幂等 · 行尾随文件归一 · 插入块按目标行尾转写。

用法：py -3 scripts/_w959_version_sync.py [--dry-run]
"""
import argparse
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CHANGELOG_SEG = """### W959（2026-10-26）：T10《Playwright 历史问题全谱审计报告》V1.1 计数口径订正批

> **来源**：用户 2026-10-26 审查意见——「方法论质量是 A 级，但作为审计件有一处**必须先修的硬伤**：核心计数不自洽（审计件的第一价值是可复验，数字对不上就不可复验）」。
>
> - **文件**：docs/11-方案报告/计划方案/T10-任务计划执行与经验沉淀报告-2026-10-22.md、scripts/_w959_t10_v11.py、docs/11-方案报告/README.md、docs/00-导读/W批次编号对账表.md

**计数订正**：§13 全谱表**实列 31 条**（A 7 + B 4 + C 6 + D 5 + E 3 + F 1 + G 2 + H 3），而 V1.0 全篇按「25 项」计数（首轮会话答复口径，落盘扩容后计数未同步）⇒ V1.1 全面改为 31 条口径，并写明 25 → 31 的差额来源（首轮口径 + 补录 5 条非缺陷项 + H 族独立成族 1 条开放项）。

**四态显式化**：已修复 **21** · 非缺陷 **5**（设计内 / 现状 / 已澄清 / 结论已入库）· 仍开放 **5** · 未验证 **0**；并写明「非缺陷」项为何不计入缺陷（本就不可「修复」）。

**开放项双口径**：V-04 拆为条目口径（≤5·实测 5）与根因口径（≤3·实测 3），并**披露** V1.0 的预警规则（>3 提级 P0）按条目口径本应触发却未触发（口径声明缺失·非数据错误）。

**§18 口径说明**：「6 件」为交付物**类别数**、「11 件」为**文件件数**，两个数口径不同、不可互换。

**落实 4 处商榷**：§14.2「无增量覆盖」按本报告 E-05 纪律降级为**待验证**并给出取证方法（用例覆盖对比表）· P-05 剥离 A-6（模块解析分裂需另配设计）· P-01 删步骤处加防回归注释建议 · E-09 加工具化路径备注。

**结论与判断一字未改**——本批只改计数与口径声明。

**状态**：**已收官**（V1.1 订正批；**让号**：W958 已被并行会话「归档分段批」占用 ⇒ 本批 W959）

"""

HANDOVER_ITEM = (
    "- **W959 T10 V1.1 计数口径订正批**：用户审查意见指出 T10 审计报告「核心计数不自洽」⇒ "
    "§13 实列 **31 条**（V1.0 误记 25 项·首轮口径未同步）全面订正；状态四态显式化"
    "（已修复 21 / 非缺陷 5 / 仍开放 5 / 未验证 0）；开放项拆条目与根因双口径并披露 V1.0 预警未触发；"
    "§18「6 类 / 11 件」补口径说明；落实 4 处商榷（§14.2 降级待验证 / P-05 剥离 A-6 / "
    "P-01 防回归注释 / E-09 工具化路径）——**结论与判断一字未改**；**让号**：W958 被并行会话占用 ⇒ 本批 W959。\n"
)

STRUCTURE_ITEM = (
    "- **W959（2026-10-26）**：T10 审计报告 V1.1 计数口径订正批（31 条四态 + 开放项双口径）"
    "<!--doc-sync:exempt-->\n"
)

FILE_INDEX_SEG = """## W959 T10 V1.1 计数口径订正批（2026-10-26）

| 文件 | W | 说明 |
|---|---|---|
| docs/11-方案报告/计划方案/T10-任务计划执行与经验沉淀报告-2026-10-22.md | W959 | 修改：V1.1 计数口径订正（31 条四态 + 开放项双口径 + §18 口径说明 + 4 处商榷落实·结论未改） |
| scripts/_w959_t10_v11.py | W959 | 新增：V1.1 订正脚本（行号 + 断言片段双重约束·字节级改写保行尾·31 条作业·倒序应用·幂等） |
| docs/11-方案报告/README.md | W959 | 登记：§六 T-10 行版本标注更新为 V1.1（W959 计数口径订正批） |
| docs/00-导读/W批次编号对账表.md | W959 | 登记：W959 认领行（让号留痕）+ 收官回填 |
| HANDOVER.md | W959 | 同步：一、当前进度增 W959 条目 + 最后更新链前置 + 当前 HEAD |
| CHANGELOG.md | W959 | 新增：W959 版段（四件套） |
| scripts/output/file-index.md | W959 | 登记：W959 段（本段） |

"""

PLAN = {
    "CHANGELOG.md": {
        "replaces": [
            ("编号规则段上限 W001-W957 → W001-W959",
             "W### ID（W001-W957）", "W### ID（W001-W959）", 1),
        ],
        "inserts": [
            ("新增 W959 版段（插在 W957 段之前）",
             "### W957（2026-10-26）：", CHANGELOG_SEG, 1, "before"),
        ],
    },
    "README.md": {
        "replaces": [
            ("当前批次行 W957 → W959",
             "> **当前批次 W957（2026-10-26）**：GSAP 动效体系引入批施工批（公共动效载体 + 试点页三类动效 + 写法机检）<!--doc-sync:exempt-->",
             "> **当前批次 W959（2026-10-26）**：T10 审计报告 V1.1 计数口径订正批（31 条四态 + 开放项双口径）<!--doc-sync:exempt-->", 1),
        ],
        "inserts": [],
    },
    "docs/00-导读/项目说明.md": {
        "replaces": [
            ("当前批次行 W957 → W959",
             "> 当前批次 W957（2026-10-26）：GSAP 动效体系引入批施工批（公共动效载体 + 试点页三类动效 + 写法机检）·详细变更见",
             "> 当前批次 W959（2026-10-26）：T10 审计报告 V1.1 计数口径订正批（31 条四态 + 开放项双口径）·详细变更见", 1),
        ],
        "inserts": [],
    },
    "CITATION.cff": {
        "replaces": [
            ("批次号形态 version W957 → W959", 'version: "W957"', 'version: "W959"', 1),
        ],
        "inserts": [],
    },
    ".github/workflows/README.md": {
        "replaces": [
            ("头部版本链上限 W450-W957 → W450-W959", "→ W450-W957**", "→ W450-W959**", 1),
            ("头部项目标识 W957 → W959", "（`D:\\xiyouji`，W957）", "（`D:\\xiyouji`，W959）", 1),
        ],
        "inserts": [],
    },
    "HANDOVER.md": {
        "replaces": [
            ("「一、当前进度」标题 W957 → W959",
             "## 一、当前进度（W957 GSAP 动效体系引入批施工批；更早批次详见 CHANGELOG.md）",
             "## 一、当前进度（W959 T10 审计报告 V1.1 计数口径订正批；更早批次详见 CHANGELOG.md）", 1),
            ("「最后更新」链首 W957 → W959（文件头 + 文末行·两处同起句·分隔符各异故不带分隔符）",
             "最后更新：2026-10-26（W957 GSAP 动效体系引入批施工批）",
             "最后更新：2026-10-26（W959 T10 审计报告 V1.1 计数口径订正批）", 2),
            ("「当前 HEAD」W957 → W959",
             "当前 HEAD = W957（GSAP 动效体系引入批施工批：公共动效载体 + 试点 5 页三类动效 + 写法机检 + 实跑 30 组 0 FAIL）",
             "当前 HEAD = W959（T10 审计报告 V1.1 计数口径订正批：31 条四态 + 开放项双口径 + §18 口径说明 + 4 处商榷落实；结论未改）", 1),
        ],
        "inserts": [
            ("一、当前进度增 W959 条目（接在标题行之后）",
             "## 一、当前进度（W959 T10 审计报告 V1.1 计数口径订正批；更早批次详见 CHANGELOG.md）",
             HANDOVER_ITEM, 1, "after"),
        ],
    },
    "STRUCTURE.md": {
        "replaces": [],
        "inserts": [
            ("里程碑增 W959 条目（前置）",
             "- **W957（2026-10-26）**：", STRUCTURE_ITEM, 1, "before"),
        ],
    },
    "scripts/output/file-index.md": {
        "replaces": [],
        "inserts": [
            ("新增 W959 反向索引段（插在 W957 段之前·倒序）",
             "## W957 GSAP 动效体系引入批·施工批", FILE_INDEX_SEG, 1, "before"),
        ],
    },
}


def read(rel):
    path = os.path.join(ROOT, rel)
    with open(path, encoding="utf-8", newline="") as f:
        raw = f.read()
    if "\r\n" in raw:
        nl = "\r\n"
        bare_lf = any(ln == "\n" for ln in raw.split("\r\n"))
    elif "\n" in raw:
        nl = "\n"
        bare_lf = False
    else:
        nl = "\r"
        bare_lf = False
    if bare_lf:
        raise SystemExit("混合行尾：%s——先归一行尾" % rel)
    return raw, nl


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    for rel, spec in PLAN.items():
        raw, nl = read(rel)
        orig = raw
        notes = []
        for desc, old, new, expect in spec["replaces"]:
            n = raw.count(old)
            if n == 0 and raw.count(new) > 0:
                notes.append("SKIP  %s：%s（已应用·幂等）" % (rel, desc))
                continue
            if n != expect:
                print("ABORT  %s：命中 %d ≠ 期望 %d（%s）" % (rel, n, expect, desc))
                return 1
            raw = raw.replace(old, new)
            notes.append("REPL  %s：%s" % (rel, desc))
        for desc, anchor, block, expect, mode in spec["inserts"]:
            n = raw.count(anchor)
            if n != expect:
                print("ABORT  %s：锚点命中 %d ≠ 期望 %d（%s）" % (rel, n, expect, desc))
                return 1
            head = block.split("\n")[0]
            if head in raw:
                notes.append("SKIP  %s：%s（已存在·幂等）" % (rel, desc))
                continue
            blk = block.replace("\n", nl)
            if mode == "after":
                raw = raw.replace(anchor, anchor + nl + blk, 1)
            else:
                raw = raw.replace(anchor, blk + anchor, 1)
            notes.append("INS   %s：%s" % (rel, desc))
        for ln in notes:
            print(("DRY    " if args.dry_run else "") + ln)
        if raw == orig:
            print("       %s：无变化" % rel)
            continue
        if args.dry_run:
            print("DRY    %s：%d B → %d B" % (rel, len(orig), len(raw)))
            continue
        with open(os.path.join(ROOT, rel), "w", encoding="utf-8", newline="") as f:
            f.write(raw)
        print("OK     %s：%d B → %d B" % (rel, len(orig), len(raw)))

    print(("DRY-RUN " if args.dry_run else "版本面同步") + "完成：%d 个面" % len(PLAN))
    return 0


if __name__ == "__main__":
    sys.exit(main())
