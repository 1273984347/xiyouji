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


def test_upsert_chain_entry_inserts_in_batch_order():
    """正样本：本批 entry 不存在 ⇒ 按批号序插入（比链首批次小 ⇒ 插到链首之后）。"""
    chain = "2026-11-04（W1123 新批）·2026-11-04（W1121 旧批）·"
    out, st = bc._upsert_chain_entry(chain, "2026-11-04（W1122 测试批）", "W1122", "·")
    assert st == "inserted"
    assert out.index("（W1123") < out.index("（W1122") < out.index("（W1121"), "低号批 entry 必须排在链首之后"


def test_upsert_chain_entry_moves_entry_off_chain_head():
    """正样本：本批 entry 已占链首而链首更新 ⇒ 重排到按序位（幂等路径的��置校正）。"""
    chain = "2026-11-04（W1122 测试批）·2026-11-04（W1123 新批）·"
    out, st = bc._upsert_chain_entry(chain, "2026-11-04（W1122 测试批）", "W1122", "·")
    assert st == "moved"
    assert out.index("（W1123") < out.index("（W1122"), "低号批 entry 不得占据链首"


def test_upsert_chain_entry_is_idempotent_when_in_place():
    """正样本：本批 entry 已存在且位置正确 ⇒ 零变化（可重复执行）。"""
    chain = "2026-11-04（W1123 新批）·2026-11-04（W1122 测试批）·"
    out, st = bc._upsert_chain_entry(chain, "2026-11-04（W1122 测试批）", "W1122", "·")
    assert st == "unchanged"
    assert out == chain


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


# ---------------- 里程碑块链（按批号序·低号批不得占链首） ----------------
#
# 病根（W1122 批 PR #130 CI 实证）：里程碑块此前**无条件插到链首** ⇒ 低号批（W1122 < 现役
# W1123）占据链首 ⇒ 第 31 门禁 C2「交接文档头链链首 ≡ CHANGELOG 顶段」判红（本地与 CI 同红）。
# 与 AGENTS 脚注条目 / 交接头尾链同族：链式面必须按批号序落位。

HANDOVER_SAMPLE = (
    "# 交接文档\n\n"
    "## 零、当前阻塞\n\n无\n\n"
    "## 一、当前进度（W1123 新描述；更早批次详见 CHANGELOG.md）\n"
    "- **W1123 新批次**：新内容\n"
    "- **W1121 旧批次**：旧内容\n"
    "> 历史概要（W1100 及更早）的详细记录见 CHANGELOG.md\n\n"
    "## 二、下一步方向候选清单\n\n正文不应被吞\n"
)


def _ms_chain(s):
    return [b[0] for b in bc._handover_milestone_blocks(s)]


def test_milestone_insert_places_low_batch_by_number_order():
    """正样本：低号批落段 ⇒ 插到按序位（不得占链首）。"""
    out, st = bc._upsert_handover_milestone(
        HANDOVER_SAMPLE, "- **W1122 测试批**：内容\n", "W1122", "\n")
    assert st == "inserted"
    assert _ms_chain(out) == [1123, 1122, 1121]
    assert out.index("W1123") < out.index("W1122") < out.index("W1121")


def test_milestone_upsert_is_idempotent_on_rerun():
    """正样本：本批块已存在且位置正确 ⇒ 零变化（可重复执行）。"""
    once, _ = bc._upsert_handover_milestone(
        HANDOVER_SAMPLE, "- **W1122 测试批**：内容\n", "W1122", "\n")
    twice, st = bc._upsert_handover_milestone(once, "- **W1122 测试批**：内容\n", "W1122", "\n")
    assert st == "unchanged"
    assert twice == once


