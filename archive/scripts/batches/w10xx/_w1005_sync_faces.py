# -*- coding: utf-8 -*-
"""_w1005_sync_faces.py — 补并行 W1004 批的版本面欠账（2 处）+ 定位 HANDOVER HEAD 行

现状：CHANGELOG 现役段已是 W1004，但两处版本面仍停在 W1003 ⇒ 门禁 4 处红
（索引健康 / 治理文档维护契约 ×2 / 文档口径体检）—— **与本批资产面无关**，
但仓带着红会影响后续所有批次 ⇒ 按「修实例必修根」替他结清。

修两处：
  ① CHANGELOG 编号规则行 `（W001-W1003）` → `（W001-W1004）`
  ② .github/workflows/README.md 第 3 行的批次号 `（D:\\xiyouji，W1003）` → W1004
用法：py -3 scripts/_w1005_sync_faces.py [--dry-run]
"""
import io
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(REPO, "CHANGELOG.md")
WF = os.path.join(REPO, ".github", "workflows", "README.md")
HAND = os.path.join(REPO, "HANDOVER.md")


def read(p):
    raw = io.open(p, "rb").read()
    return raw.decode("utf-8"), ("\r\n" if b"\r\n" in raw else "\n")


def write(p, text, nl):
    tmp = p + ".tmp"
    io.open(tmp, "wb").write(text.encode("utf-8"))
    os.replace(tmp, p)


def main() -> int:
    dry = "--dry-run" in sys.argv

    # ① CHANGELOG 编号规则
    t, n = read(CH)
    lines = t.split("\n")
    ch = 0
    for i, ln in enumerate(lines):
        if "编号规则" in ln:
            new = re.sub(r"[（(]W001-W\d{3,4}[)）]", "（W001-W1004）", ln)
            if new != ln:
                lines[i] = new
                ch += 1
    t = "\n".join(lines)
    if ch:
        if dry:
            print("DRY  CHANGELOG 编号规则 → W001-W1004")
        else:
            write(CH, t, n)
            print("OK   CHANGELOG 编号规则 → W001-W1004")

    # ② workflows README 头部批次号
    t, n = read(WF)
    lines = t.split("\n")
    ch2 = 0
    for i, ln in enumerate(lines):
        if i < 12 and "W1003" in ln and "W450-" in ln:
            lines[i] = ln.replace("W1003", "W1004")
            ch2 += 1
    t = "\n".join(lines)
    if ch2:
        if dry:
            print("DRY  workflows README 头部 → W1004")
        else:
            write(WF, t, n)
            print("OK   workflows README 头部 → W1004")

    # ③ HANDOVER 里带 HEAD 字样且批次号落后的行
    t, _ = read(HAND)
    for i, ln in enumerate(t.split("\n")):
        if "HEAD" in ln and re.search(r"W100[0-3]", ln):
            print("HANDOVER 疑似滞后行 %d| %s" % (i + 1, ln[:190]))

    t, _ = read(CH)
    print("复核 编号规则：", re.findall(r"[（(]W001-W\d{4}[)）]", t)[:3])
    t, _ = read(WF)
    print("复核 workflows 头部：", re.findall(r"W450-W\d{4}", t)[:2])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
