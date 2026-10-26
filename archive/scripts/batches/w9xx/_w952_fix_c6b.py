# -*- coding: utf-8 -*-
"""_w952_fix_c6b.py — 修 _w952_fix_c6.py 里 NEW_FILES 的错误路径项（_w952_check_crop_helper.py 不存在）"""
import io
import os

P = os.path.join(r"D:\xiyouji", "scripts", "_w952_fix_c6.py")
raw = io.open(P, "rb").read()
nl = "\r\n" if b"\r\n" in raw else "\n"
t = raw.decode("utf-8").replace("\r\n", "\n")

old = ('"scripts/_w952_cascade.py、scripts/_w952_check_crop_helper.py、"\n'
       '    "scripts/_w952_fix_j10.py、scripts/_w952_make_edge_sample.py、scripts/_w952_update_readme.py、"')
new = ('"scripts/_w952_cascade.py、scripts/_w952_fix_c6.py、"\n'
       '    "scripts/_w952_fix_j10.py、scripts/_w952_make_edge_sample.py、scripts/_w952_update_readme.py、"')
if old not in t:
    print("未命中（可能已修）")
else:
    t = t.replace(old, new, 1)
    io.open(P, "w", encoding="utf-8", newline="").write(t.replace("\n", nl))
    print("已修：_w952_check_crop_helper.py → _w952_fix_c6.py")
