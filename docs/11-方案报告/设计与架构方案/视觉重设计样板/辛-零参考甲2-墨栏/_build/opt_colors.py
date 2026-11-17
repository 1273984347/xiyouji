# -*- coding: utf-8 -*-
"""在矿物颜料色相家族内搜索：最大化色盲模拟下的最小两两 ΔE，同时保证图形对比度≥3:1。"""
import importlib.util, itertools, os

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("pc", os.path.join(HERE, "..", "_palette_check.py"))
pc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pc)

SLOTS = ["石青", "赭石", "胭脂", "松绿", "藤黄", "绛紫"]
LIGHT_CAND = [
    ["#2E6C97", "#35739C", "#2A6A96", "#3C7FA8", "#1F6389"],
    ["#A85A16", "#B5641F", "#9C5512", "#BE6C24", "#8F4E10"],
    ["#A83E77", "#C25C93", "#B84A83", "#CC5E95", "#9C3570"],
    ["#2F7355", "#4E9E77", "#357F5E", "#3A8A66", "#235F44"],
    ["#A9800B", "#B98A0E", "#9C7408", "#C09514", "#8E6706"],
    ["#6B4585", "#8B5FAE", "#7A4E96", "#8558A8", "#7E56A0"],
]
DARK_CAND = [
    ["#74AED3", "#86B8DA", "#6BA6CC", "#9AC4E2", "#5E9EC6"],
    ["#D08A3C", "#DB9A52", "#C87F32", "#E0A868", "#B87428"],
    ["#D982AE", "#E294BC", "#CE74A0", "#EBA6C8", "#C26490"],
    ["#5FB08C", "#6CBC9A", "#58A582", "#7FC7A8", "#4C9878"],
    ["#D8B44E", "#E4C468", "#CBA545", "#EED37E", "#BC9638"],
    ["#B294DC", "#C0A6E6", "#A585D0", "#CBB4EC", "#9679C4"],
]

def score(combo, surface):
    worst = 999.0
    for i in range(len(combo)):
        for j in range(i + 1, len(combo)):
            for kind in ("protan", "deutan", "tritan"):
                de = pc.delta_e_cvd(combo[i], combo[j], kind)
                if de < worst:
                    worst = de
    for c in combo:
        if pc.contrast(c, surface) < 3.0:
            return -1.0
    return worst

def search(cands, surface, label):
    best = []
    for combo in itertools.product(*cands):
        s = score(list(combo), surface)
        if s < 0:
            continue
        best.append((s, combo))
    best.sort(key=lambda x: -x[0])
    print("=== %s ===" % label)
    for s, combo in best[:4]:
        det = []
        for i in range(len(combo)):
            for j in range(i + 1, len(combo)):
                for kind in ("protan", "deutan", "tritan"):
                    det.append((pc.delta_e_cvd(combo[i], combo[j], kind), i, j, kind))
        det.sort()
        print("  minΔE %6.2f  弱对: %s/%s(%s) %.1f" % (s, SLOTS[det[0][1]], SLOTS[det[0][2]], det[0][3], det[0][0]))
        print("     " + "  ".join("%s=%s" % (SLOTS[i], c) for i, c in enumerate(combo)))
    return best[0][1]

if __name__ == "__main__":
    lb = search(LIGHT_CAND, "#FFFDF8", "亮态")
    db = search(DARK_CAND, "#28241D", "暗态")
    print()
    print("LIGHT =", list(lb))
    print("DARK  =", list(db))
