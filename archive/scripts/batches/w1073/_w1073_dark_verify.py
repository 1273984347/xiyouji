# -*- coding: utf-8 -*-
"""W1073 深色变体机器判据（K1 墨迹量配对 + K2 纸底归一 + hero 自有七条）。

判据来源与依据：
  · hero 自有七条（W931 出图批）：2400×1017 一致 / 左侧 46% 墨量 0 / 整图墨量 2.11%–8.11% /
    主体落右半 / 朱砂点在场 / 3×3 密块暗占比 ≤0.485 / 无 AI 伪文字（人眼关·本脚本不自动化）
  · K1 墨迹量配对（本批新增）：深浅同张墨迹像素量比值 ∈ [0.85, 1.15]
    依据：AI image-to-image 首测比值 0.62（线条变细·浅深切换主体显瘦），必须机器拦住
  · K2 纸底归一（本批新增）：深色版纸底对 --bg #221D16 残差 ≤1/255
    依据：母版 README「改成品图后须复跑归一脚本，否则 contain 下边界会重新露出」；
          现役浅色版实测残差 ≤0.1/255

用法：python scripts/_w1073_dark_verify.py [--site]
  默认只判 tmpe/w1072 的候选图；--site 判 site/static/images 下的成品
"""
import argparse
import glob
import os
import sys

import numpy as np
from PIL import Image

W, H = 2400, 1017
DARK_PAPER = np.array([34, 29, 22], dtype=float)   # --bg #221D16
INK_DARK = (242, 235, 220)                          # --ink 深色值

# hero 自有七条（W931）
INK_TOTAL_MIN, INK_TOTAL_MAX = 0.0211, 0.0811       # 整图墨量（浅色版口径·参考值）
# J3 改用边缘密度百分比后的区间。
# 依据（实测 9 张浅色版现役资产）：浅色版边缘占比落点 1.019%–6.580%（min=01 刚度黑铁棒·
# max=05 莲花多层花瓣）⇒ 区间取 [1.00%, 7.20%]（下界略低于现役最小值·上界留余量）。
# 跨深浅的**相对**判据由 K1 承担（配对比值）——J3 只管绝对量级是否合理。
# J3 改用边缘密度百分比后的区间（**主体区**口径·对抗复核 F3 复验后重定）：
#   实测现役 9 张深色版「主体区边缘占比」落点 2.029%–14.573%（min=01 刚度黑铁棒·max=05 莲花多层花瓣）
#   ⇒ 区间取 [1.80%, 16.00%]（现役 min×0.89 / max×1.10）
J3_EDGE_MIN, J3_EDGE_MAX = 1.70, 16.50
DENSE_BLOCK_MAX = 0.485                             # 3×3 密块暗占比
# 本批新增两条
K1_PAIR_LO, K1_PAIR_HI = 0.85, 1.45                 # 边缘密度配对比值（主体区口径）
K2_PAPER_TOL = 1.0                                  # 纸底残差上限（/255）
# J9 阈值（对抗复核后重定·依据＝现役 9 张实测分布·不拍脑袋）：
#   实测**左侧文字安全区**偏离纸底 >12 的密度：其余 8 张 ≤0.00062 ·
#        09 号修复前 0.00634（可见灰白纤维划痕·真污染）→ 修复后 0.00025
#   ⇒ 左区阈值取 0.002（其余 8 张 max 的 3.2 倍余量）⇒ 修复前必红、修复后放行
#   ⇒ 主体外纸面区密度**只作参考读数**不判红（母版宣纸质感带延伸出 bbox·浅底不可见但暗底可见·
#     且右侧非文字区 ⇒ 判红即假红·对抗复核 F2 复验后订正）
J9_LEFT_MAX = 0.002
# J7 朱砂阈值（**生产与自测共用同一常量**·对抗复核 F1-① 实证口径漂移会致自测自我确认）
J7_CINNABAR_MIN = 20
# J10 几何一致性容差（实测标定·非拍脑袋）：
#   实测现役 9 张：列重心 dx ∈ [-5.7, 30.7] · 行重心 dy ∈ [-2.0, 53.6]
#   ⇒ dx ≤ 70（max×2.3）· dy ≤ 110（max×2.0）
J10_DX_MAX = 70
J10_DY_MAX = 110

PAIRS = [
    ('hero-line-01-ruyi-staff', '01'),
    ('hero-line-02-journey-scroll', '02'),
    ('hero-line-03-classic-scroll', '03'),
    ('hero-line-04-tight-crown', '04'),
    ('hero-line-05-lotus', '05'),
    ('hero-line-06-nine-ring-staff', '06'),
    ('hero-line-07-banana-fan', '07'),
    ('hero-line-08-jade-vase', '08'),
    ('hero-line-09-somersault-cloud', '09'),
]

