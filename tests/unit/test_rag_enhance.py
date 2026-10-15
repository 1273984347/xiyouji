"""W744 单元测试：rag_enhance 增强检索层（T-01 Phase-1 集成）。

覆盖（纯逻辑·零重依赖·CI 兼容）：
- RAG_ENHANCE 档位解析（xiyouji_rag.enhance_level·默认 off / 别名 / 非法值）
- 加权 RRF 池融合（rrf_fuse·dense×2 权重语义与共识优先·k=60 分母核验）
- 并池合并（merge_pools·保序去重）
- 改写输出清理与消息构造（clean_rewrite / build_rewrite_messages）
- 智能改写路由（should_rewrite·短实体判据·W745）
- chunks → 映射重建（doc_rows_from_chunks）
- 离线预置（hf_model_cached / hf_offline_prepare·缓存探测与强制离线）
- 引擎档位校验（EnhanceEngine 拒绝 off / 非法值·构造不触发重依赖加载）

运行：py -m pytest tests/unit/test_rag_enhance.py -v
"""
import os
import sys
from pathlib import Path

import pytest

RAG_DIR = Path(__file__).resolve().parent.parent.parent / "scripts" / "rag"
if str(RAG_DIR) not in sys.path:
    sys.path.insert(0, str(RAG_DIR))

import rag_enhance  # noqa: E402
import xiyouji_rag  # noqa: E402


@pytest.fixture(autouse=True)
def _restore_hf_env():
    """hf_offline_prepare 会写全局 HF_HUB_OFFLINE——测试后恢复，防跨测试污染。"""
    prior = os.environ.get("HF_HUB_OFFLINE")
    yield
    if prior is None:
        os.environ.pop("HF_HUB_OFFLINE", None)
    else:
        os.environ["HF_HUB_OFFLINE"] = prior

# ---------- 档位解析 ----------

def test_enhance_level_default_off(monkeypatch):
    monkeypatch.delenv("RAG_ENHANCE", raising=False)
    assert xiyouji_rag.enhance_level() == "off"


@pytest.mark.parametrize("raw", ["", "off", "0", "false", "no", "none", "bm25", " OFF "])
def test_enhance_level_off_aliases(monkeypatch, raw):
    monkeypatch.setenv("RAG_ENHANCE", raw)
    assert xiyouji_rag.enhance_level() == "off"


@pytest.mark.parametrize("raw", ["dense", "rerank", "rewrite", "Dense", " REWRITE "])
def test_enhance_level_valid(monkeypatch, raw):
    monkeypatch.setenv("RAG_ENHANCE", raw)
    assert xiyouji_rag.enhance_level() == raw.strip().lower()


def test_enhance_level_invalid_raises(monkeypatch):
    monkeypatch.setenv("RAG_ENHANCE", "turbo")
    with pytest.raises(ValueError):
        xiyouji_rag.enhance_level()


# ---------- 加权 RRF 池融合 ----------

def test_rrf_fuse_dense_weight_priority():
    # dense 权重 2.0：dense 榜 rank1（2/61）高于 bm25 榜 rank1（1/61）
    out = rag_enhance.rrf_fuse([["a"], ["b"]], weights=(1.0, rag_enhance.DENSE_WEIGHT))
    assert [p for p, _ in out] == ["b", "a"]


def test_rrf_fuse_consensus_beats_single_top():
    # 双榜共识（1/62 + 2/62 ≈ 0.0484）高于 dense 单榜 rank1（2/61 ≈ 0.0328）
    out = rag_enhance.rrf_fuse([["a", "c"], ["b", "c"]], weights=(1.0, 2.0))
    assert out[0][0] == "c"


def test_rrf_fuse_zero_weight_skips():
    out = rag_enhance.rrf_fuse([["a"], ["b"]], weights=(1.0, 0.0))
    assert [p for p, _ in out] == ["a"]


def test_rrf_fuse_k60_formula():
    # k=60 分母核验：rank0 分 = w/61
    out = dict(rag_enhance.rrf_fuse([["a"]], weights=(1.0,)))
    assert abs(out["a"] - 1.0 / 61) < 1e-12


def test_rrf_fuse_weights_length_guard():
    with pytest.raises(ValueError):
        rag_enhance.rrf_fuse([["a"], ["b"]], weights=(1.0,))


# ---------- 并池 ----------

def test_merge_pools_order_and_dedup():
    assert rag_enhance.merge_pools(["a", "b"], ["b", "c", "a"]) == ["a", "b", "c"]


def test_merge_pools_single_and_empty():
    assert rag_enhance.merge_pools(["x"]) == ["x"]
    assert rag_enhance.merge_pools() == []


# ---------- 改写输出处理 ----------

def test_clean_rewrite_first_nonempty_line():
    assert rag_enhance.clean_rewrite("五行山 两界山\n解释：……") == "五行山 两界山"


