# -*- coding: utf-8 -*-
"""_w974_negative_sample.py — 合成多维度坏样本（证伪 J6 / J8 / J10 / J3）

背景（W974）：负样本自检若只用「尺寸不对」的样本，只能证明 J1 有效，
不能证明其余判据可证伪 ⇒ 本脚本**合成**一个 3:4 尺寸但同时踩中多条判据的坏样本：
  ① J6 实心黑块   —— 下部放一块 500×500 的纯黑方块（远超 0.75 阈值）
  ② J8 相框       —— 四边各画 6 px 贯穿暗线
  ③ J10 背景不匀 —— 左侧 300 px 纯白（#FFFFFF）、其余米黄（#FAF7F0）⇒ 纸色带差
  ④ J3 整图墨量   —— 黑块拉高墨量（可超上限 0.12）
  ⑤ J9 纸色残差   —— 白色边带使最亮档像素均值偏离 #FAF7F0

输出：scripts/output/_w974_negative_sample.png（1200×1600）
用法：py -3 scripts/_w974_negative_sample.py
      py -3 scripts/_w945_plates_verify.py --negative scripts/output/_w974_negative_sample.png
"""
import os

from PIL import Image, ImageDraw

REPO = r"D:\xiyouji"
OUT = os.path.join(REPO, "scripts", "output")
PAPER = (250, 247, 240)
TARGET = (1200, 1600)


def main():
    im = Image.new("RGB", TARGET, PAPER)
    dr = ImageDraw.Draw(im)

    # ① J6：下部实心黑块
    dr.rectangle([350, 900, 850, 1400], fill=(0, 0, 0))
    # ② J8：四边贯穿暗线（相框）
    for b in (0, 4):
        dr.rectangle([b, b, TARGET[0] - 1 - b, TARGET[1] - 1 - b], outline=(20, 18, 15), width=6)
    # ③ J10：左侧纯白竖带（背景竖向色带）
    dr.rectangle([0, 0, 300, TARGET[1]], fill=(255, 255, 255))
    # 把黑块与框重画到白带之上（保持 ① ② 仍在）
    dr.rectangle([350, 900, 850, 1400], fill=(0, 0, 0))
    for b in (0, 4):
        dr.rectangle([b, b, TARGET[0] - 1 - b, TARGET[1] - 1 - b], outline=(20, 18, 15), width=6)

    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, "_w974_negative_sample.png")
    im.save(p, "PNG", optimize=True)
    print("写出负样本：%s（%dx%d）" % (p, TARGET[0], TARGET[1]))
    print("内含缺陷：① 下部 500×500 纯黑块（J6）② 四边 6 px 贯穿暗框（J8）"
          "③ 左侧 300 px 纯白竖带（J10）④ 墨量拉高（J3）⑤ 纸色残差（J9）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
