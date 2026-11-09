"""W1165 回归锁：移动视口探针分级 / 第 64 槽契约解析 / 样式归属不回退。

三层锁：
  1. 探针 grade() 四类判据的分级语义（含「可滚动容器越界不计」与「真裁剪计 WARN」对偶）
  2. 门禁 CSS 解析器的两处自身缺陷形态（多选择器组、注释污染选择器）——这两处若回退，
     门禁会对已落地修复持续误报或静默放行
  3. 仓库现状：system.css 契约齐备、cite-box.js 不再寄生样式
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import check_mobile_viewport as gate  # noqa: E402
from mobile_viewport_probe import grade as probe_grade  # noqa: E402
from mobile_viewport_probe import self_test as probe_self_test  # noqa: E402

# ---- 1. 探针分级语义 ----


def test_probe_grade_ok():
    facts = {"overflow": 0, "offenders": [], "clipped": [], "small44": [], "small24": [], "minFont": 14}
    assert probe_grade(facts, 12)[0] == "OK"


def test_probe_grade_overflow_is_fail():
    facts = {"overflow": 18, "offenders": [], "clipped": [], "small44": [], "small24": [], "minFont": 14}
    grade, why = probe_grade(facts, 12)
    assert grade == "FAIL"
    assert "水平溢出" in why[0]


def test_probe_grade_scrollable_overflow_ignored():
    """落在可横向滚动容器内的越界属移动端表格/图表既定形态——不得计 WARN。"""
    facts = {"overflow": 0, "offenders": [{"tag": "table"}], "clipped": [], "small44": [], "small24": [], "minFont": 14}
    assert probe_grade(facts, 12)[0] == "OK"


def test_probe_grade_clipped_is_warn():
    """无可滚动祖先的越界 = 被裁掉不可达，必须计 WARN。"""
    facts = {"overflow": 0, "offenders": [], "clipped": [{"tag": "div"}], "small44": [], "small24": [], "minFont": 14}
    grade, why = probe_grade(facts, 12)
    assert grade == "WARN"
    assert "裁剪" in why[0]


def test_probe_grade_tap_below_24_is_fail():
    facts = {
        "overflow": 0, "offenders": [], "clipped": [], "small44": [{"w": 30}],
        "small24": [{"w": 18}], "minFont": 14,
    }
    assert probe_grade(facts, 12)[0] == "FAIL"


def test_probe_self_test_passes():
    assert probe_self_test() == 0


def test_probe_cli_self_test_runs():
    """E3 实质执行面（脚本覆盖门禁 W1155 收紧口径）：import 冒烟不算覆盖，
    必须以 `--self-test` 形态真实跑一次子进程并断言退出码。"""
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "mobile_viewport_probe.py"), "--self-test"],
        capture_output=True, text=True, timeout=120,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "自测" in proc.stdout and "通过" in proc.stdout


# ---- 2. 门禁解析器缺陷形态（W1165 两次踩坑的回归锁）----


def test_gate_css_block_multi_selector_group():
    """多选择器组换行书写必须命中——否则 .legend-item[role=button] 永远找不到。"""
    css = '.a { color: red; }\n.legend-item[role="button"],\n.legend-cell[role="button"] {\n  min-height: 44px;\n}\n'
    assert gate.css_block(css, '.legend-item[role="button"]') is not None
    assert "44px" in gate.css_block(css, '.legend-item[role="button"]')


def test_gate_css_block_not_prefix_match():
    """`.site-footer nav` 不得误命中 `.site-footer nav a`。"""
    css = ".site-footer nav a { white-space: nowrap; }\n"
    assert gate.css_block(css, ".site-footer nav") is None


def test_gate_strip_comments_unblocks_selector():
    """注释会被选择器捕获正则吃进选择器文本——strip 后必须能命中。"""
    raw = "/* 说明：折叠标题尺寸 */\n.cite-details summary { min-height: 44px; }\n"
    assert gate.css_block(raw, ".cite-details summary") is None  # 未 strip：选择器被注释污染
    assert gate.css_block(gate.strip_comments(raw), ".cite-details summary") is not None


def test_gate_self_test_passes():
    assert gate.self_test() == 0


# ---- 3. 仓库现状锁 ----


def test_repo_contracts_intact():
    css = gate.strip_comments((ROOT / "site" / "system.css").read_text(encoding="utf-8"))
    js = (ROOT / "site" / "static" / "js" / "cite-box.js").read_text(encoding="utf-8")
    fails = gate.check_static(css, js)
    assert fails == [], f"移动视口契约被回退：{fails}"


def test_cite_box_does_not_inject_style():
    """cite 样式必须在 system.css；JS 重新 createElement('style') 即意味着样式回流寄生。"""
    js = (ROOT / "site" / "static" / "js" / "cite-box.js").read_text(encoding="utf-8")
    assert "createElement('style')" not in js
    assert 'createElement("style")' not in js
