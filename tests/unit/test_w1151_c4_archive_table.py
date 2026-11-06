"""W1151 回归锁 · 第 31 门禁 C4 登记面 = 现役台账 ∪ 台账归档表（腾窗互搏根修）。

W1151 实证：W1147 批为满足 C4 重建 W1085 台账行 ⇒ 下批腾窗（W960 窗口纪律）
依法把该行迁进 archive/docs/W批次编号对账表-ARCHIVE.md ⇒ C4 只读现役表 ⇒
已入库提交（747ed75e/26e446a7）信息里的 W1085 变「未登记」假红 2 FAIL。
根修：C4 注册集合读两面（现役表 ∪ 归档表·同 W1145 CHANGELOG 侧同型根修）；
真未登记号两面皆无 ⇒ 仍判红（判据不弱化）。

运行：py -3 -m pytest tests/unit/test_w1151_c4_archive_table.py -v
"""
import re
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import check_doc_sync as cds  # noqa: E402

RE_COMMIT_W = cds.RE_COMMIT_W


def _registered(inp):
    return cds._c4_registered_ws(inp)


def test_w_in_archive_table_counts_as_registered():
    """正样本：W1085 行只在归档表 ⇒ C4 注册集合含 W1085。"""
    inp = {
        "changelog": "### W1149（2026-11-06）：x\n",
        "table": "| W1149 | x | y | z | s | c |\n",
        "archive_changelogs_text": [],
        "archive_tables_text": ["| W1085 | 让号留痕 | — | 已收官 | 会话 | f |\n"],
    }
    reg = _registered(inp)
    assert "1085" in reg, "归档表行须计入注册集合"
    assert "1149" in reg


def test_commit_mentioning_archived_row_w_passes():
    """端到端：提交信息提 W1085（仅归档表有行）⇒ 无 C4 issue。"""
    inp = {
        "changelog": "",
        "table": "",
        "archive_changelogs_text": [],
        "archive_tables_text": ["| W1085 | x | — | 已收官 | s | f |\n"],
    }
    reg = _registered(inp)
    issues = []
    subj = "fix: W1085 让号留痕行恢复（结构损坏由归档取指针行重建）"
    for w in RE_COMMIT_W.findall(subj):
        if w not in reg:
            issues.append(w)
    assert issues == []


def test_unregistered_number_still_red():
    """负样本：真未登记号（两面皆无）⇒ 仍判红（判据不弱化）。"""
    inp = {
        "changelog": "### W1149（2026-11-06）：x\n",
        "table": "| W1149 | x | y | z | s | c |\n",
        "archive_changelogs_text": [],
        "archive_tables_text": ["| W1085 | x | — | 已收官 | s | f |\n"],
    }
    reg = _registered(inp)
    assert "1234" not in reg
    issues = [w for w in RE_COMMIT_W.findall("fix: 修复 W1234 缺陷") if w not in reg]
    assert issues == ["1234"]
