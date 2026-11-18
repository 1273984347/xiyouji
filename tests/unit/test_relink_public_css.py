"""W1274 单元测试·公共层外链化工具（scripts/relink_public_css.py）

背景：全站 867 页把 tokens.css 与 system.css 的合并副本内联在第一个 style 块里
=> 公共层改一次不能全站生效（公共层实际只被 7 页外链引用）。本工具把该块替换为两个 link。

运行：py -3 -m pytest tests/unit/test_relink_public_css.py -v
"""
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import relink_public_css as rlc  # noqa: E402


def test_strip_removes_only_exact_public_rules():
    """只剥离「选择器与声明都与公共层逐字相同」的规则·私有层必须保留。"""
    _idx = {frozenset([".a"]): {"color: red"}}
    _out, _ncut, _nkeep = rlc.strip_public_rules(".a{color: red}\n.b{color: blue}", _idx)
    assert ".b{color: blue}" in _out, "私有层规则必须保留"
    assert ".a{color: red}" not in _out, "公共层规则应被剥离"


def test_strip_keeps_overriding_rules():
    """负样本：同选择器但声明不同（私有层覆写）⇒ 不得剥离。"""
    _idx = {frozenset([".a"]): {"color: red"}}
    _out, _ncut, _nkeep = rlc.strip_public_rules(".a{color: green}", _idx)
    assert _ncut == 0, "覆写版本不得剥离"
    assert ".a{color: green}" in _out


def test_relative_href_by_depth():
    _site = Path(rlc.SITE)
    assert rlc.rel_href(str(_site / "data" / "x.html"), "tokens.css") == "../tokens.css"
    assert rlc.rel_href(str(_site / "reader" / "themes" / "x.html"), "system.css") == "../../system.css"
    assert rlc.rel_href(str(_site / "x.html"), "tokens.css") == "tokens.css"


def test_links_built_in_public_order():
    _site = Path(rlc.SITE)
    _txt = rlc.build_links(str(_site / "reader" / "themes" / "x.html"))
    assert _txt.index("tokens.css") < _txt.index("system.css"), "顺序须与原内联块一致"
    assert _txt.count("<link") == 2
