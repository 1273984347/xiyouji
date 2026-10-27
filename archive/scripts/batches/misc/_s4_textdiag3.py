"""S4：TF 尾部边界探位（2026-10-05）。"""
t = open(r"d:\xiyouji\tmpe\tf_fulltext.txt", encoding="utf-8").read()
for m in ["Corporate access solutions", "Help and contact", "Newsroom", "Keep up to date",
          "Related articles", "Latest articles", "Sign me up", "Receive personalised research",
          "Footer", "The American University in Cairo", "Rhee, W. H., and Y. J. Kim. 2024"]:
    pos = t.find(m)
    print("%-36s %s" % (m, pos))
print()
i = t.find("Corporate access solutions")
if i > 0:
    print(t[max(0, i-900):i+100].replace("\n", " | "))
