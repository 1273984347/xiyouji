# -*- coding: utf-8 -*-
"""_w1042_make_spec.py — W1042 级联 spec 生成（沿用 W1018 修正后的口径）

与 W1018 版的三处关键差异（本批已修的根因不重犯）：
  ① git 调用统一 `-c core.quotepath=false` ⇒ 含中文的路径以**真中文**写入段文件行
     （W1018 首版用了 git 默认输出 ⇒ 中文路径成 octal 转义乱码串 `W\346\211\271…`）。
  ② 文件全集 = 已提交 ∪ 索引态 ∪ 工作树 ∪ 未跟踪，再**剔除磁盘已不存在的路径**
     （一次性中间件已清理 ⇒ 列进清单会让第 31 槽 C4-f 判「未入提交树」）。
  ③ 段「文件」行只列**现存路径**（受第 31 槽 C4-f 约束：清单路径须在提交树内）；
     `file_index_rows` 另含 **rename 删除面旧名**（受第 51 槽约束：判据用
     `diff.renames=false` ⇒ rename 两侧都须在 spec 内）。

输出：scripts/output/_w1042_spec.json
用法：py -3 scripts/_w1042_make_spec.py
"""
from __future__ import annotations

import io
import json
import os
import subprocess

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "scripts", "output")
SPEC = os.path.join(OUT, "_w1042_spec.json")

BATCH = "W1042"
DATE = "2026-10-30"
TITLE = "W1042 工具面根因修复与判据补覆盖批（台账回填显式参数 / Makefile 编排 / 第 48 门禁真实新增件 / 可疑改写面复核）"
DESC = "工具面根因修复与判据补覆盖：台账回填显式参数生效、编排提示归位、门禁新增件真实文件覆盖、可疑改写面逐处复核"
HEAD_ENTRY = "2026-10-30（W1042 工具面根因修复与判据补覆盖）"
HEAD_SENTENCE = "工具面根因修复与判据补覆盖：台账回填显式参数生效、编排提示归位、门禁新增件真实文件覆盖、可疑改写面逐处复核"
AGENTS_NOTE = ("2026-10-30（W1042）工具面四修：台账回填显式参数被自动反填分支静默吞、"
               "自测汇总数硬编码、门禁新增件分支未覆盖真实仓内文件、编排完成提示归属错位。"
               "另逐处复核 43 处可疑改写面。")
MILESTONE = ("- **W1042 工具面根因修复与判据补覆盖**（含复盘批角色）：\n"
             "  - 台账回填显式参数生效（原被 --from-git 分支静默吞）+ 自测 12 正例 5 负例\n"
             "  - 第 48 门禁新增件分支补真实仓内文件用例（只替换 HEAD 判定开关）\n"
             "  - 43 处可疑改写面逐处人工复核（真缺陷登记 + 最小修法）\n"
             "  - 坑表 +4 条（124 → 128 条）+ C5e 五处计数链对账一致")

BODY = (
    "\n\n\n\n> **来源**：用户 2026-10-30 连发五项指令（修工具缺陷 / 跨行扫描器接 make ci / "
    "第 48 门禁补真实新增件用例 / 43 处可疑改写面人工复核 / 剩余 56 回继续扩量）⇒ "
    "本批取第 1–4 项（工具面批 = W1042），第 5 项按独立批次推进。\n"
    ">\n"
    "> **批号来源**：`scripts/reserve_w.py` 占号得 W1042（铁律 17·并行会话已推进至 W1041）"
    "；preflight 交集检查 PASS；复盘触发器 T1/T2/T3 三条全中 ⇒ 本批同时认领**复盘批**角色"
    "（最终报告落 `docs/11-方案报告/工作复盘与优化分析报告/`）。\n"
    ">\n"
    "> - **文件**："
)


def _git(*args):
    """git 调用统一加 `-c core.quotepath=false`（中文路径不转义）。"""
    out = subprocess.run(["git", "-c", "core.quotepath=false", "-C", REPO] + list(args),
                         capture_output=True).stdout
    return out.decode("utf-8", "replace")


