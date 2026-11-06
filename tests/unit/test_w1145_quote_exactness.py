"""W1145：标杆档案引文精确性回归锁。

锁三条：9 条引文全部命中原文索引、篡改引文必被拦截、原文索引覆盖 100 回。
"""
import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import check_dataset_provenance as prov  # noqa: E402


def _edge():
    return json.loads(prov.EDGE_DATA.read_text(encoding="utf-8"))


def _search():
    return json.loads(prov.TEXT_SEARCH.read_text(encoding="utf-8"))


def test_all_quotes_are_exact_substrings():
    assert prov.quote_exactness_errors(_edge(), _search()) == []


def test_mutated_quote_is_caught():
    bad = copy.deepcopy(_edge())
    bad["events"][0]["quotes"][0]["text"] = "这是伪造的引文"
    assert prov.quote_exactness_errors(bad, _search()) != []


def test_source_index_has_100_chapters():
    assert len(_search()["chapters"]) >= 100
