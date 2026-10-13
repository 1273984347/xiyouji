#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_w494_font_slice.py — W494 字体 unicode-range 切片（一次性，不入库）

从 W477 子集化的 NotoSansSC-Regular/Medium.woff2 按全站字频分 16 片，
输出 site/static/fonts/slices/NotoSansSC-{Regular,Medium}-slice-{NN}.woff2
+ site/static/css/fonts-slices.css（16 片 @font-face unicode-range 声明，外部 CSS 免内联膨胀）。

用法：
  python scripts/_w494_font_slice.py        # 生成切片 + css
"""
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "site" / "static" / "fonts"
OUT = FONTS / "slices"
CSS_OUT = ROOT / "site" / "static" / "css"
PY = sys.executable
SLICES = 16


def char_freq() -> Counter:
    c = Counter()
    for base in (ROOT / "docs", ROOT / "site"):
        for p in base.rglob("*"):
            if p.suffix.lower() not in (".md", ".html"):
                continue
            try:
                t = p.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            c.update(re.findall(r"[\u4e00-\u9fff\u3400-\u4dbf]", t))
    return c


def to_unicode_range(chars: str) -> str:
    cps = sorted(ord(ch) for ch in chars)
    parts = []
    start = prev = cps[0]
    for cp in cps[1:]:
        if cp - prev > 1:
            parts.append((start, prev))
            start = cp
        prev = cp
    parts.append((start, prev))
    # 合并 ≤3 的间隙会膨胀 range，直接逐段输出
    segs = []
    for a, b in parts:
        segs.append(f"U+{a:04X}" if a == b else f"U+{a:04X}-{b:04X}")
    return ",".join(segs)


def subset(src: Path, dst: Path, chars: str):
    cmd = [PY, "-m", "fontTools.subset", str(src), f"--text={chars}",
           "--flavor=woff2", f"--output-file={dst}",
           "--layout-features=*", "--name-IDs=*", "--notdef-outline",
           "--recalc-bounds", "--drop-tables+=FFTM"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"subset {src.name} 失败: {r.stderr[-300:]}")


def main():
    freq = char_freq()
    total = sum(freq.values())
    chars = sorted(freq, key=lambda ch: -freq[ch])
    print(f"全站用字 {len(chars)} 个 · 总频次 {total}")
    buckets = [chars[i::SLICES] for i in range(SLICES)]  # 轮转分桶保证每桶频次均衡
    # 轮转分桶后每桶码点分散，range 长；改用连续分桶（前 1/16 高频）保 range 短
    step = (len(chars) + SLICES - 1) // SLICES
    buckets = [chars[i * step:(i + 1) * step] for i in range(SLICES)]
    OUT.mkdir(parents=True, exist_ok=True)
    CSS_OUT.mkdir(parents=True, exist_ok=True)
    lines = ["/* W494 自动生成：Noto Sans SC unicode-range 切片（16 片）· 由 _w494_font_slice.py 生成，勿手改 */"]
    for idx, bucket in enumerate(buckets):
        if not bucket:
            continue
        cset = "".join(sorted(bucket))
        for weight, src_name, dst_name in (
            ("400", "NotoSansSC-Regular.woff2", f"NotoSansSC-Regular-slice-{idx:02d}.woff2"),
            ("500", "NotoSansSC-Medium.woff2", f"NotoSansSC-Medium-slice-{idx:02d}.woff2"),
        ):
            src = FONTS / src_name
            dst = OUT / dst_name
            subset(src, dst, cset)
        rng = to_unicode_range(cset)
        lines.append(f"@font-face {{")
        lines.append(f"  font-family: 'Noto Sans SC';")
        lines.append(f"  font-style: normal;")
        lines.append(f"  font-weight: 400;")
        lines.append(f"  font-display: optional;")
        lines.append(f"  src: url('../fonts/slices/NotoSansSC-Regular-slice-{idx:02d}.woff2') format('woff2');")
        lines.append(f"  unicode-range: {rng};")
        lines.append(f"}}")
        lines.append(f"@font-face {{")
        lines.append(f"  font-family: 'Noto Sans SC';")
        lines.append(f"  font-style: normal;")
        lines.append(f"  font-weight: 500;")
        lines.append(f"  font-display: optional;")
        lines.append(f"  src: url('../fonts/slices/NotoSansSC-Medium-slice-{idx:02d}.woff2') format('woff2');")
        lines.append(f"  unicode-range: {rng};")
        lines.append(f"}}")
        print(f"片 {idx:02d}: {len(bucket)} 字 · range 段 {len(rng.split(','))} 个")
    (CSS_OUT / "fonts-slices.css").write_text("\n".join(lines) + "\n", encoding="utf-8")
    total_size = sum(p.stat().st_size for p in OUT.glob("*.woff2"))
    print(f"切片完成: {len(list(OUT.glob('*.woff2')))} 文件 · {total_size/1024:.0f}KB")
    print(f"CSS: {CSS_OUT / 'fonts-slices.css'}")


if __name__ == "__main__":
    main()
