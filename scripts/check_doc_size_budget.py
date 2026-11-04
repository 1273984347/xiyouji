#!/usr/bin/env python3
"""check_doc_size_budget.py — 治理文档体积窗口门禁（W960 建 · 文档规范 §8 机器化）。

背景：§8 的「CHANGELOG / file-index > 50KB 或 500 行 → 归档」自 W511 时代起就是**纯条文**——
verify 54 段零体积判据、CI 零检查、级联每批只插不问，结果 CHANGELOG 长到 480KB/145 段
（超旧线 9.6 倍）、file-index 431KB/247 段（自 W511 后从未归档）。这与 W824 干扰日志断档、
第 43 篇复盘断档同族：**靠自觉的机制必掉档**（W824 实证），本门禁是同族第三个触发器。

判据（W960 立窗·W921「正本 110 段」先例沉淀为正式口径·W1120 补体积第二阈值）：
  C1 CHANGELOG 正本段数 ≤ 110（超窗 FAIL）
  C2 file-index 正本段数 ≤ 110（超窗 FAIL）
  C8 正本体积字节 ≤ MAX_DOC_BYTES（262144·单一事实源在 batch_closeout 顶层·W1119 立）
     —— **双阈值「先到者为准」**：段数窗与字节窗任一超即红（W1120 立）
     —— 字节阈值常量**只引用**既有持有方（batch_closeout）·不复制·不新建中立模块
  报告值（不判红）：四文件行数 / HANDOVER 里程碑概要块数 / AGENTS 脚注体积
  （旧 50KB 线按 W921 后实态废止·由本门禁的窗口制替代，见文档规范 §8；
    KB 自 W1120 起由报告值升为判据·口径同步见文档规范 §8 的 W1120 双阈值条目）。

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
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# W1120：体积第二阈值的**单一事实源**在 batch_closeout.py 顶层（W1119 立）⇒ 本门禁侧
# 只**引用**、不复制、不新建中立模块（让消费方引用既有持有方 ⇒ 持有方零改动·省一组 CI）。
# 引用失败 ⇒ 体积判据不可执行 ⇒ fail-closed 判红（evaluate_sizes 内）·不静默放行。
try:
    from batch_closeout import LEDGER_WINDOW, MAX_DOC_BYTES  # noqa: E402
    _SAME_SOURCE_ERR = None
except Exception as exc:  # noqa: BLE001 — 引用失败不抛栈打断全仓·改由判据 fail-closed
    MAX_DOC_BYTES = None
    LEDGER_WINDOW = None
    _SAME_SOURCE_ERR = "%s: %s" % (type(exc).__name__, exc)

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
# 台账行窗口同源于 batch_closeout.LEDGER_WINDOW（W1119 立·W1120 引用）
# ⇒ 引用失败时回退 60（W960 原值）·此时体积判据 fail-closed 判红（见 evaluate_sizes）
WINDOWS = {
    os.path.join("CHANGELOG.md"): 110,
    os.path.join("scripts", "output", "file-index.md"): 110,
    os.path.join("docs", "00-导读", "W批次编号对账表.md"): (
        LEDGER_WINDOW if LEDGER_WINDOW is not None else 60),
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


def evaluate_sizes(sizes):
    """体积第二阈值判据：正本体积字节 ≤ MAX_DOC_BYTES → FAIL 清单（空 = 合规）。

    W1120 立：段数窗口只管「条数」管不住「单条超长」⇒ 实测段面曾达 390.8KB / 109 段
    （段数在窗内·体积已超 256KiB 约 1.5 倍）⇒ 补字节第二阈值，**双阈值先到者为准**。

    sizes: {相对路径: 字节数}；键归一与 evaluate 同口径（两种分隔形态都查）。
    同源常量不可用 ⇒ fail-closed 判红（体积判据不可执行不得静默放行）。
    """
    if _SAME_SOURCE_ERR:
        return ["体积窗口 C8: 同源常量不可用（batch_closeout 引用失败：%s）"
                "——体积第二阈值不可执行（fail-closed·须修引用后方可放行）" % _SAME_SOURCE_ERR]
    fails = []
    for rel in WINDOWS:
        n = sizes.get(rel)
        if n is None:
            n = sizes.get(rel.replace("\\", "/"))
        if n is None:
            fails.append("体积窗口 C8: %s 体积不可读（fail-closed）" % rel)
        elif n > MAX_DOC_BYTES:
            fails.append(
                "体积窗口 C8: %s 正本 %d 字节 > 体积上限 %d 字节"
                "——先跑 scripts/archive_segments.py --target both --max-bytes %d --chunk 50 --apply"
                "归档腾窗（文档规范 §8·W1120 双阈值）"
                % (rel, n, MAX_DOC_BYTES, MAX_DOC_BYTES))
    return fails


def _collect_sizes():
    """实盘取正本体积字节数 → (sizes, 报告行)。读失败 ⇒ 键缺失 ⇒ 交 evaluate_sizes 判红。"""
    sizes, lines = {}, []
    for rel in WINDOWS:
        try:
            with open(os.path.join(ROOT, rel), "rb") as f:
                data = f.read()
        except OSError as e:
            lines.append("体积阈值  %-38s 体积读取失败（%s）" % (rel, e))
            continue
        sizes[rel] = len(data)
        lines.append("体积阈值  %-38s %8d 字节 / 上限 %s 字节  %s"
                     % (rel, len(data), MAX_DOC_BYTES,
                        "超限!" if MAX_DOC_BYTES and len(data) > MAX_DOC_BYTES else "ok"))
    return sizes, lines


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
                extra, face_fails = _handover_face(t)
                extra_fails.extend(face_fails)
            elif "AGENTS" in rel:
                extra, face_fails = _agents_face(t)
                extra_fails.extend(face_fails)
            lines.append("体积报告  %-38s %7.1f KB %6d 行%s" % (rel, kb, nlines, extra))

    extra_fails.extend(_version_line_anchors())
    return counts, lines, extra_fails


def _handover_face(t):
    """HANDOVER 面判据：概要块计数 + C7-4/5/6 + C6 → (extra 文本, extra_fails)。

    W1120：从 collect() 等价拆出（结构档宽档阈值：复杂度 21 > 15 / 分支 22 > 16）。
    拆分只做结构搬迁·判据与文案逐字不变（既有单测 test_c7_* 与 test_footnote_* 覆盖）。
    """
    h1 = t.find("## 一、当前进度")
    pm = t.find("> 历史概要（W")
    blocks = len(RE_HANDOVER_BLOCK.findall(t[h1:pm])) if 0 <= h1 < pm else -1
    extra = "  概要块 %d" % blocks
    extra += "（>6 须滚·W511 留 5 版口径）" if blocks > 6 else ""
    fails = []
    if not re.search(r"当前 HEAD = W\d{3,4}（[^）]*；详见 CHANGELOG）。", t):
        fails.append(
            "体积窗口 C7: HANDOVER「当前 HEAD」句形态失配（W973 清理批实证·级联下批锚点被破坏）"
            "——修法=恢复「当前 HEAD = W###（…；详见 CHANGELOG）。」")
    for hl in re.findall(r"[^\n]*最后更新：[^\n]*", t):
        _seg = hl[hl.find("最后更新：") + len("最后更新："):]  # W982 修：只数更新条目——尾链行含「创建于 2026-07-25」同 line 会误计
        if len(re.findall(r"20\d{2}-\d{2}-\d{2}（", _seg)) > 3:
            fails.append(
                "体积窗口 C7: HANDOVER 更新链条目 >3（W961/W963 手搓粘连实证·维护契约②）"
                "——修法=保留最新 3 条其余迁 CHANGELOG")
    if blocks > 6:
        fails.append(
            "体积窗口 C7: HANDOVER 概要块 %d > 6（里程碑只插不旋·W961/W963 积 19 块实证）"
            "——修法=走 batch_cascade 滚动淘汰最老块" % blocks)
    hkb = len(t.encode("utf-8")) / 1024
    if hkb > 45:
        fails.append(
            "体积窗口 C6: HANDOVER.md %.1f KB > 45 KB——五区只进不出复发"
            "（W973 契约·修法=已完成条目清除+叙事迁 HANDOVER-ARCHIVE+指针化）" % hkb)
    return extra, fails


def _agents_face(t):
    """AGENTS 面判据：版本脚注体积 + C3 + C4 → (extra 文本, extra_fails)。

    W1120：从 collect() 等价拆出（fs<0 时两段判据皆不执行·与原实现同口径）。
    """
    fs = t.find("*本文件由")
    if fs < 0:
        return "", []
    fline = t[fs:t.find("\n", fs)]
    fkb = len(fline.encode("utf-8")) / 1024
    extra = "  版本脚注 %.1f KB" % fkb
    fails = []
    if fkb > 4:
        fails.append(
            "体积窗口 C3: AGENTS.md 版本脚注 %.1f KB > 4 KB——滚动器切分失明或条目超长"
            "（W964 定形契约·修法=双形态切分+条目 ≤300 字+存量迁归档）" % fkb)
    # W965 C4：逐条定形判据（比聚合 4KB 更细——五条各 290 字的脚注可绕过 C3）
    # W999 修：原嵌在 HANDOVER>45KB 分支内——死门控（HANDOVER 瘦身后 C4 永不执行）
    # W1014：判据抽出为 check_footnote_shape（纯函数·供单测证伪），口径与写入侧对齐
    bad = check_footnote_shape(fline)
    if bad:
        fails.append(
            "体积窗口 C4: AGENTS.md 脚注 %d 条违规定形（W965 逐条判据·W1014 剥固定尾句后计）：%s"
            % (len(bad), "；".join(bad[:3])))
    return extra, fails


def _version_line_anchors():
    """C7-1/2/3：三文档版本行锚尾 → extra_fails 列表（锚尾是下批级联的 regex 依赖）。

    W1120：从 collect() 等价拆出（文件缺失仍静默跳过·归 C5/C4-f 等既有判据管）。
    """
    c7_faces = (
        ("README.md",
         r"(?m)^> \*\*当前批次 W\d{3,4}（20\d{2}-\d{2}-\d{2}）\*\*：.*·A1-A6", "锚尾 ·A1-A6"),
        ("STRUCTURE.md",
         r"(?m)^> 当前批次：W\d{3,4}（20\d{2}-\d{2}-\d{2}）— .*—\s*A1-A6", "锚尾 —A1-A6"),
        (os.path.join("docs", "00-导读", "项目说明.md"),
         r"(?m)^> 当前批次 W\d{3,4}（20\d{2}-\d{2}-\d{2}）：.*·详细变更见", "锚尾 ·详细变更见"),
    )
    fails = []
    for rel, pat, tail_name in c7_faces:
        try:
            ft = _read(rel)
        except OSError:
            continue  # 文件缺失归 C5/C4-f 等既有判据管
        if not re.search(pat, ft):
            fails.append(
                "体积窗口 C7: %s 版本行 %s 失配（手搓破坏级联锚点·W955/W961/W963 实证）"
                "——修法=恢复「当前批次 W###（日期）：…%s」形态或走 batch_cascade 级联" % (rel, tail_name, tail_name))
    return fails


def gate_lines():
    """门禁入口：返回 (FAIL 清单, 输出行)。"""
    counts, lines, extra_fails = collect()
    sizes, size_lines = _collect_sizes()
    return evaluate(counts) + evaluate_sizes(sizes) + extra_fails, lines + size_lines


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

    # ---- W1120 体积第二阈值（字节）·判据须可证伪 ----
    cap = MAX_DOC_BYTES if MAX_DOC_BYTES else 262144
    at = {rel: cap for rel in WINDOWS}
    if evaluate_sizes(at) != []:
        fails.append("负样本：恰好等于字节上限必须 0 FAIL")
    over = dict(at)
    over[list(WINDOWS)[0]] = cap + 1
    out_sz = evaluate_sizes(over)
    if len(out_sz) != 1 or "C8" not in out_sz[0] or "archive_segments" not in out_sz[0]:
        fails.append("超字节上限必须恰好 1 条 C8 FAIL 且指引 archive_segments")
    if evaluate_sizes({}) == []:
        fails.append("负样本：体积不可读必须 fail-closed 判红（禁静默跳过）")

    print()
    if fails:
        print("自测 %d 项不一致：%s" % (len(fails), fails))
        return 1
    print("自测通过：计数两形态 + 窗口边界 + 缺件 fail-closed（判据可证伪）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
