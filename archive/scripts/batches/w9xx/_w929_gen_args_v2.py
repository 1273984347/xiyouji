#!/usr/bin/env python3
"""_w929_gen_args_v2.py — W929 返工版：统一朱砂钤印形态（首轮目视复核抓到的一致性缺陷）。

首轮六张量化判据全绿，但**目视复核**抓到：钤印形态漂移——
  · hero-10 竖长条印（1:2 竖矩形）
  · hero-12 椭圆印 + 内含疑似字形
  · 其余四张为方形印
⇒ 成套一致性不达标（用户明令「成套出图保证风格一致」）。

本版两处改动（其余逐字不动·锚点/笔触/构图/主体描述全部沿用首轮）：
  ① 钤印条款写死为**正方形**（四边等长·边直·边平行）；
  ② 禁项追加 "no seal-script glyphs, no archaic symbols" ⇒ 杜绝篆书字形。
只重做 hero-10 与 hero-12 两张（其余四张已达标·不浪费）。

用法：py -3 scripts/_w929_gen_args_v2.py [out.json]
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _w929_gen_args import ANCHOR, COMP, SPECS, STROKE  # noqa: E402

SEAL = (
    "The only permitted mark is one small cinnabar-red seal impression placed in the upper right "
    "corner of the paper: a perfect square whose width equals its height, four straight parallel "
    "sides, filled with cinnabar red and containing only a few abstract geometric cut-out strokes "
    "that form no characters of any kind, nothing written anywhere in the image."
)

EXCLUDE_V2 = (
    "Strictly excluded: text, Chinese characters, calligraphy, seal-script glyphs, archaic "
    "symbols, letters, digits, logo, signature, watermark, caption, UI elements, close-up faces, "
    "ruled line, horizon line, border, frame, collage, split panels, duplicate objects, busy "
    "clutter. Nothing is written anywhere in the picture."
)

REDO = ["hero-10-mingfu-panwang", "hero-12-jingu-jingangchui"]


def prompt(subject: str) -> str:
    return "%s %s %s %s %s %s" % (subject, ANCHOR, STROKE, COMP, SEAL, EXCLUDE_V2)


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
    out = sys.argv[1] if len(sys.argv) > 1 else "tmpe/_misc/w929_args_v2.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(build(), f, ensure_ascii=False, indent=2)
    print("写出 %s（%d 条·返工 %s）" % (out, len(REDO), "、".join(REDO)))
