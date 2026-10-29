#!/usr/bin/env python3
"""check_backlog_review.py — Backlog 登记面对账触发器（W1021 建·与对抗审查触发器同族第四哨）。

背景：W1019 连续命中两条「已做完却仍挂待办」的 Backlog（BL-29 测试与 CI 早已落地、BL-33
W895 已收敛一轮），W1020 全量对账实测 **29 条里 12 条（41%）滞后**。结论：Backlog 的衰减不是
偶发而是结构性的——条目自述不可信，只有周期性拿 git 与测试实况核才能收敛。本触发器把对账
从「想起来才做」变成「每 ≥25 批机器点名」。

判据（单一·台账即事实源）：
  A1 台账**状态列**含事件 token「Backlog 对账已执行」的认领行，其**最大 W 号**距当前 max(W)
     ≥ THRESHOLD 批 → 触发。找不到 token 行 → 按「从未对账」处理（fail-closed·宁假警不漏警）。

口径铁则（沿用 check_audit_trigger 三条，同一病同一防法）：
  · **字样 ≠ 事件**：泛词「Backlog 对账」会出现在「对账发现的修复批」等非对账批里，以字样
    当事件会被无关批次静默重置计数 ⇒ 必须认 token，且 token **只在状态列认**（整行 grep 会被
    「描述这个 token 自己」的行命中·W1004 自伤同族）。
  · **max 而非文件序**：台账允许后补登记/让号，低号行可能排在末尾 ⇒ 取 max(W) 而非末行。
  · **归档同扫**：台账按行窗滚动归档到 archive/docs/W批次编号对账表-ARCHIVE.md ⇒ 只读正本
    会让「对账行已归档」退化成「从未对账」假警。判据 = 正本 ∪ 归档 的 token 行取 max。

**为什么只有批数阈值、没有天数阈值**：台账的日期只存在于「认领会话」列，而该列位置不固定
（主题列含裸竖线会整体右移，见 parse_ledger 的 W825 注释）；改从 CHANGELOG 段标题取日期需再
引一个解析面，收益不抵复杂度。项目节拍本就是 W### 批次（可连日数批、也可静默数周），
批数比日历更能反映「又发生了多少改动」——这也是 W1020 滞后的真实成因（W691 一批闭环 5 条
却零回写）。⇒ 单阈值：批数。

只提示不拦截：exit 恒 0；对账动作 = 逐条拿 git 与测试实况核 HANDOVER Backlog，
完成后把 token「Backlog 对账已执行」写进该批台账行的**状态列**。

用法：
  py -3 scripts/check_backlog_review.py            # 打印状态（exit 0）
  py -3 scripts/check_backlog_review.py --self-test
"""
from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import preflight_check as pf  # noqa: E402 — 复用台账路径与行解析

THRESHOLD = 25
ARCHIVE_LEDGER = os.path.join("archive", "docs", "W批次编号对账表-ARCHIVE.md")
TOKEN = "Backlog 对账已执行"   # 事件 token（对账批在状态列登记）
LEGACY_WORD = "Backlog 对账"   # 泛词——只用于「疑似未打标」提示，不计为事件
# 否定词窗口：状态里同时出现这些词时，token 视为**反义用法**（如「已执行（未完成）」），不计事件
_NEGATIONS = ("未完成", "待完成", "中止", "取消", "作废")


def scan_rows(ledger_text):
    """→ (状态列含 token 的 W 号列表, 只含泛词的 W 号列表)。

    token 只在**状态列**认（同 W1004 收口）：整行 grep 会命中「描述这个 token 自己」的行，
    把描述批判成一次对账（静默重置计数 ⇒ 漏警）。
    """
    token_ws, legacy_ws = [], []
    for row in pf.parse_ledger(ledger_text)["rows"]:
        status = row.get("status") or ""
        # W1022 修（审查 P1-3 同族）：**在途行不计事件**——否则写一行「在途（…已执行）」
        # 就能把计数清零，任务中断后再不报警。
        if status.startswith("在途"):
            continue
        # W1022 修（审查 P2-5）：纯子串匹配会被**反义串**骗过——
        # 「Backlog 对账已执行（未完成）」含 token 字样但语义相反，会把一次没做完的对账
        # 计成事件并重置计数。加否定词窗口（同 W1004「字样≠事件」的镜像方向）。
        if TOKEN in status and not any(neg in status for neg in _NEGATIONS):
            token_ws.append(row["w"])
        elif LEGACY_WORD in status:
            legacy_ws.append(row["w"])
    return token_ws, legacy_ws


