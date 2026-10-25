#!/usr/bin/env python3
"""_w955_version_sync.py — W955 一次性版本面同步脚本（现役 W954 → W955）

背景：W955 = GSAP 动效体系引入批第一子批（前置体检 + 执行前计划）。
      按文档规范 §11.1「必须同步的文件」，每批完成后版本面须指向最新 W 段；
      `bump_version.py` 因方案 D 守卫已停用（它要求文档仍为「当前版本」形态），
      故沿用 W954 批的形态自建一次性脚本（参照 `_w954_version_sync.py`）。

纪律：
  · **只改版本面字面量**，不改历史段、不改叙述语义；
  · 每处替换**先断言命中数**，命中数不符即中止不写盘（fail-closed）；
  · **按文件聚合**（W955 修订·首版缺陷实证）：同一文件的多个 job 必须**读一次 → 依次改 → 写一次**；
    首版按 job 逐个读+最后统一写 ⇒ 同一文件的后一个 job 基于「未写盘的旧内容」计算 ⇒ **后写覆盖先写**，
    实测 CHANGELOG / HANDOVER / 报告 README 三文件的替换被插入动作静默覆盖（5 项门禁 FAIL 实证）；
  · **插入操作走倒序锚点**：CHANGELOG 新段插在 W954 段之前 · file-index 段插在 W954 段之前
    （第 17 门禁「file-index 段倒序断言」要求 W 号严格递减）· HANDOVER / STRUCTURE 条目前置；
  · 幂等：替换项若 old 不存在但 new 已存在 → 视为已应用并跳过；插入项若块首行已存在 → 跳过；
  · 行尾随文件主行尾归一（CRLF/LF 混用文件逐文件处理·不跨文件统一）；插入块按目标文件行尾转写；
  · **不动** site 页脚（触发站点面 + CSP 重算·门禁仅 WARN）与归档面（archive/）。

用法：py -3 scripts/_w955_version_sync.py [--dry-run]
"""
import argparse
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# 版本面内容定义
# ---------------------------------------------------------------------------

CHANGELOG_SEG = """### W955（2026-10-26）：GSAP 动效体系引入批第一子批（前置体检 + 执行前计划）

> **来源**：用户 2026-10-26 携 GSAP Skills 插件发起 → 问卷裁定「**四类动效全都要**（滚动叙事 / 入场编排 / 微交互 / 现有动画体检）· 载体 = `site/` 静态站 · 交付 = **先出计划再施工**」。

> - **文件**：docs/11-方案报告/计划方案/执行前计划-T28-GSAP动效体系引入批.md、scripts/_w955_motion_audit.py、scripts/output/_w955_motion_audit.json、scripts/_w955_ledger_claim.py、scripts/_w955_version_sync.py、docs/00-导读/W批次编号对账表.md、docs/11-方案报告/README.md

**前置体检（`scripts/_w955_motion_audit.py` · 8 组事实 · 数字唯一源头）**：全站 **857** 页（reader/people 216 · reader/themes 210 · en 138 · reader 102 · data 88 · reader/essays 45 · reader/culture 35 · reader/poetry 14 · 根 9）；含 `@keyframes` **331** 页 / 1,337 处（页面私有 keyframes 仅 8 个）；含 `reveal-in` **333** 页（逐页内联复制·公共载体缺位）；含 `prefers-reduced-motion` 守卫 **334** 页；**动效禁止清单基线 0 命中**（回弹 / 360° 旋转 / 无限循环 / 视差）；`d3 .duration(N>600)` **0 页**。

**体积与预算对账**：`site/system.css` **29,660 B**，超 DESIGN.md §4A.8 上限 25,497 B 达 **4,163 B**（既有欠账·本批分流登记不改）；`site/tokens.css` 23,039 B（余量 760 B）；GSAP 3.12.5 实测 `gsap.min.js` **72,214 B** + `ScrollTrigger.min.js` **43,380 B** = 115,594 B ⇒ 内联方案每页 115,594 B（857 页约 99.1 MB）、外链每页 119 B 标签 ⇒ 裁定外链 vendored。

**三条裁定（D-01 / D-02 / D-03）**：① 引入形态 = 外链 vendored（同源·零外域依赖·CSP `script-src 'self'` 允许）；② 落点 = 公共动效载体 `site/static/js/motion-gsap.js` + 试点 5 页分级引入（W471 规划的 `motion.js` 至今未落地·公共层是既有缺口）；③ 滚动叙事 = 章节级一次性进场 + 阅读进度联动（**非视差**——DESIGN.md §5 禁止清单 + `check_motion_ban.py` 全文正则扫描含注释与变量名）。

**验证**：第 48 门禁「计划方案合规」PASS（新增文件 32 项结构判据全项符合）· 模糊词 0 命中 · `preflight_check.py --self W955` = PASS（取号无撞号 / 与在途批次无 touches 交集）· 体检脚本可复算（重跑产出同一 JSON）· `verify_delivery.py --scope docs` 0 FAIL（**注**：`--scope auto`/full 档在本机实证挂死·python 进程 CPU 零增长·被委托段无超时保护——已记录为待修项，不在本批范围）。

**状态**：**已收官**（本批 = 取证 + 执行前计划 + 登记；**施工批 = W956**——公共载体落地 + 试点 5 页接入三类动效 + 机检判据 + 施工报告）

"""

