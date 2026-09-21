#!/usr/bin/env python3
"""gen_og_cover.py — 生成社交分享封面 site/static/img/og-cover.png（W591 SEO 清零）。

规格（docs/superpowers/plans/2026-09-21-demand-side-optimization-master-plan.md WP-C 第 1 条）：
  - 精确 1200x630 px，PNG ≤ 300KB
  - 宣纸底 #faf7f2 + 朱砂 #c8463a 主标题「详解西游记」+ 副题「一源多形 · 数字人文解读 100 回」+ 站点 URL 小字
  - 脚本入库保证可复现；字体取 Windows 自带中文字体族，逐个回退

用法：python scripts/gen_og_cover.py
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "site" / "static" / "img" / "og-cover.png"

W, H = 1200, 630
PAPER = (250, 247, 242)      # --paper #faf7f2
CINNABAR = (200, 70, 58)     # --accent #c8463a
INK = (58, 58, 58)           # 墨色
INK_SOFT = (110, 105, 98)

FONT_CANDIDATES = [
    r"C:\Windows\Fonts\msyhbd.ttc",   # 微软雅黑 Bold
    r"C:\Windows\Fonts\msyh.ttc",
    r"C:\Windows\Fonts\simhei.ttf",   # 黑体
    r"C:\Windows\Fonts\simsun.ttc",   # 宋体
]


def load_font(size: int):
    for path in FONT_CANDIDATES:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    raise SystemExit("未找到可用中文字体（尝试: " + ", ".join(FONT_CANDIDATES) + "）")


def main() -> None:
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # 左侧朱砂竖条（设计主线）
    d.rectangle([0, 0, 14, H], fill=CINNABAR)

    # 主标题
    f_title = load_font(120)
    d.text((70, 150), "详解西游记", font=f_title, fill=INK)

    # 副题
    f_sub = load_font(44)
    d.text((74, 330), "一源多形 · 数字人文解读 100 回", font=f_sub, fill=CINNABAR)

    # 数据条小字
    f_meta = load_font(30)
    d.text(
        (74, 420),
        "615 篇解读文档 · 86 个数据可视化 · 133 个数据维度",
        font=f_meta,
        fill=INK_SOFT,
    )

    # 底部 URL
    f_url = load_font(26)
    d.text((74, 545), "1273984347.github.io/xiyouji", font=f_url, fill=INK_SOFT)

    # 右下朱砂印章方块「西」
    f_seal = load_font(72)
    d.rectangle([W - 190, H - 190, W - 60, H - 60], fill=CINNABAR)
    d.text((W - 160, H - 176), "西", font=f_seal, fill=PAPER)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, "PNG", optimize=True)
    size = OUT.stat().st_size
    assert img.size == (1200, 630), img.size
    assert size <= 300 * 1024, f"og-cover.png 超 300KB：{size}"
    print(f"[OK] {OUT.relative_to(ROOT)} {img.size} {size}B")


if __name__ == "__main__":
    main()
