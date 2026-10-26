# -*- coding: utf-8 -*-
"""W952：把 12 张线描题图按站内既有 chapter-plate 范式插入 12 个 reader 人物/主题页

范式来源（site/reader/ch007.html 等百回页·W888 既有；W936/W945/W948 已用于 21 张题图）：
  样式  .chapter-plate { margin:28px auto 36px; max-width:420px; }
        .chapter-plate img { width:100%; height:auto; display:block; opacity:.92; }
        html[data-theme="dark"] .chapter-plate { display:none; }   ← 浅底宣纸图贴深色底会成亮斑
  位置  <h1> 之后（题图位）
  标记  <figure class="chapter-plate"> + <img loading="lazy" decoding="async">

幂等：已有 chapter-plate 的页面跳过；样式已存在则不重复插入。
写回用 newline=''（不二次转换 \r\n）。
"""
import io
import os
import re

REPO = r"D:\xiyouji"

# (页面相对路径, 图片文件名, alt 文本)
JOBS = [
    ("site/reader/people/白龙马.html", "plate-line-01-bailongma.webp",
     "白龙马线描立像：白衣龙君头戴金冠、双手横持三叉戟，身后隐约浮起一条白龙龙影"),
    ("site/reader/people/独角兕大王.html", "plate-line-02-dujiao-shengwang.webp",
     "独角兕大王线描立像：青牛妖王额心生一只竖直长角，身披乌金铠甲，双手横持方头钢叉"),
    ("site/reader/people/灵感大王.html", "plate-line-03-linggan.webp",
     "灵感大王线描立像：鱼王头戴王冠身着龙袍，下身覆鳞鱼尾分叉展开，双手托一只盛水玉钵"),
    ("site/reader/people/黄风怪外传.html", "plate-line-04-huangfengguai.webp",
     "黄风怪线描立像：黄鼠狼身妖王头戴毗卢帽，双手持一把叶形芭蕉扇，身侧卷起三道风纹"),
    ("site/reader/people/赛太岁.html", "plate-line-05-saitaisui.webp",
     "赛太岁线描立像：人面狮身的金毛犼身披红色法衣，颈挂一枚硕大的紫金铃"),
    ("site/reader/people/九灵元圣-方向二深化.html", "plate-line-06-jiuLingyuansheng.webp",
     "九灵元圣线描立像：狮身雄健，颈部同时生出九个狮头、鬃毛层叠"),
    ("site/reader/people/哪吒.html", "plate-line-07-nezha.webp",
     "哪吒线描立像：少年神将双髻束发，颈挂乾坤圈，一手火尖枪一手混天绫，脚下风火轮"),
    ("site/reader/people/昴日星官.html", "plate-line-08-angrixingguan.webp",
     "昴日星官线描立像：头戴星冠身着羽衣，面部化作一只大公鸡形貌，手持长鞭"),
    ("site/reader/themes/紧箍咒专题.html", "plate-line-09-jingu-topic.webp",
     "紧箍咒主题线描立像：悟空头戴金圈紧箍、内缘一圈九个倒刺钩，额前系朱砂红绦，双手紧握金箍棒"),
    ("site/reader/themes/筋斗云专题.html", "plate-line-10-jindouyun-topic.webp",
     "筋斗云主题线描立像：悟空头戴凤翅紫金冠端坐于层叠祥云之上，一手前指衣袂后扬"),
    ("site/reader/themes/法宝系统专题.html", "plate-line-11-fabao-topic.webp",
     "法宝系统主题线描立像：道装仙人双手托举一排弧形排开的法宝——紫金红葫芦、玉净瓶、芭蕉扇、乾坤圈、金钢琢"),
    ("site/reader/themes/无字真经专题.html", "plate-line-12-wuzi-jing-topic.webp",
     "无字真经主题线描立像：比丘僧人双手捧着一卷完全空白的经卷，卷面只有淡赭金横纹、无任何字迹"),
]

CSS = """    /* W952：专题题图（线描人物/主题立像·沿用章回页 chapter-plate 范式·浅底宣纸图暗色模式隐藏） */
    .chapter-plate { margin: 28px auto 36px; max-width: 420px; }
    .chapter-plate img { width: 100%; height: auto; display: block; opacity: .92; }
    html[data-theme="dark"] .chapter-plate { display: none; }
"""


def main() -> int:
    for rel, img, alt in JOBS:
        path = os.path.join(REPO, rel.replace("/", os.sep))
        if not os.path.exists(path):
            print("SKIP  文件不存在: " + rel)
            continue
        raw = io.open(path, "rb").read()
        text = raw.decode("utf-8")
        nl = "\r\n" if b"\r\n" in raw else "\n"
        orig = text

        # 1) 样式：若本页已有 chapter-plate 规则则跳过
        if ".chapter-plate" not in text:
            m = re.search(r"[ \t]*</style>", text)
            if not m:
                print("SKIP  未找到 </style>: " + rel)
                continue
            css = CSS.replace("\n", nl) if nl != "\n" else CSS
            text = text[:m.start()] + css + text[m.start():]

        # 2) 题图：插在 <h1>…</h1> 之后（已存在则跳过）
        if "chapter-plate" in text.split("</style>")[-1]:
            print("SKIP  已有插图: " + rel)
            continue
        depth = rel.count("/") - 1   # site/reader/people/x.html → ../../static/...
        prefix = "../" * depth + "static/images/"
        fig = (
            '<figure class="chapter-plate">' + nl +
            '<img src="' + prefix + img + '" alt="' + alt + '" loading="lazy" decoding="async">' + nl +
            '</figure>' + nl
        )
        h1 = re.search(r"<h1>[^<]*</h1>\r?\n", text)
        if not h1:
            print("SKIP  未找到 <h1>: " + rel)
            continue
        text = text[:h1.end()] + fig + text[h1.end():]

        if text == orig:
            print("NOOP  " + rel)
            continue
        io.open(path, "w", encoding="utf-8", newline="").write(text)
        print("OK    " + rel + "  <- " + img)


if __name__ == "__main__":
    raise SystemExit(main())
