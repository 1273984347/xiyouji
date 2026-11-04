"""W1130 单元测试 · C9 冲突标记对账的方案报告扫描面扩展。

病根（W1127 实证）：C9 的扫描面只有 5 个治理文件 ⇒ 方案报告目录（含 计划方案/）不在其中
⇒ 我方 W1127 合并冲突时把未清理的冲突标记带进报告并合入 main ⇒ 门禁仍 0 FAIL。
W1130：把 C9 扫描面扩展到 docs/11-方案报告 下全部 .md（递归）⇒ 判据强度提升。

运行：py -3 -m pytest tests/unit/test_w1130_c9_report_scope.py -v
"""
import os
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import check_doc_sync as m  # noqa: E402


def _report_texts(text):
    return {"docs/11-方案报告/计划方案/T99-样例.md": text}


def test_c9_flags_report_containing_conflict_marks():
    """负样本：报告件含冲突标记 ⇒ 判红（此前该形态完全不在扫描面内）。"""
    issues = []
    m._check_c9_conflict_marks(
        {"c9_report_texts": _report_texts("正文\n<<<<<<< HEAD\nA\n=======\nB\n>>>>>>> origin/main\n")},
        issues)
    assert issues, "报告件含冲突标记未判红"
    assert "T99-样例.md" in issues[0]


def test_c9_skips_report_with_explicit_exempt_mark():
    """正样本：报告件行内带 doc-sync:exempt ⇒ 跳过（刻意引用标记字面量的场景）。"""
    issues = []
    m._check_c9_conflict_marks(
        {"c9_report_texts": _report_texts("<<<<<<< HEAD <!--doc-sync:exempt--> 教学引用\n")},
        issues)
    assert issues == []


def test_c9_ignores_quoted_marker_line():
    """正样本：引用块（行首 >）里的标记字面量不算冲突标记。"""
    issues = []
    m._check_c9_conflict_marks(
        {"c9_report_texts": _report_texts("> <<<<<<< HEAD 教学引用\n")},
        issues)
    assert issues == []


def test_c9_report_surfaces_covers_plan_subdirectory(tmp_path, monkeypatch):
    """正样本：扫描面覆盖 计划方案/ 子目录（C5b 的除外只针对聚合数字·不适用于结构缺陷）。"""
    base = tmp_path / "docs" / "11-方案报告"
    (base / "计划方案").mkdir(parents=True)
    (base / "计划方案" / "T99-样例.md").write_text("x", encoding="utf-8")
    (base / "根层.md").write_text("x", encoding="utf-8")
    monkeypatch.setattr(m, "ROOT", str(tmp_path))
    names = [p.replace(os.sep, "/") for p in m.c9_report_surfaces()]
    assert any("计划方案" in n for n in names), names
    assert any("根层.md" in n for n in names), names


def test_c9_report_surfaces_ignores_non_markdown(tmp_path, monkeypatch):
    """正样本：扫描面只收 .md（不扫二进制/脚本）。"""
    base = tmp_path / "docs" / "11-方案报告"
    base.mkdir(parents=True)
    (base / "a.md").write_text("x", encoding="utf-8")
    (base / "b.json").write_text("{}", encoding="utf-8")
    monkeypatch.setattr(m, "ROOT", str(tmp_path))
    names = [os.path.basename(p) for p in m.c9_report_surfaces()]
    assert "a.md" in names
    assert "b.json" not in names
