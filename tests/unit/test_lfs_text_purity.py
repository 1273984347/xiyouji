"""LFS 文本纯净性判据的单测（W1214）。

背景：W1209 的 LFS 迁移把 assets/promo 下的 md/html 也托管进 LFS（排除行被同批整行删除，
排除语义随之消失）⇒ CI 的 actions/checkout 默认不拉 LFS 真身 ⇒ 工作树是指针文本 ⇒
第 45 槽 parse_index() 返回 None ⇒ C2「结构不合生成器模板」× 6 目录 ⇒ Delivery Gate 红
⇒ PR #171 被 required check 硬拦（本地绿是因为工作树有 git lfs checkout 恢复的真身）。

本组单测钉住三件事：
  ① 判据本身：指针内容识别 + 文本扩展名圈定；
  ② 判据能抓：在合成 git 仓里造一个「指针形态」的 md ⇒ 必须命中且只命中它；
  ③ 回归锁：真仓当前 0 命中（有人再把文本文件 LFS 化 ⇒ 本单测当场红）。
"""
from __future__ import annotations

import importlib.util
import pathlib
import subprocess
import sys

import pytest

SCRIPT = pathlib.Path(__file__).resolve().parents[2] / "scripts" / "check_lfs_text_purity.py"
REPO = pathlib.Path(__file__).resolve().parents[2]


def _load():
    spec = importlib.util.spec_from_file_location("check_lfs_text_purity", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_is_pointer_bytes_detects_lfs_pointer():
    mod = _load()
    ptr = (mod.POINTER_SIGNATURE.decode("ascii") + "\noid sha256:" + "0" * 64 + "\nsize 42\n")
    assert mod.is_pointer_bytes(ptr.encode("utf-8")) is True


def test_is_pointer_bytes_rejects_normal_text():
    mod = _load()
    assert mod.is_pointer_bytes("# 文件索引 · promo\n".encode()) is False
    assert mod.is_pointer_bytes(b"") is False
    # 签名不在首行 ⇒ 不是指针（避免误伤正文里提到该 URL 的文档）
    assert mod.is_pointer_bytes(b"prefix\n" + mod.POINTER_SIGNATURE + b"\n") is False


def test_is_text_path_covers_text_and_excludes_binary():
    mod = _load()
    for p in ("a.md", "a.html", "a.py", "a.json", "a.yaml", "a.svg", "A.MD"):
        assert mod.is_text_path(p) is True, p
    for p in ("a.png", "a.jpg", "a.webp", "a.pdf", "a.zip", "a.mp4", "noext"):
        assert mod.is_text_path(p) is False, p


def test_scan_finds_pointer_only_in_synthetic_repo(tmp_path):
    mod = _load()
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    (repo / "plain.md").write_text("# 普通文本\n", encoding="utf-8")
    (repo / "pointer.md").write_text(
        mod.POINTER_SIGNATURE.decode("ascii") + "\noid sha256:" + "0" * 64 + "\nsize 42\n",
        encoding="utf-8",
    )
    (repo / "pic.png").write_bytes(b"\x89PNG\r\n\x1a\n")
    subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True)
    subprocess.run(
        ["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@example.com",
         "commit", "-q", "-m", "synth"],
        check=True,
    )
    n_text, bad = mod.scan_index_text_pointers(str(repo))
    assert bad == ["pointer.md"]
    assert n_text == 2  # plain.md + pointer.md（png 不在文本白名单）


def test_real_repo_has_no_lfs_managed_text_file():
    """回归锁：真仓索引里不得有被 LFS 托管的文本文件（W1214 修复后的现状）。"""
    mod = _load()
    n_text, bad = mod.scan_index_text_pointers(str(REPO))
    assert bad == [], "以下文本文件被 LFS 托管（CI 无 LFS 真身时不可读）：%r" % (bad,)
    assert n_text > 0


def test_gate_mode_is_executable():
    """脚本须能以解释器实跑（--gate 退出码 0）⇒ 提供「实质执行面」证据。

    门禁第 42 槽判「根级脚本覆盖」时，E1 形态（解释器 + scripts/ 路径）与 E3 形态
    （模块 import + 执行标记）都认这条实跑路径——不是靠字符串出现蒙混。
    """
    r = subprocess.run([sys.executable, str(SCRIPT), "--gate"], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    assert r.returncode == 0, r.stdout + r.stderr
    assert "LFS 文本纯净性" in r.stdout


def test_summary_line_carries_failure_items():
    mod = _load()
    green = mod.summary_line(0, 5644, [])
    assert green.startswith(mod.MARKER)
    assert "0 FAIL / 5644 文本文件" in green
    assert "失败项" not in green

    red = mod.summary_line(1, 5644, ["assets/promo/INDEX.md"])
    assert "1 FAIL / 5644 文本文件" in red
    assert "失败项：" in red
    assert "assets/promo/INDEX.md" in red

    many = mod.summary_line(7, 5644, ["p%d" % i for i in range(7)])
    assert "共 7 条" in many
    assert "余 2 条" in many


def test_blob_helpers_fail_closed_on_git_error(monkeypatch):
    """W1214 审查修复锁：cat-file 非零 ⇒ 抛 RuntimeError（空表不得当成 0 FAIL 假绿）。"""
    mod = _load()

    class _Proc:
        returncode = 128
        stdout = b""
        stderr = b"fatal: bad object"

    monkeypatch.setattr(mod.subprocess, "run", lambda *a, **k: _Proc())
    with pytest.raises(RuntimeError):
        mod._blob_sizes("/tmp", ["deadbeef"])
    with pytest.raises(RuntimeError):
        mod._blob_batch("/tmp", ["deadbeef"])
