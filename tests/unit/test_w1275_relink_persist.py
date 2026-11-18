"""W1275 单元测试·公共层外链化的持久性与口径同源（scripts/relink_public_css.py + scripts/inline_css.py）

背景（W1275 实测取证）：
  ① 外链化后页内仍带「INLINED CSS」标记 ⇒ scripts/inline_css.py --force 会把公共层
     重新内联 ⇒ A 方案外链化被静默回退（无任何报错）⇒ 标记与外链形态必须同源。
  ② relink 的公共层索引若拿「带注释的原文」比对页内副本 ⇒ 命中面被系统性低估
     （副本是 inline_css.strip_comments 的产物）⇒ 公共层规则残留页内 ⇒ 残留规则落在
     外链公共层之后 ⇒ 覆写层级反转（实测 body 16px→15px）⇒ 索引口径必须与传播端同源。

运行：py -3 -m pytest tests/unit/test_w1275_relink_persist.py -v
"""
import shutil
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import inline_css  # noqa: E402
import relink_public_css as rlc  # noqa: E402

# W1275：pytest 默认 tmp_path 落在系统盘（C:）而 site/ 在 D: ⇒ os.path.relpath 跨盘符报错
# ⇒ 临时页一律落在仓内 tmpe（gitignore 临时区·不入库）。
_TMP_ROOT = Path(__file__).resolve().parent.parent.parent / "tmpe" / "pytest_w1275"


def _tmpdir(name):
    path = _TMP_ROOT / name
    if path.exists():
        shutil.rmtree(path, ignore_errors=True)
    path.mkdir(parents=True, exist_ok=True)
    return path


def _public_css():
    """公共层原件的传播形态（剥块注释·与 inline_css 一致）。"""
    parts = []
    for name in rlc.PUBLIC_FILES:
        path = Path(rlc.SITE) / name
        parts.append(inline_css.strip_comments(path.read_text(encoding="utf-8")))
    return "\n\n".join(parts)


def _mk_page(tmp_path, name, html):
    path = tmp_path / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    return str(path)


def test_relink_output_has_two_links_and_no_marker():
    tmp_path = _tmpdir("relink_main")
    """改造后：两个 link 齐全 + 残留内联标记被清除 + 页私有层保留。"""
    html = ("<html><head>\n<!-- INLINED CSS (tokens.css + system.css) -->\n<style>\n"
            + _public_css() + "\n.priv-layer{color:red}\n</style>\n</head><body>x</body></html>")
    page = _mk_page(tmp_path, "en/x.html", html)
    idx = rlc.public_rule_index()
    status, _before, _after, _note = rlc.relink_page(page, idx, apply=True)
    out = Path(page).read_text(encoding="utf-8")
    assert status == "changed", "应判定为改造（公共层副本足够多）"
    assert out.count("<link") == 2, "必须生成两个公共层 link"
    assert rlc.rel_href(page, "tokens.css") in out, "tokens link 的相对路径须按页目录计算"
    assert rlc.rel_href(page, "system.css") in out, "system link 的相对路径须按页目录计算"
    assert "INLINED CSS" not in out, "外链页不得再留「内联副本」标记（否则 --force 会转回内联）"
    assert ".priv-layer{color:red}" in out, "页私有层必须保留"


def test_public_index_is_strip_comments_synced():
    """索引口径必须与传播端同源（剥注释）⇒ 带注释的公共层规则也要能被命中。"""
    idx = rlc.public_rule_index()
    css = inline_css.strip_comments((Path(rlc.SITE) / "system.css").read_text(encoding="utf-8"))
    hit = 0
    for sels, body, _s, _e in rlc._top_rules(css):
        if body in idx.get(sels, set()):
            hit += 1
    assert hit > 0, "剥注释后的公共层规则必须能逐字命中索引"


def test_marker_cleaned_then_idempotent():
    tmp_path = _tmpdir("relink_marker")
    """已外链页的残留标记：首次清理 ⇒ 再跑不再改（幂等）。"""
    target = tmp_path / "en" / "y.html"
    href_t = rlc.rel_href(str(target), "tokens.css")
    href_s = rlc.rel_href(str(target), "system.css")
    html = ("<html><head>\n<!-- INLINED CSS (tokens.css + system.css) -->\n"
            "<link rel=\"stylesheet\" href=\"" + href_t + "\">\n"
            "<link rel=\"stylesheet\" href=\"" + href_s + "\">\n"
            "<style>.priv{color:red}</style>\n</head><body>x</body></html>")
    page = _mk_page(tmp_path, "en/y.html", html)
    idx = rlc.public_rule_index()
    status, _b, _a, _n = rlc.relink_page(page, idx, apply=True)
    out = Path(page).read_text(encoding="utf-8")
    assert status == "cleaned", "已外链但残留标记 ⇒ 应判定为清理"
    assert "INLINED CSS" not in out, "残留标记必须被清除"
    status2, _b2, _a2, _n2 = rlc.relink_page(page, idx, apply=True)
    assert status2 == "already", "清理后再次运行应无改动（幂等）"


def test_external_page_not_reinlined_by_force(monkeypatch):
    tmp_path = _tmpdir("inline_ext")
    """外链页（即便残留标记）被 --force 处理时 ⇒ 跳过外链转内联（不静默回退 A 方案）。"""
    monkeypatch.setattr(inline_css, "SITE_DIR", str(tmp_path))
    (tmp_path / "tokens.css").write_text(":root{--a:1}", encoding="utf-8")
    (tmp_path / "system.css").write_text(".x{color:red}", encoding="utf-8")
    monkeypatch.setattr(inline_css, "TOKENS", str(tmp_path / "tokens.css"))
    monkeypatch.setattr(inline_css, "SYSTEM", str(tmp_path / "system.css"))
    page = _mk_page(tmp_path, "en/ext.html",
                    "<head><!-- INLINED CSS -->\n"
                    "<link rel=\"stylesheet\" href=\"../tokens.css\">\n"
                    "<style>.priv{color:red}</style></head>")
    assert inline_css.process(page, force=True, dry=False) == "skip-external"
    assert "INLINED CSS" in Path(page).read_text(encoding="utf-8"), "不得改写外链页"


def test_inlined_page_still_resynced(monkeypatch):
    tmp_path = _tmpdir("inline_inl")
    """负向：内联页（无 link）在 --force 下仍须重同步（既有行为不被本批破坏）。"""
    monkeypatch.setattr(inline_css, "SITE_DIR", str(tmp_path))
    (tmp_path / "tokens.css").write_text(":root{--a:1}", encoding="utf-8")
    (tmp_path / "system.css").write_text(".x{color:red}", encoding="utf-8")
    monkeypatch.setattr(inline_css, "TOKENS", str(tmp_path / "tokens.css"))
    monkeypatch.setattr(inline_css, "SYSTEM", str(tmp_path / "system.css"))
    page = _mk_page(tmp_path, "en/inl.html",
                    "<head><!-- INLINED CSS -->\n<style>.old{}</style></head>")
    assert inline_css.process(page, force=True, dry=True) == "re-synced"
