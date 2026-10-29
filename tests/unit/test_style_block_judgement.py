r"""W1022 回归锁：INLINED 副本的识别判据（W1019 治本的承重墙）

## 缺口取证（对抗审查 P1-2）

W1019 把「跳过 INLINED 副本」的判据从「块内含注释文本 `tokens.css —`」改成
「`<!-- INLINED CSS … -->` 标记与紧随 `<style>` 配对」（`utils/gate_common.iter_private_style_blocks`），
理由是注释文本会被任何「剥离 CSS 注释」的动作静默抹掉（实证 228 页误判）。

但改完之后**零回归锁**：全库 `grep -rln "iter_private_style_blocks|INLINED_STYLE_RE|strip_comments" tests/`
命中 0。判据若被后人改回字样识别，228 页静默误判会原样复发且无红灯。

## 判据

  J1 带 INLINED 标记的块**不进**私有块集合；未标记的同页块正常返回
  J2 块内**彻底无 CSS 注释**（strip_comments 之后）仍能识别——这正是旧判据做不到的
  J3 多 style 块 + 带属性 `<style id=…>` 不误配（W1022 审查 P2-4 同源缺陷）
"""
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from inline_css import strip_comments  # noqa: E402
from utils.gate_common import iter_private_style_blocks  # noqa: E402


def _bodies(html):
    return [body for body, _ in iter_private_style_blocks(html)]


def test_j1_marked_block_excluded_unmarked_kept():
    html = (
        '<!-- INLINED CSS (tokens.css + system.css) · 单一事实源: site/tokens.css -->\n'
        '    <style>:root{--a:1}</style>\n'
        '    <style>.private{color:red}</style>'
    )
    bodies = _bodies(html)
    assert len(bodies) == 1, bodies
    assert ".private" in bodies[0]


def test_j2_identified_even_after_comments_stripped():
    """旧判据（靠块内 `tokens.css —` 字样）在此必失败；新判据（标记配对）必通过。"""
    css = strip_comments("/* tokens.css — 这是说明注释 */\n:root{--a:1}")   # 注释被剥掉
    assert "tokens.css" not in css, "前置条件：剥注释后块内已无识别字样"
    html = "<!-- INLINED CSS x --><style>%s</style>" % css
    assert _bodies(html) == []


def test_j3_attributed_style_tags_and_multiple_blocks():
    html = (
        '<style id="audit-halo">.a{}</style>'
        '<!-- INLINED CSS y --><style type="text/css">.b{}</style>'
        '<style>.c{}</style>'
    )
    bodies = _bodies(html)
    assert len(bodies) == 2, bodies
    assert any(".a" in b for b in bodies)
    assert any(".c" in b for b in bodies)
    assert not any(".b" in b for b in bodies), "带属性的 INLINED 块也必须被排除"
