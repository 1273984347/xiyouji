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


def test_extract_added_skips_inplace_rewrite_pair():
    """W1157 正本迁根根修锁：-旧/+新 同号改写对不得冒充「新增条目」。

    迁移态实测：git mv 后 pathspec 单路径 diff 把整表 292 条全呈 + 行 ⇒ 111 例自撞假红。
    双路径 pathspec（PITFALLS_PATHS）+ 改写对剔除双保险，此锁防二者任一退化。
    """
    diff_edit = (
        "@@ -1,2 +1,2 @@\n"
        "-- **甲**（W1000 实证·E-500）：旧措辞\n"
        "+- **甲**（W1000 实证·E-500）：新措辞\n"
    )
    assert chk._extract_added(diff_edit) == [], "就地改写被误当新增"
    diff_copy = "+- **乙**（W1001 实证·E-500）：复制粘贴重号（原行不动）\n"
    got = chk._extract_added(diff_copy)
    assert len(got) == 1 and "E-500" in got[0], "复制粘贴重号必须保留（W1112/W1155 锁）"
