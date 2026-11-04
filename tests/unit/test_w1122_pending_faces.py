"""W1122 单元测试 · 补段工具的**双面独立判定**（根修遗留 A：单面「已立段」判定）。

病根（W1120 批登记的遗留 A）：backfill_changelog.collect_pending 的「已立段」判定
**只看 CHANGELOG 一面** ⇒ 某批若 CHANGELOG 已立段而 file-index 未立段 ⇒ 被判「已立段」
⇒ 跳过 ⇒ **file-index 段永远补不上**（双面判定 ⇒ 两面分判 ⇒ 只补缺的那一面）。

运行：py -3 -m pytest tests/unit/test_w1122_pending_faces.py -v
"""
import json
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import backfill_changelog as bf  # noqa: E402

SPEC = {
    "batch": "W2000",
    "date": "2026-11-04",
    "title": "W2000 测试批",
    "desc": "测试",
    "head_entry": "2026-11-04（W2000 测试批）",
    "head_sentence": "测试",
    "changelog_body": "\n\nbody\n",
    "milestone_block": "- **W2000 测试批**：内容",
    "agents_note": "2026-11-04（W2000）测试",
    "file_index_rows": ["| a.py | W2000 | 本批工具/产物 |"],
}


def _write_spec(tmp_path):
    p = tmp_path / "_w2000_spec.json"
    p.write_text(json.dumps(SPEC, ensure_ascii=False), encoding="utf-8")
    return str(p)


def _install(monkeypatch, tmp_path, cl_text, fi_text):
    """注入合成两面内容 + 单个 spec 文件。"""
    spec_path = _write_spec(tmp_path)

    def fake_load(path):
        if path == "CHANGELOG.md":
            return cl_text, "\n"
        if path == "scripts/output/file-index.md":
            return fi_text, "\n"
        return "", "\n"

    monkeypatch.setattr(bf, "load", fake_load)
    monkeypatch.setattr(bf.glob, "glob", lambda pattern: [spec_path])


def test_both_faces_missing_means_both_need_backfill(monkeypatch, tmp_path):
    """正样本：两面皆未立段 ⇒ 两面都待补。"""
    _install(monkeypatch, tmp_path, "### W1999（2026-11-01）：旧段\n", "## W1999 旧段（2026-11-01）\n")
    faces, _est, _fi = bf.collect_pending_faces()
    assert len(faces) == 1
    w, _spec, need_cl, need_fi = faces[0]
    assert w == 2000
    assert need_cl is True and need_fi is True


def test_changelog_only_established_means_only_file_index_pending(monkeypatch, tmp_path):
    """核心正样本：CHANGELOG 面已立段、file-index 面未立段 ⇒ **只判 file-index 面待补**。

    这是原单面判定的病灶：原实现会把该批判为「已立段」而整批跳过 ⇒ file-index 段补不上。
    """
    _install(monkeypatch, tmp_path,
             "### W2000（2026-11-04）：测试批\n\nbody\n\n### W1999（2026-11-01）：旧段\n",
             "## W1999 旧段（2026-11-01）\n")
    faces, _est, _fi = bf.collect_pending_faces()
    assert len(faces) == 1, "一面已立一面未立必须仍被判为待补（原单面判定会漏判）"
    w, _spec, need_cl, need_fi = faces[0]
    assert w == 2000
    assert need_cl is False, "CHANGELOG 面已立段 ⇒ 不得重复补（防同号双段）"
    assert need_fi is True, "file-index 面未立段 ⇒ 必须判为待补（这就是遗留 A 的修复点）"


def test_file_index_only_established_means_only_changelog_pending(monkeypatch, tmp_path):
    """正样本：file-index 面已立段、CHANGELOG 面未立段 ⇒ 只判 CHANGELOG 面待补。"""
    _install(monkeypatch, tmp_path,
             "### W1999（2026-11-01）：旧段\n",
             "## W2000 测试批（2026-11-04）\n\n| 文件 | W | 说明 |\n|---|---|---|\n\n\n"
             "## W1999 旧段（2026-11-01）\n")
    faces, _est, _fi = bf.collect_pending_faces()
    assert len(faces) == 1
    w, _spec, need_cl, need_fi = faces[0]
    assert w == 2000
    assert need_cl is True and need_fi is False


def test_both_faces_established_means_not_pending(monkeypatch, tmp_path):
    """正样本：两面皆已立段 ⇒ 不待补（不重复补段）。"""
    _install(monkeypatch, tmp_path,
             "### W2000（2026-11-04）：测试批\n\nbody\n\n### W1999（2026-11-01）：旧段\n",
             "## W2000 测试批（2026-11-04）\n\n| 文件 | W | 说明 |\n|---|---|---|\n\n\n"
             "## W1999 旧段（2026-11-01）\n")
    faces, _est, _fi = bf.collect_pending_faces()
    assert faces == [], "两面皆已立段 ⇒ 不得判为待补"


def test_collect_pending_keeps_legacy_shape_and_semantics(monkeypatch, tmp_path):
    """兼容性：collect_pending 的返回形状与语义不变（按 CHANGELOG 面判定·既有调用方不受影响）。"""
    _install(monkeypatch, tmp_path,
             "### W2000（2026-11-04）：测试批\n\nbody\n\n### W1999（2026-11-01）：旧段\n",
             "## W1999 旧段（2026-11-01）\n")
    pending, established = bf.collect_pending()
    assert pending == [], "CHANGELOG 面已立段 ⇒ 旧语义（只看 CHANGELOG 面）判为非待补"
    assert 2000 in established
