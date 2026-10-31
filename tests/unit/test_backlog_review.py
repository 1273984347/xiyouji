"""W1021 单元测试·check_backlog_review.py（Backlog 登记面对账触发器）。

起因：W1019 连中两条「已做完却仍挂待办」的 Backlog（BL-29/BL-33），W1020 全量对账实测
**滞后率 41%（12/29）**——衰减是结构性的，故把对账做成「每 ≥25 批机器点名」。

判据与 check_audit_trigger 同族，回归锁沿用同三条铁则：
  · 字样 ≠ 事件：只认状态列的 token「Backlog 对账已执行」，泛词不得重置计数；
  · max 而非文件序：末尾补登记的低号 token 行不得把 last 拉低；
  · 归档同扫：对账行被归档后不得退化成「从未对账」假警。

运行：py -m pytest tests/unit/test_backlog_review.py -v
"""
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import check_backlog_review as cbr  # noqa: E402

TOKEN = cbr.TOKEN


def ledger(token_at=None, start=1001, upto=1050, extra=()):
    """token 只写在**状态列**（位置判定·防主题列自伤）。"""
    rows = []
    for w in range(start, upto + 1):
        status = "已收官（%s·12 条移出）" % TOKEN if w == token_at else "已收官"
        rows.append("| W%d | 常规批 | a | b | %s | s | x |" % (w, status))
    rows.extend(extra)
    return "\n".join(rows)


def test_threshold_triggers_at_25():
    ok, lines = cbr.evaluate(ledger(token_at=1025, start=1025))           # gap 25（边界含）
    assert ok and lines[0].startswith("⚠")
    ok24, lines24 = cbr.evaluate(ledger(token_at=1026, start=1026))       # gap 24
    assert not ok24 and any("未触发" in x for x in lines24)


def test_no_token_is_fail_closed():
    ok, lines = cbr.evaluate(ledger())
    assert ok and any("从未对账" in x for x in lines)
    assert cbr.evaluate("")[0]      # 台账无 W 行亦 fail-closed


def test_generic_wording_does_not_reset():
    """泛词行（对账发现的修复批）不得重置计数——同 W1003 B1 回归。"""
    extra = ["| W1051 | 修对账发现的问题 | a | b | 已收官（Backlog 对账修复批·未打 token） | s | q |"]
    ok, lines = cbr.evaluate(ledger(start=1001, upto=1050) + "\n" + "\n".join(extra))
    assert ok, "泛词行不得重置计数"
    assert any("疑似未打标" in x for x in lines)


def test_token_in_subject_column_not_counted():
    """主题列写 token、状态列没有 ⇒ 不算一次对账（防「描述 token 自己」的行自伤）。"""
    row = "| W1005 | 触发器改认事件 token「%s」 | a | b | 已收官 | s | x |" % TOKEN
    assert cbr.evaluate(row)[0]


def test_last_is_max_not_file_order():
    """token 在 W1020、max=1044、末尾追加低号 W1010 ⇒ last 取 1020（gap 24·未触发）。

    若按文件序取末行 W1010 ⇒ gap 34 会误触发——该误触发即本用例的可证伪点。
    """
    extra = ["| W1010 | 补登记 | a | b | 已收官（%s） | s | z |" % TOKEN]
    ok, lines = cbr.evaluate(ledger(token_at=1020, start=1020, upto=1044) + "\n" + "\n".join(extra))
    assert not ok
    assert any("W1020" in x and "24 批" in x for x in lines)


def test_archive_rows_counted():
    """正本无 token、归档有 ⇒ 判「距上次 W990 未触发」，不得退化成「从未对账」。"""
    ok, lines = cbr.evaluate("| W1005 | 常规批 | a | b | 已收官 | s | x |",
                             archive_text="| W990 | 常规批 | a | b | 已收官（%s） | s | y |" % TOKEN)
    assert not ok
    assert any("W990" in x for x in lines)


def test_same_batch_does_not_trigger():
    row = "| W1005 | 常规批 | a | b | 已收官（%s） | s | x |" % TOKEN
    assert not cbr.evaluate(row)[0]
