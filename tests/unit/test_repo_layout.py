"""W1011 单元测试·check_repo_layout.py（第 52 门禁：仓库布局）。

背景：用户「对项目的所有文件进行整理分类」——盘点发现真错位 5 个（根临时脚本、
三个空壳目录、入口文档），于是把「哪个目录装什么」变成判据，防三个月后复发。

覆盖：判据 5 例（干净/根文件多出/顶层目录多出/隐藏目录豁免/白名单陈腐）+ 真仓端点契约。

运行：py -m pytest tests/unit/test_repo_layout.py -v
"""
import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import check_repo_layout as crl  # noqa: E402


def test_clean_layout_passes():
    ok, ef, ed, ms = crl.judge(["README.md"], ["docs", "scripts"],
                               {"README.md"}, {"docs", "scripts"}, set())
    assert ok and ef == [] and ed == [] and ms == []


def test_stray_root_file_flagged():
    ok, ef, _, _ = crl.judge(["README.md", "_tmp_x.py"], ["docs"],
                             {"README.md"}, {"docs"}, set())
    assert ok is False and ef == ["_tmp_x.py"]


def test_stray_top_dir_flagged():
    ok, _, ed, _ = crl.judge(["README.md"], ["docs", "junk"],
                             {"README.md"}, {"docs"}, set())
    assert ok is False and ed == ["junk"]


def test_hidden_dirs_exempt():
    ok, _, ed, _ = crl.judge(["README.md"], ["docs", ".git", ".ruff_cache"],
                             {"README.md"}, {"docs"}, set())
    assert ok and ed == []


def test_stale_whitelist_detected():
    """声明了但磁盘不存在 → 进 missing（由 run_gate 判 FAIL·防白名单陈腐）。"""
    _, _, _, ms = crl.judge(["README.md"], ["docs"],
                            {"README.md", "ghost.md"}, {"docs", "ghost"}, set())
    assert ms == ["ghost", "ghost.md"]


def test_real_repo_passes_and_prints_marker():
    """真仓端点：布局应合规，且汇总行必为末行（防静默跳过契约）。"""
    r = subprocess.run([sys.executable, str(SCRIPTS_DIR / "check_repo_layout.py"), "--gate"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
    lines = [x for x in r.stdout.strip().splitlines() if x.strip()]
    assert lines and lines[-1].startswith("---- 第 52 门禁 仓库布局："), lines[-1:]


def test_self_test_cli_passes():
    r = subprocess.run([sys.executable, str(SCRIPTS_DIR / "check_repo_layout.py"), "--self-test"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "5/5" in r.stdout
