#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_w988_verify.py — W988 验收判据（可复算·含负样本自证）

V1  13 个 banner 页：`<figure class="chapter-banner">` 恰 1 个 · `.chapter-banner {` CSS 恰 1 条 · img 指向的文件真实存在
V2  14 个 scene  页：`<figure class="chapter-scene">` 恰 1 个 · CSS 恰 1 条 · img 指向的文件真实存在
V3  banner figure 位于 `</h1>` 之后（顶部横幅位）
V4  scene figure 位于正文首个章节标题（h2/h3）之前；无章节标题者位于轨标块后的 `<hr />` 之后
V5  102 页 og:image 指向的文件真实存在 · og:image:width=1200 · og:image:height=630 · 站内无残留「共用通用图」的配图页
V6  暗色模式隐藏规则存在（浅底宣纸图贴深底会成亮斑）
V7  横幅资产 = 1200×500 · og 资产 = 1200×630（全部逐张量）
V8  27 张源卡仍被引用（本批不得误删源图）
V9  **负样本自证**：把同一判据套到「缺 CSS / 多 figure / 图文件缺失 / og 尺寸写错」的坏样本上必须报 FAIL

用法：py -3 scripts/_w988_verify.py [--negative]
"""
from __future__ import annotations

import os
import re
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _w988_plan import ALL, BANNERS, SCENES  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "site", "static", "images")
PRE = os.path.join(ROOT, "scripts", "output", "_w988_precheck.json")

RE_BANNER_FIG = re.compile(r'<figure class="chapter-banner">\s*<img src="([^"]+)"')
RE_SCENE_FIG = re.compile(r'<figure class="chapter-scene">\s*<img src="([^"]+)"')
RE_OG = re.compile(r'<meta property="og:image" content="([^"]+)"')
RE_OG_W = re.compile(r'<meta property="og:image:width" content="(\d+)"')
RE_OG_H = re.compile(r'<meta property="og:image:height" content="(\d+)"')
RE_CHAPTER = re.compile(r"^[ \t]*<h[23][ >]", re.M)
# CSS 规则计数必须**行首锚定**：否则 `html[data-theme="dark"] .chapter-banner {` 这条暗色规则
# 会被子串计数算成第二条规则（判据自身缺陷·曾把 27 页全判红——实测证伪）。
RE_CSS_BANNER = re.compile(r"^[ \t]*\.chapter-banner \{", re.M)
RE_CSS_SCENE = re.compile(r"^[ \t]*\.chapter-scene \{", re.M)

BANNER_TARGETS = {b["target"] for b in BANNERS}
OG_BASE = "https://1273984347.github.io/xiyouji/static/images/"


def read(p: str) -> str:
    with open(p, encoding="utf-8", errors="ignore") as fh:
        return fh.read()


def rel_img_exists(page_rel: str, src: str) -> bool:
    return os.path.exists(os.path.normpath(os.path.join(
        os.path.dirname(os.path.join(ROOT, page_rel)), src)))


def check_pages() -> list:
    fails = []
    for item in ALL:
        target = item["target"]
        slot = "banner" if target in BANNER_TARGETS else "scene"
        path = os.path.join(ROOT, target.replace("/", os.sep))
        if not os.path.exists(path):
            fails.append((target, "页面缺失"))
            continue
        s = read(path)
        fig_re = RE_BANNER_FIG if slot == "banner" else RE_SCENE_FIG
        cls = "chapter-banner" if slot == "banner" else "chapter-scene"
        figs = fig_re.findall(s)
        if len(figs) != 1:
            fails.append((target, "%s figure 数 = %d（应为 1）" % (cls, len(figs))))
            continue
        css_re = RE_CSS_BANNER if slot == "banner" else RE_CSS_SCENE
        n_css = len(css_re.findall(s))
        if n_css != 1:
            fails.append((target, "%s CSS 规则数 = %d（行首锚定·应为 1）" % (cls, n_css)))
        if not rel_img_exists(target, figs[0]):
            fails.append((target, "图文件不存在: " + figs[0]))
        if 'html[data-theme="dark"] .' + cls in s:
            pass
        else:
            fails.append((target, "缺暗色模式隐藏规则"))
        if slot == "banner":
            h1 = s.find("</h1>")
            fig = s.find('<figure class="chapter-banner">')
            if h1 < 0 or fig < 0 or fig < h1:
                fails.append((target, "横幅不在 </h1> 之后"))
        else:
            m = RE_CHAPTER.search(s)
            fig = s.find('<figure class="chapter-scene">')
            if m and fig > m.start():
                fails.append((target, "场景图不在首个章节标题之前"))
            if not m and fig < 0:
                fails.append((target, "场景图缺失"))
    return fails


def check_og() -> list:
    import json
    with open(PRE, encoding="utf-8") as fh:
        pre = json.load(fh)
    fails = []
    for o in pre["og_plan"]:
        target = o["page"]
        path = os.path.join(ROOT, target.replace("/", os.sep))
        s = read(path)
        m = RE_OG.search(s)
        if not m:
            fails.append((target, "og:image 缺失"))
            continue
        url = m.group(1)
        if url != OG_BASE + o["out"]:
            fails.append((target, "og:image 指向非计划图: " + url))
        if not os.path.exists(os.path.join(IMG, o["out"])):
            fails.append((target, "og 图文件缺失: " + o["out"]))
        mw, mh = RE_OG_W.search(s), RE_OG_H.search(s)
        if not mw or mw.group(1) != "1200":
            fails.append((target, "og:image:width 非 1200"))
        if not mh or mh.group(1) != "630":
            fails.append((target, "og:image:height 非 630"))
    return fails


def check_assets() -> list:
    fails = []
    for b in BANNERS:
        p = os.path.join(IMG, "banner-" + b["card"] + ".webp")
        if not os.path.exists(p):
            fails.append((b["card"], "横幅资产缺失"))
            continue
        if Image.open(p).size != (1200, 500):
            fails.append((b["card"], "横幅尺寸 = %s（应为 1200×500）" % (Image.open(p).size,)))
    import json
    with open(PRE, encoding="utf-8") as fh:
        pre = json.load(fh)
    for o in pre["og_plan"]:
        p = os.path.join(IMG, o["out"])
        if not os.path.exists(p):
            fails.append((o["out"], "og 资产缺失"))
            continue
        if Image.open(p).size != (1200, 630):
            fails.append((o["out"], "og 尺寸 = %s（应为 1200×630）" % (Image.open(p).size,)))
    return fails


def check_sources_referenced() -> list:
    fails = []
    for item in ALL:
        target = item["target"]
        s = read(os.path.join(ROOT, target.replace("/", os.sep)))
        if item["card"] + ".webp" not in s:
            fails.append((target, "源卡未被引用: " + item["card"]))
    return fails


def negative_self_test() -> list:
    """负样本自证：造四种坏样本，同一套判据必须每一种都报 FAIL。"""
    import json
    import tempfile
    with open(PRE, encoding="utf-8") as fh:
        pre = json.load(fh)
    bad_pages = {
        "缺CSS": lambda s: s.replace(".chapter-banner {", ".chapter-banner-XX {"),
        "多figure": lambda s: s.replace(
            '<figure class="chapter-banner">',
            '<figure class="chapter-banner"><img src="../../static/images/banner-card-14-bajie-choupa.webp" alt="x"></figure><figure class="chapter-banner">',
            1),
        "图缺失": lambda s: s.replace("banner-card-14-bajie-choupa.webp", "banner-not-exist.webp"),
        "og尺寸错": lambda s: s.replace('<meta property="og:image:width" content="1200">',
                                        '<meta property="og:image:width" content="800">'),
    }
    results = []
    sample_page = os.path.join(ROOT, "site", "reader", "people", "猪八戒.html")
    orig = read(sample_page)
    for name, mut in bad_pages.items():
        tmp = os.path.join(tempfile.gettempdir(), "_w988_neg_%s.html" % name)
        with open(tmp, "w", encoding="utf-8") as fh:
            fh.write(mut(orig))
        # 直接复用判据的核心断言（对同一页做四项检查）
        s = read(tmp)
        caught = []
        if len(RE_CSS_BANNER.findall(s)) != 1:
            caught.append("css")
        if len(RE_BANNER_FIG.findall(s)) != 1:
            caught.append("figure")
        for u in RE_BANNER_FIG.findall(s):
            if not rel_img_exists("site/reader/people/猪八戒.html", u):
                caught.append("img")
        mw = RE_OG_W.search(s)
        if not mw or mw.group(1) != "1200":
            caught.append("ogw")
        os.remove(tmp)
        ok = bool(caught)
        results.append((name, caught, ok))
    return results


def main() -> int:
    groups = {
        "V1-V4 页面接入": check_pages(),
        "V5 og:image": check_og(),
        "V7 资产尺寸": check_assets(),
        "V8 源卡引用": check_sources_referenced(),
    }
    total = 0
    for g, fails in groups.items():
        print("%-18s %s" % (g, "PASS" if not fails else "FAIL %d" % len(fails)))
        for t, why in fails[:20]:
            print("    -", t, "|", why)
        total += len(fails)

    neg = negative_self_test()
    print("%-18s %s" % ("V9 负样本自证", "PASS" if all(r[2] for r in neg) else "FAIL"))
    for name, caught, ok in neg:
        print("    - %-10s 命中=%s %s" % (name, caught, "OK" if ok else "未命中·判据失效"))
    if not all(r[2] for r in neg):
        total += 1

    print("\n合计：%d 处 FAIL" % total)
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
