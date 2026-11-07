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
    """W1155 语义订正（深度审计 #56）：原「编号+标题相同视为自身」豁免正是复制粘贴
    重复条目（同号同标题）永不检出的漏洞本体。新语义：added 是真增量（生产路径来自
    基线 diff，与 existing 无交集）⇒ 不判红；同号（含同标题）即红。"""
    existing = ['- **甲**（W1000 实证·E-500）：甲']
    added = ['- **乙**（W1001 实证·E-501）：乙']
    dups, _stock, _added = chk.audit('HEAD', existing, added)
    assert not dups, '真增量被误判撞号'
    copy_line = '- **甲**（W1001 实证·E-500）：甲'
    dups2, _s2, _a2 = chk.audit('HEAD', existing, [copy_line])
    assert dups2, '同号复制粘贴形态必须判红（56 修复本体）'


def test_resolve_base_returns_usable_ref():
    """基点回退链必须给出可用 ref 与来源说明（公开 API 形态·主会话 #110 后返回二元组）。"""
    ref, source = chk.resolve_base()
    assert isinstance(ref, str) and ref.strip(), '基点 ref 为空'
    assert isinstance(source, str) and source.strip(), '基点来源说明为空'
