"""docs_index.py 跨平台排序稳定性测试（W773·CI 首跑分歧根修）。

背景：`sorted(Path)` 在 Windows 用 normcase（大小写不敏感）、Linux 用大小写
敏感——docs/00-导读 的 `design.md` 与 `10-方法论沉淀` 的大小写混排条目在
两平台排序不同，第 17 门禁的 INDEX.md 产物级校验因此「本地（Windows）绿 /
CI（Linux）红」。修法 = scan_docs 显式 `str(p).lower()` 排序键（W773）。

本测试用合成目录断言该不变量（不依赖运行平台）：
  - 大小写混排条目按小写键排序（Beta 排在 alpha 后）
  - 真实 docs/ 树的条目序满足小写键不变量
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))

import docs_index  # noqa: E402


def _write_md(p: Path, title: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("# %s\n\nbody\n" % title, encoding="utf-8")


def test_scan_docs_entry_order_is_case_insensitive(tmp_path):
    """合成目录：Beta/alpha/Gamma 必须按小写键序（alpha→Beta→Gamma）。

    若退化回裸 sorted(Path)：Linux 上 Gamma/Beta（大写 ASCII 排在 lowercase
    前）会排到 alpha 之前 → 本断言红。**注意**：Windows 的 normcase 与小写键
    等价，本断言在 Windows 上两法均绿——真实执行位是 CI（Linux·gate 17 的
    INDEX 产物级校验），与 W773「CI 才是实证位」同款保护模型。
    """
    sec = tmp_path / "00-导读"
    for name, title in (("Beta.md", "Beta 文档"), ("alpha.md", "alpha 文档"), ("Gamma.md", "Gamma 文档")):
        _write_md(sec / name, title)
    _write_md(sec / "INDEX.md", "应被跳过的索引自身")

    scanned = docs_index.scan_docs(tmp_path)
    entries = scanned["00 · 导读"]
    rels = [rel for _title, rel in entries]
    assert rels == ["00-导读/alpha.md", "00-导读/Beta.md", "00-导读/Gamma.md"], (
        "条目序非小写键序（跨平台不稳定·W773 根修回退？）：%s" % rels)


def test_scan_docs_real_tree_satisfies_lowercase_invariant():
    """真实 docs/ 树：每个板块的条目序必须满足 str(rel).lower() 不变量。"""
    scanned = docs_index.scan_docs(docs_index.DEFAULT_DOCS_DIR)
    assert scanned, "docs/ 扫描结果为空（目录被挪走？）"
    for section, entries in scanned.items():
        rels = [rel for _title, rel in entries]
        assert rels == sorted(rels, key=str.lower), (
            "%s 板块条目序违反小写键不变量（CI Linux 将红）：%s" % (section, rels[:5]))


def test_render_index_disk_matches_generator():
    """磁盘 INDEX.md 与生成器输出逐字节一致（与第 17 门禁同判据·pytest 面兜底）。"""
    output = docs_index.DEFAULT_OUTPUT
    assert output.exists(), "docs/INDEX.md 不存在"
    expected = docs_index.render_index(docs_index.scan_docs(docs_index.DEFAULT_DOCS_DIR))
    assert output.read_text(encoding="utf-8") == expected, (
        "INDEX.md 已过期——运行 python scripts/docs_index.py 重建")
