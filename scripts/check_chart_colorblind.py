#!/usr/bin/env python3
"""check_chart_colorblind.py — 第 29 门禁 · 图表配色色盲安全（PD-1a · W653）

判据（D-6 裁决：WARN+基线冻结·基线外新增即 FAIL；D-5 裁决：只扫 site/data 87 页）：
  ① 二型色觉模拟：Machado et al. 2009 deuteranopia / protanopia（sRGB 线性域矩阵·severity 1.0）
  ② 页内数据色板两两求 CIEDE2000 ΔE：min(ΔE_deuter, ΔE_protan) < 10 判违规（红绿混淆典型阈值）
  ③ 色板口径：赋值语境色（fill/stroke/color 的 attr/style/css 赋值）∪ var(--chart-*/--accent*) 解析
     ∪ d3.scheme* 内置色板；中性色（RGB 通道差 <24 或 L* 极端）与渐变 stop（装饰）不入对

口径偏差（已记 W653 CHANGELOG·计划风险条目的规避）：
  静态解析限定 **light 主题真值**（源码字面 + var(--x) 对 tokens.css light 解析）。
  暗色 computed 态的色盲检查需 http 渲染（W589 口径），归 PD-4 异常态矩阵，本门禁不覆盖。

豁免（W589 登记 semantics）：
  - 页含 scaleLinear/scaleSequential/scaleSqrt/interpolate*（连续色阶）→ 页级豁免 data-driven-scale
  - fill="none" / 渐变 stop / 中性色 / 纯白黑 → 不入对

用法：
  python scripts/check_chart_colorblind.py --survey            # 形态普查 → colorblind-survey.json
  python scripts/check_chart_colorblind.py --report            # 全量报告（不判退出码）
  python scripts/check_chart_colorblind.py --generate-baseline # 冻结存量（colorblind-baseline.txt）
  python scripts/check_chart_colorblind.py --gate              # 门禁模式（verify_delivery 调用）
  python scripts/check_chart_colorblind.py --self-test         # 4 例构造页自检
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from export_design_tokens import parse_css  # noqa: E402

SITE_DATA = ROOT / "site" / "data"
TOKENS_CSS = ROOT / "site" / "tokens.css"
BASELINE = ROOT / "scripts" / "output" / "colorblind-baseline.txt"
SURVEY = ROOT / "scripts" / "output" / "colorblind-survey.json"
SKIP_STEMS = ("_shell", "_template")
THRESHOLD = 10.0

# ---- Machado et al. 2009（severity 1.0·sRGB 线性域）----
SIM_MATRICES = {
    "deuter": (
        (0.367322, 0.860646, -0.227968),
        (0.280085, 0.672501, 0.047413),
        (-0.011820, 0.042940, 0.968881),
    ),
    "protan": (
        (0.152286, 1.052583, -0.204868),
        (0.114503, 0.786281, 0.099216),
        (-0.003882, -0.048116, 1.051998),
    ),
}

# d3 内置分类色板（普查覆盖的 scheme 名 → hex 列表）
D3_SCHEMES = {
    "Category10": ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c5642", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"],
    "Tableau10": ["#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f", "#edc948", "#b07aa1", "#ff9da7", "#9c755f", "#bab0ac"],
    "Set1": ["#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00", "#ffff33", "#a65628", "#f781bf", "#999999"],
    "Set2": ["#66c2a5", "#fc8d62", "#8da0cb", "#e78ac3", "#a6d854", "#ffd92f", "#e5c494", "#b3b3b3"],
    "Set3": ["#8dd3c7", "#ffffb3", "#bebada", "#fb8072", "#80b1d3", "#fdb462", "#b3de69", "#fccde5", "#d9d9d9", "#bc80bd", "#ccebc5", "#ffed6f"],
}

RE_HEX = re.compile(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b")
RE_RGB = re.compile(r"rgba?\(\s*([\d.]+)[,\s]+([\d.]+)[,\s]+([\d.]+)(?:[,\s]+([\d.]+))?\s*\)")
RE_HSL = re.compile(r"hsla?\(([^)]+)\)")
RE_VAR = re.compile(r"var\(\s*(--[\w-]+)\s*\)")
RE_SCHEME = re.compile(r"d3\.scheme(\w+)")
RE_ASSIGN = re.compile(
    r"""(?:fill|stroke|color)\s*[:=]\s*["']?\s*((?:#[0-9a-fA-F]{3,8})|(?:rgba?\([^)]*\))|(?:var\(--[\w-]+\)))"""
    r"""|["'](?:fill|stroke|color)["']\s*,\s*["']?\s*((?:#[0-9a-fA-F]{3,8})|(?:rgba?\([^)]*\))|(?:var\(--[\w-]+\)))"""
)
RE_FS_ASSIGN = re.compile(
    r"""(?:fill|stroke)\s*[:=]\s*["']?\s*((?:#[0-9a-fA-F]{3,8})|(?:rgba?\([^)]*\))|(?:var\(--[\w-]+\)))"""
    r"""|["'](?:fill|stroke)["']\s*,\s*["']?\s*((?:#[0-9a-fA-F]{3,8})|(?:rgba?\([^)]*\))|(?:var\(--[\w-]+\)))"""
)
RE_SCALE_CONT = re.compile(r"scale(?:Linear|Sequential|Sqrt|Log|Pow|Diverging)\s*\(|interpolate\w*\(")
RE_STOP_BLOCK = re.compile(r"<(?:linear|radial)Gradient[\s\S]*?</(?:linear|radial)Gradient>", re.I)


