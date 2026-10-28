import re

FILES = ["CHANGELOG.md", "HANDOVER.md", ".github/workflows/README.md", "README.md",
         "STRUCTURE.md", "docs/00-导读/项目说明.md", "CITATION.cff"]
PAT = re.compile(r"W100[0-9]")
for f in FILES:
    s = open(f, encoding="utf-8").read()
    print("=" * 10, f)
    for i, ln in enumerate(s.split("\n")[:400]):
        if PAT.search(ln) and (("编号规则" in ln) or ("当前" in ln) or ("最后更新" in ln)
                               or ("HEAD" in ln) or ("里程碑" in ln) or ("version" in ln)
                               or ("W450-" in ln)):
            print("  %4d| %s" % (i + 1, ln[:200]))
