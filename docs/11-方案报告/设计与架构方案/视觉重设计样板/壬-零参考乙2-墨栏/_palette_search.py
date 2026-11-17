# -*- coding: utf-8 -*-
"""色板推导：固定颜料色相槽，在约束下逐槽优化明度/彩度。

约束：
  · 亮态：相对亮度 Y <= 0.2583（保证对白底 >= 3:1），Y >= 0.030
  · 暗态：Y >= 0.115（保证对墨底 >= 3:1），Y <= 0.60
  · 目标：最大化「两两 min(常视 ΔE00, protan/deutan/tritan 模拟 ΔE00)」中的最小值
槽位固定为八种传统颜料色相，因此解出的颜色天生在调性内，而不是随机彩虹。

用法：py -3 _palette_search.py
"""
import math

def lin(c):
    c /= 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def enc(c):
    c = max(0.0, min(1.0, c))
    v = 12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055
    return v * 255.0

def luminance(rgb):
    r, g, b = (lin(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def contrast(a, b):
    la, lb = luminance(a), luminance(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)

def lab_of(rgb):
    r, g, b = (lin(c) for c in rgb)
    x = r * 0.4124564 + g * 0.3575761 + b * 0.1804375
    y = r * 0.2126729 + g * 0.7151522 + b * 0.0721750
    z = r * 0.0193339 + g * 0.1191920 + b * 0.9503041
    def f(t):
        return t ** (1 / 3) if t > (6 / 29) ** 3 else t / (3 * (6 / 29) ** 2) + 4 / 29
    fx, fy, fz = f(x / 0.95047), f(y / 1.0), f(z / 1.08883)
    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))

def lab_to_srgb(lab):
    L, a, b = lab
    fy = (L + 16) / 116.0
    fx = fy + a / 500.0
    fz = fy - b / 200.0
    def fi(t):
        return t ** 3 if t > (6 / 29) ** 3 else 3 * (6 / 29) ** 2 * (t - 4 / 29)
    x, y, z = fi(fx) * 0.95047, fi(fy), fi(fz) * 1.08883
    r = x * 3.2404542 + y * -1.5371385 + z * -0.4985314
    g = x * -0.9692660 + y * 1.8760108 + z * 0.0415560
    bb = x * 0.0556434 + y * -0.2040259 + z * 1.0572252
    def gam(c):
        c = max(0.0, min(1.0, c))
        v = 12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055
        return int(round(v * 255))
    return tuple(gam(c) for c in (r, g, bb))

MACHADO = {
    "protan": [[0.152286, 1.052583, -0.204868], [0.114503, 0.786281, 0.099216], [-0.003882, -0.048116, 1.051998]],
    "deutan": [[0.367322, 0.860646, -0.227968], [0.280085, 0.672501, 0.047413], [-0.011820, 0.042940, 0.968881]],
    "tritan": [[1.255528, -0.076749, -0.178779], [-0.078411, 0.930809, 0.147602], [0.004733, 0.691367, 0.303900]],
}

def sim_lab(rgb, kind):
    ls = [lin(c) for c in rgb]
    m = MACHADO[kind]
    return lab_of(tuple(enc(max(0.0, min(1.0, sum(m[i][j] * ls[j] for j in range(3))))) for i in range(3)))

