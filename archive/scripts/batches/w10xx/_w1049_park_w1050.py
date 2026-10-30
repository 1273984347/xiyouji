# -*- coding: utf-8 -*-
"""_w1049_park_w1050.py — 把 W1050 段/行「停泊」到 tmpe/（内容零丢失）

根因：用户令「W1050 六件在途件收官时摘出勿卷入」+ 第 31 门禁 C4-f/C2
**读工作树** ⇒ 只要工作树仍含 W1050 内容，门禁必红（与本批无关但挡住收官）。

处置：把 W1050 的**内容**（CHANGELOG 段 + 台账行）从工作树文本中**移出**，
     完整副本存入 `tmpe/_w1050_park/`（gitignore 区）⇒
       · 工作树 == 本批提交内容 ⇒ 门禁可绿
       · W1050 批重放时从 tmpe/_w1050_park/ 取回原样（零丢失）
       · 本批提交不含任何 W1050 内容

**不删任何内容**：全部先备份到 tmpe/ 再改工作树。
用法：py -3 archive/scripts/batches/w10xx/_w1049_park_w1050.py [--restore]
"""
import io
import os
import re
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
PARK = os.path.join(REPO, "tmpe", "_w1050_park")

CHANGELOG = "CHANGELOG.md"
LEDGER = "docs/00-导读/W批次编号对账表.md"


def park_path(name):
    return os.path.join(PARK, name)


def read(p):
    raw = io.open(p, "rb").read()
    return raw.decode("utf-8"), ("\r\n" if b"\r\n" in raw else "\n")


def write(p, text, nl):
    data = text.replace("\n", nl).encode("utf-8")
    tmp = p + ".tmp"
    with io.open(tmp, "wb") as fh:
        fh.write(data)
    os.replace(tmp, p)


def strip_changelog_w1050(text):
    """剔除 `### W1050` 整段（标题行 + 到下一个 `### ` 之前的全部内容）。"""
    lines = text.split("\n")
    out, skipping = [], False
    for ln in lines:
        if ln.startswith("### W1050"):
            skipping = True
            continue
        if skipping:
            if ln.startswith("### "):
                skipping = False
                out.append(ln)
            continue
        out.append(ln)
    return "\n".join(out)


def strip_ledger_w1050(text):
    """剔除台账的 `| W1050 |` 行。"""
    lines = text.split("\n")
    out = [ln for ln in lines if not ln.startswith("| W1050 ")]
    assert len(out) == len(lines) - 1, "台账 W1050 行数异常：%d → %d" % (len(lines), len(out))
    return "\n".join(out)


def restore():
    print("== 从 tmpe/_w1050_park/ 还原 ==")
    for name, target in (("CHANGELOG.w1050-section.md", CHANGELOG),
                         ("W批次编号对账表.w1050-row.md", LEDGER)):
        src = park_path(name)
        if not os.path.exists(src):
            print("  SKIP  %s 无备份" % name)
            continue
        park = io.open(src, encoding="utf-8").read()
        p = os.path.join(REPO, target.replace("/", os.sep))
        text, nl = read(p)
        if target == CHANGELOG:
            # 插回：W1050 段应排在 W1049 段之前（按号序降序）
            m = re.search(r"(?m)^### W1049", text)
            assert m, "还原锚点未找到（W1049 段）"
            text = text[:m.start()] + park.rstrip("\n") + "\n\n" + text[m.start():]
        else:
            lines = text.split("\n")
            m = max((i for i, l in enumerate(lines) if l.startswith("| W1049 ")), default=len(lines) - 1)
            lines.insert(m + 1, park.rstrip("\n"))
            text = "\n".join(lines)
        write(p, text, nl)
        print("  OK    已还原 %s（%d 字符）" % (target, len(park)))
    return 0


def main() -> int:
    if "--restore" in sys.argv:
        return restore()

    os.makedirs(PARK, exist_ok=True)
    print("== ① CHANGELOG：备份并剔除 W1050 段 ==")
    p = os.path.join(REPO, CHANGELOG)
    text, nl = read(p)
    m = re.search(r"(?m)^### W1050.*?(?=^### )", text, re.S | re.M)
    if m:
        sec = m.group(0)
        io.open(park_path("CHANGELOG.w1050-section.md"), "w", encoding="utf-8",
                newline="\n").write(sec)
        print("  备份 W1050 段 %d 字符 → tmpe/_w1050_park/" % len(sec))
        text = text[:m.start()] + text[m.end():]
        write(p, text, nl)
        print("  已从工作树剔除")
    else:
        print("  SKIP  工作树 CHANGELOG 无 W1050 段")

    print("\n== ② 台账：备份并剔除 W1050 行 ==")
    p = os.path.join(REPO, LEDGER.replace("/", os.sep))
    text, nl = read(p)
    row = next((l for l in text.split("\n") if l.startswith("| W1050 ")), None)
    if row:
        io.open(park_path("W批次编号对账表.w1050-row.md"), "w", encoding="utf-8",
                newline="\n").write(row)
        print("  备份 W1050 行 %d 字符 → tmpe/_w1050_park/" % len(row))
        text = strip_ledger_w1050(text)
        write(p, text, nl)
        print("  已从工作树剔除")
    else:
        print("  SKIP  工作树台账无 W1050 行")

    print("\n== 复核 ==")
    for f in (CHANGELOG, LEDGER):
        t = io.open(os.path.join(REPO, f.replace("/", os.sep)), encoding="utf-8").read()
        has = "W1050" in t
        print("  %-40s 工作树含 W1050 = %s" % (f, has))
    print("  备份目录：tmpe/_w1050_park/（gitignore 区·W1050 批重放时取回）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
