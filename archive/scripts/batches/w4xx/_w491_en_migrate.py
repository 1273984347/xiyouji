#!/usr/bin/env python3
"""W491 E4 EN 站 85 同名可视化页迁移（一次性脚本，不入门禁/CI）

复用 W478 六规则范式（R-SHADOW/R-RADIUS/R-TRANS/R-FOCUS/裸色白名单/R-EXEMPT）。
E4 派生 = CN data 86 页与 site/en 同名 85 页（缺 journey-geo-3d）。
仅处理页私有 <style> 块（跳过 INLINED tokens+system 块）；禁全站盲正则——页面清单由派生命令生成。

用法：
  python scripts/_w490_migrate.py --dry    # 仅输出拟改行供审查
  python scripts/_w490_migrate.py          # 实际应用
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "site" / "en"
DRY = "--dry" in sys.argv

PILOTS = {"hardship-heatmap.html", "intertextuality-network.html", "chapter-stats.html"}


EN_PAGES = [l.strip() for l in open(ROOT / "scripts" / "output" / "_w491_en_list.txt", encoding="utf-8") if l.strip()]


def derive_list():
    return [DATA / (p + ".html") for p in EN_PAGES]


# ---- 规则 ----
RADIUS_MAP = [(1, 3, "var(--radius-sm)"), (4, 8, "var(--radius-md)"), (9, 12, "var(--radius-lg)")]

COLOR_MAP = [
    (re.compile(r"#ffffff\b", re.I), "var(--paper)"),
    (re.compile(r"#fff\b", re.I), "var(--paper)"),
    (re.compile(r"#fff8e7\b|#fff8ec\b|#fffdf8\b", re.I), "var(--paper-warm)"),
    (re.compile(r"#f5e9d4\b|#f5efe4\b|#f5ede0\b", re.I), "var(--paper-warm)"),
    (re.compile(r"#23201a\b", re.I), "var(--ink)"),
    (re.compile(r"#2c2418\b", re.I), "var(--ink)"),
    (re.compile(r"#6b5e4d\b|#6b6455\b", re.I), "var(--ink-soft)"),
]

TRANS_DUR = [(re.compile(r"(\b|,\s*)all\s+0?\.2s\b"), r"\1all var(--dur-base)"),
             (re.compile(r"(\b|,\s*)all\s+0?\.15s\b"), r"\1all var(--dur-fast)"),
             (re.compile(r"(?<![\d.])0?\.2s\b(?![\d])"), "var(--dur-base)"),
             (re.compile(r"(?<![\d.])0?\.15s\b(?![\d])"), "var(--dur-fast)")]

SHADOW_HARD = re.compile(r"box-shadow:\s*(0[^;]*rgba?\([^)]*\)[^;]*)", re.I)


def map_radius_val(m):
    val = m.group(1)
    def one(tok):
        tok = tok.strip()
        mm = re.fullmatch(r"(\d+)px", tok)
        if not mm:
            return tok
        n = int(mm.group(1))
        if n >= 999 or tok == "50%":
            return "var(--radius-pill)"
        for lo, hi, rep in RADIUS_MAP:
            if lo <= n <= hi:
                return rep
        return tok
    return "border-radius: " + " ".join(one(t) for t in val.split())


def shadow_repl(m, selector_ctx):
    val = m.group(1)
    if ":hover" in selector_ctx:
        return "box-shadow: var(--elev-2)"
    if re.search(r"tip|tooltip|popover|modal", selector_ctx, re.I):
        return "box-shadow: var(--elev-3)"
    if "rgba(0, 0, 0, 0.3" in val or "rgba(0,0,0,0.3" in val:
        return "box-shadow: var(--elev-3)"
    return "box-shadow: var(--elev-1)"


def private_blocks(html):
    """返回 [(start,end,text)] 页私有 style 块（排除 INLINED 块）。"""
    out = []
    for m in re.finditer(r"<style[^>]*>(.*?)</style>", html, re.S):
        body = m.group(1)
        if "INLINED CSS" in html[max(0, m.start() - 200):m.start()]:
            continue
        if "--elev-0: none" in body or "system.css — 详解西游记" in body:
            continue
        out.append((m.start(1), m.end(1), body))
    return out


def migrate_page(path, dry, stats):
    html = path.read_text(encoding="utf-8")
    counts = {"shadow": 0, "radius": 0, "trans": 0, "color": 0, "focus": 0}
    new_html = html
    for start, end, body in reversed(private_blocks(html)):
        nb = body
        # R-FOCUS
        nb, n = re.subn(r"var\(--focus-ring[^)]*\)", "color-mix(in srgb, var(--accent) 15%, transparent)", nb)
        counts["focus"] += n
        # R-SHADOW（带选择器上下文）
        def do_shadow(m):
            ctx = nb[max(0, nb.rfind("}", 0, m.start()) + 1 if nb.rfind("}", 0, m.start()) >= 0 else 0):m.start()]
            sel = nb[nb.rfind("\n", 0, m.start()) + 1:m.start()] if "\n" in nb[:m.start()] else ctx
            counts["shadow"] += 1
            return shadow_repl(m, ctx + sel)
        nb = SHADOW_HARD.sub(do_shadow, nb)
        # R-RADIUS
        nb, n = re.subn(r"border-radius:\s*([^;]+);", map_radius_val, nb)
        counts["radius"] += n
        # R-TRANS
        for pat, rep in TRANS_DUR:
            nb, n = pat.subn(rep, nb)
            counts["trans"] += n
        # 裸色白名单
        for pat, rep in COLOR_MAP:
            nb, n = pat.subn(rep, nb)
            counts["color"] += n
        # R-EXEMPT 登记：剩余裸 hex 数
        remaining = len(re.findall(r"#[0-9a-fA-F]{3,8}\b", nb)) + len(re.findall(r"\brgba?\(", nb))
        if remaining and "e-track-exempt" not in nb:
            nb = nb.replace("/* === 仅本页特有样式", f"/* e-track-exempt: chart-data-colors {remaining} 处 */\n        /* === 仅本页特有样式", 1)
            if "/* === 仅本页特有样式" not in nb:
                nb = f"/* e-track-exempt: chart-data-colors {remaining} 处 */\n" + nb
        counts["exempt"] = remaining
        if not dry:
            new_html = new_html[:start] + nb + new_html[end:]
        if dry:
            for line in nb.splitlines():
                if re.search(r"var\(--elev-|var\(--radius-|var\(--dur-|var\(--paper|var\(--ink|e-track-exempt", line):
                    print(f"    {path.name}: {line.strip()[:100]}")
    if not dry and new_html != html:
        path.write_text(new_html, encoding="utf-8")
    stats[path.name] = counts
    return counts


def main():
    pages = derive_list()
    print(f"[INFO] 待迁移 {len(pages)} 页（已排除试点 3 页）· DRY={DRY}")
    stats = {}
    for p in pages:
        migrate_page(p, DRY, stats)
    print("\n| 页 | R-SHADOW | R-RADIUS | R-TRANS | R-FOCUS | 裸色→令牌 | 豁免 N |")
    print("|:---|:---|:---|:---|:---|:---|:---|")
    for name, c in sorted(stats.items()):
        print(f"| {name} | {c['shadow']} | {c['radius']} | {c['trans']} | {c['focus']} | {c['color']} | {c.get('exempt', 0)} |")


if __name__ == "__main__":
    main()
