#!/usr/bin/env python3
"""check_audit_trigger.py — 对抗式审查触发器（W1000 建·与复盘触发器同族的第三哨）。

背景：W998 批的 subagent 对抗式审查（迁移守恒/门禁实跑/代码缺陷全查）一次抓出
P1×2/P2×4——证明「写哨兵的人也需要被哨兵盯」。本触发器把这类审查从「想起来才派」
变成「每 ≥20 批机器点名」。条款与触发点双件套（W824 纪律·防干扰日志断档模式复发）。

判据（单一·台账即事实源）：
  A1 台账**状态列**含事件 token「对抗审查已派发」的认领行，其**最大 W 号**距当前 max(W) ≥ 20 批 → 触发。
  找不到 token 行 → 按「从未审查」处理，直接触发（fail-closed·宁假警不漏警）。
  含泛词「对抗式审查」但**无 token** 的行只出 NOTE（疑似未打标·不重置计数）——W1003 修（B1）。

口径两条铁则（W1003 定）：
  · **字样 ≠ 事件**：泛词会出现在「修复审查发现的问题」「审查常驻化批」等非派发行里，
    以字样当事件会被无关批次**静默重置计数**（漏警实证：41 批未真审仍判未触发）⇒ 必须用 token；
    且 token **只在状态列认**（整行 grep 会被「描述 token 本身」的行命中·W1004 自伤实证）。
  · **max 而非文件序**：台账允许后补登记/让号（W931/W935），低号行可能排在末尾 ⇒
    取文件末条会把 gap 算错（实证：真实 24 批报 28 批）⇒ 取含 token 行的最大 W 号。
  · **归档同扫**（W1008 补 I2）：台账行按 60 行窗滚动归档到
    `archive/docs/W批次编号对账表-ARCHIVE.md` ⇒ 只读正本会让「审查行已归档」被误判成
    「从未审查」（假警）。判据 = 正本 ∪ 归档 的 token 行取 max。

只提示不拦截：exit 恒 0；派发动作 = 会话按 docs/agent/adversarial-audit-prompt.md
模板派发 subagent，登记行须在**状态列**写 token「对抗审查已派发」才被本器认得。

用法：
  py -3 scripts/check_audit_trigger.py            # 打印状态（exit 0）
  py -3 scripts/check_audit_trigger.py --self-test
"""
from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import preflight_check as pf  # noqa: E402 — 复用台账路径与行解析

THRESHOLD = 20
ARCHIVE_LEDGER = os.path.join("archive", "docs", "W批次编号对账表-ARCHIVE.md")
TOKEN = "对抗审查已派发"     # 事件 token（派发会话登记时写入认领行任意格）
LEGACY_WORD = "对抗式审查"   # 泛词——只用于「疑似未打标」提示，不计为事件


def scan_rows(ledger_text):
    """→ (有 token 的 W 号列表, 只含泛词的 W 号列表)。

    **token 只在「状态列」认**（W1004 收口）：整行 grep 会被「描述这个 token 自己」的行命中——
    本批台账行写「触发器改认事件 token『…』」即把自己判成一次派发（实证自伤）。
    状态列是「这批最后怎么样了」的唯一权威格，描述性文字只会出现在主题/摘要列 ⇒ 位置判定。
    """
    token_ws, legacy_ws = [], []
    for row in pf.parse_ledger(ledger_text)["rows"]:
        status = row.get("status") or ""
        # W1022 修（审查 P1-3·fail-open）：**在途行不计事件**。原实现只认 token 字样，
        # 而认领行在派发时就写「在途（对抗审查已派发·审查中）」⇒ 写一行在途登记即可把
        # 本哨清零，审查中断/丢弃后再不报警（实测 W1022 在途行把「W998 已 23 批」压回 0）。
        # 语义：token 标记的是「已派发这一事实」，但**事件完结**才应重置计数。
        if status.startswith("在途"):
            continue
        if TOKEN in status:
            token_ws.append(row["w"])
        elif LEGACY_WORD in status:
            legacy_ws.append(row["w"])
    return token_ws, legacy_ws


