# -*- coding: utf-8 -*-
"""_w984_insert_plates.py — W984：12 页接入（6 替换 + 6 新增·幂等）

两种动作
  REPLACE（6 个回目页）：页面已有浓墨渲染题图（`<figure class="chapter-plate" aria-hidden="true">` + 空 alt）
    ⇒ 改为引用本批线描版，并**移除 aria-hidden**（线描版有可描述内容，保留 aria-hidden 会让读屏用户永远听不到）
    ⇒ **原浓墨版文件 chap-*.webp 一律保留不删**（用户明令），仅页面引用切换
  INSERT（6 个新页）：沿用既有 chapter-plate 范式（样式块 + `<figure>` 插 `<h1>` 之后）

样式沿用既有范式（若本页已有 .chapter-plate 规则则不重复插入）：
  .chapter-plate { margin: 28px auto 36px; max-width: 420px; }
  .chapter-plate img { width: 100%; height: auto; display: block; opacity: .92; }
  html[data-theme="dark"] .chapter-plate { display: none; }

幂等：已是目标图源 ⇒ SKIP；REPLACE 页若 img src 已是本批图 ⇒ SKIP。
写回用 newline=''（不二次转换 \\r\\n）。

用法：py -3 scripts/_w984_insert_plates.py
"""
import io
import os
import re
import sys

REPO = r"D:\xiyouji"

# (页面相对路径, 动作, 图片文件名, alt 文本)
JOBS = [
    # —— REPLACE 6：回目页（浓墨版文件保留不删）——
    ("site/reader/ch007.html", "REPLACE", "plate-line-37-ch007-bagua-lu.webp",
     "第 007 回线描立像：孙悟空头戴凤翅紫金冠、身着虎皮裙，双手横持如意金箍棒，身侧立三足圆筒八卦炉，身后是横贯铁链的山"),
    ("site/reader/ch014.html", "REPLACE", "plate-line-38-ch014-liubei.webp",
     "第 014 回线描立像：孙悟空高举如意金箍棒，脚边放着一顶山贼头巾与一把朴刀，身后立一株古树"),
    ("site/reader/ch015.html", "REPLACE", "plate-line-39-ch015-yingchou.webp",
     "第 015 回线描立像：白龙马四足稳立，马身盘绕缰绳，身旁枯松一株，脚下三道涧水纹"),
    ("site/reader/ch023.html", "REPLACE", "plate-line-40-ch023-sichan.webp",
     "第 023 回线描立像：唐僧合十立于一侧宫装妇人旁，地上放着一只绣鞋，妇人手持香炉"),
    ("site/reader/ch027.html", "REPLACE", "plate-line-41-ch027-bailong.webp",
     "第 027 回线描立像：白龙自河水中探出，龙首昂起，河岸上唐僧隔水合十"),
    ("site/reader/ch030.html", "REPLACE", "plate-line-42-ch030-sancha.webp",
     "第 030 回线描立像：沙僧横持月牙铲，脚边放着一只扁担，身后三道旋起的风纹"),
    # —— INSERT 6：people 2 + themes 1 + essays·poetry·culture 各 1 ——
    ("site/reader/people/罗刹女外传.html", "INSERT", "plate-line-43-luoshanv.webp",
     "罗刹女线描立像：长发披肩，双手横持三尖两刃刀，手边悬着一只颈系朱红封带的小口圆腹红葫芦"),
    ("site/reader/people/奎木狼外传.html", "INSERT", "plate-line-44-kuimulang.webp",
     "奎木狼线描立像：狼首人身、头戴铁盔，双手横持一柄方头铜锤"),
    ("site/reader/themes/招安的两种结局专题.html", "INSERT", "plate-line-45-zhaoan-topic.webp",
     "招安主题线描立像：天庭官员乌纱官帽绯色圆领官袍，双手平托一卷完全留白的招安诏书，身侧一方留白官印"),
    ("site/reader/essays/西游与服饰学.html", "INSERT", "plate-line-46-fushi-topic.webp",
     "西游与服饰学主题线描立像：明代官员乌纱帽配青色圆领补服，胸前禽兽补纹以墨线勾出，腰束玉带"),
    ("site/reader/poetry/原著景物诗分类赏析专题.html", "INSERT", "plate-line-47-jingwu-topic.webp",
     "西游诗词意象谱系主题线描立像：披发诗僧立于孤舟之上，身旁一轮圆月，远处两座山峰，舟下三道水纹"),
    ("site/reader/culture/历史玄奘与小说玄奘专题.html", "INSERT", "plate-line-48-xuanzang-topic.webp",
     "历史玄奘与小说玄奘专题线描立像：负笈僧人身着袈裟背负竹制经箱、手握竹杖，身后是长安城垣与一面留白旌旗"),
]

