#!/usr/bin/env python3
"""_w929_gen_args.py — W929 六张站点 Hero 素材图的生成参数（锚点承 W852→W893，本批按主视觉改造）。

锚点纪律（承 W852→W882→W893 五批）：
  · art direction 段（五色锁死：宣纸 #FAF7F0 / 玄墨 #221D16 / 淡墨 #6B6455 / 单一朱砂 #C8463A / 赭金 #E9B885）
    与「松散枯笔湿染」笔触句 —— **逐字复用 W893**，一个字不改。
  · 构图句 —— **逐字复用 W893 的 16:9 版**（主体止于上 2/3 + 下三分之一完全空白宣纸 = 叠字区）。
    W881 实证：正面几何描述词会被模型字面执行画成横贯硬线，故沿用纯否定式写法。
  · 本批**两处刻意改动**（相对 W893，逐条留痕）：
    ① 笔触段从「淡彩湿染」加强为「浓墨剪影为主、淡墨为辅」——对齐 assets/promo/hero-main-visual.png
       的主视觉观感（宣纸底 + 浓墨大块剪影），这是用户点名的参考风格。
    ② 禁项清单**移除** "seal stamp"、另加一条「唯一允许的印记 = 右上角极小朱砂方印（抽象几何笔画·
       不可辨识字符）」——用户点名的参考风格含「朱砂钤记」。仍保留 signature / Chinese characters /
       calligraphy 禁令 ⇒ 不产生可读文字。成图后逐张目视复核，若出现乱码字符则该张去印重做。
  · 画幅差异只在交付端机械处理，锚点段六张完全同源。

主题分配（四类全覆盖 · 6 张）：人物叙事 2 / 法器符号 1 / 世界观场景 2 / 学术概念 1。
题材全部避开既有 hero-01..09 与 card-01..27 撞车。
"""
import json

# ---------------------------------------------------------------- 锚点（逐字复用 W893）
ANCHOR = (
    "Art direction (identical for the whole series): contemporary Chinese ink-and-wash painting "
    "(水墨淡彩) on warm rice paper. Palette locked to exactly these tones: paper base #FAF7F0, "
    "warm beige wash #F1EBDD, ink linework and dark masses in xuan ink #221D16, secondary ink "
    "#6B6455, a single restrained cinnabar-red accent #C8463A covering under 5% of the frame, "
    "soft ochre-gold #E9B885 as the only highlight. Matte, flat, low-saturation value structure; "
    "confident brush linework; generous negative space; scholarly and calm, not decorative. "
    "No glossy 3D, no photorealism, no neon or saturated hues, no gradients, no heavy texture, "
    "no vignette. Rendered with loose, broken xuan-ink brush strokes and soft wet washes; edges "
    "fade and bleed; no hard vector outlines, no cel shading, no crisp digital line art."
)

# 本批改动 ①：笔触段加强为「浓墨剪影为主」
STROKE = (
    "Rendered as bold xuan-ink silhouettes and masses over soft wet washes: the principal forms "
    "read as solid dark cut-out shapes with dry-brush broken edges, secondary forms stay pale and "
    "washed, a few decisive strokes, elements evenly spaced and clearly separated, nothing "
    "overlapping."
)

# 构图句（逐字复用 W893 的 16:9 版）
COMP = (
    "Composition rule (obey exactly): 16:9 wide banner; the subject sits in the upper two "
    "thirds of the canvas with open blank paper below it; the lower third is completely empty "
    "warm rice-paper (#FAF7F0) with no objects, no ink, no texture, no marks and no gradient "
    "- a clean reserved strip for a headline. One single clear focal subject, large and readable."
)

# 本批改动 ②：禁项移除 seal stamp，改为「唯一允许的印记」条款
EXCLUDE = (
    "Strictly excluded: text, Chinese characters, calligraphy, letters, digits, logo, signature, "
    "watermark, caption, UI elements, close-up faces, ruled line, horizon line, border, "
    "frame, collage, split panels, duplicate objects, busy clutter. "
    "The only permitted mark is one tiny cinnabar-red square seal impression in the upper right "
    "area, no larger than three percent of the frame width, made only of abstract geometric "
    "strokes with no characters of any kind and nothing written."
)


