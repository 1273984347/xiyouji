r"""W1331 专项测试：竖版图表专项（窄屏压缩不可读 / 标签越出视口）

## 为什么测

本批的失效形态是「桌面完好、竖屏悄悄缩成 4px 字」：
- 页面私有 svg 若被后续改造换成新 id/新容器 ⇒ 注入块规则悬空（选择器无对象）；
- 注入块若重复叠加 ⇒ 页面字节膨胀且规则互相覆盖；
- 判据若把「横向可滚」误判为「压缩」⇒ 会把正常图表也强行加宽。
本文件把「判据函数 + 注入幂等 + 真实页锚点」钉成可回归判据。

## 覆盖判据

  G1 build_block：压缩项 → min-width=viewBox 宽（无滚动容器时补 *:has 滚动）
  G2 build_block：越界项 → overflow:visible + 容器可滚
  G3 build_block：无静态 svg id → skipped（不猜选择器）
  G4 真实页抽检：注入块恰一块、规则值与探针账本一致
  G5 grade 判据负样本（压缩 / 越界 / 正常）
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import _w1331_chart_portrait_fix as fix  # noqa: E402
import _w1331_chart_portrait_probe as probe  # noqa: E402
from _w1331_chart_portrait_fix import MARK, build_block  # noqa: E402

FIX = SCRIPTS / "_w1331_chart_portrait_fix.py"

HTML = '<html><head></head><body><svg id="c1" viewBox="0 0 900 400"></svg></body></html>'


def _c(**kw):
    base = {"id": "", "cls": "", "parentCls": "", "vbw": 900, "scale": 1.0, "effFs": 10,
            "scroll": None, "outOfViewport": 0, "outOfSvg": 0, "right": 200}
    base.update(kw)
    return base


def test_build_block_compressed():
    block, applied, skipped = build_block(HTML, {"compressed": [_c(id="c1", scale=0.4, effFs=4.0)],
                                                 "overflow": []})
    assert block and MARK in block
    assert "#c1 { min-width: 900px; }" in block
    assert "*:has(> #c1) { overflow-x: auto; }" in block
    assert not skipped


def test_build_block_scroll_exists_no_extra_scroller():
    block, _, _ = build_block(HTML, {"compressed": [_c(id="c1", scale=0.5, effFs=5.0, scroll="chart-wrap")],
                                     "overflow": []})
    assert "#c1 { min-width: 900px; }" in block
    assert "overflow-x: auto" not in block


def test_build_block_overflow_visible():
    block, applied, _ = build_block(HTML, {"compressed": [],
                                           "overflow": [_c(id="c1", outOfViewport=3)]})
    assert "#c1 { overflow: visible; }" in block
    assert "*:has(> #c1) { overflow-x: auto; }" in block
    assert applied[0]["mode"] == "overflow-visible"


def test_build_block_missing_static_id_is_skipped():
    block, applied, skipped = build_block(HTML, {"compressed": [_c(id="nope", scale=0.4, effFs=4.0)],
                                                 "overflow": []})
    assert block is None
    assert skipped and skipped[0]["why"] == "无可定位选择器"


def test_real_pages_have_exactly_one_block():
    """抽检三类锚点页：压缩类 / 越界类 / 手工锚点，各自注入块恰一块。"""
    pages = ["site/data/journey-route.html", "site/data/magic-system.html",
             "site/data/pilgrim-team-psychology-arc.html", "site/data/text-evolution.html",
             "site/data/graph-explorer.html"]
    for rel in pages:
        t = (ROOT / rel).read_text(encoding="utf-8")
        assert t.count('data-w1331="1"') == 1, rel
        assert MARK in t, rel
        assert re.search(r"min-width: \d+px|overflow: visible", t), rel


def test_real_page_rule_matches_viewbox():
    """journey-route #timeline 的 viewBox 宽 1120 ⇒ 规则必须 1120px。"""
    t = (ROOT / "site/data/journey-route.html").read_text(encoding="utf-8")
    assert "#timeline { min-width: 1120px; }" in t


def test_grade_rules():
    good = {"vw": 375, "overflow": 0, "svgCharts": [_c(id="c1", scroll="chart-wrap")], "canvases": []}
    assert probe.grade(good)[0] == "OK"
    comp = {"vw": 375, "overflow": 0,
            "svgCharts": [_c(id="c1", scale=0.4, effFs=4.0, scroll=None)], "canvases": []}
    g, why = probe.grade(comp)
    assert g == "FAIL" and any("压缩不可读" in w for w in why)
    ovf = {"vw": 375, "overflow": 0,
           "svgCharts": [_c(id="c1", outOfViewport=2, scroll=None)], "canvases": []}
    g2, why2 = probe.grade(ovf)
    assert g2 == "FAIL" and any("越出视口" in w for w in why2)


def test_cli_help_smoke():
    """脚本可执行（覆盖门禁 E3 的 subprocess 形态）。"""
    for script in (FIX, SCRIPTS / "_w1331_chart_portrait_probe.py"):
        r = subprocess.run([sys.executable, str(script), "--help"],
                           capture_output=True, text=True, timeout=60)
        assert r.returncode == 0, script.name
