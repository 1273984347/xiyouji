# -*- coding: utf-8 -*-
"""_w953_prep_raws.py — prepare 脚本的出图轮次目录表加 round8（W953）

轮次优先级：靠前者优先（重出张落在后一轮）⇒ round8 是 W953 的最新一轮。
"""
import io
import os
import sys

P = os.path.join(r"D:\xiyouji", "scripts", "_w945_prepare.py")
OLD = 'RAW_DIRS = [os.path.join(SET_DIR, "raw", "round7"),'
NEW = 'RAW_DIRS = [os.path.join(SET_DIR, "raw", "round8"),\n            os.path.join(SET_DIR, "raw", "round7"),'


def main():
    raw = io.open(P, "rb").read()
    nl = "\r\n" if b"\r\n" in raw else "\n"
    t = raw.decode("utf-8").replace("\r\n", "\n")
    if OLD not in t:
        print("已含 round8（幂等跳过）")
        return 0
    t = t.replace(OLD, NEW, 1)
    io.open(P, "w", encoding="utf-8", newline="").write(t.replace("\n", nl))
    print("prepare 轮次目录表已加 round8（W953 优先）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
