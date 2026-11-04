"""W1120 单元测试 · 体积第二阈值（字节）+ 幂等段重建独立入口。

覆盖：同源常量一致 / 字节阈值边界 / 缺件 fail-closed / 双阈值独立生效 /
现网在窗内 / 重建幂等（两次⇒零变化）/ 只动本批段 / 未立段降序位插入 / 两面下界对齐。

运行：py -3 -m pytest tests/unit/test_w1120_size_threshold_and_rebuild.py -v
"""
import os
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import backfill_changelog as bf  # noqa: E402
import batch_closeout as bc  # noqa: E402
import check_doc_size_budget as dsb  # noqa: E402
import rebuild_section as rs  # noqa: E402

SPEC = {
    "batch": "W1120",
    "date": "2026-11-04",
    "title": "W1120 测试批",
    "desc": "测试",
    "head_entry": "2026-11-04（W1120 测试批）",
    "head_sentence": "测试",
    "changelog_body": "\n\n**本批要点**：测试内容\n",
    "milestone_block": "- **测试**：内容",
    "agents_note": "2026-11-04（W1120）测试",
    "file_index_rows": ["| a.py | W1120 | 本批工具/产物 |"],
}

CL = "\n".join([
    "### W1119（2026-11-04）：上批",
    "body-1119",
    "",
    "### W1118（2026-11-04）：上上批",
    "body-1118",
    "",
])

FI = "\n".join([
    "## W1119 标题（2026-11-04）",
    "| a | b |",
    "",
    "## W1118 标题（2026-11-04）",
    "| a | b |",
    "",
])


# ---- 体积第二阈值（字节）----

def test_same_source_constant_is_single_fact():
    """门禁侧的字节上限必须与工具侧同源（只引用不复制）——单一事实源锁。"""
    assert dsb.MAX_DOC_BYTES == bc.MAX_DOC_BYTES
    assert dsb.LEDGER_WINDOW == bc.LEDGER_WINDOW
    assert dsb.WINDOWS[os.path.join("docs", "00-导读", "W批次编号对账表.md")] == bc.LEDGER_WINDOW


def test_size_threshold_boundary():
    """字节上限：恰等于放行 / 超 1 字节判红（恰 1 条 C8 + 归档指引）。"""
    cap = dsb.MAX_DOC_BYTES
    at = {rel: cap for rel in dsb.WINDOWS}
    assert dsb.evaluate_sizes(at) == []
    over = dict(at)
    over[list(dsb.WINDOWS)[0]] = cap + 1
    out = dsb.evaluate_sizes(over)
    assert len(out) == 1 and "C8" in out[0] and "archive_segments" in out[0]


def test_size_threshold_missing_fails_closed():
    """体积不可读必须 fail-closed 判红（禁静默跳过）。"""
    assert dsb.evaluate_sizes({}) != []


def test_two_thresholds_are_independent():
    """双阈值独立：段数在窗内但字节超限 ⇒ 仍须判红（先到者为准）。"""
    counts = {rel: 1 for rel in dsb.WINDOWS}
    assert dsb.evaluate(counts) == []
    sizes = {rel: dsb.MAX_DOC_BYTES + 1 for rel in dsb.WINDOWS}
    assert len(dsb.evaluate_sizes(sizes)) == len(dsb.WINDOWS)


def test_real_tree_within_size_budget():
    """现网三面必须在字节窗内（防回退锚）。"""
    sizes, _lines = dsb._collect_sizes()
    for rel, n in sizes.items():
        assert n <= dsb.MAX_DOC_BYTES, "%s 体积 %d 超上限" % (rel, n)


# ---- 幂等段重建独立入口 ----

def test_rebuild_inserts_when_missing():
    """未立段 ⇒ 按降序位插入（不得顶置·顶置会破坏段序不变量）。"""
    cl, changed, action = rs.rebuild_changelog(CL, "W1120", bf.changelog_block(SPEC))
    assert changed is True
    assert "未立段" in action
    assert cl.index("### W1120") < cl.index("### W1119")
    fi, changed, _ = rs.rebuild_file_index(FI, "W1120", bf.file_index_block(SPEC))
    assert changed is True
    assert fi.index("## W1120") < fi.index("## W1119")


def test_rebuild_is_idempotent():
    """幂等核心：首跑插入后二次执行必为零变化且文本逐字节相同。"""
    cl1, ch1, _ = rs.rebuild_changelog(CL, "W1120", bf.changelog_block(SPEC))
    cl2, ch2, act2 = rs.rebuild_changelog(cl1, "W1120", bf.changelog_block(SPEC))
    assert ch1 is True and ch2 is False
    assert cl1 == cl2
    assert "零变化" in act2


def test_rebuild_only_touches_own_segment():
    """只动本批段：历史段逐段内容必须一字不变（禁改历史段）。"""
    cl, _c, _a = rs.rebuild_changelog(CL, "W1120", bf.changelog_block(SPEC))
    ok, diff = rs.history_unchanged(CL, cl, "W1120", "changelog")
    assert ok is True, diff
    fi, _c, _a = rs.rebuild_file_index(FI, "W1120", bf.file_index_block(SPEC))
    ok, diff = rs.history_unchanged(FI, fi, "W1120", "file-index")
    assert ok is True, diff


def test_history_change_is_detected():
    """负样本：历史段被改动必须被抓（断言可证伪）。"""
    cl, _c, _a = rs.rebuild_changelog(CL, "W1120", bf.changelog_block(SPEC))
    tampered = cl.replace("body-1118", "body-1118-TAMPERED")
    ok, diff = rs.history_unchanged(CL, tampered, "W1120", "changelog")
    assert ok is False and 1118 in diff


def test_boundary_check_flags_misalignment():
    """两面下界不一致必须判为不对齐（边界对齐断言可证伪）。"""
    ok, cl_min, fi_min, note = rs.boundary_check(CL, FI)
    assert ok is True and cl_min == fi_min == 1118
    ok2, _a, _b, note2 = rs.boundary_check(CL, "\n".join([
        "## W1119 标题（2026-11-04）", "| a | b |", "",
        "## W1100 标题（2026-11-04）", "| a | b |", "",
    ]))
    assert ok2 is False and "下界不一致" in note2
