# -*- coding: utf-8 -*-
"""_w952_make_edge_sample.py — 造「左右白边」负样本，验证 J10 口径修正后仍可证伪

背景：W952 把 J10 的段内统计由「整段均值」改为「最亮 20% 像素均值」（修主体伸进顶部带的误报）。
**改口径必须自证仍能抓住真缺陷** —— 本脚本给一张合规母版左右各加 120 px 纯白边，
算出 J10 值并断言 > 阈值（5.0）；若不成立 ⇒ 判据被改废了。

输出：%TEMP%/w952_negative_white_edge.png（不入库）
"""
import os
import sys
import tempfile

from PIL import Image

REPO = r"D:\xiyouji"
sys.path.insert(0, os.path.join(REPO, "scripts"))
import importlib.util

spec = importlib.util.spec_from_file_location(
    "pv", os.path.join(REPO, "scripts", "_w945_plates_verify.py"))
pv = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pv)

SRC = os.path.join(REPO, "assets", "promo", "plate-set", "plate-line-06-jiuLingyuansheng.png")
EDGE = 120


def main():
    im = Image.open(SRC).convert("RGB")
    w, h = im.size
    out = Image.new("RGB", (w + 2 * EDGE, h), (255, 255, 255))
    out.paste(im, (EDGE, 0))
    dst = os.path.join(tempfile.gettempdir(), "w952_negative_white_edge.png")
    out.save(dst)

    good = pv.bg_band_diff(im)
    bad = pv.bg_band_diff(out)
    print("合规图 J10 = %.3f（阈值 %.1f）" % (good, pv.J10_MAX))
    print("白边样本 J10 = %.3f（阈值 %.1f）  样本：%s" % (bad, pv.J10_MAX, dst))
    if bad <= pv.J10_MAX:
        print("FAIL  判据被改废了：带白边的样本未被 J10 抓出")
        return 1
    if good > pv.J10_MAX:
        print("FAIL  合规图被判红（口径过严）")
        return 1
    print("PASS  J10 口径修正后仍可证伪：合规 %.3f ≤ 阈值，白边 %.3f > 阈值" % (good, bad))
    return 0


if __name__ == "__main__":
    sys.exit(main())
