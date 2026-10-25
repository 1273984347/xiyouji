#!/usr/bin/env python3
"""_w957_ledger_claim.py — W957 台账认领行追加（认领即占号·规则一）。

让号留痕：W956 已被并行会话「登记面治理批」（commit 5b1d3e38）占用并收官
          ⇒ 本批按「先落地者保留」让号至 **W957**（preflight 取号 = max+1 = 957）。

纪律：
  · 只**追加**一行，不改任何历史行；
  · 幂等：已存在 `| W957 |` 开头行则跳过并退出 0；
  · 行尾随文件主行尾归一（混行尾即中止·fail-closed，仿 batch_cascade 的 W706 防线）；
  · touches 列只登记**级联之外的手工共享面**（CHANGELOG / HANDOVER / README / STRUCTURE /
    项目说明 / CITATION / workflows README / file-index 属级联面·不列；台账追加行属 append
    安全操作·不列；5 个试点页为本批独占文件·不列）。

用法：py -3 scripts/_w957_ledger_claim.py [--dry-run]
"""
import argparse
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(ROOT, "docs", "00-导读", "W批次编号对账表.md")
W = "W957"

TOPIC = (
    "GSAP 动效体系引入批·施工批（公共动效载体落地 + 试点 5 页三类动效 + 机检判据·W957）："
    "承接 W955 执行前计划（用户 2026-10-26 携 GSAP Skills 插件发起「滚动叙事 / 入场编排 / 微交互 / 现有动画体检」四类全都要·"
    "问卷裁定载体 = `site/` 静态站、交付 = 先出计划再施工）；"
    "**让号留痕**——W956 已被并行会话「登记面治理批」（commit 5b1d3e38·已收官）占用，"
    "按「先落地者保留」让号至 **W957**（preflight 取号 = max+1 = 957·无撞号·touches 无交集）；"
    "① **试点页机选**——新建 `scripts/_w956_pilot_pick.py`（按 ASM-14 三条规则机选·非手挑），"
    "实测 527 候选（首页 1 / 回目 100 / 专题 210 / 人物 216），"
    "入选 5 页 = `site/index.html` + `site/reader/ch007.html` + `site/reader/themes/西游与死亡研究专题.html` + "
    "`site/reader/people/黄风怪外传.html` + `site/reader/people/白骨精.html`（覆盖首页/回目/专题/人物四类页型）；"
    "② **引入形态**——GSAP 3.12.5 两文件外链 vendored 至 `site/static/js/`（72,214 B + 43,380 B = 115,594 B·"
    "内联方案 857 页约 99.1 MB 故否决）；③ **落点**——新建公共动效载体 `site/static/js/motion-gsap.js`"
    "（补 W471 规划却从未落地的公共层缺口）+ 试点 5 页引入；"
    "④ **三类动效**——滚动叙事（章节级一次性进场 + 阅读进度联动·**非视差**：DESIGN §5 禁止清单 + "
    "`check_motion_ban.py` 全文正则扫描含注释与变量名）/ 入场编排（Timeline + stagger·时长 ≤600 ms）/ "
    "微交互联动（跨元素时序；单元素 hover 反馈保留既有 CSS 实现）；"
    "⑤ **合规**——RM 双守卫（`gsap.matchMedia` + duration 0 直达终态）· fail-open（无 GSAP 时内容直接可见）· "
    "只动 transform 与 opacity · 缓动白名单（power1/2/3.out + power2.inOut·禁 back/elastic/none/linear）· "
    "禁 360° 及以上旋转 · 禁无限循环；⑥ **机检**——新建独立判据脚本 `scripts/check_gsap_motion.py`"
    "（**不改管控文件**·挂载 verify_delivery 第 49 槽待用户批准）"
)

ROW = (
    "| %s | %s | —（认领占号·本行提交后回填 hash） | —（待回填） | "
    "**在途**（认领占号·施工中） | "
    "主会话 2026-10-26（GSAP 动效体系引入批·施工批） | "
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
        print("%s 认领行已存在——跳过（幂等）" % W)
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