def ciede2000(lab1, lab2):
    l1, a1, b1 = lab1; l2, a2, b2 = lab2
    c1 = math.hypot(a1, b1); c2 = math.hypot(a2, b2)
    cbar = (c1 + c2) / 2.0
    g = 0.5 * (1 - math.sqrt(cbar ** 7 / (cbar ** 7 + 25.0 ** 7)))
    a1p, a2p = (1 + g) * a1, (1 + g) * a2
    c1p, c2p = math.hypot(a1p, b1), math.hypot(a2p, b2)
    h1p = math.degrees(math.atan2(b1, a1p)) % 360 if (a1p or b1) else 0.0
    h2p = math.degrees(math.atan2(b2, a2p)) % 360 if (a2p or b2) else 0.0
    dl, dc = l2 - l1, c2p - c1p
    if c1p * c2p == 0:
        dh = 0.0
    else:
        d = h2p - h1p
        if d > 180: d -= 360
        elif d < -180: d += 360
        dh = d
    dhp = 2 * math.sqrt(c1p * c2p) * math.sin(math.radians(dh) / 2)
    lbp, cbp = (l1 + l2) / 2, (c1p + c2p) / 2
    if c1p * c2p == 0: hbp = h1p + h2p
    elif abs(h1p - h2p) <= 180: hbp = (h1p + h2p) / 2
    elif h1p + h2p < 360: hbp = (h1p + h2p + 360) / 2
    else: hbp = (h1p + h2p - 360) / 2
    t = (1 - 0.17 * math.cos(math.radians(hbp - 30)) + 0.24 * math.cos(math.radians(2 * hbp))
         + 0.32 * math.cos(math.radians(3 * hbp + 6)) - 0.20 * math.cos(math.radians(4 * hbp - 63)))
    dtheta = 30 * math.exp(-(((hbp - 275) / 25) ** 2))
    rc = 2 * math.sqrt(cbp ** 7 / (cbp ** 7 + 25.0 ** 7))
    sl = 1 + (0.015 * (lbp - 50) ** 2) / math.sqrt(20 + (lbp - 50) ** 2)
    sc = 1 + 0.045 * cbp
    sh = 1 + 0.015 * cbp * t
    rt = -math.sin(math.radians(2 * dtheta)) * rc
    return math.sqrt((dl / sl) ** 2 + (dc / sc) ** 2 + (dhp / sh) ** 2 + rt * (dc / sc) * (dhp / sh))

# 名称, Lab 色相角, 彩度上限（矿物颜料的"灰度"上限，避免霓虹感）, 色相容差
SLOTS = [("石青", 258, 40, 10), ("朱砂", 33, 46, 10), ("石绿", 150, 32, 12),
         ("赭黄", 88, 42, 12), ("绛紫", 333, 34, 10), ("青碧", 205, 30, 10),
         ("檀褐", 62, 40, 10)]

def build_slots(ymin, ymax, lrange):
    out = {}
    for name, hue, cmax, htol in SLOTS:
        cands = []
        for L in lrange:
            for C in range(14, cmax + 1, 2):
                for hh in range(hue - htol, hue + htol + 1, 5):
                    a = C * math.cos(math.radians(hh)); b = C * math.sin(math.radians(hh))
                    rgb = lab_to_srgb((L, a, b))
                    y = luminance(rgb)
                    if ymin <= y <= ymax:
                        cands.append(rgb)
        out[name] = sorted(set(cands))
    # 淡墨槽：低彩度中性，靠明度拉开
    neutral = []
    for L in lrange:
        for C in (0, 3, 6, 9):
            a = C * math.cos(math.radians(70)); b = C * math.sin(math.radians(70))
            rgb = lab_to_srgb((L, a, b))
            y = luminance(rgb)
            if ymin <= y <= ymax:
                neutral.append(rgb)
    out["淡墨"] = sorted(set(neutral))
    return out

def spaces(rgb):
    return [lab_of(rgb)] + [sim_lab(rgb, k) for k in ("protan", "deutan", "tritan")]

def dist(p, q):
    """Chebyshev-ish 最小的 Lab 欧氏距离（四个空间取最小）"""
    best = 1e9
    for i in range(4):
        d = math.dist(p[i], q[i])
        if d < best:
            best = d
    return best

