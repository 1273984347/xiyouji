# -*- coding: utf-8 -*-
"""_w1018_fix_names_order.py — W1018 批两处修根因

① **脚本名前缀与批号脱节**：资产批号因并行批占位由 W1016 让为 **W1018**，但脚本仍沿用
   `_w1016_*.py` ⇒ 第 42 门禁 C4「历史批 `_w*.py` 滞留」判红 **10 件**（W1016 已被并行
   「教训固化批」占用 ⇒ `_w1016_*` 属他方号段）。
   ⇒ 修法：把 `scripts/_w1016_*.py` 改名为 `_w1018_*.py`，并改文件内自引用。

② **W1015 段插入位置错**：段内定向插入按「第一个 W 号 > 目标」定位 ⇒ W1015 段被放到 W1018 段
   **之前** ⇒ CHANGELOG「现役段」变成 W1015 ⇒ 14 个版本面（编号规则 / 最后更新链 / CITATION /
   workflows README / 里程碑行）全部与 W1018 不一致。
   ⇒ 修法：W1015 段必须落在**现役段 W1018 之后**（第 2 位），使现役段仍是最新号。

用法：py -3 scripts/_w1018_fix_names_order.py [--dry-run]
"""
from __future__ import annotations

import io
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(REPO, "scripts")
CH = os.path.join(REPO, "CHANGELOG.md")
FI = os.path.join(REPO, "scripts", "output", "file-index.md")


def read(p):
    raw = io.open(p, "rb").read()
    return raw.decode("utf-8"), ("\r\n" if b"\r\n" in raw else "\n")


def write(p, text):
    tmp = p + ".tmp"
    io.open(tmp, "wb").write(text.encode("utf-8"))
    os.replace(tmp, p)


def rename_scripts(dry):
    moved = []
    for fn in sorted(os.listdir(SCRIPTS)):
        if not (fn.startswith("_w1016_") and fn.endswith(".py")):
            continue
        new = fn.replace("_w1016_", "_w1018_")
        src = os.path.join(SCRIPTS, fn)
        dst = os.path.join(SCRIPTS, new)
        assert not os.path.exists(dst), "目标已存在：%s" % new
        text, nl = read(src)
        text2 = text.replace("_w1016_", "_w1018_").replace("_w1016", "_w1018")
        text2 = text2.replace("W1016 批", "W1018 批").replace("（W1016", "（W1018")
        if dry:
            print("DRY  %s → %s" % (fn, new))
        else:
            write(src, text2)
            os.rename(src, dst)
            print("OK   %s → %s" % (fn, new))
        moved.append(new)
    return moved


def move_w1015_after_w1018(path, dry, is_index=False):
    """行级重排：把 W1015 段（整段）从原位取出，插到 W1018 段末尾之后。

    用行级操作而非正则 lookahead（后者在段内含 `### W` 字样时易误截）。
    """
    text, nl = read(path)
    prefix = "## " if is_index else "### "
    lines = text.split("\n")

    def seg_range(prefix_w):
        start = None
        for i, l in enumerate(lines):
            if l.startswith(prefix + prefix_w):
                start = i
                break
        if start is None:
            return None, None
        end = len(lines)
        for j in range(start + 1, len(lines)):
            if lines[j].startswith(prefix + "W"):
                end = j
                break
        return start, end

    s15, e15 = seg_range("W1015")
    s18, e18 = seg_range("W1018")
    if s15 is None or s18 is None:
        print("SKIP  %s 未定位 W1015/W1018 段" % os.path.basename(path))
        return
    if s15 > s18:
        print("SKIP  %s W1015 段已在 W1018 之后" % os.path.basename(path))
        return
    seg15 = lines[s15:e15]
    rest = lines[:s15] + lines[e15:]
    # 移除后重新定位 W1018 段尾
    off = s18 - (e15 - s15)
    out = rest[:off + (e18 - s18)] + seg15 + rest[off + (e18 - s18):]
    if dry:
        print("DRY  %s W1015 段移到 W1018 段之后" % os.path.basename(path))
    else:
        write(path, "\n".join(out))
        print("OK   %s W1015 段移到 W1018 段之后" % os.path.basename(path))


def main() -> int:
    dry = "--dry-run" in sys.argv
    moved = rename_scripts(dry)
    print("改名 %d 个脚本（_w1016_* → _w1018_*）" % len(moved))
    move_w1015_after_w1018(CH, dry, is_index=False)
    move_w1015_after_w1018(FI, dry, is_index=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
