"""check_folder_docs.py 跨平台新鲜度门禁测试（W780）。

背景：gen_folder_docs.py@W779 的 index.md/README.md 是「生成时点快照」，目录内容
增删后清单过期且无机器防线。第 45 槽（check_folder_docs.py）把该漂移面收进门禁。

跨平台纪律（pitfalls「latent 三问 + 双平台断言禁例」）：合成树断言全部基于名字符串
（sorted(str)=码点序两平台一致）；零 os.name/盘符/大小写语义断言；临时目录注入，
不触真实仓库——真实执行位=CI（Linux）与本地（Windows）同断言。
"""

import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import check_folder_docs as cfd  # noqa: E402
import gen_folder_docs as gen  # noqa: E402

GATE = SCRIPTS / "check_folder_docs.py"


def _run(*args, timeout=120):
    return subprocess.run(
        [sys.executable, str(GATE), *args],
        capture_output=True, text=True, timeout=timeout, cwd=str(ROOT),
    )


@pytest.fixture()
def synth_tree(tmp_path, monkeypatch):
    """合成在管树：alpha/（a.md+b.py+两件套），ROOT 与 gitignored 缓存指向它。"""
    monkeypatch.setattr(gen, "ROOT", str(tmp_path))
    monkeypatch.setattr(gen, "_GITIGNORED_DIRS", set())
    d1 = tmp_path / "alpha"
    d1.mkdir()
    (d1 / "a.md").write_text("", encoding="utf-8")
    (d1 / "b.py").write_text("", encoding="utf-8")
    for kind in ("index.md", "README.md"):
        (d1 / kind).write_text(gen.render(str(d1), kind), encoding="utf-8", newline="\n")
    return d1


def _codes(fails):
    return [f.split(" ")[0] for f in fails]


def test_fresh_tree_passes(synth_tree):
    assert cfd.check_dir(str(synth_tree)) == []


def test_added_file_detected(synth_tree):
    (synth_tree / "c.py").write_text("", encoding="utf-8")
    assert "C3" in _codes(cfd.check_dir(str(synth_tree)))


def test_removed_file_detected(synth_tree):
    (synth_tree / "b.py").unlink()
    assert "C3" in _codes(cfd.check_dir(str(synth_tree)))


def test_added_subdir_detected(synth_tree):
    (synth_tree / "sub").mkdir()
    assert "C2" in _codes(cfd.check_dir(str(synth_tree)))


def test_missing_readme_detected(synth_tree):
    (synth_tree / "README.md").unlink()
    assert "C1" in _codes(cfd.check_dir(str(synth_tree)))


def test_missing_index_detected(synth_tree):
    (synth_tree / "index.md").unlink()
    assert "C1" in _codes(cfd.check_dir(str(synth_tree)))


def test_tampered_list_detected(synth_tree):
    idx = synth_tree / "index.md"
    idx.write_text(idx.read_text(encoding="utf-8").replace("- `a.md`\n", ""),
                   encoding="utf-8", newline="\n")
    assert "C3" in _codes(cfd.check_dir(str(synth_tree)))


def test_title_drift_detected(synth_tree):
    idx = synth_tree / "index.md"
    idx.write_text(idx.read_text(encoding="utf-8").replace("# 文件索引 · alpha",
                                                           "# 文件索引 · alpha-old"),
                   encoding="utf-8", newline="\n")
    assert "C4" in _codes(cfd.check_dir(str(synth_tree)))


def test_mangled_template_detected(synth_tree):
    (synth_tree / "index.md").write_text("# 手写清单\n\n随便写的\n", encoding="utf-8")
    fails = cfd.check_dir(str(synth_tree))
    assert fails and "结构不合生成器模板" in fails[0]


def test_parse_index_roundtrip(synth_tree):
    parsed = cfd.parse_index((synth_tree / "index.md").read_text(encoding="utf-8"))
    assert parsed is not None
    assert parsed["title"] == "alpha"
    assert parsed["sub_n"] == 0
    assert parsed["file_n"] == 2
    assert parsed["files"] == ["a.md", "b.py"]