# ---------------- 色彩数学（纯 stdlib） ----------------

def _srgb_to_linear(c: float) -> float:
    c /= 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _linear_to_srgb(c: float) -> int:
    v = 12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055
    return max(0, min(255, round(v * 255)))


def _hex_to_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def _rgb_to_lab(rgb: tuple[float, float, float]) -> tuple[float, float, float]:
    r, g, b = (_srgb_to_linear(x) for x in rgb)
    x = (0.4124564 * r + 0.3575761 * g + 0.1804375 * b) / 0.95047
    y = (0.2126729 * r + 0.7151522 * g + 0.0721750 * b) / 1.00000
    z = (0.0193339 * r + 0.1191920 * g + 0.9503041 * b) / 1.08883

    def f(t: float) -> float:
        return t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116

    fx, fy, fz = f(x), f(y), f(z)
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)


def simulate(rgb: tuple[int, int, int], kind: str) -> tuple[int, int, int]:
    mat = SIM_MATRICES[kind]
    lin = tuple(_srgb_to_linear(x) for x in rgb)
    out = tuple(
        max(0.0, min(1.0, mat[i][0] * lin[0] + mat[i][1] * lin[1] + mat[i][2] * lin[2]))
        for i in range(3)
    )
    return tuple(_linear_to_srgb(x) for x in out)


def ciede2000(lab1: tuple[float, float, float], lab2: tuple[float, float, float]) -> float:
    L1, a1, b1 = lab1
    L2, a2, b2 = lab2
    C1 = (a1 * a1 + b1 * b1) ** 0.5
    C2 = (a2 * a2 + b2 * b2) ** 0.5
    Cb = (C1 + C2) / 2
    G = 0.5 * (1 - (Cb ** 7 / (Cb ** 7 + 25 ** 7)) ** 0.5) if Cb ** 7 else 0.5
    a1p, a2p = (1 + G) * a1, (1 + G) * a2
    C1p = (a1p * a1p + b1 * b1) ** 0.5
    C2p = (a2p * a2p + b2 * b2) ** 0.5
    import math

    h1p = math.degrees(math.atan2(b1, a1p)) % 360 if a1p or b1 else 0.0
    h2p = math.degrees(math.atan2(b2, a2p)) % 360 if a2p or b2 else 0.0
    dLp = L2 - L1
    dCp = C2p - C1p
    if C1p * C2p == 0:
        dhp = 0.0
    elif abs(h2p - h1p) <= 180:
        dhp = h2p - h1p
    elif h2p - h1p > 180:
        dhp = h2p - h1p - 360
    else:
        dhp = h2p - h1p + 360
    dHp = 2 * (C1p * C2p) ** 0.5 * math.sin(math.radians(dhp) / 2)
    Lbp, Cbp = (L1 + L2) / 2, (C1p + C2p) / 2
    if C1p * C2p == 0:
        hbp = h1p + h2p
    elif abs(h1p - h2p) <= 180:
        hbp = (h1p + h2p) / 2
    elif h2p - h1p > 180:
        hbp = (h1p + h2p + 360) / 2
    else:
        hbp = (h1p + h2p - 360) / 2
    T = (1 - 0.17 * math.cos(math.radians(hbp - 30)) + 0.24 * math.cos(math.radians(2 * hbp))
         + 0.32 * math.cos(math.radians(3 * hbp + 6)) - 0.20 * math.cos(math.radians(4 * hbp - 63)))
    d_theta = 30 * math.exp(-(((hbp - 275) / 25) ** 2))
    RC = 2 * (Cbp ** 7 / (Cbp ** 7 + 25 ** 7)) ** 0.5 if Cbp ** 7 else 0.0
    SL = 1 + (0.015 * (Lbp - 50) ** 2) / (20 + (Lbp - 50) ** 2) ** 0.5
    SC = 1 + 0.045 * Cbp
    SH = 1 + 0.015 * Cbp * T
    RT = -math.sin(math.radians(2 * d_theta)) * RC
    return (
        (dLp / SL) ** 2 + (dCp / SC) ** 2 + (dHp / SH) ** 2
        - RT * (dCp / SC) * (dHp / SH)
    ) ** 0.5


