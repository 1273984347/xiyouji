# -*- coding: utf-8 -*-
"""_w1005_fix_head_sentence.py — 修 HANDOVER 的「当前 HEAD = W###」句（治理契约判据 C4）

判据（`check_governance_docs.py`）：`当前 HEAD = (?:vX.Y.Z )?W###` 必须 ≡ CHANGELOG 最新段。
现状：该句仍写 W1003，而 CHANGELOG 顶段已是 W1004 ⇒ 门禁红「交接文档 HEAD W1003 与
CHANGELOG 最新段 W1004 不一致」（治理契约 + 文档口径体检共 2 项）⇒ 属并行 W1004 批的欠账。

本脚本把该句的批次号对齐到 CHANGELOG 现役段号（自动取·不写死）。
用法：py -3 scripts/_w1005_fix_head_sentence.py [--dry-run]
"""
import io
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HAND = os.path.join(REPO, "HANDOVER.md")
CH = os.path.join(REPO, "CHANGELOG.md")


def read(p):
    raw = io.open(p, "rb").read()
    return raw.decode("utf-8"), ("\r\n" if b"\r\n" in raw else "\n")


def write(p, text, nl):
    tmp = p + ".tmp"
    io.open(tmp, "wb").write(text.encode("utf-8"))
    os.replace(tmp, p)


def main() -> int:
    dry = "--dry-run" in sys.argv
    ch, _ = read(CH)
    m = re.search(r"^### W(\d{3,4})", ch, re.M)
    cur = m.group(1) if m else None
    print("CHANGELOG 现役段 =", cur)
    if not cur:
        return 1

    t, n = read(HAND)
    hits = list(re.finditer(r"当前 HEAD = (?:v[\d.]+\s+)?W(\d+)", t))
    if not hits:
        print("FAIL  未找到「当前 HEAD = W…」句")
        return 1
    for h in hits:
        print("   现状 @%d: %s" % (h.start(), t[h.start():h.start() + 90].replace("\n", " ")))
    t2 = re.sub(r"当前 HEAD = (?:v[\d.]+\s+)?W\d+", "当前 HEAD = W%s" % cur, t)
    if t2 == t:
        print("SKIP  已是 W%s" % cur)
        return 0
    if dry:
        print("DRY  HEAD 句 → W%s" % cur)
    else:
        write(HAND, t2, n)
        print("OK   HANDOVER「当前 HEAD」句 → W%s" % cur)
    m2 = re.search(r"当前 HEAD = (?:v[\d.]+\s+)?W(\d+)", t2)
    print("复核 HEAD =", m2.group(1) if m2 else "未解析")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
