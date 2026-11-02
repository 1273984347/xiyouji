# -*- coding: utf-8 -*-
"""color_delta_guard.py — ΔL* 阈值机器判据（补偿失配可接受幅度·W1103）

## 为什么需要它

W1097–W1099 把页内硬编码图表色换成 CSS 令牌后，暗色下出现两类**补偿失配**（E-88）：

1. `filter` 消失——前缀型补偿 `svg path[fill^="#"] { filter: brightness(1.12) }`
   按 **content attribute 字面值**匹配 ⇒ 换成 `var(--chart-N)` 后不再以 `#` 开头 ⇒ 规则失配；
2. computed fill 落回 CSS 类色——字面值型补偿 `svg [fill="#3a6b8c" i] { fill: #7d99a9 }`
   特异性高于元素自身类规则 ⇒ 失配后落到类规则的颜色，**不是**硬编码色。

「失配可不可接受」此前只靠人眼看。本工具把它变成**可机读的实数**：
对每个色对算 CIELAB 亮度差 ΔL*，按阈值分三档 ⇒ 超阈值必须显式补偿，否则阻断。

## 阈值口径（实测校准·非拍脑袋）

站点自有两套补偿机制，其等效 ΔL* 幅度实测为两个**互不重叠**的区间：

- **弱补偿**（前缀型 brightness 1.12）⇒ 等效 ΔL* **1.1 ~ 5.6**（59 个补偿原色全覆盖·中位 4.5）
- **强补偿**（字面值型重映射）⇒ 等效 ΔL* **14.7 ~ 55.1**（中位 24.2）

⇒ 判据分档（默认可配）：

| 档 | ΔL* | 含义 | 依据 |
|---|---|---|---|
| OK | ≤ 6 | 可接受 | 不超过既有弱补偿机制的最大等效幅度（5.6） |
| WARN | 6 ~ 12 | 需人工确认 | 超出弱补偿尺度·但未达强补偿下限（14.7） |
| BLOCK | > 12 | 必须显式补偿 | 接近强补偿幅度下限 ⇒ 差异不可忽视 |

## 用法

    py -3 scripts/color_delta_guard.py pairs --pairs pairs.json
    py -3 scripts/color_delta_guard.py scan-comp --site site
    py -3 scripts/color_delta_guard.py scan-tokens --tokens site/tokens.css
    py -3 scripts/color_delta_guard.py scan-palette --tokens site/tokens.css --site site
    py -3 scripts/color_delta_guard.py --self-test

退出码：0 通过 · 1 存在 BLOCK 档色对 · 2 断言/输入错误。
"""

import argparse
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEFAULT_OK = 6.0
DEFAULT_WARN = 12.0

# 12 色调色板（W1100 盘点口径·含浅色值与暗色值两种形态）
HEX12 = ["C8463A", "E46250", "3A6B8C", "6B8E5A", "B38F58", "D8CFBC",
         "8A6D3B", "E9B885", "7FA8C9", "E0604F", "C9A96B", "9DB98A"]
# 调色板色 → 目标令牌（浅色值与暗色值共用同一令牌）
PALETTE_TOKEN = {
    "#c8463a": "--chart-1", "#e46250": "--chart-1", "#e0604f": "--chart-1",
    "#3a6b8c": "--chart-2", "#7fa8c9": "--chart-2",
    "#b38f58": "--chart-3", "#6b8e5a": "--chart-4", "#9db98a": "--chart-4",
    "#d8cfbc": "--chart-5", "#8a6d3b": "--chart-6", "#c9a96b": "--chart-6",
    "#e9b885": "--accent-soft",
}

# sRGB → XYZ（D65）矩阵
_M = (
    (0.4124564, 0.3575761, 0.1804375),
    (0.2126729, 0.7151522, 0.0721750),
    (0.0193339, 0.1191920, 0.9503041),
)
_WHITE = (0.95047, 1.0, 1.08883)


def hex_to_rgb(value):
    """#rgb / #rrggbb → (r,g,b) 0-255。非法值抛 ValueError。"""
    h = str(value).strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) != 6 or not re.fullmatch(r"[0-9a-fA-F]{6}", h):
        raise ValueError("非法 hex 色值：%r" % (value,))
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _linearize(c8):
    c = c8 / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def srgb_to_lab(value):
    """sRGB hex → CIELAB（D65）。返回 (L*, a*, b*)。"""
    r, g, b = [_linearize(v) for v in hex_to_rgb(value)]
    xyz = [sum(row[i] * (r, g, b)[i] for i in range(3)) for row in _M]
    xyz = [xyz[i] / _WHITE[i] for i in range(3)]

    def f(t):
        if t > (6.0 / 29.0) ** 3:
            return t ** (1.0 / 3.0)
        return t / (3 * (6.0 / 29.0) ** 2) + 4.0 / 29.0

    fx, fy, fz = (f(v) for v in xyz)
    return (116.0 * fy - 16.0, 500.0 * (fx - fy), 200.0 * (fy - fz))


