"""W985 单元测试·gen_tools_inventory（机器工具清单：分类规则/用途提取/渲染与对账）。

运行：py -m pytest tests/unit/test_tools_inventory.py -v
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import gen_tools_inventory as gti  # noqa: E402


def test_categorize_priority():
    """下划线 > 精确覆盖 > 前缀 > 兜底（check_review_trigger 覆盖 check_ 前缀）。"""
    assert gti.categorize("_w977_scan.py") == gti.CAT_ONE_OFF
    assert gti.categorize("check_review_trigger.py") == "批次与登记"
    assert gti.categorize("check_js_syntax.py") == "门禁与校验"
    assert gti.categorize("generate_csp.py") == "生成与索引"
    assert gti.categorize("gen_folder_docs.py") == "生成与索引"
    assert gti.categorize("tmpe_tidy.py") == "运维与临时区"
    assert gti.categorize("slice_screenshots.py") == gti.CAT_MISC


def test_purpose_of_extraction():
    assert gti.purpose_of("a.py", '"""批次开工前置核验。\n\n详述"""') == "批次开工前置核验。"
    assert gti.purpose_of("b.js", "// Playwright 批量截图\nconst x = 1;").startswith("Playwright")
    assert gti.purpose_of("c.py", "x = 1\n") == "—"
    assert gti.purpose_of("d.py", "def f():\n    pass") == "—"


def test_build_inventory_sections_and_counts():
    md = gti.build_inventory([
        ("check_x.py", '"""门禁 X。"""'),
        ("_y.py", '"""一次性 Y。"""'),
        ("batch_cascade.py", '"""级联器。"""'),
    ])
    assert "共 **3** 件" in md
    assert "## 门禁与校验（1）" in md and "## 批次与登记（1）" in md
    assert gti.CAT_ONE_OFF + "（1）" in md
    assert "| `check_x.py` | 门禁 X。 |" in md
    assert "禁手改" in md and "{GENERATED_AT}" not in md.replace("生成时间：{GENERATED_AT}", "")


def test_check_mode_detects_drift(tmp_path, monkeypatch):
    """--check 判据：表格主体漂移必红·零差异必绿（时间戳不入判定）。"""
    entries = [("check_x.py", '"""门禁 X。"""')]
    out = tmp_path / "tools-inventory.md"
    want = gti.build_inventory(entries).replace("{GENERATED_AT}", "2026-01-01 00:00")
    out.write_text(want, encoding="utf-8")
    monkeypatch.setattr(gti, "collect_entries", lambda: entries)
    monkeypatch.setattr(gti, "OUT", str(out))
    assert gti.check() == 0
    stale = want.replace("## 门禁与校验（1）", "## 门禁与校验（2）")
    out.write_text(stale, encoding="utf-8")
    assert gti.check() == 1


def test_real_tree_inventory_matches_tracked_count():
    """实盘回归锁：生成清单行数 == tracked 顶层工具件数（清单面无遗漏）。"""
    import tracked_files as tf

    tracked = {n for n in tf.tracked_in_dir("scripts")
               if "/" not in n and n.endswith((".py", ".js", ".mjs"))}
    md = gti.build_inventory(gti.collect_entries())
    rows = [ln for ln in md.splitlines() if ln.startswith("| `")]
    assert len(rows) == len(tracked), "清单行数 %d ≠ tracked %d" % (len(rows), len(tracked))
