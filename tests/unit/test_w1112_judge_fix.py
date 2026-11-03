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


def test_same_entry_itself_not_counted_as_duplicate():
    """豁免口径的正向侧：既有条目与新增条目「编号+标题完全相同」⇒ 视为自身 ⇒ 不判红。"""
    line = '- **甲**（W1000 实证·E-500）：甲'
    dups, _stock, _added = chk.audit('HEAD', [line], [line])
    assert not dups, '自身被误判为撞号（豁免口径反向失真）'


def test_resolve_base_returns_usable_ref():
    """基点回退链必须给出可用 ref 与来源说明（公开 API 形态·主会话 #110 后返回二元组）。"""
    ref, source = chk.resolve_base()
    assert isinstance(ref, str) and ref.strip(), '基点 ref 为空'
    assert isinstance(source, str) and source.strip(), '基点来源说明为空'