def delta_l(c1, c2):
    """ΔL*：两色 CIELAB 亮度差（绝对值）。"""
    return abs(srgb_to_lab(c1)[0] - srgb_to_lab(c2)[0])


def delta_e76(c1, c2):
    """ΔE*76：总色差（亮度 + 色度）。"""
    l1, a1, b1 = srgb_to_lab(c1)
    l2, a2, b2 = srgb_to_lab(c2)
    return ((l1 - l2) ** 2 + (a1 - a2) ** 2 + (b1 - b2) ** 2) ** 0.5


def brightness_hex(value, k=1.12):
    """CSS `filter: brightness(k)` 的等效色（sRGB 编码值域上乘 k·与浏览器口径一致）。"""
    rgb = [min(255, max(0, int(round(v * k)))) for v in hex_to_rgb(value)]
    return "#%02x%02x%02x" % tuple(rgb)


def grade(delta, ok=DEFAULT_OK, warn=DEFAULT_WARN):
    """按阈值分档：OK / WARN / BLOCK。"""
    if delta <= ok:
        return "OK"
    if delta <= warn:
        return "WARN"
    return "BLOCK"


RE_TOKEN = re.compile(r"(--[a-z0-9-]+)\s*:\s*(#[0-9a-fA-F]{3,8})\s*;", re.I)
RE_LITERAL_COMP = re.compile(
    r'\[fill="(#[0-9a-fA-F]{3,8})"\s*i\][^{]*\{[^}]*?fill:\s*(#[0-9a-fA-F]{3,8})', re.I)
RE_PREFIX_COMP = re.compile(r'\[fill\^="#"\][^{]*\{[^}]*?filter:\s*brightness\(([\d.]+)\)', re.I)


def parse_tokens(css_text):
    """解析 CSS 文本 → (浅色令牌表, 暗色令牌表)。

    暗色表 = 首个 `html[data-theme="dark"] {...}` 块内的令牌定义；
    未在该块出现的令牌即**暗色无覆盖**（暗色下沿用浅色值）。
    """
    head = css_text
    dark = {}
    m = re.search(r'html\[data-theme="dark"\][^{]*\{', css_text)
    if m:
        start = m.end()
        depth = 1
        i = start
        while i < len(css_text) and depth:
            if css_text[i] == "{":
                depth += 1
            elif css_text[i] == "}":
                depth -= 1
            i += 1
        dark = dict(RE_TOKEN.findall(css_text[start:i - 1]))
        head = css_text[:m.start()]
    light = dict(RE_TOKEN.findall(head))
    return light, dark


def parse_literal_comp(text):
    """字面值型补偿条目 → [(原色, 补偿色)]（保持出现序·去重保首条）。"""
    seen = set()
    out = []
    for src, dst in RE_LITERAL_COMP.findall(text):
        key = (src.lower(), dst.lower())
        if key not in seen:
            seen.add(key)
            out.append(key)
    return out


def parse_prefix_comp(text):
    """前缀型补偿的 brightness 系数 → [float]。"""
    return [float(x) for x in RE_PREFIX_COMP.findall(text)]


def load_pairs(path):
    """读色对清单 JSON：{"pairs":[{"label":..,"before":"#hex","after":"#hex"}]}"""
    with io.open(path, encoding="utf-8") as f:
        data = json.load(f)
    items = data["pairs"] if isinstance(data, dict) else data
    return [(it.get("label", ""), it["before"], it["after"]) for it in items]


def eval_pairs(pairs, ok=DEFAULT_OK, warn=DEFAULT_WARN):
    """逐对算 ΔL*/ΔE76 + 分档。返回 (rows, summary)。"""
    rows = []
    counts = {"OK": 0, "WARN": 0, "BLOCK": 0}
    for label, before, after in pairs:
        d = delta_l(before, after)
        g = grade(d, ok, warn)
        counts[g] += 1
        rows.append({"label": label, "before": before, "after": after,
                     "delta_l": round(d, 2), "delta_e76": round(delta_e76(before, after), 2),
                     "grade": g})
    summary = {"total": len(rows), "ok": counts["OK"], "warn": counts["WARN"],
               "block": counts["BLOCK"], "ok_threshold": ok, "warn_threshold": warn}
    return rows, summary


def _percentile(values, p):
    """百分位（线性最近秩）。空序列返回 0.0。"""
    if not values:
        return 0.0
    s = sorted(values)
    idx = min(len(s) - 1, int(round(p / 100.0 * (len(s) - 1))))
    return s[idx]


