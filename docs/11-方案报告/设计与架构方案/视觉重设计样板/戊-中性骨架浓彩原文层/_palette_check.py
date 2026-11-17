# -*- coding: utf-8 -*-
"""W1262 palette engineering: WCAG contrast + colorblind simulation (Machado 2009).

Outputs markdown tables for SPEC.md and lists failing pairs so hex values can be
iterated. Pure stdlib.
"""
import itertools

# ---------------------------------------------------------------- sRGB / WCAG
def _lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def luminance(hexc):
    hexc = hexc.lstrip('#')
    r, g, b = (int(hexc[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)

def contrast(fg, bg):
    l1, l2 = sorted((luminance(fg), luminance(bg)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)

# ------------------------------------------------------- colorblind simulation
# Machado, Oliveira & Fernandes 2009, severity 1.0 matrices (sRGB linear space)
CB_MATS = {
    'protan': (
        0.152286, 1.052583, -0.204868,
        0.114503, 0.786281,  0.099216,
       -0.003882,-0.048116,  1.051998),
    'deutan': (
        0.367322, 0.860646, -0.227968,
        0.280085, 0.672501,  0.047413,
       -0.011820, 0.042940,  0.968881),
    'tritan': (
        1.255528,-0.076749, -0.178779,
       -0.078411, 0.930809,  0.147602,
        0.004733, 0.691367,  0.303900),
}

def _gam(c):
    return 12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055

def _to_xyz_linear(hexc):
    hexc = hexc.lstrip('#')
    r, g, b = (int(hexc[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    return _lin(r), _lin(g), _lin(b)

def simulate(hexc, kind):
    m = CB_MATS[kind]
    r, g, b = _to_xyz_linear(hexc)
    nr = m[0]*r + m[1]*g + m[2]*b
    ng = m[3]*r + m[4]*g + m[5]*b
    nb = m[6]*r + m[7]*g + m[8]*b
    return tuple(min(1.0, max(0.0, _gam(v))) for v in (nr, ng, nb))

def _lab_from_rgb01(rgb):
    # sRGB D65 -> Lab
    r, g, b = rgb
    def f(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = f(r), f(g), f(b)
    X = 0.4124564*r + 0.3575761*g + 0.1804375*b
    Y = 0.2126729*r + 0.7151522*g + 0.0721750*b
    Z = 0.0193339*r + 0.1191920*g + 0.9503041*b
    Xn, Yn, Zn = 0.95047, 1.00000, 1.08883
    def g2(t):
        return t ** (1/3) if t > 0.008856 else (7.787 * t + 16/116)
    fx, fy, fz = g2(X/Xn), g2(Y/Yn), g2(Z/Zn)
    return 116*fy - 16, 500*(fx - fy), 200*(fy - fz)

def delta_e(rgb1, rgb2):
    l1 = _lab_from_rgb01(rgb1)
    l2 = _lab_from_rgb01(rgb2)
    return (sum((a-b)**2 for a, b in zip(l1, l2))) ** 0.5

def cb_min_delta(colors):
    worst = {}
    for kind in CB_MATS:
        sims = [simulate(c, kind) for c in colors]
        mn = min(delta_e(a, b) for a, b in itertools.combinations(sims, 2))
        worst[kind] = mn
    return worst

# ---------------------------------------------------------------- the palette
# name: (light, dark)
P = {
    # surfaces — v3 Route C: light = R1 neutral gallery wall, dark = warm grotto ground
    'bg':              ('#F2F1EE', '#151110'),
    'paper':           ('#FBFAF7', '#1E1813'),
    'paper-warm':      ('#F1EEE8', '#241D16'),
    'surface-canvas':  ('#FBFAF7', '#191410'),
    'surface-raised':  ('#FFFEFB', '#2A2119'),
    'surface-sunken':  ('#EAE7E1', '#0F0B08'),
    'surface-inset':   ('#E4E1DA', '#0B0806'),
    'dark':            ('#211E19', '#0C0906'),
    'dark-text':       ('#F0EDE6', '#F2EBDC'),
    'text-inverse':    ('#FFF8F5', '#1E0F08'),
    # text — neutral cool ink (light) / warm paper text on grotto (dark)
    'ink':             ('#26231D', '#F1E9D8'),
    'ink-soft':        ('#57534A', '#B5AA97'),
    'ink-faint':       ('#6F6A60', '#968C7A'),
    'accent-text':     ('#B03A20', '#F07150'),
    # accent (graphics)
    'accent':          ('#BF4127', '#E8654A'),
    'accent-deep':     ('#9C321D', '#F07E60'),
    # states (text-safe)
    'ok':              ('#2E7D5B', '#5FB78D'),
    'warn':            ('#8A5F14', '#D3A54E'),
    'info':            ('#2E6695', '#6FA9DB'),
    'danger':          ('#A62218', '#E97067'),
    'rebel':           ('#8A5F14', '#D8A85A'),
    # data series (8) — 国画颜料谱, values unchanged across all three rounds (CB ladder preserved)
    'series-1':        ('#BF4127', '#E8654A'),  # 朱砂
    'series-2':        ('#386D94', '#82AFD0'),  # 石青
    'series-3':        ('#B2872F', '#D7B167'),  # 石黄
    'series-4':        ('#255C49', '#56B796'),  # 石绿
    'series-5':        ('#A65B80', '#D5B0C3'),  # 胭脂
    'series-6':        ('#4991B3', '#CCE0EA'),  # 青金
    'series-7':        ('#4C3A27', '#846342'),  # 赭石
    'series-8':        ('#3F4A56', '#8697A7'),  # 墨灰
}

LIGHT_BG = 'paper'   # text-bearing card surface
LIGHT_PAGE = 'bg'
DARK_BG = 'paper'
DARK_PAGE = 'bg'

PAIRS = [
    # (label, fg, bg, min_ratio)
    ('L ink / paper (body)',          'ink', 'paper', 4.5),
    ('L ink / bg (body)',             'ink', 'bg', 4.5),
    ('L ink-soft / paper',            'ink-soft', 'paper', 4.5),
    ('L ink-soft / bg',               'ink-soft', 'bg', 4.5),
    ('L ink-faint / paper',           'ink-faint', 'paper', 4.5),
    ('L ink-faint / bg',              'ink-faint', 'bg', 4.5),
    ('L accent-text / paper (links)', 'accent-text', 'paper', 4.5),
    ('L accent-text / bg',            'accent-text', 'bg', 4.5),
    ('L accent / paper (graphic)',    'accent', 'paper', 3.0),
    ('L text-inverse / accent (btn)', '#FFF8F5', 'accent', 4.5),
    ('L dark-text / dark',            'dark-text', 'dark', 4.5),
    ('L ok / paper',                  'ok', 'paper', 4.5),
    ('L warn / paper',                'warn', 'paper', 4.5),
    ('L info / paper',                'info', 'paper', 4.5),
    ('L danger / paper',              'danger', 'paper', 4.5),
    ('L rebel / paper',               'rebel', 'paper', 4.5),
    ('L series-1 / canvas',           'series-1', 'surface-canvas', 3.0),
    ('L series-2 / canvas',           'series-2', 'surface-canvas', 3.0),
    ('L series-3 / canvas',           'series-3', 'surface-canvas', 3.0),
    ('L series-4 / canvas',           'series-4', 'surface-canvas', 3.0),
    ('L series-5 / canvas',           'series-5', 'surface-canvas', 3.0),
    ('L series-6 / canvas',           'series-6', 'surface-canvas', 3.0),
    ('L series-7 / canvas',           'series-7', 'surface-canvas', 3.0),
    ('L series-8 / canvas',           'series-8', 'surface-canvas', 3.0),
    ('D ink / paper (body)',          'ink', 'paper', 4.5),
    ('D ink / bg (body)',             'ink', 'bg', 4.5),
    ('D ink-soft / paper',            'ink-soft', 'paper', 4.5),
    ('D ink-soft / bg',               'ink-soft', 'bg', 4.5),
    ('D ink-faint / paper',           'ink-faint', 'paper', 4.5),
    ('D ink-faint / bg',              'ink-faint', 'bg', 4.5),
    ('D accent-text / paper (links)', 'accent-text', 'paper', 4.5),
    ('D accent-text / bg',            'accent-text', 'bg', 4.5),
    ('D accent / paper (graphic)',    'accent', 'paper', 3.0),
    ('D dark-text / dark',            'dark-text', 'dark', 4.5),
    ('D text-inverse / accent (btn)', 'text-inverse', 'accent', 4.5),
    ('D ok / paper',                  'ok', 'paper', 4.5),
    ('D warn / paper',                'warn', 'paper', 4.5),
    ('D info / paper',                'info', 'paper', 4.5),
    ('D danger / paper',              'danger', 'paper', 4.5),
    ('D rebel / paper',               'rebel', 'paper', 4.5),
    ('D series-1 / canvas',           'series-1', 'surface-canvas', 3.0),
    ('D series-2 / canvas',           'series-2', 'surface-canvas', 3.0),
    ('D series-3 / canvas',           'series-3', 'surface-canvas', 3.0),
    ('D series-4 / canvas',           'series-4', 'surface-canvas', 3.0),
    ('D series-5 / canvas',           'series-5', 'surface-canvas', 3.0),
    ('D series-6 / canvas',           'series-6', 'surface-canvas', 3.0),
    ('D series-7 / canvas',           'series-7', 'surface-canvas', 3.0),
    ('D series-8 / canvas',           'series-8', 'surface-canvas', 3.0),
]

def value(key, dark=False):
    v = P[key]
    return v[1] if dark else v[0]

def resolve(tok):
    return value(tok, tok in DARK_CTX) if tok in P else tok

DARK_CTX = set()  # filled per pair below

def main():
    failures = []
    rows = []
    for label, fg, bg, mn in PAIRS:
        dark = label.startswith('D ')
        DARK_CTX.clear()
        if dark:
            # which tokens should resolve to dark values
            DARK_CTX.update(P.keys())
        fgv, bgv = resolve(fg), resolve(bg)
        r = contrast(fgv, bgv)
        ok = r >= mn
        rows.append((label, fgv, bgv, r, mn, ok))
        if not ok:
            failures.append((label, fgv, bgv, r, mn))

    # colorblind report for both series sets
    light_series = [value(f'series-{i}', False) for i in range(1, 9)]
    dark_series = [value(f'series-{i}', True) for i in range(1, 9)]
    cb_light = cb_min_delta(light_series)
    cb_dark = cb_min_delta(dark_series)

    print('| 对 | 前景 | 背景 | 对比度 | 要求 | 判定 |')
    print('|---|---|---|---|---|---|')
    for label, fgv, bgv, r, mn, ok in rows:
        print(f'| {label} | `{fgv}` | `{bgv}` | {r:.2f} | ≥{mn} | {"PASS" if ok else "**FAIL**"} |')
    print()
    print('Series colorblind min pairwise ΔE (CIE76):')
    print(f'  light: protan {cb_light["protan"]:.1f}  deutan {cb_light["deutan"]:.1f}  tritan {cb_light["tritan"]:.1f}')
    print(f'  dark : protan {cb_dark["protan"]:.1f}  deutan {cb_dark["deutan"]:.1f}  tritan {cb_dark["tritan"]:.1f}')
    print()
    if failures:
        print('FAILURES:')
        for label, fgv, bgv, r, mn in failures:
            print(f'  {label}: {fgv} on {bgv} = {r:.2f} (< {mn})')
    else:
        print('ALL CONTRAST PAIRS PASS')

    # per-series lightness listing to verify deliberate lightness spacing
    print()
    print('series lightness (L*):')
    for i in range(1, 9):
        c = value(f'series-{i}', False)
        L = _lab_from_rgb01(simulate(c, 'protan'))[0]
        L0 = _lab_from_rgb01(_to_xyz_linear(c))[0]
        print(f'  series-{i} {c}  L*={L0:.1f}  protan-L*={L:.1f}')

def _hsl_to_hex(h, s, l):
    """h 0-360, s/l 0-1 -> hex."""
    def f(n):
        k = (n + h / 30) % 12
        a = s * min(l, 1 - l)
        v = l - a * max(-1, min(k - 3, 9 - k, 1))
        return round(v * 255)
    return '#{:02X}{:02X}{:02X}'.format(f(0), f(8), f(4))

HUE_SAT = {  # hue, saturation per series family (Okabe-Ito derived hues)
    1: (18, 0.58),   # vermilion (accent anchor, fixed)
    2: (205, 0.45),  # indigo blue
    3: (40, 0.58),   # amber
    4: (160, 0.42),  # celadon green
    5: (330, 0.30),  # plum
    6: (199, 0.42),  # stream blue
    7: (30, 0.33),   # umber
    8: (210, 0.16),  # slate
}

def lab_L_of(hexc):
    r, g, b = (int(hexc.lstrip('#')[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    return _lab_from_rgb01((r, g, b))[0]

def hex_at_L(h, s, target_L):
    """Binary-search HSL lightness to hit a target CIE L* for hue h, sat s."""
    lo, hi = 0.0, 1.0
    for _ in range(40):
        mid = (lo + hi) / 2
        L = lab_L_of(_hsl_to_hex(h, s, mid))
        if L < target_L:
            lo = mid
        else:
            hi = mid
    return _hsl_to_hex(h, s, (lo + hi) / 2)

def build_series(targets, sats):
    return {i: hex_at_L(HUE_SAT[i][0], sats[i], targets[i]) for i in targets}

LIGHT_TARGETS = {1: 45, 2: 40, 3: 58, 4: 36, 5: 48, 6: 57, 7: 26, 8: 31}
LIGHT_SATS = {1: 0.58, 2: 0.45, 3: 0.55, 4: 0.42, 5: 0.30, 6: 0.42, 7: 0.33, 8: 0.16}
DARK_TARGETS = {1: 62, 2: 72, 3: 74, 4: 68, 5: 78, 6: 84, 7: 52, 8: 64}
DARK_SATS = {1: 0.58, 2: 0.44, 3: 0.55, 4: 0.40, 5: 0.32, 6: 0.42, 7: 0.33, 8: 0.16}
ANCHORS = {False: '#BF4127', True: '#E8654A'}  # series-1 fixed (accent)

def series_set(dark):
    targets = dict(DARK_TARGETS if dark else LIGHT_TARGETS)
    sats = dict(DARK_SATS if dark else LIGHT_SATS)
    cols = {i: (ANCHORS[dark] if i == 1 else hex_at_L(HUE_SAT[i][0], sats[i], targets[i])) for i in range(1, 9)}
    return cols, targets

def obj(cols):
    keys = sorted(cols)
    mn = 1e9
    for kind in CB_MATS:
        sims = [simulate(cols[k], kind) for k in keys]
        for a, b in itertools.combinations(sims, 2):
            mn = min(mn, delta_e(a, b))
    return mn

def climb(cols, dark, bounds=(26, 60), passes=30, step=1.0):
    cols = dict(cols)
    for _ in range(passes):
        improved = False
        for i in range(2, 9):
            base = obj(cols)
            h, s = HUE_SAT[i]
            cur_L = lab_L_of(cols[i])
            for d in (step, -step):
                nl = min(bounds[1], max(bounds[0], cur_L + d))
                cand = dict(cols)
                cand[i] = hex_at_L(h, s, nl)
                if obj(cand) > base + 1e-6:
                    cols = cand
                    improved = True
                    break
        if not improved:
            break
    return cols

def report(cols, bg, name):
    keys = sorted(cols)
    for i in keys:
        c = cols[i]
        print(f'  s{i}: {c}  L*={lab_L_of(c):.1f}  contrast={contrast(c, bg):.2f}')
    for kind in CB_MATS:
        sims = [simulate(cols[k], kind) for k in keys]
        mn, pair = 1e9, None
        for k1, k2 in itertools.combinations(keys, 2):
            d = delta_e(sims[k1 - 1], sims[k2 - 1])
            if d < mn:
                mn, pair = d, (k1, k2)
        print(f'  {name} {kind} min dE = {mn:.1f} (s{pair[0]} vs s{pair[1]})')
    print(f'  {name} WORST min dE = {obj(cols):.1f}')

if __name__ == '__main__':
    import sys
    if '--series' in sys.argv:
        for dark, bg, name, bounds in ((False, '#FBFAF7', 'LIGHT', (26, 60)), (True, '#181613', 'DARK', (44, 88))):
            cols, _ = series_set(dark)
            cols = climb(cols, dark, bounds=bounds)
            print(f'{name} series (after climb):')
            report(cols, bg, name)
            print()
        sys.exit(0)
    main()

if __name__ == '__main__':
    import sys
    if '--series' in sys.argv:
        for name, targets, sats, bg in (
            ('LIGHT', LIGHT_TARGETS, LIGHT_SATS, '#FBFAF7'),
            ('DARK', DARK_TARGETS, DARK_SATS, '#181613'),
        ):
            print(f'{name} series:')
            cols = build_series(targets, sats)
            for i in sorted(cols):
                c = cols[i]
                print(f'  s{i}: {c}  L*={lab_L_of(c):.1f}  contrast-vs-canvas={contrast(c, bg):.2f}')
            keys = sorted(cols)
            for kind in CB_MATS:
                sims = [simulate(cols[k], kind) for k in keys]
                mn = min(delta_e(a, b) for a, b in itertools.combinations(sims, 2))
                pair = min(
                    ((k1, k2) for k1, k2 in itertools.combinations(keys, 2)
                     if abs(delta_e(simulate(cols[k1], kind), simulate(cols[k2], kind)) - mn) < 1e-9)
                )
                print(f'  {name} {kind} min dE = {mn:.1f} (s{pair[0]} vs s{pair[1]})')
        sys.exit(0)
    main()
