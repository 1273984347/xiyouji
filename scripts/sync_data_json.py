#!/usr/bin/env python3
"""W678 WP-6.1：dataset 生成器输出 → site/data/json 部署副本 单向同步（清单制）。

三层断链根治（W640/方案 WP-6.1）：生成器 scripts/M_*/B_*/ → scripts/output/data/（生成器自写）
→ site/data/json/（此前手抄）。本脚本封最后一段：默认同步全部 47 副本，
--files 限名单副本；--dry 只报差异哈希不落盘。
"""
import argparse
import glob
import hashlib
import shutil


def sync(files=None, dry=False):
    outs = sorted(glob.glob("scripts/output/data/*.json"))
    pairs = []
    for o in outs:
        name = o.replace("\\", "/").rsplit("/", 1)[-1]
        dep = "site/data/json/" + name.replace("-", "_")
        pairs.append((o, dep))
    if files:
        want = {f.strip() for f in files.split(",")}
        pairs = [p for p in pairs if p[0].replace("\\", "/").rsplit("/", 1)[-1] in want]
    changed = 0
    for src, dep in pairs:
        try:
            a = open(src, "rb").read()
            b = open(dep, "rb").read()
        except FileNotFoundError:
            print("SKIP 部署副本不存在:", dep)
            continue
        if hashlib.sha256(a).hexdigest() != hashlib.sha256(b).hexdigest():
            changed += 1
            print(("DRY " if dry else "SYNC") + " %s -> %s" % (src, dep))
            if not dry:
                shutil.copyfile(src, dep)
    print("共 %d 对，差异 %d%s" % (len(pairs), changed, "（dry）" if dry else " 已同步"))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--files", default=None, help="逗号分隔的输出文件名白名单")
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    sync(a.files, a.dry)
