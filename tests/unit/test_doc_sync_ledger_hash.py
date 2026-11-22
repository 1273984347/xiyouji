"""W1306 单元测试·第 31 门禁新增子项（C4-g 台账 hash 历史链有效性 / C4-h 审查 P2 编号化登记）

覆盖：
  - parse_ledger_hash_refs   台账 hash 列定位（相对状态格·主题含竖线仍正确）+ 占位 hash 不算
  - eval_ledger_hash_refs    祖先前缀匹配 + 存量豁免基线（基线内 NOTE / 基线外 FAIL）

运行：py -3 -m pytest tests/unit/test_doc_sync_ledger_hash.py -v
"""
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import check_doc_sync as cds  # noqa: E402

LEDGER_SAMPLE = "\n".join([
    "| W1294 | 某批 | 2dddcfdd1 | W1294 段 | 已收官（x） | mavis | — | 本会话（W1294） | — |",
    "| W1300 | 某批 | 48621ae3a | W1300 段 | 已收官（y） | mavis | — | 本会话（W1300） | — |",
    "| W1305 | 认领中 | —（待回填） | —（待回填） | 在途（认领·未收官） | mavis | — | 本会话（W1305） | — |",
    "| W1306 | 主题含|裸竖线 | 104f54b60 | W1306 段 | 已收官（z） | mavis | — | 本会话（W1306） | — |",
])


def test_parse_ledger_hash_refs():
    refs = dict(cds.parse_ledger_hash_refs(LEDGER_SAMPLE))
    assert refs.get("W1294") == "2dddcfdd1"
    assert refs.get("W1300") == "48621ae3a"
    assert "W1305" not in refs          # 占位 hash（—（待回填））不算引用
    assert refs.get("W1306") == "104f54b60"  # 主题含裸竖线 → 行右移 → hash 仍定位正确


def test_eval_all_ancestors_no_issue():
    anc = {"2dddcfdd1" + "0" * 30, "48621ae3a" + "0" * 30, "104f54b60" + "0" * 30}
    refs = cds.parse_ledger_hash_refs(LEDGER_SAMPLE)
    issues, notes = cds.eval_ledger_hash_refs(refs, anc, set())
    assert issues == []
    assert notes == []


def test_eval_dangling_in_baseline_is_note_only():
    anc = {"48621ae3a" + "0" * 30}          # W1294 的 hash 不在链上
    refs = [("W1294", "2dddcfdd1")]
    issues, notes = cds.eval_ledger_hash_refs(refs, anc, {"W1294"})
    assert issues == [] and len(notes) == 1 and "C4-g" in notes[0]


def test_eval_dangling_outside_baseline_is_fail():
    anc = {"48621ae3a" + "0" * 30}
    refs = [("W1294", "2dddcfdd1")]
    issues, notes = cds.eval_ledger_hash_refs(refs, anc, set())
    assert len(issues) == 1 and "C4-g" in issues[0]


def test_eval_short_hash_prefix_match():
    anc = {"2dddcfdd1" + "0" * 30}
    issues, _notes = cds.eval_ledger_hash_refs([("W1", "2dddcfdd")], anc, set())
    assert issues == []
