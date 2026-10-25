# -*- coding: utf-8 -*-
"""_w952_fix_c6c.py — 修 CHANGELOG 段里的不存在路径（CRLF 归一后替换）+ 重新级联

① `_w952_fix_c6b.py` 上次因未做 CRLF 归一而未命中 ⇒ 本脚本读入后先归一为 \n 再替换
② 替换后从 HEAD 恢复 CHANGELOG.md（丢弃旧段）⇒ 重跑 cascade（写工作树 + 精确暂存）
"""
import io
import os
import subprocess
import sys

REPO = r"D:\xiyouji"
FIX = os.path.join(REPO, "scripts", "_w952_fix_c6.py")
CASCADE = os.path.join(REPO, "scripts", "_w952_cascade.py")


def read_norm(p):
    raw = io.open(p, "rb").read()
    nl = "\r\n" if b"\r\n" in raw else "\n"
    return raw.decode("utf-8").replace("\r\n", "\n"), nl


def write_keep(p, t, nl):
    io.open(p, "w", encoding="utf-8", newline="").write(t.replace("\n", nl))


def main():
    t, nl = read_norm(FIX)
    old = '"scripts/_w952_cascade.py、scripts/_w952_check_crop_helper.py、"\n    "scripts/_w952_fix_j10.py、'
    new = '"scripts/_w952_cascade.py、scripts/_w952_fix_c6.py、"\n    "scripts/_w952_fix_j10.py、'
    if old in t:
        t = t.replace(old, new, 1)
        write_keep(FIX, t, nl)
        print("已修 _w952_fix_c6.py 的 NEW_FILES（去不存在的 _w952_check_crop_helper.py）")
    else:
        print("WARN _w952_fix_c6.py 未命中（可能已修）")

    # 确认 cascade 常量里也不含该路径
    t2, nl2 = read_norm(CASCADE)
    if "_w952_check_crop_helper" in t2:
        t2 = t2.replace("scripts/_w952_check_crop_helper.py、", "scripts/_w952_fix_c6.py、", 1)
        write_keep(CASCADE, t2, nl2)
        print("已直接修 cascade 常量")
    else:
        print("cascade 常量已不含该路径")

    # 从 HEAD 恢复 CHANGELOG.md ⇒ 重跑级联
    p = subprocess.run(["git", "checkout", "HEAD", "--", "CHANGELOG.md"], cwd=REPO,
                       capture_output=True, text=True)
    if p.returncode != 0:
        print("FATAL checkout 失败: " + p.stderr[:200])
        return 2
    r = subprocess.run([sys.executable, os.path.join(REPO, "scripts", "_w952_cascade.py")],
                       cwd=REPO, capture_output=True, text=True, encoding="utf-8")
    print(r.stdout.strip()[-600:] or r.stderr.strip()[-600:])
    return 0


if __name__ == "__main__":
    sys.exit(main())
