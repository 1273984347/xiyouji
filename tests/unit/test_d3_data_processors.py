# -*- coding: utf-8 -*-
"""W236-E E5 测试深化·D3.js 数据处理函数单元测试·pytest 风格

本测试模块以 Python 等价逻辑模拟 site/data/*.html 中 D3.js 的核心数据处理流程，
覆盖数据加载（JSON/CSV）/格式转换/聚合计算/边界条件/数值验证等场景。

被测目标（与前端 D3 处理链对应）：
  - load_chapter_data        ← d3.json / d3.csv 加载章回数据
  - aggregate_character_stats← d3.rollup / d3.nest 角色统计聚合
  - normalize_metrics        ← d3.scaleLinear 归一化
  - format_conversion        ← d3.csvParse / d3.json 互转
  - parse_journey_route      ← d3.line 路径解析
  - build_node_link          ← d3.forceSimulation 节点边构造
  - compute_sentiment_arc    ← d3.area 情感弧线计算
  - bucket_hardships         ← d3.histogram 难难分桶
  - sanitize_numeric         ← d3 拼接数据时的数值清洗
  - merge_datasets           ← d3.merge / Array.join 多源合并

运行：pytest tests/unit/test_d3_data_processors.py -v
"""
import csv
import io
import json
from pathlib import Path

import pytest


# ---------------------------------------------------------------------------
# 被测函数：以 Python 实现 D3.js 等价数据处理逻辑
# ---------------------------------------------------------------------------

def load_chapter_data(json_text):
    """模拟 d3.json：从 JSON 文本加载章回数据，空输入返回空列表。"""
    if not json_text or not json_text.strip():
        return []
    data = json.loads(json_text)
    if isinstance(data, dict):
        data = [data]
    return list(data)


def aggregate_character_stats(records):
    """模拟 d3.rollup：按角色名聚合出场次数与平均戏份权重。"""
    bucket = {}
    for r in records:
        name = r.get("character") or r.get("name")
        if not name:
            continue
        weight = float(r.get("weight", 0))
        appear = 1
        entry = bucket.setdefault(name, {"count": 0, "weight_sum": 0.0})
        entry["count"] += appear
        entry["weight_sum"] += weight
    result = {}
    for name, agg in bucket.items():
        avg = agg["weight_sum"] / agg["count"] if agg["count"] else 0.0
        result[name] = {"count": agg["count"], "avg_weight": round(avg, 4)}
    return result


def normalize_metrics(values, domain=None):
    """模拟 d3.scaleLinear().domain().range([0,1])：线性归一化到 [0,1]。"""
    clean = [float(v) for v in values if v is not None]
    if not clean:
        return []
    lo, hi = (min(clean), max(clean)) if domain is None else (float(domain[0]), float(domain[1]))
    if hi == lo:
        return [0.5 for _ in clean]
    return [round((v - lo) / (hi - lo), 4) for v in clean]


def format_conversion(payload, target):
    """模拟 d3.csvParse / d3.json 互转：dict 列表 ↔ CSV 字符串。"""
    if target == "csv":
        if not payload:
            return ""
        fields = list(payload[0].keys())
        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=fields)
        writer.writeheader()
        for row in payload:
            writer.writerow({k: row.get(k, "") for k in fields})
        return buf.getvalue().strip()
    if target == "json":
        if isinstance(payload, str):
            reader = csv.DictReader(io.StringIO(payload))
            return [dict(row) for row in reader]
        return list(payload)
    raise ValueError(f"不支持的转换目标: {target}")


def parse_journey_route(points):
    """模拟 d3.line：将有序坐标点解析为折线路径描述。"""
    pts = [(float(p["x"]), float(p["y"])) for p in points if "x" in p and "y" in p]
    if not pts:
        return ""
    return "M " + " L ".join(f"{x:.2f} {y:.2f}" for x, y in pts)


