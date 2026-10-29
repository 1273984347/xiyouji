# -*- coding: utf-8 -*-
"""_w1013_stage.py — W1013 落位：12 个回目页接入题图 + 换专属 og:image

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

用法：py -3 scripts/_w1013_stage.py [--dry-run]
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

CSS = """    /* W1013：回目题图（线描族·沿用章回页 chapter-plate 范式·浅底宣纸图暗色模式隐藏） */
    .chapter-plate { margin: 28px auto 36px; max-width: 420px; }
    .chapter-plate img { width: 100%; height: auto; display: block; opacity: .92; }
    html[data-theme="dark"] .chapter-plate { display: none; }
"""

# (回目页, 站点版文件名, alt)
JOBS = [
    ("ch002", "plate-line-61-ch002-puti.webp",
     "菩提祖师线描立像：白须垂胸、头戴混元帽、宽袖道袍，右手竖起三指作敲头之姿，左手抚一卷竹简"),
    ("ch012", "plate-line-62-ch012-jinchanzi.webp",
     "金蝉童子线描立像：头顶双髻、身着素色僧衣、双手合十于胸前"),
    ("ch013", "plate-line-63-ch013-taibaixingxing.webp",
     "太白金星线描立像：头戴道巾、白须长及胸腹，右手竖执一柄玉笏，左手抚须"),
    ("ch021", "plate-line-64-ch021-lingji.webp",
     "灵吉菩萨线描立像：头戴宝冠、宽袖袈裟，左手托一柄飞龙宝杖（杖头八爪金龙），右手结印"),
    ("ch038", "plate-line-65-ch038-wujiguowang.webp",
     "乌鸡国王线描立像：头戴冕旒、宽袖龙袍，双手拱于身前"),
    ("ch045", "plate-line-66-ch045-huli.webp",
     "虎力大仙与猴形行者对峙的线描场面：虎首人身的妖王右手持一柄直杆钢鞭，猴王斜举金箍棒相对而立"),
    ("ch078", "plate-line-67-ch078-zhizhujing.webp",
     "盘丝洞的线描场面：八条节肢的蜘蛛精张臂而立，与一名袈裟僧人隔空相对"),
    ("ch082", "plate-line-68-ch082-bailujing.webp",
     "白鹿精线描立像：头顶生一对鹿角、身着宽袖僧衣、双手合十"),
    ("ch083", "plate-line-69-ch083-laoshujing.webp",
     "老鼠精地涌夫人线描立像：尖耳门牙、头戴镶宝僧帽，右手托一只紫金钵"),
    ("ch086", "plate-line-70-ch086-bichandawang.webp",
     "辟寒大王与辟暑大王的线描场面：双角冠帽的两名妖王执刀枪并肩怒视猴形行者"),
    ("ch087", "plate-line-71-ch087-yuhuawang.webp",
     "玉华州三王子的线描场面：三名戴金冠的王子执长枪陌刀双剑，朝向猴形行者"),
    ("ch092", "plate-line-72-ch092-dizang.webp",
     "地藏王与冥府判官的线描场面：地藏王托锡杖握明珠，獬豸冠判官并立"),
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