def _is_neutral(rgb: tuple[int, int, int]) -> bool:
    r, g, b = rgb
    if max(r, g, b) - min(r, g, b) < 24:
        return True
    L, _, _ = _rgb_to_lab((r, g, b))
    return L > 92 or L < 12


def min_delta_e(rgb: tuple[int, int, int], rgb2: tuple[int, int, int]) -> tuple[float, str]:
    best = (1e9, "")
    for kind in SIM_MATRICES:
        de = ciede2000(
            _rgb_to_lab(simulate(rgb, kind)),
            _rgb_to_lab(simulate(rgb2, kind)),
        )
        if de < best[0]:
            best = (de, kind)
    return best


# ---------------- 页面色板抽取 ----------------

def resolve_var(name: str, token_map: dict[str, str]) -> str | None:
    v = token_map.get(name)
    if v is None:
        return None
    m = re.match(r"^var\((--[\w-]+)\)$", v.strip())
    if m:
        return resolve_var(m.group(1), token_map)
    return v


def to_rgb(color: str, token_map: dict[str, str]) -> tuple[int, int, int] | None:
    c = color.strip()
    if c.startswith("#"):
        try:
            return _hex_to_rgb(c)
        except ValueError:
            return None
    m = RE_RGB.match(c)
    if m:
        try:
            return tuple(int(float(x)) for x in m.groups()[:3])
        except ValueError:
            return None
    m = RE_VAR.match(c)
    if m:
        resolved = resolve_var(m.group(1), token_map)
        if resolved and resolved != c:
            return to_rgb(resolved, token_map)
    return None


def strip_embedded(html: str) -> str:
    """剔除 const EMBEDDED_DATA = {...} 数据块——生成期节点色不是页面分类色板（W653 普查发现）。"""
    out = []
    pos = 0
    while True:
        i = html.find("const EMBEDDED_DATA", pos)
        if i == -1:
            out.append(html[pos:])
            break
        out.append(html[pos:i])
        j = html.find("{", i)
        depth = 0
        k = j
        while k < len(html):
            if html[k] == "{":
                depth += 1
            elif html[k] == "}":
                depth -= 1
                if depth == 0:
                    break
            k += 1
        end = html.find("\n", k) + 1 if k < len(html) else len(html)
        out.append("/* EMBEDDED_DATA stripped（色盲门禁：生成期数据色不入分类色板） */\n")
        pos = end
    return "".join(out)


def cluster_palette(palette: dict[str, str], merge_de: float = 3.0) -> dict[str, str]:
    """近似重复色聚类（ΔE<3 合并保留首个）——生成色阶/数据 ramp 的数百近似色坍缩为代表色。"""
    kept: list[tuple[str, str]] = []
    for hx, src in palette.items():
        rgb = _hex_to_rgb(hx)
        dup = False
        for khx, _ in kept:
            if ciede2000(_rgb_to_lab(_hex_to_rgb(khx)), _rgb_to_lab(rgb)) < merge_de:
                dup = True
                break
        if not dup:
            kept.append((hx, src))
    return dict(kept)


