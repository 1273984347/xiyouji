"""W1003 单元测试·check_audit_trigger.py（对抗式审查触发器）。

背景：W1000 建器时台账 W1000 行 touches 声明过本文件但**从未创建**（声明与实物不符，W1002 审查 B-02）。
本批补齐，并把 B1/B2 两条判据缺陷钉成回归：
  · B1（字样≠事件）：末行只提泛词「对抗式审查」不得重置计数（旧实现会静默漏警）；
  · B2（max 而非文件序）：末尾补登记的低号 token 行不得把 last 拉低（旧实现按文件序取末条）。

运行：py -m pytest tests/unit/test_audit_trigger.py -v
"""
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import check_audit_trigger as cat  # noqa: E402

TOKEN = cat.TOKEN


def ledger(token_at=None, start=1001, upto=1021, extra=()):
    """token 只写在**状态列**（第 5 格）——W1004 起的位置判定。"""
    rows = []
    for w in range(start, upto + 1):
        status = "已收官（对抗审查已派发·subagent 派发）" if w == token_at else "已收官"
        rows.append("| W%d | 常规批 | a | b | %s | s | x |" % (w, status))
    rows.extend(extra)
    return "\n".join(rows)


def test_threshold_triggers_at_20():
    ok, lines = cat.evaluate(ledger(token_at=1000, start=1000))          # gap 21
    assert ok and lines[0].startswith("⚠")
    ok20, _ = cat.evaluate(ledger(token_at=1000, start=1000, upto=1020))  # gap 20（边界含）
    assert ok20 is True


def test_under_threshold_silent():
    ok, lines = cat.evaluate(ledger(token_at=1000, start=1000, upto=1005))
    assert ok is False and any("未触发" in x for x in lines)


def test_empty_ledger_fail_closed():
    ok, _ = cat.evaluate("")
    assert ok is True


def test_prose_mention_not_counted():
    ok, _ = cat.evaluate("散文里提 %s 但不是台账行\n| W1005 | 常规批 | a | b | 已收官 | s | x |" % TOKEN)
    assert ok is True


def test_b1_generic_word_does_not_reset_clock():
    """B1 回归：41 批未派发 + 末行只提泛词 → 仍触发，且给出「疑似未打标」提示。"""
    text = ledger(upto=1040, extra=["| W1041 | 修 W998 遗留问题 | a | b | 已收官（对抗式审查修复批·未打 token） | s | q |"])
    ok, lines = cat.evaluate(text)
    assert ok is True
    assert any("疑似未打标" in x for x in lines)


def test_b2_backfilled_lower_row_does_not_shift_last():
    """B2 回归：末尾补登记低号 token 行 → last 取 max（W1000），gap 报 24 而非 28。"""
    text = ledger(token_at=1000, start=1000, upto=1024,
                  extra=["| W996 | 补登记（欠账补齐） | a | b | 已收官（%s） | s | z |" % TOKEN])
    ok, lines = cat.evaluate(text)
    assert ok is True
    assert any("W1000" in x and "24 批" in x for x in lines), lines


def test_same_batch_no_trigger():
    ok, _ = cat.evaluate("| W1005 | 常规批 | a | b | 已收官（%s） | s | x |" % TOKEN)
    assert ok is False


def test_token_in_topic_cell_does_not_count():
    """W1004 自伤回归：主题/摘要列写 token（如台账行描述本机制）不得判为一次派发。"""
    ok, _ = cat.evaluate("| W1005 | 触发器改认事件 token「%s」 | a | b | 已收官 | s | x |" % TOKEN)
    assert ok is True


def test_archive_ledger_token_counts():
    """I2 回归（W1008）：审查行被行窗归档后，判据仍要从归档台账认得它——不得退化成「从未审查」。"""
    ok, lines = cat.evaluate("| W1005 | 常规批 | a | b | 已收官 | s | x |",
                             archive_text="| W990 | 常规批 | a | b | 已收官（%s） | s | y |" % TOKEN)
    assert ok is False, lines
    assert any("W990" in x and "未触发" in x for x in lines), lines


def test_self_test_cli_passes():
    import subprocess
    r = subprocess.run([sys.executable, str(SCRIPTS_DIR / "check_audit_trigger.py"), "--self-test"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
    assert r.returncode == 0, r.stdout + r.stderr