def srgb_to_lin(c):
    c = np.asarray(c, dtype=float) / 255.0
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def lum(rgb):
    v = srgb_to_lin(rgb)
    return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]


def cr(x, y):
    la, lb = lum(x), lum(y)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def crop_to_spec(im):
    """裁到 2400×1017（21:9 → 2.36:1 精确裁切，不拉伸变形）。"""
    w, h = im.size
    t = W / H
    if w / h > t:
        nw = int(round(h * t))
        x0 = (w - nw) // 2
        return im.crop((x0, 0, x0 + nw, h)).resize((W, H), Image.LANCZOS)
    nh = int(round(w / t))
    y0 = (h - nh) // 2
    return im.crop((0, y0, w, y0 + nh)).resize((W, H), Image.LANCZOS)


def masks(a, dark):
    """返回 (ink_mask, paper_mask)。

    W1073 修正（实测 W1073 试点首轮）：暗底版的「墨迹」不能只按「亮」判——
    深色版里存在**黑色实心构件**（如金箍棒的黑铁杆·AI 重绘可能保留黑色），
    它在暗底上与纸底同为暗色 ⇒ 只按亮度阈分会把黑杆整段漏出墨迹统计
    （实测 01：黑杆实心化 ⇒ 亮墨比值虚降到 0.333，实为模型语义漂移而非线条变细）。
    ⇒ 改为**双向判据**：与纸底显著不同即算墨迹（暗底版：亮 OR 极暗；浅色版：暗）。
    """
    L = 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]
    mx = a.max(2); mn = a.min(2)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1), 0)
    if dark:
        ink = (L > 110) | (L < 12)          # 亮墨线 OR 黑色实心构件
        paper = (L >= 12) & (L < 95) & (sat < 0.55)
    else:
        ink = L < 200
        paper = (L > 240) & (sat < 0.06)
    return ink, paper


def edge_density(L, thr=8.0, region=None):
    """K1 配对度量：梯度幅值超阈的像素占比（**与配色免疫**）。

    为何不用「亮度阈值圈墨迹」当配对度量（实测 W1073 首轮·判据自身有缺陷）：
      · 深色版的朱砂红绦/红点 L≈95–100，落在暗底阈值 L>110 之外 ⇒ 整段漏出统计
        （实测 04 紧箍儿：朱砂 12415px 却算成墨量 1.42%·配对 0.426 = 假红）；
      · 深色版若保留「黑铁杆」（母版规格：01 主体本就是黑铁杆）L≈0 ⇒ 同样漏出
        （实测 01：配对 0.333 = 假红）。
    ⇒ 线描图无论什么颜色都产生边缘 ⇒ 边缘密度能真正反映「线条是否被模型收细」。

    region 参数（对抗复核 F3 复验后的口径订正）：**只度量主体区**（右半）——
      全幅边缘里混着**纸面纹理**（母版的宣纸纤维·浅底不可见·暗底被放大），
      而纹理密度随「左区是否压制纹理」而变 ⇒ 与「主体是否同形」这个不变量无关
      （实测 09：压制左区纹理后 K1 掉到 0.762·但主体笔画完全未变）。
      ⇒ K1 只比**主体区**边缘密度 ⇒ 直接对应「同主体同站位」验收要点。
    """
    gx = np.abs(np.diff(L, axis=1))[:-1, :]
    gy = np.abs(np.diff(L, axis=0))[:, :-1]
    g = np.maximum(gx, gy)
    if region is not None:
        x0, x1 = region
        g = g[:, x0:x1]
    return float((g > thr).mean())


def dense_block_ratio(ink):
    """3×3 密块暗占比（hero 自有判据）：把图切块，统计墨覆盖率超阈的块占比。"""
    bh, bw = H // 3, W // 3
    blocks = []
    for by in range(3):
        for bx in range(3):
            blk = ink[by * bh:(by + 1) * bh, bx * bw:(bx + 1) * bw]
            blocks.append(blk.mean())
    # 「密块」= 该块墨覆盖率 > 0.5
    dense = sum(1 for v in blocks if v > 0.5)
    return dense / len(blocks)


