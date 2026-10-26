#!/usr/bin/env python3
"""_w961_version_sync.py — W961 版本面 + 登记面同步（W959 → W961·挂槽批 + F9 订正批）。

按文件聚合·逐文件读改写一次（W957 批验证过的结构）；断言命中数（fail-closed）；幂等。
用法：py -3 scripts/_w961_version_sync.py [--dry-run]
"""
import argparse
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CHANGELOG_SEG = """### W961（2026-10-26）：GSAP 写法机检挂 verify_delivery 第 50 槽 + F9 裸 ease 假阳性订正批

> **来源**：用户 2026-10-26 批准「把 GSAP 写法机检挂成 verify_delivery 常驻槽」（改管控文件）·同批自查抓出体检判据假阳性。
>
> - **文件**：scripts/verify_delivery.py、scripts/check_gsap_motion.py、scripts/_w955_motion_audit.py、scripts/_w960_pilot_shots.py、AGENTS.md、scripts/output/_w955_motion_audit.json、docs/11-方案报告/计划方案/执行前计划-T28-GSAP动效体系引入批.md、docs/11-方案报告/计划方案/T28-任务计划执行与经验沉淀报告-2026-10-26.md、docs/00-导读/W批次编号对账表.md

**① 挂槽（用户批准）**：`check_gsap_motion.py` 升为**第 50 门禁「GSAP 写法」**（verify_delivery 只改两处：EXPECTED_SECTION_NAMES + _STRICT_GATES·marker 由注册表派生）。**理由**：`site/static/js/` 下自有 JS 原不在任何静态门禁扫描域内（check_motion_ban 只扫 HTML + 两份 CSS·check_js_syntax 只扫 855 个 HTML 内联脚本）⇒ 载体写坏时**全站 54 段门禁全绿**。显式豁免机制：文件内写 `gsap-motion: waive J3 J4` 可豁免写法类规则，**J2 宪法级禁词不可豁免**，豁免逐条打印不静默。连带同步 AGENTS.md §4.2 第 50 条 + gate_count 49→50 + pytest_collected 900→902。

**② F9 假阳性订正**：`_w955_motion_audit.py` 裸 ease 正则无负向前查 ⇒ 命中的是数据字段名（`avg_ease` / `most_ease`）与令牌定义 ⇒ 原结论「**2 页 4 处裸 ease 违规**」**作废**；判据修好后复扫得**存量**裸 ease 49 处 / 25 页（形如 `transition: color 0.15s ease;`），按 DESIGN §5.2「禁**新增**」口径**存量不计入欠账**；连带订正 7 处表述（结论与判断未动），既有欠账由 2 条收敛为 **1 条**。

**③ 试点实跑截图**：新增 `scripts/_w960_pilot_shots.py`（5 试点页 × 2 视口终态截图 + 首页入场序列分解帧）；实测 10 组全部 gsap=True、编排单元终态 opacity 最小值 = 1。

**让号留痕**：W956 / W958 / W960 均被并行会话占用 ⇒ 本批让号至 **W961**。

**状态**：**已收官**（挂槽 + 订正 + 截图工具；**差异化推广批待开工**——按页型差异化：入口层上 intro/fold，内容层 reader 正文暂不铺 sections）

"""

HANDOVER_ITEM = (
    "- **W961 GSAP 写法机检挂槽批 + F9 假阳性订正批**：用户批准把 `check_gsap_motion.py` 挂成 "
    "verify_delivery **第 50 槽**——理由：`site/static/js/` 下自有 JS 原不在任何静态门禁扫描域内 ⇒ "
    "载体写坏时全站 54 段门禁全绿；含显式豁免机制（J2 宪法级禁词不可豁免·豁免不静默）；"
    "连带同步 AGENTS §4.2 第 50 条 + gate_count 49→50 + pytest_collected 900→902；"
    "同批自查抓出**体检判据假阳性**——「2 页 4 处裸 ease 违规」实为命中数据字段名（`avg_ease` / `most_ease`）"
    "⇒ 结论作废·连带订正 7 处表述·既有欠账由 2 条收敛为 1 条；**让号**：W956/W958/W960 被并行会话占用 ⇒ W961。\n"
)

