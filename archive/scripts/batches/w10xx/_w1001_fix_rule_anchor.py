import io
import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(REPO, "CHANGELOG.md")

t = io.open(CH, encoding="utf-8").read()
lines = t.split("\n")
keep_idx = None
for i, ln in enumerate(lines):
    if "编号规则" in ln and "（W001-W" in ln:
        keep_idx = i
        break
if keep_idx is None:
    print("FAIL  未找到编号规则行")
    raise SystemExit(1)

changed = 0
for i, ln in enumerate(lines):
    if i == keep_idx:
        continue
    while "（W001-W" in ln:
        ln = re.sub(r"（W001-W(\d{4})）", r"W001-W\1", ln)
        changed += 1
    lines[i] = ln
new = "\n".join(lines)
tmp = CH + ".tmp"
io.open(tmp, "wb").write(new.encode("utf-8"))
os.replace(tmp, CH)
print("保留行 #%d · 改写 %d 处 · 复核全角形态 %d 处"
      % (keep_idx, changed, len(re.findall(r"（W001-W\d{4}）", new))))
