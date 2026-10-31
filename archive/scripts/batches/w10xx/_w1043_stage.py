# -*- coding: utf-8 -*-
"""_w1043_stage.py — W1016 落位：12 个回目页接入题图 + 换专属 og:image

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

用法：py -3 scripts/_w1043_stage.py [--dry-run]
"""
from __future__ import annotations

import io
import os
import re
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))), "scripts"))
from subject_band import crop_band  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
SET_DIR = os.path.join(REPO, "assets", "promo", "plate-set")
IMG = os.path.join(REPO, "site", "static", "images")
OG_BASE = "https://1273984347.github.io/xiyouji/static/images/"
OG_W, OG_H = 1200, 630
MAX_OG_BYTES = 300 * 1024

CSS = """    /* W1043：回目题图（线描族·沿用章回页 chapter-plate 范式·浅底宣纸图暗色模式隐藏） */
    .chapter-plate { margin: 28px auto 36px; max-width: 420px; }
    .chapter-plate img { width: 100%; height: auto; display: block; opacity: .92; }
    html[data-theme="dark"] .chapter-plate { display: none; }
"""

# (回目页, 站点版文件名, alt)
JOBS = [
    ("ch053", "plate-line-85-ch053-ruyizhenxian.webp",
     "如意真仙的线描立像：七瓣莲花冠、宽袖道袍，双手捧一枚圆润果实"),
    ("ch033", "plate-line-86-ch033-chuikouxian.webp",
     "吹口仙的线描立像：斗笠宽檐、宽袖短褂，双手交叠腹前作吹哨之姿"),
    ("ch094", "plate-line-87-ch094-taiyinxingjun.webp",
     "太阴星君的线描立像：高挽发髻插一支素簪，广袖长裙、双手拢于袖中"),
    ("ch073", "plate-line-88-ch073-duomuguai.webp",
     "多目怪的线描立像：素色冠帽、宽袖长袍，额面与两颊散布数枚圆形小眼"),
    ("ch069", "plate-line-89-ch069-ziyangzhenren.webp",
     "紫阳真人的线描立像：莲花冠、宽袖道袍，双手捧一只扁圆形葫芦"),
    ("ch090", "plate-line-90-ch090-yijiukutianzun.webp",
     "乙救苦天尊的线描立像：莲瓣冠、宽袖帝君袍，双手结印于胸前"),
    ("ch071", "plate-line-91-ch071-jiuling-shiba.webp",
     "九灵元圣与十八罗汉的线描场面：独角仙人与两列罗汉同框"),
    ("ch086", "plate-line-92-ch086-bihan-bishu.webp",
     "辟寒大王与辟暑大王的线描场面：冰棱角冠与薄片角冠两名妖王相对而立"),
    ("ch095", "plate-line-93-ch095-yumian.webp",
     "玉面狐狸与猴形行者的线描场面：白面狐妖拈诀，与执棒行者相对"),
    ("ch029", "plate-line-94-ch029-bengpo-baboren.webp",
     "奔波儿灞与灞波儿奔的线描场面：水纹帽两名巡海小妖并肩而行"),
    ("ch085", "plate-line-95-ch085-diyongfuren.webp",
     "地涌夫人与猴形行者的线描场面：白鼻鼠妖作拈诀之姿，与执棒行者隔洞对峙"),
    ("ch097", "plate-line-96-ch097-xiniu.webp",
     "犀牛怪与猴形行者的线描场面：额生粗短独角的犀牛妖，与执棒行者隔山对峙"),
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
