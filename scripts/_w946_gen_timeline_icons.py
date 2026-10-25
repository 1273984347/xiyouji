#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""W946 · 时间线专属图标集（16 枚·东方线描）

与 W939 的通用 UI 图标集分开：通用集按「功能」设计（搜索/播放/关闭…），
本集按「事件语义」设计——时间线的 emoji 是一符多义的粗粒度标记
（📖 同时表示「佛经西行」与「连环画普及」），故必须按语义而非按字符拆分。

规格同通用集：24×24 viewBox / stroke 1.5 / round cap+join / fill:none / stroke:currentColor。
产出：site/static/icons/ui/tl-*.svg + scripts/output/_w946_timeline_icons.js（ICO 映射·供 timeline 页内联）
用法：py -3 scripts/_w946_gen_timeline_icons.py
"""
from __future__ import annotations

import json
import pathlib

HEAD = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" '
        'stroke="currentColor" stroke-width="1.5" stroke-linecap="round" '
        'stroke-linejoin="round" aria-hidden="true">')
TAIL = "</svg>\n"

# name -> (语义, 路径 d)
ICONS: dict[str, tuple[str, str]] = {
    # —— 成书与纪实 ——
    "tl-pilgrim": ("玄奘西行（行脚僧·背经卷·持杖·日轮）",
                   "M8.4 6.9a1.8 1.8 0 1 0 0 3.6 1.8 1.8 0 0 0 0-3.6zM8.4 10.5v4.6l-1.7 4.6M8.4 15.1l1.8 4.6M10 8.6l3.6 1.5-1.3 3-3.6-1.5zM12.2 8.2v9.4M17.4 6.2a2.1 2.1 0 1 0 .01 0M19.8 12.4l2.6-1.8M14.8 12.4l-2.4-1.6"),
    "tl-scroll": ("大唐西域记（立轴·复用通用 scroll 形态·保留独立名以对齐事件语义）",
                  "M5.8 4.4h12.4a1.6 1.6 0 0 1 0 3.2H5.8a1.6 1.6 0 0 1 0-3.2zM5.8 16.4h12.4a1.6 1.6 0 0 1 0 3.2H5.8a1.6 1.6 0 0 1 0-3.2zM7.4 7.6v8.8M16.6 7.6v8.8"),
    "tl-star-spark": ("取经诗话（灵光初现·星芒）",
                      "M12 3.2l1.5 4.6 4.6 1.5-4.6 1.5L12 15.4l-1.5-4.6L5.9 9.3l4.6-1.5zM18.4 15.2l.7 2.1 2.1.7-2.1.7-.7 2.1-.7-2.1-2.1-.7 2.1-.7z"),
    "tl-mask": ("戏曲与影视演出（脸谱·眉眼与口）",
                "M12 3.4c4.4 0 7.6 2.6 7.6 7.2 0 5.4-3.4 9.9-7.6 9.9S4.4 16 4.4 10.6c0-4.6 3.2-7.2 7.6-7.2zM8.6 9.4c.7-.8 1.9-.8 2.6 0M12.8 9.4c.7-.8 1.9-.8 2.6 0M9.8 15.2c1.4.9 3 .9 4.4 0"),
    # —— 版本与评点 ——
    "tl-codex": ("世德堂百回本（厚册·书签带）",
                 "M6.4 3.6h9.2a2 2 0 0 1 2 2v14.8H8.4a2 2 0 0 1-2-2zM17.6 7.2h1.8a.8.8 0 0 1 .8.8v10.4a1.6 1.6 0 0 1-1.6 1.6H8.4M12 6.4h2.2v3.6H12z"),
    "tl-taiji": ("丹道评点（太极·阴阳鱼）",
                 "M12 3.4a8.6 8.6 0 1 0 0 17.2 8.6 8.6 0 0 0 0-17.2zM12 3.4a4.3 4.3 0 0 1 0 8.6 4.3 4.3 0 0 0 0 8.6M12 12h.01"),
    "tl-critical-edition": ("现代整理校注本（叠册·校注符）",
                            "M4.4 5.2h6.2v13.6H4.4zM10.6 5.2h6.2v13.6h-6.2M16.8 5.2h2.8v13.6h-2.8M7.5 8.4v6M13.7 8.4v6M6.6 12h1.8"),
    "tl-brush-comment": ("评点笺注（笔与点）",
                         "M5 19.4l1.2-4.2L15 6.4a1.9 1.9 0 0 1 2.7 2.7L8.9 17.7zM14 7.4l2.7 2.7M3.6 21h4"),
    "tl-punctuation": ("新式标点排印（逗号·句号·引号）",
                       "M6.2 9.2c1 0 1.6.6 1.6 1.5 0 .9-.8 1.6-1.8 2M12.6 12.4a1 1 0 1 0 .01 0M17 6.4v3.4M19.8 6.4v3.4"),
    "tl-pencil": ("校注修订（笔尖与批注线）",
                  "M4.4 19.6l1-3.8L14.2 7a1.8 1.8 0 0 1 2.6 2.6l-8.8 8.8zM13.2 8l2.6 2.6M8 14.8h6.4M8 17.6h4.4"),
    "tl-database": ("古籍数字化（数据层叠·检索环）",
                    "M12 3.4c3.9 0 7 1.2 7 2.6s-3.1 2.6-7 2.6-7-1.2-7-2.6 3.1-2.6 7-2.6zM5 6v12c0 1.4 3.1 2.6 7 2.6s7-1.2 7-2.6V6M5 12c0 1.4 3.1 2.6 7 2.6s7-1.2 7-2.6"),
    # —— 传播与改编 ——
    "tl-comic": ("连环画普及（画格连环）",
                 "M3.6 6.4h7.2v6.2H3.6zM13.2 6.4h7.2v6.2h-7.2zM3.6 15.2h7.2v4.4H3.6zM13.2 15.2h7.2v4.4h-7.2z"),
    "tl-newyear-print": ("清代年画（门神轴·画框）",
                          "M6.6 3.6h10.8v16.8H6.6zM9 6.4h6v5.2H9zM9 14.2c.9-1.4 2-2.1 3-2.1s2.1.7 3 2.1M12 17.4v.01"),
    "tl-film": ("电影（胶片与片门）",
                "M3.6 5.4h16.8v13.2H3.6zM3.6 9.2h16.8M3.6 14.8h16.8M7.6 5.4v3.8M12 5.4v3.8M16.4 5.4v3.8M7.6 14.8v3.8M12 14.8v3.8M16.4 14.8v3.8"),
    "tl-tv": ("电视剧（显像管·天线）",
              "M3.6 7.4h16.8v10.2H3.6zM8.4 20.4h7.2M12 17.6v2.8M8.4 10.8h7.2v3.6H8.4zM8.4 7.4l3.6-4M15.6 7.4l-3.6-4"),
    "tl-gamepad": ("游戏与网文（手柄·十字键）",
                   "M7.4 8.4h9.2a4.6 4.6 0 0 1 4.5 5.6l-.6 3a2.2 2.2 0 0 1-4 .6l-1.6-2.4H9.1l-1.6 2.4a2.2 2.2 0 0 1-4-.6l-.6-3a4.6 4.6 0 0 1 4.5-5.6zM8 11.4v4M6 13.4h4M15 12.4v.01M17.2 14.4v.01"),
}


def main() -> int:
    out = pathlib.Path("site/static/icons/ui")
    out.mkdir(parents=True, exist_ok=True)
    mapping = {}
    for name, (desc, d) in ICONS.items():
        svg = f'{HEAD}\n  <path d="{d}"/>\n{TAIL}'
        (out / f"{name}.svg").write_text(svg, encoding="utf-8")
        # 映射里的 SVG 须带 class="ico"（吃 .ico 基类的尺寸与描边参数）与完整 fill/stroke 属性
        mapping[name] = svg.replace("\n", "").replace("  ", "").replace(
            "<svg ", '<svg class="ico" ')
        print(f"{name:22s} {len(svg):4d}B  {desc}")
    print(f"\n共 {len(ICONS)} 枚 → {out}")

    # 供 timeline 页内联的 ICO 映射（JS 字面量）
    # ⚠️ 图标名含连字符（tl-critical-edition）⇒ 对象键必须加引号，否则 JS 语法错误
    js = ["// W946 · 时间线专属图标映射（由 scripts/_w946_gen_timeline_icons.py 生成·勿手改）",
          "var TL_ICO = {"]
    for name in ICONS:
        js.append(f"  '{name}': '{mapping[name]}',")
    js.append("};")
    jsp = pathlib.Path("scripts/output/_w946_timeline_icons.js")
    jsp.write_text("\n".join(js) + "\n", encoding="utf-8")
    print(f"映射表 → {jsp}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
