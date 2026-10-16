"""W761 专项测试：scripts/utils/path_guard.py（W536 路径守卫公共模块）

覆盖判据（每条对应一个真实失效模式）：
  G1 双根常量       → PROJECT_ROOT/SCRIPTS_ROOT 值正确且 SCRIPTS_ROOT 嵌于 PROJECT_ROOT
  G2 仓库根放行     → make_guard(PROJECT_ROOT) 放行仓库内路径并真实写入（自清）
  G3 仓库根拒绝     → 仓外路径 raise SystemExit 且消息文本稳定、零落盘
  G4 scripts 根放行 → make_guard(SCRIPTS_ROOT) 放行 scripts/ 内路径并真实写入（自清）
  G5 scripts 根拒绝 → 仓内但 scripts/ 外路径同样拒绝（双根语义差·钉死防误统一）
  G6 闭包独立性     → 两个不同根的 guard 互不干扰（工厂模式回归）

运行：py -m pytest tests/unit/test_path_guard.py -v
"""
import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from utils.path_guard import PROJECT_ROOT, SCRIPTS_ROOT, make_guard  # noqa: E402


# ------------------------------------------------------------------ G1 双根常量
def test_g1_root_constants():
    assert PROJECT_ROOT == os.path.realpath(str(ROOT)), "PROJECT_ROOT 必须是仓库根"
    assert SCRIPTS_ROOT == os.path.join(PROJECT_ROOT, "scripts"), "SCRIPTS_ROOT 必须是 scripts/ 目录"
    assert SCRIPTS_ROOT.startswith(PROJECT_ROOT + os.sep), "SCRIPTS_ROOT 应嵌于 PROJECT_ROOT"


# -------------------------------------------------------------- G2 仓库根放行
def test_g2_project_root_allows_internal_write():
    probe_dir = Path(PROJECT_ROOT) / "_w761_guard_probe"
    probe_dir.mkdir(exist_ok=True)
    probe = probe_dir / "ok.txt"
    guard = make_guard(PROJECT_ROOT)
    try:
        with guard(str(probe), "w", encoding="utf-8") as f:
            f.write("ok")
        assert probe.read_text(encoding="utf-8") == "ok"
    finally:
        if probe.exists():
            probe.unlink()
        try:
            probe_dir.rmdir()
        except OSError:
            pass


# -------------------------------------------------------------- G3 仓库根拒绝
def test_g3_project_root_blocks_outside(tmp_path):
    outside = tmp_path / "evil.txt"
    guard = make_guard(PROJECT_ROOT)
    with pytest.raises(SystemExit) as ei:
        guard(str(outside), "w", encoding="utf-8")
    assert "W536 guard: path escapes project root" in str(ei.value), "消息文本与历史内联实现逐字一致"
    assert not outside.exists(), "守卫必须拒绝且零落盘"


# ------------------------------------------------------------ G4 scripts 根放行
def test_g4_scripts_root_allows_internal_write():
    probe_dir = Path(SCRIPTS_ROOT) / "output" / "_w761_guard_probe"
    probe_dir.mkdir(parents=True, exist_ok=True)
    probe = probe_dir / "ok.txt"
    guard = make_guard(SCRIPTS_ROOT)
    try:
        with guard(str(probe), "w", encoding="utf-8") as f:
            f.write("ok")
        assert probe.read_text(encoding="utf-8") == "ok"
    finally:
        if probe.exists():
            probe.unlink()
        try:
            probe_dir.rmdir()
        except OSError:
            pass


# ------------------------------------------------------------ G5 scripts 根拒绝
def test_g5_scripts_root_blocks_repo_external_path():
    """仓内但 scripts/ 外（如 docs/）必须被 scripts 根拒绝——双根语义差钉死。"""
    inside_repo_outside_scripts = os.path.join(PROJECT_ROOT, "docs", "_w761_should_not_write.txt")
    guard = make_guard(SCRIPTS_ROOT)
    with pytest.raises(SystemExit) as ei:
        guard(inside_repo_outside_scripts, "w", encoding="utf-8")
    assert "W536 guard" in str(ei.value)
    assert not os.path.exists(inside_repo_outside_scripts)


# ------------------------------------------------------------ G6 闭包独立性
def test_g6_independent_closure_roots(tmp_path):
    """两个不同根的 guard 并存：scripts 根拒仓外、仓库根放行仓内（互不串根）。"""
    scripts_guard = make_guard(SCRIPTS_ROOT)
    repo_guard = make_guard(PROJECT_ROOT)
    outside = tmp_path / "x.txt"
    with pytest.raises(SystemExit):
        scripts_guard(str(outside), "w", encoding="utf-8")
    probe_dir = Path(PROJECT_ROOT) / "_w761_guard_probe"
    probe_dir.mkdir(exist_ok=True)
    probe = probe_dir / "ok.txt"
    try:
        with repo_guard(str(probe), "w", encoding="utf-8") as f:
            f.write("ok")
        assert probe.exists()
    finally:
        if probe.exists():
            probe.unlink()
        try:
            probe_dir.rmdir()
        except OSError:
            pass
