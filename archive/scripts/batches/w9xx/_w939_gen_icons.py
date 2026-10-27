#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""W941 · 东方线描图标集生成器

产出 site/static/icons/ui/<name>.svg（26 枚·设计资产单一事实源）
规格：24×24 viewBox · stroke 1.6 · round cap/join · fill:none · stroke=currentColor
风格：东方线描（简笔象形 · 转角圆化 · 线条克制）
用法：py -3 scripts/_w939_gen_icons.py
"""
from __future__ import annotations

import json
import pathlib

HEAD = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" '
        'stroke="currentColor" stroke-width="1.5" stroke-linecap="round" '
        'stroke-linejoin="round" aria-hidden="true">')
TAIL = "</svg>\n"

# name -> (语义说明, 路径 d)
ICONS: dict[str, tuple[str, str, str]] = {
    # —— 反馈与收藏 ——
    "star": ("收藏（空心五角星·五瓣尖锋向上）",
             "M12 3.4l2.55 5.17 5.7.83-4.12 4.02.97 5.68L12 16.45l-5.1 2.68.97-5.68-4.12-4.02 5.7-.83z"),
    "star-solid": ("已收藏（实心五角星·与空心同构）",
                   "M12 3.4l2.55 5.17 5.7.83-4.12 4.02.97 5.68L12 16.45l-5.1 2.68.97-5.68-4.12-4.02 5.7-.83z"),
    "thumb-up": ("赞同（竖起拇指·腕部收窄）",
                 "M14 9.4V5.6a2.8 2.8 0 0 0-2.8-2.8L7.6 11.4v10.2h10.6a1.9 1.9 0 0 0 1.85-1.55l1.3-8.2a1.9 1.9 0 0 0-1.85-2.25zM7.6 21.6H4.6a1.9 1.9 0 0 1-1.9-1.9v-6.6a1.9 1.9 0 0 1 1.9-1.9h3", ""),
    "thumb-down": ("不赞同（拇指向下·竖拇指的垂直镜像·非手绘改写）",
                   "M14 9.4V5.6a2.8 2.8 0 0 0-2.8-2.8L7.6 11.4v10.2h10.6a1.9 1.9 0 0 0 1.85-1.55l1.3-8.2a1.9 1.9 0 0 0-1.85-2.25zM7.6 21.6H4.6a1.9 1.9 0 0 1-1.9-1.9v-6.6a1.9 1.9 0 0 1 1.9-1.9h3",
                   ' transform="translate(0 24) scale(1 -1)"'),
    # —— 判定符号 ——
    "check": ("正确（勾·东方书画式短挑）", "M4.8 12.4l4.7 4.9L19.2 6.8"),
    "cross": ("错误（叉·对称双撇）", "M6.4 6.4l11.2 11.2M17.6 6.4L6.4 17.6"),
    # —— 检索与工具 ——
    "search": ("检索（放大镜·东方圆窗）",
               "M10.6 3.6a7 7 0 1 0 0 14 7 7 0 0 0 0-14zM15.9 15.9l5 5"),
    "inspect": ("细查（放大镜内加十字准星）",
                "M10.6 3.6a7 7 0 1 0 0 14 7 7 0 0 0 0-14zM15.9 15.9l5 5M7.9 10.6h5.4M10.6 7.9v5.4"),
    "book": ("典籍（线装书·右翻口）",
             "M5.2 4.6h10.4a2.4 2.4 0 0 1 2.4 2.4v12.4H7.6a2.4 2.4 0 0 1-2.4-2.4zM18 19.4V7M8.4 8.8h6.6M8.4 12.2h6.6"),
    "book-open": ("展卷（翻开的书·中缝一笔）",
                  "M12 6.6C10.6 5.1 8.6 4.6 6 4.6H3.6v12.8c2.6 0 4.6.5 6 1.9 1.4-1.4 3.4-1.9 6-1.9V4.6c-2.6 0-4.6.5-6 2zM12 6.6v12.7"),
    "scroll": ("卷轴（立轴·上下轴头宽于纸面）",
               "M5.8 4.4h12.4a1.6 1.6 0 0 1 0 3.2H5.8a1.6 1.6 0 0 1 0-3.2zM5.8 16.4h12.4a1.6 1.6 0 0 1 0 3.2H5.8a1.6 1.6 0 0 1 0-3.2zM7.4 7.6v8.8M16.6 7.6v8.8"),
    "radio": ("播讲（广播匣·天线与声纹）",
              "M4.2 9.6h15.6v8.9a1.5 1.5 0 0 1-1.5 1.5H5.7a1.5 1.5 0 0 1-1.5-1.5zM8.4 9.6l3.6-5.1 3.6 5.1M8 13.2h8M8 16.4h5"),
    "pin": ("钉住（图钉·圆头斜肩与钉尖）",
            "M9.4 3.6h5.2l-.8 5.1 2.4 2.2H7.8l2.4-2.2zM12 10.9v9.5M10.2 3.6h3.6"),
    "warn": ("警示（三角叹号·顶角锐立）",
             "M12 3.4l9.4 16.2H2.6zM12 9.4v4.8M12 16.8v.6"),
    "quote": ("引语（双曲引号·竖排双勾）",
              "M6.2 15.4V9.8c0-2.5 1.6-4.3 4-4.8l.5 1.7c-1.4.5-2.2 1.4-2.3 2.6h2.4v6.1zM14.6 15.4V9.8c0-2.5 1.6-4.3 4-4.8l.5 1.7c-1.4.5-2.2 1.4-2.3 2.6H19v6.1z"),
    # —— 人物与学阶 ——
    "child": ("幼学（童蒙·圆头身）",
              "M12 4.4a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5zM8.2 20.4c0-2.7 1.7-4.6 3.8-4.6s3.8 1.9 3.8 4.6M6.4 12.4l2.4 1.6M17.6 12.4l-2.4 1.6"),
    "schoolbag": ("初学（书囊·提梁与横带）",
                  "M6.4 9.6h11.2a1.6 1.6 0 0 1 1.6 1.6v8a1.6 1.6 0 0 1-1.6 1.6H6.4a1.6 1.6 0 0 1-1.6-1.6v-8a1.6 1.6 0 0 1 1.6-1.6zM9.2 9.6V7.8a2.8 2.8 0 0 1 5.6 0v1.8M7.6 14.6h8.8"),
    "cap": ("高学（士冠·垂缨）",
            "M2.8 9.3L12 4.6l9.2 4.7-9.2 4.7zM6.8 11.9v4.6c0 1.5 2.3 2.7 5.2 2.7s5.2-1.2 5.2-2.7v-4.6M20.6 10.4v4.6"),
    # —— 成长与器物 ——
    "sprout": ("启蒙（幼苗·双叶对生）",
               "M12 20.4v-7.6M12 12.8c0-3.4-2.6-6.2-5.7-6.2 0 3.4 2.6 6.2 5.7 6.2zM12 12.8c0-4 2.9-7.3 6.7-7.3 0 4-2.9 7.3-6.7 7.3z"),
    "alchemy": ("进阶（炼金方符·菱中三横）",
                "M12 2.9l9.1 9.1-9.1 9.1L2.9 12zM8.4 12h7.2M9.7 8.7h4.6M9.7 15.3h4.6"),
    "pen": ("著述（墨笔·斜锋）",
            "M4.2 19.8l1.1-4.3L15.4 5.4a2 2 0 0 1 2.8 2.8L8.1 18.5zM14.4 6.4l3.2 3.2"),
    "chart": ("统计（柱状·三柱不等高）",
              "M4 20.2h16M7.4 20.2v-5.8M12 20.2V8.4M16.6 20.2v-8.6"),
    "globe": ("寰宇（地球·经纬两线）",
              "M12 3.2a8.8 8.8 0 1 0 0 17.6 8.8 8.8 0 0 0 0-17.6zM3.3 12h17.4M12 3.2c2.4 2.6 3.6 5.6 3.6 8.8s-1.2 6.2-3.6 8.8c-2.4-2.6-3.6-5.6-3.6-8.8S9.6 5.8 12 3.2z"),
    # —— 界面控件 ——
    "note": ("便签与文档（折角纸页）",
             "M6 3.6h8l4 4v12.8H6zM14 3.6v4h4M9.2 12h5.6M9.2 15.4h3.6"),
    "link": ("链接（双环相扣）",
             "M8.4 12.2a3.4 3.4 0 0 0 2.4 5.9l1.6-1.6a3.4 3.4 0 0 0 0-4.8M15.6 11.8a3.4 3.4 0 0 0-2.4-5.9l-1.6 1.6a3.4 3.4 0 0 0 0 4.8M9.9 14.1l4.2-4.2"),
    "menu": ("菜单（三横·中线略短）", "M4 7h16M4 12h16M4 17h16"),
    "close": ("关闭（方框内叉·与判定叉区分）",
              "M7 4.9h10a2.1 2.1 0 0 1 2.1 2.1v10a2.1 2.1 0 0 1-2.1 2.1H7a2.1 2.1 0 0 1-2.1-2.1V7A2.1 2.1 0 0 1 7 4.9zM9.8 9.8l4.4 4.4M14.2 9.8l-4.4 4.4"),
    "play": ("播放（实心三角·尖朝右）", "M8.4 5.4l10 6.6-10 6.6z"),
    "pause": ("暂停（双竖·等距）", "M9.2 5.6v12.8M14.8 5.6v12.8"),
}


def main() -> int:
    # W950：光学尺寸归一参数（视觉边长统一 + 网格居中）· 生成 scripts/output/_w950_icon_normalize.json
    NORM = {}
    _norm_file = pathlib.Path("scripts/output/_w950_icon_normalize.json")
    if _norm_file.exists():
        try:
            NORM = json.loads(_norm_file.read_text(encoding="utf-8"))
        except Exception:
            NORM = {}
    out = pathlib.Path("site/static/icons/ui")
    out.mkdir(parents=True, exist_ok=True)
    for name, spec in ICONS.items():
        desc, d = spec[0], spec[1]
        tr = spec[2] if len(spec) > 2 else ""
        fill = ' fill="currentColor"' if name.endswith("-solid") else ""
        body = f'<path d="{d}"{tr}{fill}/>' if (tr or fill) else f'<path d="{d}"/>'
        _n = NORM.get(name)
        if _n:
            # 归一参数须与既有 transform（镜像等）合并进**同一个** transform 属性，
            # 否则会拼出「d="…" translate(..) transform=".."」这种非法 XML。
            _pre = f'translate({_n["tx"]} {_n["ty"]}) scale({_n["s"]})'
            if tr:
                _inner = tr.strip()
                _inner = _inner[_inner.index('"') + 1:-1]
                tr = f' transform="{_pre} {_inner}"'
            else:
                tr = f' transform="{_pre}"'
            body = f'<path d="{d}"{tr}{fill}/>'
        svg = f"{HEAD}\n  {body}\n{TAIL}"
        (out / f"{name}.svg").write_text(svg, encoding="utf-8")
        print(f"{name:12s} {len(svg):4d}B  {desc}")
    print(f"\n共 {len(ICONS)} 枚 → {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
