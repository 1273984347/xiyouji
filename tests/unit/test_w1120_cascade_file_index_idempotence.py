"""W1120 单元测试 · 级联 file-index 面的幂等修复（已立段则不再追加）。

病根（对方 W1121 批实测转交我方）：batch_cascade._face_file_index 此前**无条件**在最新段前
插入 ⇒ 本批号已由补段工具立过段时 ⇒ 插出**同号双段**（CHANGELOG 面有「batch == 顶段+1」
断言挡住 ⇒ 只有 file-index 面漏判）。

修复分层：
  · 本批号已立段且**内容一致** ⇒ 零变化不追加（幂等·可重复执行）
  · 本批号已立段但**内容不一致** ⇒ fail-closed + 指引 scripts/rebuild_section.py 重建
    （不静默留 stale 段·不制造同号双段）

运行：py -3 -m pytest tests/unit/test_w1120_cascade_file_index_idempotence.py -v
"""
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import batch_cascade as bc  # noqa: E402

SPEC = {
    "batch": "W1120",
    "date": "2026-11-04",
    "title": "W1120 测试批",
    "desc": "测试",
    "head_entry": "2026-11-04（W1120 测试批）",
    "head_sentence": "测试",
    "changelog_body": "\n\nbody\n",
    "milestone_block": "- **测试**：内容",
    "agents_note": "2026-11-04（W1120）测试",
    "file_index_rows": ["| a.py | W1120 | 本批工具/产物 |"],
}

HEAD = "## W1120 测试批（2026-11-04）"
SEG = "\n".join([
    HEAD, "", "| 文件 | W | 说明 |", "|---|---|---|",
    "| a.py | W1120 | 本批工具/产物 |", "", "",
])
OLD = "\n".join([
    "## W1119 标题（2026-11-04）", "| a | b |", "", "",
])


def _ctx():
    return bc._Ctx(SPEC)


def test_file_index_face_skips_when_segment_already_identical(monkeypatch):
    """正样本：已立段且内容一致 ⇒ 幂等跳过（ctx.pend 不新增落盘项）。"""
    text = SEG + OLD
    monkeypatch.setattr(bc, "load", lambda p: (text, "\n"))
    ctx = _ctx()
    bc._face_file_index(ctx)
    assert ctx.pend == [], "已立段且内容一致时不得再追加（否则同号双段）"


def test_file_index_face_fails_closed_when_existing_segment_differs(monkeypatch):
    """负样本：已立段但内容不一致 ⇒ fail-closed（拒绝追加并指引重建）。"""
    stale = "\n".join([
        "## W1120 旧标题（2026-11-04）", "", "| 文件 | W | 说明 |", "|---|---|---|",
        "| old.py | W1120 | 旧 |", "", "",
    ])
    monkeypatch.setattr(bc, "load", lambda p: (stale + OLD, "\n"))
    ctx = _ctx()
    with pytest.raises(AssertionError) as exc:
        bc._face_file_index(ctx)
    assert "rebuild_section.py" in str(exc.value), "失败信息须给出重建入口指引"
    assert ctx.pend == []


def test_file_index_face_appends_when_segment_absent(monkeypatch):
    """正样本：本批号未立段 ⇒ 正常追加（既有行为不变）。"""
    monkeypatch.setattr(bc, "load", lambda p: (OLD, "\n"))
    ctx = _ctx()
    bc._face_file_index(ctx)
    assert len(ctx.pend) == 1
    path, content, _nl = ctx.pend[0]
    assert path == "scripts/output/file-index.md"
    assert content.index("## W1120") < content.index("## W1119"), "新段须在最新段之前"