def cmd_pairs(args):
    """pairs 子命令：对色对清单求 ΔL* 并分档。"""
    rows, summary = eval_pairs(load_pairs(args.pairs), args.ok, args.warn)
    for r in rows:
        print("[%s] ΔL*=%6.2f  ΔE76=%6.2f  %s -> %s  %s" % (
            r["grade"], r["delta_l"], r["delta_e76"], r["before"], r["after"], r["label"]))
    print("汇总：%d 对（OK %d / WARN %d / BLOCK %d）·阈值 OK≤%.1f WARN≤%.1f" % (
        summary["total"], summary["ok"], summary["warn"], summary["block"],
        summary["ok_threshold"], summary["warn_threshold"]))
    return 1 if summary["block"] else 0


def _iter_site_files(site_dir):
    """遍历站点下全部 html/css 文件路径。"""
    for dp, _dn, fn in os.walk(site_dir):
        for f in sorted(fn):
            if f.endswith((".html", ".css")):
                yield os.path.join(dp, f)


def collect_comp(site_dir):
    """全站字面值型补偿 + 前缀型 brightness 系数。返回 (pairs, pages, entries, prefix_k)。"""
    pairs = {}
    pages = 0
    entries = 0
    prefix_k = []
    for p in _iter_site_files(site_dir):
        text = io.open(p, encoding="utf-8", errors="replace").read()
        found = parse_literal_comp(text)
        if found:
            pages += 1
            entries += len(found)
            for s, d in found:
                pairs.setdefault(s, d)
        for k in parse_prefix_comp(text):
            if k not in prefix_k:
                prefix_k.append(k)
    return pairs, pages, entries, prefix_k


def cmd_scan_comp(args):
    """scan-comp 子命令：扫描全站补偿表并给出等效 ΔL* 分布（阈值校准的原始数据）。"""
    pairs, pages, entries, prefix_k = collect_comp(args.site)
    strong = sorted(delta_l(s, d) for s, d in pairs.items())
    ks = prefix_k or [1.12]
    weak = sorted(delta_l(s, brightness_hex(s, k)) for k in ks for s in pairs)
    print("字面值型补偿：%d 文件 / %d 条 / 唯一原色 %d 个" % (pages, entries, len(pairs)))
    if strong:
        print("  强补偿等效 ΔL*：min=%.1f p25=%.1f p50=%.1f p75=%.1f max=%.1f" % (
            strong[0], _percentile(strong, 25), _percentile(strong, 50),
            _percentile(strong, 75), strong[-1]))
    if weak:
        print("  弱补偿 brightness 系数：%s · 等效 ΔL*：min=%.1f p50=%.1f max=%.1f" % (
            ",".join("%.2f" % k for k in ks), weak[0], _percentile(weak, 50), weak[-1]))
    print("  判据阈值（可配）：OK≤%.1f · WARN≤%.1f · BLOCK>%.1f" % (args.ok, args.warn, args.warn))
    return 0


def cmd_scan_tokens(args):
    """scan-tokens 子命令：令牌暗色覆盖体检（暗色无覆盖 = 档 3 的硬前置缺口）。"""
    css = io.open(args.tokens, encoding="utf-8").read()
    light, dark = parse_tokens(css)
    missing = [(n, v) for n, v in sorted(light.items()) if n not in dark]
    print("浅色令牌 %d 个 · 暗色覆盖 %d 个 · 暗色无覆盖 %d 个" % (
        len(light), len(dark), len(missing)))
    for name, val in missing:
        tag = "图表色·须补" if name.startswith("--chart") or name == "--accent-soft" else "其它"
        print("  [暗色无覆盖] %-16s = %-8s（暗色沿用浅色值）· %s" % (name, val, tag))
    return 0


