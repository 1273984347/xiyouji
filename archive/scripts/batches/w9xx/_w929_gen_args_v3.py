#!/usr/bin/env python3
"""_w929_gen_args_v3.py — W929 第二轮返工：钤印内文去字形化。

返工轨迹（留痕）：
  · v1 首轮：量化全绿·目视抳出**形态漂移**——hero-10 竖长条印 / hero-12 椭圆印 / 其余四张方形印。
  · v2 二轮：把形态写死为正方形后，**印面被画成清晰篆字形**（"可读汉字"观感）⇒ 与零文字纪律冲突。
  · v3 三轮（本版）：印面限定为**纯朱砂色块 + 不规则留白/颜料斑驳**，并显式排除
    任何"类似文字的笔画/字形/符号" ⇒ 保留"钤记位置与方形轮廓"的成套统一，同时消除字形。
  主体描述 / 锚点 / 笔触句 / 构图句 四段全部逐字沿用（只改钤印条款与禁项清单）。

用法：py -3 scripts/_w929_gen_args_v3.py [out.json]
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _w929_gen_args import ANCHOR, COMP, SPECS, STROKE  # noqa: E402

SEAL_V3 = (
    "The only permitted mark is one small cinnabar-red seal impression in the upper right corner of "
    "the paper: a square block of solid cinnabar pigment with slightly uneven stamped edges, its "
    "interior broken only by a few irregular pale gaps of unpainted paper and soft pigment mottling "
    "- no lines, no strokes, no glyphs, no characters, no resemblance to any script or writing "
    "system of any kind."
)

EXCLUDE_V3 = (
    "Strictly excluded: text, Chinese characters, calligraphy, seal-script glyphs, archaic symbols, "
    "letters, digits, logo, signature, watermark, caption, UI elements, close-up faces, ruled line, "
    "horizon line, border, frame, collage, split panels, duplicate objects, busy clutter, any "
    "writing-like mark, any glyph-like shape. Nothing is written anywhere in the picture and no "
    "shape in it resembles a character."
)

REDO = ["hero-10-mingfu-panwang", "hero-12-jingu-jingangchui"]


def prompt(subject: str) -> str:
    return "%s %s %s %s %s %s" % (subject, ANCHOR, STROKE, COMP, SEAL_V3, EXCLUDE_V3)


def build():
    reqs = []
    for s in SPECS:
        if s["key"] not in REDO:
            continue
        reqs.append({
            "output_file": s["key"] + ".png",
            "aspect_ratio": "16:9",
            "resolution": "2K",
            "prompt": prompt(s["subj"]),
        })
    return {"requests": reqs}


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "tmpe/_misc/w929_args_v3.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(build(), f, ensure_ascii=False, indent=2)
    print("写出 %s（%d 条·第三轮 %s）" % (out, len(REDO), "、".join(REDO)))
