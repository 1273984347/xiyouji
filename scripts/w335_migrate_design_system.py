#!/usr/bin/env python3
"""
w335_migrate_design_system.py — 批量迁移 site/data/*.html 到新设计系统
========================================================================
将旧版数据页（内联 :root + 深棕渐变 hero + 旧 footer）转换为：
  tokens.css + system.css + 页面特有 CSS + 新 topnav/hero/footer

用法：
  python w335_migrate_design_system.py --dry-run   # 预览，不写入
  python w335_migrate_design_system.py             # 执行迁移
  python w335_migrate_design_system.py --files a.html b.html  # 仅迁移指定文件

幂等：已迁移的页面（含 system.css 链接）会被跳过。
"""

import re
import sys
import argparse
from pathlib import Path

SITE_DATA = Path(__file__).resolve().parent.parent / "site" / "data"

# 跳过的特殊页面（结构差异大，需手动处理）
SKIP_FILES = {
    "_shell.html",          # 模板本身
    "81-hardships.html",    # 已手动迁移（标杆）
    "tag-cloud.html",       # 特殊结构（D3 标签云，无标准 hero）
    "text-search.html",     # 特殊结构（全文检索，无标准 hero）
}

# 分类映射（从文件名推断 kicker 标签）
CATEGORY_MAP = {
    "chapter-stats": "A · 文本基础",
    "character-appearance": "B · 人物",
    "relationships": "D · 关系",
    "journey-route": "E · 地理",
    "philosophy": "G · 哲学",
    "risk-project": "H · 风险与项目",
    "monster-sociology": "I · 妖怪社会学",
    "power-resources": "J · 权力与资源",
    "karma-reincarnation": "K · 命运与轮回",
    "business-model": "L · 商业模型",
    "cave-estate": "M · 洞府房产",
    "magic-system": "N · 法术阵法",
    "aesthetics": "O · 美学时尚",
    "music-structure": "P · 音乐声效",
    "text-evolution": "Q · 源流演变",
    "criticism-history": "Q+ · 批评史",
    "concept-device": "Q+ · 观念装置",
    "cross-time-danmaku": "Q++ · 弹幕博物馆",
    "century-dialogue": "Q++ · 世纪对话",
    "famous-time-travel": "Q++ · 名人穿越",
    "emotional-heatmap": "Q+++ · 情感热力图",
    "interactive-timeline": "Q+++ · 交互时间线",
    "ai-dialogue": "Q+++ · AI 对话",
    "deconstruction": "R · 解构作品",
    "global-pattern": "S · 全球模式",
    "counterfactual": "T · 反事实推断",
    "cultural-misreading": "U · 文化错位",
    "workplace": "V · 打工人职场",
    "social-media": "W · 社媒人设",
    "game-webnovel": "X · 游戏网文",
    "ethics-consumption": "Y · 伦理消费",
    "chart-design": "Z · 图表设计",
    "narrative-experiment": "AA · 叙事实验",
    "visual-art": "AB · 视觉艺术",
    "methodology-matrix": "AC · 方法论矩阵",
    "cognitive-psychology": "AD · 认知心理",
    "ecology": "AE · 生态学",
    "jurisprudence": "AF · 法理经济",
    "material-archaeology": "AG · 物质考古",
    "linguistics": "AH · 语言学",
}

# 通用 CSS 模式（这些在 system.css 中已有，可从内联中删除）
GENERIC_CSS_PATTERNS = [
    r':root\s*\{[^}]*\}',
    r'\*\s*\{[^}]*\}',
    r'body\s*\{[^}]*\}',
    r'\.hero\s*\{[^}]*\}',
    r'\.hero::after\s*\{[^}]*\}',
    r'\.hero\s+h1\s*\{[^}]*\}',
    r'\.hero\s+\.subtitle\s*\{[^}]*\}',
    r'\.hero\s+\.tagline\s*\{[^}]*\}',
    r'\.hero\s+\.breadcrumb[^{]*\{[^}]*\}',
    r'\.breadcrumb\s*\{[^}]*\}',
    r'\.breadcrumb\s+a\s*\{[^}]*\}',
    r'\.breadcrumb\s+a:hover\s*\{[^}]*\}',
    r'\.container\s*\{[^}]*\}',
    r'\.kpi-row\s*\{[^}]*\}',
    r'\.kpi-card\s*\{[^}]*\}',
    r'\.kpi-card\s+\.label\s*\{[^}]*\}',
    r'\.kpi-card\s+\.value\s*\{[^}]*\}',
    r'\.kpi-card\s+\.desc\s*\{[^}]*\}',
    r'\.section\s*\{[^}]*\}',
    r'\.section-title\s*\{[^}]*\}',
    r'\.section-sub\s*\{[^}]*\}',
    r'footer\s*\{[^}]*\}',
    r'footer\s+a\s*\{[^}]*\}',
    r'footer\s+a:hover\s*\{[^}]*\}',
    r'a:focus-visible[^{]*\{[^}]*\}',
    r'button:focus-visible[^{]*\{[^}]*\}',
]


