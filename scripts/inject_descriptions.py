#!/usr/bin/env python3
"""inject_descriptions.py — 全站 meta description 注入 + title 清理（W641）。

背景：W591 SEO 注入覆盖 og:image/canonical/JSON-LD/hreflang 但未含 description；
第十一份外部评审实证 site/data 86 页 0 页有 description（全站实测 231/235 缺）。
第 26 门禁（check_seo_head.py）同批扩 R1 description 必备项防复发。

描述来源（逐页取首个非空，截 158 字符）：
  1. h2.section-title 序列（去「壹 · 」等序数前缀·取前 3 个拼接）——zh/en 页均有效
  2. 首个 .section-sub 文本（EN kicker 页）
  3. title 去站点后缀兜底

title 清理：
  - 「详解西游记 · 详解西游记」→「详解西游记」（title 与 og:title 同改）
  - title/og:title 中「 · Wxxx…」内部编号段删除（保留页名与站点后缀）

幂等：已有 meta description 的页跳过；替换均带出现次数断言。
范围：site/data、site/en、site 根（跳过 _ 开头模板）。
"""
import html
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEO_MARK = "<!-- SEO:INJECTED -->"
NUM_PREFIX = re.compile(r"^(?:[一二三四五六七八九十百]{1,3}|Section\s*\d+|Part\s*\d+)\s*[·•]\s*")
SITE_SUFFIX_ZH = " · 详解西游记"
SITE_SUFFIX_EN = " · Annotated Journey to the West"


def pages():
    for sub in ("data", "en", ""):
        d = os.path.join(ROOT, "site", sub) if sub else os.path.join(ROOT, "site")
        for f in sorted(os.listdir(d)):
            if f.endswith(".html") and not f.startswith("_"):
                yield os.path.join(d, f)


def strip_tags(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


def derive_desc(s, is_en):
    title_m = re.search(r"<title>([^<]+)</title>", s)
    title = strip_tags(title_m.group(1)) if title_m else ""
    # 1) h2.section-title 序列
    h2s = [strip_tags(t) for t in re.findall(r'<h2[^>]*class="[^"]*section-title[^"]*"[^>]*>(.*?)</h2>', s, re.S)]
    h2s = [NUM_PREFIX.sub("", t) for t in h2s if t and len(t) > 3][:3]
    parts = " · ".join(h2s) if h2s else ""
    # 2) 首个 section-sub（EN kicker 页）
    if len(parts) < 20:
        sub = re.search(r'<div class="section-sub">(.*?)</div>', s, re.S)
        if sub:
            parts = strip_tags(sub.group(1))[:120]
    # 3) title 兜底
    if len(parts) < 12:
        parts = re.sub(r"\s*·\s*(详解西游记|Annotated Journey to the West).*$", "", title)
    if len(parts) > 158:
        parts = re.sub(r"[ ·，。]+$", "", parts[:155]) + "…"
    suffix = SITE_SUFFIX_EN if is_en else SITE_SUFFIX_ZH
    return f"{parts}{suffix}" if parts else ""


def inject(s, desc, is_en):
    meta = f'    <meta name="description" content="{html.escape(desc, quote=True)}">'
    if is_en or 'lang="en"' in s[:2000]:
        meta += f'\n    <meta property="og:description" content="{html.escape(desc, quote=True)}">'
    if SEO_MARK in s:
        return s.replace(SEO_MARK, SEO_MARK + "\n" + meta, 1)
    i = s.find("</head>")
    assert i > 0, "no </head>"
    return s[:i] + meta + "\n" + s[i:]


def clean_title(s):
    """双后缀 + W 编号段清理（title 与 og:title 同改）。返回 (new_s, n_changes)。"""
    n = 0
    for pat, rep in [
        (r"详解西游记 · 详解西游记", "详解西游记"),
        (r"( · W\d+[0-9A-Za-z ]*)*( · (?:详解西游记|Annotated Journey to the West))", r"\2"),
    ]:
        s2, k = re.subn(pat, rep, s)
        n += k
        s = s2
    return s, n


def main():
    n_desc, n_skip, n_title, n_write = 0, 0, 0, 0
    no_desc_after = []
    for p in pages():
        rel = os.path.relpath(p, ROOT)
        s = open(p, encoding="utf-8", newline="").read()
        orig = s
        if 'name="description"' not in s:
            is_en = rel.replace("\\", "/").startswith("site/en/")
            desc = derive_desc(s, is_en)
            assert desc, f"{rel}: 描述推导为空"
            s = inject(s, desc, is_en)
            assert 'name="description"' in s, f"{rel}: 注入失败"
            n_desc += 1
        else:
            n_skip += 1
        s, k = clean_title(s)
        n_title += k
        if s != orig:
            open(p, "w", encoding="utf-8", newline="").write(s)
            n_write += 1
        if 'name="description"' not in s:
            no_desc_after.append(rel)
    print(f"description 注入 {n_desc} 页 · 跳过已有 {n_skip} 页 · title 清理 {n_title} 处 · 落盘 {n_write} 页")
    if no_desc_after:
        print("仍缺 description:", no_desc_after[:10])
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
