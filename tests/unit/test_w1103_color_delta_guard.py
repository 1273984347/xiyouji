# -*- coding: utf-8 -*-
"""color_delta_guard.py 判据逻辑测试（W1103·ΔL* 阈值机器判据）。

锁死判据的**纯逻辑口径**（不触浏览器·零真实仓库数据依赖）：

- **ΔL* 锚点用 CIE 标准参考值**（#000000 → L*=0 · #ffffff → L*=100 · #808080 → L*=53.585）
  ⇒ 这些是外部标准常数·**不共用被测实现** ⇒ 实现若算错公式会立刻被独立锚点抓住
  （自检式判据的通病：门禁用同一实现比对 ⇒ 口径漂移不可见·见 E-90 同族纪律）；
- 阈值三档边界必须精确（6 / 12 为实测校准值·边界包含关系固定）；
- 解析器必须覆盖：暗色块覆盖 / 未覆盖 / important 变体 / 大小写；
- BLOCK 档必须被计数并可由退出码表达（负样本：同色对不得误报 BLOCK）。

跨平台纪律：合成 CSS 文本 + 合成色对，零真实仓库数据、零浏览器依赖。
"""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import color_delta_guard as guard  # noqa: E402


# ---------- 色度学锚点（CIE 标准参考值·与实现无关） ----------

def test_lab_anchors_are_standard_values():
    """#000000/#ffffff/#808080 的 L* 是 CIE 标准常数——实现算错公式必被抓住。"""
    assert guard.srgb_to_lab("#000000")[0] == pytest.approx(0.0, abs=0.01)
    assert guard.srgb_to_lab("#ffffff")[0] == pytest.approx(100.0, abs=0.01)
    assert guard.srgb_to_lab("#808080")[0] == pytest.approx(53.585, abs=0.01)


def test_lab_is_gray_achromatic():
    """中性灰的 a*/b* 应接近 0（灰阶不产生色度）。"""
    _l, a, b = guard.srgb_to_lab("#808080")
    assert abs(a) < 0.5
    assert abs(b) < 0.5


def test_delta_l_is_absolute_and_symmetric():
    """ΔL* 取绝对值且对称。"""
    assert guard.delta_l("#c8463a", "#c8463a") == pytest.approx(0.0, abs=1e-9)
    assert guard.delta_l("#3a6b8c", "#7d99a9") == pytest.approx(
        guard.delta_l("#7d99a9", "#3a6b8c"), abs=1e-9)


def test_delta_l_known_pair():
    """已知色对的 ΔL*（暗色补偿 #3a6b8c → #7d99a9 实测 18.4）。"""
    assert guard.delta_l("#3a6b8c", "#7d99a9") == pytest.approx(18.4, abs=0.1)


def test_delta_e76_zero_for_identical_colors():
    """同色 ΔE*76 = 0；异色 > 0。"""
    assert guard.delta_e76("#c8463a", "#c8463a") == pytest.approx(0.0, abs=1e-9)
    assert guard.delta_e76("#c8463a", "#3a6b8c") > 1.0


# ---------- 阈值分档（实测校准值 6 / 12） ----------

def test_default_thresholds_are_calibrated_values():
    """默认阈值必须是实测校准出的 6.0 / 12.0（改值须同步改依据）。"""
    assert guard.DEFAULT_OK == 6.0
    assert guard.DEFAULT_WARN == 12.0


@pytest.mark.parametrize("delta,expected", [
    (0.0, "OK"), (5.6, "OK"), (6.0, "OK"),
    (6.01, "WARN"), (11.9, "WARN"), (12.0, "WARN"),
    (12.01, "BLOCK"), (24.2, "BLOCK"),
])
def test_grade_boundaries(delta, expected):
    """分档边界包含关系固定：OK≤6 · WARN(6,12] · BLOCK>12。"""
    assert guard.grade(delta) == expected


def test_grade_thresholds_are_configurable():
    """阈值可配——自定义阈值后分档随阈值走。"""
    assert guard.grade(8.0, ok=8.0, warn=8.0) == "OK"
    assert guard.grade(8.01, ok=8.0, warn=20.0) == "WARN"
    assert guard.grade(20.01, ok=8.0, warn=20.0) == "BLOCK"


# ---------- brightness 等效 ----------

def test_brightness_hex_known_value():
    """brightness(1.12) 等效色（与浏览器 sRGB 值域乘算口径一致）。"""
    assert guard.brightness_hex("#3a6b8c", 1.12) == "#41789d"


