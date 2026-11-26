#!/usr/bin/env python3
"""_w1331_merge_reports.py — W1331 竖版图表双视口报告合并（一次性·复算口径）。

口径（报告 §1.4）：
  - 压缩项只取 375（DESIGN 最小验收视口）——320 下运行时按容器重设 viewBox 的响应式
    小图会把 vbw 压成容器宽，若混入会把伪压缩当固定宽去加 min-width；
  - 320 只补「文字越出视口」项（窄屏更易越界）。
输出：scripts/output/_w1331_chart_portrait_report_merged.json（供 fix --report 使用）。

用法：
  py -3 scripts/_w1331_merge_reports.py
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "scripts", "output")


def load(name):
    return json.load(open(os.path.join(OUT_DIR, name), encoding="utf-8"))


def main():
    a = load("_w1331_chart_portrait_report_375.json")
    b = load("_w1331_chart_portrait_report_320.json")
    pages = {}
    for p in a["pages"]:
        ent = pages.setdefault(p["page"], {"page": p["page"], "vw": 375,
                                           "overflow": p.get("overflow", 0),
                                           "canvases": [], "svgCharts": {}})
        for c in p.get("svgCharts", []):
            ck = c.get("id") or c.get("cls") or (c.get("parentCls") or "") + "#" + str(c.get("vbw"))
            ent["svgCharts"][ck] = dict(c)
    for p in b["pages"]:
        ent = pages.setdefault(p["page"], {"page": p["page"], "vw": 320,
                                           "overflow": p.get("overflow", 0),
                                           "canvases": [], "svgCharts": {}})
        for c in p.get("svgCharts", []):
            if not c.get("outOfViewport"):
                continue
            ck = c.get("id") or c.get("cls") or (c.get("parentCls") or "") + "#" + str(c.get("vbw"))
            old = ent["svgCharts"].get(ck)
            if old is None:
                ent["svgCharts"][ck] = dict(c)
            else:
                old["outOfViewport"] = max(old.get("outOfViewport") or 0, c["outOfViewport"])
    out = {"viewport": {"width": "375(+320 overflow)"}, "pages": []}
    for ent in pages.values():
        ent["svgCharts"] = list(ent["svgCharts"].values())
        out["pages"].append(ent)
    dst = os.path.join(OUT_DIR, "_w1331_chart_portrait_report_merged.json")
    with open(dst, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("merged pages", len(out["pages"]))


if __name__ == "__main__":
    main()
