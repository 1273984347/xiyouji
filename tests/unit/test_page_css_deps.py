"""W1273 单元测试·页面样式表依赖普查（scripts/check_page_css_deps.py）

背景：W1273 做「私有层规则归并进公共层」时，用 grep system.css 判断目标页是否加载公共层
⇒ 被页面注释假命中 ⇒ 对**自包含页**（无 link stylesheet）归并无效 ⇒ 页面样式丢失。

运行：py -3 -m pytest tests/unit/test_page_css_deps.py -v
"""
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import check_page_css_deps as dep  # noqa: E402

Q = chr(34) + chr(39)


def test_link_stylesheet_marks_external():
    assert dep.page_style_deps("<link rel=" + Q + "stylesheet" + Q + " href=" + Q + "a.css" + Q + ">")[0] is True


def test_page_without_link_is_selfcontained():
    assert dep.page_style_deps("<style>a{color:red}</style>")[0] is False


def test_comment_mentioning_system_css_is_not_a_reference():
    """负样本：注释里的 system.css 字样 ≠ 加载公共层（W1273 假命中形态）。"""
    _html = "<style>/* W1251 · 不进 system.css 以免全站 861 页内联重写 */</style>"
    assert dep.page_style_deps(_html)[2] is False


def test_link_attribute_order_does_not_matter():
    """负样本修正：rel 在 href 之后也须识别（W1273 正例1 曾因此失败）。"""
    _html = "<link href=" + Q + "a.css" + Q + " rel=" + Q + "stylesheet" + Q + ">"
    assert dep.page_style_deps(_html)[0] is True


def test_inline_style_blocks_counted():
    assert dep.page_style_deps("<style>a{}</style><style>b{}</style>")[1] == 2
