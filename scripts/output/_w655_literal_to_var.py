#!/usr/bin/env python3
"""W655 临时脚本：B-9② 字面色值→CSS 变量转换（token 值精确匹配·attr→style·暗色 chart 亮度核算）"""
import sys, json, re
from pathlib import Path

ROOT = Path(".").resolve()
sys.path.insert(0, str(ROOT / "scripts"))
from check_chart_colorblind import _srgb_to_linear, _rgb_to_lab  # 复用色彩数学

payload = json.load(open("scripts/output/design-tokens.json", encoding="utf-8"))
# light 令牌：值(lower) → [(pref, token_name)]——chart-N 优先用于 fill/stroke
val2tok = {}
for k, t in payload["tokens"].items():
    theme, name = k.split("/", 1)
    if theme != "light":
        continue
    v = t["$value"].strip()
    if not (v.startswith("#") or v.startswith("rgb")):
        continue
    pref = 0 if name.startswith("chart-") else (1 if name.startswith("accent") else 2)
    val2tok.setdefault(v.lower(), []).append((pref, name))
for v in val2tok:
    val2tok[v].sort()

def pick_token(value: str, prop: str) -> str | None:
    cands = val2tok.get(value.strip().lower())
    if not cands:
        return None
    if prop in ("fill", "stroke"):
        chart = [n for p, n in cands if n.startswith("chart-")]
        if chart:
            return chart[0]
    return cands[0][1]

def lum(hexv: str) -> float:
    r, g, b = (int(hexv[i:i+2], 16) for i in (1, 3, 5))
    return 0.2126 * _srgb_to_linear(r) + 0.7152 * _srgb_to_linear(g) + 0.0722 * _srgb_to_linear(b)

# 暗色 --chart-N 提亮核算（W587 规则：L<0.16 → 提到 ≥0.22 保色相）
print("== 暗色 --chart-N 亮度核算 ==")
for name in ("chart-1", "chart-2", "chart-3", "chart-4", "chart-5", "chart-6"):
    key = "light/" + name
    v = payload["tokens"][key]["$value"]
    L = lum(v)
    need = "  ← 需提亮(L<0.16)" if L < 0.16 else ""
    print(f"  {name}: {v} L={L:.3f}{need}")

RE_ATTR = re.compile(r'\.attr\(\s*(["\'])(fill|stroke|color)\1\s*,\s*(["\'])((?:#|rgb|var\()[^"\']*)\3\s*\)')
RE_STYLE = re.compile(r'\.style\(\s*(["\'])(fill|stroke|color)\1\s*,\s*(["\'])((?:#|rgb|var\()[^"\']*)\3\s*\)')

def conv_page(p: Path) -> dict:
    s = p.read_text(encoding="utf-8")
    rep = {"attr": 0, "style": 0}
    def sub_attr(m):
        q, prop, q2, val = m.group(1), m.group(2), m.group(3), m.group(4)
        tok = pick_token(val, prop)
        if not tok:
            return m.group(0)
        rep["attr"] += 1
        return f'.style({q}{prop}{q}, {q2}var({tok}){q2})'
    def sub_style(m):
        q, prop, q2, val = m.group(1), m.group(2), m.group(3), m.group(4)
        if val.startswith("var("):
            return m.group(0)
        tok = pick_token(val, prop)
        if not tok:
            return m.group(0)
        rep["style"] += 1
        return f'.style({q}{prop}{q}, {q2}var({tok}){q2})'
    s = RE_ATTR.sub(sub_attr, s)
    s = RE_STYLE.sub(sub_style, s)
    if rep["attr"] or rep["style"]:
        p.write_text(s, encoding="utf-8", newline="")
    return rep

pages = sorted(p for p in (ROOT / "site" / "data").glob("*.html") if p.stem not in ("_shell", "_template"))
total = {"attr": 0, "style": 0}
touched = []
for p in pages:
    r = conv_page(p)
    if r["attr"] or r["style"]:
        touched.append((p.name, r["attr"], r["style"]))
        total["attr"] += r["attr"]; total["style"] += r["style"]
print(f"转换完成：attr→style {total['attr']} 处 · style 字面量→var {total['style']} 处 · 触及 {len(touched)} 页")
for name, a, st in sorted(touched, key=lambda x: -(x[1]+x[2]))[:12]:
    print(f"  {name}: attr→style {a} · style→var {st}")