HANDOVER_ITEM = (
    "- **W955 GSAP 动效体系引入批第一子批**（计划批）：用户携 GSAP Skills 插件发起"
    "「滚动叙事 / 入场编排 / 微交互 / 现有动画体检」全都要，载体 = `site/` 静态站，交付 = 先出计划再施工；"
    "前置体检 8 组事实（857 页 / 禁词基线 0 命中 / duration>600 0 页 / `system.css` 超 §4A.8 预算 4,163 B）；"
    "GSAP 3.12.5 实测 115,594 B ⇒ 裁定外链 vendored；落点 = 公共动效载体 + 试点 5 页分级引入；"
    "视差被 DESIGN §5 禁止 ⇒ 滚动叙事改为非视差形态；"
    "《执行前计划-T28》落 `docs/11-方案报告/计划方案/`（12 条 AC / 16 条 ASM / 14 步 ST / 9 指标 / 8 风险 / 9 决策）；"
    "**施工批 = W956**。\n"
)

STRUCTURE_ITEM = (
    "- **W955（2026-10-26）**：GSAP 动效体系引入批第一子批（前置体检 + 执行前计划·施工批 W956）"
    "<!--doc-sync:exempt-->\n"
)

FILE_INDEX_SEG = """## W955 GSAP 动效体系引入批第一子批（前置体检 + 执行前计划）（2026-10-26）

| 文件 | W | 说明 |
|---|---|---|
| docs/11-方案报告/计划方案/执行前计划-T28-GSAP动效体系引入批.md | W955 | 新增：T-28 执行前计划（3 目标 + 12 条 AC + 16 条 ASM + 14 步 ST + 9 指标 + 8 风险 + 9 决策 + 12 项自包含检查） |
| scripts/_w955_motion_audit.py | W955 | 新增：动效体检取证脚本（8 组事实·数字唯一源头·禁词基线复用 check_motion_ban 正则） |
| scripts/output/_w955_motion_audit.json | W955 | 新增：体检基线快照（页面分布 / 动效存量 / RM 覆盖 / 体积预算 / GSAP 体量测算） |
| scripts/_w955_ledger_claim.py | W955 | 新增：台账认领行追加器（只追加不改历史行 / 幂等 / 混行尾 fail-closed） |
| scripts/_w955_version_sync.py | W955 | 新增：版本面同步脚本（按文件聚合·逐文件读改写一次·断言命中数·倒序锚点） |
| docs/00-导读/W批次编号对账表.md | W955 | 登记：W955 认领行（认领即占号·单独提交） |
| docs/11-方案报告/README.md | W955 | 登记：§六 增 T-28 执行前计划行（序号 33）+ 件数刷新 |
| HANDOVER.md | W955 | 同步：一、当前进度增 W955 条目 + 最后更新链前置 W955 |
| CHANGELOG.md | W955 | 新增：W955 版段（四件套） |
| docs/INDEX.md | W955 | 重建：新增 T-28 执行前计划后重生成（765 篇文档 · 13 板块） |
| site/data/search.html | W955 | 刷新：站内搜索索引（中文）重嵌入（含新计划件条目） |
| site/en/search.html | W955 | 刷新：站内搜索索引（英文）重嵌入 |
| site/**（2 页 meta CSP） | W955 | 重算：搜索页内联脚本变更后的 CSP 哈希同步（2 页 · 861 个内联脚本哈希） |
| scripts/output/file-index.md | W955 | 登记：W955 段（本段） |

"""

REPORT_README_ROW = (
    "| 33 | T-28《执行前计划》— GSAP 动效体系引入批（W955：前置体检 + 执行前计划·施工批 W956·2026-10-26·V1.0） | "
    "[执行前计划-T28-GSAP动效体系引入批.md](计划方案/执行前计划-T28-GSAP动效体系引入批.md) | "
    "框架第二十八次执行：用户 2026-10-26 携 GSAP Skills 插件发起「滚动叙事 / 入场编排 / 微交互 / 现有动画体检」"
    "**四类全都要** → 问卷裁定载体 = `site/` 静态站、交付 = 先出计划再施工；"
    "**前置体检 8 组事实**（857 页 / 含 `@keyframes` 331 页 / 含 `reveal-in` 333 页 / RM 守卫 334 页 / "
    "**动效禁止清单基线 0 命中** / `d3 .duration(N>600)` 0 页 / `system.css` 29,660 B 超 §4A.8 上限 **4,163 B** / "
    "裸 ease 违规 4 处）；**GSAP 3.12.5 实测 115,594 B** ⇒ 裁定外链 vendored（内联方案 857 页约 99.1 MB）；"
    "落点 = 公共动效载体 `site/static/js/motion-gsap.js` + 试点 5 页分级引入"
    "（W471 规划的 `motion.js` 至今未落地·公共层是既有缺口）；"
    "**视差被 DESIGN §5 禁则** ⇒ 滚动叙事改为章节级进场 + 进度联动（非视差）；"
    "含 3 目标 + 12 条 AC + 16 条 ASM + 14 步 ST + 9 指标 + 8 风险 + **9 决策** + 12 项自包含检查 · "
    "**施工批 = W956** |\n"
)

