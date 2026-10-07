"""按川大艺术学三研究方向筛北服全刊候选（2026-10-06·一次性·只打印不下载）。"""
import json
import re

items = json.load(open(r"d:\xiyouji\scripts\_s4_bift_all400.json", encoding="utf-8"))
TAKEN = re.compile("八角纹|纪念馆|本土化|原真|数智时代|龙凤虎纹|克拉克|模仿与改制|百褶裙|女褂|扎染|视域下的传统服饰纹样|解码混沌|虹桥|参军戏")

DIRS = {
    "①设计理论与历史研究": re.compile("设计史|设计理论|设计思想|造物|工艺美术|包豪斯|现代设计|设计文化|设计观念|设计师|设计教育|设计批评|设计策略|工艺史|设计方法"),
    "②艺术历史、理论与批评研究": re.compile("美术史|艺术史|壁画|画像|石窟|考古|考释|考辨|画派|画坛|艺术批评|艺术理论|美学|画论|画学|品评|书学|雕塑史"),
    "③中国现当代艺术研究": re.compile("当代|现当代|现代艺术|新中国|20世纪|水墨|先锋|实验艺术|现代性|当代审美|当代设计|当代艺术|时代"),
}
seen = set()
for dname, kw in DIRS.items():
    print("\n===== %s =====" % dname)
    cnt = 0
    for a in items:
        t = re.sub(r"<br\s*/?>", "", a.get("Title") or "")
        if kw.search(t) and not TAKEN.search(t) and t not in seen and cnt < 12:
            seen.add(t)
            au = re.sub(r"[（(].*?[)）]", "", (a.get("AuthorsList") or ""))
            print("  [%s] %s | %s" % (a.get("YearIssue_No"), t[:44], au[:20]))
            cnt += 1
    if cnt == 0:
        print("  （无）")
