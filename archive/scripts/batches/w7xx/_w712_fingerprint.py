"""W712 一次性：BL-24 搬迁内容指纹对账（挑刺 #6 P0 闭环）——git a998581d 时代 AGENTS §4.2/§4.3
原文 vs docs/agent/gates.md/pitfalls.md 现文的标题/首句/整行三级对账。
结果：40 条标题全在位、31 条首句全命中、31 条整行守恒 0 缺失（零丢失实证）。留档备复跑。"""

import re
import subprocess
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REV = "a998581d"  # 搬迁前最后一态（W708 收官）
old = subprocess.run(["git", "show", f"{REV}:AGENTS.md"], capture_output=True, text=True, encoding="utf-8").stdout
issues = []

i42 = old.find("### 4.2")
i43 = old.find("### 4.3")
sec42 = old[i42:i43]
old_gates = re.findall(r"^(\d+)\. \*\*(.+?)\*\*", sec42, re.M)
assert len(old_gates) == 40, len(old_gates)
gates_now = open("docs/agent/gates.md", encoding="utf-8").read()
for num, title in old_gates:
    if f"**{title}**" not in gates_now:
        issues.append(f"gates.md 缺条目 {num}. {title[:40]}")

sec43 = old[i43 : old.find("### 4.4")]
tips = [ln for ln in sec43.splitlines() if ln.startswith("- **")]
assert len(tips) == 31, len(tips)
pit_now = open("docs/agent/pitfalls.md", encoding="utf-8").read()
whole_missing = []
for t in tips:
    body = t.lstrip("- ").strip()
    if body[:30] not in pit_now:
        issues.append(f"pitfalls.md 缺条目首句: {body[:40]}")
    if body not in pit_now:
        whole_missing.append(body[:44])

print(f"§4.2 40 条标题对账: {'OK' if not any(i.startswith('gates') for i in issues) else '有缺'}")
print(f"§4.3 31 条首句对账: {'OK' if not any(i.startswith('pitfalls') for i in issues) else '有缺'}")
print(f"§4.3 31 条整行守恒缺失: {len(whole_missing)}")
for w in whole_missing:
    print("  -", w)
print(f"ISSUES: {len(issues)}")
sys.exit(1 if issues else 0)
