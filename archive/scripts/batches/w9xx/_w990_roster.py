import re

s = open("assets/promo/plate-set/README.md", encoding="utf-8").read()
rows = re.findall(r"^\| `(plate-line-[^`]+)` \| ([^|]+) \|", s, re.M)
print("plate-set 主体清单（%d 张）:" % len(rows))
for a, b in rows:
    print("  %-40s %s" % (a.strip(), b.strip()))
