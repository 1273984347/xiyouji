r"""
build_reader.py — 站内阅读器渲染器（W593 单板块 → W660 多板块映射驱动）

板块表（SECTIONS）驱动：六源目录 → reader 子目录；01 逐回保留 chNNN 命名与
prev/next 连载语义，02-06 按文件名排序 prev/next；reader/index.html 升级六板块分组目录。

链接改写规则（W593 四规则 + W660 扩充·深度感知）：
  ① 板块内 md 互链 → 同目录 .html（01 的 第NNN回-*.md → chNNN.html；README.md 除外→blob）
  ② 跨板块 docs md → {up}{sub}/{name}.html（01 → {up}chNNN.html）
  ③ site 资源 ../../site/… → {up}data/…
  ③b 非六板块 docs（00-导读/07-09/10/治理/模板）→ GitHub blob（站外保留）
  ④ http/锚点保持
未识别 .md 链接 → 残留清单（非零退出）。

用法：python scripts/build_reader.py            # 全量渲染 01-06
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "site" / "reader"
BLOB = "https://github.com/1273984347/xiyouji/blob/main/docs/"
BASE = "https://1273984347.github.io/xiyouji/"
OG_IMAGE = BASE + "static/img/og-cover.png"

# 板块表：源目录名 → (子目录, 板块标题)。01 特殊：chNNN 命名+数字 prev/next。
SECTIONS = [
    ("01-全书逐回解读", "", "逐回解读"),
    ("02-人物深度分析", "people", "人物深度"),
    ("03-主题与情节专题", "themes", "主题专题"),
    ("04-文化与历史背景", "culture", "文化背景"),
    ("05-诗词歌赋", "poetry", "诗词歌赋"),
    ("06-个人随笔", "essays", "个人随笔"),
]
SUB = {src: sub for src, sub, _ in SECTIONS}
BOARD_DIRS = {src for src, _, _ in SECTIONS}

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
  .reader-group { margin: 34px 0 8px; font-size: 19px; font-weight: 700; color: var(--ink);
    border-bottom: 2px solid var(--accent); padding-bottom: 6px; }
"""