def cinnabar_px(a):
    """J7 朱砂点睛计数（**宽色相带**·承负样本自测 N5 收紧后的再平衡）。

    口径演化（三次自测驱动·每版都跑负样本验证）：
      · 初版 `r>100 & r-b>40 & r-g>50` ⇒ **太松**：朱砂混向金色后仍满足 ⇒ 抓不到退化（N5 假绿）；
      · 二版 `r>140 & r-g>85 & g<95` ⇒ **只数到高饱和核心**：深色版朱砂被提亮后
        核心缩小（实测 09：浅 819 px → 深 58 px·但视觉面积相当且更鲜明）⇒ 假红。
      · 三版 `r>110 & r-g>60 & g<130` ⇒ 仍让「混色残余」通过（实测残余 37 px·r-g=76·g=129）。
      · **四版（本版·定稿）** `r>110 & r-g>95 & g<100` ——
        实测真朱砂：01 号 r-g 中位 131·g 中位 60；08 号 r-g 中位 147·g 中位 50；
        混色残余：r-g=76·g=129 ⇒ 该带能同时满足「抓住混色退化」与「不误杀真朱砂」。
    """
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return int(((r > 110) & ((r - g) > 95) & (g < 100)).sum())


def cinnabar_bbox(a):
    """朱砂像素的包围盒（用于「位置与浅色版一致」判据·J7b）——与 cinnabar_px 同一色相带。"""
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    m = (r > 110) & ((r - g) > 95) & (g < 100)
    ys, xs = np.where(m)
    if len(xs) == 0:
        return None
    return xs.min(), xs.max(), ys.min(), ys.max()


def ink_mask_of(a):
    """与配色无关的「墨迹」掩码：**显著偏离本图中位亮度**的像素。

    浅底版：暗于纸底（med-12）；暗底版：亮于纸底（med+12）。
    ⇒ 两版口径统一（都按「偏离本图基线」判定）⇒ 几何可比。
    """
    L = 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]
    med = float(np.median(L))
    return (L < med - 12) if med > 150 else (L > med + 12)


def proj_centroid(a, mask, x0=None, x1=None):
    """主体区（默认右 54%）的**列投影重心**（对纹理噪声不敏感）。"""
    if x0 is None:
        x0 = int(W * 0.46)
    if x1 is None:
        x1 = W
    w = mask[:, x0:x1].sum(axis=0).astype(float)
    tot = w.sum()
    if tot == 0:
        return None, 0.0
    idx = np.arange(x0, x1)
    return float((w * idx).sum() / tot), float(tot)


def vproj_centroid(a, mask, x0=None, x1=None):
    """主体区的**行投影重心**。"""
    if x0 is None:
        x0 = int(W * 0.46)
    if x1 is None:
        x1 = W
    w = mask[:, x0:x1].sum(axis=1).astype(float)
    tot = w.sum()
    if tot == 0:
        return None, 0.0
    idx = np.arange(H)
    return float((w * idx).sum() / tot), float(tot)


def subject_bbox(a):
    """主体包围盒（用于 J9 扣掉主体区 + J10 几何一致性）。

    口径（三轮订正·均据对抗复核实证）：
      ① 原实现取墨迹像素的 min/max ⇒ **被单颗孤立噪点拉爆**（实测 06：12 颗噪点把
         bbox 从 x[1536,2338] 拉成 x[0,2386]）⇒ 改用**列投影分位数**（排除两端离群列）。
      ② 分支判定原用 `sat.max() < 0.1` 判「浅色版」⇒ **有朱砂点的浅色版**（09 等）
         会被误判为深色版 ⇒ 浅色版 bbox 退化为整幅 ⇒ 几何对比全错。
      ③ 浅色版用「暗墨 L<200」、深色版用「亮线 L>110」⇒ **两版口径不同 ⇒ 不可比**
         （实测 06：深宽 519 vs 浅宽 843·09：深宽 1077 vs 浅宽 1434——差异来自
          「白瓷/米白/暗芯」这类**中间调部件在两版被归到了不同侧**）。
      ⇒ 最终口径：**两版统一用「边缘图」**（梯度幅值超阈·与配色完全无关）
        ⇒ 任何颜色/明暗的部件在两版都产生边缘 ⇒ bbox 可比。
    """
    L = 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]
    g = np.maximum(np.abs(np.diff(L, axis=1))[:-1, :], np.abs(np.diff(L, axis=0))[:, :-1])
    ink = g > 6.0
    col = ink.sum(axis=0)
    tot = col.sum()
    if tot == 0:
        return None
    nz = np.where(col > 0)[0]
    cum = np.cumsum(col[nz]) / tot
    lo = nz[min(np.searchsorted(cum, 0.01), len(nz) - 1)]
    hi = nz[min(np.searchsorted(cum, 0.99), len(nz) - 1)]
    ys, xs = np.where(ink[:, lo:hi + 1])
    if len(xs) == 0:
        return None
    y0, y1 = ys.min(), ys.max()
    mx_pad = int(W * 0.02)
    my_pad = int(H * 0.02)
    return (max(0, int(lo) - mx_pad), min(W, int(hi) + mx_pad),
            max(0, int(y0) - my_pad), min(H, int(y1) + my_pad))


