"""W1138：数据集溯源校验器回归锁。

锁三条：合法数据零违例、8 例负样本全部拦截、两个页面 EMBEDDED 同步标记在位。
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import check_dataset_provenance as prov  # noqa: E402


def _data():
    return json.loads(prov.DATA.read_text(encoding="utf-8"))


def _edge():
    return json.loads(prov.EDGE_DATA.read_text(encoding="utf-8"))


def test_valid_dataset_has_no_violation():
    assert prov.validate(_data()) == []


def test_self_test_cases_are_all_caught():
    assert prov.self_test(_data(), _edge()) == []


def test_page_embedded_copy_is_synced():
    assert prov.page_sync_errors() == []