def page_palette(html: str, token_map: dict[str, str]) -> dict:
    """抽取页面「系列色板」（W653 三轮口径迭代定稿）。

    系列色板 = 数据系列分类色（同图图例会同时出现的颜色），来源三族：
      a. chart 变量：var(--chart-1..6)/var(--accent)/var(--accent-2..4) 的赋值使用
      b. d3.scheme* 内置色板
      c. colorMap 式字面映射：`"标签": "#hex"`（网络图分类色等·含数组 [.., "#hex", ..]）
    UI 修饰色（边框/徽章/背景的 color: 与 rgba 低透明）不在范围——色盲安全是数据系列问题。
    连续色阶页（scaleLinear 等·W589 数据驱动角色色口径）页级豁免。
    """
    body = strip_embedded(html)
    gradient_n = len(RE_STOP_BLOCK.findall(body))
    body = RE_STOP_BLOCK.sub("", body)

    exempt = "data-driven-scale" if RE_SCALE_CONT.search(body) else None

    palette: dict[str, str] = {}
    neutrals = 0

    def put(color: str, src: str) -> None:
        nonlocal neutrals
        rgb = to_rgb(color, token_map)
        if rgb is None:
            return
        if _is_neutral(rgb):
            neutrals += 1
            return
        palette.setdefault("#%02x%02x%02x" % rgb, src)

    # a. chart 系列变量的定义使用（fill/stroke/color 语境——accent 亦为朱砂主系列色）
    for m in RE_ASSIGN.finditer(body):
        c = (m.group(1) or m.group(2) or "").strip()
        if RE_VAR.match(c) and ("chart" in c or "accent" in c):
            put(c, c)
    # b. d3 scheme
    for m in RE_SCHEME.finditer(body):
        for hx in D3_SCHEMES.get(m.group(1), []):
            put(hx, f"d3.scheme{m.group(1)}")
    # c. colorMap 式映射 / 色板数组（label: "#hex" 与 [#hex, #hex, ...]）
    for m in re.finditer(r"""["'][^"']{1,32}["']\s*:\s*["'](#[0-9a-fA-F]{6})["']""", body):
        put(m.group(1), "colorMap:" + m.group(1))
    for m in re.finditer(r"""(\[\s*(?:"#[0-9a-fA-F]{6}"\s*,\s*){2,}"#[0-9a-fA-F]{6}"\s*\])""", body):
        for hx in re.findall(r"#([0-9a-fA-F]{6})", m.group(1)):
            put("#" + hx, "palette-array")
    # d. fill/stroke 赋值（attr 与 css 两形态·不含 color: 文本色——UI 修饰色不入系列色板）
    for m in RE_FS_ASSIGN.finditer(body):
        put(m.group(1) or m.group(2), "fill/stroke")

    # 近似去噪（ΔE<3 合并——仅去数据 ramp 中间色的重复计数；违规判据 ΔE<10 必须严格大于
    # 聚类阈值，否则坏样本会被聚类自身吞并——W653 self-test 实证）·全量进基线冻结（D-6）
    palette = cluster_palette(palette, merge_de=3.0)
    return {"palette": palette, "neutrals": neutrals, "gradient_stops": gradient_n, "exempt": exempt}


def scan_pages() -> list[Path]:
    return [p for p in sorted(SITE_DATA.glob("*.html")) if p.stem not in SKIP_STEMS]


def token_map_light() -> dict[str, str]:
    decls, _ = parse_css(TOKENS_CSS.read_text(encoding="utf-8"))
    tm: dict[str, str] = {}
    for d in decls:
        if d["theme"] == "light" and d["name"] not in tm:
            tm[d["name"]] = d["value"]
    return tm


