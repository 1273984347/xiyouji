# -*- coding: utf-8 -*-
"""_w974_prepare.py — W974 成品处理（**只处理 raw/round11 的本批 12 张**）

与 `_w945_prepare.py` 的关系：
  · 复用其全部处理逻辑（裁 3:4 → 缩放 1200×1600 → 纸色归一 → 母版/站点版 → 拼图）
  · **关键差异**：作用域限定为 `raw/round11`（本批原件），**不重跑全目录**
    ⇒ 既有 40 张母版与站点版零改动（不完成定义第 5 条 / V-11 监控项）

每一步都幂等，可在同一批原件上反复重跑。

流程：
  1. 读 assets/promo/plate-set/raw/round11/*.jpg（出图原件，模型返回实为 JPEG）
  2. 中心裁切到精确 3:4（不拉伸）→ 缩放 1200×1600
  3. 纸色归一到页面底色 #FAF7F0（亮度加权加性平移·迭代至 |delta| < 0.3·上限 6 轮）
  4. 存母版 assets/promo/plate-set/plate-line-NN-*.png + .webp（含上部留白·供卡片叠字用）
  5. 站点版 = **只裁掉主体上方的留白**（cut = 主体顶 − 6 px·保留下部地面留白）→ site/static/images/
  6. 拼图 preview-contact-sheet.png（全目录 52 张·4 列自适应行数）

用法：py -3 scripts/_w974_prepare.py [--dry-run]
"""
from __future__ import annotations

import argparse
import os
import sys

from PIL import Image, ImageChops, ImageDraw

REPO = r"D:\xiyouji"
SET_DIR = os.path.join(REPO, "assets", "promo", "plate-set")
RAW_DIR = os.path.join(SET_DIR, "raw", "round11")
SITE_IMG = os.path.join(REPO, "site", "static", "images")
TARGET = (250, 247, 240)          # 页面底色 #FAF7F0
OUT_W, OUT_H = 1200, 1600         # 母版尺寸（3:4）
SITE_TOP_PAD = 6                  # 站点版主体顶距画布顶的余量（px）
SUBJ_MIN_AREA = 200               # 主体簇面积下限（px²）——小于此视为纸面噪点/孤立墨点
SUBJ_ROW_LIMIT = 800              # 慢速路径扫描的上部行数


def measure_paper(im: Image.Image):
    """最亮一档像素均值 = 该图纸色基调（阈值 238·排除墨晕干扰）"""
    small = im.resize((240, 320))
    px = list(small.getdata())
    bright = [p for p in px if sum(p) / 3 > 238]
    if not bright:
        bright = [p for p in px if sum(p) / 3 > 225]
    if not bright:
        return (0, 0, 0)
    return tuple(sum(c) / len(bright) for c in zip(*bright))


def normalize(im: Image.Image, delta) -> Image.Image:
    """按亮度加权的加性平移：亮像素权重 1（精确落目标）·暗像素权重 0（不动）"""
    r, g, b = im.split()
    out = []
    for ch, d in zip((r, g, b), delta):
        lut = []
        for v in range(256):
            w = 0.0 if v <= 180 else min(1.0, (v - 180) / 75.0)
            lut.append(max(0, min(255, int(round(v + d * w)))))
        out.append(ch.point(lut))
    return Image.merge("RGB", out)


def crop_3_4(im: Image.Image) -> Image.Image:
    """中心裁切到精确 3:4（不拉伸变形）"""
    w, h = im.size
    want = 3.0 / 4.0
    if abs(w / float(h) - want) < 0.002:
        return im
    if w / float(h) > want:          # 太宽 → 裁左右
        nw = int(round(h * want))
        x = (w - nw) // 2
        return im.crop((x, 0, x + nw, h))
    nh = int(round(w / want))        # 太高 → 裁上下
    y = (h - nh) // 2
    return im.crop((0, y, w, y + nh))


