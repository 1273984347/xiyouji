# -*- coding: utf-8 -*-
"""_w1049_stage_ledger.py — 精确暂存台账（HEAD 版 + 仅替换我方 W1049 行）

纪律（承 W1047 先例）：台账属共享面 ⇒ 不得整文件 `git add`（会把他方在途行代提交）。
做法：以 HEAD 版台账为基底，仅把工作树里**我方 W1049 行**替换进去 ⇒ 其余行（含 W1050 行）保持 HEAD 原样。

用法：py -3 archive/scripts/batches/w10xx/_w1049_stage_ledger.py
"""
import io
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
LED = "docs/00-导读/W批次编号对账表.md"
BATCH = "W1049"


def git(*a, **kw):
    return subprocess.run(["git", "-c", "core.quotepath=false", "-C", REPO] + list(a),
                          capture_output=True, **kw)


def main() -> int:
    head = git("show", "HEAD:" + LED, check=True).stdout.decode("utf-8")
    work = io.open(os.path.join(REPO, LED.replace("/", os.sep)), encoding="utf-8",
                   newline="").read()
    hlines = head.split("\n")
    wlines = work.split("\n")

    def pick(lines):
        return next((l for l in lines if l.startswith("| %s " % BATCH)), None)

    wl, hl = pick(wlines), pick(hlines)
    if wl is None:
        print("FAIL  工作树缺 %s 行" % BATCH)
        return 1
    if hl is None:
        print("NOTE  HEAD 无 %s 行（本批新增行）" % BATCH)

    # 基底选择：**工作树**（已剔除 W1050 行 + 含我方 W1049 行）
    #   —— 用 HEAD 作基底会残留 HEAD 的末尾空行差异（实测多 1 行）。
    # 台账是共享面 ⇒ 本批只允许「工作树 - 他方在途行」进入提交；
    # W1050 行已由 `_w1049_park_w1050.py` 从工作树剔除 ⇒ 工作树即本批提交内容。
    new_lines = list(wlines)

    # 自证：工作树与 HEAD 的差异行必须全部是我方行（他方在途行不得代提）
    others = [l for l in wlines if l not in hlines and not l.startswith("| %s " % BATCH)
              and l.strip()]
    if others:
        print("FAIL  工作树含我方行之外的差异 %d 行（拒绝暂存·零代提）" % len(others))
        for l in others[:3]:
            print("      %s" % l[:100])
        return 1
    print("OK    自证：工作树与 HEAD 的唯一差异是我方 %s 行（他方在途行零代提）" % BATCH)

    new_text = "\n".join(new_lines)
    blob = git("hash-object", "-w", "--stdin", input=new_text.encode("utf-8"),
               check=True).stdout.decode().strip()
    git("update-index", "--cacheinfo", "100644,%s,%s" % (blob, LED), check=True)
    print("OK    台账已精确暂存（blob=%s·零代提）" % blob[:10])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