CSS = """    /* W984：题图（线描人物/场景·沿用章回页 chapter-plate 范式·浅底宣纸图暗色模式隐藏） */
    .chapter-plate { margin: 28px auto 36px; max-width: 420px; }
    .chapter-plate img { width: 100%; height: auto; display: block; opacity: .92; }
    html[data-theme="dark"] .chapter-plate { display: none; }
"""

RE_FIG = re.compile(
    r'<figure class="chapter-plate"[^>]*>\s*<img[^>]*src="([^"]+)"[^>]*>\s*</figure>',
    re.S)


def main() -> int:
    replaced = inserted = skipped = failed = 0
    for rel, action, img, alt in JOBS:
        path = os.path.join(REPO, rel.replace("/", os.sep))
        if not os.path.exists(path):
            print("SKIP  文件不存在: " + rel)
            skipped += 1
            continue
        raw = io.open(path, "rb").read()
        text = raw.decode("utf-8")
        nl = "\r\n" if b"\r\n" in raw else "\n"
        orig = text
        depth = rel.count("/") - 1
        prefix = "../" * depth + "static/images/"
        target = prefix + img

        if action == "REPLACE":
            m = RE_FIG.search(text)
            if not m:
                print("FAIL  未找到既有 chapter-plate figure: " + rel)
                failed += 1
                continue
            if m.group(1) == target:
                print("SKIP  已指向本批图源: " + rel)
                skipped += 1
                continue
            old_src = m.group(1)
            fig = (
                '<figure class="chapter-plate">' + nl +
                '<img src="' + target + '" alt="' + alt + '" loading="lazy" decoding="async">' + nl +
                '</figure>'
            )
            text = text[:m.start()] + fig + text[m.end():]
            print("OK    替换 %-34s %s → %s（aria-hidden 已移除·原文件保留）" % (rel, old_src, target))
            replaced += 1
        else:  # INSERT
            if "chapter-plate" in text.split("</style>")[-1]:
                print("SKIP  已有插图: " + rel)
                skipped += 1
                continue
            if ".chapter-plate" not in text:
                m = re.search(r"[ \t]*</style>", text)
                if not m:
                    print("FAIL  未找到 </style>: " + rel)
                    failed += 1
                    continue
                css = CSS.replace("\n", nl) if nl != "\n" else CSS
                text = text[:m.start()] + css + text[m.start():]
            h1 = re.search(r"<h1>[^<]*</h1>\r?\n", text)
            if not h1:
                print("FAIL  未找到 <h1>: " + rel)
                failed += 1
                continue
            fig = (
                '<figure class="chapter-plate">' + nl +
                '<img src="' + target + '" alt="' + alt + '" loading="lazy" decoding="async">' + nl +
                '</figure>' + nl
            )
            text = text[:h1.end()] + fig + text[h1.end():]
            print("OK    接入 %-34s %s" % (rel, target))
            inserted += 1

        if text == orig:
            continue
        io.open(path, "w", encoding="utf-8", newline="").write(text)

    print("\n合计：替换 %d 页 · 接入 %d 页 · 跳过 %d 页 · 失败 %d 页" % (
        replaced, inserted, skipped, failed))
    return 1 if failed or (replaced + inserted) != len(JOBS) else 0


if __name__ == "__main__":
    raise SystemExit(main())
