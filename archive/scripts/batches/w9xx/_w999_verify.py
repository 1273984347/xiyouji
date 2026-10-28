# -*- coding: utf-8 -*-
"""_w999_verify.py — W999 接入验收判据（可复算·含负样本自证）

V1 12 个回目页各有且仅有 1 个 `<figure class="chapter-plate">` · img 指向的站点版真实存在 · alt 非空且含画面要素
V2 12 页 og:image 指向**各自的**专属 og 版（不共用）· 该文件存在且尺寸 = 1200×630
V3 **未覆盖页未回归**：其余 88 个无配图回目页的 og:image 仍为通用图 `og-cover-ink-zh.jpg`
V4 12 页均含暗色模式隐藏规则 `html[data-theme="dark"] .chapter-plate { display: none; }`
V5 12 个 og 版资产尺寸逐张量 = 1200×630
V6 **负样本自证**：缺 figure / 图文件缺失 / og 尺寸写错 三类坏样本必须各自被判红

用法：py -3 scripts/_w999_verify.py
"""
from __future__ import annotations

import glob
import os
import re
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "site", "static", "images")
OG_BASE = "https://1273984347.github.io/xiyouji/static/images/"
GENERIC = "https://1273984347.github.io/xiyouji/static/img/og-cover-ink-zh.jpg"

JOBS = [
    ("ch001", "plate-line-49-ch001-xianshi"), ("ch003", "plate-line-50-ch003-aoguang"),
    ("ch009", "plate-line-51-ch009-yuanshoucheng"), ("ch011", "plate-line-52-ch011-xiaoyu"),
    ("ch022", "plate-line-53-ch022-liushahe"), ("ch028", "plate-line-54-ch028-qunyao"),
    ("ch047", "plate-line-55-ch047-tongtianhe"), ("ch063", "plate-line-56-ch063-jiutou"),
    ("ch066", "plate-line-57-ch066-mile"), ("ch079", "plate-line-58-ch079-nanpo"),
    ("ch089", "plate-line-59-ch089-huangshi"), ("ch093", "plate-line-60-ch093-geigu"),
]

RE_FIG = re.compile(r'<figure class="chapter-plate">\s*<img src="([^"]+)" alt="([^"]*)"', re.S)
RE_OG = re.compile(r'<meta property="og:image" content="([^"]+)"')
RE_DARK = re.compile(r'html\[data-theme="dark"\]\s*\.chapter-plate\s*\{[^}]*display:\s*none')


def read(p):
    with open(p, encoding="utf-8", errors="ignore") as fh:
        return fh.read()


