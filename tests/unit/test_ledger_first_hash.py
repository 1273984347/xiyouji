"""W1272 单元测试·台账登记与回填面（ledger_backfill + preflight_check 共享判据）

覆盖三处同族缺陷（均属「台账登记/回填面」）：
  D1 首笔倒置——git log 默认倒序（最新在前）⇒ wnum_commit_index 取到的「首笔」
     实为末笔 ⇒ 台账 hash 列（语义=首笔）会被写坏；
  D2 列位错位——locate_cells 取 touches=n-2 ⇒ 9 格现行行指到「本会话」列 ⇒
     回填 touches 写错格（与 preflight 实际消费面不一致）；
  D3 认领行形态——append-claim 产 7 格行 ⇒ locate_cells 直接 fail-closed ⇒
     认领行无法收官回填 ⇒ 该批永久占着 touches 挡死后来者。

运行：py -3 -m pytest tests/unit/test_ledger_first_hash.py -v
"""
import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import ledger_backfill  # noqa: E402
from preflight_check import wnum_commit_index  # noqa: E402

GIT_CANDIDATES = [r"C:\Program Files\Git\bin\git.exe", "git"]


def _git_bin() -> str:
    for cand in GIT_CANDIDATES:
        if cand == "git":
            found = shutil.which("git")
            if found:
                return found
        elif os.path.exists(cand):
            return cand
    raise RuntimeError("git 不可用·本组用例需真实 git 命令")


def _run_git(repo: Path, *args: str) -> str:
    r = subprocess.run([_git_bin(), *args], cwd=str(repo), capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
    assert r.returncode == 0, "git %s 失败：%s" % (" ".join(args), r.stderr[:200])
    return r.stdout


def _make_repo(tmp_path: Path, subjects) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    _run_git(repo, "init")
    for i, subj in enumerate(subjects):
        (repo / "f.txt").write_text("x%d\n" % i, encoding="utf-8")
        _run_git(repo, "add", "f.txt")
        _run_git(repo, "-c", "user.name=Tester", "-c", "user.email=t@example.com",
                "commit", "-m", subj)
    return repo


def test_git_commit_index_returns_earliest_commit(tmp_path, monkeypatch):
    """D1 端到端：多笔批自动反填的 hash 必须是**最早一笔**（首笔）·不是末笔。"""
    repo = _make_repo(tmp_path, [
        "chore(scope): W9999 第一笔",
        "chore(scope): W9999 第二笔",
        "chore(scope): W9999 第三笔",
        "chore(scope): W9999 第四笔",
    ])
    ordered = _run_git(repo, "log", "--reverse", "--format=%H").split()
    monkeypatch.chdir(repo)
    idx = ledger_backfill.git_commit_index()
    assert 9999 in idx, "描述段开头 W 形态的批次号应被识别"
    assert idx[9999][0] == 4, "提交数应为 4"
    first = idx[9999][1]
    assert ordered[0].startswith(first), "首笔应是最早提交 %s·实得 %s" % (ordered[0], first)
    assert not ordered[-1].startswith(first), "首笔不得是末笔 %s" % ordered[-1]


def test_order_contract_is_load_bearing():
    """D1 判据区分力：同一批提交·顺序不同 ⇒ 取到的「首笔」不同 ⇒ 顺序契约不可省。"""
    lines = ["aaa1111 chore(scope): W9999 第一笔", "bbb2222 chore(scope): W9999 第二笔"]
    fwd = wnum_commit_index(lines)
    rev = wnum_commit_index(list(reversed(lines)))
    assert fwd[9999][1] == "aaa1111"
    assert rev[9999][1] == "bbb2222"
    assert fwd[9999][1] != rev[9999][1]


def test_locate_cells_touches_targets_last_cell():
    """D2：touches 取末格（9 格现行行 + 7 格旧行皆成立）⇒ 与 preflight 消费面同源。"""
    row9 = "| W900 | 主题 | aaa1111 | bbb2222 | 已收官（x） | 主会话 | — | 本会话（W900） | f1.py, f2.md |"
    cells9 = [c.strip() for c in row9.strip().strip("|").split("|")]
    loc9 = ledger_backfill.locate_cells(cells9)
    assert loc9["touches"] == len(cells9) - 1
    assert cells9[loc9["touches"]] == "f1.py, f2.md"
    assert cells9[loc9["hash"]] == "aaa1111"
    assert cells9[loc9["session"]] == "主会话"
    row7 = "| W900 | 主题 | aaa1111 | bbb2222 | 已收官（x） | 主会话 | f1.py |"
    cells7 = [c.strip() for c in row7.strip().strip("|").split("|")]
    loc7 = ledger_backfill.locate_cells(cells7)
    assert loc7["touches"] == len(cells7) - 1


def test_append_claim_row_is_parseable(tmp_path):
    """D3：认领行须是现行 9 格形态 ⇒ 能被 locate_cells 解析 ⇒ 收官时可回填。"""
    p = tmp_path / "ledger.md"
    p.write_text(
        "| W# | 主题 | 关联 commit | CHANGELOG 版段 | 状态 | 认领会话 | touches |\n"
        "| W900 | x | a | b | 已收官（x） | s | t |\n", encoding="utf-8")
    ns = argparse.Namespace(w=1272, desc="测试描述", session="主会话@mavis",
                           touches="f1.py · f2.md")
    assert ledger_backfill.cmd_append_claim(ns, str(p)) == 0
    row = [ln for ln in ledger_backfill.read_ledger(str(p)) if ln.startswith("| W1272")][0]
    cells = [c.strip() for c in row.strip().strip("|").split("|")]
    assert len(cells) == 9, "认领行应为现行 9 格形态·实得 %d 格" % len(cells)
    loc = ledger_backfill.locate_cells(cells)
    assert cells[loc["status"]].startswith("在途")
    assert cells[loc["touches"]] == "f1.py · f2.md"


def test_append_claim_rejects_bare_pipe(tmp_path):
    """D3 防线：单元格内裸竖线会致列错位（E-253 同族）⇒ 写入前必须 fail-closed。"""
    p = tmp_path / "ledger.md"
    p.write_text("| W# | 主题 | a | b | 已收官（x） | s | t |\n", encoding="utf-8")
    ns = argparse.Namespace(w=1273, desc="含|竖线的描述", session="主会话", touches="a.py")
    assert ledger_backfill.cmd_append_claim(ns, str(p)) == 1
    assert not any(ln.startswith("| W1273")
                    for ln in ledger_backfill.read_ledger(str(p)))
