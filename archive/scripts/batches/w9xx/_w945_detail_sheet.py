# -*- coding: utf-8 -*-
"""_w945_detail_sheet.py — 出「主体特写」拼图：自动裁各张主体包围盒并放大，用于人眼核形制

用法：py -3 scripts/_w945_detail_sheet.py [输出路径]
输出：assets/promo/plate-set/preview-detail-sheet.png（4 列 × 2 行·每格主体放大到接近原始分辨率）
"""
import os
import sys

from PIL import Image, ImageChops, ImageDraw

REPO = r"D:\xiyouji"
SET_DIR = os.path.join(REPO, "assets", "promo", "plate-set")
STEMS = [
    ("plate-line-01-wukong", "01 悟空·金箍棒+凤翅冠"),
    ("plate-line-02-tangseng", "02 唐僧·五佛冠+锡杖"),
    ("plate-line-03-bajie", "03 八戒·九齿钉耙"),
    ("plate-line-04-shaseng", "04 沙僧·骷髅项链+月牙铲"),
    ("plate-line-05-guanyin", "05 观音·玉净瓶+柳枝"),
    ("plate-line-06-erlangshen", "06 二郎神·天眼+三尖刃"),
    ("plate-line-07-baigujing", "07 白骨精·三变残影"),
    ("plate-line-08-honghaier", "08 红孩儿·火尖枪+真火"),
    ("plate-line-01-jinjiao", "09 金角大王·紫金红葫芦"),
    ("plate-line-02-niumowang", "10 牛魔王·牛首+混铁棍"),
    ("plate-line-03-tieshanggongzhu", "11 铁扇公主·叶形芭蕉扇"),
    ("plate-line-04-xiezi", "12 蝎子精·蝎尾毒钩+毒桩"),
    ("plate-line-05-huangpaoguai", "13 黄袍怪·狼首+金钢琢"),
    ("plate-line-06-zhenyuan", "14 镇元大仙·人参果+拂尘"),
    ("plate-line-07-dapeng", "15 大鹏金翅雕·鹏翼+二气瓶"),
    ("plate-line-08-taishanglaojun", "16 太上老君·太极图+拂尘"),
    ("plate-line-01-bailongma", "17 白龙马·三叉戟+龙影"),
    ("plate-line-02-dujiao-shengwang", "18 独角兕大王·独角+钢叉"),
    ("plate-line-03-linggan", "19 灵感大王·鱼尾+玉钵"),
    ("plate-line-04-huangfengguai", "20 黄风怪·黄鼠狼+芭蕉扇"),
    ("plate-line-05-saitaisui", "21 赛太岁·金毛犼+紫金铃"),
    ("plate-line-06-jiuLingyuansheng", "22 九灵元圣·九头狮"),
    ("plate-line-07-nezha", "23 哪吒·乾坤圈+火尖枪"),
    ("plate-line-08-angrixingguan", "24 昴日星官·公鸡+长鞭"),
    ("plate-line-09-jingu-topic", "25 紧箍咒·九倒刺金箍"),
    ("plate-line-10-jindouyun-topic", "26 筋斗云·祥云涡卷"),
    ("plate-line-11-fabao-topic", "27 法宝系统·五法宝列阵"),
    ("plate-line-12-wuzi-jing-topic", "28 无字真经·空白经卷"),
]
PAPER = (250, 247, 240)


def ink_bbox(im: Image.Image, tol=26):
    """主体包围盒：与纸底差 > tol 的像素的外接框（顶部 28% 留白区排除）"""
    w, h = im.size
    reg = im.crop((0, int(h * 0.25), w, h)).convert("RGB")
    d = ImageChops.difference(reg, Image.new("RGB", reg.size, PAPER))
    r, g, b = d.split()
    m = ImageChops.lighter(ImageChops.lighter(r, g), b)
    mask = m.point(lambda v: 255 if v > tol else 0)
    bbox = mask.getbbox()
    if not bbox:
        return (0, int(h * 0.25), w, h)
    x0, y0, x1, y1 = bbox
    y0 += int(h * 0.25)
    return (x0, y0, x1, y1)


def main(argv):
    out = argv[0] if argv else os.path.join(SET_DIR, "preview-detail-sheet.png")
    cols = 4
    rows = (len(STEMS) + cols - 1) // cols
    cw, ch = 600, 800
    pad, lab = 12, 24
    sheet = Image.new("RGB", (cols * cw + (cols + 1) * pad,
                              rows * (ch + lab) + (rows + 1) * pad), PAPER)
    dr = ImageDraw.Draw(sheet)
    for i, (stem, title) in enumerate(STEMS):
        p = os.path.join(SET_DIR, stem + ".png")
        im = Image.open(p).convert("RGB")
        bb = ink_bbox(im)
        crop = im.crop(bb)
        sc = min(cw / float(crop.width), ch / float(crop.height))
        crop = crop.resize((max(1, int(crop.width * sc)), max(1, int(crop.height * sc))),
                           Image.LANCZOS)
        r, c = divmod(i, cols)
        x = pad + c * (cw + pad)
        y = pad + r * (ch + lab + pad)
        sheet.paste(crop, (x + (cw - crop.width) // 2, y + (ch - crop.height) // 2))
        dr.rectangle([x, y, x + cw - 1, y + ch - 1], outline=(190, 182, 166))
        dr.text((x + 4, y + ch + 5), title, fill=(50, 45, 38))
        print("%-24s 主体 bbox=%s  放大后=%dx%d" % (stem, bb, crop.width, crop.height))
    sheet.save(out, "PNG", optimize=True)
    print("输出：%s（%dx%d）" % (out, sheet.size[0], sheet.size[1]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
