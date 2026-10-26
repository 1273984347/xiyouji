#!/usr/bin/env python
"""_s4_papercheck_a_cite_extract.py — A 轨论文引用结构抽取（一次性·只读）

A 轨无投稿版 docx（bundled papercheck 提取器不适用），改以 Markdown 源做结构抽取：
- 正文（## 参考文献 之前）内 [n] / [n-m] 标记与 [^n] 脚注标记的计数（预期：均为 0）
- 「## 参考文献」节 [n] 条目清单（主稿与匿名稿比对）
- 原著引文行（> 原文引文）计数

输出：tmpe/papercheck_a_cite_evidence.json
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(r"d:\xiyouji")
FILES = {
    "main": ROOT / "docs/S4-学术投稿/01-论文/明清小说方向-投稿版.md",
    "anon": ROOT / "docs/S4-学术投稿/01-论文/明清小说方向-匿名稿.md",
}
MARK = re.compile(r"\[\d+(?:\s*[-–]\s*\d+)?\]")
FN = re.compile(r"\[\^\d+\]")
REF = re.compile(r"^\[(\d+)\]\s*(.+)$", re.M)
QUOTE = re.compile(r"^>\s*原文引文", re.M)


def main() -> int:
    out: dict[str, dict] = {}
    for key, path in FILES.items():
        t = path.read_text(encoding="utf-8")
        if "## 参考文献" in t:
            body, refs = t.split("## 参考文献", 1)
        else:
            body, refs = t, ""
        out[key] = {
            "file": str(path),
            "body_numeric_markers": [m.group(0) for m in MARK.finditer(body)],
            "body_footnote_markers": [m.group(0) for m in FN.finditer(body)],
            "ref_entries": {m.group(1): m.group(2).strip() for m in REF.finditer(refs)},
            "quote_lines": len(QUOTE.findall(body)),
        }
    m, a = out["main"], out["anon"]
    refs_identical = m["ref_entries"] == a["ref_entries"]
    print("== main ==")
    print("body numeric markers:", len(m["body_numeric_markers"]))
    print("body footnote markers:", len(m["body_footnote_markers"]))
    print("ref entries:", sorted(int(k) for k in m["ref_entries"]))
    print("quote lines:", m["quote_lines"])
    print("== anon ==")
    print("body numeric markers:", len(a["body_numeric_markers"]))
    print("body footnote markers:", len(a["body_footnote_markers"]))
    print("ref entries:", sorted(int(k) for k in a["ref_entries"]))
    print("quote lines:", a["quote_lines"])
    print("refs identical main/anon:", refs_identical)
    OUT = ROOT / "tmpe/papercheck_a_cite_evidence.json"
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print("out:", OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
