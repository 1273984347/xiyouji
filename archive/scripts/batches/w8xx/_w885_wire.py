#!/usr/bin/env python3
"""_w885_wire.py — W885 接线批：把已入库的水墨素材真正接到页面上。

三件事（全部「改源不摸副本」，故下次重生成不会抹掉）：
① **site/system.css 加一条 `.hero-ornament` 规则**（源文件）→ 数据页/可视化页外链 system.css，
   规则立即生效；下次 inline_css 重跑时它会被内联进副本，不会像「写进副本」那样被抹掉。
② **site/data/*.html（87·去 _shell.html）+ site/en/*.html**：在 `.hero` 区内挂一张**深底直显版**
   viz 插画（浅底宣纸图贴在暗色 hero 上会成亮斑，故暗带用深底版）。按页名映射四类母题。
③ **首页 site/index.html 与 site/en/index.html**：给 `.masthead` 加浅底 Hero 横幅底图——该段文字
   落在图的底部留白带上（底图专门留的），深墨字对浅底可读。

行尾原样保留（读写均 newline=""）；已接过的页跳过（幂等）。
用法：python scripts/_w885_wire.py [--dry-run]
"""
from __future__ import annotations

import argparse
import glob
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def rel(p: str) -> str:
    return os.path.relpath(p, ROOT).replace("\\", "/")


def read(p: str) -> str:
    with io.open(os.path.normpath(p), encoding="utf-8", newline="") as f:
        return f.read()


def write(p: str, s: str) -> None:
    with io.open(os.path.normpath(p), "w", encoding="utf-8", newline="") as f:
        f.write(s)


# ---- 页名 → viz 母题（深底直显版） ----
def viz_for(name: str) -> str:
    n = name.lower()
    if any(k in n for k in ("network", "relationships", "social-media")):
        return "viz-dark-01-network"
    if "heatmap" in n:
        return "viz-dark-02-heatmap"
    if "radar" in n:
        return "viz-dark-03-radar"
    if "timeline" in n:
        return "viz-dark-04-timeline"
    return "viz-dark-02-heatmap"      # 默认：疏密墨点阵（万用母题）


CSS_RULE = """/* W885：数据页/可视化页页头装饰插画（深底直显版·浅底宣纸图贴在暗色 hero 上会成亮斑） */
.hero-ornament {
    position: absolute;
    right: clamp(var(--space-6), 5vw, var(--space-12));
    bottom: clamp(var(--space-5), 4vw, var(--space-9));
    width: clamp(140px, 18vw, 240px);
    height: auto;
    opacity: .9;
    pointer-events: none;
}

@media (max-width: 768px) {

    .hero-ornament {
        display: none;
    }
}
"""

# 内联副本版（与内联 CSS 的缩进风格一致）：**站点页面在 file:// 下由 CSP 的 style-src 'self' 拦掉
# 外链样式表，样式实际全部来自每页的内联副本**（即 inline_css.py 从 site/system.css 注入的那份）。
# 故本规则须「源 + 内联副本」双写：源保证下次 inline_css 重跑时仍带它，内联副本保证当前即生效。
CSS_RULE_INLINE = """/* W885：页头装饰插画定位（与 site/system.css 同源·内联副本因 file:// 下 CSP 拦外链而必须自带） */
    .hero-ornament {
        position: absolute;
        right: clamp(var(--space-6), 5vw, var(--space-12));
        bottom: clamp(var(--space-5), 4vw, var(--space-9));
        width: clamp(140px, 18vw, 240px);
        height: auto;
        opacity: .9;
        pointer-events: none;
    }

    @media (max-width: 768px) {

        .hero-ornament {
            display: none;
        }
    }
"""


def inject_inline_rule(p: str) -> bool:
    """把 .hero-ornament 规则补进该页的内联副本块（找出含 .hero 规则的那块，插在其末尾）。"""
    s = read(p)
    if ".hero-ornament" in s:
        return False
    for m in re.finditer(r"(<style[^>]*>)(.*?)(</style>)", s, re.S):
        body = m.group(2)
        if ".hero {" not in body:
            continue
        # 取**第一个**含 .hero 规则的块＝inline_css.py 从 site/system.css 注入的那份副本
        new_body = body.rstrip("\n") + "\n" + CSS_RULE_INLINE
        s = s[:m.start(2)] + new_body + s[m.end(2):]
        write(p, s)
        return True
    return False



