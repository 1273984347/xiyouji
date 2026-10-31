# -*- coding: utf-8 -*-
"""_w999_insert.py — W999 接入：12 个回目页题图 + 专属 1200×630 og:image

三件事（均幂等）：
  ① 派生 12 个 og 版（母版 1200×1600 → 1200×630·主体居中带或头部带）→ site/static/images/og-<母版名>.webp
  ② 12 个回目页在 `<h1>` 之后插入 `<figure class="chapter-plate">`（题图位·真实 alt）
  ③ 12 页 og:image 换成该页专属 og 版

口径：
  · og 裁切：主体跨高 ≤ 630 ⇒ **居中带**（主体完整）；> 630 ⇒ **头部带** [主体顶−30, +630]（保头与胸腹）
  · 主体检测：连通簇（面积 ≥ 200 px²）+ 排除朱砂（r−g ≥ 35）与赭金（luma ≥ 90）——复用 `_w988_subject.py`
  · 页面：仅本批 12 个 chXXX.html；**不触碰其余 88 个无配图回目页**（其 og:image 仍为通用图）

用法：py -3 scripts/_w999_insert.py [--dry-run]
"""
from __future__ import annotations

import io
import os
import re
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _w988_subject import crop_band  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SET_DIR = os.path.join(ROOT, "assets", "promo", "plate-set")
SITE_IMG = os.path.join(ROOT, "site", "static", "images")
OG_W, OG_H = 1200, 630
OG_BASE = "https://1273984347.github.io/xiyouji/static/images/"

# 母版 stem → (回目, alt)
JOBS = [
    ("plate-line-49-ch001-xianshi", "ch001",
     "花果山顶仙石裂开：立地的仙石身裂一道竖缝，缝中透出微光，猴形小童自裂石中探出半身仰头，身旁散落细碎石屑"),
    ("plate-line-50-ch003-aoguang", "ch003",
     "东海龙王敖广线描立像：头戴冕旒十二串珠，身着云龙纹长袍，白须垂胸，双手拱于身前"),
    ("plate-line-51-ch009-yuanshoucheng", "ch009",
     "渔翁袁守诚线描立像：头戴斗笠披蓑衣，坐于江边青石之上，膝上摊开竹简卦签，手执一枝笔"),
    ("plate-line-52-ch011-xiaoyu", "ch011",
     "萧瑀线描立像：头戴乌纱帽，身着绯色圆领官袍，双手捧笏板于胸前，身姿微躬"),
    ("plate-line-53-ch022-liushahe", "ch022",
     "流沙河水面对峙：左侧猪首人身的八戒双手横持九齿钉耙，右侧卷发深肤的沙僧单手斜举月牙刃降妖宝杖，水花飞溅"),
    ("plate-line-54-ch028-qunyao", "ch028",
     "花果山群妖聚义：五六名猴形妖将环立成半圈，各持刀枪棍棒，中央一面大旗竖起"),
    ("plate-line-55-ch047-tongtianhe", "ch047",
     "通天河畔夜色：猴形悟空执如意金箍棒、猪首八戒双手持九齿钉耙，两人并肩挡在河岸之前，身前护着一名男童与一名女童"),
    ("plate-line-56-ch063-jiutou", "ch063",
     "碧波潭水殿前：猪首八戒执九齿钉耙与卷发深肤的沙僧持月牙铲合力扑向颈环九头的妖将，妖将怀中抱一枚明珠"),
    ("plate-line-57-ch066-mile", "ch066",
     "弥勒佛线描立像：大耳圆腹、袒胸露腹，左手持布袋，右手握念珠，笑口常开"),
    ("plate-line-58-ch079-nanpo", "ch079",
     "南极仙翁线描立像：头戴莲花冠，白须垂胸，右手持芭蕉扇，左手托寿桃，身旁立一头白鹿"),
    ("plate-line-59-ch089-huangshi", "ch089",
     "豹头山妖洞宴席：狮首人身的黄狮精立于石案之侧，案上横陈一把九齿钉耙与两只粗陶酒碗"),
    ("plate-line-60-ch093-geigu", "ch093",
     "给孤独长者线描立像：头戴毗卢帽，双手合十，身前放一柄铁锸与一叠功德簿"),
]

