#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_w944_cascade.py — W944 四面登记 + 当前态指针（章回插画新组批）"""
import argparse
import io
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATCH = "W944"
LEDGER = os.path.join(REPO, "docs", "00-导读", "W批次编号对账表.md")
CHANGELOG = os.path.join(REPO, "CHANGELOG.md")
FILE_INDEX = os.path.join(REPO, "scripts", "output", "file-index.md")

CLAIM_ROW = (
    "| W944 | 章回插画新组批（用户 2026-10-25 认可 W943 记录的弱项「章回 6 张「挑担人赶路」重复度极高·若要丰富可另出一组」"
    "并答「可以」）：① **问题**——站内 6 张章回插画（chap-07/14/15/23/27/30）原为**同一构图**（挑担僧人赶路）仅换山水，"
    "回目与画面无对应关系；② **改法**——按各自回目情节另出一组 6 张（水墨浓墨剪影风·宣纸底 + 浓墨剪影 + 淡赭金远山 + "
    "单个朱砂方印·正方 1200×1200）：第 007 回 八卦炉（三足丹炉 + 火焰）/ 第 014 回 心猿归正（猴形剪影 + 金箍 + "
    "勒绳）/ 第 015 回 鹰愁涧（惊马扬蹄 + 缰绳 + 瀑布崖）/ 第 023 回 四圣试禅心（打坐僧 + 孤灯 + 雾中两道人影）/ "
    "第 027 回 尸魔三戏（三道人影渐次消散 + 月 + 茅屋）/ 第 030 回 邪魔侵正法（蛇形妖影 + 洞口 + 螺旋墨风）——"
    "**每张现与回目情节对应**；③ **一处模型伪影已修**——第 023 回新图自带一圈黑边框（模型给禅心图套了相框）⇒ "
    "按近黑像素带自动检测裁除（裁 66 px·四边）后重存；④ 旧版 6 张已备份（%TEMP%/bak_chap-*.webp·可回退） | "
    "—（待回填） | —（待回填） | 在途（认领·未收官） | 并行 Agent 会话 2026-10-25（章回插画新组批） | "
    "`site/static/images/chap-07.webp`（重出·八卦炉）· `site/static/images/chap-14.webp`（重出·紧箍咒）· "
    "`site/static/images/chap-15.webp`（重出·鹰愁涧惊马）· `site/static/images/chap-23.webp`（重出·禅心·去黑框）· "
    "`site/static/images/chap-27.webp`（重出·三打白骨精）· `site/static/images/chap-30.webp`（重出·黄风怪）· "
    "`CHANGELOG.md`（W944 版段）· `docs/00-导读/W批次编号对账表.md`（本行）· `scripts/output/file-index.md`（W944 段）· "
    "`scripts/_w944_cascade.py`（本批脚本） |"
)

CHANGELOG_SEG = """### W944（2026-10-25）：章回插画新组（6 张按回目情节重出·打破「挑担人赶路」同构）

> **来源**：用户 2026-10-25 认可 W943 记录的弱项「章回 6 张「挑担人赶路」重复度极高，若要丰富可另出一组」并答「可以」。

> - **文件**：site/static/images/chap-07.webp、site/static/images/chap-14.webp、site/static/images/chap-15.webp、site/static/images/chap-23.webp、site/static/images/chap-27.webp、site/static/images/chap-30.webp、CHANGELOG.md、docs/00-导读/W批次编号对账表.md、scripts/output/file-index.md、scripts/_w944_cascade.py

**问题**：站内 6 张章回插画（chap-07 / 14 / 15 / 23 / 27 / 30）原为**同一构图**（挑担僧人赶路）仅换山水，与所在回目无对应关系。

**改法**：按各自回目情节另出一组 6 张（水墨浓墨剪影风：宣纸底 + 浓墨剪影 + 淡赭金远山 + 单个朱砂方印，正方 1200×1200）——第 007 回 八卦炉（三足丹炉 + 火焰）、第 014 回 心猿归正（猴形剪影 + 金箍 + 勒绳）、第 015 回 鹰愁涧（惊马扬蹄 + 缰绳 + 瀑布崖）、第 023 回 四圣试禅心（打坐僧 + 孤灯 + 雾中两道人影）、第 027 回 尸魔三戏（三道人影渐次消散 + 月 + 茅屋）、第 030 回 邪魔侵正法（蛇形妖影 + 洞口 + 螺旋墨风）——**每张现与回目情节对应**。

**一处模型伪影已修**：第 023 回新图自带一圈黑边框（模型给禅心图套了相框）⇒ 按四边近黑像素带自动检测裁除（每边 66 px）后重存。

> - **验证**：6 张逐张放大目视（构图与回目情节对应 + 无黑框 + 无伪文字）+ 旧版 6 张备份于 %TEMP%/bak_chap-*.webp 可回退 · 第 31 与第 45 门禁 0 FAIL
> - **状态**：在途（认领登记 W944·待提交入库）

"""

