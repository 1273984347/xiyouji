# -*- coding: utf-8 -*-
"""_w1018_closeout_faces.py — W1015 + W1018 两批的登记面一次性落盘

四件事：
  ① 坑表 +3 条（E-35 级联节 / E-36 + E-37 流程节）+ 2 处节标题条数
  ② 计数链 4 处：AGENTS §4.3 声明（109 → 112）· HANDOVER 两处指针（101 → 112）
  ③ W1015 段插段（CHANGELOG + file-index）——**按号序插在 W1016 段之前**（W1015 号已被
     并行批占位过 ⇒ 无法走级联路径，只能段内定向插入；W1018 段内已连带登记 W1015）
  ④ 方案报告 README §六 登记 T38 + 节标题件数

全部写盘走「临时文件 + os.replace」原子替换 + 写后行数/行尾不变断言。
用法：py -3 scripts/_w1018_closeout_faces.py [--dry-run]
"""
from __future__ import annotations

import io
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIT = os.path.join(REPO, "docs", "agent", "pitfalls.md")
AG = os.path.join(REPO, "AGENTS.md")
HO = os.path.join(REPO, "HANDOVER.md")
CH = os.path.join(REPO, "CHANGELOG.md")
FI = os.path.join(REPO, "scripts", "output", "file-index.md")
RD = os.path.join(REPO, "docs", "11-方案报告", "README.md")

E35 = ("- **静态扫描判据自身会误报：排除符含 `\\n` ⇒ 该字符类不跨行**（W1015 实证·E-35）："
       "给「改写面正则是否可能跨行吞行」写静态扫描器时，首版把 `//[^\\n]*` 判为高危 ⇒ 实测该字符类的"
       "**排除符含 `\\n`** ⇒ 它**不匹配换行** ⇒ 不可能跨行 ⇒ 纯误报。⇒ 修法：① 判定「可跨行」必须看"
       "**排除符内容**（含 `\\n`/`\\r` ⇒ 该类不跨行），不能只看「用了 `[^…]`」；② 扫描器必须带**负样本自证**"
       "（经典高危必抓 + 三种安全形态必不报），否则「零高危」可能是判据恒真；③ 扫描器只能覆盖"
       "**可静态判定**的模式（f-string 模式、跨行拼接模式等需交人工）⇒ 报告须写明覆盖边界。\n")
E36 = ("- **派生脚本里的「期望值」也必须按当批实算，不能沿用上一批**（W1015 实证·E-36）："
       "落位验收脚本由上一批程序化派生 ⇒ 其期望值（缺口 68 / 有配图 32 / 通用 og 66）仍写死上一批基线 ⇒ "
       "本批实跑判红 3 项，而**实际基线已被其他批次推进**（有配图 32→44、缺口 68→56）⇒ 判红是"
       "**期望值过期**不是产出错。⇒ 修法：① 派生时**期望值必须重算**（当批开工前实算基线 + 本批增量）；"
       "② 尽量让脚本**现算**而非写死；③ 验收判红先查「期望值是不是上一批的」再查产出。\n")
E37 = ("- **派生脚本要逐项核对「路径常量」；重出件的下载必须先删旧件**（W1015 实证·E-37）："
       "① 派生下载器时只改了 manifest 名与批号串，**漏改 DEST 目录常量**（仍指上一批目录）⇒ 12 张原件"
       "全落错目录 ⇒ 成品处理报「无出图原件」；② 下载器幂等逻辑「已存在且 ≥MIN_BYTES ⇒ SKIP」⇒ "
       "**重出后旧件不会被覆盖**⇒ 复验的是旧图（判据全绿也是假绿）。⇒ 修法：① 派生后**逐项列出与目录/路径"
       "相关的常量**（DEST/RAW/OUT/SET_DIR…）逐个核对；② 派生脚本自带**残留断言 + 路径常量清单**；"
       "③ 派生后**立即端到端跑一次**（下载 → 成品处理）而不只 dry-run；④ **重出流程必须先删旧原件再下载**。\n")

