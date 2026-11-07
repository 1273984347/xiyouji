"""W1141：数据集溯源校验器挂第 61 槽的回归锁。

锁三条：verify 注册表在位、校验器输出门禁汇总行、治理文档口径一致。
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_gate_registered_in_verify_delivery():
    src = (ROOT / "scripts" / "verify_delivery.py").read_text(encoding="utf-8")
    assert 'script="check_dataset_provenance.py"' in src
    assert '"数据集溯源"' in src
    assert "---- 第 61 门禁 数据集溯源：" in src


def test_validator_prints_gate_summary_line():
    r = subprocess.run(
        [sys.executable, "scripts/check_dataset_provenance.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert r.returncode == 0, r.stdout + r.stderr
    assert "---- 第 61 门禁 数据集溯源：0 FAIL ----" in r.stdout


def test_gate_docs_agree_on_slot_61():
    """W1155 订正：原断言钉死「61 槽」字面（W1149 加 62/63 槽后即过期·N3 同族）——
    改为动态对账：AGENTS §4.2 声明的槽数 == gates.md 编号条目实数。"""
    import re as _re
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    gates = (ROOT / "docs" / "agent" / "gates.md").read_text(encoding="utf-8")
    m = _re.search(r"内含 (\d+) 槽", agents)
    assert m, "AGENTS §4.2 须声明槽数（内含 N 槽）"
    n_agents = int(m.group(1))
    n_gates = len(_re.findall(r"^\d{1,2}\. \*\*", gates, _re.M))
    assert n_agents == n_gates, f"AGENTS 声明 {n_agents} 槽 ≠ gates.md 编号条目 {n_gates}"
    assert "61. **数据集溯源**" in gates