def ink_top(im, tol=26):
    """母版墨迹包围盒的顶边（主体顶）——站点版裁切线用

    ⚠️ W974 修正：**bbox 顶 ≠ 主体顶**。
    实测（`scripts/_w974_probe_subjtop.py`）：`plate-line-24-wudidong-topic` 顶部第 18 行仅
    **3 个孤立像素**（差值 41）——放大取证（`_probe_top_zoom.png`）显示 0–260 px 为纯宣纸底，
    只余极淡墨点污渍、零主体笔触 ⇒ bbox 顶被纸面噪点拉到 18 px ⇒ 裁切线失真
    （站点版 1588 px ≈ 母版高·标题与主体间仍多留约 160 px 空白）。

    ⇒ 改为「**主体顶 = 面积 ≥ SUBJ_MIN_AREA 的墨迹连通簇的最小顶**」：
      孤立噪点（个位数 px²）被滤掉；真实稀疏顶部（冠尖/羽饰）属大簇 ⇒ 保留、不切主体。

    注：既有 40 张中有 3 张两种口径不同（03-danaotian-gong +188 / 05-hunshi-sihou +113 /
    11-jingubang-zhongliang +4 px）——那 3 张属**存量**，本批不重写（见收官报告存量欠账登记），
    且其差异需人眼判定是噪点还是真实笔触后方可处置 ⇒ 不做自动化批量改。
    """
    reg = im.convert("RGB")
    d = ImageChops.difference(reg, Image.new("RGB", reg.size, TARGET))
    r, g, b = d.split()
    m = ImageChops.lighter(ImageChops.lighter(r, g), b)
    mask = m.point(lambda v: 255 if v > tol else 0)
    bbox = mask.getbbox()
    if not bbox:
        return 0
    w, h = reg.size
    px = mask.load()

    # 快速路径：bbox 顶所在簇面积达标 ⇒ bbox 顶即主体顶
    area = _cluster_area(px, w, h, bbox[0], bbox[1])
    if area >= SUBJ_MIN_AREA:
        return bbox[1]

    # 慢速路径：上部区域全扫，找面积 ≥ SUBJ_MIN_AREA 的簇的最小顶
    limit = min(h, SUBJ_ROW_LIMIT)
    seen = bytearray(w * limit)
    best = None
    for y0 in range(limit):
        for x0 in range(w):
            i0 = y0 * w + x0
            if seen[i0] or px[x0, y0] == 0:
                continue
            stack = [(x0, y0)]
            seen[i0] = 1
            c_area = 0
            c_miny = y0
            while stack:
                x, y = stack.pop()
                if px[x, y] == 0:
                    continue
                c_area += 1
                if y < c_miny:
                    c_miny = y
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        if dx == 0 and dy == 0:
                            continue
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < w and 0 <= ny < limit:
                            j = ny * w + nx
                            if not seen[j] and px[nx, ny]:
                                seen[j] = 1
                                stack.append((nx, ny))
            if c_area >= SUBJ_MIN_AREA and (best is None or c_miny < best):
                best = c_miny
    return best if best is not None else bbox[1]


def _cluster_area(px, w, h, sx, sy):
    """从 (sx, sy) 出发的 8-邻接连通簇面积"""
    stack = [(sx, sy)]
    seen = set()
    area = 0
    while stack:
        x, y = stack.pop()
        if (x, y) in seen:
            continue
        seen.add((x, y))
        if px[x, y] == 0:
            continue
        area += 1
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h:
                    stack.append((nx, ny))
    return area


def stem_of(base: str) -> str:
    """plate-line-13-xxx → plate-line-13-xxx（与既有 prepare 同一取名口径）"""
    parts = base.split("-", 2)
    if len(parts) < 3:
        return base
    return parts[0] + "-" + parts[1] + "-" + parts[2]


def collect_raws():
    """只收本批轮次目录的原件（不跨轮次·不碰既有 40 张）"""
    picked = []
    if not os.path.isdir(RAW_DIR):
        return picked
    for fn in sorted(os.listdir(RAW_DIR)):
        if fn.lower().endswith((".jpg", ".jpeg", ".png")):
            picked.append(os.path.join(RAW_DIR, fn))
    return picked


