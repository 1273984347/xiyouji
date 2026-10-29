# -*- coding: utf-8 -*-
"""_w1018_pick2.py — W1016 选材第二轮：只扫「候选新角色」词（补词典·避开已出 100 slug）

已出 100 个 slug 的对照（人工核对结论）：
  已出人物类 = 悟空/唐僧/八戒/沙僧/白龙马/观音/二郎/白骨精/红孩儿/金角/银角/牛魔王/
  铁扇公主/蝎子精/黄袍怪/镇元大仙/大鹏金翅雕/太上老君/独角兕大王/灵感大王/黄风怪/
  赛太岁/九灵元圣/哪吒/昴日星官/黄眉大王/黑熊精/托塔李靖/玉兔精/如来/玉皇大帝/
  百眼魔君/嫦娥/罗刹女/奎木狼 + W1001 批 12（敖广/袁守诚/萧瑀/六贼/沙僧/群妖/…）
  + W1013 批 12（菩提祖师/金蝉子/太白金星/灵吉菩萨/乌鸡国王/虎力大仙/蜘蛛精/白鹿精/
  老鼠精/辟寒大王/玉华王/地藏王）
⇒ 本轮词典只放**候选新角色**，逐回打上下文片段（证据），供定 12 个。

用法：py -3 scripts/_w1018_pick2.py
"""
import io
import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CANDS = [
    "虎先锋", "羊力大仙", "鹿力大仙", "金兜大王", "青牛", "摩昂", "老鼋", "鼋",
    "蜈蚣精", "多目怪", "毒敌大王", "青狮", "白象", "孔雀大明王", "孔雀",
    "秦广王", "崔判官", "寇员外", "杏仙", "木仙", "十八公", "拂云叟",
    "善财运使", "全真", "虎力大仙", "辟寒", "辟暑", "辟尘", "黄风大王",
    "虎都", "虎穴", "巴山虎", "倚海龙", "九尾狐狸", "赛太岁", "鹿力",
    "羊力", "虎力", "灵感大王", "鼍龙", "金毛犼", "赛九尾", "白鹏",
    "孔雀屏", "玉面狐狸", "白面狐狸", "虎穴山", "花果山", "水帘洞",
    "黑松林", "镇海禅林寺", "寇洪", "陈家庄", "魏家", "玉华州", "金顶大仙",
]


def main() -> int:
    reader = os.path.join(REPO, "site", "reader")
    hit_rows = []
    for fn in sorted(os.listdir(reader)):
        if not fn.startswith("ch") or not fn.endswith(".html"):
            continue
        s = io.open(os.path.join(reader, fn), encoding="utf-8", errors="ignore").read()
        if re.search(r'<figure class="chapter-(plate|scene)">', s):
            continue                       # 只看缺口回
        body = s[s.find("<article"):]
        t = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", body))
        h1 = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
        title = re.sub(r"<[^>]+>", "", h1.group(1)).strip() if h1 else ""
        hits = []
        for w in CANDS:
            c = t.count(w)
            if c:
                i = t.find(w)
                hits.append((c, w, t[max(0, i - 60):i + 150]))
        if hits:
            hits.sort(reverse=True)
            hit_rows.append((fn[:5], title, hits))

    print("== 缺口回中命中候选新角色的回（按出现次数）==")
    for ch, title, hits in hit_rows:
        print("\n  %s %s" % (ch, title[:40]))
        for c, w, ctx in hits[:4]:
            print("     [%s×%d] %s" % (w, c, ctx[:170]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
