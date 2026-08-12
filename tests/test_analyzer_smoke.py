"""W424 M3：A-AH 核心分析脚本冒烟测试（--help 可运行性）。

背景：35 个核心数据脚本此前零直接单测。本文件先以"能否正常进入 argparse"
守护 import 期 / 运行时回归（例如 word_frequency.py 曾因 jieba 在 import 期
崩溃，连 --help 都到不了）。只验证可运行性，不校验数据正确性——
数据正确性由 verify_delivery.py 的数据漂移门禁（scripts/check_data_drift.js）守护。
"""

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"

ANALYZER_SCRIPTS = [
    "A_文本基础/word_frequency.py",
    "A_文本基础/chapter_stats.py",
    "B_人物/character_appearance.py",
    "B_人物/character_network.py",
    "F_时间/timeline.py",
]

jieba_available = importlib.util.find_spec("jieba") is not None


@pytest.mark.parametrize("rel", ANALYZER_SCRIPTS)
def test_analyzer_script_help(rel):
    script = SCRIPTS_DIR / rel
    if rel == "A_文本基础/word_frequency.py" and not jieba_available:
        pytest.skip("jieba 未安装（CI 安装 requirements.txt 后全量运行）")
    r = subprocess.run(
        [sys.executable, str(script), "--help"],
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert r.returncode == 0, f"{rel} --help 失败:\n{r.stderr}"
    assert "usage" in (r.stdout + r.stderr).lower(), f"{rel} 未输出 usage"
