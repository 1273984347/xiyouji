#!/usr/bin/env python3
"""inject_seo_head.py — 全站 SEO head 注入器（W591 SEO 清零·幂等）。

方案：docs/superpowers/plans/2026-09-21-demand-side-optimization-master-plan.md WP-C 第 2-4 条。

对 233 页（排除模板壳 _template.html / data/_shell.html）注入：
  - <link rel="canonical">（部署基 URL + 站点自身相对路径）
  - og:title / og:description（缺失且页面有 meta description 时）/ og:type / og:url
  - og:image + og:image:width/height（og-cover.png）+ twitter:card
  - hreflang 中英互链（EN 站全扁平：EN 候选 = en/ + ZH 路径去 data/ 前缀）
  - index.html 的 JSON-LD 由外链 src 改为内联（爬虫不解析 src 写法）

规则：
  - 幂等：页面含 <!-- SEO:INJECTED --> 标记即跳过；逐标签判重（已有 og:title 的页只补缺失项）
  - 插入位置：</title> 之后整块插入，块尾落标记
  - 配对清单落盘 scripts/output/hreflang-pairs.json（check_seo_head.py 的机判锚点）

用法：
  python scripts/inject_seo_head.py --only index.html,data/emotional-heatmap.html   # 试跑
  python scripts/inject_seo_head.py                                                 # 全量 233 页
"""
from __future__ import annotations

import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
OUT_PAIRS = ROOT / "scripts" / "output" / "hreflang-pairs.json"

BASE = "https://1273984347.github.io/xiyouji/"
OG_IMAGE = BASE + "static/img/og-cover.png"
EXCLUDE = {"_template.html", "data/_shell.html"}
MARKER = "<!-- SEO:INJECTED -->"
JSONLD_SRC_TAG = '<script type="application/ld+json" src="structured-data.jsonld"></script>'


def site_pages() -> list[str]:
    return sorted(
        p.relative_to(SITE).as_posix()
        for p in SITE.rglob("*.html")
        if p.relative_to(SITE).as_posix() not in EXCLUDE
    )


def en_candidate(zh_rel: str) -> str:
    return "en/" + (zh_rel[len("data/"):] if zh_rel.startswith("data/") else zh_rel)


def zh_candidate(en_rel: str, page_set: set[str]) -> str | None:
    base = en_rel[len("en/"):]
    if base in page_set:
        return base
    if "data/" + base in page_set:
        return "data/" + base
    return None


def derive_pairs(pages: list[str]) -> list[dict]:
    page_set = set(pages)
    pairs = []
    for p in pages:
        if p.startswith("en/"):
            continue
        en = en_candidate(p)
        if en in page_set:
            pairs.append({"zh": p, "en": en})
    return pairs


def head_block(self_url: str, zh_href: str | None, en_href: str | None, og_type: str,
               title: str, desc: str | None, has: set[str], is_en: bool) -> tuple[str, list[str]]:
    """构造待插入块。self_url=页面自身绝对 URL（canonical/og:url 用）；
    zh_href/en_href=hreflang 指向（仅配对成功时非 None）；x-default 仅 ZH 页。"""
    lines: list[str] = []
    added: list[str] = []

    def add(tag: str, name: str):
        lines.append("    " + tag)
        added.append(name)

    if "canonical" not in has:
        add(f'<link rel="canonical" href="{self_url}">', "canonical")
    if "og:title" not in has:
        add(f'<meta property="og:title" content="{html.escape(title, quote=True)}">', "og:title")
    if "og:description" not in has and desc:
        add(f'<meta property="og:description" content="{html.escape(desc, quote=True)}">', "og:description")
    if "og:type" not in has:
        add(f'<meta property="og:type" content="{og_type}">', "og:type")
    if "og:url" not in has:
        add(f'<meta property="og:url" content="{self_url}">', "og:url")
    if "og:image" not in has:
        add(f'<meta property="og:image" content="{OG_IMAGE}">', "og:image")
        add('<meta property="og:image:width" content="1200">', "og:image:width")
        add('<meta property="og:image:height" content="630">', "og:image:height")
    if "twitter:card" not in has:
        add('<meta name="twitter:card" content="summary_large_image">', "twitter:card")
    if zh_href and en_href:
        add(f'<link rel="alternate" hreflang="zh-CN" href="{zh_href}">', "hreflang:zh-CN")
        add(f'<link rel="alternate" hreflang="en" href="{en_href}">', "hreflang:en")
        if not is_en:
            add(f'<link rel="alternate" hreflang="x-default" href="{zh_href}">', "hreflang:x-default")
    if not lines:
        return "", added
    lines.append("    " + MARKER)
    return "\n".join(lines), added


