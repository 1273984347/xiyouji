#!/usr/bin/env python3
"""_w955_ledger_claim.py — W955 台账认领行追加（认领即占号·规则一）。

纪律：
  · 只**追加**一行，不改任何历史行（表头规则②「不改他方行」）；
  · 幂等：已存在 `| W955 |` 开头行则跳过并退出 0；
  · 行尾随文件主行尾归一（混行尾即中止·fail-closed，仿 batch_cascade 的 W706 防线）；
  · touches 列只登记**级联之外的手工共享面**（CHANGELOG / HANDOVER / README / STRUCTURE /
    项目说明 / CITATION / workflows README 属级联面·不列；台账追加行属 append 安全操作·不列）。

用法：py -3 scripts/_w955_ledger_claim.py [--dry-run]
"""
import argparse
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(ROOT, "docs", "00-导读", "W批次编号对账表.md")
W = "W955"

TOPIC = (
    "GSAP 动效体系引入批·第一子批（取证 + 执行前计划·W955）："
    "用户 2026-10-26 携 GSAP Skills 插件发起，裁定四类动效诉求（滚动叙事 / 入场编排 / 微交互 / 现有动画体检）**全部要做**，"
    "载体 = `site/` 静态站，交付 = 先出计划再施工；"
    "① **前置体检**——新建 `scripts/_w955_motion_audit.py` 作全批数字唯一源头（8 组事实），"
    "实测 857 页 / 含 @keyframes 331 页 / 含 reveal-in 333 页 / 含 RM 守卫 334 页 / "
    "动效禁止清单基线 **0 命中** / `d3 .duration(N>600)` **0 页** / "
    "`system.css` 29,660 B（超 DESIGN §4A.8 上限 25,497 B 达 **4,163 B**·既有欠账）/ "
    "`tokens.css` 23,039 B（余量 760 B）/ 裸 ease 违规 4 处（`site/data/chart-design.html` 与 `site/en/chart-design.html`）；"
    "② **GSAP 库实测**——3.12.5 两文件可下载（`gsap.min.js` 72,214 B + `ScrollTrigger.min.js` 43,380 B = 115,594 B），"
    "内联方案为每页 115,594 B（857 页约 99.1 MB）·外链为每页 119 B 标签 ⇒ 裁定外链 vendored；"
    "③ **动效宪法约束**——DESIGN.md §5 禁回弹 / 禁 360° 旋转 / 禁无限循环 / 禁视差 / 禁裸 ease·linear / 时长 ≤ 600 ms / "
    "RM 双守卫强制 / 只动 transform 与 opacity ⇒ 用户诉求中的「视差」须以非视差滚动叙事替代（计划 D-03）；"
    "④ **落点裁定**——公共动效载体 `site/static/js/motion-gsap.js`（W471 规划的 `motion.js` 至今未落地·公共层是既有缺口）+ 试点 5 页分级引入（计划 D-01/D-02/D-05）；"
    "⑤ **交付**——《执行前计划-T28-GSAP动效体系引入批.md》落 `docs/11-方案报告/计划方案/`，"
    "含 3 目标 + 12 条 AC + 16 条 ASM + 14 步 ST + 9 指标 + 8 风险 + 9 决策 + 12 项自包含检查；"
    "**施工批为 W956**（本批只做取证 + 计划 + 登记 + 提交）"
)

ROW = (
    "| %s | %s | —（认领占号·本行提交后回填 hash） | —（待回填） | "
    "**在途**（认领占号·计划件已落盘·施工批 W956 待启动） | "
    "主会话 2026-10-26（GSAP 动效体系引入批） | "
    "`docs/11-方案报告/README.md`（§六 登记行） |" % (W, TOPIC)
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    with open(LEDGER, encoding="utf-8", newline="") as f:
        raw = f.read()

    if "\r\n" in raw:
        nl = "\r\n"
    elif re.search(r"(?<!\r)\n", raw):
        nl = "\n"
    else:
        nl = "\r"
    if nl == "\r" or (("\r\n" in raw) and re.search(r"(?<!\r)\n", raw)):
        print("混合行尾——fail-closed（仿 batch_cascade W706 防线）")
        return 1

    if any(ln.startswith("| %s |" % W) for ln in raw.split(nl)):
        print("W955 认领行已存在——跳过（幂等）")
        return 0

    if not raw.endswith(nl):
        raw += nl
    new = raw + ROW + nl

    if args.dry_run:
        print("DRY-RUN：将从 %d B 增至 %d B（新增 1 行）" % (len(raw), len(new)))
        print(ROW[:200] + " …")
        return 0

    with open(LEDGER, "w", encoding="utf-8", newline="") as f:
        f.write(new)
    print("认领行已追加：%s（%d B → %d B）" % (LEDGER, len(raw), len(new)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
