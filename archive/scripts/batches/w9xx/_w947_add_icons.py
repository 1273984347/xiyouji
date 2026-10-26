#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""W947 · 通用图标集补 2 枚（便签 note / 链条 link）

背景：核验发现两处此前遗漏的**界面图标位**——
  · agent-web PermissionDialog 的 📝（纯图标 span）· InlinePermissionCard 的 ⚠️（图标 + 文字标题）
  · site/static/js/rag-chat.js 的 🔗（图谱三元组前缀）
warn（⚠ 警示三角）已在通用集内，只需补 note 与 link 两枚。
规格同通用集：24×24 / stroke 1.5 / round cap+join / fill:none / stroke:currentColor。
用法：py -3 scripts/_w947_add_icons.py
"""
from __future__ import annotations

import pathlib

HEAD = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" '
        'stroke="currentColor" stroke-width="1.5" stroke-linecap="round" '
        'stroke-linejoin="round" aria-hidden="true">')

NEW = {
    "note": ("便签与文档（折角纸页）",
             "M6 3.6h8l4 4v12.8H6zM14 3.6v4h4M9.2 12h5.6M9.2 15.4h3.6"),
    "link": ("链接（双环相扣）",
             "M9.7 14.3a3.5 3.5 0 0 0 5 0l2.6-2.6a3.5 3.5 0 0 0-5-5l-1.3 1.3M14.3 9.7a3.5 3.5 0 0 0-5 0l-2.6 2.6a3.5 3.5 0 0 0 5 5l1.3-1.3"),
}

GEN = pathlib.Path("scripts/_w939_gen_icons.py")
OUT = pathlib.Path("site/static/icons/ui")


def main() -> int:
    # 1) 写图标文件
    for name, (desc, d) in NEW.items():
        svg = f'{HEAD}\n  <path d="{d}"/>\n</svg>\n'
        (OUT / f"{name}.svg").write_text(svg, encoding="utf-8")
        print(f"  {name:8s} {len(svg):4d}B  {desc}")

    # 2) 并入生成器（保持生成器为唯一事实源）
    src = GEN.read_text(encoding="utf-8")
    if '"note":' not in src:
        anchor = '    "menu": ('
        block = ('    "note": ("便签与文档（折角纸页）",\n'
                 '             "M6 3.6h8l4 4v12.8H6zM14 3.6v4h4M9.2 12h5.6M9.2 15.4h3.6"),\n'
                 '    "link": ("链接（双环相扣）",\n'
                 '             "M9.7 14.3a3.5 3.5 0 0 0 5 0l2.6-2.6a3.5 3.5 0 0 0-5-5l-1.3 1.3M14.3 9.7a3.5 3.5 0 0 0-5 0l-2.6 2.6a3.5 3.5 0 0 0 5 5l1.3-1.3"),\n')
        src = src.replace(anchor, block + anchor, 1)
        GEN.write_text(src, encoding="utf-8")
        print(f"  生成器已并入 2 枚 → {GEN}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
