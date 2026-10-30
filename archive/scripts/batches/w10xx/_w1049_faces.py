# -*- coding: utf-8 -*-
"""_w1049_faces.py — 收官当前态面（README/STRUCTURE/项目说明/CITATION/workflows/页脚）

背景：`backfill_changelog.py --refresh-current` 能正确刷新三面（README/STRUCTURE/项目说明），
但 HANDOVER 面因本批**已手工改过**「一、当前进度」标题 ⇒ 级联的锚点正则失配 ⇒ 中止。
⇒ 本脚本用**定点替换**完成剩余当前态面（与级联产物形态一致·但走可复验的定点替换）。

本批描述（desc）取自 spec 的 title/desc，与 CHANGELOG W1049 段一致。

用法：py -3 archive/scripts/batches/w10xx/_w1049_faces.py [--dry-run]
"""
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
SPEC = os.path.join(REPO, "scripts", "output", "_w1049_spec.json")

W = "W1049"
DATE = "2026-10-31"
DESC = "回次 og:image 全覆盖批·第五轮（12 张线描立像/场面·编号 97–108）"
DESC_SHORT = "回次 og:image 全覆盖第五轮 12 张"


def read(p):
    raw = io.open(p, "rb").read()
    return raw.decode("utf-8"), ("\r\n" if b"\r\n" in raw else "\n")


def write(p, text, nl):
    data = text.replace("\n", nl).encode("utf-8")
    tmp = p + ".tmp"
    with io.open(tmp, "wb") as fh:
        fh.write(data)
    os.replace(tmp, p)


def sub(text, old, new, label):
    if old not in text:
        print("  SKIP  %s（锚点未命中：%s）" % (label, old[:50]))
        return text, False
    print("  OK    %s" % label)
    return text.replace(old, new), True


def main() -> int:
    dry = "--dry-run" in sys.argv
    spec = json.load(io.open(SPEC, encoding="utf-8"))
    assert spec["batch"] == "W1049", "spec 批次号不符"

    jobs = [
        # (相对路径, [(old, new, label), ...])
        ("CITATION.cff", [
            ('version: "W1048"', 'version: "%s"' % W, "CITATION version → %s" % W),
        ]),
        (".github/workflows/README.md", [
            ("W450-W1048", "W450-%s" % W, "workflows 里程碑区间上限 → %s" % W),
        ]),
    ]

    changed = []
    for rel, subs in jobs:
        p = os.path.join(REPO, rel.replace("/", os.sep))
        if not os.path.exists(p):
            print("SKIP  %s 不存在" % rel)
            continue
        text, nl = read(p)
        print("== %s ==" % rel)
        for old, new, label in subs:
            text, hit = sub(text, old, new, label)
            if hit:
                changed.append(p)
        if dry:
            continue
        write(p, text, nl)

    if dry:
        print("DRY 未落盘")
        return 0
    print("---- 当前态面更新完成（%d 文件）----" % len(set(changed)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
