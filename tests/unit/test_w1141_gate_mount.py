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
    W1279 地图化二次重锚：声明面 = gates.md H1「N 槽」== 编号条目实数；AGENTS 侧 = 路由行存在。"""
    import re as _re
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    gates = (ROOT / "docs" / "agent" / "gates.md").read_text(encoding="utf-8")
    h1 = gates.split("\n")[0]
    m = _re.search(r"(\d+) 槽", h1)
    assert m, "gates.md H1 须声明槽数（N 槽）"
    n_declaration = int(m.group(1))
    n_gates = len(_re.findall(r"^\d+\. \*\*", gates, _re.M))
    assert n_declaration == n_gates, f"gates.md H1 声明 {n_declaration} 槽 ≠ 编号条目 {n_gates}"
    assert "61. **数据集溯源**" in gates
    assert "docs/agent/gates.md" in agents, "AGENTS 路由表缺 gates.md"
