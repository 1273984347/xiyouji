# -*- coding: utf-8 -*-
"""_w999_fix_wnum.py — W999 段号订正 + 插入本批 W999 段

发现（台账即事实源）：并行会话的「必守纪律晋升批」在 CHANGELOG / file-index 里写成
`### W999`，但它自己的**台账行是 W998**（`docs/00-导读/W批次编号对账表.md`）⇒ 段号与台账行错位 1。
仓内铁则是「CHANGELOG 现役段 W 号须有对账表表格行」（第 31 门禁 C4 认领行强制），
段号必须与台账行一致 ⇒ 本脚本只做**段号订正**（内容一字未改），再插入本批自己的 W999 段。

处置：
  ① 它的 `### W999` → `### W998`（CHANGELOG + file-index 两处）· 状态行补注订正原因
  ② 插入本批 `### W999`（回次 og:image 全覆盖批·第一轮试点）

用法：py -3 scripts/_w999_fix_wnum.py [--dry-run]
"""
from __future__ import annotations

import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _w999_closeout import BODY  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "scripts", "output")
CH = os.path.join(REPO, "CHANGELOG.md")
FI = os.path.join(OUT, "file-index.md")

OLD_HDR = "### W999（2026-10-28）：必守纪律晋升批"
NEW_HDR = "### W998（2026-10-28）：必守纪律晋升批"
MY_HDR = "### W999（2026-10-28）：回次 og:image 全覆盖批·第一轮试点（12 张线描立像/场面）"


def read(p):
    raw = io.open(p, "rb").read()
    return raw.decode("utf-8"), ("\r\n" if b"\r\n" in raw else "\n")


def write(p, text, nl):
    tmp = p + ".tmp"
    io.open(tmp, "wb").write(text.encode("utf-8"))
    os.replace(tmp, p)


def main() -> int:
    dry = "--dry-run" in os.sys.argv

    # ---------- ① CHANGELOG ----------
    t, n = read(CH)
    if OLD_HDR in t:
        t = t.replace(OLD_HDR, NEW_HDR, 1)
        # 状态行补注（不改原措辞主体，只加订正说明）
        t = re.sub(r"(> - \*\*状态\*\*：\*\*已收官\*\*（W999 git 反填·纪律晋升三层落地)",
                   r"\1·**段号订正 W999→W998**：本批台账行为 W998（台账即事实源·段号须与台账行一致）",
                   t, count=1)
        if dry:
            print("DRY  CHANGELOG：它的 W999 段 → W998")
        else:
            write(CH, t, n)
            print("OK   CHANGELOG：它的 W999 段已订正为 W998（内容未改）")
    elif NEW_HDR in t:
        print("SKIP  CHANGELOG 它的段已是 W998")
    else:
        print("WARN  CHANGELOG 未找到它的 W999 段（可能已被它自行订正）")

    # ---------- ② 插入本批 W999 段 ----------
    t, n = read(CH)
    if MY_HDR in t:
        print("SKIP  CHANGELOG 本批 W999 段已在")
    else:
        seg = MY_HDR + BODY + "\n"
        heads = [(int(m.group(1)), m.start()) for m in re.finditer(r"^### W(\d{3,4}) ", t, re.M)]
        pos = None
        for w, s in heads:
            if w < 999:
                pos = s
                break
        if pos is None:
            pos = 0
        t = t[:pos] + seg + t[pos:]
        if dry:
            print("DRY  CHANGELOG 将插入本批 W999 段")
        else:
            write(CH, t, n)
            print("OK   CHANGELOG 本批 W999 段已插入")

    # ---------- ③ file-index ----------
    t, n = read(FI)
    t2 = t.replace("## W999 必守纪律晋升批", "## W998 必守纪律晋升批", 1)
    if t2 != t:
        if dry:
            print("DRY  file-index：它的 W999 段 → W998")
        else:
            write(FI, t2, n)
            print("OK   file-index：它的 W999 段已订正为 W998")
    else:
        print("SKIP  file-index 它的段已是 W998 或形态不同")

    # ---------- ④ 复核 ----------
    t, _ = read(CH)
    print("CHANGELOG 现役段序：", re.findall(r"^### W(\d{3,4}) ", t, re.M)[:6])
    t, _ = read(FI)
    print("file-index 段序：", re.findall(r"^## W(\d{3,4}) ", t, re.M)[:6])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
