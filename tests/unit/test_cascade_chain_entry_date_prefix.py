"""W1308 单元测试·交接文档「最后更新」链首的日期前缀处理（cascade 链式面）

背景：同号条目**文本变更**时，cascade 的「按批号替换」分支只替换「（W#### …）」括号区间
⇒ 条目左侧的旧日期前缀残留 ⇒ 产出「最后更新：2026-11-232026-11-23（W1308 …）」双日期
⇒ 下游登记面一致性闸的正则「最后更新：<日期>（W####」匹配不上 ⇒ 判红
「HANDOVER 无「最后更新」行」。

运行：py -3 -m pytest tests/unit/test_cascade_chain_entry_date_prefix.py -v
"""
import re
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import batch_cascade as bc  # noqa: E402

CHAIN_HEAD_RE = re.compile(r"最后更新：\d{4}-\d{2}-\d{2}（W\d{4}")


def test_first_insert_puts_new_batch_at_chain_head():
    chain = "2026-11-23（W1307 遗留清偿: L-08 目录件伪血缘治本）·（W1260 及更早批次详见 CHANGELOG.md）"
    entry = "2026-11-23（W1308 收官链 L-11 治本）"
    out, st = bc._upsert_chain_entry(chain, entry, "W1308", "·")
    assert st == "inserted"
    assert out.startswith("2026-11-23（W1308")
    assert CHAIN_HEAD_RE.search("最后更新：" + out)


def test_same_batch_text_change_replaces_date_prefix_too():
    """同号条目文本变更 ⇒ 整段替换（日期前缀一并替换）⇒ 不产双日期。"""
    chain = "2026-11-23（W1308 旧摘要）·2026-11-23（W1307 遗留清偿）·（W1260 及更早批次详见 CHANGELOG.md）"
    entry = "2026-11-23（W1308 新摘要）"
    out, st = bc._upsert_chain_entry(chain, entry, "W1308", "·")
    assert st == "replaced"
    assert "2026-11-232026-11-23" not in out
    assert out.startswith("2026-11-23（W1308 新摘要）·2026-11-23（W1307")


def test_duplicate_date_residue_is_cleaned():
    """既有双日期残留形态 ⇒ 即便条目文本一致也清理（幂等自愈）。"""
    chain = "2026-11-232026-11-23（W1308 摘要）·2026-11-23（W1307 遗留清偿）"
    entry = "2026-11-23（W1308 摘要）"
    out, st = bc._upsert_chain_entry(chain, entry, "W1308", "·")
    assert st == "replaced"
    assert "2026-11-232026-11-23" not in out
    assert out.startswith("2026-11-23（W1308 摘要）·2026-11-23（W1307")
