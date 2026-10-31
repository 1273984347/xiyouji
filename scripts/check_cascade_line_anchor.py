#!/usr/bin/env python3
"""check_cascade_line_anchor.py — 级联三文档面「行锚定」不变量自证（跨批复用判据 · W1005 建）

为什么需要它（W1005 实证）：`batch_cascade._face_three_docs` 的项目说明「当前版本」列表行
正则用 `[^·]*`（**无尾锚点**）⇒ 旧 desc 行内无「·」时匹配区间跨行 ⇒ `re.sub` 替换的是整个
匹配区间 ⇒ 项目说明.md 103 行→102 行，第 49 行「当前阶段」行首被静默删掉，而级联
「写后自检全部通过」。反直觉点：旧 desc **含**「·」时反而安全（止于行内）；desc **无**「·」
（正是 C6 判据 W841 要求的形态）才触发吞并。

本判据**直接调用** `batch_cascade._face_three_docs`（不复制正则 ⇒ 判据与被测物同源，
不会随实现漂移而恒真），用**合成样本**驱动，断言两件事：

  ① 三个文档面替换后**行数不变**（行锚定不变量）；
  ② 合成样本确实能触发旧缺陷——复刻旧正则必须复现跨行吞行（**负样本有效性自证**）。
     否则「①恒真」就又是一个恒真的检查。

用法：py -3 scripts/check_cascade_line_anchor.py [--json]
退出码：0 = 全绿；1 = 有 FAIL。
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import batch_cascade as bc  # noqa: E402

# 合成样本：desc 一律**无「·」**（C6 W841 要求的形态）⇒ 旧正则必跨行；
# 且紧邻行含「·」⇒ 给旧正则一个可吞的终点。
FAKE = {
    "README.md": (
        "> **当前批次 W1004（2026-10-29）**：甲、乙、丙·A1-A6\n"
        "# 标题\n"
        "正文行\n"
    ),
    "STRUCTURE.md": (
        "> 当前批次：W1004（2026-10-29）— 甲、乙、丙—A1-A6\n"
        "# 标题\n"
        "正文行\n"
    ),
    "docs/00-导读/项目说明.md": (
        "> 当前批次 W1004（2026-10-29）：甲、乙、丙·详细变更见 CHANGELOG\n"
        "- **当前版本**：W1004（2026-10-29）— 甲、乙、丙\n"
        "- **当前阶段**：丙阶段内容·尾巴\n"
        "- **关键产出**：甲产出\n"
    ),
}

# 旧正则复刻（仅用于**证明样本有效**，不参与判定）——与 W1005 修复前的实现逐字一致。
OLD_LIST_LINE = re.compile(
    r"(\*\*当前(?:版本|批次)\*\*：)(?:v[\d.]+|W\d+)（[^）]*）— (?:v[\d.]+\s+)?(?:W\d+\s+)?[^·]*"
)


class _Ctx:
    """batch_cascade._Ctx 的最小替身（只带 _face_three_docs 用到的字段）。"""

    def __init__(self, batch, date, desc):
        self.batch, self.date, self.desc = batch, date, desc
        self.pend = []


def _run():
    """跑被测实现（monkeypatch load 指向合成样本）⇒ 返回 {path: new_text}。"""
    orig_load = bc.load
    bc.load = lambda path: (FAKE[path], "\n")
    try:
        ctx = _Ctx("W1005", "2026-10-29", "丁、戊、己")
        bc._face_three_docs(ctx)
    finally:
        bc.load = orig_load
    return {p: t for p, t, _nl in ctx.pend}


def check():
    issues, notes = [], []
    out = _run()

    # ① 行锚定不变量：三个面替换后行数不变
    for path, src in FAKE.items():
        if path not in out:
            issues.append("行锚定：%s 未产出改写结果（被测实现未命中该面）" % path)
            continue
        if out[path].count("\n") != src.count("\n"):
            issues.append("行锚定：%s 替换后行数 %d → %d（跨行吞并复发）"
                          % (path, src.count("\n"), out[path].count("\n")))
        else:
            notes.append("行锚定：%s 行数不变（%d）" % (path, src.count("\n")))

    # ①-2 关键内容完好：紧邻行首不得被吞
    proj = out.get("docs/00-导读/项目说明.md", "")
    for must in ("- **当前阶段**：丙阶段内容·尾巴", "- **关键产出**：甲产出"):
        if must not in proj:
            issues.append("行锚定：项目说明.md 丢失内容「%s」（跨行吞并复发）" % must)
    if "- **当前版本**：W1005（2026-10-29）— 丁、戊、己" not in proj:
        issues.append("行锚定：项目说明.md「当前版本」列表行未更新为当批（新旧 desc 混写）")
    if not proj.startswith("> 当前批次 W1005（2026-10-29）：丁、戊、己·详细变更见 CHANGELOG"):
        issues.append("行锚定：项目说明.md 头部版本行未更新或结构性尾缀被破坏")
    if not out.get("README.md", "").startswith(
            "> **当前批次 W1005（2026-10-29）**：丁、戊、己·A1-A6"):
        issues.append("行锚定：README.md 版本行未更新或结构性尾缀被破坏")
    if not out.get("STRUCTURE.md", "").startswith(
            "> 当前批次：W1005（2026-10-29）— 丁、戊、己—A1-A6"):
        issues.append("行锚定：STRUCTURE.md 版本行未更新或结构性尾缀被破坏")

    # ② 负样本有效性自证：复刻的旧正则必须复现跨行吞行（否则 ① 恒真）
    src = FAKE["docs/00-导读/项目说明.md"]
    m = OLD_LIST_LINE.search(src)
    if not m or "\n" not in m.group(0):
        issues.append("负样本无效：旧正则未在合成样本上复现跨行匹配（样本已不能触发旧缺陷）")
    else:
        after = OLD_LIST_LINE.sub(r"\g<1>替换", src, count=1)
        if after.count("\n") >= src.count("\n"):
            issues.append("负样本无效：旧正则未复现吞行（行数未减少）")
        else:
            notes.append("负样本有效：旧正则跨行匹配 %d 字符·吞行 %d 行（⇒ ① 的行数断言非恒真）"
                         % (len(m.group(0)), src.count("\n") - after.count("\n")))

    return notes, issues


def main():
    notes, issues = check()
    for n in notes:
        print("[NOTE] " + n)
    for i in issues:
        print("FAIL  " + i)
    if "--json" in sys.argv:
        print(json.dumps({"notes": notes, "issues": issues}, ensure_ascii=False, indent=2))
    print("---- 级联行锚定判据：%d FAIL · %d NOTE ----" % (len(issues), len(notes)))
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
