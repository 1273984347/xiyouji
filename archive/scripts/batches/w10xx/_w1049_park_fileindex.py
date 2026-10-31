# -*- coding: utf-8 -*-
"""_w1049_park_fileindex.py — 停泊 file-index 的 W1050 段（与 CHANGELOG/台账 同法）

背景：W1050 批的级联把 `## W1050 …` 段写进了 `scripts/output/file-index.md`
⇒ 工作树含 W1050 段而我的提交不含 ⇒ 第 31 门禁 C4-f 报「工作树未提交残留」。
处置：把该段备份到 tmpe/_w1050_park/ 后从工作树剔除（内容零丢失·W1050 批重放时取回）。

用法：py -3 archive/scripts/batches/w10xx/_w1049_park_fileindex.py [--restore]
"""
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
PARK = os.path.join(REPO, "tmpe", "_w1050_park")
TARGET = "scripts/output/file-index.md"


def read(p):
    raw = io.open(p, "rb").read()
    return raw.decode("utf-8"), ("\r\n" if b"\r\n" in raw else "\n")


def write(p, text, nl):
    data = text.replace("\n", nl).encode("utf-8")
    tmp = p + ".tmp"
    with io.open(tmp, "wb") as fh:
        fh.write(data)
    os.replace(tmp, p)


def strip_w1050(text):
    lines = text.split("\n")
    out, skipping, level0 = [], False, None
    for ln in lines:
        m = re.match(r"^(#{2,3})\s+W(\d{3,4})", ln)
        if m:
            lvl = len(m.group(1))
            if m.group(2) == "1050":
                skipping, level0 = True, lvl
                continue
            if skipping and lvl <= level0:
                skipping = False
                out.append(ln)
                continue
        if skipping:
            continue
        out.append(ln)
    return "\n".join(out)


def main() -> int:
    p = os.path.join(REPO, TARGET.replace("/", os.sep))
    if "--restore" in sys.argv:
        src = os.path.join(PARK, "file-index.w1050-section.md")
        if not os.path.exists(src):
            print("SKIP  无备份")
            return 0
        park = io.open(src, encoding="utf-8").read()
        text, nl = read(p)
        m = re.search(r"(?m)^## W1049\b", text)
        assert m, "还原锚点未找到（W1049 段）"
        text = text[:m.start()] + park.rstrip("\n") + "\n\n" + text[m.start():]
        write(p, text, nl)
        print("OK    已还原 file-index 的 W1050 段（%d 字符）" % len(park))
        return 0

    os.makedirs(PARK, exist_ok=True)
    text, nl = read(p)
    m = re.search(r"(?m)^## W1050\b.*?(?=^## )", text, re.S | re.M)
    if not m:
        print("SKIP  工作树 file-index 无 W1050 段")
        return 0
    sec = m.group(0)
    io.open(os.path.join(PARK, "file-index.w1050-section.md"), "w", encoding="utf-8",
            newline="\n").write(sec)
    print("备份 W1050 段 %d 字符 → tmpe/_w1050_park/" % len(sec))
    write(p, strip_w1050(text), nl)
    print("已从工作树剔除")
    t2, _ = read(p)
    print("复核：工作树含 W1050 段 = %s" % ("## W1050" in t2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
