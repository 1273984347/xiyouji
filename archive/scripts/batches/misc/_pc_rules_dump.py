#!/usr/bin/env python3
"""一次性：取 PaperCheck 规则引擎 raw report（装饰投稿版 docx）并落盘明细。

progressive_papercheck.py 只输出 summary；本脚本直接调 services.report_service
拿 raw_report，写 tmpe/papercheck_rules_submit_raw.json，供逐条核对
「8 处格式问题 / 1 条未使用参考 / 6 条参考计数」的明细。
"""
import json
import sys
from pathlib import Path

RULES_ROOT = Path(r"c:\Users\12739\.trae-cn\plugins\trae-remote-official\tashan-research-skills\1.0.0\skills\papercheck\assets\paperchecker-rules")
DOC = Path(r"d:\xiyouji\docs\S4-学术投稿\05-投稿\装饰投稿\设计方向-装饰投稿版.docx")
OUT = Path(r"d:\xiyouji\tmpe\papercheck_rules_submit_raw.json")

sys.path.insert(0, str(RULES_ROOT))
from services.report_service import analyze_document  # noqa: E402

analysis = analyze_document(str(DOC), author_format="full", citation_standard="ucas")
raw = analysis.get("raw_report", {})
OUT.write_text(json.dumps(raw, ensure_ascii=False, indent=2), encoding="utf-8")
print("summary:", json.dumps(raw.get("summary", {}), ensure_ascii=False))
for k, v in raw.items():
    if isinstance(v, list) and v:
        print("list_field:", k, "len:", len(v))
    if isinstance(v, dict):
        print("dict_field:", k, "keys:", list(v.keys())[:12])
print("written:", OUT)

print("\n=== unused_references ===")
print(json.dumps(raw.get("unused_references", []), ensure_ascii=False, indent=1))
print("\n=== reference_format_issues ===")
print(json.dumps(raw.get("reference_format_issues", []), ensure_ascii=False, indent=1)[:3000])
print("\n=== results(前5条摘要) ===")
for r in raw.get("results", []):
    if isinstance(r, dict):
        keep = {k: r.get(k) for k in ("citation", "reference", "match_type", "matched", "confidence", "issues", "unmatched_reason") if k in r}
        print(json.dumps(keep, ensure_ascii=False)[:500])