def build_node_link(nodes, edges):
    """模拟 d3.forceSimulation 节点-边构造：返回带 degree 字段的节点列表。"""
    degree = {n["id"]: 0 for n in nodes}
    valid_ids = set(degree)
    out_edges = []
    for e in edges:
        s, t = e.get("source"), e.get("target")
        if s in valid_ids and t in valid_ids:
            degree[s] += 1
            degree[t] += 1
            out_edges.append({"source": s, "target": t, "weight": float(e.get("weight", 1))})
    out_nodes = [dict(n, degree=degree[n["id"]]) for n in nodes]
    return {"nodes": out_nodes, "links": out_edges}


def compute_sentiment_arc(samples):
    """模拟 d3.area：基于情感分值序列计算上下包络。"""
    cleaned = [float(s) for s in samples if s is not None]
    if not cleaned:
        return {"baseline": [], "upper": [], "lower": []}
    baseline = [round(v, 4) for v in cleaned]
    upper = [round(v + 0.5, 4) for v in cleaned]
    lower = [round(v - 0.5, 4) for v in cleaned]
    return {"baseline": baseline, "upper": upper, "lower": lower}


def bucket_hardships(values, bins=10):
    """模拟 d3.histogram：将难难强度分桶统计。"""
    clean = [float(v) for v in values if v is not None]
    if not clean:
        return []
    lo, hi = min(clean), max(clean)
    if hi == lo:
        return [{"x0": lo, "x1": hi, "count": len(clean)}]
    width = (hi - lo) / bins
    buckets = [{"x0": lo + i * width, "x1": lo + (i + 1) * width, "count": 0} for i in range(bins)]
    for v in clean:
        idx = int((v - lo) / width)
        if idx >= bins:
            idx = bins - 1
        buckets[idx]["count"] += 1
    return buckets


def sanitize_numeric(raw):
    """模拟 D3 数据拼接阶段的数值清洗：非法值归零。"""
    if raw is None:
        return 0.0
    try:
        return float(raw)
    except (TypeError, ValueError):
        return 0.0


def merge_datasets(*datasets):
    """模拟 d3.merge / Array.join：多源数据合并去重（按 id）。"""
    seen = {}
    for ds in datasets:
        for row in ds or []:
            key = row.get("id")
            if key is None:
                continue
            seen[key] = row
    return list(seen.values())


# ---------------------------------------------------------------------------
# 测试夹具
# ---------------------------------------------------------------------------

@pytest.fixture
def chapter_records():
    return [
        {"character": "孙悟空", "chapter": 1, "weight": 0.9},
        {"character": "唐僧", "chapter": 1, "weight": 0.6},
        {"character": "孙悟空", "chapter": 2, "weight": 0.8},
        {"character": "猪八戒", "chapter": 2, "weight": 0.5},
        {"character": "沙悟净", "chapter": 2, "weight": 0.3},
        {"character": "孙悟空", "chapter": 3, "weight": 1.0},
    ]


@pytest.fixture
def csv_text():
    return "character,weight\n孙悟空,0.9\n唐僧,0.6\n猪八戒,0.5\n"


# ---------------------------------------------------------------------------
# 数据加载测试
# ---------------------------------------------------------------------------

class TestLoadChapterData:
    def test_load_chapter_data_valid_json(self):
        text = json.dumps([{"chapter": 1}, {"chapter": 2}])
        data = load_chapter_data(text)
        assert len(data) == 2
        assert data[0]["chapter"] == 1

    def test_load_chapter_data_single_object(self):
        text = json.dumps({"chapter": 1})
        data = load_chapter_data(text)
        assert isinstance(data, list)
        assert data[0]["chapter"] == 1

    def test_load_chapter_data_empty_string(self):
        assert load_chapter_data("") == []
        assert load_chapter_data("   ") == []


# ---------------------------------------------------------------------------
# 聚合计算测试
# ---------------------------------------------------------------------------

