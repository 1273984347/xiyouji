"""W1215 单元测试·坑位计数链生成器化（stats 新键 + pitfalls 段头窄域 sweep + C5e 剥标记补盲）。

覆盖：
  T1 真仓回归锁：坑位键齐全·total = 六主题和 = 声明和 = 实测和（不钉绝对数字）
  T2 pitfall_theme_counts 解析带 marker 段头（sweep 跟随后形态）
  T3 sweep_markers 对 pitfalls.md 窄域生效——段头跟随·正文历史示例标记不被改写
  T4 C5e 补两盲区形态（「完整 N 条见」/「N 条坑·六主题」＝W1214 实漏 321 的形态）
  T4b C5e 剥标记匹配（标记字面量与实值相等 ⇒ 零 issue）
  T5 未知主题名 fail-closed（KeyError·新主题须先登记 PITFALL_THEME_KEYS）
运行：py -m pytest tests/unit/test_w1215_count_markers.py -v
"""
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import check_doc_sync as cds  # noqa: E402
import pytest  # noqa: E402
import stats as stats_mod  # noqa: E402


def test_t1_real_repo_pitfall_keys_consistent():
    pf = stats_mod._pitfall_stats()
    themes = {k: v for k, v in pf.items() if k != "pitfalls_total"}
    assert len(themes) == 6
    assert pf["pitfalls_total"] == sum(themes.values())
    _d, _a = cds.pitfall_theme_counts()
    assert pf["pitfalls_total"] == sum(_a.values()) == sum(_d.values())


def test_t2_theme_counts_parse_marked_headers():
    pit = (
        "### CSS / 视觉渲染（48<!--stats:pitfalls_css--> 条）\n"
        "\n"
        "- **a**（W1 实证·E-1）\n"
        "- **b**（W2 实证·E-2）\n"
        "### JS / CSP / 运行时（99 条）\n"
        "\n"
        "- **c**（W3 实证·E-3）\n"
    )
    declared, actual = cds.pitfall_theme_counts({"pitfalls": pit})
    assert declared == {"CSS / 视觉渲染": 48, "JS / CSP / 运行时": 99}
    assert actual == {"CSS / 视觉渲染": 2, "JS / CSP / 运行时": 1}


def test_t3_sweep_narrow_scope_on_pitfalls(tmp_path):
    pit_file = tmp_path / "pitfalls.md"
    pit_file.write_text(
        "### CSS / 视觉渲染（48<!--stats:pitfalls_css--> 条）\n"
        "- **历史示例**（W913 实证·E-195）：旧值 615<!--stats:a1_a6_docs--> 曾漂移\n"
        "### JS / CSP / 运行时（12<!--stats:pitfalls_js--> 条）\n",
        encoding="utf-8",
    )
    values = {"pitfalls_css": 50, "pitfalls_js": 12, "a1_a6_docs": 623}
    updated, _details = stats_mod.sweep_markers(
        values, files=[str(pit_file)], narrow_pred=lambda fp: True)
    text = pit_file.read_text(encoding="utf-8")
    assert "（50<!--stats:pitfalls_css--> 条）" in text  # 段头跟随
    assert "12<!--stats:pitfalls_js-->" in text  # 同值不动
    assert "615<!--stats:a1_a6_docs-->" in text  # 正文历史示例标记不被改写（窄域核心）
    assert updated == 1


def test_t4_c5e_covers_blind_shapes():
    # 两处 W1214 实漏形态——AGENTS「完整 N 条见」/ HANDOVER「N 条坑·六主题」：
    # 旧 pattern 集合对此零命中（正是 321 漏改静默全绿的根源），现必须逐处判红
    inp = {
        "pitfalls": "### 流程 / 协作 / 取证（2 条）\n- **a**（W1 实证·E-1）\n- **b**（W2 实证·E-2）\n",
        "agents": "完整 9 条见",
        "jiaojie": "9 条坑·六主题",
        "skill": "",
    }
    issues = []
    cds._c5e_pitfall_counts_injected(inp, issues)
    hits = [i for i in issues
            if i.startswith("C5e: AGENTS.md 声明") or i.startswith("C5e: HANDOVER.md 声明")]
    assert len(hits) == 2, hits


def test_t4b_c5e_matches_marked_literals_zero_issue_when_equal():
    inp = {
        "pitfalls": "### 流程 / 协作 / 取证（2 条）\n- **a**（W1 实证·E-1）\n- **b**（W2 实证·E-2）\n",
        "agents": "完整 2<!--stats:pitfalls_total--> 条见",
        "jiaojie": "",
        "skill": "",
    }
    issues = []
    cds._c5e_pitfall_counts_injected(inp, issues)
    assert not [i for i in issues if "声明" in i and "AGENTS.md" in i]


def test_t5_unknown_theme_fails_closed(monkeypatch):
    monkeypatch.setattr(
        cds, "pitfall_theme_counts", lambda inp=None: ({"新主题": 1}, {"新主题": 1}))
    with pytest.raises(KeyError):
        stats_mod._pitfall_stats()
