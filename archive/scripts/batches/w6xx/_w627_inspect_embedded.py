#!/usr/bin/env python3
"""W627 取证：EN EMBEDDED（_w627_extract_embedded.js 产出）对部署 JSON（zh）的覆盖度盘点。只读。"""
import json
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"D:\xiyouji"
CJK = re.compile(r"[\u4e00-\u9fff]")


def long_fields(o, path=""):
    out = {}
    if isinstance(o, dict):
        for k, v in o.items():
            out.update(long_fields(v, f"{path}.{k}"))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            out.update(long_fields(v, f"{path}[{i}]"))
    elif isinstance(o, str) and len(o) > 8:
        out[path] = o
    return out


emb_all = json.load(open(ROOT + r"\scripts\output\_w627_embedded_en.json", encoding="utf-8"))
PAIRS = [
    ("villain_matrix", "villain_matrix.json", emb_all["methodology"]),
    ("rescue_roi", "rescue_roi.json", emb_all["methodology"]),
    ("methodology_summary", "methodology_summary.json", emb_all["methodology"]),
    ("monster_clock", "monster_clock.json", emb_all["chart"]),
    ("chart_design_summary", "chart_design_summary.json", emb_all["chart"]),
]
for name, zh_file, emb_src in PAIRS:
    zh = json.load(open(ROOT + r"\site\data\json" + "\\" + zh_file, encoding="utf-8"))
    zh_lf = long_fields(zh)
    emb = emb_src.get(name)
    emb_lf = long_fields(emb) if emb is not None else {}
    hit = miss = 0
    misses = []
    for p, v in zh_lf.items():
        ev = emb_lf.get(p)
        if ev is not None and not CJK.search(ev):
            hit += 1
        else:
            miss += 1
            misses.append(p)
    print(f"== {name}: zh长文本={len(zh_lf)} EN命中={hit} 未命中={miss}")
    if misses:
        print(f"   未命中: {misses[:10]}")
