"""W1273 单元测试·内联 CSS 选择器残渣判据（scripts/check_css_inline_residue.py）

背景：批量归并页面私有层规则进公共层时，脚本切点算错会留下「声明被删、选择器残留」的
孤立选择器行 ⇒ 浏览器容错渲染 ⇒ 探针/门禁全绿而 CSS 已损坏（W1273 实测翻车）。

运行：py -3 -m pytest tests/unit/test_css_inline_residue.py -v
"""
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import check_css_inline_residue as ccir  # noqa: E402


def test_normal_css_has_no_residue():
    assert ccir.find_residue(".a { color: red; }\n.b { margin: 0; }\n") == []


def test_multiline_selector_list_is_not_residue():
    _css = "h1, h2,\n.section-title, .card h2,\n.quick-links h3 { font-family: serif; }\n"
    assert ccir.find_residue(_css) == []


def test_selector_without_declaration_block_is_residue():
    """负样本：声明被删、选择器残留 ⇒ 必须判红（W1273 翻车形态）。"""
    _css = ".silk-hero\n.silk-hero img\nhtml[data-theme=\"dark\"] .silk-hero .silk-hero-dark\n"
    assert ccir.find_residue(_css), "选择器残渣必须被判出"


def test_half_removed_rule_is_residue():
    _css = ".x { color: red; }\n.y, .z\n"
    assert ccir.find_residue(_css), "半截规则必须被判出"


def test_sample_page_has_no_residue():
    """正样本：本批样板页归并后内联 CSS 无残渣（真实仓内文件）。"""
    _p = Path(__file__).resolve().parent.parent.parent / "site" / "reader" / "themes" / "二十八星宿专题.html"
    assert _p.exists(), "样板页缺失"
    assert ccir.scan_file(str(_p)) == [], "样板页不应有选择器残渣"
