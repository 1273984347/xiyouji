# -*- coding: utf-8 -*-
"""_w1005_probe_asset_sizes.py — W1005 终稿报告用的资产实测（尺寸/字节/页面口径）

只读脚本：不改任何文件。WebP 三格式（VP8 / VP8L / VP8X）分别解析，避免只读 VP8X 偏移导致
尺寸乱读（本批首测即踩：按固定偏移读出 67110656x2350791998 的荒谬值）。

用法：py -3 scripts/_w1005_probe_asset_sizes.py
"""
import io
import os
import re
import struct

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

WEBPS = [
    "site/static/images/ink-mountains-hero.webp",
    "site/static/images/hero-01-xihai-yunhai.webp",
]
PNGS = [
    "assets/promo/output/xiyouji-flyer-a4-front.png",
    "assets/promo/output/xiyouji-flyer-a4-en-front.png",
]


def webp_size(p):
    b = io.open(p, "rb").read()
    assert b[:4] == b"RIFF" and b[8:12] == b"WEBP", "非 WebP：%s" % p
    fmt = b[12:16]
    if fmt == b"VP8X":
        w = int.from_bytes(b[24:27], "little") + 1
        h = int.from_bytes(b[27:30], "little") + 1
    elif fmt == b"VP8 ":
        w = struct.unpack("<H", b[26:28])[0] & 0x3FFF
        h = struct.unpack("<H", b[28:30])[0] & 0x3FFF
    elif fmt == b"VP8L":
        bits = int.from_bytes(b[21:25], "little")
        w = (bits & 0x3FFF) + 1
        h = ((bits >> 14) & 0x3FFF) + 1
    else:
        raise AssertionError("未知 WebP 子格式：%r" % fmt)
    return fmt.decode("ascii"), w, h, len(b)


def png_size(p):
    b = io.open(p, "rb").read()
    assert b[:8] == b"\x89PNG\r\n\x1a\n", "非 PNG：%s" % p
    w, h = struct.unpack(">II", b[16:24])
    return w, h, len(b)


def main():
    print("== WebP 资产 ==")
    for rel in WEBPS:
        fmt, w, h, n = webp_size(os.path.join(REPO, rel))
        print("  %-46s %s %dx%d  %d B (%.1f KB)" % (rel, fmt, w, h, n, n / 1024.0))
    print("== PNG 快照 ==")
    for rel in PNGS:
        w, h, n = png_size(os.path.join(REPO, rel))
        print("  %-46s %dx%d  %d B (%.1f KB)" % (rel, w, h, n, n / 1024.0))

    print("== 站点页面口径 ==")
    tot = hero_cls = ref_ink = ref_xihai = hero_any = 0
    for root, _dirs, fs in os.walk(os.path.join(REPO, "site")):
        for f in fs:
            if not f.endswith(".html"):
                continue
            tot += 1
            s = io.open(os.path.join(root, f), encoding="utf-8", errors="ignore").read()
            if re.search(r'class="[^"]*\bhero\b', s):
                hero_cls += 1
            if "ink-mountains-hero.webp" in s:
                ref_ink += 1
            if "hero-01-xihai-yunhai.webp" in s:
                ref_xihai += 1
            if "/static/images/hero" in s:
                hero_any += 1
    print("  site html 总数            %d" % tot)
    print("  含 hero 类的页面           %d" % hero_cls)
    print("  引用 ink-mountains-hero    %d" % ref_ink)
    print("  引用 hero-01-xihai-yunhai  %d" % ref_xihai)
    print("  引用 /static/images/hero*  %d" % hero_any)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
