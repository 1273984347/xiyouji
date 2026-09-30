#!/usr/bin/env python3
"""原著引文硬验证（W503 第 20 门禁）：`> 原文引文（第N回）：“……”` 行必须精确命中原著。

引文语法（文档规范 §4.8）：
    > 原文引文（第N回）：“……”
- N ∈ 1-100；引号全角；引文单行，必须是 dataset/text-search.json chapters[N-1].text 的子串。
- 归一规则：比较前双方去除全部空白（re.sub(r'\\s+','')，兼容原文换行）；除此之外逐字精确。
- 禁止省略号节引——需节引时拆成多条引文行；每条引文独立命中。
- 任何文档中任一引文行未命中 = FAIL（存量锚定引文行实测为 0，无历史豁免）。
- 防静默跳过（2026-09-27 A 轨审查 ISSUE-001 加固）：凡以「原文引文」起始、却未匹配
  规范语法（`> 原文引文（第N回）：`）的行，一律 FAIL——堵死"格式漂移整行不进分母、
  报 100% 实为空真"的盲区（实证：匿名稿 3 条引文行因回目号带空格+半角引号曾长期被跳过）。
  疑似判定容忍常见漂移前缀：`>原文引文`、`> **原文引文` 等（2026-09-27 二档加固）。
- 自检（2026-09-27 加固）：`--self-test` 以内存正负样本 4 例验证判定行为，防规则回归。

用法：
  python scripts/check_citations.py --file <md>   # 单文件
  python scripts/check_citations.py --dir docs/   # 目录全量（门禁模式用）
  python scripts/check_citations.py --self-test   # 自检（不依赖外部文档）
"""
import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEXT_SEARCH = os.path.join(ROOT, "dataset", "text-search.json")
CITE_RE = re.compile(r"^> 原文引文（第(\d+)回）：(.*)$")
SUSPECT_RE = re.compile(r"^>?\s*(?:\*\*)?\s*原文引文")


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
            # 防静默跳过（2026-09-27 加固）：疑似引文行但语法漂移 → 直接判 FAIL
            if SUSPECT_RE.match(ln.strip()):
                fails.append((i, "疑似引文行未采用规范语法（`> 原文引文（第N回）：` 全角引号·回目号无空格），将不进核验分母"))
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


DQ = chr(34)
SELF_TEST_CASES = [
    (True, "> 原文引文（第1回）：“混沌未分天地乱”", "正样本·规范语法"),
    (False, "> 原文引文（第 1 回）：“混沌未分天地乱”", "负样本·回目号带空格（曾致静默跳过）"),
    (False, "> 原文引文（第1回）：" + DQ + "混沌未分天地乱" + DQ, "负样本·半角引号"),
    (False, "> **原文引文（第1回）：“混沌未分天地乱”", "负样本·粗体前缀漂移"),
]


def self_test(chapters):
    bad = 0
    for expect_pass, line, label in SELF_TEST_CASES:
        total, fails = check_text(line + "\n", chapters)
        passed = (len(fails) == 0) and (total == 1)
        if passed != expect_pass:
            print("FAIL self-test：%s（期望 %s，实得 total=%d / fails=%d）"
                  % (label, "通过" if expect_pass else "失败", total, len(fails)))
            bad += 1
    print("self-test %s：%d/%d" % ("通过" if not bad else "失败",
                                    len(SELF_TEST_CASES) - bad, len(SELF_TEST_CASES)))
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser(description="原著引文硬验证（W503）")
    ap.add_argument("--file", help="单文件模式")
    ap.add_argument("--dir", help="目录模式（递归扫全部 .md）")
    ap.add_argument("--self-test", action="store_true", help="自检（内存正负样本，不依赖外部文档）")
    args = ap.parse_args()

    chapters = load_chapters()

    if args.self_test:
        return self_test(chapters)

    if not args.file and not args.dir:
        ap.error("需要 --file 或 --dir（或 --self-test）")
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
