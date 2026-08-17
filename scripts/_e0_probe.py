#!/usr/bin/env python3
"""E0 探针（Phase W476 · 一次性诊断脚本，不入门禁/CI）

P1 全站页面内联 <style> 裸色计数（hex/rgb()/rgba()/hsl()，排除 SVG fill 属性内的数据色登记另计）
P2 transition 时长形态统计（all  shorthand / 秒值分布）
P3 9 根页 hero/nav/footer 结构一致性（关键标记存在性矩阵）
P6 页面 <style> 公共组件选择器重复计数（.hero/.topnav/.site-footer/.kpi-card/.section 等）

用法：python scripts/_e0_probe.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"

STYLE_RE = re.compile(r"<style[^>]*>(.*?)</style>", re.S | re.I)
HEX_RE = re.compile(r"#[0-9a-fA-F]{3,8}\b")
RGB_RE = re.compile(r"\brgba?\(")
HSL_RE = re.compile(r"\bhsla?\(")
TRANS_RE = re.compile(r"transition\s*:[^;}]*", re.I)
ALL_RE = re.compile(r"\ball\b")
SEC_RE = re.compile(r"(\d+(?:\.\d+)?)\s*s\b")
MS_RE = re.compile(r"(\d+(?:\.\d+)?)\s*ms\b")
VAR_RE = re.compile(r"var\(--dur")

COMMON_SELECTORS = [".hero", ".topnav", ".site-footer", ".kpi-card", ".section", ".chart-tooltip", ".card", "footer"]

ROOT_PAGES = ["index.html", "dashboard.html", "curated.html", "tag-cloud.html", "search.html",
              "data-explorer.html", "dukou-engine.html", "academic-papers.html", "characters.html"]


def collect_pages():
    pages = []
    for p in sorted(SITE.glob("*.html")):
        pages.append(p)
    for p in sorted((SITE / "data").glob("*.html")):
        if p.name != "_shell.html":
            pages.append(p)
    for p in sorted((SITE / "en").glob("*.html")):
        pages.append(p)
    return pages


def main():
    pages = collect_pages()
    print(f"扫描页数：{len(pages)}（site 根 + data + en）\n")

    # ---- P1 裸色计数 ----
    total_hex = total_rgb = total_hsl = 0
    pages_with_hex = 0
    top_pages = []
    for p in pages:
        styles = "".join(STYLE_RE.findall(p.read_text(encoding="utf-8", errors="ignore")))
        h = len(HEX_RE.findall(styles))
        r = len(RGB_RE.findall(styles))
        s = len(HSL_RE.findall(styles))
        total_hex += h
        total_rgb += r
        total_hsl += s
        if h:
            pages_with_hex += 1
            top_pages.append((h + r + s, str(p.relative_to(ROOT))))
    print("== P1 页面 <style> 裸色计数 ==")
    print(f"hex 总数 {total_hex} · rgb()/rgba() 总数 {total_rgb} · hsl() 总数 {total_hsl}")
    print(f"含裸 hex 的页数 {pages_with_hex}/{len(pages)}")
    top_pages.sort(reverse=True)
    print("裸色最多前 10 页：")
    for n, rel in top_pages[:10]:
        print(f"  {n:4d}  {rel}")

    # ---- P2 transition 形态 ----
    t_all = t_var = t_sec = t_ms = t_plain = 0
    sec_vals = {}
    pages_trans = 0
    for p in pages:
        styles = "".join(STYLE_RE.findall(p.read_text(encoding="utf-8", errors="ignore")))
        ts = TRANS_RE.findall(styles)
        if ts:
            pages_trans += 1
        for t in ts:
            if ALL_RE.search(t):
                t_all += 1
            if VAR_RE.search(t):
                t_var += 1
            for v in SEC_RE.findall(t):
                t_sec += 1
                sec_vals[v] = sec_vals.get(v, 0) + 1
            t_ms += len(MS_RE.findall(t))
            if not (ALL_RE.search(t) or VAR_RE.search(t) or SEC_RE.search(t) or MS_RE.search(t)):
                t_plain += 1
    print("\n== P2 transition 形态 ==")
    print(f"含 transition 声明的页数 {pages_trans}/{len(pages)}")
    print(f"transition: all 形态 {t_all} · var(--dur-*) 形态 {t_var} · 秒值 {t_sec} · 毫秒值 {t_ms}")
    print("秒值分布 top8:", sorted(sec_vals.items(), key=lambda kv: -kv[1])[:8])

    # ---- P3 根页结构一致性 ----
    print("\n== P3 根页 hero/nav/footer 标记矩阵 ==")
    marks = ["class=\"hero\"", "class=\"topnav\"", "site-footer", "gen-time", "class=\"container\"", "footer-meta"]
    header = "页面".ljust(28) + "".join(m[:12].ljust(13) for m in marks)
    print(header)
    for name in ROOT_PAGES:
        p = SITE / name
        if not p.exists():
            print(f"{name}  <不存在>")
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        row = name.ljust(28)
        for m in marks:
            row += ("Y" if m in text else "-").ljust(13)
        print(row)

    # ---- P6 公共选择器重复 ----
    print("\n== P6 页面 <style> 公共组件选择器重复（定义页数） ==")
    for sel in COMMON_SELECTORS:
        cnt = 0
        for p in pages:
            styles = "".join(STYLE_RE.findall(p.read_text(encoding="utf-8", errors="ignore")))
            if re.search(re.escape(sel) + r"[\s{:,\[]", styles):
                cnt += 1
        print(f"  {sel:18s} 出现在 {cnt} 页的内联 <style>")


if __name__ == "__main__":
    main()
