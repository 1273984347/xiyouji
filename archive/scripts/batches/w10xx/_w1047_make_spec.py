# -*- coding: utf-8 -*-
"""_w1045_make_spec.py — W1045 级联 spec 生成（复核 + 治理 + og A+ 修复）

**并行纪律**：工作树内混有并行会话（W1044 批）的在途件 ⇒ 本生成器**显式排除**它们，
避免 spec 把他人在途件写进本批清单（⇒ 提交时代提）。

沿用 W1043 已修的三处口径（不得重犯）：
  ① git 调用统一 `-c core.quotepath=false` ⇒ 中文路径以真中文写入段文件行；
  ② 文件全集剔除**磁盘已不存在**的路径；
  ③ 段「文件」行只列现存路径；`file_index_rows` 另含 rename 删除面旧名。

输出：scripts/output/_w1047_spec.json
用法：py -3 archive/scripts/batches/w10xx/_w1045_make_spec.py
"""
from __future__ import annotations

import fnmatch
import io
import json
import os
import subprocess

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
OUT = os.path.join(REPO, "scripts", "output")
SPEC = os.path.join(OUT, "_w1047_spec.json")

BATCH = "W1047"
DATE = "2026-10-31"
TITLE = "W1047 图表判据剥标签根修（标签语法约束 + 剥离顺序修正）"
DESC = "图表判据剥标签根修：标签按语法约束且注释优先剥离，修复五页误吞正文且零漏剥标签"
HEAD_ENTRY = "2026-10-31（W1047 图表判据剥标签根修）"
HEAD_SENTENCE = "图表判据剥标签根修：标签按语法约束且注释优先剥离，修复五页误吞正文且零漏剥标签"
AGENTS_NOTE = ("2026-10-31（W1047）图表判据剥标签根修：标签按语法约束，"
               "注释优先剥离；影子对照八百五十七页，修复五页误吞正文，零漏剥标签。")
MILESTONE = ("- **W1047 图表判据剥标签根修**：\n"
             "  - 根因两处：标签起点过宽（JS 比较符 <= 被当标签）+ 剥离顺序（注释里的 script 字面量）\n"
             "  - 修法：标签按语法约束（标签名字母开头）+ 注释优先剥离\n"
             "  - 影子对照 857 页：修复 5 页误吞正文，零漏剥标签\n"
             "  - 判据自测补 2 例可证伪锁 + 全站实跑 235 页 FAIL 0 + 坑表 +2 条")
BODY = (
    "\n\n\n\n> **来源**：用户 2026-10-30 收尾时选定的取舍项——存量 `check_chart_data.py` 的剥标签"
    "正则（实测 2 处真吞 JS 正文；补 `\\n\\r` 会让多行合法标签剥不干净）⇒ 本批以**根因修法**落地。\n"
    ">\n"
    "> - **文件**：")


# 并行会话（W1044 批）的在途件 ⇒ 显式排除，避免代提
EXCLUDE = [
    "*_w1044_*",
    "pytest.ini",
    "scripts/check_doc_sync.py",
    "scripts/check_plan_template.py",
    "docs/11-方案报告/设计与架构方案/*",
    "docs/11-方案报告/计划方案/执行前计划-W1043-*",
    "docs/11-方案报告/计划方案/执行前计划-W1046-*",
    "tmve_review_w1045_verify.md",
    "archive/scripts/batches/w10xx/_w1013_download.py",
    "archive/scripts/batches/w10xx/_w1018_download.py",
    "archive/scripts/batches/w10xx/_w1043_download.py",
    "archive/scripts/batches/w10xx/_w1043_make_spec.py",
    "archive/scripts/batches/w10xx/_w1043_master.py",
    "archive/scripts/batches/w10xx/_w1043_pick.py",
    "archive/scripts/batches/w10xx/_w1043_prepare.py",
    "archive/scripts/batches/w10xx/_w1043_verify.py",
]


def _git(*args):
    out = subprocess.run(["git", "-c", "core.quotepath=false", "-C", REPO] + list(args),
                         capture_output=True).stdout
    return out.decode("utf-8", "replace")


def _excluded(path):
    return any(fnmatch.fnmatch(path, pat) for pat in EXCLUDE)


def _collect_files():
    files = []

    def add(p):
        p = p.strip().strip('"')
        if p and not p.startswith("tmpe/") and not _excluded(p) and p not in files:
            files.append(p)

    for ln in _git("diff", "--cached", "--name-only").splitlines():
        add(ln)
    for ln in _git("diff", "--name-only").splitlines():
        add(ln)
    for ln in _git("status", "--porcelain").splitlines():
        if ln.startswith("?? "):
            add(ln[3:])
    alive = [p for p in files
             if os.path.exists(os.path.join(REPO, p.replace("/", os.sep)))]
    dropped = [p for p in files if p not in alive]
    if dropped:
        print("[DEBUG] 剔除磁盘已不存在路径 %d 项" % len(dropped))
    return sorted(alive)


def _rename_map():
    m = {}
    for ln in _git("status", "--porcelain").splitlines():
        if ln.startswith("R  ") and " -> " in ln:
            old, new = ln[3:].split(" -> ", 1)
            m[old.strip()] = new.strip()
    return m


