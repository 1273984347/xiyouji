"""S4：TF 文本分区细看（2026-10-05）。"""
t = open(r"d:\xiyouji\tmpe\tf_fulltext.txt", encoding="utf-8").read()

def show(a, b, label):
    seg = t[a:b].replace("\n", " | ")
    print("----- %s [%d:%d] -----" % (label, a, b))
    print(seg[:600])
    print()

show(700, 1650, "top-TOC 区")
show(1650, 3300, "Abstract/KEYWORDS 区")
show(83800, 90500, "Conclusion/Funding/References 区")
show(96000, 99942, "tail 区")
