"""W746 单元测试：page_router 语义页面路由（纯逻辑·零重依赖·CI 兼容）。

覆盖（不加载模型·不读站点——纯函数层）：
- _layer 题层判定（基线/中等/难题/探针·W746 冻结结构）
- _clean_title 站名前后缀清洗（含空值回退）
- hit_at top-N 命中判定（子串口径·n 截断）

运行：py -m pytest tests/unit/test_page_router.py -v
"""
import sys
from pathlib import Path

RAG_DIR = Path(__file__).resolve().parent.parent.parent / "scripts" / "rag"
if str(RAG_DIR) not in sys.path:
    sys.path.insert(0, str(RAG_DIR))

import page_router  # noqa: E402

# ---------- 题层判定 ----------

def test_layer_baseline_range():
    for qid in ("R01", "R05", "R10"):
        assert page_router._layer(qid) == "基线"


def test_layer_mid_range():
    for qid in ("R11", "R14", "R18"):
        assert page_router._layer(qid) == "中等"


def test_layer_hard_and_probe():
    assert page_router._layer("R20") == "难题"
    assert page_router._layer("R19") == "探针"
    assert page_router._layer("R21") == "探针"


# ---------- title 清洗 ----------

def test_clean_title_strips_site_suffix():
    assert page_router._clean_title("天庭权力关系图 · 详解西游记", "x.html") == "天庭权力关系图"


def test_clean_title_strips_site_prefix():
    assert page_router._clean_title("详解西游记 · 人物关系可交互视图", "x.html") == "人物关系可交互视图"


def test_clean_title_collapses_whitespace_and_fallback():
    assert page_router._clean_title("取经  全路程图", "x.html") == "取经 全路程图"
    # 纯站名（无「 · 」分隔）清洗不掉——非空即保留·不回退文件名
    assert page_router._clean_title("  详解西游记  ", "fallback.html") == "详解西游记"
    # 空/None → 回退文件名
    assert page_router._clean_title("", "fallback.html") == "fallback.html"
    assert page_router._clean_title(None, "fallback.html") == "fallback.html"


# ---------- top-N 命中判定 ----------

def test_hit_at_substring_match():
    expect = ["81-hardships", "hardship-heatmap"]
    files = ["chapter-stats.html", "81-hardships-view.html", "tag-cloud.html"]
    assert page_router.hit_at(expect, files, 1) is False
    assert page_router.hit_at(expect, files, 3) is True


def test_hit_at_first_position():
    expect = ["tag-cloud"]
    assert page_router.hit_at(expect, ["tag-cloud.html", "x.html"], 1) is True
    assert page_router.hit_at(expect, ["x.html", "tag-cloud.html"], 1) is False


def test_hit_at_empty_and_n_bound():
    assert page_router.hit_at(["a"], [], 1) is False
    assert page_router.hit_at(["a"], ["a.html"], 0) is False