def cmd_scan_palette(args):
    """scan-palette 子命令：调色板 12 色双态体检（替换前实际色 → 令牌色）。"""
    css = io.open(args.tokens, encoding="utf-8").read()
    light, dark = parse_tokens(css)
    pairs, _pages, _entries, prefix_k = collect_comp(args.site)
    ks = prefix_k or [1.12]
    rows = []
    tally = {"dark": {"OK": 0, "WARN": 0, "BLOCK": 0, "NO_DARK": 0},
             "light": {"OK": 0, "WARN": 0, "BLOCK": 0}}
    for h in HEX12:
        x = "#" + h.lower()
        token = PALETTE_TOKEN.get(x)
        if not token:
            continue
        comp = pairs.get(x)
        comp_note = "字面值补偿" if comp else "仅前缀型 filter"
        dark_before = comp if comp else brightness_hex(x, ks[0])
        dark_after = dark.get(token)
        light_before = x
        light_after = light.get(token)
        d_dark = delta_l(dark_before, dark_after) if dark_after else None
        d_light = delta_l(light_before, light_after) if light_after else None
        g_dark = grade(d_dark, args.ok, args.warn) if d_dark is not None else "NO_DARK"
        g_light = grade(d_light, args.ok, args.warn) if d_light is not None else "NO_LIGHT"
        tally["dark"][g_dark] += 1
        tally["light"][g_light] += 1
        rows.append((x, token, comp_note, dark_before, dark_after, d_dark, g_dark,
                     light_before, light_after, d_light, g_light))
    print("调色板 %d 色双态体检（阈值 OK≤%.1f · WARN≤%.1f）" % (len(rows), args.ok, args.warn))
    print("  %-9s %-13s %-13s %-9s -> %-9s %6s %-8s | %-9s -> %-9s %6s %-8s" % (
        "原色", "令牌", "补偿形态", "暗色前", "暗色后", "ΔL*", "暗档",
        "浅色前", "浅色后", "ΔL*", "浅档"))
    for r in rows:
        dd = "n/a" if r[5] is None else "%.1f" % r[5]
        dl = "n/a" if r[9] is None else "%.1f" % r[9]
        print("  %-9s %-13s %-13s %-9s -> %-9s %6s %-8s | %-9s -> %-9s %6s %-8s" % (
            r[0], r[1], r[2], r[3], r[4] or "(无覆盖)", dd, r[6],
            r[7], r[8] or "(无)", dl, r[10]))
    print("汇总：暗色档 %s" % tally["dark"])
    print("      浅色档 %s" % tally["light"])
    return 0


def self_test():
    """内建自检（锚点用 CIE 标准参考值·与实现无关）。"""
    assert abs(srgb_to_lab("#000000")[0] - 0.0) < 0.01
    assert abs(srgb_to_lab("#ffffff")[0] - 100.0) < 0.01
    assert abs(srgb_to_lab("#808080")[0] - 53.585) < 0.01
    assert abs(delta_l("#c8463a", "#c8463a")) < 1e-9
    assert abs(delta_e76("#c8463a", "#c8463a")) < 1e-9
    assert grade(6.0) == "OK"
    assert grade(6.01) == "WARN"
    assert grade(12.0) == "WARN"
    assert grade(12.01) == "BLOCK"
    assert brightness_hex("#3a6b8c", 1.12) == "#41789d"
    assert hex_to_rgb("#fff") == (255, 255, 255)
    lt, dk = parse_tokens(':root{--a:#111111;}html[data-theme="dark"]{--a:#222222;--b:#333333;}')
    assert lt["--a"] == "#111111" and dk["--a"] == "#222222" and dk["--b"] == "#333333"
    comp = parse_literal_comp('svg [fill="#3a6b8c" i] { fill: #7d99a9; }')
    assert comp == [("#3a6b8c", "#7d99a9")], comp
    try:
        hex_to_rgb("#zz")
        raise AssertionError("非法 hex 未抛错")
    except ValueError:
        pass
    print("self-test: 全部通过")
    return 0


def main(argv=None):
    """命令行入口。"""
    ap = argparse.ArgumentParser(description="ΔL* 阈值机器判据")
    ap.add_argument("--ok", type=float, default=DEFAULT_OK,
                    help="OK 档上限（默认 %.1f）" % DEFAULT_OK)
    ap.add_argument("--warn", type=float, default=DEFAULT_WARN,
                    help="WARN 档上限（默认 %.1f）" % DEFAULT_WARN)
    ap.add_argument("--self-test", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    p_pairs = sub.add_parser("pairs", help="对色对清单求 ΔL* 并分档")
    p_pairs.add_argument("--pairs", required=True)
    p_comp = sub.add_parser("scan-comp", help="扫描全站补偿表并给出等效 ΔL* 分布")
    p_comp.add_argument("--site", default=os.path.join(ROOT, "site"))
    p_tok = sub.add_parser("scan-tokens", help="令牌暗色覆盖体检")
    p_tok.add_argument("--tokens", default=os.path.join(ROOT, "site", "tokens.css"))
    p_pal = sub.add_parser("scan-palette", help="调色板 12 色双态体检（替换前 → 令牌色）")
    p_pal.add_argument("--tokens", default=os.path.join(ROOT, "site", "tokens.css"))
    p_pal.add_argument("--site", default=os.path.join(ROOT, "site"))
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    if args.cmd == "pairs":
        return cmd_pairs(args)
    if args.cmd == "scan-comp":
        return cmd_scan_comp(args)
    if args.cmd == "scan-tokens":
        return cmd_scan_tokens(args)
    if args.cmd == "scan-palette":
        return cmd_scan_palette(args)
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
