#!/usr/bin/env python3
"""check_doc_size_budget.py — 治理文档体积窗口门禁（W960 建 · 文档规范 §8 机器化）。

背景：§8 的「CHANGELOG / file-index > 50KB 或 500 行 → 归档」自 W511 时代起就是**纯条文**——
verify 54 段零体积判据、CI 零检查、级联每批只插不问，结果 CHANGELOG 长到 480KB/145 段
（超旧线 9.6 倍）、file-index 431KB/247 段（自 W511 后从未归档）。这与 W824 干扰日志断档、
第 43 篇复盘断档同族：**靠自觉的机制必掉档**（W824 实证），本门禁是同族第三个触发器。

判据（W960 立窗·W921「正本 110 段」先例沉淀为正式口径）：
  C1 CHANGELOG 正本段数 ≤ 110（超窗 FAIL）
  C2 file-index 正本段数 ≤ 110（超窗 FAIL）
  报告值（不判红）：四文件 KB / 行数 / HANDOVER 里程碑概要块数——KB 不作判据
  （旧 50KB 线按 W921 后实态废止·由本门禁的窗口制替代，见文档规范 §8）。

接线：preflight_check.py 开工判据（超窗 FAIL 拦截开工·修法=跑 scripts/archive_segments.py）；
batch_cascade.py 落盘后提示位（每批收官报一次体积态）。

用法：
  py -3 scripts/check_doc_size_budget.py              # 门禁（exit 1 = 超窗）
  py -3 scripts/check_doc_size_budget.py --report     # 只报不判
  py -3 scripts/check_doc_size_budget.py --self-test
"""
from __future__ import annotations

import argparse
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RE_CL_SEG = re.compile(r"^### (?:v[\d.]+（[^）]*）：W(\d+)|W(\d+)（[^）]*）：)", re.M)
RE_FI_SEG = re.compile(r"^## (W\d+) ", re.M)
RE_HANDOVER_BLOCK = re.compile(r"^- \*\*(?:v[\d.]+ )?W\d+[^*]*\*+：", re.M)
# W1014：AGENTS 脚注固定尾句家具（写入侧 batch_cascade.py:396 `tail = "。如与上述权威文档
# 冲突，以权威文档为准。*"` 逐字对齐）——C4 逐条计量前剥它，使判据口径与写入侧「量 note 本体」
# 一致；否则末条 = note + 家具被合并计数，任何 97–120 字注记皆「级联绿 / 门禁红」（W1013 首踩）
_FOOTNOTE_TAIL_RE = re.compile(r"。?如与上述权威文档冲突，以权威文档为准。?\*+\s*$")


def check_footnote_shape(footnote_line, cap=120):
    r"""AGENTS 版本脚注逐条定形判据（W965 C4·W1014 口径对齐）→ 违规描述列表（空 = 合规）。

    计量对象 = **剥去固定尾句家具后的条目本体**，与写入侧 batch_cascade 的
    `spec.agents_note 长 > 120` 守卫同一口径。家具是文档级免责句（非任何一批的注记），
    原实现把它并进末条计数 ⇒ 97–120 字注记「级联绿 / 门禁红」（W1013 首踩：117 字被算 141）。
    剥离只影响末条的家具部分，条目本体超长照样抓（见 _self_test 负样本）。
    """
    bad = []
    for e in re.split(r"；(?=20\d{2}-\d{2}-\d{2}（)", footnote_line)[1:]:
        if not re.match(r"^20\d{2}-\d{2}-\d{2}（W\d{3,4}）", e):
            bad.append("条目头非阿拉伯形态：" + e[:24])
            continue
        body = _FOOTNOTE_TAIL_RE.sub("", e)
        if len(body) > cap:
            bad.append("条目 %d 字 > %d：%s…" % (len(body), cap, body[:24]))
    return bad

# 正本窗口（文档规范 §8·W960 立窗）
WINDOWS = {
    os.path.join("CHANGELOG.md"): 110,
    os.path.join("scripts", "output", "file-index.md"): 110,
    os.path.join("docs", "00-导读", "W批次编号对账表.md"): 60,
}
REPORT_FILES = WINDOWS | {
    os.path.join("AGENTS.md"): None,
    os.path.join("HANDOVER.md"): None,
}


def count_segments(text, kind):
    """按文件种类数正本段数（kind: changelog|file-index）。"""
    if kind == "changelog":
        return len(RE_CL_SEG.findall(text))
    if kind == "ledger":
        return len(re.findall(r"(?m)^\| W\d{3,4} ", text))
    return len(RE_FI_SEG.findall(text))


