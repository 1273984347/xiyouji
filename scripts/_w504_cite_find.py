#!/usr/bin/env python3
"""W504 一次性辅助：在 dataset/text-search.json 中按关键词检索原著句子候选。

用法：
  python scripts/_w504_cite_find.py --kw 白骨精 三打 --top 8
  python scripts/_w504_cite_find.py --kw 心猿 --ch 14 --top 5     # 限定回目
输出：每行 `第N回 | 句子`。句子按 。！？； 切分，候选须全部包含给定关键词（或关系用 --any）。
"""
import argparse
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SENT_SPLIT = re.compile(r"(?<=[。！？；])")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kw", required=True, help="关键词，空格分隔多个")
    ap.add_argument("--ch", type=int, help="限定回目（1-100）")
    ap.add_argument("--top", type=int, default=8)
    ap.add_argument("--any", action="store_true", help="任一关键词命中即输出（默认须全含）")
    args = ap.parse_args()

    kws = [k for k in args.kw.split() if k]
    d = json.load(open(os.path.join(ROOT, "dataset", "text-search.json"), encoding="utf-8"))
    hits = []
    for c in d["chapters"]:
        num = int(c["num"])
        if args.ch and num != args.ch:
            continue
        for sent in SENT_SPLIT.split(c["text"]):
            s = sent.strip()
            if len(s) < 6 or len(s) > 120:
                continue
            ok = (any(k in s for k in kws)) if getattr(args, "any") else all(k in s for k in kws)
            if ok:
                hits.append((num, s))
    for num, s in hits[: args.top]:
        print("第%d回 | %s" % (num, s))
    if not hits:
        print("（无命中）")


if __name__ == "__main__":
    main()
