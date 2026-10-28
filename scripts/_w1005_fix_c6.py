# -*- coding: utf-8 -*-
"""_w1005_fix_c6.py — 修 C6：项目说明.md 两处版本行的 desc 含「·」

门禁 C6（`check_doc_sync.py`）：版本行 desc 不得含分隔符「·」——写入后会使**下一批**级联锚点正则失配
（W826 实证：三处全断·任何批都无法落段）。

现状：并行 W1004 批写的版本行 desc 里用了「·」分隔 ⇒ 1 项核心 FAIL（与本批资产面无关，
但会阻断后续所有批次的落段）⇒ 按「修实例必修根」替他修：把两处版本行（头部引用行 + 「当前版本」
列表行）里的「·」换成「、」（语义不变）。

用法：py -3 scripts/_w1005_fix_c6.py [--dry-run]
"""
import io
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(REPO, "docs", "00-导读", "项目说明.md")


def read(p):
    raw = io.open(p, "rb").read()
    return raw.decode("utf-8"), ("\r\n" if b"\r\n" in raw else "\n")


def write(p, text, nl):
    tmp = p + ".tmp"
    io.open(tmp, "wb").write(text.encode("utf-8"))
    os.replace(tmp, p)


def main() -> int:
    dry = "--dry-run" in sys.argv
    t, n = read(P)
    lines = t.split("\n")
    ch = 0
    for i, ln in enumerate(lines):
        if ("当前批次 W" in ln or "**当前版本**" in ln) and "·" in ln:
            new = ln.replace("·", "、")
            lines[i] = new
            ch += 1
            print("   %4d| %s" % (i + 1, new[:150]))
    if not ch:
        print("SKIP  未发现含「·」的版本行")
        return 0
    t = "\n".join(lines)
    if dry:
        print("DRY  将改 %d 行" % ch)
    else:
        write(P, t, n)
        print("OK   项目说明.md 版本行 desc「·」→「、」（%d 行）" % ch)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
