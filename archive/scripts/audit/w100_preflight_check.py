"""Preflight 三轨验证：cooccurrence.json 与 relationships.html 一致性检查"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ===== Track 1: cooccurrence.json 关键指标 =====
print("=" * 60)
print("Track 1: cooccurrence.json 关键指标")
print("=" * 60)
cooc_path = ROOT / "scripts" / "output" / "data" / "cooccurrence.json"
with open(cooc_path, "r", encoding="utf-8") as f:
    cooc = json.load(f)

cl = cooc["chapter_level"]
sl = cooc["scene_level"]
print(f"chapter_level: nodes={len(cl['nodes'])} edges={len(cl['edges'])}")
print(f"scene_level: nodes={len(sl['nodes'])} edges={len(sl['edges'])}")
print(f"CL top5 nodes: {[(n['id'], n['count']) for n in cl['nodes'][:5]]}")
print(f"CL top5 edges: {[(e['source'], e['target'], e['weight']) for e in cl['edges'][:5]]}")
print(f"SL top5 nodes: {[(n['id'], n['count']) for n in sl['nodes'][:5]]}")
print(f"SL top5 edges: {[(e['source'], e['target'], e['weight']) for e in sl['edges'][:5]]}")

# 关键人物
tangseng = next(n for n in cl["nodes"] if n["id"] == "唐僧")
wukong = next(n for n in cl["nodes"] if n["id"] == "孙悟空")
print(f"\n唐僧 出场回数: {tangseng['count']}")
print(f"孙悟空 出场回数: {wukong['count']}")

# 唐僧-孙悟空 共现
ts_wk = next(e for e in cl["edges"]
             if (e["source"] == "唐僧" and e["target"] == "孙悟空")
             or (e["source"] == "孙悟空" and e["target"] == "唐僧"))
print(f"唐僧-孙悟空 共现回数: {ts_wk['weight']}")

# characters.json
print("\n" + "=" * 60)
print("characters.json 关键指标")
print("=" * 60)
char_path = ROOT / "scripts" / "output" / "data" / "characters.json"
with open(char_path, "r", encoding="utf-8") as f:
    chars = json.load(f)
print(f"total_chapters: {chars['total_chapters']}")
print(f"character_count: {chars['character_count']}")
print(f"Top 5: {[(c['name'], c['appear_chapters'], c['total_mentions']) for c in chars['characters'][:5]]}")

# dialogues.json
print("\n" + "=" * 60)
print("dialogues.json 关键指标")
print("=" * 60)
dial_path = ROOT / "scripts" / "output" / "data" / "dialogues.json"
with open(dial_path, "r", encoding="utf-8") as f:
    dial = json.load(f)
print(f"total_dialogues: {dial['total_dialogues']}")
print(f"speaker_count: {dial['speaker_count']}")
print(f"Top 5 speakers: {dial['speaker_ranking'][:5]}")

# ===== Track 2: relationships.html EMBEDDED 数据嵌入检查 =====
print("\n" + "=" * 60)
print("Track 2: relationships.html EMBEDDED 数据嵌入")
print("=" * 60)
html_path = ROOT / "site" / "data" / "relationships.html"
content = html_path.read_text(encoding="utf-8")

# 改用 brace matching 提取 EMBEDDED 对象（避免 .*? 跨段失败）
emb_start_match = re.search(r'EMBEDDED\s*=\s*\{', content)
if emb_start_match:
    # 找到 EMBEDDED 起始的 '{' 位置
    brace_start = content.index("{", emb_start_match.start())
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
        embedded = json.loads(embedded_str)
        print(f"EMBEDDED keys: {list(embedded.keys())}")
        ecooc = embedded.get("cooccurrence", {})
        ecl = ecooc.get("chapter_level", {})
        esl = ecooc.get("scene_level", {})
        print(f"EMBEDDED.cooccurrence chapter_level: nodes={len(ecl.get('nodes', []))} edges={len(ecl.get('edges', []))}")
        print(f"EMBEDDED.cooccurrence scene_level: nodes={len(esl.get('nodes', []))} edges={len(esl.get('edges', []))}")
        cl_match = (len(ecl.get("nodes", [])) == len(cl["nodes"])
                    and len(ecl.get("edges", [])) == len(cl["edges"]))
        sl_match = (len(esl.get("nodes", [])) == len(sl["nodes"])
                    and len(esl.get("edges", [])) == len(sl["edges"]))
        print(f"chapter_level 一致: {cl_match}")
        print(f"scene_level 一致: {sl_match}")
        # 抽样检查 Top 5 节点和 Top 5 边
        if ecl.get("nodes") and ecl.get("edges"):
            print(f"EMBEDDED CL top5 nodes: {[(n['id'], n['count']) for n in ecl['nodes'][:5]]}")
            print(f"EMBEDDED CL top5 edges: {[(e['source'], e['target'], e['weight']) for e in ecl['edges'][:5]]}")
    except json.JSONDecodeError as e:
        print(f"EMBEDDED JSON 解析失败: {e}")
else:
    print("未找到 EMBEDDED 对象")

# 检查关键渲染函数
render_funcs = [
    "renderCooccurrenceForce",
    "renderCooccurrenceTable",
    "renderCooccurrenceInsights",
    "renderBelbinRadar",
    "renderBelbinLegend",
    "renderBelbinTable",
    "renderBelbinInsights",
]
print("\n渲染函数存在性检查：")
for fn in render_funcs:
    found = f"function {fn}" in content or f"const {fn}" in content
    print(f"  {fn}: {'✓' if found else '✗'}")

# 检查关键 section
sections = [
    ("Section 5 人物共现网络", "人物共现"),
    ("力导向图 svg id", 'id="chart-cooccurrence-force"'),
    ("维度切换 select", 'id="cooc-level-select"'),
    ("边权重 input", 'id="cooc-min-weight"'),
    ("重绘 button", 'id="cooc-redraw"'),
    ("Top 20 关系表", 'id="cooc-table"'),
]
print("\n关键 DOM 元素检查：")
for label, pattern in sections:
    found = pattern in content
    print(f"  {label}: {'✓' if found else '✗'}")

# ===== Track 3: 数据描述一致性 =====
print("\n" + "=" * 60)
print("Track 3: relationships.html 文案数据一致性")
print("=" * 60)
desc_patterns = [
    ("35 节点", "35"),
    ("329 共现边", "329"),
    ("274 场景边", "274"),
    ("90 回共现", "90"),
    ("chapter_level", "chapter_level"),
    ("scene_level", "scene_level"),
]
for label, kw in desc_patterns:
    found = kw in content
    print(f"  {label} ({kw}): {'✓' if found else '✗'}")

# 文件大小
print(f"\nrelationships.html 文件大小: {len(content)} 字节")
print(f"cooccurrence.json 文件大小: {cooc_path.stat().st_size} 字节")
print(f"characters.json 文件大小: {char_path.stat().st_size} 字节")
print(f"dialogues.json 文件大小: {dial_path.stat().st_size} 字节")

print("\n" + "=" * 60)
print("Preflight 三轨验证完成")
print("=" * 60)