def test_in_scope_excludes_governed_trees(tmp_path, monkeypatch):
    monkeypatch.setattr(gen, "ROOT", str(tmp_path))
    governed = tmp_path / "docs" / "10-方法论沉淀"
    governed.mkdir(parents=True)
    normal = tmp_path / "scripts"
    normal.mkdir()
    assert gen.in_scope(str(governed)) is False
    assert gen.in_scope(str(normal)) is True


def test_self_test_cli_exit_zero():
    r = _run("--self-test")
    assert r.returncode == 0, r.stdout + r.stderr
    assert "self-test 7 例（1 正 6 负）：全过" in r.stdout


def test_regen_restores_freshness(synth_tree):
    """漂移后重跑生成器 --force 单目录渲染即可恢复新鲜（修复路径存在性）。"""
    (synth_tree / "c.py").write_text("", encoding="utf-8")
    assert "C3" in _codes(cfd.check_dir(str(synth_tree)))
    for kind in ("index.md", "README.md"):
        (synth_tree / kind).write_text(gen.render(str(synth_tree), kind),
                                       encoding="utf-8", newline="\n")
    # c.py 仍在磁盘 → 清单更新后反而新鲜
    assert cfd.check_dir(str(synth_tree)) == []
    assert os.path.isfile(synth_tree / "c.py")


def _patch_gen_root(monkeypatch, tmp_path):
    """先打 ROOT 补丁再动 gen.render——跨盘 relpath（C: 临时目录 vs D: 仓库根）会炸。"""
    monkeypatch.setattr(gen, "ROOT", str(tmp_path))
    monkeypatch.setattr(gen, "_GITIGNORED_DIRS", set())


def test_case_collides_detection(tmp_path):
    """大小写变体目录必须可判定（两平台同构：listdir 真名小写比对·不依赖 fs 语义）。"""
    gov = tmp_path / "gov"
    gov.mkdir()
    (gov / "INDEX.md").write_text("# 大写索引\n", encoding="utf-8")
    assert gen.case_collides(str(gov)) is True
    lower = tmp_path / "lower"
    lower.mkdir()
    (lower / "readme.md").write_text("# 小写变体\n", encoding="utf-8")
    assert gen.case_collides(str(lower)) is True
    normal = tmp_path / "normal"
    normal.mkdir()
    assert gen.case_collides(str(normal)) is False


def test_refresh_repairs_stale_owned(tmp_path, monkeypatch):
    """陈旧的生成物（带生成来源标记）必须被 --refresh 修复——门禁修复路径可用性。"""
    _patch_gen_root(monkeypatch, tmp_path)
    d1 = tmp_path / "alpha"
    d1.mkdir()
    (d1 / "a.md").write_text("", encoding="utf-8")
    for kind in ("index.md", "README.md"):
        (d1 / kind).write_text(gen.render(str(d1), kind), encoding="utf-8", newline="\n")
    (d1 / "new.py").write_text("", encoding="utf-8")  # 制造漂移
    assert "C3" in _codes(cfd.check_dir(str(d1)))
    monkeypatch.setattr(sys, "argv", ["gen_folder_docs.py", "--refresh"])
    assert gen.main() == 0
    assert cfd.check_dir(str(d1)) == []


def test_refresh_preserves_hand_owned(tmp_path, monkeypatch):
    """人工维护件（无生成来源标记）必须被 --refresh 原样保留——防 --force 式误轰。"""
    _patch_gen_root(monkeypatch, tmp_path)
    d1 = tmp_path / "hand"
    d1.mkdir()
    (d1 / "a.md").write_text("", encoding="utf-8")
    hand = "# 手工维护目录\n\n自定义内容（无生成来源标记）\n"
    (d1 / "README.md").write_text(hand, encoding="utf-8", newline="\n")
    monkeypatch.setattr(sys, "argv", ["gen_folder_docs.py", "--refresh"])
    assert gen.main() == 0
    assert (d1 / "README.md").read_text(encoding="utf-8") == hand
