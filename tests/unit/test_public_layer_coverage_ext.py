"""W1274 单元测试·公共层覆盖率判据的新维度「实际加载面」（scripts/check_public_layer_coverage.py）

背景：原口径按「类归属」计（11.9%）而实测只有少数页真正加载公共层（W1273 实测 7/875）
=> 指标高估真实接管面。W1274 新增独立维度：外链页占比（实际生效面），旧口径与棘轮不动。

运行：py -3 -m pytest tests/unit/test_public_layer_coverage_ext.py -v
"""
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import check_public_layer_coverage as cov  # noqa: E402


def test_link_pattern_matches_public_css():
    assert cov.RE_LINK_CSS.search('<link rel="stylesheet" href="../system.css">')
    assert cov.RE_LINK_CSS.search('<link rel="stylesheet" href="../../tokens.css">')


def test_link_pattern_ignores_other_css():
    assert not cov.RE_LINK_CSS.search('<link rel="stylesheet" href="style.css">')
    assert not cov.RE_LINK_CSS.search('<script src="system.css"></script>')


def test_ext_ratio_defaults_are_sane():
    """新维度独立棘轮：下限低于实测、目标 100%（铺开完才达成）。"""
    assert 0 < cov.DEFAULT_MIN_EXT_RATIO < 1
    assert cov.DEFAULT_TARGET_EXT_RATIO == 1.0
    assert cov.DEFAULT_MIN_RATIO == 0.118, "旧口径棘轮不得因新增维度而改动"
