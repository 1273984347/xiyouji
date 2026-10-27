"""S4：ACM/TF 转存文本边界诊断（2026-10-05）。"""
import re

for name, path in [("ACM", r"d:\xiyouji\tmpe\acm_fulltext.txt"), ("TF", r"d:\xiyouji\tmpe\tf_fulltext.txt")]:
    t = open(path, encoding="utf-8").read()
    print("=====", name, "| total:", len(t))
    marks = ["We developed an AI-assisted", "Abstract", "ABSTRACT", "Introduction", "Keywords", "KEYWORDS",
             "Conclusion", "References", "REFERENCES", "Funding", "Acknowledg", "Notes on contributors",
             "Index Terms", "Information & Contributors", "Bibliometrics", "Reading Options",
             "Full article:", "Spatializing", "Simdogihaeng"]
    for m in marks:
        pos = [x.start() for x in re.finditer(re.escape(m), t)]
        if pos:
            print("  %-28s n=%d  first=%d  last=%d" % (m, len(pos), pos[0], pos[-1]))
    print()
