#!/usr/bin/env python3
"""_w893_gen_args.py — W893 十二张素材图的生成参数（锚点沿用 W882 改写版）。

四画幅各三张 + 四主题各三张（拉丁方排布·每画幅内三张主题互不相同）：
  16:9 Hero ×3  → 回目场景 / 通用意象 / 数据可视化插画
  1:1 卡片 ×3   → 回目场景 / 主要人物 / 数据可视化插画
  3:4 竖版 ×3   → 通用意象 / 主要人物 / 回目场景
  1200×630 ×3  → 通用意象 / 主要人物 / 数据可视化插画

锚点纪律（承 W852→W882 五批）：
  · art direction 段、配色五色、松散枯笔湿染笔触句、禁项清单 —— 逐字复用，不改一字。
  · 构图句用 W882 的**纯否定式改写版**：不写「clear horizontal composition boundary」这类
    正面几何描述词（W881 实证：正面描述会被模型字面执行、画成横贯全幅硬线），
    改为「主体坐于上方三分之二 + 下三分之一为空白宣纸」+ 禁项补 ruled line/horizon line。
  · 画幅差异只在交付端机械处理，锚点段四批完全同源。
"""
import json

# ---------------------------------------------------------------- 锚点（逐字复用）
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

STROKE = (
    "Rendered with loose xuan-ink brush strokes and soft wet washes: broken dry-brush edges that "
    "bleed into the rice paper, forms simplified rather than crisply outlined, a few decisive "
    "strokes, elements evenly spaced and clearly separated, nothing overlapping."
)

EXCLUDE = (
    "Strictly excluded: text, Chinese characters, calligraphy, letters, digits, logo, signature, "
    "seal stamp, watermark, caption, UI elements, close-up faces, ruled line, horizon line, border, "
    "frame, collage, split panels, duplicate objects, busy clutter."
)


def comp(fmt: str) -> str:
    """构图句：按画幅改几何，其余表述与 W882 改写版同源（纯否定式，无正面几何描述词）。"""
    if fmt == "16:9":
        return (
            "Composition rule (obey exactly): 16:9 wide banner; the subject sits in the upper two "
            "thirds of the canvas with open blank paper below it; the lower third is completely empty "
            "warm rice-paper (#FAF7F0) with no objects, no ink, no texture, no marks and no gradient "
            "- a clean reserved strip for a headline. One single clear focal subject, large and readable."
        )
    if fmt == "1:1":
        return (
            "Composition rule (obey exactly): 1:1 square canvas; the subject sits in the upper two "
            "thirds of the canvas with open blank paper below it; the lower third is completely empty "
            "warm rice-paper (#FAF7F0) with no objects, no ink, no texture, no marks and no gradient "
            "- a clean reserved area for a title. One single clear focal subject, large and readable."
        )
    if fmt == "3:4":
        return (
            "Composition rule (obey exactly): 3:4 tall vertical canvas; the subject sits in the upper "
            "two thirds of the canvas with open blank paper below it; the lower third is completely "
            "empty warm rice-paper (#FAF7F0) with no objects, no ink, no texture, no marks and no "
            "gradient - a clean reserved area for a title. One single clear focal subject, large and readable."
        )
    if fmt == "630":
        return (
            "Composition rule (obey exactly): wide banner for social sharing; the subject sits in the "
            "upper two thirds of the canvas with open blank paper below it; the lower third is "
            "completely empty warm rice-paper (#FAF7F0) with no objects, no ink, no texture, no marks "
            "and no gradient - a clean reserved strip for a headline. One single clear focal subject, "
            "large and readable."
        )
    raise ValueError(fmt)


def prompt(subject: str, fmt: str) -> str:
    return "%s %s %s %s" % (subject, ANCHOR, comp(fmt), EXCLUDE)