def last_review_batch(ledger_text):
    """最近一次对账批次 = 含 token 行的最大 W 号；无 → None（max 而非文件序，见模块 docstring）。"""
    token_ws, _legacy = scan_rows(ledger_text)
    return max(token_ws) if token_ws else None


def evaluate(ledger_text, archive_text=""):
    """→ (触发?, 提示行)。纯逻辑入口供单测。archive_text = 归档台账（行窗滚动迁出的旧行）。"""
    max_w = pf.parse_ledger(ledger_text)["max_w"]
    merged = ledger_text + "\n" + (archive_text or "")
    token_ws, legacy_ws = scan_rows(merged)
    last = max(token_ws) if token_ws else None
    suspect = sorted(w for w in legacy_ws if w not in token_ws)
    notes = []
    if suspect:
        notes.append("疑似未打标：W%s 提到「%s」但状态列无 token「%s」——不重置计数；"
                     "若确为对账批请补 token" % ("/W".join(str(w) for w in suspect[-3:]),
                                              LEGACY_WORD, TOKEN))
    if max_w is None:
        return True, ["⚠ Backlog 对账触发器不可判定：台账无 W 行（fail-closed）"] + notes
    if last is None:
        return True, ["⚠ Backlog 对账触发：台账状态列无「%s」登记行（按从未对账处理·fail-closed）"
                      "——逐条拿 git 与测试实况核 HANDOVER Backlog，完成后在状态列补 token" % TOKEN] + notes
    gap = max_w - last
    if gap >= THRESHOLD:
        return True, ["⚠ Backlog 对账触发：距上次对账（W%d）已 %d 批 ≥ %d——HANDOVER Backlog 登记面"
                      "按 41%% 滞后率衰减，建议开一个对账批（判据=git 与测试实况，非条目自述）"
                      % (last, gap, THRESHOLD)] + notes
    return False, ["Backlog 对账触发器：距上次（W%d）%d 批 < %d——未触发" % (last, gap, THRESHOLD)] + notes


def notice_lines():
    """preflight 提示位入口。"""
    try:
        text = open(os.path.join(pf.ROOT, pf.LEDGER), encoding="utf-8", newline="").read()
    except OSError as e:
        return ["⚠ Backlog 对账触发器不可读台账（%s）——fail-closed 按已触发处理" % e]
    try:
        archived = open(os.path.join(pf.ROOT, ARCHIVE_LEDGER), encoding="utf-8", newline="").read()
    except OSError:
        archived = ""   # 归档缺失不阻断：正本判据仍成立，只是少了历史行
    _, lines = evaluate(text, archived)
    return lines


def _row(w, body="常规批", status="已收官"):
    return "| W%d | %s | a | b | %s | s | x |" % (w, body, status)


def _rows(token_at=None, upto=1050, start=1001, extra=None):
    out = []
    for w in range(start, upto + 1):
        status = "已收官（Backlog 对账已执行·12 条移出）" if (token_at and w == token_at) else "已收官"
        out.append(_row(w, status=status))
    if extra:
        out.extend(extra)
    return "\n".join(out)