CH_W1015 = """### W1015（2026-10-29）：工具链稳健性补强①（跨行改写扫描器 + 第 48 门禁读盘路径覆盖）

> **来源**：用户 2026-10-29 令「同族扫描 + 第 48 门禁补覆盖 做完再继续剩余 68 回扩量」。
>
> - **文件**：scripts/check_cross_line_rewrite.py、scripts/check_plan_template.py、scripts/ci_sim.py、tests/unit/test_cross_line_rewrite.py、tests/unit/test_plan_template_read_disk.py、docs/00-导读/W批次编号对账表.md。
>
> **本批要点**：① **跨行改写扫描器**（新增）——病根：「`[^X]*` 无尾锚点 ⇒ 匹配段可跨行 ⇒ `re.sub` 整段替换 = 静默删行」（W1005 实证）。全仓 scripts/ 全树实扫 ⇒ **改写面高危 0 处**（另 43 处可疑 + 184 处只读面）；判据自带 **4 例负样本自证**（含「排除符含 `\\n` ⇒ 必不报」）；接线 `ci_sim.py` 第 8 项（避门禁本体·§11.2 禁擅改）。② **第 48 门禁读盘路径补覆盖**——`judge_file()` 的读盘面此前**零覆盖**（自测 ①~⑤ 全走纯函数 `R.judge`）⇒ W1005 批在首个新增计划方案件进仓时崩在 `AttributeError: module 'plan_template_review' has no attribute 'io'` ⇒ 潜伏到真实新增件才引爆；现补 self_test ⑧ 例 + 4 例 pytest。
>
> **验证**：扫描器 `--self-test` 4/4 · `--gate` 0 FAIL（高危 0 处）· 第 48 门禁 `--self-test` 9/9 · pytest 9 passed。
>
> - **状态**：已收官（让号留痕：并行 W1014「工具链体检整改批」先落地 ⇒ 本会话让号 **W1015**；台账行用 `update-index --cacheinfo` 精确暂存·未代提他方在途件）

"""

FI_W1015 = """## W1015 工具链稳健性补强①（2026-10-29）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_cross_line_rewrite.py | W1015 | 跨行改写扫描器（改写面高危 0 处·自带 4 例负样本自证） |
| scripts/check_plan_template.py | W1015 | 第 48 门禁读盘路径补覆盖（self_test 第 ⑧ 例） |
| scripts/ci_sim.py | W1015 | CI 侧预演接线（新增第 8 项跨行扫描） |
| tests/unit/test_cross_line_rewrite.py | W1015 | 扫描器单测 5 例 |
| tests/unit/test_plan_template_read_disk.py | W1015 | 读盘路径单测 4 例 |
| docs/00-导读/W批次编号对账表.md | W1015 | 台账认领行（精确暂存·未代提他方在途件） |

"""

RD_ROW = ("| 48 | T-38《任务计划执行与经验沉淀报告》— 工具链稳健性补强 + 回次 og:image 全覆盖·第三轮"
          "（2026-10-29·V1.0·W1015+W1018·两批合一） | "
          "[T38-任务计划执行与经验沉淀报告-2026-10-29.md](计划方案/T38-任务计划执行与经验沉淀报告-2026-10-29.md) | "
          "框架第三十八次执行（**两批合一**·用户令三件事一批交付）：① 跨行改写扫描器（全仓 scripts/ 全树实扫 "
          "**高危 0 处**·判据带 4 例负样本自证·接线 ci_sim 第 8 项）② 第 48 门禁**读盘路径**补覆盖"
          "（此前零覆盖 ⇒ 潜伏到首个新增件才引爆）③ 第三轮 12 张（编号 73–84·3 张重出·覆盖 32 → 44 回·"
          "缺口 68 → 56 回）·附 3 条经验沉淀（109 → 112 条） |")


def read(p):
    raw = io.open(p, "rb").read()
    return raw.decode("utf-8"), ("\r\n" if b"\r\n" in raw else "\n")


def write(p, text):
    tmp = p + ".tmp"
    io.open(tmp, "wb").write(text.encode("utf-8"))
    os.replace(tmp, p)


