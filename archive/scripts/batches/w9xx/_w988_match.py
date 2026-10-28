#!/usr/bin/env python3
"""_w988_match.py — W988 落位候选页语义盘点（只读）

对 27 张 card-* 用**画面题材词**（人工实读拼图后定，非文件名猜测）检索全站 reader 页，
输出命中页的 H1 + 首段 + 已有插图状态，供人工定案。

输出：scripts/output/_w988_match.json
"""
from __future__ import annotations

import glob
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "scripts", "output", "_w988_match.json")

# 27 张卡 · 题材词（人工实读 site/static/images/card-*.webp 拼图后定案）
CARDS = {
    # ---- 场景卡（14 张）----
    "card-01-huoshan":          {"kind": "scene", "words": ["火焰山"]},
    "card-02-tongtianhe":       {"kind": "scene", "words": ["通天河"]},
    "card-03-shituoling":       {"kind": "scene", "words": ["狮驼岭"]},
    "card-04-dushuangxuejiang": {"kind": "scene", "words": ["黑水河", "雪江", "独钓", "寒江雪"]},
    "card-05-mingyuesongjian":  {"kind": "scene", "words": ["明月", "松间", "松风", "月"]},
    "card-06-yunshenzhibu":     {"kind": "scene", "words": ["云栈洞", "云深", "云海"]},
    "card-07-baiyao":           {"kind": "scene", "words": ["百妖", "群妖", "妖谱", "小妖"]},
    "card-08-zhuowuquan":       {"kind": "scene", "words": ["濯垢泉", "濯武泉", "盘丝洞", "泉"]},
    "card-09-sanyao":           {"kind": "scene", "words": ["三妖", "白鹿精", "白象精", "玉面狐狸"]},
    "card-10-gusichenzhong":    {"kind": "scene", "words": ["镇海寺", "古寺", "钟", "禅", "寺"]},
    "card-11-songyunshitan":    {"kind": "scene", "words": ["花果山", "松云", "石坛", "水帘洞"]},
    "card-12-shuyuanxingtantan": {"kind": "scene", "words": ["书院", "杏坛", "讲学", "教育"]},
    "card-25-santiebaigujing":  {"kind": "scene", "words": ["白骨精", "白骨"]},
    "card-27-rejiao-fenxi":     {"kind": "scene", "words": ["神学", "宗教", "佛学", "映射"]},
    # ---- 人物卡（13 张）----
    "card-13-bajie-yuexia":     {"kind": "figure", "who": "bajie"},
    "card-14-bajie-choupa":     {"kind": "figure", "who": "bajie"},
    "card-15-bajie-zuoxie":     {"kind": "figure", "who": "bajie"},
    "card-16-bajie-yunzhong":   {"kind": "figure", "who": "bajie"},
    "card-17-bajie-denggao":    {"kind": "figure", "who": "bajie"},
    "card-18-bajie-daodan":     {"kind": "figure", "who": "bajie"},
    "card-19-shaseng-dujiang":  {"kind": "figure", "who": "shaseng"},
    "card-20-shaseng-zhenshui": {"kind": "figure", "who": "shaseng"},
    "card-21-shaseng-shouye":   {"kind": "figure", "who": "shaseng"},
    "card-22-shaseng-fuzhong":  {"kind": "figure", "who": "shaseng"},
    "card-23-shixiong-bingli":  {"kind": "figure", "who": "team"},
    "card-24-shixiong-shanmen": {"kind": "figure", "who": "team"},
    "card-26-wukong-jingu":     {"kind": "figure", "who": "wukong"},
}

WHO_WORDS = {
    "bajie":   ["猪八戒", "悟能", "八戒"],
    "shaseng": ["沙僧", "沙悟净", "卷帘大将"],
    "team":    ["取经团队", "师兄弟", "五众", "取经五众"],
    "wukong":  ["孙悟空", "悟空", "行者", "齐天大圣", "孙行者"],
}

RE_TAG = re.compile(r"<[^>]+>")


def txt(s: str) -> str:
    return re.sub(r"\s+", " ", RE_TAG.sub(" ", s)).strip()


def main() -> None:
    pages = []
    for f in sorted(glob.glob(os.path.join(ROOT, "site", "reader", "**", "*.html"), recursive=True)):
        s = open(f, encoding="utf-8", errors="ignore").read()
        rel = os.path.relpath(f, ROOT).replace("\\", "/")
        h1 = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
        # 首段：第一个 <p>…</p>
        p1 = re.search(r"<p[^>]*>(.*?)</p>", s, re.S)
        h2s = re.findall(r"<h2[^>]*>(.*?)</h2>", s, re.S)
        pages.append({
            "path": rel,
            "lib": rel.split("/")[2],
            "h1": txt(h1.group(1)) if h1 else "",
            "lead": txt(p1.group(1))[:150] if p1 else "",
            "h2": [txt(x)[:40] for x in h2s[:6]],
            "has_plate": "chapter-plate" in s,
            "has_scene": "chapter-scene" in s,
        })

    # 倒排：词 → 页
    def hits(words):
        out = []
        for w in words:
            hs = [p for p in pages if w in p["h1"] or w in p["lead"] or any(w in h for h in p["h2"])]
            if hs:
                out.append({"word": w, "pages": hs})
        return out

    result = []
    for card, meta in CARDS.items():
        if meta["kind"] == "scene":
            hs = hits(meta["words"])
            seen, merged = set(), []
            for grp in hs:
                for p in grp["pages"]:
                    if p["path"] in seen:
                        continue
                    seen.add(p["path"])
                    merged.append(p)
            result.append({"card": card, "kind": "scene", "words": meta["words"],
                           "candidates": merged, "count": len(merged)})
        else:
            hs = hits(WHO_WORDS[meta["who"]])
            seen, merged = set(), []
            for grp in hs:
                for p in grp["pages"]:
                    if p["path"] in seen:
                        continue
                    seen.add(p["path"])
                    merged.append(p)
            result.append({"card": card, "kind": "figure", "who": meta["who"],
                           "words": WHO_WORDS[meta["who"]],
                           "candidates": merged, "count": len(merged)})

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=1)

    for r in result:
        print(f"\n=== {r['card']}  [{r['kind']}]  命中 {r['count']}")
        for p in r["candidates"][:12]:
            tag = []
            if p["has_plate"]:
                tag.append("plate")
            if p["has_scene"]:
                tag.append("scene")
            print(f"   [{'/'.join(p['lib'].split('/'))}] {p['h1'][:34]:36} {'+'.join(tag) or '-':11} {p['path']}")
    print("\n写出:", os.path.relpath(OUT, ROOT).replace("\\", "/"))


if __name__ == "__main__":
    main()
