# -*- coding: utf-8 -*-
"""_w1013_read.py — W1013 批 12 回原文实读（选材证据）

方法（沿用 W1001 批 `_w990_read.py` 的纪律，但改为**先扫后选**）：
  ① 对候选回逐个统计「人物名词典」在该回原文中的出现次数 ⇒ 得到该回真实出场角色谱；
  ② 对出现次数最多的候选角色，打印**首次出现的上下文片段**（原文证据·可人工复核）；
  ③ 与已出 60 个 plate-line 主体比对 ⇒ 标记「已出/未出」⇒ 未出者方可作新主体。

输出：scripts/output/_w1013_read.json + stdout 证据表
用法：py -3 scripts/_w1013_read.py
"""
import io
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "scripts", "output", "_w1013_read.json")

# 候选回（缺口内·沿用 W1001 批「战斗回场面·其余立像」的粗分：标 scene 者为打斗主回）
# 可用命令行覆盖：py -3 scripts/_w1013_read.py ch002 ch005 ...
CANDIDATES = [
    ("ch002", "portrait"), ("ch005", "scene"), ("ch012", "portrait"),
    ("ch013", "portrait"), ("ch016", "portrait"), ("ch020", "scene"),
    ("ch021", "portrait"), ("ch024", "scene"), ("ch026", "portrait"),
    ("ch031", "scene"), ("ch034", "portrait"), ("ch037", "portrait"),
]
if len(sys.argv) > 1:
    CANDIDATES = [(a, "portrait") for a in sys.argv[1:]]

# 人物名词典（取页面正文常见称谓）
NAMES = [
    "悟空", "行者", "八戒", "沙僧", "悟净", "唐僧", "玄奘", "白龙马",
    "观音", "如来", "佛祖", "祖师", "太白金星", "金星", "镇元大仙", "镇元仙",
    "灵吉菩萨", "灵吉", "风神", "丁甲", "二郎", "显圣", "熊罴", "黑熊", "黑风怪",
    "金池长老", "法明", "殷温娇", "高太公", "黄风怪", "黄风大王", "灵感大王",
    "金蝉", "翠云山", "菩提", "凤凰", "斑衣鳜婆", "银角", "精细鬼", "莲花洞",
    "蜘蛛", "蜈蚣", "毗蓝婆", "大鹏", "金翅", "秦广王", "幽冥", "判官", "崔判官",
    "阎王", "地藏", "托塔", "哪吒", "李天王", "老君", "铁扇", "红孩儿",
    "白骨精", "黄袍怪", "奎木狼", "百眼魔君", "赛太岁", "九灵元圣", "玉面狐狸",
    "白面狐狸", "玉兔", "嫦娥", "牛魔王", "铁扇公主", "金角大王", "碧波潭",
    # W1013 批扩充词典（扫后半程回目·找未出角色）
    "金兜大王", "辟寒大王", "辟暑大王", "辟尘大王", "羊力大仙", "虎力大仙", "鹿力大仙",
    "白面狐狸精", "玉面狐狸精", "虎先锋", "白鹿精", "白熊", "灵感大王", "鲤鱼",
    "鼍龙", "摩昂", "蜘蛛精", "蜈蚣精", "蜈蚣", "毗蓝婆", "玉华州", "玉华王",
    "辟寒", "辟暑", "辟尘", "虎力", "羊力", "鹿力", "金翅大鹏雕", "大鹏金翅",
    "地藏", "谛听", "普贤", "文殊", "九灵", "赛太", "太白金星", "菩提祖师",
    "金蝉子", "乌鸡国王", "清风", "明月", "伯钦", "镇山太保", "灵吉", "银角大王",
    # W1013 第二轮扩充（补后段回目角色）
    "犀牛", "辟暑", "老鼋", "鼋", "鼍", "摩昂", "老鼠精", "狐狸精", "白面狐狸",
    "玉面狐狸", "蜘蛛精", "蜈蚣精", "金兜", "青牛", "如意真仙", "灵虚子",
    "黄眉大王", "虎力大仙", "羊力大仙", "鹿力大仙", "辟尘大王", "辟寒大王",
]


def chapter_text(ch):
    p = os.path.join(REPO, "site", "reader", "%s.html" % ch)
    s = io.open(p, encoding="utf-8", errors="ignore").read()
    body = s[s.find("<article"):]
    t = re.sub(r"<[^>]+>", "", body)
    return re.sub(r"\s+", " ", t)


def roster_stems():
    p = os.path.join(REPO, "assets", "promo", "plate-set", "README.md")
    stems = []
    if os.path.exists(p):
        txt = io.open(p, encoding="utf-8").read()
        stems = [a.strip() for a, _b in re.findall(r"^\| `([^`]+)` \| ([^|]+) \|", txt, re.M)]
    return stems


def main() -> int:
    stems = roster_stems()
    out = {}
    for ch, kind in CANDIDATES:
        t = chapter_text(ch)
        hits = []
        for n in NAMES:
            c = t.count(n)
            if c:
                hits.append((c, n))
        hits.sort(reverse=True)
        h1 = re.search(r"<h1[^>]*>(.*?)</h1>",
                       io.open(os.path.join(REPO, "site", "reader", "%s.html" % ch),
                               encoding="utf-8", errors="ignore").read(), re.S)
        title = re.sub(r"<[^>]+>", "", h1.group(1)).strip() if h1 else ""
        # 证据：前 3 个角色的首次出现上下文
        ev = []
        for _c, n in hits[:3]:
            i = t.find(n)
            ev.append({"name": n, "ctx": t[max(0, i - 100):i + 200]})
        out[ch] = {"kind": kind, "title": title,
                   "hits": [(n, c) for c, n in hits[:8]],
                   "evidence": ev}
        print("=" * 24, ch, "·", title)
        print("   候选范式:", kind, "· 出场角色（前 8）:",
              "、".join("%s×%d" % (n, c) for c, n in hits[:8]) or "（无命中）")
        for e in ev:
            print("   [%s] %s" % (e["name"], e["ctx"][:190]))
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(json.dumps(out, ensure_ascii=False, indent=1))
    print("\n已出 plate-line 主体 %d 个（选材须避开）" % len([s for s in stems if s.startswith("plate-line")]))
    print("写出:", os.path.relpath(OUT, REPO).replace("\\", "/"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