def rewrite_links(md: str, docs_root: str, up: str, up2: str, up3: str) -> tuple[str, list[str]]:
    """深度感知改写。up = 页面到 reader 根的相对前缀（'' 或 '../'）。

    ① 板块内 md 互链（README.md 除外→blob）
    ② 跨板块 md → {up}{sub}/{name}.html（01 → {up}chNNN.html）
    ③ site 资源 ../../site/… → {up}…
    ③b 非六板块 md（../x/*.md 与 ../../x.md）→ GitHub blob
    ④ http/锚点保持
    """
    # ① 板块内 md 互链（README.md → blob·不入 reader）
    if docs_root == "01-全书逐回解读":
        md = re.sub(r"\]\(\.?/?(第\d{3}回-[^)]*\.md)\)",
                    lambda m: "](ch" + m.group(1)[1:4] + ".html)", md)
        md = re.sub(r"\]\(\.?/?README\.md\)",
                    lambda m: "](" + BLOB + docs_root + "/README.md)", md)
    else:
        md = re.sub(r"\]\((\.?/?(?!README\.md)[^)/]+\.md)\)",
                    lambda m: "](" + m.group(1).lstrip("./")[:-3] + ".html)", md)
        md = re.sub(r"\]\(\.?/?README\.md\)",
                    lambda m: "](" + BLOB + docs_root + "/README.md)", md)
    # ② 跨板块 md 互链（深度感知）
    def cross_cat(m: re.Match) -> str:
        d, fn = m.group(1), m.group(2)
        sub = SUB.get(d)
        if sub is None:
            return m.group(0)
        if d == "01-全书逐回解读":
            return "](" + up + "ch" + fn[1:4] + ".html)"
        return "](" + up + sub + "/" + fn[:-3] + ".html)"

    md = re.sub(r"\]\(\.\./(0[1-6]-[^/]+)/([^)/]+\.md)\)", cross_cat, md)
    # ③ site 资源（up2 由调用方传入：data 在 reader 根上一级）
    md = md.replace("](../../site/", "](" + up2)
    # ③c 仓库根的 scripts 引用（up3 由调用方传入）
    md = md.replace("](../../scripts/", "](" + up3 + "scripts/")
    # ③b 非六板块 docs → GitHub blob（单段/双段）
    md = re.sub(r"\]\(\.\./((?!0[1-6]-)[^)/]+\.md)\)",
                lambda m: "](" + BLOB + m.group(1) + ")", md)
    md = re.sub(r"\]\(\.\./([^)/]+)/([^)/]+\.md)\)",
                lambda m: "](" + BLOB + m.group(1) + "/" + m.group(2) + ")", md)
    md = re.sub(r"\]\(\.\./\.\./((?!site/)[^)]+\.md)\)",
                lambda m: "](" + BLOB + m.group(1) + ")", md)
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
    # 深度按 site/reader/ 内相对路径计（剥掉 URL 用 reader/ 前缀）
    rel_in_reader = rel[len("reader/"):] if rel.startswith("reader/") else rel
    prefix = "../" * (rel_in_reader.count("/") + 1)
    url = BASE + "reader/" + rel
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
<link rel="stylesheet" href="{prefix}tokens.css">
<link rel="stylesheet" href="{prefix}system.css">
<script src="{prefix}js/theme-init.js"></script>
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
    docs = ROOT / "docs"
    OUT.mkdir(parents=True, exist_ok=True)

    n_pages = 0
    sections_out: list[tuple[str, list[tuple[str, str]]]] = []
    leftovers_all: list[str] = []

    for docs_root, sub, cat_title in SECTIONS:
        src = docs / docs_root
        files = sorted(p for p in src.glob("*.md") if p.name != "README.md")
        assert files, f"{docs_root} 无 md"

        rendered: list[tuple[str, str, str]] = []  # (out_rel, fname, display)
        for f in files:
            md = f.read_text(encoding="utf-8")
            h1, _full = extract(md)
            out_name = f"ch{int(f.name[1:4]):03d}.html" if docs_root == "01-全书逐回解读" else f.stem + ".html"
            out_rel = (sub + "/" + out_name) if sub else out_name
            rendered.append((out_rel, f.name, h1 or f.stem))
        if docs_root != "01-全书逐回解读":
            rendered.sort(key=lambda x: x[1])
        entries = [(rel, disp) for rel, _, disp in rendered]
        sections_out.append((cat_title, entries))

        for idx, (out_rel, fname, _disp) in enumerate(rendered):
            depth = out_rel.count("/")
            up = "../" * depth
            up2 = "../" * (depth + 1)
            up3 = "../" * (depth + 2)
            md = (src / fname).read_text(encoding="utf-8")
            md, leftovers = rewrite_links(md, docs_root, up, up2, up3)
            leftovers_all += [(out_rel, u) for u in leftovers]
            body_html = markdown.markdown(md, extensions=["tables"])
            h1, full = extract((src / fname).read_text(encoding="utf-8"))
            title = full or h1 or out_rel
            desc = f"{title}——《详解西游记》{cat_title}"

            prev_rel = rendered[idx - 1][0] if idx > 0 else None
            next_rel = rendered[idx + 1][0] if idx + 1 < len(rendered) else None

            def pn_html(target: str | None, label: str, dup: str) -> str:
                if not target:
                    return f'<span class="off">{label}（无）</span>'
                return f'<a href="{dup}{target}">{label}</a>'

            dup = depth * "../"
            prev_html = pn_html(prev_rel, "← 上一篇", dup)
            next_html = pn_html(next_rel, "下一篇 →", dup)
            home = (dup + "index.html") if depth else "index.html"

            blob = f"{BLOB}{docs_root}/{fname}"
            body = f"""  <nav class="reader-topnav">
    <a class="brand" href="{home}">详解西游记 · 站内阅读</a>
    <a href="{up}../index.html">站点首页</a>
    <a href="{blob}" rel="noopener">在 GitHub 查看源文件</a>
  </nav>
  <article class="reader-body">
{body_html}
  </article>
  <nav class="reader-pn">{prev_html}{next_html}</nav>"""
            (OUT / out_rel).parent.mkdir(parents=True, exist_ok=True)
            (OUT / out_rel).write_text(
                page_shell(out_rel, title, desc, body), encoding="utf-8", newline="\n")
            n_pages += 1
        # 板块目录页（02-06）——目录页位于 sub/ 内·条目链接补 ../ 前缀
        if sub:
            items = "\n".join(f'<li><a href="../{rel}">{disp}</a></li>' for rel, disp in entries)
            (OUT / sub / "index.html").write_text(
                page_shell(sub + "/index.html", f"{cat_title} · 目录",
                           f"《详解西游记》{cat_title}目录（{len(entries)} 篇）",
                           f'<h1 style="font-size:26px;">{cat_title}</h1>\n<ul class="reader-idx">\n{items}\n</ul>'),
                encoding="utf-8", newline="\n")
            n_pages += 1

    # 总目录：六板块分组
    idx_body = ""
    for cat_title, entries in sections_out:
        idx_body += f'<div class="reader-group">{cat_title}（{len(entries)}）</div>\n<ul class="reader-idx">\n'
        idx_body += "\n".join(f'<li><a href="{rel}">{disp}</a></li>' for rel, disp in entries)
        idx_body += "\n</ul>\n"
    (OUT / "index.html").write_text(
        page_shell("index.html", "站内阅读 · 全目录",
                   "《详解西游记》站内阅读目录（六板块）", idx_body),
        encoding="utf-8", newline="\n")
    n_pages += 1

    print(f"[OK] 生成 {n_pages} 页（含内容页/板块目录/总目录）→ site/reader/")
    if leftovers_all:
        print(f"[WARN] 未识别的 .md 链接 {len(leftovers_all)} 处：")
        for loc, u in leftovers_all[:10]:
            print("  ", loc, u)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
