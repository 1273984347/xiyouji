#!/usr/bin/env python3
"""W504 一次性：生成 content-trust-report.json + .md（三值分布 + 未核验学术轨清单 + 时间戳）。"""
import datetime
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIRS = ["01-全书逐回解读", "02-人物深度分析", "03-主题与情节专题",
        "04-文化与历史背景", "05-诗词歌赋", "06-个人随笔"]
ACAD = set(open(os.path.join(ROOT, "scripts", "output", "_w504_acad_list.txt"),
                encoding="utf-8").read().strip().splitlines())

stats = {"未核验": 0, "引文已核验": 0, "专家已核验": 0}
acad_green = 0
unverified_acad = []

for d in DIRS:
    dp = os.path.join(ROOT, "docs", d)
    for fn in sorted(os.listdir(dp)):
        if not fn.endswith(".md") or fn == "README.md":
            continue
        rel = "docs/%s/%s" % (d, fn)
        text = open(os.path.join(dp, fn), encoding="utf-8").read()
        m = re.search(r"^> 核验状态：(\S+)", text, re.M)
        st = m.group(1) if m else "未核验"
        stats[st] = stats.get(st, 0) + 1
        if rel in ACAD:
            if st == "引文已核验":
                acad_green += 1
            else:
                c = len(re.findall(r"^> (?:原文)?引文", text, re.M))
                unverified_acad.append({"file": rel, "citations": c})

report = {
    "generated_at": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z"),
    "total_documents": sum(stats.values()),
    "distribution": stats,
    "academic_track_total": len(ACAD),
    "academic_track_green": acad_green,
    "unverified_academic_track": unverified_acad,
    "sum_check": sum(stats.values()),
}

op = os.path.join(ROOT, "scripts", "output")
json.dump(report, open(os.path.join(op, "content-trust-report.json"), "w",
                       encoding="utf-8"), ensure_ascii=False, indent=2)

md = []
md.append("# 内容可信度报告（W504 · A+ 路径）")
md.append("")
md.append("- 生成时间：%s" % report["generated_at"])
md.append("- 总文档数：%d（A1–A6 内容，不含 README）" % report["total_documents"])
md.append("- 三值分布：未核验 %d · 引文已核验 %d · 专家已核验 %d"
          % (stats["未核验"], stats["引文已核验"], stats["专家已核验"]))
md.append("- 三值合计校验：%s" % ("通过" if report["sum_check"] == report["total_documents"] else "失败"))
md.append("- 学术轨：%d 篇 · 绿标（引文已核验）%d 篇 · 未核验 %d 篇"
          % (report["academic_track_total"], acad_green, len(unverified_acad)))
md.append("- A+ 目标达成：%s" % ("是（G=105）" if acad_green == 105 else "否（G=%d）" % acad_green))
md.append("")
md.append("## 未核验学术轨清单（引文行数）")
md.append("")
if unverified_acad:
    md.append("| 文件 | 引文行数 |")
    md.append("|:---|:---|")
    for it in unverified_acad:
        md.append("| %s | %d |" % (it["file"], it["citations"]))
else:
    md.append("（无——学术轨 105 篇已全部标绿）")
md.append("")
open(os.path.join(op, "content-trust-report.md"), "w", encoding="utf-8", newline="\n").write("\n".join(md))
print("报告生成：分布=%s · 学术轨绿标=%d/%d · 合计校验=%s"
      % (stats, acad_green, len(ACAD), "通过" if report["sum_check"] == report["total_documents"] else "失败"))
