"""_w608_crop_fig5.py — W608 匿名稿图 5 顶栏脱敏裁剪（一次性·可重复执行）

图 5-取经路线图-浅.png（2640×6422）为整页截图，顶部约 110px 含站点品牌栏
（「详解西游记」logo + 首页/数据看板/标签云/全文检索 导航）——双盲评审脱敏面。
裁顶栏后输出衍生图至 tmpe（不入仓库图表目录·仅匿名稿 docx 经 FIG5_OVERRIDE 引用）。
图 3/图 4 经核查为纯图表无品牌栏，无需处理。
"""
from PIL import Image
import os

SRC = r"D:\xiyouji\docs\S4-学术投稿\图表\图5-取经路线图-浅.png"
OUT = r"D:\xiyouji\tmpe\w607_docxgen\图5-取经路线图-浅-匿名.png"
CROP_TOP = 175  # 品牌栏高（160px 时顶缘仍余 logo 底尖红线·175px 净·KPI 区自 y≈235 起）

img = Image.open(SRC)
w, h = img.size
assert (w, h) == (2640, 6422), f"源图尺寸变化：{w}x{h}，请复核 CROP_TOP"
cropped = img.crop((0, CROP_TOP, w, h))
os.makedirs(os.path.dirname(OUT), exist_ok=True)
cropped.save(OUT)
print(f"cropped: {w}x{h} -> {w}x{h - CROP_TOP} -> {OUT}")