def analyze(pages: list[Path], token_map: dict[str, str]) -> dict[str, dict]:
    out = {}
    for p in pages:
        html = p.read_text(encoding="utf-8", errors="ignore")
        info = page_palette(html, token_map)
        violations = []
        if not info["exempt"]:
            colors = sorted(info["palette"].items())
            # 预计算模拟态 Lab（每色每模拟一次·配对复用——全页 O(n²) 对不重算模拟）
            lab_cache: dict[tuple[str, str], tuple[float, float, float]] = {}
            for hx, src in colors:
                rgb = to_rgb(src, token_map) or _hex_to_rgb(hx)
                for kind in SIM_MATRICES:
                    lab_cache[(hx, kind)] = _rgb_to_lab(simulate(rgb, kind))
            for i in range(len(colors)):
                for j in range(i + 1, len(colors)):
                    (hx1, src1), (hx2, src2) = colors[i], colors[j]
                    best = (1e9, "")
                    for kind in SIM_MATRICES:
                        de = ciede2000(lab_cache[(hx1, kind)], lab_cache[(hx2, kind)])
                        if de < best[0]:
                            best = (de, kind)
                    if best[0] < THRESHOLD:
                        violations.append({
                            "a": hx1, "b": hx2, "delta_e": round(best[0], 1), "sim": best[1],
                            "src": f"{src1} × {src2}",
                        })
        out[str(p.relative_to(ROOT)).replace("\\", "/")] = {
            "exempt": info["exempt"],
            "palette_size": len(info["palette"]),
            "neutrals": info["neutrals"],
            "gradient_stops": info["gradient_stops"],
            "violations": violations,
        }
    return out


def _fmt_report(results: dict) -> None:
    n_viol = sum(len(r["violations"]) for r in results.values())
    n_exempt = sum(1 for r in results.values() if r["exempt"])
    print(f"---- 色盲安全：扫描 {len(results)} 页 · 违规对 {n_viol} · 豁免页 {n_exempt}（连续色阶·W589 口径） ----")


def do_survey(pages: list[Path], token_map: dict[str, str]) -> int:
    variants = {"hex": 0, "rgb": 0, "hsl": 0, "var": 0, "scheme": 0, "gradient_stop": 0}
    per_page = {}
    for p in pages:
        html = p.read_text(encoding="utf-8", errors="ignore")
        stops = len(RE_STOP_BLOCK.findall(html))
        v = {
            "hex": len(RE_HEX.findall(html)),
            "rgb": len(RE_RGB.findall(html)),
            "hsl": len(RE_HSL.findall(html)),
            "var": len(RE_VAR.findall(html)),
            "scheme": len(RE_SCHEME.findall(html)),
            "gradient_stop": stops,
        }
        for k in variants:
            variants[k] += v[k]
        per_page[str(p.relative_to(ROOT)).replace("\\", "/")] = v
    payload = {
        "survey_date": date_today(),
        "pages": len(pages),
        "variants_total": variants,
        "per_page": per_page,
        "note": "形态普查先于正则（W653）·色值书写变体：hex/rgb()/hsl()/var(--x)/d3.scheme*/渐变 stop",
    }
    SURVEY.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"普查已写出：{SURVEY.relative_to(ROOT)}")
    print("  变体分布：" + " · ".join(f"{k}={v}" for k, v in variants.items()))
    return 0


def date_today() -> str:
    from datetime import date as _d
    return _d.today().isoformat()


def do_report(pages: list[Path], token_map: dict[str, str]) -> int:
    results = analyze(pages, token_map)
    for page, r in results.items():
        tag = r["exempt"] or "scanned"
        print(f"{page}: palette={r['palette_size']} violations={len(r['violations'])} exempt={tag}")
        for v in r["violations"]:
            print(f"    {v['a']} × {v['b']} · ΔE={v['delta_e']} ({v['sim']}) · {v['src']}")
    _fmt_report(results)
    return 0


def do_baseline(pages: list[Path], token_map: dict[str, str]) -> int:
    results = analyze(pages, token_map)
    lines = [
        "# 第 29 门禁 · 图表配色色盲安全基线（PD-1a·W653）",
        "# 语义：违规集合单调不增——基线内 frozen（WARN 豁免）·基线外新增 FAIL·修复后删行收紧",
        f"# 格式：page|hexA|hexB|sim|delta   ·快照 {date_today()} ·阈值 ΔE<{THRESHOLD}·口径=light 静态",
    ]
    n = 0
    for page in sorted(results):
        for v in results[page]["violations"]:
            lines.append(f"{page}|{v['a']}|{v['b']}|{v['sim']}|{v['delta_e']}")
            n += 1
    BASELINE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"基线已冻结：{BASELINE.relative_to(ROOT)} · 违规对 {n} · 豁免页 {sum(1 for r in results.values() if r['exempt'])}")
    return 0


