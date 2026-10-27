# -*- coding: utf-8 -*-
"""_w952_fix_backfill.py — 修 W952 回填脚本的批次参数 + 从 HEAD 恢复被误改的台账 W951 行

问题：`_w952_make_backfill.py` 只改了 `BATCH` 常量，漏改 `main()` 里硬编码的 `--w 951`
⇒ 首跑误把 **W951 行**回填成了 W952 的状态文本（污染历史行）。

处置：① 把 `--w 951` 改为 `--w 952` ② 从 HEAD 恢复台账（HEAD 里 W951 行是正确的收官状态）
     ③ 重跑 W952 回填（精确暂存随之覆盖）。
"""
import io
import os
import subprocess
import sys

REPO = r"D:\xiyouji"
P = os.path.join(REPO, "scripts", "_w952_backfill_stage.py")


def read_norm(p):
    raw = io.open(p, "rb").read()
    nl = "\r\n" if b"\r\n" in raw else "\n"
    return raw.decode("utf-8").replace("\r\n", "\n"), nl


def main():
    t, nl = read_norm(P)
    n = 0
    for old, new in (('"--w", "951"', '"--w", "952"'),
                     ('"--w", "951",', '"--w", "952",'),
                     ('BATCH = "W951"', 'BATCH = "W952"')):
        if old in t:
            t = t.replace(old, new)
            n += 1
    io.open(P, "w", encoding="utf-8", newline="").write(t.replace("\n", nl))
    print("回填脚本参数已修 %d 处" % n)

    # 从 HEAD 恢复台账（丢弃被误改的 W951 行）
    p = subprocess.run(["git", "checkout", "HEAD", "--", "docs/00-导读/W批次编号对账表.md"],
                       cwd=REPO, capture_output=True, text=True)
    if p.returncode != 0:
        print("FATAL checkout 失败: " + p.stderr[:200])
        return 2
    print("台账已从 HEAD 恢复（W951 行回到正确状态）")

    r = subprocess.run([sys.executable, P], cwd=REPO, capture_output=True,
                       text=True, encoding="utf-8")
    print(r.stdout.strip()[-700:] or r.stderr.strip()[-700:])
    return r.returncode


if __name__ == "__main__":
    sys.exit(main())
