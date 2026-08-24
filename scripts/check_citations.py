#!/usr/bin/env python3
"""原著引文硬验证（W503 第 20 门禁）：`> 原文引文（第N回）：“……”` 行必须精确命中原著。

引文语法（文档规范 §4.8）：
    > 原文引文（第N回）：“……”
- N ∈ 1-100；引号全角；引文单行，必须是 dataset/text-search.json chapters[N-1].text 的子串。
- 归一规则：比较前双方去除全部空白（re.sub(r'\\s+','')，兼容原文换行）；除此之外逐字精确。
- 禁止省略号节引——需节引时拆成多条引文行；每条引文独立命中。
- 任何文档中任一引文行未命中 = FAIL（存量锚定引文行实测为 0，无历史豁免）。

用法：
  python scripts/check_citations.py --file <md>   # 单文件
  python scripts/check_citations.py --dir docs/   # 目录全量（门禁模式用）
"""
import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEXT_SEARCH = os.path.join(ROOT, "dataset", "text-search.json")
CITE_RE = re.compile(r"^> 原文引文（第(\d+)回）：(.*)$")


def norm(s):
    return re.sub(r"\s+", "", s)


def load_chapters():
    d = json.load(open(TEXT_SEARCH, encoding="utf-8"))
    chs = {}
    for c in d["chapters"]:
        chs[int(c["num"])] = norm(c["text"])
    return chs


def check_text(text, chapters):
    """返回 (总条数, 失败清单[(行号, 原因)])。"""
    total, fails = 0, []
    for i, ln in enumerate(text.splitlines(), 1):
        m = CITE_RE.match(ln.strip())
        if not m:
            continue
        total += 1
        num = int(m.group(1))
        quote = m.group(2).strip()
        if not (quote.startswith("“") and quote.endswith("”") and len(quote) >= 2):
            fails.append((i, "引文未用全角引号“…”包裹"))
            continue
        body = norm(quote[1:-1])
        if not body:
            fails.append((i, "引文为空"))
            continue
        if num not in chapters:
            fails.append((i, "回目 %d 超出 1-100" % num))
            continue
        if body not in chapters[num]:
            fails.append((i, "第%d回未命中（非原文精确子串）" % num))
    return total, fails


def iter_md(base):
    for r, _, fns in os.walk(base):
        for fn in sorted(fns):
            if fn.endswith(".md"):
                yield os.path.join(r, fn)


def rel_or_abs(p):
    try:
        return os.path.relpath(p, ROOT).replace(os.sep, "/")
    except ValueError:
        return p.replace(os.sep, "/")


def main():
    ap = argparse.ArgumentParser(description="原著引文硬验证（W503）")
    ap.add_argument("--file", help="单文件模式")
    ap.add_argument("--dir", help="目录模式（递归扫全部 .md）")
    args = ap.parse_args()
    if not args.file and not args.dir:
        ap.error("需要 --file 或 --dir")

    chapters = load_chapters()
    files = [args.file] if args.file else list(iter_md(args.dir))

    g_total, g_fail_files = 0, 0
    for p in files:
        try:
            text = open(p, encoding="utf-8").read()
        except Exception as e:
            print("FAIL %s: 读取失败 %s" % (p, e))
            g_fail_files += 1
            continue
        total, fails = check_text(text, chapters)
        g_total += total
        if fails:
            g_fail_files += 1
            rel = rel_or_abs(p)
            for ln_no, why in fails[:5]:
                print("FAIL %s:%d %s" % (rel, ln_no, why))

    if g_fail_files:
        print("引文核验：共 %d 条引文行 · %d 个文件存在未命中/格式错误" % (g_total, g_fail_files))
        return 1
    print("引文核验通过：共 %d 条引文行 · 命中率 100%%（%d 个文件扫描）" % (g_total, len(files)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
