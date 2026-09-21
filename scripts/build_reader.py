#!/usr/bin/env python3
"""build_reader.py — docs 站内阅读器生成器（W593 阅读器试点 WP-D1）。

方案：docs/superpowers/plans/2026-09-21-demand-side-optimization-master-plan.md WP-D1。

输入：docs/01-全书逐回解读/第(\\d{3})回-*.md（100 篇）
输出：site/reader/ch001.html … ch100.html + site/reader/index.html

链接改写规则（D1 口径）：
  ① 同板块章节互链  第NNN回-*.md（含 ./ 前缀）      → chNNN.html
  ② 指向 site 资源  ](../../site/X)                 → ](../X)
  ③ 跨板块 docs md  ](../<板块>/x.md)               → GitHub blob 绝对 URL（D2 升级为站内）
  ④ 图片：docs/01 实测 0 张，无需处理

页面规格：
  - tokens/system 走 <link>（同站根页形态）；私有 <style> 仅引用 token 变量（token 覆盖率门禁 0 裸色）
  - head 内建 SEO 全套（canonical/og:title/og:type=article/og:url/og:image/twitter:card）+ SEO:INJECTED 标记
  - 上一篇/下一篇：chNNN±1，ch001 无上一篇、ch100 无下一篇（aria-disabled，不渲染死链）
  - 纯静态无 fetch（不适用 EMBEDDED 回退铁律）；无版本页脚（不参与新鲜度耦合面）
  - 无内联脚本（CSP 由 generate_csp.py 注入空哈希 meta）

用法：python scripts/build_reader.py
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "docs" / "01-全书逐回解读"
OUT = ROOT / "site" / "reader"
BLOB = "https://github.com/1273984347/xiyouji/blob/main/docs/01-全书逐回解读/"
BASE = "https://1273984347.github.io/xiyouji/"
OG_IMAGE = BASE + "static/img/og-cover.png"

STYLE = """
  .reader-wrap { max-width: 760px; margin: 0 auto; padding: 0 16px 72px; }
  .reader-topnav { display: flex; flex-wrap: wrap; gap: 14px; align-items: center;
    padding: 14px 0; border-bottom: 1px solid var(--line); margin-bottom: 28px;
    font-size: 14px; }
  .reader-topnav a { color: var(--accent); text-decoration: none; }
  .reader-topnav a:hover { text-decoration: underline; }
  .reader-topnav .brand { color: var(--ink); font-weight: 700; }
  .reader-body { font-family: var(--font-serif, serif); color: var(--ink);
    line-height: 1.9; font-size: 17px; }
  .reader-body h1 { font-size: 28px; line-height: var(--leading-tight); margin: 12px 0 20px; }
  .reader-body h2 { font-size: 21px; margin: 34px 0 12px; padding-left: 10px;
    border-left: 3px solid var(--accent); }
  .reader-body h3 { font-size: 18px; margin: 24px 0 10px; }
  .reader-body blockquote { margin: 14px 0; padding: 8px 14px; color: var(--ink-soft);
    background: var(--paper-warm, var(--paper)); border-left: 3px solid var(--ink-faint); }
  .reader-body a { color: var(--accent); }
  .reader-body hr { border: 0; border-top: 1px solid var(--line); margin: 32px 0; }
  .reader-meta { color: var(--ink-soft); font-size: 13px; margin: 0 0 26px; }
  .reader-pn { display: flex; justify-content: space-between; gap: 12px; margin-top: 44px;
    padding-top: 18px; border-top: 1px solid var(--line); font-size: 15px; }
  .reader-pn a { color: var(--accent); text-decoration: none; }
  .reader-pn a:hover { text-decoration: underline; }
  .reader-pn .off { color: var(--ink-faint); }
  .reader-idx { list-style: none; padding: 0; margin: 24px 0 0;
    display: grid; grid-template-columns: 1fr; gap: 2px; }
  @media (min-width: 640px) { .reader-idx { grid-template-columns: 1fr 1fr; } }
  .reader-idx a { display: block; padding: 9px 12px; color: var(--ink); text-decoration: none;
    border: 1px solid var(--line); border-radius: var(--radius-sm, 4px); font-size: 14px; }
  .reader-idx a:hover { border-color: var(--accent); color: var(--accent); }
  .reader-idx .no { color: var(--ink-faint); font-family: var(--font-mono, monospace); margin-right: 8px; }
