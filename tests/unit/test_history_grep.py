"""W1340 单元测试·history_grep.py（归档面检索·P1-3 根修）。

覆盖：字面量 / 正则 / 忽略大小写 / 每文件上限 / 默认检索面只收归档件 / 退出码语义。
运行：py -m pytest tests/unit/test_history_grep.py -v
"""
import json
import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from history_grep import search  # noqa: E402


def _make_archive(tmp_path):
    docs = tmp_path / "archive" / "docs"
    docs.mkdir(parents=True)
    (docs / "CHANGELOG-ARCHIVE.md").write_text(
        "### W1253（2026-11-21）：旧段\n正文：段数窗\n### W1252（2026-11-20）：更旧\n正文\n",
        encoding="utf-8")
    (docs / "file-index-ARCHIVE-tier2-W1200-W1240.md").write_text(
        "## W1210 标题\n| a | W1253 |\n", encoding="utf-8")
    (docs / "archive-log.jsonl").write_text(
        json.dumps({"event": "migrate", "batch": "W1340", "moved_count": 2}, ensure_ascii=False) + "\n",
        encoding="utf-8")
    (docs / "README.md").write_text("W1253 不应被默认检索面收录\n", encoding="utf-8")
    return tmp_path


def test_literal_hit_across_volumes(tmp_path):
    root = _make_archive(tmp_path)
    hits = search(str(root), "W1253")
    files = {h["file"] for h in hits}
    assert "archive/docs/CHANGELOG-ARCHIVE.md" in files
    assert "archive/docs/file-index-ARCHIVE-tier2-W1200-W1240.md" in files
    assert all("README" not in f for f in files), "README 不属于归档检索面"


def test_regex_and_ignore_case(tmp_path):
    root = _make_archive(tmp_path)
    assert search(str(root), r"W12\d\d", regex=True)
    assert search(str(root), "段数窗", ignore_case=True)
    assert not search(str(root), "不存在的词")


def test_per_file_limit(tmp_path):
    root = _make_archive(tmp_path)
    hits = search(str(root), "W1253", limit=1)
    per = {}
    for h in hits:
        per[h["file"]] = per.get(h["file"], 0) + 1
    assert all(v == 1 for v in per.values())


def test_cli_exit_codes(tmp_path):
    root = _make_archive(tmp_path)
    cwd = Path(__file__).resolve().parent.parent.parent
    ok = subprocess.run([sys.executable, str(SCRIPTS_DIR / "history_grep.py"), "W1253", "--root", str(root)],
                        capture_output=True, text=True, encoding="utf-8", cwd=str(cwd))
    assert ok.returncode == 0 and "命中" in ok.stdout
    miss = subprocess.run([sys.executable, str(SCRIPTS_DIR / "history_grep.py"), "绝不存在XYZ", "--root", str(root)],
                          capture_output=True, text=True, encoding="utf-8", cwd=str(cwd))
    assert miss.returncode == 1


def test_cli_json_shape(tmp_path):
    root = _make_archive(tmp_path)
    cwd = Path(__file__).resolve().parent.parent.parent
    r = subprocess.run([sys.executable, str(SCRIPTS_DIR / "history_grep.py"), "W1253", "--root", str(root), "--json"],
                       capture_output=True, text=True, encoding="utf-8", cwd=str(cwd))
    data = json.loads(r.stdout)
    assert data["pattern"] == "W1253" and data["count"] == len(data["hits"]) >= 2
