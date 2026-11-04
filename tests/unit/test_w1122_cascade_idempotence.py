"""W1122 单元测试 · 级联插入型面的幂等原语（根修 W1117 §6.1 R-01「段插入仍非幂等」）。

病根（W1117 R-01 原文登记）：「级联的**段插入仍非幂等**（段已存在即断言失败）⇒ 落段后无法重跑
级联 ⇒ 本批改走 backfill 补段工具 ⇒ 但『补段后再改段内容』仍需重建该段」。

W1122 根修：抽出**单一事实源**的幂等 upsert 原语（scripts/cascade_idempotence.py）并接入插入型面：
  · 本批条目不存在 ⇒ 插入（既有行为不变）
  · 本批条目已存在且**内容一致** ⇒ **零变化**（可重复执行·不再「静默重复」）
  · 本批条目已存在但**内容不一致** ⇒ **替换**为新内容（落段后可重跑级联修正）

运行：py -3 -m pytest tests/unit/test_w1122_cascade_idempotence.py -v
"""
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import batch_cascade as bc  # noqa: E402
import cascade_idempotence as ci  # noqa: E402
import pytest  # noqa: E402

SPEC = {
    "batch": "W1122",
    "date": "2026-11-04",
    "title": "W1122 测试批",
    "desc": "测试描述",
    "head_entry": "2026-11-04（W1122 测试批）",
    "head_sentence": "测试描述",
    "changelog_body": "\n\n**本批要点**：测试\n\n",
    "milestone_block": "- **W1122 测试批**：内容",
    "agents_note": "2026-11-04（W1122）测试条目",
    "file_index_rows": ["| a.py | W1122 | 本批工具/产物 |"],
}

AGENTS_SAMPLE = (
    "# AGENTS\n\n"
    "规则正文。\n\n"
    "*本文件由 AGENTS 维护；2026-11-04（W1121）旧条目。如与上述权威文档冲突，以权威文档为准。*\n"
)

FOOT_SAMPLE = (
    "<html><body><footer><p>W1121 旧批次 · 更早批次详见 CHANGELOG.md</p>"
    "</footer></body></html>\n"
)

CL_RULE = (
    "**W### 编号规则**：W001-W0900 对应 v0.1-v2.0.72；"
    "W100+ 对应 v2.1.0+（W001-W1121）\n\n"
)

CL_WITH_BATCH = (
    "# 更新日志\n\n" + CL_RULE +
    "### W1122（2026-11-04）：测试批\n\n**本批要点**：测试\n\n\n"
    "### W1121（2026-11-04）：旧标题\n\n旧段正文\n"
)


def _ctx():
    return bc._Ctx(SPEC)


# ---------------- 原语三态 ----------------


def test_upsert_entry_inserts_when_entry_absent():
    """正样本：本批条目不存在 ⇒ 插入（既有行为不变）。"""
    text = "AAA\nBBB\n"
    out, st = ci.upsert_entry(
        text,
        locate=lambda t: ci.locate_entry(t, r"^ZZZ"),
        build=lambda: "ZZZ\n",
        insert_at=lambda t: t.index("BBB"),
    )
    assert st == "inserted"
    assert out == "AAA\nZZZ\nBBB\n"


def test_upsert_entry_keeps_text_when_identical():
    """正样本：本批条目已存在且内容一致 ⇒ 零变化（可重复执行）。"""
    text = "AAA\nZZZ\nBBB\n"
    out, st = ci.upsert_entry(
        text,
        locate=lambda t: ci.locate_entry(t, r"^ZZZ"),
        build=lambda: "ZZZ\n",
        insert_at=lambda t: t.index("BBB"),
    )
    assert st == "unchanged"
    assert out == text


def test_upsert_entry_replaces_when_differs():
    """正样本：本批条目已存在但内容不一致 ⇒ 替换为新内容（重跑级联修正路径）。"""
    text = "AAA\nOLD\nBBB\n"
    out, st = ci.upsert_entry(
        text,
        locate=lambda t: ci.locate_entry(t, r"^OLD"),
        build=lambda: "NEW\n",
        insert_at=lambda t: t.index("BBB"),
    )
    assert st == "replaced"
    assert "OLD" not in out
    assert "NEW" in out


# ---------------- 定位器 ----------------


def test_locate_entry_returns_line_span_without_end_re():
    text = "AAA\nZZZ here\nBBB\n"
    span = ci.locate_entry(text, r"^ZZZ")
    assert span is not None
    s, e = span
    assert text[s:e].strip() == "ZZZ here"


def test_locate_entry_returns_span_upto_end_match():
    text = "AAA\nZZZ one\nZZZ two\nEND\n"
    span = ci.locate_entry(text, r"^ZZZ", r"^END")
    assert span is not None
    s, e = span
    assert "ZZZ one" in text[s:e]
    assert "END" not in text[s:e]


def test_locate_entry_returns_none_when_no_match():
    assert ci.locate_entry("AAA\nBBB\n", r"^ZZZ") is None


def test_locate_handover_milestone_finds_batch_block():
    s = (
        "## 一、当前进度（W1121 旧描述；更早批次详见 CHANGELOG.md）\n"
        "- **W1121 旧批次**：旧内容\n"
        "- **W1122 测试批**：内容\n"
        "- **W1120 更早**：更早内容\n"
    )
    span = bc._locate_handover_milestone(s, "W1122")
    assert span is not None
    st, en = span
    assert "W1122" in s[st:en]
    assert "W1121" not in s[st:en]


