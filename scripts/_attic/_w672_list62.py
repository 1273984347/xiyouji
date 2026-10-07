# -*- coding: utf-8 -*-
# _w672_list62.py — 计算 WP-1.2 受影响文件清单（62 文件）与 10 页抽样（方案 §三 WP-1.2 验收 5 抽样规则）
import glob
import io
import re

tok = io.open("site/tokens.css", encoding="utf-8").read()
tok_defs = set(re.findall(r"(--[\w-]+)\s*:", tok))
var_re = re.compile(r"var\((--[\w-]+)\)")
def_re = re.compile(r"(--[\w-]+)\s*:")
all_files = sorted(glob.glob("site/data/*.html") + glob.glob("site/*.html") + glob.glob("site/en/*.html"))
out = []
for f in all_files:
    src = io.open(f, encoding="utf-8", errors="replace").read()
    style_blocks = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", src, re.S | re.I))
    inline_attr = " ".join(re.findall(r'style="([^"]*)"', src))
    js_text = "\n".join(re.findall(r"<script[^>]*>(.*?)</script>", src, re.S | re.I))
    defs = set(re.findall(def_re, style_blocks)) | set(re.findall(def_re, inline_attr))
    defs |= set(re.findall(r"['\"]?(--[\w-]+)\s*[:=]", js_text))
    defs |= set(re.findall(r"\.style\(\s*[\"'](--[\w-]+)", js_text))
    defs |= set(re.findall(r"setProperty\(\s*[\"'](--[\w-]+)", js_text))
    known = defs | tok_defs
    if any(v not in known for v in var_re.findall(style_blocks)):
        rel = f.replace("site\\", "").replace("site/", "").replace(".html", "")
        out.append(rel)
print("files:", len(out))
io.open(".review-tmp/_w672/w62_files.txt", "w", encoding="utf-8").write("\n".join(out) + "\n")
sample = [out[i - 1] for i in (1, 8, 15, 21, 28, 35, 42, 48, 55, 62)]
io.open(".review-tmp/_w672/w12_pages.txt", "w", encoding="utf-8").write("\n".join(sample) + "\n")
print("sample:", sample)
