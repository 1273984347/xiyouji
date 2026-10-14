"""W743 单元测试：xiyouji_rag 加权 RRF 融合（T-01 融合层消融重构）。

背景：T-01 Phase-0 五系统对照实证——原四路等权 RRF（含「标题命中」「短语位置」）
为负贡献（18 查询 recall@5：四路全融 0.217~0.239 vs A+B 0.347~0.367）。W743 消融
为「A 原始 BM25 ×1.0 + B 别名扩展 BM25 ×0.5」的加权融合。

运行：py -m pytest tests/unit/test_rag_fusion.py -v
"""
import sys
from pathlib import Path

RAG_DIR = Path(__file__).resolve().parent.parent.parent / "scripts" / "rag"
if str(RAG_DIR) not in sys.path:
    sys.path.insert(0, str(RAG_DIR))

import xiyouji_rag  # noqa: E402


def test_rrf_default_equal_weights():
    # 两列表等权：各榜 rank1 同分（1/61），稳定序沿插入顺序
    a = [(9.0, 0), (8.0, 1)]
    b = [(9.0, 2), (8.0, 3)]
    out = [i for i, _ in xiyouji_rag._rrf([a, b])]
    assert out[0] == 0 and out[1] == 2 and out[2] == 1 and out[3] == 3


def test_rrf_weight_scales_contribution():
    # list2 权重 0.5 → 其 rank1（0.5/61）低于 list1 rank1（1/61）
    a = [(9.0, 0)]
    b = [(9.0, 1)]
    out = [i for i, _ in xiyouji_rag._rrf([a, b], weights=(1.0, 0.5))]
    assert out[0] == 0


def test_rrf_zero_weight_skips_list():
    a = [(9.0, 0)]
    b = [(9.0, 1)]
    out = [i for i, _ in xiyouji_rag._rrf([a, b], weights=(1.0, 0.0))]
    assert out == [0]


def test_rrf_consensus_beats_single_top():
    # 双榜上榜文档（1/62 + 0.5/61 ≈ 0.0243）高于单榜 rank1（1/61 ≈ 0.0164）
    a = [(9.0, 0), (8.0, 5)]
    b = [(9.0, 5), (8.0, 2)]
    out = [i for i, _ in xiyouji_rag._rrf([a, b], weights=(1.0, 0.5))]
    assert out[0] == 5
