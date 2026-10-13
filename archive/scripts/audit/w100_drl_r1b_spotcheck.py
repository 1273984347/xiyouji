"""DRL R1b spot-check: 关键数据点验证"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

print("=" * 60)
print("DRL R1b spot-check: 关键数据点验证")
print("=" * 60)

# 加载 dialogues.json
dial_path = ROOT / "scripts" / "output" / "data" / "dialogues.json"
with open(dial_path, "r", encoding="utf-8") as f:
    dial = json.load(f)

# ===== Spot-check 1: 第100回引语归属（验证 W100-3 修复点）=====
print("\n--- Spot-check 1: 第100回引语归属 ---")
ch100 = [d for d in dial["dialogues"] if d["chapter"] == 100]
print(f"第100回引语总数: {len(ch100)}")

# 关键测试点：原误判为如来的"他们都成佛，如何把我做个净坛使者？"
target_quote = "他们都成佛"
matches = [d for d in ch100 if target_quote in d["quote"]]
print(f"含 '{target_quote}' 的引语数: {len(matches)}")
for d in matches:
    print(f"  speaker={d['speaker']}, alias={d['alias_used']}, pattern={d['pattern']}")
    print(f"  quote={d['quote'][:80]}...")

# 抽样第100回前5条引语
print("\n第100回前5条引语：")
for d in ch100[:5]:
    print(f"  speaker={d['speaker']}, alias={d['alias_used']}, pattern={d['pattern']}, quote={d['quote'][:50]}...")

# ===== Spot-check 2: 关键人物引语数 =====
print("\n--- Spot-check 2: 关键人物引语数 ---")
for sp in ["孙悟空", "唐僧", "猪八戒", "沙僧", "观音", "如来"]:
    count = sum(1 for d in dial["dialogues"] if d["speaker"] == sp)
    print(f"  {sp}: {count} 条引语")

# ===== Spot-check 3: characters.json 出场回数与原文比对 =====
print("\n--- Spot-check 3: characters.json 关键人物出场回数 ---")
char_path = ROOT / "scripts" / "output" / "data" / "characters.json"
with open(char_path, "r", encoding="utf-8") as f:
    chars = json.load(f)

# 抽样 5 个关键人物的 first_appear 是否合理
# 悟空第1回、唐僧第9回（陈光蕊出场为第9回）、八戒第18回、沙僧第22回、白龙马第15回
expected_first = {
    "孙悟空": 1,
    "唐僧": 9,
    "猪八戒": 18,
    "沙僧": 22,
    "白龙马": 15,
}
for c in chars["characters"][:10]:
    name = c["name"]
    if name in expected_first:
        actual = c["first_appear"]
        expected = expected_first[name]
        match = "✓" if actual == expected else f"✗ (expected {expected})"
        print(f"  {name}: first_appear={actual} {match}, appear_chapters={c['appear_chapters']}, total_mentions={c['total_mentions']}")

# ===== Spot-check 4: cooccurrence.json 唐僧-孙悟空共现 90 回验证 =====
print("\n--- Spot-check 4: 唐僧-孙悟空共现回数验证 ---")
cooc_path = ROOT / "scripts" / "output" / "data" / "cooccurrence.json"
with open(cooc_path, "r", encoding="utf-8") as f:
    cooc = json.load(f)

# 唐僧和孙悟空同时出现的回数应该是 90（唐僧出场 92 回中除第9回前世 + 第12回化身）
ts = next(c for c in chars["characters"] if c["name"] == "唐僧")
wk = next(c for c in chars["characters"] if c["name"] == "孙悟空")
ts_chapters = set(ts["appear_in_chapters"])
wk_chapters = set(wk["appear_in_chapters"])
intersection = ts_chapters & wk_chapters
print(f"  唐僧出场回数: {len(ts_chapters)}")
print(f"  孙悟空出场回数: {len(wk_chapters)}")
print(f"  集合交集: {len(intersection)}")
cl_ts_wk = next(e for e in cooc["chapter_level"]["edges"]
                if {e["source"], e["target"]} == {"唐僧", "孙悟空"})
print(f"  cooccurrence.json 中记录: {cl_ts_wk['weight']}")
print(f"  一致: {'✓' if cl_ts_wk['weight'] == len(intersection) else '✗'}")

# ===== Spot-check 5: EMBEDDED.cooccurrence 与 cooccurrence.json 完全一致 =====
print("\n--- Spot-check 5: EMBEDDED.cooccurrence 与 cooccurrence.json 一致性 ---")
html_path = ROOT / "site" / "data" / "relationships.html"
content = html_path.read_text(encoding="utf-8")

# 找到 cooccurrence: { 起始
cooc_start = content.find("cooccurrence: {")
if cooc_start == -1:
    print("  未找到 EMBEDDED.cooccurrence")
else:
    # 找到对应的闭合 }
    brace_start = content.index("{", cooc_start)
    depth = 0
    brace_end = brace_start
    for i in range(brace_start, len(content)):
        if content[i] == "{":
            depth += 1
        elif content[i] == "}":
            depth -= 1
            if depth == 0:
                brace_end = i
                break
    embedded_str = content[brace_start:brace_end + 1]
    try:
        embedded_cooc = json.loads(embedded_str)
        # 对比节点数和边数
        cl_match = (len(embedded_cooc["chapter_level"]["nodes"]) == len(cooc["chapter_level"]["nodes"])
                    and len(embedded_cooc["chapter_level"]["edges"]) == len(cooc["chapter_level"]["edges"]))
        sl_match = (len(embedded_cooc["scene_level"]["nodes"]) == len(cooc["scene_level"]["nodes"])
                    and len(embedded_cooc["scene_level"]["edges"]) == len(cooc["scene_level"]["edges"]))
        print(f"  chapter_level nodes/edges 一致: {cl_match}")
        print(f"  scene_level nodes/edges 一致: {sl_match}")
        # 抽样对比 Top 1 节点和 Top 1 边
        en0 = embedded_cooc["chapter_level"]["nodes"][0]
        cn0 = cooc["chapter_level"]["nodes"][0]
        print(f"  EMBEDDED Top1 node: {en0}")
        print(f"  JSON Top1 node:     {cn0}")
        print(f"  Top1 node 一致: {en0 == cn0}")
        ee0 = embedded_cooc["chapter_level"]["edges"][0]
        ce0 = cooc["chapter_level"]["edges"][0]
        print(f"  EMBEDDED Top1 edge: {ee0}")
        print(f"  JSON Top1 edge:     {ce0}")
        print(f"  Top1 edge 一致: {ee0 == ce0}")
    except json.JSONDecodeError as e:
        print(f"  EMBEDDED.cooccurrence JSON 解析失败: {e}")

# ===== Spot-check 6: 关键引语原文回溯（验证第100回引语归属准确性）=====
print("\n--- Spot-check 6: 第100回关键引语原文回溯 ---")
# 加载第100回原文
ts_html = (ROOT / "site" / "data" / "text-search.html").read_text(encoding="utf-8")
ch100_match = re.search(r'num:\s*100,\s*\n\s*title:\s*"([^"]+)",.*?text:\s*`([^`]+)`', ts_html, re.DOTALL)
if ch100_match:
    ch100_text = ch100_match.group(2)
    # 查找关键引语
    test_quotes = [
        ("他们都成佛", "猪八戒"),  # 原误判如来，应归属猪八戒
        ("净坛使者", "猪八戒"),
    ]
    for q, expected_speaker in test_quotes:
        if q in ch100_text:
            # 找到 q 所在位置，向前回溯 100 字符找说话者
            idx = ch100_text.find(q)
            ctx = ch100_text[max(0, idx - 100):idx + len(q) + 50]
            print(f"  引语 '{q}' 上下文：")
            print(f"    ...{ctx}...")
            # dialogues.json 中归属
            dj_matches = [d for d in ch100 if q in d["quote"]]
            for d in dj_matches:
                actual = d["speaker"]
                match = "✓" if actual == expected_speaker else f"✗ (expected {expected_speaker})"
                print(f"    dialogues.json 归属: {actual} {match}")
        else:
            print(f"  引语 '{q}' 在第100回原文中未找到")
else:
    print("  第100回原文未找到")

print("\n" + "=" * 60)
print("DRL R1b spot-check 完成")
print("=" * 60)
