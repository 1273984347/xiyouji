#!/usr/bin/env python3
"""_w957_version_sync.py — W957 版本面 + 登记面同步（现役 W955 → W957）。

沿用 W955 批验证过的「**按文件聚合 · 逐文件读改写一次**」结构（W955 首版按 job 逐个读、
最后统一写 ⇒ 同文件后一个 job 覆盖前一个的改动，5 项门禁 FAIL 暴露）。

纪律：
  · 每处替换先断言命中数，不符即中止不写盘（fail-closed）；幂等（已应用则跳过）；
  · 行尾随文件主行尾归一，插入块按目标文件行尾转写；
  · 只改版本面与登记面字面量，不改叙述语义与历史段。

用法：py -3 scripts/_w957_version_sync.py [--dry-run]
"""
import argparse
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CHANGELOG_SEG = """### W957（2026-10-26）：GSAP 动效体系引入批·施工批（公共动效载体 + 试点 5 页三类动效 + 机检）

> **来源**：用户 2026-10-26 携 GSAP Skills 插件发起「滚动叙事 / 入场编排 / 微交互 / 现有动画体检」四类全都要 → 问卷裁定载体 = `site/` 静态站、交付 = 先出计划再施工 → W955 出计划 → 用户令「开工」→ W957 施工。
>
> - **文件**：site/static/js/motion-gsap.js、site/static/js/gsap.min.js、site/static/js/ScrollTrigger.min.js、site/index.html、site/reader/ch007.html、site/reader/themes/西游与死亡研究专题.html、site/reader/people/黄风怪外传.html、site/reader/people/白骨精.html、scripts/_w956_pilot_pick.py、scripts/_w957_wire_pilot.py、scripts/_w957_motion_probe.py、scripts/check_gsap_motion.py、scripts/_w957_ledger_claim.py、docs/11-方案报告/计划方案/T28-任务计划执行与经验沉淀报告-2026-10-26.md

**让号留痕**：W956 已被并行会话「登记面治理批」（`5b1d3e38`）占用并收官 ⇒ 本批按「先落地者保留」让号至 **W957**（preflight 取号 = max+1 = 957 · 无撞号 · touches 无交集）。

**落地四件**：① **公共动效载体** `site/static/js/motion-gsap.js`（GSAP 3.12.5 两文件外链 vendored·72,214 + 43,380 = 115,594 B·**不内联**：内联方案 857 页约 99.1 MB）；② **试点页机选**——`_w956_pilot_pick.py` 按三条规则扫 **527** 候选 → 入选 5 页（首页 + 回目正文 + 专题 + 人物×2·覆盖四类页型），单页增量 **187 / 199 / 208 / 208 / 208 B**（合计 +1,010 B）；③ **三类动效**——入场编排（首页首屏 8 元素 Timeline）/ 滚动叙事（分节单元批量进场·**非视差**：DESIGN §5 禁止清单）/ 微交互（折叠块展开编排）；④ **写法机检**——独立脚本 `check_gsap_motion.py`（8 项判据 + 自测 8/8；**不改管控文件**，挂槽待用户批准）。

**实测**：浏览器实跑 **30 组**（5 页 × 3 视口 × 2 动效偏好态）**0 FAIL**（RM 态载体执行数 = 0 · ScrollTrigger 实例 = 0 · 编排单元残留初始态 = 0）；pageerror = 0；CSP 856 页 0 漂移；禁词基线 0 命中。

**三条自纠**：探针 RM 判据改用「载体自报执行数」（GSAP 全局时间轴恒含库自身 tween ⇒ 原口径恒红）；站内 RAG 请求环境类 error 归 NOTE；机检自测抓出自身两处盲区（时长表 / 缓动常量表形态）并补判据。

**状态**：**已收官**（施工批完成；**推广批与门禁挂载待用户裁决**——Q-01 机检挂槽、Q-02 推广范围）

"""

HANDOVER_ITEM = (
    "- **W957 GSAP 动效体系引入批·施工批**：用户令「开工」⇒ 落地公共动效载体 "
    "`site/static/js/motion-gsap.js`（GSAP 3.12.5 外链 vendored·115,594 B·不内联）；"
    "试点页按规则**机选** 5 页（首页 + 回目正文 + 专题 + 人物×2·527 候选），单页增量 187–208 B；"
    "三类动效落地（入场编排 / 滚动叙事·非视差 / 折叠块微交互）；"
    "浏览器实跑 **30 组 0 FAIL**（含 RM 态零介入）；新建独立写法机检 `check_gsap_motion.py`（自测 8/8）；"
    "**让号**：W956 被并行会话占用 ⇒ 本批 W957；T28 施工报告落 `docs/11-方案报告/计划方案/`。\n"
)

STRUCTURE_ITEM = (
    "- **W957（2026-10-26）**：GSAP 动效体系引入批·施工批（公共动效载体 + 试点 5 页三类动效 + 机检）"
    "<!--doc-sync:exempt-->\n"
)

