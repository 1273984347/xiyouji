"""W1009 单元测试·batch_spec（spec 解析唯一入口）+ 级联收尾 stats 自动刷新。

背景：
  ① 「本批应动哪些文件」曾有两份实现（safe_commit._spec_paths / check_commit_scope.spec_paths_for），
     W1007 因一处 `cells[1]`、一处 `cells[0]` 差点放行越界件 ⇒ 收敛为 batch_spec。
  ② C5d（stats 漂移）在 W1006/W1007/W1008 三批各假红一次，都靠人记得手跑 ⇒ 级联收尾自动刷。

运行：py -m pytest tests/unit/test_batch_spec.py -v
"""
import json
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import batch_spec  # noqa: E402


def test_paths_from_rows_first_cell_is_path():
    """表行 `| 路径 | W#### | 说明 |` —— 去壳后**第 1 格**是路径（W1007 踩过取第 2 格）。"""
    rows = ["| scripts/a.py | W1009 | 说明 |", "| docs/b.md | W1009 | 说明 |"]
    assert batch_spec.paths_from_rows(rows) == ["docs/b.md", "scripts/a.py"]


def test_paths_from_rows_skips_header_and_blanks():
    rows = ["| 文件 | W | 说明 |", "|---|---|---|", "|  | W1009 | 空 |", "| c.py | W1009 | x |"]
    assert batch_spec.paths_from_rows(rows) == ["c.py"]


def test_paths_from_rows_dedupes_and_normalizes():
    rows = ["| a\\b.py | W1009 | x |", "| a/b.py | W1009 | y |", "| a/b.py | W1009 | z |"]
    assert batch_spec.paths_from_rows(rows) == ["a/b.py"]


def test_spec_paths_from_spec_empty():
    assert batch_spec.spec_paths_from_spec({}) == []
    assert batch_spec.spec_paths_from_spec({"file_index_rows": None}) == []


def test_spec_paths_reads_file(tmp_path):
    p = tmp_path / "spec.json"
    p.write_text(json.dumps({"file_index_rows": ["| x.py | W1009 | a |"]}, ensure_ascii=False), encoding="utf-8")
    assert batch_spec.spec_paths(str(p)) == ["x.py"]


def test_two_call_sites_agree():
    """safe_commit 与第 51 槽必须给同一答案——这是本模块存在的理由。"""
    import check_commit_scope as ccs
    import safe_commit as sc

    spec = {"file_index_rows": ["| a.py | W1009 | x |", "| docs/b.md | W1009 | y |"]}
    assert sc._spec_paths(spec) == batch_spec.spec_paths_from_spec(spec)
    assert ccs.spec_paths_for(1009) in (None, []) or isinstance(ccs.spec_paths_for(1009), list)


def test_refresh_stats_ok_and_fail(capsys):
    """级联收尾 stats：成功返回 True，失败返回 False 且不静默（打印 FAIL）。"""
    import batch_cascade as bc

    class R:
        def __init__(self, rc, out):
            self.returncode, self.stdout, self.stderr = rc, out, ""

    orig = bc._STATS_RUNNER
    try:
        bc._STATS_RUNNER = lambda cmd: R(0, "OK    -> stats.json（变更 1 键）")
        assert bc._refresh_stats("W1009") is True
        out = capsys.readouterr().out
        assert "[STATS] OK" in out

        bc._STATS_RUNNER = lambda cmd: R(2, "Traceback ...")
        assert bc._refresh_stats("W1009") is False
        out = capsys.readouterr().out
        assert "[STATS] FAIL" in out
    finally:
        bc._STATS_RUNNER = orig
