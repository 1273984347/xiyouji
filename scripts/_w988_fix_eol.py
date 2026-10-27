#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_w988_fix_eol.py — W988 修复 W988 批写盘污染的行尾（CRCRLF → CRLF）

背景：`_w988_insert.py` 早期版本写盘时做了 `text.replace("\\n", "\\r\\n")`，
而读入的 text 本身已是 CRLF（工作区行尾·git core.autocrlf=true ⇒ 仓库存 LF）
⇒ 每个换行被写成 CRCRLF，污染全部 102 个改动页面。

本脚本**只做字节级** CRCRLF → CRLF 还原，不改任何其它字节；幂等。
用法：py -3 scripts/_w988_fix_eol.py [--dry-run]
"""
from __future__ import annotations

import glob
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main() -> int:
    dry = "--dry-run" in sys.argv
    fixed = 0
    scanned = 0
    for f in sorted(glob.glob(os.path.join(ROOT, "site", "**", "*.html"), recursive=True)):
        raw = open(f, "rb").read()
        scanned += 1
        if b"\r\r\n" not in raw:
            continue
        n = raw.count(b"\r\r\n")
        new = raw.replace(b"\r\r\n", b"\r\n")
        # 同一页被改两次 ⇒ 会出现 CRCRCRLF（3 个 CR）⇒ 循环替换直到干净
        rounds = 1
        while b"\r\r\n" in new:
            new = new.replace(b"\r\r\n", b"\r\n")
            rounds += 1
            if rounds > 10:
                raise SystemExit("行尾修复未收敛: " + rel)
        rel = os.path.relpath(f, ROOT).replace("\\", "/")
        if not dry:
            tmp = f + ".tmp"
            with open(tmp, "wb") as fh:
                fh.write(new)
            os.replace(tmp, f)
        print("FIX   %-60s CRCRLF %d 处" % (rel, n))
        fixed += 1
    print("\n扫描 %d 页 · 修复 %d 页" % (scanned, fixed))
    return 0


if __name__ == "__main__":
    sys.exit(main())
