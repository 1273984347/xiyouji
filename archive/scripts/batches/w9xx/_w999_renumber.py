# -*- coding: utf-8 -*-
"""_w999_renumber.py — W999 → W1001 再让号（段号与台账行一一对应）

对齐后的实况（台账即事实源）：
  台账 W998 行 = 对抗式审查修复批（并行会话·已入库 0a26ce85）⇒ W998 已被占用
  CHANGELOG `### W999（必守纪律晋升批）` = 并行会话的另一批（已入库 5870ec32）
  台账 W999 行 = **本批**（我登记的认领行）⇒ 与上面的段**同号不同批**
⇒ 按「先落地者保留」本批再让号 **W1001**，并让出台账 W999。

处置：
  ① 撤销上一轮对它的段号订正（它的段号回到 W999——W998 已被修复批占用）
  ② 本批段号 W999 → W1001（CHANGELOG 段位不变·仍在顶；file-index 新插 W1001 段）
  ③ 台账：删本批的 W999 认领行 → 追加 W1001 认领行（desc 写两次让号链条）
  ④ T35 报告批次号 W999 → W1001（让号链条写进 §5.1 与偏差表）

用法：py -3 scripts/_w999_renumber.py [--dry-run]
"""
from __future__ import annotations

import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _w999_closeout import FILES, BODY  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "scripts", "output")
CH = os.path.join(REPO, "CHANGELOG.md")
FI = os.path.join(OUT, "file-index.md")
LED = os.path.join(REPO, "docs", "00-导读", "W批次编号对账表.md")
T35 = os.path.join(REPO, "docs", "11-方案报告", "计划方案",
                    "T35-任务计划执行与经验沉淀报告-2026-10-28.md")

MY_HDR_999 = "### W999（2026-10-28）：回次 og:image 全覆盖批·第一轮试点（12 张线描立像/场面）"
MY_HDR_1001 = "### W1001（2026-10-28）：回次 og:image 全覆盖批·第一轮试点（12 张线描立像/场面）"
OTHER_998 = "### W998（2026-10-28）：必守纪律晋升批"
OTHER_999 = "### W999（2026-10-28）：必守纪律晋升批"

CLAIM_1001 = (
    "| W1001 | 回次 og:image 全覆盖批·第一轮试点 12 张（用户 2026-10-27 选区指定「下一批建议：100 回全覆盖 og:image」"
    "→ 2026-10-28 令『开始』；问卷裁定=线描立像族·沿用 plate-set 母版段 / 按题材定主体（战斗回场面·其余立像）/ 先出 12 张试点）"
    "= 缺口实读 80 回（初查 92 系盘点正则过严）→ 试点 12 张（6 立像 + 6 场面·主体全部避开已出的 34 个角色）"
    "→ 落位 12 个回目页（题图位 + 专属 1200×630 og:image）→ 回目覆盖 8 → 20 回 | —（待回填） | —（待回填） | "
    "在途（认领·未收官） | 主会话 2026-10-28 | site/reader,site/static/images,assets/promo/plate-set,"
    "docs/11-方案报告,docs/agent/pitfalls.md,AGENTS.md,HANDOVER.md,CHANGELOG.md,"
    "docs/00-导读/W批次编号对账表.md,scripts,docs/10-方法论沉淀 |")


def read(p):
    raw = io.open(p, "rb").read()
    return raw.decode("utf-8"), ("\r\n" if b"\r\n" in raw else "\n")


def write(p, text, nl):
    tmp = p + ".tmp"
    io.open(tmp, "wb").write(text.encode("utf-8"))
    os.replace(tmp, p)