def test_locate_handover_milestone_returns_none_for_other_batch():
    s = "## 一、当前进度（W1121 旧描述）\n- **W1121 旧批次**：旧内容\n"
    assert bc._locate_handover_milestone(s, "W1122") is None


def test_locate_cl_section_finds_batch_segment():
    s = "### W1122（2026-11-04）：标题\n\nbody\n\n### W1121（2026-11-04）：旧标题\n\nold\n"
    span = bc._locate_cl_section(s, "W1122")
    assert span is not None
    st, en = span
    assert "W1122" in s[st:en]
    assert "W1121" not in s[st:en]


def test_locate_cl_section_returns_none_for_absent_batch():
    s = "### W1121（2026-11-04）：旧标题\n\nold\n"
    assert bc._locate_cl_section(s, "W1122") is None


# ---------------- 面级端到端（幂等） ----------------


def _agents_run(monkeypatch, sample):
    monkeypatch.setattr(bc, "load", lambda p: (sample, "\n"))
    ctx = _ctx()
    bc._face_agents(ctx)
    return ctx.pend[0][1]


def test_agents_face_inserts_note_when_absent(monkeypatch):
    out = _agents_run(monkeypatch, AGENTS_SAMPLE)
    assert out.count("（W1122）") == 1


def test_agents_face_is_idempotent_on_rerun(monkeypatch):
    once = _agents_run(monkeypatch, AGENTS_SAMPLE)
    twice = _agents_run(monkeypatch, once)
    assert twice.count("（W1122）") == 1, "重跑级联不得重复插入脚注条目（原为静默重复）"
    assert twice == once


AGENTS_SAMPLE_TWO = (
    "# AGENTS\n\n"
    "规则正文。\n\n"
    "*本文件由 AGENTS 维护；2026-11-04（W1121）旧条目；2026-11-04（W1123）新条目。"
    "如与上述权威文档冲突，以权威文档为准。*\n"
)


def test_agents_face_inserts_note_in_batch_order(monkeypatch):
    """正样本：低号批落段时按批号序插入（不得插在末尾）。

    病根：脚注条目按批号**升序**排列（断言 _nums == sorted(_nums)），而原实现恒插在末尾
    ⇒ 低号批（并行让号后的常见形态）落段即触发「脚注条目乱序」断言。
    """
    out = _agents_run(monkeypatch, AGENTS_SAMPLE_TWO)
    assert out.count("（W1122）") == 1
    assert out.index("（W1122）") < out.index("（W1123）"), "低号批条目必须排在高号批之前"


def test_agents_face_replaces_stale_note(monkeypatch):
    stale = AGENTS_SAMPLE.replace(
        "W1121）旧条目", "W1121）旧条目；2026-11-04（W1122）过期条目"
    )
    out = _agents_run(monkeypatch, stale)
    assert out.count("（W1122）") == 1
    assert "过期条目" not in out, "本批脚注条目内容不一致 ⇒ 应替换而非追加"


def _foot_run(monkeypatch, sample):
    monkeypatch.setattr(bc, "load", lambda p: (sample, "\n"))
    ctx = _ctx()
    bc._face_footers(ctx)
    return ctx.pend[0][1]


def test_footers_face_inserts_token_when_absent(monkeypatch):
    out = _foot_run(monkeypatch, FOOT_SAMPLE)
    assert out.count("W1122") == 1


def test_footers_face_is_idempotent_on_rerun(monkeypatch):
    once = _foot_run(monkeypatch, FOOT_SAMPLE)
    twice = _foot_run(monkeypatch, once)
    assert twice.count("W1122") == 1, "重跑级联不得重复插入页脚链 token"
    assert twice == once


# ---------------- CHANGELOG 段面（幂等 + fail-closed） ----------------


def test_changelog_face_is_idempotent_when_segment_exists(monkeypatch):
    """正样本：本批段已存在且内容一致 ⇒ 幂等跳过插入（不产生同号双段）。"""
    monkeypatch.setattr(bc, "load", lambda p: (CL_WITH_BATCH, "\n"))
    ctx = _ctx()
    bc._face_changelog(ctx)
    assert len(ctx.pend) == 1
    _path, out, _nl = ctx.pend[0]
    assert out.count("### W1122（") == 1, "不得插出同号双段"


def test_changelog_face_fails_closed_when_segment_differs(monkeypatch):
    """负样本：本批段已存在但内容不一致 ⇒ fail-closed 并指引 rebuild_section.py 重建。"""
    stale = CL_WITH_BATCH.replace("**本批要点**：测试", "**本批要点**：旧内容")
    monkeypatch.setattr(bc, "load", lambda p: (stale, "\n"))
    ctx = _ctx()
    with pytest.raises(AssertionError) as exc:
        bc._face_changelog(ctx)
    assert "rebuild_section.py" in str(exc.value), "失败信息须给出重建入口指引"
    assert ctx.pend == []


# ---------------- 其余面定位器 ----------------


def test_locate_handover_head_entry_finds_batch_entry():
    s = "> 最后更新：2026-11-04（W1122 测试批）·2026-11-04（W1121 旧批）·\n正文\n"
    span = bc._locate_handover_head_entry(s, "2026-11-04（W1122 测试批）")
    assert span is not None
    st, en = span
    assert "W1122" in s[st:en]
    assert "W1121" not in s[st:en]


def test_locate_workflows_marker_finds_batch_marker():
    s = "头（无 workflow 结构改动）+ W1122 测试描述·无 workflow 结构改动）。\n"
    span = bc._locate_workflows_marker(s, 1122, "测试描述")
    assert span is not None
    st, en = span
    assert "W1122" in s[st:en]