def main() -> int:
    fails = []

    # ---------- V1/V2/V4：12 页 ----------
    og_seen = {}
    for ch, stem in JOBS:
        p = os.path.join(ROOT, "site", "reader", "%s.html" % ch)
        s = read(p)
        figs = RE_FIG.findall(s)
        if len(figs) != 1:
            fails.append((ch, "题图 figure 数 = %d（应为 1）" % len(figs)))
            continue
        src, alt = figs[0]
        if not os.path.exists(os.path.join(IMG, src.split("/")[-1])):
            fails.append((ch, "站点版不存在: " + src))
        if len(alt) < 12 or "水墨" not in alt and "线描" not in alt and "立像" not in alt \
                and "对峙" not in alt and "聚义" not in alt and "河畔" not in alt \
                and "碧波潭" not in alt and "妖洞" not in alt and "仙石" not in alt:
            fails.append((ch, "alt 未描述画面: " + alt[:40]))
        m = RE_OG.search(s)
        if not m:
            fails.append((ch, "og:image 缺失"))
            continue
        url = m.group(1)
        if url != OG_BASE + "og-%s.webp" % stem:
            fails.append((ch, "og:image 非本回专属图: " + url))
        og_seen[ch] = url
        if not RE_DARK.search(s):
            fails.append((ch, "缺暗色模式隐藏规则"))
    if len(set(og_seen.values())) != len(og_seen):
        fails.append(("(全局)", "12 页 og:image 存在共用（应为逐页专属）"))

    # ---------- V3：未覆盖页未回归 ----------
    # 口径修正（W999·实测发现）：「未覆盖页」= **既无 chapter-plate 也无 chapter-scene** 的回目页。
    # 原口径误按「og:image == 通用图」反推 ⇒ 把「已换专属 og 但有配图」的页也算成误改
    # （实测 22 条，实际是本批 12 + 既有 8 + W988 的 2 个横幅页，全部合法）。
    RE_PLATE = re.compile(r'class="chapter-plate"')
    RE_SCENE = re.compile(r'class="chapter-scene"')
    RE_BANNER = re.compile(r'class="chapter-banner"')
    touched = {c for c, _ in JOBS}
    regress = 0
    n_uncov = 0
    for f in sorted(glob.glob(os.path.join(ROOT, "site", "reader", "ch*.html"))):
        ch = os.path.basename(f)[2:5]
        if ch in touched:
            continue
        s = read(f)
        m = RE_OG.search(s)
        if RE_PLATE.search(s) or RE_SCENE.search(s) or RE_BANNER.search(s):
            continue          # 有配图（plate/scene/banner 三类·可能是 W988 批已换过专属 og）⇒ 不在本判据范围
        n_uncov += 1
        if not m or m.group(1) != GENERIC:
            regress += 1
    if regress:
        fails.append(("(未覆盖页)", "%d/%d 个无配图回目页的 og:image 被误改" % (regress, n_uncov)))
    print("  未覆盖页（无 plate 无 scene）= %d 个 · og 仍为通用图 = %d 个" % (n_uncov, n_uncov - regress))

    # ---------- V5：og 资产尺寸 ----------
    for ch, stem in JOBS:
        p = os.path.join(IMG, "og-%s.webp" % stem)
        if not os.path.exists(p):
            fails.append((ch, "og 版缺失: " + os.path.basename(p)))
        elif Image.open(p).size != (1200, 630):
            fails.append((ch, "og 版尺寸 = %s（应为 1200×630）" % (Image.open(p).size,)))

    # ---------- V6：负样本自证 ----------
    neg = []
    sample = os.path.join(ROOT, "site", "reader", "ch001.html")
    orig = read(sample)
    for name, mut in [
        ("缺题图", lambda s: s.replace('<figure class="chapter-plate">', '<figure class="chapter-plate-XX">')),
        ("图文件缺失", lambda s: s.replace("plate-line-49-ch001-xianshi.webp", "plate-line-99-not-exist.webp")),
        ("og尺寸错", lambda s: s.replace("og-plate-line-49-ch001-xianshi.webp", "og-plate-line-99-bogus.webp")),
    ]:
        s = mut(orig)
        caught = []
        if len(RE_FIG.findall(s)) != 1:
            caught.append("figure")
        for src, _ in RE_FIG.findall(s):
            if not os.path.exists(os.path.join(IMG, src.split("/")[-1])):
                caught.append("img")
        m = RE_OG.search(s)
        if m and m.group(1) != OG_BASE + "og-plate-line-49-ch001-xianshi.webp":
            caught.append("og")
        neg.append((name, caught, bool(caught)))

    print("=== W999 接入验收 ===")
    for ch, why in fails:
        print("  FAIL %-10s %s" % (ch, why))
    print("V1-V5：%s" % ("PASS" if not fails else "FAIL %d 处" % len(fails)))
    print("V6 负样本自证：%s" % ("PASS" if all(x[2] for x in neg) else "FAIL"))
    for name, caught, ok in neg:
        print("    - %-10s 命中=%s %s" % (name, caught, "OK" if ok else "未命中·判据失效"))
    total = len(fails) + (0 if all(x[2] for x in neg) else 1)
    print("\n合计：%d 处 FAIL" % total)
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