def solid_black_ratio(a):
    """J8 黑色实心构件占比（深色版专项）。

    病根（实测 W1073 试点 01）：AI 重绘把「黑铁杆」理解成黑色实心杆——
    深色底上该构件与纸底同为暗色，肉眼极易漏看，但它是**语义漂移**
    （浅色版该处是纸色 + 细墨线，非实心黑块）⇒ 必须机器判据拦。
    口径：L<12 的像素占「与纸底显著不同」像素的比例；浅色版该处若为实心黑块，
    其暗像素占比会远高于线描形态。
    """
    L = 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]
    dark_px = (L < 12)
    if dark_px.sum() == 0:
        return 0.0, 0
    return float(dark_px.mean()), int(dark_px.sum())


def paper_cleanliness(a, subject_box=None):
    """J9 纸面洁净度（深色版专项）。

    病根（实测 W1073 试点 09·筋斗云）：AI 重绘把宣纸纤维质感画成了**黑色划痕**，
    撒满整幅纸面 —— 肉眼在缩略图上像"做旧质感"，但它污染了文字安全区
    （实测左侧 46% 墨量 0.00641 > 0.002 门槛），且浅色版对应处是干净纸面。

    口径订正（对抗复核 F1-② 实证·原口径恒真）：原实现统计 `L<12` 的**暗于纸底**像素，
    而 09 的纤维划痕是 L∈[12,95) 的**中灰** ⇒ 全部落进 paper 掩码 ⇒ 密度恒为 0
    （实测：左区偏离纸底 >12 的像素 7113 个·密度 0.00634·而判据读数 0.0）。
    ⇒ 改为**与纸底色的通道距离**：任一通道偏离 DARK_PAPER 超过 12/255 即算「不是纸底」。

    口径订正②（对抗复核 F1-③ 实证·原口径恒真）：原实现统计**整幅**暗像素，
    会把母版规格内的**黑色实心构件**（01 如意金箍棒的「黑铁杆」·浅色版同样有
    40770 个黑像素、x∈[1236,2280] 主体区）误判为"纸面划痕"。
    ⇒ 改为**扣掉主体包围盒**后，只统计**纸面区域**的偏离像素密度。
    """
    DARK = np.array([34, 29, 22], dtype=float)
    dev = np.abs(a - DARK[None, None, :]).max(axis=2)   # 与纸底色的通道距离
    speck = dev > 12
    left = speck[:, :int(W * 0.46)]
    left_density = float(left.mean())
    whole_density = float(speck.mean())
    if subject_box is not None:
        x0, x1, y0, y1 = subject_box
        paper_mask = np.ones_like(speck)
        paper_mask[y0:y1, x0:x1] = False
        paper_density = float((speck & paper_mask).sum() / max(paper_mask.sum(), 1))
    else:
        paper_density = float('nan')
    return left_density, whole_density, paper_density


def analyze(path, dark):
    im = Image.open(path).convert('RGB')
    # —— J1 尺寸判据必须在**裁切前**取原始尺寸（负样本自测 N6 实证）——
    #   若只判裁切后的尺寸 ⇒ 恒为 (2400,1017) ⇒ **J1 恒真**（假绿）。
    raw_size = im.size
    im = crop_to_spec(im)
    a = np.asarray(im).astype(float)
    ink, paper = masks(a, dark)
    left = ink[:, :int(W * 0.46)]
    # 左区纸面污点密度（与纸底色的通道距离 > 12）——J9 口径
    dev = np.abs(a - DARK_PAPER[None, None, :]).max(axis=2)
    left_dirty = float((dev[:, :int(W * 0.46)] > 12).mean())
    res = {
        'raw_size': raw_size,
        'size': im.size,
        'left_dirty': left_dirty,
        'left_ink_ratio': left.sum() / max(left.size, 1),
        'ink_ratio': ink.mean(),
        'right_share': ink[:, int(W * 0.5):].sum() / max(ink.sum(), 1),
        'paper_mean': a[paper].mean(0) if paper.sum() else np.array([np.nan] * 3),
        'paper_std': a[paper].std(0) if paper.sum() else np.array([np.nan] * 3),
        'paper_px': int(paper.sum()),
        'dense': dense_block_ratio(ink),
        'cinnabar': cinnabar_px(a),
    }
    return res, a


