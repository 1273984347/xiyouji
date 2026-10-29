r"""BL-33 回归锁：inline_css.py 根级已内联页的重同步路径

## 缺口取证

W875 为「根级页面用 tokens.css 无前缀」加了 `depth == 0 → skip-no-link` 的**无条件**
早退，副作用是把根级**已内联**页（site/dukou-engine.html / site/_template.html）的
重同步路径一并堵死——W876 只能手工靶向修，此后两页内联块长期停在旧版：缺 W856
brand-mark / W895 kpi-row / W885 hero-ornament / W939 ico 等 74–79 行，且 _template
残留 1320px 字面量与旧赭金、旧 accent 值。本批撤除早退，改由「无外链且未内联」判据接管。

## 判据

  R1 根级已内联页 + --force ⇒ re-synced（早退不得复活）
  R2 外链页 + --force（不带 --inline-links）⇒ skip-external（W895 护栏不被本改动破坏）
"""
import inline_css


def _prepare(tmp_path, monkeypatch):
    """把 SITE_DIR/TOKENS/SYSTEM 重定向到 tmp_path，隔离真实站点。"""
    monkeypatch.setattr(inline_css, "SITE_DIR", str(tmp_path))
    (tmp_path / "tokens.css").write_text(":root{--a:1}", encoding="utf-8")
    (tmp_path / "system.css").write_text(".x{color:red}", encoding="utf-8")
    monkeypatch.setattr(inline_css, "TOKENS", str(tmp_path / "tokens.css"))
    monkeypatch.setattr(inline_css, "SYSTEM", str(tmp_path / "system.css"))


def _mk(tmp_path, name, html):
    p = tmp_path / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(html, encoding="utf-8")
    return str(p)


def test_r1_root_inlined_page_is_resynced(tmp_path, monkeypatch):
    _prepare(tmp_path, monkeypatch)
    p = _mk(tmp_path, "dukou-engine.html", "<head><!-- INLINED CSS --><style>.old{}</style></head>")
    assert inline_css.process(p, force=True, dry=True) == "re-synced"


def test_r1b_root_inlined_page_skipped_without_force(tmp_path, monkeypatch):
    _prepare(tmp_path, monkeypatch)
    p = _mk(tmp_path, "_template.html", "<head><!-- INLINED CSS --><style>.old{}</style></head>")
    assert inline_css.process(p, force=False, dry=True) == "skip-inlined"


def test_r2_external_page_still_guarded(tmp_path, monkeypatch):
    _prepare(tmp_path, monkeypatch)
    p = _mk(tmp_path, "data/ext.html", '<head><link rel="stylesheet" href="../tokens.css"></head>')
    assert inline_css.process(p, force=True, dry=True) == "skip-external"