def evaluate(counts):
    """{相对路径: 段数} → 超窗 FAIL 清单（空 = 合规）——纯函数。

    键归一：调用方可能传正斜杠形态（collect 用 os.path.join 在 Windows 产生反斜杠），
    两侧都查一次——W960 单测实证键形态不一致会把「超窗」误判成「缺文件」。
    """
    fails = []
    for rel, window in WINDOWS.items():
        n = counts.get(rel)
        if n is None:
            n = counts.get(rel.replace("\\", "/"))
        if n is None:
            fails.append("体积窗口 C%s: %s 不可读（fail-closed）" % (len(fails) + 1, rel))
        elif n > window:
            # 修法指引按文件种类分治（W976）：台账是表格行且行序穿插，归档工具是
            # archive_ledger_rows.py（W970 建）——段式 archive_segments.py 不管台账，
            # 旧文案对台账是死路指引（实测：C3 超窗期台账修剪器恰在 A5 崩溃期）。
            tool = ("scripts/archive_ledger_rows.py --apply（台账行归档）"
                    if "对账表" in rel else "scripts/archive_segments.py 归档")
            fails.append(
                "体积窗口 C%d: %s 正本 %d 段 > 窗口 %d 段——先跑 %s 再动工（文档规范 §8·W960 立窗）"
                % (len(fails) + 1, rel, n, window, tool))
    return fails


def _read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8", newline="") as f:
        return f.read()


def collect():
    """实盘取数 → (counts, report_lines, extra_fails)。"""
    counts, lines, extra_fails = {}, [], []
    for rel in REPORT_FILES:
        try:
            t = _read(rel)
        except OSError as e:
            counts[rel] = None
            lines.append("体积窗口  %-38s 读取失败（%s）" % (rel, e))
            continue
        kb = len(t.encode("utf-8")) / 1024
        nlines = t.count("\n") + 1
        if rel in WINDOWS:
            if "对账表" in rel:
                kind = "ledger"
            else:
                kind = "changelog" if "CHANGELOG" in rel else "file-index"
            n = count_segments(t, kind)
            counts[rel] = n
            window = WINDOWS[rel]
            mark = "超窗!" if n > window else "ok"
            lines.append("体积窗口  %-38s %7.1f KB %6d 行  段 %4d / 窗口 %d  %s"
                         % (rel, kb, nlines, n, window, mark))
        else:
            extra = ""
            if "HANDOVER" in rel:
                h1 = t.find("## 一、当前进度")
                pm = t.find("> 历史概要（W")
                blocks = len(RE_HANDOVER_BLOCK.findall(t[h1:pm])) if 0 <= h1 < pm else -1
                extra = "  概要块 %d" % blocks
                extra += "（>6 须滚·W511 留 5 版口径）" if blocks > 6 else ""
                # ---- C7-4/5/6：HANDOVER 版本面契约（W982·三层方案②——W973/W961 手搓实证的开工面防线）----
                if not re.search(r"当前 HEAD = W\d{3,4}（[^）]*；详见 CHANGELOG）。", t):
                    extra_fails.append(
                        "体积窗口 C7: HANDOVER「当前 HEAD」句形态失配（W973 清理批实证·级联下批锚点被破坏）"
                        "——修法=恢复「当前 HEAD = W###（…；详见 CHANGELOG）。」")
                for hl in re.findall(r"[^\n]*最后更新：[^\n]*", t):
                    _seg = hl[hl.find("最后更新：") + len("最后更新："):]  # W982 修：只数更新条目——尾链行含「创建于 2026-07-25」同 line 会误计
                    if len(re.findall(r"20\d{2}-\d{2}-\d{2}（", _seg)) > 3:
                        extra_fails.append(
                            "体积窗口 C7: HANDOVER 更新链条目 >3（W961/W963 手搓粘连实证·维护契约②）"
                            "——修法=保留最新 3 条其余迁 CHANGELOG")
                if blocks > 6:
                    extra_fails.append(
                        "体积窗口 C7: HANDOVER 概要块 %d > 6（里程碑只插不旋·W961/W963 积 19 块实证）"
                        "——修法=走 batch_cascade 滚动淘汰最老块" % blocks)
            if "AGENTS" in rel:
                fs = t.find("*本文件由")
                if fs >= 0:
                    fline = t[fs:t.find("\n", fs)]
                    fkb = len(fline.encode("utf-8")) / 1024
                    extra = "  版本脚注 %.1f KB" % fkb
                    if fkb > 4:
                        extra_fails.append(
                            "体积窗口 C3: AGENTS.md 版本脚注 %.1f KB > 4 KB——滚动器切分失明或条目超长"
                            "（W964 定形契约·修法=双形态切分+条目 ≤300 字+存量迁归档）" % fkb)
            if "HANDOVER" in rel:
                hkb = len(t.encode("utf-8")) / 1024
                if hkb > 45:
                    extra_fails.append(
                        "体积窗口 C6: HANDOVER.md %.1f KB > 45 KB——五区只进不出复发"
                        "（W973 契约·修法=已完成条目清除+叙事迁 HANDOVER-ARCHIVE+指针化）" % hkb)
            if "AGENTS" in rel:
                # W965 C4：逐条定形判据（比聚合 4KB 更细——五条各 290 字的脚注可绕过 C3）
                # W999 修：原嵌在 HANDOVER>45KB 分支内——死门控（HANDOVER 瘦身后 C4 永不执行）
                # 且 fline 跨迭代引用可 NameError（subagent 审查 P1-1 实证复现）
                # W1014：判据抽出为 check_footnote_shape（纯函数·供单测证伪），口径与写入侧对齐
                if fs >= 0:
                    bad = check_footnote_shape(fline)
                    if bad:
                        extra_fails.append(
                            "体积窗口 C4: AGENTS.md 脚注 %d 条违规定形（W965 逐条判据·W1014 剥固定尾句后计）：%s"
                            % (len(bad), "；".join(bad[:3])))
            lines.append("体积报告  %-38s %7.1f KB %6d 行%s" % (rel, kb, nlines, extra))

    # ---- C7-1/2/3：三文档版本行锚尾（W982·三层方案②——锚尾是下批级联的 regex 依赖·手搓删除即全仓级联瘫痪）----
    c7_faces = (
        ("README.md",
         r"(?m)^> \*\*当前批次 W\d{3,4}（20\d{2}-\d{2}-\d{2}）\*\*：.*·A1-A6", "锚尾 ·A1-A6"),
        ("STRUCTURE.md",
         r"(?m)^> 当前批次：W\d{3,4}（20\d{2}-\d{2}-\d{2}）— .*—\s*A1-A6", "锚尾 —A1-A6"),
        (os.path.join("docs", "00-导读", "项目说明.md"),
         r"(?m)^> 当前批次 W\d{3,4}（20\d{2}-\d{2}-\d{2}）：.*·详细变更见", "锚尾 ·详细变更见"),
    )
    for rel, pat, tail_name in c7_faces:
        try:
            ft = _read(rel)
        except OSError:
            continue  # 文件缺失归 C5/C4-f 等既有判据管
        if not re.search(pat, ft):
            extra_fails.append(
                "体积窗口 C7: %s 版本行 %s 失配（手搓破坏级联锚点·W955/W961/W963 实证）"
                "——修法=恢复「当前批次 W###（日期）：…%s」形态或走 batch_cascade 级联" % (rel, tail_name, tail_name))
    return counts, lines, extra_fails


