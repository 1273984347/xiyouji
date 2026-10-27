# -*- coding: utf-8 -*-
"""_w953_fix_file_line.py — 补齐 CHANGELOG W953 段「文件」行的缺项（重出批次与辅助脚本）

背景：cascade 的 FILE_LIST 更新后，因 W953 段已存在于 HEAD ⇒ cascade 幂等跳过 ⇒ 文件行仍是旧清单。
此处只补缺项（不重排整段）⇒ 工作树改完再按 HEAD 基底精确暂存。
"""
import io
import os
import subprocess
import sys

REPO = r"D:\xiyouji"
REL = "CHANGELOG.md"

MISSING = [
    "scripts/output/_w953_batch4.json", "scripts/output/_w953_batch5.json",
    "scripts/_w953_prep_raws2.py", "scripts/_w953_prep_raws3.py",
    "scripts/_w953_update_readme.py", "scripts/_w953_zoom.py",
    "scripts/_w953_fix_cascade.py", "scripts/_w953_backfill_stage.py",
    "assets/promo/plate-set/zoom-w953/w953-recheck.png",
]


def read_norm(p):
    raw = io.open(p, "rb").read()
    nl = "\r\n" if b"\r\n" in raw else "\n"
    return raw.decode("utf-8").replace("\r\n", "\n"), nl


def main():
    p = os.path.join(REPO, REL)
    t, nl = read_norm(p)
    # 定位 W953 段的「文件」行
    lines = t.split("\n")
    idx = None
    in_seg = False
    for i, ln in enumerate(lines):
        if ln.startswith("### W953（"):
            in_seg = True
            continue
        if in_seg and ln.startswith("> - **文件**："):
            idx = i
            break
        if in_seg and ln.startswith("### "):
            break
    if idx is None:
        print("FATAL 未找到 W953 段的文件行")
        return 2
    line = lines[idx]
    add = [f for f in MISSING if f not in line]
    if add:
        lines[idx] = line.rstrip() + "、" + "、".join(add)
    new_t = "\n".join(lines)
    io.open(p, "w", encoding="utf-8", newline="").write(new_t.replace("\n", nl))
    print("工作树文件行补齐 %d 项" % len(add))

    # 精确暂存（HEAD 基底 + 同样的替换）
    head = subprocess.run(["git", "show", "HEAD:" + REL], cwd=REPO,
                          capture_output=True).stdout.decode("utf-8")
    hlines = head.split("\n")
    hidx = None
    in_seg = False
    for i, ln in enumerate(hlines):
        if ln.startswith("### W953（"):
            in_seg = True
            continue
        if in_seg and ln.startswith("> - **文件**："):
            hidx = i
            break
        if in_seg and ln.startswith("### "):
            break
    if hidx is None:
        print("FATAL HEAD 里未找到 W953 段文件行")
        return 2
    hadd = [f for f in MISSING if f not in hlines[hidx]]
    if hadd:
        hlines[hidx] = hlines[hidx].rstrip() + "、" + "、".join(hadd)
    head_new = "\n".join(hlines)
    if head_new == head:
        print("HEAD 基底下无新增 → 跳过暂存")
        return 0
    blob = subprocess.run(["git", "hash-object", "-w", "--stdin"], cwd=REPO,
                          input=head_new.encode("utf-8"), capture_output=True)
    b = blob.stdout.decode().strip()
    r = subprocess.run(["git", "update-index", "--cacheinfo", "100644," + b + "," + REL],
                       cwd=REPO, capture_output=True)
    if r.returncode != 0:
        print("FATAL update-index: " + r.stderr.decode("utf-8", "replace")[:200])
        return 2
    print("精确暂存 %s（blob %s·补 %d 项）" % (REL, b[:8], len(hadd)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
