r"""check_cross_line_rewrite.py — 同族扫描：改写面正则的「跨行静默删内容」风险清单

病根（W1005 实证）：Python 字符类 `[^X]` **匹配换行符**、`\s` 亦然 ⇒ 若某条正则的匹配段写成
`[^X]*` 且**无紧跟的尾锚点**，其匹配区间可跨行；`re.sub` 替换的是**整个匹配区间** ⇒ 跨行匹配
等于静默删掉中间行的内容，且往往仍报「自检全通过」。

本扫描器（**报告型**·不改任何文件）分三档输出：
  🔴 改写面高危：调用 re.sub / re.subn 且模式含 `[^…]*`/`[^…]+` 且**无尾锚点**
  🟡 改写面可疑：模式含 `[^…]*` 但有尾锚点（锚点是否紧跟需人工确认）
  ⚪ 只读面：仅 search/findall/match（跨行只致 fail-closed 误报，不产生破坏）

「尾锚点」判定：同一模式串中，`[^…]*` 之后**紧邻**出现非字符类的字面量（`·`/`—`/中文/标点）
⇒ 视为有锚点（仍可能跨行吃到别处，标 🟡 供人工确认）。

扫描范围：scripts/ 全树（含 archive/scripts/ 归档区——归档件若被恢复使用会带病）。
用法：py -3 scripts/check_cross_line_rewrite.py [--json]
"""
from __future__ import annotations

import ast
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCAN_DIRS = [os.path.join(ROOT, "scripts")]
SKIP_DIR_PARTS = {"__pycache__", "node_modules", ".git", "tmpe"}

# 匹配段形如 [^X]* 或 [^X]+（X 非换行）
RE_NEGCLASS_STAR = re.compile(r"\[\^([^\]]+)\][*+]")
# 字面量锚点候选（非 \w 非空白的中日韩/标点/间隔号等）
RE_LITERAL_ANCHOR = re.compile(r"[·—、：:;；,，。「」『』《》【】（）()\[\]{}!?！？\"'`|/\\=><^~@#$%&*+=]")


def _pattern_of(node):
    """取 re.sub/search 的第一个参数（模式）。支持字符串常量与拼接。"""
    if node is None:
        return None
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        a = _pattern_of(node.left)
        b = _pattern_of(node.right)
        if a is not None and b is not None:
            return a + b
    if isinstance(node, ast.JoinedStr):
        return None      # f-string 模式 ⇒ 静态不可判 ⇒ 交人工
    return None


def _can_cross_line(pat):
    """模式里是否存在**可跨行**的 `[^X]*` 匹配段。

    关键判定：字符类的**排除符**里若含 `\\n` / `\\r`（转义形式），该类**不匹配换行** ⇒ 安全。
    ⇒ `[^\n]*` / `[^\r\n]*` **不会跨行**（首测把 `//[^\n]*` 误报为高危即源于此）。
    """
    for m in RE_NEGCLASS_STAR.finditer(pat):
        excl = m.group(1)
        if "\\n" in excl or "\\r" in excl:
            continue          # 该字符类排除换行 ⇒ 整条模式不跨行（就此段而言）
        return True
    return False


def _has_tail_anchor(pat):
    """`[^…]*` 之后是否紧跟字面量锚点（仅对可跨行的字符类有意义）。"""
    for m in RE_NEGCLASS_STAR.finditer(pat):
        excl = m.group(1)
        if "\\n" in excl or "\\r" in excl:
            continue
        tail = pat[m.end():]
        if tail and RE_LITERAL_ANCHOR.search(tail[:2]):
            return True
    return False


def scan():
    high, mid, low, skipped = [], [], [], []
    for base in SCAN_DIRS:
        for root, dirs, files in os.walk(base):
            dirs[:] = [d for d in dirs if d not in SKIP_DIR_PARTS]
            for fn in files:
                if not fn.endswith(".py"):
                    continue
                p = os.path.join(root, fn)
                rel = os.path.relpath(p, ROOT).replace("\\", "/")
                try:
                    src = open(p, encoding="utf-8").read()
                    tree = ast.parse(src)
                except Exception as e:  # noqa: BLE001
                    skipped.append((rel, "解析失败：%r" % (e,)))
                    continue
                for node in ast.walk(tree):
                    if not isinstance(node, ast.Call):
                        continue
                    fn_name = None
                    if isinstance(node.func, ast.Attribute):
                        fn_name = node.func.attr
                    elif isinstance(node.func, ast.Name):
                        fn_name = node.func.id
                    if fn_name not in ("sub", "subn", "search", "findall", "finditer", "match", "fullmatch"):
                        continue
                    if not node.args:
                        continue
                    pat = _pattern_of(node.args[0])
                    if pat is None:
                        continue
                    if not RE_NEGCLASS_STAR.search(pat):
                        continue
                    cross = _can_cross_line(pat)
                    item = {"file": rel, "line": node.lineno,
                            "func": fn_name, "pattern": pat[:160],
                            "cross": cross, "anchor": _has_tail_anchor(pat)}
                    if fn_name in ("sub", "subn"):
                        if not cross:
                            continue          # 排除符含 \n ⇒ 不跨行 ⇒ 安全
                        (mid if item["anchor"] else high).append(item)
                    else:
                        if not cross:
                            continue          # 只读面且不跨行 ⇒ 无需列
                        low.append(item)
    return high, mid, low, skipped


