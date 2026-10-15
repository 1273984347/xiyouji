# _w555_f1.py — F1: en/81-hardships.html 内嵌 81 行英文清单 + 移除越界 fetch
import io
import json
import re
from collections import Counter

CAUSE = {
    "arranged": "Tathāgata / Guanyin arranged",
    "wild": "True wild demons",
    "mount": "Heavenly / Western steeds incarnate",
    "mind": "Inner demonic obstacles",
}
ENDING = {"taken": "Rescued (with backing)", "killed": "Killed (no backing)", "recruited": "Subdued"}
DIFF = {"solo": "Wukong solved alone", "rescue": "Needed reinforcements"}

NAMES = {
    1: "The Golden Cicada Banished", 2: "Nearly Killed at Birth", 3: "Cast Adrift on the River",
    4: "Seeking Kin, Redressing Wrong", 5: "A Tiger at the City Gate", 6: "Escort Lost in the Pit",
    7: "On Twin Fork Ridge", 8: "At the Boundary Ridge", 9: "A New Horse at the Ravine",
    10: "Fire in the Night", 11: "The Stolen Cassock", 12: "Zhu Bajie Taken In",
    13: "Blocked by Yellow Wind", 14: "Seeking Lingji's Aid", 15: "The Flowing Sands Barrier",
    16: "Sha Wujing Taken In", 17: "The Four Sages Manifest", 18: "Ordeal at Wuzhuang Temple",
    19: "Reviving the Ginseng Tree", 20: "The Mind-Monkey Dismissed", 21: "Lost in Black Pine Forest",
    22: "A Letter from Baoxiang", 23: "Turned Tiger in Court", 24: "Demons of Flat-Top Mountain",
    25: "Honoring Buddha in Wuji", 26: "The Demon's Disguise", 27: "Monster of Numbered Hill",
    28: "The Monk Whirled Away", 29: "The Mind-Monkey Afflicted", 30: "Invoking the Sage's Aid",
    31: "Sunk in the Black River", 32: "Hauling Carts in Chechi", 33: "The Great Contest",
    34: "Daoists Out, Monks In", 35: "The Great Flood on the Road", 36: "Sunk in the Heavenly River",
    37: "The Fish-Basket Revelation", 38: "Demon of Golden Hat Mountain", 39: "Heaven's Host Cannot Subdue",
    40: "Asking Buddha the Origin", 41: "Sick from the River Water", 42: "Held in Marriage at West Liang",
    43: "Torment in the Pipa Cave", 44: "The Mind-Monkey Dismissed Again", 45: "Telling the False Monkey",
    46: "Blocked at Flaming Mountain", 47: "Seeking the Palm-Leaf Fan", 48: "Binding the Bull Demon King",
    49: "Sweeping the Pagoda", 50: "Demon at the Precious Grove", 51: "The Holy Monk Captured",
    52: "The Persimmon Lane", 53: "Medicine in Zhuzi Kingdom", 54: "Rescuing the Stolen Queen",
    55: "Subduing the Demon, Recovering the Queen", 56: "Bajie Carried Away", 57: "In the Silk-Spinning Cave",
    58: "Bajie at the Cleansing Spring", 59: "The Great Sage Banished", 60: "Blocked at Lion-Camel Ridge",
    61: "Gloom over the City", 62: "Golden Clangs in the Void", 63: "Saving the Boys of Biqiu",
    64: "Telling Demon from Man", 65: "Chasing the Rhinoceros Demons", 66: "A Marriage Proposal in India",
    67: "Detained at Tongtai", 68: "Reborn at Cloud-Reaching Ford", 69: "Scriptures Incomplete",
    70: "Pearls Hung Aloft", 71: "Taking Color and Form", 72: "Meeting Fierce Beasts",
    73: "Wind, Snow and Ice", 74: "Into the Turtle's Depths", 75: "The Dark Demon's Mischief",
    76: "The Old Turtle Sinks", 77: "The Canon Not Yet Whole", 78: "Thunderclap in the Buddha's Land",
    79: "Scriptures Spread Abroad", 80: "The Road Home from India", 81: "The Five Sages Made Perfect",
}

src = json.load(open('scripts/output/data/hardships_81.json', encoding='utf-8'))
rows = src['hardships'] if isinstance(src, dict) else src
assert len(rows) == 81

built = []
for r in rows:
    n = r['n']
    built.append({
        "n": n,
        "name": NAMES[n],
        "chapter": "Prologue" if str(r['chapter']) == '前传' else str(int(r['chapter'])),
        "cause": CAUSE[r['cause']],
        "ending": ENDING[r['ending']],
        "difficulty": DIFF[r['difficulty']],
    })