def last_audit_batch(ledger_text):
    """最近一次「已派发」事件的批次号 = 含 token 行的**最大 W 号**；无 → None。

    max 而非文件序：台账允许后补登记/让号，低号行可能追加在末尾（W931/W935 明确合法），
    文件序会把 gap 算歪（W1003 B2 实证：真实 24 批报 28 批）。
    """
    token_ws, _legacy = scan_rows(ledger_text)
    return max(token_ws) if token_ws else None


def evaluate(ledger_text, archive_text=""):
    """→ (触发?, 提示行)。纯逻辑入口供单测。

    archive_text：归档台账（行窗滚动迁出的旧行）——与正本合并后取 token max，
    否则「审查行被归档」会退化成「从未审查」假警（W1008 I2）。
    """
    max_w = pf.parse_ledger(ledger_text)["max_w"]
    merged = ledger_text + "\n" + (archive_text or "")
    token_ws, legacy_ws = scan_rows(merged)
    last = max(token_ws) if token_ws else None
    suspect = sorted(w for w in legacy_ws if w not in token_ws)
    notes = []
    if suspect:
        notes.append("疑似未打标：W%s 提到「%s」但无 token「%s」——不重置计数；若确为审查批请补 token"
                     % ("/W".join(str(w) for w in suspect[-3:]), LEGACY_WORD, TOKEN))
    if max_w is None:
        return True, ["⚠ 对抗审查触发器不可判定：台账无 W 行（fail-closed）"] + notes
    if last is None:
        return True, ["⚠ 对抗审查触发：台账无「%s」登记行（按从未审查处理·fail-closed）——按模板派发"
                      "（docs/agent/adversarial-audit-prompt.md）" % TOKEN] + notes
    gap = max_w - last
    if gap >= THRESHOLD:
        return True, ["⚠ 对抗审查触发：距上次对抗审查（W%d·已派发）已 %d 批 ≥ %d"
                      "——按 docs/agent/adversarial-audit-prompt.md 模板派发 subagent，登记行须写 token「%s」"
                      % (last, gap, THRESHOLD, TOKEN)] + notes
    return False, ["对抗审查触发器：距上次（W%d）%d 批 < %d——未触发" % (last, gap, THRESHOLD)] + notes


def notice_lines():
    """preflight 提示位入口。"""
    try:
        text = open(os.path.join(pf.ROOT, pf.LEDGER), encoding="utf-8", newline="").read()
    except OSError as e:
        return ["⚠ 对抗审查触发器不可读台账（%s）——fail-closed 按已触发处理" % e]
    try:
        archived = open(os.path.join(pf.ROOT, ARCHIVE_LEDGER), encoding="utf-8", newline="").read()
    except OSError:
        archived = ""   # 归档缺失不阻断：正本判据仍成立，只是少了历史行
    _, lines = evaluate(text, archived)
    return lines