RE_H1 = re.compile(r"</h1>")
RE_OG = re.compile(r'(<meta property="og:image" content=")([^"]+)(")')
RE_STYLE_END = re.compile(r"[ \t]*</style>")

CSS_PLATE = """    /* W999：回次题图（线描族·沿用既有 chapter-plate 规范·浅底宣纸图暗色模式隐藏） */
    .chapter-plate { margin: 28px auto 36px; max-width: 420px; }
    .chapter-plate img { width: 100%; height: auto; display: block; opacity: .92; }
    html[data-theme="dark"] .chapter-plate { display: none; }
"""


def read(p):
    raw = io.open(p, "rb").read()
    return raw.decode("utf-8"), ("\r\n" if b"\r\n" in raw else "\n")


def write(p, text, nl):
    tmp = p + ".tmp"
    io.open(tmp, "wb").write(text.encode("utf-8"))
    os.replace(tmp, p)


def make_og(stem: str) -> str:
    """母版 → 1200×630 og 版（幂等：已存在且尺寸对则跳过）。"""
    out_name = "og-%s.webp" % stem
    out_path = os.path.join(SITE_IMG, out_name)
    src = os.path.join(SET_DIR, stem + ".png")
    if os.path.exists(out_path) and Image.open(out_path).size == (OG_W, OG_H):
        return out_name + " (已存在)"
    im = Image.open(src).convert("RGB")
    cropped, info = crop_band(im, OG_W, OG_H, "og")
    tmp = out_path + ".tmp"
    cropped.save(tmp, "WEBP", quality=90, method=6)
    os.replace(tmp, out_path)
    return "%s (主体 %d..%d 裁 %s)" % (out_name, info["subject_top"], info["subject_bottom"], info["crop_y"])


def main() -> int:
    dry = "--dry-run" in sys.argv
    ok = skip = fail = 0
    for stem, ch, alt in JOBS:
        src_site = os.path.join(SITE_IMG, stem + ".webp")
        if not os.path.exists(src_site):
            print("FAIL  站点版缺失: " + stem)
            fail += 1
            continue
        og_note = make_og(stem)
        page_rel = "site/reader/%s.html" % ch
        path = os.path.join(ROOT, page_rel.replace("/", os.sep))
        text, nl = read(path)
        orig = text
        if 'class="chapter-plate"' not in text:
            # ① 题图位插在 </h1> 之后
            m = RE_H1.search(text)
            if not m:
                print("FAIL  未找到 </h1>: " + ch)
                fail += 1
                continue
            fig = ('<figure class="chapter-plate">' + nl +
                   '<img src="../../static/images/%s.webp" alt="%s" loading="lazy" decoding="async">' % (stem, alt) + nl +
                   '</figure>' + nl + nl)
            text = text[:m.end()] + nl + fig + text[m.end():]
            # ② 样式块（若本页无 .chapter-plate 规则）
            if ".chapter-plate {" not in text:
                ms = list(RE_STYLE_END.finditer(text))
                if not ms:
                    print("FAIL  未找到 </style>: " + ch)
                    fail += 1
                    continue
                m2 = ms[-1]
                block = CSS_PLATE.replace("\n", nl) if nl != "\n" else CSS_PLATE
                text = text[:m2.start()] + block + text[m2.start():]
        # ③ og:image 换专属图
        new_url = OG_BASE + "og-%s.webp" % stem
        mo = RE_OG.search(text)
        if not mo:
            print("FAIL  og:image 缺失: " + ch)
            fail += 1
            continue
        if mo.group(2) != new_url:
            text = text[:mo.start(2)] + new_url + text[mo.end(2):]
        if text != orig:
            if dry:
                print("DRY   %-9s 题图+og  |  %s" % (ch, og_note))
            else:
                write(path, text, nl)
                print("OK    %-9s 题图+og  |  %s" % (ch, og_note))
            ok += 1
        else:
            print("SKIP  %-9s 已接入" % ch)
            skip += 1
    print("\n合计：接入 %d · 跳过 %d · 失败 %d" % (ok, skip, fail))
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
