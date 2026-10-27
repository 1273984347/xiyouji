# -*- coding: utf-8 -*-
"""W948：把 8 张线描人物题图按站内既有 chapter-plate 范式插入 8 个 reader 人物页

范式来源（site/reader/ch007.html 等百回页·W888 既有；W936/W945 已用于 13 张题图）：
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
    ("site/reader/people/金角大王.html", "plate-line-01-jinjiao.webp",
     "金角大王线描立像：头戴道冠身穿道袍，右手托举紫金红葫芦、葫芦颈系朱红封带"),
    ("site/reader/people/牛魔王.html", "plate-line-02-niumowang.webp",
     "牛魔王线描立像：牛首生两只粗大弯角，身披厚重铠甲，双手横持混铁棍"),
    ("site/reader/people/铁扇公主.html", "plate-line-03-tieshanggongzhu.webp",
     "铁扇公主线描立像：高髻广袖罗裙，双手持一把叶形长卵的大芭蕉扇，扇面中脉细脉清晰"),
    ("site/reader/people/蝎子精.html", "plate-line-04-xiezi.webp",
     "蝎子精线描立像：白衣艳丽女妖，腰后一条上翘蝎尾、尾端毒钩锐利，手持长杆倒马毒桩"),
    ("site/reader/people/黄袍怪.html", "plate-line-05-huangpaoguai.webp",
     "黄袍怪线描立像：头戴金盔身披明黄战袍，狼首尖耳獠牙，双手持金钢琢"),
    ("site/reader/people/镇元大仙.html", "plate-line-06-zhenyuan.webp",
     "镇元大仙线描立像：道冠宽袖道袍的老仙，左手托人形人参果，右手执拂尘"),
    ("site/reader/people/大鹏金翅雕.html", "plate-line-07-dapeng.webp",
     "大鹏金翅雕线描立像：人身背后展开巨大鹏翼，双手托阴阳二气瓶"),
    ("site/reader/people/太上老君.html", "plate-line-08-taishanglaojun.webp",
     "太上老君线描立像：白发长须老道，左手执拂尘，右手平托黑白阴阳鱼太极图"),
]

CSS = """    /* W948：专题题图（线描人物立像·沿用章回页 chapter-plate 范式·浅底宣纸图暗色模式隐藏） */
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