def test_clean_rewrite_blank_and_none():
    assert rag_enhance.clean_rewrite("   \n  ") == ""
    assert rag_enhance.clean_rewrite(None) == ""
    assert rag_enhance.clean_rewrite("") == ""


def test_build_rewrite_messages_shape():
    msgs = rag_enhance.build_rewrite_messages("猴子被压在哪座山下")
    assert msgs[0]["role"] == "system" and "改写" in msgs[0]["content"]
    assert msgs[1] == {"role": "user", "content": "猴子被压在哪座山下"}


# ---------- 智能改写路由（W745） ----------

@pytest.mark.parametrize("q", ["白骨精", "铁扇公主", "紧箍咒", "真假美猴王", "牛魔王", "大闹天宫"])
def test_should_rewrite_short_entity_skips(q):
    assert rag_enhance.should_rewrite(q) is False


@pytest.mark.parametrize("q", [
    "猴子被压在哪座山下",
    "孙悟空头上那个一收就疼的圈",
    "吃了能长生不老的那种果子",
    "妖怪为什么都有后台",
    "孙悟空其实代表人的哪一部分",
])
def test_should_rewrite_descriptive_routes(q):
    assert rag_enhance.should_rewrite(q) is True


def test_should_rewrite_edge_cases():
    assert rag_enhance.should_rewrite("") is False
    assert rag_enhance.should_rewrite(None) is False
    assert rag_enhance.should_rewrite("观音的坐骑") is True     # 短但含「的」结构
    assert rag_enhance.should_rewrite("国王是谁") is True      # 短但疑问词
    assert rag_enhance.should_rewrite("大闹天宫悟空") is False  # 6 字=上限·短实体
    assert rag_enhance.should_rewrite("大闹天宫孙悟空") is True  # 7 字>上限


# ---------- chunks 映射 ----------

def test_doc_rows_from_chunks():
    chunks = [
        {"chunk_id": "c0", "doc_idx": 0, "path": "a.md", "text": "x"},
        {"chunk_id": "c1", "doc_idx": 1, "path": "b.md", "text": "y"},
        {"chunk_id": "c2", "doc_idx": 0, "path": "a.md", "text": "z"},
    ]
    path_by_idx, doc_rows = rag_enhance.doc_rows_from_chunks(chunks)
    assert path_by_idx == {0: "a.md", 1: "b.md"}
    assert doc_rows == {0: [0, 2], 1: [1]}


# ---------- 离线预置 ----------

def test_hf_model_cached_detects_snapshot(monkeypatch, tmp_path):
    hub = tmp_path / "hub"
    (hub / "models--BAAI--bge-small-zh-v1.5" / "snapshots" / "abc123").mkdir(parents=True)
    monkeypatch.setenv("HF_HUB_CACHE", str(hub))
    assert rag_enhance.hf_model_cached("BAAI/bge-small-zh-v1.5") is True
    assert rag_enhance.hf_model_cached("BAAI/not-downloaded") is False


def test_hf_offline_prepare_sets_offline_when_all_cached(monkeypatch, tmp_path):
    hub = tmp_path / "hub"
    (hub / "models--A--m1" / "snapshots" / "x").mkdir(parents=True)
    monkeypatch.setenv("HF_HUB_CACHE", str(hub))
    monkeypatch.delenv("HF_HUB_OFFLINE", raising=False)
    assert rag_enhance.hf_offline_prepare(["A/m1"]) is True
    assert os.environ.get("HF_HUB_OFFLINE") == "1"


def test_hf_offline_prepare_missing_cache_keeps_online(monkeypatch, tmp_path):
    monkeypatch.setenv("HF_HUB_CACHE", str(tmp_path / "empty-hub"))
    monkeypatch.delenv("HF_HUB_OFFLINE", raising=False)
    assert rag_enhance.hf_offline_prepare(["A/m1"]) is False
    assert os.environ.get("HF_HUB_OFFLINE") is None


def test_hf_offline_prepare_respects_forced_offline(monkeypatch, tmp_path):
    monkeypatch.setenv("HF_HUB_CACHE", str(tmp_path / "empty-hub"))
    monkeypatch.setenv("HF_HUB_OFFLINE", "1")
    assert rag_enhance.hf_offline_prepare(["A/m1"]) is True


# ---------- 引擎 ----------

def test_engine_rejects_off_level():
    with pytest.raises(ValueError):
        rag_enhance.EnhanceEngine("off")


def test_engine_constructs_without_heavy_deps(tmp_path):
    # 构造不加载模型/产物（惰性）——零重依赖环境可构造
    eng = rag_enhance.EnhanceEngine("rerank", output_dir=str(tmp_path / "nope"))
    assert eng.level == "rerank"
    assert eng._loaded is False


def test_engine_retrieve_requires_bm25_injection(tmp_path):
    eng = rag_enhance.EnhanceEngine("dense", output_dir=str(tmp_path / "nope"))
    with pytest.raises(ValueError):
        eng.retrieve_ranked("任意查询")
