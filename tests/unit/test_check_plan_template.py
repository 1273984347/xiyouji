"""test_check_plan_template.py — 第 48 门禁「计划方案合规」单测（纯逻辑面）

包住 scripts/check_plan_template.py 的判据自证：5 例纯逻辑（新增合规 / 新增缺项必红 /
存量缺项不误判 / 新增缺项必红 / 补齐恢复必绿）。git 端到端 2 例（会在 计划方案/ 内造
临时文件）由脚本 `--self-test` 单独跑，不进 pytest——避免 CI 里往仓内写文件。
"""
import importlib.util
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCRIPT = os.path.join(ROOT, "scripts", "check_plan_template.py")

spec = importlib.util.spec_from_file_location("check_plan_template", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def test_pure_logic_self_test_all_pass():
    """纯逻辑 5 例必须全过（判红方向、存量豁免方向、恢复方向三向都锁死）。"""
    assert mod.self_test(include_git=False) == 0


def test_good_sample_is_compliant():
    """合规样本的「不符合项集合」必须为空（判据表本身没把合规样本判红）。"""
    judged = mod.R.judge(mod.GOOD, "执行前计划-TXX.md")
    assert mod.R.fail_set(judged) == set()


def test_bad_sample_has_missing_items():
    """缺项样本必须被判出整项缺失（§5.7/§5.9/附录）。"""
    judged = mod.R.judge(mod.BAD, "执行前计划-TXX.md")
    assert "C22" in mod.R.fail_set(judged)
    assert "C03" in mod.R.fail_set(judged)


def test_gate_marker_is_declared():
    """门禁槽汇总行必须与 verify_delivery 的 marker 完全一致（防挂载后汇总行对不上）。"""
    verify = open(os.path.join(ROOT, "scripts", "verify_delivery.py"), encoding="utf-8").read()
    assert mod.MARKER in verify
    assert 'section="计划方案合规"' in verify
    assert 'script="check_plan_template.py"' in verify
