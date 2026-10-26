# -*- coding: utf-8 -*-
"""_w974_zoom.py — W974 12 张题图的人眼放大复核图（题材辨识度 + 形制正确性）

产出两组图：
  ① `zoom-w974/full-NN.png`  —— 主体区全图（裁掉顶部留白·缩放至宽 560）：看**题材辨识度**
     （能不能靠西游元素认出这一张）
  ② `zoom-w974/detail-NN.png` —— **局部放大**（自动定位墨迹最密集的 420×420 窗口·
     ×2 放大到 840×840）：看**形制正确性**（塔有几层、剑有几个星点、葫芦颈细不细…）

局部窗口自动定位：numpy 积分图（summed-area table）⇒ 滑窗求墨量 O(1)，
取墨量最高的窗口 ⇒ 墨迹最密集处通常正是标志物/主体核心，无需人工指定坐标。

用法：py -3 scripts/_w974_zoom.py
"""
import os

import numpy as np
from PIL import Image, ImageDraw, ImageChops

REPO = r"D:\xiyouji"
SET_DIR = os.path.join(REPO, "assets", "promo", "plate-set")
OUT = os.path.join(SET_DIR, "zoom-w974")
PAPER = (250, 247, 240)
TOL = 26
WIN = 420                     # 局部窗口边长
ZOOM = 2                     # 放大倍数

# 本批 12 张（顺序 = 批次顺序·人物 6 + 主题 6）
STEMS = [
    "plate-line-13-jinjiaodawang",
    "plate-line-14-yinjiaodawang",
    "plate-line-15-huangmeidawang",
    "plate-line-16-heixiongjing",
    "plate-line-17-tuota-lijing",
    "plate-line-18-yutujing",
    "plate-line-19-nvziguo-topic",
    "plate-line-20-chelingguo-topic",
    "plate-line-21-shituoling-topic",
    "plate-line-22-tonghehe-topic",
    "plate-line-23-pansidong-topic",
    "plate-line-24-wudidong-topic",
]


def ink_mask(im):
    d = ImageChops.difference(im.convert("RGB"), Image.new("RGB", im.size, PAPER))
    r, g, b = d.split()
    m = ImageChops.lighter(ImageChops.lighter(r, g), b)
    return np.array(m.point(lambda v: 255 if v > TOL else 0), dtype=np.int32)


def subject_top(mask, w, h):
    """主体顶 = 墨迹 bbox 顶（本图顶部噪点已确认不会命中本批 12 张·见 probe_subjtop）"""
    ys = np.nonzero(mask.any(axis=1))[0]
    return int(ys[0]) if len(ys) else 0


def densest_window(mask, win):
    """积分图滑窗：取墨量最高的 win×win 窗口，返回 (x0, y0)"""
    h, w = mask.shape
    sat = mask.cumsum(axis=0).cumsum(axis=1)
    sat = np.pad(sat, ((1, 0), (1, 0)), mode="constant")
    best = (-1, 0, 0)
    for y0 in range(0, max(1, h - win + 1), 20):
        y1 = y0 + win
        row = sat[y1, win:] - sat[y0, win:] - sat[y1, :-win] + sat[y0, :-win]
        i = int(np.argmax(row))
        v = int(row[i])
        if v > best[0]:
            best = (v, i, y0)
    return best[1], best[2]


def main():
    if not os.path.isdir(OUT):
        os.makedirs(OUT)

    for n, stem in enumerate(STEMS, 1):
        p = os.path.join(SET_DIR, stem + ".png")
        im = Image.open(p).convert("RGB")
        w, h = im.size
        mask = ink_mask(im)
        top = subject_top(mask, w, h)

        # ① 主体区全图（宽 560）
        body = im.crop((0, max(0, top - 10), w, h))
        scale = 560.0 / body.width
        full = body.resize((560, max(1, int(body.height * scale))), Image.LANCZOS)
        full.save(os.path.join(OUT, "full-%02d.png" % n), "PNG", optimize=True)

        # ② 局部放大（墨迹最密集的 WIN×WIN 窗口·×2）
        x0, y0 = densest_window(mask, WIN)
        x0 = max(0, min(w - WIN, x0))
        y0 = max(0, min(h - WIN, y0))
        det = im.crop((x0, y0, x0 + WIN, y0 + WIN)).resize(
            (WIN * ZOOM, WIN * ZOOM), Image.LANCZOS)
        det.save(os.path.join(OUT, "detail-%02d.png" % n), "PNG", optimize=True)
        print("%02d %-32s 主体顶=%-4d 细节窗=(%d,%d)" % (n, stem, top, x0, y0))

    # ---- 拼图：每张 4 格（full + detail 交替）----
    for gi in range(3):
        items = STEMS[gi * 4:(gi + 1) * 4]
        pad, lab = 12, 22
        cw, ch = 840, 840
        sheet = Image.new("RGB", (2 * cw + 3 * pad, 2 * (ch + lab) + 3 * pad), PAPER)
        dr = ImageDraw.Draw(sheet)
        for i, stem in enumerate(items):
            n = gi * 4 + i + 1
            r, c = divmod(i, 2)
            x = pad + c * (cw + pad)
            y = pad + r * (ch + lab + pad)
            sheet.paste(Image.open(os.path.join(OUT, "detail-%02d.png" % n)).convert("RGB"), (x, y))
            dr.rectangle([x, y, x + cw - 1, y + ch - 1], outline=(190, 182, 166))
            dr.text((x + 4, y + ch + 5), "%02d %s" % (n, stem.replace("plate-line-", "")),
                    fill=(50, 45, 38))
        out = os.path.join(OUT, "detail-sheet-g%d.png" % (gi + 1))
        sheet.save(out, "PNG", optimize=True)
        print("拼图：%s（%dx%d）" % (out, sheet.size[0], sheet.size[1]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
