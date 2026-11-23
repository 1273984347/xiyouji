#!/usr/bin/env python3
"""W1309 · L-08 目录件伪血缘：一次性订正伪「生成日期/生成时点」元信息行。

性质：**只删元信息行**（内容逐字无损）· **幂等**（删过即无操作）· **单文件隔离**
（非 UTF-8 / IO 异常只记录不中断整批·对抗审查 P2-1/P2-2）。

判定口径（P2-2 收紧）：仅「等值 + 已知后缀白名单」命中 ⇒ **人工行不会被删**
（如「> 生成时点：2026-10-18（人工标注）」不在白名单内）。

用法：py -3 scripts/output/_w1309_fix_legacy_dates.py <清单文件>
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LEGACY_LINES = ("> 生成日期：2026-10-18",)
LEGACY_PREFIXES = ("> 生成时点：2026-10-18 · 由 ",)


def fix_one(rel):
    p = os.path.join(ROOT, rel)
    if not os.path.isfile(p):
        return "missing"
    with open(p, "rb") as f:
        raw = f.read()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        return "nonutf8:" + type(exc).__name__
    nl = "\r\n" if "\r\n" in text else "\n"
    out = []
    hit = 0
    for ln in text.split(nl):
        s = ln.strip()
        if s in LEGACY_LINES or s in LEGACY_PREFIXES:
            hit += 1
            continue
        out.append(ln)
    if not hit:
        return "clean"
    with open(p, "wb") as f:
        f.write(nl.join(out).encode("utf-8"))
    return "fixed"


def main():
    if len(sys.argv) != 2:
        print("用法：_w1309_fix_legacy_dates.py <清单文件>")
        return 2
    with open(sys.argv[1], encoding="utf-8") as fh:
        rels = [ln.strip() for ln in fh
                if ln.strip() and not ln.lstrip().startswith("#")]
    stat = {"fixed": 0, "clean": 0, "missing": 0}
    odd = []
    for rel in rels:
        try:
            r = fix_one(rel.replace("\\", "/"))
        except Exception as exc:
            r = "error:" + type(exc).__name__
        if r.startswith(("nonutf8", "error")):
            odd.append(rel + "（" + r + "）")
            continue
        stat[r] = stat.get(r, 0) + 1
    print("清单 %d 件：已订正 %d · 无伪日期 %d · 缺件 %d · 异常隔离 %d" % (
        len(rels), stat["fixed"], stat["clean"], stat["missing"], len(odd)))
    for o in odd[:20]:
        print("  ODD  " + o)
    return 0


if __name__ == "__main__":
    sys.exit(main())
