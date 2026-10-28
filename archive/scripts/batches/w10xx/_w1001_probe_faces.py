import re

FILES = {
    "HANDOVER.md": ["最后更新", "里程碑", "W1000"],
    ".github/workflows/README.md": ["W1000", "版本"],
    "README.md": ["最后更新", "当前批次"],
    "STRUCTURE.md": ["最后更新", "当前批次"],
    "docs/00-导读/项目说明.md": ["最后更新", "当前批次"],
    "CITATION.cff": ["version"],
}
for f, keys in FILES.items():
    s = open(f, encoding="utf-8").read()
    print("=" * 8, f)
    for i, ln in enumerate(s.split("\n")):
        if any(k in ln for k in keys) and ("W1000" in ln or "最后更新" in ln or "当前批次" in ln
                                          or ("version" in ln and "W" in ln)):
            print("  %4d| %s" % (i + 1, ln[:190]))