def prompt(subject: str) -> str:
    return "%s %s %s %s %s" % (subject, ANCHOR, STROKE, COMP, EXCLUDE)


# ---------------------------------------------------------------- 六张
SPECS = [
    dict(key="hero-10-mingfu-panwang", theme="人物叙事", subj=(
        "A pale ink hall scene: a file of dark robed underworld judges standing in a slow procession "
        "across the upper area, each figure a simplified solid silhouette seen from behind or "
        "three-quarter back with no face visible, tall black official hats forming a rhythmic row, "
        "one figure at the front holding a long brush and a scroll, a single cinnabar-red lantern "
        "glowing low between them, pale mist pooling at their feet. The procession dissolves into "
        "blank paper by two thirds of the canvas height."
    )),
    dict(key="hero-11-chiping-boshan", theme="人物叙事", subj=(
        "A solitary standing bodhisattva figure in the upper area, seen from behind with the face "
        "never visible, a tall robe falling in heavy straight folds of dense xuan ink, a small jade "
        "vase held in one raised hand, a soft ring of light around the head, one small cinnabar-red "
        "ribbon knotted at the sash, the figure standing alone on bare paper, the robe base "
        "dissolving into blank paper by two thirds of the canvas height."
    )),
    dict(key="hero-12-jingu-jingangchui", theme="法器符号", subj=(
        "A still life of two ritual objects resting on bare paper in the upper area: a plain dark "
        "iron ring of medium thickness lying flat in slight perspective, and beside it a short "
        "vajra scepter with a faceted head and a wrapped grip laid at a shallow diagonal, both "
        "rendered as dense black ink silhouettes with dry-brush broken edges, one small cinnabar-red "
        "cord tied to the ring, a faint ochre-gold gleam along the vajra head. The objects fade into "
        "blank paper by two thirds of the canvas height."
    )),
    dict(key="hero-13-wujingshan-liangjie", theme="世界观场景", subj=(
        "A towering cliff of dark stone rising through the upper area, split down the middle by a "
        "deep vertical cleft with pale light seeping through it, horizontal bands of old prayer cloth "
        "and rusted iron chains pressed across the rock face, thin dry-brush pines on the ledges, one "
        "small cinnabar-red pennant caught on a chain, drifting mist crossing the cleft, a faint "
        "ochre-gold dawn light on the upper rocks. The cliff base dissolves into blank paper by two "
        "thirds of the canvas height."
    )),
    dict(key="hero-14-donghai-longgong", theme="世界观场景", subj=(
        "An underwater palace seen through clear water in the upper area: layered palace roofs and "
        "slender pillars rising from a pale water floor, a long serpentine dragon silhouette coiling "
        "once around the central hall, thin horizontal ink strokes marking the water surface above, "
        "a scatter of pale bubbles, one small cinnabar-red pearl glowing near the dragon's head, cool "
        "grey washes shading the far walls. The water washes out into blank paper by two thirds of "
        "the canvas height."
    )),
    dict(key="hero-15-liudao-lunhui", theme="学术概念", subj=(
        "An abstract ink diagram evoking a wheel of six realms: three concentric broken ink rings in "
        "the upper area, each ring drawn with dry-brush strokes that break and fade, six dark ink "
        "segment masses set around the outer ring at even spacing, one segment filled with cinnabar "
        "red, a faint ochre-gold halo behind the centre, pale paper showing between the rings, "
        "nothing overlapping and no straight ruled lines. The diagram fades into blank paper by two "
        "thirds of the canvas height."
    )),
]


def build():
    reqs = []
    for s in SPECS:
        reqs.append({
            "output_file": s["key"] + ".png",
            "aspect_ratio": "16:9",
            "resolution": "2K",
            "prompt": prompt(s["subj"]),
        })
    return {"requests": reqs}


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "tmpe/_misc/w929_args.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(build(), f, ensure_ascii=False, indent=2)
    print("写出 %s（%d 条）" % (out, len(SPECS)))
