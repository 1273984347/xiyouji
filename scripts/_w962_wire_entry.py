#!/usr/bin/env python3
"""_w962_wire_entry.py — W962 差异化推广批：入口层接线（9 页 · cards 模式）。

推广口径（用户 2026-10-26 裁决「按页型差异化推广」）：
  · **入口层**（本批）：7 个 reader 体裁 hub 页 + curated + guide ⇒ cards 模式
  · **内容层**（不做）：reader 622 页正文 / data 88 页 / en 138 页 ⇒ 暂不铺 sections
  · **不动**：index.html（已有 intro）· dashboard / dukou-engine / 404 / rum-viewer / visit-viewer
    （重交互页或工具页，动效收益低且干扰风险高）

编排单元：
  · hub 页：容器 `.reader-wrap` + target `.reader-idx a`（索引条目，stagger 自适应封顶 ≈1.2 s）
  · curated：容器 `.curated-grid`（2 处）+ target `.curated-card`
  · guide：容器 `.paths-grid` + target `.path-card`

纪律：字节级改写（保行尾）· 每处先断言命中数（fail-closed）· 幂等 · 单页增量上限 250 B。

用法：py -3 scripts/_w962_wire_entry.py [--dry-run]
"""
import argparse
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CARDS_ATTR = ' data-gsap="cards" data-gsap-target=".reader-idx a"'
CARDS_ATTR_CURATED = ' data-gsap="cards" data-gsap-target=".curated-card"'
CARDS_ATTR_GUIDE = ' data-gsap="cards" data-gsap-target=".path-card"'

# (页, 路径前缀, 属性锚点, 新属性, 锚点期望次数, script 锚点)
PAGES = [
    ("site/reader/index.html", "../static/js/",
     '<main class="reader-wrap">', CARDS_ATTR, 1,
     '<script src="../js/reader-enhance.js" defer></script>'),
    ("site/reader/themes-hub.html", "../static/js/",
     '<main class="reader-wrap">', CARDS_ATTR, 1,
     '<script src="../js/reader-enhance.js" defer></script>'),
    ("site/reader/themes/index.html", "../../static/js/",
     '<main class="reader-wrap">', CARDS_ATTR, 1,
     '<script src="../../js/reader-enhance.js" defer></script>'),
    ("site/reader/people/index.html", "../../static/js/",
     '<main class="reader-wrap">', CARDS_ATTR, 1,
     '<script src="../../js/reader-enhance.js" defer></script>'),
    ("site/reader/essays/index.html", "../../static/js/",
     '<main class="reader-wrap">', CARDS_ATTR, 1,
     '<script src="../../js/reader-enhance.js" defer></script>'),
    ("site/reader/culture/index.html", "../../static/js/",
     '<main class="reader-wrap">', CARDS_ATTR, 1,
     '<script src="../../js/reader-enhance.js" defer></script>'),
    ("site/reader/poetry/index.html", "../../static/js/",
     '<main class="reader-wrap">', CARDS_ATTR, 1,
     '<script src="../../js/reader-enhance.js" defer></script>'),
    ("site/guide.html", "static/js/",
     '<div class="paths-grid">', CARDS_ATTR_GUIDE, 1,
     '<script defer src="js/visit-log.js"></script>'),
]

# W962 本批不做项（透明留痕）：
#   · **site/curated.html**——其 2 个 .curated-grid 分属 3 个 `.section.reveal-in` 区块；
#     若把 cards 属性提到共同父（= .section.reveal-in）会与既有 reveal-in 进场机制交叠
#     （父级自身 opacity 0 + 我们对后代设初始态 ⇒ 双重控制语义），
#     若逐个 grid 加属性则单页增量 269 B 超 250 B 上限 ⇒ 本批不做，留专项批处理。
#   · **内容层** reader 622 页正文 / data 88 页 / en 138 页 ⇒ 暂不铺 sections（用户裁决口径）
#   · **index.html**（已有 intro）· dashboard / dukou-engine / 404 / rum-viewer / visit-viewer
#     （重交互页或工具页，动效收益低且干扰风险高）

SCRIPT_BLOCK = ('<script defer src="{p}gsap.min.js"></script>'
                '<script defer src="{p}ScrollTrigger.min.js"></script>'
                '<script defer src="{p}motion-gsap.js"></script>')


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    total = 0
    for rel, prefix, attr_anchor, attr_new, attr_expect, script_anchor in PAGES:
        path = os.path.join(ROOT, rel.replace("/", os.sep))
        with open(path, "rb") as f:
            raw = f.read()
        before = len(raw)
        if ('data-gsap="cards"' in raw.decode("utf-8", "ignore")):
            print("SKIP   %s：已接入" % rel)
            continue
        ab = attr_anchor.encode("utf-8")
        n = raw.count(ab)
        if n != attr_expect:
            print("ABORT  %s：属性锚点命中 %d ≠ 期望 %d（%s）" % (rel, n, attr_expect, attr_anchor))
            return 1
        raw = raw.replace(ab, (attr_anchor + attr_new).encode("utf-8"))
        sb = script_anchor.encode("utf-8")
        n = raw.count(sb)
        if n != 1:
            print("ABORT  %s：脚本锚点命中 %d ≠ 期望 1（%s）" % (rel, n, script_anchor))
            return 1
        nl = b"\r\n" if b"\r\n" in raw else b"\n"
        block = SCRIPT_BLOCK.format(p=prefix).encode("utf-8")
        raw = raw.replace(sb, sb + nl + block + nl, 1)
        delta = len(raw) - before
        total += delta
        print("%-6s %-42s 增量 %+d B" % ("DRY" if args.dry_run else "OK", rel, delta))
        if delta > 250:
            print("ABORT  %s：单页增量 %d B 超 250 B 上限" % (rel, delta))
            return 1
        if args.dry_run:
            continue
        with open(path, "wb") as f:
            f.write(raw)
    print("%s完成：%d 页 · 合计增量 %+d B"
          % ("DRY-RUN " if args.dry_run else "接入", len(PAGES), total))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
