"""W1340 单元测试·archive_segments 事务写与迁移台账（P1-1 / P1-2）。

覆盖：① 跨面写：两件都成功才保留；② 第二件写失败 ⇒ 第一件回滚；
       ③ 迁移台账只追加 JSONL（每面一条）。
运行：py -m pytest tests/unit/test_archive_segments_transaction.py -v
"""
import json
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import archive_segments as ars  # noqa: E402


def test_write_all_commits_both(tmp_path):
    a, b = tmp_path / "a.md", tmp_path / "b.md"
    a.write_text("A0", encoding="utf-8")
    b.write_text("B0", encoding="utf-8")
    ars._write_all_or_rollback([(str(a), "A1"), (str(b), "B1")])
    assert a.read_text(encoding="utf-8") == "A1"
    assert b.read_text(encoding="utf-8") == "B1"


def test_write_all_rolls_back_on_second_failure(tmp_path):
    a = tmp_path / "a.md"
    a.write_text("A0", encoding="utf-8")
    bad = tmp_path / "missing_dir" / "b.md"  # 父目录不存在 ⇒ 第二件写失败
    with pytest.raises(OSError):
        ars._write_all_or_rollback([(str(a), "A1"), (str(bad), "B1")])
    assert a.read_text(encoding="utf-8") == "A0", "第一件必须回滚到原内容"


def test_append_archive_log_jsonl(tmp_path, monkeypatch):
    monkeypatch.setattr(ars, "ROOT", str(tmp_path))
    recs = [
        {"target": "changelog", "moved_count": 2, "w_min": 1251, "w_max": 1252},
        {"target": "file-index", "moved_count": 2, "w_min": 1251, "w_max": 1252},
    ]
    ars._append_archive_log(recs, "W1340")
    log = tmp_path / "archive" / "docs" / "archive-log.jsonl"
    lines = [json.loads(x) for x in log.read_text(encoding="utf-8").splitlines() if x.strip()]
    assert len(lines) == 2
    assert {x["target"] for x in lines} == {"changelog", "file-index"}
    assert all(x["event"] == "migrate" and x["batch"] == "W1340" and x["ts"] for x in lines)
    # 再追加一次 ⇒ 只增长不覆盖
    ars._append_archive_log(recs[:1], "W1341")
    lines2 = [json.loads(x) for x in log.read_text(encoding="utf-8").splitlines() if x.strip()]
    assert len(lines2) == 3
