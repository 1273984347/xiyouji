"""W1006 单元测试·safe_commit --expect-spec（防代提硬拦）。

背景：代提已发生三次（W989 级联十四面 / W1002 审查 B3 / W1004 被 W1005 全量提交带走）。
根因是「共享工作树 + 他方 `git add -A`」——索引里混入 spec 之外的在途件。
本判据在提交前把索引态与本批 spec 求差，非空即拒。

覆盖：纯判据 4 例（含 fail-closed 空 spec）+ git 端到端 2 例（拦住 / 放行）。

运行：py -m pytest tests/unit/test_safe_commit_expect_spec.py -v
"""
import json
import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import safe_commit as sc  # noqa: E402


def _spec(tmp_path, paths):
    p = tmp_path / "spec.json"
    rows = ["| %s | W1006 | 本批 |" % x for x in paths]
    p.write_text(json.dumps({"file_index_rows": rows}, ensure_ascii=False), encoding="utf-8")
    return p


def test_spec_paths_parsed_from_rows(tmp_path):
    p = _spec(tmp_path, ["a.py", "docs/b.md"])
    spec = json.loads(p.read_text(encoding="utf-8"))
    assert sc._spec_paths(spec) == ["a.py", "docs/b.md"]


def test_plan_spec_subset_ok():
    ok, extra, missing = sc._plan_spec(["a.py"], ["a.py", "b.md"])
    assert ok is True and extra == [] and missing == ["b.md"]


def test_plan_spec_extra_rejected():
    ok, extra, _ = sc._plan_spec(["a.py", "other.py"], ["a.py"])
    assert ok is False and extra == ["other.py"]


def test_plan_spec_empty_spec_fail_closed():
    ok, extra, _ = sc._plan_spec(["a.py"], [])
    assert ok is False and extra == ["a.py"]


def test_plan_spec_empty_index_not_fatal():
    """索引空（尚未 add）不算代提——只提示缺件。"""
    ok, extra, missing = sc._plan_spec([], ["a.py"])
    assert ok is True and missing == ["a.py"]


def _git(repo, *args):
    return subprocess.run(["git", "-C", str(repo)] + list(args), capture_output=True, text=True, encoding="utf-8")


def _repo(tmp_path):
    repo = tmp_path / "r"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "t@t")
    _git(repo, "config", "user.name", "t")
    (repo / "a.py").write_text("a\n", encoding="utf-8")
    _git(repo, "add", "a.py")
    _git(repo, "commit", "-q", "-m", "init")
    return repo


def test_cli_blocks_extra_staged(tmp_path):
    repo = _repo(tmp_path)
    (repo / "a.py").write_text("a2\n", encoding="utf-8")
    (repo / "foreign.py").write_text("x\n", encoding="utf-8")
    _git(repo, "add", "a.py", "foreign.py")
    spec = _spec(tmp_path, ["a.py"])
    r = subprocess.run([sys.executable, str(SCRIPTS_DIR / "safe_commit.py"), "-m", "t",
                        "--expect-spec", str(spec)], cwd=repo, capture_output=True, text=True, encoding="utf-8")
    assert r.returncode == 1, r.stdout + r.stderr
    assert "spec 之外" in r.stdout and "foreign.py" in r.stdout
    log = _git(repo, "log", "--oneline").stdout
    assert log.count("\n") == 1  # 仍只有 init 一笔


def test_cli_allows_index_subset(tmp_path):
    repo = _repo(tmp_path)
    (repo / "a.py").write_text("a3\n", encoding="utf-8")
    _git(repo, "add", "a.py")
    spec = _spec(tmp_path, ["a.py", "b.md"])
    r = subprocess.run([sys.executable, str(SCRIPTS_DIR / "safe_commit.py"), "-m", "ok",
                        "--expect-spec", str(spec)], cwd=repo, capture_output=True, text=True, encoding="utf-8")
    assert r.returncode == 0, r.stdout + r.stderr
    assert _git(repo, "log", "--oneline").stdout.count("\n") == 2