# ---------------------------------------------------------------- 十二张（拉丁方）
# key: 输出文件名 stem；fmt: 目标画幅；subj: 主体描述段
SPECS = [
    # —— 16:9 Hero ×3 ——
    dict(key="hero-07-liudao-lingyun", fmt="16:9", subj=(
        "A journey across immense layered mountain ranges at first light: pale ink-wash ridges "
        "receding into a sea of clouds, one long winding trail etched across a mid-ground ridge, "
        "seven tiny traveller silhouettes walking it in single file, one small cinnabar-red pennant "
        "among them. The mountain base dissolves into blank paper by two thirds of the canvas height."
    )),
    dict(key="hero-08-yunhai-chengqiao", fmt="16:9", subj=(
        "A vast sea of clouds filling the upper canvas, a single stone arch bridge emerging from the "
        "white cloud bank at the centre, a small dark-robed pilgrim and a small white horse standing "
        "on the bridge deck, a single cinnabar-red cloth streamer tied to the bridge rail. The cloud "
        "bank dissolves into blank paper by two thirds of the canvas height."
    )),
    dict(key="hero-09-shijue-wangluo", fmt="16:9", subj=(
        "An abstract ink diagram evoking a network of relations: a loose mesh of thin ink-drawn roots "
        "and branches interlocking across the upper area, small dark nodes where they meet, one node "
        "filled with cinnabar red, pale paper showing between the strands, a few soft ochre-gold "
        "connecting arcs. The mesh fades into blank paper by two thirds of the canvas height."
    )),
    # —— 1:1 卡片 ×3 ——
    dict(key="card-25-santiebaigujing", fmt="1:1", subj=(
        "A square ink composition: a stone grotto cliff on the left half with pale stacked tomb shapes "
        "inside its hollow, a white-boned skeletal figure standing small at the cave mouth in the "
        "middle distance, a single cinnabar-red strip of cloth snagged on the rocks. The cliff base "
        "dissolves into blank paper by two thirds of the canvas height."
    )),
    dict(key="card-26-wukong-jingu", fmt="1:1", subj=(
        "A square ink composition: a monkey-like warrior standing full length, seen from three-quarter "
        "back view with the face never visible, a long iron staff with a gold-wrapped head held upright "
        "in one hand, a short ochre-gold tiger-striped apron over a dark robe, one small cinnabar-red "
        "cord knotted at the sash, the figure standing alone on bare paper."
    )),
    dict(key="card-27-rejiao-fenxi", fmt="1:1", subj=(
        "A square ink motif evoking a sentiment heat field: a loose grid of soft dark ink dots "
        "scattered across the upper area, dot size and density varying to suggest intensity, one band "
        "of dots filled with cinnabar red, a few pale ochre-gold dots scattered among them, pale paper "
        "showing between the dots. The dot field fades into blank paper by two thirds of the canvas height."
    )),
    # —— 3:4 竖版 ×3 ——
    dict(key="post-07-gu-shan-yingxue", fmt="3:4", subj=(
        "A tall vertical ink portrait of an ancient mountain: a towering layered rock mass rising "
        "through the upper canvas, thin dry-brush pines clinging to a ledge, drifting pale mist bands "
        "crossing the stone, one small cinnabar-red pagoda lantern glowing at the cliff edge, a faint "
        "ochre-gold glow of dawn on the upper rocks. The mountain base dissolves into blank paper by "
        "two thirds of the canvas height."
    )),
    dict(key="post-08-tangseng-chanshi", fmt="3:4", subj=(
        "A tall vertical ink portrait of a monk standing full length, seen from behind with the face "
        "never visible, a ringed monk's staff held upright in one hand, a plain ochre-gold robe "
        "falling in loose folds, a soft pale halo of light around the head, one small cinnabar-red "
        "bead string at the wrist, the figure standing alone on bare paper."
    )),
    dict(key="post-09-bajiaoshan-zhaoyun", fmt="3:4", subj=(
        "A tall vertical ink portrait of a broad-pigmented boar-like warrior standing full length, "
        "seen from three-quarter back view with the face never visible, a nine-toothed rake resting "
        "on one shoulder, a dark robe over a pale ochre-gold belly, one small cinnabar-red ribbon at "
        "the collar, the figure standing alone on bare paper."
    )),
    # —— 1200×630 分享图 ×3 ——
    dict(key="og-13-changgui-shanmen", fmt="630", subj=(
        "A wide ink scene of a ruined temple gate: a weathered stone archway with broken lintels "
        "standing in the upper area, wild grass and pale moss around its base, mist threading through "
        "the opening, one small cinnabar-red prayer cloth caught on the stone, a faint ochre-gold lamp "
        "glow deep inside the gate. The ruins dissolve into blank paper by two thirds of the canvas height."
    )),
    dict(key="og-14-shaseng-denggao", fmt="630", subj=(
        "A wide ink scene of a moonlit river crossing: a low stone pier crossing a pale water surface "
        "in the upper area, a long-necked water bird resting on the pier with its wings half raised, "
        "the moon's soft ochre-gold reflection broken on the water, one small cinnabar-red float on a "
        "reed. The water washes out into blank paper by two thirds of the canvas height."
    )),
    dict(key="og-15-shijian-liejian", fmt="630", subj=(
        "A wide ink diagram evoking a chronological sequence: a horizontal procession of small carved "
        "notches and short vertical strokes across the upper area, spacing widening toward the left, "
        "one notch filled with cinnabar red, a few pale ochre-gold markers between them, pale paper "
        "showing between the marks. The sequence fades into blank paper by two thirds of the canvas height."
    )),
]

# 生成器支持的源比例（交付端机械处理成目标像素）
SRC_ASPECT = {"16:9": "16:9", "1:1": "1:1", "3:4": "3:4", "630": "16:9"}


def build():
    reqs = []
    for s in SPECS:
        reqs.append({
            "output_file": s["key"] + ".png",
            "aspect_ratio": SRC_ASPECT[s["fmt"]],
            "resolution": "2K",
            "prompt": prompt(s["subj"], s["fmt"]),
        })
    return {"requests": reqs}


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "tmpe/_misc/w893_args.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(build(), f, ensure_ascii=False, indent=2)
    print("写出 %s（%d 条）" % (out, len(SPECS)))