def _collect_files():
    """本批文件全集（段「文件」行与 file_index_rows 的唯一来源）。

    本批为**一次提交**（工具面 + 登记面同笔）⇒ 清单 = 索引态 ∪ 工作树 ∪ 未跟踪；
    再**剔除磁盘已不存在的路径**（一次性中间件已清理 ⇒ 列进清单会让第 31 槽
    C4-f 判「未入提交树」）。
    """
    files = []

    def add(p):
        p = p.strip().strip('"')
        if p and not p.startswith("tmpe/") and p not in files:
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
        print("[DEBUG] 剔除磁盘已不存在路径 %d 项：%s" % (len(dropped), dropped))
    return sorted(alive)


def _rename_map():
    """本批 rename 映射 {旧名: 新名}（rename 两侧都须在 spec 内）。"""
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
        if f.startswith("scripts/_w1042"):
            return "本批工具脚本"
        if f.startswith("scripts/output/_w1042"):
            return "本批 spec 与级联清单"
        if f.startswith("tests/"):
            return "本批单测（判据覆盖）"
        if f == "scripts/ledger_backfill.py":
            return "台账回填工具（显式参数生效根因修复）"
        if f == "Makefile":
            return "本地 CI 编排（完成提示归位）"
        if f == "docs/agent/pitfalls.md":
            return "坑表（+4 条教训）"
        if f in ("AGENTS.md", "HANDOVER.md"):
            return "计数链同步（坑表条数指针）"
        if f.startswith("docs/11-"):
            return "方案报告（执行前计划 + 复盘报告）"
        if f.startswith("docs/00-"):
            return "台账（认领行与收官回填）"
        if f.startswith("scripts/output/"):
            return "登记面产物（索引/统计/工具清单）"
        return "本批新增/修改"

    rows = ["| %s | W1042 | %s |" % (f, note_of(f)) for f in files]
    for old in deleted:
        rows.append("| %s | W1042 | 本批改名·旧名（已由 %s 取代） |" % (old, renames[old]))

    body = BODY + "、".join(files) + "。\n\n"
    body += ("**本批要点**：① **台账回填显式参数根因修复**——`ledger_backfill.py` 的 `--from-git` "
             "分支把「取值优先级」与「是否产生变更」耦合在同一个 `is None` 判断里 ⇒ 显式 "
             "`--status`/`--hash` 被静默吞且不报错（帮助文案却写「显式可覆盖」）；"
             "同族缺陷 `--cascade` 只在 else 分支处理 ⇒ 改统一取值决策层（显式优先·显式缺失"
             "才用机器反填）；② **自测汇总数改由源码统计**（原硬编码「3 正例绿 + 4 负例红」"
             "⇒ 实为 12 条正例断言 + 5 条负例断言）；③ **第 48 门禁新增件分支补真实仓内文件"
             "用例**（原 tmp 仓根替身 ⇒ 真实路径/真实字节链路从未覆盖；改只替换 HEAD 判定"
             "开关）；④ **43 处可疑改写面逐处人工复核**；⑤ **坑表 +4 条**（124 → 128 条·"
             "六主题分项与 AGENTS/HANDOVER 计数链五处对账一致）；⑥ **`make ci` 接线核实**——"
             "跨行扫描器已由并行 W1014 接入 ci 链（Makefile `$(MAKE) cross-line`）⇒ 本批只做"
             "完成提示归属归位（`==> ci 完成` 原落在 cross-line 目标体内）。\n\n")
    body += ("**验证**：`ledger_backfill --self-test` 退出码 0（12 条正例断言 + 5 条负例断言）· "
             "显式 `--status` 覆盖生效负样本自证（显式文本入列且非自动反填文本）· "
             "`pytest tests/unit/test_plan_template_read_disk.py` **6 例全绿** · "
             "第 48 门禁对本批执行前计划件实跑 **0 FAIL**（新增文件·全项符合）· "
             "跨行扫描器 `--gate` 高危 **0 处** · 43 处可疑面逐处结论见复盘报告 · "
             "全量门禁见收官提交。\n\n")
    body += ("> - **状态**：已收官（工具面四修 + 复核 43 处 + 坑表 +4 条 + 计数链一致·"
             "待用户裁决真缺陷是否即刻修复）\n")

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
