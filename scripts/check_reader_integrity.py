"""第 62 门禁：site/reader 完整性（C1 占位词 / C2 GitHub 链接 / C3 单 h1 / C4 标题唯一）。

判据来源：2026-11-06 全仓逐逻辑审计 §9——reader 622 页此前无专属门禁，
占位词 205 页、GitHub 前缀错误 199 条、多 h1 33 页、同题页 3 组均靠人工发现。
"""
from __future__ import annotations

import os
import re
import sys
import tempfile
from collections import Counter
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
MARKER = "---- 第 62 门禁 reader 完整性："

PLACEHOLDER_RE = re.compile(r"（待补）|\(待补\)|待完善|内容建设中|TODO\b|FIXME\b|Lorem ipsum")
GITHUB_RE = re.compile(
    r"https://github\.com/1273984347/xiyouji/(?:blob|tree)/main/([^\"'#?)\s]+)")
TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S)
H1_RE = re.compile(r"<h1\b", re.I)
REDIRECT_RE = re.compile(r"<meta[^>]+http-equiv=[\"']refresh[\"']", re.I)
STRIP_SCRIPT = re.compile(r"<script\b[\s\S]*?</script>", re.I)
STRIP_STYLE = re.compile(r"<style\b[\s\S]*?</style>", re.I)
STRIP_COMMENT = re.compile(r"<!--[\s\S]*?-->")
STRIP_TAG = re.compile(r"<[^>]+>")


def _pages(base: Path) -> list[Path]:
    reader = base / "site" / "reader"
    if not reader.is_dir():
        return []
    return sorted(p for p in reader.rglob("*.html"))


def _read(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def _visible(html: str) -> str:
    t = STRIP_SCRIPT.sub(" ", html)
    t = STRIP_STYLE.sub(" ", t)
    t = STRIP_COMMENT.sub(" ", t)
    t = STRIP_TAG.sub(" ", t)
    return re.sub(r"\s+", " ", t)


def c1_placeholders(pages: list[Path], base: Path) -> list[str]:
    fails = []
    for p in pages:
        m = PLACEHOLDER_RE.search(_visible(_read(p)))
        if m:
            fails.append("%s 可见正文含占位词「%s」" % (p.relative_to(base).as_posix(), m.group(0)))
    return fails


def c2_github_links(pages: list[Path], base: Path) -> list[str]:
    fails = []
    for p in pages:
        for m in GITHUB_RE.finditer(_read(p)):
            rel = unquote(m.group(1)).split("#")[0].split("?")[0]
            target = os.path.normpath(os.path.join(base, rel))
            if not os.path.exists(target):
                fails.append("%s GitHub 链接目标不存在：%s" % (p.relative_to(base).as_posix(), rel))
    return fails


def c3_single_h1(pages: list[Path], base: Path) -> list[str]:
    fails = []
    for p in pages:
        html = _read(p)
        if REDIRECT_RE.search(html):
            continue
        n = len(H1_RE.findall(html))
        if n != 1:
            fails.append("%s h1 数量=%d（内容页须恰 1 个）" % (p.relative_to(base).as_posix(), n))
    return fails


def c4_unique_titles(pages: list[Path], base: Path) -> list[str]:
    titles = Counter()
    where = {}
    for p in pages:
        m = TITLE_RE.search(_read(p))
        if not m:
            continue
        title = re.sub(r"\s+", " ", m.group(1)).strip()
        titles[title] += 1
        where.setdefault(title, []).append(p.relative_to(base).as_posix())
    return ["标题重复「%s」：%s" % (t, "、".join(where[t])) for t, n in titles.items() if n > 1]


def scan(base: Path = ROOT) -> tuple[list[str], int]:
    pages = _pages(base)
    if not pages:
        return [], 0
    fails = []
    fails += c1_placeholders(pages, base)
    fails += c2_github_links(pages, base)
    fails += c3_single_h1(pages, base)
    fails += c4_unique_titles(pages, base)
    return fails, len(pages)


def _self_test() -> int:
    with tempfile.TemporaryDirectory() as td:
        base = Path(td)
        (base / "site" / "reader").mkdir(parents=True)
        (base / "README.md").write_text("ok", encoding="utf-8")
        good = '<html><head><title>唯一页</title></head><body><h1>x</h1>' \
               '<a href="https://github.com/1273984347/xiyouji/blob/main/README.md">r</a></body></html>'
        (base / "site" / "reader" / "good.html").write_text(good, encoding="utf-8")
        bad_ph = '<html><head><title>占位页</title></head><body><h1>x</h1><p>（待补）</p></body></html>'
        (base / "site" / "reader" / "ph.html").write_text(bad_ph, encoding="utf-8")
        bad_gh = '<html><head><title>坏链页</title></head><body><h1>x</h1>' \
                 '<a href="https://github.com/1273984347/xiyouji/blob/main/docs/source/no.md">x</a></body></html>'
        (base / "site" / "reader" / "gh.html").write_text(bad_gh, encoding="utf-8")
        bad_h1 = '<html><head><title>双 H1</title></head><body><h1>a</h1><h1>b</h1></body></html>'
        (base / "site" / "reader" / "h1.html").write_text(bad_h1, encoding="utf-8")
        dup = '<html><head><title>重复页</title></head><body><h1>x</h1></body></html>'
        (base / "site" / "reader" / "dup1.html").write_text(dup, encoding="utf-8")
        (base / "site" / "reader" / "dup2.html").write_text(dup, encoding="utf-8")
        fails, n = scan(base)
        checks = [
            ("C1 占位词", any("ph.html" in f for f in fails)),
            ("C2 GitHub 链接", any("gh.html" in f for f in fails)),
            ("C3 单 h1", any("h1.html" in f for f in fails)),
            ("C4 标题唯一", any("标题重复" in f for f in fails)),
            ("正向页不误报", not any("good.html" in f for f in fails)),
        ]
        print("self-test 页数=%d" % n)
        bad = 0
        for name, ok in checks:
            print(("OK  " if ok else "FAIL") + " " + name)
            bad += 0 if ok else 1
        print("self-test", "PASS" if bad == 0 else "FAIL")
        return 0 if bad == 0 else 1


def main() -> int:
    if "--self-test" in sys.argv:
        return _self_test()
    fails, n = scan()
    if n == 0:
        print("FAIL 基础设施缺失：site/reader 无 HTML（fail-closed）")
        print(MARKER + " 不可执行 ----")
        return 2
    for f in fails:
        print("FAIL " + f)
    print(MARKER + " %d FAIL（扫描 %d 页） ----" % (len(fails), n))
    if "--report" in sys.argv:
        return 0
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
