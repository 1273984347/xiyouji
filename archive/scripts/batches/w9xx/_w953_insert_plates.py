# -*- coding: utf-8 -*-
"""W953：把 12 张线描题图按站内既有 chapter-plate 范式插入 12 个 reader 专题页

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
    ("site/reader/themes/真假美猴王专题.html", "plate-line-01-zhenjia-meihouwang.webp",
     "真假美猴王主题线描立像：两个一模一样的猴王并排，各持一根相同的如意金箍棒，右侧一面照妖镜"),
    ("site/reader/themes/蟠桃园-体制内的秘密.html", "plate-line-02-pantao-yuan.webp",
     "蟠桃园主题线描立像：守园仙童双手前托浅盘，盘中三枚蟠桃，身后一株蟠桃树枝叶"),
    ("site/reader/themes/大闹天宫-英雄还是悲剧.html", "plate-line-03-danaotian-gong.webp",
     "大闹天宫主题线描立像：悟空头戴凤翅紫金冠、双手横持如意金箍棒，左肩扛杏黄旗杆，身后蟠桃枝叶"),
    ("site/reader/themes/水帘洞专题.html", "plate-line-04-shuilandong.webp",
     "水帘洞主题线描立像：石猴双手前伸作拨开帘幕之姿，身前垂落石帘，身后洞口与飞瀑"),
    ("site/reader/themes/混世四猴专题.html", "plate-line-05-hunshi-sihou.webp",
     "混世四猴主题线描立像：四只猴王一字排开——灵明石猴、赤尻马猴、通臂猿猴、六耳猕猴"),
    ("site/reader/themes/兵器的自我修养专题.html", "plate-line-06-bingqi-xiuyang.webp",
     "兵器专题线描立像：如意金箍棒、九齿钉耙、月牙铲、火尖枪四件悬浮排开，下方一位武僧抱拳而立"),
    ("site/reader/themes/二十八星宿专题.html", "plate-line-07-ershiba-xingsu.webp",
     "二十八星宿主题线描立像：星宿神将头戴星冠、身着星辰纹战袍，身后一轮星盘，一手持星形拂尘"),
    ("site/reader/themes/四值功曹专题.html", "plate-line-08-sizhi-gongcao.webp",
     "四值功曹主题线描立像：值年执玉板、值月执铜镜、值日执日轮、值时执漏刻，四位神将一字排开"),
    ("site/reader/themes/五方揭谛专题.html", "plate-line-09-wufang-jiedi.webp",
     "五方揭谛主题线描立像：五位护法神僧一字排开，各持金刚杵、铜铃、念珠、九环锡杖、玉如意"),
    ("site/reader/themes/六丁六甲专题.html", "plate-line-10-liuding-liujia.webp",
     "六丁六甲主题线描立像：六位甲胄神将结成一圈围向中央正面的一位，各执戟斧枪刀锤鞭"),
    ("site/reader/themes/金箍棒的重量-一万三千五百斤的秘密.html", "plate-line-11-jingubang-zhongliang.webp",
     "金箍棒重量主题线描立像：如意金箍棒横置，下方一杆大秤、秤砣是一只金箍环，旁边猴王侧身托起秤杆"),
    ("site/reader/themes/器物传记学专题.html", "plate-line-12-qiwu-zhuanji.webp",
     "器物传记主题线描立像：牛首妖王持混铁棍与白衣龙君托玉净瓶并立，两人之间悬着一只紫金红葫芦"),
]

CSS = """    /* W953：专题题图（线描主题立像·沿用章回页 chapter-plate 范式·浅底宣纸图暗色模式隐藏） */
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