def main() -> int:
    files = _collect_files()
    renames = _rename_map()
    deleted = sorted(p for p in renames if p not in files)
    print("[DEBUG] files=%d · rename=%d · 删除面=%d" % (len(files), len(renames), len(deleted)))

    def note_of(f):
        if f == "scripts/check_chart_data.py":
            return "图表判据（剥标签按语法约束 + 注释优先剥离 + 2 例可证伪锁）"
        if f.startswith("site/static/images/"):
            return "站点图（判据输出变化的连带产物）"
        if f == "scripts/check_cross_line_rewrite.py":
            return "跨行扫描器（上一批成果·本批未改）"
        if f == "scripts/cross_line_baseline.json":
            return "跨行判据基线（上一批成果·本批未改）"
        if f == "scripts/batch_cascade.py":
            return "级联工具（上一批成果·本批未改）"
        if f == "scripts/subject_band.py" or f == "scripts/check_crop.py":
            return "og 裁切根修与判据加固（上一批成果·本批未改）"
        if f.startswith("tests/"):
            return "本批单测"
        if f == "docs/agent/gates.md" or f == "docs/agent/pitfalls.md":
            return "治理面（槽数口径 / 坑表 +5 条）"
        if f.startswith("docs/11-"):
            return "方案报告（执行前计划 + 复核报告 / README 登记归位与件数实算）"
        if f.startswith("docs/00-"):
            return "台账（认领行与收官回填）"
        if f.startswith("scripts/output/"):
            return "登记面产物（索引/统计/工具清单）"
        return "本批新增/修改"

    rows = ["| %s | W1045 | %s |" % (f, note_of(f)) for f in files]
    for old in deleted:
        rows.append("| %s | W1045 | 本批改名·旧名（已由 %s 取代） |" % (old, renames[old]))

    body = BODY + "、".join(files) + "。\n\n"
    body += ("**本批要点**：① **两路逐处复核 167 处候选**——scripts 域 38 处（真缺陷 **0** · 假阳 18 · "
             "只读 20）· archive 域 129 处（真缺陷 **13** · 假阳 106 · 只读 10）；② **真缺陷 13 处**"
             "同族同形态（close_cascade 家族「项目说明列表行」正则末尾 `[^·]*` 无尾锚点 ⇒ 替换时"
             "静默吞掉「当前版本」行之下的「当前阶段」「关键产出」两行·构造实验行数 5 → 2）⇒ "
             "**两处**排除符都补 `\\n\\r`（只补末尾一处时扫描器仍判可跨行）· 行为中性；"
             "③ **判据升级**——基线键由内容指纹升为**四输入**（文件|完整模式|完整替换串|行号）⇒ "
             "堵死三类残余豁免（同文件新增同模式调用点 / 替换串语义变更 / 超长模式显示截断撞键）；"
             "跨行判定补 `\\s` 盲区（`\\s` 亦排除换行）· 自测 11 → 12 例；④ **存量陈旧清理**——"
             "槽数三处统一 **52**（gates.md 标题 / HANDOVER 指针 / scripts/README）· 基线失效项清理"
             "（50 → 44）· `docs/11-方案报告/README.md` 4 条登记行由末尾游离表迁回各分区表尾 + "
             "§五 15 → 16 / §六 51 → 54（按磁盘实算）；⑤ **og 切头 A+ 修复**——按用户裁决"
             "「缺陷修复与版式统一分开记账」：回退 **99** 张无缺陷存量的版式改写、保留 **13** 张"
             "（本批 12 张中 5 张真被切 + 存量同类 2 张）⇒ 保留张顶边留白 27–31px、**0 张被切**·"
             "落位验收仍 0 FAIL；⑥ **坑表 +5 条**（133 → 138）· 治理声明对账 0 FAIL。\n\n")
    body += ("**验证**：逐处结论 167/167 · 真缺陷修复 13/13 · 扫描器自测 12/12 · 扫描器单测 9 passed · "
             "跨行门禁 0 FAIL（基线外新增 0 处）· 治理声明对账 0 FAIL（坑表 138）· og 保留张顶边 "
             "27–31px（0 张被切）· 母版判据 124/0 · 裁切验算 124/0 · 落位验收 0 FAIL · "
             "全量门禁见收官提交。\n\n")
    body += ("> - **状态**：已收官（复核 167 处 + 真缺陷 13 处已修 + 判据升四输入 + 存量陈旧清理 + "
             "og A+ 修复 + 坑表 +5 条·待用户裁决 check_chart_data 剥标签取舍）\n")

    spec = {
        "batch": BATCH,
        "date": DATE,
        "title": TITLE,
        "desc": DESC,
        "head_entry": HEAD_ENTRY,
        "head_sentence": HEAD_SENTENCE,
        "changelog_body": body,
        "milestone_block": MILESTONE,
        "agents_note": AGENTS_NOTE,
        "file_index_rows": rows,
    }
    io.open(SPEC, "w", encoding="utf-8", newline="\n").write(json.dumps(spec, ensure_ascii=False, indent=1))
    print("spec 写出 · %s · 文件清单 %d 项 · file_index %d 行 · agents_note %d 字"
          % (os.path.basename(SPEC), len(files), len(rows), len(AGENTS_NOTE)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
