# -*- coding: utf-8 -*-
"""_w983_insert_plates.py — W983：把 12 张线描题图按站内既有 chapter-plate 范式接入 12 个 reader 页

范式来源（`site/reader/ch007.html` 等百回页·W888 既有；W936/W945/W948/W952/W953 已用于 33 张题图）：
  样式  .chapter-plate { margin:28px auto 36px; max-width:420px; }
        .chapter-plate img { width:100%; height:auto; display:block; opacity:.92; }
        html[data-theme="dark"] .chapter-plate { display:none; }   ← 浅底宣纸图贴深色底会成亮斑
  位置  <h1> 之后（题图位）
  标记  <figure class="chapter-plate"> + <img loading="lazy" decoding="async">

幂等：已有 chapter-plate 的页面跳过；样式已存在则不重复插入。
写回用 newline=''（不二次转换 \r\n）。

题材 → 落位页的选择依据（见执行前计划 T30 附录 A·12 条落位页已由 ST-03 先验脚本逐页实读确认存在且无题图）：
  · people 4 张 → people 库主页面（如来 / 玉帝 / 百眼魔君 / 嫦娥外传）
  · themes 3 张 → themes 库专题页（神学干预机制 / 取经路径地理符号学 / 取经密码学）
  · essays·poetry·culture 3 张 → 三库专题页（西游与民俗学 / 西游诗词意象谱系 / 明代科举制度对照）
  · 回目页 2 张 → 第 010 回 / 第 004 回
"""
import io
import os
import re

REPO = r"D:\xiyouji"

# (页面相对路径, 图片文件名, alt 文本)
JOBS = [
    # —— people 人物 4 ——
    ("site/reader/people/如来.html", "plate-line-25-rulai.webp",
     "如来线描立像：头螺髻垂双耳，立于层叠莲花宝座，身披袈裟双手胸前结印"),
    ("site/reader/people/玉帝.html", "plate-line-26-yudi.webp",
     "玉皇大帝线描立像：头戴冕旒十二串珠，身着玄色宽袖帝服，双手平举白玉笏"),
    ("site/reader/people/百眼魔君.html", "plate-line-27-baiyan-mojun.webp",
     "百眼魔君线描立像：披发黄袍，额头正中张开一只内嵌数十小眼的千眼巨目，双手横持降妖杵"),
    ("site/reader/people/嫦娥外传.html", "plate-line-28-change.webp",
     "嫦娥线描立像：广袖长裙，右手抱玉兔，左手拈桂枝，身旁一轮满月"),
    # —— themes 主题 3 ——
    ("site/reader/themes/神学干预机制专题.html", "plate-line-29-shenxue-ganyu-topic.webp",
     "神学干预机制主题线描立像：如来左掌向下翻转压住五行山，右侧观音手持净瓶插柳枝"),
    ("site/reader/themes/取经路径地理符号学专题.html", "plate-line-30-lujing-ditu-topic.webp",
     "取经路径地理符号学主题线描立像：身披僧衣的行者双手平举展开的古代舆图，图上路线串起驿站圆点"),
    ("site/reader/themes/取经密码学专题.html", "plate-line-31-mima-pan-topic.webp",
     "取经密码学主题线描立像：道袍天机士左手托青铜密码转盘，右手边半卷竹简"),
    # —— essays / poetry / culture 跨学科 3 ——
    ("site/reader/essays/西游与民俗学.html", "plate-line-32-minsu-taofu-topic.webp",
     "西游与民俗学主题线描立像：披甲门神右手按剑、左手执桃符木牌，身侧散落爆竹"),
    ("site/reader/poetry/西游诗词意象谱系专题.html", "plate-line-33-yixiang-puxi-topic.webp",
     "西游诗词意象谱系主题线描立像：唐僧左手拈念珠仰首望月，右手边摊开一卷诗笺"),
    ("site/reader/culture/明代科举制度对照专题.html", "plate-line-34-keju-zhidu-topic.webp",
     "明代科举制度对照主题线描立像：青衫书生头戴儒巾，双手捧一卷考卷，身旁一方砚台"),
    # —— 回目页 2 ——
    ("site/reader/ch010.html", "plate-line-35-ch010-weizheng.webp",
     "第 010 回线描立像：魏征幞头绯色官服，双手横持长剑，身侧盘绕一条三爪之龙"),
    ("site/reader/ch004.html", "plate-line-36-ch004-bimawen.webp",
     "第 004 回线描立像：猴王头戴乌纱官帽、身着青色天庭官服，右手高举齐天大圣旗，左手托方官印"),
]

CSS = """    /* W983：题图（线描人物/主题立像·沿用章回页 chapter-plate 范式·浅底宣纸图暗色模式隐藏） */
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
