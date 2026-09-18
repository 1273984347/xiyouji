# -*- coding: utf-8 -*-
"""W582 试点前置：TOP 填充色的来源页与设置方式。"""
import json
from collections import defaultdict

rows = [json.loads(l) for l in open("scripts/output/render-state-audit-baseline.jsonl", encoding="utf-8") if l.strip()]
targets = {
    "rgb(0, 0, 0)": set(),
    "rgb(58, 107, 140)": set(),
    "rgb(128, 0, 38)": set(),
}
for r in rows:
    for s in r.get("invisibleShapes", []):
        if s["fill"] in targets:
            targets[s["fill"]].add((r["page"], s["owner"], s["tag"]))

for f, pages in targets.items():
    print(f"== {f}")
    owners = defaultdict(int)
    for pg, owner, tag in pages:
        owners[(pg, owner, tag)] += 1
    for (pg, owner, tag), _ in sorted(owners.items()):
        print(f"   {pg}  {owner}  <{tag}>")
