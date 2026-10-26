"""W949 · ① 堵回归漏洞：dataset 数据源的 emoji 图标字段 → 图标名

根因：W946 只改了页面**内嵌副本**（site/data/timeline.html）的 icon 字段，
      没改**数据源** dataset/timeline.json ⇒ 任何一次跑生成器都会把 emoji 灌回页面
      ⇒ 治理结果不可复现（假收敛）。
处置：数据源按与页面相同的 22 条顺序，emoji → 语义专属图标名（tl-*）。
"""
import json
import pathlib
import re
import sys

sys.path.insert(0, "scripts")
ORDER = [
    "tl-pilgrim", "tl-scroll", "tl-star-spark", "tl-mask", "tl-codex", "tl-taiji",
    "tl-critical-edition", "tl-codex", "tl-taiji", "tl-brush-comment", "tl-punctuation",
    "tl-critical-edition", "tl-pencil", "tl-database", "tl-mask", "tl-newyear-print",
    "tl-comic", "tl-film", "tl-tv", "tl-mask", "tl-film", "tl-gamepad",
]

p = pathlib.Path("dataset/timeline.json")
raw = p.read_text(encoding="utf-8")
found = re.findall(r'("icon":\s*")([^"]*)(")', raw)
print(f"数据源 icon 字段 {len(found)} 个（期望 22）")
if len(found) != len(ORDER):
    print("!! 数量与顺序表不符·中止（防错位）")
    raise SystemExit(2)
if all(v == ORDER[i] for i, (_, v, _) in enumerate(found)):
    print("① 数据源已是图标名（此前已改）·跳过")
else:
    it = iter(ORDER)
    out = re.sub(r'("icon":\s*")[^"]*(")',
                 lambda m: m.group(1) + next(it) + m.group(2), raw)
    p.write_text(out, encoding="utf-8")
    print("① dataset/timeline.json 已改：emoji → 图标名")

# 校验：数据源与页面内嵌副本逐条一致
page = pathlib.Path("site/data/timeline.html").read_text(encoding="utf-8")
ds = re.findall(r'"icon":\s*"([^"]*)"', p.read_text(encoding="utf-8"))
pg = re.findall(r"icon:\s*'([^']*)'", page)
print(f"  数据源 {len(ds)} 条 / 页面内嵌 {len(pg)} 条 · 逐位一致: {ds == pg}")
if ds != pg:
    print("  !! 两处不一致：")
    for i, (a, b) in enumerate(zip(ds, pg)):
        if a != b:
            print(f"     第 {i+1} 条：数据源 {a} ≠ 页面 {b}")
    raise SystemExit(2)

# 顺带核对 en 版页面
en = pathlib.Path("site/en/timeline.html").read_text(encoding="utf-8")
enp = re.findall(r"icon:\s*'([^']*)'", en)
print(f"  英文版 {len(enp)} 条 · 与数据源一致: {enp == ds}")
print("done")