def extract_title(html: str) -> str:
    m = re.search(r'<title>([^<]+)</title>', html)
    if m:
        return m.group(1).replace(" · 详解西游记", "").strip()
    return "数据可视化"


def extract_hero_content(html: str) -> dict:
    """从旧版 hero 中提取 h1、subtitle、tagline。"""
    result = {"h1": "", "subtitle": "", "tagline": ""}
    # h1
    m = re.search(r'<header class="hero"[^>]*>.*?<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
    if m:
        result["h1"] = re.sub(r'<[^>]+>', '', m.group(1)).strip()
    # subtitle
    m = re.search(r'<(?:div|p) class="subtitle"[^>]*>(.*?)</(?:div|p)>', html, re.DOTALL)
    if m:
        result["subtitle"] = re.sub(r'<[^>]+>', '', m.group(1)).strip()
    # tagline
    m = re.search(r'<(?:div|p) class="tagline"[^>]*>(.*?)</(?:div|p)>', html, re.DOTALL)
    if m:
        result["tagline"] = re.sub(r'<[^>]+>', '', m.group(1)).strip()
    return result


def extract_page_css(html: str) -> str:
    """提取内联 <style> 中的页面特有 CSS（去除通用模式）。"""
    m = re.search(r'<style>(.*?)</style>', html, re.DOTALL)
    if not m:
        return ""
    css = m.group(1)
    # 移除通用模式
    for pattern in GENERIC_CSS_PATTERNS:
        css = re.sub(pattern, '', css, flags=re.DOTALL)
    # 移除响应式中对通用类的引用（保留页面特有的）
    # 清理多余空行
    css = re.sub(r'\n{3,}', '\n\n', css)
    css = css.strip()
    return css


def get_category(filename: str) -> str:
    stem = Path(filename).stem
    if stem in CATEGORY_MAP:
        return CATEGORY_MAP[stem]
    # 尝试前缀匹配
    for key, val in CATEGORY_MAP.items():
        if stem.startswith(key):
            return val
    return "数据可视化"


def extract_footer_links(html: str) -> str:
    """提取旧 footer 中的'深入阅读'链接（如果有）。"""
    m = re.search(r'深入阅读[：:]\s*<a href="([^"]+)"[^>]*>([^<]+)</a>', html)
    if m:
        return f' · <a href="{m.group(1)}">{m.group(2)}</a>'
    return ""


def build_new_head(title: str, page_css: str) -> str:
    css_block = ""
    if page_css:
        css_block = f"""    <style>
        /* === 仅本页特有样式（通用组件由 system.css 提供） === */
        {page_css}
    </style>"""
    else:
        css_block = "    <!-- 本页无特有样式，全部由 system.css 提供 -->"

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="#FAF7F0">
    <title>{title} · 详解西游记</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <noscript><p style="color:#C8463A;padding:12px;">本页面需 JavaScript 才能渲染图表。</p></noscript>
    <link rel="stylesheet" href="../tokens.css">
    <link rel="stylesheet" href="../system.css">
{css_block}
</head>"""


def build_topnav() -> str:
    return """    <header class="topnav">
        <a class="brand" href="../index.html">
            <span class="seal">西游<br>详解</span>
            <span class="wordmark">详解西游记</span>
        </a>
        <nav aria-label="主导航">
            <a href="../index.html">首页</a>
            <a href="../dashboard.html">数据看板</a>
            <a href="tag-cloud.html">标签云</a>
            <a href="text-search.html">全文检索</a>
        </nav>
    </header>"""


def build_hero(hero: dict, category: str) -> str:
    h1 = hero["h1"] or "数据可视化"
    subtitle = hero["subtitle"] or ""
    tagline_line = f'\n        <p class="tagline">{hero["tagline"]}</p>' if hero["tagline"] else ""
    subtitle_line = f'\n        <p class="subtitle">{subtitle}</p>' if subtitle else ""
    return f"""    <section class="hero">
        <p class="breadcrumb"><a href="../index.html">首页</a> / <a href="../dashboard.html">数据看板</a> / {h1}</p>
        <p class="kicker">{category}</p>
        <h1>{h1}</h1>{subtitle_line}{tagline_line}
    </section>"""


def build_footer(extra_link: str = "") -> str:
    return f"""    <footer class="site-footer">
        <div>
            <div class="footer-brand">详解西游记</div>
            <div class="footer-meta">v2.2.86 · W334 · 数据可视化{extra_link}</div>
        </div>
        <nav aria-label="页脚导航">
            <a href="../index.html">首页</a>
            <a href="../dashboard.html">看板</a>
            <a href="tag-cloud.html">标签云</a>
            <a href="text-search.html">全文检索</a>
        </nav>
    </footer>"""


def migrate_file(filepath: Path, dry_run: bool = False) -> str:
    """迁移单个文件。返回状态描述。"""
    html = filepath.read_text(encoding="utf-8")

    # 幂等检查：已含 system.css 则跳过
    if "system.css" in html:
        return "SKIP (already migrated)"

    # 必须有旧版 hero 才处理
    if '<header class="hero"' not in html and "<header class='hero'" not in html:
        return "SKIP (no standard hero found)"

    # 提取信息
    title = extract_title(html)
    hero = extract_hero_content(html)
    page_css = extract_page_css(html)
    category = get_category(filepath.name)
    footer_extra = extract_footer_links(html)

    # 提取 body 内容（hero 之后到 footer 之前）
    # 找 hero 结束位置
    hero_end = re.search(r'</header>\s*', html)
    if not hero_end:
        return "SKIP (cannot find hero end)"

    # 找 footer 开始位置
    footer_start = re.search(r'\s*<footer', html)
    if not footer_start:
        return "SKIP (cannot find footer)"

    # body 内容 = hero 之后到 footer 之前
    body_content = html[hero_end.end():footer_start.start()]

    # 清理 body 内容中的旧 breadcrumb 和旧 container 包装
    body_content = re.sub(r'<div class="breadcrumb">.*?</div>\s*', '', body_content, flags=re.DOTALL)
    # 替换 <main class="container"> 为 <main id="main" class="page-wrap" ...>
    body_content = re.sub(
        r'<main class="container"[^>]*>',
        '<main id="main" class="page-wrap" style="padding-top:32px;padding-bottom:64px;">',
        body_content
    )
    # 如果没有 <main>，包一个
    if "<main" not in body_content:
        body_content = f'    <main id="main" class="page-wrap" style="padding-top:32px;padding-bottom:64px;">\n{body_content}\n    </main>'

    # 提取 </footer> 之后的内容（script 等）
    after_footer = re.search(r'</footer>\s*', html)
    tail_content = html[after_footer.end():] if after_footer else ""

    # 组装新文件
    new_html = "\n".join([
        build_new_head(title, page_css),
        "<body>",
        '    <a class="skip-link" href="#main" style="position:absolute;left:-9999px;top:0;background:var(--dark);color:var(--dark-text);padding:10px 18px;z-index:100;">跳到主要内容</a>',
        "",
        build_topnav(),
        "",
        build_hero(hero, category),
        "",
        body_content.strip(),
        "",
        build_footer(footer_extra),
        "",
        tail_content.strip(),
        "</body>",
        "</html>",
    ])

    if dry_run:
        return f"WOULD MIGRATE: {title} [{category}] (css {len(page_css)} chars)"

    filepath.write_text(new_html, encoding="utf-8")
    return f"MIGRATED: {title} [{category}]"


def main():
    parser = argparse.ArgumentParser(description="迁移 site/data/ 页面到新设计系统")
    parser.add_argument("--dry-run", action="store_true", help="预览模式，不写入文件")
    parser.add_argument("--files", nargs="*", help="仅迁移指定文件（文件名，非路径）")
    args = parser.parse_args()

    if not SITE_DATA.exists():
        print(f"ERROR: {SITE_DATA} not found")
        sys.exit(1)

    # 收集目标文件
    if args.files:
        targets = [SITE_DATA / f for f in args.files]
    else:
        targets = sorted(SITE_DATA.glob("*.html"))

    migrated = 0
    skipped = 0
    errors = 0

    for filepath in targets:
        if filepath.name in SKIP_FILES:
            print(f"  SKIP (excluded): {filepath.name}")
            skipped += 1
            continue
        if not filepath.exists():
            print(f"  ERROR: {filepath.name} not found")
            errors += 1
            continue
        try:
            result = migrate_file(filepath, dry_run=args.dry_run)
            print(f"  {result}: {filepath.name}")
            if result.startswith("SKIP"):
                skipped += 1
            elif result.startswith("MIGRATED") or result.startswith("WOULD"):
                migrated += 1
        except Exception as e:
            print(f"  ERROR: {filepath.name} — {e}")
            errors += 1

    print(f"\n{'[DRY RUN] ' if args.dry_run else ''}完成：{migrated} 迁移 / {skipped} 跳过 / {errors} 错误")


if __name__ == "__main__":
    main()
