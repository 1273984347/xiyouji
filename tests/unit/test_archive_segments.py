"""W960 单元测试·archive_segments.py（版段滚动归档常驻工具·五道守恒断言）。

用合成小文件在 tmpdir 里走完整迁移路径：正/负样本双向锁。
运行：py -m pytest tests/unit/test_archive_segments.py -v
"""
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import archive_segments as ars  # noqa: E402


def _make_tree(tmp_path, n_src=6, n_arc=2, arc_mode="top"):
    """合成正本（n_src 段·降序 Wn..W1）与归档（n_arc 段·降序 W(n+n_arc)..W(n+1)）。"""
    src = "\n".join("### W%03d（2026-10-26）：段%d\n\n正文 %d。\n" % (n_src - i, i, i)
                    for i in range(n_src)) + "\n"
    base = n_src
    arc = "# 归档头\n\n" + "\n".join("### W%03d（2026-09-01）：旧段%d\n\n旧正文 %d。\n"
                                    % (base + n_arc - i, i, i) for i in range(n_arc)) + "\n"
    src_p = tmp_path / "src.md"
    arc_p = tmp_path / "arc.md"
    src_p.write_text(src, encoding="utf-8", newline="")
    arc_p.write_text(arc, encoding="utf-8", newline="")
    return src_p, arc_p


def test_move_conserves_and_appends(tmp_path):
    """正例：迁 3 留 3——切分点与迁移内容正确（move 全流程绑定 ROOT·单测走纯函数层 plan）。"""
    src_p, arc_p = _make_tree(tmp_path, arc_mode="top")
    s = src_p.read_text(encoding="utf-8")
    cut, moved_ws = ars.plan(s, ars.RE_CL_SEG, 3)
    assert moved_ws == [3, 2, 1]  # 6 段留 3：迁出最老三段 W003-W001
    moved_text = s[cut:]
    assert moved_text.startswith("### W003")
    kept = s[:cut]
    assert kept.count("### W") == 3 and "### W006" in kept


def test_plan_rejects_non_descending(tmp_path):
    src_p, _ = _make_tree(tmp_path)
    s = src_p.read_text(encoding="utf-8").replace("### W003", "### W009", 1)
    with pytest.raises(AssertionError, match="降序"):
        ars.plan(s, ars.RE_CL_SEG, 3)


def test_plan_rejects_keep_ge_total(tmp_path):
    """W1042 契约更新（并行 W1014 机制修法的单测同步）：段数恰等于 keep ⇒ **不是失败**。

    病根：W1014（61ea60b5）把 `plan()` 的「段数 == keep ⇒ 断言失败」改成「未超窗 ⇒ 返回
    (None, [])」（未超窗本就是正常状态，断言失败会让级联回窗误报 FAIL），但**配套单测
    仍守旧契约** ⇒ W1014 收官后该用例长期红 ⇒ 全量 pytest 与 CI 阻塞。
    ⇒ 本批把用例改为断言新契约（无迁移 = 正常态），并补 keep > total 的同族形态。
    """
    src_p, _ = _make_tree(tmp_path, n_src=3)
    cut, moved_ws = ars.plan(src_p.read_text(encoding="utf-8"), ars.RE_CL_SEG, 3)
    assert cut is None and moved_ws == [], "未超窗时应返回无迁移（cut=None·moved=[]）"
    # 同族形态：keep 大于总段数 ⇒ 同样是无迁移（不得抛异常）
    cut2, moved2 = ars.plan(src_p.read_text(encoding="utf-8"), ars.RE_CL_SEG, 9)
    assert cut2 is None and moved2 == [], "keep > 总段数时应返回无迁移"


def test_wnum_handles_all_three_forms():
    m = ars.RE_CL_SEG.search("### v2.3.9（2026-08-01）：W900 c")
    assert ars._wnum(m) == 900  # v 前缀形态 group(1)=纯数字（W960 修：禁剥位）
    m2 = ars.RE_CL_SEG.search("### W802（2026-10-22）：x")
    assert ars._wnum(m2) == 802
    m3 = ars.RE_FI_SEG.search("## W958 标题（d）")
    assert ars._wnum(m3) == 958