def _self_test() -> int:
    """七态自证：阈值两侧 / 不可判定 / 散文豁免 / B1 字样不重置 / B2 取 max 不取文件序 / 疑似提示。"""
    fails = []

    def rows(token_at=None, upto=1021, start=1001, extra=None):
        out = []
        for w in range(start, upto + 1):
            body, status = "常规批", "已收官"
            if token_at and w == token_at:
                status = "已收官（对抗审查已派发·subagent 派发 P1×2/P2×4 清偿）"
            out.append("| W%d | %s | a | b | %s | s | x |" % (w, body, status))
        if extra:
            out.extend(extra)
        return "\n".join(out)

    # T1 21 批间隔（token 在 W1000）→ 触发
    ok, lines = evaluate(rows(token_at=1000, start=1000))
    if not ok or not lines[0].startswith("⚠"):
        fails.append("T1 21 批间隔应触发")

    # T2 5 批间隔 → 不触发
    ok5, lines5 = evaluate(rows(token_at=1000, upto=1005, start=1000))
    if ok5 or not any("未触发" in x for x in lines5):
        fails.append("T2 5 批间隔不应触发：%s" % lines5)

    # T3 无台账行 → 不可判定（fail-closed）
    ok3, _ = evaluate("")
    if not ok3:
        fails.append("T3 空台账应 fail-closed 触发")

    # T4 散文提及不算登记行 → 仍触发
    ok4, _ = evaluate("散文里提对抗审查已派发但不是台账行\n| W1005 | 常规批 | a | b | 已收官 | s | x |")
    if not ok4:
        fails.append("T4 非台账行提及不应计为登记")

    # T5（B1 回归）41 批未真审，末行只提泛词「对抗式审查」→ 必须触发（旧实现被静默重置）
    b1 = rows(token_at=None, upto=1040, start=1001,
              extra=["| W1041 | 修 W998 遗留问题 | a | b | 已收官（对抗式审查修复批·未打 token） | s | q |"])
    ok5b, lines5b = evaluate(b1)
    if not ok5b:
        fails.append("T5 B1 回归：泛词行不得重置计数（应触发）")
    if not any("疑似未打标" in x for x in lines5b):
        fails.append("T5 B1 回归：应给出「疑似未打标」提示")

    # T6（B2 回归）token 在 W1000、max=1024、末尾追加低号 token 补登记行 W996 → last 必须取 1000
    b2 = rows(token_at=1000, upto=1024, start=1000,
              extra=["| W996 | 补登记（欠账补齐） | a | b | 已收官（对抗审查已派发） | s | z |"])
    ok6, lines6 = evaluate(b2)
    if not ok6:
        fails.append("T6 B2 回归：24 批应触发")
    elif not any("W1000" in x and "24 批" in x for x in lines6):
        fails.append("T6 B2 回归：应报「W1000…24 批」而非按文件序算 28 批：%s" % lines6)

    # T6b 主题列写 token、状态列没有 → 不算派发（W1004 自伤实证）
    ok6b, lines6b = evaluate("| W1005 | 触发器改认事件 token「对抗审查已派发」 | a | b | 已收官 | s | x |")
    if not ok6b:
        fails.append("T6b 主题列提及 token 不应计为派发（应触发）")

    # T8（I2 回归）正本无 token、归档有 token → 不得退化成「从未审查」
    ok8, lines8 = evaluate("| W1005 | 常规批 | a | b | 已收官 | s | x |",
                           archive_text="| W990 | 常规批 | a | b | 已收官（对抗审查已派发） | s | y |")
    if ok8 or not any("W990" in x and "未触发" in x for x in lines8):
        fails.append("T8 归档 token 应被计入（应判「距上次 W990 未触发」·不得报「从未审查」）：%s" % lines8)

    # T7 当前批等于 token 批（gap 0）→ 不触发
    ok7, _ = evaluate("| W1005 | 常规批 | a | b | 已收官（对抗审查已派发） | s | x |")
    if ok7:
        fails.append("T7 同批派发不应触发")

    # T9（W1022 P1-3 回归·fail-open）在途行即使写了 token 也**不得重置计数**——
    # 原实现只认字样，写一行在途登记即可永久压制本哨（实测把「W998 已 23 批」压回 0）。
    ok9, lines9 = evaluate(rows(token_at=1000, upto=1024, start=1000,
                                extra=["| W1025 | 在途审查 | a | b | 在途（对抗审查已派发·审查中） | s | x |"]))
    if not ok9 or not any("W1000" in y and "25 批" in y for y in lines9):
        fails.append("T9 在途行不得重置计数（应以 W1000 计 25 批触发）：%s" % lines9)

    print()
    if fails:
        print("自测 %d 项不一致：%s" % (len(fails), fails))
        return 1
    print("自测通过：阈值两侧/不可判定/散文豁免/B1 字样不重置/B1b 主题列不算/B2 取 max/归档同扫/同批 八态（判据可证伪）")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="对抗式审查触发器（W1000）")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return _self_test()
    for line in notice_lines():
        print(("WARN  " if line.startswith("⚠") else "NOTE  ") + line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
