# -*- coding: utf-8 -*-
"""_w1016_pick.py — W1016 选材：缺口 68 回全量角色谱扫描 × 已出 100 主体对照

一份脚本出选材证据（不再靠多次 argv 扫）：
  ① 缺口回（无配图）全量；
  ② 每回的角色谱（按词典统计出现次数·取前 6）；
  ③ 每个角色标记「已出 / 未出」（已出基线 = plate-set 的 **slug 唯一集合**，实测 100 个）；
  ④ 汇总「未出角色」候选池（按出现次数降序）⇒ 供挑 12 个新主体。

输出：scripts/output/_w1016_pick.json
用法：py -3 scripts/_w1016_pick.py
"""
from __future__ import annotations

import io
import json
import os
import re
from collections import Counter

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SET = os.path.join(REPO, "assets", "promo", "plate-set")
OUT = os.path.join(REPO, "scripts", "output", "_w1016_pick.json")

NAMES = [
    "悟空", "行者", "八戒", "沙僧", "悟净", "唐僧", "玄奘", "白龙马", "白龙",
    "观音", "如来", "佛祖", "祖师", "太白金星", "金星", "镇元大仙", "镇元仙",
    "灵吉菩萨", "灵吉", "风神", "丁甲", "二郎", "显圣", "熊罴", "黑熊", "黑风怪",
    "金池长老", "法明", "殷温娇", "高太公", "黄风怪", "黄风大王", "灵感大王",
    "金蝉", "翠云山", "菩提", "凤凰", "斑衣鳜婆", "银角", "精细鬼", "莲花洞",
    "蜘蛛精", "蜈蚣精", "毗蓝婆", "大鹏", "金翅", "秦广王", "幽冥", "判官", "崔判官",
    "阎王", "地藏", "托塔", "哪吒", "李天王", "老君", "铁扇", "红孩儿",
    "白骨精", "黄袍怪", "奎木狼", "百眼魔君", "赛太岁", "九灵元圣", "玉面狐狸",
    "白面狐狸", "玉兔", "嫦娥", "牛魔王", "铁扇公主", "金角大王", "碧波潭",
    "金兜大王", "辟寒大王", "辟暑大王", "辟尘大王", "羊力大仙", "虎力大仙", "鹿力大仙",
    "白面狐狸精", "玉面狐狸精", "虎先锋", "白鹿精", "白熊", "鲤鱼",
    "鼍龙", "摩昂", "蜘蛛", "蜈蚣", "玉华州", "玉华王", "辟寒", "辟暑", "辟尘",
    "虎力", "羊力", "鹿力", "金翅大鹏雕", "大鹏金翅", "普贤", "文殊", "谛听",
    "虎力大仙", "赛太", "金蝉子", "乌鸡国王", "清风", "明月", "伯钦", "镇山太保",
    "老鼠精", "地涌夫人", "老鼋", "鼋", "九灵", "金毛犼", "独角兕", "摩云",
    "黄眉大王", "玉面狐狸精", "羊力大仙", "黑熊", "青狮", "白象", "赛太岁",
    "孔雀大明王", "白鹏", "白孔雀", "赛九尾", "九尾狐狸", "狐", "狐妖",
    "虎都", "虎穴", "金毛", "辟寒大王", "辟暑大王", "辟尘大王", "独角",
    "太乙", "救苦", "灵山", "如来佛", "观音大士", "托塔天王", "三头六臂",
    "金角", "银角", "黄风", "赛太", "九灵", "灵感", "辟寒", "辟暑", "辟尘",
]
NAMES = sorted(set(NAMES))


def chapter_text(ch):
    p = os.path.join(REPO, "site", "reader", "%s.html" % ch)
    s = io.open(p, encoding="utf-8", errors="ignore").read()
    body = s[s.find("<article"):]
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", body))


def already_out():
    """已出主体基线 = plate-set 的 slug 唯一集合（去编号）。"""
    files = sorted(f for f in os.listdir(SET) if f.startswith("plate-line-") and f.endswith(".png"))
    slugs = [re.sub(r"^plate-line-\d+-", "", f)[:-4] for f in files]
    return set(slugs), len(slugs), len(files)


def main() -> int:
    out_slugs, n_slug, n_files = already_out()
    # 已出角色的**关键词**集合（slug 是拼音，无法直接匹配中文角色名⇒用 README 描述 + slug 双面）
    desc_by_slug = {}
    rp = os.path.join(SET, "README.md")
    if os.path.exists(rp):
        txt = io.open(rp, encoding="utf-8").read()
        for m in re.finditer(r"^\|\s*`([^`]+)`\s*\|([^|]*)\|", txt, re.M):
            key = re.sub(r"^plate-line-\d+-", "", m.group(1).strip())
            desc_by_slug.setdefault(key, m.group(2).strip())
    used_words = set()
    for s, d in desc_by_slug.items():
        used_words.add(s.lower())
        for w in re.findall(r"[一-鿿]{2,5}", d):
            used_words.add(w)

    def is_out(name):
        if name in used_words:
            return True
        return any(name in s.lower() for s in out_slugs if len(s) >= 3)

    # 缺口回
    gap = []
    for fn in sorted(os.listdir(os.path.join(REPO, "site", "reader"))):
        if not fn.startswith("ch") or not fn.endswith(".html"):
            continue
        s = io.open(os.path.join(REPO, "site", "reader", fn), encoding="utf-8", errors="ignore").read()
        if re.search(r'<figure class="chapter-(plate|scene)">', s):
            continue
        gap.append(fn[:5])          # chXXX（含前缀·页面文件名是 ch005.html）

    rows = []
    pool = Counter()
    for ch in gap:
        t = chapter_text(ch)
        h1 = re.search(r"<h1[^>]*>(.*?)</h1>",
                       io.open(os.path.join(REPO, "site", "reader", "%s.html" % ch), encoding="utf-8",
                               errors="ignore").read(), re.S)
        title = re.sub(r"<[^>]+>", "", h1.group(1)).strip() if h1 else ""
        hits = []
        for n in NAMES:
            c = t.count(n)
            if c:
                hits.append((c, n))
        hits.sort(reverse=True)
        top = hits[:6]
        new_ones = [n for c, n in top if not is_out(n)]
        for n in new_ones:
            pool[n] += max(1, dict(top).get(n, 0))
        rows.append({"ch": ch, "title": title,
                     "roles": [(n, c) for c, n in top],
                     "new_roles": new_ones})

    data = {"gap_total": len(gap), "already_out_slugs": n_slug, "already_out_files": n_files,
            "rows": rows,
            "new_role_pool": [(n, c) for n, c in pool.most_common(60)]}
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(json.dumps(data, ensure_ascii=False, indent=1))

    print("已出主体：%d 个 slug / %d 个母版文件 · 缺口 %d 回" % (n_slug, n_files, len(gap)))
    print("\n== 缺口回角色谱（★ = 未出角色候选）==")
    for r in rows:
        marks = "、".join(("%s×%d" % (n, c)) + ("" if not is_out(n) else "·旧") for n, c in r["roles"])
        print("  ch%s %-34s %s" % (r["ch"], r["title"][:34], marks[:110]))
    print("\n== 未出角色候选池（按出现次数）==")
    for n, c in data["new_role_pool"][:40]:
        print("  %-12s %d" % (n, c))
    print("\n写出:", os.path.relpath(OUT, REPO).replace("\\", "/"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
