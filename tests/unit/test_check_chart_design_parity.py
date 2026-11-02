"""W1105 专项测试：scripts/check_chart_design_parity.py（第 53 槽 · 图表中英对拍）

## 为什么测这个脚本

chart-design 是同一页的中英两版（site/data/chart-design.html 与 site/en/chart-design.html）。
两页独立演进 ⇒ 数值漂移与强制契约标记（reduced-motion 守卫 / tooltip 统一类名）缺失都
只能靠人工发现。本脚本把二者机器化；它自身若判据失效（逐键对拍漏分支 / 契约标记口径
放宽 / 基础设施缺失时静默放过），整个防护面会静默归零 ⇒ 门禁脚本必须自证。

## 覆盖判据

  P1 现网实跑：退出码 0 且汇总行「0 FAIL」（干净态不假红）
  P2 数值对拍判据：数值不等 ⇒ 检出；非数值（专名）差异 ⇒ 不判红但列出；单侧键 ⇒ 检出
  P3 契约标记判据：中英齐平 ⇒ 通过；一侧缺标记 ⇒ 检出并指明缺哪一侧
  P4 挂载一致性：段名在 EXPECTED_SECTION_NAMES 与门禁元组两侧都在，且相对序一致
  P5 负样本自证：把 EN 侧文本抽掉契约标记后，契约判据必须报缺（防口径放宽致假绿）
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import check_chart_design_parity as par  # noqa: E402

GATE = SCRIPTS / "check_chart_design_parity.py"


def _run(*args, timeout=120):
    return subprocess.run(
        [sys.executable, str(GATE), *args],
        capture_output=True,
        text=True,
        timeout=timeout,
        cwd=str(ROOT),
    )


def test_p1_live_tree_passes():
    """P1：现网实跑 0 FAIL（退出码 0 + 汇总行）。"""
    r = _run()
    assert r.returncode == 0, "第 53 门禁在现网树上 FAIL：\n%s" % (r.stdout[-1200:] + r.stderr[-500:])
    assert "0 FAIL" in r.stdout, "缺汇总行（疑似未真正执行）：\n%s" % r.stdout[-800:]


def test_p2_numeric_parity_detects_drift():
    """P2：数值不等必检出；专名差异不判红；单侧键必检出。"""
    zh = {"a": 1, "b": {"c": 2.5}, "name": "青牛精"}
    en = {"a": 1, "b": {"c": 2.5}, "name": "Green Ox Spirit"}
    num, name, only = par.check_numeric_parity(zh, en)
    assert num == [], "同值数值不应判漂移：%r" % (num,)
    assert len(name) == 1 and "name" in name[0][0], "专名差异应被归入非数值差异：%r" % (name,)
    assert only == []

    num, name, only = par.check_numeric_parity(zh, {"a": 1, "b": {"c": 9.9}, "name": "x"})
    assert len(num) == 1 and num[0][0] == "/b/c", "数值漂移未检出：%r" % (num,)

    num, name, only = par.check_numeric_parity(zh, {"a": 1})
    assert only, "单侧键未检出：%r" % (only,)


def test_p3_contract_marks_require_both_sides():
    """P3：契约标记中英齐平才通过；一侧缺 ⇒ 检出并指明缺侧。"""
    zh = "MOYUN_RM chart-tooltip prefers-reduced-motion"
    assert par.check_contract_marks(zh, zh) == [], "双侧齐平不应报缺"

    missing = par.check_contract_marks(zh, "chart-tooltip prefers-reduced-motion")
    assert len(missing) == 1
    mark, side, _desc = missing[0]
    assert mark == "MOYUN_RM" and side == "EN", "缺侧判定错误：%r" % (missing,)

    missing = par.check_contract_marks("chart-tooltip", zh)
    assert len(missing) == 2, "ZH 侧缺两项应报两项：%r" % (missing,)
    assert all(side == "ZH" for _m, side, _d in missing)


def test_p4_mount_consistency():
    """P4：挂槽一致性——段名两侧都在 + 相对序一致（第 41 门禁 C2 同款对账）。"""
    sys.path.insert(0, str(SCRIPTS))
    import verify_delivery as v  # noqa: E402

    assert "图表中英对拍" in v.EXPECTED_SECTION_NAMES, "段名未入 EXPECTED_SECTION_NAMES"
    sections = [g.section for g in v._STRICT_GATES]
    assert "图表中英对拍" in sections, "段名未入门禁元组"
    assert [n for n in v.EXPECTED_SECTION_NAMES if n in set(sections)] == sections, "相对序不一致"
    scripts = [g.script for g in v._STRICT_GATES]
    assert "check_chart_design_parity.py" in scripts, "脚本未挂载到门禁元组"


def test_p5_negative_sample_contract_mark_removed():
    """P5：负样本自证——抽掉 EN 侧契约标记后判据必须报缺（防口径放宽致假绿）。"""
    zh = "MOYUN_RM chart-tooltip prefers-reduced-motion"
    en_full = "MOYUN_RM chart-tooltip prefers-reduced-motion"
    assert par.check_contract_marks(zh, en_full) == []

    en_broken = en_full.replace("MOYUN_RM", "")
    missing = par.check_contract_marks(zh, en_broken)
    assert len(missing) == 1 and missing[0][0] == "MOYUN_RM", "负样本未被检出：%r" % (missing,)


def test_p6_walk_flattens_nested_structures():
    """P6：_walk 把嵌套 dict/list 摊平成点分路径（逐键对拍的前提）。"""
    obj = {"x": 1, "y": {"z": [10, 20]}}
    flat = dict(par._walk(obj))
    assert flat["/x"] == 1
    assert flat["/y/z/0"] == 10
    assert flat["/y/z/1"] == 20
