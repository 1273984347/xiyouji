# -*- coding: utf-8 -*-
"""色板机器复算：WCAG 对比度 + Machado 色盲模拟 + CIEDE2000 ΔE。

判定口径（阈值是本设计自己定的，写在这里以便复核）：
  · 正文类令牌（文本/语义/强调文字）对各自底色 >= 4.5:1
  · 图形类令牌（序列色/控件边框/强调色）对各自底色 >= 3:1
  · 序列色两两 ΔE00：常视 >= 12；protan/deutan/tritan 模拟后 >= 8
    （阈值 12 而非 15 的理由：8 色序列全部要在近白底 >= 3:1，亮度带被压到 L* 27-58，实测上限约 14）
  · 明暗两块暗态令牌集与值逐项相等（与 _audit.py 互为交叉验证）

用法：py -3 _palette_check.py
"""
import math
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
TOKENS = (ROOT / "tokens.css").read_text(encoding="utf-8")

FAILURES = []
CHECKS = 0


def check(label, ok, detail=""):
    global CHECKS
    CHECKS += 1
    tag = "PASS" if ok else "FAIL"
    line = "[%s] %-46s %s" % (tag, label, detail)
    print(line)
    if not ok:
        FAILURES.append(label)
    return ok


# ---------- CSS 解析 ----------
def block_after(css, marker):
    i = css.index(marker)
    j = css.index("{", i)
    depth = 0
    for k in range(j, len(css)):
        if css[k] == "{":
            depth += 1
        elif css[k] == "}":
            depth -= 1
            if depth == 0:
                return css[j + 1:k]
    raise ValueError("未闭合的块: " + marker)


def parse_decls(text):
    text = re.sub(r"/\*.*?\*/", " ", text, flags=re.S)
    out = {}
    for part in text.split(";"):
        if ":" not in part:
            continue
        name, value = part.split(":", 1)
        name = name.strip()
        if name.startswith("--"):
            out[name] = value.strip()
    return out


LIGHT = parse_decls(block_after(TOKENS, ":root {"))
DARK_ATTR = parse_decls(block_after(TOKENS, ':root[data-theme="dark"] {'))
DARK_MEDIA = parse_decls(block_after(TOKENS, ':root:not([data-theme="light"]) {'))


