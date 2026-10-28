# -*- coding: utf-8 -*-
"""_w1005_fix_tail_sep.py — F2：恢复项目说明.md 头部版本行的**结构性尾缀**分隔符「·」

背景（W1005 根因链的一环）：
  C6 判据（`check_doc_sync.py` W841）要求版本行 desc **内容**禁含「·」/「—」——
  但它的实现（`_check_c6_version_desc_seps`）已用 `tails` 元组把**结构性尾缀**
  （`·A1-A6` / `—A1-A6` / `·详细变更见`）从 desc 段里截掉后再检查。
  ⇒ 正确口径是：**desc 内容用「、」，结构性尾缀必须保留「·」/「—」**。

  本批的 `_w1005_fix_c6.py` 手工修 C6 时对**整行**无差别替换「·」→「、」，
  把结构性尾缀「·详细变更见」一并改成「、详细变更见」⇒ 级联正则
  `[^·]*·详细变更见` 失配 ⇒ `batch_cascade` 断言「项目说明头部版本行未变化」⇒ 级联无法落段。

实证（历史形态回看）：
  29927caa（W1002 批后）行6 尾部 = 「…·详细变更见」  ← 结构尾缀用「·」·级联所写
  1ff008c3（W1004 批后）行6 尾部 = 「…·教训入库·详细变更见 CHANGELOG」 ← desc 内容「·」+ 结构尾缀「·」并存
  HEAD（W1005 修 C6 后）  行6 尾部 = 「…、教训入库、详细变更见 CHANGELOG」 ← 结构尾缀被误改·失配

本脚本只做一件事：把行6 的「、详细变更见 CHANGELOG」恢复为「·详细变更见 CHANGELOG」。
不碰 desc 内容（其「、」是 C6 要求的合法形态）。

用法：py -3 scripts/_w1005_fix_tail_sep.py [--dry-run]
"""
import io
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(REPO, "docs", "00-导读", "项目说明.md")

OLD_TAIL = "、详细变更见 CHANGELOG"
NEW_TAIL = "·详细变更见 CHANGELOG"


def main() -> int:
    dry = "--dry-run" in sys.argv
    raw = io.open(P, "rb").read()
    text = raw.decode("utf-8")
    nl = "\r\n" if b"\r\n" in raw else "\n"

    # 锚点唯一性断言：防误伤其它行（fail-closed）
    n = text.count(OLD_TAIL)
    assert n == 1, "锚点「%s」命中 %d 次（应恰为 1·项目说明.md 头部版本行）" % (OLD_TAIL, n)
    assert NEW_TAIL not in text, "目标尾缀「%s」已存在——无需修复（幂等）" % NEW_TAIL

    # 只在「当前批次」版本行内替换
    out = text.replace(OLD_TAIL, NEW_TAIL, 1)
    assert out != text

    for i, l in enumerate(out.split("\n"), 1):
        if "当前批次 W" in l:
            print("   %4d| %s" % (i, l[:190]))

    if dry:
        print("DRY  将恢复 1 处结构性尾缀分隔符")
        return 0

    # 原子替换（临时文件 + os.replace）——中途失败原文件毫发无损
    tmp = P + ".tmp"
    io.open(tmp, "wb").write(out.encode("utf-8"))
    os.replace(tmp, P)

    # 写后自检：行尾不变 + 无 CRCRLF + 行数不变
    raw2 = io.open(P, "rb").read()
    assert raw2.count(b"\r\r\n") == 0, "写后 CRCRLF 计数 ≠ 0（行尾污染）"
    assert raw2.count(b"\n") == raw.count(b"\n"), "写后行数变化（%d→%d）" % (
        raw.count(b"\n"), raw2.count(b"\n"))
    assert ("\r\n" in raw.decode("utf-8")) == ("\r\n" in raw2.decode("utf-8")), "写后行尾风格改变"
    print("OK   项目说明.md 结构性尾缀「、详细变更见」→「·详细变更见」（1 处·行尾与行数不变）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