STRUCTURE_ITEM = (
    "- **W961（2026-10-26）**：GSAP 写法机检挂 verify_delivery 第 50 槽 + F9 假阳性订正"
    "<!--doc-sync:exempt-->\n"
)

FILE_INDEX_SEG = """## W961 GSAP 写法机检挂槽批 + F9 假阳性订正批（2026-10-26）

| 文件 | W | 说明 |
|---|---|---|
| scripts/verify_delivery.py | W961 | 修改：挂第 50 门禁「GSAP 写法」（EXPECTED_SECTION_NAMES + _STRICT_GATES 两处·marker 自动派生）+ _SCOPE_CORE 恒跑 |
| scripts/check_gsap_motion.py | W961 | 修改：加汇总行 marker + 显式豁免机制（J3/J4/J7 可豁免·J2 不可豁免·逐条打印） |
| scripts/_w955_motion_audit.py | W961 | 修改：裸 ease 判据加负向前查（修假阳性：原命中数据字段名 `avg_ease` / `most_ease` 与令牌定义） |
| scripts/output/_w955_motion_audit.json | W961 | 刷新：F9 复扫产物（存量裸 ease 49 处 / 25 页·按「禁新增」口径不计欠账） |
| scripts/_w960_pilot_shots.py | W961 | 新增：试点页实跑截图工具（终态截图 + 入场序列分解帧 + 编排单元可见性 JSON） |
| AGENTS.md | W961 | 修改：§4.2 门禁清单补第 50 条「GSAP 动效写法槽」 |
| docs/11-方案报告/计划方案/执行前计划-T28-GSAP动效体系引入批.md | W961 | 修改：订正 4 处「裸 ease 欠账」表述（假阳性作废·存量不计欠账） |
| docs/11-方案报告/计划方案/T28-任务计划执行与经验沉淀报告-2026-10-26.md | W961 | 修改：订正 2 处同款表述 |
| docs/00-导读/W批次编号对账表.md | W961 | 登记：W961 认领行（让号留痕）+ W955 行订正 1 处 |
| README.md · pytest.ini · 系统架构方案 ×2 | W961 | 修改：统计标记同步（gate_count 49→50·pytest_collected 900→902） |
| HANDOVER.md | W961 | 同步：一、当前进度增 W961 条目 + 最后更新链前置 + 当前 HEAD |
| CHANGELOG.md | W961 | 新增：W961 版段（四件套） |
| scripts/output/file-index.md | W961 | 登记：W961 段（本段） |

"""

