# -*- coding: utf-8 -*-
"""_w1043_pick.py — W1043 第四轮选材：缺口回角色谱扫描 + 已出主体对照表

口径（沿用 W1018 批）：
  · 缺口 = 回目页 og:image 指向通用图（og-cover-ink-zh.jpg）者（54 回）；
  · 角色谱 = 对每回正文统计角色名出现次数（正则取妖/人名形态词）；
  · 已出对照 = plate-line-*.png 的全部 slug（母版级全表避重）。

输出：stdout（人工挑选用）· 不写盘
用法：py -3 archive/scripts/batches/w10xx/_w1043_pick.py
"""
import io
import os
import re
import sys
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
RD = os.path.join(REPO, "site", "reader")
SET = os.path.join(REPO, "assets", "promo", "plate-set")

RE_OG = re.compile(r'og:image"\s+content="([^"]+)"')
RE_ROLE = re.compile(
    r"[一-龥]{2,4}"
    r"(?:精|怪|仙|大王|大圣|元帅|将军|国师|僧|道人|罗汉|菩萨|真人|居士|妖|魔|君|圣|尊|使)"
)
RE_TAG = re.compile(r"<[^>]+>")

# ---- 缺口回 ----
have, card, gap = set(), set(), []
for fn in sorted(os.listdir(RD)):
    if not fn.endswith(".html"):
        continue
    ch = fn[:5]
    t = io.open(os.path.join(RD, fn), encoding="utf-8", errors="ignore").read()
    m = RE_OG.search(t)
    src = m.group(1) if m else ""
    if "og-plate-line" in src:
        have.add(ch)
    elif "card-" in src:
        card.add(ch)
    else:
        gap.append(ch)

print("已落位专属 og = %d 回 · card 专属 = %d 回 · 缺口 = %d 回" % (len(have), len(card), len(gap)))

# ---- 已出 slug 全表 ----
slugs = set()
for fn in os.listdir(SET):
    # W1044 订正：原正则 `[a-z0-9-]` 大小写敏感 ⇒ 漏掉唯一带大写的存量 slug
    # `plate-line-06-jiuLingyuansheng` ⇒ 唯一数被少算 1（111 而非 112·W1043 实误）。
    m = re.match(r"plate-line-(\d+)(?:-ch(\d+))?-([A-Za-z0-9-]+)\.png$", fn)
    if m:
        slugs.add((m.group(2), m.group(3)))
print("已出母版 = %d 张 · 唯一 slug = %d 个" % (
    len([f for f in os.listdir(SET) if f.startswith("plate-line-") and f.endswith(".png")]),
    len({s for _c, s in slugs})))

# ---- 角色谱 ----
role_hits = Counter()
role_ch = {}
for ch in gap:
    p = os.path.join(RD, ch + ".html")
    if not os.path.exists(p):
        continue
    t = io.open(p, encoding="utf-8", errors="ignore").read()
    t = RE_TAG.sub(" ", t)
    for r in RE_ROLE.findall(t):
        role_hits[r] += 1
        role_ch.setdefault(r, set()).add(ch)

print("\n== 缺口回角色谱（出现次数 ≥ 4·按次数降序）==")
for r, n in sorted(role_hits.items(), key=lambda kv: (-kv[1], kv[0])):
    if n < 4:
        continue
    print("  %-8s ×%-4d 回: %s" % (r, n, " ".join(sorted(role_ch[r])[:6])))

print("\n== 已出 slug（ch + slug）对照表 ==")
for c, s in sorted(slugs, key=lambda x: (x[0], x[1])):
    print("  %s %s" % (c, s))
