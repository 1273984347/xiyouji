# -*- coding: utf-8 -*-
"""_w1005_fix_c6.py — 修 C6：项目说明.md 两处版本行的 desc 含「·」

门禁 C6（`check_doc_sync.py`）：版本行 desc 不得含分隔符「·」——写入后会使**下一批**级联锚点正则失配
（W826 实证：三处全断·任何批都无法落段）。

现状：并行 W1004 批写的版本行 desc 里用了「·」分隔 ⇒ 1 项核心 FAIL（与本批资产面无关，
但会阻断后续所有批次的落段）⇒ 按「修实例必修根」替他修：把两处版本行（头部引用行 + 「当前版本」
列表行）里的「·」换成「、」（语义不变）。

⚠ W1005 批内修正（本脚本首版有缺陷·已实测并留证）：
  首版对**整行**无差别替换「·」→「、」，把**结构性尾缀**「·详细变更见」一并改掉
  ⇒ 级联正则 `[^·]*·详细变更见` 失配 ⇒ `batch_cascade` 断言「项目说明头部版本行未变化」
  ⇒ 级联无法落段（本批实际卡在这里两轮）。
  正确口径（`check_doc_sync.py` 的 `_check_c6_version_desc_seps` 已用 `tails` 元组实现）：
  **desc 内容**用「、」分隔；**结构性尾缀**（「·A1-A6」/「—A1-A6」/「·详细变更见」）必须原样保留。
  ⇒ 本脚本改为「尾缀白名单豁免」：只替换 desc 内容里的「·」，尾缀段不动。

用法：py -3 scripts/_w1005_fix_c6.py [--dry-run]
"""
import io
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(REPO, "docs", "00-导读", "项目说明.md")

# 结构性尾缀白名单（W1005 补）——这些「·」/「—」是级联锚点的必要组成，不是 desc 内容分隔符。
# 豁免它们 ⇒ 手改 desc 不会连带破坏下一批级联。
TAIL_TOKENS = ("·详细变更见", "·A1-A6", "—A1-A6")


def split_tail(line):
    """把版本行拆成 (head, tail)。tail 是首个命中的结构性尾缀（连同其前后缀），其余为 desc 内容。"""
    best = None
    for t in TAIL_TOKENS:
        i = line.find(t)
        if i != -1 and (best is None or i < best[0]):
            best = (i, t)
    if best is None:
        return line, ""
    i, t = best
    return line[:i], line[i:]


def main() -> int:
    dry = "--dry-run" in sys.argv
    t, n = read(P)
    lines = t.split("\n")
    ch = 0
    for i, ln in enumerate(lines):
        if ("当前批次 W" in ln or "**当前版本**" in ln) and "·" in ln:
            head, tail = split_tail(ln)
            new_head = head.replace("·", "、")
            if new_head == head:
                continue
            new = new_head + tail
            lines[i] = new
            ch += 1
            print("   %4d| %s" % (i + 1, new[:150]))
    if not ch:
        print("SKIP  未发现含「·」的版本行（尾缀白名单豁免后 desc 已干净）")
        return 0
    t = "\n".join(lines)
    if dry:
        print("DRY  将改 %d 行" % ch)
    else:
        write(P, t, n)
        print("OK   项目说明.md 版本行 desc「·」→「、」（%d 行·结构性尾缀豁免）" % ch)
    return 0


def read(p):
    raw = io.open(p, "rb").read()
    return raw.decode("utf-8"), ("\r\n" if b"\r\n" in raw else "\n")


def write(p, text, nl):
    tmp = p + ".tmp"
    io.open(tmp, "wb").write(text.encode("utf-8"))
    os.replace(tmp, p)


def main() -> int:
    dry = "--dry-run" in sys.argv
    t, n = read(P)
    lines = t.split("\n")
    ch = 0
    for i, ln in enumerate(lines):
        if ("当前批次 W" in ln or "**当前版本**" in ln) and "·" in ln:
            new = ln.replace("·", "、")
            lines[i] = new
            ch += 1
            print("   %4d| %s" % (i + 1, new[:150]))
    if not ch:
        print("SKIP  未发现含「·」的版本行")
        return 0
    t = "\n".join(lines)
    if dry:
        print("DRY  将改 %d 行" % ch)
    else:
        write(P, t, n)
        print("OK   项目说明.md 版本行 desc「·」→「、」（%d 行）" % ch)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
