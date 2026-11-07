"""W1149 回归锁：reader 完整性 / dataset 清单 / 生成器路径映射。"""
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import audit_repo  # noqa: E402
import build_reader  # noqa: E402
import check_dataset_manifest  # noqa: E402
import check_reader_integrity  # noqa: E402


def test_reader_integrity_self_test():
    assert check_reader_integrity._self_test() == 0


def test_reader_integrity_repo_clean():
    fails, n = check_reader_integrity.scan(ROOT)
    assert n >= 623
    assert fails == []


def test_reader_pages_self_contained_css():
    html = (ROOT / "site" / "reader" / "ch001.html").read_text(encoding="utf-8")
    assert "INLINED CSS" in html
    assert '<link rel="stylesheet" href="../tokens.css">' not in html
    assert '<link rel="stylesheet" href="../system.css">' not in html


def test_dataset_index_generator_exists():
    p = ROOT / "scripts" / "gen_dataset_index.py"
    assert p.exists()
    assert "def main" in p.read_text(encoding="utf-8")


def test_dataset_manifest_self_test():
    assert check_dataset_manifest._self_test() == 0


def test_dataset_manifest_repo_clean():
    fails, n = check_dataset_manifest.scan(ROOT)
    assert n == 45  # W1157 退役孤儿 dashboard.json：46→45（README/INDEX 已同步）
    assert fails == []


def test_blob_url_mapping():
    assert build_reader._blob_url("source/原文/分回/第001回.md") == build_reader.REPO_BLOB + "source/原文/分回/第001回.md"
    assert build_reader._blob_url("CHANGELOG.md") == build_reader.REPO_BLOB + "CHANGELOG.md"
    assert build_reader._blob_url("00-导读/文档规范.md") == build_reader.BLOB + "00-导读/文档规范.md"
    assert build_reader._blob_url("../source/x.md") == build_reader.REPO_BLOB + "source/x.md"


def test_docs_no_placeholder():
    for sec in ("01-全书逐回解读", "02-人物深度分析", "03-主题与情节专题",
                "04-文化与历史背景", "05-诗词歌赋", "06-个人随笔"):
        for p in (ROOT / "docs" / sec).glob("*.md"):
            assert "（待补）" not in p.read_text(encoding="utf-8"), p


def test_dataset_chapter_no_zero_sentinel():
    for name, path in (("monster-female-network.json", ("monsterFemale", "nodes")),
                       ("monster-hierarchy-network.json", ("network", "nodes")),
                       ("underworld-power-network.json", ("network", "nodes"))):
        data = json.loads((ROOT / "dataset" / name).read_text(encoding="utf-8"))
        obj = data
        for k in path:
            obj = obj[k]
        for node in obj:
            assert node.get("chapter", node.get("回目")) != 0, (name, node)
            if node.get("chapter_scope"):
                assert node.get("chapter") is None or node.get("回目") is None


def test_audit_repo_smoke():
    r = audit_repo.reader_report()
    d = audit_repo.dataset_report()
    p = audit_repo.patterns_report()
    assert r["fail_n"] == 0 and r["pages"] >= 623
    assert d["fail_n"] == 0 and d["files"] == 45  # W1157 退役孤儿 dashboard.json：46→45
    assert p["placeholders"]["pages"] == 0
    assert p["docs_source_prefix"]["pages"] == 0


def test_edge_quote_status_complete():
    data = json.loads((ROOT / "dataset" / "edge-wukong-tangseng.json").read_text(encoding="utf-8"))
    assert len(data["events"]) == 9
    for e in data["events"]:
        assert e["quote_status"] in ("verified", "not_probed")
        if e["quote_status"] == "verified":
            assert e["quotes"]
        else:
            assert e.get("quote_note")
