"""W994 单元测试·check_archive_health + archive_tier2（归档打磨双件的纯函数判据）。

运行：py -m pytest tests/unit/test_archive_health.py -v
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import archive_tier2 as at2  # noqa: E402
import check_archive_health as cah  # noqa: E402


def test_t1_size_boundaries(tmp_path):
    """1MB 线三态：破线 / 判距预警 / 正常。"""
    for name, kb in (("CHANGELOG-ARCHIVE.md", 1100), ("file-index-ARCHIVE.md", 850), ("AGENTS-ARCHIVE.md", 10)):
        (tmp_path / name).write_bytes(b"x" * (kb * 1024))
    rows = {n: (s, over, warn) for n, s, over, warn in cah.t1_sizes(str(tmp_path))}
    assert rows["CHANGELOG-ARCHIVE.md"][1] is True          # 破线
    assert rows["file-index-ARCHIVE.md"][2] is True         # 预警
    assert rows["AGENTS-ARCHIVE.md"][1] is False            # 正常


def test_t2_coverage_semantics():
    """顶层计数对账 + 子目录/段目录组行覆盖（W994 语义：组行计数而非逐件行）。"""
    tracked = ["archive/scripts/_a.py", "archive/scripts/b.md",
               "archive/scripts/attic/x.py", "archive/scripts/batches/w9xx/_b.py"]
    readme = ("| `archive/scripts/`（顶层存量 +2 件） | … |\n"
              "结构树：archive/scripts/batches/w9xx 组行；目录树含 attic/")
    cov = cah.t2_coverage(tracked, readme)
    assert cov["top_disk"] == 2 and cov["top_row"] == 2      # 计数对账一致
    assert cov["subdirs_missing"] == [] and cov["segs_missing"] == []
    # 计数漂移
    cov2 = cah.t2_coverage(tracked + ["archive/scripts/new.py"], readme)
    assert cov2["top_disk"] == 3 and cov2["top_row"] == 2
    # batches 自身 README/index 不算段名（W994 修：depth≥3 才是段成员）
    cov3 = cah.t2_coverage(tracked + ["archive/scripts/batches/README.md"], readme)
    assert "README.md" not in cov3["segs_missing"]


def test_t2_batches_own_files_not_segments():
    """batches/README.md 与 index.md 是 batches 的门面件——不得判为「段目录缺组行」。"""
    tracked = ["archive/scripts/batches/README.md", "archive/scripts/batches/index.md"]
    cov = cah.t2_coverage(tracked, "x")
    assert cov["segs_missing"] == []


def test_tier2_plan_prefix_cut():
    """tier-2 切分：号序前缀 + 全文字节目标 + A4 键序（ascii 合成·chars==bytes）。"""
    segs = "".join("### W%d (d): t\n\nbody %d\n\n" % (905 + i, i) for i in range(5))
    text = "# header\n\n> chain\n\n" + segs
    header, moved, kept = at2.plan(text, at2.KINDS["changelog"]["block"], "changelog", target=100)
    assert [k for k, _s, _e in moved] == [905, 906]
    assert kept[0][0] == 907
    # span 切除（位置升序）后字节守恒
    body = text[len(header):]
    cut = sorted((s - len(header), e - len(header)) for _k, s, e in moved)
    out, cur = [], 0
    for s, e in cut:
        out.append(body[cur:s])
        cur = e
    out.append(body[cur:])
    assert len("".join(out)) + sum(e - s for _k, s, e in moved) == len(body)


def test_tier2_plan_mixed_layers_key_zero_oldest():
    """file-index 两代混层：目录节（无 W 号）键 0 排最老·先迁。"""
    fx = ("# fx\n\n## site/data/（归档段：v2.0.4）\n\n| a | W031 |\n\n"
          "## W389 后期段\n\n| b | x |\n")
    _h, moved, _k = at2.plan(fx, at2.KINDS["file-index"]["block"], "file-index", target=10)
    assert [k for k, _s, _e in moved] == [0, 389]
