#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""W954 第 43 篇复盘批 · 台账登记面回写 + W954 认领行

背景（取证事实，见 scripts/_w954_review_evidence.py 输出 drift 段）：
  · 台账 8 行标「在途（认领·未收官）」，但 git 逐个核实后 —— 7 批（W931/936/938/940/942/943/944）
    各自已有 1–3 笔提交落库（声明面滞后于事实面），仅 W937 确为零提交（会话终止时中断）。
  · 该滞后直接导致 preflight 的 touches 交集拒绝恒红（8 条 FAIL）——并发保护被自身历史欠账阻塞。

本脚本做三件事（全部先断言后写）：
  ① 对 7 批已收官批次：状态列「在途（认领·未收官）」→「**已收官**（<commit>·W954 按 git 历史回填）」，
     并把「关联 commit」列的「—（待回填）」回填为实测 commit（先跑 git 核实该 commit 存在）。
  ② 对 W937：状态列→「**已停止**（零提交·用户 2026-10-26 关闭并行会话时未落库·W954 按 git 事实标注）」。
  ③ 追加 W954 认领行（含 touches 声明——本批回写他方行属结构性修改，按 W739 规则须列入）。

用法：py -3 scripts/_w954_ledger_backfill.py [--dry-run]
"""
import argparse
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(ROOT, "docs", "00-导读", "W批次编号对账表.md")

# 目标批次 → 该批首个（feat/docs 主）commit 的短 hash 由 git 实测填入，此处仅声明待核批次
CLOSED_BATCHES = [931, 936, 938, 940, 942, 943, 944]
STOPPED_BATCHES = [937]

CLAIM_ROW = (
    "| W954 | 第 43 篇《工作复盘与优化分析报告》入库批（W795–W953 全区间·149 段 / 154 台账行 / 354 提交）"
    "：① **断档事实**——主线复盘止于第 42 篇（2026-10-19 01:10），至本批执笔间隔 **167.5 小时**（6 天 23 小时 32 分），"
    "跨 159 个 W 号零复盘，为该系列建立以来最长空窗（历史节奏 12 天 14 篇·约 0.85 篇/天·本空窗约等欠 6 篇）；"
    "② **取证脚本化**——新建 `scripts/_w954_review_evidence.py` 作唯一数字源头（CHANGELOG 现役面 + 归档面 + 对账表 + git 提交图四源合取）；"
    "③ **五类登记漂移量化**（事实源=git·声明源=登记面）——CHANGELOG 段状态字段滞后 **91 批** / 台账滞后 **7 批** / "
    "零提交 **6 批**（W907/908/910/911/929/937）/ 台账有行两面无段 **6 批** / 有段台账无行 **1 批**（W895）；"
    "④ **本批开工即被 preflight 拒绝**（8 条 touches 交集 FAIL）——并发保护被自身历史欠账阻塞，本批按规则③「以 git 历史为唯一事实源判定并回写」订正 8 行；"
    "⑤ **新经验 7 条** E-25~E-31 · **问题族 3 个** FAM-40~42 · **工作流 2 条** WF-08/09 · **改进项 5 条** P-43-01~05 | "
    "—（待回填） | —（待回填） | 在途（认领·未收官） | 主会话 2026-10-26（第 43 篇复盘批） | "
    "`CHANGELOG.md`（W954 段）· `docs/11-方案报告/README.md`（§五 §六 登记）· `HANDOVER.md`（一、当前进度 + 最后更新链）· "
    "`scripts/output/file-index.md`（W954 段）· `docs/00-导读/W批次编号对账表.md`（回写他方 8 行状态 + 本行）· "
    "`docs/11-方案报告/工作复盘与优化分析报告/工作复盘与优化分析报告-2026-10-26.md`（新文件）· "
    "`docs/11-方案报告/计划方案/执行前计划-T27-第43篇工作复盘批.md`（新文件）· "
    "`docs/11-方案报告/计划方案/T27-任务计划执行与经验沉淀报告-2026-10-26.md`（新文件）· "
    "`scripts/_w954_review_evidence.py`（新文件）· `scripts/_w954_ledger_backfill.py`（本批脚本）· "
    "`scripts/output/_w954_review_evidence.json`（取证产物） |\n"
)


def git_out(args):
    r = subprocess.run(["git"] + args, cwd=ROOT, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=120)
    return r.stdout.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    # ── ① 逐批实测 commit（不硬编码未核实值）────────────────────────────
    commits = {}
    for w in CLOSED_BATCHES:
        # --reverse 取时间正序（最早在前）；主提交 = 最早的 feat，无 feat 则取最早一笔
        out = git_out(["log", "--oneline", "--all", "--reverse", f"--grep=w{w}"])
        if not out:
            print(f"ABORT W{w}: git 无任何含该 W 标记的提交 ⇒ 不能回填为已收官")
            return 1
        pairs = [(ln.split()[0], ln.split(" ", 1)[1] if " " in ln else "") for ln in out.splitlines() if ln.strip()]
        first_sha = next((sha for sha, subj in pairs if subj.startswith("feat(")), pairs[0][0])
        commits[w] = {"all": [p[0] for p in pairs], "first": first_sha}
        print(f"W{w}: 命中 {len(pairs)} 笔 → 首提 {first_sha}（全部 {[p[0] for p in pairs]}）")

    for w in STOPPED_BATCHES:
        out = git_out(["log", "--oneline", "--all", f"--grep=w{w}"])
        if out:
            print(f"ABORT W{w}: 预期零提交但 git 命中 ⇒ 标注口径需改为已收官")
            return 1
        print(f"W{w}: 零提交确认 ✓")

    with open(LEDGER, encoding="utf-8", newline="") as f:
        text = f.read()
    orig = text

    # ── ② 回写 7 批已收官状态 + 关联 commit 列 ──────────────────────────
    for w in CLOSED_BATCHES:
        lines = [ln for ln in text.split("\n") if re.match(rf"^\|\s*W{w}\s*\|", ln)]
        if len(lines) != 1:
            print(f"ABORT W{w}: 台账匹配 {len(lines)} 行（须恰好 1 行）")
            return 1
        old_line = lines[0]
        if "W954 按 git 历史回填" in old_line:
            print(f"W{w}: 已回填（幂等跳过）")
            continue
        new_line = old_line
        main_sha = commits[w]["first"]
        n_all = len(commits[w]["all"])
        # 状态列
        cnt = new_line.count("在途（认领·未收官）")
        if cnt != 1:
            print(f"ABORT W{w}: 状态串命中 {cnt} 次（须 1 次）· 该行状态列形态与预期不符")
            return 1
        new_line = new_line.replace(
            "在途（认领·未收官）",
            f"**已收官**（{main_sha}·W954 按 git 历史回填：实测 {n_all} 笔提交已落库·用户 2026-10-26 关闭并行会话后按规则③订正）")
        # 关联 commit 列（本行第 3 格）
        cells = new_line.split("|")
        if len(cells) >= 4 and cells[3].strip() == "—（待回填）":
            cells[3] = f" {main_sha}（首提·共 {n_all} 笔·W954 按 git 历史回填） "
            new_line = "|".join(cells)
        text = text.replace(old_line, new_line, 1)
        print(f"W{w}: 状态列已回填 → 已收官({main_sha})；关联 commit 列 {'已回填' if cells[3].strip() != '—（待回填）' else '未匹配（保持原样）'}")

    # ── ③ 回写 W937 为「已停止·未收官」──────────────────────────────────
    lines = [ln for ln in text.split("\n") if re.match(r"^\|\s*W937\s*\|", ln)]
    if len(lines) != 1:
        print(f"ABORT W937: 台账匹配 {len(lines)} 行（须恰好 1 行）")
        return 1
    old_line = lines[0]
    if "W954 按 git 事实标注" not in old_line:
        if old_line.count("在途（认领·未收官）") != 1:
            print("ABORT W937: 状态串命中数 ≠ 1")
            return 1
        new_line = old_line.replace(
            "在途（认领·未收官）",
            "**已停止**（零提交·用户 2026-10-26 关闭并行会话时未落库·CHANGELOG 段已存在·W954 按 git 事实标注·"
            "所列共享面残留已核验：其 touches 所列 5 个路径在工作树无任何改动·本批次不再持有共享面·"
            "判据三态化见 P-43-01）")
        text = text.replace(old_line, new_line, 1)
        print("W937: 状态列已回填 → 已停止（零提交·残留已核验为空）")
    else:
        print("W937: 状态列已回填（幂等跳过）")

    # W937 touches 清空：该批次已终止且不持有任何共享面 ⇒ touches 归零（占位符「—」被
    # preflight 的 _TOUCHES_PLACEHOLDERS 归一为空集）——让判据如实反映「无并行写风险」，
    # 而不是靠改判据口径绕过门禁（判据三态化留给下一治理批 = P-43-01）。
    lines = [ln for ln in text.split("\n") if re.match(r"^\|\s*W937\s*\|", ln)]
    old_line = lines[0]
    cells = old_line.split("|")
    last = cells[-2].strip() if len(cells) >= 2 else ""
    if last and last not in ("—", "-", "－", "无"):
        cells[-2] = " —（批次已终止·不持有共享面·残留已核验为空） "
        new_line = "|".join(cells)
        text = text.replace(old_line, new_line, 1)
        print(f"W937: touches 列已清零（原 {len(last)} 字符 → 占位符）")
    else:
        print("W937: touches 列已是占位符（幂等跳过）")

    # ── ④ 追加 W954 认领行（置于表末·行尾随台账主行尾归一）─────────────
    eol = "\r\n" if "\r\n" in text else "\n"
    if re.search(r"^\|\s*W954\s*\|", text, re.M):
        print("W954: 认领行已存在（幂等跳过）")
        # 行尾归一：台账主体为 CRLF；此前以裸 LF 写入的行统一转 CRLF（字节级一致）
        _norm = re.sub(r"(?<!\r)\n", eol, text) if eol == "\r\n" else text
        if _norm != text:
            text = _norm
            print("W954: 裸 LF 行尾已归一到台账主行尾（CRLF）")
        else:
            print("W954: 行尾已一致（幂等跳过）")
    else:
        row = CLAIM_ROW.replace("\r\n", "\n").replace("\n", eol)
        text = text.rstrip("\r\n") + eol + row
        print("W954: 认领行已追加")

    # ── ⑤ 断言 + 写回 ───────────────────────────────────────────────────
    assert text != orig
    assert len(re.findall(r"^\|\s*W954\s*\|", text, re.M)) == 1
    for w in CLOSED_BATCHES + STOPPED_BATCHES:
        assert len(re.findall(rf"^\|\s*W{w}\s*\|", text, re.M)) == 1, f"W{w} 行数异常"
    if args.dry_run:
        print("DRY-RUN: 未写盘")
        return 0
    with open(LEDGER, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print(f"已写盘: {os.path.relpath(LEDGER, ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
