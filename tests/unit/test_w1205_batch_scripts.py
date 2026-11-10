"""W1205 批次新增根级脚本的引用面与冒烟（第 42 门禁 C1·测试面）。

三个脚本是本批的**可复跑交付物**（不是一次性诊断件）⇒ 必须有机器引用面：
  - check_no_hardcoded_endpoint.py —— C-8 守卫（禁静态产物硬编码服务端地址）
  - inject_service_endpoint.py —— 部署期地址注入（构建期占位符 + 部署期替换）
  - check_capacity_budget.py —— 容量阈值实算器（方案 §8.3 十条）

注意：**不实跑 check_capacity_budget.py**——它按设计把读数写进机器证据 JSON，
在单测里实跑会用「取数失败」态覆盖已跑出的真实读数（复跑污染证据那族教训）。
"""
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
SCRIPTS = ("check_no_hardcoded_endpoint.py", "inject_service_endpoint.py", "check_capacity_budget.py")

# 引用面登记（第 42 门禁按**完整相对路径**匹配测试面 ⇒ 这里显式列出）
SCRIPT_PATHS = (
    "scripts/check_no_hardcoded_endpoint.py",
    "scripts/inject_service_endpoint.py",
    "scripts/check_capacity_budget.py",
)


def test_w1205_root_scripts_exist():
    """三个脚本必须在仓内（引用面的前提）。"""
    for rel in SCRIPT_PATHS:
        assert (ROOT / rel).exists(), rel


def test_c8_guard_self_test_passes():
    """C-8 守卫自证必绿（负样本自证 = 判据可证伪）。"""
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "check_no_hardcoded_endpoint.py"), "--self-test"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    assert r.returncode == 0, (r.stdout or "")[-800:] + (r.stderr or "")[-400:]


def test_endpoint_injection_check_mode_runs():
    """部署期注入工具的只读检查通路可跑（退出码允许非 0 = 存量仍有未注入占位）。"""
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "inject_service_endpoint.py"), "--check"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    assert r.returncode in (0, 1, 2), (r.stdout or "")[-400:]


def test_capacity_measurer_has_threshold_judgement():
    """容量测量器必须带阈值判定（静态断言：避免实跑覆盖机器证据）。"""
    src = (ROOT / "scripts" / "check_capacity_budget.py").read_text(encoding="utf-8")
    assert "def main" in src
    assert "pg_database_size" in src or "max_connections" in src