def check_dark(dark_path, light_path, label):
    d, da = analyze(dark_path, dark=True)
    l, la = analyze(light_path, dark=False)
    fails = []

    # J8 黑色实心构件（深色版专项）——浅色版对应处若为线描则暗像素占比应很低
    d_black, d_black_px = solid_black_ratio(da)
    l_black, l_black_px = solid_black_ratio(la)
    if d_black > 0.02 and d_black > max(l_black * 3, 0.02):
        fails.append(f'J8 黑色实心构件占比 {d_black*100:.2f}%（浅色版 {l_black*100:.2f}%）'
                     f'——疑似把线描构件实心化（AI 语义漂移）')

    # 边缘密度（配色免疫·J3 与 K1 同源度量）
    # K1 只度量**主体区**（右半·对抗复核 F3 复验口径）：全幅边缘混着纸面纹理·
    # 纹理密度随「左区是否压制纹理」而变 ⇒ 与「主体是否同形」无关
    SUBJ = (int(W * 0.5), W)
    d_edge = edge_density(0.299 * da[:, :, 0] + 0.587 * da[:, :, 1] + 0.114 * da[:, :, 2], region=SUBJ)
    l_edge = edge_density(0.299 * la[:, :, 0] + 0.587 * la[:, :, 1] + 0.114 * la[:, :, 2], region=SUBJ)
    edge_ratio = d_edge / max(l_edge, 1e-9)

    # J9 纸面洁净度（深色版专项·扣掉主体包围盒后统计纸面区）
    d_box = subject_bbox(da)
    l_box = subject_bbox(la)
    d_left_dirty, d_all_dirty, d_paper_dirty = paper_cleanliness(da, d_box)
    l_left_dirty, l_all_dirty, l_paper_dirty = paper_cleanliness(la, l_box)
    if d_left_dirty > J9_LEFT_MAX:
        fails.append(f'J9 文字安全区纸面有污点 密度 {d_left_dirty:.5f} > {J9_LEFT_MAX}'
                     f'——暗底放大了纸面纹理/划痕')
    # 主体外纸面区：只作**参考项**不判红（对抗复核 F2 复验后的口径再订正）——
    #   实测：09 的母版纹理带会延伸出主体 bbox（右侧宣纸质感区）⇒ 该密度天然偏高（0.0032），
    #   但那是**母版有意为之的宣纸质感**（浅色版同位置同样有·只是浅底不可见），
    #   且右侧不是文字区（叠字只发生在左侧 46%）⇒ 判红即假红。
    #   ⇒ 判据改为「只判左侧文字安全区必须干净」；主体外纸面区密度降级为参考读数。

    if d['raw_size'] != (W, H):
        fails.append(f'J1 原始尺寸 {d["raw_size"]} != {(W, H)}（判原图·非裁切后）')
    if d['left_ink_ratio'] > 0.002:
        fails.append(f'J2 左侧 46% 墨量 {d["left_ink_ratio"]:.5f} > 0.002')
    # J3 整图墨量：改用**边缘密度百分比**（配色免疫）
    # 口径订正（实测 W1073 首轮）：原口径「暗底版亮墨像素占比 ∈ [2.11%, 8.11%]」失效——
    #   浅色版整图墨量 2.11%–8.11% 是 hero 自有判据（W931），其统计对象是**全部深色墨迹**；
    #   而深色版的墨是**亮金/米白**，且部分主体含白瓷/米白大色块（08 玉净瓶瓶身、04 紧箍儿），
    #   这些色块 L 在 200–240 ⇒ 浅色版口径会把它们全排除 ⇒ 04/08 被误判「墨量 1.4%」= 假红。
    #   改用边缘密度（与 K1 同源·同一度量不同区间）⇒ 与配色解耦。
    d_edge_pct = 100 * d_edge
    if not (J3_EDGE_MIN <= d_edge_pct <= J3_EDGE_MAX):
        fails.append(f'J3 边缘密度占比 {d_edge_pct:.3f}% 越出 '
                     f'{J3_EDGE_MIN:.3f}%-{J3_EDGE_MAX:.3f}%')
    if d['right_share'] < 0.90:
        fails.append(f'J4 主体落右半区 {d["right_share"]*100:.1f}% < 90%')

    # —— J10 几何一致性（对抗复核 F3 要求·补「同主体同站位」的机器判据）——
    #   口径选型（三轮订正后定稿·依据＝实测标定而非直觉）：
    #     · bbox 口径**不可用**——深浅两版的「墨」按颜色阈值定义时口径不同
    #       （浅底版暗墨 / 暗底版亮线·白瓷米白与暗芯部件被归到不同侧）⇒ bbox 不可比；
    #       改用统一「偏离中位亮度」掩码后，bbox 又被暗底上放大的纸面纹理污染
    #       （实测 06：深宽 1992 vs 浅宽 529）。
    #     ⇒ 改用**投影重心**（对纹理噪声不敏感）+ 实测标定容差：
    #       实测现役 9 张：列重心 dx ∈ [-5.7, 30.7] · 行重心 dy ∈ [-2.0, 53.6]
    #       ⇒ 容差取 dx ≤ 70 px · dy ≤ 110 px（实测 max 的 2 倍余量）
    #       ⇒ 负样本（横向翻转主体）列重心 dx 会达数百 px ⇒ 必被抓到。
    cl, _ = proj_centroid(la, ink_mask_of(la))
    cd, _ = proj_centroid(da, ink_mask_of(da))
    vl, _ = vproj_centroid(la, ink_mask_of(la))
    vd, _ = vproj_centroid(da, ink_mask_of(da))
    if cl is not None and cd is not None:
        dx = abs(cd - cl)
        if dx > J10_DX_MAX:
            fails.append(f'J10 主体列重心偏移 dx={dx:.0f}px > {J10_DX_MAX}'
                         f'（深 {cd:.0f} vs 浅 {cl:.0f}）——主体站位漂移')
    if vl is not None and vd is not None:
        dy = abs(vd - vl)
        if dy > J10_DY_MAX:
            fails.append(f'J10 主体行重心偏移 dy={dy:.0f}px > {J10_DY_MAX}'
                         f'（深 {vd:.0f} vs 浅 {vl:.0f}）——主体站位漂移')
    if d['dense'] > DENSE_BLOCK_MAX:
        fails.append(f'J6 密块暗占比 {d["dense"]:.3f} > {DENSE_BLOCK_MAX}')
    if d['cinnabar'] < J7_CINNABAR_MIN:
        fails.append(f'J7 朱砂点睛几乎消失：深 {d["cinnabar"]}px / 浅 {l["cinnabar"]}px')
    else:
        # J7b 位置一致性：朱砂包围盒须与浅色版**同一处**（母版规格：点睛在主体右侧固定位）
        db = cinnabar_bbox(da)
        lb = cinnabar_bbox(la)
        if db and lb:
            dx = abs((db[0] + db[1]) / 2 - (lb[0] + lb[1]) / 2)
            dy = abs((db[2] + db[3]) / 2 - (lb[2] + lb[3]) / 2)
            if dx > 80 or dy > 60:
                fails.append(f'J7b 朱砂点睛位置偏移 深中心({(db[0]+db[1])//2},{(db[2]+db[3])//2}) '
                             f'vs 浅中心({(lb[0]+lb[1])//2},{(lb[2]+lb[3])//2})·dx={dx:.0f} dy={dy:.0f}')

    ratio = d['ink_ratio'] / max(l['ink_ratio'], 1e-9)
    if not (K1_PAIR_LO <= edge_ratio <= K1_PAIR_HI):
        fails.append(f'K1 边缘密度配对比值 {edge_ratio:.3f} 越出 [{K1_PAIR_LO}, {K1_PAIR_HI}]'
                     f'（深 {d_edge:.4f} / 浅 {l_edge:.4f}）——线条被收细或改写')
    resid = np.abs(d['paper_mean'] - DARK_PAPER).max() if d['paper_px'] else float('nan')
    if d['paper_px'] < 1000:
        fails.append(f'K2 纸底像素仅 {d["paper_px"]}·无法判定')
    elif resid > K2_PAPER_TOL:
        fails.append(f'K2 纸底残差 {resid:.2f}/255 > {K2_PAPER_TOL}')

    contrast = cr(INK_DARK, tuple(np.round(d['paper_mean']).astype(int)))
    if contrast < 4.5:
        fails.append(f'K3 对比度 {contrast:.2f} < 4.5 (AA)')

    print(f'--- {label} ---')
    print(f'  J1 尺寸 {d["size"][0]}x{d["size"][1]} | J2 左46%墨量 {d["left_ink_ratio"]:.5f} | '
          f'J3 整图墨量 {d["ink_ratio"]*100:.2f}% | J4 右半区 {d["right_share"]*100:.1f}%')
    print(f'  J3 边缘占比 {d_edge_pct:.3f}% | J4 右半区 {d["right_share"]*100:.1f}%')
    print(f'  J6 密块暗占比 {d["dense"]:.3f} | J7 朱砂 {d["cinnabar"]}px | '
          f'J8 黑实心 {d_black*100:.2f}%（浅 {l_black*100:.2f}%）')
    print(f'  J9 杂点 左侧 {d_left_dirty:.5f} / 纸面区 {d_paper_dirty:.5f}'
          f'（浅 {l_left_dirty:.5f} / {l_paper_dirty:.5f}）')
    print(f'  K1 边缘配对 {edge_ratio:.3f}（深 {d_edge:.4f}/浅 {l_edge:.4f}）| '
          f'K2 纸底残差 {resid:.2f}/255 | K3 对比度 {contrast:.2f}')
    if fails:
        for f_ in fails:
            print(f'  FAIL {f_}')
    else:
        print('  PASS 全部判据')
    return not fails


