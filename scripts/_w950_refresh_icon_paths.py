#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""W950 · 图标图形刷新器（把打磨后的新图形同步到全仓已内联的 SVG）

匹配键 = (d, transform, fill) 复合键——单靠 d 有三组歧义
（scroll/tl-scroll、star/star-solid、thumb-up/thumb-down）⇒ 必须带 transform 与 fill 区分。

同步面：A 通用集内联 SVG · B timeline 的 TL_ICO 映射块 · C agent-web UiIcons.tsx
用法：py -3 scripts/_w950_refresh_icon_paths.py [--dry]
"""
from __future__ import annotations

import argparse
import pathlib
import re
import subprocess
import sys
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parent.parent
ICON_DIR = ROOT / "site" / "static" / "icons" / "ui"


def parse_body(body: str) -> tuple[str, str, str]:
    """从 path 属性串取出 (d, transform, fill)"""
    d = re.search(r'd="([^"]+)"', body)
    tr = re.search(r'transform="([^"]+)"', body)
    fl = re.search(r'fill="([^"]+)"', body)
    return (d.group(1) if d else "",
            tr.group(1) if tr else "",
            fl.group(1) if fl else "")


def key(d: str, tr: str, fl: str) -> str:
    return f"{d}||{tr}||{fl}"


def git_old_assets() -> dict[str, str]:
    """HEAD 旧资产的复合键 → 图标名"""
    per_key = defaultdict(list)
    names = subprocess.run(["git", "ls-tree", "--name-only", "HEAD", "site/static/icons/ui/"],
                           capture_output=True, text=True, encoding="utf-8").stdout.split()
    for n in names:
        base = pathlib.Path(n).name
        if not base.endswith(".svg"):
            continue
        r = subprocess.run(["git", "show", f"HEAD:site/static/icons/ui/{base}"],
                           capture_output=True, text=True, encoding="utf-8")
        if r.returncode != 0:
            continue
        m = re.search(r"<path ([^/]+)/>", r.stdout)
        if m:
            d, tr, fl = parse_body(m.group(1))
            per_key[key(d, tr, fl)].append(base[:-4])
    dup = {k: v for k, v in per_key.items() if len(v) > 1}
    if dup:
        print(f"  ⚠ 复合键仍有歧义 {len(dup)} 组：{list(dup.values())[:3]}")
    return {k: v[0] for k, v in per_key.items()}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args()

    old_map = git_old_assets()
    print(f"HEAD 旧资产复合键 → 图标名 映射 {len(old_map)} 条")

    new_by_name = {}
    for p in sorted(ICON_DIR.glob("*.svg")):
        raw = p.read_text(encoding="utf-8")
        m = re.search(r"<path ([^/]+)/>", raw)
        d, tr, fl = parse_body(m.group(1))
        new_by_name[p.stem] = (d, tr, fl)

    targets = []
    for root in ["site", "xiyouji-agent-web/src"]:
        for p in sorted((ROOT / root).rglob("*")):
            if p.is_file() and p.suffix.lower() in {".html", ".js", ".tsx", ".ts", ".mjs", ".cjs"}:
                targets.append(p)

    total_a = files_a = 0
    for p in targets:
        text = p.read_text(encoding="utf-8")
        orig = text
        cnt = [0]

        def repl(m):
            d = m.group(1)
            tr = m.group(2) or ""
            trm = re.search(r'transform="([^"]+)"', tr)
            flm = re.search(r'fill="([^"]+)"', tr)
            k = key(d, trm.group(1) if trm else "", flm.group(1) if flm else "")
            name = old_map.get(k)
            if not name:
                return m.group(0)
            cnt[0] += 1
            nd, ntr, nfl = new_by_name[name]
            tr_out = f' transform="{ntr}"' if ntr else ""
            fl_out = f' fill="{nfl}"' if nfl else ""
            return f'<path d="{nd}"{tr_out}{fl_out}/>'

        text = re.sub(r'<path d="([^"]+)"((?:[^>"]|"[^"]*")*?)/>', repl, text)
        if text != orig:
            total_a += cnt[0]
            files_a += 1
            if not args.dry:
                p.write_text(text, encoding="utf-8")
    print(f"A) 内联 SVG path 同步 {total_a} 处 · 改动 {files_a} 个文件")

    mapping_js = (ROOT / "scripts" / "output" / "_w946_timeline_icons.js").read_text(encoding="utf-8")
    total_b = 0
    for p in targets:
        text = p.read_text(encoding="utf-8")
        if "var TL_ICO" not in text:
            continue
        new_text, n = re.subn(r"var TL_ICO = \{.*?\n\};", mapping_js.strip(), text, count=1, flags=re.S)
        if n and new_text != text:
            total_b += 1
            if not args.dry:
                p.write_text(new_text, encoding="utf-8")
    print(f"B) TL_ICO 映射块同步 {total_b} 处")

    ui = ROOT / "xiyouji-agent-web" / "src" / "components" / "UiIcons.tsx"
    total_c = 0
    if ui.exists():
        text = ui.read_text(encoding="utf-8")
        orig = text
        for cand in ("note", "link", "warn"):
            nd, ntr, nfl = new_by_name[cand]
            pat = re.compile(r'd="' + re.escape(nd) + r'"')
            if not pat.search(text):
                # 旧 d（未重画或已改）→ 也要同步：按图标名定位函数体
                continue
            if ntr:
                nums = [x.strip() for x in ntr.replace(",", " ").split()]
                text = pat.sub(
                    f'<g transform="translate({nums[0]} {nums[1]}) scale({nums[2]})">'
                    f'<path d="{nd}" /></g>', text, count=1)
            total_c += 1
        if text != orig:
            if not args.dry:
                ui.write_text(text, encoding="utf-8")
            print(f"C) UiIcons.tsx 同步 {total_c} 处")

    if args.dry:
        print("[DRY] 未写盘")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        import traceback
        traceback.print_exc()
        sys.exit(2)