class TestAggregateCharacterStats:
    def test_aggregate_character_stats_counts(self, chapter_records):
        stats = aggregate_character_stats(chapter_records)
        assert stats["孙悟空"]["count"] == 3
        assert stats["唐僧"]["count"] == 1
        assert stats["猪八戒"]["count"] == 1

    def test_aggregate_character_stats_avg_weight(self, chapter_records):
        stats = aggregate_character_stats(chapter_records)
        # 孙悟空权重 0.9 + 0.8 + 1.0 = 2.7 / 3 = 0.9
        assert stats["孙悟空"]["avg_weight"] == pytest.approx(0.9, abs=1e-3)

    def test_aggregate_character_stats_missing_name_skipped(self):
        records = [{"weight": 0.5}, {"character": "孙悟空", "weight": 0.8}]
        stats = aggregate_character_stats(records)
        assert "孙悟空" in stats
        assert len(stats) == 1


# ---------------------------------------------------------------------------
# 归一化测试
# ---------------------------------------------------------------------------

class TestNormalizeMetrics:
    def test_normalize_metrics_basic(self):
        out = normalize_metrics([0, 5, 10])
        assert out[0] == 0.0
        assert out[2] == 1.0
        assert out[1] == pytest.approx(0.5, abs=1e-3)

    def test_normalize_metrics_constant(self):
        out = normalize_metrics([7, 7, 7])
        assert out == [0.5, 0.5, 0.5]

    def test_normalize_metrics_empty(self):
        assert normalize_metrics([]) == []

    def test_normalize_metrics_custom_domain(self):
        out = normalize_metrics([5], domain=(0, 10))
        assert out == [0.5]


# ---------------------------------------------------------------------------
# 格式转换测试
# ---------------------------------------------------------------------------

class TestFormatConversion:
    def test_format_conversion_json_to_csv(self, csv_text):
        payload = [{"character": "孙悟空", "weight": "0.9"},
                   {"character": "唐僧", "weight": "0.6"},
                   {"character": "猪八戒", "weight": "0.5"}]
        out = format_conversion(payload, "csv")
        assert "character,weight" in out
        assert "孙悟空,0.9" in out

    def test_format_conversion_csv_to_json(self, csv_text):
        out = format_conversion(csv_text, "json")
        assert len(out) == 3
        assert out[0]["character"] == "孙悟空"

    def test_format_conversion_empty_csv(self):
        assert format_conversion([], "csv") == ""

    def test_format_conversion_invalid_target(self):
        with pytest.raises(ValueError):
            format_conversion([], "xml")


# ---------------------------------------------------------------------------
# 路径解析测试
# ---------------------------------------------------------------------------

class TestParseJourneyRoute:
    def test_parse_journey_route_basic(self):
        pts = [{"x": 0, "y": 0}, {"x": 1, "y": 1}, {"x": 2, "y": 0.5}]
        path = parse_journey_route(pts)
        assert path.startswith("M ")
        assert " L " in path
        assert "0.00 0.00" in path

    def test_parse_journey_route_empty(self):
        assert parse_journey_route([]) == ""

    def test_parse_journey_route_skip_invalid(self):
        pts = [{"x": 1, "y": 1}, {"x": 2}, {"y": 3}]
        path = parse_journey_route(pts)
        assert path.count("L") == 0  # 只剩起点


# ---------------------------------------------------------------------------
# 节点-边构造测试
# ---------------------------------------------------------------------------

class TestBuildNodeLink:
    def test_build_node_link_degree(self):
        nodes = [{"id": "a"}, {"id": "b"}, {"id": "c"}]
        edges = [{"source": "a", "target": "b", "weight": 2},
                 {"source": "b", "target": "c"}]
        g = build_node_link(nodes, edges)
        by_id = {n["id"]: n for n in g["nodes"]}
        assert by_id["a"]["degree"] == 1
        assert by_id["b"]["degree"] == 2
        assert by_id["c"]["degree"] == 1
        assert len(g["links"]) == 2

    def test_build_node_link_skip_invalid_edge(self):
        nodes = [{"id": "a"}]
        edges = [{"source": "a", "target": "ghost"}, {"source": "a", "target": "a"}]
        g = build_node_link(nodes, edges)
        # self-loop source==target 仍计入（D3 force 默认不阻断）
        assert len(g["links"]) == 1
        assert g["links"][0]["target"] == "a"


