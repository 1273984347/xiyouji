# -*- coding: utf-8 -*-
"""_w945_make_frame_sample.py — 造一个「带黑框」的负样本，验证 J8 相框判据仍可证伪

做法：取一张合规题图，四周加 8px 纯黑边框 ⇒ 与 W944 踩过的「模型给插画套黑框」同型。
输出到 %TEMP%（不入库）· 供 `py -3 scripts/_w945_plates_verify.py --negative <路径>` 使用。
"""
import io
import os
import tempfile

from PIL import Image

REPO = r"D:\xiyouji"
SRC = os.path.join(REPO, "assets", "promo", "plate-set", "plate-line-06-erlangshen.png")
DST = os.path.join(tempfile.gettempdir(), "w945_negative_framed.png")

im = Image.open(SRC).convert("RGB")
w, h = im.size
b = 8
out = Image.new("RGB", (w + 2 * b, h + 2 * b), (0, 0, 0))
out.paste(im, (b, b))
out.save(DST)
print("负样本已生成：%s（%dx%d·黑框 %d px）" % (DST, out.size[0], out.size[1], b))
