#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_fix_oob_fetch.py — W563/A-3：治理越界 fetch（部署根=site/，../../scripts/* 必 404）。

α 类机械处理（本脚本）：目标 JSON 全部存在于 scripts/output/data/ 的页面——
  把前缀字面量改写为站内部径并复制 JSON 副本到 site/data/json/：
    site/data/*.html   ../../scripts/output/data/  ->  json/
    site/en/*.html     ../../scripts/output/data/  ->  ../data/json/
    site/*.html(根)    ../scripts/output/data/     ->  ./data/json/
显式跳过（转手工，方案档 §A-3 β/γ-1/γ-2）：
  - 文件名含 chapter-stats（β：内联 EMBEDDED_DATA）
  - 任一目标 JSON 磁盘缺失（γ：semiotics 删 fetch / character-appearance 清字面量）

行尾 CRLF 原样保留（newline='' 读写，纯子串替换不动行尾）。
用法：python scripts/_fix_oob_fetch.py          # 预演
      python scripts/_fix_oob_fetch.py --apply  # 落盘 + 复制副本
"""
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
SRC_DATA = os.path.join(ROOT, "scripts", "output", "data")
DST_JSON = os.path.join(SITE, "data", "json")

LIT_RE = re.compile(r"(?:\.\./)+scripts/output/data/")
FILE_RE = re.compile(r"(?:\.\./)+scripts/output/data/([\w.-]+)")


def rules_for(p):
    rel = os.path.relpath(p, SITE).replace(os.sep, "/")
    if rel.startswith("data/"):
        return "../../scripts/output/data/", "json/"
    if rel.startswith("en/"):
        return "../../scripts/output/data/", "../data/json/"
    return "../scripts/output/data/", "./data/json/"


def main():
    apply = "--apply" in sys.argv
    os.makedirs(DST_JSON, exist_ok=True)
    n_alpha = 0
    manual = []
    copied = set()
    for dirpath, _, files in os.walk(SITE):
        if any(seg.startswith(".") for seg in dirpath.split(os.sep)):
            continue
        for fn in sorted(files):
            if not fn.endswith(".html"):
                continue
            p = os.path.join(dirpath, fn)
            with open(p, encoding="utf-8", newline="", errors="ignore") as f:
                s = f.read()
            if "scripts/output/data/" not in s:
                continue
            targets = sorted(set(FILE_RE.findall(s)))
            missing = [t for t in targets if not os.path.exists(os.path.join(SRC_DATA, t))]
            rel = os.path.relpath(p, ROOT)
            if "chapter-stats" in fn:
                manual.append((rel, "beta: targets=%s missing=%s" % (targets, missing)))
                continue
            if missing:
                manual.append((rel, "gamma: missing=%s" % missing))
                continue
            old_prefix, new_prefix = rules_for(p)
            # 两步替换：先带 ../ 前缀的形态（fetch/baseUrl 代码），再裸形态
            # （W463 数据源徽标 <code>…</code>、JS 注释、说明文字——统一后语义仍准确）
            n_occ = s.count(old_prefix) + s.replace(old_prefix, "").count("scripts/output/data/")
            if apply:
                s2 = s.replace(old_prefix, new_prefix)
                s2 = s2.replace("scripts/output/data/", new_prefix)
                with open(p, "w", encoding="utf-8", newline="") as f:
                    f.write(s2)
                for t in targets:
                    src = os.path.join(SRC_DATA, t)
                    dst = os.path.join(DST_JSON, t)
                    if t not in copied:
                        shutil.copyfile(src, dst)
                        copied.add(t)
            n_alpha += 1
            print(("APPLY " if apply else "DRY   ") + rel + "  prefix×%d targets=%d" % (n_occ, len(targets)))
    print("---")
    print(f"α 类处理 {n_alpha} 页 · 复制副本 {len(copied)} 个 · 转手工 {len(manual)} 页")
    for rel, why in manual:
        print("  MANUAL", rel, "->", why)


if __name__ == "__main__":
    main()
