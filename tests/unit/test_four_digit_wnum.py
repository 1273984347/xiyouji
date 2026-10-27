"""W969 单元测试·四位号（W1000+）解析形态——三位号迁移的正向锁。

W964 扫描登记 65 处 W\\d{3} 定时炸弹（W1000 会被错读为 W100），W969 迁移为 W\\d{3,4}。
本文件用合成行锁住关键解析器的四位号行为。
运行：py -m pytest tests/unit/test_four_digit_wnum.py -v
"""
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import preflight_check  # noqa: E402

LEDGER_W1000 = "\n".join([
    "| W968 | 拆分批 | a | b | 已收官 | s | x |",
    "| W1000 | 四位号批 | c | d | 已收官 | s | y |",
    "- **W1000**：现势下一自由号（预留登记豁免）。",
])


def test_parse_ledger_four_digit_row():
    got = preflight_check.parse_ledger(LEDGER_W1000)
    assert got["max_w"] == 1000
    ws = [r["w"] for r in got["rows"]]
    assert ws == [968, 1000]


def test_parse_ledger_four_digit_inflight():
    line = "| W1000 | 四位号在途批 | —（待回填） | —（待回填） | 在途（认领·未收官） | s | a.py |"
    got = preflight_check.parse_ledger(line)
    row = got["rows"][0]
    assert row["w"] == 1000
    assert preflight_check.is_inflight(row["status"])
    assert row["touches"] == {"a.py"}


def test_parse_ledger_no_misread_as_w100():
    """负样本（病根复现）：W1000 不得被三位号正则错读为 W100。"""
    got = preflight_check.parse_ledger(LEDGER_W1000)
    assert 100 not in [r["w"] for r in got["rows"]]


def test_wnum_commit_index_four_digit():
    idx = preflight_check.wnum_commit_index(["abc1234 feat(w1000): 四位号批"])
    assert idx.get(1000) == [1, "abc1234"]
    assert 100 not in idx
