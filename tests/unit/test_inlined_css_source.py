"""W1274 单元测试·页面样式来源门禁（scripts/check_inlined_css.py）

背景：批三走 A 方案（公共层外链化）后，「INLINED 块 ≥ 20KB」这一形态判据会在外链化
页面误判 ⇒ 口径改为二选一：内联形态保留原判据；外链形态校验两个公共层 link 齐全且
目标文件真实存在（相对页目录解析）⇒ 相对路径写错即判红。

运行：py -3 -m pytest tests/unit/test_inlined_css_source.py -v
"""
import os
import sys
import tempfile
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import check_inlined_css as cic  # noqa: E402


def _mkpage(html):
    _d = tempfile.mkdtemp(prefix="src_")
    _data = os.path.join(_d, "site", "data")
    os.makedirs(_data)
    _p = os.path.join(_data, "t.html")
    with open(_p, "w", encoding="utf-8") as fh:
        fh.write(html)
    return _d, _p


def test_external_links_with_existing_targets_pass():
    _d, _p = _mkpage('<link rel="stylesheet" href="../../tokens.css">\n'
                     '<link rel="stylesheet" href="../../system.css">')
    for _n in ("tokens.css", "system.css"):
        with open(os.path.join(_d, _n), "w", encoding="utf-8") as fh:
            fh.write("x")
    _ok, _why, _kind = cic.judge_page(open(_p, encoding="utf-8").read(), _p)
    assert _ok is True, "两个公共层外链齐全且目标存在时应判过"
    assert _kind == "external"


def test_external_link_missing_target_fails():
    _d, _p = _mkpage('<link rel="stylesheet" href="../../tokens.css">\n'
                     '<link rel="stylesheet" href="../../gone.css">')
    for _n in ("tokens.css", "system.css"):
        with open(os.path.join(_d, _n), "w", encoding="utf-8") as fh:
            fh.write("x")
    _ok, _why, _kind = cic.judge_page(open(_p, encoding="utf-8").read(), _p)
    assert _ok is False, "外链目标缺失必须判红（样式会整体失效）"


def test_incomplete_external_pair_fails():
    _d, _p = _mkpage('<link rel="stylesheet" href="../../tokens.css">')
    with open(os.path.join(_d, "tokens.css"), "w", encoding="utf-8") as fh:
        fh.write("x")
    _ok, _why, _kind = cic.judge_page(open(_p, encoding="utf-8").read(), _p)
    assert _ok is False, "只链 tokens 不链 system 应判红"
