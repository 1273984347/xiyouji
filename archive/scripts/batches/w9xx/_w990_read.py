import re

CH = {
    "ch001": ["仙石", "石猴", "花果山"],
    "ch003": ["敖广", "龙宫", "东海"],
    "ch009": ["袁守诚", "渔翁", "钓"],
    "ch011": ["萧瑀", "太宗", "还魂"],
    "ch022": ["流沙河", "八戒", "悟净"],
    "ch028": ["群妖", "聚义", "花果山"],
    "ch047": ["金童", "木童", "通天水"],
    "ch063": ["九头虫", "龙宫", "宝贝"],
    "ch066": ["弥勒", "人种袋"],
    "ch079": ["老寿", "南极", "仙翁"],
    "ch089": ["黄狮", "钉钯", "豹头山"],
    "ch093": ["给孤独", "园", "布袋"],
}

for ch, words in CH.items():
    s = open("site/reader/%s.html" % ch, encoding="utf-8", errors="ignore").read()
    body = s[s.find("<article"):]
    text = re.sub(r"<[^>]+>", "", body)
    text = re.sub(r"\s+", " ", text)
    print("=" * 20, ch)
    for w in words:
        i = text.find(w)
        if i >= 0:
            print("  [%s] %s" % (w, text[max(0, i - 120):i + 220]))
            break