def gate_lines():
    """门禁入口：返回 (FAIL 清单, 输出行)。"""
    counts, lines, extra_fails = collect()
    return evaluate(counts) + extra_fails, lines


def main() -> int:
    ap = argparse.ArgumentParser(description="治理文档体积窗口门禁（W960）")
    ap.add_argument("--report", action="store_true", help="只报不判（exit 0）")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return _self_test()
    fails, lines = gate_lines()
    for line in lines:
        print(line)
    if args.report:
        return 0
    if fails:
        for f in fails:
            print("FAIL ", f)
        print("---- 体积窗口门禁：%d FAIL（修法=按各 FAIL 行内指引跑对应归档工具）----" % len(fails))
        return 1
    print("---- 体积窗口门禁：0 FAIL（窗口 %s）----" % WINDOWS)
    return 0


def _self_test() -> int:
    fails = []

    # count_segments：两种段标题形态
    cl = "\n".join(["### W958（2026-10-26）：a", "x", "### W957（2026-10-26）：b",
                    "### v2.3.9（2026-08-01）：W900 c", "尾巴"])
    if count_segments(cl, "changelog") != 3:
        fails.append("changelog 段计数应 3（含旧 v 前缀形态）")
    fi = "\n".join(["## W958 标题（2026-10-26）", "| a | b |", "## W957 标题（d）"])
    if count_segments(fi, "file-index") != 2:
        fails.append("file-index 段计数应 2")

    # evaluate：窗口边界（110 过 / 111 红）+ 缺文件 fail-closed
    if evaluate({"CHANGELOG.md": 110, os.path.join("scripts", "output", "file-index.md"): 110, os.path.join("docs", "00-导读", "W批次编号对账表.md"): 60}) != []:
        fails.append("负样本：恰在窗口上必须 0 FAIL")
    out = evaluate({"CHANGELOG.md": 111, os.path.join("scripts", "output", "file-index.md"): 5, os.path.join("docs", "00-导读", "W批次编号对账表.md"): 60})
    if len(out) != 1 or "111" not in out[0]:
        fails.append("111 段必须恰好产出 1 条 FAIL 且带计数")
    if evaluate({}) == []:
        fails.append("负样本：文件缺失必须 fail-closed 判红（禁静默跳过）")

    # 修法指引分治（W976）：台账超窗必须指向 archive_ledger_rows（段式工具不管台账）
    out_led = evaluate({"CHANGELOG.md": 110, os.path.join("scripts", "output", "file-index.md"): 110,
                        os.path.join("docs", "00-导读", "W批次编号对账表.md"): 61})
    if len(out_led) != 1 or "61" not in out_led[0] or "archive_ledger_rows" not in out_led[0]:
        fails.append("台账超窗必须恰好 1 条 FAIL 且指引 archive_ledger_rows")

    print()
    if fails:
        print("自测 %d 项不一致：%s" % (len(fails), fails))
        return 1
    print("自测通过：计数两形态 + 窗口边界 + 缺件 fail-closed（判据可证伪）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
