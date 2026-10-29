# -*- coding: utf-8 -*-
"""_w1016_stage.py — W1016 落位：12 个回目页接入题图 + 换专属 og:image

口径来源（实读现役页 ch003.html 确认·非记忆）：
  og:image base = https://1273984347.github.io/xiyouji/static/images/og-<stem>.webp
  题图 src      = ../static/images/<站点版名>.webp（reader 页深度 1）
  插图位置      = </h1> 之后（题图位）
  alt 形态      = 「<主体>线描立像：<细节>」/ 场面写「<主体>与<对方>对峙的线描场面：…」
  样式块        = 本页无 .chapter-plate 时插在最后一个 </style> 前（暗色模式隐藏）

og 派生：`subject_band.crop_band(im, 1200, 630, "og")`（主体跨高 ≤630 ⇒ 居中带；
          >630 ⇒ 头部带 [主体顶−30, +630]）⇒ 只裁不缩放·不拉伸变形。

幂等：已有 chapter-plate 的页面跳过插图；og 文件已存在且尺寸正确则跳过派生。
写回：临时文件 + os.replace（原子）·newline='' 保留原行尾。
只碰本批 12 个页面 ⇒ 其余 68 个无配图回目页的 og:image 零改动。

用法：py -3 scripts/_w1016_stage.py [--dry-run]
"""
from __future__ import annotations

import io
import os
import re
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from subject_band import crop_band  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SET_DIR = os.path.join(REPO, "assets", "promo", "plate-set")
IMG = os.path.join(REPO, "site", "static", "images")
OG_BASE = "https://1273984347.github.io/xiyouji/static/images/"
OG_W, OG_H = 1200, 630
MAX_OG_BYTES = 300 * 1024

CSS = """    /* W1016：回目题图（线描族·沿用章回页 chapter-plate 范式·浅底宣纸图暗色模式隐藏） */
    .chapter-plate { margin: 28px auto 36px; max-width: 420px; }
    .chapter-plate img { width: 100%; height: auto; display: block; opacity: .92; }
    html[data-theme="dark"] .chapter-plate { display: none; }
"""

# (回目页, 站点版文件名, alt)
JOBS = [
    ("ch020", "plate-line-73-ch020-huxianfeng.webp",
     "虎先锋线描立像：虎首人身、宽袖战袍，双手横持一柄九齿钯"),
    ("ch024", "plate-line-74-ch024-qingfeng.webp",
     "清风童子的线描立像：双髻道童衣，双手捧一只木托盘，盘中两枚人参果"),
    ("ch034", "plate-line-75-ch034-bashanhu.webp",
     "巴山虎与倚海龙的线描场面：虎首与龙首两名小妖并肩，各执朴刀与长枪"),
    ("ch043", "plate-line-76-ch043-tuolong.webp",
     "鼍龙与摩昂的线描场面：龙母托三棱简、龙子按钢叉，对面猴形行者相对"),
    ("ch044", "plate-line-77-ch044-yangli.webp",
     "羊力大仙与猴形行者的线描场面：道冠妖道持拂尘，与执棒行者隔案相持"),
    ("ch049", "plate-line-78-ch049-laoyuan.webp",
     "老鼋的线描立像：龟首人身、白须垂胸，背负玄色甲壳伏于水中"),
    ("ch051", "plate-line-79-ch051-qingniu.webp",
     "青牛精与猴形行者的线描场面：额生独角的妖王左手套金圈，与执棒行者对峙"),
    ("ch064", "plate-line-80-ch064-xingxian.webp",
     "杏仙的线描立像：鬓发如云、宽袖长裙，右手执一柄素面折扇"),
    ("ch074", "plate-line-81-ch074-qingshi.webp",
     "青狮与白象的线描场面：狮首与象首两名魔头并肩，各执长柄兵器怒视猴形行者"),
    ("ch091", "plate-line-82-ch091-bidun.webp",
     "辟尘大王与猴形行者的线描场面：双角冠妖王双手握藤缠长柄兵器，与执棒行者对峙"),
    ("ch096", "plate-line-83-ch096-kouyuanwai.webp",
     "寇员外的线描立像：头戴方巾、宽袖锦袍，双手拱于身前相迎"),
    ("ch008", "plate-line-84-ch008-jinding.webp",
     "金顶大仙的线描立像：莲花冠、白须及胸，双手捧一柄拂尘端立"),
]