def _self_test() -> int:
    """十一态自证：阈值两侧 / 不可判定 / 非台账行豁免 / 泛词不重置 / 取 max 不取文件序 /
    归档同扫 / 同批 / 反义串不计 / 在途不计。"""
    fails = []

    # T1 间隔 25 批 → 触发
    ok, lines = evaluate(_rows(token_at=1025, upto=1050, start=1025))
    if not ok or not lines[0].startswith("⚠"):
        fails.append("T1 25 批间隔应触发：%s" % lines[:1])

    # T2 间隔 5 批 → 不触发
    ok2, lines2 = evaluate(_rows(token_at=1020, upto=1025, start=1020))
    if ok2 or not any("未触发" in x for x in lines2):
        fails.append("T2 5 批间隔不应触发：%s" % lines2)

    # T3 空台账 → fail-closed
    if not evaluate("")[0]:
        fails.append("T3 空台账应 fail-closed 触发")

    # T4 散文提及不算登记行 → 仍触发
    if not evaluate("散文里写 Backlog 对账已执行但不是台账行\n" + _row(1005))[0]:
        fails.append("T4 非台账行提及不应计为登记")

    # T5 泛词行不得重置计数（同 W1003 B1）
    ok5, lines5 = evaluate(_rows(token_at=None, upto=1040, start=1001,
                                 extra=[_row(1041, "修对账发现的问题",
                                             "已收官（Backlog 对账修复批·未打 token）")]))
    if not ok5:
        fails.append("T5 泛词行不得重置计数（应触发）")
    if not any("疑似未打标" in x for x in lines5):
        fails.append("T5 应给出「疑似未打标」提示")

    # T6 token 在 W1020、max=1044、末尾追加低号补登记 W1010 → last 取 1020（max 非文件序）。
    # 若按文件序取末行 W1010 ⇒ gap=34 会误触发；正确实现应报「W1020…24 批·未触发」。
    ok6, lines6 = evaluate(_rows(token_at=1020, upto=1044, start=1020,
                                 extra=[_row(1010, "补登记", "已收官（Backlog 对账已执行）")]))
    if ok6 or not any("W1020" in x and "24 批" in x and "未触发" in x for x in lines6):
        fails.append("T6 应报「W1020…24 批·未触发」而非按文件序算 34 批：%s" % lines6)

    # T6b 主题列写 token、状态列没有 → 不算对账（W1004 同族自伤）
    if not evaluate(_row(1005, "触发器改认事件 token「Backlog 对账已执行」"))[0]:
        fails.append("T6b 主题列提及 token 不应计为对账")

    # T7 同批（gap 0）→ 不触发
    if evaluate(_row(1005, status="已收官（Backlog 对账已执行）"))[0]:
        fails.append("T7 同批不应触发")

    # T8 正本无 token、归档有 → 不得退化成「从未对账」
    ok8, lines8 = evaluate(_row(1005),
                           archive_text=_row(990, status="已收官（Backlog 对账已执行）"))
    if ok8 or not any("W990" in x and "未触发" in x for x in lines8):
        fails.append("T8 归档 token 应被计入（不得报「从未对账」）：%s" % lines8)

    # T9（W1022 P2-5 回归）**反义串**含 token 字样但语义相反 → 不得计为事件
    ok9, lines9 = evaluate(_row(1005, status="已收官（Backlog 对账已执行（未完成））"))
    if not ok9:
        fails.append("T9 反义串「已执行（未完成）」不得计为事件（应触发）")

    # T10（W1022 P1-3 同族）在途行写 token → 不计事件（防写一行在途即永久压制）
    ok10, lines10 = evaluate(_row(1005, status="在途（Backlog 对账已执行·对账中）"))
    if not ok10:
        fails.append("T10 在途行不得计为事件（应触发）")

    print()
    if fails:
        print("自测 %d 项不一致：%s" % (len(fails), fails))
        return 1
    print("自测通过：阈值两侧/不可判定/非台账行豁免/泛词不重置/取 max/主题列不算/同批/归档同扫/反义串不计/在途不计 十一态（判据可证伪）")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Backlog 登记面对账触发器（W1021）")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return _self_test()
    for line in notice_lines():
        print(("WARN  " if line.startswith("⚠") else "NOTE  ") + line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
