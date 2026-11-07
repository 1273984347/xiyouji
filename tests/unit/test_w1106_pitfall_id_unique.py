import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import check_pitfall_id_unique as chk  # noqa: E402


def test_clean_input_no_dup():
    # W1155 语义订正：added 必须是**真增量**（生产路径来自基线 diff）——全表传入形态
    # 在「标题豁免」移除后即自身撞号（恰是该豁免掩盖的复制粘贴重复场景）。
    lines = [
        "- **甲**（W1000 实证·E-500）：甲",
        "- **乙**（W1001 实证·E-501）：乙",
    ]
    added = ["- **丙**（W1002 实证·E-502）：丙"]
    dups, stock, a = chk.audit("HEAD", lines, added=added)
    assert dups == []
    assert len(a) == 1


def test_entry_body_only_not_reference():
    """正文里引用别的编号不算本体 ⇒ 不判重号。（W1155：added 改真增量形态）"""
    lines = [
        "- **甲**（W1000 实证·E-500）：正文提到（W1001 实证·E-501）不算本体",
    ]
    added = ["- **丙**（W1002 实证·E-502）：正文提到（W1001 实证·E-501）不算本体"]
    dups, stock, a = chk.audit("HEAD", lines, added=added)
    assert dups == []
    assert len(a) == 1


def test_stock_duplicates_reported_as_note():
    lines = [
        "- **甲**（W1000 实证·E-500）：甲",
        "- **乙**（W1001 实证·E-500）：乙",
    ]
    dups, stock, added = chk.audit("HEAD", lines, added=[])
    assert dups == []
    assert "E-500" in stock