RE_OG = re.compile(r'(<meta property="og:image" content=")([^"]+)(")')


def read(p):
    raw = io.open(p, "rb").read()
    return raw.decode("utf-8"), ("\r\n" if b"\r\n" in raw else "\n")


def write(p, text):
    tmp = p + ".tmp"
    io.open(tmp, "wb").write(text.encode("utf-8"))
    os.replace(tmp, p)


def main() -> int:
    dry = "--dry-run" in sys.argv
    ok = 0

    # ---------- ① og 版派生（12 个） ----------
    for ch, site_name, _alt in JOBS:
        stem = site_name[:-5]                      # 去 .webp
        src = os.path.join(SET_DIR, stem + ".png")
        out = os.path.join(IMG, "og-%s.webp" % stem)
        assert os.path.exists(src), "母版缺失：%s" % src
        assert os.path.exists(os.path.join(IMG, site_name)), "站点版缺失：%s" % site_name
        if os.path.exists(out):
            with Image.open(out) as im:
                if im.size == (OG_W, OG_H) and os.path.getsize(out) <= MAX_OG_BYTES:
                    print("SKIP  og-%s.webp 已在位（%dx%d·%dB）"
                          % (stem, im.size[0], im.size[1], os.path.getsize(out)))
                    ok += 1
                    continue
        im = Image.open(src).convert("RGB")
        cropped, info = crop_band(im, OG_W, OG_H, "og")
        assert cropped.size == (OG_W, OG_H), "og 尺寸错：%s" % (cropped.size,)
        if dry:
            print("DRY  og-%s.webp ← %s（裁切线 %s）" % (stem, stem + ".png", info["crop_y"]))
        else:
            tmp = out + ".tmp"
            cropped.save(tmp, "WEBP", quality=90, method=6)
            os.replace(tmp, out)
            size = os.path.getsize(out)
            assert size <= MAX_OG_BYTES, "og 超 300KB：%s" % size
            print("OK   og-%s.webp %dx%d %dB（裁切线 %s）"
                  % (stem, OG_W, OG_H, size, info["crop_y"]))
        ok += 1

    # ---------- ② 页面接入（题图 + og:image） ----------
    for ch, site_name, alt in JOBS:
        rel = "site/reader/%s.html" % ch
        path = os.path.join(REPO, rel.replace("/", os.sep))
        assert os.path.exists(path), "页面缺失：%s" % rel
        text, nl = read(path)
        orig = text

        # 2.1 样式块（幂等）
        if ".chapter-plate" not in text:
            m = re.search(r"[ \t]*</style>", text)
            assert m, "%s 未找到 </style>" % rel
            css = CSS.replace("\n", nl) if nl != "\n" else CSS
            text = text[:m.start()] + css + text[m.start():]

        # 2.2 题图（幂等：已有 figure 则跳过）
        if 'class="chapter-plate"' not in text:
            j = text.find("</h1>")
            assert j != -1, "%s 未找到 </h1>" % rel
            depth = rel.count("/") - 1
            prefix = "../" * depth + "static/images/"
            fig = (
                '<figure class="chapter-plate">' + nl +
                '<img src="' + prefix + site_name + '" alt="' + alt + '" loading="lazy" decoding="async">' + nl +
                '</figure>' + nl
            )
            text = text[:j + len("</h1>")] + nl + fig + text[j + len("</h1>"):]

        # 2.3 og:image 换专属版（幂等）
        want = OG_BASE + "og-" + site_name[:-5] + ".webp"
        m = RE_OG.search(text)
        assert m, "%s 缺 og:image" % rel
        if m.group(2) != want:
            text = RE_OG.sub(lambda mm: mm.group(1) + want + mm.group(3), text, count=1)

        if text == orig:
            print("SKIP  %s 无改动" % rel)
        elif dry:
            print("DRY  %s 接入题图 + 换 og:image" % rel)
        else:
            write(path, text)
            print("OK   %s 接入题图 + og:image → og-%s.webp" % (rel, site_name[:-5]))
        ok += 1

    print("---- 落位 %d 步完成 ----" % ok)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
