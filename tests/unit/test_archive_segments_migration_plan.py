"""W1308 单元测试·治理文档归档腾窗（迁出量最小化 + 两面同下界对齐 + 编号规则段保护）

覆盖：
  - plan_by_size      迁出量 = 「体积刚好达标」的**最小**段数（原实现以 chunk 为固定步长
                       ⇒ 在「正本段数 < chunk + 保留底线」时被迫迁到击穿铁律 22 底线；
                       实测 file-index 正本 50 段·仅超窗 820 B ⇒ 原实现迁 44 段⇒剩 6 段⇒断言红）
  - _rule_seg_index   末尾文件级块内的编号规则串**不构成**迁出禁令（CHANGELOG 假阳性：
                       规则串实际在「## [Unreleased]」块内·该块不随段迁出）
  - plan_align_below  对齐迁出：迁出 W < min_w 的段；迁出块会含编号规则段时 fail-closed
  - 集成               仓内两面正本按体积腾窗后：两面同下界 + 各留 ≥ 20 段（AGENTS 铁律 22）

运行：py -3 -m pytest tests/unit/test_archive_segments_migration_plan.py -v
"""
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import archive_segments as A  # noqa: E402
import batch_cascade as bc  # noqa: E402

MAX_DOC_BYTES = 262144


def _hits(text, re_seg):
    return [(A._wnum(m), m.start()) for m in re_seg.finditer(text)]


def test_plan_by_size_migrates_minimal_segments():
    """迁出 k 段后体积达标，且迁出 k-1 段仍超窗 ⇒ k 即最小达标段数。"""
    re_seg = A.RE_FI_SEG
    body = "x" * 900
    text = "".join("## W%d 标题\n\n%s\n\n" % (w, body) for w in range(1300, 1247, -1))
    cap = len(text.encode("utf-8")) - 1000
    cut, moved = A.plan_by_size(text, re_seg, cap, chunk=50)
    assert moved, "超窗必须有迁出"
    hits = _hits(text, re_seg)
    n = len(hits)
    k = len(moved)
    assert len(text[:hits[n - k][1]].encode("utf-8")) <= cap
    assert len(text[:hits[n - k + 1][1]].encode("utf-8")) > cap


def test_plan_by_size_respects_rule_segment_guard():
    """编号规则段不得被迁出：真禁令（file-index 形态·串在登记行里）⇒ 迁出 fail-closed。"""
    re_seg = A.RE_FI_SEG
    parts = ["## W%d 标题\n\n| a | W%d | 说明 |\n\n" % (w, w) for w in range(1300, 1290, -1)]
    parts.append("## W1289 标题\n\n| CHANGELOG.md | W1289 | 编号规则段推进（W001-W1289） |\n\n")
    text = "".join(parts)
    hits = _hits(text, re_seg)
    assert A._rule_seg_index(hits, text) == len(hits) - 1
    with pytest.raises(AssertionError):
        A.plan_align_below(text, re_seg, 1290)


def test_rule_string_in_tail_block_is_not_a_guard():
    """CHANGELOG 形态：规则串落在末尾文件级块（Unreleased）内 ⇒ 不构成迁出禁令。"""
    re_seg = A.TARGETS["changelog"]["re_seg"]
    text = ("### v1.0（2026-01-01）：W1300\n\n内容\n\n"
            "# 更新日志\n\n## [Unreleased]\n\n"
            "> **W### 编号规则**：每个版本段标注唯一 W### ID（W001-W1300）。\n")
    hits = _hits(text, re_seg)
    assert hits and A._rule_seg_index(hits, text) is None


def test_plan_align_below_moves_strictly_below_min_w():
    re_seg = A.RE_FI_SEG
    text = "".join("## W%d 标题\n\nx\n\n" % w for w in range(1300, 1293, -1))
    cut, moved = A.plan_align_below(text, re_seg, 1296)
    assert moved == [1295, 1294]
    cut, moved = A.plan_align_below(text, re_seg, 1294)
    assert moved == [] and cut is None


def test_repo_faces_align_and_keep_floor():
    """仓内两面正本按体积腾窗后：两面同下界 + 各留 ≥ 20 段（AGENTS 铁律 22）。"""
    faces = ("changelog", "file-index")
    ws_all, plans = {}, {}
    for t in faces:
        s, _nl = bc.load(A.TARGETS[t]["src"])
        ws_all[t] = [A._wnum(m) for m in A.TARGETS[t]["re_seg"].finditer(s)]
        plans[t] = A.plan_by_size(s, A.TARGETS[t]["re_seg"], MAX_DOC_BYTES, 50)
    after = {}
    for t in faces:
        mv = plans[t][1]
        after[t] = A._min_after(ws_all[t], mv) if mv else min(ws_all[t])
    target = max(after.values())
    finals = {}
    for t in faces:
        s, _nl = bc.load(A.TARGETS[t]["src"])
        cut, mv = A.plan_align_below(s, A.TARGETS[t]["re_seg"], target)
        finals[t] = A._min_after(ws_all[t], mv)
        kept = s[:cut] if cut is not None else s
        assert len(A.TARGETS[t]["re_seg"].findall(kept)) >= 20
        assert len(kept.encode("utf-8")) <= MAX_DOC_BYTES
    assert len(set(finals.values())) == 1
