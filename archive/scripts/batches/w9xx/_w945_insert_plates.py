# -*- coding: utf-8 -*-
"""W945：把 8 张线描人物题图按站内既有 chapter-plate 范式插入 8 个 reader 专题页

范式来源（site/reader/ch007.html 等百回页·W888 既有；site/reader/themes/取经路线地理专题.html·W936 既有）：
  样式  .chapter-plate { margin:28px auto 36px; max-width:420px; }
        .chapter-plate img { width:100%; height:auto; display:block; opacity:.92; }
        html[data-theme="dark"] .chapter-plate { display:none; }   ← 浅底宣纸图贴深色底会成亮斑
  位置  <h1> 之后（题图位）
  标记  <figure class="chapter-plate"> + <img loading="lazy" decoding="async">

与章回页的差异：章回插画是纯装饰（alt="" + aria-hidden）·本题图带题材信息 ⇒ 用描述性 alt。

幂等：已有 chapter-plate 的页面跳过；样式已存在则不重复插入。
写回用 newline=''（不二次转换 \r\n）。
"""
import io
import os
import re

REPO = r"D:\xiyouji"

# (页面相对路径, 图片文件名, alt 文本)
JOBS = [
    ("site/reader/themes/猴王到行者-五次蜕变.html", "plate-line-01-wukong.webp",
     "大圣悟空线描立像：头戴凤翅紫金冠，身披锁子甲与虎皮战裙，双手横持两端带金箍的如意金箍棒"),
    ("site/reader/themes/唐僧-凡躯圣心.html", "plate-line-02-tangseng.webp",
     "唐僧线描立像：头戴五佛冠，身披田相格纹袈裟，颈挂佛珠双手合十，身侧竖立莲花宝珠顶的九环锡杖"),
    ("site/reader/people/猪八戒.html", "plate-line-03-bajie.webp",
     "猪八戒线描立像：蒲扇耳前垂、外突猪鼻与獠牙，双手持横梁上排布九枚弯齿的钉耙"),
    ("site/reader/themes/沙僧-沉默者的智慧.html", "plate-line-04-shaseng.webp",
     "沙悟净线描立像：络腮胡卷发，颈挂骷髅头骨项链，双手持月牙刃的降妖宝杖"),
    ("site/reader/people/观音.html", "plate-line-05-guanyin.webp",
     "观音菩萨线描立像：头戴宝冠长辫垂肩，双手托玉净瓶、瓶中插柳枝，身下为莲花座"),
    ("site/reader/people/二郎神.html", "plate-line-06-erlangshen.webp",
     "二郎显圣真君线描立像：头戴凤翅金盔、额心竖目，持三尖两刃刀，脚旁伏哮天犬"),
    ("site/reader/people/白骨精.html", "plate-line-07-baigujing.webp",
     "白骨精线描立像：素白长裙、手提青色鬼火灯笼，身后浮现村姑、老妇、老翁三层渐次消散的残影"),
    ("site/reader/people/红孩儿.html", "plate-line-08-honghaier.webp",
     "红孩儿线描立像：赤红短发如火焰，项戴红肚兜，赤足持长枪，枪尖火焰与周身三昧真火"),
]

CSS = """    /* W945：专题题图（线描人物立像·沿用章回页 chapter-plate 范式·浅底宣纸图暗色模式隐藏） */
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
        depth = rel.count("/") - 1   # site/reader/themes/x.html → ../../static/...
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
