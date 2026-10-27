#!/usr/bin/env python3
"""一次性：W987 接入验收探针（题图/场景图并存 · 类名不混 · 暗色规则 · HTTP 200）"""
import io
import os
import re
import sys
import urllib.request

REPO = r"D:\xiyouji"
BASE = "http://127.0.0.1:8765/"
PAGES = ["ch007", "ch014", "ch015", "ch023", "ch027", "ch030"]
IMGS = {"ch007": "chap-07.webp", "ch014": "chap-14.webp", "ch015": "chap-15.webp",
        "ch023": "chap-23.webp", "ch027": "chap-27.webp", "ch030": "chap-30.webp"}

RE_PLATE_FIG = re.compile(r'<figure class="chapter-plate">')
RE_SCENE_FIG = re.compile(r'<figure class="chapter-scene">')
RE_SCENE_CSS = re.compile(r'\.chapter-scene\s*\{[^}]*\}')
RE_DARK = re.compile(r'html\[data-theme="dark"\]\s*\.chapter-scene\s*\{\s*display:\s*none')

bad = 0
for p in PAGES:
    path = os.path.join(REPO, "site", "reader", "%s.html" % p)
    t = io.open(path, encoding="utf-8", newline="").read()
    n_plate = len(RE_PLATE_FIG.findall(t))
    n_scene = len(RE_SCENE_FIG.findall(t))
    css_ok = bool(RE_SCENE_CSS.search(t))
    dark_ok = bool(RE_DARK.search(t))
    alt_ok = 'alt="第 0' in t and "水墨意境图" in t
    try:
        u = BASE + "static/images/" + IMGS[p]
        r = urllib.request.urlopen(u, timeout=20)
        code, ctype, nbytes = r.getcode(), r.headers.get("Content-Type"), len(r.read())
    except Exception as e:
        code, ctype, nbytes = "ERR", str(e)[:40], 0
    ok = (n_plate == 1 and n_scene == 1 and css_ok and dark_ok and alt_ok and code == 200)
    if not ok:
        bad += 1
    print("%-6s %-7s 题图=%d 场景图=%d 样式=%s 暗色隐藏=%s alt=%s HTTP=%s %s %dB" % (
        "OK" if ok else "FAIL", p, n_plate, n_scene, css_ok, dark_ok, alt_ok, code, ctype, nbytes))

print("\n接入验收：%d/%d 页通过" % (len(PAGES) - bad, len(PAGES)))
sys.exit(1 if bad else 0)
