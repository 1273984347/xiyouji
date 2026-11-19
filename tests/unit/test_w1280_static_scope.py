"""W1280 单元测试·静态契约判据的判定面随产物形态修订（公共层并入判定面）

背景：公共层外链化后，页内静态契约声明（第 53 槽 chart-tooltip、第 64 槽 A8 窄屏特征）
由公共层提供 ⇒ 判据只看页内文本会把「形态变更」误判为「契约丢失」⇒ EN 138 页全判红。

判据：
  R1 页内提供 ⇒ 满足（内联形态口径不变）
  R2 页内没有但公共层提供（页以 <link> 引用）⇒ 满足（形态变更后的等价形态）
  R3 两边都没有 ⇒ 判红（契约确实丢失）

运行：py -3 -m pytest tests/unit/test_w1280_static_scope.py -v
"""
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from utils.css_public_layer import public_layer_text  # noqa: E402


def test_r1_inline_page_text_counts():
    """R1：页内提供的特征，判定面文本里必须能命中。"""
    html = "<html><head><style>@media (max-width: 640px){.x{overflow-x:auto}}</style></head></html>"
    text = html + public_layer_text(html, str(SCRIPTS_DIR.parent / "site" / "en"))
    assert "overflow-x" in text


def test_r2_external_page_gets_public_layer_text():
    """R2：页以 <link> 引用公共层 ⇒ 公共层文本进入判定面。"""
    html = "<html><head><link rel=\"stylesheet\" href=\"../tokens.css\"></head></html>"
    page_dir = str(SCRIPTS_DIR.parent / "site" / "en")
    text = public_layer_text(html, page_dir)
    assert "tokens.css" in html and text != "", "外链页必须取到公共层文本"


def test_r3_page_without_public_layer_returns_empty():
    """R3：未引用公共层的页 ⇒ 公共层文本为空串（内联形态口径不变）。"""
    html = "<html><head><style>.a{color:red}</style></head></html>"
    assert public_layer_text(html, str(SCRIPTS_DIR.parent / "site" / "en")) == ""
