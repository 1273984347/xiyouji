#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_w988_insert.py — W988 接入：27 张水墨卡上站 + 102 页 og:image 换专属图

三件事（每件都幂等）：
  ① **13 张角色页顶部横幅**：新立 `.chapter-banner` 规范（宽幅 1200×500·限宽 720px·暗色隐藏），
     插在 `</h1>` 之后（若该页已有题图 figure ⇒ 横幅在其**之前**，形成「横幅在上·竖题图在下」的宽窄分层）。
  ② **14 张主题页场景图**：沿用 W987 的 `.chapter-scene` 规范（1:1·限宽 520px·可带印章·暗色隐藏），
     插在正文首个章节标题（`<h2>` 或 `<h3>`）之前；该页若无章节标题 ⇒ 插在轨标块之后的 `<hr />` 之后。
  ③ **102 页 og:image**：由「全站共用一张通用图」改为**该页首屏第一张配图**的 1200×630 裁切版。

写盘纪律：原子替换（tmp + os.replace）·保原行尾（newline=''）·同文件多次写串行。
用法：py -3 scripts/_w988_insert.py [--dry-run]
"""
from __future__ import annotations

import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _w988_plan import ALL, BANNERS, SCENES  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRE = os.path.join(ROOT, "scripts", "output", "_w988_precheck.json")
OG_BASE = "https://1273984347.github.io/xiyouji/static/images/"

CSS_BANNER = """    /* W988：角色页顶部横幅（水墨意境卡族·1:1 源另裁 1200×500 宽幅·与题图 .chapter-plate 刻意分开的独立规范） */
    .chapter-banner { margin: 26px auto 32px; max-width: 720px; }
    .chapter-banner img { width: 100%; height: auto; display: block; opacity: .95; }
    html[data-theme="dark"] .chapter-banner { display: none; }
"""

CSS_SCENE = """    /* W987：场景插图（水墨意境卡族·可带印章·与题图 .chapter-plate 刻意分开的独立规范） */
    .chapter-scene { margin: 34px auto 30px; max-width: 520px; }
    .chapter-scene img { width: 100%; height: auto; display: block; opacity: .95; }
    html[data-theme="dark"] .chapter-scene { display: none; }