"""


def rewrite_links(md: str, rel_out: str) -> tuple[str, list[str]]:
    """按 D1 三规则改写链接；返回 (新 md, 残留未识别链接清单)。"""
    # ① 章节互链
    md = re.sub(r"\]\(\.?/?(第\d{3}回-[^)]*\.md)\)",
                lambda m: "](ch" + m.group(1)[1:4] + ".html)", md)
    # ② site 资源
    md = md.replace("](../../site/", "](../")
    # ③ 跨板块 docs → blob
    md = re.sub(r"\]\(\.\./([^)]+\.md)\)",
                lambda m: "](https://github.com/1273984347/xiyouji/blob/main/docs/" + m.group(1) + ")", md)
    # 审计残留
    left = [u for u in re.findall(r"\]\(([^)]+)\)", md)
            if u.endswith(".md") and not u.startswith("http")]
    return md, left


def extract(md: str) -> tuple[str, str | None]:
    """返回 (H1 文本, chapter-meta 的 full_title)。"""
    m = re.search(r"^# (.+)$", md, re.M)
    h1 = m.group(1).strip() if m else ""
    c = re.search(r"chapter-meta: (\{.*?\})", md)
    full = None
    if c:
        try:
            full = json.loads(c.group(1)).get("full_title")
        except json.JSONDecodeError:
            full = None
    return h1, full


def head(rel: str, title: str, desc: str) -> str:
    url = BASE + rel
    t = html.escape(title, quote=True)
    d = html.escape(desc, quote=True)
    return f"""<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{t}</title>
<!-- SEO:INJECTED -->
<meta name="description" content="{d}">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:type" content="article">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{OG_IMAGE}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="../tokens.css">
<link rel="stylesheet" href="../system.css">
<script src="../js/theme-init.js"></script>
<style>{STYLE}</style>"""


def page_shell(rel: str, title: str, desc: str, body: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
{head(rel, title, desc)}
</head>
<body>
<main class="reader-wrap">
{body}
</main>
</body>
</html>
"""


def main() -> None:
    files = sorted(SRC.glob("第*回-*.md"))
    assert len(files) == 100, f"预期 100 篇，实得 {len(files)}"
    OUT.mkdir(parents=True, exist_ok=True)

    chapters = []  # (num, fname, h1, full_title)
    for f in files:
        num = int(f.name[1:4])
        md = f.read_text(encoding="utf-8")
        h1, full = extract(md)
        chapters.append((num, f.name, h1, full))

    leftovers_all = []
    for num, fname, h1, _full in chapters:
        md = (SRC / fname).read_text(encoding="utf-8")
        md, leftovers = rewrite_links(md, f"ch{num:03d}.html")
        leftovers_all += [(f"ch{num:03d}", u) for u in leftovers]
        body_html = markdown.markdown(md, extensions=["tables"])
        title = h1 or f"第{num:03d}回"
        desc = f"{title}——《详解西游记》逐回解读"
        prev_html = (f'<a href="ch{num - 1:03d}.html">← 上一回（第{num - 1:03d}回）</a>'
                     if num > 1 else '<span class="off">← 上一回（无）</span>')
        next_html = (f'<a href="ch{num + 1:03d}.html">下一回（第{num + 1:03d}回）→</a>'
                     if num < 100 else '<span class="off">下一回（无）→</span>')
        body = f"""  <nav class="reader-topnav">
    <a class="brand" href="index.html">详解西游记 · 逐回阅读</a>
    <a href="../index.html">站点首页</a>
    <a href="{BLOB}{fname}" rel="noopener">在 GitHub 查看源文件</a>
  </nav>
  <article class="reader-body">
{body_html}
  </article>
  <nav class="reader-pn" aria-label="上一篇下一篇">
    {prev_html}
    {next_html}
  </nav>"""
        (OUT / f"ch{num:03d}.html").write_text(
            page_shell(f"reader/ch{num:03d}.html", title, desc, body),
            encoding="utf-8", newline="\n")

    # 目录页
    items = []
    for num, _fname, _h1, full in chapters:
        label = full or f"第{num}回"
        items.append(f'    <li><a href="ch{num:03d}.html">'
                     f'<span class="no">{num:03d}</span>{html.escape(label)}</a></li>')
    idx_body = f"""  <nav class="reader-topnav">
    <a class="brand" href="index.html">详解西游记 · 逐回阅读</a>
    <a href="../index.html">站点首页</a>
  </nav>
  <h1 style="font-size:26px;">全 100 回目录</h1>
  <p class="reader-meta">共 100 篇 · 点击进入单回阅读；每回含上一篇/下一篇连载导航。</p>
  <ul class="reader-idx">
{chr(10).join(items)}
  </ul>"""
    (OUT / "index.html").write_text(
        page_shell("reader/index.html", "全 100 回目录 · 逐回阅读",
                   "《详解西游记》全 100 回逐回解读目录", idx_body),
        encoding="utf-8", newline="\n")

    print(f"[OK] 生成 ch001-ch100 + index 共 {101} 页 → site/reader/")
    if leftovers_all:
        print(f"[WARN] 未识别的 .md 链接 {len(leftovers_all)} 处：")
        for loc, u in leftovers_all[:10]:
            print("  ", loc, u)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