# ---------------------------------------------------------------------------
# 情感弧线测试
# ---------------------------------------------------------------------------

class TestComputeSentimentArc:
    def test_compute_sentiment_arc_envelope(self):
        arc = compute_sentiment_arc([0.2, 0.5, -0.3])
        assert arc["baseline"] == [0.2, 0.5, -0.3]
        assert arc["upper"][0] == pytest.approx(0.7, abs=1e-3)
        assert arc["lower"][2] == pytest.approx(-0.8, abs=1e-3)

    def test_compute_sentiment_arc_empty(self):
        arc = compute_sentiment_arc([])
        assert arc == {"baseline": [], "upper": [], "lower": []}


# ---------------------------------------------------------------------------
# 难难分桶测试
# ---------------------------------------------------------------------------

class TestBucketHardships:
    def test_bucket_hardships_count_sum(self):
        vals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        buckets = bucket_hardships(vals, bins=5)
        total = sum(b["count"] for b in buckets)
        assert total == 10
        assert len(buckets) == 5

    def test_bucket_hardships_constant(self):
        buckets = bucket_hardships([5, 5, 5], bins=5)
        assert len(buckets) == 1
        assert buckets[0]["count"] == 3

    def test_bucket_hardships_empty(self):
        assert bucket_hardships([]) == []


# ---------------------------------------------------------------------------
# 边界条件测试
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_edge_cases_empty_aggregate(self):
        assert aggregate_character_stats([]) == {}

    def test_edge_cases_negative_normalize(self):
        out = normalize_metrics([-10, 0, 10])
        assert out[0] == 0.0
        assert out[2] == 1.0
        assert out[1] == 0.5

    def test_edge_cases_negative_weights(self):
        records = [{"character": "白骨精", "weight": -0.3},
                   {"character": "白骨精", "weight": 0.1}]
        stats = aggregate_character_stats(records)
        assert stats["白骨精"]["avg_weight"] == pytest.approx(-0.1, abs=1e-3)

    def test_edge_cases_sanitize_numeric(self):
        assert sanitize_numeric("3.14") == 3.14
        assert sanitize_numeric(None) == 0.0
        assert sanitize_numeric("abc") == 0.0
        assert sanitize_numeric(True) == 1.0

    def test_edge_cases_merge_datasets_dedup(self):
        a = [{"id": 1, "v": "a"}, {"id": 2, "v": "b"}]
        b = [{"id": 2, "v": "b2"}, {"id": 3, "v": "c"}]
        merged = merge_datasets(a, b)
        ids = {row["id"] for row in merged}
        assert ids == {1, 2, 3}
        # 后者覆盖前者
        row2 = next(r for r in merged if r["id"] == 2)
        assert row2["v"] == "b2"

    def test_edge_cases_merge_datasets_with_none(self):
        merged = merge_datasets(None, [{"id": 1}], [{"id": 2}])
        assert len(merged) == 2


# ---------------------------------------------------------------------------
# 数值验证测试
# ---------------------------------------------------------------------------

class TestNumericValidation:
    def test_numeric_validation_bucket_range(self):
        buckets = bucket_hardships([0, 100], bins=4)
        assert buckets[0]["x0"] == 0
        assert buckets[-1]["x1"] == 100
        # 每个桶宽度 25
        for b in buckets:
            assert b["x1"] - b["x0"] == pytest.approx(25.0, abs=1e-3)

    def test_numeric_validation_route_float_format(self):
        path = parse_journey_route([{"x": 1.23456, "y": 2.789}])
        assert "1.23 2.79" in path

    def test_numeric_validation_link_weight_default(self):
        g = build_node_link([{"id": "a"}, {"id": "b"}],
                            [{"source": "a", "target": "b"}])
        assert g["links"][0]["weight"] == 1.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
# FILE_INDEX: tests/unit/test_d3_data_processors.py | W236-E | E5 单元测试
