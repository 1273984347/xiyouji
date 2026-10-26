# -*- coding: utf-8 -*-
"""_w945_probe_handover.py — 定位 HANDOVER 幂等失败的行（逐行 diff 两次快照）"""
import difflib
import io
import os
import re
import subprocess
import sys

REPO = r"D:\xiyouji"
H = os.path.join(REPO, "HANDOVER.md")


def snap():
    return io.open(H, encoding="utf-8").read().split("\n")


a = snap()
subprocess.run([sys.executable, os.path.join(REPO, "scripts", "_w945_cascade.py")],
               cwd=REPO, capture_output=True)
b = snap()
diffs = [d for d in difflib.unified_diff(a, b, "before", "after", n=0, lineterm="")]
if not diffs:
    print("无差异（幂等成立）")
else:
    for d in diffs[:30]:
        print(d[:400])