FILE_INDEX_SEG = """## W957 GSAP 动效体系引入批·施工批（公共动效载体 + 试点 5 页三类动效 + 机检）（2026-10-26）

| 文件 | W | 说明 |
|---|---|---|
| site/static/js/motion-gsap.js | W957 | 新增：公共动效载体（RM 双守卫 + fail-open + 三模式 intro/sections/fold + 排除 reveal-in） |
| site/static/js/gsap.min.js | W957 | 新增：GSAP 3.12.5 外链 vendored（72,214 B·不内联） |
| site/static/js/ScrollTrigger.min.js | W957 | 新增：ScrollTrigger 3.12.5 外链 vendored（43,380 B） |
| site/index.html | W957 | 修改：试点接入（data-gsap=intro + 三脚本外链·增量 187 B） |
| site/reader/ch007.html | W957 | 修改：试点接入（data-gsap=sections + 三脚本外链·增量 199 B） |
| site/reader/themes/西游与死亡研究专题.html | W957 | 修改：试点接入（增量 208 B） |
| site/reader/people/黄风怪外传.html | W957 | 修改：试点接入（增量 208 B） |
| site/reader/people/白骨精.html | W957 | 修改：试点接入（增量 208 B） |
| scripts/_w956_pilot_pick.py | W957 | 新增：试点页机选探针（3 条规则 · 527 候选 · 可复算） |
| scripts/_w957_wire_pilot.py | W957 | 新增：试点页接入器（字节级改写保行尾 · 断言命中数 · 幂等） |
| scripts/_w957_motion_probe.py | W957 | 新增：浏览器实跑探针（30 组 · RM 判据 + 环境类分离） |
| scripts/check_gsap_motion.py | W957 | 新增：GSAP 写法机检（8 项判据 + 自测 8/8·独立脚本不改管控件） |
| scripts/_w957_ledger_claim.py | W957 | 新增：台账认领行追加器（只追加不改历史行 / 幂等 / 混行尾 fail-closed） |
| scripts/output/_w956_pilot_pick.json | W957 | 新增：试点机选产物（5 页清单 + 527 候选特征量） |
| scripts/output/_w957_motion_probe.json | W957 | 新增：实跑产物（30 组采集 + 判定 PASS） |
| docs/11-方案报告/计划方案/T28-任务计划执行与经验沉淀报告-2026-10-26.md | W957 | 新增：T-28 施工报告（执行记录 / 12 条 AC 验收 / 8 条经验 E-01~E-08 / 5 条偏差留档） |
| docs/11-方案报告/README.md | W957 | 登记：§六 增 T-28 报告行（序号 34）+ 件数刷新 |
| docs/00-导读/W批次编号对账表.md | W957 | 登记：W957 认领行（让号留痕）+ 收官回填 |
| HANDOVER.md | W957 | 同步：一、当前进度增 W957 条目 + 最后更新链前置 + 当前 HEAD |
| CHANGELOG.md | W957 | 新增：W957 版段（四件套） |
| scripts/output/file-index.md | W957 | 登记：W957 段（本段） |

"""

REPORT_README_ROW = (
    "| 34 | T-28《任务计划执行与经验沉淀报告》— GSAP 动效体系引入批·施工批（W957：公共动效载体 + 试点 5 页三类动效 + 写法机检·2026-10-26·V1.0） | "
    "[T28-任务计划执行与经验沉淀报告-2026-10-26.md](计划方案/T28-任务计划执行与经验沉淀报告-2026-10-26.md) | "
    "框架第二十八次执行的终稿报告：① **公共动效载体** `site/static/js/motion-gsap.js` 落地"
    "（GSAP 3.12.5 两文件外链 vendored·115,594 B·**不内联**——内联方案 857 页约 99.1 MB）· "
    "RM 双守卫 + fail-open + 排除 `.reveal-in` 争抢；② **试点页机选**（`_w956_pilot_pick.py`·3 条规则·527 候选→5 页·"
    "覆盖首页/回目/专题/人物四类·单页增量 187–208 B）；③ **三类动效**——入场编排（首页首屏 8 元素 Timeline）/ "
    "滚动叙事（分节单元批量进场·**非视差**·DESIGN §5 禁则）/ 微交互（折叠块展开编排）；"
    "④ **浏览器实跑 30 组 0 FAIL**（5 页 × 3 视口 × 2 动效偏好态·RM 态载体执行数 = 0）；"
    "⑤ **写法机检** `check_gsap_motion.py`（8 项判据 + 自测 8/8·**不改管控文件**·挂槽待批准）；"
    "⑥ **三条自纠**（探针 RM 判据改用载体自报执行数 / RAG 环境类 error 归 NOTE / 机检自测抓出 2 处自身盲区）；"
    "含 12 条 AC 验收 + 8 条经验 E-01~E-08 + 5 条偏差留档 + 4 项未验证声明 · **让号**：W956 被并行会话占用 ⇒ 本批 W957 |\n"
)

