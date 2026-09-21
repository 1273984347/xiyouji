#!/usr/bin/env python3
"""check_seo_head.py — SEO head 完整性常驻检查（W591 SEO 清零）。

方案：docs/superpowers/plans/2026-09-21-demand-side-optimization-master-plan.md WP-C 第 6 条。
独立可跑；如经用户批准可注册为 verify_delivery 第 26 门禁（--check 形态兼容门禁调用）。

检查面：
  SEO 注入面 233 页 = site 全部 HTML 减模板壳（_template.html / data/_shell.html）
  sitemap 收录面 230 页 = 233 页再减 rum-viewer.html / visit-viewer.html / 404.html
  R1 每页必备：viewport / canonical(=BASE+自身路径) / og:title / og:image(=og-cover 绝对 URL) / og:url / twitter:card
  R2 hreflang 与 scripts/output/hreflang-pairs.json 双向一致（配对页双方各含 zh-CN+en；ZH 页含 x-default；非配对页不得含 hreflang link）
  R3 sitemap <loc> 集合 == 磁盘页面集合（sitemap 收录面口径）且 lastmod ≤ 当天
  R4 og-cover.png 存在、精确 1200x630、≤300KB
  R5 index.html JSON-LD 为内联（无 src 外链写法）且 json.loads 可解析、无 example.com 占位域名

用法：python scripts/check_seo_head.py [--check]   # 违例 >0 退出码 1
"""
from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
SITEMAP = SITE / "sitemap.xml"
PAIRS = ROOT / "scripts" / "output" / "hreflang-pairs.json"
COVER = SITE / "static" / "img" / "og-cover.png"

BASE = "https://1273984347.github.io/xiyouji/"
OG_IMAGE = BASE + "static/img/og-cover.png"
# 两个排除面语义不同：SEO 注入面=233 页（只排模板壳）；
# sitemap 收录面=229 页（与 verify_delivery 现役 sitemap 门禁期望集一致：另排本地工具页两页 + 两个 data/-view 辅助页；404.html 按门禁要求收录）
SEO_EXCLUDE = {"_template.html", "data/_shell.html"}
SITEMAP_EXCLUDE = SEO_EXCLUDE | {
    "rum-viewer.html", "visit-viewer.html",
    "data/81-hardships-view.html", "data/character-relationship-3d-view.html",
}


def site_pages() -> list[str]:
    return sorted(
        p.relative_to(SITE).as_posix()
        for p in SITE.rglob("*.html")
        if p.relative_to(SITE).as_posix() not in SEO_EXCLUDE
    )


def en_candidate(zh_rel: str) -> str:
    return "en/" + (zh_rel[len("data/"):] if zh_rel.startswith("data/") else zh_rel)


def main() -> bool:
    violations: list[str] = []
    pages = site_pages()
    page_set = set(pages)
    today = time.strftime("%Y-%m-%d")

    # R4 og-cover
    if not COVER.exists():
        violations.append("R4 og-cover.png 不存在")
    else:
        from PIL import Image
        with Image.open(COVER) as im:
            if im.size != (1200, 630):
                violations.append(f"R4 og-cover 尺寸 {im.size} != (1200,630)")
        if COVER.stat().st_size > 300 * 1024:
            violations.append(f"R4 og-cover 超 300KB: {COVER.stat().st_size}B")

    # R1 每页 head 必备项
    for rel in pages:
        s = (SITE / rel).read_text(encoding="utf-8")
        url = BASE + rel
        head = s[:s.find("</head>")] if "</head>" in s else s
        checks = [
            ('name="viewport"', "viewport"),
            (f'<link rel="canonical" href="{url}">', "canonical"),
            ('property="og:title"', "og:title"),
            (f'<meta property="og:image" content="{OG_IMAGE}">', "og:image"),
            (f'<meta property="og:url" content="{url}">', "og:url"),
            ('name="twitter:card"', "twitter:card"),
        ]
        for probe, name in checks:
            if probe not in head:
                violations.append(f"R1 {rel} 缺 {name}")

    # R2 hreflang 与配对清单双向一致
    data = json.loads(PAIRS.read_text(encoding="utf-8"))
    pairs = {(p["zh"], p["en"]) for p in data["pairs"]}
    derived = {(p, en_candidate(p)) for p in pages if not p.startswith("en/") and en_candidate(p) in page_set}
    if pairs != derived:
        violations.append(f"R2 hreflang-pairs.json 与磁盘推导不一致（文件 {len(pairs)} vs 推导 {len(derived)}）")
    for zh, en in pairs:
        zs = (SITE / zh).read_text(encoding="utf-8")
        es = (SITE / en).read_text(encoding="utf-8")
        for probe, name in [
            (f'hreflang="zh-CN" href="{BASE}{zh}"', f"{zh} zh-CN"),
            (f'hreflang="en" href="{BASE}{en}"', f"{zh} en"),
            (f'hreflang="x-default" href="{BASE}{zh}"', f"{zh} x-default"),
        ]:
            if probe not in zs:
                violations.append(f"R2 ZH 页缺 {name}")
        for probe, name in [
            (f'hreflang="zh-CN" href="{BASE}{zh}"', f"{en} zh-CN"),
            (f'hreflang="en" href="{BASE}{en}"', f"{en} en"),
        ]:
            if probe not in es:
                violations.append(f"R2 EN 页缺 {name}")
    for rel in pages:
        s = (SITE / rel).read_text(encoding="utf-8")
        # 仅检查 <link hreflang>（alternate 机制）；<a hreflang> 属性为历史既有用法不在此列
        if re.search(r"<link[^>]+hreflang=", s) and not any(rel in pr for pr in pairs):
            violations.append(f"R2 非配对页含 hreflang link: {rel}")

    # R3 sitemap
    sm = SITEMAP.read_text(encoding="utf-8")
    locs = set(re.findall(r"<loc>([^<]+)</loc>", sm))
    expect = {BASE + p for p in pages if p not in SITEMAP_EXCLUDE}
    if locs != expect:
        violations.append(f"R3 sitemap 集合不等：多 {sorted(locs - expect)[:3]} 少 {sorted(expect - locs)[:3]}")
    bad_lm = [lm for lm in re.findall(r"<lastmod>([^<]+)</lastmod>", sm) if lm > today]
    if bad_lm:
        violations.append(f"R3 lastmod 晚于当天: {bad_lm[:3]}")

    # R5 index JSON-LD
    idx = (SITE / "index.html").read_text(encoding="utf-8")
    if 'application/ld+json" src=' in idx:
        violations.append("R5 index.html JSON-LD 仍为 src 外链写法")
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', idx, re.S)
    if not m:
        violations.append("R5 index.html 未找到内联 JSON-LD")
    else:
        try:
            json.loads(m.group(1))
        except json.JSONDecodeError as e:
            violations.append(f"R5 JSON-LD 解析失败: {e}")
    if "example.com" in idx:
        violations.append("R5 index.html 含 example.com 占位域名")

    if violations:
        print(f"SEO head 检查 FAIL：{len(violations)} 项违例")
        for v in violations[:50]:
            print("  FAIL", v)
        return False
    print(f"SEO head 检查通过（{len(pages)} 页 · 配对 {len(pairs)} · sitemap 集合一致 · JSON-LD 内联有效）")
    return True


if __name__ == "__main__":
    ok = main()
    sys.exit(0 if ok else 1)
