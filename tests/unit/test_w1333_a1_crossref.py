r"""W1333 专项测试：A1 逐回交叉引用 + reader 阅读体验（首个折叠默认展开）

## 为什么测

- A1 关联行若漏页/断链 ⇒ reader 站内互链出现死链（历史 W459 同族）；
- 若关联行重复插入 ⇒ 100 页各多一条（幂等失效）；
- reader 重生成若丢掉首个折叠的 open ⇒ 回目页首屏重新变空。

## 覆盖判据

  G1 100 回各恰一条 w1333-crossref 行（--check 模式 0 问题）
  G2 关联行内链接全部存在（无死链）
  G3 注入器幂等（重跑零改动）
  G4 build_reader 首个折叠默认 open、其余收起（ch001 抽样）
  G5 CLI --check 在真实仓库 PASS
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import w1333_a1_crossref as cr  # noqa: E402
from w1333_a1_crossref import MARK, build_line, load_pages  # noqa: E402

SCRIPT = SCRIPTS / "w1333_a1_crossref.py"


def test_every_page_has_exactly_one_line():
    pages = load_pages()
    assert len(pages) == 100
    for pg in pages:
        assert len(cr.LINE_RE.findall(pg["text"])) == 1, pg["name"]


def test_no_dead_links():
    pages = load_pages()
    assert cr.check(pages) == []


def test_idempotent():
    pages = load_pages()
    for pg in pages[:5]:
        prev = None
        line = build_line(pg, None, None)
        if line is None:
            continue
        new, action = cr.apply_page(pg, line)
        assert action in ("update", "insert")
        again, action2 = cr.apply_page({"text": new, "path": pg["path"], "name": pg["name"],
                                        "num": pg["num"], "chars": pg["chars"]}, line)
        assert again == new, pg["name"]


def test_line_shape():
    pages = load_pages()
    first = pages[0]
    line = build_line(first, None, pages[1])
    assert MARK in line and "第002回" in line and "孙悟空" in line


def test_reader_first_fold_open():
    html = (ROOT / "site/reader/ch001.html").read_text(encoding="utf-8")
    m = re.findall(r'<details class="reader-fold"([^>]*)><summary>([^<]+)</summary>', html)
    assert m, "reader 页应有折叠段"
    assert m[0][1] == "剧情梗概" and "open" in m[0][0]
    for attrs, name in m[1:]:
        assert "open" not in attrs, name


def test_cli_check_passes():
    r = subprocess.run([sys.executable, str(SCRIPT), "--check"],
                       capture_output=True, text=True, timeout=120)
    assert r.returncode == 0, r.stdout[-500:]
    assert "问题 0" in r.stdout