def do_gate(pages: list[Path], token_map: dict[str, str]) -> int:
    if not BASELINE.exists():
        print(f"FAIL 基线缺失：{BASELINE.relative_to(ROOT)} — refuse to pass（先跑 --generate-baseline）")
        return 1
    base: dict[str, set] = {}
    for line in BASELINE.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#"):
            continue
        parts = line.split("|")
        if len(parts) >= 4:
            base.setdefault(parts[0], set()).add(f"{parts[1]}|{parts[2]}")
    results = analyze(pages, token_map)
    new_v, frozen, exempt_n = [], [], 0
    for page, r in results.items():
        if r["exempt"]:
            exempt_n += 1
        for v in r["violations"]:
            pair = f"{v['a']}|{v['b']}"
            if pair in base.get(page, set()):
                frozen.append(f"{page} :: {pair} ΔE={v['delta_e']}")
            else:
                new_v.append(f"{page} :: {v['a']} × {v['b']} ΔE={v['delta_e']}（{v['sim']}·{v['src']}）")
    for line in new_v:
        print("FAIL " + line)
    print(
        f"---- 第 29 门禁 色盲安全：扫描 {len(results)} 页 · 基线外违规 {len(new_v)} · "
        f"冻结存量 {len(frozen)} · 豁免页 {exempt_n} · 阈值 ΔE<{THRESHOLD}（口径=light 静态·暗色归 PD-4） ----"
    )
    if frozen:
        print(f"WARN 存量 {len(frozen)} 对已冻结豁免（D-6 裁决：收敛至阈值以下再转 FAIL）")
    return 1 if new_v else 0


def do_self_test(tmp: Path) -> int:
    tmp.mkdir(parents=True, exist_ok=True)
    good = """<html><body><div id="dataSource">数据源：json/x.json</div><script>
d3.select("#c").selectAll("rect").data([1,2]).enter().append("rect")
  .attr("fill", "#3A6B8C"); /* 靛蓝 */
d3.select("#c2").selectAll("rect").data([1,2]).enter().append("rect")
  .attr("fill", "#E9B885"); /* 浅金 */
</script></body></html>"""
    bad = """<html><body><script>
sel.attr("fill", "#C8463A"); /* 朱砂红 */
sel.attr("stroke", "#6B8E5A"); /* 苔绿 */
</script></body></html>"""
    neutral = """<html><body><script>
sel.attr("fill", "#23201A"); sel.attr("stroke", "#6B6455");
</script></body></html>"""
    scale_page = """<html><body><script>
const color = d3.scaleLinear().domain([0,10]).range(["#C8463A","#6B8E5A"]);
sel.attr("fill", "#C8463A"); sel.attr("stroke", "#6B8E5A");
</script></body></html>"""
    cases = [("good.html", good, 0), ("bad.html", bad, 1), ("neutral.html", neutral, 0), ("scale.html", scale_page, 0)]
    rc = 0
    tm = token_map_light()
    for name, html, want in cases:
        f = tmp / name
        f.write_text(html, encoding="utf-8")
        r = analyze([f], tm)[str(f.relative_to(ROOT)).replace("\\", "/")]
        got = len(r["violations"])
        ok = got == want
        rc = rc if ok else 2
        print(f"{'OK  ' if ok else 'FAIL'} {name}: 期望违规 {want} · 实际 {got}（exempt={r['exempt']}）")
    print("self-test", "PASS" if rc == 0 else "FAIL")
    return rc


def main() -> int:
    argv = sys.argv
    token_map = token_map_light()
    if "--self-test" in argv:
        return do_self_test(ROOT / ".review-tmp" / "colorblind-selftest")
    pages = scan_pages()
    if not pages:
        print(f"FAIL 未扫到页面：{SITE_DATA}")
        return 1
    if "--survey" in argv:
        return do_survey(pages, token_map)
    if "--report" in argv:
        return do_report(pages, token_map)
    if "--generate-baseline" in argv:
        return do_baseline(pages, token_map)
    if "--gate" in argv:
        return do_gate(pages, token_map)
    print(__doc__)
    return 0


if __name__ == "__main__":
    sys.exit(main())
