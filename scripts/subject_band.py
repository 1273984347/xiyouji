#!/usr/bin/env python3
"""subject_band.py — 主体检测与派生裁切（不写盘·纯函数·W988 建·W1004 由归档桶转正）

为什么不用整幅墨迹 bbox（W974 实证的两个坑都在这里）：
  ① **孤立噪点会把主体顶拉歪**——整幅 bbox 顶可能被几枚 px 级污渍拉到画布顶
     （实测一张主体顶在 437 px 的图，bbox 顶被拉到 18 px）⇒ 改用
     **面积 ≥ min_area 的连通簇的最小顶**（真主体的稀疏顶部属大簇·必保留）。
  ② **朱砂印章是红不是墨**——水墨意境卡族每张带一枚朱红印章（右下/左下角），
     它与纸色的差值远大于阈值 ⇒ 整幅 bbox 会把印章当成主体的一部分。
     ⇒ 主体掩膜必须**排除朱砂像素**（r−g ≥ 35）**与赭金像素**（luma ≥ 90）。

三条不变量（横幅/og 派生共用·自证可证伪）：
  ① 主体顶未被切：裁切线上边 ≤ 主体顶
  ② 主体底未被切：裁切线下边 ≥ 主体底（当主体跨高 ≤ 目标高时才要求）
  ③ 头顶余量 > 0：裁切线上边到主体顶之间留出呼吸空间
"""
from __future__ import annotations

import numpy as np
from PIL import Image
from scipy import ndimage

PAPER = (250, 247, 240)
MIN_CLUSTER_AREA = 200      # W974 实证：200 px² 能滤掉孤立噪点又不切稀疏主体顶
VERMILION_MIN_RG = 35      # 朱砂 #C8463A ⇒ r−g = 70；赭金 #8A6D3B ⇒ r−g = 29（低于阈值不误判）
INK_LUMA_MAX = 90          # 墨 #23201A luma≈32；赭金 luma≈112；朱砂 luma≈108 ⇒ 阈值 90 只留墨


def _rgb_array(im: Image.Image) -> np.ndarray:
    return np.asarray(im.convert("RGB"), dtype=np.int16)


def ink_mask(im: Image.Image, tol: int = 26) -> np.ndarray:
    """整幅墨迹掩膜（含朱砂与赭金）——用于「画面是否为空」这类粗判。"""
    a = _rgb_array(im)
    d = np.abs(a - np.array(PAPER, dtype=np.int16)).max(axis=2)
    return d > tol


def body_mask(im: Image.Image, tol: int = 26) -> np.ndarray:
    """**主体墨**掩膜：排除朱砂（印章/点睛）与赭金，只留墨色笔画。"""
    a = _rgb_array(im)
    d = np.abs(a - np.array(PAPER, dtype=np.int16)).max(axis=2)
    m = d > tol
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    vermilion = (r - g) >= VERMILION_MIN_RG
    luma = (0.299 * r + 0.587 * g + 0.114 * b)
    light = luma >= INK_LUMA_MAX
    return m & ~vermilion & ~light


def subject_band(im: Image.Image, min_area: int = MIN_CLUSTER_AREA):
    """返回 (主体顶, 主体底, 主体像素数)：连通簇法（面积 ≥ min_area 的簇的极值）。

    主体底取**全部**有效簇的最大底（含小簇）——底部的地面线/飘带往往是小簇，
    漏掉它们会把裁切线抬得太高导致「地面留白」丢失。
    """
    m = body_mask(im)
    if not m.any():
        return None, None, 0
    labels, n = ndimage.label(m, structure=np.ones((3, 3), dtype=int))
    if n == 0:
        return None, None, 0
    sizes = ndimage.sum(m, labels, index=np.arange(1, n + 1))
    big = np.where(sizes >= min_area)[0] + 1
    if big.size == 0:                      # 无达标簇 ⇒ 退化到整幅 bbox（并由调用方告警）
        ys = np.where(m)[0]
        return int(ys.min()), int(ys.max() + 1), int(m.sum())
    tops = []
    for lb in big:
        ys = np.where(labels == lb)[0]
        tops.append(int(ys.min()))
    top = min(tops)
    ys_all = np.where(m)[0]
    bottom = int(ys_all.max() + 1)
    return top, bottom, int(m.sum())


def crop_band(im: Image.Image, out_w: int, out_h: int, mode: str, head_pad: int = 30):
    """按主体带派生一个 out_w × out_h 的图（只裁不缩放——不拉伸变形）。

    mode="banner"（1:1 → 宽幅）：保「头顶 + 上半身」——裁切带上边 = 主体顶 − head_pad。
    mode="og"（→ 社交卡 1200×630）：
        · 主体跨高 ≤ out_h ⇒ 取**居中带**（主体完整，上下留白对称）
        · 主体跨高 >  out_h ⇒ 取**头部带** [主体顶 − head_pad, +out_h]（保头部与胸腹）

    返回 (cropped_image, info)；info 含裁切线、主体顶/底、头顶余量·供验算脚本判红。
    """
    top, bottom, _ = subject_band(im)
    if top is None:
        raise ValueError("画面无主体墨迹·不可裁切")
    w, h = im.size
    span = bottom - top
    if mode == "banner":
        y0 = max(0, top - head_pad)
        y1 = min(h, y0 + out_h)
        if y1 - y0 < out_h:                # 触底则上移，保证高度足
            y1 = h
            y0 = max(0, y1 - out_h)
    elif mode == "og":
        if span <= out_h:
            y0 = max(0, top - (out_h - span) // 2)
            y1 = min(h, y0 + out_h)
            if y1 - y0 < out_h:
                y1 = min(h, y0 + out_h)
        else:
            y0 = max(0, top - head_pad)
            y1 = min(h, y0 + out_h)
            if y1 - y0 < out_h:
                y1 = h
                y0 = max(0, y1 - out_h)
    else:
        raise ValueError("未知 mode: " + mode)
    if y1 - y0 != out_h:                   # 极端兜底：源高不足则补纸面
        raise ValueError("源高 %d 不足目标高 %d" % (h, out_h))
    out = im.crop((0, y0, w, y1)).resize((out_w, out_h), Image.LANCZOS) \
        if (w, y1 - y0) != (out_w, out_h) else im.crop((0, y0, w, y1))
    info = {
        "src_size": [w, h], "crop_y": [y0, y1], "subject_top": top, "subject_bottom": bottom,
        "head_room": top - y0, "span": span, "mode": mode,
        "subject_bottom_kept": bottom <= y1,
    }
    return out, info