FILE_INDEX_SEG = (
    "## W944 章回插画新组（6 张按回目情节重出）（2026-10-25）\n\n"
    "| 文件 | W | 说明 |\n"
    "|---|---|---|\n"
    "| site/static/images/chap-07.webp | W944 | 重出·第 007 回 八卦炉（三足丹炉 + 火焰） |\n"
    "| site/static/images/chap-14.webp | W944 | 重出·第 014 回 心猿归正（猴形剪影 + 金箍 + 勒绳） |\n"
    "| site/static/images/chap-15.webp | W944 | 重出·第 015 回 鹰愁涧（惊马扬蹄 + 缰绳 + 瀑布崖） |\n"
    "| site/static/images/chap-23.webp | W944 | 重出·第 023 回 四圣试禅心（打坐僧 + 孤灯 + 雾中两影·去黑框） |\n"
    "| site/static/images/chap-27.webp | W944 | 重出·第 027 回 尸魔三戏（三道人影渐次消散 + 月 + 茅屋） |\n"
    "| site/static/images/chap-30.webp | W944 | 重出·第 030 回 邪魔侵正法（蛇形妖影 + 洞口 + 螺旋墨风） |\n"
    "| scripts/_w944_cascade.py | W944 | 四面登记 + 当前态指针 |\n"
    "| CHANGELOG.md | W944 | W944 版段（四件套） |\n"
    "| docs/00-导读/W批次编号对账表.md | W944 | W944 认领行 |\n"
    "\n"
)


def read(p):
    raw = io.open(p, "rb").read()
    nl = "\r\n" if b"\r\n" in raw else "\n"
    return raw.decode("utf-8").replace("\r\n", "\n"), nl


def write(p, t, nl):
    io.open(p, "w", encoding="utf-8", newline="").write(t.replace("\n", nl))


def segs(txt):
    out = []
    for i, ln in enumerate(txt.split("\n")):
        if ln.startswith("### "):
            m = re.search(r"W(\d+)", ln)
            if m:
                out.append((int(m.group(1)), i))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    dry = args.dry_run
    rep = []

    t, nl = read(LEDGER)
    if re.search(r"^\| " + BATCH + r" \|", t, re.M):
        rep.append("认领行已存在（幂等跳过）")
    else:
        lines = t.split("\n")
        idx = None
        for i, ln in enumerate(lines):
            m = re.match(r"^\| W(\d+) \|", ln)
            if m and int(m.group(1)) < 944:
                idx = i
                break
        if idx is None:
            idx = max(i for i, ln in enumerate(lines) if ln.startswith("| W"))
        lines.insert(idx + 1, CLAIM_ROW)
        rep.append(("DRY " if dry else "") + "认领行已插入（第 %d 行）" % (idx + 2))
        if not dry:
            write(LEDGER, "\n".join(lines), nl)

    t, nl = read(CHANGELOG)
    if re.search(r"^### " + BATCH + r"（", t, re.M):
        rep.append("CHANGELOG 段已存在（幂等跳过）")
    else:
        pos = None
        for n, i in segs(t):
            if n < 944:
                pos = len("\n".join(t.split("\n")[:i])) + 1
                break
        new_t = t[:pos] + CHANGELOG_SEG + t[pos:]
        nums = [n for n, _ in segs(new_t)]
        if nums.count(944) != 1 or any(nums[i] < nums[i + 1] for i in range(len(nums) - 1)):
            print("FATAL CHANGELOG 段序断言失败")
            return 2
        rep.append(("DRY " if dry else "") + "CHANGELOG 段已插入（段序前 5 = %s）" % nums[:5])
        if not dry:
            write(CHANGELOG, new_t, nl)

    t, nl = read(FILE_INDEX)
    if re.search(r"^## " + BATCH + r" ", t, re.M):
        rep.append("file-index 段已存在（幂等跳过）")
    else:
        m = re.search(r"^## W\d+ ", t, re.M)
        pos = m.start() if m else len(t)   # 降序表·最新在前
        new_t = t[:pos] + FILE_INDEX_SEG + t[pos:]
        if len(re.findall(r"^## W944 ", new_t, re.M)) != 1:
            print("FATAL file-index 目标段异常")
            return 2
        rep.append(("DRY " if dry else "") + "file-index 段已插入")
        if not dry:
            write(FILE_INDEX, new_t, nl)

    p = os.path.join(REPO, "README.md")
    t, nl = read(p)
    t = re.sub(r"> \*\*当前批次 W\d+（2026-10-25）\*\*：[^\n]*",
               "> **当前批次 W944（2026-10-25）**：章回插画新组（六张按各自回目情节重出，打破「挑担人赶路」同构）", t, count=1)
    if not dry:
        write(p, t, nl)
    rep.append("README 抬头已更新")

    p = os.path.join(REPO, "HANDOVER.md")
    t, nl = read(p)
    t = re.sub(r"> 最后更新：2026-10-25（W\d+", "> 最后更新：2026-10-25（W944 章回插画新组批）·2026-10-25（W943", t, count=1)
    t = re.sub(r"## 一、当前进度（W\d+[^\n]*\n",
               "## 一、当前进度（W944 章回插画新组批；更早批次详见 CHANGELOG.md）\n"
               "- **W944 章回插画新组批**：站内 6 张章回插画原为同一构图（挑担人赶路）且与回目无对应 ⇒ 按各回情节重出"
               "（八卦炉 / 紧箍咒 / 鹰愁涧惊马 / 四圣试禅心 / 三打白骨精 / 黄风怪），并修掉第 023 回新图自带的黑边框伪影。\n",
               t, count=1)
    t = re.sub(r"最后更新：2026-10-25（W\d+", "最后更新：2026-10-25（W944 章回插画新组批）；2026-10-25（W943", t, count=1)
    if not dry:
        write(p, t, nl)
    rep.append("HANDOVER 指针已更新")

    t, nl = read(CHANGELOG)
    t = re.sub(r"（W001-W\d+）", "（W001-W944）", t, count=1)
    if not dry:
        write(CHANGELOG, t, nl)
    rep.append("CHANGELOG 规则段已更新")

    for r in rep:
        print(" -", r)
    return 0


if __name__ == "__main__":
    sys.exit(main())
