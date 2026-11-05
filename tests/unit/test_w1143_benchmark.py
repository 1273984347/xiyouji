"""W1143：唐僧—孙悟空标杆档案回归锁。

锁四条：标杆数据零违例、max/mean 聚合一致、引文回目落在事件区间、页面同步。
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import check_dataset_provenance as prov  # noqa: E402


def _edge():
    return json.loads(prov.EDGE_DATA.read_text(encoding="utf-8"))


def test_edge_dataset_has_no_violation():
    assert prov.validate_edge(_edge()) == []


def test_edge_aggregate_matches_max_and_mean():
    data = _edge()
    weights = [event["event_weight"] for event in data["events"]]
    assert data["aggregate"]["edge_weight"] == max(weights)
    assert abs(data["aggregate"]["event_weight_mean"] - sum(weights) / len(weights)) < 1e-9


def test_quotes_are_inside_event_chapter_ranges():
    for event in _edge()["events"]:
        for quote in event.get("quotes", []):
            assert event["chapter_start"] <= quote["chapter"] <= event["chapter_end"]


def test_benchmark_page_is_synced():
    assert prov.page_sync_errors() == []