"""

RE_STYLE_END = re.compile(r"[ \t]*</style>")
RE_H1_END = re.compile(r"</h1>")
RE_CHAPTER = re.compile(r"^[ \t]*<h[23][ >]", re.M)
RE_HR = re.compile(r"<hr\s*/?>", re.M)
RE_BLOCKQUOTE_END = re.compile(r"</blockquote>")
RE_OG_IMAGE = re.compile(r'(<meta property="og:image" content=")([^"]+)(")')


def read_text(path: str):
    raw = io.open(path, "rb").read()
    return raw.decode("utf-8"), ("\r\n" if b"\r\n" in raw else "\n")


def write_text(path: str, text: str, nl: str) -> None:
    """原子替换写盘。

    **绝不**做 `text.replace("\n", nl)`：读入的 text 已是磁盘原文（工作区为 CRLF·
    git core.autocrlf=true 下仓库存 LF），再把 "\\n" 替换成 "\\r\\n" 会把已有的
    CRLF 变成 CRCRLF（每个换行多一个 CR）⇒ 整文件行尾被污染。
    （W988 实证：102 个页面 CRLF→CRCRLF，浏览器里 CSS 规则疑似失效。）
    ⇒ 原样写字节，行尾交由 git 的 autocrlf 处理。
    """
    tmp = path + ".tmp"
    io.open(tmp, "wb").write(text.encode("utf-8"))
    os.replace(tmp, path)


def add_css(text: str, css: str, nl: str, marker: str) -> str:
    """把 CSS 块插到最后一个 </style> 之前（若该规则尚不存在）。"""
    if marker in text:
        return text
    ms = list(RE_STYLE_END.finditer(text))
    if not ms:
        raise ValueError("未找到 </style>")
    m = ms[-1]
    block = css.replace("\n", nl) if nl != "\n" else css
    return text[:m.start()] + block + text[m.start():]


def scene_anchor(text: str) -> int:
    """场景图插入点：正文首个章节标题（h2/h3）之前；无 ⇒ 轨标块后 <hr /> 之后；再无 ⇒ </blockquote> 之后。"""
    m = RE_CHAPTER.search(text)
    if m:
        return m.start()
    m = RE_HR.search(text)
    if m:
        return m.end()
    m = RE_BLOCKQUOTE_END.search(text)
    if m:
        return m.end()
    raise ValueError("找不到场景图插入点")


def rel_url(target: str, name: str) -> str:
    depth = target.count("/") - 1          # site/reader/people/x.html → 3 级
    return "../" * depth + "static/images/" + name


def main() -> int:
    dry = "--dry-run" in sys.argv
    with open(PRE, encoding="utf-8") as fh:
        pre = json.load(fh)
    BANNER_TARGETS = {b["target"] for b in BANNERS}
    og_map = {o["page"]: o for o in pre["og_plan"]}

    stats = {"banner": [0, 0], "scene": [0, 0], "og": [0, 0]}
    errors = []

    # ---------- ①② 27 页接入 ----------
    for item in ALL:
        target = item["target"]
        slot = "banner" if target in BANNER_TARGETS else "scene"
        path = os.path.join(ROOT, target.replace("/", os.sep))
        if not os.path.exists(path):
            errors.append("页面缺失: " + target)
            continue
        text, nl = read_text(path)
        orig = text

        if slot == "banner":
            if 'class="chapter-banner"' in text:
                print("SKIP  已有横幅: " + target)
                stats["banner"][1] += 1
                continue
            else:
                text = add_css(text, CSS_BANNER, nl, ".chapter-banner")
                m = RE_H1_END.search(text)
                if not m:
                    errors.append("未找到 </h1>: " + target)
                    continue
                img = "banner-" + item["card"] + ".webp"
                alt = item["subject"] + "（水墨意境横幅）"
                fig = ('<figure class="chapter-banner">' + nl +
                       '<img src="' + rel_url(target, img) + '" alt="' + alt +
                       '" loading="lazy" decoding="async">' + nl +
                       '</figure>' + nl + nl)
                text = text[:m.end()] + nl + fig + text[m.end():]
        else:
            if 'class="chapter-scene"' in text:
                print("SKIP  已有场景图: " + target)
                stats["scene"][1] += 1
                continue
            else:
                text = add_css(text, CSS_SCENE, nl, ".chapter-scene")
                pos = scene_anchor(text)
                img = item["card"] + ".webp"
                alt = item["subject"] + "（水墨意境插图）"
                fig = ('<figure class="chapter-scene">' + nl +
                       '<img src="' + rel_url(target, img) + '" alt="' + alt +
                       '" loading="lazy" decoding="async">' + nl +
                       '</figure>' + nl + nl)
                text = text[:pos] + fig + text[pos:]

        if text != orig:
            if dry:
                print("DRY   %-8s %s" % (slot, target))
            else:
                write_text(path, text, nl)
                print("OK    %-8s %s" % (slot, target))
            stats[slot][0] += 1
        else:
            stats[slot][1] += 1

    # ---------- ③ 102 页 og:image ----------
    for target, o in sorted(og_map.items()):
        path = os.path.join(ROOT, target.replace("/", os.sep))
        if not os.path.exists(path):
            errors.append("og 目标页缺失: " + target)
            continue
        text, nl = read_text(path)
        orig = text
        new_url = OG_BASE + o["out"]
        m = RE_OG_IMAGE.search(text)
        if not m:
            errors.append("og:image 缺失: " + target)
            continue
        if m.group(2) == new_url:
            stats["og"][1] += 1
            continue
        text = text[:m.start(2)] + new_url + text[m.end(2):]
        if text != orig:
            if dry:
                print("DRY   og      %s -> %s" % (target, o["out"]))
            else:
                write_text(path, text, nl)
                print("OK    og      %s -> %s" % (target, o["out"]))
            stats["og"][0] += 1
        else:
            stats["og"][1] += 1

    print("\n合计：横幅 接入 %d · 跳过 %d ｜ 场景 接入 %d · 跳过 %d ｜ og 改 %d · 跳过 %d"
          % (stats["banner"][0], stats["banner"][1], stats["scene"][0], stats["scene"][1],
             stats["og"][0], stats["og"][1]))
    if errors:
        print("\n!! 错误 %d 条：" % len(errors))
        for e in errors:
            print("   ", e)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
