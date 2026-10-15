r"""W751 专项测试：scripts/check_script_coverage.py（第 42 门禁 · 根级脚本覆盖）

## 为什么测这个脚本

第 42 门禁是「新增脚本必须带测试/门禁/CI/Make 引用或显式登记豁免」的**唯一机器防线**——
它自身若判据失效（正则写坏、基线解析放水、fail-closed 下限被绕过），整个防护面会静默归零。
门禁脚本必须自证（项目 W663/W709 教训：门禁自身漂移要靠点检抓）。

## 覆盖判据

  G1 干净态：现网实跑 0 FAIL（当前仓库真实状态）
  G2 自检：`--self-test` 5/5 且退出码 0
  G3 报告模式：`--list` 退出码 0 且打印三段计数（不判假绿）
  G4 判据单元：evaluate() 对四类注入（新增无引用/基线陈腐/引用面塌陷/重复行）必须给出对应码
  G5 基线纪律：基线不得为空（空基线=全量 FAIL 或称「被清空」，两种都属失效形态）

## 手法

纯判据用 evaluate() 注入构造；CLI 面走 subprocess（真实入口，含退出码语义）。
"""

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import check_script_coverage as cov  # noqa: E402

GATE = SCRIPTS / "check_script_coverage.py"


def _run(*args, timeout=120):
    return subprocess.run(
        [sys.executable, str(GATE), *args],
        capture_output=True, text=True, timeout=timeout, cwd=str(ROOT),
    )


def _fake_input(**over):
    fill = ["fill%02d.py" % i for i in range(cov.MIN_SCRIPTS)]
    base = {
        "scripts": ["alpha.py", "beta.py"] + fill,
        "corpus_text": "\n".join(['"alpha.py"', "import beta"] + fill),
        "baseline_raw": "\n".join(["# c"] + ["fill%02d.py" % i for i in range(cov.MIN_BASELINE)]),
        "_self_test": True,
    }
    base.update(over)
    return base


# ------------------------------------------------------------------ G1/G2/G3 真实入口
def test_g1_live_tree_passes_gate():
    r = _run()
    assert r.returncode == 0, "第 42 门禁在现网树上 FAIL：\n%s" % (r.stdout[-1500:] + r.stderr[-500:])
    assert "---- 第 42 门禁 根级脚本覆盖：0 FAIL ----" in r.stdout, "缺汇总行（疑似未真正扫描）"


def test_g2_self_test_all_pass():
    r = _run("--self-test")
    assert r.returncode == 0, r.stdout[-800:]
    assert "self-test：6/6 通过" in r.stdout


def test_g3_list_reports_counts():
    r = _run("--list")
    assert r.returncode == 0
    assert "根级脚本" in r.stdout and "豁免登记" in r.stdout


# --------------------------------------------------------------------- G4 判据单元
def test_g4_unknown_script_is_c1():
    issues = cov.evaluate(_fake_input(scripts=_fake_input()["scripts"] + ["brandnew.py"]))
    assert any(i.startswith("C1") and "brandnew.py" in i for i in issues)


def test_g4b_stale_baseline_line_is_c2():
    issues = cov.evaluate(_fake_input(baseline_raw="# c\nfill00.py\ngone.py\n"))
    assert any(i.startswith("C2") and "gone.py" in i for i in issues)


def test_g4c_empty_corpus_is_c3_fail_closed():
    issues = cov.evaluate(_fake_input(corpus_text="   "))
    assert any(i.startswith("C3") for i in issues)


def test_g4d_duplicate_baseline_line_is_c2():
    raw = "\n".join(["fill00.py", "fill00.py"] + ["fill%02d.py" % i for i in range(1, cov.MIN_BASELINE)])
    issues = cov.evaluate(_fake_input(baseline_raw=raw))
    assert any(i.startswith("C2") and "重复" in i for i in issues)


def test_g4e_clean_input_has_no_issues():
    assert cov.evaluate(_fake_input()) == []


# ----------------------------------------------------------------------- G5 基线纪律
def test_g5_real_baseline_is_annotated_and_nonempty():
    text = (SCRIPTS / "output" / "script-coverage-baseline.txt").read_text(encoding="utf-8")
    lines = [ln for ln in text.splitlines() if ln.strip() and not ln.startswith("#")]
    assert len(lines) >= cov.MIN_BASELINE, "现网基线仅 %d 行（下限 %d）" % (len(lines), cov.MIN_BASELINE)
    # 门禁自身由本测试文件覆盖，不得出现在豁免表（自证：豁免表不是逃生门）
    assert not any(ln.split("#")[0].strip() == "check_script_coverage.py" for ln in lines), \
        "门禁脚本自身被登记豁免——它已有本专测覆盖，请从基线移除"
    # 豁免行必须带分类注释（禁「垃圾桶」式裸登记）
    annotated = [ln for ln in lines if "#" in ln]
    assert len(annotated) == len(lines), "存在未注明分类理由的豁免行：%s" % [
        ln for ln in lines if "#" not in ln
    ]


def test_g5b_baseline_entries_all_exist_on_disk():
    text = (SCRIPTS / "output" / "script-coverage-baseline.txt").read_text(encoding="utf-8")
    names = [ln.split("#")[0].strip() for ln in text.splitlines() if ln.strip() and not ln.startswith("#")]
    missing = [n for n in names if not (SCRIPTS / n).exists()]
    assert not missing, "基线陈腐行：%s" % missing
