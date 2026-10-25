# -*- coding: utf-8 -*-
"""_w953_prep_raws2.py — prepare 轮次目录表加 round9（W953 重出 4 张·优先级最高）"""
import io
import os
import sys

P = os.path.join(r"D:\xiyouji", "scripts", "_w945_prepare.py")
OLD = 'RAW_DIRS = [os.path.join(SET_DIR, "raw", "round8"),'
NEW = 'RAW_DIRS = [os.path.join(SET_DIR, "raw", "round9"),\n            os.path.join(SET_DIR, "raw", "round8"),'


def main():
    raw = io.open(P, "rb").read()
    nl = "\r\n" if b"\r\n" in raw else "\n"
    t = raw.decode("utf-8").replace("\r\n", "\n")
    if OLD not in t:
        print("已含 round9（幂等跳过）")
        return 0
    t = t.replace(OLD, NEW, 1)
    io.open(P, "w", encoding="utf-8", newline="").write(t.replace("\n", nl))
    print("prepare 轮次目录表已加 round9")
    return 0


if __name__ == "__main__":
    sys.exit(main())
