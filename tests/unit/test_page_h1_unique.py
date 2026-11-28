r"""W1349/W1352 站点页面 H1 唯一性判据（全站）。

## 为什么测这个

W1347 批量改 `<h1>` 时暴露了两页**正文 header 复制 hero 标题**的存量缺陷
（`character-semantic-network` / `theological-intervention-network`，各含 2 个同句 `<h1>`）。
单 h1 是页面大纲与 SEO 的基本契约：重复会让读屏与抓取各读两次标题；批量改标题时两处必须
同步改，漏一处就是「标题与正文不一致」的静默缺陷。W1349 先覆盖 `site/data`，W1352 全站化。

## 口径（W1352）

- 扫描 `site/**/*.html`，排除模板壳 `site/_template.html` 与 `site/data/_shell.html`；
- **重定向存根豁免**：带 `<meta http-equiv="refresh">` 的页面不参与判定——与第 62 槽
  `check_reader_integrity` C3 同口径（内容页才判「恰 1 个 h1」，跳转壳页无正文；
  现存一例 `site/reader/themes/index.html` 已并入 themes-hub）；
- **先剥 HTML 注释**再数：模板注释里会写 `<h1>`/`<title>` 字样（W1348 实证），
  不剥会假红（把注释里的示例当标题）；
- 每页恰好 1 个 `<h1>`，且内容非空。
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SITE = ROOT / "site"
SKIP = {"_template.html", "data/_shell.html"}
COMMENT = re.compile(r"<!--.*?-->", re.S)
H1 = re.compile(r"<h1\b[^>]*>(.*?)</h1>", re.S)
REDIRECT = re.compile(r"<meta[^>]+http-equiv=[\"']refresh[\"']", re.I)


def _texts():
    for p in sorted(SITE.rglob("*.html")):
        rel = p.relative_to(SITE).as_posix()
        if rel in SKIP:
            continue
        txt = COMMENT.sub("", p.read_text(encoding="utf-8"))
        if REDIRECT.search(txt):
            continue
        yield rel, txt


def test_each_page_has_exactly_one_h1():
    bad = [(rel, len(H1.findall(txt))) for rel, txt in _texts() if len(H1.findall(txt)) != 1]
    assert not bad, "H1 数量不等于 1 的页面：%r" % (bad,)


def test_h1_not_empty():
    empty = []
    for rel, txt in _texts():
        m = H1.search(txt)
        if m and not m.group(1).strip():
            empty.append(rel)
    assert not empty, "H1 内容为空的页面：%r" % (empty,)
