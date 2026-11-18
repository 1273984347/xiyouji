"""W1276 单元测试·token 覆盖率的「公共层管辖」口径修订（scripts/check_token_coverage.py）

背景（W1276 实测）：公共层外链化后，公共层规则的**页内变体**（声明与原件不同·未被剥离）
留在页内私有块里 ⇒ 该判据按「页私有块裸色」计数时全站每页多计 1 处（实测新增项恒为
`.hero{background:#221D16}`）⇒ 属口径失配而非新增裸色。修法：统计时剔除「与公共层同选择器
且属性交集非空」的规则（口径与 relink 的公共层变体判定同源）。

判据：
  R1 公共层管辖规则（同选择器 + 属性交集非空）⇒ 不计入页私有裸色
  R2 真私有裸色（选择器不命中公共层）⇒ 照旧计入（判定强度不降）
  R3 无豁免注释但仍有私有裸色 ⇒ 判红（负向：防口径修订把门槛放宽成真空）

运行：py -3 -m pytest tests/unit/test_w1276_token_scope.py -v
"""
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import check_token_coverage as ctc  # noqa: E402


def _page(tmp_path, name, css, exempt=None):
    head = "<html><head><style>" + css + "</style></head><body>x</body></html>"
    if exempt is not None:
        head = ("<html><head><style>/* e-track-exempt: chart-data-colors %d 处 */"
                % exempt + css + "</style></head><body>x</body></html>")
    p = tmp_path / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(head, encoding="utf-8")
    return p


def test_r1_public_scope_rule_not_counted(tmp_path):
    """公共层管辖规则（.hero 的 background 属性）⇒ 不计入页私有裸色。"""
    p = _page(tmp_path, "a.html", ".hero{background:#221D16}")
    ui, allowed, _sh, has_ex = ctc.check_page(p)
    assert ui == 0, "公共层管辖规则的裸色不应计入（口径随外链形态修订）"


def test_r2_private_bare_color_still_counted(tmp_path):
    """真私有裸色（.brand 不在公共层）⇒ 照旧计入（判定强度不降）。"""
    p = _page(tmp_path, "b.html", ".brand{background:#221D16}")
    ui, _allowed, _sh, _has = ctc.check_page(p)
    assert ui == 1, "真私有裸色必须照旧计入"


def test_r3_no_exemption_with_private_color_fails(tmp_path, capsys):
    """负向：无豁免注释但有私有裸色 ⇒ 仍判红（口径修订不得把门槛放宽成真空）。"""
    p = _page(tmp_path, "c.html", ".brand{background:#221D16}")
    ui, allowed, _sh, has_ex = ctc.check_page(p)
    assert ui == 1 and allowed == 0 and not has_ex, "该页应落在「无豁免但有裸色」分支"
