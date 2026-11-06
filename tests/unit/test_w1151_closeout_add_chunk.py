"""W1151 回归锁 · batch_closeout._add_paths 巨批分块（WinError 206 根修）。

W1151 实证：全站 INLINED 副本同步 851 页 ⇒ 单条 `git add` 命令行超 Windows
CreateProcess 32767 字符上限 ⇒ FileNotFoundError 直接炸链。根修 = 分块 add
（git add 暂存区跨调用累积·结果与单条等价）。

运行：py -3 -m pytest tests/unit/test_w1151_closeout_add_chunk.py -v
"""
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import batch_closeout as bco  # noqa: E402


class _Rec:
    """记录每次 run() 的实参并恒返回成功。"""

    def __init__(self):
        self.calls = []

    def __call__(self, args, **kw):
        self.calls.append(args)
        return (0, "")


def test_add_paths_chunks_large_batches(monkeypatch, tmp_path):
    """巨批路径集 ⇒ 多条 git add·每块 ≤200 条。"""
    rec = _Rec()
    monkeypatch.setattr(bco, "run", rec)
    monkeypatch.setattr(bco, "ROOT", str(tmp_path))
    paths = [f"site/data/page-{i:03d}.html" for i in range(450)]
    for p in paths:
        (tmp_path / p).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / p).write_text("x", encoding="utf-8")
    assert bco._add_paths(paths) is True
    assert len(rec.calls) == 3  # 450 = 200 + 200 + 50
    for c in rec.calls:
        assert c[0] == "git" and c[1] == "add" and c[2] == "--"
        assert len(c) - 3 <= 200


def test_add_paths_single_chunk_small_batches(monkeypatch, tmp_path):
    """小批保持单块（≤200 一条·不退化）。"""
    rec = _Rec()
    monkeypatch.setattr(bco, "run", rec)
    monkeypatch.setattr(bco, "ROOT", str(tmp_path))
    paths = ["a.md", "b.md"]
    for p in paths:
        (tmp_path / p).write_text("x", encoding="utf-8")
    assert bco._add_paths(paths) is True
    assert len(rec.calls) == 1
    assert rec.calls[0][3:] == paths


def test_add_paths_aborts_on_block_failure(monkeypatch, tmp_path):
    """任一块失败 ⇒ 整体中止（fail-closed·与单条语义一致）。"""
    rec = _Rec()
    monkeypatch.setattr(bco, "run", rec)
    monkeypatch.setattr(bco, "ROOT", str(tmp_path))
    paths = [f"site/page-{i}.html" for i in range(201)]
    for p in paths:
        (tmp_path / p).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / p).write_text("x", encoding="utf-8")
    rec.calls = []

    def fail_second(args, **kw):
        rec.calls.append(args)
        return (0, "") if len(rec.calls) == 1 else (128, "fatal: bad pathspec")

    monkeypatch.setattr(bco, "run", fail_second)
    assert bco._add_paths(paths) is False
    assert len(rec.calls) == 2  # 第二块失败即止·不再发第三块
