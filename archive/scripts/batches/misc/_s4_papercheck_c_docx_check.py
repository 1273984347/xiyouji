#!/usr/bin/env python
"""_s4_papercheck_c_docx_check.py — C 轨投稿版 docx 交付件结构检查（一次性·只读）

核查项：真 Word 脚注条目数、正文脚注引用数、图版数（word/media）、脚注编号
设置（settings.xml 的 w:footnotePr，_c_track_docx_footnote_fix.py 的补丁痕迹）。
输出：标准输出 JSON + tmpe/papercheck_c_docx_check.json
"""
from __future__ import annotations

import json
import re
import zipfile
from pathlib import Path

DOCX = Path(r"d:\xiyouji\docs\S4-学术投稿\可验证性方向-投稿版.docx")
OUT = Path(r"d:\xiyouji\tmpe\papercheck_c_docx_check.json")


def main() -> int:
    z = zipfile.ZipFile(DOCX)
    names = z.namelist()
    doc = z.read("word/document.xml").decode("utf-8")
    fn = z.read("word/footnotes.xml").decode("utf-8") if "word/footnotes.xml" in names else ""
    settings = z.read("word/settings.xml").decode("utf-8") if "word/settings.xml" in names else ""
    result = {
        "docx": str(DOCX),
        "size": DOCX.stat().st_size,
        "footnotes_xml_present": "word/footnotes.xml" in names,
        "footnote_entries": len(re.findall(r'<w:footnote [^>]*w:id="(?!-1|0")', fn)),
        "footnote_references_in_document": doc.count("footnoteReference"),
        "media_count": len([n for n in names if n.startswith("word/media/")]),
        "media_files": sorted(n.split("/")[-1] for n in names if n.startswith("word/media/")),
        "settings_has_footnotePr": "w:footnotePr" in settings,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
