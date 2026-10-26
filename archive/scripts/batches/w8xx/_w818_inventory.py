#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_w818_inventory.py — 静态站现状盘点 + 候选技术生态数据（W818 取证脚本·一次性诊断件·不入 CI）。

用途：为本仓《静态站前端框架化选型对比》报告（docs/11-方案报告/静态站前端框架化选型对比-2026-10-20.md）
      §3 现状盘点 与 §5.1/§5.5 生态数据 提供**可复算**的一次性取证。

用法：
    py -3 scripts/_w818_inventory.py                # 现状盘点（仅标准库·零网络·零依赖）
    py -3 scripts/_w818_inventory.py --ecosystem    # 追加 npm registry + GitHub API 一手数据（需联网）

设计约束（仓内纪律）：
  · 仅用标准库；不开网络（除非显式 --ecosystem）；不写仓内任何文件（只读）。
  · 结论数字以本脚本实跑输出为准，禁从旧文档复制（文档规范 §4.9「数字当批现测」）。
"""
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
DATA = SITE / "data"

RE_STYLE = re.compile(r"<style\b[^>]*>", re.I)
RE_SCRIPT_INLINE = re.compile(r"<script\b(?![^>]*\bsrc=)[^>]*>", re.I)
RE_SCRIPT_SRC = re.compile(r"<script\b[^>]*\bsrc=[\"']([^\"']+)[\"']", re.I)
RE_CSP = re.compile(r"<meta\b[^>]*http-equiv=[\"']Content-Security-Policy[\"']", re.I)
RE_LINK_CSS = re.compile(r"<link\b[^>]*rel=[\"']stylesheet[\"'][^>]*>", re.I)
RE_EMBEDDED = re.compile(r"EMBEDDED", re.I)
RE_FETCH = re.compile(r"\bfetch\s*\(", re.I)
RE_MODULE = re.compile(r"<script\b[^>]*type=[\"']module[\"']", re.I)
RE_INLINE_HANDLER = re.compile(r"\son[a-z]+\s*=", re.I)

NPM_PKGS = ["vite", "react", "react-dom", "astro", "@astrojs/react", "lit",
            "vite-plugin-singlefile", "@11ty/eleventy", "svelte", "typescript"]
GH_REPOS = ["vitejs/vite", "facebook/react", "withastro/astro", "lit/lit",
            "11ty/eleventy", "sveltejs/svelte", "vitejs/vite-plugin-singlefile"]
UA = {"User-Agent": "xiyouji-w818-inventory"}


def site_inventory():
    """site/ 页面资产盘点：体量分布 · 内联结构 · 数据回退形态 · 本地化依赖体积。"""
    rows = []
    for p in sorted(DATA.glob("*.html")):
        txt = p.read_text(encoding="utf-8", errors="replace")
        rows.append({
            "file": p.name,
            "bytes": p.stat().st_size,
            "style_blocks": len(RE_STYLE.findall(txt)),
            "script_inline": len(RE_SCRIPT_INLINE.findall(txt)),
            "script_src": len(RE_SCRIPT_SRC.findall(txt)),
            "link_css": len(RE_LINK_CSS.findall(txt)),
            "csp_meta": len(RE_CSP.findall(txt)),
            "embedded": len(RE_EMBEDDED.findall(txt)),
            "fetch": len(RE_FETCH.findall(txt)),
            "module": len(RE_MODULE.findall(txt)),
            "inline_handler": len(RE_INLINE_HANDLER.findall(txt)),
        })
    n = len(rows)
    sizes = sorted(r["bytes"] for r in rows)
    total = sum(sizes)
    # 极值页名：直接按行取（不可用 sizes 的下标回查 rows——sizes 已排序而 rows 未排序·下标错配）
    max_row = max(rows, key=lambda r: r["bytes"])
    min_row = min(rows, key=lambda r: r["bytes"])
    buckets = {"<60KB": 0, "60-100KB": 0, "100-150KB": 0, ">=150KB": 0}
    for s in sizes:
        kb = s / 1024
        buckets["<60KB" if kb < 60 else "60-100KB" if kb < 100 else "100-150KB" if kb < 150 else ">=150KB"] += 1

    def count_dir(rel):
        return len(list((SITE / rel).glob("*.html"))) if (SITE / rel).exists() else 0

    all_html = [p for p in SITE.rglob("*.html")]
    print("=== A. site/data %d 页体量 ===" % n)
    print("  合计 = %d B (%.2f MB) · 均值 = %d B (%.1f KB) · 中位 = %d B (%.1f KB)"
          % (total, total / 1048576.0, total / n, total / n / 1024.0, sizes[n // 2], sizes[n // 2] / 1024.0))
    print("  最大 = %d B (%s) · 最小 = %d B (%s)"
          % (sizes[-1], max_row["file"], sizes[0], min_row["file"]))
    print("  分档: " + " · ".join("%s=%d 页" % (k, v) for k, v in buckets.items()))
    print()
    print("=== B. 内联结构（合计 / 含该形态页数）===")
    for key, label in (("style_blocks", "内联 <style> 块"), ("script_inline", "内联 <script> 块"),
                       ("script_src", "外链 <script src>"), ("link_css", "<link rel=stylesheet>"),
                       ("csp_meta", "CSP meta 标签"), ("module", "type=module 脚本"),
                       ("inline_handler", "on* 内联事件属性")):
        vals = [r[key] for r in rows]
        print("  %-22s 合计=%-5d 页数=%-4d 单页最多=%d"
              % (label, sum(vals), sum(1 for v in vals if v > 0), max(vals)))
    print()
    print("=== C. 数据回退形态 ===")
    both = sum(1 for r in rows if r["embedded"] > 0 and r["fetch"] > 0)
    print("  含 EMBEDDED = %d/%d 页 · 含 fetch = %d/%d 页 · 双态 = %d 页"
          % (sum(1 for r in rows if r["embedded"] > 0), n,
             sum(1 for r in rows if r["fetch"] > 0), n, both))
    print()
    print("=== D. 站点目录构成 ===")
    reader_dir = SITE / "reader"
    reader_html = list(reader_dir.rglob("*.html")) if reader_dir.exists() else []  # 递归·含子目录（culture/essays/people/poetry/themes）
    print("  site/data = %d 页 · site/en = %d 页 · site/reader = %d 页（递归）· site 根 = %d 页 · 全站 = %d 页"
          % (n, count_dir("en"), len(reader_html),
             count_dir("."), len(all_html)))
    reader_bytes = sum(p.stat().st_size for p in reader_html)
    print("  site/reader 总体积 = %d B (%.2f MB)" % (reader_bytes, reader_bytes / 1048576.0))
    print("  site 全站 HTML 总体积 = %d B (%.2f MB)"
          % (sum(p.stat().st_size for p in all_html), sum(p.stat().st_size for p in all_html) / 1048576.0))
    print()
    print("=== E. 本地化依赖体积（零外域依赖资产）===")
    for f in sorted((SITE / "static" / "js").glob("*"), key=lambda x: -x.stat().st_size):
        if f.is_file():
            print("  %-28s %d B (%.1f KB)" % (f.name, f.stat().st_size, f.stat().st_size / 1024.0))
    return {"pages_data": n, "total_bytes": total, "avg_bytes": int(total / n),
            "median_bytes": sizes[n // 2], "max_bytes": sizes[-1], "min_bytes": sizes[0],
            "buckets": buckets, "site_all_html": len(all_html)}


def _get_json(url, timeout=45):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8", errors="replace"))


def ecosystem():
    """npm registry + GitHub API 一手数据：版本 / 发布日期 / 许可 / 近周下载 / stars / 最后 push。"""
    print("=== F. npm registry 一手数据 ===")
    print("%-26s %-12s %-12s %-14s %s" % ("包", "最新版本", "最后发布", "许可", "近周下载"))
    for pkg in NPM_PKGS:
        ver = lic = pub = dl = "-"
        try:
            latest = _get_json("https://registry.npmjs.org/%s/latest" % pkg.replace("/", "%2f"))
            ver = latest.get("version", "-")
            lic = latest.get("license") or (latest.get("licenses") or [{}])[0].get("type") or "-"
        except Exception as exc:  # noqa: BLE001
            lic = "ERR:%s" % type(exc).__name__
        try:
            pack = _get_json("https://registry.npmjs.org/%s" % pkg.replace("/", "%2f"))
            pub = (pack.get("time", {}).get(ver) or "")[:10] or "-"
        except Exception:  # noqa: BLE001
            pass
        try:
            dl = _get_json("https://api.npmjs.org/downloads/point/last-week/%s" % pkg.replace("/", "%2f")).get("downloads", "-")
        except Exception:  # noqa: BLE001
            pass
        print("%-26s %-12s %-12s %-14s %s" % (pkg, ver, pub, str(lic)[:14], dl))
    print()
    print("=== G. GitHub 一手数据 ===")
    print("%-34s %-9s %-10s %-22s %s" % ("仓库", "stars", "forks", "最后 push", "license"))
    for repo in GH_REPOS:
        try:
            d = _get_json("https://api.github.com/repos/%s" % repo)
            print("%-34s %-9s %-10s %-22s %s" % (repo, d.get("stargazers_count"), d.get("forks_count"),
                                                  (d.get("pushed_at") or "-")[:19], (d.get("license") or {}).get("spdx_id")))
        except Exception as exc:  # noqa: BLE001
            print("%-34s ERR:%s" % (repo, exc))


def main():
    site_inventory()
    if "--ecosystem" in sys.argv:
        ecosystem()
    else:
        print("（追加生态数据：py -3 scripts/_w818_inventory.py --ecosystem）")


if __name__ == "__main__":
    main()
