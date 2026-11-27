r"""W1349 站点页面 H1 唯一性判据。

## 为什么测这个

W1347 批量改 `<h1>` 时暴露了两页**正文 header 复制 hero 标题**的存量缺陷：
`character-semantic-network.html` 与 `theological-intervention-network.html` 各含 2 个
`<h1>`（同句）。单 h1 是页面大纲与 SEO 的基本契约，重复会让读屏与抓取各读两次标题；
且批量改标题时两个 h1 必须同步改，漏一个就是「标题与正文不一致」的静默缺陷。

## 口径

- 扫描 `site/data/*.html`（排除模板壳 `_shell.html`）；
- **先剥 HTML 注释**再数 h1——模板注释里会写 `<h1>`/`<title>` 字样（W1348 实证），
  不剥会假红（把注释里的示例当标题）；
- 每页恰好 1 个 `<h1>`，且内容非空。
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DATA = ROOT / "site" / "data"
COMMENT = re.compile(r"<!--.*?-->", re.S)
H1 = re.compile(r"<h1\b[^>]*>(.*?)</h1>", re.S)


def _texts():
    for p in sorted(DATA.glob("*.html")):
        if p.name == "_shell.html":
            continue
        yield p.name, COMMENT.sub("", p.read_text(encoding="utf-8"))


def test_each_page_has_exactly_one_h1():
    bad = [(name, len(H1.findall(txt))) for name, txt in _texts() if len(H1.findall(txt)) != 1]
    assert not bad, "H1 数量不等于 1 的页面：%r" % (bad,)


def test_h1_not_empty():
    empty = []
    for name, txt in _texts():
        m = H1.search(txt)
        if m and not m.group(1).strip():
            empty.append(name)
    assert not empty, "H1 内容为空的页面：%r" % (empty,)
