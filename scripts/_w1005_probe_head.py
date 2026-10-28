import re
import glob

print("=== HANDOVER.md 里行首 `- **W` 的前 6 条（RE_JIAOJIE_HEAD 链首判定）===")
s = open("HANDOVER.md", encoding="utf-8").read()
for m in list(re.finditer(r"^-\s*\*\*(?:v\d+\.\d+\.\d+\s+)?W(\d+)", s, re.M))[:6]:
    print("   @%d  W%s | %s" % (m.start(), m.group(1), s[m.start():m.start() + 90].replace("\n", " ")))

print()
print("=== 全仓「HEAD」+ W 批号 的当前态句 ===")
for f in ["README.md", "STRUCTURE.md", "HANDOVER.md", "docs/00-导读/项目说明.md",
          ".github/workflows/README.md", "AGENTS.md", "docs/00-导读/文档规范.md",
          "docs/README.md", "README.md"]:
    try:
        t = open(f, encoding="utf-8").read()
    except OSError:
        continue
    for i, ln in enumerate(t.split("\n")):
        if "HEAD" in ln and re.search(r"W\d{3,4}", ln) and len(ln) < 400:
            print("   %-30s %4d| %s" % (f, i + 1, ln.strip()[:180]))
