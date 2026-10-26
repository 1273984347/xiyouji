# -*- coding: utf-8 -*-
"""_w974_insert_plates.py — W974：把 12 张线描题图按站内既有 chapter-plate 范式接入 12 个 reader 页

范式来源（`site/reader/ch007.html` 等百回页·W888 既有；W936/W945/W948/W952/W953 已用于 33 张题图）：
  样式  .chapter-plate { margin:28px auto 36px; max-width:420px; }
        .chapter-plate img { width:100%; height:auto; display:block; opacity:.92; }
        html[data-theme="dark"] .chapter-plate { display:none; }   ← 浅底宣纸图贴深色底会成亮斑
  位置  <h1> 之后（题图位）
  标记  <figure class="chapter-plate"> + <img loading="lazy" decoding="async">

幂等：已有 chapter-plate 的页面跳过；样式已存在则不重复插入。
写回用 newline=''（不二次转换 \r\n）。

题材 → 落位页的选择依据（见执行前计划 T29 附录 A）：
  · 人物组 6 张 → people 库对应角色页
  · 主题组 6 张 → people 库中对应的主题/专题页（女儿国国王 / 车迟国三国师 / 狮驼岭三魔 / 老鼋 / 蜘蛛精 / 老鼠精）
  · 「金角大王」图改落 `金角银角深化专题.html`——因 `people/金角大王.html` 已被 W945 的紧箍儿题图占用
"""
import io
import os
import re

REPO = r"D:\xiyouji"

# (页面相对路径, 图片文件名, alt 文本)
JOBS = [
    # —— 人物 6 ——
    ("site/reader/people/金角银角深化专题.html", "plate-line-13-jinjiaodawang.webp",
     "金角大王线描立像：头戴紫金冠、身着杏黄道袍，左手托细颈紫金红葫芦、右手托白瓷羊脂玉净瓶"),
    ("site/reader/people/银角大王.html", "plate-line-14-yinjiaodawang.webp",
     "银角大王线描立像：头戴银丝宝冠、身着白色道袍，右手横持七星剑、左手垂下盘成三圈的幌金绳"),
    ("site/reader/people/黄眉老佛外传.html", "plate-line-15-huangmeidawang.webp",
     "黄眉大王线描立像：右肩扛人种袋、左手托半面金铙，神情骄矜"),
    ("site/reader/people/黑熊精.html", "plate-line-16-heixiongjing.webp",
     "黑熊精线描立像：熊身人相、头戴小金箍，双手横持两端带金箍的如意金箍棒"),
    ("site/reader/people/托塔李天王外传.html", "plate-line-17-tuota-lijing.webp",
     "托塔李靖线描立像：身披金甲头戴金冠，左手平托七层玲珑宝塔、右手按着一柄宝剑"),
    ("site/reader/people/玉兔精.html", "plate-line-18-yutujing.webp",
     "玉兔精线描立像：兔首人身、颈挂念珠，右手横持捣药杵、左手托一只浅口玉药臼"),
    # —— 主题 6 ——
    ("site/reader/people/女儿国国王.html", "plate-line-19-nvziguo-topic.webp",
     "女儿国主题线描立像：唐僧身前横置一把四弦琵琶，身后一道子母河与垂柳"),
    ("site/reader/people/车迟国三国师外传.html", "plate-line-20-chelingguo-topic.webp",
     "车迟国斗法主题线描立像：三位道士一字排开——虎首、羊首、鹿首，身前油锅、右侧仙丹"),
    ("site/reader/people/狮驼岭三魔-方向二深化.html", "plate-line-21-shituoling-topic.webp",
     "狮驼岭主题线描立像：青狮、白象、金翅大鹏雕三者横向并列，形制分明"),
    ("site/reader/people/老鼋外传.html", "plate-line-22-tonghehe-topic.webp",
     "通天河主题线描立像：老鼋四足立住、背上驮着一卷空白经卷，四周是通天河水波"),
    ("site/reader/people/蜘蛛精.html", "plate-line-23-pansidong-topic.webp",
     "盘丝洞主题线描立像：唐僧身前是濯垢泉池，画面上方垂下数道放射状蛛丝"),
    ("site/reader/people/老鼠精.html", "plate-line-24-wudidong-topic.webp",
     "无底洞主题线描立像：金鼻白毛鼠精鼻头一点朱砂红，一手执细钢钎，身后是地洞石壁"),
]

CSS = """    /* W974：题图（线描人物/主题立像·沿用章回页 chapter-plate 范式·浅底宣纸图暗色模式隐藏） */
    .chapter-plate { margin: 28px auto 36px; max-width: 420px; }
    .chapter-plate img { width: 100%; height: auto; display: block; opacity: .92; }
    html[data-theme="dark"] .chapter-plate { display: none; }
"""


def main() -> int:
    ok = skipped = failed = 0
    for rel, img, alt in JOBS:
        path = os.path.join(REPO, rel.replace("/", os.sep))
        if not os.path.exists(path):
            print("SKIP  文件不存在: " + rel)
            skipped += 1
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
                skipped += 1
                continue
            css = CSS.replace("\n", nl) if nl != "\n" else CSS
            text = text[:m.start()] + css + text[m.start():]

        # 2) 题图：插在 <h1>…</h1> 之后（已存在则跳过）
        if "chapter-plate" in text.split("</style>")[-1]:
            print("SKIP  已有插图: " + rel)
            skipped += 1
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
            skipped += 1
            continue
        text = text[:h1.end()] + fig + text[h1.end():]

        if text == orig:
            print("NOOP  " + rel)
            skipped += 1
            continue
        io.open(path, "w", encoding="utf-8", newline="").write(text)
        print("OK    " + rel + "  <- " + img)
        ok += 1
    print("\n合计：接入 %d 页 · 跳过 %d 页 · 失败 %d 页" % (ok, skipped, failed))
    return 0 if ok == len(JOBS) else 1


if __name__ == "__main__":
    raise SystemExit(main())
