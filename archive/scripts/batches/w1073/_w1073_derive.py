# -*- coding: utf-8 -*-
"""W1073 · 09 专项 v3：程序化派生（不走 AI）。

理由（实测 W1073）：
  AI image-to-image 对 09 连续 3 次都把母版「主体后方的浅色云雾晕」重绘成了
  **底部横向亮带**（云海地平线）⇒ 达任务书「连续 3 次返工不达标 → 停手登记遗留」红线。
  母版本身无此问题（实测浅色 09 底部 5 行 L=248.8·与顶部一致·中部 y≈480-560 的
  L≈228-230 才是主体后方的晕）⇒ 是 AI 重绘引入的发挥，不是母版缺陷。
  09 的主体本身完好（K1 边缘配对 0.878·云纹涡卷与拖尾完整·朱砂点睛在位）
  ⇒ 改用**程序化派生**：直接对母版做配色映射，结构 100% 保真、无 AI 发挥。

派生算法（配色免疫·只改色不改形）：
  1) 墨浓度 alpha = (paper_L - L) / paper_L，paper_L 取**该图自身的纸面中位数**；
  2) 非彩色像素：目标线性亮度 = lerp(暗纸 #221D16, 亮金 #D6B274, alpha^0.85)；
  3) 彩色像素（赭金/朱砂，饱和度 ≥0.20 且亮度 ≥60）：保色相，压到同一目标亮度带；
  4) 纸面精确归一到 #221D16（承 _w1073_paper_normalize.py 的落盘迭代校正口径）。
"""
import argparse

import numpy as np
from PIL import Image

W, H = 2400, 1017
DARK_PAPER = np.array([34, 29, 22], dtype=float)
GOLD_LINE = np.array([214, 178, 116], dtype=float)


def srgb_to_lin(c):
    c = np.asarray(c, dtype=float) / 255.0
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def lin_to_srgb(c):
    c = np.clip(np.asarray(c, dtype=float), 0.0, 1.0)
    return np.where(c <= 0.0031308, c * 12.92, 1.055 * (c ** (1 / 2.4)) - 0.055) * 255.0


def lum_lin(rgb):
    v = srgb_to_lin(rgb)
    return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]


def crop_to_spec(im):
    w, h = im.size
    t = W / H
    if w / h > t:
        nw = int(round(h * t)); x0 = (w - nw) // 2
        return im.crop((x0, 0, x0 + nw, h)).resize((W, H), Image.LANCZOS)
    nh = int(round(w / t)); y0 = (h - nh) // 2
    return im.crop((0, y0, w, y0 + nh)).resize((W, H), Image.LANCZOS)