def wire_system_css(dry: bool) -> int:
    p = os.path.join(ROOT, "site", "system.css")
    s = read(p)
    if ".hero-ornament" in s:
        print("  system.css：已有 .hero-ornament 规则·跳过")
        return 0
    if not s.endswith("\n"):
        s += "\n"
    s += "\n" + CSS_RULE
    if not dry:
        write(p, s)
    print("  system.css：追加 .hero-ornament 规则（%d 字符）" % len(CSS_RULE))
    return 1


def wire_hero_ornaments(dry: bool) -> int:
    """在有 .hero 的数据页/英文页插入装饰插画 <img>。"""
    pages = []
    for pat in ("site/data/*.html", "site/en/*.html"):
        pages += sorted(glob.glob(os.path.join(ROOT, pat)))
    changed = 0
    for p in pages:
        name = os.path.basename(p)
        if name in ("_shell.html", "_template.html"):
            continue
        s = read(p)
        if 'class="hero"' not in s:
            continue
        if "hero-ornament" in s:
            continue
        i = s.find('class="hero"')
        # zh 侧是 <section class="hero">，en 侧是 <header class="hero"> —— 按开标签类型找闭合标签
        m = re.search(r"<(section|header)[^>]*class=\"hero\"[^>]*>", s)
        if not m:
            print("  [跳过·未找到 hero 开标签] %s" % rel(p))
            continue
        close_tag = "</%s>" % m.group(1)
        j = s.find(close_tag, m.end())
        if i < 0 or j < 0:
            print("  [跳过·结构不匹配] %s" % rel(p))
            continue
        src = "../static/images/%s.webp" % viz_for(name)
        img = ('\n            <img class="hero-ornament" src="%s" alt="" aria-hidden="true" '
               'loading="lazy" decoding="async">\n        ' % src)
        s2 = s[:j] + img + s[j:]
        if not dry:
            write(p, s2)
            inject_inline_rule(p)     # 规则同步进内联副本（file:// 下外链被 CSP 拦·样式只认内联）
        changed += 1
    print("  装饰插画：%d 页接入" % changed)
    return changed


def wire_inline_rules(dry: bool) -> int:
    """给所有已插装饰插画的页补内联规则（幂等·与插图步骤解耦，便于重跑）。"""
    n = 0
    for pat in ("site/data/*.html", "site/en/*.html"):
        for p in sorted(glob.glob(os.path.join(ROOT, pat))):
            s = read(p)
            if "hero-ornament" not in s:
                continue
            if ".hero-ornament" in s:          # 规则已在内联副本里
                continue
            if dry:
                n += 1
                continue
            if inject_inline_rule(p):
                n += 1
    print("  内联副本补规则：%d 页" % n)
    return n


MASTHEAD_RULE = """            background-image: url('%s');
            background-size: cover;
            background-position: center bottom;
            background-repeat: no-repeat;
"""

MASTHEADS = [
    # zh 首页首屏是浅色 .masthead 区 → 铺浅底 Hero 横幅（文字落在图底部的留白带上）。
    # en 首页首屏是暗色 .hero 区，system.css 的 .hero 规则已带 W879 的浅底浓墨底图 + soft-light
    # 合成（暗底上显影为剪影），故 **不再重复加图**。
    ("site/index.html", "static/images/hero-01-xihai-yunhai.webp"),
]


def wire_masthead(dry: bool) -> int:
    changed = 0
    for rp, img in MASTHEADS:
        p = os.path.join(ROOT, rp)
        s = read(p)
        if "hero-0" in s and "background-image" in s:
            print("  %s：已接·跳过" % rp)
            continue
        m = re.search(r"(\n        \.masthead \{\n)(.*?)(\n        \})", s, re.S)
        if not m:
            print("  [跳过·未找到 .masthead 规则] %s" % rp)
            continue
        rule = MASTHEAD_RULE % img
        s2 = s[:m.end(2)] + "\n" + rule.rstrip("\n") + s[m.end(2):]
        if not dry:
            write(p, s2)
        changed += 1
    print("  首页首屏底图：%d 页接入" % changed)
    return changed


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    print("[%s] W885 接线批" % ("DRY-RUN" if args.dry_run else "APPLY"))
    wire_system_css(args.dry_run)
    wire_hero_ornaments(args.dry_run)
    wire_inline_rules(args.dry_run)
    wire_masthead(args.dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())