def patch(path, pairs, dry, lines_delta=0):
    text, nl = read(path)
    orig = text
    for old, new, cnt in pairs:
        n = text.count(old)
        assert n == cnt, "%s 锚点命中 %d 次（期望 %d）：%r" % (os.path.basename(path), n, cnt, old[:50])
        text = text.replace(old, new)
    assert text.count("\n") == orig.count("\n") + lines_delta, \
        "%s 行数变化异常（期望 +%d）" % (os.path.basename(path), lines_delta)
    if dry:
        print("DRY  %s 将改 %d 处" % (os.path.basename(path), len(pairs)))
    else:
        write(path, text)
        print("OK   %s 改 %d 处" % (os.path.basename(path), len(pairs)))
    return text


def insert_section(text, header, section, pat):
    """按 W 号降序插入：插在「第一个比它大的 W 段」之前。"""
    if header in text:
        return text, False
    heads = [(int(m.group(1)), m.start()) for m in re.finditer(pat, text, re.M)]
    target = int(re.search(r"W(\d{3,4})", header).group(1))
    pos = None
    for w, s in heads:
        if w > target:
            pos = s
            break
    if pos is None:
        pos = text.rindex("\n") + 1
    return text[:pos] + section + text[pos:], True


def main() -> int:
    dry = "--dry-run" in sys.argv

    # ① 坑表 3 条 + 2 处节标题（条数**动态读**·并行批已改过节标题）
    text, _nl = read(PIT)
    sec_cascade = re.search(r"(### 级联 / CHANGELOG（(\d+) 条）\n)(.*?)(?=\n### )", text, re.S)
    assert sec_cascade, "未定位级联节"
    n_c = int(sec_cascade.group(2))
    body = sec_cascade.group(3).rstrip("\n") + "\n" + E35
    text = text[:sec_cascade.start(3)] + body + text[sec_cascade.end(3):]
    sec_flow = re.search(r"(### 流程 / 协作 / 取证（(\d+) 条）\n)(.*?)(?=\n### |\Z)", text, re.S)
    assert sec_flow, "未定位流程节"
    n_f = int(sec_flow.group(2))
    body = sec_flow.group(3).rstrip("\n") + "\n" + E36 + E37
    text = text[:sec_flow.start(3)] + body + text[sec_flow.end(3):]
    text = text.replace("### 级联 / CHANGELOG（%d 条）" % n_c, "### 级联 / CHANGELOG（%d 条）" % (n_c + 1))
    text = text.replace("### 流程 / 协作 / 取证（%d 条）" % n_f, "### 流程 / 协作 / 取证（%d 条）" % (n_f + 2))
    if dry:
        print("DRY  坑表 +3 条 + 2 处节标题（级联 %d→%d · 流程 %d→%d）" % (n_c, n_c + 1, n_f, n_f + 2))
    else:
        write(PIT, text)
        print("OK   坑表 +3 条（E-35/E-36/E-37）+ 2 处节标题")

    # ② 计数链：AGENTS 109 → 112；HANDOVER 101 → 112（两处）
    patch(AG, [("109 条坑位", "112 条坑位", 1)], dry)
    patch(HO, [("（101 条·六主题", "（112 条·六主题", 2)], dry)

    # ③ W1015 段插段（CHANGELOG + file-index）
    for path, pat, header, section in (
        (CH, r"^### W(\d{3,4})", "### W1015", CH_W1015),
        (FI, r"^## W(\d{3,4})", "## W1015", FI_W1015),
    ):
        text, _nl = read(path)
        text2, added = insert_section(text, header, section, pat)
        if not added:
            print("SKIP  %s 已有 W1015 段" % os.path.basename(path))
            continue
        if dry:
            print("DRY  %s 将插入 W1015 段" % os.path.basename(path))
        else:
            write(path, text2)
            print("OK   %s 插入 W1015 段" % os.path.basename(path))

    # ④ 方案报告 README §六 登记 + 节标题件数
    patch(RD, [("| 47 | T-37", RD_ROW + "\n| 47 | T-37", 1),
                ("### 六、计划方案（48 件）", "### 六、计划方案（49 件）", 1)], dry, lines_delta=1)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