PLAN = {
    "CHANGELOG.md": {
        "replaces": [("编号规则段上限 W001-W959 → W001-W961",
                      "W### ID（W001-W959）", "W### ID（W001-W961）", 1)],
        "inserts": [("新增 W961 版段（插在 W959 段之前）",
                      "### W959（2026-10-26）：", CHANGELOG_SEG, 1, "before")],
    },
    "README.md": {
        "replaces": [("当前批次行 W959 → W961",
                      "> **当前批次 W959（2026-10-26）**：T10 审计报告 V1.1 计数口径订正批（31 条四态 + 开放项双口径）<!--doc-sync:exempt-->",
                      "> **当前批次 W961（2026-10-26）**：GSAP 写法机检挂 verify_delivery 第 50 槽 + F9 裸 ease 假阳性订正<!--doc-sync:exempt-->", 1)],
        "inserts": [],
    },
    "docs/00-导读/项目说明.md": {
        "replaces": [("当前批次行 W959 → W961",
                      "> 当前批次 W959（2026-10-26）：T10 审计报告 V1.1 计数口径订正批（31 条四态 + 开放项双口径）·详细变更见",
                      "> 当前批次 W961（2026-10-26）：GSAP 写法机检挂 verify_delivery 第 50 槽 + F9 裸 ease 假阳性订正·详细变更见", 1)],
        "inserts": [],
    },
    "CITATION.cff": {
        "replaces": [("批次号形态 version W959 → W961", 'version: "W959"', 'version: "W961"', 1)],
        "inserts": [],
    },
    ".github/workflows/README.md": {
        "replaces": [("头部版本链上限 W450-W959 → W450-W961", "→ W450-W959**", "→ W450-W961**", 1),
                     ("头部项目标识 W959 → W961", "（`D:\\xiyouji`，W959）", "（`D:\\xiyouji`，W961）", 1)],
        "inserts": [],
    },
    "HANDOVER.md": {
        "replaces": [("「一、当前进度」标题 W959 → W961",
                      "## 一、当前进度（W959 T10 审计报告 V1.1 计数口径订正批；更早批次详见 CHANGELOG.md）",
                      "## 一、当前进度（W961 GSAP 写法机检挂槽批 + F9 假阳性订正批；更早批次详见 CHANGELOG.md）", 1),
                     ("「最后更新」链首 W959 → W961（两处同起句）",
                      "最后更新：2026-10-26（W959 T10 审计报告 V1.1 计数口径订正批）",
                      "最后更新：2026-10-26（W961 GSAP 写法机检挂槽批 + F9 假阳性订正批）", 2),
                     ("「当前 HEAD」W959 → W961",
                      "当前 HEAD = W959（T10 审计报告 V1.1 计数口径订正批：31 条四态 + 开放项双口径 + §18 口径说明 + 4 处商榷落实；结论未改）",
                      "当前 HEAD = W961（GSAP 写法机检挂 verify_delivery 第 50 槽 + 显式豁免机制 + F9 裸 ease 假阳性订正（7 处表述））", 1)],
        "inserts": [("一、当前进度增 W961 条目（接在标题行之后）",
                      "## 一、当前进度（W961 GSAP 写法机检挂槽批 + F9 假阳性订正批；更早批次详见 CHANGELOG.md）",
                      HANDOVER_ITEM, 1, "after")],
    },
    "STRUCTURE.md": {
        "replaces": [],
        "inserts": [("里程碑增 W961 条目（前置）", "- **W959（2026-10-26）**：", STRUCTURE_ITEM, 1, "before")],
    },
    "scripts/output/file-index.md": {
        "replaces": [],
        "inserts": [("新增 W961 反向索引段（插在 W959 段之前·倒序）",
                      "## W959 T10 V1.1 计数口径订正批", FILE_INDEX_SEG, 1, "before")],
    },
}


def read(rel):
    path = os.path.join(ROOT, rel)
    with open(path, encoding="utf-8", newline="") as f:
        raw = f.read()
    if "\r\n" in raw:
        nl = "\r\n"
        bare = any(ln == "\n" for ln in raw.split("\r\n"))
    elif "\n" in raw:
        nl = "\n"
        bare = False
    else:
        nl = "\r"
        bare = False
    if bare:
        raise SystemExit("混合行尾：%s" % rel)
    return raw, nl


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    for rel, spec in PLAN.items():
        raw, nl = read(rel)
        orig = raw
        for desc, old, new, expect in spec["replaces"]:
            n = raw.count(old)
            if n == 0 and raw.count(new) > 0:
                print("SKIP   %s：%s（已应用）" % (rel, desc))
                continue
            if n != expect:
                print("ABORT  %s：命中 %d ≠ 期望 %d（%s）" % (rel, n, expect, desc))
                return 1
            raw = raw.replace(old, new)
            print("%s %s：%s" % ("DRY    " if args.dry_run else "REPL  ", rel, desc))
        for desc, anchor, block, expect, mode in spec["inserts"]:
            n = raw.count(anchor)
            if n != expect:
                print("ABORT  %s：锚点命中 %d ≠ 期望 %d（%s）" % (rel, n, expect, desc))
                return 1
            if block.split("\n")[0] in raw:
                print("SKIP   %s：%s（已存在）" % (rel, desc))
                continue
            blk = block.replace("\n", nl)
            raw = raw.replace(anchor, (anchor + nl + blk) if mode == "after" else (blk + anchor), 1)
            print("%s %s：%s" % ("DRY    " if args.dry_run else "INS   ", rel, desc))
        if raw == orig:
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
    raise SystemExit(main())
