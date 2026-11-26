"""W1335 单元测试·归档分卷（gen_archive_manifest + archive_tier2 分卷 + check_archive_health T5/T6）。

覆盖：卷宽对齐 / 迁出上界截断 / 卷谱系扫描（冻结标注·同号多卷）/ T5 三档判定
（真缺段 / 台账自述豁免 / 显式豁免簿）/ 清单 --check 过期识别 / T6 总量。

运行：py -m pytest tests/unit/test_w1335_archive_sharding.py -v
"""
from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import archive_tier2 as at2  # noqa: E402
import check_archive_health as cah  # noqa: E402
import gen_archive_manifest as gam  # noqa: E402

CL_SEG = "### W%d（2026-01-01）：第 %d 批\n\n正文若干\n\n"


def test_align_boundary_250():
    """卷宽对齐：起点 951 ⇒ 本卷上界 1000；整数倍边界不跨卷。"""
    assert at2.align_boundary(951, 250) == 1000
    assert at2.align_boundary(1000, 250) == 1000
    assert at2.align_boundary(1001, 250) == 1250
    assert at2.align_boundary(1, 250) == 250
    assert at2.align_boundary(0, 250) == 250  # 目录节（无 W 号）按 1 处理


def test_plan_max_key_truncates():
    """plan(max_key)：迁出上界外的段不得被迁（分卷宽度硬约束）。"""
    text = "# header\n\n" + "".join(CL_SEG % (w, w) for w in (250, 200, 100))
    header, moved, kept = at2.plan(text, at2.re.compile(r"(?m)^### "), "changelog", target=1, max_key=200)
    assert [k for k, _s, _e in moved] == [100, 200], "只应迁到边界 200 为止"
    assert [k for k, _s, _e in kept] == [250]


def test_scan_family_frozen_and_duplicate(tmp_path):
    """卷谱系：冻结卷被标注；同号出现在两卷 ⇒ duplicates 命中。"""
    (tmp_path / "CHANGELOG-ARCHIVE.md").write_text(CL_SEG % (105, 105), encoding="utf-8")
    (tmp_path / "CHANGELOG-ARCHIVE-tier2.md").write_text(CL_SEG % (105, 105), encoding="utf-8")
    (tmp_path / "CHANGELOG-ARCHIVE-tier2-W1-W120.md").write_text(CL_SEG % (99, 99), encoding="utf-8")
    vols, union, dup = gam.scan_family(str(tmp_path), "changelog")
    assert union == {99, 105}
    frozen = {v["file"] for v in vols if v["frozen"]}
    assert frozen == {"CHANGELOG-ARCHIVE-tier2.md"}, "无范围名旧卷必须被标为冻结"
    assert "105" in dup and len(dup["105"]) == 2


def test_t5_three_way_judgement():
    """T5：已收官无段 ⇒ missing；台账自述（作废/合并段）⇒ explained；豁免簿 ⇒ exempt。"""
    fams = {"changelog": {"_union": {10, 11}, "duplicates": {}}}
    rows = {
        10: "| W10 | 甲 | — | — | 已收官 |",
        11: "| W11 | 乙 | — | — | 已收官 |",
        12: "| W12 | 丙 | — | — | 已收官 |",      # 真缺段
        13: "| W13 | 丁 | — | — | 作废 |",        # 自述
        14: "| W14 | 戊 | v2.0（合并段·D1） | — | 已收官 |",  # 自述
        15: "| W15 | 己 | — | — | 已收官 |",      # 显式豁免簿
    }
    res = gam.t5_coverage(fams, rows, exemptions={15: "历史缺口·已核实"})
    assert res["missing"] == [12]
    assert res["explained"] == 2
    assert res["exempt"] == [15]


def test_manifest_check_detects_drift(tmp_path, monkeypatch):
    """清单 --check：盘面变化但清单未刷 ⇒ 判过期（exit 1）。"""
    monkeypatch.setattr(gam, "ARCH", str(tmp_path))
    monkeypatch.setattr(gam, "MANIFEST_JSON", str(tmp_path / "archive-manifest.json"))
    (tmp_path / "CHANGELOG-ARCHIVE.md").write_text(CL_SEG % (5, 5), encoding="utf-8")
    assert gam.refresh() == 0
    assert gam.check() == 0, "刚刷新应当一致"
    (tmp_path / "CHANGELOG-ARCHIVE.md").write_text(
        (CL_SEG % (5, 5)) + (CL_SEG % (4, 4)), encoding="utf-8")
    assert gam.check() == 1, "新增一段但未刷清单 ⇒ 必须判过期"


def test_t6_total_bytes(tmp_path):
    """T6：archive/docs 总量累加（口径=字节）。"""
    (tmp_path / "a.md").write_bytes(b"x" * 100)
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "b.md").write_bytes(b"y" * 50)
    assert cah.t6_arch_docs_total(str(tmp_path)) == 150
    assert cah.ARCH_DOCS_CAP == 12 * 1024 * 1024