def main() -> int:
    dry = "--dry-run" in sys.argv

    # ---------- ① 撤销对它的段号订正 ----------
    for p, old, new in ((CH, OTHER_998, OTHER_999), (FI, "## W998 必守纪律晋升批", "## W999 必守纪律晋升批")):
        t, n = read(p)
        if old in t:
            t = t.replace(old, new, 1)
            t = re.sub(r"·\*\*段号订正 W999→W998\*\*：本批台账行为 W998（台账即事实源·段号须与台账行一致）", "", t)
            if dry:
                print("DRY  %s：撤销段号订正（回 W999）" % os.path.basename(p))
            else:
                write(p, t, n)
                print("OK   %s：已撤销段号订正（回 W999）" % os.path.basename(p))

    # ---------- ② 本批段号 → W1001 ----------
    t, n = read(CH)
    if MY_HDR_999 in t:
        t = t.replace(MY_HDR_999, MY_HDR_1001, 1)
        t = t.replace("> **让号留痕**：拟用 W990，但 preflight 实测台账 max=W998 ⇒ W990–W998 已被并行批次占用（**先落地者保留**）⇒ 让号 **W999**。",
                      "> **让号留痕（两次）**：① 拟用 W990，preflight 实测台账 max=W998 ⇒ W990–W998 已被并行批次占用 ⇒ 让号 **W999**；"
                      "② 但并行会话的「必守纪律晋升批」已以 `### W999` 段入库（其台账行为 W998，W998 已被「对抗式审查修复批」占用）"
                      "⇒ 与本批台账 W999 行同号不同批 ⇒ 按「先落地者保留」本批**再让号 W1001**。")
        if dry:
            print("DRY  CHANGELOG 本批段号 → W1001")
        else:
            write(CH, t, n)
            print("OK   CHANGELOG 本批段号 → W1001")

    # ---------- ③ file-index 插 W1001 段 ----------
    t, n = read(FI)
    if "## W1001 " in t:
        print("SKIP  file-index 已有 W1001 段")
    else:
        rows = []
        for f in FILES:
            note = "本批新增/修改"
            if f.startswith("site/reader/ch"):
                note = "回目页接入题图 + 换专属 1200×630 og:image"
            elif f.startswith("site/static/images/og-"):
                note = "专属 og:image（1200×630·由母版裁切）"
            elif f.startswith("site/static/images/plate-line-"):
                note = "站点版（母版裁切·只裁上部留白）"
            elif f.startswith("assets/promo/plate-set/raw/"):
                note = "出图原件（12 张·含重出）"
            elif f.startswith("assets/promo/plate-set/plate-line-"):
                note = "新增母版（1200×1600）"
            elif f.startswith("scripts/"):
                note = "本批工具/产物"
            elif f.startswith("docs/"):
                note = "登记面（报告/坑表/计数链/方法论/台账）"
            rows.append("| %s | W1001 | %s |" % (f, note))
        seg = ("## W1001 回次 og:image 全覆盖批·第一轮试点（2026-10-28）\n\n"
               "| 文件 | W | 说明 |\n|---|---|---|\n" + "\n".join(rows) + "\n\n")
        heads = [(int(m.group(1)), m.start()) for m in re.finditer(r"^## W(\d{3,4}) ", t, re.M)]
        pos = None
        for w, s in heads:
            if w < 1001:
                pos = s
                break
        if pos is None:
            pos = 0
        t = t[:pos] + seg + t[pos:]
        if dry:
            print("DRY  file-index 插 W1001 段（%d 行）" % len(rows))
        else:
            write(FI, t, n)
            print("OK   file-index W1001 段已插入（%d 行）" % len(rows))

    # ---------- ④ 台账：删 W999 认领行 + 追加 W1001 行 ----------
    t, n = read(LED)
    lines = t.split("\n")
    out = []
    removed = 0
    for ln in lines:
        if re.match(r"^\|\s*W999\s*\|", ln) and "回次 og:image 全覆盖批" in ln:
            removed += 1
            continue
        out.append(ln)
    t = "\n".join(out)
    # 追加 W1001 行（插在 W1000 行之后·按号序）
    lines = t.split("\n")
    pos = None
    for i, ln in enumerate(lines):
        if re.match(r"^\|\s*W1000\s*\|", ln):
            pos = i + 1
            break
    if pos is None:
        pos = len(lines)
    lines.insert(pos, CLAIM_1001)
    t = "\n".join(lines)
    if dry:
        print("DRY  台账：删 W999 行 %d · 追加 W1001 行" % removed)
    else:
        write(LED, t, n)
        print("OK   台账：删 W999 行 %d · 追加 W1001 行" % removed)

    # ---------- ⑤ T35 改号 ----------
    t, n = read(T35)
    t = t.replace("**W999**", "**W1001**").replace("批次号 = **W999**", "批次号 = **W1001**")
    t = t.replace("施工批 = **W999**", "施工批 = **W1001**")
    t = t.replace("| **W 批次号** | **W999**（**让号留痕**：用户选区指定时我拟用 W990，但 preflight 实测台账 max=W998 ⇒ W990–W998 已被并行批次占用 ⇒ 按「先落地者保留」让号 **W999**） |",
                  "| **W 批次号** | **W1001**（**两次让号留痕**：① 拟用 W990，preflight 实测台账 max=W998 ⇒ W990–W998 被并行批次占用 ⇒ 让号 W999；② 并行会话的「必守纪律晋升批」已以 `### W999` 段入库（W998 已被「对抗式审查修复批」占用）⇒ 与本批台账 W999 行同号不同批 ⇒ 按「先落地者保留」再让号 **W1001**） |")
    t = t.replace("W999（**让号留痕**", "W1001（**两次让号留痕**")
    if "偏差 8" not in t:
        t = t.replace("| 偏差 7 |", """| 偏差 8 | **本批主体内容被并行 W1000 提交代提入库**，且批次号**两次让出** | 原计划为「W999 单笔提交」 | 并行会话的 `5870ec32 feat(w1000)` 是全量提交且时点晚于本批 `git add -A` ⇒ 把本批 115 个资产 + 102 个页面改动一并带入；随后发现 CHANGELOG 的 `### W999` 段已被并行会话的「必守纪律晋升批」占用（W998 已被「对抗式审查修复批」占用）⇒ 与本批台账 W999 行同号不同批 | 主体内容挂在他人提交下 + 号段冲突 | ① 不回滚（回滚会连带撤销并行 W1000 的合法改动）② 本批**再让号 W1001**（台账删 W999 行 + 追加 W1001 行 + CHANGELOG/file-index 段号同步）③ 在 CHANGELOG W1001 段状态行与 T35 §6 如实登记代提事实 | 主会话 | 2026-10-28 |
| 偏差 7 |""")
    if dry:
        print("DRY  T35 改号 W999 → W1001")
    else:
        write(T35, t, n)
        print("OK   T35 已改号 W1001")

    # ---------- ⑥ 复核 ----------
    t, _ = read(CH)
    print("CHANGELOG 段序：", re.findall(r"^### (W\d{3,4})", t, re.M)[:6])
    t, _ = read(FI)
    print("file-index 段序：", re.findall(r"^## (W\d{3,4})", t, re.M)[:6])
    t, _ = read(LED)
    print("台账 W99x-W100x：", re.findall(r"^\| (W(?:99[5-9]|100\d)) \|", t, re.M))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