def all_masters():
    """全目录母版（拼图用·既有 40 + 本批 12）"""
    out = []
    if not os.path.isdir(SET_DIR):
        return out
    for fn in sorted(os.listdir(SET_DIR)):
        if fn.startswith("plate-line-") and fn.endswith(".png"):
            out.append(os.path.join(SET_DIR, fn))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    raws = collect_raws()
    if not raws:
        print("FAIL  %s 下无出图原件（本批原件目录）" % RAW_DIR)
        return 1
    print("本批原件：%d 份（作用域限定 raw/round11·既有 40 张不重写）" % len(raws))

    for rp in raws:
        base = os.path.splitext(os.path.basename(rp))[0]
        stem = stem_of(base)
        im = Image.open(rp).convert("RGB")
        src_size = im.size
        im = crop_3_4(im).resize((OUT_W, OUT_H), Image.LANCZOS)
        # 归一迭代：上限 6 轮·收敛条件 |delta| < 0.3（W948 实证：2 轮不够）
        for _ in range(6):
            avg = measure_paper(im)
            delta = tuple(TARGET[i] - avg[i] for i in range(3))
            if all(abs(d) < 0.3 for d in delta):
                break
            im = normalize(im, delta)
        avg = measure_paper(im)
        delta = tuple(TARGET[i] - avg[i] for i in range(3))
        print("%-34s 源 %s → %dx%d  归一后纸色 %s  残差=(%+.1f,%+.1f,%+.1f)" % (
            base, "%dx%d" % src_size, OUT_W, OUT_H, tuple(round(c) for c in avg),
            delta[0], delta[1], delta[2]))
        if args.dry_run:
            continue

        out_png = os.path.join(SET_DIR, stem + ".png")
        im.save(out_png, "PNG", optimize=True)
        out_webp = os.path.join(SET_DIR, stem + ".webp")
        im.save(out_webp, "WEBP", quality=90, method=6)

        # 站点版 = 只裁掉主体上方的留白（保留下部地面留白·W951 裁决）
        top_i = ink_top(im)
        cut = max(0, top_i - SITE_TOP_PAD)
        site_im = im.crop((0, cut, OUT_W, OUT_H))
        if not os.path.isdir(SITE_IMG):
            os.makedirs(SITE_IMG)
        site_webp = os.path.join(SITE_IMG, stem + ".webp")
        site_im.save(site_webp, "WEBP", quality=90, method=6)
        print("      母版 %s.png/.webp · 站点版：主体顶 %d → 裁掉上部 %d px → %dx%d" % (
            stem, top_i, cut, site_im.size[0], site_im.size[1]))

    if args.dry_run:
        return 0

    # ---- 拼图：全目录母版（4 列 · 行数自适应）----
    masters = all_masters()
    cols = 4
    tw, th = 300, 400
    pad, label_h = 14, 26
    rows = (len(masters) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw + (cols + 1) * pad,
                              rows * (th + label_h) + (rows + 1) * pad), TARGET)
    dr = ImageDraw.Draw(sheet)
    for i, mp in enumerate(masters):
        r, c = divmod(i, cols)
        x = pad + c * (tw + pad)
        y = pad + r * (th + label_h + pad)
        sheet.paste(Image.open(mp).convert("RGB").resize((tw, th), Image.LANCZOS), (x, y))
        dr.rectangle([x, y, x + tw - 1, y + th - 1], outline=(180, 172, 156))
        dr.text((x + 4, y + th + 6), os.path.basename(mp)[:-4].replace("plate-line-", ""),
                fill=(60, 54, 44))
    out_sheet = os.path.join(SET_DIR, "preview-contact-sheet.png")
    sheet.save(out_sheet, "PNG", optimize=True)
    sheet.convert("RGB").save(os.path.splitext(out_sheet)[0] + ".webp", "WEBP", quality=90, method=6)
    print("拼图：%s（%dx%d·%d 张）" % (out_sheet, sheet.size[0], sheet.size[1], len(masters)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
