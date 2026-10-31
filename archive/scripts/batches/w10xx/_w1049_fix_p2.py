# -*- coding: utf-8 -*-
"""_w1049_fix_p2.py — 修 P2-1（og 体积区间声明与实测不符）+ P2-2（cache 移出本批 spec）

P2-1：CHANGELOG 段与 spec 写「35–187KB」，实测为 **39.6–141.9KB**（40566–145292 B）
      ⇒ 声明≠落地·违反写作可验证纪律（文档规范 §4.9）⇒ 改为实测区间。
P2-2：`scripts/output/_vermilion_solid_cache.json` 是门禁缓存产物（sha1+时间戳）
      ⇒ 不应列入本批 spec 的「文件」行 ⇒ 从 spec 剔除（文件本身保留在仓内）。

用法：py -3 archive/scripts/batches/w10xx/_w1049_fix_p2.py
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
CHANGELOG = os.path.join(REPO, "CHANGELOG.md")
CACHE = "scripts/output/_vermilion_solid_cache.json"

OLD_TEXT = "12 个 og 版 1200×630 且 35–187KB（全部 ≤300KB）"
NEW_TEXT = "12 个 og 版 1200×630 且 39.6–141.9KB（实测 40566–145292 B·全部 ≤300KB）"
OLD_TEXT2 = "12 个 og 版 1200×630 且 35–187KB"
NEW_TEXT2 = "12 个 og 版 1200×630 且 39.6–141.9KB（实测 40566–145292 B）"


def read(p):
    raw = io.open(p, "rb").read()
    return raw.decode("utf-8"), ("\r\n" if b"\r\n" in raw else "\n")


def write(p, text, nl):
    data = text.replace("\n", nl).encode("utf-8")
    tmp = p + ".tmp"
    with io.open(tmp, "wb") as fh:
        fh.write(data)
    os.replace(tmp, p)


def main() -> int:
    # ---------- ① spec ----------
    spec = json.load(io.open(SPEC, encoding="utf-8"))
    body = spec["changelog_body"]
    n = 0
    if OLD_TEXT in body:
        body = body.replace(OLD_TEXT, NEW_TEXT)
        n += 1
    if OLD_TEXT2 in body:
        body = body.replace(OLD_TEXT2, NEW_TEXT2)
        n += 1
    spec["changelog_body"] = body
    rows = spec["file_index_rows"]
    before = len(rows)
    spec["file_index_rows"] = [r for r in rows if CACHE not in r]
    print("spec：changelog_body 体积声明修正 %d 处 · 文件行 %d → %d（剔除 cache）"
          % (n, before, len(spec["file_index_rows"])))
    tmp = SPEC + ".tmp"
    with io.open(tmp, "wb") as fh:
        fh.write(json.dumps(spec, ensure_ascii=False, indent=1).encode("utf-8"))
    os.replace(tmp, SPEC)

    # ---------- ② CHANGELOG 段 ----------
    text, nl = read(CHANGELOG)
    c = 0
    if OLD_TEXT in text:
        text = text.replace(OLD_TEXT, NEW_TEXT)
        c += 1
    if OLD_TEXT2 in text:
        text = text.replace(OLD_TEXT2, NEW_TEXT2)
        c += 1
    write(CHANGELOG, text, nl)
    print("CHANGELOG：体积声明修正 %d 处" % c)

    # ---------- ③ make_spec 脚本同步（保证重生成时不再写回旧值）----------
    mk = os.path.join(HERE, "_w1049_make_spec.py")
    t = io.open(mk, encoding="utf-8").read()
    if OLD_TEXT in t or OLD_TEXT2 in t:
        t = t.replace(OLD_TEXT, NEW_TEXT).replace(OLD_TEXT2, NEW_TEXT2)
        tmp = mk + ".tmp"
        with io.open(tmp, "wb") as fh:
            fh.write(t.encode("utf-8"))
        os.replace(tmp, mk)
        print("make_spec.py：体积声明同步修正")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