def process(rel: str, pairs_map: dict[str, str], page_set: set[str]) -> tuple[bool, list[str]]:
    """处理单页；返回 (是否写入, 添加的标签列表)。"""
    path = SITE / rel
    with path.open(encoding="utf-8", newline="") as f:
        s = f.read()
    if MARKER in s:
        return False, []

    t_open = s.find("<title>")
    assert t_open != -1, rel + " 未找到 <title>"
    t_close = s.find("</title>", t_open)
    title = s[t_open + len("<title>"):t_close].strip()

    desc = None
    di = s.find('<meta name="description" content="')
    if di != -1:
        d_end = s.find('"', di + len('<meta name="description" content="'))
        desc = s[di + len('<meta name="description" content="'):d_end]

    has: set[str] = set()
    for probe, name in [
        ('<link rel="canonical"', "canonical"), ('property="og:title"', "og:title"),
        ('property="og:description"', "og:description"), ('property="og:type"', "og:type"),
        ('property="og:url"', "og:url"), ('property="og:image"', "og:image"),
        ('name="twitter:card"', "twitter:card"),
    ]:
        if probe in s:
            has.add(name)

    is_en = rel.startswith("en/")
    self_url = BASE + rel
    if is_en:
        zh_rel = zh_candidate(rel, page_set)
        zh_href = BASE + zh_rel if zh_rel else None
        en_href = BASE + rel if zh_rel else None
    else:
        en_pair = pairs_map.get(rel)
        zh_href = BASE + rel
        en_href = BASE + en_pair if en_pair else None
    # og:type：data 可视化页及其 EN 镜像均视为 article（同一内容的两语言版本类型一致）
    is_data_like = rel.startswith("data/") or (is_en and zh_rel and zh_rel.startswith("data/"))
    og_type = "article" if is_data_like else "website"

    block, added = head_block(self_url, zh_href, en_href, og_type, title, desc, has, is_en)

    if rel == "index.html" and JSONLD_SRC_TAG in s:
        jsonld = (SITE / "structured-data.jsonld").read_text(encoding="utf-8").strip()
        inline = '<script type="application/ld+json">\n' + jsonld + "\n</script>"
        s = s.replace(JSONLD_SRC_TAG, inline, 1)
        added.append("jsonld:inline")

    if block:
        insert_at = t_close + len("</title>")
        s = s[:insert_at] + "\n" + block + s[insert_at:]

    if added:
        with path.open("w", encoding="utf-8", newline="") as f:
            f.write(s)
    return bool(added), added


def main() -> None:
    only = None
    if len(sys.argv) > 2 and sys.argv[1] == "--only":
        only = [x.strip() for x in sys.argv[2].split(",")]

    pages = site_pages()
    page_set = set(pages)
    pairs = derive_pairs(pages)
    pairs_map = {p["zh"]: p["en"] for p in pairs}
    OUT_PAIRS.write_text(
        json.dumps({"base": BASE, "generated": "2026-09-21",
                    "rule": "en_candidate = en/ + zh_rel 去 data/ 前缀", "pairs": pairs},
                   ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")

    targets = [p for p in pages if only is None or p in only]
    if only is not None:
        missing = set(only) - set(pages)
        assert not missing, f"--only 含未知页面: {missing}"

    written = skipped = 0
    for rel in targets:
        did, added = process(rel, pairs_map, page_set)
        if did:
            written += 1
            print(f"[W] {rel}: {', '.join(added)}")
        else:
            skipped += 1
    print(f"[DONE] 目标 {len(targets)} · 写入 {written} · 跳过 {skipped} · 配对 {len(pairs)}")


if __name__ == "__main__":
    main()