# 聚合与页面 KPI 断言一致（防翻译批次引入数据矛盾——L1 规则3 同页计数）
p = 'site/en/81-hardships.html'
html = io.open(p, encoding='utf-8').read()
mc = re.search(r'by_cause:\s*\{(.*?)\}', html, re.S)
me = re.search(r'by_ending:\s*\{(.*?)\}', html, re.S)
md = re.search(r'by_difficulty:\s*\{(.*?)\}', html, re.S)
page_by_cause = dict(re.findall(r'"([^"]+)":\s*(\d+)', mc.group(1)))
page_by_ending = dict(re.findall(r'"([^"]+)":\s*(\d+)', me.group(1)))
page_by_diff = dict(re.findall(r'"([^"]+)":\s*(\d+)', md.group(1)))
cc = Counter(b['cause'] for b in built)
ce = Counter(b['ending'] for b in built)
cd = Counter(b['difficulty'] for b in built)
assert all(int(page_by_cause[k]) == cc[k] for k in page_by_cause), (page_by_cause, cc)
assert all(int(page_by_ending[k]) == ce[k] for k in page_by_ending), (page_by_ending, ce)
assert all(int(page_by_diff[k]) == cd[k] for k in page_by_diff), (page_by_diff, cd)

# cross_cause_ending 断言
mx = re.search(r'cross_cause_ending:\s*\{(.*?)\n\s*\},', html, re.S)
page_cross = {}
for cm in re.finditer(r'"([^"]+)":\s*\{([^}]*)\}', mx.group(1)):
    page_cross[cm.group(1)] = dict(re.findall(r'"([^"]+)":\s*(\d+)', cm.group(2)))
built_cross = {}
for b in built:
    built_cross.setdefault(b['cause'], Counter())[b['ending']] += 1
for cause, endmap in page_cross.items():
    for ending, v in endmap.items():
        assert built_cross[cause][ending] == int(v), (cause, ending, v, built_cross[cause][ending])
print('聚合断言全过（by_cause/by_ending/by_difficulty/cross）')

# 生成 JS 数组文本
lines = []
for b in built:
    lines.append('            {"n": %d, "name": "%s", "chapter": "%s", "cause": "%s", "ending": "%s", "difficulty": "%s"},'
                 % (b['n'], b['name'], b['chapter'], b['cause'], b['ending'], b['difficulty']))
arr_text = '\r\n'.join(lines).rstrip(',') if '\r' in html[:2000] else '\n'.join(lines).rstrip(',')
nl = '\r\n' if '\r\n' in html else '\n'
arr_text = nl.join(l.rstrip(',') for l in [x.strip() for x in []]) # noop guard
arr_text = nl.join(
    '            ' + json.dumps(b, ensure_ascii=False) for b in built
)

# 1) 填充 hardships 数组
m = re.search(r'(hardships:\s*\[)\s*(\]\s*\};)', html)
assert m, 'hardships 空数组定位失败'
html = html[:m.start()] + 'hardships: [' + nl + arr_text + nl + '        ]' + html[m.end(2) - 1:]

# 2) 注释更新
html = html.replace('// 81 难完整清单：默认为空，由 ../scripts/output/data/hardships_81.json 提供',
                    '// 81 难完整清单（英译名 + 英文标签，W555 F1 内嵌；聚合与下方 by_* 断言一致）')

# 3) 移除越界 fetch（scripts/output 在 site/ 之外，部署态 404；且中文码数据会覆盖英文标签）
old_load = re.search(r'    // 加载数据（fetch 失败则用嵌入数据）.*?\n    \}', html, re.S)
assert old_load, 'loadData 定位失败'
new_load = (
    '    // 加载数据（W555 F1：清单已内嵌，直用嵌入数据——原 fetch 指向 site 外路径，'
    + 'file:// 与 Pages 部署态双断，且中文码数据会覆盖本页英文标签）' + nl
    + '    async function loadData() {' + nl
    + "        document.getElementById('dataSource').innerHTML =" + nl
    + "            'Data source: embedded full list (works offline / file:// / GitHub Pages)';" + nl
    + '        return EMBEDDED_DATA;' + nl
    + '    }'
)
html = html[:old_load.start()] + new_load + html[old_load.end():]

io.open(p, 'w', encoding='utf-8', newline='').write(html)
print('F1 落盘：81 行内嵌 + fetch 移除')
