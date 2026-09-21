#!/usr/bin/env python3
"""gen_sitemap.py — site/sitemap.xml 生成器（W591 SEO 清零）。

方案：docs/superpowers/plans/2026-09-21-demand-side-optimization-master-plan.md WP-C 第 5 条。

规则：
  - 遍历 site/**/*.html，排除常量 EXCLUDE（模板壳/本地工具页/404），当前产出 230 条
  - <lastmod> 取 git log -1 --format=%cs -- <file>（无 git 历史回落当天日期）
  - priority：根页 0.9 / data/ 0.8 / en/ 0.6；changefreq 统一 monthly
  - 凡页面增删或改标题的批次，收尾须重跑本脚本（写入当批收尾清单）

用法：python scripts/gen_sitemap.py
"""
from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
SITEMAP = SITE / "sitemap.xml"
BASE = "https://1273984347.github.io/xiyouji/"

EXCLUDE = {
    "_template.html",        # 模板壳
    "data/_shell.html",      # 可视化模板壳
    "rum-viewer.html",       # 本地工具页
    "visit-viewer.html",     # 本地工具页
    "data/81-hardships-view.html",           # 辅助视图页（与现役 sitemap 门禁期望集一致）
    "data/character-relationship-3d-view.html",  # 辅助视图页（同上）
}


def lastmod(repo_rel: str, today: str) -> str:
    out = subprocess.run(
        ["git", "log", "-1", "--format=%cs", "--", repo_rel],
        cwd=ROOT, capture_output=True, text=True,
    ).stdout.strip()
    return out if out else today


def main() -> None:
    today = time.strftime("%Y-%m-%d")
    pages = sorted(
        p.relative_to(SITE).as_posix()
        for p in SITE.rglob("*.html")
        if p.relative_to(SITE).as_posix() not in EXCLUDE
    )
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f"<!-- W591 SEO 清零·sitemap 由 scripts/gen_sitemap.py 生成·{len(pages)} 页面"
        f"（EXCLUDE: {', '.join(sorted(EXCLUDE))}） -->",
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for rel in pages:
        prio = "0.9" if "/" not in rel else ("0.8" if rel.startswith("data/") else "0.6")
        lm = lastmod("site/" + rel, today)
        lines.append(
            f"  <url><loc>{BASE}{rel}</loc><lastmod>{lm}</lastmod>"
            f"<changefreq>monthly</changefreq><priority>{prio}</priority></url>"
        )
    lines.append("</urlset>")
    SITEMAP.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[OK] {SITEMAP.relative_to(ROOT)} {len(pages)} URLs")


if __name__ == "__main__":
    sys.exit(main())