def test_brightness_raises_luminance_and_never_overflows():
    """提亮必然抬高 L*；过曝被夹到 255 不越界。"""
    assert guard.delta_l("#3a6b8c", guard.brightness_hex("#3a6b8c", 1.12)) > 0
    assert guard.brightness_hex("#ffffff", 1.12) == "#ffffff"


def test_brightness_identity_k():
    """k=1 时等效色等于原色（字节级一致）。"""
    assert guard.brightness_hex("#c8463a", 1.0) == "#c8463a"


# ---------- 解析器 ----------

def test_parse_tokens_dark_override():
    """暗色块覆盖浅色令牌；块外令牌不覆盖。"""
    css = ':root{--a:#111111;}html[data-theme="dark"]{--a:#222222;--b:#333333;}'
    light, dark = guard.parse_tokens(css)
    assert light["--a"] == "#111111"
    assert dark["--a"] == "#222222"
    assert dark["--b"] == "#333333"
    assert "--b" not in light


def test_parse_tokens_handles_nested_braces():
    """暗色块内含嵌套 {} 时截取不得越界。"""
    css = ':root{--a:#111111;}html[data-theme="dark"]{--a:#222222;}.x{--z:#444444;}'
    light, dark = guard.parse_tokens(css)
    assert dark["--a"] == "#222222"
    assert "--z" not in dark


def test_parse_literal_comp_variants():
    """字面值型补偿：大小写 i 标记 / important / 多选择器前缀都要命中。"""
    css = ('html[data-theme="dark"] svg [fill="#3a6b8c" i] { fill: #7d99a9; }\n'
           'html[data-theme="dark"] svg [fill="#8c2a2a" i] { fill: #be8880 !important; }\n'
           'html[data-theme="dark"] svg path [fill="#2c5f7c" i] { fill: #7f99a4; }')
    comp = guard.parse_literal_comp(css)
    assert ("#3a6b8c", "#7d99a9") in comp
    assert ("#8c2a2a", "#be8880") in comp
    assert ("#2c5f7c", "#7f99a4") in comp


def test_parse_literal_comp_dedups():
    """同一条补偿在页面内重复出现只取一条。"""
    css = 'svg [fill="#3a6b8c" i] { fill: #7d99a9; }' * 3
    assert len(guard.parse_literal_comp(css)) == 1


def test_parse_prefix_comp_reads_brightness():
    """前缀型补偿的 brightness 系数可解析。"""
    css = 'html[data-theme="dark"] svg path[fill^="#"]{ filter: brightness(1.12) saturate(1.05); }'
    assert guard.parse_prefix_comp(css) == [1.12]


def test_parse_prefix_comp_empty_when_absent():
    """无前缀型补偿时返回空列表（不得臆造系数）。"""
    assert guard.parse_prefix_comp("body{color:red}") == []


# ---------- 色对评估 ----------

def test_eval_pairs_counts_and_flags_block():
    """BLOCK 必须被计数（同色对不得误报 BLOCK）。"""
    pairs = [("同色", "#c8463a", "#c8463a"),
             ("中差", "#c8463a", "#e0604f"),
             ("强补偿", "#3a6b8c", "#7d99a9")]
    rows, summary = guard.eval_pairs(pairs)
    assert summary["total"] == 3
    assert summary["ok"] == 1
    assert summary["warn"] == 1
    assert summary["block"] == 1
    assert rows[0]["grade"] == "OK"
    assert rows[1]["grade"] == "WARN"
    assert rows[2]["grade"] == "BLOCK"


def test_eval_pairs_returns_numeric_readings():
    """每行都带 ΔL* 与 ΔE*76 数值（可机读）。"""
    rows, _summary = guard.eval_pairs([("x", "#c8463a", "#e0604f")])
    assert rows[0]["delta_l"] == pytest.approx(8.6, abs=0.1)
    assert rows[0]["delta_e76"] > 0


# ---------- 输入校验 ----------

def test_hex_to_rgb_rejects_invalid():
    """非法 hex 必须抛 ValueError（不得静默返回黑）。"""
    for bad in ("#zz", "#12345", "notacolor", ""):
        with pytest.raises(ValueError):
            guard.hex_to_rgb(bad)


def test_hex_to_rgb_accepts_short_form():
    """三位 hex 展开为三位字节。"""
    assert guard.hex_to_rgb("#fff") == (255, 255, 255)
    assert guard.hex_to_rgb("#c8463a") == (200, 70, 58)


def test_percentile_empty_is_zero():
    """空序列的百分位返回 0.0（不得抛错）。"""
    assert guard._percentile([], 50) == 0.0
