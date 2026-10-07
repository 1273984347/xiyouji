"""补充批候选筛选：中外交流/近代/理论方法（2026-10-06·一次性·只打印）。"""
import json
import re

items = json.load(open(r"d:\xiyouji\scripts\_s4_bift_all400.json", encoding="utf-8"))
TAKEN = re.compile("八角纹|纪念馆|本土化|原真|数智时代|龙凤虎纹|克拉克|模仿与改制|百褶裙|女褂|扎染|视域下的传统服饰纹样|解码混沌|虹桥|参军戏|口述史|存在论转向|罗兰|设计师身份的变迁|持扇|图画与屏幕|撒马尔罕|研究范式建构|卫生宣传画|石器时代|百苗图|羊角花|蜀地佛教版画|舟溪式|板瑶|三星堆|花腰傣|淄博")
KW = re.compile("中外|域外|西方|欧洲|日本|交流|互鉴|丝路|丝绸之路|海外|近代|民国|晚清|明清|宋代|唐代|传播|影响|观念|理论|美学|批评|方法")
cnt = 0
for a in items:
    t = re.sub(r"<br\s*/?>", " ", a.get("Title") or "")
    t = re.sub(r"\s+", " ", t).strip()
    if KW.search(t) and not TAKEN.search(t) and cnt < 18:
        cnt += 1
        au = re.sub(r"[（(].*?[)）]", "", (a.get("AuthorsList") or ""))
        print("  [%s] %s | %s" % (a.get("YearIssue_No"), t[:46], au[:18]))
print("共 %d 条" % cnt)
