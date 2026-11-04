"""W1134 两个交互探针的专项单测（第 42 门禁根级脚本覆盖面 · 四面引用之一）。

覆盖的两个脚本：
- scripts/font_weight_probe.py —— 暗色字重降档取证
- scripts/ime_scroll_probe.py  —— IME 防误发 + 阈值滚动取证

本单测钉住两个探针的**自测结论**（负样本自证必须全绿）：
    探针自带的 --self-test 里每条负样本都刻意构造一个「坏读数」，
    要求判据必须抓住它；若判据被改弱（漏抓），本单测即红。
"""

from __future__ import annotations

import os
import subprocess
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FONT_PROBE = os.path.join(ROOT, "scripts", "font_weight_probe.py")
IME_PROBE = os.path.join(ROOT, "scripts", "ime_scroll_probe.py")


def _run_self_test(script_path):
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    proc = subprocess.run(
        [sys.executable, script_path, "--self-test"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        cwd=ROOT, env=env, timeout=180,
    )
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


@pytest.mark.parametrize("script_path", [FONT_PROBE, IME_PROBE],
                         ids=["font_weight_probe", "ime_scroll_probe"])
def test_probe_self_test_passes(script_path):
    """两个探针的负样本自测必须全绿（判据被改弱即红）。"""
    assert os.path.exists(script_path), "探针文件缺失：%s" % script_path
    code, out = _run_self_test(script_path)
    assert code == 0, "探针自测未通过（%s）：\n%s" % (os.path.basename(script_path), out)
    assert "FAIL" not in out, "探针自测输出含 FAIL：\n%s" % out


def test_font_weight_probe_declares_three_assertions():
    """字重探针必须声明 A1/A2/A3 三条断言（缺一条即判据缺口）。"""
    src = open(FONT_PROBE, encoding="utf-8").read()
    for token in ("A1", "A2", "A3"):
        assert token in src, "字重探针缺断言 %s" % token
    # 数字位槽位必须登记为不得降档
    assert "NUMERIC_SLOTS" in src, "字重探针缺数字位豁免清单"
    assert "BASELINE_CAP" in src, "字重探针缺基准上限表"


def test_ime_probe_declares_guard_and_scroll_cases():
    """IME/滚动探针必须覆盖防误发三态（G1/G2/G3）与滚动三态（G4/G4b/G5）。"""
    src = open(IME_PROBE, encoding="utf-8").read()
    for token in ("G1", "G2", "G3", "G4", "G4b", "G5", "G6"):
        assert token in src, "IME/滚动探针缺用例 %s" % token
    assert "COMPOSITION_GUARD_MS" in src or "500" in src, "探针未覆盖 500ms 拦截窗"
