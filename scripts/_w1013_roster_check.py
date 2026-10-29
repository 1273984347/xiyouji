# -*- coding: utf-8 -*-
"""_w1013_roster_check.py — W1013 主体去重硬判据（V-02）：候选主体 × 已出母版全表

为什么需要独立脚本（W1001 批坑表 E-05/E-21 同族）：
  ① **编号不全局唯一**——plate-set 的编号 1–12 被四个批次族复用（实测：编号 1–8 各 4 次、
     9–12 各 2 次）⇒ 「编号 max」不等于「主体数」；
  ② **README 登记不全**——实测 88 个母版文件里 README 只登记 76 条 ⇒ 只按 README 避重会漏 12 个；
  ⇒ 真实判据 = **slug 唯一集合**（实测 88 个母版 = 88 个唯一 slug）。

本脚本只读：对候选主体关键词，在**88 个 slug** + README 描述列双面查重，并打印全表。

用法：py -3 scripts/_w1013_roster_check.py
"""
import io
import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLATE = os.path.join(REPO, "assets", "promo", "plate-set")

# 候选主体（回 × 主体名 × 判定关键词·小写）
CANDS = [
    ("ch002", "菩提祖师", ["puti", "zushi", "shifu"]),
    ("ch012", "金蝉子", ["jinchan", "chantai"]),
    ("ch013", "太白金星", ["taibai", "baixing", "jinxing"]),
    ("ch021", "灵吉菩萨", ["lingji"]),
    ("ch038", "乌鸡国王", ["wuji", "guowang"]),
    ("ch045", "虎力大仙", ["huli"]),
    ("ch078", "蜘蛛精", ["zhizhu"]),
    ("ch082", "白鹿精", ["bailu"]),
    ("ch083", "老鼠精", ["laoshu", "dishu"]),
    ("ch086", "辟寒大王", ["bichan", "bidai", "biyu", "bic"]),
    ("ch087", "玉华王", ["yuhua"]),
    ("ch092", "地藏王", ["dizang"]),
]


def main() -> int:
    files = sorted(f for f in os.listdir(PLATE)
                   if f.startswith("plate-line-") and f.endswith(".png"))
    slugs = [re.sub(r"^plate-line-\d+-", "", f)[:-4] for f in files]
    assert len(set(slugs)) == len(slugs), "slug 非唯一（编号复用导致）"
    nums = [int(re.match(r"plate-line-(\d+)-", f).group(1)) for f in files]
    print("已出母版 %d 个（slug 全唯一）· 编号 max=%d · 编号最小 %d"
          % (len(files), max(nums), min(nums)))

    desc = {}
    rp = os.path.join(PLATE, "README.md")
    if os.path.exists(rp):
        txt = io.open(rp, encoding="utf-8").read()
        for m in re.finditer(r"^\|\s*`([^`]+)`\s*\|([^|]*)\|", txt, re.M):
            key = m.group(1).strip()
            val = m.group(2).strip()
            # README 的键是「plate-line-NN-slug」全名，而文件 slug 是去编号的裸 slug
            # ⇒ 双键登记（首测即因只用全名键致描述列覆盖 0/88·主体名判据漏检）
            desc[key] = val
            desc[re.sub(r"^plate-line-\d+-", "", key)] = val
    print("README 登记条目 %d 条（覆盖 %d/%d 个 slug）"
          % (len(desc), len([s for s in slugs if s in desc]), len(slugs)))

    print("\n--- 候选主体 × 已出全表查重 ---")
    clash = 0
    for ch, name, kws in CANDS:
        hit_slug = [s for s in slugs if any(k in s.lower() for k in kws)]
        hit_desc = [s for s in slugs if s in desc and any(k in desc[s].lower() for k in kws)]
        flag = "★冲突" if (hit_slug or hit_desc) else "未出 ✓"
        if hit_slug or hit_desc:
            clash += 1
        print("  %-6s %-10s %-9s slug命中=%-18s 描述命中=%s"
              % (ch, name, flag, hit_slug or "无", hit_desc or "无"))

    print("\n--- 已出 slug 全表（%d）---" % len(slugs))
    for i in range(0, len(slugs), 4):
        print("  " + " · ".join("%-26s" % s for s in slugs[i:i + 4]))

    print("\n结论：%d 个候选主体与已出全表冲突" % clash)
    return 1 if clash else 0


if __name__ == "__main__":
    raise SystemExit(main())
