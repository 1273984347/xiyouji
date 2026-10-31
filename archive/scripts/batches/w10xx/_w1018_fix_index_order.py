# -*- coding: utf-8 -*-
"""_w1018_fix_index_order.py — 三处收口修根因

① **file-index 段序必须严格递减**（第 17 门禁：最新在前）⇒ W1015 段须落在 **W1016 段之后**；
   而 **CHANGELOG 只要求「现役段 = 最新号」**（治理契约门禁查的是编号规则/最后更新链与现役段一致，
   不查段序严格递减）⇒ 两面口径不同 ⇒ CHANGELOG 的 W1015 段**留在 W1018 之后**（保证现役=最新），
   file-index 的 W1015 段**移到 W1016 之后**（保证严格递减）。

② **段「文件」行与 spec 必须用改名后的路径**（`scripts/_w1016_*` → `scripts/_w1018_*`）：
   改名后的文件在本批入库前不在提交树内 ⇒ C4-f 会判「文件清单未入提交树」、第 51 门禁会判
   「索引含 spec 之外的文件」⇒ 段与 spec 统一改为新名。

用法：py -3 scripts/_w1018_fix_index_order.py [--dry-run]
"""
from __future__ import annotations

import io
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(REPO, "CHANGELOG.md")
FI = os.path.join(REPO, "scripts", "output", "file-index.md")
SPEC = os.path.join(REPO, "scripts", "output", "_w1018_spec.json")


def read(p):
    raw = io.open(p, "rb").read()
    return raw.decode("utf-8"), ("\r\n" if b"\r\n" in raw else "\n")


def write(p, text):
    tmp = p + ".tmp"
    io.open(tmp, "wb").write(text.encode("utf-8"))
    os.replace(tmp, p)


def move_block_after(path, block_prefix, anchor_prefix, dry, label):
    """把以 block_prefix 开头的那一段整块，移到以 anchor_prefix 开头的段之后（行级操作）。"""
    text, nl = read(path)
    lines = text.split("\n")

    def rng(pfx):
        s = None
        for i, l in enumerate(lines):
            if l.startswith(pfx):
                s = i
                break
        if s is None:
            return None, None
        e = len(lines)
        for j in range(s + 1, len(lines)):
            if lines[j].startswith(pfx[:3]) and lines[j][3:4].isupper():
                e = j
                break
            if lines[j].startswith(pfx[:3]):
                e = j
                break
        return s, e

    sb, eb = rng(block_prefix)
    sa, ea = rng(anchor_prefix)
    if sb is None or sa is None:
        print("SKIP  %s 未定位 %s / %s" % (os.path.basename(path), block_prefix, anchor_prefix))
        return
    if sb > sa:
        print("SKIP  %s %s 已在 %s 之后" % (os.path.basename(path), label, anchor_prefix))
        return
    seg = lines[sb:eb]
    rest = lines[:sb] + lines[eb:]
    off = sa - (eb - sb)
    out = rest[:off + (ea - sa)] + seg + rest[off + (ea - sa):]
    if dry:
        print("DRY  %s %s 段移到 %s 段之后" % (os.path.basename(path), label, anchor_prefix))
    else:
        write(path, "\n".join(out))
        print("OK   %s %s 段移到 %s 段之后" % (os.path.basename(path), label, anchor_prefix))


def main() -> int:
    dry = "--dry-run" in sys.argv

    # ① file-index：W1015 段移到 W1016 段之后（严格递减）
    move_block_after(FI, "## W1015", "## W1016", dry, "W1015")
    # CHANGELOG：保持 W1015 在 W1018 之后（现役段 = 最新·治理契约口径）

    # ② 段「文件」行 + spec 统一改新名
    for path in (CH, FI, SPEC):
        text, nl = read(path)
        n = text.count("_w1016_")
        if n == 0:
            print("SKIP  %s 无旧名" % os.path.relpath(path, REPO).replace("\\", "/"))
            continue
        text2 = text.replace("_w1016_", "_w1018_")
        assert text2.count("\n") == text.count("\n"), "%s 行数变化" % path
        if dry:
            print("DRY  %s 替换 %d 处旧名" % (os.path.relpath(path, REPO).replace("\\", "/"), n))
        else:
            write(path, text2)
            print("OK   %s 替换 %d 处旧名" % (os.path.relpath(path, REPO).replace("\\", "/"), n))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
