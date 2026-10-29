"""W1014 单元测试·第 48 门禁的「读盘路径」覆盖（`check_plan_template.judge_file`）。

背景：W1005 批在**首个新增计划方案件**进仓时，第 48 门禁崩在
`AttributeError: module 'plan_template_review' has no attribute 'io'`——根因是 `judge_file()`
的读盘用了 `R.io.open(...)`（依赖被导入模块**恰好也 import 了 io**），而该路径**只在有新增件
时才被走到** ⇒ 既有自测全走纯函数 `R.judge(text)` ⇒ 潜伏到真实新增件才引爆。

⇒ 本批补的覆盖：`judge_file()` 的**读盘路径**必须被单测走到（三例）：
  ① 真实计划件读盘（HEAD 已存在 ⇒ 走「存量」分支）；
  ② tmp 仓根下的缺项件读盘（monkeypatch ROOT ⇒ 走「新增件」分支⇒ 必判红）；
  ③ 不存在的路径（读失败分支）。

⇒ 未来若有人把读盘改回 `R.io.open` 之类，本文件 ①② 直接 AttributeError ⇒ 测试红。
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
SCRIPTS_DIR = REPO / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import check_plan_template as cpt  # noqa: E402

REAL_REL = "docs/11-方案报告/计划方案/T37-任务计划执行与经验沉淀报告-2026-10-29.md"


def test_judge_file_reads_real_plan_from_disk():
    """① 真实计划件读盘 ⇒ 合规 ⇒ PASS（且 is_new=False ⇒ 走了 HEAD 命中分支）。"""
    assert (REPO / REAL_REL).exists(), "真实计划件不在位：%s" % REAL_REL
    verdict, d = cpt.judge_file(REAL_REL)
    assert verdict == "PASS", "真实计划件被判 FAIL：%s" % (d,)
    assert d.get("is_new") is False, "真实计划件应走「存量」分支：%s" % (d,)


def test_judge_file_new_missing_item_fails(tmp_path, monkeypatch):
    """② 新增件读盘（tmp 仓根）⇒ 缺整项 ⇒ 必判红（走「新增件」分支）。"""
    rel = "docs/11-方案报告/计划方案/_w1014_tmp_probe.md"
    p = tmp_path / "docs" / "11-方案报告" / "计划方案" / "_w1014_tmp_probe.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(cpt.BAD, encoding="utf-8")
    monkeypatch.setattr(cpt, "ROOT", str(tmp_path))
    verdict, d = cpt.judge_file(rel)
    assert verdict == "FAIL", "缺项新增件未被判红：%s" % (d,)
    assert d.get("new_fail"), "缺项新增件未报不符合项：%s" % (d,)


def test_judge_file_missing_path_reports_error(tmp_path, monkeypatch):
    """③ 路径不存在 ⇒ 读失败分支 ⇒ FAIL + error 字段（不抛未捕获异常）。"""
    monkeypatch.setattr(cpt, "ROOT", str(tmp_path))
    verdict, d = cpt.judge_file("docs/11-方案报告/计划方案/_w1014_not_exist.md")
    assert verdict == "FAIL"
    assert d.get("error"), "缺 error 字段：%s" % (d,)


def test_bad_sample_actually_loses_criteria():
    """④ 合成缺项样本确实比合规样本少判据（保证 ② 判红不是因为别的原因）。"""
    good = cpt.R.judge(cpt.GOOD, "执行前计划-TXX.md")
    bad = cpt.R.judge(cpt.BAD, "执行前计划-TXX.md")
    assert cpt.R.fail_set(good) == set()
    assert cpt.R.fail_set(bad), "BAD 样本竟无不符合项"
    assert cpt.R.fail_set(bad) - cpt.R.fail_set(good), "BAD 与 GOOD 的不符合项集合相同"