# ---------------------------------------------------------------------------
# 按文件聚合的作业表（每文件：replaces + inserts）
# ---------------------------------------------------------------------------

PLAN = {
    "CHANGELOG.md": {
        "replaces": [
            ("编号规则段上限 W001-W954 → W001-W955",
             "W### ID（W001-W954）", "W### ID（W001-W955）", 1),
        ],
        "inserts": [
            ("新增 W955 版段（插在 W954 段之前）",
             "### W954（2026-10-26）：", CHANGELOG_SEG, 1, "before"),
        ],
    },
    "README.md": {
        "replaces": [
            ("当前批次行 W954 → W955",
             "> **当前批次 W954（2026-10-26）**：工作复盘报告入库批（W795–W953 全区间复盘、149 段、154 行、354 提交，断档 167.5 小时后补做）<!--doc-sync:exempt-->",
             "> **当前批次 W955（2026-10-26）**：GSAP 动效体系引入批第一子批（前置体检 + 执行前计划、施工批 W956）<!--doc-sync:exempt-->", 1),
        ],
        "inserts": [],
    },
    "docs/00-导读/项目说明.md": {
        "replaces": [
            ("当前批次行 W954 → W955",
             "> 当前批次 W954（2026-10-26）：工作复盘报告入库批（主线复盘断档后的全区间补做，含登记面漂移量化与并发门禁恢复）·详细变更见",
             "> 当前批次 W955（2026-10-26）：GSAP 动效体系引入批第一子批（前置体检 + 执行前计划、施工批 W956）·详细变更见", 1),
        ],
        "inserts": [],
    },
    "CITATION.cff": {
        "replaces": [
            ("批次号形态 version W954 → W955", 'version: "W954"', 'version: "W955"', 1),
        ],
        "inserts": [],
    },
    ".github/workflows/README.md": {
        "replaces": [
            ("头部版本链上限 W450-W954 → W450-W955", "→ W450-W954**", "→ W450-W955**", 1),
            ("头部项目标识 W954 → W955", "（`D:\\xiyouji`，W954）", "（`D:\\xiyouji`，W955）", 1),
            ("里程碑行上限 W450-W954 → W450-W955", "**W450-W954**：", "**W450-W955**：", 1),
        ],
        "inserts": [],
    },
    "HANDOVER.md": {
        "replaces": [
            ("「一、当前进度」标题 W954 → W955",
             "## 一、当前进度（W954 第 43 篇工作复盘批；更早批次详见 CHANGELOG.md）",
             "## 一、当前进度（W955 GSAP 动效体系引入批第一子批；更早批次详见 CHANGELOG.md）", 1),
            ("「最后更新」链首 W954 → W955（文件头 + 文末行·同一锚点两处）",
             "最后更新：2026-10-26（W954 第 43 篇工作复盘批）",
             "最后更新：2026-10-26（W955 GSAP 动效体系引入批第一子批）·2026-10-26（W954 第 43 篇工作复盘批）", 2),
            ("「当前 HEAD」W954 → W955",
             "当前 HEAD = W954（第 43 篇工作复盘批：W795–W953 全区间复盘 149 段 / 154 行 / 354 提交 + 登记面漂移五类量化与台账 8 行回写）",
             "当前 HEAD = W955（GSAP 动效体系引入批第一子批：前置体检 8 组事实 + 执行前计划 T-28 + 版本面同步；施工批 W956）", 1),
        ],
        "inserts": [
            ("一、当前进度增 W955 条目（前置）",
             "- **W954 第 43 篇工作复盘批**：", HANDOVER_ITEM, 1, "before"),
        ],
    },
    "STRUCTURE.md": {
        "replaces": [],
        "inserts": [
            ("里程碑增 W955 条目（前置）", "- **W954（2026-10-26）**：", STRUCTURE_ITEM, 1, "before"),
        ],
    },
    "scripts/output/file-index.md": {
        "replaces": [],
        "inserts": [
            ("新增 W955 反向索引段（插在 W954 段之前·倒序）",
             "## W954 第 43 篇工作复盘批（2026-10-26）", FILE_INDEX_SEG, 1, "before"),
        ],
    },
    "docs/11-方案报告/README.md": {
        "replaces": [
            ("§六 计划方案件数 35 → 36", "### 六、计划方案（35 件）", "### 六、计划方案（36 件）", 1),
        ],
        "inserts": [
            ("§六 增 T-28 执行前计划登记行（序号 33·接在序号 32 行之后）",
             "含 6 条经验沉淀（E-01~E-06·对应复盘全局 E-25~E-31）+ 6 条偏差留档 + 6 项未验证项显式声明 + 7 项后续行动 |",
             REPORT_README_ROW, 1, "after"),
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

    print(("DRY-RUN" if args.dry_run else "版本面同步") + "完成：%d 个面" % len(PLAN))
    return 0


if __name__ == "__main__":
    sys.exit(main())
