"""W1154 回归锁 · run_all.discover_scripts B 类发现器（基础设施审计 §3.5.2-1）。

原缺陷：字典序第一个 .py 会选中 B_人物/__init__.py ⇒ B 类三分析器从未进批量生成，
而站点页面明写「由 run_all.py 批量生成」+ check_data_drift 对无 JSON 页跳过 ⇒ 静默陈旧。

运行：py -3 -m pytest tests/unit/test_w1154_run_all_discovery.py -v
"""
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import run_all  # noqa: E402


def test_b_category_picks_real_analyzer():
    d = dict(run_all.discover_scripts())
    b = d.get("B")
    assert b is not None, "B 类必须被发现"
    assert b.name != "__init__.py", "B 类不得选中 __init__.py"
    assert b.name in ("character_appearance.py", "character_network.py", "character_nlp.py"), b.name


def test_no_category_picks_dunder_or_underscore():
    for cat, p in run_all.discover_scripts():
        assert p.name != "__init__.py", f"{cat} 选中了 __init__.py"
        assert not p.name.startswith("_"), f"{cat} 选中了下划线前缀件 {p.name}"
