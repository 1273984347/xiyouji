#!/usr/bin/env python
"""_s4_papercheck_c_cite_extract.py — C 轨论文脚注体例引用证据抽取（一次性·只读）

PaperCheck 适配层：C 轨采用 [^n] 脚注体例，bundled extract_citation_evidence.py
（目标为 [n] 顺序编码制的正文段落）在其 docx 上输出 0/0——Word 脚注存于
footnotes.xml，不在正文段落序列中。本脚本直接解析 Markdown 源（与投稿版 docx
同刻生成、内容一致），抽取：

- 行内标记 [^n] 的全部出现位置与所在段落（含是否落在摘要区）
- 「## 注释」节的定义全文
- 结构核验：标记集↔定义集 1:1、首次出现顺序是否升序、重复出现计数
- 匿名稿对照：标记集与出现总数比对

输出：tmpe/papercheck_c_cite_evidence.json（机器可读证据）
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(r"d:\xiyouji")
OUT = ROOT / "tmpe" / "papercheck_c_cite_evidence.json"

FILES = {
    "main": ROOT / "docs/S4-学术投稿/01-论文/可验证性方向-投稿版.md",
    "anon": ROOT / "docs/S4-学术投稿/01-论文/可验证性方向-匿名稿.md",
}

MARKER = re.compile(r"\[\^(\d+)\]")
DEF = re.compile(r"^\[\^(\d+)\]:\s*(.+)$", re.M)


def paragraphs(text: str) -> list[str]:
    paras = []
    for block in re.split(r"\n\s*\n", text):
        block = block.strip()
        if block:
            paras.append(block)
    return paras


def analyze(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    note_idx = text.index("## 注释")
    body, notes = text[:note_idx], text[note_idx:]
    defs = {int(m.group(1)): m.group(2).strip() for m in DEF.finditer(notes)}
    paras = paragraphs(body)
    abs_end = next((i for i, p in enumerate(paras) if p.startswith("## 一")), -1)
    occ: dict[int, list[dict]] = {}
    for i, p in enumerate(paras):
        for m in MARKER.finditer(p):
            n = int(m.group(1))
            occ.setdefault(n, []).append(
                {
                    "para_index": i,
                    "in_abstract": 0 <= i < abs_end,
                    "para_head": re.sub(r"\s+", " ", p)[:60],
                    "para_text": re.sub(r"\s+", " ", p)[:800],
                }
            )
    first_pos = {n: v[0]["para_index"] for n, v in occ.items()}
    order = sorted(occ, key=lambda n: (first_pos[n], n))
    return {
        "file": str(path),
        "markers_unique": sorted(occ),
        "defs_unique": sorted(defs),
        "missing_defs": sorted(set(occ) - set(defs)),
        "unused_defs": sorted(set(defs) - set(occ)),
        "first_occurrence_order": order,
        "order_is_ascending": order == sorted(order),
        "occurrence_total": sum(len(v) for v in occ.values()),
        "occurrences": {str(n): v for n, v in sorted(occ.items())},
        "definitions": {str(n): defs.get(n) for n in sorted(defs)},
    }


def main() -> int:
    out: dict[str, dict] = {}
    for key, path in FILES.items():
        if path.exists():
            out[key] = analyze(path)
        else:
            out[key] = {"file": str(path), "exists": False}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    main_r = out["main"]
    print("== main ==")
    print("markers:", main_r["markers_unique"])
    print("defs:", main_r["defs_unique"])
    print("missing/unused defs:", main_r["missing_defs"], main_r["unused_defs"])
    print(
        "order ascending:",
        main_r["order_is_ascending"],
        "| total occurrences:",
        main_r["occurrence_total"],
    )
    for n in main_r["markers_unique"]:
        c = main_r["occurrences"][str(n)]
        flag = " [摘要]" if c[0]["in_abstract"] else ""
        print(f"[^{n}] x{len(c)} first@{c[0]['para_index']}{flag} | {c[0]['para_head']}")
    anon = out.get("anon", {})
    if anon.get("markers_unique") is not None:
        print("== anon ==")
        print(
            "markers equal to main:",
            anon["markers_unique"] == main_r["markers_unique"],
            "| occurrences:",
            anon["occurrence_total"],
            "vs main",
            main_r["occurrence_total"],
            "| order ascending:",
            anon["order_is_ascending"],
        )
    print("out:", OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
