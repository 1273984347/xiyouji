#!/usr/bin/env python3
"""check_dark_heatmap_ramps.py — 热力图暗色态色阶可见性守卫（暗色门禁第 80 槽的离线前置判据）。

背景（CI 实证）：暗色门禁（check_dark_state_gate.js）判「深底上相对亮度 Y<0.16 的填充图形
为 invisible」。W1365 实测 8 页 × 10 处 invisible，根因＝热力图色阶沿用亮色态深端
（YlOrRd 深红端 Y=0.076 / Blues 深端 Y=0.062）⇒ 暗底上不可见。仓内既有范式（W993）＝
暗色态换中明度冷纸色渐变。本脚本离线复算该判据：

  ① 扫 site/**/*.html 里所有 d3.scaleSequential(...) 的 interpolator 表达式；
  ② 有暗色分支（dataset.theme === 'dark'）⇒ 取分支色阶 hex 列表，按 d3.interpolateRgbBasis
     的分段线性 RGB 插值采样 256 步，断言 minY >= 0.16（门禁同口径）；
  ③ 无暗色分支 ⇒ 记为隐患（WARN），登记进豁免清单后方可不判红（存量页分批收敛）；
  ④ 任一非豁免页有色阶不达标 ⇒ exit 1。

用法：python scripts/check_dark_heatmap_ramps.py [--json 输出路径]
豁免清单：scripts/output/dark-heatmap-exemptions.txt（每行：<页面路径>  # 原因）
"""
from __future__ import annotations

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
EXEMPT = os.path.join(ROOT, "scripts", "output", "dark-heatmap-exemptions.txt")

THRESH_Y = 0.16          # 暗色门禁同口径：深底上 Y<0.16 判 invisible
TEXT_MIN = 3.0           # WCAG 1.4.11 非文本对比度（格内数值）
DARK_BG = (26, 23, 20)   # 暗色态 body 底（实测 rgb(26,23,20)）

SCALE_RE = re.compile(r"d3\.scaleSequential\(")
BASIS_RE = re.compile(r"interpolateRgbBasis\(\[([^\]]*)\]\)")
HEX_RE = re.compile(r"#([0-9A-Fa-f]{6})")
DARK_MARK_RE = re.compile(r"dataset\.theme\s*===\s*['\"]dark['\"]")


def _lin(v: float) -> float:
    v /= 255.0
    return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4


def rel_lum(rgb) -> float:
    return 0.2126 * _lin(rgb[0]) + 0.7152 * _lin(rgb[1]) + 0.0722 * _lin(rgb[2])


def contrast(l1: float, l2: float) -> float:
    a, b = max(l1, l2), min(l1, l2)
    return (a + 0.05) / (b + 0.05)


def hex_rgb(h: str):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def sample_basis(hexes, steps: int = 256):
    """按 d3.interpolateRgbBasis 的分段线性 RGB 插值采样 → (minY, 最差灰字对比, 最差底对比)。"""
    pts = [hex_rgb(h) for h in hexes]
    if len(pts) < 2:
        return None
    ink = rel_lum(hex_rgb("#1a1410"))
    min_y, worst_text, worst_bg = 9.9, 9.9, 9.9
    for i in range(steps + 1):
        t = i / steps * (len(pts) - 1)
        k = min(int(t), len(pts) - 2)
        f = t - k
        c = tuple(pts[k][j] + (pts[k + 1][j] - pts[k][j]) * f for j in range(3))
        y = rel_lum(c)
        min_y = min(min_y, y)
        worst_text = min(worst_text, max(contrast(y, ink), contrast(y, 1.0)))
        worst_bg = min(worst_bg, contrast(y, rel_lum(DARK_BG)))
    return min_y, worst_text, worst_bg


def _match_paren(src: str, open_idx: int) -> int:
    depth = 0
    i = open_idx
    while i < len(src):
        if src[i] == "(":
            depth += 1
        elif src[i] == ")":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


def scan_page_sample(src: str):
    """返回该页热力图色阶的判定记录。"""
    recs = []
    for m in SCALE_RE.finditer(src):
        # 链式调用（.domain().interpolator()）的信息在括号之外 ⇒ 取到语句结束（;）的整条链
        semi = src.find(";", m.end())
        expr = src[m.end():semi] if semi > 0 else src[m.end():m.end() + 600]
        basis = BASIS_RE.search(expr)
        has_dark = bool(DARK_MARK_RE.search(expr))
        if basis and has_dark:
            hexes = HEX_RE.findall(basis.group(1))
            sampled = sample_basis(hexes)
            if sampled is None:
                continue
            min_y, worst_text, worst_bg = sampled
            recs.append({
                "kind": "dark-branch", "hexes": hexes, "minY": round(min_y, 4),
                "worstText": round(worst_text, 2), "worstBg": round(worst_bg, 2),
                "ok": min_y >= THRESH_Y and worst_text >= TEXT_MIN,
            })
        elif has_dark:
            recs.append({"kind": "dark-branch-unparsed", "ok": False})
        else:
            # 存量：色阶无暗色分支 ⇒ 记隐患（WARN）而非 FAIL（待分批收敛）
            recs.append({"kind": "no-dark-branch", "ok": False})
    return recs


def scan_page(path: str):
    # page-level wrapper
    return scan_page_sample(open(path, encoding="utf-8").read())


def load_exemptions():
    out = set()
    if os.path.exists(EXEMPT):
        for line in open(EXEMPT, encoding="utf-8"):
            line = line.split("#")[0].strip()
            if line:
                out.add(line.replace("\\", "/"))
    return out


def collect():
    exempt = load_exemptions()
    rows = []
    for dirpath, _dirs, files in os.walk(SITE):
        for fn in files:
            if not fn.endswith(".html"):
                continue
            p = os.path.join(dirpath, fn)
            rel = os.path.relpath(p, ROOT).replace("\\", "/")
            recs = scan_page(p)
            if not recs:
                continue
            kinds = {r["kind"] for r in recs}
            if "no-dark-branch" in kinds:
                status = "WARN"      # 存量未收敛（登记豁免后不判红）
            elif all(r["ok"] for r in recs):
                status = "PASS"
            else:
                status = "FAIL"
            if rel in exempt and status != "PASS":
                status = "EXEMPT"
            rows.append({"page": rel, "status": status, "n": len(recs),
                         "minY": min([r.get("minY", 9.9) for r in recs]),
                         "worstText": min([r.get("worstText", 9.9) for r in recs])})
    return rows


def main() -> int:
    rows = collect()
    fails = [r for r in rows if r["status"] == "FAIL"]
    warns = [r for r in rows if r["status"] == "WARN"]
    exem = [r for r in rows if r["status"] == "EXEMPT"]
    print("暗色热力图色阶守卫：页面 %d（PASS %d · WARN %d · EXEMPT %d · FAIL %d）"
          % (len(rows), len(rows) - len(fails) - len(warns) - len(exem),
             len(warns), len(exem), len(fails)))
    for r in sorted(rows, key=lambda x: (x["status"], x["page"])):
        if r["status"] != "PASS":
            print("  %-8s %-52s minY=%.4f worstText=%.2f" % (r["status"], r["page"], r["minY"], r["worstText"]))
    if "--json" in sys.argv:
        i = sys.argv.index("--json")
        out = sys.argv[i + 1] if i + 1 < len(sys.argv) else "scripts/output/dark-heatmap-ramps.json"
        p = out if os.path.isabs(out) else os.path.join(ROOT, out)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            json.dump(rows, f, ensure_ascii=False, indent=1)
        print("  json →", os.path.relpath(p, ROOT))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
