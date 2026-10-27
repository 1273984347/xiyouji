# -*- coding: utf-8 -*-
"""_w987_insert_scenes.py — W987：把 6 张水墨意境图接入回目页「场景插图」位

与题图范式**刻意分开**：
  题图  `.chapter-plate`   —— 母版段禁文字/书法/印章；暗色模式隐藏；限宽 420px
  场景图 `.chapter-scene`  —— 本族每张带朱红印章 ⇒ 不适用题图母版段；同样暗色隐藏（浅底贴深色底会成亮斑）

插入点：正文**首个 `<h2>` 之前**（首屏留给题图·第二资产下沉到正文入口）。
幂等：页面已含 `chapter-scene` ⇒ SKIP。
写回用 newline=''（不二次转换 \\r\\n）。

用法：py -3 scripts/_w987_insert_scenes.py
"""
import io
import os
import re
import sys

REPO = r"D:\xiyouji"

# (页面文件名, 源图名, alt 文本)
JOBS = [
    ("ch007", "chap-07.webp",
     "第 007 回水墨意境图：八卦炉立于石上，炉火上扬，地面留墨影，右下角一枚朱红印章"),
    ("ch014", "chap-14.webp",
     "第 014 回水墨意境图：猴形剪影攀绳而上，浓墨大写意，右下角一枚朱红印章"),
    ("ch015", "chap-15.webp",
     "第 015 回水墨意境图：白马立于崖边引缰，右侧大笔水墨山崖，右下角一枚朱红印章"),
    ("ch023", "chap-23.webp",
     "第 023 回水墨意境图：静坐剪影与一盏烛台，远处两道人影淡出，右下角一枚朱红印章"),
    ("ch027", "chap-27.webp",
     "第 027 回水墨意境图：三个背影走向茅屋，上方一轮日晕，檐下一副扁担，右下角一枚朱红印章"),
    ("ch030", "chap-30.webp",
     "第 030 回水墨意境图：黑虎盘于洞口，山峦与旋纹铺陈，右下角一枚朱红印章"),
]

CSS = """    /* W987：场景插图（水墨意境卡族·可带印章·与题图 .chapter-plate 刻意分开的独立规范） */
    .chapter-scene { margin: 34px auto 30px; max-width: 520px; }
    .chapter-scene img { width: 100%; height: auto; display: block; opacity: .95; }
    html[data-theme="dark"] .chapter-scene { display: none; }
"""

RE_SCENE = re.compile(r'class="chapter-scene"')
RE_H2 = re.compile(r"^[ \t]*<h2>", re.M)


def main() -> int:
    ok = skipped = failed = 0
    for name, img, alt in JOBS:
        rel = "site/reader/%s.html" % name
        path = os.path.join(REPO, rel.replace("/", os.sep))
        if not os.path.exists(path):
            print("SKIP  文件不存在: " + rel)
            skipped += 1
            continue
        raw = io.open(path, "rb").read()
        text = raw.decode("utf-8")
        nl = "\r\n" if b"\r\n" in raw else "\n"
        orig = text

        if RE_SCENE.search(text):
            print("SKIP  已有场景图: " + rel)
            skipped += 1
            continue

        # 1) 样式：若本页无 .chapter-scene 规则则插到最后一个 </style> 之前
        if ".chapter-scene" not in text:
            ms = list(re.finditer(r"[ \t]*</style>", text))
            if not ms:
                print("FAIL  未找到 </style>: " + rel)
                failed += 1
                continue
            m = ms[-1]
            css = CSS.replace("\n", nl) if nl != "\n" else CSS
            text = text[:m.start()] + css + text[m.start():]

        # 2) 场景图：插在正文首个 <h2> 之前
        h2 = RE_H2.search(text)
        if not h2:
            print("FAIL  未找到 <h2>: " + rel)
            failed += 1
            continue
        prefix = "../static/images/"
        fig = (
            '<figure class="chapter-scene">' + nl +
            '<img src="' + prefix + img + '" alt="' + alt + '" loading="lazy" decoding="async">' + nl +
            '</figure>' + nl + nl
        )
        text = text[:h2.start()] + fig + text[h2.start():]

        if text == orig:
            print("NOOP  " + rel)
            skipped += 1
            continue
        io.open(path, "w", encoding="utf-8", newline="").write(text)
        print("OK    %-30s <- %s" % (rel, img))
        ok += 1

    print("\n合计：接入 %d 页 · 跳过 %d 页 · 失败 %d 页" % (ok, skipped, failed))
    return 1 if failed or ok != len(JOBS) else 0


if __name__ == "__main__":
    raise SystemExit(main())