def test_milestone_moves_low_batch_off_chain_head():
    """正样本：本批块占链首而链上有更高号 ⇒ 位置校正（第 31 门禁 C2 的根因修复）。"""
    bad = HANDOVER_SAMPLE.replace(
        "- **W1123 新批次**：新内容\n",
        "- **W1122 测试批**：内容\n- **W1123 新批次**：新内容\n")
    out, st = bc._upsert_handover_milestone(bad, "- **W1122 测试批**：内容\n", "W1122", "\n")
    assert st == "moved"
    assert _ms_chain(out) == [1123, 1122, 1121]
    assert out.index("W1123") < out.index("W1122"), "低号批块不得占据链首"


def test_milestone_replace_does_not_swallow_following_section():
    """负样本：链尾块内容不一致 ⇒ 替换区间有界·不得吞掉后续章节与历史概要指针。"""
    bad = HANDOVER_SAMPLE.replace(
        "- **W1121 旧批次**：旧内容\n",
        "- **W1121 旧批次**：旧内容\n- **W1120 更早**：更早内容\n")
    out, st = bc._upsert_handover_milestone(bad, "- **W1120 更早**：新内容\n", "W1120", "\n")
    assert st == "replaced"
    assert "正文不应被吞" in out, "替换区间越界吞掉了后续章节正文"
    assert "> 历史概要" in out, "替换区间越界吞掉了历史概要指针"


# ---------------- 脚注条目区间（条目正文可含分号·不得累积副本） ----------------
#
# 病根（W1122 批 PR #130 工作树实证）：脚注条目终点此前按「下一个『；』」界定 ⇒ **条目正文
# 本身含分号时区间被截断** ⇒ 每次重跑判定「内容不一致」⇒ 替换 ⇒ 残留尾巴 ⇒ 同号条目无限
# 累积（实测脚注里累积到 4 份）。

AGENTS_SAMPLE_SEMICOLON = (
    "# AGENTS\n\n"
    "规则正文。\n\n"
    "*本文件由 AGENTS 维护；2026-11-04（W1122）条目甲；条目乙。；"
    "2026-11-04（W1121）旧条目。如与上述权威文档冲突，以权威文档为准。*\n"
)


def test_agents_note_span_covers_whole_entry_containing_semicolon():
    """正样本：条目正文含分号 ⇒ 定位区间必须覆盖整条（不得在内部分号处截断）。"""
    spans = bc._locate_agents_note(AGENTS_SAMPLE_SEMICOLON, "W1122")
    assert len(spans) == 1
    st, en = spans[0]
    seg = AGENTS_SAMPLE_SEMICOLON[st:en]
    assert "条目甲" in seg and "条目乙" in seg, "条目区间在内部分号处被截断"
    assert "W1121" not in seg


def test_agents_note_span_ignores_batch_mentioned_outside_footnote():
    """正样本：正文提及本批号 ⇒ 不得被误当作脚注条目定位。"""
    s = AGENTS_SAMPLE_SEMICOLON.replace("规则正文。", "规则正文（W1122）。")
    spans = bc._locate_agents_note(s, "W1122")
    assert len(spans) == 1
    st, _en = spans[0]
    assert s[st:].startswith("2026-11-04（W1122）"), "定位到了脚注行之外的提及"


def test_agents_face_collapses_duplicated_entries(monkeypatch):
    """正样本：同号条目重复副本 ⇒ 收敛为唯一一条（旧缺陷曾累积到 4 份）。"""
    dup = AGENTS_SAMPLE.replace(
        "（W1121）旧条目。",
        "（W1121）旧条目；2026-11-04（W1122）测试条目。；2026-11-04（W1122）测试条目。")
    out = _agents_run(monkeypatch, dup)
    assert out.count("（W1122）") == 1, "同号脚注条目重复未收敛"
    assert out.count("测试条目") == 1


def test_agents_face_rerun_does_not_accumulate_entries(monkeypatch):
    """正样本：条目正文含分号时重跑 ⇒ 零变化（不得重复插入）。"""
    once = _agents_run(monkeypatch, AGENTS_SAMPLE_SEMICOLON)
    twice = _agents_run(monkeypatch, once)
    assert twice.count("（W1122）") == 1
    assert twice == once, "含分号条目在重跑后发生累积或改写"
