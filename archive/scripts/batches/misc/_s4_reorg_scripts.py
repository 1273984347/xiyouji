# _s4_reorg_scripts.py — 论文文件迁移后的脚本路径常量修正（一次性·断言式）

REPS = [
    ("S4-学术投稿/学术论文-", "S4-学术投稿/01-论文/学术论文-"),
    ("S4-学术投稿/学术论文C轨", "S4-学术投稿/01-论文/学术论文C轨"),
    ("S4-学术投稿\\学术论文-", "S4-学术投稿\\01-论文\\学术论文-"),
    ("S4-学术投稿\\学术论文C轨", "S4-学术投稿\\01-论文\\学术论文C轨"),
]
# B 轨不受影响：上述模式均不匹配 "S4-学术投稿/05-投稿/装饰投稿/学术论文B轨" 与 "S4-学术投稿\\学术论文B轨"
FILES = [
    r"scripts\_audit_a_track_paper_data.py",
    r"scripts\_audit_c_track_paper_data.py",
    r"scripts\_s4_papercheck_a_cite_extract.py",
    r"scripts\_s4_papercheck_c_cite_extract.py",
    r"scripts\_s4a_note_conversion.py",
    r"scripts\_w613_a_anon.py",
    r"scripts\_w613_a_track.py",
    r"scripts\_s4_c_sync_snapshot.py",
    r"scripts\_c_track_docx_footnote_fix.py",
]
for f in FILES:
    text = open(f, encoding="utf-8").read()
    total = 0
    for old, new in REPS:
        n = text.count(old)
        if n:
            text = text.replace(old, new)
            total += n
    if total:
        open(f, "w", encoding="utf-8", newline="").write(text)
    print("%-46s %d 处" % (f, total))
# 全仓残留校验：论文路径旧形态应为 0
left = 0
for f in FILES:
    t = open(f, encoding="utf-8").read()
    for old, _ in REPS:
        left += t.count(old)
print("残留旧路径:", left, "（期望 0）")
assert left == 0
