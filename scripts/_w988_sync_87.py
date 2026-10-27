# -*- coding: utf-8 -*-
"""_w988_sync_87.py — W988 坑表条数口径同步（80 → 86 → 87）

E-17 补入后，坑表由 86 条变 87 条 ⇒ 需同步：
  ① `scripts/_w988_make_spec.py` 的 changelog_body / file_index_rows 措辞
  ② T34 终稿报告的 §0 / §6 / §7 / §8 措辞
用法：py -3 scripts/_w988_sync_87.py [--dry-run]
"""
import io
import os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PAIRS = [
    ("坑表 +5 条 + 方法论篇 §2.9", "坑表 +7 条（80 → 87）+ 方法论篇 §2.9"),
    ("坑表 +6 条（80 → 86）", "坑表 +7 条（80 → 87）"),
    ("坑表 +6 条（80 → 86：", "坑表 +7 条（80 → 87："),
    ("+6 条（80 → 86：", "+7 条（80 → 87："),
    ("（80 → 86：", "（80 → 87："),
    ("坑表 +6 条", "坑表 +7 条"),
    ("（80 → 86）", "（80 → 87）"),
    ("80 → 86 条", "80 → 87 条"),
    ("86 条（CSS", "87 条（CSS"),
    ("坑位条数声明 80 → 86", "坑位条数声明 80 → 87"),
    ("坑位条数指针 80 → 86", "坑位条数指针 80 → 87"),
    ("坑表 80 → 86", "坑表 80 → 87"),
    ("（80 → 86）", "（80 → 87）"),
]

FILES = [
    "scripts/_w988_make_spec.py",
    "docs/11-方案报告/计划方案/T34-任务计划执行与经验沉淀报告-2026-10-27.md",
]


def read(p):
    raw = io.open(p, "rb").read()
    return raw.decode("utf-8"), ("\r\n" if b"\r\n" in raw else "\n")


def write(p, text, nl):
    tmp = p + ".tmp"
    io.open(tmp, "wb").write(text.replace("\r\n", "\n").replace("\n", nl).encode("utf-8"))
    os.replace(tmp, p)


def main() -> int:
    dry = "--dry-run" in os.sys.argv
    for rel in FILES:
        p = os.path.join(REPO, rel.replace("/", os.sep))
        t, n = read(p)
        orig = t
        hits = 0
        for old, new in PAIRS:
            c = t.count(old)
            if c:
                t = t.replace(old, new)
                hits += c
        if t == orig:
            print("SKIP  %s 无待同步措辞" % rel)
            continue
        if dry:
            print("DRY  %s：%d 处措辞待同步" % (rel, hits))
        else:
            write(p, t, n)
            print("OK   %s：%d 处措辞已同步" % (rel, hits))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