def optimize(slots, k=8):
    names = list(slots)
    pre = {n: [(c, spaces(c)) for c in slots[n]] for n in names}
    init = []
    for n in names:
        mid = pre[n][len(pre[n]) // 2]
        init.append(mid)
    cur = list(init)
    def score(sel):
        s = 1e9
        for i in range(len(sel)):
            for j in range(i + 1, len(sel)):
                s = min(s, dist(sel[i][1], sel[j][1]))
        return s
    best = score(cur)
    improved = True
    while improved:
        improved = False
        for i in range(len(cur)):
            bestc, bests = cur[i], best
            for cand in pre[names[i]]:
                trial = list(cur); trial[i] = cand
                s = score(trial)
                if s > bests + 1e-9:
                    bestc, bests = cand, s
            if bests > best + 1e-9:
                cur[i] = bestc; best = bests; improved = True
    return names, cur, best

def report(tag, names, chosen, bg):
    print("\n== %s ==" % tag)
    cols = [c[0] for c in chosen]
    mn = 1e9; mnp = 1e9
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            n = ciede2000(lab_of(cols[i]), lab_of(cols[j]))
            sims = [ciede2000(sim_lab(cols[i], k), sim_lab(cols[j], k)) for k in MACHADO]
            mn = min(mn, n); mnp = min(mnp, min(sims))
    for i, c in enumerate(chosen):
        print("  %-4s #%02X%02X%02X  对底色 %.2f:1" % (names[i], c[0][0], c[0][1], c[0][2], contrast(c[0], bg)))
    print("  常视最小 ΔE00 = %.1f ；色盲模拟最小 ΔE00 = %.1f" % (mn, mnp))

light = build_slots(0.030, 0.2583, range(26, 60, 2))
dark = build_slots(0.16, 0.60, range(48, 87, 2))
for _n, _l in (("亮", light), ("暗", dark)):
    print("候选数 %s态: %s" % (_n, {k: len(v) for k, v in _l.items()}))
light = {k: v for k, v in light.items() if v}
dark = {k: v for k, v in dark.items() if v}
ln, lc, ls_ = optimize(light)
report("亮态序列色（对白底 >= 3:1）", ln, lc, (250, 250, 246))
dn, dc, ds = optimize(dark)
report("暗态序列色（对墨底 >= 3:1）", dn, dc, (26, 29, 33))

# ---------- 暗态：同一批颜料的「灯下版」 ----------
# 色相、彩度不变，明度整体上移 ΔL*，保持颜料性格与两两感知距离；
# 在 [0.16, 0.60] 的亮度带内选 ΔL*，使最暗的一色仍对墨底 >= 3:1。
def pair_min(c1, c2):
    n = ciede2000(lab_of(c1), lab_of(c2))
    sims = [ciede2000(sim_lab(c1, k), sim_lab(c2, k)) for k in MACHADO]
    return n, min(sims)



def pair_table(tag, cols, names):
    print("\n  %s 两两 ΔE00（常视 / 模拟最小）" % tag)
    mn6 = 1e9; mn6s = 1e9; mn8 = 1e9; mn8s = 1e9
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            n, s = pair_min(cols[i], cols[j])
            mn8 = min(mn8, n); mn8s = min(mn8s, s)
            if i < 6 and j < 6:
                mn6 = min(mn6, n); mn6s = min(mn6s, s)
            flag = "" if s >= 8 else "  <8"
            print("    %-4s %-4s 常视 %5.1f | 模拟最小 %5.1f%s" % (names[i], names[j], n, s, flag))
    print("    → 前六色最小：常视 %.1f / 模拟 %.1f ；全八色最小：常视 %.1f / 模拟 %.1f" % (mn6, mn6s, mn8, mn8s))
    return mn6, mn6s, mn8, mn8s

def gamut_fit(lab):
    L, C, H = lab
    a = C * math.cos(math.radians(H)); b = C * math.sin(math.radians(H))
    for _ in range(40):
        rgb = lab_to_srgb((L, a, b))
        ok = all(0 <= v <= 255 for v in rgb)
        if ok:
            return rgb, (L, a, b)
        C *= 0.97
        a = C * math.cos(math.radians(H)); b = C * math.sin(math.radians(H))
    return lab_to_srgb((L, 0, 0)), (L, 0, 0)

def derive_dark(light_chosen):
    labs = []
    for c in light_chosen:
        L, a, b = lab_of(c[0])
        labs.append((L, math.hypot(a, b), math.degrees(math.atan2(b, a)) % 360))
    best = None
    for delta in range(16, 40):
        cand = []
        ok = True
        for (L, C, H) in labs:
            rgb, lab2 = gamut_fit((min(92, L + delta), C, H))
            y = luminance(rgb)
            if y < 0.16 or y > 0.62:
                ok = False
                break
            cand.append((rgb, lab2))
        if not ok:
            continue
        s = 1e9
        for i in range(len(cand)):
            for j in range(i + 1, len(cand)):
                s = min(s, min(pair_min(cand[i][0], cand[j][0])[0], pair_min(cand[i][0], cand[j][0])[1]))
        if best is None or s > best[0]:
            best = (s, delta, cand)
    return best


dark2 = build_slots(0.16, 0.60, range(48, 77, 2))
dn2, dc2, ds2 = optimize(dark2)
print("\n== 暗态候选 B：独立优化（L* 48..76 中亮） ==")
for n, c in zip(dn2, dc2):
    print("  %-4s #%02X%02X%02X  对墨底 %.2f:1" % (n, c[0][0], c[0][1], c[0][2], contrast(c[0], (26, 29, 33))))
pair_table("暗态B", [c[0] for c in dc2], dn2)

dscore, ddelta, dcand = derive_dark(lc)
print("\n== 暗态序列色（亮态颜料整体提亮 ΔL*=%d） ==" % ddelta)
mn = 1e9; mnp = 1e9
for i in range(len(dcand)):
    for j in range(i + 1, len(dcand)):
        n = ciede2000(lab_of(dcand[i][0]), lab_of(dcand[j][0]))
        sims = [ciede2000(sim_lab(dcand[i][0], k), sim_lab(dcand[j][0], k)) for k in MACHADO]
        mn = min(mn, n); mnp = min(mnp, min(sims))
for n, c in zip(ln, dcand):
    print("  %-4s #%02X%02X%02X  对墨底 %.2f:1" % (n, c[0][0], c[0][1], c[0][2], contrast(c[0], (26, 29, 33))))
print("  常视最小 ΔE00 = %.1f ；色盲模拟最小 ΔE00 = %.1f" % (mn, mnp))



pair_table("亮态", [c[0] for c in lc], ln)


# ---------- 暗态朱砂：在「模拟 ΔE >= 8.5」约束内求更鲜明的一档 ----------
# 手改朱砂会与檀褐在 deutan 下收敛，故此处仍由机器求解：目标取彩度上限，
# 约束为与暗态其余七色的最小模拟 ΔE00 >= 8.0（等于判定阈值）。
def tune_zhu_sha(dark_cols, idx):
    others = [c for i, c in enumerate(dark_cols) if i != idx]
    best = None
    for L in range(46, 64, 1):
        for C in range(28, 54, 2):
            for Hh in range(26, 42, 2):
                rgb, lab2 = gamut_fit((L, C, Hh))
                y = luminance(rgb)
                if y < 0.16 or y > 0.50:
                    continue
                worst = min(min(pair_min(rgb, o)[1] for o in others),
                            min(pair_min(rgb, o)[0] for o in others) * 0 + 1e9)
                if worst < 8.0:
                    continue
                vivid = C
                if best is None or vivid > best[0]:
                    best = (vivid, rgb, lab2, worst)
    return best

if dcand:
    cols = [c[0] for c in dcand]
    tb = tune_zhu_sha(cols, 1)
    if tb:
        print("\n== 暗态朱砂求解（约束内取最鲜明） ==")
        print("  #%02X%02X%02X  L*=%.1f C=%.1f  与其余七色最小模拟 ΔE=%.1f  对墨底 %.2f:1"
              % (tb[1][0], tb[1][1], tb[1][2], tb[2][0], tb[0], tb[3], contrast(tb[1], (26, 29, 33))))

print("\n亮态 CSS:")
for n, c in zip(ln, lc):
    print("  --series-%s : #%02X%02X%02X" % ({"石青": 1, "朱砂": 2, "石绿": 3, "赭黄": 4, "绛紫": 5, "青碧": 6, "檀褐": 7, "淡墨": 8}[n], c[0][0], c[0][1], c[0][2]))
print("暗态 CSS:")
for n, c in zip(ln, dcand):
    print("  --series-%s : #%02X%02X%02X" % ({"石青": 1, "朱砂": 2, "石绿": 3, "赭黄": 4, "绛紫": 5, "青碧": 6, "檀褐": 7, "淡墨": 8}[n], c[0][0], c[0][1], c[0][2]))
