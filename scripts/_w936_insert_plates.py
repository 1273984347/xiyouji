# -*- coding: utf-8 -*-
"""W936：把 5 张浓墨无字视觉按站内既有 chapter-plate 范式插入 5 个专题页

范式来源（site/reader/ch007.html 等百回页·W888 既有）：
  样式  .chapter-plate { margin:28px auto 36px; max-width:420px; }
        .chapter-plate img { width:100%; height:auto; display:block; opacity:.92; }
        html[data-theme="dark"] .chapter-plate { display:none; }   ← 浅底宣纸图贴深色底会成亮斑
  位置  <h1> 之后、首个 blockquote 之前（题图位）
  标记  <figure class="chapter-plate"> + <img loading="lazy" decoding="async">

与章回页的差异：章回插画是纯装饰（alt="" + aria-hidden）·本题图带题材信息 ⇒ 用描述性 alt（a11y 更好）。
"""
import io
import os
import re

REPO = r"D:\xiyouji"

# (页面相对路径, 图片文件名, alt 文本)
JOBS = [
    ("site/reader/people/地府体系深化专题.html", "plate-mingfu-panwang.webp",
     "冥府判官队列的浓墨剪影：黑帽判官执生死簿列队而下"),
    ("site/reader/people/紧箍儿的内侧-器物传记.html", "plate-jingu-jingangchui.webp",
     "紧箍与金刚杵的静物对置：左为紧箍红绦，右为金刚杵"),
    ("site/reader/themes/取经地理学专题.html", "plate-wujingshan-liangjie.webp",
     "五行山与两界山：浓墨山峦间横贯锁链"),
    ("site/reader/people/四海龙王外传.html", "plate-donghai-longgong.webp",
     "东海龙宫水殿：盘龙绕殿，气泡浮升"),
    ("site/reader/themes/西游与死亡研究专题.html", "plate-liudao-lunhui.webp",
     "六道轮回的抽象水墨：环轮与六道笔意"),
]

CSS = """    /* W936：专题题图（浓墨无字视觉·沿用章回页 chapter-plate 范式·浅底宣纸图暗色模式隐藏） */
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
        # 写回：newline='' 不作换行转换（文本已含原生 \r\n，避免二次转换产生双 CR）
        io.open(path, "w", encoding="utf-8", newline="").write(text)
        print("OK    " + rel + "  ← " + img)


if __name__ == "__main__":
    main()
