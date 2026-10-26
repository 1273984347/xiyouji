#!/usr/bin/env python3
"""W926 证据提取器（只读）——把扫描结果里的可疑判定逐条实证到「文件是否存在」层面。

输出：scripts/output/_w926_ia_evidence.json + 控制台摘要
用法：py -3 scripts/_w926_ia_extract.py
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
OUT = ROOT / "scripts" / "output" / "_w926_ia_evidence.json"

A_TAG = re.compile(r'<a\b([^>]*)>(.*?)</a>', re.S | re.I)
ATTR_HREF = re.compile(r'href\s*=\s*"([^"]*)"', re.I)
ATTR_DOWNLOAD = re.compile(r'\bdownload\b', re.I)
FETCH_REL = re.compile(r"""fetch\s*\(\s*['"]([^'"]+)['"]""")
SITEMAP_LOC = re.compile(r"<loc>([^<]+)</loc>")


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def main() -> int:
    html_files = sorted(SITE.rglob("*.html"))
    dl_links: list[dict] = []
    dir_links: list[dict] = []
    fetch_targets: list[dict] = []

    for f in html_files:
        rel = f.relative_to(SITE).as_posix()
        h = read(f)
        for attrs, inner in A_TAG.findall(h):
            hm = ATTR_HREF.search(attrs)
            if not hm:
                continue
            href = hm.group(1).strip()
            if not href or href.startswith(("http://", "https://", "//", "mailto:", "javascript:", "data:", "#")):
                continue
            target = href.split("#")[0].split("?")[0]
            if not target:
                continue
            tgt = (f.parent / target).resolve()
            try:
                rel_tgt = tgt.relative_to(SITE.resolve()).as_posix()
            except ValueError:
                rel_tgt = str(tgt)
            exists = tgt.exists()
            is_dir = tgt.is_dir()
            rec = {"page": rel, "href": href, "text": re.sub(r"<[^>]+>", "", inner).strip()[:40],
                   "resolved": rel_tgt, "exists": exists, "is_dir": is_dir}
            if is_dir:
                rec["dir_has_index"] = (tgt / "index.html").exists()
                dir_links.append(rec)
            elif not exists and ATTR_DOWNLOAD.search(attrs):
                dl_links.append(rec)
            elif not exists:
                dl_links.append(rec)
        for m in FETCH_REL.finditer(h):
            u = m.group(1)
            if u.startswith(("http://", "https://", "//", "data:")):
                continue
            tgt = (f.parent / u.split("?")[0]).resolve()
            try:
                rel_tgt = tgt.relative_to(SITE.resolve()).as_posix()
            except ValueError:
                rel_tgt = str(tgt)
            fetch_targets.append({"page": rel, "url": u, "resolved": rel_tgt, "exists": tgt.exists()})

    # sitemap 覆盖
    sitemap = SITE / "sitemap.xml"
    locs: set[str] = set()
    if sitemap.exists():
        for m in SITEMAP_LOC.finditer(read(sitemap)):
            u = m.group(1).strip()
            locs.add(u)

    # 关键 hub 页的出链
    hubs = {}
    for hub in ("index.html", "guide.html", "dashboard.html", "curated.html",
                "reader/index.html", "reader/themes-hub.html", "reader/themes/index.html",
                "reader/poetry/index.html", "reader/essays/index.html",
                "data/index.html", "en/index.html"):
        p = SITE / hub
        if not p.exists():
            hubs[hub] = {"exists": False}
            continue
        h = read(p)
        hrefs = [ATTR_HREF.search(a).group(1) for a, _ in A_TAG.findall(h) if ATTR_HREF.search(a)]
        hubs[hub] = {"exists": True, "bytes": len(h.encode("utf-8")), "n_links": len(hrefs),
                     "links": sorted(set(hrefs))[:400]}

    # 不可达页是否在 sitemap
    audit = json.loads((ROOT / "scripts" / "output" / "_w926_ia_audit.json").read_text(encoding="utf-8"))
    unreachable = audit["A_paths"]["unreachable_from_index"]
    unreachable_sitemap = {p: any(p.split("/")[-1] in loc for loc in locs) for p in unreachable}

    evidence = {
        "download_link_dead": dl_links,
        "download_link_dead_count": len(dl_links),
        "download_link_pages": sorted({d["page"] for d in dl_links}),
        "dir_links": dir_links,
        "fetch_targets_missing": [f for f in fetch_targets if not f["exists"]],
        "fetch_targets_missing_count": sum(1 for f in fetch_targets if not f["exists"]),
        "fetch_targets_total": len(fetch_targets),
        "sitemap_locs": len(locs),
        "unreachable_in_sitemap": unreachable_sitemap,
        "hubs": hubs,
    }
    OUT.write_text(json.dumps(evidence, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"[证据提取] {OUT}")
    print(f"  死链型 <a> 目标缺失：{len(dl_links)} 条 / 涉及 {len(evidence['download_link_pages'])} 页")
    print(f"  fetch 相对目标缺失：{evidence['fetch_targets_missing_count']} / {len(fetch_targets)}")
    print(f"  目录型链接：{len(dir_links)} 条（其中无 index.html 的目录 {sum(1 for d in dir_links if not d.get('dir_has_index'))}）")
    print(f"  sitemap locs：{len(locs)}")
    print("  —— 缺失 fetch 目标（前 25）——")
    for f in evidence["fetch_targets_missing"][:25]:
        print(f"    {f['page']} -> {f['url']}  ({f['resolved']})")
    print("  —— 目录链接 ——")
    for d in dir_links[:20]:
        print(f"    {d['page']} -> {d['href']}  exists={d['exists']} has_index={d.get('dir_has_index')}")
    print("  —— 不可达页是否在 sitemap ——")
    for p, v in unreachable_sitemap.items():
        print(f"    {p}: in_sitemap={v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
