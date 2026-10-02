#!/usr/bin/env python3
"""诊断：全仓扫描「疑似引文行」——以 `> 原文引文` 开头但不匹配门禁正则的行。

用途（2026-09-27 A 轨审查 ISSUE-001 配套）：
门禁 check_citations.py 只识别 `^> 原文引文（第N回）：`，格式漂移行被静默跳过
（分母为 0 的"100%"空真）。本脚本先摸清全仓分布，再决定修复面与门禁加固。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CITE_RE = re.compile(r"^> 原文引文（第(\d+)回）：(.*)$")
LOOSE_RE = re.compile(r"^>?\s*原文引文")


def main() -> int:
    suspects = []
    total = 0
    for p in sorted((ROOT / "docs").rglob("*.md")):
        for i, ln in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            s = ln.strip()
            if CITE_RE.match(s):
                total += 1
            elif LOOSE_RE.match(s):
                suspects.append((str(p.relative_to(ROOT)).replace("\\", "/"), i, s[:80]))
    print("recognized_citation_lines:", total)
    print("suspect_lines:", len(suspects))
    for f, i, s in suspects:
        print("  %s:%d  %s" % (f, i, s))
    return 0


if __name__ == "__main__":
    sys.exit(main())