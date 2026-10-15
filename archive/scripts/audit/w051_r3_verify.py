"""W051 R3 完整验证：HTML 数据 vs 原始数据 hardships_81.py 一致性"""
import re
import importlib.util

# 加载原始数据
spec = importlib.util.spec_from_file_location("h", r"d:\1\xiyouji\scripts\C_情节\hardships_81.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
orig = {h["n"]: h for h in m.HARDSHIPS_81}

# 解析 HTML 数据
html = open(r"d:\1\xiyouji\site\data\hardship-heatmap.html", "r", encoding="utf-8").read()
pattern = re.compile(
    r'\{n:(\d+), name:"([^"]+)", chapter:"([^"]+)", chNum:(\d+), '
    r'cause:"([^"]+)", ending:"([^"]+)", difficulty:"([^"]+)", '
    r'score:(\d+), stage:"([^"]+)"\}'
)
html_items = pattern.findall(html)
print(f"HTML items: {len(html_items)}")
print(f"Orig items: {len(orig)}")

# 比对
mismatches = []
for n_str, name, chap, chnum, cause, ending, diff, score, stage in html_items:
    n = int(n_str)
    if n not in orig:
        mismatches.append(f"n={n} NOT in orig")
        continue
    o = orig[n]
    # chapter 字段：orig 用 int (回目数) 或 "前传"
    o_chap_str = str(o["chapter"])
    # HTML 中 "第13回" → 13, "前传" → "前传"
    if o_chap_str == "前传":
        if chap != "前传":
            mismatches.append(f"n={n} chapter: orig=前传, html={chap}")
    else:
        html_chap_num = chap.replace("第", "").replace("回", "")
        if html_chap_num != o_chap_str:
            mismatches.append(f"n={n} chapter: orig={o_chap_str}, html={chap}")
    if o["name"] != name:
        mismatches.append(f"n={n} name: orig={o['name']}, html={name}")
    if o["cause"] != cause:
        mismatches.append(f"n={n} cause: orig={o['cause']}, html={cause}")
    if o["ending"] != ending:
        mismatches.append(f"n={n} ending: orig={o['ending']}, html={ending}")
    if o["difficulty"] != diff:
        mismatches.append(f"n={n} difficulty: orig={o['difficulty']}, html={diff}")

print(f"\nMismatches: {len(mismatches)}")
for m in mismatches[:30]:
    print(f"  {m}")

# KPI 验证
print("\n=== KPI 验证 ===")
scores = [int(s) for s in re.findall(r"score:(\d+)", html)]
import statistics
print(f"总数: {len(scores)} (期望 81)")
print(f"平均难度: {sum(scores)/len(scores):.2f} (HTML 显示 5.5)")
print(f"标准差: {statistics.stdev(scores):.2f} (HTML 显示 2.2)")
hard = [s for s in scores if s >= 9]
print(f"极难数(9-10): {len(hard)} (HTML 显示 8)")
print(f"极难占比: {len(hard)/len(scores)*100:.1f}% (HTML 显示 9.9%)")

# 极难回目列表
hard_chapters = set()
for n_str, name, chap, chnum, cause, ending, diff, score, stage in html_items:
    if int(score) >= 9:
        hard_chapters.add(chap)
print(f"极难回目: {sorted(hard_chapters)}")
print(f"HTML 显示: 第 40/50/52/58/61/74/75 回")
