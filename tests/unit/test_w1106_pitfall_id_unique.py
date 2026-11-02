import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import check_pitfall_id_unique as chk  # noqa: E402


def test_clean_input_no_dup():
    lines = [
        "- **甲**（W1000 实证·E-500）：甲",
        "- **乙**（W1001 实证·E-501）：乙",
    ]
    dups, stock, added = chk.audit("HEAD", lines, added=lines)
    assert dups == []
    assert len(added) == 2


def test_entry_body_only_not_reference():
    """正文里引用别的编号不算本体 ⇒ 不判重号。"""
    lines = [
        "- **甲**（W1000 实证·E-500）：正文提到（W1001 实证·E-501）不算本体",
    ]
    dups, stock, added = chk.audit("HEAD", lines, added=lines)
    assert dups == []
    assert len(added) == 1


def test_stock_duplicates_reported_as_note():
    lines = [
        "- **甲**（W1000 实证·E-500）：甲",
        "- **乙**（W1001 实证·E-500）：乙",
    ]
    dups, stock, added = chk.audit("HEAD", lines, added=[])
    assert dups == []
    assert "E-500" in stock