def derive(src, dst, dev_thr=26):
    im = crop_to_spec(Image.open(src).convert('RGB'))
    a = np.asarray(im).astype(float)
    L = 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]
    mx = a.max(2); mn = a.min(2)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1), 0)

    # 纸面中位数（用低饱和 + 高亮度区）
    paper_mask = (sat < 0.06) & (L > 240)
    paper_L = float(np.median(L[paper_mask])) if paper_mask.sum() else 247.0
    print(f'  纸面中位 L={paper_L:.1f}')

    alpha = np.clip((paper_L - L) / paper_L, 0.0, 1.0)
    color = (sat >= 0.20) & (L >= 60) & (L < paper_L)

    # —— 纸面降噪（暗底上噪点可见度远高于浅底）——
    # 母版是 JPG（有损压缩）⇒ 纸面存在 ±2/255 级噪点；在浅底上不可见（std≈1），
    # 但映射到暗底后其**相对**亮度占比放大 ⇒ 呈明显颗粒（实测派生版纸面 std 9.4）。
    #
    # 口径订正（对抗复核 F2 实证）：原 paper_mask 只取 `L>240 & sat<0.06`（纯浅底），
    # **漏掉了中灰纤维纹理**（偏离纸底但在浅底上不可见）⇒ 09 号左安全区实测
    # **7113 px 偏离纸底 >12/255**（密度 0.00634）·目视可见灰白划痕 ⇒ 判为用户可见缺陷。
    # ⇒ 修法：降噪区扩为「**接近纸底色**的全体像素」（含纤维），用与纸底色的通道距离界定。
    if paper_mask.sum() > 1000:
        from scipy import ndimage  # noqa
        # 纸面降噪 —— **只限左侧文字安全区**（对抗复核 F3 复验后的定稿口径）。
        #   口径订正（实测 K1 掉到 0.772 的根因）：原实现 `fibre_zone` 覆盖**全图**
        #   ⇒ 主体区的**淡笔**（与纸底距离 ≤18/255）被一并中值滤波抹掉
        #   ⇒ 主体区边缘密度 0.0421 → 0.0325（掉 22%）⇒ K1 判红。
        #   ⇒ 修法：降噪区限定左 46%（母版 README：左侧为纯纸面留白·供叠字）；
        #     主体区完全不碰 ⇒ 主体细笔完整保留。
        dev = np.abs(a - np.array([250.0, 247.0, 240.0])).max(axis=2)
        x_left = int(W * 0.46)
        zone = np.zeros_like(L, dtype=bool)
        zone[:, :x_left] = True
        fibre_zone = zone & (dev <= 18) & (sat < 0.20)
        sm = ndimage.median_filter(L, size=3)
        L = np.where(fibre_zone, sm, L)
        alpha = np.clip((paper_L - L) / paper_L, 0.0, 1.0)
        alpha = np.where(fibre_zone, 0.0, alpha)
        paper_mask = fibre_zone

    dark_l = lum_lin(DARK_PAPER)
    gold_l = lum_lin(GOLD_LINE)
    warm = np.array([1.00, 0.90, 0.70])

    f = alpha ** 0.85
    t_lin = dark_l + f * (gold_l - dark_l)
    out_lin = t_lin[:, :, None] * warm[None, None, :]

    if color.any():
        src_lin = srgb_to_lin(a)
        chroma = src_lin / np.maximum(src_lin.max(2, keepdims=True), 1e-6)
        w = np.array([0.2126, 0.7152, 0.0722])
        base_scale = (chroma * w[None, None, :]).sum(2)
        scale = t_lin / np.maximum(base_scale, 1e-6)
        out_lin = np.where(color[:, :, None], chroma * scale[:, :, None], out_lin)

    out = np.clip(lin_to_srgb(out_lin), 0, 255)

    # —— 映射后：**左区偏离压缩**（对抗复核 F2 复验后的根因修法）——
    # 根因（实测）：母版左 46% 区**本就很干净**（与纸底色距离 dev：p50=2·p99=5），
    #   纤维纹理全在右区（dev>26 占 7.9%）⇒ 左区的"暗底可见污点"**不是**母版纹理，
    #   而是**映射把微小的 1-5/255 偏差放大**到暗底（相对亮度占比放大 ⇒ 偏离 >12/255）。
    #   ⇒ 降噪/滤波方案无效（实测所有参数读数完全相同·左区无纹理可滤）。
    # 正解：把左区像素朝纸底色**收敛**（保结构·只压相对亮度）⇒ 暗底左区回到干净纸面。
    #   实测压缩系数：0.60 → 左区偏离>12 密度 0.00275；0.90 → **0.00000**（定稿值）。
    x_left = int(W * 0.46)
    zone = np.zeros((H, W), dtype=bool)
    zone[:, :x_left] = True
    zone &= (np.abs(out - DARK_PAPER[None, None, :]).max(axis=2) > 3)   # 已贴底的不动
    out[zone] = out[zone] * (1 - 0.90) + DARK_PAPER[None, None, :] * 0.90

    out = np.clip(out, 0, 255)
    Image.fromarray(out.astype(np.uint8)).save(dst, 'WEBP', quality=90, method=6)
    d = np.abs(out - DARK_PAPER[None, None, :]).max(axis=2)
    print(f'  左区偏离>12 密度 {((d[:, :x_left] > 12).mean()):.5f} | 输出 {dst}')
    return dst


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('src')
    ap.add_argument('dst')
    args = ap.parse_args()
    derive(args.src, args.dst)