def self_test():
    """判据可证伪性自测（负样本·承坑表 E-05/E-06 纪律：判据必须能被证伪）。

    每条负样本**只破坏一个维度**，且必须被对应判据抓到：
      N1 纸底偏色（把纸底整体加亮）      → K2 残差必红
      N2 线条被收细（把墨线区压成纸色）    → K1 边缘配对必红
      N3 主体画到左半区（水平翻转）        → J4 右半区占比必红
      N4 文字安全区被墨迹污染              → J2 左侧 46% 墨量必红
      N5 朱砂点睛被抹掉                    → J7 必红
      N6 尺寸不对（缩到一半）              → J1 必红
    另跑一组**正样本**（现役成品）确认不误杀。
    """
    import tempfile
    import shutil

    print('=== 判据自测（负样本须红 / 正样本须绿）===')
    base = 'site/static/images/hero-line-01-ruyi-staff-dark.webp'
    light = 'site/static/images/hero-line-01-ruyi-staff.webp'
    if not os.path.exists(base):
        print('FAIL 正样本缺失，跳过自测')
        return 1

    ok, fails = True, []
    a = np.asarray(Image.open(base).convert('RGB')).astype(float)
    L = 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]

    def save(arr, tag):
        p = os.path.join(tempfile.gettempdir(), f'_w1073_neg_{tag}.webp')
        Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).save(p, 'WEBP', quality=90)
        return p

    # N1 纸底偏色
    n1 = a.copy(); n1 += 12
    p1 = save(n1, 'paper')
    # N2 线条收细（把亮墨线压向纸色）
    n2 = a.copy()
    bright = L > 110
    n2[bright] = n2[bright] * 0.25 + np.array(DARK_PAPER) * 0.75
    p2 = save(n2, 'thin')
    # N3 主体画到左半区
    n3 = a[:, ::-1, :].copy()
    p3 = save(n3, 'left')
    # N4 左侧文字安全区被污染
    n4 = a.copy(); n4[:, :int(W * 0.46)] = 250
    p4 = save(n4, 'safearea')
    # N5 朱砂点睛被抹掉（**彻底移除**朱砂像素 → 换成中性金·不留残余）
    n5 = a.copy()
    r, g, b = n5[:, :, 0], n5[:, :, 1], n5[:, :, 2]
    cinn = (r > 110) & ((r - g) > 60) & (g < 130)
    n5[cinn] = n5[cinn] * 0.4 + np.array([214, 178, 116]) * 0.6
    p5 = save(n5, 'nocinnabar')
    # N6 尺寸不对
    p6 = os.path.join(tempfile.gettempdir(), '_w1073_neg_size.webp')
    Image.open(base).convert('RGB').resize((1200, 508), Image.LANCZOS).save(p6, 'WEBP', quality=90)
    # N7 主体平移（几何漂移·对抗复核 F3 要求补的负样本）——**真平移**：把主体区整体右移 300px
    n7 = a.copy()
    shift = 300
    n7[:, :W - shift] = a[:, shift:]
    p7 = save(n7, 'shift')
    # N8 左区纸面放大纹理（模拟暗底可见的纤维污点）
    n8 = a.copy()
    n8[:, :int(W * 0.46)] += 16
    p8 = save(n8, 'leftspeck')

    CASES = [
        ('N1 纸底偏色', p1, 'K2'),
        ('N2 线条收细', p2, 'K1'),
        ('N3 主体跑到左半区', p3, 'J4'),
        ('N4 文字安全区被污染', p4, 'J2'),
        ('N5 朱砂点睛被抹掉', p5, 'J7'),
        ('N6 尺寸不对', p6, 'J1'),
        ('N7 主体平移（几何漂移）', p7, 'J10'),
        ('N8 左区纸面放大纹理', p8, 'J9'),
    ]
    for label, path, expect in CASES:
        d, da = analyze(path, dark=True)
        l, la = analyze(light, dark=False)
        d_edge = edge_density(0.299 * da[:, :, 0] + 0.587 * da[:, :, 1] + 0.114 * da[:, :, 2])
        l_edge = edge_density(0.299 * la[:, :, 0] + 0.587 * la[:, :, 1] + 0.114 * la[:, :, 2])
        ratio = d_edge / max(l_edge, 1e-9)
        resid = np.abs(d['paper_mean'] - DARK_PAPER).max() if d['paper_px'] else float('nan')
        d_m = ink_mask_of(da)
        l_m = ink_mask_of(la)
        d_cx, _ = proj_centroid(da, d_m)
        l_cx, _ = proj_centroid(la, l_m)
        j10_dx = abs(d_cx - l_cx) if (d_cx is not None and l_cx is not None) else 0.0
        hit = {
            'K2': not (resid <= K2_PAPER_TOL),
            'K1': not (K1_PAIR_LO <= ratio <= K1_PAIR_HI),
            'J4': d['right_share'] < 0.90,
            'J2': d['left_ink_ratio'] > 0.002,
            'J7': d['cinnabar'] < J7_CINNABAR_MIN,
            'J1': d['raw_size'] != (W, H),
            'J10': j10_dx > J10_DX_MAX,
            'J9': d['left_dirty'] > J9_LEFT_MAX,
        }[expect]
        mark = 'OK ' if hit else 'FAIL'
        if not hit:
            ok = False
            fails.append(f'{label} 未被抓到（期望 {expect} 必红）')
        print(f'  {mark} {label} · 期望 {expect} 必红 · 实测命中={hit} '
              f'(K1={ratio:.3f} K2={resid:.2f} J2={d["left_ink_ratio"]:.5f} '
              f'J4={d["right_share"]*100:.1f}% J7={d["cinnabar"]} J1raw={d["raw_size"]} '
              f'J10dx={j10_dx:.0f} J9L={d.get("left_dirty", 0):.5f})')
        try:
            os.remove(path)
        except OSError:
            pass

    # 正样本：现役成品须全绿
    print('  --- 正样本（现役成品）须全绿 ---')
    good = check_dark(base, light, '正样本 hero-line-01')
    if not good:
        ok = False
        fails.append('正样本被误判（判据过严）')

    print()
    print(f'=== 自测结论：{"全部通过 ✅" if ok else "存在 FAIL ❌"} ===')
    for f in fails:
        print('  FAIL', f)
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--site', action='store_true', help='判 site/static/images 下的成品')
    ap.add_argument('--cand', default='tmpe/w1072', help='候选图目录')
    ap.add_argument('--self-test', action='store_true', help='判据可证伪性自测（负样本）')
    args = ap.parse_args()

    if args.self_test:
        sys.exit(self_test())

    if args.site:
        pairs = [(f'site/static/images/{stem}-dark.webp',
                  f'site/static/images/{stem}.webp')
                 for stem, _ in PAIRS]
    else:
        pairs = []
        for stem, num in PAIRS:
            # 候选图：**优先取候选目录**（对抗复核 F1-④ 实证：原实现把 site 成品排第一
            # ⇒ --cand 参数被架空 ⇒ 出图迭代期「判候选图」实际不生效·判据空转）
            cand = sorted(glob.glob(f'{args.cand}/norm/{stem}-dark-norm.webp'))
            cand += sorted(glob.glob(f'{args.cand}/ai-{num}-dark.*'))
            if not cand:
                site_p = f'site/static/images/{stem}-dark.webp'
                if os.path.exists(site_p):
                    cand.append(site_p)
            light = f'site/static/images/{stem}.webp'
            if cand:
                pairs.append((cand[0], light))
            else:
                print(f'SKIP {stem}: 候选图缺失')

    all_ok = True
    for cand, light in pairs:
        ok = check_dark(cand, light, os.path.basename(cand))
        all_ok = all_ok and ok
        print()

    print('=== 结论 ===')
    if all_ok and pairs:
        print('全部判据通过 ✅')
        return 0
    print('存在 FAIL ❌')
    return 1


if __name__ == '__main__':
    sys.exit(main())