# ---------- 颜色数学 ----------
def parse_hex(value):
    v = value.strip()
    m = re.fullmatch(r"#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})", v)
    if not m:
        return None
    h = m.group(1)
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def to_linear(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def to_srgb(c):
    c = max(0.0, min(1.0, c))
    v = 12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055
    return v * 255.0


def luminance(rgb):
    r, g, b = (to_linear(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def srgb_to_lab(rgb):
    r, g, b = (to_linear(c) for c in rgb)
    x = r * 0.4124564 + g * 0.3575761 + b * 0.1804375
    y = r * 0.2126729 + g * 0.7151522 + b * 0.0721750
    z = r * 0.0193339 + g * 0.1191920 + b * 0.9503041

    def f(t):
        return t ** (1 / 3) if t > (6 / 29) ** 3 else t / (3 * (6 / 29) ** 2) + 4 / 29

    fx, fy, fz = f(x / 0.95047), f(y / 1.0), f(z / 1.08883)
    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))


def ciede2000(lab1, lab2):
    l1, a1, b1 = lab1
    l2, a2, b2 = lab2
    c1 = math.hypot(a1, b1)
    c2 = math.hypot(a2, b2)
    cbar = (c1 + c2) / 2.0
    g = 0.5 * (1 - math.sqrt(cbar ** 7 / (cbar ** 7 + 25.0 ** 7)))
    a1p, a2p = (1 + g) * a1, (1 + g) * a2
    c1p, c2p = math.hypot(a1p, b1), math.hypot(a2p, b2)
    h1p = math.degrees(math.atan2(b1, a1p)) % 360 if (a1p or b1) else 0.0
    h2p = math.degrees(math.atan2(b2, a2p)) % 360 if (a2p or b2) else 0.0
    dl = l2 - l1
    dc = c2p - c1p
    if c1p * c2p == 0:
        dh = 0.0
    else:
        d = h2p - h1p
        if d > 180:
            d -= 360
        elif d < -180:
            d += 360
        dh = d
    dhp = 2 * math.sqrt(c1p * c2p) * math.sin(math.radians(dh) / 2)
    lbp = (l1 + l2) / 2
    cbp = (c1p + c2p) / 2
    if c1p * c2p == 0:
        hbp = h1p + h2p
    elif abs(h1p - h2p) <= 180:
        hbp = (h1p + h2p) / 2
    elif h1p + h2p < 360:
        hbp = (h1p + h2p + 360) / 2
    else:
        hbp = (h1p + h2p - 360) / 2
    t = (1 - 0.17 * math.cos(math.radians(hbp - 30)) + 0.24 * math.cos(math.radians(2 * hbp))
         + 0.32 * math.cos(math.radians(3 * hbp + 6)) - 0.20 * math.cos(math.radians(4 * hbp - 63)))
    dtheta = 30 * math.exp(-(((hbp - 275) / 25) ** 2))
    rc = 2 * math.sqrt(cbp ** 7 / (cbp ** 7 + 25.0 ** 7))
    sl = 1 + (0.015 * (lbp - 50) ** 2) / math.sqrt(20 + (lbp - 50) ** 2)
    sc = 1 + 0.045 * cbp
    sh = 1 + 0.015 * cbp * t
    rt = -math.sin(math.radians(2 * dtheta)) * rc
    return math.sqrt((dl / sl) ** 2 + (dc / sc) ** 2 + (dhp / sh) ** 2 + rt * (dc / sc) * (dhp / sh))


MACHADO = {
    "protan": [[0.152286, 1.052583, -0.204868],
               [0.114503, 0.786281, 0.099216],
               [-0.003882, -0.048116, 1.051998]],
    "deutan": [[0.367322, 0.860646, -0.227968],
               [0.280085, 0.672501, 0.047413],
               [-0.011820, 0.042940, 0.968881]],
    "tritan": [[1.255528, -0.076749, -0.178779],
               [-0.078411, 0.930809, 0.147602],
               [0.004733, 0.691367, 0.303900]],
}


def simulate(rgb, kind):
    lin = [to_linear(c) for c in rgb]
    m = MACHADO[kind]
    out = []
    for i in range(3):
        v = sum(m[i][j] * lin[j] for j in range(3))
        out.append(to_srgb(max(0.0, min(1.0, v))))
    return tuple(out)


# ---------- 1. 明暗两块暗态令牌集与值逐项相等 ----------
check("暗态令牌集：属性选择器 vs 媒体查询 数量一致",
      len(DARK_ATTR) == len(DARK_MEDIA),
      "%d vs %d" % (len(DARK_ATTR), len(DARK_MEDIA)))
diff = [k for k in DARK_ATTR if DARK_ATTR.get(k) != DARK_MEDIA.get(k)]
check("暗态令牌值：两块逐项相等", not diff, "不一致：%s" % (", ".join(diff[:5]) if diff else "无"))

# ---------- 2. 文本对比度 ----------
TEXT_ON_PAPER = ["--text-primary", "--text-secondary", "--text-tertiary", "--ink", "--ink-soft",
                 "--ink-faint", "--text-hero", "--accent-text", "--ok", "--warn", "--info",
                 "--danger", "--status-neg", "--rebel"]
for theme, block in (("亮态", LIGHT), ("暗态", DARK_ATTR)):
    paper = parse_hex(block["--paper"])
    raised = parse_hex(block["--surface-raised"])
    worst = None
    for name in TEXT_ON_PAPER:
        c = parse_hex(block[name])
        ratio = contrast(c, paper)
        if worst is None or ratio < worst[1]:
            worst = (name, ratio)
        check("%s · 文本 %s 对纸面 >= 4.5:1" % (theme, name), ratio >= 4.5, "%.2f:1" % ratio)
    print("       └ %s 正文最小对比度: %s %.2f:1" % (theme, worst[0], worst[1]))
    ink_inv = parse_hex(block["--text-inverse"])
    dark_bg = parse_hex(block["--dark"])
    r1 = contrast(ink_inv, dark_bg)
    check("%s · 深底反白文字 >= 4.5:1" % theme, r1 >= 4.5, "%.2f:1" % r1)
    r2 = contrast(parse_hex(block["--dark-text"]), dark_bg)
    check("%s · 拓片段文字 >= 4.5:1" % theme, r2 >= 4.5, "%.2f:1" % r2)

# ---------- 3. 图形/控件对比度 >= 3:1 ----------
GRAPHICS = ["--accent", "--accent-deep", "--border-accent", "--ink-faint",
            "--chart-1", "--chart-2", "--chart-3", "--chart-4", "--chart-5", "--chart-6"]
for theme, block in (("亮态", LIGHT), ("暗态", DARK_ATTR)):
    for bg_name in ("--paper", "--surface-raised"):
        bg = parse_hex(block[bg_name])
        for name in GRAPHICS:
            c = parse_hex(block[name])
            ratio = contrast(c, bg)
            check("%s · 图形 %s 对 %s >= 3:1" % (theme, name, bg_name), ratio >= 3.0, "%.2f:1" % ratio)

# ---------- 4. 序列色两两 ΔE（常视 + 三种色盲模拟） ----------
def series_pairs(block):
    names = ["--series-%d" % i for i in range(1, 9)]
    cols = [parse_hex(block[n]) for n in names]
    out = []
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            out.append((names[i], names[j], cols[i], cols[j]))
    return out


for theme, block in (("亮态", LIGHT), ("暗态", DARK_ATTR)):
    pairs = series_pairs(block)
    min_norm = (None, 1e9)
    min_sim = (None, 1e9)
    for n1, n2, c1, c2 in pairs:
        d = ciede2000(srgb_to_lab(c1), srgb_to_lab(c2))
        if d < min_norm[1]:
            min_norm = ("%s/%s" % (n1, n2), d)
        for kind in ("protan", "deutan", "tritan"):
            ds = ciede2000(srgb_to_lab(simulate(c1, kind)), srgb_to_lab(simulate(c2, kind)))
            if ds < min_sim[1]:
                min_sim = ("%s/%s(%s)" % (n1, n2, kind), ds)
    check("%s · 序列色常视 ΔE00 最小 >= 12" % theme, min_norm[1] >= 12,
          "%s ΔE=%.1f" % (min_norm[0], min_norm[1]))
    check("%s · 序列色色盲模拟 ΔE00 最小 >= 8" % theme, min_sim[1] >= 8,
          "%s ΔE=%.1f" % (min_sim[0], min_sim[1]))

# ---------- 5. 序列色两两明细（留痕） ----------
print("\n  序列色明细（两两 ΔE00，常视 / protan / deutan / tritan）")
for theme, block in (("亮态", LIGHT), ("暗态", DARK_ATTR)):
    print("  ── %s ──" % theme)
    pairs = series_pairs(block)
    for n1, n2, c1, c2 in pairs:
        d = ciede2000(srgb_to_lab(c1), srgb_to_lab(c2))
        sims = [ciede2000(srgb_to_lab(simulate(c1, k)), srgb_to_lab(simulate(c2, k)))
                for k in ("protan", "deutan", "tritan")]
        flag = "" if (d >= 12 and min(sims) >= 8) else "  <-- 未达标"
        print("    %-12s %-12s 常视 %5.1f | P %5.1f  D %5.1f  T %5.1f%s"
              % (n1, n2, d, sims[0], sims[1], sims[2], flag))

print("\n共 %d 项检查，失败 %d 项" % (CHECKS, len(FAILURES)))
if FAILURES:
    print("RESULT: FAIL")
    for f in FAILURES:
        print("  - " + f)
    sys.exit(1)
print("RESULT: PASS")
