import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))

import check_pitfall_id_unique as chk  # noqa: E402


def test_same_batch_different_title_is_duplicate():
    """豁免只排除「自身」（标题+编号相同）⇒ 同批号不同标题亦判红。"""
    lines = [
        '- **甲**（W1000 实证·E-500）：甲',
        '- **乙**（W1000 实证·E-500）：乙',
    ]
    added = ['- **乙**（W1000 实证·E-500）：乙']
    dups, stock, _ = chk.audit('HEAD', lines, added)
    assert dups, '同批撞号未判红（豁免口径过宽）'


def test_resolve_base_returns_usable_ref():
    """基点回退链必须给出可用 ref（不得为空）。"""
    b = chk._resolve_base('HEAD')
    assert isinstance(b, str) and b.strip()

