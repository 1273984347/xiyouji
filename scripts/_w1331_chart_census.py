#!/usr/bin/env python3
"""_w1331_chart_census.py — W1331 竖版图表专项·静态普查（一次性）。

对 site/data/*.html 与 site/en/*.html 逐页统计图表容器形态：
  - 容器类名：chart-block / chart-wrap / chart-container / chart-scroll / chart-box
  - 图表载体：svg / canvas / THREE
  - 固定宽度风险：width="980" / width:980 / min-width: 6xx/9xx 字面
  - 表格：裸 <table> 与 .table-wrap 包裹
输出：scripts/output/_w1331_chart_census.json + 控制台摘要。
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "scripts", "output", "_w1331_chart_census.json")

CONTAINERS = ["chart-block", "chart-wrap", "chart-container", "chart-scroll", "chart-box"]
PATS = {
    "width_980": r'width\s*=\s*["\']?980|width\s*:\s*980',
    "min_width_literal": r'min-width\s*:\s*(6\d\d|7\d\d|8\d\d|9\d\d)\s*px',
    "table_wrap": r'class\s*=\s*"[^"]*table-wrap',
    "svg": r"<svg\b",
    "canvas": r"<canvas\b",
    "three": r"THREE|three(?:\.min)?\.js",
}


def scan(path):
    t = open(path, encoding="utf-8", errors="ignore").read()
    row = {"page": os.path.relpath(path, os.path.join(ROOT, "site")).replace("\\", "/")}
    row["containers"] = [c for c in CONTAINERS if re.search(r'class\s*=\s*"[^"]*\b' + c + r'\b', t)]
    row["svg"] = len(re.findall(PATS["svg"], t))
    row["canvas"] = len(re.findall(PATS["canvas"], t))
    row["three"] = bool(re.search(PATS["three"], t))
    row["tables"] = len(re.findall(r"<table\b", t))
    row["table_wrap"] = len(re.findall(PATS["table_wrap"], t))
    row["width_980"] = len(re.findall(PATS["width_980"], t))
    row["min_width_literal"] = re.findall(PATS["min_width_literal"], t)[:6]
    row["chartish"] = row["svg"] > 0 or row["canvas"] > 0 or row["three"]
    return row


def main():
    rows = []
    for sub in ("data", "en"):
        d = os.path.join(ROOT, "site", sub)
        if not os.path.isdir(d):
            continue
        for name in sorted(os.listdir(d)):
            if name.endswith(".html"):
                rows.append(scan(os.path.join(d, name)))
    chart = [r for r in rows if r["chartish"]]
    summary = {
        "pages": len(rows),
        "chart_pages": len(chart),
        "no_container": [r["page"] for r in chart if not r["containers"]],
        "width_980": [r["page"] for r in rows if r["width_980"]],
        "min_width_literal": {r["page"]: r["min_width_literal"] for r in rows if r["min_width_literal"]},
        "tables_no_wrap": [
            {"page": r["page"], "tables": r["tables"], "wraps": r["table_wrap"]}
            for r in rows if r["tables"] > r["table_wrap"]
        ],
        "container_dist": {},
    }
    for r in chart:
        key = ",".join(r["containers"]) or "(none)"
        summary["container_dist"][key] = summary["container_dist"].get(key, 0) + 1
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump({"summary": summary, "rows": rows}, f, ensure_ascii=False, indent=1)
    print(json.dumps(summary, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