PLAN = {
    "CHANGELOG.md": {
        "replaces": [
            ("编号规则段上限 W001-W956 → W001-W957",
             "W### ID（W001-W956）", "W### ID（W001-W957）", 1),
        ],
        "inserts": [
            ("新增 W957 版段（插在 W956 段之前）",
             "### W956（2026-10-26）：", CHANGELOG_SEG, 1, "before"),
        ],
    },
    "README.md": {
        "replaces": [
            ("当前批次行 W956 → W957",
             "> **当前批次 W956（2026-10-26）**：登记面治理批（preflight 在途判定加 git 条件与复盘触发器落地）·A1-A6<!--doc-sync:exempt-->",
             "> **当前批次 W957（2026-10-26）**：GSAP 动效体系引入批施工批（公共动效载体 + 试点 5 页三类动效 + 写法机检）<!--doc-sync:exempt-->", 1),
        ],
        "inserts": [],
    },
    "docs/00-导读/项目说明.md": {
        "replaces": [
            ("当前批次行 W956 → W957",
             "> 当前批次 W956（2026-10-26）：登记面治理批（preflight 在途判定加 git 条件与复盘触发器落地）·详细变更见",
             "> 当前批次 W957（2026-10-26）：GSAP 动效体系引入批施工批（公共动效载体 + 试点 5 页三类动效 + 写法机检）·详细变更见", 1),
        ],
        "inserts": [],
    },
    "CITATION.cff": {
        "replaces": [
            ("批次号形态 version W956 → W957", 'version: "W956"', 'version: "W957"', 1),
        ],
        "inserts": [],
    },
    ".github/workflows/README.md": {
        "replaces": [
            ("头部版本链上限 W450-W956 → W450-W957", "→ W450-W956**", "→ W450-W957**", 1),
            ("头部项目标识 W956 → W957", "（`D:\\xiyouji`，W956）", "（`D:\\xiyouji`，W957）", 1),
            ("里程碑行上限 W450-W956 → W450-W957", "**W450-W956**：", "**W450-W957**：", 1),
        ],
        "inserts": [],
    },
    "HANDOVER.md": {
        "replaces": [
            ("「一、当前进度」标题 W956 → W957",
             "## 一、当前进度（W956 登记面治理批（preflight 在途判定加 git 条件与复盘触发器落地）；更早批次详见 CHANGELOG.md）",
             "## 一、当前进度（W957 GSAP 动效体系引入批施工批；更早批次详见 CHANGELOG.md）", 1),
            ("「最后更新」链首 W956 → W957（文件头·圆点分隔）",
             "最后更新：2026-10-26（W956 登记面治理批）·",
             "最后更新：2026-10-26（W957 GSAP 动效体系引入批施工批）·", 1),
            ("「最后更新」链首 W956 → W957（文末行·分号分隔）",
             "最后更新：2026-10-26（W956 登记面治理批）；",
             "最后更新：2026-10-26（W957 GSAP 动效体系引入批施工批）；", 1),
            ("「当前 HEAD」W956 → W957",
             "当前 HEAD = W956（preflight 在途判定加 git 条件与复盘触发器落地；详见 CHANGELOG）",
             "当前 HEAD = W957（GSAP 动效体系引入批施工批：公共动效载体 + 试点 5 页三类动效 + 写法机检 + 实跑 30 组 0 FAIL）", 1),
        ],
        "inserts": [
            ("一、当前进度增 W957 条目（接在标题行之后）",
             "## 一、当前进度（W957 GSAP 动效体系引入批施工批；更早批次详见 CHANGELOG.md）",
             HANDOVER_ITEM, 1, "after"),
        ],
    },
    "STRUCTURE.md": {
        "replaces": [],
        "inserts": [
            ("里程碑增 W957 条目（前置）",
             "- **W955（2026-10-26）**：", STRUCTURE_ITEM, 1, "before"),
        ],
    },
    "scripts/output/file-index.md": {
        "replaces": [],
        "inserts": [
            ("新增 W957 反向索引段（插在 W956 段之前·倒序）",
             "## W956 登记面治理批", FILE_INDEX_SEG, 1, "before"),
        ],
    },
    "docs/11-方案报告/README.md": {
        "replaces": [
            ("§六 计划方案件数 36 → 37", "### 六、计划方案（36 件）", "### 六、计划方案（37 件）", 1),
        ],
        "inserts": [
            ("§六 增 T-28 施工报告登记行（序号 34·接在序号 33 之后）",
             "含 3 目标 + 12 条 AC + 16 条 ASM + 14 步 ST + 9 指标 + 8 风险 + **9 决策** + 12 项自包含检查 · **施工批 = W956** |",
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

    print(("DRY-RUN " if args.dry_run else "版本面同步") + "完成：%d 个面" % len(PLAN))
    return 0


if __name__ == "__main__":
    sys.exit(main())
