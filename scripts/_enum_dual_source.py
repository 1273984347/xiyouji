#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_enum_dual_source.py — W565/C-1：枚举「EMBEDDED 完整 + fetch 同源」双源页。

判定（方案档 §C-1）：
  ① 页面存在 const EMBEDDED / EMBEDDED_DATA；
  ② 页面存在 A-3 改写后的站内 fetch 形态（'json/' 前缀 fetch/baseUrl/DATA_DIR/const base）；
输出：scripts/output/dual-source-pages.txt——每页一行
  <相对路径>\t<EMBEDDED块字节数>\t<fetch形态次数>，按 EMBEDDED 体量降序。
C-2 处置范围由体量决定：EMBEDDED 大（双传输浪费显著）→ 单源化；
EMBEDDED 很小 → 登记「保留 fetch」（收益微小，保留数据独立更新能力）。

用法：python scripts/_enum_dual_source.py
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
OUT = os.path.join(ROOT, "scripts", "output", "dual-source-pages.txt")

EMBED_RE = re.compile(r"const\s+(EMBEDDED_DATA|EMBEDDED)\s*=\s*(\{[\s\S]*?\n\s*\};)")
FETCH_RE = re.compile(r"fetch\([^)]*['\"](?:\.\./)*(?:\./)?(?:data/)?json/")
# baseUrl/DATA_DIR 变量拼接形态：fetch(path) 内无字面量，以 loadJson 调用 + json/ 赋值识别
VAR_RE = re.compile(r"['\"]json/['\"]")
LOADJSON_RE = re.compile(r"loadJson\(")


def main():
    rows = []
    for dirpath, _, files in os.walk(SITE):
        if any(seg.startswith(".") for seg in dirpath.split(os.sep)):
            continue
        for fn in files:
            if not fn.endswith(".html"):
                continue
            p = os.path.join(dirpath, fn)
            with open(p, encoding="utf-8", newline="", errors="ignore") as f:
                s = f.read()
            m = EMBED_RE.search(s)
            if not m:
                continue
            fetches = len(FETCH_RE.findall(s))
            if fetches == 0 and VAR_RE.search(s) and LOADJSON_RE.search(s):
                fetches = len(LOADJSON_RE.findall(s))  # 变量拼接形态按 loadJson 调用数计
            if fetches == 0:
                continue
            rows.append((len(m.group(2)), os.path.relpath(p, ROOT), fetches))
    rows.sort(reverse=True)
    with open(OUT, "w", encoding="utf-8", newline="") as f:
        for size, rel, n in rows:
            f.write(f"{rel}\t{size}\t{n}\n")
    total = sum(r[0] for r in rows)
    big = [r for r in rows if r[0] >= 50 * 1024]
    print(f"双源页共 {len(rows)} · EMBEDDED 合计 {total/1024:.0f}KB · ≥50KB 的 {len(big)} 页：")
    for size, rel, n in rows[:12]:
        print(f"  {size/1024:7.1f}KB  fetch×{n}  {rel}")
    print("清单已写出", os.path.relpath(OUT, ROOT))


if __name__ == "__main__":
    main()
