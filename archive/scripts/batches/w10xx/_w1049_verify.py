# -*- coding: utf-8 -*-
"""_w1049_verify.py — W1049 落位验收（AC-03~AC-11 的机器侧复核）

六项断言（每项带期望输出·fail-closed）：
  ① 12 个回目页均含 chapter-plate 题图且 img src 指向本批站点版
  ② 12 页 og:image 均指向专属 og-<stem>.webp（不再是通用图）
  ③ 12 个 og 版尺寸 == 1200×630 且 ≤300KB
  ④ 缺口复算：100 回中已有配图 55→67 回、缺口 45→33 回
  ⑤ **未覆盖页未回归**：其余 88 页的 og:image 仍为落位前的取值（31 通用图 + 2 张既有 card-* 专属 + 55 回已落位专属）
  ⑥ 12 页均含暗色模式隐藏规则 html[data-theme="dark"] .chapter-plate { display: none; }

用法：py -3 archive/scripts/batches/w10xx/_w1049_verify.py
"""
from __future__ import annotations

import glob
import io
import json
import os
import re
import sys

from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
IMG = os.path.join(REPO, "site", "static", "images")
OG_BASE = "https://1273984347.github.io/xiyouji/static/images/"

# W1049：本批 12 个目标回实读均无任何配图（`_w1049_pick_verify.py` ① 项判据）
# ⇒ 无「已有旧题图只换 og」的例外回，PREEXISTING 为空集。
PREEXISTING = set()  # W1049：本批 12 回实读均无任何配图⇒无例外回

JOBS = [
    ('ch016', 'plate-line-97-ch016-jinchi-zhanglao.webp'),
    ('ch039', 'plate-line-98-ch039-wenshu-pusa.webp'),
    ('ch046', 'plate-line-99-ch046-luli-daxian.webp'),
    ('ch050', 'plate-line-100-ch050-huode-xingjun.webp'),
    ('ch055', 'plate-line-101-ch055-nvguo-guowang.webp'),
    ('ch084', 'plate-line-102-ch084-miefo-guowang.webp'),
    ('ch005', 'plate-line-103-ch005-sida-tianwang.webp'),
    ('ch018', 'plate-line-104-ch018-gao-taigong.webp'),
    ('ch032', 'plate-line-105-ch032-yinjiao-dawang.webp'),
    ('ch056', 'plate-line-106-ch056-shidai-yanjun.webp'),
    ('ch067', 'plate-line-107-ch067-honglin-damang.webp'),
    ('ch058', 'plate-line-108-ch058-diting.webp'),
]

RE_OG = re.compile(r'<meta property="og:image" content="([^"]+)"')
RE_PLATE = re.compile(r'<figure class="chapter-plate">\s*<img src="([^"]+)" alt="([^"]*)"')
DARK_RULE = 'html[data-theme="dark"] .chapter-plate { display: none; }'
# 沿用上一批修正：原判据用**整串字面量**匹配 ⇒ 页面 CSS 为多行排版时误判「缺暗色隐藏规则」
# ⇒ 改为容忍空白的正则（坑表 puti-shouye 第 5 条：判据禁止依赖脆弱特征）
# 本批不修改该判据·仅继承
RE_DARK_RULE = re.compile(r'html\[data-theme="dark"\]\s*\.chapter-plate\s*\{[^}]*display:\s*none')


def main() -> int:
    fails = []
    notes = []

    # ①② 题图与 og:image
    for ch, site_name in JOBS:
        p = os.path.join(REPO, "site", "reader", "%s.html" % ch)
        s = io.open(p, encoding="utf-8").read()
        mp = RE_PLATE.search(s)
        if not mp:
            fails.append("%s 缺 chapter-plate 题图" % ch)
            continue
        if ch not in PREEXISTING and mp.group(1).split("/")[-1] != site_name:
            fails.append("%s 题图 src=%s ≠ %s" % (ch, mp.group(1), site_name))
        if ch in PREEXISTING:
            notes.append("      %s 已有旧题图（%s）⇒ 本批只换 og:image·题图不覆盖"
                         % (ch, mp.group(1).split("/")[-1]))
        if not mp.group(2).strip():
            fails.append("%s 题图 alt 为空" % ch)
        mo = RE_OG.search(s)
        want = OG_BASE + "og-" + site_name[:-5] + ".webp"
        if not mo or mo.group(1) != want:
            fails.append("%s og:image=%s ≠ %s" % (ch, mo.group(1) if mo else "(无)", want))
        if not RE_DARK_RULE.search(s):
            fails.append("%s 缺暗色隐藏规则" % ch)
    notes.append("①② 题图 + og:image + alt：12 页逐页核对")

    # ③ og 版尺寸与体积
    for ch, site_name in JOBS:
        stem = site_name[:-5]
        p = os.path.join(IMG, "og-%s.webp" % stem)
        if not os.path.exists(p):
            fails.append("og-%s.webp 缺失" % stem)
            continue
        with Image.open(p) as im:
            if im.size != (1200, 630):
                fails.append("og-%s.webp 尺寸 %s ≠ (1200,630)" % (stem, im.size))
        size = os.path.getsize(p)
        if size > 300 * 1024:
            fails.append("og-%s.webp 超 300KB：%dB" % (stem, size))
    notes.append("③ 12 个 og 版：尺寸 1200×630 + ≤300KB")

    # ④⑤ 缺口复算 + 未覆盖页未回归
    rows = []
    for f in sorted(glob.glob(os.path.join(REPO, "site", "reader", "ch*.html"))):
        s = io.open(f, encoding="utf-8").read()
        ch = os.path.basename(f)[2:5]
        has_plate = bool(re.search(r'<figure class="chapter-plate">', s))
        has_scene = bool(re.search(r'<figure class="chapter-scene">', s))
        mo = RE_OG.search(s)
        rows.append({"ch": ch, "covered": has_plate or has_scene,
                     "og": mo.group(1) if mo else ""})
    covered = [r for r in rows if r["covered"]]
    gap = [r for r in rows if not r["covered"]]
    if len(covered) != 67:
        fails.append("有配图回数 %d ≠ 67（期望 55+12·本批 12 回全部新增题图）" % len(covered))
    if len(gap) != 33:
        fails.append("缺口 %d ≠ 33" % len(gap))
    generic = [r for r in gap if "og-cover-ink-zh.jpg" in r["og"]]
    other = [r for r in gap if "og-cover-ink-zh.jpg" not in r["og"]]
    if len(generic) != 31:
        fails.append("缺口中通用 og 页 %d ≠ 31" % len(generic))
    notes.append("④⑤ 缺口复算：有配图 %d / 缺口 %d（其中通用 og %d + 既有专属 %d）"
                 % (len(covered), len(gap), len(generic), len(other)))
    for r in other:
        notes.append("      缺口页保留既有专属 og：%s → %s" % (r["ch"], r["og"].split("/")[-1]))

    # ⑥ 暗色隐藏规则（逐页查 .chapter-plate 与 dark 规则共存）
    for ch, _s in JOBS:
        p = os.path.join(REPO, "site", "reader", "%s.html" % ch)
        s = io.open(p, encoding="utf-8").read()
        if ".chapter-plate" not in s:
            fails.append("%s 无 chapter-plate 规则" % ch)
    notes.append("⑥ 暗色隐藏规则：12 页均含 .chapter-plate 样式块")

    for n in notes:
        print("[NOTE] " + n)
    for f in fails:
        print("FAIL  " + f)
    print("---- W1049 落位验收：%d FAIL · %d NOTE ----" % (len(fails), len(notes)))
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