def _self_test():
    """4 例负样本自证（判据可证伪性）：高危必抓 · 三种安全形态必不报。"""
    cases = []

    def add(name, cond, detail=""):
        cases.append((name, bool(cond), detail))

    # ① 经典高危：`[^·]*` 无尾锚点 ⇒ 可跨行 ⇒ 必须判高危
    add("① 经典高危（`[^·]*` 无锚点）→ 判高危",
        _can_cross_line("[^·]*") and not _has_tail_anchor("[^·]*"),
        "cross=%s anchor=%s" % (_can_cross_line("[^·]*"), _has_tail_anchor("[^·]*")))
    # ② 排除符含 \n ⇒ 该字符类不跨行 ⇒ 必须不判高危（首测即把 `//[^\n]*` 误报为高危）
    add("② 排除符含 \\n（`[^\\n]*`）→ 不判高危",
        not _can_cross_line(r"//[^\n]*"),
        "cross=%s" % _can_cross_line(r"//[^\n]*"))
    # ③ 行锚定形态（W1005 修法）：`[^\n\r·]*·A1-A6` ⇒ 不跨行 ⇒ 必须不判高危
    add("③ 行锚定形态（`[^\\n\\r·]*·A1-A6`）→ 不判高危",
        not _can_cross_line(r"[^\n\r·]*·A1-A6"),
        "cross=%s" % _can_cross_line(r"[^\n\r·]*·A1-A6"))
    # ④ 有紧跟字面量锚点的可跨行形态 ⇒ 归「可疑」而非「高危」
    add("④ 可跨行但有紧跟锚点（`[^）]*）`）→ 归可疑非高危",
        _can_cross_line("（[^）]*）") and _has_tail_anchor("（[^）]*）"),
        "cross=%s anchor=%s" % (_can_cross_line("（[^）]*）"), _has_tail_anchor("（[^）]*）")))

    ok = True
    for name, passed, detail in cases:
        print("  %s %s%s" % ("PASS" if passed else "FAIL", name, ("  [%s]" % detail) if detail else ""))
        ok = ok and passed
    print("SELF_TEST_%s（%d/%d 例通过）" % ("OK" if ok else "FAIL", sum(1 for _, p, _ in cases if p), len(cases)))
    return 0 if ok else 1


def main() -> int:
    if "--self-test" in sys.argv:
        return _self_test()
    high, mid, low, skipped = scan()
    print("== 改写面高危（`[^…]*` 无尾锚点 ⇒ 匹配段可跨行 ⇒ re.sub 整段替换 = 静默删行）==")
    for it in high:
        print("  [RED ] %s:%d  re.%s  pattern=%r" % (it["file"], it["line"], it["func"], it["pattern"]))
    print("   共 %d 处" % len(high))
    print("\n== 改写面可疑（含 `[^…]*` 但有尾锚点·需人工确认锚点是否紧跟）==")
    for it in mid:
        print("  [YELL] %s:%d  re.%s  pattern=%r" % (it["file"], it["line"], it["func"], it["pattern"]))
    print("   共 %d 处" % len(mid))
    print("\n== 只读面（search/findall/match·跨行只致 fail-closed 误报·不产生破坏）==")
    for it in low:
        print("  [RO ] %s:%d  re.%s  pattern=%r" % (it["file"], it["line"], it["func"], it["pattern"]))
    print("   共 %d 处" % len(low))
    if skipped:
        print("\n== 跳过（解析失败）==")
        for rel, why in skipped:
            print("  [SKIP] %s · %s" % (rel, why))
    if "--json" in sys.argv:
        print(json.dumps({"high": high, "mid": mid, "low": low}, ensure_ascii=False, indent=1))

    # ---- 门禁模式：改写面高危必须为 0（W1005 修复后的常驻防线）----
    if "--gate" in sys.argv:
        if high:
            print("FAIL  改写面高危 %d 处（`[^…]*` 无尾锚点 ⇒ 匹配段可跨行 ⇒ re.sub 整段替换 = 静默删行）" % len(high))
            for it in high:
                print("  extra: %s:%d  re.%s  pattern=%r" % (it["file"], it["line"], it["func"], it["pattern"]))
            print("---- 跨行改写门禁：1 FAIL ----")
            return 1
        print("NOTE  改写面高危 0 处（可跨行但有紧跟锚点的可疑 %d 处·只读面 %d 处·不判红）" % (len(mid), len(low)))
        print("---- 跨行改写门禁：0 FAIL ----")
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
