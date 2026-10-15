#!/usr/bin/env python3
"""W504 一次性工具：向学术轨文档头部插入原著引文行并预校验。

用法：
  python scripts/_w504_insert_cites.py <md文件> <spec.json>
spec.json 格式：[[回目号, 引文句体], ...]
行为：
  1. 对 dataset/text-search.json 归一后校验每条句体为对应回目 text 子串，任一失败即中止不写文件；
  2. 在文件头部 "> 引用：" 行紧后面插入 `> 原文引文（第N回）："句体"` 行（全角引号）；
  3. 若文件已含 "> 原文引文" 行则中止（防重复插入）。
"""
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEXT_SEARCH = os.path.join(ROOT, "dataset", "text-search.json")


def norm(s):
    return re.sub(r"\s+", "", s)


def main():
    md, spec_path = sys.argv[1], sys.argv[2]
    spec = json.load(open(spec_path, encoding="utf-8"))
    chapters = {}
    d = json.load(open(TEXT_SEARCH, encoding="utf-8"))
    for c in d["chapters"]:
        chapters[int(c["num"])] = norm(c["text"])

    for num, body in spec:
        if norm(body) not in chapters[int(num)]:
            print("ABORT 第%d回未命中：%s" % (num, body[:30]))
            sys.exit(1)

    text = io.open(md, encoding="utf-8").read()
    if "> 原文引文" in text:
        print("ABORT 文件已含引文行")
        sys.exit(1)
    lines = text.split("\n")
    idx = None
    for i, ln in enumerate(lines):
        if ln.strip().startswith("> 引用："):
            idx = i
            break
    if idx is None:
        print("ABORT 未找到 > 引用：行")
        sys.exit(1)
    ins = []
    for num, body in spec:
        ins.append("> 原文引文（第%d回）：\u201c%s\u201d" % (int(num), body))
    lines[idx + 1:idx + 1] = ins
    io.open(md, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
    print("INSERTED %d 条" % len(ins))


if __name__ == "__main__":
    main()
